---
source: ethresearch
topic_id: 8749
title: A pre-consensus mechanism to secure instant finality and long interval in zkRollup
author: leohio
date: "2021-02-24"
category: Layer 2
tags: []
url: https://ethresear.ch/t/a-pre-consensus-mechanism-to-secure-instant-finality-and-long-interval-in-zkrollup/8749
views: 11253
likes: 11
posts_count: 11
---

# A pre-consensus mechanism to secure instant finality and long interval in zkRollup

**1) TL;DR** :

This post proposes a pre-consensus mechanism to secure instant finality and reduce verification gas cost, without compromising instant fund exit in zkRollup.

**2) Background & Motivation** :

zkRollup can achieve instant finality by adopting a short enough commitment interval (like 10 min). The trust risk of aggregators in this method is increasing in the length of intervals, while the cost of finalization (=if groth16, verification gas cost is over 200k gas per commit ) is decreasing in the length of intervals.

Let us start from reminding the over 200k gas (= $100 ~ $500 ) of zk’s pairing verification.

This costs aggregators at each interval of zkRollup to verify and finalize the commitment.

This cost cannot be ignored since zkRollup’s commitment interval is short  because instant exit gets finalized with this commitment and instant finality (economic finality, 0 conf) can be allowed as far as the interval is short and a malicious aggregator has little incentives to revert.

It is hard to change this interval even if many transactions can be aggregated with recursive zk and efficient proof calculation systems. Safety will be compromised if the interval is simply lengthened.

Then we need to think how to achieve both of a safe instant finality and a long verification interval in zkRollup.

**3) Approach**:

The aggregator’s running cost stems from the condition that gas cost of zk-verification on contracts are high and interval is short.

Thus we make the verification interval longer without compromising safety and usability.

**3.1) First Step: skipping zk-pairing-verification**

The first thing we can come up with naturally is skipping pairing calculations and introducing simple fraud proof against the commitment.

Aggregators submit proof or anything they need to verify zkRollup commitment to the contract, but does not execute pairing calculation at this moment and skip paying 200k gas. This commitment gets verified after the period passes. Each state in a commitment will be the public input of the next commitment. Some Ether from aggregator needs to be funded as a penalty to incentivise verifiers (=fraud watchers).

`hash(public input, zk-proof-data, last state root, next state root, tx hash, aggregator address)` is the commitment.

The preimages are emitted in events onchain, and this commitment is saved in the contract storage.

This approach has a big advantage.

Instantly, everyone can be a watchtower, who is the equivalent of “verifier” in ORU (Optimistic Rollup) context, without a fullnode or any special setup.

Data accessibility problems do not occur because everything needed to verify or to execute fraud proof is in an event emitted onchain. L2 transaction data and the storage of  its result is not required to have when executing fraud proofs, because such data is already aggregated in zk’s public inputs and proofs.

If a malicious aggregator submitted the malicious merkle root, and abandoned all tx data and merkle tree data, there is no need to set up a fullnode to fraud proof. Just checking the zk-proof data and executing the verify function with pairing are enough to detect such

malicious activities.

However this method has a security problem.

If 51% attack occurs on L1 to make a malicious merkle root rightful, it’s hard to stop it.

As 51% execution cost is increasing in the block length, we need this period long enough to make 51% attack hard. The ideal length of one period will be 7 days because of just the same reason that ORU’s exit period is 7 days which can be calculated from the mining cost and then realistic attack incentive.

With this condition, there’s no reason to avoid ORU and use this solution.

**3.2) Second Step:  pre-consensus commitment without zk-verification , finalize with recursive zk’s  pairing**

We can overcome the aforementioned security issue in the following way.

We treat the commitment without zk-verification as pre-consensus which restricts the finality with zk-verification.

`(consensus commit ) => (pre-consensus commit ) => (pre-consensus commit ) => …. =>  (pre-consensus commit ) => (consensus commit )`

All of pre-consensus commitments restrict the consensus with pairing. So L2 users can have safe instant finalities of their transactions. The consensus commitment needs to be verified with all pre-consensus commitment with recursive zk. There are 2 circuits: pre-consensus circuit and recursive circuit. Pre-consensus circuit contains the logic of the dapp which is zkRolluped. Recursive circuit only has to get  pre-consensus data in L1 as public inputs.

Pre-consensus can be merged horizontally over the time period by recursive zk: At the same time recursive zk can also be used vertically for mass transaction aggregation to a  pre-consensus commitment.

If any fraud pre-consensus commitment disturbs the consensus verification with pairing, this is always able to be fraud proven by zk-pairing mathematically. Once this fraud is proven, an aggregator removes this with the zk-verifier-function, and restarts the aggregating and pre-consensus committing.

