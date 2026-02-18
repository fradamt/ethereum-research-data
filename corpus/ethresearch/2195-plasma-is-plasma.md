---
source: ethresearch
topic_id: 2195
title: Plasma is plasma :)
author: josojo
date: "2018-06-10"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-is-plasma/2195
views: 5884
likes: 4
posts_count: 9
---

# Plasma is plasma :)

**TL;DR**

We propose an alternative light-client concept for plasma chain clients. This solution requires clients to have even fewer resources (memory, CPU and bandwidth) as compared to plasma cash requirements. The solution is based on zk-snark.

**Background**

Plasma-cash brought a lot of innovation to light. Plasma cash eliminated confirm signatures, enabled a low resource validation of plasma chains for clients and tackled the mass exit network overload challenge. Just to name the biggest 3 advantages.

But the regular plasma is catching up. The [“More Viable Product”](https://ethresear.ch/t/more-viable-plasma/2160/) is eliminating confirm signatures for plasma as well. The mass exit network overload challenge can be tackled by longer exit periods (more than 2 weeks) and [great services](https://ethresear.ch/t/simple-fast-withdrawals/2128/).

This post shows how plasma can be implemented, such that the resource requirements for clients are even lower than in plasma cash using zk-snarks.

You see, plasma is not just catching up, plasma is plasma ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9) No more complicated coin splitting and merging or cash exchangers are required.

**Zk-snark abilities**

Let P be a program which takes two inputs. The first input i is meant to be public. The second input w is a witness which can be kept private. We use o for an output of P.

Given a program P, an input i and an output o, if a prover knows a witness w such that o = P(i, w) then the prover can produce a proof where:

- (space density)  The proof is very short (just a few hundred bytes even for a very large program; e.g. Zcash achieves 288 bytes)
- (time density) The proof verifies in time linear to the lengths of i and o ( and does not depend on w)
- (zero knowledge) The proof leaks nothing about the execution of P or the contents of w other than the existence of w

**Zk-snark for plasma**

Let’s change the concept from above for our purposes.

We set:

i = (i_1, i_2): I_1 is Merkle root hash of all valid, spendable utxo of our plasma chain and i_2 is the list of new deposits into the plasma chain and exits from it.

w = (w_1, w_2): w_1 is the list of valid spendable utxo, w_2 is the list of transactions of a plasma block.

o = (o_1, o_2): o_1 is the Merkle hash of the new valid, spendable utxo after processing the block’s transactions. o_2 is the Merkle hash of the w_2.

And furthermore we assume that P runs the following logic:

- check i == Merkle_root_hash(w_1)
- check that each transaction is signed correctly
- incorporates i_2 to the list of valid, spendable utxos w_1,
- check that for each transaction the inputs are valid
- updates with each transaction the valid, spendable utxos
- build the Merkle hash of the newest list of valid, spendable utxo after processing all transactions
- calculate the Merkle hash of all transaction processed.

With this setup, verification is very easy. For each block, the chain operator publishes o_1 to the root chain and publishes o_2 and the zk-snark proof of o=P(i,w) to all clients. For verifying a correct block transition from one block to another block, the clients only need to verify:

- zk-snark proof and o_2 is available
- o_2 coincides with the published hash to the root chain,
- zk-snark proof  for P(i,w) is valid, where i is o_1 from the previous block ( the hash of the previous list of valid, spendable utxos)

If the client checks only these 3 things, he knows, that his utxo was not spent and all utxos have a valid origin. Hence, he knows that he will be able to withdraw his utxos later. If any of these 3 checks fails, he is just supposed to withdraw his uxtos from the chain.

**Analysis**

This described solution keeps everything related to zk-snarks off the chain and hence doesn’t cost any gas, in contrast to other proposed solutions. The creation of these proofs is the most resource intense component, but it can be done by the central plasma chain operator. Verifying them can be done very, very efficiently by the clients.

Currently, I am trying to implement this zk-snark protocol with this [library](https://github.com/scipr-lab/libsnark). If you see any challenges with this approach, please let me know.

edits:

If there is a new exit on the main chain, clients need to know that it is a legit exit. Hence, the chain operator could provide a Merkle proof that the exit is in current w_1. If the clients receive these Merkle proofs, all is good. But if the chain operator turns malicious, then everyone needs to get the data for the challenging process from somewhere else. So there needs to be at least some trust-worthy data centers, which are storing all transactions and are willing to distribute them later.

## Replies

**MaxC** (2018-06-10):

Hi Josojo, I had recently been writing up a spec for Zcash on Plasma. Would be great to collaborate and discuss. Although, I feel our proposals are trying to achieve different things.

---

**ldct** (2018-06-10):

What is the exit game for this chain?

---

**josojo** (2018-06-10):

[@MaxC](/u/maxc) sure, send you pm

[@ldct](/u/ldct)

That is the beauty. You do not need to change anything about the actual implementation of the plasma mvp or “more viable product”.

It’s just that the central plasma operator can create the proofs as described additionally and the clients can be sure that they can withdraw their coins later. Clients no longer need to verify all data of a block, just the proof. In case the proof is not correct or there is a data unavailability, we can not use this information to slash the operator since proofs were completely offline. But the client knows that he has to leave the plasma chain. That is all we need.

---

**MaxC** (2018-06-10):

I had been writing up a spec for a plasma thing.

---

**3esmit** (2018-06-10):

This would make possible for the witness proofing a balance in past block times?

I’m looking forward a plasma contract which can provide proofs for requests like this from MiniMeToken https://github.com/status-im/contracts/blob/minimetoken/contracts/token/MiniMeToken.sol#L338-L351

That are extremely useful for governance.

The Plasma contract should be albe to check if an account had an certain amount of value in balance at determined block.

MiniMeToken interface is:

```auto
function balanceOfAt(address _who, uint256 _block) public view returns (uint256 balance)
```

Plasma contract interface should be:

```auto
function balanceOfAtIs(address _who, uint256 _block, uint256 _balance, bytes32 _witness) public view returns (bool valid)

```

`bytes32 _witness` is unsure, depends on the implementation type, but in order to verify the parameters probably some proof would be needed for calculating against the balance and merkle tree.

---

**josojo** (2018-06-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/3esmit/48/503_2.png) 3esmit:

> This would make possible for the witness proofing a balance in past block times?

The information would be available in the hash of w_2. Yes. But unfortunately, the list of all spendable, valid utxos will probably very long and the depth of the Merkle tree will be very high. If the Merkle proofs are too long, solidity will not handle them well( or gas costs would be very high). That is why I proposed to keep w_2 off-chain anyways.

But if you are interested in this kind of plasma, maybe one can do it by not requiring the whole Merkle proof in one solidity call, but playing a trueBit game for the Merkle-proof.

Yes, for governance these kind thoughts are very interseting.

---

**ldct** (2018-06-11):

I’ll try to summarize this proposal, correct me if I’m wrong: you replace client verification of validity of the plasma chain (necessary for security in plasma mvp) with client verification of a snark, provided by the operator, of validity of the plasma chain, together with the existence of a trusted third party that replicates previously available plasma transactions.

---

**3esmit** (2018-06-12):

I think this is an interesting proposal, because we might be able to use this to make contracts read from plasma state.

I would like to see some interface to check user balances (if possible also past block states), so the markle root can be used to proof at other contracts that some user have some balance in that Plasma contract.

My intention is to use the plasma chain deposits as voting power. Looking forward example implementations so I can tryout ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

