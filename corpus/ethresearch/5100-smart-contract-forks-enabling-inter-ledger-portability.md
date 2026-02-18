---
source: ethresearch
topic_id: 5100
title: Smart Contract forks - enabling inter-ledger portability
author: informartin
date: "2019-03-06"
category: Applications
tags: []
url: https://ethresear.ch/t/smart-contract-forks-enabling-inter-ledger-portability/5100
views: 3421
likes: 6
posts_count: 10
---

# Smart Contract forks - enabling inter-ledger portability

**VeriSmart** is a tools that permits migrating Smart Contracts between EVM-compatible blockcains, maintaing it’s execution logic and state. No trust in the migrating entity is required, as the target contract’s validity is verifiable through merkle proofs.

The details of the chosen approach can be found in a research paper that is going to be published at ICBC2019: https://arxiv.org/abs/1902.03868

A prototypical implementation can be found here (a bit messy still, but works as a start): https://github.com/informartin/VeriSmart

---

**Motivation:** During a smart contract’ life cycle, external requirements may change or the host blockchain may become insecure due to e.g. lacking incentives, bugs etc. Changing application scenarios may also require shifting from a public chain to a permissioned one or vice versa.

**Contrext:**  the contract code needs to be executable on both platforms and support for as many platforms as possible is desirable to enable full flexibility in choosing the target chain. Recently, many blockchain implementations have adopted the EVM as a common execution environment (e.g. Hyperledger Sawtooth, Hyperleder Fabric, Hyperledger Burrow, Quorum, Qtum and Counterparty).

**Approach:** To enable smart contract portability between EVM-compatible blockchains without trust requirements in the executing enitity, I have come up with a mechanism that re-executes all past transactions to reconstruct the currect contract state. While doing so, a key/value map is built that represents the current state at the time of the transaction’s execution. After re-executing all past transactions chronologically, the final state is obtained and set in the target contract’s constructor. Using the resulting merkle tree, the state’s validity becomes verfiable (i.e. no alterations have been made to either contract code or state). Depending on the contract’s size, multiple approaches exist to achieve this. For instance, the contract state may be too large to be deployed in the constructor of the contract. In this case the contract is split into deployment-, logic-, and state-contract. The state contracts holds all variables, but delegates function calls to the logic contract. The deployment contract is authorized to set variables during the deployment phase and is destroyed thereafter to prevent unintendet alterations. Also, many smart contracts refer to other contracts or inherit from them, in these cases dependencies have to be deployed recursively while inserting the new addresses in the bytecode/state. All operations are conducted in bytecode so that the original high level code is not required.

I would appreciate any thoughts and feedback!

## Replies

**burrrata** (2019-03-08):

Sounds expensive. If you have to replay all the tx and dependencies in a contract’s history, do you also have to pay for it?

---

**informartin** (2019-03-08):

The beauty of it is that is not required to replay all tx on the target blockchain. They only have to be replayed locally to reconstruct the resulting state. As it is local, there is no cost attached to it.

The final state is then deployed for which you would have to pay gas fees, but the costs only depend on the amount of set variables in the final state and is independent of the amount of past transactions. This may, depending on the contract, still require quite some gas, but that really depends on the target ledger. In case it is a permissioned one, that could be negligible.

EDIT: A downside of this approach is that events are not available for the migrated contract. I’m still investigating how to tackle that issue.

---

**burrrata** (2019-03-08):

