// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "@openzeppelin/contracts/access/Ownable.sol";

contract PriceOracle is Ownable {
    // simple on-chain oracle feed (push-based)
    uint256 public lastPrice;
    uint256 public lastTimestamp;

    event PriceUpdated(uint256 price, uint256 timestamp);

    function updatePrice(uint256 price) external onlyOwner {
        lastPrice = price;
        lastTimestamp = block.timestamp;
        emit PriceUpdated(price, lastTimestamp);
    }

    function readPrice() external view returns (uint256 price, uint256 timestamp) {
        return (lastPrice, lastTimestamp);
    }
}
