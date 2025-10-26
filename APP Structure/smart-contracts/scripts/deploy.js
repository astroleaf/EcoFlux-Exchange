// smart-contracts/scripts/deploy.js
const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with:", deployer.address);

  // Deploy EnergyToken
  const EnergyToken = await hre.ethers.getContractFactory("EnergyToken");
  const token = await EnergyToken.deploy("EnergyToken", "ENGY", hre.ethers.utils.parseUnits("1000000", 18));
  await token.deployed();
  console.log("EnergyToken deployed to:", token.address);

  // Deploy PriceOracle
  const PriceOracle = await hre.ethers.getContractFactory("PriceOracle");
  const oracle = await PriceOracle.deploy();
  await oracle.deployed();
  console.log("PriceOracle deployed to:", oracle.address);

  // Deploy TradingContract with token address
  const TradingContract = await hre.ethers.getContractFactory("TradingContract");
  const trading = await TradingContract.deploy(token.address);
  await trading.deployed();
  console.log("TradingContract deployed to:", trading.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
