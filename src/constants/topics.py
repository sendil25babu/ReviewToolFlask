"""
Constants for topics/roles available in the application.
"""

from constants.paths import DATA_PATH


def build_topics_from_data_path():
    """Build unique topic names from Yes/No response files in static/data/topic."""
    topics = set()
    topic_data_path = DATA_PATH / "topic"

    files = topic_data_path.glob(
        "*.txt") if topic_data_path.exists() else DATA_PATH.glob("*.txt")

    for file_path in files:
        name = file_path.name

        if name.endswith("-YesResponse.txt"):
            topics.add(name[: -len("-YesResponse.txt")])
        elif name.endswith("-NoResponse.txt"):
            topics.add(name[: -len("-NoResponse.txt")])

    return sorted(topics)


TOPICS = build_topics_from_data_path()
