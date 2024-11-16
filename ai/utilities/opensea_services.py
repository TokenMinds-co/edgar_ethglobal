import requests
import time
import json

# Replace these with your values
NFT_CONTRACT_ADDRESS = "0x1234567890abcdef1234567890abcdef12345678"  # Dummy contract
NFT_TOKEN_ID = "1"  # Token ID of your NFT
SELLER_ADDRESS = "0xabcdef1234567890abcdef1234567890abcdef12"  # Your wallet address
START_PRICE = "0.1"  
EXPIRATION_TIME = int(time.time()) + 7 * 24 * 60 * 60  # 7 days from now
OPENSEA_API_URL = "https://testnets-api.opensea.io/v2/orders/base_sepolia/seaport/listings"


def list_nft_to_opensea():
    # Build the request payload
    payload = {
        "parameters": {
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
        "signature": "0x",  # Placeholder; add signed data later
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
    





