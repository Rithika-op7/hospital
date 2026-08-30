# Embedding Model Selection

## Selected Model

**Model:** `BAAI/bge-small-en-v1.5`

The retrieval pipeline uses the `BAAI/bge-small-en-v1.5` embedding model to generate dense vector representations for semantic search.

## Selection Rationale

The embedding model was selected based on the trade-off between retrieval quality, computational efficiency, and local execution requirements.

The project is designed to run locally on a standard development environment. Therefore, using a lightweight embedding model provides a practical balance between semantic retrieval capability and inference cost.

## MTEB-Informed Considerations

The BGE family of embedding models is widely used for retrieval-oriented embedding tasks and is designed to perform well across semantic similarity and information retrieval benchmarks.

The selection of the smaller BGE variant prioritizes:

* Strong retrieval-oriented embedding performance.
* Efficient local inference.
* Lower memory requirements compared with larger embedding models.
* Faster embedding generation during indexing.
* Practical query latency during retrieval.

The project prioritizes a lightweight retrieval architecture rather than maximizing benchmark performance through a significantly larger embedding model.

## Dimensionality and Storage Trade-Off

The selected model produces dense embeddings suitable for indexing with FAISS.

Embedding dimensionality directly affects:

* Vector storage requirements.
* Index memory consumption.
* Similarity search efficiency.
* Indexing time.

A smaller embedding model reduces infrastructure requirements while maintaining sufficient semantic representation quality for the synthetic policy corpus used in this project.

This makes the model suitable for a prototype that must run locally without requiring expensive embedding APIs.

## Cost Considerations

The embedding model runs locally using SentenceTransformers.

This provides several advantages:

* No per-request embedding API cost.
* No external embedding service dependency.
* Reproducible indexing.
* Offline embedding generation after model download.

The primary cost is local compute time during document indexing and query embedding generation.

## Alternatives Considered

Larger embedding models could potentially provide improved semantic retrieval performance but would increase:

* Memory usage.
* Model loading time.
* Embedding latency.
* Hardware requirements.

Hosted embedding APIs could simplify infrastructure but introduce:

* API costs.
* External service dependencies.
* Network latency.
* Potential rate limits.

For this project, `BAAI/bge-small-en-v1.5` provides an appropriate balance between retrieval quality, efficiency, and ease of local deployment.

## Retrieval Compatibility

The embeddings are stored in a FAISS vector index and queried using normalized query embeddings.

Dense semantic retrieval is combined with BM25 lexical retrieval. The two retrieval strategies complement each other:

* **BGE embeddings:** Capture semantic similarity between the question and policy clauses.
* **BM25:** Captures exact lexical matches and important policy terminology.
* **RRF:** Combines rankings from both retrieval methods.

This hybrid design reduces dependence on a single retrieval approach.

## Final Decision

The project selected:

```text
BAAI/bge-small-en-v1.5
```

because it provides a practical balance of:

* Retrieval-oriented semantic performance.
* Lightweight local execution.
* Lower infrastructure requirements.
* No per-query embedding API cost.
* Compatibility with FAISS.
* Efficient integration with hybrid retrieval.
