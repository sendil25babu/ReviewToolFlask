from pathlib import Path
import shutil
# import whisper
from agents.TranscriptSummary.processTranscript import process_transcript_workflow
from constants.paths import DATA_PATH
from agents.TranscriptSummary.generateTranscript import transcribe_video


def createVideoPath(interviewId, default_folder="C:\\SendilFolder\\PythonExercise\\ReviewTool"):
    """Create interview folder under static/data, copy video from default folder, and return copied path."""
    if not isinstance(interviewId, str) or not interviewId.strip():
        raise ValueError("interviewId must be a non-empty string")

    normalized_interview_id = interviewId.strip()
    source_video_path = Path(default_folder) / f"{normalized_interview_id}.mp4"

    if not source_video_path.exists():
        raise FileNotFoundError(
            f"Source video not found: {source_video_path}"
        )

    destination_dir = DATA_PATH / normalized_interview_id
    destination_dir.mkdir(parents=True, exist_ok=True)

    destination_video_path = destination_dir / source_video_path.name
    shutil.copy2(source_video_path, destination_video_path)

    return str(destination_video_path)


def generate_review(request_details):
    """Generate review output using the request payload from app.py."""
    topic_name = request_details.get("topic")
    interview_id = request_details.get("interviewId", "")
    skip_transcript = bool(request_details.get("skipTranscript", False))

    createVideoPath(interview_id)

    transcript_file = transcribe_video(
        interview_id, skip_transcript=skip_transcript)

    if transcript_file is None or not transcript_file.exists():
        return {"error": f"Transcript file not found: {transcript_file}"}

    result = process_transcript_workflow(
        transcript_file=str(transcript_file),
        topic_name=topic_name,
        output_dir=str(DATA_PATH / interview_id)
    )

    if "error" in result:
        return result["error"]

    return {
        "review_output": "review_output",
        "workflow": "review_output",
    }
