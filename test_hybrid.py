from retriever import HybridRetriever


retriever = HybridRetriever()

query = "What PPE is required for airborne isolation?"


print("\n===== VECTOR SEARCH =====")

vector_results = retriever.vector_search(query, k=5)

for rank, result in enumerate(vector_results, 1):

    chunk = result["chunk"]

    print(
        f"\nRank {rank} | Score: {result['score']:.4f}"
    )

    print(
        chunk["metadata"]["document_id"],
        "| Clause:",
        chunk["metadata"]["clause_id"]
    )

    print(chunk["page_content"][:200])


print("\n\n===== BM25 SEARCH =====")

bm25_results = retriever.bm25_search(query, k=5)

for rank, result in enumerate(bm25_results, 1):

    chunk = result["chunk"]

    print(
        f"\nRank {rank} | Score: {result['score']:.4f}"
    )

    print(
        chunk["metadata"]["document_id"],
        "| Clause:",
        chunk["metadata"]["clause_id"]
    )

    print(chunk["page_content"][:200])

print("\n\n===== HYBRID RRF SEARCH =====")

hybrid_results = retriever.hybrid_search(query, k=10)

for rank, result in enumerate(hybrid_results[:5], 1):

    chunk = result["chunk"]

    print(
        f"\nRank {rank} | RRF Score: {result['score']:.4f}"
    )

    print(
        chunk["metadata"]["document_id"],
        "| Clause:",
        chunk["metadata"]["clause_id"]
    )

    print(chunk["page_content"][:200])

print("\n\n===== FINAL RERANKED RESULTS =====")

final_results = retriever.retrieve(
    query,
    candidate_k=20,
    top_k=5
)

for rank, result in enumerate(final_results, 1):

    chunk = result["chunk"]

    print(f"\nRank {rank}")
    print(f"Rerank Score: {result['rerank_score']:.4f}")
    print(
        chunk["metadata"]["document_id"],
        "| Clause:",
        chunk["metadata"]["clause_id"]
    )
    print(chunk["page_content"][:250])