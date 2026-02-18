---
source: ethresearch
topic_id: 17119
title: Can Ethscripts really replace L2? Can dumb contracts establish an ecosystem？
author: baiyibo
date: "2023-10-18"
category: Layer 2
tags: []
url: https://ethresear.ch/t/can-ethscripts-really-replace-l2-can-dumb-contracts-establish-an-ecosystem/17119
views: 2181
likes: 4
posts_count: 6
---

# Can Ethscripts really replace L2? Can dumb contracts establish an ecosystem？

Ethscriptions are an alternative to smart contracts—which are prohibitively expensive for most users—and to L2s, which today are centralized.

Ethscriptions is a protocol that allows users to share information and perform computations on Ethereum L1 at a drastically lower cost.

Ethscriptions achieves this by bypassing smart contract storage and execution and instead calculating state by applying deterministic protocol rules to “dumb” Ethereum calldata.

The goal of Ethscriptions is to give ordinary users the ability to perform decentralized computations for a reasonable price.

Today, Ethscriptions primarily function as cheaper NFTs. After the launch of the Ethscriptions Virtual Machine, they will function as a cheaper alternative to the Ethereum Virtual Machine.

###

What is Calldata?

Ethscriptions are cheaper because they store data on-chain using Ethereum transaction calldata, not smart contracts.

When you send someone eth via an Ethereum transaction, calldata is the “notes field.” Sometimes people write things in the notes field, but typically when you send eth to a person you leave it blank. When you interact with a smart contract, however, you add the information you’re passing to the smart contract—the function name and parameters—to the calldata field.

Ethscriptions are similar in that they encode data into calldata, but this information is not directed at smart contracts.

This video breaks it down:

  [![image](https://ethresear.ch/uploads/default/original/2X/4/449922dbc6f2d82511ded6671256dd0788923d20.jpeg)](https://www.youtube.com/watch?v=SjVrSihJOkU)

Using calldata like this enables ethscriptions to be 100% on-chain, permissionless, and censorship resistant, at a fraction of the cost of NFTs.

##

FAQ

###

**Are Ethscriptions secure and trustless?**

Absolutely! You can use the Ethscriptions protocol without relying on external parties. While it might be convenient to trust an indexer, like most Ethereum community members do with Etherscan, you can always rebuild and verify the indexer data manually.

###

**Are Ethscriptions decentralized?**

Yes, Ethscriptions reinterpret existing Ethereum data, which is decentralized by nature. No one’s permission is required to use Ethscriptions and no one can ban you from using it. By contrast, NFTs often rely on data stored in specific contracts that one person might control.

###

**Does relying on off-chain indexers as the source of truth make Ethscriptions centralized?**

Ethscriptions doesn’t rely on off-chain indexers as the source of truth any more than Ethereum relies on Etherscan as the source of truth. Both types of indexers are tools, and if they report data inconsistent with protocol rules they should be fixed. The key to decentralization is that these kinds of bugs can be discovered and verified by all protocol participants equally.

###

Who invented Ethscriptions?

The [first ethscription] was created in 2016, but the formal protocol was developed by Tom Lehman aka [Middlemarch]twitter. In addition to Bitcoin inscriptions, he was inspired by the famous “proto-Ethscription” from the Poly Network hacker that you can see [in this transaction]0x0ae3d3ce3630b5162484db5f3bdfacdfba33724ffb195ea92a6056beaa169490.

The author writes:

> ETHEREUM HAS THE POTENTIAL TO BE A SECURED AND ANONYMOUS COMMUNICATION CHANNEL, BUT ITS NOT FRIENDLY TO AVERAGE USERS. THE EXTRACTION OF MESSAGE REQUIRES SOME THEQUINIES, THE ENCRYPTION OF MESSAGE IS A MORE ADVANCED SKILL. I HAVE NO RESEARCH ON EXISTING PROJECTS. AND THE GAS FEE STOPS MOST USERS, THOUGH IT DOES NOT STOP REFUGEES. IS IT POSSIBLE TO ULTILIZE THE ETH NETWORK FOR FREE BY USING EXTREMELY LOW GAS? A SNAPCHAT ON CHAIN?

## Replies

**ControlCplusControlV** (2023-10-22):

You are essentially 2 comments away from re-discovering the entire idea of rollups. Bitcoin ordinals is a compromise and so is this, which is plainly stupid given the same constraints don’t exist on Ethereum as they do on Bitcoin, and they still have stupid properties there

---

**alexhook** (2023-12-05):

correct me if i’m wrong, ethscriptions are just transactions with necessary data in the transaction calldata, similar to bitcoin’s ordinals. basically, some data which can be used by some off-chain program (ordinals node) is stored inside the transaction.

ordinals make sense for bitcoin since it doesn’t have any smart contracts and it’s basically the only way to perform any actions on the blockchain besides transferring BTC back and forth, but it doesn’t make much sense in ethereum, because we have smart contracts and all necessary data can be stored in their storage, even without any off-chain computations/encodings/etc thanks to EVM

so it’s incorrect to compare ethscriptions with L2s since they are fundamentally different things and have different tasks

---

**signalxu** (2023-12-05):

I think this concept falls short in addressing high gas fees and scalability issues. Additionally, it might pose challenges in indexing data associated with the execution layer and lacks universality.

---

**atiselsts** (2023-12-22):

I’m by no means an expert, but I think Ethscriptions have some value as a new approach exploring the design space, specifically Ethscriptions + off-chain contracts, like in Facet.

Pros:

1. Avoids the centralized sequencer transaction ordering problem of L2
2. Intuitive to most users
3. Have smaller attack surface compared with L2 bridge contracts & mechanisms
4. Work really well together with DA solutions

Cons:

1. Unclear how to make off-chain contract execution cryptoeconomically sustainable in presence of hostile actors (an L2 sequencer can force the users to pay a tx fee for execution; no similar actor exists here)
2. Less compression possible than with rollups (no tx batching)

Other risks:

1. Reliance on off-chain indexers. Unclear if it’s worse than relying on RPC and Etherscan (“a user can run their own node” seems to be in the same ballpark as “a user can run their own indexer”).
2. How to fix the off-chain contract that the users want to run and the VM version they want to use? Hashes could be included as part of the tx calldata, but that makes each tx significantly more expensive.

If it’s permitted to link to Twitter here, I made a thread that aims to clarify the difference between L2, other scaling solutions, and Ethscriptions: https://x.com/atiselsts_eth/status/1736740200678822193

---

**jimmieaa** (2023-12-23):

With Ethscriptions technology, works can be protected from unauthorized modification and copying, and the authenticity and ownership of the work can be independently verified, whereas NFTs relying on a specific smart contract may be under the control of the contract’s creator, which may affect the security and independence of the work to some extent.

