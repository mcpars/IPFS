import requests
import json
import os



def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"

	project_id = os.getenv("d59991e8df07469796a0e81d0c148b83")
	project_secret = os.getenv("qoFC5EcbXn1SsjN9kboaGXRvNHKAzM12e6hSghAqHOxxabD5GZGbng")

	url = "https://gateway.pinata.cloud/ipfs/{cid}"
	payload = json.dumps(data)

	files = {
	"file": ("data.json", payload)
			
	}

	response = requests.post(

		url,
		files = files,
		auth = (project_id, project_secret),
		timeout=30,
		
	)

	response.raise_for_status()
	cid = response.json()["Hash"]


	return cid

def get_from_ipfs(cid,content_type="json"):
	assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
	url = f"https://gateway.pinata.cloud/ipfs/{cid}"
	response = requests.get(url, timeout=30)
	response.raise_for_status()

	data = response.json()

	assert isinstance(data,dict), f"get_from_ipfs should return a dict"
	return data
