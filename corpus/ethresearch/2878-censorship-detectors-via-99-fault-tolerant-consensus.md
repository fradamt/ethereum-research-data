---
source: ethresearch
topic_id: 2878
title: Censorship detectors via 99% fault tolerant consensus
author: vbuterin
date: "2018-08-10"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/censorship-detectors-via-99-fault-tolerant-consensus/2878
views: 3795
likes: 3
posts_count: 3
---

# Censorship detectors via 99% fault tolerant consensus

See previous work: [Censorship rejection through "suspicion scores"](https://ethresear.ch/t/censorship-rejection-through-suspicion-scores/305)

See also as background: https://vitalik.ca/general/2018/08/07/99_fault_tolerant.html

We can use the 99% fault tolerant consensus algorithm described above by having it constantly run “in the background”, to create a consensus on what data was broadcasted at what times, and therefore what data the main chain is maliciously failing to include.

Using old finalized blockchain state as a source of validators and entropy, we agree on a sequence of validators, `V[1]`, `V[2]`…, where each validator is assigned to a slot (eg. of 1 minute length). Let `[G + D * x, G + D * (x+1)]` be the time interval associated with slot `x`. At time `G + D * (k * 100)`, any validator in `V[k * 100] ... V[k * 100 + 99]` can publish a message `(h, sig(h))` for any hash `h` of a block that they saw in the previous interval of 100 * D seconds. Over the next 100 periods, the 99% fault tolerant consensus protocol runs: any validator in that set, upon receiving a value `v` with `n` signatures with some hash `h` that they did not yet sign off on, checks if the time is less than `G + D * (k * 100 + n)`, and if it is then it publishes `(v, sig(v))` with their own signature.

Clients watching this process accept a block with hash `h` as having been published within a given slot if they see the block and they see a message with `n` signatures before time `G + D * (k * 100 + n - 0.5)`. There is a proof (see blog post) that, if the network latency assumption is correct, clients will agree on which blocks were published during what interval. Now, we can socially agree on a definition of “censorship” (eg. if a block was published during interval `k`, and was not included in a chain that was published after interval `k+1`, then that chain is censoring that block), and coordinate on rejecting majority chains that are censoring, and coordinate on a minority soft fork to get around the attack.

## Replies

**daniel_sg** (2018-08-21):

Hello,

Can I ask to what degree this can/must be integrated with the beacon chain algorithm?

So I noticed that the slot length in this proposal is 1 minute, which is different from the 8 seconds for slots in the beacon chain (in the blog post on vitalik.ca they’re the same). Is this intentional in the sense that it works for any slot length?

Or is some synchrony needed between the two mechanisms to be able to prove to observers/clients that the block was really proposed ‘in time’ for the next proposer to use it as a parent? (Instead of being censored by a supermajority who are pretending to not receive the minority’s blocks in time?)

And can I also ask to what degree there is overlap between the messages used normally for block information transmission and the new mechanism? Can many of those messages be reused, but with validators adding their signature to those messages if the time constraints aren’t violated? (There may be more, because a validator who receives a known message/block but with more signatures than they previously saw will probably want to rebroadcast it.) Does this require synchrony?

In the OM(m) and SM(m) algorithms of the Byzantine Generals Problem paper by Lamport et al., ‘m’ refers to the maximum number of signatures for a message - a lower value for m means a smaller number of messages, but less security. Will this algorithm include a similar maximum?

---

**vbuterin** (2018-08-21):

The slots in the beacon chain and in this algorithm don’t need to be the same; the two mechanisms can be fairly decoupled from each other, at least minute-by-minute.

