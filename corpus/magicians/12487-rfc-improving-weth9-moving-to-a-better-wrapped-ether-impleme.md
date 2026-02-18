---
source: magicians
topic_id: 12487
title: "RFC: Improving WETH9 - Moving to a better Wrapped Ether Implementation"
author: Philogy
date: "2023-01-08"
category: Magicians > Primordial Soup
tags: [token]
url: https://ethereum-magicians.org/t/rfc-improving-weth9-moving-to-a-better-wrapped-ether-implementation/12487
views: 2956
likes: 1
posts_count: 10
---

# RFC: Improving WETH9 - Moving to a better Wrapped Ether Implementation

## Motivation

There are several issues and inefficiencies that face smart contract developers when using the widely used [WETH9](https://etherscan.io/token/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2) implementation. This post aims to discuss tradeoffs of different design details of a new and improved WETH contract. I’ve already begun working on it under the name “YAM-WETH”, standing for “Yet Another Maximized Wrapped Ether implementation”. You can view the repo [here](https://github.com/philogy/yam-weth).

## Core WETH9 Issues

### Silent Fallback Method

WETH9 has a notorious silent fallback method that will silently accept any call even if the selector does not match any implemented method. This is a common foot gun for smart contract developers who expect most token contracts to revert if they’re called with a method they do not implement. This was also the cause of [Multicoin’s $ 1M bridge hack](https://medium.com/zengo/without-permit-multichains-exploit-explained-8417e8c1639b).

### Inefficient Common Patterns

There are some very common patterns that smart contracts go through when contract’s such as DEX routers interact with WETH, however due to WETH9 only implementing a basic `deposit` and `withdraw` method these patterns usually require multiple calls and otherwise unused `receive()` methods.

- “Deposit & Transfer”

```solidity
WETH9.deposit{ value: amount}();
WETH9.transfer(recipient, amount);
```
- “Withdraw & Transfer”

```solidity
receive() external payable {
    require(msg.sender == address(WETH9));
}
// ...
WETH9.withdraw(amount);
SafeTransferLib.safeTransferETH(recipient, amount);
```
- “Withdraw From”

```solidity
receive() external payable {
    require(msg.sender == address(WETH));
}
// ...
WETH9.transferFrom(account, address(this), amount);
WETH9.withdraw(amount);
```
- “Withdraw From & Transfer”

```solidity
receive() external payable {
    require(msg.sender == address(WETH));
}
// ...
WETH9.transferFrom(from, address(this), amount);
WETH9.withdraw(amount);
SafeTransferLib.safeTransferETH(to, amount);
```

Outside of simplicity there’s no reason why patterns couldn’t be made accessible via individual, direct calls. Making such patterns accessible within a single call allows for direct crediting of balances without the unnecessary costs of accessing added intermediary storage slots.

## Design Tradeoffs

### General Efficiency

While my current implementation is technically in solidity most of the actual business logic is written in inline-assembly. The tradeoff here is implementation simplicity & ease of auditability vs. efficiency. However I believe for a contract as widely used as WETH the implementation should aim to be as efficent as possible because of how commonly WETH is used in the wider ecosystem.

### Leveraging Leftover Space In The Balance Slot

Since WETH’s total supply is fundamentally limited by the total amount of circulating ETH it’s total supply, at least on mainnet is likely to always fit within 96-bits giving it a maximum of 79.2B ETH. This leaves 160-bits leftover in the storage slot that stores user balances.

**Storing a “Primary Operator” in the leftover space**

In the current YAM-WETH implementation, this is used to store the address of a special “primary operator” of the individual account that can spend WETH on behalf of an account as if they had an infinite allowance. Since it’s stored in the balance slot this allows for more efficient setting and transfer froms for that operator because the allowance slot does not have to be touched.

The question also arises whether the `allowance` method should also return `type(uint).max` for the primary operator to make it play better with frontends and other contracts. One could also imagine emitting `Approval` events when the primary operator is set although this would complicate the `approve` method a little.

### ERC-2612 Permits

Since the ERC-2612 standard fundamentally relies on EC-Recover there’s a question as to how long-lasting an implementation that implements the standard will be due to quantum resistance. The ecosystem will surely have to find a solution since other tokens also depend on EC-Recover but it’s not entirely known how Ethereum will implement quantum resistance. If it’s mainly done via account abstraction an ERC-2612 compliant implementation may become vulnerable in the future.

### Flash Minting

The main tradeoff of allowing “flash minting” would be that WETH may become partially unbacked for the duration of a transaction. This may prevent certain contracts, in certain contexts from always redeeming WETH for ETH 1:1. This downside can be limited but not eliminated by putting a cap on the percentage of the supply that can be flash minted. This will ensure that unless the borrower is able to trigger a large redemption outside of their loan contracts are unlikely to ever be in a situation where they cannot redeem their WETH for ETH 1:1 unless ownership is extremely concentrated.

## Closing Words

WETH is an incredibly important piece of the smart contract ecosystem therefore I think it’s extremely important I consider and take feedback if I aim to create a newer version that’s not only improved but also widely used.

## Replies

**Pandapip1** (2023-01-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/philogy/48/4714_2.png) Philogy:

> ### ERC-2612 Permits

How about using EIP-2771? I’m working on an extension to it that requires a lower amount of trust.

---

**xinbenlv** (2023-01-09):

Thanks for the proposal. [@Philogy](/u/philogy)

Also consider ERC-5453 Endorsement to replace ERC-2612 in which case you can supply the permit ECDSA or other type of signature with within the same TX call?

---

**Philogy** (2023-01-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pandapip1/48/5511_2.png) Pandapip1:

> How about using EIP-2771? I’m working on an extension to it that requires a lower amount of trust.

Don’t see how a *trusted* forwarder would require less trust? Wouldn’t a ERC2771 forwarder implementing some type of ec-recover based authentication scheme also be vulnerable to quantum algorithms in the future? Not sure I fully understand the benefit.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> Also consider ERC-5453 Endorsement to replace ERC-2612 in which case you can supply the permit ECDSA or other type of signature with within the same TX call?

Alternative authentication methods are interesting but if I allow for ECDSA signature-based permits, even if it is under another standard it doesn’t answer the fundamental question of whether or not it should be included or how it could be safely deprecated.

---

**Pandapip1** (2023-01-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/philogy/48/4714_2.png) Philogy:

> Don’t see how a trusted forwarder would require less trust? Wouldn’t a ERC2771 forwarder implementing some type of ec-recover based authentication scheme also be vulnerable to quantum algorithms in the future? Not sure I fully understand the benefit.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pandapip1/48/5511_2.png)
    [Trustless EIP-2771](https://ethereum-magicians.org/t/trustless-eip-2771/12497) [Primordial Soup](/c/primordial-soup/9)



> This is a pretty simple idea: instead of trusting EIP-2771 forwarders to return authorized addresses, instead, if an address would be taken, two addresses can be taken: the address of the forwarder, and the address assigned by the forwarder. For example, EIP-20 would be extended with the following functions:
> function balanceOf(address _ownerForwarder, address _owner) public view returns (uint256 balance)
> function transfer(address _toForwarder, address _to, uint256 _value) public returns (bool s…

---

**xinbenlv** (2023-01-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/philogy/48/4714_2.png) Philogy:

> Alternative authentication methods are interesting but if I allow for ECDSA signature-based permits, even if it is under another standard it doesn’t answer the fundamental question of whether or not it should be included or how it could be safely deprecated.

Are you designing specification of a standard or a specification for the implementation?

---

**Philogy** (2023-01-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> Are you designing specification of a standard or a specification for the implementation?

Neither.

I’m requesting feedback to what extent it’d be problematic to allow for ECDSA based authentication.

---

**xinbenlv** (2023-01-10):

Oh, sure. happy to chime in.

Since ETH client nodes use ECDSA to validate TX…

That is to say, if ECDSA becomes insecure (e.g. by bug or by quantum computation advancement), we have much bigger problem than WETH with ECDSA on-chain validation becomes a problem. Most contracts compliant with ERC-712 and ERC-1271 must change. I am sure at the time the whole Ethereum ecosystem will have a discussion then.

Therefore, in the context of WETH and its design decision, I suggest you disregard the possibility of ECSDA being insecure, just like we will worry less about ETH’s PoS stops working for any smart contract design as well. It will be solved a a different level in the future if becomes a problem.

---

**joeysantoro** (2023-10-26):

[@Philogy](/u/philogy) [@xinbenlv](/u/xinbenlv) I’m working on a similar new wrapped eth which leverages the above ideas plus [EIP-7535](https://ethereum-magicians.org/t/eip-7535-eth-native-asset-tokenized-vault/16068/5) and EIP-1153 transient approvals

I came across ERC-5453 and think there is a cool opportunity to add a combined functionality / standardizartion by making the endorsement use transient storage.

Would be keen to hear thoughts on this

---

**sbacha** (2023-10-31):

Guys, we want WETH9, that’s it, that’s all the functionality it needs.

The reason to redeploy an updated WETH9 is so that we can have the same canonical address on different chains. That currently is not the case.

Changing WETH makes it *not* WETH. People have already done that, and it has caused issues (see Gnosis Chain’s version of WETH).

I can not stress this enough, the current feature set is all that is needed.

