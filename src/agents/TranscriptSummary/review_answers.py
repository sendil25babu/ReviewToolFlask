import json
import requests

INPUT_FILE = "retrieval_results.json"
OUTPUT_FILE = "interview_review.json"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"

TEMPERATURE = 0
NUM_PREDICT = 40


def build_stage1_prompt(question, context):

    return f"""
        You are an interview reviewer.
        Question:
        {question}
        Candidate Response:
        {context}
        Task:
            Determine whether the candidate meaningfully addressed the interview question.
            Reply with ONLY one word.
            YES
            or
            NO
        """


def build_stage2_prompt(question, context):

    return f"""
        You are an interview reviewer.

        Question:
        {question}

        Candidate Response:
        {context}

        Write exactly one sentence.

        Rules:

        - Maximum 20 words.
        - Third person.
        - Start with He explained or He discussed.
        - Reuse important words from the question.
        - Summarize only the topic.
        - Do not evaluate.
        - Do not answer the interview question.
        - Output only one sentence.
        """


def ask_qwen(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": TEMPERATURE,
                "num_predict": NUM_PREDICT,
                "top_p": 0.1,
                "repeat_penalty": 1.1
            }
        },
        timeout=120
    )
    response.raise_for_status()
    return response.json()["response"].strip()


def review_retrieved_answers(input_file=INPUT_FILE, output_file=OUTPUT_FILE):
    with open(input_file, encoding="utf-8") as f:
        retrieval_results = json.load(f)

    reviews = []

    for item in retrieval_results:
        question = item["question"]
        context = item["context"]
        decision = ask_qwen(
            build_stage1_prompt(question, context)
        ).upper()

        if decision.startswith("YES"):
            review = ask_qwen(
                build_stage2_prompt(question, context)
            )
        else:
            review = "He did not address this question."

        reviews.append({
            "question": question,
            "review": review
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=4, ensure_ascii=False)

    print(f"Saved review output to {output_file}")
    return reviews


if __name__ == "__main__":
    review_retrieved_answers(INPUT_FILE, OUTPUT_FILE)
