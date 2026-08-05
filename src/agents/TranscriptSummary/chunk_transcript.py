import json
import re
from pathlib import Path

INPUT_FILE = "transcript_clean.txt"
OUTPUT_FILE = "transcript_chunks.json"

TARGET_WORDS = 200      # Recommended: 150-300
OVERLAP_WORDS = 50      # Recommended: 30-75


def split_into_sentences(text):
    """
    Split transcript into sentences while preserving punctuation.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def word_count(text):
    return len(text.split())


def last_words(text, count):
    words = text.split()
    return " ".join(words[-count:])


def create_chunks(sentences, target_words=200, overlap_words=50):
    chunks = []

    current_sentences = []
    current_word_count = 0

    for sentence in sentences:
        sentence_words = word_count(sentence)

        if current_word_count + sentence_words <= target_words:
            current_sentences.append(sentence)
            current_word_count += sentence_words
        else:
            chunk_text = " ".join(current_sentences).strip()

            if chunk_text:
                chunks.append(chunk_text)

            overlap = last_words(chunk_text, overlap_words)

            current_sentences = []

            if overlap:
                current_sentences.append(overlap)

            current_sentences.append(sentence)
            current_word_count = word_count(" ".join(current_sentences))

    if current_sentences:
        chunks.append(" ".join(current_sentences).strip())

    return chunks


def build_chunk_json(chunks):
    json_chunks = []

    for idx, chunk in enumerate(chunks, start=1):

        json_chunks.append({
            "chunk_id": idx,
            "text": chunk,
            "word_count": word_count(chunk),
            "embedding": None,
            "metadata": {
                "retrieval_score": None,
                "matched_question": None,
                "review": None
            }
        })

    return json_chunks


def main():

    transcript = Path(INPUT_FILE).read_text(encoding="utf-8")

    sentences = split_into_sentences(transcript)

    chunks = create_chunks(
        sentences,
        target_words=TARGET_WORDS,
        overlap_words=OVERLAP_WORDS
    )

    chunk_json = build_chunk_json(chunks)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chunk_json, f, indent=4, ensure_ascii=False)

    print(f"Created {len(chunk_json)} chunks.")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
