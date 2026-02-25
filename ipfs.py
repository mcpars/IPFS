import requests
import json
import os

def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"

    # Prefer JWT if available (easiest)
    jwt = os.getenv("PINATA_JWT")
    
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {"Authorization": f"Bearer {jwt}"}

       

    r = requests.post(url, json=data, headers=headers, timeout=30)

    r.raise_for_status()
    cid = r.json()["IpfsHash"]
    return cid


def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), "get_from_ipfs accepts a cid in the form of a string"

    # Gateway fetch (no auth required)
    gateways = [
        f"https://gateway.pinata.cloud/ipfs/{cid}",
        f"https://ipfs.io/ipfs/{cid}",
        f"https://cloudflare-ipfs.com/ipfs/{cid}",
    ]

    last_err = None
    for url in gateways:
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            data = r.json()
            assert isinstance(data, dict), "get_from_ipfs should return a dict"
            return data
        except Exception as e:
            last_err = e

    raise RuntimeError(f"Failed to fetch CID {cid} from gateways. Last error: {last_err}")
