---
source: ethresearch
topic_id: 6478
title: Yank to BeaconChain
author: decanus
date: "2019-11-21"
category: Sharded Execution
tags: [cross-shard]
url: https://ethresear.ch/t/yank-to-beaconchain/6478
views: 2725
likes: 6
posts_count: 5
---

# Yank to BeaconChain

Assuming there are contracts hosted on the BeaconChain, there should be some function to yank contracts from various shards and add them to the BeaconChain.

We define a bounded set `A` that contains contracts. `A` is bounded in order to restrict it to those contracts deemed as popular by various validators and to create some competition between contracts.

Assuming contract `C` is not in `A` and receives more transactions than any contract in `A`, a validator would create a proposal to add this contract to set `A`. Once the set has been filled the contract with the least transactions to it would be replaced by `C`.

The reason behind this is to move the most popular contracts into a highly available global state. This would reduce latency between cross-shard transactions with popular contracts.

Loredana wrote up a similar proposal using a master shard: https://medium.com/@loredana.cirstea/a-master-shard-to-account-for-ethereum-2-0-global-scope-c9b475415fa3, however this did not contain yanking logic.

## Replies

**DZack** (2019-11-21):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/d/b4bc9f/48.png) decanus:

> Once the set has been filled the contract with the least transactions to it would be replaced by C .

I imagine there will be a lot of competition for contracts to be on the beacon chain; the “most/least transactions” rubric could incentivize spam.

---

**adiasg** (2019-11-21):

Simply the number of transactions is not a good way for scoring contracts. Imagine a case where the contract `C` receives more transactions than the least scoring contract in `A`, but all those transactions are coming from the shard that `C` is on.

A good scoring heuristic for contracts should consider:

- Frequency & average gas costs of calls from each of the shards
- Storage cost of the contract

There are other open questions such as:

- Should contracts once hosted on the beacon chain persistent forever, so that none of it’s dependencies are broken?
- Should the protocol have a scoring heuristic to decide which contracts to place on the beacon chain, or should we be utilitarian and design it as an ongoing auction?
- If organizing the shard space so that popular contracts have equal access from all shards is the objective, then is hierarchical sharding a better solution than hosting contracts on the beacon chain?

---

**decanus** (2019-11-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/adiasg/48/1635_2.png) adiasg:

> Simply the number of transactions is not a good way for scoring contract

Totally agree, this was just about providing some function for scoring a contracts “importance” to be in the set of contracts on the beaconchain. Totally agree that there can be other methods.

---

**villanuevawill** (2019-11-21):

[On-beacon-chain saved contracts](https://ethresear.ch/t/on-beacon-chain-saved-contracts/6295), which quotes, “Contracts frequently needing to be yanked across shards, passing all contract code in through a receipt”

I believe something like you describe is definitely on the roadmap and needs to be investigated more. You bring up great points (should it be automated vs. deployed with a fee?)

