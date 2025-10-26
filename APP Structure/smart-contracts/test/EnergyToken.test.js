const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("EnergyToken", function () {
  it("deploys and mints initial supply", async function () {
    const [owner, addr1] = await ethers.getSigners();
    const Token = await ethers.getContractFactory("EnergyToken");
    const token = await Token.deploy("EnergyToken", "ENGY", ethers.utils.parseUnits("1000", 18));
    await token.deployed();

    const total = await token.totalSupply();
    expect(total).to.equal(ethers.utils.parseUnits("1000", 18));

    // mint more
    await token.mint(addr1.address, ethers.utils.parseUnits("100", 18));
    const bal = await token.balanceOf(addr1.address);
    expect(bal).to.equal(ethers.utils.parseUnits("100", 18));
  });
});
