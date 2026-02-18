---
source: ethresearch
topic_id: 7776
title: Efficient unassisted exit witness generation from rollups
author: vbuterin
date: "2020-07-29"
category: Cryptography
tags: []
url: https://ethresear.ch/t/efficient-unassisted-exit-witness-generation-from-rollups/7776
views: 3815
likes: 7
posts_count: 6
---

# Efficient unassisted exit witness generation from rollups

One challenge with current rollup protocols is that if you are a light client of the rollup (ie. you’re not processing the transactions in the rollup yourself, you’re talking to third parties to get proofs of any part of the state you care about), you have no way to generate a Merkle proof of your rollup account balance to exit the rollup without either (i) talking to a third party or (ii) processing the rollup’s entire history yourself.

This is not a large problem in practice, as we expect there to be many state-providing intermediaries and only one honest intermediary is required to assist an exit, but especially if we want to guarantee the ability to exit a rollup quickly even in extreme scenarios, it seems desirable to try to improve on this.

### Understanding the status quo

A rollup is a sequence of on-chain **batches**; each batch contains a list of **state updates** (eg. “account 482 now has balance 808000”), a **post-state root** (the root hash of the new rollup state after applying those updated), and an **attestation** claiming that the post-state root really is the result of applying the updates to the previous state root. In an optimistic rollup, the attestation is a signature from an account that has ETH or other assets deposited, which could be confiscated if they signed an incorrect claim (which can be later proven on-chain via a fraud proof), in a ZK-rollup, it’s a SNARK directly proving the claim.

To withdraw from a rollup, the user needs to generate the current state. They can do this by starting from the beginning, and sequentially processing all state updates (note: there’s no need to compute any hashes while doing this; just keep a table of the whole state). At the end, they generate the entire Merkle tree, allowing them to withdraw.

Suppose that a rollup has n transactions-per-batch, has been in existence for t batches, and has state growth factor r (this is just the portion of activity in the rollup that is creating new accounts, as opposed to editing existing accounts; we’re assuming an eth1-like rollup with no substantial state clearing). The above algorithm requires O(nt) “logistical” operations (searching for a key in a map, editing values, doing arithmetic; all very cheap) and \approx ntr hashes. This is actually surprisingly cheap; you can compute ~1 million hashes per second on a consumer laptop, so a 1200-tx-per-batch (100 TPS) rollup running for a year (~2.5m batches) would require ~3 billion logistical operations and 300 million hashes assuming r=0.1. So far, ~5-10 minutes to generate the current state and be able to withdraw.

Things get trickier when the rollup state size exceeds RAM size, as O(nt) disk accesses would also be required. Disk accesses are unfortunately only possible in the low tens of thousands per second, and so here unfortunately generating the state starts to take hours or longer.

### Proposal

Instead of each rollup batch containing one post-state root, we split up the state into \frac{n}{32} sections, where n is the expected transaction count per batch; the batch must include the post-state root of each section. Note that we can still only save one root on-chain in the state; we just need the batch attestation to also attest to the \frac{n}{32} section roots. Additionally, state updates in the batch must be themselves split up by sections.

Now, generating an exit witness (a Merkle branch for an account) can be split up into two parts: (i) the part of the branch proving the section root is part of the global state, which can be done using only the section roots, and (ii) proving that the account is committed to in the section root.

(i) is trivial, requiring only \frac{n}{32} hashes (reminder: n is transactions-per-batch, so this would at most be ~1000).

(ii) requires the same procedure as in the status quo: clients scan through all historical batches, compute the state and then finally generate the Merkle tree. However, instead of concerning themselves with the entire history, clients can look only at the portion of the batch that deals with the section their account is in, compute only that state, and Merklize only the state.

Now, let’s look at client overhead: on average, each section deals with 32 transactions, so the logistical overhead is O(32t), and the hashing required is O(32tr): both *constant* in the level of usage (!!!). The additional overhead added by this scheme is one hash per 32 transactions, so roughly one byte added to each transaction in the rollup (this could be reduced further by reducing the section count to eg. \frac{n}{256} for one-bit-per-transaction data overhead). Realistically, the main overhead for the client will be that of re-fetching the historical data, if the client does not store history (as most eth1 clients likely won’t in the future).

### Extension: limiting history lookup

A rollup with some state clearing procedure (rent or otherwise) to allow a fixed state size could also require batches to provide on-chain specific accounts (eg. if the state size is D, the k\ mod\ D'th account in the state would be published as part of the k'th batch). This ensures that clients looking to withdraw would only need to go back a finite amount of time in history. Alternatively, the state clearing procedure may well explicitly require state objects to be “poked” once every eg. 6 months to remain part of the state; in that case, we get this benefit “for free” already and there’s no need for an extra procedure to deliberately walk through and re-publish accounts from the state.

## Replies

**sachayves** (2020-07-29):

this is great -)

