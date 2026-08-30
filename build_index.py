import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path


# Paths
CHUNKS_PATH = "data/processed/chunks.json"
INDEX_PATH = "data/faiss_index/index.faiss"
METADATA_PATH = "data/faiss_index/metadata.json"


# Load chunks
with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")


# Load embedding model
model = SentenceTransformer("BAAI/bge-small-en-v1.5")


# Extract chunk text
texts = [chunk["page_content"] for chunk in chunks]


# Create embeddings
print("Creating embeddings...")
embeddings = model.encode(
    texts,
    show_progress_bar=True,
    normalize_embeddings=True
)

embeddings = np.array(embeddings).astype("float32")

print("Embedding shape:", embeddings.shape)


# Create FAISS index
dimension = embeddings.shape[1]

# Inner Product works as cosine similarity because embeddings are normalized
index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

print(f"Vectors indexed: {index.ntotal}")


# Create output directory
Path("data/faiss_index").mkdir(parents=True, exist_ok=True)


# Save FAISS index
faiss.write_index(index, INDEX_PATH)

with open(METADATA_PATH, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)


print("\nFAISS index created successfully!")
print(f"Index saved to: {INDEX_PATH}")
print(f"Metadata saved to: {METADATA_PATH}")