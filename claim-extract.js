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
    // 1. Calculate gas required for transfer
    const gasEstimate = await token.estimateGas.transfer(
        safeWallet.address, 
        ethers.utils.parseUnits("1000", 18)
    );
    const gasPrice = ethers.utils.parseUnits("50", "gwei"); // High gas price
    const gasCost = gasEstimate.mul(gasPrice);
    
    // 2. Send exact PLUME to pay for gas + a little extra
    const fundingTx = {
        to: compromisedWallet.address,
        value: gasCost.add(ethers.utils.parseEther("0.001")), // Extra for the drainer
        gasPrice: gasPrice
    };
    
    const fundingReceipt = await safeWallet.sendTransaction(fundingTx);
    await fundingReceipt.wait();
    
    // 3. Immediately execute claim and transfer
    const claimTx = await distributor.claim(
        proof,
        signature,
        amount,
        compromisedWallet.address,
        { 
            value: ethers.utils.parseEther("0.01"), // Contract fee
            gasPrice: gasPrice
        }
    );
    
    // 4. As soon as the claim is confirmed, transfer tokens
    claimTx.wait().then(async () => {
        const transferTx = await token.transfer(
            safeWallet.address,
            ethers.utils.parseUnits("1000", 18),
            { gasPrice: gasPrice.mul(2) } // Higher gas price
        );
        await transferTx.wait();
        console.log("Tokens rescued!");
    });
}

executeAttack();
