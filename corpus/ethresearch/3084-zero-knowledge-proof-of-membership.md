---
source: ethresearch
topic_id: 3084
title: Zero-Knowledge Proof of Membership
author: fubuloubu
date: "2018-08-25"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/zero-knowledge-proof-of-membership/3084
views: 4572
likes: 2
posts_count: 5
---

# Zero-Knowledge Proof of Membership

Myself and my co-conspirator Sean (who is not on this forum) are working on a project which aims to privately trade non-fungible assets. Our project has a particular need for the ability to prove membership of transaction participants in a public whitelist in order to ensure validity of the transaction. We are looking to do so without revealing the particular identity of each participant through utilizing a zero-knowledge proof. We are both exploring zk-SNARKs to this end, and do not know of a method to do this in the prior literature. (Please point us in the right direction if there is!)

---

We came up with a construction of how to do this tonight and wanted to run it past the community to understand if there are any flaws in the construction. It requires:

1. The root of a Merkle Tree for this membership list that is agreed upon by all parties (public parameter)
2. A fixed depth to that tree (constant; e.g. depth of 32)
3. A Merkle proof of an identity (represented by a Public Key) in this list (private parameter)
4. The private key corresponding to the PubKey in the proof (private parameter)

---

Merkle Proof, for reference:

[![image](https://ethresear.ch/uploads/default/original/2X/c/c5681e567187053ee3691f1969e8b0b9087ac5af.jpeg)qYBPm.jpeg600×338 26.8 KB](https://ethresear.ch/uploads/default/c5681e567187053ee3691f1969e8b0b9087ac5af)

The construction of the zk-SNARK would be as follows:

1. Given H_{ABCDEFGH} (public), prove that HASH(H_{ABCD}, H_{EFGH}) is equal
2. Assuming above holds, prove that H_{ABCD} == HASH(H_{AB}, H_{CD})
3. Repeat 2) for up to the depth of the tree (known prior to proof construction)
4. Prove the hash of the Public Key (T_D, secret parameter) is equal to H_D
5. Finally, prove the Private Key (secret parameter) is associated with the given Public Key T_D.

---

A bit of an explanation as to why this would work is that each step in the zk-SNARK provides transitive trust properties to the next step in the process, creating an overall quality guarantee of the proof that is equal to the depth times the quality guarantee of zk-SNARKs in general (which is high, but not absolute). Since the network participants all know the root hash to start with, and trust the algorithm in the zk-SNARK to evaluate the merkle proof, they can trust that each step in the process of handling the Merkle Proof validation builds upon trust of the prior and finalize to the node that is only known to the prover. The last step proves the knowledge of the secret information necessary to show that the prover is indeed in control of the key of the node required for their Merkle Proof to be valid.

---

Excuse my lack of precise terminology for this outline, hopefully it is clear enough what the construction is here that it is possible to evaluate its correctness. If not, I can create a more formal edit when I have more time and sleep ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

## Replies

**dlubarov** (2018-08-25):

Looks good to me. What you describe is similar to the ZeroCash design. There’s a Merkle tree containing the ledger, where each leaf is essentially `commitment(pk, amount)`. Transactions are then proved to be valid inside a SNARK. The root is a public input, while `sk` and `amount` are private inputs. The “POUR” circuit computes `pk` from `sk`, computes a commitment which exists in the ledger, then gives a proof of membership.

Have you considered transparent NIZKP systems such as ZKBoo++, STARKs, or Bulletproofs? They would let you make the tree height dynamic, among other benefits.

Would this run on the EVM? If so, there are a few other projects working on an EVM implementation of SNARKs, like [@barryWhiteHat](/u/barrywhitehat)’s [Miximus](https://github.com/barryWhiteHat/miximus).

---

**fubuloubu** (2018-08-26):

Thanks for responding!

You’re right, the more I look into Zcash’s transaction structure the more I realize that Plasma Cash is very similar, using commitments instead of addresses. We’re hoping to augment that structure with additional zk proof of membership that both parties in transaction are valid without revealing identity.

You are indeed correct that these membership lists would be maintained on Ethereum, such that the snark would have to be computable on Ethereum in order to facilitate Plasma Exits. I was thinking of an alternative structure where the exiting party (who is known anyways from submitting the transaction) would simply provide full knowledge proofs that match the zero knowledge transactions. We are still working on that part of the construction, but it is very interesting to just utilize the underlying zk-structure in the Plasma Exits (if possible)

I haven’t heard about ZKBoo++, will look into them. Still getting up to speed on STARKs and Bulletproofs. Miximus is a good reference I will explore further. Thanks for the suggestions!

---

**gakonst** (2018-08-26):

Is it correct to say that the goal of this is to create a constant size succinct Proof of Membership which can be verified cheaply, contrary to having a Merkle Proof of Membership which requires O(lgN) hashes to verify (where the tree has 2^N elements)?

Thinking of this in Plasma Cash context, there is a requirement of proving the non-inclusion of data in a specific index of the merkle tree (more specifically, prove a coin which is residing at a certain index of the tree was not spent in a list of blocks). Currently, this is done by providing a full merkle proof for the coin, for each block. Do you see a way to do a recursive proof for a number of different blocks that is smaller than the size of the non-inclusion proofs? (which also scale with the number of blocks generated)

---

**fubuloubu** (2018-08-26):

I’m not sure my structure for an inclusion proof would work for an exclusion proof. What the above basically states is “I have secret information that proves I am some leaf in the tree, and I can prove that leaf is in the tree via a non-trivial pathway from the roothash”. An exclusion proof would be “the ownership of this specific leaf has not changed” which must be provided for all leaves on a regular basis. I agree that a succinct exclusion proof would be very useful.

I’m still trying to understand the requirement for exclusion proofs in Plasma Cash. I know it has to do with exit procedures, and our exit procedures are being designed with different incentives than most financial applications. Trying to understand how they fit together.

