---
source: magicians
topic_id: 16225
title: "ERC-1363: Payable Token"
author: vittominacori
date: "2023-10-23"
category: EIPs
tags: [erc1363]
url: https://ethereum-magicians.org/t/erc-1363-payable-token/16225
views: 872
likes: 0
posts_count: 4
---

# ERC-1363: Payable Token

**This thread is intended to be the official [EIP-1363](https://eips.ethereum.org/EIPS/eip-1363) discussions link.**

## Abstract

ERC-1363 is an extension interface for ERC-20 tokens that supports executing code on a recipient contract after transfers, or code on a spender contract after approvals, in a single transaction.

The following standard allows for the implementation of a standard API for tokens interaction with smart contracts after `transfer`, `transferFrom` or `approve`.

This standard provides basic functionality to transfer tokens, as well as allow tokens to be approved so they can be spent by another on-chain third party, and then make a callback on the receiver or spender contract.

The following are functions and callbacks introduced by this EIP:

- transferAndCall and transferFromAndCall will call an onTransferReceived on a ERC1363Receiver contract.
- approveAndCall will call an onApprovalReceived on a ERC1363Spender contract.

## Motivation

There is no way to execute code on a receiver/spender contract after an ERC-20 `transfer`, `transferFrom` or `approve` so, to perform an action, it is required to send another transaction.

This introduces complexity in UI development and friction on adoption as users must wait for the first transaction to be executed and then submit the second one. They must also pay GAS twice.

This proposal aims to make tokens capable of performing actions more easily and working without the use of any off-chain listener.

It allows to make a callback on a receiver/spender contract, after a transfer or an approval, in a single transaction.

Tokens defined by this EIP can be used for specific utilities in all cases that require a callback to be executed after a transfer or an approval received.

This EIP is also useful for avoiding token loss or token locking in contracts by verifying the recipient contract’s ability to handle tokens.

## Specification

Smart contracts implementing the ERC-1363 standard **MUST** implement all of the functions in the `ERC1363` interface, as well as the `ERC20` and `ERC165` interfaces.

```solidity
pragma solidity ^0.8.0;

interface ERC1363 is ERC20, ERC165 {
    function transferAndCall(address to, uint256 value) external returns (bool);
    function transferAndCall(address to, uint256 value, bytes calldata data) external returns (bool);
    function transferFromAndCall(address from, address to, uint256 value) external returns (bool);
    function transferFromAndCall(address from, address to, uint256 value, bytes calldata data) external returns (bool);
    function approveAndCall(address spender, uint256 value) external returns (bool);
    function approveAndCall(address spender, uint256 value, bytes calldata data) external returns (bool);
}

interface ERC20 {
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
    function approve(address spender, uint256 value) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
}

interface ERC165 {
    function supportsInterface(bytes4 interfaceId) external view returns (bool);
}
```

A contract that wants to accept ERC-1363 tokens via `transferAndCall` or `transferFromAndCall` **MUST** implement the `ERC1363Receiver` interface:

```solidity
interface ERC1363Receiver {
    function onTransferReceived(address operator, address from, uint256 value, bytes calldata data) external returns (bytes4);
}
```

A contract that wants to accept ERC-1363 tokens via `approveAndCall` **MUST** implement the `ERC1363Spender` interface:

```solidity
interface ERC1363Spender {
    function onApprovalReceived(address owner, uint256 value, bytes calldata data) external returns (bytes4);
}
```

Full specification in the official Final [ERC-1363](https://eips.ethereum.org/EIPS/eip-1363) page.

Reference implementation and test cases can be found [here](https://github.com/vittominacori/erc1363-payable-token).

## Replies

**vittominacori** (2023-10-23):

Reference to discussions about EIP-1363:

- https://github.com/ethereum/eips/issues/1363
- https://github.com/ethereum/ERCs/pull/31
- https://github.com/ethereum/EIPs/pull/5167
- https://ethereum-magicians.org/t/why-isnt-there-an-erc-for-safetransfer-for-erc-20/7604
- https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3736
- https://github.com/OpenZeppelin/openzeppelin-contracts/pull/4631
- https://github.com/OpenZeppelin/openzeppelin-contracts/pull/3525
- https://github.com/OpenZeppelin/openzeppelin-contracts/pull/3017

---

**Dexaran** (2023-10-27):

**I would like to raise the security concern.**

ERC-1363 is backwards compatible with ERC-20 which means that this EIP inherits the security flaw of ERC-20 transferring workflow. The ERC-20 security flaw will be described in [EIP-7544](https://github.com/ethereum/EIPs/pull/7915).

TL;DR: ERC-20 implements two transferring methods (1) `transfer` and (2) `approve & transferFrom`. Both transferring methods do not support error handling i.e. if a user will make an action that is known to be a mistake and therefore MUST be reverted - it will burn the users money instead. ERC-20 standard places a burden of determining the method of transferring tokens on the end user which combined with the lack of error handling creates a security problem that resulted in a loss of [at least $130M worth of tokens](https://www.reddit.com/r/ethereum/comments/15hdz96/today_at_least_130m_worth_of_tokens_are_lost/). Later estimations showed [$201M lost tokens](https://gist.github.com/Dexaran/40213a04ce46b394279ac7daa581ce87) in top50 examined contracts.

You can find more info here:

- The description of an issue and its classification according to “software vulnerability criterias” ERC20 token standard vulnerability classification. · GitHub
- The author of the ERC-20 standard confirmed it is a security flaw https://twitter.com/feindura/status/1715086538462155198
- A common example of a user suffering form this issue Reddit - Dive into anything
- A common example of another user suffering from this issue in 2023 Reddit - Dive into anything
- Token losses calculator script: Stuck Tokens
- Security statement regarding the ERC-20 standard: Guest Post by Callisto Network: ERC-20 Standard – Callisto Network Security Department Statement | CoinMarketCap

I would strongly recommend to add the described problem to the “Security Considerations” section of the EIP.

I would also recommend adding a suggestion “Any contract MUST implement a special function that would allow for extraction of accidentally deposited tokens”

```auto
function rescueERC20(address _token) onlyOwner external
{
    // This function must extract "stuck" tokens
    // that were deposited to the contract by mistake and couldn't be rejected
    // because the `transfer` function does not allow for error handling.
    // Implementation logic can vary depending on the contract, this is an example.
    amount = IERC20(_token).balanceOf(address(this));
    IERC20(_token).transfer(msg.sender, amount);
}
```

---

**vittominacori** (2023-10-27):

Thanks for reporting.

We all know that the ERC-20 standard lacks the ability to notify token receiver or to verify whether the recipient is capable of handling the tokens received. This is exactly why ERC-1363 was built.

ERC-1363 is not intended to solve this problem or be a new standard to replace ERC-20, but adds these features while maintaining backward compatibility with ERC-20.

ERC-20 has been around since the early days and all decentralized applications use this standard. It has market capitalization and cannot be easily stopped or replaced with a new (modern) standard. We have to live with this standard for a medium/long period. As long as the ecosystem evolves, any user interface should intercept these design pattern issues and guide the user to make their choice.

Since this is an ERC-20 design issue, and since ERC-1363 only extends ERC-20 and adds methods that should not be affected by this issue, I think the security consideration should be in the ERC-20 specification, and then we could refer to it as we have already done for the question of allowances.

As for the recovery suggestion, it is not related to ERC-1363 nor to ERC-20, but concerns any contract that can receive ERC-20, ERC-721 or any other asset that can be transferred. If you would like to discuss this, please check out [Token Recover](https://github.com/vittominacori/eth-token-recover).