Ok cool! Thanks for clarifying that ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Do you think that this could be used to move contracts from the Ethereum L1 chain to plasma L2 chains with “[predicate contracts](https://medium.com/plasma-group/towards-a-general-purpose-plasma-f1cc4d49c1f4)”?

---

**jpitts** (2019-03-11):

Am I right to assume that both the origin and target EVM blockchain have to be running the same EVM release (with the same opcodes)?

IMO the EVM is not properly versioned right now; I aim to help champion an effort to make the EVM versioning more clear. Right now they track the larger protocol upgrades which may not always involve changes to the EVM.

For reference, here is my list of successful and aborted protocol upgrades: https://gist.github.com/jpitts/4c541a4efa2f8872ce9acf63da5c4921

---

**jpitts** (2019-03-11):

Perhaps being too imaginative here:

What kind of scenarios are there for verifiably moving a “smart contract and state” from blockchain A to blockchain B, in which blockchain B’s EVM has a different set of opcodes?

Could there be an intermediary step after blockchain A, e.g. a migration blockchain where the “smart contract and state” are modified in a verifiable way… and then the “smart contract and state” are finally moved to blockchain B?

---

**informartin** (2019-03-11):

Moving contracts between plasma chains is a cool idea!

tbh, I’m not that familiar with predicate contracts yet, but wil definitely have a look at it.

---

**informartin** (2019-03-11):

Different EVM versions could be an issue for sure if that includes new opcodes. Of course, changes in gas costs etc. wouldn’t affect the applicability though.

Assuming a contract migration towards a blockchain that only supports a subset of opcodes, I could imagine that those opcodes are substituted by library contract calls which emulate the original opcode, where possible. Then, that substitution would be applied to the bytecode that is deployed to the target chain. To verify the validity of the code, third party entities may apply the same logic instead of simply comparing source and target bytecode.

---

**alexeiZamyatin** (2019-03-11):

Interesting paper. However, it’s hard for me to see the exact use case of this.

If you migrate an ERC20 contract across system borders, the accounts associated with token ownership are likely not present on the other chain.

Exceptions here are probably sharding and hard forks.

If this is to be used for sharding, you would have to ensure that no changes are made to the contract state on the source chain - otherwise, clients could end up making decisions on the target chain relying on an expired (source) contract state. That is, you need to implement a mutex.

If you are shifting a contract from a permissionless* to a permissioned chain, you still end up trusting the validators of the permissioned chain for both liveness and safety. You might as well trust them to relay to you the latest contract state from the permissionless chain?

Even more so, if you’re going the other way round.

(Actually, that’s essentially what you are suggesting, no?)

You should also check out PeaceRelay (https://github.com/KyberNetwork/peace-relay) or cross-shard yanking ([Cross-shard contract yanking](https://ethresear.ch/t/cross-shard-contract-yanking/1450)).

On another note: if you are updating static references to other contracts (e.g. libraries), how do you *efficiently* prove that the contracts are equivalent? I mean, you could have manipulated the state of the library, but I would only find out if I manually verify this.

Perhaps you could add a hash of the bytecode of each referenced contract to the “main” contract before migration (or even upon first deployment n the source chain)? This would at least allow users to quickly check if any of the libraries have been modified.

- note: you can have public permissioned chains, hence public == permissionless

[EDIT: fixing typos]

---

**informartin** (2019-03-13):

Thanks for the feedback and hints!

From my point of view the main motivation to migrate a contract to another blockchain is the current disparity of incentives between miners and contract users. While miners are interested in high rewards, partially originating from gas fees, with as little (computational) input as possible, users would like to pay as little as possible and have interest in a high degree of decentralization, high throughput and low latency. As all of this is hard to achieve at the same time and priorities may change over time, contract users may decide to move to another ledger. Being able to do so prevents a new kind of lock-in effect towards a single blockchain instance.

In order to be independent of any central authorities, e.g. contract owners, any participant should be able to perform the migration. To take an analogy from the blockchain space, this would be a hard fork of the smart contract itself. And as for any hard fork, the participants decide on the application they are continuing to use. Therefore, it is kind of desired to be able to use both contracts in the aftermath of a migration. At least this is the case fore the described use case scenario.

As for the addresses, it is assumed that the address pattern described in the Yellow Paper, Appendix F is followed on both chains. As a result, tokens and so forth could be claimed as well by using the same key pair.

Applying the proposed migration process to sharding seems promising to me. As an extension to cross-shard yanking this could allow moving larger contracts between shards in comparison to the limitations when just extracting the state from a receipt.

When checking out PeaceRelay the last time my biggest concern was the verifiability of Ethash block headers. It is claimed that the verification mechanism that was proposed in [Smart Pool](http://smartpool.io/docs/smartpool.pdf) will be used in the future. However, since that claim quite some time has passed. Being able to integrate Merkle proofs from such a relay could be really beneficial though!

About the verifiability for referenced contracts: The current implementation takes care of it during the migration process by recursively migrating such dependencies. Here, a map of source and target contracts is created. As of now, the verification targets single contracts only though. Therefore, the next implementation step will be exporting the map of substituted addresses during the migration process and using it for verifying the correctness of all dependencies as well.

