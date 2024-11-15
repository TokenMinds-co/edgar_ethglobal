import os
import json
from swarm import Agent
from cdp import *
from dotenv import load_dotenv
import utilities.nft_services as nft_services
import utilities.image_services as image_services
import utilities.twitter_services as twitter_services


load_dotenv()

# Configure CDP with environment variables
Cdp.configure_from_json("cdp_api_key.json")
Cdp.use_server_signer = False
print("CDP SDK has been successfully configured from JSON file.")

# Variables
agent_wallet = {}

def get_first_string_data(data):
    # Assuming 'data' is the dictionary containing the JSON
    first_key = list(data.keys())[0]  # Get the first key in the dictionary
    return first_key


wallet_data_path = "wallet_seed.json"
if os.path.exists(wallet_data_path):
    # Load existing wallet data
    with open(wallet_data_path, "r") as file:
        wallet_dict = json.load(file)
        print("Loaded existing wallet data.\n")
        wallet_id = get_first_string_data(wallet_dict)

        agent_wallet = Wallet.fetch(wallet_id)
        agent_wallet.load_seed("wallet_seed.json")
        # print(agent_wallet.addresses)
else:
    # Create a new wallet and save it to the file
    print("Wallet not found, creating new walllet.\n")
    agent_wallet = Wallet.create(network_id="base-sepolia")

    agent_wallet.save_seed("wallet_seed.json", encrypt=False)
    print("Created new wallet and saved data.")

    # Request faucet
    faucet = agent_wallet.faucet()
    print(f"Requesting faucet..")
    print(f"Faucet transaction: {faucet}")
    print(f"Agent wallet address: {agent_wallet.default_address.address_id}")


# Create the Based Agent with all available functions
snarky = Agent(
    name="Snarky",
    instructions="You're an AI autonomous agent named Snarky. You've been tasked to raise funds by selling NFT and will use the funds you gathered for donation to charity in the end. You can deploy a nft contract if it's not yet deployed, mint a NFT using the deployed contract (but check first if it's already time to mint or not), list the NFT you've minted to OpenSea, and then post/market that NFT on Twitter. Do each process one by one! (don't mint multiple NFT at the same time).",
    functions=[
        nft_services.deploy_nft,
        nft_services.time_to_mint,
        nft_services.mint_nft,
        nft_services.list_nft_to_opensea,
        twitter_services.post_nft_on_twitter,
        # image_services.generate_art,
    ],
)
