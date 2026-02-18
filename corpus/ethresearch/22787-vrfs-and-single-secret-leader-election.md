---
source: ethresearch
topic_id: 22787
title: VRFs and Single Secret Leader Election
author: "71104"
date: "2025-07-21"
category: Cryptography
tags: [single-secret-leader-election]
url: https://ethresear.ch/t/vrfs-and-single-secret-leader-election/22787
views: 340
likes: 3
posts_count: 5
---

# VRFs and Single Secret Leader Election

## Introduction

While doing research for my own blockchain project I’ve found [evidence](https://x.com/drakefjustin/status/1215659733048266752) that the Ethereum Foundation has been investigating a VRF with DDH construction for single secret leader election (SSLE).

Throughout my time on this board I’ve generally found a lack of awareness and understanding of the DDH construction, which is a shame because people tend to employ needlessly complex setups involving zk-S{N,T}ARKs. Don’t get me wrong, I’m a huge fan of zk-S{N,T}ARKs but they’re also very complex and a massive overkill compared to a couple of additions and multiplications over an elliptic curve.

So I thought of starting a thread to provide a quick introduction for anyone interested. This starter is based on the construction described by [RFC-9381](https://datatracker.ietf.org/doc/rfc9381/) and it also works as my personal notes for my project.

As usual, if something’s off please let me know. Future readers may make critical security depend on this.

## FAQ

### 1. What’s a VRF?

A *Verifiable Random Function* is essentially a hash that carries a zero-knowledge proof of its correct execution.

### 2. You mean a hash with a zk-SNARK?

Not quite. The zero-knowledge proof of a VRF with DDH construction is much lighter and based on much simpler math than a full-on zk-SNARK. It’s vaguely similar to a [Schnorr signature](https://en.wikipedia.org/wiki/Schnorr_signature).

### 3. What’s DDH construction?

DDH stands for [Decisional Diffie-Hellman](https://en.wikipedia.org/wiki/Decisional_Diffie%E2%80%93Hellman_assumption) and refers to the hardness assumption that guarantees the soundness of the scheme we’ll discuss here. There are other VRF constructions but we won’t discuss them.

### 4. Why is that better than a regular hash with an accompanying zk-SNARK?

Because the zero-knowledge proof of a VRF is much easier to implement, gives less chances of introducing bugs, and can be implemented in a project even if the project doesn’t depend on a zk-SNARK framework. With a VRF scheme one doesn’t need to worry about their circuit being underconstrained or overconstrained. There’s no circuit and there are no constraints.

### 5. How does that allow for non-interactive leader election?

- At the beginning of a slot each node of the network runs vrf(slot_number || epoch_randomness);
- if the resulting random value is less than or equal to the node’s share of the total stake, the node is a leader and no one else knows;
- if the node is a leader it starts building the block;
- at the end of the slot all leaders publish their blocks along with the proof of the VRF, showing they were in fact leaders;
- the fork is resolved with LMD-GHOST as usual.

**There’s no need for the nodes to commit to a value at the beginning of every slot.**

### 6. Does that mean Ethereum would no longer need RANDAO?

Weeeell… maybe. You still need a way to generate the `epoch_randomness` parameter above. We could arguably get rid of RANDAO by using one of the latest canonical block hashes though, e.g. the hash of block N-10 (younger hashes would cause fork ambiguity).

And yes, you do want extra public global randomness to seed the VRF, otherwise a node could precalculate its entire leader schedule for the foreseeable future and start taking bribes from external actors to act a certain way at certain times.

### 7. But wait, vrf(slot_number || epoch_randomness) is deterministic, anyone can calculate it.

Nope. The VRF output depends on the private key of the prover, so only the prover can calculate it.

### 8. Can the prover grind on its keypair to achieve a favorable outcome?

Not if the keypair is the wallet used to stake. Other nodes will use your public key to verify your VRF proof.

### 9. I’m sold. Tell me the algorithm!

Sure, read on.

## Definitions

NOTE: through this article we’re assuming the use of elliptic curve cryptography (ECC), so for example when committing a scalar we’ll use the notation x \cdot G rather than g^x. The reader is expected to be familiar with ECC.

- G = the generator point of the elliptic curve.
- x = the private key of the prover.
- P = the public key of the prover.
- n = a secret random nonce that the prover must discard once finished.
- m = an arbitrary message that we use to seed the VRF (it includes the slot number and epoch randomness in SSLE schemes).
- \Gamma = the output random value from the VRF.
- \pi = the zero-knowledge correctness proof of the VRF.
- HashToScalar = a cryptographic hash function such as SHA3.
- HashToCurve = a special hash function that returns an elliptic curve point rather than a scalar. It’s based on an existing cryptographic hash such as SHA3.

**WARNING**: do not attempt to implement `HashToCurve` on your own, e.g. by hashing to a scalar with SHA3 and then multiplying the scalar by G to commit it to the curve. Even if you do that safely (e.g. by performing integer clamping correctly if you’re on Ed25519) the distribution of the output point wouldn’t be uniform, so the resulting point wouldn’t be suitable for the VRF output. The implementation of `HashToCurve` **MUST** be provided by your secure ECC library, such as [the one from curve25519-dalek](https://docs.rs/curve25519-dalek/latest/curve25519_dalek/ristretto/struct.RistrettoPoint.html#method.hash_from_bytes) and [the one from pasta_curves](https://docs.rs/pasta_curves/latest/pasta_curves/arithmetic/trait.CurveExt.html#tymethod.hash_to_curve).

## Proving Algorithm

- Hash to the curve:

H = HashToCurve(slot\_number || epoch\_randomness)

- Calculate the output point:

\Gamma = x \cdot H

- Generate the proof points:

U = n \cdot G \\
V = n \cdot H

- Calculate the challenge hash:

c = HashToScalar(P, H, \Gamma, U, V)

- Calculate the Schnorr-like signature scalar:

s = n + c \cdot x \mod q

\pi = (c, s). Output (\Gamma, \pi).

## Verification Algorithm

- Hash to the curve:

H = HashToCurve(slot\_number || epoch\_randomness)

- Recover the proof points:

U’ = s \cdot G - c \cdot P \\
V’ = s \cdot H - c \cdot \Gamma

- Recover the challenge hash:

c’ = HashToScalar(P, H, \Gamma, U', V')

The proof is valid iff c’ = c.

## Uses in smartcontracts

If we exposed a VRF to the EVM, could it replace external oracles like the [ChainLink VRF](https://chain.link/vrf)? **This VRF could be seeded with an arbitrary message provided by the smartcontract and proven with the private key of the block builder, but the proof would have to be verified by all block validators**.

Sample Solidity signature:

```sol
/// Returns a uniformly distributed 256-bit word seeded with the provided seed.
/// Implemented securely by calculating a VRF validated with the block.
function get_randomness(bytes seed) returns (bytes32);
```

Whatever system we choose for randomness in dApps, it needs to be resistant to:

- prediction – obviously;
- bias – obviously;
- grinding – block builders must not be able to make many attempts until they get a favorable outcome in the dApp;
- censorship – the random outcome must not keep changing, it must remain constant from a certain block on, otherwise the nodes of the network may censor the randomness-resolving transaction until they get a favorable outcome.

Let’s now compare the following approaches:

1. Using the hash of the previous block as a source of randomness – fails on all counts: block builders can censor all transactions to the dApp until a favorable block hash shows up, they can grind on a block hash by reordering transactions and then submit a transaction to the dApp at the next block, etc.
2. Using the hash of the current block – the dApp commits to a block and will get its hash in a future transaction. Still fails in many ways, e.g. block builders can submit the commitment transaction and then the resolving one in the next block, but if those two blocks don’t work out a favorable outcome they can try again with a different fork.
3. Using the hash of the next block – same problem as above, it just needs an extra block (which may still be on a fork).
4. Using the hash of block N+10 – the dApp commits to block N and randomness will be the hash of block N+10, when block N is canonical. Fails on grinding because block builders can make many attempts by reordering the transactions of block N+10.
5. DDH-based VRF seeded with the hash from 10 blocks ago – still vulnerable to censorship because “the hash from 10 blocks ago” keeps changing.
6. Commit to block N, then at block N+11 use the get_randomness function as defined above, seeding it with the hash of block N+10 – the last two blocks (N+10 and N+11) may still be on a fork, so a block builder can make many attempts by reordering the transactions of block N+10.
7. Commit to block N, then at block N+20 use get_randomness seeding it with the hash of block N+10 – seems to pass all tests, and it’s not too far from what ChainLink does. A bit slow maybe, but it assumes it takes 10 slots for a block to become canonical, so maybe we have some room for improvement by setting lower thresholds.

## Replies

**jonhubby** (2025-07-22):

Hey 71104, thanks for the detailed breakdown, really clear summary of the DDH-based VRF approach. I especially appreciate the comparison at the end between different randomness sources; that context helps a lot. One quick question: do you see any issues with using this VRF setup in a PoS chain where validator sets rotate frequently? Curious how the keypair binding would work with ephemeral keys or delegations.

---

**arianaraghi** (2025-07-23):

Hey [@71104](/u/71104) ,

Fantastic work in your explanation.

I have recently proposed EIP-7956. In summary, I proposed a deterministic way to order transactions within a block (after a subset is chosen freely by the builder), using a randomness. Since VRFs were not inherently supported, I proposed using RANDAO’s random number generation from the consensus layer (beacon chain) for each slot.

Note that this requires a separate EIP to propose adding RANDAO to this layer, or at least a clear per-slot connection between the two layers.

I was wondering that have you considered proposing this VRF to be added to the Ethereum, or can I have the permission to add this as the companion EIP to my previous EIP-7956, instead of engaging RANDAO for each slot?

Also, if it is ok with you, I want to have your name in the EIP, and have your help designing the EIP in a better way.

Thanks in advance.

---

**71104** (2025-07-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/jonhubby/48/20094_2.png) jonhubby:

> One quick question: do you see any issues with using this VRF setup in a PoS chain where validator sets rotate frequently? Curious how the keypair binding would work with ephemeral keys or delegations.

I’m not sure what you mean but the keypair must definitely **not** be ephemeral. It must be a keypair that the block builder has officially committed to since joining the network, such as the keypair of the wallet used to stake.

If that’s not the case it becomes possible for any node to try many different keypairs until they get a private key that just so happens to make the node a leader for the slot.

Note that using the keypair of your wallet is safe (as long as the VRF is implemented correctly and the nonce is unpredictable and fresh at every slot) because the proof is zero-knowledge, which in this context means it’s infeasible to recover the private key x from a VRF output. If you really want to add an extra layer of security you can engineer the network-joining protocol such that the node is required to commit to a public key when entering the network, but one way or another the keypair **must** be commited to.

---

**71104** (2025-07-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/arianaraghi/48/13038_2.png) aryaethn:

> […] Note that this requires a separate EIP to propose adding RANDAO to this layer, or at least a clear per-slot connection between the two layers.

I see the problem. That’s lots of extra complexity indeed.

![](https://ethresear.ch/user_avatar/ethresear.ch/arianaraghi/48/13038_2.png) aryaethn:

> I was wondering that have you considered proposing this VRF to be added to the Ethereum,

Actually no, I was kind of assuming the Ethereum folks were already on it…?

![](https://ethresear.ch/user_avatar/ethresear.ch/arianaraghi/48/13038_2.png) aryaethn:

> or can I have the permission to add this as the companion EIP to my previous EIP-7956, instead of engaging RANDAO for each slot?
> Also, if it is ok with you, I want to have your name in the EIP, and have your help designing the EIP in a better way.

Totally cool, I’ll send you a DM.

