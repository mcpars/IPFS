import requests
import json
import os

def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"

	project_id = os.getenv("INFURA_IPFS_PROJECT_ID")
	project_secret = os.getenv("INFURA_IPFS_PROJECT_SECRET")

	url = "https://ipfs.infura.io:5001/api/v0/add"
	payload = json.dumps(data)

	files = {
	"file": ("data.json", payload, "application/json")
			
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
	url = f"https://ipfs.io/ipfs/{cid}"
	response = requests.get(url, timeout=30)
	response.raise_for_status()

	data = response.json()

	assert isinstance(data,dict), f"get_from_ipfs should return a dict"
	return data
