---
source: magicians
topic_id: 5805
title: Proposed Verkle tree scheme for Ethereum state
author: vbuterin
date: "2021-03-25"
category: Working Groups > Ethereum 1.x Ring
tags: [trie]
url: https://ethereum-magicians.org/t/proposed-verkle-tree-scheme-for-ethereum-state/5805
views: 7938
likes: 11
posts_count: 26
---

# Proposed Verkle tree scheme for Ethereum state

# Proposed Verkle tree scheme for Ethereum state

*Edit 2021.06.07: edited the leaf structure to fit account headers and code and a few storage slots together*

This document describes a proposal for how concretely the Ethereum state can be represented in a Verkle tree.

See [HackMD - Collaborative Markdown Knowledge Base](https://notes.ethereum.org/_N1mutVERDKtqGIEYc-Flw) for notes of how Verkle tries work.

## Desiderata

- Short witness length for accounts or storage, even under “attack”. This necessitates:

An “extension node”-like scheme where the bulk of an address or storage key can be stored as part of a single node, instead of always going 32 layers deep
- Hashing account addresses and storage keys to prevent attackers from filling the storage in locations that are close enough to each other that branches to them become very long without doing a very large amount of brute force computation

Maximum simplicity. Particularly, it would be ideal to be able to describe the result as a single Verkle tree
Forward-compatibility (eg. ability to add more objects into an account header in the future)
Code for an account should be stored in one or a few subtrees, so that a witness for many code chunks can be minimally sized
Frequently-accessed values (eg. balance, nonce) should be stored in one or a few subtrees, so that a witness for this data can be minimally sized
Data should be by default reasonably distributed across the entire state tree, to make syncing easier

An updated proposal, which puts account data closer together to reduce the witness size per-account-access:

---

The proposed scheme can be described in two different ways:

1. We can view it as a “trie of commitments”, with two additional simplifications:

Only leaf nodes containing extended paths, no “internal” extension nodes
2. The leaves of the top trie are only commitments (that are Kate commitments of the same type as the commitments used in the trie), and not “a hash pointing to a header which contains two values, a bytearray and a tree” as is the status quo today
3. We can view it as a single tree, where there are internal extension nodes but they can only extend up to the 31 byte boundary (tree keys MUST be 32 bytes long)

These two perspectives are completely equivalent. We will focus on (2) for the rest of the description, but notice that if you take perspective (1) you will get a design where each account is a subtree.

The Verkle tree structure used, from the first perspective, will be equivalent to the structure [described here](https://notes.ethereum.org/_N1mutVERDKtqGIEYc-Flw). From the second perspective, it would be equivalent to the structure described in that document, except that instead of (key, value) leaf nodes, there would be intermediary nodes that extend up to the 31 byte boundary.

We define the spec by defining “tree keys”, eg. if we say that the tree key for storage slot Y of account X is some value `f(X, Y) = Z`, that means that when we SSTORE to storage slot Y in account X, we would be editing the value in the tree at location `Z` (where `Z` is a 32-byte value).

Note also that when we “store `N` at position `P` in the tree”, we are *actually* storing `hash(N) % 2**255`. This is to preserve compatibility with the current 32-byte-chunk-focused storage mechanism, and to distinguish “empty” from “zero” (which is important for [state expiry proposals](https://hackmd.io/@vbuterin/state_expiry_paths)).

### Parameters

| Parameter | Value |
| --- | --- |
| VERSION_LEAF_KEY | 0 |
| BALANCE_LEAF_KEY | 1 |
| NONCE_LEAF_KEY | 2 |
| CODE_KECCAK_LEAF_KEY | 3 |
| CODE_SIZE_LEAF_KEY | 4 |
| HEADER_STORAGE_OFFSET | 64 |
| CODE_OFFSET | 128 |
| VERKLE_NODE_WIDTH | 256 |
| MAIN_STORAGE_OFFSET | 256**31 |

*It’s a required invariant that `VERKLE_NODE_WIDTH > CODE_OFFSET > HEADER_STORAGE_OFFSET` and that `HEADER_STORAGE_OFFSET` is greater than the leaf keys. Additionally, `MAIN_STORAGE_OFFSET` must be a power of `VERKLE_NODE_WIDTH`.*

### Header values

The tree keys for this data are defined as follows:

```auto
def get_tree_key(address: Address, tree_index: int, sub_index: int):
    # Asssumes VERKLE_NODE_WIDTH = 256
    return (
        hash(address + tree_index.to_bytes(32, 'big'))[:31] +
        bytes([sub_index])
    )

def get_tree_key_for_version(address: Address):
    return get_tree_key(address, 0, VERSION_LEAF_KEY)

def get_tree_key_for_balance(address: Address):
    return get_tree_key(address, 0, BALANCE_LEAF_KEY)

def get_tree_key_for_nonce(address: Address):
    return get_tree_key(address, 0, NONCE_LEAF_KEY)

# Backwards compatibility for EXTCODEHASH
def get_tree_key_for_code_keccak(address: Address):
    return get_tree_key(address, 0, CODE_KECCAK_LEAF_KEY)

# Backwards compatibility for EXTCODESIZE
def get_tree_key_for_code_size(address: Address):
    return get_tree_key(address, 0, CODE_SIZE_LEAF_KEY)
```

### Code

```python
def get_tree_key_for_code_chunk(address: Address, chunk_id: int):
    return get_tree_key(
        address,
        (CODE_OFFSET + chunk) // VERKLE_NODE_WIDTH,
        (CODE_OFFSET + chunk)  % VERKLE_NODE_WIDTH
    )
```

Chunk `i` contains a 32 byte value, where bytes 1…31 are bytes `i*31...(i+1)*31 - 1` of the code (ie. the i’th 31-byte slice of it), and byte 0 is the number of leading bytes that are part of PUSHDATA (eg. if part of the code is `...PUSH4 99 98 | 97 96 PUSH1 128 MSTORE...` where `|` is the position where a new chunk begins, then the encoding of the latter chunk would begin `2 97 96 PUSH1 128 MSTORE` to reflect that the first 2 bytes are PUSHDATA).

### Storage

```python
def get_tree_key_for_storage_slot(address: Address, storage_key: int):
    if storage_key < (CODE_OFFSET - HEADER_STORAGE_OFFSET):
        pos = HEADER_STORAGE_OFFSET + storage_key
    else:
        pos = MAIN_STORAGE_OFFSET + storage_key
    return get_tree_key(
        address,
        pos // VERKLE_NODE_WIDTH,
        pos % VERKLE_NODE_WIDTH
    )
```

Note that storage slots in the same size `VERKLE_NODE_WIDTH` range (ie. a range the form `x*VERKLE_NODE_WIDTH ... (x+1)*VERKLE_NODE_WIDTH-1`) are all, with the exception of the `HEADER_STORAGE_OFFSET` special case, part of a single commitment. This is an optimization to make witnesses more efficient when related storage slots are accessed together. If desired, this optimization can be exposed to the gas schedule, making it more gas-efficient to make contracts that store related slots together (however, Solidity already stores in this way by default).

Additionally, storage slots `0 ... (CODE_OFFSET - HEADER_STORAGE_OFFSET - 1)` are stored in the first commitment (so you can think of them as “editable extra header fields”); this is a further optimization and allows many simple contracts to fully execute by loading only a single commitment.

## Replies

**pipermerriam** (2021-03-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Note also that when we “store N at position P in the tree”, we are actually storing hash(N) % 2**255. This is to preserve compatibility with the current 32-byte-chunk-focused storage mechanism, and to distinguish “empty” from “zero”

I don’t understand this part.  This seems to suggests that we are not storing the value but the hash of the value?  Which is confusing to me since hashing implies we can’t recover the original value?

---

**carver** (2021-03-25):

IIUC, we would *logically* store the hash in the tree for the purposes of generating the verkle commitment, but we would *in practice* store the original value in whatever on-disk key/value store is used.

---

**vbuterin** (2021-03-25):

This is exactly correct.

---

**carver** (2021-03-26):

So calling `SELFDESTRUCT` would take O(num_used_slots) to clear them all out. The cleanest resolution to that problem is to say that we should disable `SELFDESTRUCT` before verkles go live. (which I’m in favor of doing anyway)

---

**vbuterin** (2021-03-26):

There’s a way to do it without that: have a “number of times self-destructed” counter in the state and mix it in with the address and storage key to compute the tree path. But that’s ugly in a different way, and yes, we [should just disable SELFDESTRUCT](https://hackmd.io/@HWeNw8hNRimMm2m2GH56Cw/selfdestruct).

---

**pipermerriam** (2021-03-27):

So it seem like we either:

- Get rid of SELFDESTRUCT which based on some recent discussion in ACD looks like it may be complex due to the interplay with CREATE2 and “upgradeable” contracts.
- Keep SELFDESTRUCT but replace the actual state clearing with an alternate mechanism that just abandons the state.  When combined with the state expiration schemes, this is effectively like deleting it since it will become inaccessible and eventually expire.
- Keep SELFDESTRUCT and determine how we can clear the state in a manner that doesn’t have O(n) complexity.

---

**vbuterin** (2021-03-27):

Right, those are basically the three choices. My preference is strongly toward the first, and we acknowledge that upgradeable contracts through a full-reset mechanism were a mistake.

---

**carver** (2021-03-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> and we acknowledge that upgradeable contracts through a full-reset mechanism were a mistake.

![:100:](https://ethereum-magicians.org/images/emoji/twitter/100.png?v=12)

… and if `DELEGATECALL` isn’t appealing enough as an upgrade mechanism, let’s figure out how to improve that. (rather than how to keep in-place contract morphing via `SELFDESTRUCT`).

---

**dankrad** (2021-04-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Data should be by default reasonably distributed across the entire state tree, to make syncing easier

I don’t quite understand how this proposal achieves this. The initial 3 bytes are taken directly from the account address. So if an account has a 1 GB storage tree, then the subtree starting with those three bytes will store that 1 GB of data, much more than 100 GB / 2^24 = ~ 6 kB that an average subtree at that level stores.

---

**poemm** (2021-04-07):

As you know, `address[:3]` guarantees deduplicatation of an account’s the first 3 witness chunks. So I think the motivation is to optimize witness size. So just a clever trick.

I was wondering: is there any reason not to do `address[:2]` or `address[:4]`? More generally, what is the motivation for the “reasonably distributed” property (edit: how does it make syncing easier edit2: and how does it trade-off with the “short witness length” property)?

---

**poemm** (2021-04-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Frequently-accessed values (eg. balance, nonce) should be stored in one or a few subtrees, so that a witness for this data can be minimally sized

It is clever to use `hash(same thing)` + `bytes([i])`, `chunk_lo`, or `s_key_lo` to keep related values as neighbors in the tree.

A further optimization: the account version/balance/nonce/codehash/codesize commitment can also store, for example, the first ~100 code chunks and the smallest ~100 storage keys. But this optimization adds complexity, so I won’t push it.

---

**gballet** (2021-04-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> ```auto
> def get_storage_slot_tree_key(address, storage_key):
>     s_key_hi = (storage_key // 256).to_bytes(32, 'big')
>     s_key_lo = bytes([storage_key % 256])
>     return address[:3] + hash(address + b'\x02' + s_key_hi)[:28] + s_key_lo
> ```

Is there a reason for `s_key_hi` to be a 32-byte integer? The most significant byte is always `\x00`, so it seems that it could be omitted.

---

**vbuterin** (2021-04-14):

[@dankrad](/u/dankrad) [@poemm](/u/poemm) I’m not super attached to `address[:3]` specifically. There’s a tradeoff: `address[:4]` makes witnesses slightly smaller, but it makes data less well-distributed, as then it would be a `1/2**32` slice instead of a `1/2**24` slice that could have a large number of keys. Meanwhile `address[:2]` slightly reduces the witness size advantage, at the cost of improving distribution. It’s possible that the optimal thing to do is to just abandon the `address[:x]` thing entirely; it would not be that bad, because in a max-sized block the first ~1.5 bytes are saturated anyway, and it would make the even-distribution property *very* strong (only deliberate attacks could concentrate keys).

---

**vbuterin** (2021-04-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png) gballet:

> Is there a reason for s_key_hi to be a 32-byte integer? The most significant byte is always \x00, so it seems that it could be omitted.

No big reason. I guess making it a 32-byte integer is slightly more standardized, as we have plenty of 256-bit ints but no other 248-bit ints. It doesn’t make a significant difference either way.

---

**g11in** (2021-05-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Note that the header and code of a block are all part of a single depth-2 commitment tree; this is an optimization to make code witnesses more efficient, as transactions that access an account always

I guess we mean account here instead of block?

---

**g11in** (2021-05-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Note that storage slots in the same size-65536 range (eg. 0…65536, 131072…196607) are all part of a single commitment;

So account’s basic data (header + code) is chunked into 256*32 byte chunks for generating a commitment per chunk and storage chunked into 65536 * 32 bytes

i.e. basic data’s leaf is Commitment of poly that take these 256 evaluations i.e.

`Commitment(P| P(w^0)=Hash(0th 32 byte)... P(w^255)=Hash(255th 32 Byes)` i.e. commitment of  some `P= 255 max degree poly in w`

and storage data’s leaf is  a poly which takes these 65536 valuations i.e.

`Commitment(P| P(w^0)=Hash(0th 32 byte).... P(w^655355)= Hash (65535th 32 byte)` i.e. commitment of some `P= 65535 max degree poly in w` ?

and rest of the commitments in the verkel tree corresponding to polys which take 256 max evaluations (hence 256 max degree) of their children.

---

**storc** (2021-06-23):

Sorry it’s late in my timezone and I’m too tired to connect a few concepts I haven’t touched in a few years.

Any reason why you’ve ruled out using a trie instead? It sounds like there’s a concern for an attacker to build out an imbalanced tree and debilitate ease of access.

What about a self-balancing trie where rebalancing process includes a random/pseudo-random hash that would limit predictability of structure on rebalance.

This seems nice because you keep sub-trees, search is almost always optimal (or can be reconfigured based on assembly), AND assembly of the tree itself is quick (meaning the rebalancing act isn’t too expensive)

I also like that with deterministic locations …you could jump without having to traverse from the beginning (so even quicker)

---

**Shymaa-Arafat** (2021-06-24):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/d26b3c/48.png) storc:

> Any reason why you’ve ruled out using a trie instead?

Ethereum uses Tries from the very beginning

I think those 2 can give u an idea about the status quo, and the problem of proof size


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-2584)





###











      ![](https://ethereum-magicians.org/uploads/default/optimized/2X/e/e806eff31f5c56c5b4933fead6d7389a9db04a1f_2_500x500.png)

      [Ethereum Foundation Blog](https://blog.ethereum.org/2020/11/30/the-1x-files-code-merkleization)



    ![](https://ethereum-magicians.org/uploads/default/optimized/2X/6/685fdf765b4042d444d5b2ef923c0c365661f1f8_2_690x271.png)

###










This new Verkle Tree/Trie I haven’t complete reading yet, but has the augmented tree property where u can get the proof only from nodes along the path without the need to fetch all siblings along the path

( Kate Commitments r associative functions)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/g11in/48/3906_2.png) g11in:

> Note3.3:
>  (applying Elliptic Curve) is a linear operator i.e.
> +[y]=[x+y].also a=[ax]
> Note3.5:
> Commitment of f(x): C(f)=[f(s)] is also a linear operator i.e. C(f+g)=C(f)+C(g)

.

Anyways, I believe this is a shorter to the point note about the data structure part, if u can’t read all of the above at once (like me)

https://vitalik.ca/general/2021/06/18/verkle.html

---

**Shymaa-Arafat** (2021-07-06):

Have u read this old thread from 2017 I think?



      [gnusha.org](https://gnusha.org/pi/bitcoindev/CAPg+sBgruEiXya6oFy6VpmR1KPDebjeGDtZZU+facZx5=L_a5w@mail.gmail.com/)





###










I know it’s about Bitcoin, but maybe it can add some useful insight about the Cryptographic merits of the idea

[![IMG_20210706_131230](https://ethereum-magicians.org/uploads/default/optimized/2X/8/8d084c857e9a8a4ecced13167ce65ae3a5878541_2_225x500.jpeg)IMG_20210706_131230720×1600 217 KB](https://ethereum-magicians.org/uploads/default/8d084c857e9a8a4ecced13167ce65ae3a5878541)

[![IMG_20210706_130634](https://ethereum-magicians.org/uploads/default/optimized/2X/e/e12f508205a8a3b45bf6c71d0c70900d51384a28_2_225x500.jpeg)IMG_20210706_130634720×1600 223 KB](https://ethereum-magicians.org/uploads/default/e12f508205a8a3b45bf6c71d0c70900d51384a28)

.

I don’t know,  could be I’m wrong & they’re not related methodologies?

---

**storc** (2021-07-12):

Thanks Shymaa! Appreciate your respectful answer and the resources you condensed for me to be brought up to speed.


*(5 more replies not shown)*
