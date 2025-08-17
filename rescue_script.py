import os
import asyncio
from web3 import Web3

# --- 1. CONFIGURACIÓN ---
PROVIDER_URL = "https://rpc.plume.org/"
w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))

COMPROMISED_PK = ""
SECURE_PK = ""

if not COMPROMISED_PK or not SECURE_PK:
    raise Exception("¡ERROR! Las claves privadas no están configuradas como variables de entorno. Abortando por seguridad.")

compromised_wallet_address = w3.eth.account.from_key(COMPROMISED_PK).address
safe_wallet_address = w3.eth.account.from_key(SECURE_PK).address

DISTRIBUTOR_ADDRESS = "0xA6d5766b0AA22967Cd03FDC5C11AA81304A9D6B1"
DISTRIBUTOR_ABI = '[{"inputs":[{"internalType":"bytes32[]","name":"_proof","type":"bytes32[]"},{"internalType":"bytes","name":"_signature","type":"bytes"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"address","name":"_onBehalfOf","type":"address"}],"name":"claim","outputs":[],"stateMutability":"payable","type":"function"}]'
distributor_contract = w3.eth.contract(address=DISTRIBUTOR_ADDRESS, abi=DISTRIBUTOR_ABI)

# --- 2. PARÁMETROS DEL RECLAMO ---
PROOF = [
    "0xd1a74bcc7a0397c6e9a6ab6fb90781b052de0bf678709ed8e6e595255576c82d", "0xee38c539a90af06459b49c9a698ae451b45e660facdbcda35069fc84ccbcb259", "0xe1b3cc1be5af681ecd151b69c104be3da7638a6f497a8ee59d2f319a55e64cf9", "0x4411749d1af61618ee9303cd7123349feafa5bc1f1fe06a7516f6dcdbcf79467", "0x61f860f3d5e04ed4bc227a3006a3be4fa35d64228f4418b65260759c27f48967", "0x93b7081ebd314c572de2c93ebc9fd8b37b7276eae775493c8b85e6f05c8427fd", "0xd66062fe64d071fff316fd61d5bc53ba9c5739c3c1d51a298fc93b3fd1466b29", "0x3ec5d1946dcebd87fe209905c9e043e245bdc046405b6d38284db853b051768c", "0xa13dd81daf1cc619501483de491ef2668098ebf28d7ae4c200f3e62cd070b351", "0x3135807d14d4c7e77fa348b654aa0d33359b69561ee084d112bb6b39c1196851", "0xc699e5a423340676939251a443812fbe2070176a5ee43b68fbd8587818b78943", "0x6bbbca8f7db22328c71f3fec847ebafee4c1eb208f8acbfad63d28d1909c2ac5", "0x7d3d5def6dfaf8aaa347fb13112af630e71aad40be96a103b8e049e21f5a456f", "0xcdad841ec39daa6da1e6556c7f5efca907e12590fbb8c0b9cdca795d84cdb91e", "0x32569936e29d1eb2c250730df8ddaf9af143b9232dca368311809afe375aa844", "0x28fa500e3f567889dff8f1a8f6f2aad90ead3bead2f2f82af07acdbbe2262d92", "0x2451faed44f21b90060e073fad518fa1981b914c4c1dc1315384d08ef1338ca6", "0xa03af8117ebe8d7eea5d752c16b882a840e92f9ed2566f838d5d0b31cfd48fd9"
]
SIGNATURE = "0xfb45d7172b74e6429fec3104988276dced1ef8da4de8f5a6130aee289da2f3be32b0c90b8e9e13694039f7f863ea3b8af99ad3d46eaa6f9ce89754924d57e2881b"
AMOUNT = 2475000000000000000000
ON_BEHALF_OF = compromised_wallet_address

# --- 3. FUNCIÓN DE RESCATE ---