in case it’s of use to anyone, the original [twitter thread](https://twitter.com/VitalikButerin/status/1288304594515300353) that motivated this solution.

---

**adlerjohn** (2020-07-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> we split up the state into \frac{n}{32} sections

This means that you can’t have more than 32 interactions with the same contract or account in the same block. Should be noted.

As usual, the devil is in the details. There are two ways of sharding (yes, we’re going there) the state: static and dynamic:

1. Static: The state is sharded at genesis, using estimates of n. Cross-shard transactions are impossible.
2. Dynamic: The state is sharded on a per-block basis, with the block producer deciding. This opens up the exploit vector of the block producer choosing to shard the state with the user’s tx in one shard and the rest of the txs to address 0xFFFF.... To produce a state root, the user must apply state transitions touching state elements with address < 0xFFFF..., i.e. all of them. (The address doesn’t have to be all F, it’s easy to get 10+ Fs, so hashing the address doesn’t help.)

Which specific state sharding scheme do you propose? These two aren’t the only way, but hopefully should be sufficient to show that “we split up the state” is missing critical details.

---

**vbuterin** (2020-07-29):

> This means that you can’t have more than 32 interactions with the same contract or account in the same block. Should be noted.

Actually, only the last state of the state object after all of the interactions would need to go on chain, so I don’t think that particular problem actually exists. Remember that in a rollup it’s not txs that go on chain, it’s the post-state of every account that gets modified.

Though you’re right that I did shove under the rug the problem of heterogeneous access. A dynamic approach could work; basically have a rule that if a section has size >64, then split it up into two sub-sections, and provide the roots to both sub-sections of the state. Though I think a static approach would be fine in practice, especially as long as you randomly hash the addresses of state objects, so even eg. two storage slots of the same contract would appear in different locations; that way, concentration would only happen as a result of an active attack.

---

**adlerjohn** (2020-07-30):

Let’s consider ZK rollups, since that’s the primary target of this post anyways.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> it’s the post-state of every account that gets modified

It’s actually the *state deltas* (e.g. `(Alice, Bob, 5)`) not *post states* (e.g. `(Alice, Alice_bal, Bob, Bob_bal)`. The reason is plain as day: post states have an extra amount. In other words, the overhead of this using this scheme isn’t ~1 byte per tx, it’s an extra amount per tx! From what I could gather of ZK rollups available today, for zkSync this is 5 bytes, and for Loopring this is 16 bytes. Which would decrease tps by on the order of 30+%.

We could *in theory* construct a ZKP that elides away everything at the block level, but that would require an enormous amount of research and implementation effort, and would have insane proving costs. Let’s stay within the unfortunately tight bounds of reality.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> basically have a rule that if a section has size >64, then split it up into two sub-sections, and provide the roots to both sub-sections of the state

State is effectively unbounded in size, so splitting up state like this wouldn’t help. Or rather, what you’re proposing here isn’t clear.

The attack is:

32 txs to addresses in the range `0x0000...`–`0xFFF0...`

32 txs to addresses in the range `0xFFF0...`–`0xFFF1...`

32 txs to addresses in the range `0xFFF1...`–`0xFFF2...`

and so on. There’s nothing to split here.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> randomly hash the addresses of state objects

An attacker only needs to find \log{\frac{n}{32}}-bit collisions, i.e. it’s trivial. Hashing the addresses doesn’t help at all.

*Edit:* These points about addresses are a red herring since ZK rollup implementations use indices instead of addresses. It should be noted that we may not be able to assume a uniform distribution with indices, as we could with the output of a hash function.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> concentration would only happen as a result of an active attack

That’s correct! And detecting such an attack requires a synchrony assumption, defeating most of the point of ZK rollups over optimistic rollup.

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> Static: The state is sharded at genesis, using estimates of n . Cross-shard transactions are impossible.

Finally, even if we concede that the static approach’s synchrony assumption is fine, we either have to forbid cross-shard transactions (they would allow an attacker to simply flood one of the shards) *or* we have to double-count cross-shard transactions, which would greatly decrease the number of transactions that can fit in a batch, increasing overheads even more.

---

**vbuterin** (2020-08-01):

Yeah, you’re right that the scheme doesn’t really work well with deltas; aside from what you mentioned the other big problem is that for Alice and Bob to be able to find the state update it would need to exist in both Alice and Bob’s segment of the rollup batch, doubling the size (ie. post-states would be more efficient at that point). So yes, rollups would have to become ~30% more expensive in some cases (though not in all cases, eg. I don’t think zk zk rollups would grow much).

I do think that concentration attacks are beatable if we think harder; though the least-bad solution may well be pushing the solution up to client level by adding a gas mechanic to limit activity per address/index range and letting clients choose to move their account to another address/index range. Though I should point out that even if active attacks are not handled, the gains from this technique are still far from worthless, as all users other than the attacked user could still exit quickly.

