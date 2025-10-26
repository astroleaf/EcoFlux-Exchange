// smart-contracts/scripts/verify.js
const hre = require("hardhat");

async function main() {
  // Example usage:
  // npx hardhat run scripts/verify.js --network mainnet
  const address = process.argv[2];
  const argsJson = process.argv[3] || "[]";
  const args = JSON.parse(argsJson);

  if (!address) {
    console.error("Usage: node verify.js <contractAddress> <constructorArgsAsJsonArray>");
    process.exit(1);
  }

  try {
    await hre.run("verify:verify", {
      address,
      constructorArguments: args,
    });
    console.log("Verification submitted for", address);
  } catch (err) {
    console.error("Verification failed:", err.message || err);
  }
}

main();
