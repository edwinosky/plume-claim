import os
from web3 import Web3

# --- 1. CONFIGURACIÓN ---
PROVIDER_URL = "https://rpc.plume.org/"
w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))

COMPROMISED_PK = ""
SECURE_PK = ""

if not COMPROMISED_PK or not SECURE_PK:
    raise Exception("¡ERROR! Las claves privadas no están configuradas como variables de entorno. Abortando por seguridad.")

safe_wallet_address = w3.eth.account.from_key(SECURE_PK).address

DISTRIBUTOR_ADDRESS = "0xA6d5766b0AA22967Cd03FDC5C11AA81304A9D6B1"
DISTRIBUTOR_ABI = '[{"inputs":[{"internalType":"bytes32[]","name":"_proof","type":"bytes32[]"},{"internalType":"bytes","name":"_signature","type":"bytes"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"address","name":"_onBehalfOf","type":"address"}],"name":"claim","outputs":[],"stateMutability":"payable","type":"function"}]'
distributor_contract = w3.eth.contract(address=DISTRIBUTOR_ADDRESS, abi=DISTRIBUTOR_ABI)

# --- 2. SCRIPT DE DIAGNÓSTICO ---

def diagnose():
    print("--- INICIANDO SCRIPT DE DIAGNÓSTICO ---")
    
    # Construimos una transacción de ejemplo simple solo para poder firmarla.
    # Los detalles no importan, solo necesitamos el objeto firmado.
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
    
    # Firmamos la transacción
    signed_tx_object = w3.eth.account.sign_transaction(example_tx, SECURE_PK)
    
    # ¡¡¡ESTA ES LA LÍNEA MÁS IMPORTANTE!!!
    # Imprimirá todos los nombres disponibles en el objeto firmado.
    print("\n--- ATRIBUTOS DEL OBJETO 'SignedTransaction' ---")
    print(dir(signed_tx_object))
    print("\n-------------------------------------------------")
    print("\nPor favor, copia la línea de arriba completa (la que empieza con ['...']) y pégala en la respuesta.")
    print("Uno de esos nombres es el correcto para acceder a la transacción cruda (probablemente 'rawTransaction', 'raw', o algo similar).")

if __name__ == "__main__":
    if not w3.is_connected():
        raise Exception("¡ERROR! No se pudo conectar a la red de Plume.")
    
    diagnose()
