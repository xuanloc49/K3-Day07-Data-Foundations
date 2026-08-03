from typing import Callable

from .store import EmbeddingStore


class KnowledgeBaseAgent:
    """
    An agent that answers questions using a vector knowledge base.

    Retrieval-augmented generation (RAG) pattern:
        1. Retrieve top-k relevant chunks from the store.
        2. Build a prompt with the chunks as context.
        3. Call the LLM to generate an answer.
    """

    def __init__(self, store: EmbeddingStore, llm_fn: Callable[[str], str]) -> None:
        self.store = store
        self.llm_fn = llm_fn

    def answer(self, question: str, top_k: int = 3) -> str:
        results = self.store.search(question, top_k=top_k)
        if not results:
            return "No relevant context found in the knowledge base."

        context_blocks: list[str] = []
        for index, result in enumerate(results, start=1):
            metadata = result.get("metadata", {})
            doc_id = metadata.get("doc_id") or metadata.get("source") or "unknown"
            context_blocks.append(f"[{index}] (doc_id: {doc_id}) {result['content']}")

        prompt = (
            "Instruction: Answer using only the context below. "
            "If the context is insufficient, say clearly that you do not know.\n\n"
            f"Context:\n{chr(10).join(context_blocks)}\n\n"
            f"Question: {question}\n\n"
            "Answer:"
        )
        return self.llm_fn(prompt)
