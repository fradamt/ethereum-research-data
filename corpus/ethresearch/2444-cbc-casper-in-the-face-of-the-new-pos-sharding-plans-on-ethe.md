---
source: ethresearch
topic_id: 2444
title: CBC-Casper in the face of the new PoS+Sharding plans on Ethereum
author: Mikerah
date: "2018-07-05"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/cbc-casper-in-the-face-of-the-new-pos-sharding-plans-on-ethereum/2444
views: 4387
likes: 8
posts_count: 11
---

# CBC-Casper in the face of the new PoS+Sharding plans on Ethereum

CBC-Casper aka Vlad’s Casper is the separate research being done on transitioning Ethereum to a Proof-of-Stake blockchain. Since the announcement several weeks ago about combining FFG Casper and Sharding research efforts in order to transition Ethereum to a PoS blockchain, there has been no mention of CBC-Casper.

Is CBC-Casper still an ongoing research project for the Ethereum Foundation?

If so, how will it be integrated, if at all, into the new direction of the Ethereum ecosystem?

## Replies

**vbuterin** (2018-07-05):

CBC is still ongoing, and the design is being made with CBC future-compatibility in mind.

---

**jamesray1** (2018-08-21):

https://twitter.com/VitalikButerin/status/1029905990085357568

I just want to comment on this here, as maybe you didn’t see my reply on Twitter. What you mean here is Casper FFG on an independent chain, and not full PoS Casper CBC. As I have mentioned before, I would prefer to go straight to implementing CBC Casper. It might be more complicated to implement in the short-term, but in the long-run, there would be less work involved with going straight to CBC Casper, rather than FFG with PoW then later CBC with full PoS, and will result in scalability coupled with energy efficiency, rather than scalability with PoW, which consumes a lot of energy, e.g. with predictions for the energy consumption of Bitcoin being as much as Denmark by 2020. While PoW Nakamoto cryptocurrencies *may* be less energy-intensive than fiat money, with that prediction in mind, I am skeptical of that, and we really need to prioritize sustainability in all our actions.

---

**vbuterin** (2018-08-21):

> What you mean here is Casper FFG on an independent chain,

What I mean is full PoS Casper FFG.

---

**jamesray1** (2018-08-22):

I would prefer to develop a spec using Casper CBC rather than implement a spec using Casper FFG.

---

**vbuterin** (2018-08-22):

Can I ask what you like about Casper CBC? Certainly interested in CBC longer-term but as far as I can tell the exact specs aren’t ready yet, and it would represent a considerable efficiency decrease in ways that in principle absolutely could be mitigated but in practice still requires some more research.

---

**jamesray1** (2018-08-22):

Right, first of all, while I’ve read papers for FFG and CBC, but it’s been a while now, and I may not fully understand both protocols and all of their pros and cons, so perhaps after I finish gossipsub I’ll scrutinize them again. I like that it’s correct-by-construction, i.e. using maths to formally prove safety; that you can explore the full tradeoff triangle (which may make further R&D to see if you can have different applications using variants of the protocol designed for a different point of the triangle interesting), extending on relative local views of safety from each node to consensus safety, etc. But perhaps I shouldn’t be so adamant about which one to focus on implementing in the short-term, and may need to look more into it to get a better idea.

But generally, like I’ve said, it seems that it would be less work in the long-run to go straight to implementing CBC.

---

