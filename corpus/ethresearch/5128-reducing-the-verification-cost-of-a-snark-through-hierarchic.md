---
source: ethresearch
topic_id: 5128
title: Reducing the verification cost of a SNARK through hierarchical aggregation
author: AlexandreBelling
date: "2019-03-11"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/reducing-the-verification-cost-of-a-snark-through-hierarchical-aggregation/5128
views: 9614
likes: 22
posts_count: 11
---

# Reducing the verification cost of a SNARK through hierarchical aggregation

Hi all, I have been working for a few month on a scheme named Boojum to reduce the cost of a snark verification. A PoC demo can be found in this [repo](https://github.com/AlexandreBelling/go-boojum)

## Overview

This [article](https://eprint.iacr.org/2014/595.pdf) introduced recursive snark aggregation using cycle of elliptic curves, and created the concept of Proof Carrying Data (PCD) and it has been seen as potential solution to instantly (30ms) verify the state of the chain through a single SNARK verification. This however raises the problem of data availability as it can potentially create situations where the state becomes inaccessible.

We propose here a predicate-agnostic solution to combine multiple ppzksnarks proofs (forged for various circuits) into a single one that can be verified in constant time (plus a tiny linear extra cost per proof). This is a variation of the PCD proof system and it comes with two circuits described in the diagram below:

[![aggregation_circuits](https://ethresear.ch/uploads/default/optimized/2X/4/4aad3200f018badd62e5ae8946c87ecffd539a3e_2_690x215.png)aggregation_circuits1324×414 28.3 KB](https://ethresear.ch/uploads/default/4aad3200f018badd62e5ae8946c87ecffd539a3e)

Both circuits represents the following predicate: “I have run a ZK-SNARK verifier algorithm on 2 given triplets (proofs, vk and primary inputs) and their output was 1 in both”. This will work only for any circuits with a primary input of length 1 but there is no loss of generality: given a snark friendly cryptographic hash function, we can always convert a multi-primary-input circuit into a single-primary-input by passing the primary inputs as auxilliary and adding the following constraint :

```
Primary = Hash(Auxilliary)
```

This heuristic is furthermore applied to our circuits, thanks to that we enable proof for an instance of boojum circuit to be used as an input of another instance. Hence, we can recursively aggregate proof with the same two circuits.

The two circuits differs in the sense that they are not defined on the same EC. Any proof generated on one of theses can be verified recursively inside a proof on the other one. This is a necessary conditions for constructing a practical recursive SNARKs. We are using the elliptic curve cycle MNT4-MNT6 introduced in [the same paper](https://eprint.iacr.org/2014/595.pdf).

One of the main difference with PCD is that Boojum accepts a verification key as a public parameter. The generator does not make assumption over the proof he is going to verify. The concern here is not about what circuit is being proved on but rather to convince that a verifier has run successfully for a given triplet (proof, verification key, primary input).

Additionnally, PCD recursive aggregation works in a sequential way: assignments are added one after the others in the proof, while here we describe a protocol aggregating proofs in a hierarchical fashion.

[![tree_of_proof](https://ethresear.ch/uploads/default/original/2X/4/45c4684f8e7d4bffbda548bf1192cdadb3ce746a.png)tree_of_proof591×351 13.4 KB](https://ethresear.ch/uploads/default/45c4684f8e7d4bffbda548bf1192cdadb3ce746a)

The leaf nodes (ie: the batch of proofs to be aggregated together) are inputed as:

- A verification key
- A proof
- A primary inputs of the the proved assignement

## On-chain verification

Each parent node (ie: aggregated proof) takes the hash of the previous proofs as primary inputs. Therefore during the verification of the root proof, we need to first reconstruct its input by recursively hashing the intermediary nodes.

[![verification](https://ethresear.ch/uploads/default/optimized/2X/d/df19df3e0d8173bf0c3ab5e42c1ce73925e9e58f_2_690x249.png)verification1263×457 19.7 KB](https://ethresear.ch/uploads/default/df19df3e0d8173bf0c3ab5e42c1ce73925e9e58f)

```
In yellow, the elements that are sent in the payload to the verifier.
In grey, the elements that are already known to the verifier
In blue, the elements that are recomputed during verification by the verifier
```

### Gas Cost estimation

Although no proper benchmark has been run yet. We can estimate that currently each aggregated proofs weights 355 bytes in average (373B for MNT6 and 337B for MNT4). And each verification key (on MNT4 only) weights 717B. This adds up to (355 + 337 + 717 = 1409B) for each proof. This represents an extra cost of 88641 Gas per extra proof assuming we can neglect the zero-bytes.

This estimation also does not takes into account the cost of re-hashing the merkle tree. We currently uses “subset sum hash” which is available as a gadget in libsnark. It is worth noting that this hash function has been cryptanalyzed (see this [article](http://www.math.ttu.edu/~cmonico/research/linearhash.pdf)). For this reason, it cannot remains a definitive choice and its replacement will obviously have an impact on the verification cost of an extra proof.

Other options are being considered as a potential replacement:

- Pedersen Hash (We could re-use zcash implementation)
- MiMc
- David-Meyers

(Taken from this [topic](https://ethresear.ch/t/cheap-hash-functions-for-zksnark-merkle-tree-proofs-which-can-be-calculated-on-chain/3176))

In the worst case the overhead of hashing each aggregated snark is still significantly lower compared to the current cost of a verification and compared to the ~90k gas payload we would have to pay per extra proof.

### Improving the size of the payload

In this aggregation protocol, we don’t care this much about the intermediary proofs. The only thing that matter is that *theses proofs exist and have been successfully verified* the same applies for the leafs proofs (ie: the proofs that are submitted to the process of aggregation).

In the end what an end-user wants to prove is only that they have a valid assignment for a given public input and a given circuit. Therefore, instead of publishing the proofs on-chain we could simply publish a hash of them. The proof would have to be communicated off-chain to the aggregator pool though.

The improved version of the circuit is described in the figure below:

[![aggregation_circuit_improved](https://ethresear.ch/uploads/default/optimized/2X/a/aacb19e7b5de6305b617cb0d2a132d3bac97dbdf_2_690x324.png)aggregation_circuit_improved1192×560 35.5 KB](https://ethresear.ch/uploads/default/aacb19e7b5de6305b617cb0d2a132d3bac97dbdf)

The additional payload per extra proof is decreased to (32 * 4 =) 128B (8kGas) and thus given a cheap snark friendly hash function the cost of a verification becomes really interesting.

## Off-chain aggregation

The tree structure of the aggregated proof makes it possible to distribute the proving computation across a pool of worker. Given that each aggregation steps takes about 20sec, it would takes over 5.5 hours to aggregate 1024 proofs. However, in an ideal case, with 512 workers, the process finishes in only 3min12. If we could run a prover on a GPU, then we would be able to have a much better throughput without requiring a too big pool of worker.

The protocol should be reasonably efficient (ie: replicate as least as possible the aggregation), resilient to malicious actors (no one can prevent or slow down the aggregation process efficiently).

Additionally this protocol should include a reward mechanism in it in order to incentivize the worker to join the pool. This is not a trivial task because the BFT condition requires tasks to be replicated and that can create situations in which workers are actually not rewarded for their tasks.

### Proof of Stake based aggregation protocol

An idea of possible design is to use of a PoS leader election (so we can avoid sybil attack):

- People can submit a proof to the pool in they provide token/eths
- The workers can join the pool if they provide a stake
- A leader is randomly elected in the pool at a regular rate
- The leader dispatch the job across the pool and manage faults
- Each worker adds an address in its aggregation proof so that he gets rewarded
- Each worker keeps track of his previous jobs (in case of leader failure)
- Each job produced by a worker is checked by the verifier.
- Each pair of job assigned to the worker by the leader is checked.
- When all the jobs are complete, the leader sends the aggregated proof to be verified on-chain.
- If the leader does not answer after a specified timeout, the next elected one takes the leadership and each worker sends their past jobs.

The leader should schedule tasks as randomly as possible in order to make it impossible for a rogue worker to get it all the time. In this case, workers and leader failure are well-handled. But we need other mechanism to ensure attack are less likely to happen.

- Each exchanged message should be authenticated (eg: signed). When a fake proof is produced any member can report it and earn the faulty worker’s stack.

We have no evidence so far that such a protocol would is actually secure

## Replies

**HarryR** (2019-03-16):

There is one problem though.

Which is that Ethereum doesn’t support pairing operations on MNT curves. I would love to be able to use them, as - you have described - it makes recursive SNARKs possible and lots of interesting things like aggregation are opened up to us.

Other applications using recursive SNARK verification is to have a verification key associated with each leaf in the merkle tree, where a proof for that key must be provided to update the data associated with the leaf. Think of it as being a generic database layer, where each node can be associated with a different user-specifiable application - and the application can even be allowed to change the verification key for that leaf.

---

**AlexandreBelling** (2019-03-16):

Thanks for your feedbacks [@HarryR](/u/harryr)

As you say, they are not supported with the mainnet so far. I believe that before it could happen, we would need to get an assessment of security for thoses specific MNT4-MNT6 curves and a good implementation. The good side, is that we can have the same approach with STARKS once it becomes practical to use them on Ethereum. In the meantime we can still play with private/side chains. I am planning to write a precompile to see how it can performs at the current stage.

> Other applications using recursive SNARK verification is to have a verification key associated with each leaf in the merkle tree, where a proof for that key must be provided to update the data associated with the leaf.

If I understand correctly, we could also think of it as a generic confidential and permissioned data anchor on-chain, where the data could be anything (token balance/ personal info/ medical data …). That’s interesting. We can also add atomic-updates logics in the nodes (in the form of a circuit) so that we can ease up users interaction.

In a complementary way, we could also rely on multi-predicate (described [here](https://eprint.iacr.org/2015/377.pdf)). Basically, it consists in embedding several verification key in a circuit so that the cost having many independant updates logic remains low.

---

**burdges** (2019-03-17):

We looked into these at W3F, and chatted with some business guy at Coda, but right now Coda uses the curves recommended in the curve cycles paper https://eprint.iacr.org/2014/595.pdf which only provides 80 bits of security.

We discussed the curve choice problem for curve cycles in this thread: https://moderncrypto.org/mail-archive/curves/2018/001004.html

I’ve now forgotten why I thought if the attack that weakened the BN128 curve does not apply to these curves.  In any case, we must still expect some further weakening, simply due to these being pairing friendly curves.  I’d therefore worry even that the trusted setup could be broken in a decade or so, although an evolving trusted setup like SONIC might help slightly.

I’d also thought the curve cycles paper also found some horrifically slow curve over an 800 bit base field, although not seeing it in the paper right now.  If so, that’s as least secure, just slow.

We never spoke with Izaak Meckler, Vanishree Rao, or Rebekah Mercer (Coda’s cryptographers), only some business guy, so maybe they’ve found better curve cycles than the curve cycles paper found.  At least some curve experts do not expect this to be possible however.

---

I’d pursue this by instead asking: Is there a curve cycle in which some but not all support pairings, but all the curves offer reasonable security.  I’d then build the infrastructure using another zero-knowledge proof technique for the curve that lack pairings.  We exploit the less efficient zero-knowledge proofs only as a mechanism to produce a proof of verifying a SNARK that can itself be checked in a SNARK, never actually send them over the wire.

I’d think this makes an excellent PhD project for anyone who really knows elliptic curves and likes zero-knowledge proofs.  It’s way more than twice as much code as doing this Coda’s way, but you could build on both the zcash and dalek zk ecosystems, which the zcash devs want to converge anyways.

---

**AlexandreBelling** (2019-03-17):

Thanks for the info [@burdges](/u/burdges),

You might be interested in this paper: https://arxiv.org/pdf/1803.02067.pdf

It is a characterization of all the MNT4-6 cycles of elliptic curves cycles, it should be possible to pick a cycle that is reasonnably secure and practical for ethereum.

Although, I don’t think doing this on a slow elliptic curve is that much a problem :

Let’s assume,

- We have a 3M gas snark verification because we are on a 3x slower curve cycle
- The cost of an extra proof being aggregated to be 15K Gas
- A block gas limit of 8M

Then we can aggregate 333 proofs per block instead of 466. This is less efficient but not what I would call a no-go.

Most of the costs is for the prover, but I assume we will have proving hardware

I like your idea of combining together several proof scheme in the cycle. We could for instance alternate between bulletproofs and SNARKS, I wonder how expensive the bulletproof verification inside the SNARK would be though.

---

**burdges** (2019-03-17):

Interesting article, maybe their results will yield better curves, but maybe their results provide stronger evidence that no good curves exist too.

We’re interested in curve cycles largely so that the block verification functions can become constant space and time, and verify the history, so mostly the same reasons as Coda.

We know applications for curves with a base field of order matching the group order of another curve, like ZCash’s Jubjub curve, but such applications normally do not require cycles, only a chain of curves.  I’ve some comments here:

https://forum.web3.foundation/t/verifiable-random-pederson-commitments/39

We do not require smart contracts to do interesting things on polkadot, so I never worry about them really.  Yet, I’d think many smart contract applications would similarly require only such a series of curves, not an actual cycle.  I suppose the cycle permits you to continually verify keep arbitrary amounts of data off chain though.

---

**barryWhiteHat** (2019-03-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexandrebelling/48/3280_2.png) AlexandreBelling:

> I am planning to write a precompile to see how it can performs at the current stage.

Have you considered writing an EIP to include a recursive freindly curve in eth? If we can find a practicle curve with reasonable secureity i think this is a no brainer.

---

**AlexandreBelling** (2019-04-02):

Following your recommandation, I submitted an EIP draft to support elliptic curve cycle MNT4.

Here is the link : https://github.com/ethereum/EIPs/pull/1895

---

**danib31** (2019-06-11):

Very nice job [@AlexandreBelling](/u/alexandrebelling)! I do believe that proof aggregation and EC cycles is one of the most challenging problems in the zk space, mostly because of the difficulty of finding the “perfect” cycle sort to speak.

At the ZKProof workshop there was a breakout session lead by Izaak Mekler on SNARK composition and it was very interesting. I have not mapped the conversation here to the notes, but here is the link, in case you find anything useful!


      ![](https://ethresear.ch/uploads/default/original/3X/1/6/16b9a4813150ee07280dfde763354289623eafe9.png)

      [The ZKProof Community – 10 Apr 19](https://community.zkproof.org/t/breakout-session-snarks-on-snarks-recursive-composition/137)



    ![image](https://ethresear.ch/uploads/default/optimized/3X/f/e/fe49fd71747a0e75851f92852473aea044bf32a5_2_690x345.png)



###





          2nd ZKProof Workshop






Time: Thursday April 11th, 12:05 - 12:45  Preprocessing SNARKs have the major drawback that the size of the computation to be verified must be fixed before performing a setup.  Recursive composition of SNARKs is a powerful technique for creating...



    Reading time: 3 mins 🕑
      Likes: 14 ❤

---

**AlexandreBelling** (2019-06-15):

Very interesting session.  My opinion, is that in the current state, as long as a cycle satisfies the following statements they are suitable for proof aggregation on a blockchain:

- Can achieve 128 bits of security
- One of the curve is efficient enough to be realistically verified on a blockchain (should be able to execute in 200 - 300 ms). Possibly parallelized for entreprise application.
- One of the curve order has a reasonnably high 2-adicity (so that it is not a limitation on the number of proofs we need ) and the others have at least 17 (so that it can support a circuit with a single verifier).

An alternative would be to resort to hash-based proof system like STARKs. Aurora seems to be a good fit (if we reduce the cost of transaction data) but I have no idea how many constraints are needed in order to implement an Aurora verfier in an Aurora proof.

I also do not know if Aurora proving can be efficiently parallelized. [Link to Aurora paper](https://eprint.iacr.org/2018/828.pdf)

---

**daira** (2019-11-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/burdges/48/1997_2.png) burdges:

> I’d pursue this by instead asking: Is there a curve cycle in which some but not all support pairings, but all the curves offer reasonable security.

Yes that’s quite feasible, using 2-cycles of a BN curve and a non-pairing-friendly curve. There is code to generate such cycles where both curves have high 2-adicity, at [curvesearch/halfpairing.sage at master · daira/curvesearch · GitHub](https://github.com/daira/curvesearch/blob/master/halfpairing.sage) . The bit length needs to be ~384 bits to resist Kim–Barbulescu attacks. We mention these cycles briefly in the [Halo paper](https://eprint.iacr.org/2019/1021), although we ended up using a non-pairing cycle in Halo since we wanted transparent setup. They’re also discussed in [Zcash issue 4092](https://github.com/zcash/zcash/issues/4092).

