def combine_artist_data(spotify_data, lastfm_data, artist_input):
    tags = lastfm_data.get("tags") or []

    if isinstance(tags, list):
        genres = ", ".join(tags)
    else:
        genres = tags

    artist_name = (
            spotify_data.get("artist_name_spotify")
            or lastfm_data.get("artist_name_lastfm")
            or artist_input.get("artist_name")
    )

    return {
        "id_spoti": spotify_data.get("id_spoti"),
        "id_lastfm": lastfm_data.get("id_lastfm"),
        "artist_name": artist_name,
        "listeners": lastfm_data.get("listeners"),
        "popularity": spotify_data.get("popularity"),
        "genres": genres,
        "start_date": artist_input.get("start_date"),
        "language": artist_input.get("language"),
    }