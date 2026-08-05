import json
import requests
import numpy as np
from pathlib import Path

# -----------------------------
# Configuration
# -----------------------------

INPUT_JSON = "transcript_chunks.json"

OUTPUT_JSON = "transcript_chunks.json"
OUTPUT_EMBEDDINGS = "transcript_embeddings.npy"

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL = "nomic-embed-text"


# -----------------------------
# Generate Embedding
# -----------------------------

def generate_embedding(text):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": text
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["embedding"]


# -----------------------------
# Main
# -----------------------------

def main():

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    embeddings = []

    total = len(chunks)

    for index, chunk in enumerate(chunks, start=1):

        print(f"Embedding {index}/{total}")

        embedding = generate_embedding(chunk["text"])

        embeddings.append(embedding)

        # Remove large embedding from JSON
        chunk.pop("embedding", None)

        # Store useful metadata
        chunk["metadata"]["embedding_index"] = index - 1
        chunk["metadata"]["embedding_model"] = MODEL

    embeddings = np.array(embeddings, dtype=np.float32)

    # Save metadata
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4, ensure_ascii=False)

    # Save embeddings
    np.save(OUTPUT_EMBEDDINGS, embeddings)

    print()
    print(f"Chunks        : {len(chunks)}")
    print(f"Embeddings    : {embeddings.shape}")
    print(f"Metadata File : {OUTPUT_JSON}")
    print(f"Vector File   : {OUTPUT_EMBEDDINGS}")


if __name__ == "__main__":
    main()
