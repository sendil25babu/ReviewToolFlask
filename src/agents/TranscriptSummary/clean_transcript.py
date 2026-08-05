import re
from pathlib import Path


class TranscriptCleaner:
    def __init__(self):
        self.filler_patterns = [
            r"\bum\b",
            r"\buh\b",
            r"\ber\b",
            r"\bah\b",
            r"\bhmm\b",
            r"\byou know\b",
            r"\bi mean\b",
            r"\bkind of\b",
            r"\bsort of\b",
            r"\bokay\b",
            r"\bok\b"
        ]

        self.speaker_pattern = re.compile(
            r"^(interviewer|candidate|speaker\s*\d+|host)\s*:\s*",
            re.IGNORECASE,
        )

        self.timestamp_patterns = [
            re.compile(r"\[\d{2}:\d{2}:\d{2}\]"),
            re.compile(r"\d{2}:\d{2}:\d{2}"),
            re.compile(r"\d{2}:\d{2}")
        ]

    def remove_timestamps(self, text):
        for pattern in self.timestamp_patterns:
            text = pattern.sub("", text)
        return text

    def remove_speaker_labels(self, text):
        lines = []

        for line in text.splitlines():
            line = self.speaker_pattern.sub("", line)
            lines.append(line)

        return "\n".join(lines)

    def remove_fillers(self, text):
        for filler in self.filler_patterns:
            text = re.sub(filler, "", text, flags=re.IGNORECASE)

        text = re.sub(r"\s{2,}", " ", text)

        return text

    def merge_lines(self, text):
        lines = [x.strip() for x in text.splitlines() if x.strip()]
        return " ".join(lines)

    def remove_duplicate_sentences(self, text):
        sentences = re.split(r'(?<=[.!?])\s+', text)

        cleaned = []
        previous = ""

        for sentence in sentences:
            sentence = sentence.strip()

            if not sentence:
                continue

            if sentence.lower() == previous.lower():
                continue

            cleaned.append(sentence)
            previous = sentence

        return " ".join(cleaned)

    def cleanup_spaces(self, text):
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\s+([.,!?])", r"\1", text)
        return text.strip()

    def clean(self, transcript):
        transcript = self.remove_timestamps(transcript)
        transcript = self.remove_speaker_labels(transcript)
        transcript = self.remove_fillers(transcript)
        transcript = self.merge_lines(transcript)
        transcript = self.remove_duplicate_sentences(transcript)
        transcript = self.cleanup_spaces(transcript)

        return transcript


def clean_transcript(input_file, output_file):
    cleaner = TranscriptCleaner()

    transcript = Path(input_file).read_text(encoding="utf-8")

    cleaned = cleaner.clean(transcript)

    Path(output_file).write_text(cleaned, encoding="utf-8")

    print(f"Original Length : {len(transcript):,}")
    print(f"Cleaned Length  : {len(cleaned):,}")
    print(f"Saved : {output_file}")


if __name__ == "__main__":
    clean_transcript(
        "transcript.txt",
        "transcript_clean.txt"
    )
