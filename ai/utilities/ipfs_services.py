import os
import requests
import json
import asyncio
import re
from dotenv import load_dotenv

load_dotenv()

url = "https://api.tatum.io/v3/ipfs"
TATUM_API_KEY = os.getenv("TATUM_API_KEY")

def extract_image_link(text):
    url_pattern = r"https?://[^\s]+"
    match = re.search(url_pattern, text)
    return match.group(0) if match else None

# Cratea a function to get the last string of the path py / charcters
def get_last_string(path):
    """
    Get the last string of the path by / characters and make sure to remove the space

    Args:
    path (str): The path that you want to get the last string

    Returns:
    str: The last string of the path
    """
    
    try:
      # Call the function and print the result
      return path.split("/")[-1].split(" ")[0]
    
    except Exception as e:
        print(f"Error deploying NFT contract: {str(e)}")


def upload_file_to_ipfs():
    """
    Upload a file to IPFS and return the IPFS hash.

    Returns:
      str: IPFS hash of the uploaded file
    """
    files = { "file": ("data.json", open("data.json", "rb"), "application/json") }
    headers = {
        "accept": "application/json",
        "x-api-key": TATUM_API_KEY
    }
    response = requests.post(url, files=files, headers=headers)
    data = response.json()

    # delete the file
    os.remove("data.json")

    return data["ipfsHash"]

def upload_data_to_ipfs(name, description, image):
    """
    Upload data to IPFS and return the IPFS hash.

    Args:
      name (str): Name of the NFT
      description (str): Description of the NFT
      image (str): URL of the image to upload

    Returns:
      str: IPFS hash of the uploaded data
    """

    data = {
        "name": name,
        "description": description,
        "image": "ipfs://" + get_last_string(image)
    }

    # save data to a file data.json
    with open("data.json", "w") as file:
        json.dump(data, file)
        
    return upload_file_to_ipfs()

# def get_file_from_ipfs(hash):
#     headers = {
#       "accept": "*",
#       "x-api-key": TATUM_API_KEY
#     }

#     response = requests.get(f"{url}/{hash}", headers=headers)
#     print(response.text)

def upload_image_to_ipfs(imageUrl):
    """
    Upload an image to IPFS and return the IPFS hash.

    Args:
      imageUrl (str): URL of the image to upload

    Returns:
      str: IPFS hash of the uploaded image
    """
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

