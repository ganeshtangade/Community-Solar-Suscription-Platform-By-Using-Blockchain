import json
import os

from web3 import Web3
from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


BLOCKCHAIN_RPC_URL = os.getenv(
    "BLOCKCHAIN_RPC_URL"
)

CONTRACT_ADDRESS = os.getenv(
    "BLOCKCHAIN_CONTRACT_ADDRESS"
)

PRIVATE_KEY = os.getenv(
    "BLOCKCHAIN_PRIVATE_KEY"
)


# =========================================================
# CONNECT TO GANACHE
# =========================================================

w3 = Web3(
    Web3.HTTPProvider(
        BLOCKCHAIN_RPC_URL
    )
)


# =========================================================
# LOAD ABI
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

ABI_PATH = os.path.join(
    BASE_DIR,
    "blockchain",
    "abi.json"
)


with open(
    ABI_PATH,
    "r"
) as file:

    CONTRACT_ABI = json.load(file)


# =========================================================
# CONTRACT
# =========================================================

contract = w3.eth.contract(

    address=Web3.to_checksum_address(
        CONTRACT_ADDRESS
    ),

    abi=CONTRACT_ABI
)


# =========================================================
# CHECK CONNECTION
# =========================================================

def is_blockchain_connected():

    return w3.is_connected()


# =========================================================
# RECORD ENERGY ALLOCATION
# =========================================================

def record_energy_allocation(

    allocation_id,

    generation_id,

    subscription_id,

    allocated_kwh

):

    if not w3.is_connected():

        raise Exception(
            "Blockchain is not connected"
        )


    if not PRIVATE_KEY:

        raise Exception(
            "BLOCKCHAIN_PRIVATE_KEY is not configured"
        )


    # Get wallet address from private key
    account = w3.eth.account.from_key(
        PRIVATE_KEY
    )

    wallet_address = account.address


    # Convert kWh to Wh
    energy_wh = int(
        round(
            allocated_kwh * 1000
        )
    )


    # Get current nonce
    nonce = w3.eth.get_transaction_count(
        wallet_address
    )


    # Build transaction
    transaction = contract.functions.recordAllocation(

        allocation_id,

        generation_id,

        subscription_id,

        energy_wh

    ).build_transaction({

        "from": wallet_address,

        "nonce": nonce,

        "gas": 300000,

        "gasPrice": w3.eth.gas_price

    })


    # Sign transaction
    signed_transaction = w3.eth.account.sign_transaction(

        transaction,

        private_key=PRIVATE_KEY

    )


    # Send transaction
    transaction_hash = w3.eth.send_raw_transaction(

        signed_transaction.raw_transaction

    )


    # Wait for blockchain confirmation
    receipt = w3.eth.wait_for_transaction_receipt(

        transaction_hash

    )


    return {

        "transaction_hash":
            transaction_hash.hex(),

        "block_number":
            receipt["blockNumber"],

        "status":
            receipt["status"]

    }