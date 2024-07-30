import json
import os
import requests


def getToken(username: str, password: str, emailCode: str = "") -> str:
    """
    Get a token for the Factorio web API.

    WARNING: This function provides no rate limiting and measures should be taken to prevent spamming

    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        emailCode (str, optional): The email code obtained from the email sent to the user. Defaults to "".

    Returns:
        str: The token obtained from the API.
    """
    request = requests.post(
        "https://auth.factorio.com/api-login",
        params={"username": username, "password": password, "email_code": emailCode},
        headers={"Content-Type": "application/json"},
        timeout=10,
        verify=True,
    )
    data: dict = request.json()
    # print(json.dumps(request.json(),indent=4))
    request.close()
    try:
        if data.get("error", None) is not None:
            raise Exception(data["error"] + "\n" + data["message"])
    except AttributeError:
        return data[0]
