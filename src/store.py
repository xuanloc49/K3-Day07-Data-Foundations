from __future__ import annotations

from typing import Any, Callable

from .chunking import _dot
from .embeddings import _mock_embed
from .models import Document


class EmbeddingStore:
    """
    A vector store for text chunks.

    Tries to use ChromaDB if available; falls back to an in-memory store.
    The embedding_fn parameter allows injection of mock embeddings for tests.
    """

    def __init__(
        self,
        collection_name: str = "documents",
        embedding_fn: Callable[[str], list[float]] | None = None,
    ) -> None:
        self._embedding_fn = embedding_fn or _mock_embed
        self._collection_name = collection_name
        self._use_chroma = False
        self._store: list[dict[str, Any]] = []
        self._collection = None
        self._next_index = 0

        try:
            import chromadb

            client = chromadb.Client()
            self._collection = client.get_or_create_collection(name=collection_name)
            self._use_chroma = True
        except Exception:
            self._use_chroma = False
            self._collection = None

    def _make_record(self, doc: Document) -> dict[str, Any]:
        metadata = dict(doc.metadata)
        metadata.setdefault(
            "doc_id",
            doc.id.split("::")[0] if "::" in doc.id else doc.id,
        )
        return {
            "id": f"{doc.id}-{self._next_index}",
            "content": doc.content,
            "embedding": self._embedding_fn(doc.content),
            "metadata": metadata,
        }

    def _make_result(self, record: dict[str, Any], score: float) -> dict[str, Any]:
        return {
            "id": record["id"],
            "content": record["content"],
            "metadata": dict(record.get("metadata", {})),
            "score": score,
        }

    def _search_records(self, query: str, records: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
        query_vector = self._embedding_fn(query)
        scored = [
            self._make_result(record, _dot(query_vector, record["embedding"]))
            for record in records
        ]
        return sorted(scored, key=lambda item: item["score"], reverse=True)[:top_k]

    def add_documents(self, docs: list[Document]) -> None:
        """
        Embed each document's content and store it.

        For ChromaDB: use collection.add(ids=[...], documents=[...], embeddings=[...])
        For in-memory: append dicts to self._store
        """
        if not docs:
            return

        if self._use_chroma and self._collection is not None:
            ids: list[str] = []
            documents: list[str] = []
            embeddings: list[list[float]] = []
            metadatas: list[dict[str, Any]] = []
            for doc in docs:
                record = self._make_record(doc)
                ids.append(record["id"])
                documents.append(record["content"])
                embeddings.append(record["embedding"])
                metadatas.append(record["metadata"])
                self._next_index += 1
            self._collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
            )
            return

        for doc in docs:
            self._store.append(self._make_record(doc))
            self._next_index += 1

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """
        Find the top_k most similar documents to query.

        For in-memory: compute dot product of query embedding vs all stored embeddings.
        """
        if self._use_chroma and self._collection is not None:
            query_embedding = self._embedding_fn(query)
            response = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=min(top_k, max(self.get_collection_size(), 1)),
            )
            results: list[dict[str, Any]] = []
            ids = response.get("ids", [[]])[0]
            documents = response.get("documents", [[]])[0]
            metadatas = response.get("metadatas", [[]])[0]
            distances = response.get("distances", [[]])[0]
            for record_id, content, metadata, distance in zip(ids, documents, metadatas, distances):
                results.append(
                    {
                        "id": record_id,
                        "content": content,
                        "metadata": metadata or {},
                        "score": 1.0 - distance,
                    }
                )
            return sorted(results, key=lambda item: item["score"], reverse=True)[:top_k]

        return self._search_records(query, self._store, top_k)

    def get_collection_size(self) -> int:
        """Return the total number of stored chunks."""
        if self._use_chroma and self._collection is not None:
            return self._collection.count()
        return len(self._store)

    def _filter_records(self, metadata_filter: dict) -> list[dict[str, Any]]:
        return [
            record
            for record in self._store
            if all(record.get("metadata", {}).get(key) == value for key, value in metadata_filter.items())
        ]

    def search_with_filter(self, query: str, top_k: int = 3, metadata_filter: dict = None) -> list[dict]:
        """
        Search with optional metadata pre-filtering.

        Filter first, rank second: only records matching every key/value pair
        are scored; then _search_records ranks the filtered set.
        """
        if metadata_filter is None:
            return self.search(query, top_k=top_k)

        return self._search_records(query, self._filter_records(metadata_filter), top_k)

    def delete_document(self, doc_id: str) -> bool:
        """
        Remove all chunks belonging to a document.

        Returns True if any chunks were removed, False otherwise.
        """
        def belongs_to_doc(record: dict[str, Any]) -> bool:
            return record.get("metadata", {}).get("doc_id") == doc_id

        if self._use_chroma and self._collection is not None:
            existing = self._collection.get()
            ids_to_delete = []
            for record_id, metadata in zip(existing.get("ids", []), existing.get("metadatas", [])):
                metadata = metadata or {}
                if metadata.get("doc_id") == doc_id:
                    ids_to_delete.append(record_id)
            if not ids_to_delete:
                return False
            self._collection.delete(ids=ids_to_delete)
            return True

        before = len(self._store)
        self._store = [record for record in self._store if not belongs_to_doc(record)]
        return len(self._store) < before
