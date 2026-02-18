---
source: magicians
topic_id: 6142
title: Add opcode to access storage trie root hash for account
author: rmeissner
date: "2021-05-03"
category: EIPs
tags: [opcodes, trie]
url: https://ethereum-magicians.org/t/add-opcode-to-access-storage-trie-root-hash-for-account/6142
views: 1319
likes: 0
posts_count: 3
---

# Add opcode to access storage trie root hash for account

I would like to propose to add an opcode that allows accessing the storage trie root hash for an account. This would allow to perform storage verification and gas optimizations.

### Verification

Currently it is impossible to verify that nothing has changed inside the storage tree of a specific account. There are some cases where this is very interesting to know. E.g. assuming you have a smart contract wallet and you want to ensure that nothing is changed in the storage tree during an execution of a internal transaction. Currently this would be quite expensive or impossible (as you would have to know all storage slots and compare them before and after). By comparing the storage tree root hash this could be simplified.

### Gas optimizations

A big chunk of gas costs are related to storage read. By adding read access to the storage trie root hash it is possible to write contracts in a “hybrid” stateless manner. E.g. provide the state to the user still via view functions, but for function that do on chain computations the state could be provided via the calldata and verified against the root hash. This could be done even for other accounts than the own, potentially allowing contracts to “access” state of other accounts.

### Considerations

- The gas costs should probably be similar to EXTCODEHASH
- If contracts perform verification on the root hash, they might break if a different hashing algorithm (instead of a merkle trie) is used.
- Should this be an opcode or rather a precompile.

Would love to hear some opinions on this opcode ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

## Replies

**vbuterin** (2021-05-03):

I get the impulse behind doing something like this, but it would unfortunately be a bad idea in practice imo, for forward-compatibility reasons. Namely, it would severely hamstring our ability to move from the current two-layer hexary patricia tree structure to a different and better tree structure (eg. *single-layer Verkle trees* like [this proposal](https://ethereum-magicians.org/t/proposed-verkle-tree-scheme-for-ethereum-state/5805)).

---

**rmeissner** (2021-05-04):

Yeah I talked with Artem from TurboGeth about it and I get the issues.

Maybe I should rephrase the question. It would be nice to have a way to check or prevent storage changes of a specific address. E.g. staticcall will prevent any state changes on any address. I would be nice to limit it to the storage (excl balance) of the current address. To be fair that is super specific to my use case so I tried thinking of a way that also brings value to others.

I am not sure what the best way would be, but I would assume that making guarantees about the whole storage of a contract (not just specific) could be very useful.

