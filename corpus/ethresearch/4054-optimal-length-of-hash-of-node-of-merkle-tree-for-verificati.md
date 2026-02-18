---
source: ethresearch
topic_id: 4054
title: Optimal length of hash of node of merkle tree for verification in smart contract
author: kowalski
date: "2018-11-01"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/optimal-length-of-hash-of-node-of-merkle-tree-for-verification-in-smart-contract/4054
views: 1858
likes: 4
posts_count: 9
---

# Optimal length of hash of node of merkle tree for verification in smart contract

My problem is rather simple. I want to create a smart contract which will hold a merkle root committing it’s state with internal book-keeping. Clients who interact with this contract will need to send a merkle branch on which their action is based.

Lets say that the internal book keeping consists of 1024 data-points of `uint256` type.

Most obvious approach that comes to me is to use as hashing function  H_{1}(a,b) = keccak256(a, b), which  returns `unit256`. A client who wants to prove to smart contract a data point will need to provide 640 bytes, calculated as:

2 \cdot 10 \; \textrm{levels} \cdot 32 \; \textrm{bytes} = 640 \; \textrm{bytes}

640 bytes is not terrible, but  I want to make the system as gas-efficient as possible, so I’m looking to possibly use smaller hashes.

Somewhat attractive approach would be to use as hashing function  H_{2}(a,b) = bytes4(keccak256(a, b)).

For H_{2} the size of the proof for merkle tree with 1024 leafs would be:

2 \cdot 32\;\textrm{bytes} + 2 \cdot 9 \; \textrm{levels} \cdot 4 \; \textrm{bytes} = 136 \; \textrm{bytes}

Which sounds much better.

So I have few questions regarding the scheme above, perhaps someone can point me to some research on the subject.

1. Is H_{2} secure enough, can an attacker efficiently falsify a merkle branch using brute force ?
2. If H_{2} is not secure, does anyone know what is practical minimal length of hash that can be considered secure for this problem ?
3. Perhaps someone knows even better hashing function for this problem? By “better” I mean more secure and gas-efficient.

## Replies

**jfdelgad** (2018-11-01):

This is interesting, however, If the users are sending transactions to update the books (for instance transferring to other users which involve updating two leaves) sending 640 bytes cost about 45000 gas and in the case of 136 bytes the cost is about 9500, updating the book a mapping of addresses to uint256 will cost about 10000 gas.

---

**kowalski** (2018-11-01):

[@jfdelgad](/u/jfdelgad) your calculations regarding the gas are correct. Additional thing to consider is that in smart contract I need to verify the merkle branch, which for H_{2} will cost about 100 gas per tree level  (+1000 gas for 1024 leafs) and send tokens, which adds another 21k give or take.  All in all, the full transaction cost is estimated to about 60k gas, which I think is bearable. The major question remains if H_{2} is secure against brute force attack.

Also, in my case, users will not be able to update the books. I’m merely building a one-way one-to-many reward mechanism. Few thousand people is rewarded daily but need to cover the transaction costs to actually have tokens transferred to their mainnet account.

The above is accomplished by having an oracle updating the contract with the merkle root of a daily snapshot of sum of rewards per address calculated from the beginning of time.

What users do with their tokens after withdrawing their rewards on mainnet is entirely their business. So this isn’t really a state channel, just a very simple subset of it.

---

**jfdelgad** (2018-11-01):

I understand now. Event the case of the 640 bytes seems manageable. A possible solution to the merkle proof is to use accumulators but seems like a over complication for your case.

---

**technocrypto** (2018-11-01):

Very minor point here, but what this is a subset of is Plasma.  State channels doesn’t just mean any off-chain technique, it is specifically the one where parties update by unanimous agreement.  The merkle proof technique here is the way Plasma works (or rather, like you mentioned, a small subset of it). Plasma and state channels are very different from each other:  for a technical summary of the differences the FAQ answer [here](https://www.counterfactual.com/statechannels/) is a good start.

---

**kowalski** (2018-11-02):

You’re right Jeff. I see now that what I’m aiming at is more similar to Plasma (babyplasma?) than state channels.

I guess I will change the tag of this topic to match that because I still need an advice of someone with experience with hashing functions.

---

**vbuterin** (2018-11-03):

H_2 will **not** be secure against brute force. You will be able to find a collision in \approx \sqrt{2^{32}} = 65536 steps, or a preimage in 2^{32} \approx 4.3 * 10^9 steps. The 32 byte length is unfortunately unavoidable.

---

**kowalski** (2018-11-03):

Thank you Vitalik for your input.

Would I be correct to say that  H_1  is the best choice of hashing function for a merkle tree that is to be verified on EVM ? Are you aware of any other option that could be a viable candidate and potentially lower gas consumption ?

---

**vbuterin** (2018-11-03):

Keccak256 is indeed lowest for gas consumption of on-chain computation.

