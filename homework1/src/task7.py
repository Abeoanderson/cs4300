import requests

def get_random_joke():
    """Requests lets you send http requests easily, in this example I am getting a jock from a random joke API"""
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    # error handleing incase call fails or hangs
    response.raise_for_status()
    text = response.json()
    random_joke = f"{text['setup']} - {text['punchline']}"
    return random_joke