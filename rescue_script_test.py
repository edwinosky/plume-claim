import os
from web3 import Web3

# --- 1. CONFIGURATION ---
PROVIDER_URL = "https://rpc.plume.org/"
w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))

COMPROMISED_PK = ""
SECURE_PK = ""

if not COMPROMISED_PK or not SECURE_PK:
    raise Exception("ERROR! Private keys are not set as environment variables. Aborting for security.")

safe_wallet_address = w3.eth.account.from_key(SECURE_PK).address

DISTRIBUTOR_ADDRESS = "0xA6d5766b0AA22967Cd03FDC5C11AA81304A9D6B1"
DISTRIBUTOR_ABI = '[{"inputs":[{"internalType":"bytes32[]","name":"_proof","type":"bytes32[]"},{"internalType":"bytes","name":"_signature","type":"bytes"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"address","name":"_onBehalfOf","type":"address"}],"name":"claim","outputs":[],"stateMutability":"payable","type":"function"}]'
distributor_contract = w3.eth.contract(address=DISTRIBUTOR_ADDRESS, abi=DISTRIBUTOR_ABI)

# --- 2. DIAGNOSTIC SCRIPT ---

def diagnose():
    print("--- STARTING DIAGNOSTIC SCRIPT ---")
    
    # We build a simple example transaction just to be able to sign it.
    # The details don't matter, we just need the signed object.
    nonce_safe = w3.eth.get_transaction_count(safe_wallet_address)
    example_tx = {
        'to': '0x0000000000000000000000000000000000000000',
        'value': 0,
        'nonce': nonce_safe,
        'gas': 21000,
        'maxFeePerGas': w3.to_wei(20, 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei(1, 'gwei'),
        'chainId': w3.eth.chain_id
    }
    
    # We sign the transaction
    signed_tx_object = w3.eth.account.sign_transaction(example_tx, SECURE_PK)
    
    # THIS IS THE MOST IMPORTANT LINE!!!
    # It will print all the available names in the signed object.
    print("\n--- ATTRIBUTES OF THE 'SignedTransaction' OBJECT ---")
    print(dir(signed_tx_object))
    print("\n-------------------------------------------------")
    print("\nPlease copy the entire line above (the one that starts with ['...']) and paste it in the response.")
    print("One of those names is the correct one to access the raw transaction (probably 'rawTransaction', 'raw', or something similar).")

if __name__ == "__main__":
    if not w3.is_connected():
        raise Exception("ERROR! Could not connect to the Plume network.")
    
    diagnose()

