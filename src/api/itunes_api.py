import requests

ITUNES_GENRE_TRANSLATIONS = {
    "alternativa": "alternative",
    "pop latino": "latin pop",
    "urbano latino": "latin",
    "rock y alternativo": "alternative rock",
    "banda sonora": "soundtrack",
    "festividades": "holiday",
}


def normalize_itunes_genre(genre):
    key = genre.lower().strip()
    return ITUNES_GENRE_TRANSLATIONS.get(key, key)

def get_itunes_genres(artist_id):
    response = requests.get(
        "https://itunes.apple.com/lookup",
        params={
            "id": artist_id,
            "entity": "album",
            "country": "US",
            "lang": "en_us",
            "limit": 200
        }
    )

    response.raise_for_status()

    genres = {
        normalize_itunes_genre(item["primaryGenreName"])
        for item in response.json().get("results", [])
        if item.get("wrapperType") == "collection"
        and item.get("collectionType") == "Album"
        and item.get("primaryGenreName")
    }

    return genres