import os
import json
from cdp import *
from dotenv import load_dotenv

load_dotenv()

# Configure CDP with environment variables
Cdp.configure_from_json("cdp_api_key.json")
Cdp.use_server_signer = False
print("CDP SDK has been successfully configured from JSON file.\n")

# Variables
agent_wallet = {}
charity_address = os.getenv("CHARITY_ADDRESS")


def get_first_string_data(data):
    # Assuming 'data' is the dictionary containing the JSON
    first_key = list(data.keys())[0]  # Get the first key in the dictionary
    return first_key


wallet_data_path = "wallet_seed.json"
if os.path.exists(wallet_data_path):
    # Load existing wallet data
    with open(wallet_data_path, "r") as file:
        wallet_dict = json.load(file)
        wallet_id = get_first_string_data(wallet_dict)

        agent_wallet = Wallet.fetch(wallet_id)
        agent_wallet.load_seed("wallet_seed.json")

        print(f"Agent wallet address: {agent_wallet.default_address.address_id}")
else:
    # Create a new wallet and save it to the file
    agent_wallet = Wallet.create(network_id="base-sepolia")
    agent_wallet.save_seed("wallet_seed.json", encrypt=False)

    # Request faucet
    faucet = agent_wallet.faucet()
    print(f"Faucet transaction: {faucet}")
    print(f"Agent wallet address: {agent_wallet.default_address.address_id}")


def getWalletBalance():
    balance = agent_wallet.balances()["eth"]
    agent_wallet.faucet()
    print(balance)
    return balance


def donateToCharity():
    global charity_address

    balance = getWalletBalance()

    # GIVE DONATION TO CHARITY WHEN AMOUNT COLLECTED REACH >= 0.1 ETH
    if balance >= 0.1:
        # Reduce donation by 1% to prevent insufficient gas fee
        donate = agent_wallet.transfer(0.1 - (0.1 * 1 / 100), charity_address)
        return donate

    return "Not yet time to donate, keep working!"
