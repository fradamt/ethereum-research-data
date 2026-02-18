---
source: ethresearch
topic_id: 23274
title: Interactive No Opt-in Stealth Addresses
author: zemse
date: "2025-10-17"
category: Privacy
tags: []
url: https://ethresear.ch/t/interactive-no-opt-in-stealth-addresses/23274
views: 297
likes: 2
posts_count: 5
---

# Interactive No Opt-in Stealth Addresses

A heads up to prevent confusion, this is different idea from ERC-5564 Stealth Addresses where a sender would compute a stealth address for a non-interactive receiver.

## Summary

- In this idea, the receiver computes the address and shares with sender (not onboarded to privacy, uses legacy systems like metamask, exchanges, public wallets, smart contracts).
- This is an app that can build on top of an existing privacy scheme.
- To be able to stay private, the people you transact with do not need to be using a privacy based wallet. But you need the underlying privacy scheme to have a sufficiently large anonymity set.
- It is possible for the app to be interoperable with other privacy schemes using ERC-6538, making it work with users using its own privacy scheme, no privacy scheme and potentially other privacy schemes too.

## Motivation

Most stealth address solutions are both user opt in, i.e. both user need to follow the same protocol or set of rules. And there are many protocols. Aztec, ERC-5564, Railgun, Tornado Nova, zkBoB and many more.

So if a person A wants to pay person B, both the personas must be signed up for the same protocol. If we assume that, then it is flowers and rainbows, but in practical situation most people don’t use any privacy protocols and if some use then it might not be the one you have.

Current solutions:

- User joins multiple popular privacy protocols to be compatible with anyone out there.
- User just stay in public Ethereum while creating multiple wallet addresses where all of our transactions are public. While funds are fragmented to prevent people from figuring out your true balance, user can receive funds from anyone. But have to take care that the addresses don’t directly connect with each other and use things like tornado cash.
- Simply keep funds on a centralised exchange to receive deposits from anyone.

A huge challenge in privacy adoption for payments is a requirement that both the participants sender and receiver should be using a software that supports the same protocol. This causes signups in privacy protocols due to novelty but the user mostly ends up doing public transactions because people they interact with didn’t sign up, unless they are lucky to have peers that have signed up into same system.

## Abstract

This post is about potential solution that can allow a user to opt-in to keep their balances reasonably private while enabling them to send or receive funds to and from public ethereum addresses. This solution is an app that can be built on top of any existing UTXO based privacy scheme similar to tornado nova. It is even ok if the app is integrated by at least one wallet. The user can generate multiple EVM addresses by themselves. They interact with a sender giving them a new address. This address is a pre-computed using CREATE2. Once funds are received, the wallet software collects the funds using a relayer into the underlying privacy scheme creating a UTXO that the user can spend in future transactions.

This solution is interactive. In most of the day-to-day use cases like payments to friends or clients, interaction is involved as people still ask “do you want on mainnet or some specific L2s? prefer ETH or DAI or USDC?”. Here the user will generate a fresh address themselves and give it to the sender, that’s the interaction. The CREATE2 stealth address does not need to be an EIP/ERC since it is rather an app and the other users does not need to be opt-in for follow some new protocol.

## How does it work?

I can link to the code from a PoC from last year to express some details.

### 1. User joins this system

The user installs software which follows the described protocol. It generates a 32 byte secret and stores it for future use.

### 2. User wants to receive money from someone

User generates a fresh stealth address, which is generated as follows:

1. Hash of two words: 32 byte secret and a 32 byte nonce (can be incremental)
2. The hash is 32 byte salt used with CREATE2 to get an address https://github.com/ultralane/contracts/blob/b8e17ce7099ffb358488579927308d5f73716dc3/contracts/MixerPool.sol#L162-L166
3. User (receiver) interacts with the sender by sending them an EVM address.
4. The sender can send money to this address anyhow they want, through metamask, withdrawal from exchange or withdrawal from a privacy scheme.

### 3. User receives money from a client

1. This money is sent to a pre-computed address which is/will be a contract. https://github.com/ultralane/contracts/blob/b8e17ce7099ffb358488579927308d5f73716dc3/contracts/StealthAddress.sol
2. User’s wallet software once it is online and notices balance on the stealth address:

 It generates a secret note based on the specification of underlying privacy scheme. Usually such notes are the secret along with amount and a random binding to prevent collisions. https://github.com/ultralane/circuits/blob/42e39cd95345c6c47ee8b363854262ab03f29731/lib/src/note.nr#L3-L7