async def rescue():
    print("--- INICIANDO INTENTO DE RESCATE ---")
    print(f"Wallet Segura: {safe_wallet_address}")
    print(f"Wallet Comprometida: {compromised_wallet_address}")
    
    nonce_safe = w3.eth.get_transaction_count(safe_wallet_address)
    nonce_compromised = w3.eth.get_transaction_count(compromised_wallet_address)
    print(f"Nonce Segura: {nonce_safe}, Nonce Comprometida: {nonce_compromised}")

    priority_fee_gwei = 100 
    base_fee_gwei = w3.eth.gas_price / 1e9
    
    print(f"Gas Base Actual: {base_fee_gwei:.2f} Gwei")
    print(f"Soborno de Prioridad: {priority_fee_gwei} Gwei")

    # Transacción 1: CLAIM
    claim_tx = distributor_contract.functions.claim(
        PROOF, w3.to_bytes(hexstr=SIGNATURE), AMOUNT, ON_BEHALF_OF
    ).build_transaction({
        'from': safe_wallet_address,
        'nonce': nonce_safe,
        'gas': 350000,
        'maxFeePerGas': w3.to_wei(base_fee_gwei + 10, 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei(2, 'gwei'),
        'chainId': w3.eth.chain_id
    })
    
    # Transacción 2: TRANSFER
    gas_limit_transfer = 21000
    max_fee_transfer = w3.to_wei(base_fee_gwei + priority_fee_gwei, 'gwei')
    gas_cost_estimate = gas_limit_transfer * max_fee_transfer
    amount_to_rescue = AMOUNT - gas_cost_estimate
    
    transfer_tx = {
        'to': safe_wallet_address, 'value': amount_to_rescue, 'nonce': nonce_compromised, 'gas': gas_limit_transfer,
        'maxFeePerGas': max_fee_transfer, 'maxPriorityFeePerGas': w3.to_wei(priority_fee_gwei, 'gwei'), 'chainId': w3.eth.chain_id
    }
    
    print("\n--- Transacciones Preparadas ---")
    print(f"1. CLAIM: Llamando desde {safe_wallet_address} en nombre de {ON_BEHALF_OF}")
    print(f"2. RESCATE: Transfiriendo {w3.from_wei(amount_to_rescue, 'ether')} PLUME a la wallet segura.")
    print("---------------------------------")
    
    signed_claim_tx = w3.eth.account.sign_transaction(claim_tx, SECURE_PK)
    signed_transfer_tx = w3.eth.account.sign_transaction(transfer_tx, COMPROMISED_PK)
    
    print("\nENVIANDO TRANSACCIONES A LA RED... ¡AHORA!")
    try:
        # --- LÍNEAS CORREGIDAS CON EL ATRIBUTO CORRECTO ---
        claim_hash = w3.eth.send_raw_transaction(signed_claim_tx.raw_transaction)
        print(f"  > CLAIM enviada. Hash: {claim_hash.hex()}")
        
        transfer_hash = w3.eth.send_raw_transaction(signed_transfer_tx.raw_transaction)
        print(f"  > RESCATE enviada. Hash: {transfer_hash.hex()}")
        
        print("\nEsperando recibos...")
        claim_receipt = w3.eth.wait_for_transaction_receipt(claim_hash, timeout=300)
        transfer_receipt = w3.eth.wait_for_transaction_receipt(transfer_hash, timeout=300)
        
        print("\n--- RESULTADOS ---")
        if claim_receipt.status == 1:
            print("✅ ¡ÉXITO! La transacción de CLAIM se minó.")
        else:
            print("❌ ¡FALLO! La transacción de CLAIM revirtió. La causa más probable es una firma inválida.")
            
        if transfer_receipt.status == 1:
            print("✅🏆 ¡¡¡VICTORIA!!! La transacción de RESCATE se minó. ¡LOS FONDOS ESTÁN A SALVO!")
        else:
            print("❌ ¡FALLO! La transacción de RESCATE revirtió. Causa probable: el bot fue más rápido, el claim falló o no había fondos suficientes.")

    except Exception as e:
        print(f"\nOcurrió un error durante el envío o la espera: {e}")

if __name__ == "__main__":
    if not w3.is_connected():
        raise Exception("¡ERROR! No se pudo conectar a la red de Plume. Verifica la URL del RPC.")
    
    input("Verifica que los nonces y el gas son correctos. Asegúrate de que ambas wallets tienen fondos suficientes para el gas. Presiona ENTER para ejecutar el script de rescate.")
    asyncio.run(rescue())
