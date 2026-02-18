---
source: ethresearch
topic_id: 1659
title: Cryptoeconomic signature aggregation
author: JustinDrake
date: "2018-04-08"
category: Sharding
tags: [signature-aggregation]
url: https://ethresear.ch/t/cryptoeconomic-signature-aggregation/1659
views: 7338
likes: 13
posts_count: 16
---

# Cryptoeconomic signature aggregation

**TLDR**: We present a signature aggregation scheme intended as a possible alternative to BLS signatures in the context of [committee voting](https://ethresear.ch/t/simple-honest-majority-collation-availability-proof/1205), with applications such as committee-based notorisation and [fork-free sharding](https://ethresear.ch/t/fork-free-sharding/1058).

**Construction**

Let V be a committee of voters v_1, ..., v_n. For a given message m every voter can cast one vote by signing m. For concreteness we set |V| = 423 (as inspired by Dfinity) and require a threshold of t votes (e.g. t = |V|/2) to form a quorum.

Given at least t votes, some collateralised claimer (e.g. an eligible proposer, blockmaker or collator) can aggregate the votes by creating a bitstring B=\{b_i\} of size 423 bits, where b_i=1 represents a claim that v_i signed m, and b_i=0 otherwise. The claimer signs [m, B] to form a signature s. The cryptoeconomic aggregated signature is [m, B, s].

During some challenge period anyone can challenge the claimer to provide the signature of m from v_i if the bit b_i is set to 1. Failure to provide the signature in time slashes half the claimer’s collateral, and rewards the other half to the challenger.

**Discussion**

The overhead of the aggregation scheme is 423 bits (53 bytes). Every voter (e.g. a notary, collator, validator) knows whenever the claimer is reporting a false vote from himself, so it is risk-free for the voter to challenge the claimer.

Compared to BLS signatures, the aggregation scheme does not require a setup phase among the voters. The scheme is also quantum secure if s and the votes (signatures of m) are quantum secure.

## Replies

**jamesray1** (2018-04-08):

Well this provides more details  compared to the bitfield in [A general framework of overhead and finality time in sharding, and a proposal](https://ethresear.ch/t/a-general-framework-of-overhead-and-finality-time-in-sharding-and-a-proposal/1638/3). What are other pros and cons compared to other signature schemes, e.g. performance?

---

**vbuterin** (2018-04-08):

This is different from the bitfield in that post. In that post, all signatures are directly on chain, but each signature serves to notarize many objects (eg. 200) simultaneously; the bitfield’s function is that it’s the protocol that selects which 200 things the notary needs to sign, but the notary may not approve of all 200 of them, so through the bitfield the notary can specify which of the 200 they approve.

Here, the bitfield is a bitfield of which underlying *signatures* are present (as opposed to which underlying *messages* are approved).

---

**JustinDrake** (2018-04-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> this provides more details  compared to the bitfield in A general framework of overhead and finality time in sharding, and a proposal

The bitfields are different. This one is regarding voters and votes (one bit corresponds to a voter, and the knowledge of a vote), whereas the other is regarding proposals (one bit corresponds to a proposal header, and the availability of the proposal body).

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> What are other pros and cons compared to other signature schemes, e.g. performance?

The key goal of aggregation is succinctness, which has been achieved. The main disadvantage is that we have an interactive game so “validating” the aggregated signature takes time. Also, we need an “eligible” claimer to put down collateral and make the claim. The advantages compared to BLS are 1) no setup and 2) quantum secure.

---

**vbuterin** (2018-04-08):

I have a few concerns with actually using this in practice:

- Unless the deposit associated with this signature is extraordinarily large, there will be cases where a signature gets into the main chain despite actually being incorrect. If coupled with a main chain availability failure (eg. censorship), this could lead to a bad collation getting internally finalized more easily.
- The cryptoeconomic signature doesn’t reveal each notary’s auxiliary data for any availability challenge / proof of custody mechanics.

I suppose we could require some kind of secondary committee to sign off on all the cryptoeconomic signatures and attest to their availability, but that does add its own complexity…

---

**kfichter** (2018-04-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Unless the deposit associated with this signature is extraordinarily large, there will be cases where a signature gets into the main chain despite actually being incorrect.

Are there cases where someone benefits if voter v_{x} doesn’t sign off on the proposal but the claimer states that b_{x} = 1? i.e. if b_{x} = 1 is accepted into the root chain then v_{x} has effectively signed off on the proposal by not challenging. I do see a potential problem if only the claimer knows that v_{x} is offline and will not challenge. Otherwise it seems like (as long as deposit covers cost of challenging) it’s economical that v_{x} either challenges or the outcome of the vote is more beneficial than the return of the deposit.

So unlike BLS where an offline voter will always vote “no,” an offline voter in this system *may* vote “yes” depending on the distribution of information.

---

**vbuterin** (2018-04-24):

> Are there cases where someone benefits if voter v_x doesn’t sign off on the proposal but the claimer states that b_x = 1?

Yes, that’s absolutely possible. And yes, voter v_x could potentially never challenge (though a third party could).

---

**JustinDrake** (2018-04-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> an offline voter in this system may vote “yes”

Consider that a voter may “bluff” being offline for some time (say by being inactive for 1 month) to encourage fake yes votes and “trap” cheating claimers, My intuition is that trapping risk is enough of a deterrent to keep rational claimers honest.

---

**NicLin** (2018-04-28):

Would there be any incentives for a claimer to ignore a voter’s vote? Like preventing the voter from getting reward?

And is there a way for voter to challenge if it happens? Seems to me there’s no way to distinguish a vote being ignored and a vote that’s only signed after?

---

**bwasti** (2018-05-14):

Are there any reasons for a third party to challenge a vote?  If the voter is offline, how would a third party be able to decide to challenge a claim for that voter?  (Assuming there is a fee associated with a challenge, every vote may as well be published as it is rational to challenge every bit in the counterfactual.)

---

**meronym** (2018-09-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> During some challenge period anyone can challenge the claimer to provide the signature of mm from viv_i if the bit bib_i is set to 1. Failure to provide the signature in time slashes half the claimer’s collateral, and rewards the other half to the challenger.

An interesting thing to consider in this protocol is the plausible deniability on the claimer end: if the challenge/response communication happens off-chain, there’s no way for an external observer to determine after the fact whether the claimer failed to produce a proof or the challenger failed to deliver the challenge.

In other words, how would I prove that I sent my challenge and the claimer failed to answer it properly, when the claimer could just as well assert he never received the challenge in the first place?

---

**JustinDrake** (2018-09-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/meronym/48/1049_2.png) meronym:

> plausible deniability on the claimer end

Challenges happens onchain. That is, you use the data availability of the blockchain to solve that problem.

---

**meronym** (2018-09-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Challenges happens onchain.

For the sake of efficiency, I’m assuming the challenge/response protocol would happen offchain by default and the parties can resort to onchain settlement if they don’t succeed in completing their interaction in the offchain world. Even so, we’ll need to address griefing scenarios on both ends:

- The claimer refuses to answer challenges offchain and forces all the challengers to settle onchain. This makes economic sense if the claimer colludes with the block producers that collect the fees from these transactions.
- The challengers force the claimer to settle onchain all the claims, ramping up the total cost of proving the aggragated signature to nothing less than having all the |V|/2 signatures submitted onchain from the very start.

---

**MihailoBjelic** (2018-09-29):

I have two concerns, one for each of the possible values of a bit in the bitfield:

Value 1 (the claimer claims that the voter has voted/signed) - How can **anyone** (i.e. someone else than the voter) challenge this, if the claimer collects the votes off-chain? How can I, as a random participant in the network, know that a certain vote was never submitted to the claimer?

Value 0 (the claimer claims that the voter has not voted/signed) -  What happens if the claimer, for some reason, intentionally ignores the vote (and submits 0 to the bitfield, of course)? As far as I can see, there’s nothing the voter can do about that? It’s the same type of problem as the data availability; the voter can claim that she sent the vote, but the claimer can claim that she never received it, and neither side can be proven wrong?

---

**meronym** (2018-09-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> How can anyone (i.e. someone else than the voter) challenge this, if the claimer collects the votes offline?

I can challenge the claim by requesting the claimer to provide the signature of the original voter. The onchain contract will make sure to slash some of his collateral if he fails to provide the original signature within a predefined amount of time.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> What happens if the claimer, for some reason, intentionally ignores the vote (and submits 0 to the bitfield, of course)?

The voter–claimer channel seems to be yet another side of this protocol where connectivity issues (and the associated plausible deniability) are subtly creeping in.

---

**MihailoBjelic** (2018-09-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/meronym/48/1049_2.png) meronym:

> I can challenge the claim by requesting the claimer to provide the signature of the original voter. The onchain contract will make sure to slash some of his collateral if he fails to provide the original signature within a predefined amount of time.

Everything you wrote is correct, but my concern was:

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> How can I, as a random participant in the network, know that a certain vote was never submitted to the claimer?

I’ll try to clarify. Imagine voter A doesn’t agree with a certain proposal and doesn’t sign/vote, but malicious claimer X submits “1” anyways. How can anyone else (besides A and X) know that A didn’t vote (no one else can see the signatures, claimers collect and aggregate them off-chain), i.e. isn’t A realistically the only one who can (and hopefully will) challenge the claimer?

![](https://ethresear.ch/user_avatar/ethresear.ch/meronym/48/1049_2.png) meronym:

> The voter–claimer channel seems to be yet another side of this protocol where connectivity issues (and the associated plausible deniability) are subtly creeping in.

I din’t completely get you, but I guess the point is that there is no solution for this. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

