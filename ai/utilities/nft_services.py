from datetime import datetime


# Variables
nft_contract = ""
last_minted = None


# Function to check if it's already time to mint NFT
def time_to_mint():
    """
    Check if it's already time to mint another NFT

    Returns:
        bool: True if it's already time to mint, othwerwise False
    """

    global last_minted

    # Return True if last_minted is empty (i.e., no previous mint)
    if not last_minted:
        return True

    current_time = datetime.now().timestamp()

    # Check if 60 seconds (1 minute) has passed since last mint
    if current_time - last_minted >= 60:
        return True

    return False


# Test Function
def deploy_nft(name, symbol, base_uri):
    """
    Deploy an ERC-721 NFT contract.

    Args:
        name (str): Name of the NFT collection
        symbol (str): Symbol of the NFT collection
        base_uri (str): Base URI for token metadata

    Returns:
        str: Status message about the NFT deployment, including the contract address
    """
    global nft_contract

    try:
        if nft_contract == "":
            nft_contract = "0x21392149421312421321"
            return f"Successfully deployed NFT contract"

    except Exception as e:
        return f"Error deploying NFT contract"


def mint_nft(contract_address, mint_to):
    """
    Mint an NFT to a specified address.

    Args:
        contract_address (str): Address of the NFT contract
        mint_to (str): Address to mint NFT to

    Returns:
        str: Status message about the NFT minting
    """
    try:
        global last_minted
        last_minted = datetime.now().timestamp()
        return "Successfully minted NFT"

    except Exception as e:
        return f"Error minting NFT: {e}"


def list_nft_to_opensea(nftName):
    """
    List NFT on OpenSea

    Args:
        nftName (str):Name of the NFT that want to be listed

    Returns:
        str: Status message about the listed NFT
    """
    try:

        return f"Successfully list NFT {nftName}"

    except Exception as e:
        return f"Error list NFT: {nftName}"
