---
source: magicians
topic_id: 15925
title: Gas estimate error in token deployment in remix
author: solomoney
date: "2023-09-27"
category: Magicians > Primordial Soup
tags: [token, gas]
url: https://ethereum-magicians.org/t/gas-estimate-error-in-token-deployment-in-remix/15925
views: 442
likes: 0
posts_count: 1
---

# Gas estimate error in token deployment in remix

// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import “@openzeppelin/contracts/token/ERC20/ERC20.sol”;

import “@openzeppelin/contracts/access/Ownable.sol”;

contract FishTokenCoin is ERC20, Ownable {

constructor() ERC20(“Fish Token Coin”, “FTC”) {

uint256 initialSupply = 236700008000 * (10 ** decimals());

_mint(msg.sender, initialSupply);

}

```
// Mint new tokens and add them to the total supply
function mint(uint256 amount) public onlyOwner {
    _mint(msg.sender, amount);
}

// Burn tokens and subtract them from the total supply
function burn(uint256 amount) public {
    _burn(msg.sender, amount);
}

// Overrides the transfer function to check for valid transfers
function _transfer(
    address sender,
    address recipient,
    uint256 amount
) internal virtual override {
    require(sender != address(0), "ERC20: transfer from the zero address");
    require(recipient != address(0), "ERC20: transfer to the zero address");

    super._transfer(sender, recipient, amount);
}

// Overrides the transferFrom function to check for valid transfers
function transferFrom(
    address sender,
    address recipient,
    uint256 amount
) public virtual override returns (bool) {
    _transfer(sender, recipient, amount);
    _approve(
        sender,
        _msgSender(),
        allowance(sender, _msgSender()) - amount
    );
    return true;
}
```

}

the coding is correct but gas estimate error
