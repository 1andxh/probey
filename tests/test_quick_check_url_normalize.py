import pytest
from src.public_tools.utils import normalize_public_url


def test_normalize_public_url():
    assert normalize_public_url("google.com") == "https://google.com"

    assert normalize_public_url("https://google.com/") == "https://google.com"

    assert normalize_public_url("not-url") == "https://not-url.com"

    assert normalize_public_url(None) == ""
