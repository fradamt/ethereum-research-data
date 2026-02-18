---
source: magicians
topic_id: 12625
title: "Review ERC-6358: Omniverse Distributed Ledger Technology (O-Token Protocol)"
author: xiyu_meta
date: "2023-01-19"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/review-erc-6358-omniverse-distributed-ledger-technology-o-token-protocol/12625
views: 3931
likes: 2
posts_count: 11
---

# Review ERC-6358: Omniverse Distributed Ledger Technology (O-Token Protocol)

## Updates

- [2023.3.1] The name of this EIP might be changed according to the suggestions
- [2023.3.9] Submit some updates and add the source codes for trying.
- [2023.3.20] The updates have been merged. The latest version can be found here
- [2023.4.6] Slim down and make the presentation more succinct. We are preparing the first Demo of an ERC-6358 token.
- [2023.4.18] Add a detailed analysis for the double-spend attack issue.
- [2023.5.30] Update the implementation examples
- [2023.6.1] A simple Testnet (Demo) to try the first ERC-6358 tokens. The related front can be found at the Omniverse Demo, and we are preparing the related auto-deployment tools.
- [2024.2.28] It’s a long time to update, as in the last 8 month, we are building a zk-based omni-executor mentioned here for this protocol. The zk-related components are based on plonky2 and now we have finished a basic version of it. Next, we will make some optimization of the performance and this will be opensoure soon.
- [2024.5.16] A testnet based on erc-6358 has been launched. plonky2 is used to generate recursive proofs in FRI, and Halo2 based stark verifier is used to generate the final KZG proof, which is more friendly to on-chain smart contracts. Part of the code of the circuit is open sourceed



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-6358.md)





####

  [master](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-6358.md)



```md
---
eip: 6358
category: ERC
status: Moved
---

This file was moved to https://github.com/ethereum/ercs/blob/master/ERCS/erc-6358.md
```










## Abstract

The `ERC-6358` (Omniverse DLT) is a new **application-level** (ERC) token protocol built upon multiple existing L1 public chains, enabling asset-related operations such as transfers and receptions running **globally** and **synchronously** over different consensus spaces.

Figure.1 Architecture