Fund holders can exit whenever they make the consensus from pre-consensus with 200k gas if they are in haste. (Of course they can also wait for the consensus by aggregators).  As mentioned in the “first step”, they don’t need any special setup to make the finality of the consensus, because all inputs are already aggregated and these can be searched with onchain events. The gas cost of this recursive verification does not increase no matter how many proofs of precommitments are verified because they will be hashed to the entry hash.

51% attackers cannot finalize a malicious merkle root simply because every root should finally have the verification onchain by a logic of contract codes implemented by zk-circuit.

**4) Conclusion**:

This pre-consensus protocol with fraud proof and its relevant data accessibility allows zkRollup to have a long interval commitment (like 6 hours). This approach saves a lot of gas costs of verification calculation.

## Replies

**vbuterin** (2021-02-24):

Can I simplify the core idea here by saying that the idea is that you basically have an optimistic rollup, except one of every N (eg. N = 20) batches contains a ZK proof that proves all N batches since the previous ZK proof? So the system would still have a total safety guarantee if you wait for N batches, but if you want to wait for only a single batch you could still do so, and get optimistic-rollup-level guarantees. The benefit is that the intermediate batches would only cost ~30k gas (transaction base cost + 1 storage write) and only every Nth batch would cost the full 400k+ (or whatever) full gas cost of verifying a ZKP, so you could publish the intermediate batches much more regularly.

It’s not *exactly* instant then, right? Because you do still need to wait for the next batch to get committed into a block, which takes at least one block interval.

---

**leohio** (2021-02-25):

> Can I simplify the core idea here by saying that the idea is that you basically have an optimistic rollup, except one of every N (eg. N = 20) batches contains a ZK proof that proves all N batches since the previous ZK proof?

Yes.

If you think this is Optimistic rollup with zk rather than zkRollup with fraud proof, the following points are the advantages in comparison with Optimistic.

1. waiting period for exit is short (like 6 hours)

In addition, users can exit whenever they want with “400k+ (or whatever) full gas cost”

1. much easier to be a “verifier”

In Optimistic rollup, you have to make sure your tx is finalized in a mathematical safety, you need all transactions since the network started to reconstruct the state and make sure the commitment includes your tx never be fraud proven.

In this method, you just need the last finalized commitment and serial commitments and proofs which are obvious onchain. Maybe even browser JS code can do this whole  verification.

> and get optimistic-rollup-level guarantees.

So I don’t think this is “optimictic-rollup-level guarantees”. The finality will be obvious with a light mathematical verification process without any help from L2 storage holders.

> It’s not  exactly  instant then, right? Because you do still need to wait for the next batch to get committed into a block, which takes at least one block interval.

Right. The finality should be in a pre-consensus (batch), then the batch commitment interval is the maximum length of the unsafe period. I think this cheap batch enables projects to have a shorter interval of effective finality for their users as well, then it’ll be more secure than that with a normal interval.

---

**leohio** (2021-02-25):

> The benefit is that the intermediate batches would only cost ~30k gas (transaction base cost + 1 storage write) and only every Nth batch would cost the full 400k+ (or whatever) full gas cost of verifying a ZKP, so you could publish the intermediate batches much more regularly.

Yes. The benefit from the reduced gas cost is exactly this, excepting that

(call data of transactions & proof) will be added to (transaction base cost + 1 storage write)

---

**adlerjohn** (2021-02-25):

Interesting approach!

One nit:

![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png) leohio:

> In Optimistic rollup, […] you need all transactions since the network started to reconstruct the state

You need this with ZK rollups as well.

---

**leohio** (2021-02-25):

> Interesting approach!

Thank you.

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> One nit:
>
>
>
>
>  leohio:
>
>
> In Optimistic rollup, […] you need all transactions since the network started to reconstruct the state

You need this with ZK rollups as well.

That sentence is about foreseeing the effective finality which is not systematically finalized yet but mathematically not going to be fraud proven.

Maybe you are talking about making a proof and commit finalized with verification with zkRollup, aren’t you?

Of cource, aggregators need to have all tx data to make a proof in ZK rollup since the storage is needed to know to make a proof. But no one need to know the txs and the  storage to judge a commit is valid in zkRollup, because no commit is invalid in zkRollup.

“verifier” is a particular word in Optimistic rollup context

https://research.paradigm.xyz/rollups

---

**adlerjohn** (2021-02-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png) leohio:

> But no one need to know the txs […] to judge a commit is valid in zkRollup, because no commit is invalid in zkRollup.

