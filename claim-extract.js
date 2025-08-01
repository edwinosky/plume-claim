const { ethers } = require("ethers");

const provider = new ethers.providers.JsonRpcProvider('https://rpc.plumenetwork.xyz');
const compromisedWallet = new ethers.Wallet('PRIVATE_KEY_COMPROMISED', provider);
const safeWallet = new ethers.Wallet('PRIVATE_KEY_SECURE', provider);
const distributorAddress = "0x...";
const tokenAddress = "0x...";

const distributor = new ethers.Contract(distributorAddress, [
    "function claim(bytes32[] calldata _proof, bytes calldata _signature, uint256 _amount, address _onBehalfOf) external payable"
], compromisedWallet);

const token = new ethers.Contract(tokenAddress, [
    "function balanceOf(address) view returns (uint256)",
    "function transfer(address, uint256) returns (bool)"
], compromisedWallet);

async function executeAttack() {
    // 1. Calcular gas necesario para transferencia
    const gasEstimate = await token.estimateGas.transfer(
        safeWallet.address, 
        ethers.utils.parseUnits("1000", 18)
    );
    const gasPrice = ethers.utils.parseUnits("50", "gwei"); // Gas price alto
    const gasCost = gasEstimate.mul(gasPrice);
    
    // 2. Enviar PLUME exacto para pagar gas + un poco extra
    const fundingTx = {
        to: compromisedWallet.address,
        value: gasCost.add(ethers.utils.parseEther("0.001")), // Extra para el drainer
        gasPrice: gasPrice
    };
    
    const fundingReceipt = await safeWallet.sendTransaction(fundingTx);
    await fundingReceipt.wait();
    
    // 3. Inmediatamente ejecutar reclamo y transferencia
    const claimTx = await distributor.claim(
        proof,
        signature,
        amount,
        compromisedWallet.address,
        { 
            value: ethers.utils.parseEther("0.01"), // Fee del contrato
            gasPrice: gasPrice
        }
    );
    
    // 4. En cuanto se confirme el reclamo, transferir tokens
    claimTx.wait().then(async () => {
        const transferTx = await token.transfer(
            safeWallet.address,
            ethers.utils.parseUnits("1000", 18),
            { gasPrice: gasPrice.mul(2) } // Gas price más alto
        );
        await transferTx.wait();
        console.log("Tokens rescatados!");
    });
}

executeAttack();
