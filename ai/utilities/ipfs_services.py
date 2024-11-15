import os
import requests
import json
import asyncio
import re
from dotenv import load_dotenv

load_dotenv()

url = "https://api.tatum.io/v3/ipfs"
TATUM_API_KEY = os.getenv("TATUM_API_KEY")
print("TATUM_API_KEY: ", TATUM_API_KEY)

def extract_image_link(text):
    url_pattern = r"https?://[^\s]+"
    match = re.search(url_pattern, text)
    return match.group(0) if match else None


def upload_file_to_ipfs():
    files = { "file": ("data.json", open("data.json", "rb"), "application/json") }
    headers = {
        "accept": "application/json",
        "x-api-key": TATUM_API_KEY
    }
    response = requests.post(url, files=files, headers=headers)
    data = response.json()
    print(data)

    # delete the file
    os.remove("data.json")

    return data["ipfsHash"]

def upload_data_to_ipfs(name, description, image):
    data = {
        "name": name,
        "description": description,
        "image": image
    }

    # save data to a file data.json
    with open("data.json", "w") as file:
        json.dump(data, file)
        
    return upload_file_to_ipfs()

def get_file_from_ipfs(hash):
    headers = {
      "accept": "*",
      "x-api-key": TATUM_API_KEY
    }

    response = requests.get(f"{url}/{hash}", headers=headers)
    print(response.text)

def upload_image_to_ipfs(imageUrl):
    extracted = extract_image_link(imageUrl)
    # Download the image and save it as a file named image.png
    response = requests.get(extracted)
    with open("image.png", "wb") as file:
        file.write(response.content)
    
    # Upload the image to IPFS
    files = { "file": ("image.png", open("image.png", "rb"), "image/png") }
    headers = {
        "accept": "application/json",
        "x-api-key": TATUM_API_KEY
    }

    response = requests.post(url, files=files, headers=headers)
    data = response.json()
    # delete the file
    os.remove("image.png")

    return data["ipfsHash"]

async def generate_nft_metadata(name, description,imageResult):
    """
    Generate NFT metadata and upload it to IPFS.

    Args:
        name (str): Name of the NFT
        description (str): Description of the NFT
        imageResult (str): Image URL of the NFT
    
    Returns:
        Metadata IPFS hash
    """
    imageLink = upload_image_to_ipfs(imageResult)
    await asyncio.sleep(1)
    print("Image Link: ", imageLink)
    ipfsHash = upload_data_to_ipfs(name, description, imageLink)
    await asyncio.sleep(5)
    return ipfsHash

