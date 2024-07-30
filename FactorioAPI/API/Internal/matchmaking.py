import json
import os
import requests


def getGames(username: str, token: str) -> list:
    """
    Gets a list of game servers from the Factorio multiplayer API using the provided username and token
    
    WARNING: This function provides no rate limiting and measures should be taken to prevent spamming

    :param username: The username to authenticate with
    :param token: The authentication token to use
    :return: A list of dicts, each containing information about a game server
    """
    
    request = requests.get(
        "https://multiplayer.factorio.com/get-games",
        params={"username": username, "token": token},
    )

    servers = request.json()

    if not isinstance(servers, list):
        try:
            message = "\n"+servers["message"]
        except:
            message = ""
        raise Exception(f"Failed to get servers{message}")
    return servers
    
def getGameDetails(gameId: str) -> dict:
    """
    Gets the details of a game from the Factorio multiplayer API using the provided gameId
    
    WARNING: This function provides no rate limiting and measures should be taken to prevent spamming

    :param gameId: The id of the game to get details for
    :return: A dict containing information about the game
    """
    request = requests.get(
        f"https://multiplayer.factorio.com/get-game-details/{gameId}",
    )
    return request.json()
