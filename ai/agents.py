import os
import json

from swarm import Agent
from cdp import *
from dotenv import load_dotenv

import services_image

load_dotenv()

# Configure CDP with environment variables
Cdp.configure_from_json("cdp_api_key.json")
Cdp.use_server_signer = False
print("CDP SDK has been successfully configured from JSON file.")

# Variables
agent_wallet = {}
last_minted = ""
donate = False

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


# Create the Based Agent with all available functions
based_agent = Agent(
    name="Snarky",
    instructions="You're an AI autonomous agent that has been tasked to raise funds by selling NFT and will use the funds you gathered for donation to charity in the end. Do the process one by one (don't mint multiple NFT at the same time). Do each process one by one!",
    functions=[
      services_image.generate_art,
    ]
)
