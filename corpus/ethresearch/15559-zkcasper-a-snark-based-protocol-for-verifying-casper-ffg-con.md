---
source: ethresearch
topic_id: 15559
title: "zkCasper: A SNARK based protocol for verifying Casper FFG Consensus"
author: seunlanlege
date: "2023-05-11"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/zkcasper-a-snark-based-protocol-for-verifying-casper-ffg-consensus/15559
views: 4804
likes: 14
posts_count: 33
---

# zkCasper: A SNARK based protocol for verifying Casper FFG Consensus

In this research article I present a SNARK based protocol for verifying Ethereum’s Casper FFG consensus proofs.

With this scheme on/offchain light clients can benefit from the crypto economic security provided by the ETH 17m ($34b) at stake.


      ![](https://ethresear.ch/uploads/default/original/3X/2/4/241dbf89c916ad20e8f678eae27c3a3b753861fe.png)

      [research.polytope.technology](https://research.polytope.technology/zkcasper)



    ![](https://ethresear.ch/uploads/default/optimized/3X/3/1/3188697c933a451468f6e549bfef4619277242c4_2_690x290.png)

###



In this research article, I present a protocol for efficiently verifying the Ethereum Beacon chain's Casper FFG consensus proofs using a SNARK based scheme.

## Replies

**Raghavendra-PegaSys** (2023-08-07):

Hi [@seunlanlege](/u/seunlanlege)

Can the ZK proof of the aggregate public key be generated in parallel to the time waiting for a block’s finality? I mean suppose we have a block B1, we need to wait till B65 (more precisely slots) for the finality of B1. During this time can we start generating the ZKP for the aggregate public key of B1?

---

**seunlanlege** (2023-08-07):

Yes, we can incrementally generate proofs as we observe attestations from the various attestation committees

---

**Raghavendra-PegaSys** (2023-08-07):

It then means that basically you have at least 12 minutes for the ZK proof generation. That way the ZK proof generation is not exactly a bottle-neck

---

**seunlanlege** (2023-08-07):

Proof generation isn’t the bottleneck by any means, the original snark can prove apk committee sizes of  2^{20} - 1 in around 4mins. Admittedly this is also due to the use of bls12-377/761 curves for their high 2-adicity and the fact that the circuit itself performs no permutation checks.

[![Screenshot 2023-08-07 at 4.35.44 PM](https://ethresear.ch/uploads/default/optimized/2X/f/f6fb6b2b2bfb76edfd48595aab0769dea7f432a9_2_690x156.png)Screenshot 2023-08-07 at 4.35.44 PM1190×270 26.2 KB](https://ethresear.ch/uploads/default/f6fb6b2b2bfb76edfd48595aab0769dea7f432a9)

For zkCasper, we’ll be levergaing the bl12-381/767 curve pairing, which has no high 2-adicity, but has a somewhat highly composite group order that allows us leverage the cooley-tukey fft. It won’t be as fast as the classic radix-2 fft, but it’ll be faster than the naive dft.

---

**Raghavendra-PegaSys** (2023-08-07):

Great. I see that they are not a bottleneck, but even these proof generation times, which are in the order of minutes can be hidden inside the finality waiting times.

On a related note, in this blog you write that the sync-committee can collude to do eclipse or data withholding attack. Can you show me how this can be done a little more concretely?

I understand the sync committee protocol has no slashings but looking at some of the posts here: [Snowfork's Analysis of Sync Committee Security - Tech Talk - Polkadot Forum](https://forum.polkadot.network/t/snowforks-analysis-of-sync-committee-security/2712), [How I Learned to Stop Worrying and Love the Sync Committee](https://blog.succinct.xyz/blog/sync-committee) and [Exploring Eth’s Altair Light Client Protocol: t3rn’s vision](https://www.t3rn.io/blog/exploring-eths-altair-light-client-protocol-t3rns-vision) it looks like the probability of having a malicious sync committee is reasonably low.

---

**seunlanlege** (2023-08-07):

> On a related note, in this blog you write that the sync-committee can collude to do eclipse or data withholding attack. Can you show me how this can be done a little more concretely?

MEV middleware can allow members of the sync committee to coordinate and launch all kinds of byzantine attacks. Especially after we saw recently that [validators were exploiting flashbot bundles that were sent to them](https://twitter.com/samczsun/status/1642848556590723075?s=20).

---

**Raghavendra-PegaSys** (2023-08-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/raghavendra-pegasys/48/4532_2.png) Raghavendra-PegaSys:

> Can the ZK proof of the aggregate public key be generated in parallel to the time waiting for a block’s finality? I mean suppose we have a block B1, we need to wait till B65 (more precisely slots) for the finality of B1. During this time can we start generating the ZKP for the aggregate public key of B1?

Coming to think of it, I think such an overlapping approach is not possible. I believe the verifier node needs to preserve a buffer of at least 65 blocks. Meaning verifier verifies the snark proof for B1, and puts B1 in its buffer. Next it verifies the snark proof for B2, and puts B2 in its buffer. Likewise it continues till it verifies the snark proof for B65 and puts B65 in its buffer. Note that B65 being the checkpoint block finalises B1 to B32. So now we can act upon all the events that are generated in B1 to B32.

So in order to verify an event that happened in the block B1, we need to wait 12.4 mins for it to be finalised (which happens because of B65) and then wait for the snark proof of B65 (which in addition is 4mins). So totally 16.4 mins. Am I correct?

---

**seunlanlege** (2023-08-23):

Not really, supermajority attestations can happen before B65. And we can prove attestations as they’re produced to the verifier

---

**Raghavendra-PegaSys** (2023-08-23):

In my understanding the supermajority attestation of B65 justifies the epoch containing <B33, … B64> and finalises <B1, … B32>. Am I right?

---

**seunlanlege** (2023-08-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/raghavendra-pegasys/48/4532_2.png) Raghavendra-PegaSys:

> In my understanding the supermajority attestation of B65 justifies the epoch containing  and finalises . Am I right?

Yes this is correct. But small note, validators vote to justify the starting block of their current epoch. So they’re really justifying B33 and finalizing B1.

---

**Raghavendra-PegaSys** (2023-08-23):

In that case looks like my understanding is correct: To use an event e in block B1, you need to wait for getting B65, which is 12.4 minutes away, and then we need to generate the snark proof for B65 which is 4 mins away in addition. So the finality time and the proof times gets added.

---

**seunlanlege** (2023-08-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/raghavendra-pegasys/48/4532_2.png) Raghavendra-PegaSys:

> To use an event e in block B1, you need to wait for getting B65

Since the signatures may overlap, we don’t need to wait. We start generating proofs for attestations as we see them.

![](https://ethresear.ch/user_avatar/ethresear.ch/seunlanlege/48/9754_2.png) seunlanlege:

> Not really, supermajority attestations can happen before B65. And we can prove attestations as they’re produced to the verifier

---

**Raghavendra-PegaSys** (2023-08-24):

Yes, I know, the snark proof generation for B1 can be started as soon we have attestations for them. But to use them on the verifier side, verifier needs to know snark for B65. Otherwise, how can he trust that B1 was finalised?

---

**seunlanlege** (2023-08-24):

Validators are justifying B33, which implicitly finalizes B1. The verifier doesn’t care about B65.

---

**Raghavendra-PegaSys** (2023-08-24):

If you give only B1 for the verifier, how does the verifier know the finality of B1. In other words, how does the verifier know the existence of B65? Basically how to prove that B1 is finalised? Equivalently how to prove to verifier that there is a justified descendant block at B33, which in turn means how to prove to verifer that there is an unjustified descendant block at the level of 65 which has achieved attestations?

---

**seunlanlege** (2023-08-24):

You might be overthinking it, The only thing that matters are supermajority attestations that point to B1 as the source & B33 as the target. The verifier, after observing these attestations, confirms B1 is final and B33 is optimistically finalized, the next round of attestations point to B33 as the source and B65 as target.

---

**Raghavendra-PegaSys** (2023-08-24):

I am genuinely trying to understand here.

From this blog: [What Happens After Finality in ETH2? - HackMD](https://hackmd.io/@prysmaticlabs/finality), I see that:

> If > 2/3rds of validators vote correctly on the chain head during an epoch, we call the last epoch justified

I understand here that when there is a supermajority attestation for B65, we get the epoch <B33,…B64> justified and the epoch <B1, … B32> finalised.

---

**seunlanlege** (2023-08-24):

Yes but they’re voting to justify B65 in blocks <B65…96>

---

**Raghavendra-PegaSys** (2023-08-25):

Okay. In that case let me rephrase my original thinking here:

I believe the verifier node needs to preserve a buffer of at least 33 blocks. Meaning verifier verifies the snark proof for B1, and puts B1 in its buffer. Next it verifies the snark proof for B2, and puts B2 in its buffer. Likewise it continues till it verifies the snark proof for B33 and puts B33 in its buffer. Note that the supermajority of B33 finalises B1 to B32. So now we can act upon all the events that are generated in B1 to B32.

So the total time to act on an event e in B1 is: time to get B33 (epoch time = 6.4 mins) + time to obtain supermajority attestation of B33 + snark proof construction time (4 mins). So > 10m. Do you agree?

---

**seunlanlege** (2023-08-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/raghavendra-pegasys/48/4532_2.png) Raghavendra-PegaSys:

> I believe the verifier node needs to preserve a buffer of at least 33 blocks. Meaning verifier verifies the snark proof for B1, and puts B1 in its buffer. Next it verifies the snark proof for B2, and puts B2 in its buffer.

This is incorrect, the verifier only needs to know the epoch boundaries

![](https://ethresear.ch/user_avatar/ethresear.ch/raghavendra-pegasys/48/4532_2.png) Raghavendra-PegaSys:

> So the total time to act on an event e in B1 is: time to get B33 (epoch time = 6.4 mins) + time to obtain supermajority attestation of B33 + snark proof construction time (4 mins). So > 10m. Do you agree?

If you need the events in <B1…B33>, you’ll need B33 to become the source of the attestations. Which makes B65 the target. Voting will be done in the beacon chain blocks <B65…B96>.

So 2 epochs + the time it takes to reach supermajority attestations in the 3rd epoch.


*(12 more replies not shown)*
