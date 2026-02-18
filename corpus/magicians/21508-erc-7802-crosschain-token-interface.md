---
source: magicians
topic_id: 21508
title: "ERC-7802: Crosschain Token Interface"
author: drgorilla.eth
date: "2024-10-30"
category: ERCs
tags: [token, cross-chain]
url: https://ethereum-magicians.org/t/erc-7802-crosschain-token-interface/21508
views: 4215
likes: 27
posts_count: 15
---

# ERC-7802: Crosschain Token Interface

This ERC introduces a minimal interface for tokens to communicate cross-chain. It allows bridges with mint and burn rights to send and relay token transfers with a standardized API.

The interface is bridge agnostic and fully extensible.

PR:

https://github.com/ethereum/ERCs/pull/692

## Replies

**radek** (2024-11-06):

I welcome the minimalism.

Yet, how do you expect the compatibility with xERC20? ( ERC 7281 ) - would be nice to have that elaborated in the compatibility section.

---

**amattm** (2024-11-08):

+1 to [@radek](/u/radek) s question.

---

**ernestognw** (2024-11-28):

Hi [@drgorilla.eth](/u/drgorilla.eth), I like the ERC design as it is pretty minimal!

We’ve been working on ERC-7786 (crosschain messaging gateways) to define a minimal standard to simply “get a message to another chain”. I tried to implement ERC-7802 on top of ERC-7786. [Here’s the code (WIP)](https://github.com/OpenZeppelin/openzeppelin-community-contracts/pull/27). We’re planning to include it in the [community version of OpenZeppelin Contracts](https://github.com/OpenZeppelin/openzeppelin-community-contracts)

The idea to combine these 2 standards is because ERC-7802 defines an interface where a bridge address can mint or burn, but I would argue that it would be better if ERC-7802 depends on ERC-7786 to make the crosschain token its messaging gateway. This way, the bridge integration is abstracted away and the ERC20 can expose a `crosschainTransfer` that burns tokens on the source chain and relays a mint instruction to the destination chain.

EDIT: I’m rethinking the `crosschainTransfer` idea since I see the reasoning behind offloading the logic from the token. Still, we appreciate feedback, we’re planning to put this into the library pretty soon

---

**ernestognw** (2024-11-29):

They complement each other. ERC-7802 defines the minimal interface for an ERC-20 token to communicate cross-chain, but it doesn’t specify how a protocol should send a cross-chain message to communicate with such tokens. Similarly, it doesn’t specify how a user will transfer tokens on-chain.

I agree this standard should remain minimal, but I would agree it may benefit if they specify an optional interface for the “token bridge” that depends on ERC-7786. It also makes sense to put it in another ERC.

---

**Particle** (2024-12-04):

Regarding compatibility with xERC20 (ERC-7802), I wrote this document:


      ![](https://ethereum-magicians.org/uploads/default/original/2X/0/07f036d2a2c0489763da12d6f66e33499637ee42.png)

      [Notion](https://defi-wonderland.notion.site/xERC20-ERC7802-compatibility-14c9a4c092c780ca94a8cb81e980d813?pvs=4)



    ![](https://ethereum-magicians.org/uploads/default/optimized/2X/5/5526bc08d6fc05b1c584ed209f6866ba872b3951_2_690x362.png)

###



A tool that connects everyday work into one space. It gives you and your teams AI tools—search, writing, note-taking—inside an all-in-one, flexible workspace.

---

**frangio** (2024-12-05):

Can it be an issue that an adapter for xERC20 doesn’t emit CrosschainMint/Burn? This is not discussed in the document, but these events are specified as “MUST”. If these events wont be reliable, it might make sense to lower the requirement in the spec (SHOULD or MAY) or even remove it.

---

**Particle** (2024-12-18):

The adapter itself is not an implementation of the `IERC7802` standard, nor is it an ERC20 token. Instead, it serves as an intermediary to enable a bridge—already compliant with the `IERC7802` API—to interact with xERC20 tokens that may not natively implement this interface.

Since the adapter is merely a compatibility layer and not a token contract, it is not required to emit `CrosschainMint` or `CrosschainBurn` events. These events are only mandatory for contracts that directly implement `IERC7802`. The role of the adapter is to translate standardized bridge calls into the xERC20’s existing `mint` and `burn` functionality, ensuring operational compatibility.

---

**Arvolear** (2025-01-08):

Love the proposal! There is definitely a problem with bridges as every provider forces to use their own `mint/burn` interface.

Have several questions though:

1. Maybe it is worth expanding the crosschainMint() and crosschainBurn() interfaces to accept an additional bytes parameter?
 So the new function signatures will be:

```solidity
function crosschainMint(address _account, uint256 _amount, bytes memory _payload);
function crosschainBurn(address _account, uint256 _amount, bytes memory _payload);
```

 Possibly this can allow ERC-7802 tokens to perform some business-specific logic.
2. In the provided reference implementation, shouldn’t there be token allowance spending in the crosschainBurn() function?

```solidity
function crosschainBurn(address _from, uint256 _amount) external onlyTokenBridge {
    _spendAllowance(_from, msg.sender, _amount); // TokenBridge understands current behavior and prohibits grefing.

---

**Particle** (2025-01-09):

Great points!

1. I understand that incorporating a bytes parameter could facilitate business-specific logic; however, it goes against the design goal of maintaining a minimal interface. The goal is to keep tokens straightforward and allow for more complex hooks or logic to be handled at the bridge level.
Do you have any examples in mind of logic that would require using these bytes and cannot be implemented at the bridge level?
2. In this scenario, we assume the bridge is trusted and does not require allowance checks. Including _spendAllowance would be more consistent with systems like xERC20, where allowances are essential. However, for this minimal approach, it is not necessary. If needed, allowances can always be added later for specific implementations.

---

**modtail** (2025-01-14):

I agree with the rational and adding metadata byte param. ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

---

**radek** (2025-01-15):

Being in the middle of the implementation into ERC20 using both xERC20 and ERC7802.

I believe the mentioned `msg.sender` is not correct in the standard:

> Events
> CrosschainMint
>
>
> MUST trigger when crosschainMint is successfully called. The _sender parameter MUST be set to the msg.sender at the time the function is called.
>
>
> event CrosschainMint(address indexed _to, uint256 _amount, address indexed _sender);

I assume the rationale to emit sender is to filter out which events are related to the particular bridge.

In the case there is an adapter between the bridge and ERC20 token, such adapter becomes msg.sender.

---

**skeletor** (2025-01-31):

This is an interesting point. I see the concern about the adapter becoming `msg.sender`, but I don’t necessarily think it’s an issue for the event to emit the adapter’s address. If we change `_sender`, we might introduce inconsistencies or require extra logic to track the original caller. Keeping `msg.sender` as-is ensures consistency, and indexers can be designed to trace the adapter path when necessary.

---

**ilovelili** (2025-02-19):

Hi does ERC-7802 has a public audit report so far? Thank you! [@drgorilla.eth](/u/drgorilla.eth)

---

**radek** (2025-03-12):

FYI - here is the draft of the minimal xERC20 standard:



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/961/files)














####


      `ethereum:master` ← `radeksvarz:patch-2`




          opened 12:10PM - 12 Mar 25 UTC



          [![radeksvarz](https://avatars.githubusercontent.com/u/6020891?v=4)
            radeksvarz](https://github.com/radeksvarz)



          [+224
            -0](https://github.com/ethereum/ERCs/pull/961/files)







Minimal interface of Sovereign Bridged Token (minimal xERC20)

