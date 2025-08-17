const { ethers } = require("ethers");

// --- DATA YOU OBTAINED ---
// HERE ARE THE CORRECTED ADDRESSES WITH THEIR CHECKSUM!!!
const onBehalfOf_raw = "0xEE46358C95D7995eFC34260D34DfBe0a2FE23a5E";
const contractAddress_raw = "0xA6d5766b0AA22967Cd03FDC5C11AA81304A9D6B1";
const chainId = 98866;

const amount = "2475000000000000000000";
const proof = [
    "0xd1a74bcc7a0397c6e9a6ab6fb90781b052de0bf678709ed8e6e595255576c82d",
    "0xee38c539a90af06459b49c9a698ae451b45e660facdbcda35069fc84ccbcb259",
    "0xe1b3cc1be5af681ecd151b69c104be3da7638a6f497a8ee59d2f319a55e64cf9",
    "0x4411749d1af61618ee9303cd7123349feafa5bc1f1fe06a7516f6dcdbcf79467",
    "0x61f860f3d5e04ed4bc227a3006a3be4fa35d64228f4418b65260759c27f48967",
    "0x93b7081ebd314c572de2c93ebc9fd8b37b7276eae775493c8b85e6f05c8427fd",
    "0xd66062fe64d071fff316fd61d5bc53ba9c5739c3c1d51a298fc93b3fd1466b29",
    "0x3ec5d1946dcebd87fe209905c9e043e245bdc046405b6d38284db853b051768c",
    "0xa13dd81daf1cc619501483de491ef2668098ebf28d7ae4c200f3e62cd070b351",
    "0x3135807d14d4c7e77fa348b654aa0d33359b69561ee084d112bb6b39c1196851",
    "0xc699e5a423340676939251a443812fbe2070176a5ee43b68fbd8587818b78943",
    "0x6bbbca8f7db22328c71f3fec847ebafee4c1eb208f8acbfad63d28d1909c2ac5",
    "0x7d3d5def6dfaf8aaa347fb13112af630e71aad40be96a103b8e049e21f5a456f",
    "0xcdad841ec39daa6da1e6556c7f5efca907e12590fbb8c0b9cdca795d84cdb91e",
    "0x32569936e29d1eb2c250730df8ddaf9af143b9232dca368311809afe375aa844",
    "0x28fa500e3f567889dff8f1a8f6f2aad90ead3bead2f2f82af07acdbbe2262d92",
    "0x2451faed44f21b90060e073fad518fa1981b914c4c1dc1315384d08ef1338ca6",
    "0xa03af8117ebe8d7eea5d752c16b882a840e92f9ed2566f838d5d0b31cfd48fd9"
];

// --- CALCULATIONS ---

// 0. Validate addresses before using them
let onBehalfOf, contractAddress;
try {
    onBehalfOf = ethers.getAddress(onBehalfOf_raw);
    contractAddress = ethers.getAddress(contractAddress_raw);
    console.log("✅ Checksum validated addresses OK.");
} catch (error) {
    console.error("❌ ERROR! One of the addresses has an incorrect checksum. Copy the EXACT address from the block explorer.");
    console.error(error.message);
    process.exit(1); // Exit script on error
}

// 1. Calculate the leaf
const leaf = ethers.keccak256(
    ethers.solidityPacked(
        ["address", "uint256"],
        [onBehalfOf, amount]
    )
);
console.log(`\nLeaf: ${leaf}`);

// 2. Reconstruct the root
let root = leaf;
for (const proofElement of proof) {
    if (Buffer.compare(Buffer.from(root.slice(2), 'hex'), Buffer.from(proofElement.slice(2), 'hex')) > 0) {
        root = ethers.keccak256(Buffer.concat([Buffer.from(proofElement.slice(2), 'hex'), Buffer.from(root.slice(2), 'hex')]));
    } else {
        root = ethers.keccak256(Buffer.concat([Buffer.from(root.slice(2), 'hex'), Buffer.from(proofElement.slice(2), 'hex')]));
    }
}
console.log(`Root: ${root}`);

// 3. Generate the message that needs to be signed
const messageToSign = ethers.keccak256(
    ethers.solidityPacked(
        ["address", "uint256", "bytes32", "address", "uint256"],
        [onBehalfOf, amount, root, contractAddress, chainId]
    )
);

console.log("\n--- 🏆 COMPLETE DATA! ---");
console.log(`This is the Message Hash that the signer (0xaee7B7...) must sign:\n`);
console.log(messageToSign);
console.log("\n---------------------------------");
