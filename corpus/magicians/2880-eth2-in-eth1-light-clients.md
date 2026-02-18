---
source: magicians
topic_id: 2880
title: ETH2 in ETH1 light clients
author: vbuterin
date: "2019-03-08"
category: Magicians > Primordial Soup
tags: [eth1x, consensus-layer, precompile, light-client, eth1-eth2-merge]
url: https://ethereum-magicians.org/t/eth2-in-eth1-light-clients/2880
views: 4077
likes: 13
posts_count: 6
---

# ETH2 in ETH1 light clients

Here is a doc describing what implementing an eth2 light client would look like: https://notes.ethereum.org/s/B1DtMJZeV#

It is written in an abstracted form that depends on the phase 0 and phase 1 specs [here](https://github.com/ethereum/eth2.0-specs), but the gist is that it’s ~80 kilobytes of Merkle multi-proof verification (see [here](https://github.com/ethereum/research/blob/master/merkle_tree/merk.py) for an implementation of compact Merkle multi-proofs) every ~9 days plus verifying a BLS aggregate signature to verify a new block header. The size of the stored state is as written largely ~30 kilobytes of validator data, though this could be shrunk to just ~10 kilobytes (pubkey + balance for 256 validators).

The validator set update procedure gas cost seems low enough to process within one block:

- 80 kilobytes * 68 gas = 5.4m gas
- Saving 10 kilobytes = 2m gas (assuming you use the dirty trick of saving it as contract code, which is fine because the data doesn’t need to be modified)
- Hashes: ~3200 * 42 = 134400 (goes up to ~2.56 million if we use SHA256 instead of Keccak!)

It’s slightly over 8m, but that could be fixed by cutting the gas cost of tx data, which we want to do anyway. However, the block header verification procedure is complicated by the fact that it requires one pairing and 128 point additions in BLS-12-381, which eth1 currently does not support, and which is extra-inefficient in eth1 because it requires 384-bit numbers. This could be fixed by adding BLS-12-381 as a precompile in eth1, either as a standalone exception or as one of the first precompiles “implemented in WASM” as per the plan we discussed at the Stanford workshop (preferred).

But if we have that, then an eth2-in-eth1 client is actually not that hard, which opens the door to applications that use eth2 as an availability engine (ie. things like Plasma but waaay more powerful).

## Replies

**tvanepps** (2019-03-08):

> But if we have that, then an eth2-in-eth1 client is actually not that hard, which opens the door to applications that use eth2 as an availability engine (ie. things like Plasma but waaay more powerful).

Where can I read more about what “availability engines” are? Is it at all related to something Justin mentioned at the Magician’s chat on Monday?

> One research idea is a single unified Plasma chain to pay tx fees on any shard.

https://medium.com/ethereum-magicians/q-a-on-eth-2-0-ab1d5d3ac133

---

**vbuterin** (2019-03-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tvanepps/48/3406_2.png) tvanepps:

> Where can I read more about what “availability engines” are? Is it at all related to something Justin mentioned at the Magician’s chat on Monday?

Basically it’s a catch all term for a blockchain that is being used to store data and prove that data can be downloaded by anyone. This allows plasma-like constructions without the need for complicated exit games or 2-week waiting periods or anything like that.

---

**rossbulat** (2019-05-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Here is a doc describing what implementing an eth2 light client would look like: https://notes.ethereum.org/s/B1DtMJZeV#

This link brings me to a 404 Not Found. Interested in reading if it can be reuploaded.

---

**vbuterin** (2019-05-19):

It’s here now ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

https://github.com/ethereum/eth2.0-specs/blob/dev/specs/light_client/sync_protocol.md

---

**alonmuroch** (2020-11-04):

[@vbuterin](/u/vbuterin) could the light client be implemented in Solidity for example (considering BLS operations are available via precompiles)?

If so, a few questions:

1. Is security relies only on the selected committee? what happens if they accidentally or maliciously include an invalid block? Are there fraud-proofs that can be used to revert?
2. Validator set changes is a different operation than LightClientUpdate?

