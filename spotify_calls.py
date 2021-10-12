import base64
import os
import requests
from random import randrange

__spotify_root_endpoint = "https://api.spotify.com/v1/"
__spotify_track_embed_url = "https://open.spotify.com/embed/track/"


def get_spotify_token() -> str:
    """
    Returns a valid spotify token that can be used to make subsequent non-user-related calls.
    If the request could not be completed, the status code was not 200, or the JSON data was malformed,
    this function will throw an exception.

    This function requires two environment variables to be defined: SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET.
    Make sure these variables have been defined before calling this function, otherwise an exception will be thrown!
    """
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if client_id == None:
        raise Exception("Invalid Spotify client ID")
    if client_secret == None:
        raise Exception("Invalid Spotify client secret")

    message = base64.b64encode(f"{client_id}:{client_secret}".encode("ascii")).decode(
        "ascii"
    )
    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": "Basic " + message}
    data = {"grant_type": "client_credentials"}
    result = requests.post(url=url, headers=headers, data=data)

    if result.status_code != 200:
        raise Exception(
            "Error retrieving Spotify token (response: " + str(result.status_code) + ")"
        )

    text = result.json()

    if not "access_token" in text.keys():
        raise Exception("Malformed response from server")

    return text["access_token"]


def get_json(endpoint, token=None, params={}) -> object:
    """
    Returns JSON data from the specified GET request.

    If the request could not be completed, the status code was not 200, or the JSON data was malformed,
    this function will throw an exception.
    """
    if token == None:
        token = get_spotify_token()
    result = requests.get(
        __spotify_root_endpoint + endpoint,
        headers={"Authorization": "Bearer " + token},
        params=params,
    )

    if result.status_code != 200:
        raise Exception(
            "Error retrieving data (response: " + str(result.status_code) + ")"
        )

    return result.json()


def get_artist_top_tracks(artist_id, token=None) -> list[dict[str, object]]:
    """
    Returns the list of the top tracks of the artist with the specified artist ID.

    This function will throw an exception if the tracks could not be retrieved.
    """

    data = get_json(
        "artists/" + artist_id + "/top-tracks", token, params={"market": "US"}
    )

    tracks = []

    for track in data["tracks"]:
        tracks.append(track)
    return tracks


def get_random_artist_tracks(artist_id, token=None, limit=5) -> list[dict[str, str]]:
    """
    Returns a list of random tracks from the specified artist's list of top tracks.
    By default, up to 5 random tracks will be returned.

    This function will throw an exception if the tracks could not be retrieved.
    """

    tracks = get_artist_top_tracks(artist_id, token)

    result = []
    chosen_indices = []
    for i in range(0, len(tracks)):
        index = randrange(len(tracks))
        tries = 0
        while index in chosen_indices:
            index = randrange(len(tracks))
            tries += 1
            if tries > 10:
                # If we've already tried 10 times to get a random index and it still doesn't work, just skip this one
                index = -1
                break
        if index == -1:
            continue
        chosen_indices.append(index)
        result.append({"url": __spotify_track_embed_url + tracks[index]["id"]})

        if len(result) == limit:
            break
    return result


def get_artist_info(artist_id, token=None) -> dict[str, object]:
    """
    Returns the artist object for the artist with the specified ID.

    This function will throw an exception if the artist could not be retrieved.
    """

    artist = get_json("artists/" + artist_id, token)
    return artist


def get_related_artists(artist_id, token=None, limit=5) -> list[dict[str, str]]:
    """
    Returns a list of random artists representing the related artists to the specified artist.
    By default, up to 5 random artists will be returned.

    This function will throw an exception if the artists could not be retrieved.
    """

    related = get_json(
        "artists/" + artist_id + "/related-artists", token, params={"market": "US"}
    )

    result = []
    chosen_indices = []
    for i in len(related):
        index = randrange(len(related))
        tries = 0
        while index in chosen_indices:
            index = randrange(len(related))
            tries += 1
            if tries > 10:
                # If we've already tried 10 times to get a random index and it still doesn't work, just skip this one
                index = -1
                break
        if index == -1:
            continue
        chosen_indices.append(index)
        current_artist_id = related[index]["id"]
        top_tracks = related(current_artist_id, token)
        track_id = top_tracks(randrange(len(top_tracks)))
        result.append(
            {
                "artist_id": current_artist_id,
                "track_url": __spotify_track_embed_url + track_id,
            }
        )

        if len(result) == limit:
            break
    return result