This is not strictly true. A new ZK rollup block is invalid without data availability, which requires whoever is using the ZK rollup to know the data is available. Simply verifying the ZKP off-chain is insufficient to be sure the ZK rollup actually progressed. Assuming a majority of Ethereum miners are honest and that no light-client proof from Ethereum is invalid, you can proof that an event log happened on Ethereum (e.g. a commit was made along with some data being made available), but this assumes a majority of miners are honest. Which is strictly stronger assumption that ORUs make. If you don’t want to make that assumption, you need to make sure the data is available (on Ethereum this requires running an Ethereum full node which involves downloading all block data) *as* you verify the ZKP.

![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png) leohio:

> “verifier” is a particular word in Optimistic rollup context

Not really. When I [created the optimistic rollup design paradigm](https://ethresear.ch/t/minimal-viable-merged-consensus/5617), I did not include the notion of a distinct third-party with powerful compute that must be relied on to verify anything. Everything can be done with full nodes for the rollup, just like we do it at L1. No one calls full nodes “verifiers.” Even when [introducing incentivized third-parties](https://ethresear.ch/t/trustless-two-way-bridges-with-side-chains-by-halting/5728) and analyzing their incentives and guarantees, there is no distinct “verifier” (i.e. someone that verifies and maybe has some incentives). Rather, it’s “liquidity providers” (i.e. someone that is doing something *and also* verifies).

---

**leohio** (2021-02-25):

> This is not strictly true.  […] Assuming a majority of Ethereum miners are honest and that no light-client proof from Ethereum is invalid, you can proof that an event log happened on Ethereum (e.g. a commit was made along with some data being made available), but this assumes a majority of miners are honest. Which is strictly stronger assumption that ORUs make.

Finally I got your point!

At that assumption level about security, we can say we need have txs to judge wether or not a commitment is valid  in zkRollup.

---

**SergioDemianLerner** (2021-03-01):

I think the idea is a very good one.

What is interesting is that it doesn’t require censorship resistant L1 for soundness (only to avoid selective user censorship).

It doesn’t need a limited interval for fraud proofs.

Let’s say the “operator” submits an invalid ZK proof for a pre-commit batch. And let’s say every 20 pre-commits there is a consensus commit. Clearly the operator won’t be able to submit a valid commit phase ever, because that requires correctly verifying the invalid pre-commit proof.

Therefore the system will halt, and there is plenty of (infinite) time to submit the fraud proof. This solution is much closer to a ZK-rollup than to an ORU.

right?

---

**leohio** (2021-03-02):

Yes, what you said is correct.

![](https://ethresear.ch/user_avatar/ethresear.ch/sergiodemianlerner/48/1059_2.png) SergioDemianLerner:

> This solution is much closer to a ZK-rollup than to an ORU.

This is simply because pre-commit(pre-consensus) can not be used for any malicious activity, this is just a promise which restricting the commit of the finality and securing intermediate processes in zkRollup.

![](https://ethresear.ch/user_avatar/ethresear.ch/sergiodemianlerner/48/1059_2.png) SergioDemianLerner:

> What is interesting is that it doesn’t require censorship resistant L1 for soundness (only to avoid selective user censorship).

It is interesting that zk’s restrictions can be used for this without actual verifying execution at every interval.

Thank you for the good summary.

---

**leohio** (2022-07-31):

There were questions about OPLabs’s ([x.com](https://twitter.com/OPLabsPBC)) idea related to this post, then I thought I needed to note the difference.

[x.com](https://twitter.com/VitalikButerin/status/1553342590786813952)

> Hybrid idea: optimistic + ZK, governance only adjudicates bugs between the two
>
>
> Publish block
> Wait 24h for fraud challenges.
> 3a. If no challenge, publish ZK SNARK, finalize.
> 3b. If there is a challenge, decide based on 2-of-3 of (challenge game, ZK SNARK, governance)

https://twitter.com/kelvinfichter/status/1553323194500763649

> But there’s no reason why Bedrock can’t use a ZK proof System instead ! We think Optimistic Rollups currently have massive advantages over their ZK counterparts, but Bedrock has been designed to make a seamless transition between Optimistic and ZK possible.

The difference is basically limited, and the main difference is the timing of publishing a zkp proof.

It seems that the number of ranks of fraud-proof is also different.

https://twitter.com/VitalikButerin/status/1553342970924974082

> Reducing fraud proof time to 24h is safe because an attack would require both blocking challenges for 24h and breaking one of the three resolution mechanisms.

The key concept is here, and this was what this post originally aimed to publish.

Of course, you can set the length to 6 hours/12 hours/etc, whatever you want.

In the ORU context, you can shorten the 7 days waiting period to a few hours with this.

In the zkRollup context, you can separate the waiting period from the L2 finality period and reduce a lot of gas costs by skipping verification executions.

I’m glad and so excited to see the research on pre-consensus schemes is developing further with the wisest ppl.

