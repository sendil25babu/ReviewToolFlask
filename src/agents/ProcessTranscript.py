from pathlib import Path
# import whisper
from agents.TranscriptSummary.processTranscript import process_transcript_workflow
from constants.paths import DATA_PATH


# def transcribe_video(video_file, transcript_file):

#     model = whisper.load_model("tiny", device="cpu")

#     result = model.transcribe(video_file)

#     with open(transcript_file, "w", encoding="utf-8") as f:
#         f.write(result["text"])


def processTranscript(transcript, topicName):
    """
    Process the transcript and generate interview review output.

    transcript: path to transcript file, transcript text, or a boolean flag (legacy).
    topicName: topic key used to resolve question source file.
    """
    questions_source = DATA_PATH / f"{topicName}-YesResponse.txt"

    if not questions_source.exists():
        return f"Questions source file not found: {questions_source}"

    # Backward compatibility: if the first argument is not a path, fall back to
    # the default transcript file inside static/data.
    transcript_file = None

    if isinstance(transcript, str) and transcript.strip():
        candidate_path = Path(transcript)
        if candidate_path.exists():
            transcript_file = candidate_path

    if transcript_file is None:
        transcript_file = DATA_PATH / "transcript.txt"

    if not transcript_file.exists():
        return f"Transcript file not found: {transcript_file}"

    output_dir = DATA_PATH / "outputs" / topicName
    result = process_transcript_workflow(
        transcript_file=str(transcript_file),
        questions_source_file=str(questions_source),
        output_dir=str(output_dir),
    )

    return result["review_output"]
