---
source: magicians
topic_id: 8281
title: "EIP-4788: Beacon root in EVM"
author: ralexstokes
date: "2022-02-13"
category: EIPs > EIPs core
tags: [cancun-candidate]
url: https://ethereum-magicians.org/t/eip-4788-beacon-root-in-evm/8281
views: 11343
likes: 25
posts_count: 46
---

# EIP-4788: Beacon root in EVM

Discussion thread for [EIP-4788: Beacon block root in the EVM](https://github.com/ethereum/EIPs/pull/4788).

## Replies

**MicahZoltu** (2022-02-14):

> By including the ommersHash validation, clients can use existing code with only minimal changes (supplying the actual state root) during block production and verification.
>
>
> Having the beacon state root value in the ommers field means that it is fairly straightforward to provide the value from the block data to the EVM execution context for client implementations as they stand today.

I would like to get validation from execution client teams that this is actually of meaningful value.  It may be just as easy to completely remove the uncle validation code entirely as it would be to pseudo-replace it with this.  If so, then I would strongly advocate for changing this into a single 32-byte hash rather than an array of 1 item.

---

**jochem-brouwer** (2022-02-17):

Should the storage address be added to warm addresses by default (EIP 2929?)

---

**jochem-brouwer** (2022-02-17):

Correct me if I am wrong but this should also have a rule that if you `CALL` the storage address, this should not get removed from the state. I am pretty sure that accounts which have non-empty storage, but no code, nonce 0 and balance 0 are `DEAD` and should therefore get removed from the MPT (thus clearing the storage). The alternative could be to just send 1 wei to this address, but it should be noted in the EIP anyways.

---

**mkalinin** (2022-02-18):

A couple of things:

Epoch/slot/timestamp as a fork trigger requires support of two EL blocks at the same height with different consensus rules and/or structures. AFAIK, this is not currently supported by client implementations and might result in additional complexity.

I am echoing Vitalik’s comment on slot vs block number. Imagine an application that securely (with a proof) reads validator record from a beacon state, an interface of this app will have to do slot to block height translation to specify the right beacon block root for the proof verification process. Using slot number allows to avoid this complexity, reads will look like `slot.validator(i).effective_balance`. Though, this approach requires slots to be passed to EL block, perhaps slot numbers are suitable replacement for `difficulty` values.

---

**axic** (2022-02-18):

For the reading of the value it would be possible to include code at the address, and require a `CALL` to be made to the address as opposed to a dedicated opcode. This would be similar to [EIP-210](https://eips.ethereum.org/EIPS/eip-210).

This does raise the question why not also do the same for `RANDAO(n)` in [EIP-4399: Supplant DIFFICULTY opcode with RANDOM](https://ethereum-magicians.org/t/eip-4399-supplant-difficulty-opcode-with-random/7368).

---

**MicahZoltu** (2022-02-20):

IIUC, the two arguments are:

1. Changing the shape of the block makes it easier to differentiate between blocks of different eras as you can just look at the block’s shape to know “when” the block was from.
2. Changing the shape of the block can break existing code that depends on block shape to decode.

I think the question we need to answer is which of these is likely to have a larger negative impact on the Ethereum ecosystem long term.  If (1), then adding a new field to the end and (optionally, if we want to save 32 bytes per block) deleting OmmersHash from the middle is the ideal strategy.  If (2), then changing the interpretation of OmmersHash to be BeaconRoot is the optimal strategy.

---

**bbuddha** (2022-07-28):

This EIP is useful for liquid staking protocols that want to prove new balance updates for their validators and account fault with the highest security. Most LSDs rely on a small oracle committee to supply them this sort of information. In addition, there are tons of new applications that will be built given the trustless access to more detailed protocol parameters. Seems like a win. What are implementation barriers for this sort of thing?

---

**ralexstokes** (2022-07-29):

there are many many many applications unlocked by this EIP

the implementation barriers are not really the blocking ones, the bigger issue is simply prioritizing this feature amongst all other things we want to do to make ethereum better ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**bbuddha** (2022-07-30):

Agreed! What’s the process of getting this prioritized?

---

**ralexstokes** (2022-07-30):

im happy to help you argue for it on ACD sooner or later

i can say that it will be hard to prioritize against validator withdrawals and work around 4844

and currently ACD is very focused on a successful merge so we haven’t really done any serious Shanghai planning and I’m not sure now is the right time.

perhaps we revisit after the merge has occurred?

---

**bbuddha** (2022-07-30):

Totally. Appreciate it. Thanks for the responses, excited for this ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**kanewallmann** (2022-09-27):

My understanding is that to be able to prove some value in the beacon state, we also need to know the generalised index of the property we wish to prove (or more generally the depth of the merkle tree representations of the objects in the path with which we can compute the generalised indices of properties).

It seems likely (and is already the case in Capella) that the consensus spec containers will be appended to in future forks and so the depth of their tree representation may increment and therefore all the generalised indices of the existing properties will change too.

The consequence of this is that any smart contract that verifies proofs will need some sort of upgradability to be forwards compatible with future changes to the beacon state object.

This seems to break some of the fundamental usefulness of having the state root available on the EVM because proof verification logic cannot be made immutable. Previously, we had to trust an oracle to submit the correct state about the beacon chain. Now, we have to trust the contract owner to upgrade the proof verification logic as required by future consensus spec changes.

Unless the proof verification logic was also made part of the EVM via a precompile or something.

Am I missing something?

---

**dapplion** (2022-11-10):

This EIP requires changes to the consensus layer and engine API. Where should those be spec’ed? I recall EIP4844 having similar issues.

---

**Holterhus** (2023-02-17):

We’ve discussed an idea that seems to solve this issue on discord, so I will also write it down here for anyone interested.

Basically, if you assume that the data containers are only ever *appended* to, then the tree depth increasing is really just adding an extra “left” movement to the start of the path from the root to the leaf in question. For example, if the leaf element you are interested in is currently “right” then “left” from the root, your verifier smart contract would probably look like this:

```auto
function verify(bytes32[] proof, bytes32 root, bytes32 node) internal {
    node = keccak256(abi.encodePacked(node, proof[0]));
    node = keccak256(abi.encodePacked(proof[1], node));
    require(root == node);
}
```

The point we are making is that any time the tree depth increases from newly appended properties, the existing container properties will be in the left subtree, so the verifier could have just been implemented like this:

```auto
function verify(bytes32[] proof, bytes32 root, bytes32 node) internal {
    node = keccak256(abi.encodePacked(node, proof[0]));
    node = keccak256(abi.encodePacked(proof[1], node));
    for (uint256 i = 2; i < proof.length; ++i) {
        node = keccak256(abi.encodePacked(node, proof[i]));
    }
    require(root == node);
}
```

to allow longer proofs if they are needed in the future.

---

**haltman-at** (2023-06-08):

So is there some reason this is seemingly currently being done via a stateful (!) precompile rather than just a new opcode?  A new opcode seems like it would fit better… it’s stateful, after all, and this seems to be just reading that state, not just doing computation?  Everything about this has the characteristics of an opcode, not a precompile; it seems like the wrong mechanism is being used here.  Is it to save on opcode space?  There’s quite a lot of that still, so that hardly seems like a good reason to use this awkward, seemingly-incorrect mechanism.

---

**ralexstokes** (2023-06-09):

we can always use the “last” opcode as a pointer to an extension table so in fact there is unlimited opcode address space

a big motivator for the stateful precompile approach is facilitating the migration to a stateless world w/ Verkle tries and stateless clients

having everything required for protocol execution live w/in the execution state means the state transition function can be a function of the pre state and next block, to get the post state; which is cleaner for stateful clients and makes proofs for stateless clients easier to manage

a close analog to the functionality provided in this EIP is the `BLOCKHASH` opcode which just summons some history alongside the execution state – so now to validate an ethereum block you don’t need just the state but also this small buffer on the side of the last 256 hashes; this makes the stateless paradigm a bit more awkward so its better to design in the direction of 4788

there are even EIPs floating around to change `BLOCKHASH` so that it follows the pattern of 4788

---

**jochem-brouwer** (2023-06-10):

I have some questions regarding this EIP.

> set 32 bytes of the execution block header after the last header field as of FORK_TIMESTAMP to the 32 byte hash tree root of the parent beacon block

I am not sure how to interpret this. Does this imply that we add a new field to the block header after the last header field (such that we RLP encode this)? Or, do we first RLP-encode the block header and then add these 32 bytes…?

The new precompile (which it definitely is, since it does do some EVM behavior like SLOAD, but will not add these to warm slots to account for them) is located at `0xfffffffffffffffffffffffffffffffffffffffd`. Why here? Why not in the precompile range `0x00..00` - `0x00..00ffff` (see [EIP-1352: Specify restricted address range for precompiles/system contracts](https://eips.ethereum.org/EIPS/eip-1352), it is stagnant, but I was under the impression that those “low” addresses were indeed reserved for precompiles). I am mainly worried about RIPEMD160 scenarios ([Clarification about when touchedness is reverted during state clearance · Issue #716 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/716)). We can fix this on mainnet by sending 1 wei to this precompile (currently it has no eth). However since usually genesis files on testnets fill the precompiles in order to avoid this RIPEMD160 behavior, this `0xfffffffffffffffffffffffffffffffffffffffd` address is not there. Is there a motivation to put this there, and not at a “low” address?

---

**haltman-at** (2023-06-11):

I’m not sure I follow how using a stateful precompile makes that any better (the state still has to be stored somewhere!), but good to at least know there’s some non-arbitrary reason for it.

> there are even EIPs floating around to change BLOCKHASH so that it follows the pattern of 4788

Got a link?

---

**haltman-at** (2023-06-11):

I assumed the odd high address was to mark it as a stateful precompile rather than an ordinary one.  But meanwhile I’m wondering, why -3 of all things, when (assuming people are setting aside high addresses in this way) -1 and -2 have yet to be taken?

---

**ralexstokes** (2023-06-12):

> Got a link?

https://eips.ethereum.org/EIPS/eip-2935

the idea is that everything is under one object, namely the execution state, rather than the execution state *and* some additional context (like it is today for block hash)


*(25 more replies not shown)*
