import requests
import json
import os

def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"

    jwt = os.getenv("PINATA_JWT")
    if not jwt:
        # Optional fallback if your course uses key/secret instead of JWT
        api_key = os.getenv("PINATA_API_KEY")
        api_secret = os.getenv("PINATA_API_SECRET")
        if not (api_key and api_secret):
            raise RuntimeError("Missing Pinata credentials: set PINATA_JWT (recommended) or PINATA_API_KEY + PINATA_API_SECRET")

        url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
        headers = {"pinata_api_key": api_key, "pinata_secret_api_key": api_secret}
        r = requests.post(url, json=data, headers=headers, timeout=30)
    else:
        url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
        headers = {"Authorization": f"Bearer {jwt}"}
        r = requests.post(url, json=data, headers=headers, timeout=30)

    r.raise_for_status()
    cid = r.json()["IpfsHash"]
    return cid


def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), "get_from_ipfs accepts a cid in the form of a string"

    # Gateway fetch (no auth needed)
    url = f"https://gateway.pinata.cloud/ipfs/{cid}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()

    data = r.json()
    assert isinstance(data, dict), "get_from_ipfs should return a dict"
    return data
