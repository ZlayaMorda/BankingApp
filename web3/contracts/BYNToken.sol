// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract BYNToken is ERC20, Ownable {

    constructor(uint256 _initialSupply) ERC20("TokenBelarusianRuble", "BYNT") Ownable(msg.sender) {
        _mint(msg.sender, _initialSupply);
    }

    function mint_byn(uint256 _amount) external onlyOwner {
        _mint(msg.sender, _amount);
    }
}
