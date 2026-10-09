import re
import unicodedata
from pathlib import Path

from src.graph.genre_utils import get_macrogenres

def normalize_tag(tag):
    tag = tag.lower().strip()

    tag = unicodedata.normalize("NFKD", tag)
    tag = "".join(c for c in tag if not unicodedata.combining(c))

    tag = re.sub(r"\s+", " ", tag)

    return tag

def get_allowed_tags(filepath = "../data/input/allowed_tags"):
    allowed_tags = set()

    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(
            f"No existe {filepath}. Crea el archivo con los tags permitidos."
        )

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            tag = line.strip()

            if not tag:
                continue

            if tag.startswith("#"):
                continue

            allowed_tags.add(normalize_tag(tag))

    return allowed_tags

def filter_tags(macrogenres, tags):
    allowed_tags = get_allowed_tags()

    filtered_macrogenres = set()
    for genre in macrogenres:
        if normalize_tag(genre) in allowed_tags:
            filtered_macrogenres.add(normalize_tag(genre))

    filtered_tags = set()
    for genre in tags:
        if normalize_tag(genre) in allowed_tags:
            filtered_tags.add(normalize_tag(genre))

    final_tags = set()
    represented_macrogenres = set()
    for tag in filtered_tags:
        tag_macrogenres = {
            normalize_tag(genre)
            for genre in get_macrogenres(tag)
        }

        intersection = tag_macrogenres & filtered_macrogenres

        if intersection:
            final_tags.add(tag)
            represented_macrogenres.update(intersection)

    missing_macrogenres = filtered_macrogenres - represented_macrogenres
    final_tags.update(missing_macrogenres)

    return final_tags


def filter_dates(dates):
    if not dates:
        return None, None

    years = {int(date[:4]) for date in dates}

    return min(years), max(years)