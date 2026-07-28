"""
Constants for topics/roles available in the application.
"""

from constants.paths import DATA_PATH


def build_topics_from_data_path():
    """Build unique topic names from Yes/No response files in static/data."""
    topics = set()

    for file_path in DATA_PATH.glob("*.txt"):
        name = file_path.name

        if name.endswith("-YesResponse.txt"):
            topics.add(name[: -len("-YesResponse.txt")])
        elif name.endswith("-NoResponse.txt"):
            topics.add(name[: -len("-NoResponse.txt")])

    return sorted(topics)


TOPICS = build_topics_from_data_path()
