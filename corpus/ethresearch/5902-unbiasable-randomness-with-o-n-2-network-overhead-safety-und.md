---
source: ethresearch
topic_id: 5902
title: Unbiasable randomness with O(n^2) network overhead, safety under 34% honest and liveness under 67% honeset without BLS signatures and VDFs
author: AlexAtNear
date: "2019-07-31"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/unbiasable-randomness-with-o-n-2-network-overhead-safety-under-34-honest-and-liveness-under-67-honeset-without-bls-signatures-and-vdfs/5902
views: 2706
likes: 6
posts_count: 8
---

# Unbiasable randomness with O(n^2) network overhead, safety under 34% honest and liveness under 67% honeset without BLS signatures and VDFs

Hi, we’ve been recently doing some research on distributed randomness, want to share a RandHound-influenced protocol that has the properties from the title, would appreciate feedback.

(EDIT: the description below is fully rewritten based on some offline feedback)

(EDIT2: more formal latexified version can be found here: https://www.overleaf.com/read/pcrtmwpxvnkb)

`n` participants to do the following:

1. Each participant j generates vector  r[j] of size k = n*2/3 where each element is a 256 bit random numbers, erasure codes them to have a vector s[j] of size n with n shares such that any k shares can reconstruct the chosen k numbers, and encodes each of the n shares with the public key of one of the partipants to get a vector es[j] of size n.
They then publish es[j]. Here it’s important that nobody can recover r[j] by just observing es[j]
2. Participants reach a consensus on a set S of at least k published es's.
3. Each participant i publishes decoded row of es[{S}][i]. Once k participants published the rows, everybody can reconstruct the r[{S}].
I now want participants for each j for which r[j] was sucessfully reconstructed to be able to reproduce the es[j] and confirm that it matches the published es[j]. If it matches, then all the participants were able to reconstruct r[j], no matter what shares they observed. If a participant failed to reconstruct the erasure code or it didn’t match the es[j], then all the paritcipants either failed to reconstruct it or reconstructed something that doesn’t match es[j].
4. Let S’ be the subset of S for which the r was reconstructed. The output of the randomness beacon is the some function of the r[{S'}]

Here there are some requirements to the public key ecnryption:

1. Encryption needs to be determenistic, so that reconstructed es in step 3 matches the published es in step 1.
2. If some es[j][i] is gibberish (i.e. doesn’t decrypt or decrypts into something that is not equal to es[j][i] after re-encrypting), it should be possible to prove it.

Seems like ElGamal in which the step `y=random()` is replaced with `y=hash(input)` works for (1) above, and Chaum-Pedersen proof works for (2) if a malicious actor still used some `y` that was not equal to `y=hash(input)`.

Comparison to other schemes:

- This approach is naturally inferior to RANDAO+VDFs in that it has worse liveness and safety requirements, but VDFs have the known issues with the necessity to build ASICs (or fear that someone else will).
- It appears to be as good as threshold signatures (except that it requires n^2 network instead of n for threshold signatures IIRC) without requiring the expensive DKG step.
- Compared to RANDAO it is unbiasable
- Compared to RandShare it has lower complexity, compared to RandHound it is significantly simpler.

Feedback is appreciated.

## Replies

**AlexAtNear** (2019-07-31):

[@JustinDrake](/u/justindrake) pointed out offline that he published something that has the same properties last year:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png)
    [Leaderless k-of-n random beacon](https://ethresear.ch/t/leaderless-k-of-n-random-beacon/2046) [Sharding](/c/sharding/6)



> TLDR: We suggest a random beacon scheme where committees of size n generate random numbers if k participants participate correctly. It is in a similar vein to Dfinity’s random beacon (without use of BLS) and has the same message complexity of k messages per beacon output.
> Part 1: A single random output
> For clarity we first show how k-of-n participants generate a single output in three phases. In part 2 we combine the phases for messaging efficiency.
>
>
> Phase 1—ephemeral identities: Every parti…

---

**gokulsan** (2020-08-07):

Hi Alex,

Nice to see the post on Erasure Code approach of NEAR protocol here. I have read an elaborate article on RandHound and RandShare in the NEAR protocol blog. It was awesome. Will this approach be deterministic in a Data Shard setting when the proximity to the beacon chain becomes dynamic and probabilistic. Is it using the proximity between the Data Shard Chain and Beacon chain as a variable. My awareness about the internals of NEAR protocol is quite rudimentary. Please correct me if my understanding is completely wrong.

---

**aidenjnoirr666** (2020-08-13):

Seems still off though if one has full control without theft to occur or a chance no less the purpose of sakes, say like technology and hackers lol smaller better faster every six months , the future even a year from now no idea who can solve yet still a smoked wall to an equation …?

---

**aidenjnoirr666** (2020-08-13):

Seems better minds I know then mine could already eqaute for this to get values

---

**kladkogex** (2020-08-13):

> Participants reach a consensus on a set  S  of at least  k  published  es 's.

To reach binary consensus in many cases you need unbiasable randomness. At least for asynchronous algorithms.

Like we at SKALE using BLS  common coin for our binary consensus …

---

**AlexAtNear** (2020-08-13):

In practice partial synchrony is a reasonable assumption though, and then you can use any binary consensus that works in a partially synchronous setup (e.g. Tendermint).

---

**AlexAtNear** (2020-08-13):

I don’t know the terminology you use well enough. What is a data shard?

