import requests
import json
import os

def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"

    # Prefer JWT if available (easiest)
    jwt = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiIyZWRmYzFlZC03ZjZmLTRmYmYtYWIzMS0xZWVkMjE2MmViZDciLCJlbWFpbCI6Im1jcGFyc0BzZWFzLnVwZW5uLmVkdSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6IkZSQTEifSx7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6Ik5ZQzEifV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiJiZTJkOWFmYmJkMjg4ZDllZWZiNCIsInNjb3BlZEtleVNlY3JldCI6IjQ4ZTQzNWQyNGRjNTNiY2ZhMGNlNWI0NjM3MjA1ZjA4MmUyZTVkZDRkZjY5ZDg5ZWIyNzQwN2FiMjQyZTBiNzIiLCJleHAiOjE4MDM1MjEyMDF9.9eh9pXfQkFt1pupL8vgvRb6fVsN3fv85cPHN5aGAihc")

    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"


       

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
