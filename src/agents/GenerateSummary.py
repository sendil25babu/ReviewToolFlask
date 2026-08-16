import re
from pathlib import Path

from constants.paths import DATA_PATH, REVIEW_FOLDER_PATH
from utilities.fileOperation import create_docx_file


def generateInterviewSummary(summary_request):
    interviewId = summary_request.get("interviewId", "")
    topicName = summary_request.get("topicName", "")
    incorrect_question_input = summary_request.get(
        "incorrect_question_input", "")
    gender = summary_request.get("gender", "")

    yes_file = DATA_PATH / "topic" / f"{topicName}-YesResponse.txt"
    no_file = DATA_PATH / "topic" / f"{topicName}-NoResponse.txt"

    incorrect_questions = set(
        int(x.strip())
        for x in incorrect_question_input.split(",")
        if x.strip()
    )

    strengths_paragraph = " ".join(
        read_answers(
            yes_file,
            exclude_questions=incorrect_questions
        )
    )

    improvements_paragraph = " ".join(
        read_answers(
            no_file,
            target_questions=incorrect_questions
        )
    )

    line1 = "The candidate is skilled in " if not topicName == 'ProductBuilder' else ""
    final_summary = (
        f"Strengths: {line1}\n"
        + strengths_paragraph
        + "\n"
        + "Areas of Improvement/Weaknesses:\n"
        + improvements_paragraph
        + "\n"
        + "The candidate is good in the interview. "
        + "The areas are mentioned above where he can improve. "
        + "He can be rated at 4 stars."
    )

    if isinstance(gender, str) and gender.strip().lower() == "female":
        final_summary = apply_female_pronouns(final_summary)

    filename = f"interviewId_{interviewId}.docx"
    output_dir = REVIEW_FOLDER_PATH / interviewId
    output_file = output_dir / filename

    output_dir.mkdir(parents=True, exist_ok=True)

    create_docx_file(output_file, final_summary)

    return output_file


def apply_female_pronouns(text):
    pronoun_map = {
        r"\bHe\b": "She",
        r"\bhe\b": "she",
        r"\bhis\b": "her",
    }

    updated_text = text
    for pattern, replacement in pronoun_map.items():
        updated_text = re.sub(pattern, replacement, updated_text)

    return updated_text


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

    """
    Expected format:

    Question: Question Text
    Response Text

    Question: Question Text
    Response Text
    """

    blocks = content.split("Question:")

    results = []

    for block in blocks:

        block = block.strip()

        if not block:
            continue

        lines = block.splitlines()

        question = lines[0].strip()

        response = " ".join(
            line.strip()
            for line in lines[1:]
            if line.strip()
        )

        results.append((question, response))

    return results


def read_answers(file_path, target_questions=None, exclude_questions=None):

    answers = []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    i = 0

    while i < len(lines) - 1:

        question_line = lines[i]
        answer_line = lines[i + 1]

        match = re.match(r"^(\d+)\.", question_line)

        if match:

            question_no = int(match.group(1))

            include = True

            if target_questions is not None:
                include = question_no in target_questions

            if exclude_questions is not None:
                include = question_no not in exclude_questions

            if include:
                answers.append(answer_line)

            i += 2

        else:
            i += 1

    return answers
