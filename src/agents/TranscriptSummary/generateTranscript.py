import time
import whisper

from agents.TranscriptSummary.clean_transcript import clean_transcript
from constants.paths import DATA_PATH


def transcribe_video(interview_id, skip_transcript=False):

    video_file = DATA_PATH / interview_id / f"{interview_id}.mp4"
    transcript_file = DATA_PATH / interview_id / "transcript.txt"

    if skip_transcript:
        if transcript_file.exists():
            print("Using existing transcript ->", transcript_file)
            return transcript_file
        return None

    if transcript_file.exists():
        print("Using existing transcript ->", transcript_file)
        return transcript_file

    start = time.time()

    model = whisper.load_model("tiny", device="cpu")
    result = model.transcribe(str(video_file))
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(result["text"])

    cleaned_transcript_file = clean_transcript(transcript_file)

    end = time.time()

    print("Transcript saved ->", transcript_file)
    print("Cleaned transcript saved ->", cleaned_transcript_file)
    print("Transcription time:", round(end - start, 2), "seconds")

    return cleaned_transcript_file
