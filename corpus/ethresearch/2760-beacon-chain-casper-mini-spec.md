---
source: ethresearch
topic_id: 2760
title: Beacon chain Casper mini-spec
author: vbuterin
date: "2018-07-31"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/beacon-chain-casper-mini-spec/2760
views: 20968
likes: 13
posts_count: 23
---

# Beacon chain Casper mini-spec

The purpose of this document is to give a “mini-spec” for the beacon chain mechanism for the purpose of security analysis, safety proofs and other academic reasoning, separate from relatively irrelevant implementation details.

(Thanks [@josojo](/u/josojo) for edits!)

### Beacon chain stage 1 (no justification, no dynasty changes)

Suppose there is a validator set V = {V_1 ... V_n} (we assume for simplicity that all validators have an equal amount of “stake”). We divide time into six-second-long **slots**; if the genesis timestamp of the system is T_0, then slot i consists of the time period [T_0 + 6i, T_0 + 6(i+1)), and consider each set of 64 adjacent slots to be an “epoch”. For each epoch, we pseudorandomly choose disjoint subsets of V,  S_1 .... S_{64} with |S_i| = \frac{|V|}{64}, where |x| refers to set size (ie. the number of validators, or whatever other kind of object, in x), and within each S_i we select one particular member as the “proposer” for slot i in that epoch.

> Note: if an attacker controls less than \frac{1}{3} of the stake, then if |S_i| \ge 892 there is a less than 2^{-80} chance that the attacker controls more than \frac{1}{2} of S_i, and there is a less than 2^{-100} chance that an attacker controls all 64 indices in a given span i_k .... i_{k+63}. We can assume that it is certain that neither of these things will happen (that is, we can assume there exists a substring of validator indices p_{i_1}, p_{i_2} ... with p_{i_{k+1}} - p_{i_k} < 64 and that every S_i is majority honest).

When (from the point of view of the validator’s local clock) slot i begins, the proposer at slot i is expected to create (“propose”) a block, which contains a pointer to some parent block that they perceive as the “head of the chain”, and includes all of the **attestations** that they know about that have not yet been included into that chain.

After receiving a valid block at slot i, or after waiting for 3 seconds after the start of slot i and not receiving such a valid block, validators in S_{i\ mod\ 64} are expected to determine what they think is the “head of the chain” (if all is well, this will generally be the newly published block), and publish a (signed) attestation, [current\_slot, h], where h is the hash of the head of the chain that they know about, and current\_slot is the current slot number.

The fork choice used is “latest message driven GHOST”. The mechanism is as follows:

1. Set H to equal the genesis block.
2. Let M = [M_1 ... M_n] be the most-recent messages (ie. highest slot number messages) of each validator.
3. Choose the child of H such that the subset of M that attests to either that child or one of its descendants is largest; set H to this child.
4. Repeat (2) until H is a block with no descendants.

Claims:

- Safety: assuming the attacker controls less than \frac{1}{3} of V, and selected the portion of V to control before the validators were randomly sorted, the chain will never revert (ie. once a block is part of the canonical chain, it will be part of the canonical chain forever).
- Incentive-compatibility: assume that there is a reward for including attestations, and for one’s attestation being included in the chain (and this reward is higher if the attestation is included earlier). Proposing blocks and attesting to blocks correctly is incentive-compatible.
- Randomness fairness: in the long run, the attacker cannot gain by manipulating the randomness

### Beacon chain stage 2 (add justification and finalization)

We cluster slots into epochs: Every 64th slot is an epoch\_boundary\_slot and all 63 consecutive slots of an epoch\_boundary\_slot belong to the same epoch. The chain state keeps track of a map \mathit{justified\_hashes}, which starts at \{(0, genesis)\}, and will add new (slot, hash) pairs over time. A valid attestation now references two additional variables: an *epoch boundary hash* (ie. the hash of the highest-slot block in the chain such that floor(\frac{block.slot}{64}) < floor(\frac{attestation.current\_slot}{64})), and a *latest justified hash* (the highest-epoch hash in the justified\_hashes of the block referenced by the epoch boundary hash). Attestations published can be included in the chain, but only if the attestation’s latest justified hash equals the highest-slot hash in \mathit{justified\_hashes}.

