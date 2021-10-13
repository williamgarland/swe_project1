import os
import requests


def get_genius_token() -> str:
    """
    Returns the token used to make Genius API calls.
    This token is stored as an environment variable, and if the variable does not exist, this function will return None.
    """
    return os.getenv("GENIUS_ACCESS_TOKEN")


def get_genius_lyrics_url(track_title: str, primary_artist_name: str) -> str:
    """
    Returns a URL to the Genius page for the lyrics of the specified track.
    If there was an error making any of the Genius API calls or the returned data was malformed, this function will throw an exception.
    """
    token = get_genius_token()

    if token == None:
        raise Exception()

    base_url = "https://api.genius.com/search"

    response = requests.get(
        base_url,
        headers={"Authorization": "Bearer " + token},
        params={"q": track_title},
    )

    if response.status_code != 200:
        raise Exception()

    target = None

    for hit in response.json()["response"]["hits"]:
        if (
            primary_artist_name.lower()
            in str(hit["result"]["primary_artist"]["name"]).lower()
        ):
            target = hit
            break

    if not target:
        raise Exception()

    return target["result"]["url"]
