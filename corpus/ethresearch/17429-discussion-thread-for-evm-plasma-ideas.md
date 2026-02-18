---
source: ethresearch
topic_id: 17429
title: Discussion thread for EVM plasma ideas
author: vbuterin
date: "2023-11-15"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/discussion-thread-for-evm-plasma-ideas/17429
views: 4185
likes: 13
posts_count: 6
---

# Discussion thread for EVM plasma ideas

See:

- https://vitalik.ca/general/2023/11/14/neoplasma.html
- **Plasma Free**
- Minimal fully generalized S*ARK-based plasma

## Replies

**Perseverance** (2023-11-15):

Neat!

I guess the UTXO graph can be built and constrained observing ‘CALL’ and its value. Some considerations:

1. Spending the output of a smart contract would need to skip signature validation on the unspent output.
2. The system should have well defined rules for Choosing which unspent output(s) to use as input (an interesting design space can be explored in order to optimize for the least constraints)
3. Should an output spending from a smart contract be a subject of any additional validation apart from value check?

An difficult challenge is how to enable balance outputs merges, if the snark is a mere prover that the transfers and the utxo graph match. That would be needed to prevent some possible “dust attacks”.

Lastly, in practice Id love to see a poc to show if the cost for generating and proving the equivalence does not outweigh the benefits compared to the current rollups exit strategy.

---

**Daniel-K-Ivanov** (2023-11-16):

What would be the implication of Account Abstraction / Smart Wallets in the case of f.e Validiums using the zk UTXO concept?

Smart contract wallets cannot produce signatures that authorise unspent output in a given transfer.

---

**Mirror** (2023-11-16):

