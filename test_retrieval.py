import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# Load model
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# Load FAISS index
index = faiss.read_index("data/faiss_index/index.faiss")

# Load metadata
with open("data/faiss_index/metadata.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)


def search(query, k=5):

    # Convert query to embedding
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    query_embedding = np.array(query_embedding).astype("float32")

    # Search FAISS
    scores, indices = index.search(query_embedding, k)

    print(f"\nQuery: {query}\n")

    for rank, (score, idx) in enumerate(
        zip(scores[0], indices[0]), start=1
    ):
        chunk = chunks[idx]

        print(f"Rank {rank}")
        print(f"Score: {score:.4f}")
        print("Document:", chunk["metadata"]["document_id"])
        print("Section:", chunk["metadata"]["section_id"])
        print("Clause:", chunk["metadata"]["clause_id"])
        print("Text:", chunk["page_content"][:300])
        print("-" * 60)


search("What PPE is required for airborne isolation?")