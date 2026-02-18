---
source: magicians
topic_id: 4488
title: "ERC-2771: Secure Protocol for Native Meta Transactions"
author: lirazsiri
date: "2020-08-08"
category: EIPs
tags: [meta-transactions, erc-2771]
url: https://ethereum-magicians.org/t/erc-2771-secure-protocol-for-native-meta-transactions/4488
views: 6153
likes: 2
posts_count: 11
---

# ERC-2771: Secure Protocol for Native Meta Transactions

Discussion for https://eips.ethereum.org/EIPS/eip-2771

## Replies

**Jkor** (2021-12-29):

Interesting read, it’s a neat way of retrieving the original transaction initiator whilst minimizing gas costs for the end user.

---

**Philogy** (2022-03-10):

The proposal should be extended to support ERC20 payments to relayers as I believe this will be a common feature. Most applications will require relayers to be paid directly by users as subsidizing gas costs on mainnet will be unfeasible for most projects.

---

**dror** (2022-03-15):

This protocol explicitly defines the interface between the “Forwarder” contract and the “Recipient” contract.

It does not define the [meta] transaction format, how it arrives to the forwarder, or who pays for relaying it.

---

**SamWilsn** (2023-01-06):

> isTrustedForwarder function MAY be called on-chain, and as such gas restrictions MUST be put in place. A Gas limit of 50k SHOULD be sufficient to making the decision either inside the contract, or delegating it to another contract and doing some memory access calculations, like querying a mapping.

What is the requirement being made with the “MUST” here? That contracts calling `isTrustedForwarder` must set a gas limit?

Similarly, the “SHOULD” requirement is a bit weird as well. Perhaps both requirements could be better written as simply:

> isTrustedForwarder SHOULD NOT consume more than 50,000 gas.

---

**dror** (2023-01-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> isTrustedForwarder SHOULD NOT consume more than 50,000 gas.

Agreed. it is better wording for that.

---

**Pandapip1** (2023-01-09):

One argument against the new wording: the previous wording makes it clear that relayers **must** set a gas limit for safety reasons.

---

**SamWilsn** (2023-01-09):

Is it possible to make a call without a gas limit?

---

**Pandapip1** (2023-01-09):

Relayers should set a *reasonable* gas limit, and should be aware that they may lose funds if they use defaults provided by their library.

---

**agostbiro** (2023-01-22):

Hi,

Thanks for all the great work on this proposal! Meta transactions have already made a big positive impact on the ecosystem and they’ll only get more important.

I’m working on wallet security and **I’d like to propose that a message format containing transaction parameters becomes part of the standard.**

The reason for this is that transaction simulation is the only way to give the user accurate information about the consequences of approving a transaction.

With simple transactions, the user has to sign the actual transaction data that gets executed on-chain, so we can simulate the transaction in the wallet and tell the user what’ll happen if they approve.

With meta-transactions, off-chain signatures (which may or may not contain transaction parameters) can lead to on-chain transactions, so now it’s not possible for a wallet to guarantee to users that they’ve been informed about all on-chain state changes prior to approving them.

I think the solution could be to require in `EIP-2771` that the message that the user has to sign is an [EIP-712](https://eips.ethereum.org/EIPS/eip-712) typed structured data message that contains transaction parameters.

I’m not too familiar with `EIP-2771` implementations, but I noticed that OpenGSN already contains most of the needed parameters for transaction simulation (except for `chainId`):

[![opengsn-meta-transaction](https://ethereum-magicians.org/uploads/default/original/2X/a/a5931368c821efda855917ae417c3491c1beed76.png)opengsn-meta-transaction342×464 22.9 KB](https://ethereum-magicians.org/uploads/default/a5931368c821efda855917ae417c3491c1beed76)

So for the sake of backward compatibility, the standard could require that the `EIP-712` structured data’s message object has the following properties:

```auto
address from;
address to;
uint gas;
uint value;
bytes data;
uint nonce;
uint chainId;
```

Looking forward to hearing your thoughts!

Best,

Agost

P.S.: Just noticed that `EIP-2771` was moved to [final.](https://github.com/ethereum/EIPs/pull/6362) Not sure what’s the best way to handle my proposal now.

---

**dror** (2023-01-22):

ERC-2771 is only about the propagation of the original caller to the target contract. The target contract trusts the Forwarder to authenticate the caller (using a signature) and perform replay protection (using nonce or other mechanism)

The logic of the Forwarder is not defined by this ERC.

OpenGSN does use ERC2771 to access a target, and the [Forwarder](https://github.com/opengsn/gsn/blob/master/packages/contracts/src/forwarder/Forwarder.sol) uses EIP712, which also encode the chainId into the EIP712Domain, so it is not needed as part of the message data.

