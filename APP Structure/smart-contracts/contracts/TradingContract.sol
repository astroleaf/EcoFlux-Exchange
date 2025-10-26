// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "./EnergyToken.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract TradingContract is ReentrancyGuard, Ownable {
    IERC20 public energyToken;

    event TradeExecuted(address indexed buyer, address indexed seller, uint256 quantity, uint256 price);

    struct Order {
        address owner;
        uint256 quantity;
        uint256 price; // price per token in wei
        bool isBuy; // true => buy order, false => sell order
    }

    Order[] public orders;

    constructor(address tokenAddress) {
        energyToken = IERC20(tokenAddress);
    }

    function placeOrder(uint256 quantity, uint256 price, bool isBuy) external returns (uint256) {
        require(quantity > 0, "Quantity > 0");
        if (!isBuy) {
            // seller must approve tokens to this contract
            require(energyToken.balanceOf(msg.sender) >= quantity, "Insufficient token balance");
        }
        orders.push(Order({ owner: msg.sender, quantity: quantity, price: price, isBuy: isBuy }));
        return orders.length - 1;
    }

    function cancelOrder(uint256 idx) external {
        require(idx < orders.length, "Invalid order");
        Order storage o = orders[idx];
        require(o.owner == msg.sender || owner() == msg.sender, "Not allowed");
        o.quantity = 0;
    }

    /// naive match function: match buy and sell orders at mid price
    function matchOrders(uint256 buyIdx, uint256 sellIdx) external nonReentrant {
        require(buyIdx < orders.length && sellIdx < orders.length, "Invalid indexes");
        Order storage buy = orders[buyIdx];
        Order storage sell = orders[sellIdx];

        require(buy.isBuy && !sell.isBuy, "Sides mismatch");
        uint256 qty = buy.quantity < sell.quantity ? buy.quantity : sell.quantity;
        require(qty > 0, "No quantity");

        uint256 price = (buy.price + sell.price) / 2;

        // transfer payment from buyer to seller (assumes buyer sent ETH)
        // For simplicity in this demo, buyer must have approved contract to pull tokens? Here we use ETH payments.
        // In production use stablecoin or on-chain settlement logic.
        (bool sent, ) = sell.owner.call{value: price * qty}("");
        require(sent, "ETH transfer failed");

        // transfer energy tokens from seller to buyer
        require(energyToken.transferFrom(sell.owner, buy.owner, qty), "Token transfer failed");

        buy.quantity -= qty;
        sell.quantity -= qty;

        emit TradeExecuted(buy.owner, sell.owner, qty, price);
    }

    // receive ETH for settlement
    receive() external payable {}
    fallback() external payable {}
}
