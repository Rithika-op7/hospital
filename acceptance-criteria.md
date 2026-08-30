# Acceptance Criteria

This document defines testable acceptance criteria for the Hospital Policy RAG Assistant. Each criterion is identified using an `AC-NN` identifier and is mapped to implementation components and evaluation evidence.

---

## AC-01: Corpus Ingestion and Persistent Index

**Criterion:**
The system shall ingest a synthetic corpus containing at least 30 hospital policy documents and create a persisted vector index.

**Verification:**

* Confirm at least 30 documents exist in `data/raw/`.
* Run the ingestion and indexing pipeline.
* Confirm that `data/faiss_index/index.faiss` is generated.
* Confirm that `data/faiss_index/metadata.json` contains chunk metadata.
* Re-running ingestion should regenerate the index without requiring manual modification.

**Evidence:**

* `src/ingestion.py`
* `src/build_index.py`
* `data/raw/`
* `data/faiss_index/`

---

## AC-02: Grounded Answers with Clause-Level Citations

**Criterion:**
A user shall be able to ask a natural-language question and receive an answer grounded only in the policy corpus with at least one clause-level citation.

**Verification:**

* Submit a policy-related question.
* Confirm that the response contains an answer.
* Confirm that at least one citation contains a document ID and clause ID.
* Verify that the cited clause supports the answer.

**Evidence:**

* `src/generator.py`
* `src/schemas.py`
* `evaluation/golden_dataset.json`

---

## AC-03: Hybrid Retrieval

**Criterion:**
The retrieval pipeline shall combine lexical and semantic retrieval and fuse the result sets before generation.

**Verification:**

* Execute vector search for a query.
* Execute BM25 search for the same query.
* Confirm that both result sets are produced.
* Confirm that Reciprocal Rank Fusion combines the rankings.

**Evidence:**

* `src/retriever.py`
* `src/test_hybrid.py`

---

## AC-04: Candidate Reranking

**Criterion:**
Retrieved candidates shall be reranked using a cross-encoder before the final top-K results are passed to the generator.

**Verification:**

* Retrieve an initial candidate set.
* Apply the cross-encoder reranker.
* Confirm that the final results are sorted using reranking scores.
* Confirm that only the final top-K chunks are passed to generation.

**Evidence:**

* `src/retriever.py`
* `src/test_retrieval.py`

---

## AC-05: Abstention for Unsupported Questions

**Criterion:**
When the corpus does not support an answer, the system shall abstain rather than fabricate information.

**Verification:**

* Submit an out-of-scope question.
* Confirm that the system returns the configured abstention response.
* Confirm that `abstained` is set to `true`.
* Confirm that unsupported citations are not generated.

**Evidence:**

* `src/generator.py`
* `docs/guardrails.md`
* `docs/sample_outputs.md`

---

## AC-06: Structured Response Validation

**Criterion:**
Answers shall be returned as validated structured objects containing answer text, citations, applicable policy information, procedural steps when applicable, responsible role when applicable, confidence or grounding information, and abstention status.

**Verification:**

* Submit a supported query.
* Confirm that the returned response conforms to the Pydantic schema.
* Confirm citation objects contain document and clause identifiers.
* Confirm required response fields are present.

**Evidence:**

* `src/schemas.py`
* `src/generator.py`

---

## AC-07: Query Transformation

**Criterion:**
Complex, ambiguous, or multi-part questions shall be transformed before retrieval.

**Verification:**

* Submit a multi-part or ambiguous question.
* Confirm that the query transformation component processes the query.
* Confirm that the transformed query is used for retrieval.

**Evidence:**

* `src/query_transformer.py`
* `src/retriever.py`

---

## AC-08: Golden Evaluation Dataset

**Criterion:**
The repository shall contain a golden evaluation dataset with at least 20 questions and reference answers or expected contexts.

**Verification:**

* Confirm that `evaluation/golden_dataset.json` contains at least 20 entries.
* Confirm each entry includes a question.
* Confirm entries include ground-truth answers.
* Confirm expected document and clause information is available.

**Evidence:**

* `evaluation/golden_dataset.json`
* `evaluation/evaluation.py`

---

## AC-09: RAGAS Evaluation

**Criterion:**
The evaluation pipeline shall compute RAGAS metrics for retrieval and generation quality.

**Metrics:**

* Context Precision
* Context Recall
* Faithfulness
* Answer Relevancy

**Verification:**

* Run the RAGAS evaluation script.
* Confirm numeric metrics are generated.
* Confirm the results are saved as a report artifact.

**Evidence:**

* `evaluation/ragas_evaluation.py`
* `evaluation/ragas_report.json`

---

## AC-10: Candidate Model Comparison

**Criterion:**
At least two candidate LLMs shall be evaluated using the custom evaluation dataset and compared using documented selection criteria.

**Verification:**

* Run both candidate models against the evaluation set.
* Record evaluation results.
* Compare answer quality, grounding, reliability, latency, and cost considerations.
* Document the rationale for selecting the preferred model.

**Evidence:**

* `evaluation/model_comparison.py`
* `evaluation/model_comparison_report.md`

---

# Acceptance Criteria Traceability

| AC ID | Primary Implementation           | Test / Evaluation Evidence |
| ----- | -------------------------------- | -------------------------- |
| AC-01 | `ingestion.py`, `build_index.py` | Persisted index            |
| AC-02 | `generator.py`                   | Golden dataset             |
| AC-03 | `retriever.py`                   | Hybrid retrieval test      |
| AC-04 | `retriever.py`                   | Reranking verification     |
| AC-05 | `generator.py`                   | Abstention example         |
| AC-06 | `schemas.py`                     | Schema validation          |
| AC-07 | `query_transformer.py`           | Query transformation       |
| AC-08 | Evaluation dataset               | `evaluation.py`            |
| AC-09 | RAGAS pipeline                   | RAGAS report               |
| AC-10 | Model evaluation                 | Comparison report          |
