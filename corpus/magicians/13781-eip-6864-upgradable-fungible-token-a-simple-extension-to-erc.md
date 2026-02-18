---
source: magicians
topic_id: 13781
title: "EIP-6864: Upgradable fungible token, a simple extension to ERC-20"
author: jeffishjeff
date: "2023-04-11"
category: EIPs
tags: [token, erc-20]
url: https://ethereum-magicians.org/t/eip-6864-upgradable-fungible-token-a-simple-extension-to-erc-20/13781
views: 1582
likes: 1
posts_count: 1
---

# EIP-6864: Upgradable fungible token, a simple extension to ERC-20

## Abstract

This proposal outlines a smart contract interface for upgrading/downgrading existing ERC-20 smart contracts while maintaining user balances. The interface itself is an extension to the ERC-20 standard so that other smart contracts can continue to interact with the upgraded smart contract without changing anything other than the address.

## Motivation

By design, smart contracts are immutable and token standards like ERC-20 are minimalistic. While these design principles are fundamental in decentalized applications, there are sensible and practical situations where the ability to upgrade an ERC-20 token is desirable, such as:

- to address bugs and remove limitations
- to adopt new features and standards
- to comply w/ changing regulations

Proxy pattern using `delegatecall` opcode offers a reasonable, generalized solution to reconcile the immutability and upgradability features but has its own shortcomings:

- the smart contracts must support proxy pattern from the get go, i.e. it cannot be used on contracts that were not deployed with proxies
- upgrades are silent and irreversible, i.e. users do not have the option to opt-out

In contrast, by reducing the scope to specifically ERC-20 tokens, this proposal standardizes an ERC-20 extension that works with any existing or future ERC-20 smart contracts, is much simpler to implement and to maintain, can be reversed or nested, and offers a double confirmation opportunity for any and all users to explicitly opt-in on the upgrade.

ERC-4931 attepts to address the same problem by introducing a third “bridge” contract to help facilitate the upgrade/downgrade operations. While this design decouples upgrade/downgrade logic from token logic, ERC-4931 would require tokens to be pre-minted at the destination smart contract and owned by the bridge contrtact rather then just-in-time when upgrade is invoked. It also would not be able to support upgrade-while-transfer and see-through functions as described below.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

```solidity
pragma solidity ^0.8.0;

/**
    @title Upgradable Fungible Token
    @dev See https://eips.ethereum.org/EIPS/eip-6864
 */
interface IERC6864 is IERC20 {
    /**
      @dev MUST be emitted when tokens are upgraded
      @param from Previous owner of base ERC-20 tokens
      @param to New owner of ERC-6864 tokens
      @param amount The amount that is upgraded
    */
    event Upgrade(address indexed from, address indexed to, uint256 amount);

    /**
      @dev MUST be emitted when tokens are downgraded
      @param from Previous owner of ERC-6864 tokens
      @param to New owner of base ERC-20 tokens
      @param amount The amount that is downgraded
    */
    event Downgrade(address indexed from, address indexed to, uint256 amount);

    /**
      @notice Upgrade `amount` of base ERC-20 tokens owned by `msg.sender` to ERC-6864 tokens under `to`
      @dev `msg.sender` must directly own sufficient base ERC-20 tokens
      MUST revert if `to` is the zero address
      MUST revert if `msg.sender` does not directly own `amount` or more of base ERC-20 tokens
      @param to The address to receive ERC-6864 tokens
      @param amount The amount of base ERC-20 tokens to upgrade
    */
    function upgrade(address to, uint256 amount) external;

    /**
      @notice Downgrade `amount` of ERC-6864 tokens owned by `from` to base ERC-20 tokens under `to`
      @dev `msg.sender` must either directly own or be approved to spend sufficient ERC-6864 tokens for `from`
      MUST revert if `to` is the zero address
      MUST revert if `from` does not directly own `amount` or more of ERC-6864 tokens
      MUST revret if `msg.sender` is not `from` and is not approved to spend `amount` or more of ERC-6864 tokens for `from`
      @param from The address to release ERC-6864 tokens
      @param to The address to receive base ERC-20 tokens
      @param amount The amount of ERC-6864 tokens to downgrade
    */
    function downgrade(address from, address to, uint256 amount) external;

    /**
      @notice Get the base ERC-20 smart contract address
      @return The address of the base ERC-20 smart contract
    */
    function baseToken() external view returns (address);
}
```

