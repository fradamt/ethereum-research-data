---
source: magicians
topic_id: 23018
title: "EIP-7892: Blob Parameter Only Hardforks"
author: ethDreamer
date: "2025-02-28"
category: EIPs > EIPs core
tags: [layer-2, scaling, blob]
url: https://ethereum-magicians.org/t/eip-7892-blob-parameter-only-hardforks/23018
views: 445
likes: 6
posts_count: 9
---

# EIP-7892: Blob Parameter Only Hardforks

Discussion topic for [EIP-7892](https://eips.ethereum.org/EIPS/eip-7892)

#### Update Log

- 2025-02-28: Add EIP: Blob Parameter Only Hardforks

#### External Reviews

None as of 2025-02-28

#### Outstanding Issues

None as of 2025-02-28

## Replies

**cskiraly** (2025-06-19):

> The maxBlobsPerTx field is optional and defaults to value of max when omitted. It is not used by the consensus layer.

I think defaulting to “max” is not great. It was already a source of misunderstanding in the past, when people assumed it is 9 because max was 9. We should better avoid that same mistake. I would either keep it out of BPO scope, or make it mandatory.

---

**SamWilsn** (2025-07-30):

I’d like to suggest that instead of the `bpo*` naming convention, we go with something a bit more fun (and uniform with the glacier forks).

Here are a few options:

- Lava Types

Examples: Aa Lava, Pahoehoe Lava, Block Lava, Pillow Lava, Silicate Lava
- Pros:

Pairs nicely with the Glacier forks.
- Lava is kinda blobby.
- Short suffix.

*Cons:*

- Generally considered a natural disaster, so might carry an unfortunate connotation.
- Fairly limited list of options, could run out if there are many BPO forks.

**Organisms**

- Examples: Wolf Slime, Pretzel Slime, Chocolate Slime, Candy Slime, Raspberry Slime
- Pros:

Slimes are very blobby.
- Nearly a thousand slimy options to choose from.

*Cons:*

- Do we really want to name something slime?
- Only a limited number of common names.

**Desserts**

- Examples: Cabinet Pudding, Asida Pudding, Mango Pudding
- Pros:

Desserts are good!
- Decent number of options.
- Reasonably blobby.

*Cons:*

- Might encourage overeating.

**RPG-style Monsters**

- Examples: Gelatinous Ooze, Gray Ooze, Green Ooze
- Pros:

Can generate as many as necessary by combining an adjective with Ooze.
- The blobbiest.
- Short Suffix.

*Cons:*

- Have to watch out for trademarks.

---

**fselmo** (2025-07-30):

I like it.

2cents: Comets / asteroids are quite blobby and would be kind of close to “glaciers” (ice) of space? Aligns with the stars naming concept. I think asteroids have more common names but looks like there are plenty of comet common names to pick from (https://ssd.jpl.nasa.gov/tools/sbdb_query.html).

---

**etan-status** (2025-08-06):

I wonder why only the ForkDigest is rolled on a BPO, without the ForkVersion.

The problem with only rolling the ForkDigest is that after the BPO activates, network traffic from clients that did not upgrade remains valid on the network partition of clients that upgraded. This essentially provides withholding-as-a-service, which was a big topic back when fork choice security was revisited.

- Imagine 1/3rd didn’t update, and gets the first 17 blocks around the BPO activation (probability comparable to winning powerball lottery, which periodically happens in practice).
- Then, 1 malicious node re-broadcasts the head of these blocks on the new network partition, or maybe even just attestations to these blocks
- Peers on the new network partition have not seen any parents, and will req/rsp the missing data. Only the malicious node initially has the data, leading their nodes to gain peer score while the honest but useless peers without the data may lose peer score

Questions are:

- Is BPO safe from a perspective of fork choice?
- Is BPO safe from a perspective of sync performance?
- Why not also roll ForkVersion?

> Full hard forks require extensive coordination, testing, and implementation changes beyond parameter adjustments. For example, in Lighthouse, a typical hard fork implementation requires thousands of lines of boilerplate before any protocol changes occur. BPO forks streamline this process by avoiding the need for this boilerplate code.

The EIP rationale doesn’t make sense to me. The same coordination is required for a BPO: All users have to update clients before it activates, and the node consumes more resources after the fork, possibly requiring hardware upgrades; the experience for users is exactly the same as for a full blown fork.

Fork version could be similarly designed as a “parameter adjustment”. One has to be careful though to choose globally (across all chains) unique (fork_version, genesis_validators_root) tuples to avoid slashings across chains.

---

**poojaranjan** (2025-08-06):

[@ethDreamer](/u/ethdreamer) [explains EIP-7892](https://www.youtube.com/watch?v=Q58Wm5gtiJY) for upgrading blob parameters without a full protocol hardfork.

  [![image](https://img.youtube.com/vi/Q58Wm5gtiJY/maxresdefault.jpg)](https://www.youtube.com/watch?v=Q58Wm5gtiJY)

---

**rolfyone** (2025-08-20):

When they were initially proposed, it was because forks for some clients(iirc) were ‘expensive’ if we’re just updating one field.

In hindsight i’d just go for a fork and take the overheads and address why its so hard in how we’re doing things, or i’d push harder for not caring and setting a high maximum thats ‘sane’.

The real ‘nuts and bolts’ of these forks are in execution, and they’re a real fork at that layer. In execution they need to address target etc, and we’re only interested in the maximum value for our single validation rule that comes into play.

Initially BPO didn’t adjust the fork digest and it was seen as a problem because we’d have gossip that now is potentially ‘not compatible’ on the same topics, so adjusting digest was a way of ensuring that our topics should have relatively low noise.

Is bpo safe for fork choice? Yes - we’re only validating gossip, if we’re wrong  (too low) then we wont pass the gossip to our execution layer and we’ll drop off chain, but we’d also not see it because of the digest mismatch.

is BPO safe from a perspective of sync? I can’t see why it’d change anything here, we can sync across fork boundary now.

Why not roll fork version? - we had the context we needed to make a unique digest which is why we changed [compute_fork_digest](https://jtraglia.github.io/eth-spec-viewer/#functions-compute_fork_digest) in the way we did. by rolling in epoch and blobs into the digest, its basically the same as changing fork version, in that it changes gossip topics at the right time.

Basically we’ve implemented a fork, without the full backing of a fork, and it got complicated but was preferred by some CL (iirc). It has the same requirements for upgrade etc, and you’d lose the network peers if you don’t upgrade - its a fork.

---

**etan-status** (2025-08-21):

> I can’t see why it’d change anything here, we can sync across fork boundary now.

A regular fork boundary ensures that there is only a single gossip topic at any given time where valid data can be exchanged. This is different from BPO forks, where traffic from additional network partitions can also be valid, despite being withhold from the local view.

> by rolling in epoch and blobs into the digest, its basically the same as changing fork version

No, it is not the same, as traffic from other network partitions remains valid, if only the forkdigest is bumped.

> and you’d lose the network peers if you don’t upgrade

The tricky part about the fork transition is that Ethereum PoS is based around 2/3 honest majority. If 1/3 don’t upgrade / are malicious, and gets the first couple slots after a fork (low probability but not practically impossible), that’s where the tricky situation may show up.

Misconfigured / malicious / buggy peer may re-broadcast data from one topic to another, maybe selectively publishing only partial blobs / blocks on the other network, but crucially being the only data source on the other network partition for a large chunk of data could impact peer scoring. Also, they can selectively reveal blocks to some of the validators to trick them into attesting to the other partition, without the data being widely circulated on the validator’s primary partition.

I don’t have the capacity to run a proper study here, to see the worst impact that a 1/3 minority in a somewhat privileged network partition may have here, as in, with the ability to trick honest members from the 2/3 majority to attest to their chain as well, possibly justifying it. I do recall the [split view / justification withholding](https://notes.ethereum.org/@djrtwo/2023-fork-choice-reorg-disclosure) stuff from 2023. However, that was applicable more broadly, while my concerns here only apply to the initial 1-2 epochs of the fork.

> When they were initially proposed, it was because forks for some clients(iirc) were ‘expensive’ if we’re just updating one field.

If the shipped clients already support a future scheduled but not yet activated BPO configuration, one could just fast forward and apply that config from the getgo…

And otherwise, if the clients don’t yet support a future BPO config (but already schedule it), and further software updates are needed to support them, the fork is no longer “just updating one field” but involves more sophisticated work…

> In hindsight i’d just go for a fork and take the overheads

Could still be done. Like, just don’t schedule any BPO with Fulu, and ship BPO1/2/3 as proper forks (possibly in the same release) with:

1. ForkVersion (to invalidate traffic from other network partitions)
2. Eth-Consensus-Version name (beacon-API)
3. The new blob config
4. Performance enhancement to support the new blob config

Ultimately, the focus should be on the potential security impact.

- Either it is an issue that needs addressing (in that case, just don’t initially schedule BPO and fix it later),
- Or it isn’t  an issue (proven by mathematical / technically backed reasoning) and just go as originally planned.
- Or it is conditional and a theoretical issue if there actually would be 1/3 malicious/misconfigured/buggy peers, but there is strong practical evidence that around the scheduled fork activations, it is not a realistic scenario on Mainnet. Essentially accepting the lower security level around BPO activations.

At the very least, the EIP should acknowledge the security discussion: [EIP-7892: Blob Parameter Only Hardforks](https://eips.ethereum.org/EIPS/eip-7892#security-considerations)

---

**SamWilsn** (2025-10-07):

Coming in during last call to make a tiny meaningless change: [Give Blob Parameter Only Hardforks more human names by SamWilsn · Pull Request #10490 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/10490) ![:tada:](https://ethereum-magicians.org/images/emoji/twitter/tada.png?v=12)

