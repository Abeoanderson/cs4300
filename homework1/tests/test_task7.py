from src.task7 import get_random_joke

#since the joke api returns a new joke each time, I am mocking the  request in my test
class mock_response:
    def raise_for_status(self):
        pass

    def json(self):
        return {
            "setup": "What did Michael Jackson name his denim store?",
            "punchline": "Billy Jeans!"
        }

def test_random_joke(monkeypatch):
    def mock_get(*args, **kwargs):
        return mock_response()
    # replaces requests.get call with mock_get() so we can get our mock joke 
    monkeypatch.setattr("requests.get", mock_get)

    joke = get_random_joke()

    assert isinstance(joke, str)
    assert "Michael Jackson" in joke
