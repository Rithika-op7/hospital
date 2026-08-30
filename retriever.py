import json
import faiss
import numpy as np

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from sentence_transformers import SentenceTransformer, CrossEncoder
from config import (
    EMBEDDING_MODEL,
    RERANKER_MODEL,
    RRF_K
)

class HybridRetriever:

    def __init__(
        self,
        index_path="data/faiss_index/index.faiss",
        metadata_path="data/faiss_index/metadata.json",
        embedding_model=EMBEDDING_MODEL
    ):

        # Load chunks
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        # Load FAISS
        self.index = faiss.read_index(index_path)

        # Load embedding model
        self.model = SentenceTransformer(embedding_model)

        self.reranker = CrossEncoder(RERANKER_MODEL)

        # Prepare BM25 corpus
        self.texts = [
            chunk["page_content"]
            for chunk in self.chunks
        ]

        tokenized_corpus = [
            text.lower().split()
            for text in self.texts
        ]

        self.bm25 = BM25Okapi(tokenized_corpus)


    def vector_search(self, query, k=10):

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        query_embedding = np.array(
            query_embedding
        ).astype("float32")

        scores, indices = self.index.search(
            query_embedding,
            k
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):
            results.append({
                "index": int(idx),
                "score": float(score),
                "chunk": self.chunks[idx]
            })

        return results

    def rrf_fusion(self, vector_results, bm25_results, RRF_K):

        fused_scores = {}

        # Process vector results
        for rank, result in enumerate(vector_results, start=1):
            idx = result["index"]

            if idx not in fused_scores:
                fused_scores[idx] = 0

            fused_scores[idx] += 1 / (RRF_K + rank)

        # Process BM25 results
        for rank, result in enumerate(bm25_results, start=1):
            idx = result["index"]

            if idx not in fused_scores:
                fused_scores[idx] = 0

            fused_scores[idx] += 1 / (RRF_K + rank)

        # Sort by fused score
        ranked_results = sorted(
            fused_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for idx, score in ranked_results:
            results.append({
                "index": idx,
                "score": score,
                "chunk": self.chunks[idx]
            })

        return results
    
    def bm25_search(self, query, k=10):

        tokenized_query = query.lower().split()

        scores = self.bm25.get_scores(
            tokenized_query
        )

        top_indices = np.argsort(scores)[::-1][:k]

        results = []

        for idx in top_indices:
            results.append({
                "index": int(idx),
                "score": float(scores[idx]),
                "chunk": self.chunks[idx]
            })

        return results

    def hybrid_search(self, query, k=20):

        vector_results = self.vector_search(query, k=k)
        bm25_results = self.bm25_search(query, k=k)

        return self.rrf_fusion(
            vector_results,
            bm25_results,
            RRF_K
        )

    def rerank(self, query, results, top_k=5):

        # Create query-chunk pairs
        pairs = [
            (query, result["chunk"]["page_content"])
            for result in results
        ]

        # Score how relevant each chunk is to the query
        scores = self.reranker.predict(pairs)

        # Attach reranker scores
        for result, score in zip(results, scores):
            result["rerank_score"] = float(score)

        # Sort by reranker relevance
        reranked_results = sorted(
            results,
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return reranked_results[:top_k]

    def retrieve(self, query, candidate_k=20, top_k=5):
        candidates = self.hybrid_search(
            query,
            k=candidate_k
        )

        return self.rerank(
            query,
            candidates,
            top_k=top_k
        )