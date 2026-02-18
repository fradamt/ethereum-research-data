---
source: ethresearch
topic_id: 22749
title: "Incendia: On‑Chain Anonymous Voting via Proof‑of‑Burn"
author: pardis-toolabi
date: "2025-07-16"
category: Privacy
tags: []
url: https://ethresear.ch/t/incendia-on-chain-anonymous-voting-via-proof-of-burn/22749
views: 545
likes: 14
posts_count: 16
---

# Incendia: On‑Chain Anonymous Voting via Proof‑of‑Burn

We have recently published a paper  “Burn Your Vote”,

Proposing a protocol in which voters “burn tokens” to pseudorandom addresses and submit zk‑SNARK proofs to prove a valid burn, achieving vote integrity, coercion resistance, and unlinkability with minimal gas overhead

No FHE, No MPC, No TLP, No heavy computation.

You can explore the code here:

[GitHub ‑ Proof‑of‑Burn Voting](https://github.com/zero-savvy/burn-to-vote)

For a high‑level overview, see our paper:

[Eprint ‑ Proof‑of‑Burn Voting](https://eprint.iacr.org/2025/1022)

Why Burn Your Vote?

Current DAO voting tools either expose ballot choices, rely on heavy off‑chain MPC/FHE, or introduce trusted coordinators. Burn Your Vote plugs that gap by:

True On‑Chain Tallying: All proof verification and vote aggregation occur in smart contracts—no off‑chain authorities needed .

Privacy & Unlinkability: Voters burn tokens to pseudorandom addresses and submit zk‑SNARK proofs of a valid burn; tallies operate on plaintext votes but remain unlinkable to identities .

Coercion Resistance: Unlinkable burns + optional revoting let voters plausibly deny coerced ballots.

Scalable Performance: Constant‑time tally gas (~27 k) even at million‑voter scale—significantly lower than HTLP‑based systems like Cicada.

Reaserch focus:

Reducing Proving Time:

Right now we’re on Circom + Groth16 + rapid-snark clocking in at ~37 s per proof. We’ll look into what happens if we switch to Noir—can’t use rapid-snark there—so we’ll scope out other backends (Halo2/PLONK variants, GPU acceleration, incremental proving) or pipeline tricks to cut that down.

Receipt‑Freeness Feasibility:

Since we cant have protocol‑level randomness to add to the users proof to make it receipt‑free , we’ll explore if we can get real receipt‑freeness without breaking the system.(biggest challenge)

Circuit Optimization:

Current counts:

447 template instances

8,485,140 non‑linear constraints

3,898,619 linear constraints

We’ll try to slim down our circuits speacially heavy Merkle patricia trie since for each layer of the trie we have one keccak and one rlp.

## Replies

**lovely-necromancer** (2025-07-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/pardis-toolabi/48/20538_2.png) pardis-toolabi:

> Receipt‑Freeness Feasibility

I wonder how we can reasonably achieve this without bringing encryption or centralized coordinators into the prootocol.

---

**pardis-toolabi** (2025-07-18):

How about this


      ![](https://ethresear.ch/uploads/default/original/3X/a/1/a11e01de2c742fe17376c9d23ef0767dbe6a74c0.png)

      [Paradigm – 12 Jan 23](https://www.paradigm.xyz/2023/01/eth-rng)



    ![](https://ethresear.ch/uploads/default/optimized/3X/3/6/360770a9efee944df50e7385152367cca2f087bb_2_690x388.png)

###



Generating secure randomness on Ethereum using SNARKs










possibly the closest thing to on-chain randomness

---

**71104** (2025-07-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/pardis-toolabi/48/20538_2.png) pardis-toolabi:

> How about this
>
>
> Generating secure randomness on Ethereum using SNARKs - Paradigm
>
>
> possibly the closest thing to on-chain randomness

At this point I understand that Ethereum has plans to migrate to SSLE (single secret leader election) based on a VRF with DDH construction, which carries a zero-knowledge proof that’s much cheaper than a whole zk-SNARK. Wouldn’t a similar approach be better?

---

**Game111-cyber** (2025-07-18):

Hi I am interested in the concept of proof of burn, but I’ve got a few questions.

- When switching to Noir or other proving systems, how much improvement do you anticipate in proof generation time?
- Given the constraints of not introducing protocol-level randomness, what potential technical challenges and solutions do you see in achieving true receipt-free voting?
- Considering the current complexity of your circuits, especially the heavy computation in the Merkle Patricia Trie, what specific optimizations are you planning to explore?

---

**71104** (2025-07-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/pardis-toolabi/48/20538_2.png) pardis-toolabi:

> How about this
>
>
> Generating secure randomness on Ethereum using SNARKs - Paradigm
>
>
> possibly the closest thing to on-chain randomness

I’ve just started [this thread](https://ethresear.ch/t/vrfs-and-single-secret-leader-election/22787) about a much simpler VRF construction. It’s mainly focused on leader election but has some final considerations for use in dApps.

---

**rahul-kothari** (2025-07-23):

The burn address and nullifier depend on a random blinding commitment beta.

But to prevent double spending, the next time I try to re-vote, how does the system ensure I create the same beta?

NBecause if the beta is different, my nullifier would be different, allowing me to double-vote

---

**MichaelConnor** (2025-07-23):

Similar (but different) Q to Rahul’s above.

A user can cast multiple votes, for coercion resistance. But then they ultimately need to choose one of those votes to be tallied. We don’t want a single user to contribute multiple of their different votes to the tally.

I don’t see an explanation in the paper that explains how we ensure a user can only contribute once to the tally. The nullifiier definition (pictured) certainly doesn’t prevent this.

[![image](https://ethresear.ch/uploads/default/original/3X/6/c/6cc0c2472335bb1ae314b8781efd4ab6f5e60aae.png)image858×204 19.2 KB](https://ethresear.ch/uploads/default/6cc0c2472335bb1ae314b8781efd4ab6f5e60aae)

![image](https://ethresear.ch/uploads/default/original/3X/5/6/5698ffa2af3e257bd0c61324b83c0061ef5e5890.png)

---

**pardis-toolabi** (2025-07-23):

Thank you, I will check it out

---

**pardis-toolabi** (2025-07-23):

Great question,

Each user has to provide a prove of inclusion in the allow list merkle tree, and the same beta that user commited to in the burn address and nullifier is used in the registration phase to create the merkle tree leaf and in the implementation we make sure all the values(nullifier randomness, burn address randomness, mt leaf randomness) are the same,

So if a user changes the beta to create a new nullifier they won’t even be able to generate the proof as it fails at the equality assertions in the witness generation phase.



      [github.com/zero-savvy/burn-to-vote](https://github.com/zero-savvy/burn-to-vote/blob/3e9e3293481a9f40b0b0d02afa6f3feb0ec60bc0/circuits/vote.circom#L108)





####

  [3e9e32934](https://github.com/zero-savvy/burn-to-vote/blob/3e9e3293481a9f40b0b0d02afa6f3feb0ec60bc0/circuits/vote.circom#L108)



```circom


1. signal input mt_leaf;
2. signal input mt_pathElements[2];
3. signal input mt_pathIndices[2];
4.
5. component merkle_tree_inclusion = MerkleTreeChecker(2);
6. merkle_tree_inclusion.leaf <== mt_leaf;
7. merkle_tree_inclusion.pathElements <== mt_pathElements;
8. merkle_tree_inclusion.pathIndices <== mt_pathIndices;
9.
10. mt_root === merkle_tree_inclusion.root ;
11. mt_leaf === burn_address.secret_commitment;
12.
13.
14.
15.
16. log("nullifier check ... ");
17.
18. component nullifier_generator = Nullifier();
19. nullifier_generator.secret <== secret;
20. nullifier_generator.blindingFactor <== blinding_factor;
21. nullifier_generator.ceremonyID <== ceremonyID;


```










[![image](https://ethresear.ch/uploads/default/original/3X/c/6/c6c68cd0acb42ac8fd46ca00dc974a78426b02ac.png)image978×394 31.7 KB](https://ethresear.ch/uploads/default/c6c68cd0acb42ac8fd46ca00dc974a78426b02ac)

---

**pardis-toolabi** (2025-07-23):

Great question,

We use a merkle tree registration to bound each user to one vote and one revote, so each user has the ability vote as much as they like, but when it comes to submission they are bound by their commitment to the allow list.

[![image](https://ethresear.ch/uploads/default/original/3X/c/6/c6c68cd0acb42ac8fd46ca00dc974a78426b02ac.png)image978×394 31.7 KB](https://ethresear.ch/uploads/default/c6c68cd0acb42ac8fd46ca00dc974a78426b02ac)

---

**pardis-toolabi** (2025-07-23):

Great questions,

1. we can not say for sure until it’s finished but I would like to think we achieve 20 - 30% faster proving time, and also we have to keep in mind that the proof size is going to be higher with noir and bb so we still weighing options
2. by definition to achieve receipt freeness the user should not be able to reconstruct the proof by themself so that means that we need a input signal unknown to the user but we can’t provide that the signal as the protocol should be 100 percent trustless, and also we need that random signal to be generated trustless without heavy cryptography schemes and calculation
3. we are reviewing our implementation to pin point extra loops and messy calculations into cleaner smarter ones since changing the base implementation of the state trie is not possible.

---

**oxlumi** (2025-07-23):

Heyo! Great paper : ) Some questions and considerations came to my mind while reading:

1. In terms of receipt-freeness, the user knows β and can show it to an external coercer to demonstrate which vote they cast. But, what practical paths could be explored to inject trustless randomness into β, such that it’s unknown even to the voter, without introducing a trusted party, assuming we avoid full-fledged FHE or MPC? This question arises because, if a voter uses a frontend that includes blockhash randomness to submit their vote, it eliminates predictability but could subject users to front-running. How might such randomness be injected verifiably?
2. In the forum, it’s mentioned that β is also used in the allow-list Merkle leaf and that if mismatched, the proof fails, which is actually quite clever for binding identity. But, now suppose a DAO runs multiple votes over time, each with different voter sets. If a user reuses β across ceremonies, could this be used to link behaviors over time or something similar?
3. From the paper and the discussion below, it’s clear that the largest proof bottleneck is in MPT. I was thinking… if a rollup runs with Poseidon SMTs instead of MPT+Keccak, would the current circuit design entirely break, or could it be modularized to drop in a new state commitment format?
4. It was mentioned that the protocol supports revoting during the voting phase. How does the on-chain logic handle two revote transactions with the same nullifier arriving in the same block (via MEV or bad relayers, for example)? How is finality determined in such cases?
5. Could a VRF-voter keypair (ECDSA or EdDSA + randomness proof) serve as the basis for generating untrusted β, which could then be verified in-circuit?

Looking forward to following the discussion : )

---

**lovely-necromancer** (2025-07-23):

Hey, thanks for the feedback ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

1. Since the user at some point has to generate a ZKP for knowing \beta or a deterministic relation to it (as the preimage of a one-way function, like poseidon-hash), it is not possible to achieve it without maybe introducing another entity.
2. in the paper, we just showed the simplest construction of \Lambda, the \beta can be alway easily concatenated with the unique ceremony id of each specific voting. Due to the hiding property of the commitment scheme (or if use Hash or PRF, we say the distinguishability of its output vs random oracle), it is not possible to catch a relation between these votes.
3. it is kinda pretty modular in that regard, but since for now we are using Groth16, it would require another setup ceremony in case of any changes to circuits.
4. The on-chain revoting requires a slightly different proof. its a trick within the proof, the user poves they’ve undone their previous vote (for instance if they voted 1, they prove they’ve now willing to change), if it’s within the same block, it will work normally if the revote is after the original vote. Otherwise, the revote will fail and the original vote will be successful.
5. I believe you are mentioning this to prevent attacks like front-running, then yes, it is possible. Because in terms of the pure security of the voting scheme itself, we are assuming that user is in charge of randomness of the \beta. It’s like a philosophical problem, if you want to vote even before voting gets started, it’s ok, it’s your vote. Of course, each voting ceremony can have their own rules applied on the custom cirtuits (like the VRF you mentioned). In theory, we can use anything for \beta given that the hash function or any commitment scheme that we use to construct \Lambda is secure (collision resistance in hash function, hiding/binding for commitments, . . .).

Happy to hear back (^_^)

---

**aguzmant103** (2025-07-24):

Interesting construction, thanks for sharing.

Do you envision this solution for onchain governance systems? Or what specific use case?

My main concern is adoption. I doubt the DAOs will want their governance tokens burned, as many projects tied their performance as ecosystem to their govenrance token.

---

**pardis-toolabi** (2025-07-25):

Thank you Andy :),

Since the design provides complete privacy without the usual suspects (FHE, MPC, TLP), It’s more scalable and suitable for real world use case like any voting and auction scenarios.

About the burning for DAOs there are two different ways it can go,

1. Since in the standard method we use the burn transaction just for the “burn address” and the “timestamp”, the burning amount can be any amount which means it can be a very very small amount  or even zero. (zero is NOT recommended).
2. We can use the governance tokens for allow list creation (verifying valid voters), and burn any other token or even the native coin of the chain.
WHY?
Because if you are burning a unique token (governance token) or amount (like zero), it can be used to detect voting transactions and compromise the hiding aspect, so the best option is to use a common coin/token that makes your vote transaction look like any other transaction in the chain.
PS: Because of the burning method there is zero contact with the protocols smart contract until the voting has ended, which creates another level of privacy on top of others.

