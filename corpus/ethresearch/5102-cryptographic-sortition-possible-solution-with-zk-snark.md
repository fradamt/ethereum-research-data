---
source: ethresearch
topic_id: 5102
title: "Cryptographic sortition: possible solution with zk-snark"
author: liochon
date: "2019-03-06"
category: Sharding
tags: []
url: https://ethresear.ch/t/cryptographic-sortition-possible-solution-with-zk-snark/5102
views: 4766
likes: 10
posts_count: 6
---

# Cryptographic sortition: possible solution with zk-snark

Algorand’s self selection (https://github.com/ethresearch/p2p/issues/5#issuecomment-441457619) has been considered as a protection against DoS attacks against block proposers (BPs). The goal is to choose a BP from a pool of eligible validators in such a way that only the current BP knows it has been selected. When it publishes a block, it simultaneously publishes a proof showing that it is indeed the current BP.

Algorand’s protocol cannot be used as a means to reliably select a single BP. For example, with a single BP to choose among 300 validators, Algorand would fail to select anyone with a probability ~36% and would select two or more BPs ~26% of the time.

We found a possible solution to secret self-selection using ZK-SNARK (ZK-STARK would work as well). Obvious caveat: it’s expensive.

So the goal is to select exactly one participant from a pool of many (possibly thousands) of eligible participants. We require the following setup:

- The list of all currently eligible participants is known in advance
- These participants are identified by their public keys.
- A random beacon is available.

We want to select one of these public keys in a way that only the owner of the public key knows it has been selected. For any round the random beacon emits a random number m which participants will need to sign.

A simple solution is having all participants:

- Sign the message m: signed(m)
- Send the hash of this message: hash(signed(m))

At this point we can sort the participants by their hash(signed(m)). With a random beacon r we can select one of the participants, by picking the one at position r modulo number of participants. While this position is known by all, only the owner of the corresponding public key can publish signed(m), hence prove it was selected. But nobody can guess who was selected before signed(m) is actually published.

This scheme has obvious issues: anyone can send data d and pretend it’s some hash(signed(m)). Thus a byzantine actor can crash the protocol by sending a lot of false data. Furthermore, since we want to keep these submissions anonymous (in particular: unsigned), there is no way of knowing whether data was produced by an eligible participant or someone else, nor whether it is the hash of a signature. We need to be sure that the hash(signed(m)) is legitimate, without identifying the participant. We also need to be sure that even a legitimate but byzantine participant cannot send invalid or multiple messages.

We use a ZK-SNARK (or ZK-STARK) to solve this. We put the eligible public keys in a Merkle tree. Participants will not only send their hash(signed(m)), but also a proof that they are an eligible participants and that the value they sent is valid. Hence there will be one proof per participant. Participants will prove that they own an eligible public key by providing the Merkle path of its public key. They will then prove that the message is actually signed by the corresponding private key.

Public parameters:

- A public random number m (emitted by the random beacon).
- The roothash of all the participants’ public keys: rh
- h = hash(signed(m))

Secret parameters:

- signed(m)
- The signer’s public key: pk
- Merkled path: mp

Checks performed by the ZK-SNARK:

- The public key belongs to one of the participants: the Merkle path mp leads from the public key pk to the root hash rh,
- signed(m) checks out against the public key pk and the random number m
- hash(signed(m)) given in the public parameters is the hash of signed(m) given in the secret parameters
- signed(m) in the secret parameters is the same m given in the public parameters.

Participants must send their public parameters along with the proof 𝜋. A message gets accepted if and only if the public parameters m and roothash are valid and the proof can be verified.

There is still one problem: we generate as many proofs as there are participants, and these proofs would all need to be included on chain and verified for each round. It’s possible to generate these proofs in advance without compromising security (eg. have a long delay between the publication of the random number m to sign and the time when proposals (h, 𝜋) are committed to the chain), but the workload remains.

There are two possible solutions here.

First, we can dramatically limit the number of proofs to be both generated and committed by combining this protocol with Micali’s protocol. This works by only accepting pairs (h, 𝜋) where (✶) hash(h) < t for a threshold t selected in such a way that with overwhelming probability (1) there will be a participant that satisfies (✶), and (2) (say) 20, 100 or 1000 participants will satisfy (✶), and hence be allowed to participate. As a result, even if there are thousands of possible participants, just a few of them will actually have to generate a proof. This is equivalent of creating a self selected committee whose members will be legitimate in submitting zk-snark proofs onto chain. Note that this implicitly creates a subcommittee of likely BPs that are aware of their increased odds, so they should be given a limited time to publish their proof.

A second, complementary solution, is to have all proposals (h, 𝜋) accepted, and to reuse them over several rounds, by excluding the previously selected participants. For example, we could have the first selection executed between 1000 participants, then the second between 999 participants, then 998 and so one until we have 980, 950 or 900 participants. Only at this point do we re-execute the protocol.

That’s the principles. We have not yet implemented it, but we plan to do a PoC of it. Before that, if you identify any potential problems or improvements, we’re interested! On paper, we find that this is a solution with acceptable drawbacks for several use cases.

Olivier Bégassat, Nicolas Liochon

## Replies

**Mikerah** (2019-07-09):

This is interesting.

One suggestion I have would perhaps consider using polynomial commitments in the snark instead of merkle trees. Polynomial commitments are still expensive within a snark but not as expensive as merkle trees.

---

**burdges** (2019-09-01):

How would polynomial commitments work?  You’d run an MPC to generate a common public polynomial P(x) = \sum_i x^i A_i for which P(j) returns the public key of the j th participant?

I suppose https://pdfs.semanticscholar.org/31eb/add7a0109a584cfbf94b3afaa3c117c78c91.pdf or similar perhaps

---

**nikkolasg** (2020-02-01):

> How would polynomial commitments work? You’d run an MPC to generate a common public polynomial P(x)=∑ixiAi for which P(j) returns the public key of the j th participant?

Couldn’t you use lagrange interpolation to derive such polynomial, from the indexed list of all valid miners?

Interestingly, there would be no need to post the polynomial coefficients on chain, since it would be derived from onchain information already.  The question of the efficiency of the interpolation is another matter though, but it may not be required to do it at each round.

---

**burdges** (2020-02-02):

You could secret share many polynomials with zeros at specific points, but afaik this needs O(n^2) bandwidth.  I also dislike privacy being tied to the threshold assumption.  It’s okay for validators, but prevents reusing the code elsewhere.  Also, you cannot necessarily reuse polynomial commitment in multiple proofs, at least in proof systems like bulletproofs.

If you’re going to run a DKG then you’d presumably run a group VRF variant of a group signature for sortition.  It’s far simpler and faster than the SNARK, IPP, etc. needed for a ring VRF or the circuit discussed here.  You only need the DKG for initial issuer key creation.

Any MPC like a DKG would impose higher engineering and maintenance costs though because MPCs require tight integration between the cryptography and the overall protocol.  A ring VRF otoh can be implemented and made missuse resistant by a couple crypto devs, so your protocol devs continue working at their normal much faster pace.

At least in polkadot, we continue chain growth under praos-like security assumptions if the finality gadget stalls, but your whole protocol halts if your DKG stalls.  A group VRF could delay this for several epochs, but remains messy.

---

**nikkolasg** (2020-02-15):

I’m not sure we talk about the same thing. Mikerah suggestion was to use a polynomial instead of a MT and you asked how to get that polynomial such that P(j) = P_j where P_j is the public key of the jth participant. All I am saying is that is easy to construct such polynomial *locally* (with Lagrange interpolation), given a list of participants and their respective index.

In the SNARK, I can then prove that the index j I use gives the public key P_j by evaluating this polynomial and then I sign on, for example, P_j || R (where R is the random beacon number) to show I own the private key.

I am not sure to understand why are you talking about DKG and threshold here.

