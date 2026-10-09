import os
import requests
from dotenv import load_dotenv

load_dotenv()

APPLE_TOKEN = os.getenv("APPLE_TOKEN")
STOREFRONT = "US"

BASE_URL = "https://api.music.apple.com"

HEADERS = {
    "Authorization": f"Bearer {APPLE_TOKEN}"
}

def search_artist(artist_name):
    url = f"{BASE_URL}/v1/catalog/{STOREFRONT}/search"

    params = {
        "term": artist_name,
        "types": "artists",
        "limit": 25
    }

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()

    artists = (
        response.json()
        .get("results", {})
        .get("artists", {})
        .get("data", [])
    )

    if not artists:
        raise ValueError(f"Artist not found: {artist_name}")

    return artists[0]


def get_paginated_view(artist_id, view):
    url = (
        f"{BASE_URL}/v1/catalog/{STOREFRONT}/artists/"
        f"{artist_id}/view/{view}"
    )

    params = {"limit": 100}
    albums = []

    while url:
        response = requests.get(
            url,
            headers=HEADERS,
            params=params
        )

        # No featured albums available → valid empty result
        if response.status_code == 404 and view == "featured-albums":
            return []

        response.raise_for_status()

        data = response.json()
        albums.extend(data.get("data", []))

        next_page = data.get("next")

        if next_page:
            url = next_page if next_page.startswith("http") else BASE_URL + next_page
            params = None
        else:
            url = None

    return albums


def get_artist_data(artist_name):
    artist = search_artist(artist_name)

    artist_id = artist["id"]

    albums = get_paginated_view(
        artist_id,
        "full-albums"
    )

    genres = set()
    dates = set()

    for album in albums:

        attributes = album.get("attributes", {})
        release_date = attributes.get("releaseDate")

        if release_date:
            dates.add(release_date)

    featured_albums = get_paginated_view(
        artist_id,
        "featured-albums"
    )

    golden_dates = set()

    for album in featured_albums:

        release_date = (
            album
            .get("attributes", {})
            .get("releaseDate")
        )

        if release_date:
            golden_dates.add(release_date)

    return {
        "artist_id": artist_id,
        "dates": dates,
        "golden_dates": golden_dates
    }