### See-through Extension

The **see-through extension** is OPTIONAL. It allows for easy viewing of combined states between this ERC-6864 and base ERC-20 smart contracts.

```solidity
pragma solidity ^0.8.0;

interface IERC6864SeeThrough is IERC6864 {
  /**
    @notice Get the combined total token supply between this ERC-6864 and base ERC-20 smart contracts
    @return The combined total token supply
  */
  function combinedTotalSupply() external view returns (uint256);

  /**
    @notice Get the combined token balance of `account` between this ERC-6864 and base ERC-20 smart contracts
    @param account The address that owns the tokens
    @return The combined token balance
  */
  function combinedBalanceOf(address account) external view returns (uint256);

  /**
    @notice Get the combined allowance that `spender` is allowed to spend for `owner` between this ERC-6864 and base ERC-20 smart contracts
    @param owner The address that owns the tokens
    @param spender The address that is approve to spend the tokens
    @return The combined spending allowance
  */
  function combinedAllowance(address owner, address spender) external view returns (uint256);
}

```

## Rationale

### Extending ERC-20 standard

The goal of this proposal is to upgrade without affecting user balances, therefore leveraging existing data structure and methods is the path of the least engineering efforts as well as the most interoperability.

### Supporting downgrade

The ability to downgrade makes moving between multiple IERC-6864 implementations on the same base ERC-20 smart contract possible. It also allows a way out should bugs or limitations discovered on ERC-6864 smart contract, or the user simply changes his or her mind.

### Optional see-through extension

While these functions are useful in many situations, they are trivial to implement and results can be calculated via other public functions, hence the decision to include them in an optional extension rather than the core interface.

## Backwards Compatibility

ERC-6864 is generally compatible with the ERC-20 standard. The only caveat is that some smart contracts may opt to implement `transfer` to work with the entire combined balance (this reduces user friction, see reference implementation) rather than the standard `balanceOf` amount. In this case it is RECOMMENDED that such contract to implement `totalSupply` and `balanceOf` to return combined amount between this ERC-6864 and base ERC-20 smart contracts

## Reference Implementation

```solidity
import {IERC20, ERC20} from "@openzeppelin-contracts/token/ERC20/ERC20.sol";

contract ERC6864 is IERC6864, ERC20 {
  IERC20 private immutable s_baseToken;

    constructor(string memory name, string memory symbol, address baseToken_) ERC20(name, symbol) {
        s_baseToken = IERC20(baseToken_);
    }

    function baseToken() public view virtual override returns (address) {
        return address(s_baseToken);
    }

    function upgrade(address to, uint256 amount) public virtual override {
        address from = _msgSender();

        s_baseToken.transferFrom(from, address(this), amount);
        _mint(to, amount);

        emit Upgrade(from, to, amount);
    }

    function downgrade(address from, address to, uint256 amount) public virtual override {
        address spender = _msgSender();

        if (from != spender) {
            _spendAllowance(from, spender, amount);
        }
        _burn(from, amount);
        s_baseToken.transfer(to, amount);

        emit Downgrade(from, to, amount);
    }

    function transfer(address to, uint256 amount) public virtual override returns (bool) {
        address from = _msgSender();
        uint256 balance = balanceOf(from);

        if (balance CC0.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/6864/files)














####


      `master` ← `jeffishjeff:master`




          opened 09:42AM - 11 Apr 23 UTC



          [![](https://avatars.githubusercontent.com/u/5304123?v=4)
            jeffishjeff](https://github.com/jeffishjeff)



          [+211
            -0](https://github.com/ethereum/EIPs/pull/6864/files)







This standard outlines a smart contract interface for upgrading/downgrading exis[…](https://github.com/ethereum/EIPs/pull/6864)ting ERC-20 smart contracts while maintaining user balances. The interface itself is an extension of the ERC-20 standard so that other contracts can continue to interact with the upgraded token without any change other than updating contract address.