[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/5/5c66a509bbd87bc0685356d5e645c4bdb4832138_2_690x403.png)image3368×1968 410 KB](https://ethereum-magicians.org/uploads/default/5c66a509bbd87bc0685356d5e645c4bdb4832138)

## Motivation

- The current paradigm of token bridges makes assets fragment.
- If tokens like ETH were transferred to another chain through the current token bridge, if the chain broke down, it will be lost for users.

The core of `ERC-6358` is **synchronization** instead of **bridge-transferring**, even if all the other chains break down, as long as one chain is still running, user’s assets will not be lost.

- The fragment problem will be solved.
- The security of users’ multi-chain assets can be greatly enhanced.

## Rationale

With `ERC-6358`, we can create a global token protocol, that leverages smart contracts or similar mechanisms on existing blockchains to record the token states synchronously. The synchronization could be made by trustless off-chain synchronizers.

### Architecture

As shown in [Figure.1](#architecture), smart contracts deployed on different chains execute `o-transactions` of `ERC-6358` tokens synchronously through the trustless off-chain synchronizers.

- The ERC-6358 smart contracts could be referred to as Abstract Nodes. The states recorded by the Abstract Nodes that are deployed on different blockchains respectively could be considered as copies of the global state, and they are ultimately consistent.
- Synchronizer is an off-chain execution program responsible for carrying o-transactions from the ERC-6358 smart contracts on one blockchain to the others. The synchronizers work trustless as they just deliver o-transactions with others’ signatures, and details could be found in the workflow.

### Principle

- There should be a global user identifier for ERC-6358, which is recommended to be referred to as Omniverse Account (o-account for short) in this article. The o-account is recommended to be expressed as a public key created by the elliptic curve secp256k1. A mapping mechanism is recommended for different environments.
- The synchronization of the o-transactions guarantees the ultimate consistency of token states across all chains. The related data structure can be found here: solidity and here: rust.

A nonce mechanism is brought in to make the states consistent globally.
- The nonce appears in two places, the one is nonce in o-transaction data structure, and the other is account nonce maintained by on-chain O-DLT smart contracts.
- When synchronizing, the nonce in o-transaction data will be checked by comparing it to the account nonce.

#### Workflow

- Suppose a common user A and her related operation account nonce is $k$.
- A initiates an o-transaction on Ethereum by calling IERC6358::sendOmniverseTransaction. The current account nonce of A in the ERC-6358 smart contracts deployed on Ethereum is $k$ so the valid value of nonce in o-transaction needs to be $k+1$.
- The ERC-6358 smart contracts on Ethereum verify the signature of the o-transaction data. If the verification succeeds, the o-transaction data will be published by the smart contracts on the Ethereum side. The verification includes:

whether the balance (FT) or the ownership (NFT) is valid
- and whether the nonce in o-transaction is $k+1$

The `o-transaction` SHOULD NOT be executed on Ethereum immediately, but wait for a time.
Now, `A`’s latest submitted `nonce in o-transaction` on Ethereum is $k+1$, but still $k$ on other chains.
The off-chain synchronizers will find a newly published `o-transaction` on Ethereum but not on other chains.
Next synchronizers will rush to deliver this message because of a rewarding mechanism. (The strategy of the reward could be determined by the deployers of `ERC-6358` tokens. For example, the reward could come from the service fee or a mining mechanism.)
Finally, the `ERC-6358` smart contracts deployed on other chains will all receive the `o-transaction` data, verify the signature and execute it when the **waiting time is up**.
After execution, the `account nonce` on all chains will add 1. Now all the `account nonce` of account `A` will be $k+1$, and the state of the balances of the related account will be the same too.

## Reference Implementation

### Omniverse Account

- An Omniverse Account example: 3092860212ceb90a13e4a288e444b685ae86c63232bcb50a064cb3d25aa2c88a24cd710ea2d553a20b4f2f18d2706b8cc5a9d4ae4a50d475980c2ba83414a796

The Omniverse Account is a public key of the elliptic curve secp256k1
- The related private key of the example is:  cdfa0e50d672eb73bc5de00cc0799c70f15c5be6b6fca4a1c82c35c7471125b6

#### Mapping Mechanism for Different Environments

In the simplest implementation, we can just build two mappings to get it. One is like `pk based on sece256k1 => account address in the special environment`, and the other is the reverse mapping.

The `Account System` on `Flow` is a typical example.

- Flow has a built-in mechanism for account address => pk. The public key can be bound to an account (a special built-in data structure) and the public key can be got from the account address directly.
- A mapping from pk to the account address on Flow can be built by creating a mapping {String: Address}, in which String denotes the data type to express the public key and the Address is the data type of the account address on Flow.

## Security Considerations

### Attack Vector Analysis

According to the above, there are two roles:

- common users who initiate a o-transaction (at the application level)
- and synchronizers who just carry the o-transaction data if they find differences between different chains.

The two roles might be where the attack happens:

#### Will the synchronizers cheat?

- Simply speaking, it’s none of the synchronizer’s business as they cannot create other users’ signatures unless some common users tell him, but at this point, we think it’s a problem with the role common user.
- The synchronizer has no will and cannot do evil because the transaction data that they deliver is verified by the related signature of others(a common user).
- The synchronizers will be rewarded as long as they submit valid o-transaction data, and valid only means that the signature and the amount are both valid. This will be detailed and explained later when analyzing the role of common user.
- The synchronizers will do the delivery once they find differences between different chains:

If the current account nonce on one chain is smaller than a published nonce in o-transaction on another chain
- If the transaction data related to a specific nonce in o-transaction on one chain is different from another published o-transaction data with the same nonce in o-transaction on another chain

**Conclusion: The *synchronizers* won’t cheat because there are no benefits and no way for them to do so.**

#### Will the common user cheat?

- Simply speaking, maybe they will, but fortunately, they can’t succeed.
- Suppose the current account nonce of a common user A is $k$ on all chains.
- Common user A initiates an o-transaction on ERC-6358 smart contracts on Chain P first, in which A transfers 10 o-tokens to an o-account of a common user B. The nonce in o-transaction needs to be $k+1$. After signature and data verification, the o-transaction data(ot-P-ab for short) will be published on ERC-6358 on Chain P.
- At the same time, A initiates an o-transaction with the same nonce $k+1$ but different data(transfer 10 o-tokens to another o-account C) on Ethereum. This o-transaction(named ot-E-ac) will pass the verification on ERC-6358 smart contracts on Ethereum first, and be published.
- At this point, it seems A finished a double spend attack and the ERC-6358 states on Chain P and Ethereum are different.
- Response strategy:

As we mentioned above, the synchronizers will deliver ot-P-ab to the ERC-6358 smart contracts on Ethereum and deliver ot-E-ac to the ERC-6358 smart contracts on Chain P because they are different although with the same nonce. The synchronizer who successfully submits the o-transaction first(or in the first few) will be rewarded as the signature is valid.
- Both the ERC-6358 smart contracts on Chain P and Ethereum will find that A did cheating after they received ot-E-ac and ot-P-ab respectively as the signature of A is non-deniable.
- We mentioned above that the execution of an o-transaction will not be done immediately and instead there needs to be a fixed waiting time. So the double spend attack caused by A won’t succeed.
- There will be many synchronizers waiting for delivering o-transactions to get rewards. So although it’s almost impossible that a common user can submit two o-transactions to two chains, none of the synchronizers deliver the o-transactions successfully because of a network problem or something else, we still provide a solution:

The synchronizers will connect to several native nodes of every public chain to avoid the malicious native nodes.
- If it indeed happened that all synchronizers’ network break, the o-transaction will be synchronized when the network recovered. If the waiting time is up and the cheating o-transaction has been executed, we can still revert it from where the cheating happens according to the nonce in o-transaction and account nonce.

`A` will be punished (lock his account or something else, and this is about the certain tokenomics determined by developers according to their own situation).

**Conclusion: The *common user* maybe cheat but won’t succeed.**

## Copyright

Copyright and related rights waived via CC0.

## Additional Information

We are a team focusing on multi-chain interoperability for years, and we have some experience and open-source contributions in this field. We are always dedicated to improving the convenience and security of the cross-chain experience, and we have proposed the first multi-chain interoperability solution Granted by W3F, with milestones all achieved.

In addition, we will provide a mechanism to make Omniverse Token compatible with current ERC20/ERC721 and native tokens, that is, omniverse tokens could be exchanged on current DEX like Uniswap with others. This is related to an abstract account smart contract mechanism, as it is highly recommended that a single EIP contain a single key proposal or new idea, we won’t describe more details about this point here but still we will provide an implementation of it.

## Replies

**yyd106** (2024-03-12):

If we do synchronization in all the chains. It seem like we go back to only one chain

---

**xiyu_meta** (2024-03-13):

Nice discussion.

Actually, you mentioned one part of our target, that is:

- Easy operation: Operate your assets locally(just on any single chain you are familiar with), just as operating the erc-20/721 and native token on one chain.

and the more important part is:

- Global accessing: Access your assets globally(on any other chains you need, just as the use case in the workflow), by synchronization.

---

**yyd106** (2024-03-13):

What my understanding of **bridge-transferring**, is to transfer assets cross-chain. If that’s the case, how could synchronization handle this?

---

**xiyu_meta** (2024-03-14):

The key point is `ERC-6358` uses an **absolutely different paradigm** compared to `bridge-transferring`.

To be simple, two things may help you understand.

- Firstly, ERC-6358 is a new token standard derived from ERC-20/721
- Second, ERC-6358 treats current blockchains as abstract nodes to record status

---

**yyd106** (2024-03-14):

So, my question is, if we shift the paradigm to synchronization, what is the difference from having just one ETH chain? Because all account records on Ethereum are also not fragmented.

---

**xiyu_meta** (2024-03-15):

If you only use Ethereum, that’s it.

But if you want to use, for example, USDT(maybe O-USDT), in all Web3 ecosystems without dividing and fragmenting, but still with Ethereum’s security, that is what ERC-6358 solves.

---

**JimmyShi22** (2024-08-01):

If two chains receive transaction for the same account simultaneously, how can we resolve this data race issue?

---

**xiyu_meta** (2024-08-03):

It depends on the concrete implementation.

In the early versions, off-chain synchronizers took the submitted transactions from one chain to another. Synchronizers are trustless as users sign the transactions and the synchronizers just took. Besides, a waiting time is needed for `erc-6358` contracts on both chains. The details can be found [here](https://ethereum-magicians.org/t/review-erc-6358-omniverse-distributed-ledger-technology-o-token-protocol/12625#will-the-common-user-cheat-14).

In the current version, a `zk-executor` layer was brought in, where transactions are confirmed first. And more importantly, the gas cost is highly reduced for each transaction. The `zk-executor` is an instance of the `Modular blockchain`, whose sequencer and `DA` are smart contracts on suitable blockchains. For the zk-part, a heterogeneous circuit architecture was adopted. Simply, the zk-circuit is implemented by a hybrid of `plonky2` and `sp1`.

---

**peersky** (2024-08-03):

I’ve worked enough of time on security monitoring aspects of cross-chain tokens and I must admit it’s very complex in current implementation.

The banal example is need to monitor for invariant state. With all of that logic when one bridge burns, another bridge mints, then whenever user exits back to L1 it burns, but now on L2 it quickly becomes a mess which is very complex to monitor for.

This on it own creates very tricky situations, where invariants could exist, but there is no easy way to check this. I think that’s generally against deterministic ethos of DLT.

in this context, I do fully support the [@xiyu_meta](/u/xiyu_meta) initiative.

On the other hand, I agree with [@yyd106](/u/yyd106) that it seems to have common denominator on a protocol level. For example, rollups indeed are synchronising their `L[X]` state against `L[X-1]` as principal source of truth.

Perhaps this could be a Rollup Improvement Proposal: Multiple LX+1 could synchronise against LX. It does seem for me a neat features for rollups to build. This would raise such token rollup gas costs though .

---

**xiyu_meta** (2024-08-05):

I agree with your insights about the `cross-chain` model.

Besides, your concern about the gas costs makes sense. Because for the rollup layer of `ERC-6358`, more than one kind of gas is needed when submitting to multichains.

