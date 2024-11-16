import requests
import time
from datetime import datetime
import os
import json
from cdp import *
from dotenv import load_dotenv

load_dotenv()

url = "https://api.tatum.io/v3/ipfs"

# Configure CDP with environment variables
Cdp.configure_from_json("cdp_api_key.json")
Cdp.use_server_signer = False
print("CDP SDK has been successfully configured from JSON file.")

# Variables
agent_wallet = {}

def get_first_string_data(data):
    # Assuming 'data' is the dictionary containing the JSON
    first_key = list(data.keys())[0]  # Get the first key in the dictionary
    first_data = data[first_key]  # Access the first element's value
    # print(first_data)
    print(first_key)
    return first_key


wallet_data_path = "wallet_seed.json"
if os.path.exists(wallet_data_path):
    # Load existing wallet data
    with open(wallet_data_path, "r") as file:
        wallet_dict = json.load(file)
        print("Loaded existing wallet data.")
        wallet_id = get_first_string_data(wallet_dict)

        agent_wallet = Wallet.fetch(wallet_id)
        agent_wallet.load_seed("wallet_seed.json")
        print(agent_wallet.addresses)
else:
    # Create a new wallet and save it to the file
    print("start")
    agent_wallet = Wallet.create(network_id="base-sepolia")
    print(agent_wallet.addresses)
    print("end")
    agent_wallet.save_seed("wallet_seed.json", encrypt=False)
    print("Created new wallet and saved data.")

    # Request faucet
    faucet = agent_wallet.faucet()
    print(f"Faucet transaction: {faucet}")
    print(f"Agent wallet address: {agent_wallet.default_address.address_id}")


# Replace these with your values
NFT_CONTRACT_ADDRESS = "0x1234567890abcdef1234567890abcdef12345678"  # Dummy contract
NFT_TOKEN_ID = "1"  # Token ID of your NFT
SELLER_ADDRESS = "0xabcdef1234567890abcdef1234567890abcdef12"  # Your wallet address
START_PRICE = "0.1"  
EXPIRATION_TIME = int(time.time()) + 7 * 24 * 60 * 60  # 7 days from now
OPENSEA_API_URL = "https://testnets-api.opensea.io/v2/orders/base_sepolia/seaport/listings"


def list_nft_to_opensea():
    # Build the request payload
    params = {
            "offerer": SELLER_ADDRESS,
            "offer": [
                {
                    "itemType": 2,  # ERC-721
                    "token": NFT_CONTRACT_ADDRESS,
                    "identifierOrCriteria": NFT_TOKEN_ID,
                    "startAmount": "1",
                    "endAmount": "1",
                }
            ],
            "consideration": [
                {
                    "itemType": 0,  # ETH
                    "token": "0x0000000000000000000000000000000000000000",
                    "identifierOrCriteria": "0",
                    "startAmount": str(int(float(START_PRICE) * 10**18)),  # Convert ETH to Wei
                    "endAmount": str(int(float(START_PRICE) * 10**18)),
                    "recipient": SELLER_ADDRESS,
                }
            ],
            "startTime": int(time.time()),
            "endTime": EXPIRATION_TIME,
            "orderType": 2,  # Full open order
            "zone": "0x0000000000000000000000000000000000000000",  # No zone
            "zoneHash": "0x" + "0" * 64,  # Empty zone hash
            "salt": str(int(time.time())),  # Unique salt
            "conduitKey": "0x" + "0" * 64,  # Default conduit
            "totalOriginalConsiderationItems": 1,
        },
    
    payload = {
        "parameters": params,
        "signature": agent_wallet.sign_payload("0xe2b143ff3c2965cdb3a6f40148217e009d34212c9fb3d73ab3ac7ef347615925")
    }
    
    # Make the API request
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(
        OPENSEA_API_URL,
        headers=headers,
        data=json.dumps(payload),
    )

    # Handle the response
    if response.status_code == 201:
        print("NFT listed successfully!")
        print(response.json())
    else:
        print("Failed to list NFT:")
        print(response.status_code, response.text)
    

print(list_nft_to_opensea())