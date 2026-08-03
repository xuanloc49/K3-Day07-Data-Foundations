from __future__ import annotations

import math
import re


class FixedSizeChunker:
    """
    Split text into fixed-size chunks with optional overlap.

    Rules:
        - Each chunk is at most chunk_size characters long.
        - Consecutive chunks share overlap characters.
        - The last chunk contains whatever remains.
        - If text is shorter than chunk_size, return [text].
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 50) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []
        if len(text) <= self.chunk_size:
            return [text]

        step = self.chunk_size - self.overlap
        chunks: list[str] = []
        for start in range(0, len(text), step):
            chunk = text[start : start + self.chunk_size]
            chunks.append(chunk)
            if start + self.chunk_size >= len(text):
                break
        return chunks


_SENTENCE_PATTERN = r"(?<=[.!?])\s+"


class SentenceChunker:
    """
    Split text into chunks of at most max_sentences_per_chunk sentences.

    Sentence detection: split on ". ", "! ", "? " or ".\n".
    Strip extra whitespace from each chunk.
    """

    def __init__(self, max_sentences_per_chunk: int = 3) -> None:
        self.max_sentences_per_chunk = max(1, max_sentences_per_chunk)

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []

        limit = self.max_sentences_per_chunk
        sentences = [sentence.strip() for sentence in re.split(_SENTENCE_PATTERN, text) if sentence.strip()]
        return [" ".join(sentences[index : index + limit]) for index in range(0, len(sentences), limit)]


class RecursiveChunker:
    """
    Recursively split text using separators in priority order.

    Default separator priority:
        ["\n\n", "\n", ". ", " ", ""]
    """

    DEFAULT_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]

    def __init__(self, separators: list[str] | None = None, chunk_size: int = 500) -> None:
        self.separators = self.DEFAULT_SEPARATORS if separators is None else list(separators)
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []
        chunks = self._split(text, self.separators)
        return [chunk.strip() for chunk in chunks if chunk.strip()]

    def _fixed_size_chunks(self, text: str) -> list[str]:
        return FixedSizeChunker(chunk_size=self.chunk_size, overlap=0).chunk(text)

    def _split(self, current_text: str, remaining_separators: list[str]) -> list[str]:
        text = current_text.strip()
        if not text:
            return []

        # Base case 1: đủ ngắn
        if len(text) <= self.chunk_size:
            return [text]

        # Base case 2: hết separator hoặc separator rỗng → cắt cố định
        if not remaining_separators or remaining_separators[0] == "":
            return self._fixed_size_chunks(text)

        separator = remaining_separators[0]
        next_separators = remaining_separators[1:]

        # Separator hiện tại không có trong text → thử separator kế tiếp
        if separator not in text:
            return self._split(text, next_separators)

        splits = text.split(separator)
        chunks: list[str] = []
        merged_parts: list[str] = []

        def flush_merged() -> None:
            if not merged_parts:
                return
            merged = separator.join(merged_parts).strip()
            if merged:
                chunks.append(merged)
            merged_parts.clear()

        for index, piece in enumerate(splits):
            part = piece if index == 0 else separator + piece
            candidate = separator.join(merged_parts) + part if merged_parts else part

            if not merged_parts or len(candidate) <= self.chunk_size:
                merged_parts.append(part)
                continue

            flush_merged()
            if len(part) <= self.chunk_size:
                merged_parts.append(part)
            else:
                chunks.extend(self._split(part, next_separators))

        flush_merged()
        return chunks


def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def compute_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    cosine_similarity = dot(a, b) / (||a|| * ||b||)

    Returns 0.0 if either vector has zero magnitude.
    """
    norm_a = math.sqrt(_dot(vec_a, vec_a))
    norm_b = math.sqrt(_dot(vec_b, vec_b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return _dot(vec_a, vec_b) / (norm_a * norm_b)


class ChunkingStrategyComparator:
    """Run all built-in chunking strategies and compare their results."""

    def compare(self, text: str, chunk_size: int = 200) -> dict:
        strategies = {
            "fixed_size": FixedSizeChunker(chunk_size=chunk_size, overlap=0),
            "by_sentences": SentenceChunker(max_sentences_per_chunk=3),
            "recursive": RecursiveChunker(chunk_size=chunk_size),
        }
        result: dict[str, dict] = {}
        for name, chunker in strategies.items():
            chunks = chunker.chunk(text)
            count = len(chunks)
            avg_length = (sum(len(chunk) for chunk in chunks) / count) if count else 0.0
            result[name] = {
                "count": count,
                "avg_length": avg_length,
                "chunks": chunks,
            }
        return result
