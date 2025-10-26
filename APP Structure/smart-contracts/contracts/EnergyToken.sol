// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

/// Simple ERC20 token for energy units.
/// Uses OpenZeppelin ERC20 implementation.
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract EnergyToken is ERC20, Ownable {
    constructor(string memory name, string memory symbol, uint256 initialSupply) ERC20(name, symbol) {
        if (initialSupply > 0) {
            _mint(msg.sender, initialSupply);
        }
    }

    /// mint function accessible to owner (market operator)
    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }

    /// burn for retiring energy tokens
    function burn(address from, uint256 amount) external onlyOwner {
        _burn(from, amount);
    }
}