Note that because the state of the chain keeps track of the latest justified hash implicitly, all honest validators that vote for the same epoch boundary hash will vote for the same latest justified hash.

At each epoch boundary (ie. when processing a block where floor(\frac{b.slot}{64}) > floor(\frac{b.parent.slot}{64})), the state transition function performs the following steps.

Suppose that in a chain, the most recent epoch boundary blocks are B1, B2, B3, B4 (B4 being the most recent), with the epoch boundary corresponding to B4 having slot B4\_slot (then B3 has slot B3\_slot = B4\_slot - 64, etc). If the chain has accepted attestations from \frac{2}{3} of *all* validators that specify B4 as the epoch boundary block, then it admits (B4\_slot, B4) into \mathit{justified\_hashes}.

That is, an epoch boundary block is “justified” if \frac{2}{3} of *all* validators sign a message whose epoch boundary hash is that block, and the block becoming part of \mathit{justified\_hashes} in some chain means that the block is justified and the information proving that the block is justified has been included in that chain.

In the following three cases, we “finalize” a block:

- If B4 and B3 are in \mathit{justified\_hashes} and the attestations that justified B4 used B3 as the latest justified hash, then we finalize B3.
- If B4, B3 and B2 are in \mathit{justified\_hashes} and the attestations that justified B4 used B2 as the latest justified hash, then we finalize B2.
- If B3, B2 and B1 are in \mathit{justified\_hashes} and the attestations that justified B3 used B1 as the latest justified hash, then we finalize B1.

Note that the algorithm can work if only the first rule exists, but we add the other two rules to satisfy the cases where it takes longer for attestations to get included in the chain.

We change the fork choice rule above so that instead of starting H from the genesis block, it works as follows:

