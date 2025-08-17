const { ethers } = require("ethers");
const provider = new ethers.providers.JsonRpcProvider('https://rpc.plumenetwork.xyz');
const secureWallet = new ethers.Wallet('YOUR_PRIVATE_KEY', provider);
const compromisedAddress = "0x..."; // 
const amount = ethers.utils.parseUnits("1000", 18); // 
const proof = ["0x...", "0x..."]; // Merkle proof
const signature = "0x..."; // 
const contractAddress = "0x..."; 
const feeAmount = ethers.utils.parseEther("0.01"); // PLUME 

const abi = [
  "function claim(bytes32[] calldata _proof, bytes calldata _signature, uint256 _amount, address _onBehalfOf) external payable"
];

const contract = new ethers.Contract(contractAddress, abi, secureWallet);

const leaf = ethers.utils.solidityKeccak256(
  ['address', 'uint256'],
  [compromisedAddress, amount]
);

let root = leaf;
for (const node of proof) {
  root = ethers.utils.solidityKeccak256(
    ['bytes32', 'bytes32'],
    [root < node ? root : node, root < node ? node : root]
  );
}

// Execute claim
const tx = await contract.claim(
  proof,
  signature,
  amount,
  compromisedAddress,
  { value: feeAmount }
);

console.log("Transaction sent:", tx.hash);
await tx.wait();
console.log("Claim completed in block:", tx.blockNumber);
