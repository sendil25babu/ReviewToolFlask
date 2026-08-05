import argparse
import json
import re
from pathlib import Path

import numpy as np

from agents.TranscriptSummary.chunk_transcript import (
    TARGET_WORDS,
    OVERLAP_WORDS,
    split_into_sentences,
    create_chunks,
    build_chunk_json,
)
from agents.TranscriptSummary.clean_transcript import clean_transcript
from agents.TranscriptSummary.embed_chunks import MODEL as EMBEDDING_MODEL
from agents.TranscriptSummary.embed_chunks import generate_embedding as generate_chunk_embedding
from agents.TranscriptSummary.retrieve_chunks import (
    TOP_K,
    cosine_similarity,
    merge_chunks,
    generate_embedding as generate_query_embedding,
)
from agents.TranscriptSummary.review_answers import review_retrieved_answers


def _extract_questions(source_file, output_questions_file):
    """Extract question lines from a source file into one-question-per-line text format."""
    source_path = Path(source_file)
    output_path = Path(output_questions_file)

    lines = source_path.read_text(encoding="utf-8").splitlines()
    questions = []

    numbered_question_pattern = re.compile(r"^\s*\d+\.\s*(.+\?)\s*$")

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        match = numbered_question_pattern.match(line)
        if match:
            questions.append(match.group(1).strip())
            continue

        if line.endswith("?"):
            questions.append(line)

    # Preserve order while removing duplicates.
    deduped_questions = list(dict.fromkeys(questions))

    if not deduped_questions:
        raise ValueError(f"No questions found in: {source_file}")

    output_path.write_text("\n".join(deduped_questions), encoding="utf-8")
    return deduped_questions


def _chunk_transcript(cleaned_transcript_file, chunks_output_file):
    transcript = Path(cleaned_transcript_file).read_text(encoding="utf-8")
    sentences = split_into_sentences(transcript)

    chunks = create_chunks(
        sentences,
        target_words=TARGET_WORDS,
        overlap_words=OVERLAP_WORDS,
    )

    chunk_json = build_chunk_json(chunks)

    with open(chunks_output_file, "w", encoding="utf-8") as f:
        json.dump(chunk_json, f, indent=4, ensure_ascii=False)

    return chunk_json


def _generate_embeddings(chunks_file, embeddings_output_file):
    with open(chunks_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    embeddings = []

    for index, chunk in enumerate(chunks, start=1):
        print(f"Embedding {index}/{len(chunks)}")
        embedding = generate_chunk_embedding(chunk["text"])
        embeddings.append(embedding)

        chunk.pop("embedding", None)
        chunk["metadata"]["embedding_index"] = index - 1
        chunk["metadata"]["embedding_model"] = EMBEDDING_MODEL

    embeddings_array = np.array(embeddings, dtype=np.float32)

    with open(chunks_file, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4, ensure_ascii=False)

    np.save(embeddings_output_file, embeddings_array)

    return chunks, embeddings_array


def _retrieve_relevant_chunks(questions_file, chunks_file, embeddings_file, retrieval_output_file):
    with open(chunks_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    embeddings = np.load(embeddings_file)

    with open(questions_file, "r", encoding="utf-8") as f:
        questions = [line.strip() for line in f if line.strip()]

    results = []

    for question in questions:
        print(f"Searching: {question}")

        query_embedding = generate_query_embedding(question)
        scores = cosine_similarity(query_embedding, embeddings)
        top_indices = np.argsort(scores)[::-1][:TOP_K]

        merged_chunk_ids, context = merge_chunks(top_indices, chunks)

        results.append(
            {
                "question": question,
                "retrieved_chunk_ids": merged_chunk_ids,
                "context": context,
                "scores": [round(float(scores[i]), 4) for i in sorted(top_indices)],
            }
        )

    with open(retrieval_output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    return results


def process_transcript_workflow(
    transcript_file,
    questions_source_file,
    output_dir,
    cleaned_transcript_file="transcript_clean.txt",
    chunks_file="transcript_chunks.json",
    embeddings_file="transcript_embeddings.npy",
    extracted_questions_file="questions.txt",
    retrieval_file="retrieval_results.json",
    review_file="interview_review.json",
):
    """Run the full transcript workflow from cleaning through final review output."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    cleaned_path = output_path / cleaned_transcript_file
    chunks_path = output_path / chunks_file
    embeddings_path = output_path / embeddings_file
    questions_path = output_path / extracted_questions_file
    retrieval_path = output_path / retrieval_file
    review_path = output_path / review_file

    print("Step 1/6: Cleaning transcript")
    clean_transcript(transcript_file, str(cleaned_path))

    print("Step 2/6: Chunking transcript")
    chunk_json = _chunk_transcript(str(cleaned_path), str(chunks_path))

    print("Step 3/6: Generating embeddings")
    _, embeddings_array = _generate_embeddings(
        str(chunks_path), str(embeddings_path))

    print("Step 4/6: Preparing questions and retrieving relevant chunks")
    questions = _extract_questions(questions_source_file, str(questions_path))
    retrieval_results = _retrieve_relevant_chunks(
        str(questions_path),
        str(chunks_path),
        str(embeddings_path),
        str(retrieval_path),
    )

    print("Step 5/6 and 6/6: Review answers (Stage 1 + Stage 2)")
    reviews = review_retrieved_answers(str(retrieval_path), str(review_path))

    return {
        "cleaned_transcript": str(cleaned_path),
        "chunks": str(chunks_path),
        "embeddings": str(embeddings_path),
        "questions": str(questions_path),
        "retrieval_results": str(retrieval_path),
        "review_output": str(review_path),
        "counts": {
            "questions": len(questions),
            "chunks": len(chunk_json),
            "retrieval_results": len(retrieval_results),
            "reviews": len(reviews),
            "embedding_rows": int(embeddings_array.shape[0]),
        },
    }


def _build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Run transcript processing workflow end-to-end."
    )
    parser.add_argument("--transcript", required=True,
                        help="Path to transcript text file")
    parser.add_argument(
        "--questions-source",
        required=True,
        help="Path to source file containing interview questions",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory where workflow output files are generated",
    )
    return parser


def main():
    args = _build_arg_parser().parse_args()

    result = process_transcript_workflow(
        transcript_file=args.transcript,
        questions_source_file=args.questions_source,
        output_dir=args.output_dir,
    )

    print("Workflow complete.")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
