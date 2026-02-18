---
source: ethresearch
topic_id: 385
title: A cryptoeconomic accumulator for state-minimised contracts
author: JustinDrake
date: "2017-12-28"
category: Sharding
tags: [stateless, accumulators]
url: https://ethresear.ch/t/a-cryptoeconomic-accumulator-for-state-minimised-contracts/385
views: 6619
likes: 4
posts_count: 9
---

# A cryptoeconomic accumulator for state-minimised contracts

In [another post](https://ethresear.ch/t/history-state-and-asynchronous-accumulators-in-the-stateless-model/287/3) I looked into Merkle Mountain Ranges (MMRs) to offload history objects away from the state trie in the context of the stateless client paradigm. To summarise some of the really neat features MMRs have for maintaining witnesses of history objects:

1. Low frequency updates—witnesses are updated log(#{updates after insertion}), as opposed to once per insertion for tries
2. Extend-only updates—the witnesses (Merkle paths) only get extended, as opposed to having internal nodes be modified from unrelated object updates in the trie (this is great for parallelism)
3. Marginal memory overhead—witness maintenance requires only log(#{objects}) overhead, as opposed to #{objects} overhead for tries
4. Shorter average-case witnesses—size log(#{updates after insertion}), as opposed to size log(#{objects}) for tries
5. Shorter worst-case witnesses—size log(#{updates after insertion}), as opposed to size #{objects} for tries

Despite the witness-friendly properties of MMRs for history objects, Vitalik pointed out what seems to be their main limitation (emphasis mine):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)[History, state, and asynchronous accumulators in the stateless model](https://ethresear.ch/t/history-state-and-asynchronous-accumulators-in-the-stateless-model/287/2)

> The idea of having explicit data structures in the system to make low-witness-update-frequency  history objects easily usable is definitely an interesting one. That said, there are limits: in general, any application that allows you to reference objects from the history is very often also going to require some kind of stateful mechanism for efficiently proving whether or not those objects have already been consumed.

In the language of accumulators MMRs are not dynamic, hence the need for a dynamic accumulator (in our case, the Patricia-Merkle trie) to handle state in the general case. It then becomes natural to ask ourselves to what extent can contracts be state-minimised, so as to maximally limit the use of the trie and maximise the value of the MMR. There are two ways to minimise use of the trie:

1. Minimise amount of data stored in the trie
2. Minimise number of updates to the trie

One generic approach I suggested in the original post is to use SNARKs/STARKs to reduce the amount of data that needs to be put trie to just 32 bytes (the size of a hash). The problem with this approach is that we still have one trie update per transaction, so the number of trie updates is linear in the number of transactions. It turns out there is also a generic way to achieve a sublinear number of trie updates in this hybrid MMR-trie setup!

**A cryptoeconomic accumulator**

Below I describe a “cryptoeconomic accumulator” that is both witness-friendly and dynamic. We start with a witness-friendly MMR and, using a collateral scheme powered by the trie, bootstrap it into a dynamic accumulator.

Given an object `o` we model accumulator additions and deletions by wrapping an `add` or `del` bit of metadata to `o` (i.e. `[add, o]` and `[del, o]`). Such wrapped objects can then be appended to the MMR, with the rule that only users who have previously posted collateral can do so. The trie keeps track of who posted the collateral to enforce that rule.

A dynamic accumulator emerges if every `[del, o]` event is paired with a previous `[add, o]` event, and we never have two `[del, o]` events for the *same* `o`. (Two such repeated deletion events form a “violation”.) Violations can be prevented cryptoeconomically with the rule that if a user attempts to make a violation then any whistleblower can efficiently prove the violation within a period of time, thereby burning half the collateral and sending the other half to the whitleblower.

Notice additions and deletions to the cryptoeconomic accumulator take time to “confirm”, and there needs to be a scheme (e.g. checkpoints) to allow for rollback in case a violation attempt actually occurs. In exchange for a one-time collateral setup, a user can make an arbitrary number of deletions to the cryptoeconomic accumulator without touching the trie, thereby achieving the desired sublinearity.

**Conclusion**

It seems that MMRs just got even more awesome in the context of stateless clients. Their witness-friendly properties that are readily available for history objects can be extended to also handle state, modulo a sublinear number of trie updates.

## Replies

**vbuterin** (2017-12-28):

So the cryptoeconomic part of the MMR would basically be “here’s a signature, signed by a privkey with a deposit of 555555 ETH, saying that this accumulator does not contain [del o], and if you can disprove me then you can take the deposit”?

If so, clever and makes a lot of sense ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**JustinDrake** (2017-12-28):

Yes, you understood it exactly right ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**skilesare** (2018-02-21):

This seems really interesting but I’m having a hard time following.  Do you have any drawings or workflows of how an MMR works that you could provide?  Particularly how they would be relevant to something like the code I provide in: [Block Persistent Storage](https://ethresear.ch/t/block-persistent-storage/817/7)

---

**JustinDrake** (2018-02-21):

Since this post was made I discovered [double-batched Merkle accumulators](https://ethresear.ch/t/double-batched-merkle-log-accumulator/571) which are better than MMRs, and are much easier to understand. The scheme above works the same if you replace the accumulator.

If you’re still interested in MMRs (a.k.a. asynchronous accumulators) you can find a visual depiction of the algorithm in pages 18 and 19 [in this paper](https://eprint.iacr.org/2015/718.pdf). An MMR is basically like a binary counter where each bit is replaced with a Merkle tree root, and the carry operation merges Merkle tree roots.

---

**skilesare** (2018-02-21):

Well…now I’m interested in a visual representation of the DBMAs that are more efficient. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) I’ll jump over there and start parsing through things.

---

**JustinDrake** (2018-02-21):

It really is super simple. There’s a fixed-size bottom buffer, and an uncapped top buffer, both storing Merkle roots. Phase 1 batching Merklelises logs and saves the root to the bottom buffer. When the bottom buffer is full it is Merklelised and the root is saved to the top buffer. Below is incomplete and untested Go code.

```auto
package accumulator

type Hash [32]byte
type Log []byte

const bottomBufferSize = 1 << 10

// The bottomBuffer and topBuffer combined make up the accumulator
var bottomBuffer []Hash
var bottomBufferIndex uint
var topBuffer []Hash

func AccumulateLogs(logs []Log) {
	// Phase 1 batching: Merklelise logs and save root in bottom buffer
	var hashes []Hash
	for i := 0; i < len(logs); i += 1 {
		hashes = append(hashes, hashLog(logs[i]))
	}
	bottomBuffer[bottomBufferIndex] = getMerkleRoot(hashes)

	// Phase 2 batching: When the bottom buffer is full, Merklelise it and save root in top buffer
	bottomBufferIndex += 1
	if bottomBufferIndex % bottomBufferSize == 0 {
		bottomBufferIndex = 0
		topBuffer = append(topBuffer, getMerkleRoot(bottomBuffer))
	}
}

func hashLog(log Log) Hash{
	var hash Hash
	// TODO: Implement a hash function (e.g. SHA256, or Keccak)
	return hash
}

func getMerkleRoot(hashes []Hash) Hash{
	var root Hash
	// TODO: Merklelise hashes and return Merkle root
	return root
}
```

---

**skilesare** (2018-02-21):

Thanks for the pseudo code!

A few questions and comments:

Why not use a Patricia Tree?  At least with a PT you can prove that something doesn’t exist.  This seems like it might have value for in doing the log pairing of adds and dels.  With a patricia tree I can provide you with both a proof that my log is in the root and a proof that its invalidation ISN’T in the tree…no need for a crypto deposit.  But then you lose the easy updates?

I’m mixing two things up here that probably shouldn’t be mixed up.  On one hand, I’ve been trying to build stateless contracts that hold state off chain and just tracks a root, and on the other hand were discussing protocol layer stuff here.

This is all very interesting to me.  From a protocol layer, I’m seeing that the two-layer approach gets you some compression so that your proofs don’t get too long.  Is that the big win here?

---

**HarryR** (2018-08-28):

[@skilesare](/u/skilesare) I’ve been working on a state minimised merkle tree, and found that while it’s not possible to only store the root of the tree you can store at most one unbalanced node at each level and emit events for all appended items and calculated balanced nodes.

See further info @ https://github.com/HarryR/ethsnarks/issues/16

Python implementation: https://github.com/HarryR/ethsnarks/blob/immr/appendix/immr.py

Extracted code for the `append` function:

```python
	def append(self, item):
		lvl = 0
		while True:
			lvl_count_key = 'lvl.' + str(lvl)
			lvl_count = self._stor.get(lvl_count_key)

			self.emit(lvl, lvl_count, item)

			if lvl_count % 2 == 1:
				prev_val_key = "%d.%d" % (lvl, lvl_count - 1)
				prev_val = self._stor[prev_val_key]
				item = HashFunction(prev_val, item)
				del self._stor[prev_val_key]
			else:
				val_key = "%d.%d" % (lvl, lvl_count)
				self._stor[val_key] = item

			lvl_count += 1
			self._stor[lvl_count_key] = lvl_count
			if lvl_count % 2 != 0:
				break
			lvl += 1
```

For example, after 1000 inserts the database only stores the following items:

```auto
level 0000: 1000
level 0001: 500
level 0002: 250
level 0003: 125
level 0004: 62
level 0005: 31
level 0006: 15
level 0007: 7
level 0008: 3
level 0009: 1

level 0003 item 0124: 17091390504405981657579101865512078031112117797633598751647321595954421208885
level 0005 item 0030: 11432221231255018214084460762913861530967799609110822039801369274264043459453
level 0006 item 0014: 21709797073617348950618721483223221701276312367409941640768052740088622778821
level 0007 item 0006: 11426590355662709180378281331416813339771702869015491326709053175928753139730
level 0008 item 0002: 14255486654154165991711447228273623210898737301412569004468677634153235753660
level 0009 item 0000: 13048253346413405701399443551142082279890037746369451596589013900728189841360
```

e.g. `2*ceil(log2(n)) + 1` storage values needed at any time to store the state, clients must retrieve the nodes they need from the the event logs to construct a path to one of the unbalanced roots.

On each append a new merkle tree must be created from every unbalanced root and stored as the MMR root for that block (e.g. if multiple appends happen within the same block, only one MMR root will be stored), the clients then prove that the unbalanced node they exist under is in the MMR root for a specific block.

