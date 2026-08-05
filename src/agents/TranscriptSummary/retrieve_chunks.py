import json
import requests
import numpy as np

# ---------------- Configuration ----------------

QUESTIONS_FILE = "questions.txt"
CHUNKS_FILE = "transcript_chunks.json"
EMBEDDINGS_FILE = "transcript_embeddings.npy"
OUTPUT_FILE = "retrieval_results.json"

OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBEDDING_MODEL = "nomic-embed-text"

TOP_K = 3
OVERLAP_WORDS = 50


# ---------------- Embedding ----------------

def generate_embedding(text):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": EMBEDDING_MODEL,
            "prompt": text
        },
        timeout=120
    )

    response.raise_for_status()

    return np.array(response.json()["embedding"], dtype=np.float32)


# ---------------- Cosine Similarity ----------------

def cosine_similarity(query, vectors):

    query = query / np.linalg.norm(query)
    vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

    return np.dot(vectors, query)


# ---------------- Merge Chunks ----------------

def remove_overlap(previous_text, current_text, overlap_words):

    prev_words = previous_text.split()
    curr_words = current_text.split()

    if len(prev_words) < overlap_words or len(curr_words) < overlap_words:
        return current_text

    prev_overlap = " ".join(prev_words[-overlap_words:])
    curr_overlap = " ".join(curr_words[:overlap_words])

    if prev_overlap == curr_overlap:
        return " ".join(curr_words[overlap_words:])

    return current_text


def merge_chunks(indices, chunks):

    indices = sorted(indices)

    merged_text = ""
    merged_chunk_ids = []

    previous_chunk = None

    for idx in indices:

        chunk = chunks[idx]
        chunk_text = chunk["text"]

        merged_chunk_ids.append(chunk["chunk_id"])

        if previous_chunk is None:
            merged_text = chunk_text
        else:
            chunk_text = remove_overlap(
                merged_text,
                chunk_text,
                OVERLAP_WORDS
            )

            merged_text += "\n\n" + chunk_text

        previous_chunk = chunk

    return merged_chunk_ids, merged_text.strip()


# ---------------- Main ----------------

def main():

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    embeddings = np.load(EMBEDDINGS_FILE)

    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        questions = [x.strip() for x in f if x.strip()]

    results = []

    for question in questions:

        print(f"Searching: {question}")

        query_embedding = generate_embedding(question)

        scores = cosine_similarity(query_embedding, embeddings)

        top_indices = np.argsort(scores)[::-1][:TOP_K]

        merged_chunk_ids, context = merge_chunks(top_indices, chunks)

        results.append({
            "question": question,
            "retrieved_chunk_ids": merged_chunk_ids,
            "context": context,
            "scores": [
                round(float(scores[i]), 4)
                for i in sorted(top_indices)
            ]
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print()
    print(f"Saved retrieval results to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
