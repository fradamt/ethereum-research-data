---
source: ethresearch
topic_id: 1073
title: Proof of Visibility for Data Availability
author: MaxC
date: "2018-02-13"
category: Sharding
tags: []
url: https://ethresear.ch/t/proof-of-visibility-for-data-availability/1073
views: 2980
likes: 0
posts_count: 3
---

# Proof of Visibility for Data Availability

[@JustinDrake](/u/justindrake) [@vbuterin](/u/vbuterin)

Suppose the proposers and validators for a shard have been bribed by an attacker.

They no longer **publicly** sign off on or propose collation bodies or headers within their shard.

At the end of an epoch, the validators share with other shards a new merkle root for a set of transactions, Tx, that have been unwitnessed by honest members a shard.

Since no block Tx was signed and given to members of the shard, there can be no fraud proof against the shard for its actions. In fact, we don’t even know whether Tx is valid or not.

To help solve this problem, we propose the following proof of visibility scheme:

It uses:

(1) Proof of Custody [Justin’s post](https://ethresear.ch/t/enforcing-windback-validity-and-availability-and-a-proof-of-custody/949)

In proof of custody a user may present a ZK proof that:

D = \textrm{SHA3}((Tx[0]\oplus P) \hspace{1mm}\oplus\hspace{1mm} ... \hspace{1mm}\oplus\hspace{1mm} \textrm{SHA3}(Tx[n] \oplus P)).

We can modify this so that the ZK proof is also based on public randomness, R,  which is changed each epoch and the user’s secret key S.  We also use a commitment to the hash of Tx, H.

Present a  ZK proof that:

D = \textrm{SHA3}((R\oplus Tx[0]\oplus S) \hspace{1mm}\oplus\hspace{1mm} ... \hspace{1mm}\oplus\hspace{1mm} \textrm{SHA3}(Tx[n] \oplus S)).

S is the secret key of some P.

Tx or its hash is signed by the validators

\mathrm{Hash[Tx] =H}

Note: the randomness is generated after \mathrm{Hash[Tx] =H} is committed and broadcast to the network/other shards.

This is to ensure that the attacker can’t just change Tx for a given public and secret key (P, S) until a valid proof is found.

We also require that the digest D has 3 zeros as its least significant figures.

Now,  with all this anyone presenting such a ZK proof will be one in a thousand. By that we mean, for an attacker to acquire such a proof, he must have bribed 1000 participants on average, presenting a TX block to all of them. (A participant will not know whether they can create the proof before they have Tx,  randomness R, and have combined it with their private key S).

Giving their private keys S to the attacker for him to compute the digest is a highly risky endeavour, so the participants will not do so.

Whereas an attacker must have spread his funds over 1000 members,  to generate a proof of visibility, we can instead issue a high block reward to the first person who produces proof of invalidity in Tx. Thus, a person will be more highly incentivised to report a faulty Tx or multiple Txs than take the attacker’s bribe (by a factor of 1000 to 1 assuming equal funds).

Under the honest minority assumption, it is also likely the case that  a member of the community disseminates Tx to the wider public for scrutiny even without financial incentivisation.

Modifications of this scheme may also be useful for aggregating votes efficiently, and may even help with super-quadratic sharding.

NB: This scheme should be less computationally intensive than presenting a zero knowledge proof that:

(1) All the transactions in Tx are valid

(2) The transactions in Tx are related to a merkle root M

And note: given a proof of visibility, some honest node with high probability has Tx, from which anyone can compute a valid Merkle root M’, and compare that with  the M broadcast by validators

## Replies

**JustinDrake** (2018-02-13):

Thanks for the post Max. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) I don’t understand the problem you are proposing a solution for.

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> They no longer publicly sign off on or propose collation bodies or headers within their shard.

Privately signing off on collation headers (without submitting the collation headers to the main shard) is useless for attackers because the VMC has well-defined periods during which validators can submit collation headers.

Bribing validators for not submitting collation headers for a child shard sounds like the context for a possible stalling, censorship and/or takeover attack.

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> a new merkle root for a set of transactions, Tx, that have been unwitnessed by honest members a shard

The fork choice rule for honest validators is to only build upon collation headers for which the collation bodies are available. Because of validator shuffling and the honest majority assumption, the dominant collation header chain will have available collation bodies.

---

**MaxC** (2018-02-13):

Thanks Justin,

I realise that random shuffling of validators is a good way to resolve the bribed validator problem, coupled with a **large block height** before any cross-shard sharing of state.

I wanted to explore a way of sharing state between shards that would make transaction-finality quicker (i.e. by not having a large block height).

Instead of signing off and sharing the merkle state root for a block at height h with other shards, you can share the state of a more recent block (height =1 or 2) if there is a proof that many other people have seen that block.

If the most recent block is erroneous and has been shared with many people, a fraud proof will be easily generated. So the problem is one of data-availability- has the block been seen yet or not.

The other shards can do  things like sample active members of a shard, asking which block was the most recently seen.

However, my solution was to present a proof that the transaction block may be expected to have been seen by a large number of people with a relatively small ZK proof.

Hope this clarifies, I’m not sure about all of the inner workings of the sharding protocol, but understand more through reading your comments. Thanks.

