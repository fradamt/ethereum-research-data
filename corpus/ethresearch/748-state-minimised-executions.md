---
source: ethresearch
topic_id: 748
title: State-minimised executions
author: JustinDrake
date: "2018-01-17"
category: Sharding
tags: [stateless]
url: https://ethresear.ch/t/state-minimised-executions/748
views: 9443
likes: 5
posts_count: 27
---

# State-minimised executions

This post is a continuation of a series on stateless clients and log accumulators. For context see:

1. History, state, and asynchronous accumulators in the stateless model
2. A cryptoeconomic accumulator for state-minimised contracts
3. Batching and cyclic partitioning of logs
4. Double-batched Merkle log accumulator
5. Log shards and EMV abstraction

**TLDR**: We detail a cryptoeconomic mechanism for EMV executions with sublinear use of the state trie. It is an alternative to [cryptoeconomic accumulators](https://ethresear.ch/t/a-cryptoeconomic-accumulator-for-state-minimised-contracts/385) with the benefit that users do not need to post collateral, and only have to push logs (the cheapest kind of onchain activity).

**Construction**

Given a “normal” stateful contract `C` we construct a state-minimised equivalent contract `C’`. The contract `C’` has a “virtual state” maintained as follows:

- The contract stores a single confirmed virtual state root at a corresponding collation height.
- Users can push logs of the form [LOG T], called “virtual transactions”. (Log shards are an ideal substrate for such logs, providing cheap log ordering, friendly witnesses, and real-time data availability.)
- Virtual state transitions for C’ given a virtual transaction [LOG T] happen like state transitions for C given a transaction T.
- Collaterised “executors” can suggest unconfirmed virtual state roots at more recent collation heights than the current confirmed virtual state.
- Whistleblowers can challenge unconfirmed virtual state roots and engage in a TrueBit-style protocol with executors.
- Whistleblowers earn a share of the collateral of adversarial executors.
- Non-adversarial executors advance the virtual state root and are rewarded with an internal fee system that mimics coinbase rewards and/or gas.

**Conclusion**

The construction takes the traditional notion of a transaction and decouples data availability (via logs on log shards) and validity (via TrueBit-style cryptoeconomic execution). The end result is a state-minimised execution protocol where the cost of validation is pushed away from (onchain) validators onto (offchain) executors.

Note also that transactions corresponding to virtual transactions can assume a stateful model for executors (as opposed to a stateless model), so virtual transactions do *not* need to includes witnesses. In such a setup users get both short transactions (improving upon the standard stateless model) and cheap transactions with logs (improving upon standard execution).

## Replies

**stri8ed** (2018-01-17):

How would lite clients work in such a model?

---

**JustinDrake** (2018-01-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/stri8ed/48/1493_2.png) stri8ed:

> How would lite clients work in such a model?

A light client would do the following steps:

- sync up to the header chain of the chain/shard containing C'
- query validators for the confirmed virtual state root of C'
- query executors (acting as fully validating nodes for C') for the virtual state of C' corresponding to the confirmed virtual state root

---

**stri8ed** (2018-01-17):

So validity of a transaction would no longer be “confirmed” when it’s mined, it would need to wait till updated virtual state is committed?

How would another contract know if an internal transaction to C’ was executed successfully?

---

**JustinDrake** (2018-01-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/stri8ed/48/1493_2.png) stri8ed:

> So validity of a transaction would no longer be “confirmed” when it’s mined, it would need to wait till updated virtual state is committed?

Yes.

![](https://ethresear.ch/user_avatar/ethresear.ch/stri8ed/48/1493_2.png) stri8ed:

> How would another contract know if an internal transaction to C’ was executed successfully?

A virtual transaction of `C'` (a log) was executed successfully when the collation/block height corresponding to the confirmed virtual state root is greater than the height of the collation/block containing the virtual transaction.

---

**stri8ed** (2018-01-17):

How can the contract be certain it’s transaction has actually been included in latest virtual state of C’, as opposed to simply being ignored due to invalidity?

---

**JustinDrake** (2018-01-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/stri8ed/48/1493_2.png) stri8ed:

> How can the contract be certain it’s transaction has actually been included in latest virtual state of C’, as opposed to simply being ignored due to invalidity?

I see—How does one distinguish no-ops from transactions that actually change state? One idea is to require that the virtual state root be accompanied by a transaction trie root (similar to today’s Ethereum block headers). Then it’s just a matter of asking an executor for a membership or non-membership witness for the transaction in the transaction trie.

---

**jannikluhn** (2018-01-19):

What confirms unconfirmed virtual state roots? Some passage of time without successful challenges?

---

**JustinDrake** (2018-01-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> What confirms unconfirmed virtual state roots? Some passage of time without successful challenges?

In the proposed scheme, yes.

An alternative scheme is to confirm unconfirmed virtual state roots with SNARKs/STARKs. That would have the advantage that the “passage of time without successful challenges” part can be skipped.

---

**cdetrio** (2018-02-01):

This has been a fantastic series, I’ve followed closely for the most part but having difficulty with this one.

How do the executors work here?

If executors are stateful then aren’t we back to the same problems that motivate stateless clients (e.g. rotation of executors among shards when each shard state is huge/ever-increasing)?

I really like the idea of a “virtual state root”, though I also imagine the shard executors being stateless, either the standard merkle trie and witnesses, or (much butter imo) via cryptoeconomic accumulators. It sounds like the virtual state serves to reassign the job of state maintenance from validators to a new role (executors). Then virtual state is an additional gadget to combine with a cryptoeconomic accumulator, rather than an alternative to replace it. I’ll try to explain the Construction as I understand it, glossing over blanks or filling them with best guesses.

- Old model: Validators read the stream of transactions, and execute them by reading current state from a state root (and witnesses, in a stateless client). In other words, Validators do everything, including calculate the state roots. The Collation body has a transaction list and witness list. The witnesses are rather large, supplying leaves for all accessed state.
- New model: Validators only read the stream of transactions (“virtual transactions”), in the form of an ordered list of logs and log witnesses and a log accumulator (hand-wave). Validators normally do not execute transactions and do not calculate state roots, but they do write the state roots that are submitted by executors (“virtual state roots”). Executors execute transactions; they read the current state (from witnesses if stateless), calculate the new state root, and submit it to the Validators. When an adversarial Executor submits an incorrect state root, a whistleblower initiates a challenge, which is then adjudicated by the Validators. During the challenge, Executors provide the state reads (i.e. witnesses for state roots, including intermediate state roots) to the Validators. After the challenge period has passed, the state root becomes finalized/confirmed. Under normal periods (with no challenges), collation bodies are much smaller as they only contain virtual transaction logs and not the witnesses for accessed state.

So in the new model, Validators only validate the data availability of transaction logs (under normal periods without challenges). The job of transaction execution is shifted to Executors.

Good guesses or wrong? Reemphasizing my first question, it makes sense that “virtual transactions” (ordered list of logs) don’t need witnesses because Validators don’t (normally) execute them. But the choice of stateful or stateless Executors seems orthogonal to the virtual state of a Validator. With Executors that maintain the full state, then users get short transactions (i.e. tx’s without witnesses). But that’s not improving the stateless model, its just reversing the stateless vs stateful tradeoff (bigger tx’s vs pain of an ever-growing state).

---

**JustinDrake** (2018-02-01):

Your descriptions of the “Old model” and “New model” are good! A couple things I probably should have made more explicit:

- The scheme comes in two flavours, with either stateless executors or stateful executors. In either case, validators do not have to execute transactions (other than for adjudication) so there is a gas/CPU saving there. In case the executors are stateful then there is the extra saving that the logs do not have to include witnesses, and so the logs are considerably smaller (maybe around ~5x smaller).
- The scheme is “configurably local”. That is, it can apply to a single contract, to a group of contracts within a single shard, or to a group of contracts across several shards, but not to whole shards. So the job of an executor (to validate transactions, and optionally maintain state in the stateful flavour) is local. Contrast that to the job of validators, which is global across all contracts and shards.

> If executors are stateful then aren’t we back to the same problems that motivate stateless clients (e.g. rotation of executors among shards when each shard state is huge/ever-increasing)?

As noted above, the scheme is local. So an executor for a specific application will *not* rotate among shards. Instead, it will continuously follow the specific shards it is interested in, and filter the logs for only the relevant contracts it has to execute. Stateful executors need to have the setup to deal with the ever-growing state of a particular application, but this shouldn’t be a problem as the state growth is segregated to that single application.

In theory we could enshrine the scheme at the shard protocol level. In this case executors would still be local to a given shard and would not have to rotate among shards.

---

**MaxC** (2018-02-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> be

Without a random rotation of executors, what is to stop them from being bribed?

---

**JustinDrake** (2018-02-02):

> what is to stop them from being bribed?

The only thing executors do is suggest virtual state roots. What kind of bribing attack are you thinking about? Let’s see:

- They could maybe be bribed to not suggest virtual state roots (for slower finality) but this is an open-access model where anyone can become an executor and there are rewards for suggesting virtual state roots (and these rewards grow with the amount of unexecuted logs).
- They could maybe be bribed to suggest invalid state roots (consensus attack) but they stand to lose their entire collateral (anyone can be a whistleblower). Because state roots shown invalid are disregarded, I don’t see any clear benefit for the briber beyond the above bribe (itself not useful).

---

**MaxC** (2018-02-02):

I was mainly thinking about the data availability problem. What is to stop an attacker (large group of validators, together with some normal users and a large group of executors) from creating a state root with all but one transaction valid, but withholding the transactions to create that root from the rest of the network.

Won’t challenging these transactions be very difficult (entailing that the prover send all blocks in the chain to some independent authority)? Whistleblowers would be hard pressed to find the actual transaction that is invalid, if it indeed exists.

---

**MaxC** (2018-02-02):

Impressed with some of your constructions, very creative!

---

**MaxC** (2018-02-02):

See above posts please ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**JustinDrake** (2018-02-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> I was mainly thinking about the data availability problem.

The state-minimised application defines where the logs need to be pushed. A natural choice is simply to push logs in the same shard where the state-minimised application lives, which at a minimum has real-time data availability. As mentioned in the original post, a separate log shard would be an alternative substrate for such logs, providing cheap log ordering and real-time data availability.

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> What is to stop an attacker (large group of validators, together with some normal users and a large group of executors) from creating a state root with all but one transaction valid, but withholding the transactions to create that root from the rest of the network.

The adjudication process only accepts as evidence logs from the log source specified in the state-minimised application. Both (stateful) shards and log shards benefit from real-time data availability, so withholding logs is not an option. Put another way, withheld logs are irrelevant by construction because they necessarily haven’t been pushed onchain. Anyone who wants to be a whistleblower has the opportunity to download all the relevant logs.

---

**vbuterin** (2018-02-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> I was mainly thinking about the data availability problem. What is to stop an attacker (large group of validators, together with some normal users and a large group of executors) from creating a state root with all but one transaction valid, but withholding the transactions to create that root from the rest of the network.

This is indeed why data availability is hard. [@MaxC](/u/maxc), have you seen this post [A note on data availability and erasure coding · ethereum/research Wiki · GitHub](https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding) yet? It’s about erasure-coding blocks to turn a “100% availability” problem into a “50% availability” problem, which then *can* be probabilistically checked, plus some fraud proof mechanisms to ensure the erasure coding is correct.

---

**MaxC** (2018-02-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> yet? It’s about erasure-coding blocks to turn a “100% availability” problem into a “50% availability” problem, which then can be probabilistically checked, plus some fraud proof mechanisms to ensure the erasure coding is correct.

Ah, I hadn’t seen that before-  neat solution. I wonder if it could be made non-interactive.

---

**vbuterin** (2018-02-18):

You can with STARKs - just attack a STARK proving that the erasure code was constructed correctly, and then any client can probabilistically check availability just by randomly sampling a few chunks.

Unless by “non-interactive” you mean “a single proof that convinces everyone”, in which case the answer is no because the block proposer could publish just the proof without ever publishing any of the other data, and the single proof would not have enough data to reconstruct the block. Notice that this argument also applies if there is only one client in the network; so the availability check mechanism relies on at least some minimum number of other (honest) clients existing on the network, though this is an absolute number (eg. “1750 honest clients”), not a percentage (eg. “10% of clients must be honest”).

---

**skilesare** (2018-02-21):

Can we walk through how this would work with an actual contract C’?

Say I have a Token Contract that initializes my virtual root to give the owner the balance 1000000 tokens (see code here [Block Persistent Storage](https://ethresear.ch/t/block-persistent-storage/817/7) for a general ref, I’m actually calculating the roots on each transfer, but with this proposal, we’re going to get rid of that).

So between collations I sent one address 700000 tokens and another address 700000 tokens.  We end up with two logs of type TRANSFER  0xTHEM 700000.

Now I only have 1,000,000 so how do the validators handle this?  The first virtual transaction passes and the second fails?

Question 1: How do they actually calculate that this second virtual transaction should fail?  My contract doesn’t have access to storage so I can’t compare my balance.  In the linked code I require a proof of current balance, but I won’t have that for transaction 2.

Question 2: How do I find out that transaction 2 failed?

Question 3: If someone sends me back 250,000 later, what is there to keep someone from ‘replaying’ my transaction 2 and spending my 700,000 and leaving me with 50,000.


*(6 more replies not shown)*
