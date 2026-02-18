---
source: ethresearch
topic_id: 571
title: Double-batched Merkle log accumulator
author: JustinDrake
date: "2018-01-10"
category: Sharding
tags: [stateless, accumulators]
url: https://ethresear.ch/t/double-batched-merkle-log-accumulator/571
views: 11723
likes: 22
posts_count: 13
---

# Double-batched Merkle log accumulator

For context see:

1. History, state, and asynchronous accumulators in the stateless model
2. A cryptoeconomic accumulator for state-minimised contracts
3. Batching and cyclic partitioning of logs

**TLDR**: We describe a log accumulator with two layers of batching, significantly improving the concrete efficiency of Merkle Mountain Ranges (MMRs) and multi-MMRs (3MRs). The construction has all-round exceptional concreteness, potentially making it an ideal log accumulator for Ethereum stateless clients. In particular witnesses are only ever updated *once*.

**Construction**

Every shard is endowed with two buffers storing 32-byte hashes:

1. Bottom buffer: Fixed size with 2^n entries labelled 0, 1, ..., 2^n - 1
2. Top buffer: Variable size increasing linearly with collation height

Log accumulation is done as follows:

1. The logs produced in the collation with height i are batched into a Merkle tree with the log batch root placed in the bottom buffer with entry labelled i modulo 2^n.
2. When the last entry in the bottom buffer is updated the bottom buffer is itself batched into a Merkle tree with the root appended to the top buffer.

Notice that log witnesses only ever get updated once when the bottom buffer reaches its last entry. We call the initial witness upon log creation (the log batch Merkle path) the “pre-witness”. We call the final witness created by concatenating the pre-witness with bottom buffer Merkle path (n hashes) the “permanent witness”.

The size of the accumulator is 32*(2^n + h/2^n) bytes where h is the collation height. For concreteness we set the collation interval to 8 seconds and we set n = 13. The bottom buffer has fixed size 250kB. The top buffer grows linearly, but will take *51 years* to reach 750kB. So for all practical purposes, the accumulator can be considered to have size < 1MB.

Because we now have a concept of permanent witnesses, these can be safely stored (e.g. in cold storage) alongside private keys and left unattended arbitrarily long. Note that it is actually sufficient to store the pre-witness because the bottom buffer Merkle path can be reconstructed by SPV clients if log batch roots (one per collation) are placed in collation headers.

Notice also that this accumulator is dead-simple to reason about and implement, and induces marginal storage and CPU overhead for fully validating nodes.

**Conclusion**

We may have found the ultimate log accumulator for Ethereum! It delivers single-update witnesses (at deterministic time, within 2^n*8 seconds = 18 hours) and SPV recovery from pre-witnesses. It has a low complexity spec and implementation, and introduces marginal overheads for fully validating nodes.

## Replies

**Robert** (2018-01-11):

Very interesting suggestion!

I have a question though. How does the scheme guarantee that a “permament witness” always testifies about the most recent state of a key/value pair?

Will a permament witness (i.e. the Merkle path for a bottom buffer state root) still be considered valid if other bottom buffer state roots get appended to the top buffer later on which may change the value witnessed by our existing permanent witness?

In other words: Can a permament witness become outdated if the state of the corresponding key gets changed later on?

---

**JustinDrake** (2018-01-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/robert/48/4499_2.png) Robert:

> How does the scheme guarantee that a “permament witness” always testifies about the most recent state of a key/value pair?

The scheme does not deal with state. The accumulator is designed for append-only logs (i.e. history objects).