**vbuterin** (2018-08-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> using maths to formally prove safety

FFG has this too, see [here](https://ethresear.ch/t/epoch-less-casper-ffg-liveness-safety-argument/2702). It looks less formal, but keep in mind that the portion of CBC’s proofs that are more formal are the generic ones that assume pre-existing safety oracles; proofs for any specific oracles are still quite rough.

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> that you can explore the full tradeoff triangle (which may make further R&D to see if you can have different applications using variants of the protocol designed for a different point of the triangle interesting)

FFG has this too, with variable epoch lengths.

> But generally, like I’ve said, it seems that it would be less work in the long-run to go straight to implementing CBC.

I’m inclined to disagree; much of the machinery in FFG is quite transferable to a CBC setting. Consider:

- Signature aggregation (CBC will require more advanced aggregation eg. going straight to STARKs, but the same network pathways would be in use, similar DoS considerations would need to be analyzed, etc)
- The beacon chain: fully transferable
- Random beacon: fully transferable
- Validator shuffling: fully transferable
- Dynasty switching: “full” CBC does have a different scheme for validator induction; this would require more work

---

**jamesray1** (2018-08-22):

OK, thanks for the counterarguments! Will finish reading [Epoch-less Casper FFG liveness/safety argument](https://ethresear.ch/t/epoch-less-casper-ffg-liveness-safety-argument/2702/1) later.

---

**Honglei-Cong** (2018-08-28):

one question about ‘full pos’:

From my understanding, casper is for finalization, pow is for block proposing.

For ‘full pos’, random beacon will do the block proposing?

---

**jamesray1** (2018-08-28):

No, Casper FFG is a finality gadget that can work with any block proposal mechanism. Casper CBC is a full PoS proposal. Read the FAQs and papers for more details. [Casper Proof of Stake compendium · ethereum/wiki Wiki · GitHub](https://github.com/ethereum/wiki/wiki/Casper-Proof-of-Stake-compendium). Block proposers will do the block proposing, and they will collate transactions into blocks.

Some snippets from the spec, although you should read the whole thing before asking questions like this:

> Block production is significantly different because of the proof of stake mechanism. A client simply checks what it thinks is the canonical chain when it should create a block, and looks up what its slot number is; when the slot arrives, it either proposes or attests to a block as required.

Read the “Per-block processing” section; note my emphasis in bold in the last sentence. Also note that the best way to understand specifications (and maybe improve on them) is by implementing them yourself.

> ### Per-block processing
>
>
>
> First, set recent_block_hashes to the output of the following:
>
>
>
> ```python
> def get_new_recent_block_hashes(old_block_hashes, parent_slot,
>                                 current_slot, parent_hash):
>     d = current_slot - parent_slot
>     return old_block_hashes[d:] + [parent_hash] * min(d, len(old_block_hashes))
> ```
>
>
>
> The output of get_block_hash should not change, except that it will no longer throw for current_slot - 1, and will now throw for current_slot - CYCLE_LENGTH * 2 - 1
>
>
> A block can have 0 or more AttestationRecord objects, where each AttestationRecord object has the following fields:
>
>
>
> ```python
> fields = {
>     # Slot number
>     'slot': 'int64',
>     # Shard ID
>     'shard_id': 'int16',
>     # List of block hashes that this signature is signing over that
>     # are NOT part of the current chain, in order of oldest to newest
>     'oblique_parent_hashes': ['hash32'],
>     # Block hash in the shard that we are attesting to
>     'shard_block_hash': 'hash32',
>     # Who is participating
>     'attester_bitfield': 'bytes',
>     # Last justified block
>     'justified_slot': 'int256',
>     'justified_block_hash': 'hash32',
>     # The actual signature
>     'aggregate_sig': ['int256']
> }
> ```
>
>
>
> For each one of these attestations [TODO]:
>
>
> Verify that slot = max(block.slot_number - CYCLE_LENGTH, 0)
> Verify that the justified_slot and justified_block_hash given are in the chain and are equal to or earlier than the last_justified_slot in the crystallized state.
> Compute parent_hashes = [get_block_hash(active_state, block, slot - CYCLE_LENGTH + i) for i in range(CYCLE_LENGTH - len(oblique_parent_hashes))] + oblique_parent_hashes
> Let attestation_indices be get_indices_for_slot(crystallized_state, slot)[x], choosing x so that attestation_indices.shard_id equals the shard_id value provided to find the set of validators that is creating this attestation record.
> Verify that len(attester_bitfield) == ceil_div8(len(attestation_indices)), where ceil_div8 = (x + 7) // 8. Verify that bits len(attestation_indices).... and higher, if present (i.e. len(attestation_indices) is not a multiple of 8), are all zero
> Derive a group public key by adding the public keys of all of the attesters in attestation_indices for whom the corresponding bit in attester_bitfield (the ith bit is (attester_bitfield[i // 8] >> (7 - (i %8))) % 2) equals 1
> Verify that aggregate_sig verifies using the group pubkey generated and hash(slot.to_bytes(8, 'big') + parent_hashes + shard_id + shard_block_hash) as the message.
>
>
> Extend the list of AttestationRecord objects in the active_state, ordering the new additions in the same order as they came in the block.
>
>
> Verify that the slot % len(get_indices_for_slot(crystallized_state, slot)[0])'th attester in get_indices_for_slot(crystallized_state, slot)[0]is part of at least one of the AttestationRecord objects; this attester can be considered to be the proposer of the block

