from faucet.scrape import get_mentions, parse_mention_text, get_networks_and_addresses, TWEEPY_API
import pytest


def test_get_mentions(monkeypatch):
    """Test get_mentions."""
    def search_30_day(*args, **kwargs):
        return [
            {
                "id": 1,
                "user": {"screen_name": "testuser"},
                "text": "test text",
            },
            {
                "id": 2,
                "user": {"screen_name": "testuser"},
                "text": "test text",
            },
        ]

    monkeypatch.setattr("faucet.scrape.TWEEPY_API.search_30_day", search_30_day)

    mentions = get_mentions(label="test", from_date=1, api=TWEEPY_API, username="testuser")
    assert len(mentions) == 2


# @pytest.mark.skip()
def test_parse_mention_text():
    """Test parse_mention_text."""
    chain_id, address = parse_mention_text("test text 80001 0x123")
    assert chain_id == 80001
    assert address is None

    chain_id, address = parse_mention_text("test text 82345 blah 0x5134c5a32bf3a492A2007D55E9a98d91C1eCEb6d")
    assert chain_id is None
    assert address == "0x5134c5a32bf3a492A2007D55E9a98d91C1eCEb6d"

    chain_id, address = parse_mention_text("test text 82345 blah 0x1234 asdfasdf 7890")
    assert chain_id is None
    assert address is None


def test_get_networks_and_addresses(monkeypatch):
    """Test get_networks_and_addresses."""
    class Mention:
        def __init__(self, text):
            self.text = text

    def search_30_day(*args, **kwargs):
        return [
            Mention("test text 5 0x123"),
            Mention("test text 80001 0x5134c5a32bf3a492A2007D55E9a98d91C1eCEb6d"),
            Mention("test text 1234 0x5134c5a32bf3a492A2007D55E9a98d91C1eCEb6d"),

        ]

    monkeypatch.setattr("faucet.scrape.TWEEPY_API.search_30_day", search_30_day)

    mentions = get_mentions(label="test", from_date=1, api=TWEEPY_API, username="testuser")
    faucet_requests = get_networks_and_addresses(mentions)
    assert faucet_requests == [(80001, "0x5134c5a32bf3a492A2007D55E9a98d91C1eCEb6d")]
