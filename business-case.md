# Business Case: Hospital Policy RAG Assistant

## 1. Problem Statement

Hospital operational policies, infection-control procedures, patient-safety protocols, consent procedures, and compliance manuals contain detailed rules that staff may need to locate quickly. Searching across multiple policy documents manually can be time-consuming and may result in relevant clauses being overlooked.

This project implements a Retrieval-Augmented Generation (RAG) assistant that enables users to ask natural-language questions about a synthetic hospital policy corpus. The system retrieves relevant policy clauses and generates answers grounded only in the retrieved context.

The system is designed to reduce unsupported responses by combining hybrid retrieval, reranking, structured generation, clause-level citations, and abstention when sufficient supporting evidence is unavailable.

## 2. Target Users

The intended users of the system include:

* Hospital administrative staff
* Clinical support teams
* Nursing staff
* Compliance teams
* Patient-safety personnel
* Policy and procedure reviewers

The assistant is intended as a policy retrieval and reference-support tool. It does not replace clinical judgement, professional decision-making, or official hospital policy systems.

## 3. Corpus Description

The system uses a synthetic corpus containing 30 hospital-related policy documents across multiple domains:

* Healthcare regulatory compliance
* Privacy and data safeguards
* Workplace safety and ethics
* Informed consent procedures
* Emergency treatment and refusal of treatment
* Patient safety protocols
* Infection-control procedures
* Hospital operations and emergency response
* Patient transport procedures
* Hazardous materials and waste handling

The corpus is stored as structured Markdown and text documents. During ingestion, documents are transformed into retrievable chunks with metadata including:

* Source document
* Document ID
* Document title
* Domain
* Section ID
* Section title
* Clause ID
* Clause title

The processed corpus is persisted as both chunk metadata and a FAISS vector index.

## 4. System Scope

The assistant answers questions that are supported by the synthetic hospital policy corpus.

Core capabilities include:

* Natural-language policy questions
* Semantic vector retrieval
* Lexical BM25 retrieval
* Reciprocal Rank Fusion (RRF)
* Cross-encoder reranking
* Query transformation for complex questions
* Clause-level citations
* Structured responses
* Abstention when evidence is insufficient
* Query and answer logging with provenance information

## 5. Domain Guardrails

The system is restricted to the information available in the provided synthetic policy corpus.

The assistant must:

1. Answer using retrieved policy context only.
2. Provide clause-level citations for supported answers.
3. Abstain when the retrieved context does not support an answer.
4. Avoid using external medical or hospital knowledge.
5. Avoid inventing policies, procedures, responsible roles, or step sequences.
6. Treat the corpus as a reference source rather than a substitute for professional or clinical judgement.

Out-of-scope questions should not be answered using unsupported external knowledge.

## 6. Success Metrics

The project evaluates success across retrieval quality, grounding quality, and engineering reliability.

### Retrieval Success

The system should:

* Retrieve relevant policy clauses for user questions.
* Combine lexical and semantic retrieval.
* Use reranking to improve final context selection.
* Support query transformation for complex or multi-part questions.

### Grounding Success

The system should:

* Generate answers supported by retrieved context.
* Include at least one clause-level citation for supported answers.
* Abstain when the corpus does not provide sufficient evidence.
* Avoid unsupported information.

### Evaluation Success

The system includes:

* A golden evaluation dataset containing at least 20 questions.
* Reference answers and expected policy contexts.
* A re-runnable evaluation harness.
* RAGAS-based evaluation for context precision, context recall, faithfulness, and answer relevancy.
* Comparative evaluation of candidate LLMs.

### Engineering Success

The project should:

* Run locally using documented commands.
* Use environment variables for secrets.
* Persist the vector index.
* Externalize retrieval configuration.
* Handle provider failures gracefully.
* Provide reproducible evaluation artifacts.

## 7. Non-Goals

This project does not aim to:

* Provide real clinical advice.
* Replace official hospital information systems.
* Make autonomous clinical decisions.
* Access external medical knowledge during answer generation.
* Operate on real patient data or personally identifiable information.
* Serve as a production-certified healthcare system.

All documents used in this project are synthetic and intended solely for demonstrating RAG engineering techniques.