![:innocent:](https://ethresear.ch/images/emoji/facebook_messenger/innocent.png?v=12)We can see that this is really a short post. For those who lack background knowledge and are not interested in further reading and like to follow stars, you can read here:

1. Plasma’s Approach to Data Availability and Transaction Costs: Plasma, a class of blockchain scaling solutions, significantly addresses the data availability issue and reduces transaction costs by keeping most data and computation off-chain. Specifically, only deposits, withdrawals, and Merkle roots are maintained on-chain. This design substantially enhances scalability by not being bottlenecked by on-chain data availability constraints. Plasma’s approach, especially when combined with validity proofs like ZK-SNARKs, efficiently resolves the challenge of client-side data storage for payments, a major impediment in its earlier versions. This advancement not only addresses storage issues but also enables the creation of a Plasma-like chain capable of running an Ethereum Virtual Machine (EVM). These improvements allow for a significant reduction in transaction fees, as the data that needs to be processed and stored on-chain is minimized​​.
2. Security Upgrades and Challenges with Plasma: Plasma introduces notable security enhancements, particularly for chains that would otherwise rely on validiums. However, it faces challenges when extending its functionality beyond simple payment transactions, especially when integrated with the EVM. In the context of the EVM, many state objects lack a clear “owner,” a prerequisite for Plasma’s security, which relies on owners to monitor data availability and initiate exits if needed. Moreover, the EVM’s unrestricted dependencies mean that proving the validity of any state requires a comprehensive understanding of the entire chain, which complicates incentive alignment and creates data availability problems. Despite these challenges, Plasma’s combination with validity proofs like ZK-SNARKs offers a potential solution. These proofs can verify the validity of each Plasma block on-chain, simplifying the design and focusing concerns mainly on unavailable blocks rather than invalid ones. This method could allow for instant withdrawals under normal operating conditions, enhancing both security and efficiency​​.
3. Simplifying Developer Experience and Protecting User Funds with Plasma: Plasma simplifies the developer experience by abstracting complex ownership graphs and incentive flows within applications. Developers don’t need to intricately understand these underlying mechanisms, making it easier to build on Plasma. For user fund protection, Plasma employs various techniques like treating each coin as a separate NFT and tracking its history, or using a UTXO (Unspent Transaction Output) model for fungible tokens like ETH. These methods ensure that users can safely exit with their assets by providing relevant transaction proofs, thus safeguarding their funds. Plasma’s design, especially when combined with ZK-EVMs, is reinvigorating interest in its potential to provide more effective solutions for blockchain scaling, data availability, transaction cost reduction, and security enhancements​​.

Also according to this post:[Exit games for EVM validiums: the return of Plasma](https://vitalik.ca/general/2023/11/14/neoplasma.html) .The integration of Plasma with ZK-SNARK (Zero-Knowledge Succinct Non-Interactive Argument of Knowledge) can enhance blockchain performance and security in several key aspects. Here is a detailed analysis and application scenarios:

**Enhancing Blockchain Validity Verification:** Plasma’s design primarily involves keeping most data and computation off-chain to improve scalability. However, this design necessitates a mechanism to ensure the validity of the limited data published on-chain, such as Merkle roots. The introduction of ZK-SNARKs becomes crucial here. By employing ZK-SNARKs, the validity of each Plasma block can be proven on-chain. This significantly simplifies the design space, as the operator’s only concern is data unavailability, not invalid blocks. This verification approach reduces the amount of state data users need to download, changing from one branch per block over the last week to just one branch per asset.

**Instant Withdrawals and Simplified Challenge Process:** In normal circumstances, if the operator is honest, all withdrawals would come from the latest state. In a Plasma chain verified by ZK-SNARK, such withdrawals are not subject to challenges from the latest owner, making these withdrawals challenge-free. This means that withdrawals can be instantaneous under normal conditions, a significant security and convenience upgrade for users as it eliminates waiting times and potential challenge risks.

**Parallel UTXO Graphs for EVM:** In the case of the Ethereum Virtual Machine (EVM), ZK-SNARKs allow the implementation of a parallel UTXO (Unspent Transaction Output) graph for ETH and ERC20 tokens, and SNARK-prove the equivalence between the UTXO graph and the EVM state. This method allows us to bypass many complexities of the EVM. For instance, in an account-based system, someone can edit your account without your consent (by sending tokens, thus increasing its balance), but in the Plasma construction, this is irrelevant because the construction is over a UTXO state parallel to the EVM, where any received tokens would be separate entities.

**Total State Exiting:** Simpler schemes have also been proposed for creating a “Plasma EVM.” In these schemes, anyone can send a message on L1, compelling the operator to include a specific transaction or make a particular state branch available. If the operator fails to do so, the chain begins to revert blocks until someone posts a complete copy of the entire state or at least all the data users have marked as potentially missing. While these schemes are powerful, they cannot provide instant withdrawals under normal conditions, as there is always the possibility of having to revert the latest state.

In summary, the integration of Plasma with ZK-SNARKs not only solves the problems of data availability and scalability faced by large-scale blockchain systems, but also reduces transaction costs and complexity by decreasing the amount of data users need to download and verify, while simultaneously enhancing security and efficiency.

![:kissing_cat:](https://ethresear.ch/images/emoji/facebook_messenger/kissing_cat.png?v=12) ![:kissing_cat:](https://ethresear.ch/images/emoji/facebook_messenger/kissing_cat.png?v=12) ![:kissing_cat:](https://ethresear.ch/images/emoji/facebook_messenger/kissing_cat.png?v=12)Congratulations on reading the full article. If you want to know more about plasma technology, I recommend:




###






      [plasma.io](https://www.plasma.io/plasma-deprecated.pdf)



    https://www.plasma.io/plasma-deprecated.pdf

###



704.70 KB

---

**Daniel-K-Ivanov** (2023-11-20):

TLDR: The idea of this post is to iterate over [Vitalik’s proposal](https://vitalik.ca/general/2023/11/14/neoplasma.html) for the usage of a UTXO-based exit mechanism for validiums, instead of account-based.

## Overview

Validiums tradeoff security for scalability. By default, we think about them as using “Account-based” models for representing the state.

They impose permissioned exits due to their “account-based” state model, withdrawal exit tree and data availability design decisions.

> Account-based models require parties to have the latest state for them to prove anything about the state. It is unfeasible for users to keep the necessary data themselves, therefore exits are permissioned in validiums.

Anyone who wants to exit the validium must receive information that is held by a limited set of parties the operator(s) and data availability committee (DAC) members of the validium. In this write-up, we will consider only the operator as the one persisting the state, but in reality, in any “malicious operator” scenario both the operator(s) and the data availability committee are considered malicious. If the DAC is honest, the users will be able to reconstruct the state and exit normally.

In case of a malicious operator, the user will not be able to exit the L2 since they won’t be supplied with the necessary data for performing Merkle inclusion proof onchain. In other words, users are at the mercy of the operator when it comes to exits.

Permissioned exits are an overall downgrade of the security of the system, forcing the user to have greater trust assumptions in the validiums.

An alternative approach to the withdrawal exit tree widely used in validiums, is the usage of the UTXO model as an exit mechanism.

> UTXO graph-based exit models allow the system to additionally employ an “exit game” for withdrawals when exiting against any state prior to the latest state. It is feasible for users to keep the necessary data themselves, therefore exits become permissionless even in validiums.

A desirable property of UTXO graph-based exit models is that the same artefact - an unspent output - is sufficient to exit even if an unrelated state change occurs. When a user receives tokens they have the knowledge of the related unspent output. This information is enough for an honest user to trigger the exit game and successfully exit even if they are subject to censorship by a malicious operator.

Under a UTXO exit model, it is feasible for users to store the data required for performing exits “locally” in their wallets. This removes the need for operators to provide further artefacts for exits, making the exits permissionless.

## High-level Design

1. Operator Constructing a UTXO representation of currency and token balances

Upgrade validiums so that their operator produces a UTXO graph of the balances which is equivalent to the Account-based model. Both the Account-based model and UTXO model are constructed and persisted by the operator.

In the case of EVMs and other general-purpose VMs, the Account-based model represents the full generic state (f.e storage slots) whereas the UTXO graph model represents only the **token balances state** (f.e currency and ERC20 balances). (Aside: the Aztec team has decided to represent a generic state via UTXO graph, so this could be a further exploration space)

- UTXO model is constructed for the withdrawable currencies in the validium
- The UTXO model is represented via Merkle Trie whose leaves are the UTXO outputs. The Merkle Trie must be a Sparse Merkle Trie or an Indexed Merkle Trie to support proof of non-inclusion.
- The root of the UTXO Merkle Trie is posted onchain by the operator of the validium along with the account-based root

1. Operators generate a SNARK (ZKP) of the UTXO state

The validity proof of the validium is extended to constrain and prove that the UTXO Merkle Trie is updated correctly given an initial state of token balances and the transactions in this sequence.

1. Updated Exit Games

The wallet of the user stores the token transfer history of the account, meaning that it can construct the unspent outputs of the user.

When an honest user wants to exit the validium, they execute an L1 transaction providing the unspent output they want to exit. If the user wants to exit against the latest state and the operator provides the necessary data, the user can also provide an MIP and exit instantly. No withdrawal period is necessary since the unspent output can be proven against the latest published UTXO State Trie. **In normal cases, withdrawals are instant.**

### Malicious Exits

> It is important to note that in case of submitting exits against the latest published UTXO state trie withdrawals are instant and no challenges are necessary. These should be by far the most common use case. The next scenario deals with a malicious party in the process.

Only on rare occasions, the users might want to exit against a “historical” state. An example of this might be a user getting censored by both the validium operator and the DAC. In this case, a challenge period is necessary to account for the following cases.

**Not latest owner**

If the user tries to exit an output that is already spent in a later state. The user can get challenged by submitting an unspent output that has the same input as the malicious exit. This means that the maliciously claimed exit has already been spent.

**Double Spend**

If the user tries to exit a UTXO whose input was already spent by the previous owner.

Challenged and stopped by submitting

1. A UTXO that has the same input as the maliciously exited UTXO
2. Merkle Inclusion Branch that the transfer is in the UTXO Merkle Trie and was included prior to the maliciously exited UTXO.

This means that the maliciously claimed exit which **should be** unspent output is spent (used as an input).

**Invalid History**

If a user tries to exit a UTXO whose input does not exist.

The Merkle Trie used for the UTXO models **supports non-inclusion proofs** (SMT / Indexed Merkle Trie). Invalid history is challenged and proven by submitting a merkle proof for non-inclusion against the UTXO Merkle Trie root.

## Trade-offs

[![image](https://ethresear.ch/uploads/default/optimized/2X/d/d834021582053c829a0b006e0a83ba0123f412de_2_690x465.png)image691×466 17.6 KB](https://ethresear.ch/uploads/default/d834021582053c829a0b006e0a83ba0123f412de)

The value of using UTXO models is the security upgrade for having permissionless exits in Validiums. The downsides of that are described below

### Higher Costs

The operating costs of the validium are increased by two components

- ZKP generation for the root of the UTXO Merkle Tries
- Although minimal, there would be an increase in the L1 gas costs due to calldata and storage of UTXO Merkle Trie root(s).

### Prolonged Exits in Extreme Situations

UTXO models provide instant exits in normal operating modes where the operator is not malicious. In the case of a malicious operator, users exit against outdated root which imposes a challenge period. The downside can be perceived as not significant since it is employed only at times of rogue validium.

---

**std** (2024-05-27):

Hi Vitalik,

I just read your note, and it reminded me of a paper that I wrote some time ago: [Lower Bounds for Off-Chain Protocols: Exploring the Limits of Plasma](https://eprint.iacr.org/2020/175), together with Grzegorz Fabiański, Sebastian Faust, and Siavash Riahi. This paper shows that one cannot have Fungible Plasma without mass exits caused by data unavailability. More precisely, one cannot simultaneously achieve the benefits of Plasma Cash (no mass exists) and Fungible Plasma (short exit size). This holds even if we use the validity proofs (SNARKs) in the Plasma construction. We show it by presenting a generic attack, which I informally sketch below. It is based on the “rollback idea”: a corrupt user can always use the benefits of the data unavailability and then “roll back” to its previous state, pretending it was also under the data unavailability attack.

Wouldn’t this attack apply to the idea that you described in your note? Or am I confusing something?

#### The roll-back attack

Assume that we have a Plasma in which the honest parties do not need to react quickly on the mainchain after the operator launches a data unavailability attack (i.e., there are no “mass exists”).

Suppose we have n users in this Plasma. Denote them as U1,…, Un. Assume that at a particular time T0, each Ui (for i ≥ 2) holds 1 ETH. Moreover, assume that U1 and some subset C ⊆ {U2,…Un} of the parties is corrupt.

For example, for n = 6 and S = {U3,U5,U6}, the situation looks like this:

[![](https://ethresear.ch/uploads/default/optimized/3X/6/7/6737fa2ca5d57af20181a87709073bb4d4f5c327_2_433x162.png)1600×599 81.4 KB](https://ethresear.ch/uploads/default/6737fa2ca5d57af20181a87709073bb4d4f5c327)

Now, in time T1 > T0, the operator launches a data unavailability attack (i.e., it only publishes the hash of its data but not the data itself) against all the honest users. Each user Ui ∊ C now sends its coin to U1. Pictorially:

[![](https://ethresear.ch/uploads/default/optimized/3X/6/4/6429fac9d496a4833c5fe5819912132ca8b9b84f_2_448x277.png)1600×988 129 KB](https://ethresear.ch/uploads/default/6429fac9d496a4833c5fe5819912132ca8b9b84f)

The corrupt operator publishes the hash of the new Plasma state on the mainchain. We assume that the corrupt operator collaborates with all the corrupt users, and hence the new state will be correctly hashed. Due to the data unavailability, the honest parties do not know the new state (they only know its hash). Since we assumed that in our Plasma they do not need to immidatelly act on the mainchain, they just wait.

Now, user U1 exits with all the coins it received in time T1. Let U denote the string posted on the mainchain to describe this operation. Pictorially:

[![](https://ethresear.ch/uploads/default/optimized/3X/3/b/3ba4c8ad8bc1d5576fcce756cf28be6a2cc42198_2_551x266.png)1600×773 87.5 KB](https://ethresear.ch/uploads/default/3ba4c8ad8bc1d5576fcce756cf28be6a2cc42198)

Note that so far, the corrupt user behaved “honestly”, so if the smart contract (on the mainchain) asks U1 to prove (say, using a SNARK) that U1 owns these coins, then U1 can provide such proof.

Now, the corrupt parties “**rollback**” to time T0, i.e., they restore their previous states, pretending that from time T1, they are also under the data availability attack and the last state that they know is from time T0:

[![](https://ethresear.ch/uploads/default/optimized/3X/8/a/8ac973c6b8fbe08edada9f2c06a19513d79f1443_2_408x228.png)1600×895 144 KB](https://ethresear.ch/uploads/default/8ac973c6b8fbe08edada9f2c06a19513d79f1443)

We now consider two options:

1. String U contains enough information for the smart contract to compute C – this is essentially “Plasma Cash” as it requires long exit sizes. This is because in general it takes around n bits to describe a subset C of {2,…,n}.
2. String U does not contain enough information to compute C – then U can be short, but the smart contract does not have enough information to distinguish the “good guys” from the “bad guys”. In particular, suppose all the users decide to exit from state published at time T0 (the last state that was publicly available). Then, there is no way for the smart contract to prevent some of the corrupt users from withdrawing their coins once again. This means that the contract can be drained and the honest users’ money stolen. It is important to note that SNARKs cannot help here, as there is no way to prove in SNARK that someone was indeed under the data unavailability attack.
1600×828 133 KB

In other words: if we want to have short exits, then we need allow the users to withdraw their money from the last state that is known to them, and all the withdrawals from the subsequent states need to wait until we are sure that all these withdrawals were performed.

This is, of course, only a sketch. For the full proof see [Lower Bounds for Off-Chain Protocols: Exploring the Limits of Plasma](https://eprint.iacr.org/2020/175), where we also show that this attack is non-uniquely attributable (and hence it’s not even clear who should pay for this rapid money withdrawal).

What do you think?

Best,

Stefan

PS I don’t think the UTXO vs account-based distinction makes much difference here.

