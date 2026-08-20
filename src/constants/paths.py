from pathlib import Path

current_path = Path(__file__).resolve().parent
DATA_PATH = current_path.parent / "static" / "data"
REVIEW_FOLDER_PATH = DATA_PATH / "summarys"
