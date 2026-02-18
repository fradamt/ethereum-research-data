---
source: ethresearch
topic_id: 429
title: Shard Chain Blocks vs Collators
author: ltfschoen
date: "2018-01-03"
category: Sharding
tags: []
url: https://ethresear.ch/t/shard-chain-blocks-vs-collators/429
views: 3361
likes: 2
posts_count: 3
---

# Shard Chain Blocks vs Collators

On the Main Chain we have Block, Block Header, Block Proposer (similar to a Miner in PoW chain).

But on a Shard Chain do we have:

1. Blocks AND Collations, i.e. Blocks (Level 2 Object), and Collations (Level 1 Object) (similar to Blocks), since earlier in the Introduction section of the Sharding Specification it says “… validator could theoretically at any time be assigned the right to create a block on any shard …”. OR
2. Collations ONLY (as shown in the Table at the end of the Introduction section of the  Sharding Specification

## Replies

**ltfschoen** (2018-01-04):

I’m thankful to have come across this excellent blogpost [“Ethereum Sharding: Overview and Finality” by Hsiao-Wei Wang](https://medium.com/@icebearhww/ethereum-sharding-and-finality-65248951f649), which helped to clarify things about the Sharding Specification.

I’ve now established that “Blocks” on a Main Chain are referred to as “Collations” on Shard Chains.

I also understand that Quadratic Sharding occurs when the Main Chain is broken into Periods that each comprise of say 5x Blocks each, and where each Block comprises the State Root of a Merkle Patricia Trie (MPT), which contains a Validator Manager Contract (VMC) that provides On-Chain Governance (Parliament) to allow Validators to Vote On-Chain. Users join with a Validation Code Address and are referred to as Validators (eligible to be chosen as a Collation Proposer) of Sharding Chains by Depositing their Stake in the VMC of the Main Chain. After their Validation Code Address is Recorded in the Global Validator Pool list they wait for their Validation Code Address to be Sampled by the VMC from the Validator Pool list, which converts them from being Validators into being referred to as a Collator (Collation Proposer) that Watches a specific Shard Chain for a specific Period. The Collator Validates recent Collations and sends a Transaction to the VMC on the Main Chain, which immediately records the Collation Header Hash on the Main Chain VMC as Proof that the Collation Header (of its associated Shard Chain State Root) is Valid (for the same Period that the Collator was Sampled to be a Collation Proposer).

Based on the above process, I think in the Introduction section of the Sharding Specification should be changed, where it says “… validator could theoretically at any time be assigned the right to create a block on any shard …”. I think it should instead state something like “… validator could theoretically at any time become a collator who is assigned the right to create a collation on a specific shard …”.

---

**vbuterin** (2018-01-04):

Yeah, there’s a bit of a suboptimal terminology choice with “validator” and “collator”, as technically *all* that validators do is create collations. I like the name validator more personally (no need for the name to map directly to the word collation; we already don’t call PoW mined blocks ore or anything like that), but I’m open to arguments on this.

