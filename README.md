# Hospital Policy RAG Assistant

A Retrieval-Augmented Generation (RAG) system for answering questions based on synthetic hospital policies, SOPs, patient safety protocols, consent procedures, and compliance manuals.

## Features

- Semantic retrieval using FAISS
- Lexical retrieval using BM25
- Hybrid retrieval using Reciprocal Rank Fusion (RRF)
- Cross-encoder reranking
- Grounded answers with clause-level citations
- Structured Pydantic responses
- Query transformation
- Abstention for unsupported questions
- Evaluation pipeline

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd project_rithikakonderi_repo
```
### 2. Create a virtual environment

```bash
python -m venv .venv
```
### 3. Activate the virtual environment

```bash
.venv\Scripts\activate
```
### 4. Install dependencies

```bash
pip install -r requirements.txt
```
### 5. Configure Environmental variables

```bash
GOOGLE_API_KEY=your_google_api_key_here
```
## Run the application

```bash
python -m src.app
```
## Run evaluation

```bash
python -m evaluation.evaluation
```
## Project Structure

```bash
project/
├── data/
│   ├── raw/
│   └── faiss_index/
├── src/
│   ├── app.py
│   ├── retriever.py
│   ├── generator.py
│   ├── schemas.py
│   └── logger.py
├── evaluation/
├── logs/
├── config.py
├── requirements.txt
├── .env.example
└── README.md
```

## Cost and Latency Considerations

This project uses a hybrid retrieval pipeline consisting of BM25 retrieval, FAISS semantic search, Reciprocal Rank Fusion, cross-encoder reranking, and LLM-based answer generation.

Most retrieval operations run locally. The primary external cost and latency come from the LLM generation call.

For a representative query:

* BM25 and FAISS retrieval are expected to have low local latency.
* Cross-encoder reranking adds additional inference latency.
* LLM generation is expected to be the dominant source of end-to-end latency.
* API-based generation may incur provider-dependent usage costs.

The system retrieves and reranks a limited number of candidates before generation to reduce unnecessary context and control token usage.

No formal benchmarking or production performance governance was performed, as cost and latency are addressed at a conceptual level for this project.
