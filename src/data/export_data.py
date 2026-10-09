import csv
import time
from pathlib import Path

import pandas as pd

from src.api.applemusic_api import get_artist_data
from src.api.itunes_api import get_itunes_genres
from src.api.lastfm_api import get_lastfm_artist
from src.data.combine_data import combine_artist_data


INPUT_FILE = "../data/input/search_data"
OUTPUT_FILE = "../data/output/artists.csv"
ERRORS_FILE = "../data/output/errors.csv"


FINAL_COLUMNS = [
    "id_apple",
    "id_lastfm",
    "artist_name",
    "listeners",
    "genres",
    "min_date",
    "max_date",
    "min_golden_date",
    "max_golden_date",
    "language",
]


def read_artists_txt(filepath):
    artists = []

    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            if not row:
                continue

            artist_name = row[0].strip()

            if not artist_name or artist_name.startswith("#"):
                continue

            language = row[1].strip() if len(row) > 1 else None

            artists.append({
                "artist_name": artist_name,
                "language": language,
            })

    return artists


def export():
    Path("../data/output").mkdir(exist_ok=True)

    artists = read_artists_txt(INPUT_FILE)

    final_rows = []
    error_rows = []

    for index, artist_input in enumerate(artists, start=1):
        artist_name = artist_input["artist_name"]

        print(f"[{index}/{len(artists)}] Processing: {artist_name}")

        apple_data = {}
        itunes_genres = set()
        lastfm_data = {}

        apple_error = None
        itunes_error = None
        lastfm_error = None

        try:
            apple_data = get_artist_data(artist_name)
        except Exception as e:
            apple_error = str(e)

            apple_data = {
                "artist_id": None,
                "artist_name_apple": None,
                "dates": set(),
                "golden_dates": set(),
            }

        try:
            itunes_genres = get_itunes_genres(apple_data["artist_id"])
        except Exception as e:
            itunes_error = str(e)
            itunes_genres = set()

        try:
            lastfm_data = get_lastfm_artist(artist_name)
        except Exception as e:
            lastfm_error = str(e)

            lastfm_data = {
                "id_lastfm": None,
                "artist_name_lastfm": None,
                "listeners": None,
                "tags": [],
            }

        final_row = combine_artist_data(
            apple_data=apple_data,
            itunes_genres=itunes_genres,
            lastfm_data=lastfm_data,
            artist_input=artist_input,
        )

        final_rows.append(final_row)

        if apple_error or itunes_error or lastfm_error:
            error_rows.append({
                "artist_name": artist_name,
                "language": artist_input.get("language"),
                "apple_error": apple_error,
                "itunes_error": itunes_error,
                "lastfm_error": lastfm_error,
            })

        time.sleep(0.3)

    df = pd.DataFrame(
        final_rows,
        columns=FINAL_COLUMNS
    )

    date_columns = [
        "min_date",
        "max_date",
        "min_golden_date",
        "max_golden_date",
    ]

    df[date_columns] = df[date_columns].astype("Int64")

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )

    print(f"\nCSV saved in: {OUTPUT_FILE}")

    if error_rows:
        errors_df = pd.DataFrame(error_rows)
        errors_df.to_csv(
            ERRORS_FILE,
            index=False,
            encoding="utf-8"
        )
        print(f"Some artists gave errors. Check: {ERRORS_FILE}")