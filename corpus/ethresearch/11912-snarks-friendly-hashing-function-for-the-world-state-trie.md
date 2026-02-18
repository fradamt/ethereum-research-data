---
source: ethresearch
topic_id: 11912
title: Snarks friendly hashing function for the World State Trie
author: leosayous21
date: "2022-02-01"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/snarks-friendly-hashing-function-for-the-world-state-trie/11912
views: 2102
likes: 1
posts_count: 2
---

# Snarks friendly hashing function for the World State Trie

Hello,

Leo here from [Sismo](https://blog.sismo.io/what-is-sismo-part-1-zk-badges-73e7031bacda), we are building private attestations on Ethereum.

I’m still fairly new to ZK but have been diving in these past weeks.

After seing this [old tweet](https://twitter.com/drakefjustin/status/1110648087352090625?lang=en) from Justin Drake  I realized I was not the only one hoping for a snark/stark friendly hash function (Pedersen, Poseidon, MiMc, …) for the World State Trie of Ethereum.

I’d be grateful if someone could point me to latest advancement on this topic!

Has someone ever thought about the strategy to modify a fullnode/archive node client so it maintains a second World State Trie, friendly to snarks and update its root regularly onchain?

We could very well imagine a set of nodes maintaining such a State Trie?

Would really appreciate any feedback about this idea or resources on alternatives to get access to the Ethereum state within ZK proofs, thanks!

## Replies

**MicahZoltu** (2022-02-09):

The hard part is coming to agreement on what the correct root is (the one written periodically on L1).  This would need to be a trustless process, which means some way to at least prove fraud, but ideally prove validity.