It turns out there are several generic ways to design dapps that are state-minimised and history-maximised. See one approach [here](https://ethresear.ch/t/a-cryptoeconomic-accumulator-for-state-minimised-contracts/385). I’ll be posting an alternative approach shortly.

---

**Robert** (2018-01-16):

> The scheme does not deal with state. The accumulator is designed for append-only logs (i.e. history objects).

> It turns out there are several generic ways to design dapps that are state-minimised and history-maximised. See one approach here. I’ll be posting an alternative approach shortly.

Thanks, I now realize that you are trying to push the state into the history. I’m excited to know more about your alternative approach.

> One generic approach I suggested in the original post is to use SNARKs/STARKs to reduce the amount of data that needs to be put trie to just 32 bytes (the size of a hash). The problem with this approach is that we still have one trie update per transaction, so the number of trie updates is linear in the number of transactions.

Is the number of trie updates a real bottleneck in Ethereum? Do you happen to know which fraction of the total computations per transaction/block is used for updating the trie by rehashing the leaves?

---

**JustinDrake** (2018-01-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/robert/48/4499_2.png) Robert:

> I’m excited to know more about your alternative approach.

See the post on [state-minimised executions](https://ethresear.ch/t/state-minimised-executions/748).

![](https://ethresear.ch/user_avatar/ethresear.ch/robert/48/4499_2.png) Robert:

> Is the number of trie updates a real bottleneck in Ethereum?

My understanding is that currently trie updates are a real bottleneck in Ethereum because disk I/O is a bottleneck. Once we move to stateless clients I/O will not be a bottleneck. However, trie updates in the stateless model have a new cost, namely witnesses need to be constructed by the user, communicated to the validators, and updated by the validators. With logs, you can do away with these costs (see [state-minimised executions](https://ethresear.ch/t/state-minimised-executions/748)).

![](https://ethresear.ch/user_avatar/ethresear.ch/robert/48/4499_2.png) Robert:

> Do you happen to know which fraction of the total computations per transaction/block is used for updating the trie by rehashing the leaves?

I don’t know. My guess is that computation is marginal, instead disk I/O being the bottleneck.

---

**tawarien** (2018-02-21):

After reading up and thinking a bit about this accumulator scheme I realized that their may be a potential for even further optimization here, but it would need some investigation into different cryptographic accumulators to find the best suited one.

This scheme has the advantage that the update from pre-witness to witness happens  rarely, deterministic-ally and only once (per Bottom buffer). This means the properties required for the used accumulators are not that high. It can be a static one (one without Add and Remove functionality and thus no Witness update). The generation of the accumulator and the initial witnesses is allowed to be a bit more expensive (as it is done rarely and only once per Bottom buffer).

Instead of using a Merkle Tree for accumulating the bottom buffer other algorithms can be used that would have a constant witness size (which one would need investigation). this could reduce the witness size and depending on the algorithm its verification time even further.

The same accumulator could theoretically be used to accumulate the logs in a collation but if used here it has higher requirements in respect to performance as this is done a lot more often and has a higher impact on block creation but the property that it could be a static one still holds.

---

**JustinDrake** (2018-02-21):

> Instead of using a Merkle Tree for accumulating the bottom buffer other algorithms can be used that would have a constant witness size

Constant size witnesses is definitely something that would be awesome. There are schemes with constant-sized witnesses, e.g. RSA accumulators (see my [first ethresear.ch post](https://ethresear.ch/t/accumulators-scalability-of-utxo-blockchains-and-data-availability/176), and see below). There are downsides to RSA accumulators:

1. They have a backdoor (namely, the RSA modulus N)
2. They make strong-ish cryptographic assumptions
3. They use crypto that is not post-quantum secure

Vitalik’s opinion (and mine) is that, any of the above three criteria makes an accumulator scheme “fancy”, unsuitable for the protocol layer of Ethereum. I’ve spent a lot of time studying accumulator literature, and unfortunately all non-Merkle accumulators I could find (RSA-based, pairing-based, Euclidian ring-based) are fancy.

Nonetheless developers can make use of these accumulators at the application layer and so still benefit from their power. This is especially relevant in custom execution models (see [point 3 here](https://ethresear.ch/t/history-state-and-asynchronous-accumulators-in-the-stateless-model/287/9)). Below are the two constant-sized witness schemes for applications that I’m most excited about.

**RSA accumulators**

The most important thing that needs to be dealt with is picking the RSA modulus, and I only know of three approaches that may be suitable for decentralised applications:

1. Do a multi-party computation with many players (e.g. 100), hoping that at least two properly destroy their prime.
2. Build a super large random number from smaller random numbers, filter out small prime factors, and make a statistical analysis on the strength of the resulting RSA modulus.
3. Pick RSA-2048 from the RSA challenge as your modulus. A $200,000 bounty was posted 27 years ago for the factorisation of this number. Zcoin makes use of this modulus, which probably increases the bounty to a few tens of millions of dollars.

Unfortunately 1) and 2) are unpractical because the bit-size of the modulus would be too large. This leaves us with RSA-2048. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) The size of the witness would be on the order of the bit-size of the modulus, i.e. 64 bytes.

**SNARK-compressed Merkle paths**

This is preliminary research with Jacob Eberhard. I’ll share some initial results because they are very promising. The basic idea is that you can take a Merkle path (or even better, [many Merkle paths with batching](https://ethresear.ch/t/detailed-analysis-of-stateless-client-witness-size-and-gains-from-batching-and-multi-state-roots/862)) and compress all the hashes into a single SNARK. Below is the setup of our test, and the numbers that came out:

Setup:

- Prover is given 64 hashes (SHA256 compression function) to subsume into a single SNARK
- Prover has 2GB of RAM, 2 cores

Results:

- The SNARK has size 127 bytes (using Groth’s three point SNARK)
- Prover time is 5 seconds

From a verification perspective, Groth’s three point SNARK requires only 1 pairing check, compared to the 3 pairing check currently used e.g. in Zcash. Additionally, my understanding is that the SNARK library in Ethereum clients can be replaced by one which is about 10 times faster. I *think* verifying a SNARK currently costs 1.8M gas, so with the above 30x savings this may go down to 60K gas for verifying a SNARK.

But then again, we can use custom execution models where the cost of “execution” is just the cost of real-time data availability, namely 68 gas per non-zero byte of transaction data. So with a custom execution model, you only have to pay ~127*68 = 8,636 gas to “verify” a SNARK.

---

**vbuterin** (2018-02-21):

I talked to Dan Boneh a few weeks ago and he said that he knew of a hidden-order group (which is what all of these RSA constructions really need) with no trapdoor based on class groups. I don’t know the details though and I personally don’t know anything about class groups beyond that they have something to do with how easy it is to find non-unique factorizations in various rings of the form Z[sqrt(x)].

---

**skilesare** (2018-02-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Notice also that this accumulator is dead-simple to reason about and implement

Humor me here…say this isn’t dead-simple for me to reason about.  Where could I find a picture of how this works broken down by steps.  ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

My goal here would be to try to implement one so that I can get better at reasoning about it.

---

**JustinDrake** (2018-02-21):

See code [here](https://ethresear.ch/t/a-cryptoeconomic-accumulator-for-state-minimised-contracts/385/7).

---

**tawarien** (2018-02-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> SNARK-compressed Merkle paths

That sounds promising, I did not know that SNARK where already that advanced the size and time constraints of his proof are very promising.

Would you be so kind and as soon as it is published post a link to the paper? I would be really interested in the results

---

**jamesray1** (2018-04-22):

What does SPV stand for?

---

**JustinDrake** (2018-04-22):

It’s Bitcoin terminology meaning “Simple Payment Verification”. In the post by “SPV client” I mean one that stores the header chain and not much more.

