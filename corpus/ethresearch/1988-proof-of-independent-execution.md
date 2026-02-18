---
source: ethresearch
topic_id: 1988
title: Proof of independent execution
author: JustinDrake
date: "2018-05-12"
category: Sharding
tags: [execution]
url: https://ethresear.ch/t/proof-of-independent-execution/1988
views: 4369
likes: 5
posts_count: 16
---

# Proof of independent execution

**TLDR**: We suggest a cryptoeconomic gadget in a similar vein to [proof of custody](https://ethresear.ch/t/extending-skin-in-the-game-of-notarization-with-proofs-of-custody/1639) but for execution (as opposed to data availability). It addresses the [validator’s dilemma](https://eprint.iacr.org/2015/702.pdf), outsourcing, self-pooling, and unfair parallelism.

**Construction**

Let E be an executor (e.g. a proposer-executor or a notary-executor) voting on the validity of state roots spanning a given windback. In addition to a signature, votes now require a proof of custody of the execution trace covering the windback.

Specifically, the executor E:

1. Chooses a secret salt s (to be revealed at a later time)
2. Constructs a unique secret \tilde{s} = H(s || a) where a is the executor’s address
3. Splits the execution trace into 32-byte chunks
4. Concatenates every chunk with the unique secret \tilde{s}
5. Merklelises the concatenated chunks
6. Submits the Merkle root (the proof of independent execution) with his vote

When the salt s is revealed the proof becomes publicly verifiable and anyone can challenge a bad proof with a TrueBit-like game. Also the executor E is slashed if the secret \tilde{s} is leaked before the salt s.

Notice that the execution trace and proof are “streamable”. That is, the proof of independent execution can be built as execution happens, without having to store the entire execution trace in memory.

**Discussion**

The above construction addresses the following:

- Validator’s dilemma: An executor can’t do “copycat voting” or “windback skipping” without being liable to slashing.
- Outsourcing: An executor cannot outsource execution without leaking the secret \tilde{s} and being liable to slashing.
- Self-pooling: Two executors controlled by the same owner cannot reuse executions (“one CPU multiple votes”) because of the uniqueness of the secret \tilde{s}.
- Unfair parallelism: An executor with access to “non-mainstream parallelism” (hardware like a 32-core server or FPGAs/ASICs, or software with patented/proprietary parallelism tricks) is still bound by the “inherent sequentiality” of the execution trace layout (which may allow for, say, 4-core parallelism).

## Replies

**vbuterin** (2018-05-12):

Interesting!

The main challenge I can see regarding centralization risk is that this would encourage the creation of hash ASICs, and possibly trusted outsourcing to hash ASICs. I suppose it depends on the ratio of cost between hashing and the execution itself.

---

**JustinDrake** (2018-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I suppose it depends on the ratio of cost between hashing and the execution itself.

Yep. The hashing granularity/density is easily configurable. Also, we can use a hashing function that is significantly faster than SHA256 (see [this benchmark](https://softwareengineering.stackexchange.com/questions/49550/which-hashing-algorithm-is-best-for-uniqueness-and-speed)).

We don’t even need the hash function to be cryptographically strong, as in we don’t really need collision resistance (or even pre-image resistance?).

---

**sinahab** (2018-05-12):

Interesting! I like the lateral thinking – applying proof-of-custody to execution. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Here are some thoughts from a conversation with Jason Teutsch yesterday:

Train of thought #1 – who would take it upon themselves to challenge the Proof of Execution? Presumably others who’ve already done the execution, stored the intermediate states locally, and can now go back to check the executer’s proof.

In sharding, this would be the other executors interpreting the shard data.

In Truebit, this would have to be the solver & challengers involved in a particular task.

This seems tough for multiple reasons: 1) when a verifier executes a WASM task initially, they don’t generate state snapshots since that would be much slower than using a JIT. They only know the state snapshot trace *if* their final solution differs from the one provided by the solver, and a verification game begins; 2) there are only a handful of participants per task (solver and verifiers) so relying on them to challenge seems like an insufficient guarantee; 3) these participants are not well incentivized – they’d have to store large execution traces for tasks in the hopes of catching a lying verifier – and this is costly (given how large programs can be).

Train of thought #2 – context: Truebit is an open-entry system; *anyone* can challenge a piece of computation. Given that final adjudication happens on chain, the presence of one honest verifier per task is sufficient for security (what we’ve called “unanimous consensus”). To incentivize verifiers to check tasks, even though the expectation is that solvers do not make mistakes, we introduced the idea of probabilistic forced errors which result in large jackpot payouts.

An open question: could we use the above Proof of Execution to partially reward verifiers for checking work, without having to rely on the forced error mechanism? Or could we assign verifiers to tasks and require that they submit proofs of execution, lest they get slashed (this would be similar to sharding)? The former seems like an interesting direction. The later seems like it could weaken security (since instead of “one honest verifier per task available  globally”, the requirement would become “one honest verifier of the n assigned to the task”).

There might be something here. We’ll continue to think through it in the context of Truebit.

---

**JustinDrake** (2018-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/sinahab/48/68_2.png) sinahab:

> who would take it upon themselves to challenge the Proof of Execution?

In the case of outsourced execution, the outsourcee is incentivised to “trap” the outsourcer and challenge their own constructed bad proofs of execution to collect the slashing bounty.

Some ideas for non-outsourced scenarios:

1. People who care about doing the execution anyway. Specifically, consider a new full node that is synching up to a shard. It’s “free” (that is, marginally extra work) for that node to check proofs of execution at random as they sync along.
2. People with “free” computation available. Specifically, consider an botnet checking proofs of execution at random during time otherwise idle.
3. The Ethereum “neighbourhood watch”, i.e. volunteers who care about Ethereum and want to weed out bad actors for idealistic reasons.

![](https://ethresear.ch/user_avatar/ethresear.ch/sinahab/48/68_2.png) sinahab:

> we introduced the idea of probabilistic forced errors which result in large jackpot payouts.

Yes forced errors could work well here ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/sinahab/48/68_2.png) sinahab:

> what we’ve called “unanimous consensus”

That’s a cool way to put it! And “unanimous” is powerful because it includes *anyone* including new full nodes, botnets, the neighbourhood watch, professional bounty-hunters, crazy-OCD people, academic researchers studying TrueBit games, etc.

Also notice that, unlike TrueBit, proofs of execution don’t have to be challenged within a fixed challenge period. Instead, the challenge period can remain open while the corresponding validator is registered.

---

**sinahab** (2018-05-13):

Good point re the Proof of Execution being open challenge at later times within sharding, so long as the verifier has deposits.

And I love that breakdown of different people doing verification. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**kladkogex** (2018-05-14):

Interesting ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> We don’t even need the hash function to be cryptographically strong, as in we don’t really need collision resistance (or even pre-image resistance?).

t seems that you do not need to hash the entire hash, in most cases if will probably be enough to take a number of random breakpoints, and sample RAM at these checkpoints. So the data to hash will be a random sample over time and data, which I think could be modest

A medium-size problem that I think you will face is frontrunning

A lazy guy can front run a good guy by submitting the same Merkle root.

Then good guy can fight back by not submitting

the secret seed.  Then the bad guy will not be able to reveal the secret seed, and will at least lose the gas fee he paid for the original submission of the Merkle root.   As a result of this though the good guy will not be able to claim bounty for the validation.

I think you need to think about figuring out fine-tuning cryptoeconomic incentives, including deposits/slashing …

I believe Truebit guys never published a reasonable solution for a similar front running problem they have in the system. so it is still an open question.

---

**JustinDrake** (2018-05-14):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> A lazy guy can front run a good guy by submitting the same Merkle root

The Merkle root is a function of the unique secret \tilde{s} which is specific to a particular address. Submitting the same Merkle root necessarily produces an incorrect proof of independent execution, and will likely cause you to get slashed.

---

**kladkogex** (2018-05-14):

oops - yes I missed the point about the address ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

It makes things much better ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Still outsourcing  seems to be possible (although harder to implement)

One validator can run the computation, and then sell to all other validators customized proofs, customizing the proof for each validator.

In other words, I can run the computation,  and then sell it to 1000 guys at $1 a piece, creating a custom proof for each guy starting from the existing trace and using the guy’s address …

I think one can tweak the algorithm to  use not just the address but the private key of the validator, and then  use signatures instead of hashes.

---

**JustinDrake** (2018-05-14):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> One validator can run the computation, and then sell to all other validators customized proofs, customizing the proof for each validator.

This isn’t really possible for a couple of reasons.

First, untrusted outsourcing is severely disincentivised by the two slashing conditions. Both an incorrect Merkle root and a leaked secret \tilde{s} allows an outsourcee to receive a whitleblower bounty (several orders of magnitude more than $1).

Second, even with access to \tilde{s}, a trusted outsourcee cannot easily customise proofs. This is because reading a cached execution trace from RAM can be made at least as expensive as recomputing the trace just-in-time.

---

**kladkogex** (2018-05-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> When the salt ss is revealed the proof becomes publicly verifiable and anyone can challenge a bad proof with a TrueBit-like game. Also the executor EE is slashed if the secret ~s\tilde{s} is leaked before the salt ss.

It seems when an honest validator reveals the salt s,  Eve can intercept the message, and then front-run it revealing \tilde{s}, and therefore slashing the validator deposit.

---

**JustinDrake** (2018-05-14):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> It seems when an honest validator reveals the salt s, Eve can intercept the message, and then front-run it revealing \tilde{s}

I didn’t make that clear in the original post, but the slashing condition for the leakage of \tilde{s} expires before the period during which s should be revealed starts.

---

**chriseth** (2018-05-14):

I think what you still need is a single (or few) Merkle proofs of random leafs which are determined by the merkle root. If you don’t do that, people can just post random Merkle roots together with the correct result (which they obtained from someone else) and it is very hard to check or there is no big incentive to actually check.

---

**clesaege** (2018-05-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Splits the execution trace into 32-byte chunks
> Concatenates every chunk with the unique secret \tilde{s}

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Self-pooling : Two executors controlled by the same owner cannot reuse executions (“one CPU multiple votes”) because of the uniqueness of the secret \tilde{s}.

I may be missing something, but why couldn’t they do the computation once an then concatenate different secrets?

---

**JustinDrake** (2018-05-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/clesaege/48/533_2.png) clesaege:

> why couldn’t they do the computation once an then concatenate different secrets

On second though I think you’re right! I was originally thinking that re-concatenation of a stored trace with a different secret would be slower than re-execution because execution is streamable, but streamable multi-concatenation is possible.

---

**clesaege** (2018-05-30):

An idea (I let you explore a bit more if it makes sense) would be to use homomorphic encryption and make the computation in the encrypted domain such that the encrypted domain is different for each \tilde{s}.

But it may significantly slow down computation.