3. It locally proves that user knows the preimage to the salt.
4. It also adds the note commitment in it so that a relayer cannot tamper it (this part is not present in the PoC).
5. This payload is then given to a relayer that calls a function on the pool which makes a public transaction moving the funds into the privacy pool spendable by the user. https://github.com/ultralane/contracts/blob/b8e17ce7099ffb358488579927308d5f73716dc3/contracts/MixerPool.sol#L133-L160
6. Additionally stealth address can also register itself on the ERC-6538 registry. So that future transfers to this address from some opt-in privacy users can use an efficient route.

## User wants to send money

- User’s wallet software can check using ERC-6538 registry if the address is a stealth address and of what kind. If it turns out to be using a supported privacy protocol then handle it.

 If it is used the underlying privacy scheme, then directly spend the UTXO creating a new UTXO spendable by the receiver as per the specification of the underlying privacy protocol.
- If that is a ERC-5564: Stealth Addresses, then compute receiving address according to the protocol and to their stealth address.
- Otherwise that address is not using any privacy scheme so just withdraw funds to that address.

## Conclusions

- This solution does not directly work in case of receiving donations from unknown people in a non-interactive way. Like putting an address on your GitHub readme for any funding. Since all transactions to the same address will be visible. This is exactly where ERC-5564 shines as the sender creates a new address here, however it requires the sender to be opt-in. For donations. On repositories, people usually list many addresses like BTC, ETH, Monero, they could list another x-address of the privacy scheme Railgun or more, instead of an eth address (because it is likely user has no idea about stealth addresses or is using an outdated wallet software).
- It can be possible to combine CREATE2 stealth addresses with ERC-5564 using ERC-6538 and more privacy schemes. Basically during funds collection, the CREATE2 stealth address can register itself in the registry with multiple privacy schemes. I realise that ERC-6538 is actually very powerful and can make it possible for a wallet to interoperate with multiple privacy schemes.
- The CREATE2 stealth address are indistinguishable with other EOAs until the funds in it are collected, which will happen at some point. So it is possible for someone to scan the chain to easily find used stealth addresses and trace funds sent into privacy pools.
- The issues of revealing IP to relayers are ofcouse there.

## Replies

**MicahZoltu** (2025-10-17):

How is this different from a wallet that just generates a new EOA for each recipient?

---

**zemse** (2025-10-17):

In a wallet like metamask that generates multiple addresses there is a notion of switching into different accounts to see balance in each account.

In this kind of wallet there would be a consolidation of all of your assets together. Like you receiced 100 USDC on Account One and 200 USDC on Account Two, 300 USDC on account three. The wallet should display 600 USDC. And if you want to spend 550 USDC you can do it. Also while sending you can decide if you want to send anonymously (directly from mixing pool) or through one of your  stealth address identity (e.g. for stateful interactions in DeFi).

Conceptually, it’s exactly the same as metamask multiple accounts + mixing pool where user manually does the deposits into mixing pool themselves and manage many addresses. But it is complexity that can be easily abstracted in the app layer. Receiving money on one address and using another address identity to use it (like DeFi or betting) can be done technically using a mixer but people end up not doing it because it’s a lot of steps.

---

**aguzmant103** (2025-10-19):

Iirc implementations of stealth addresses already handle the complexity of creating addresses and aggregating balances. For example Fluidkey you can give people an ENS (andyguzman.fkey.eth) which people can send money but every time it gets used it rotates to a fresh address  I believe Curvey and Umbra Cash have similar propoerties

Iiu. what I see novel here is integrating stealth addresses that automatically sends to mixers/pools, which combines both and gives forward secrecy

---

**zemse** (2025-10-20):

I’ve tried Fluidkey it does provides a great UX for this problem without using zk proofs. They still have to connect your addresses (without a warning) incase your payment is huge. The ENS off-chain resolver seems to use the viewing keys (stored in their infrastructure?) to enable non-interactiveness. Maybe in future it is possible to use iO for blackboxing the off-chain resolver without directly sharing the viewing key with them.

Umbra cash still seems to require both participants to use the application.

I tried Curvey V2 testnet and they are doing this and it’s single user opt-in! Only that they have their own privacy scheme which means limited anonymity set but it is fair for now because we don’t have a dominating go-to privacy layer on all chains to build wallets upon, also multi language SDKs for privacy layers needed (Kohaku can fix this).

