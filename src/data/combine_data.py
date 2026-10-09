from src.data.filter_data import filter_tags, filter_dates

def combine_artist_data(apple_data, itunes_genres, lastfm_data, artist_input):
    tags = lastfm_data.get("tags") or []
    filtered_genres = ", ".join(sorted(filter_tags(itunes_genres, tags)))

    min_date, max_date = filter_dates(apple_data.get("dates"))
    min_golden_date, max_golden_date = filter_dates(apple_data.get("golden_dates"))

    artist_name = (
            apple_data.get("artist_name_apple")
            or lastfm_data.get("artist_name_lastfm")
            or artist_input.get("artist_name")
    )

    return {
        "id_apple": apple_data.get("artist_id"),
        "id_lastfm": lastfm_data.get("id_lastfm"),
        "artist_name": artist_name,
        "listeners": lastfm_data.get("listeners"),
        "genres": filtered_genres,
        "min_date": min_date,
        "max_date": max_date,
        "min_golden_date": min_golden_date,
        "max_golden_date": max_golden_date,
        "language": artist_input.get("language"),
    }