- Set H_F to the highest-slot finalized block.
- Set H_J to the highest-slot block which is justified and the client has known is justified for some time (precisely, if T_F is the time the client learned about the highest-slot finalized block, T_J is the time the client learned about some given justified block, then the client takes that block into account starting at slot T_F + (T_J - T_F) * 3
- Start the fork choice from H_J.

We then add two slashing conditions:

- A validator cannot make two distinct attestations in the same epoch
- A validator cannot make two attestations with epoch boundary slots t1, t2 and justified slots s1, s2 such that s1 < s2 < t2 < t1 and s2 & t2 are consecutive epoch boundary slots.

Claims:

- Safety: once a block becomes finalized, it will always be part of the canonical chain as seen by any node that has downloaded the chain up to the block and the evidence finalizing the block, unless at least a set of validators V_A with |V_A| \ge |V| * \frac{1}{3} violated one of the two slashing conditions (possibly a combination of the two).
- Plausible liveness: given an “honest” validator set V_H with |V_H| \ge |V| * \frac{2}{3}, V_H by itself can always finalize a new block without violating slashing conditions.
- Real liveness: assuming that after some time T network latency < 6 sec, the network will justify blocks, and an attacker with less than \frac{1}{3} of V cannot prevent this.

Arguments for safety and plausible liveness are equivalent to [[1710.09437] Casper the Friendly Finality Gadget](https://arxiv.org/abs/1710.09437). The argument for real liveness is roughly as follows. If no “new justified block” events happen, then the LMD GHOST rule is stable (this is assumed to be already proven) and clients will finalize a new block after 2 epochs (that is, within 3 epochs of any given point in time, as specific points in time could be in the middle of an epoch). The T_F + (T_J - T_F) * 3 rule ensures that “new justified block” events can only take place once every three epochs, so eventually a block will get finalized.

### Beacon chain stage 3: adding dynamic validator sets

Every block B comes with a subset of validators S_B, with the following restrictions:

- Define the dynasty of a block recursively: dynasty(genesis) = 0, generally dynasty(B) = dynasty(parent(B)) except when the processing of B finalizes a block, in which case dynasty(B) = dynasty(parent(B)) + 1.
- Each block B has a local validator set LVS(B). For two blocks in the chain, if B_1 and B_2, dynasty(B_2) - dynasty(B_1) = k, then |LVS(B_1)\ \cap\ LVS(B_2)| \ge LVS(B_1) * (1 - \frac{k}{64}) (and likewise wrt LVS(B_2)). That is, at most \frac{1}{64} of the local validator set changes with each dynasty.

Claims:

- All of the above claims hold, with appropriate replacements of V with LVS(...), except with fault tolerance possibly reduced from \frac{1}{3} to approximatively 30%.

## Replies

**mmelnychuk** (2018-07-31):

Sincere thanks for all the work and for posting this.

Sorry for taking up your time with questions, I know you’re incredibly busy right now.

What value does |V| >= 892 refer to exactly? The number of ETH?

Second, say a large economic force, such as EOS or a hostile political entity, bought enough ETH to violate the 1/3 stake assumption - are there any safeguards to protect against this unlikely but not impossible event?

---

**vbuterin** (2018-07-31):

> Second, say a large economic force, such as EOS or a hostile political entity, bought enough ETH to violate the 1/3 stake assumption - are there any safeguards to protect against this unlikely but not impossible event?

If they get between 1/3 and 1/2, then we can still have some safety conditional on a synchrony assumption. Beyond 1/2, you would need subjective resolution (ie. an honest minority soft-forks the chain and the market chooses that fork).

---

**mmelnychuk** (2018-07-31):

I’m assuming the hostile staker’s eth would be burned on the new chain

---

**vbuterin** (2018-07-31):

Yes, exactly correct.

---

**mmelnychuk** (2018-07-31):

I see what you mean subjective as it could prove to be a (possibly difficult?) social solution to such an attacker spread among multiple small stakes

edit: nvm thought it through more. it would be straightforward. thanks for your responses.

---

**kr8534** (2018-08-02):

Thanks for your continuous work and postings ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Can I get some explanation on `That is, the local validator set only changes by at most 1/60 per dynasty.` or the ethresear.ch post link relevant to it?

Less than other, I could hardly understand where the (1-k/60) and 1/60 comes from…

---

**vbuterin** (2018-08-02):

The other spec currently has validator sets changing by at most 1/15 per dynasty (1/30 added, 1/30 removed); this spec changes that fraction to 60, but it’s ultimately just a number that can be adjusted.

---

**naterush** (2018-08-17):

> Choose the descendant of H such that the highest number of validators attests to H

Do validators break ties with the lowest block hash?

---

**vbuterin** (2018-08-17):

I’d say break ties via client-side randomness. Seems safest in the existing cases where it’s been studied.

---

**unaryunix** (2018-08-20):

Would Vpi mod n always resolve to a single “proposer” for each slot i? If this proposed block is rejected by Si, for whatever reason, what would be the recovery mechanism?

---

**vbuterin** (2018-08-21):

Wait until the next slot?

---

**mratsim** (2018-09-13):

I have ported the network simulator (https://github.com/ethereum/research/blob/master/clock_disparity/ghost_node.py) to Nim (https://github.com/status-im/nim-beacon-chain/tree/master/beacon_chain/fork_choice_rule)

Port is almost 1:1 but with added types which should make it much easier for static languages as a reference implementation.

I have the following comment on the research implementation:

- The parentqueue and processed fields require respectively a heterogeneous list that can contains Blocks or Signatures and a heterogeneous dictionary indexed by either block or signature hashes and containing blocks or signatures.
This requires using type erasure in static languages (either inheritance or tagged unions). I think it would be better to have different fields that separate cleanly blocks and signatures. A dictionary/hashtable that supports indexing hashes of different lengths (one would be a BLS12-384 hash the other a Sha3 hash for example) could be tricky.

Next step is to debug it and then to port it to the v2.1 spec and integrate it in the beacon chain. I would be interested in other implementers thoughts.

---

**kladkogex** (2018-09-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The fork choice used is “recursive maximum attestation”. The mechanism is as follows:
>
>
> Set HH to equal the genesis block.
> Choose the descendant of HH such that the highest number of validators attests to HH (ie. published an attestation where H∈h1…h64H \in {h_1 … h_{64}}).
> Repeat (2) until HH is a block with no descendants

Lets say you the block number 1 (number 0 is genesis). Lets say it is signed by 60 validators out of 64.

If 1000 years from now 64 validator keys get compromised, they can sign an alternative block 1 and totally destroy the chain.  It is impossible to do the same with PoW. Whatever the math is PoS chains are a bit less secure than PoW.

From this perspective,  I think ETH strategy should be different.  Calling PoW chain “legacy” is not optimal. What needs to be said, is that there is PoW main chain, which is very secure but very slow, then there is PoS beacon chain which is ALMOST as secure as PoW but faster (say 100 tps)  and then there are shards, Plasma and other things yet faster but a bit less secure.

The same with Stage 2 and Stage 3 specs.  They are very smart but also complex, so compared to PoW, PoW is more secure just based on simplicity.  When I read the original Bitcoin paper, it is relatively easy for me to see security. When I read Stage 2 and Stage 3 specs the analysis becomes very hard, especially having that not all things are discussed such as interplay of network splits and denial of service attacks.

I do not want to say that Stage 2 and Stage 3 specs are bad. One needs to make a confession that PoS is (a little)  less secure then PoW, so based on this consideration the PoW  main chain needs to survive, it is wrong to call it legacy.  And then one can have the great beacon POS chain, and shards and Plasma and you name it.  Is is a chain of tradeoffs speed vs secuirty.

I understand that the initial idea of Ethereum was to replace PoW with PoS at some point, but this was several years ago, and all the experience learnt since points out that PoS chains are a bit less secure.  IMHO ETH project needs to tweak PoW vs PoS messaging a little bit, otherwise it is heading to an ugly moment where a total switch to PoS will lead to a fork where overwhelmingly all miners will stay with PoW, so after the fork the PoW chain will have more value than the PoS chain.

Another reason which makes a total switch to PoS unfeasible is the brand value.  People hold money in Swiss banks because of time-proven security. Similarly, people hold money on PoW because of time-proven security. 10 years of now, the bulk of money will be on PoW. So Ethereum is really shooting itself in a foot by saying it plans to kill the PoW chain.

---

**snowy13** (2018-09-25):

> If 1000 years from now 64 validator keys get compromised, they can sign an alternative block 1 and totally destroy the chain. It is impossible to do the same with PoW. Whatever the math is PoS chains are a bit less secure than PoW.

How would the current validator set in the proposed Beacon chain running GHOST accept a new genesis state at n block height?

> One needs to make a confession that PoS is (a little) less secure then PoW

Can you please explain in what context it is “a little less secure” and provide a link to research?

---

**vbuterin** (2018-09-25):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> If 1000 years from now 64 validator keys get compromised, they can sign an alternative block 1 and totally destroy the chain. It is impossible to do the same with PoW. Whatever the math is PoS chains are a bit less secure than PoW.

This is why revert limits, and weak subjectivity, are needed: https://ethereum.stackexchange.com/questions/15659/what-is-weak-subjectivity

---

**vbuterin** (2018-09-25):

I’ll also mention that I’ve been lately thinking that pure IMD GHOST is not the best idea because of a different kind of attack, and either switching to LMD or some hybrid may actually work better.

(Credit to Alistair Stewart for pointing out the scenario)

Specifically suppose that this scenario happens:

![image](https://ethresear.ch/uploads/default/original/3X/7/5/75a9063b41bff49635cd9b5dd7693554b90d700c.svg)

An attacker can now arbitrarily flip the fork choice between left and right by publishing a single validator signature to yellow and then green and so on back and forth.

The basic problem here is that there is another stability desideratum that earlier analysis missed: if we define the “extent” by which a fork choice rule favors A over B as the minimum number of validators that would need to collude to make it favor B, then we want the property that if the fork choice favors A over B at one point in time, the extent by which it favors A should naturally increase over time, and start increasing immediately. PoW longest chain, PoW GHOST, and PoS longest chain all have this property; PoS LMD GHOST does also but POS IMD GHOST does not, which is what leads to this issue. Switching to LMD (plus justification-favoring) does solve this.

---

**vbuterin** (2018-10-24):

> What are the known drawbacks of LMD in the context of FFG?

Basically, it’s “unstable” under exceptional cases due to the boundary condition.

Suppose that you have chains A and B, where A wins under LMD, but B got 65 signatures in some previous epoch, then there’s some validator with 2% that has withheld signatures for B; then that validator can cause a reorg to B at any time.

Reasons why this is not a big deal:

- Such a situation itself can only happen in an exceptional circumstance, probably requiring both high network latency and active coordination among many malicious validators; otherwise, how would the fork choice have switched from B to A?
- Even if it does happen, the fork choice should justify something in the A chain fairly quickly; the only case where it doesn’t is the case where >33% of validators are malicious or go offline.

So the range of situations in which this causes problems but outright 51% attacks are not possible is not that wide.

Also note that the worst case is a single reorg, whereas IMD’s failure mode is a large number of reorgs, potentially one per validator.

---

**Alistair** (2018-10-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Even if it does happen, the fork choice should justify something in the A chain fairly quickly; the only case where it doesn’t is the case where >33% of validators are malicious or go offline.

It can be a bit worse that that. If we get into an unlikely (but asynchronously reachable) situation, then there is an attack with less than 1/3 of votes that potentially stops anything from being finalised indefinitely. Suppose that in epochful Casper FFG with LMD on the last justified checkpoint and 10% malicious stake that votes late, we somehow have something like this:

A  - B

30%- 60%

51% - 20%

Here the bad guys are the only missing votes on the first checkpoint. Now the A chain is winning under LMD with 51% of the vote so it will keep getting votes. But the bad guys can justify B and make that the fork choice at any time. What they can do is time things so that A gets around 60% of the vote at the time of the switch. If they pull this off, then B has the last justified checkpoint and is winning, but they have the power to justify A at any time. So they wait for the next checkpoint on B to have 60% of the vote and repeat.

Now actually any fork choice rule that builds on the last justified checkpoint is vulnerable to this kind of attack. If our situation is:

A  -B

30%-70%

60%-30%

30%-60%

Then the bad guys who haven’t voted on the last two checkpoints can force a reorg to A and then later one to B by justifying these checkpoints.

We need to argue that either we never get into this kind of situation or that the timing is hard to pull off repeatedly. Now for epochless FFG, the timing of these kind of attacks can be much easier. If the honest guys in the 1/64 who vote on each block vote faster than a block, then the bad guys can reliably time to within a resolution of 1/64 of the votes. There are a few complications in replicating this attack on epochless FFG, such as the blocks that replace the checkpoints above actually being closer than 64 blocks apart but it should be doable with less than 1/3 of the vote.

So we are stuck for hoping that the set up never happens. I certainly have no idea of a credible attack that would give it.

---

**vbuterin** (2018-10-26):

For either of those setups to be possible, high latency is basically already required. Furthermore, if you can force a (30, 70) (70, 30) situation to happen repeatedly, then that already means that you can prevent justification from happening in two consecutive blocks, which means you can prevent finality indefinitely. FFG never claimed to give guarantees of ability to finalize under such conditions.

That said, it is a very good point that the three-round setup shows that no fork choice rule can prevent scenarios where the attacker can justify the non-canonical chain at any time, as one can construct scenarios where the attacker can justify *either* chain at any time.

It’s certainly an argument in favor of CBC being the right thing long term!

---

**vbuterin** (2018-11-06):

[@Alistair](/u/alistair) I think I found one solution.

First, for simplicity, we move away from epoch-less Casper and move back to epochs. Epoch-less was only an improvement because of IMD-related arguments, and without them it only provides a ~20% gain in finality time at considerable cost in complexity, so it may not even be worthwhile.

Now, here is what we do. Let N be the slot in which a client learns that some chain has been justified at a slot more recent than the current head chain’s last-justified-slot. When the client’s clock hits slot `N + k`, such a chain’s LMD score is bumped up by min(\frac{k}{EPOCH\_LENGTH}, 1).

This allows us to argue as follows. Because on average, the attacker can only flip the winner of the “highest justified epoch” rule once per epoch, eventually there will be a period of one epoch during which the attacker cannot flip the winner. During this period, whatever the chain that was head at the start of the period will have 100% support in the LMD fork choice. Hence, there will be a period of one more epoch until any other chain can take over, and during this period the chain can get justified.

The more general class of solutions here basically has to do with adding some sort of “temporary stickiness” to the LMD fork choice, sticky enough to allow a head to be justified but temporary enough to allow the FFG plausible liveness proofs to still work.


*(2 more replies not shown)*
