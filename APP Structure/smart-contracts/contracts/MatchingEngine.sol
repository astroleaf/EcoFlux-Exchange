// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

/// Lightweight on-chain matching stub (for demo).
/// In practice, matching engines run off-chain to save gas.
contract MatchingEngine {
    struct Match {
        address buyer;
        address seller;
        uint256 quantity;
        uint256 price;
        uint256 timestamp;
    }

    Match[] public matches;

    event Matched(address indexed buyer, address indexed seller, uint256 quantity, uint256 price);

    function recordMatch(address buyer, address seller, uint256 quantity, uint256 price) external {
        matches.push(Match({ buyer: buyer, seller: seller, quantity: quantity, price: price, timestamp: block.timestamp }));
        emit Matched(buyer, seller, quantity, price);
    }

    function getMatchesCount() external view returns (uint256) {
        return matches.length;
    }
}
