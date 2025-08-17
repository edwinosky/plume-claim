# Plume Network Airdrop Claim and Rescue Scripts

This repository contains a series of scripts designed to help you claim the Plume Network airdrop, especially in situations where the eligible wallet is compromised. The scripts allow you to execute a token rescue using a secure wallet to sign and pay for the transactions.

## Script Descriptions

- **`calculateRoot.js`**: A Node.js script that calculates the Merkle root and the message hash that must be signed by the secure wallet. This is the first and most crucial step to generate the signature required by the other scripts.
- **`plume-claim.js`**: A basic Node.js script to execute the `claim` function from the airdrop contract. It requires all data (proof, signature, etc.) to be entered manually.
- **`claim-extract.js`**: A more advanced script that attempts to fund the compromised wallet with the exact gas needed and then execute the claim and token transfer in a single, fast operation to avoid front-running.
- **`rescue_script.py`**: The main and recommended rescue script, written in Python. It orchestrates two transactions (a claim from the secure wallet and a transfer from the compromised wallet) to move the funds safely.
- **`rescue_script_test.py`**: A diagnostic script for debugging transaction signing issues with `web3.py`.

## Prerequisites

- **Node.js**: Version 14 or higher.
- **Python**: Version 3.8 or higher.
- **`pip`**: The Python package installer.

## Installation

1.  **Clone this repository:**
    ```bash
    git clone https://github.com/edwinosky/plume-claim.git
    cd plume-claim
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install web3
    ```

## Configuration

1.  **Create a `.env` file**:
    Copy the contents of `.env-template` to a new file named `.env`.

2.  **Add your private keys**:
    In the `.env` file, add the private keys for your secure wallet and the compromised wallet.
    ```
    SECURE_WALLET_PRIVATE_KEY="YOUR_SECURE_PRIVATE_KEY"
    COMPROMISED_WALLET_PRIVATE_KEY="YOUR_COMPROMISED_PRIVATE_KEY"
    ```

3.  **Configure the scripts**:
    - **`calculateRoot.js`**: Fill in the `onBehalfOf_raw`, `contractAddress_raw`, `amount`, and `proof` variables with your airdrop data.
    - **`rescue_script.py`**: Ensure the `COMPROMISED_PK` and `SECURE_PK` variables are loaded correctly from environment variables (or insert them directly if you prefer, though it's not recommended). Also, fill in the claim data: `PROOF`, `SIGNATURE`, `AMOUNT`.

## Usage (Recommended Method: `rescue_script.py`)

### Step 1: Calculate the Message Hash and Generate the Signature

1.  **Open `calculateRoot.js`** and fill in the following data:
    - `onBehalfOf_raw`: The address of your compromised wallet.
    - `contractAddress_raw`: The airdrop contract address.
    - `amount`: The amount of tokens to claim (in 18-decimal format).
    - `proof`: Your corresponding Merkle proof.

2.  **Run the script**:
    ```bash
    node calculateRoot.js
    ```

3.  **Copy the Message Hash** that is output to the console.

4.  **Sign the Message Hash**:
    Use a tool like MyEtherWallet, MetaMask, or a local script to sign this hash with the private key of your **secure wallet**. This signature is what you will use in the next step.

### Step 2: Execute the Rescue

1.  **Open `rescue_script.py`** and fill in the following data:
    - `COMPROMISED_PK`: The private key of the compromised wallet.
    - `SECURE_PK`: The private key of the secure wallet.
    - `PROOF`: The same Merkle proof from the previous step.
    - `SIGNATURE`: The signature you generated in the previous step.
    - `AMOUNT`: The same amount from the previous step.

2.  **Run the rescue script**:
    ```bash
    python rescue_script.py
    ```

3.  The script will prepare and send the two transactions (claim and transfer) almost simultaneously. Follow the instructions in the console.

## Disclaimer

The use of these scripts carries risks, especially when handling private keys. Review the code carefully and use it at your own risk. We are not responsible for any potential loss of funds.
