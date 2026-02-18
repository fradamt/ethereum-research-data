---
source: ethresearch
topic_id: 210
title: A two-layer account trie inside a single-layer trie
author: vbuterin
date: "2017-11-16"
category: Data Structure
tags: []
url: https://ethresear.ch/t/a-two-layer-account-trie-inside-a-single-layer-trie/210
views: 4048
likes: 17
posts_count: 5
---

# A two-layer account trie inside a single-layer trie

Currently, the ethereum state data structure is a two-layer trie. At the top there is the account tree, and each account is a 4-part data structure consisting of the nonce, balance, code and storage, where the storage is itself a key/value trie. This model has benefits, but it also has led to considerable implementation complexity. It turns out that we can get most of the benefits of the two-layer model by *embedding* it inside a single trie, with objects relating to the same account simply residing *beside* each other in the main tree, having the address of the account as a common prefix. That is, now we have:

```
main_tree[sha3(ADDRESS)] = acct = (nonce, balance, code, storage tree root)
storage_tree[sha3(KEY)] = VALUE
```

But we can instead have:

```
main_tree[sha3(ADDRESS) + \x00] = nonce
main_tree[sha3(ADDRESS) + \x01] = balance
main_tree[sha3(ADDRESS) + \x02] = code
main_tree[sha3(ADDRESS) + \x03 + sha3(KEY)] = VALUE
```

The main benefits of this would be a simple implementation.

## Replies

**yhirai** (2017-11-16):

Key-value stores might perform better on this layout (access patterns are more local; caching is easier).

---

**wanderer** (2017-11-16):

yes i think this a great idea! But also if you are considering making changes to the trie it might be worth considering moving to a [binary trie](https://github.com/dfinity/js-dfinity-radix-tree/blob/master/benchmark/results.md) also, since the light client proofs will be considerable smaller (at the cost of more lookups for full nodes)

---

**vbuterin** (2017-11-17):

We already are!

https://github.com/ethereum/research/blob/master/trie_research/new_bintrie.py

---

**AFDudley** (2017-12-26):

I strongly believe this is worth testing and seeing if it actually performs better. It should.

