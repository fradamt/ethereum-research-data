---
source: ethresearch
topic_id: 11216
title: Comment on Three Attacks on Proof-of-Stake Ethereum
author: kladkogex
date: "2021-11-08"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/comment-on-three-attacks-on-proof-of-stake-ethereum/11216
views: 3144
likes: 3
posts_count: 9
---

# Comment on Three Attacks on Proof-of-Stake Ethereum

It was interesting to read the paper

https://arxiv.org/pdf/2110.10086.pdf

It provides descriptions of attacks but does not make general conclusions and does not discuss the fact,  whether the attacks are fixable at all.

The comment that I would like is very simple and I have been making it already for several years.

The consensus used in ETH2 has never had a proof of finite time finality. This means that one can prove that it is live, but one can not prove that it will actually finalize a block in finite time.

Moreover, there is a general argument that the attacker will always be able to keep the consensus from finalizing nomatter what the fix is.

The argument simply comes from the fact, that mathematically provable binary consensus algorithms known in this universe have n^2 behavior, and ETH2 is linear in n.

Therefore,  the only way to really fix ETH2 is to make it n^2.  Otherwise it is unfixable from the math point of view.  There will always be another attack.

It may be that by continuing patching a fix after a fix after a fix one can end up with something that will work from an engineering point of view.

This will be security by obscurity.

But it will not be secure from the math point of view.

## Replies

**dankrad** (2021-11-17):

The reason that Ethereum’s consensus can run in n time rather than n^2 is BLS signature aggregation. The attacks in the paper however aren’t attacks on signature aggregation. So I don’t think your argument is valid.

Just because something isn’t described in literature doesn’t mean it can’t exist ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=10) I think that you can modify existing consensus algorithms to only require O(n) complexity by adding signature aggregation. However, you’ve got to be quite careful to ensure that the aggregation algorithm terminates and can’t easily be DOSed. Do you see a reason why this cannot be done?

---

**adlerjohn** (2021-11-18):

I can’t believe I’m doing this (getting in the way of you dismantling the OP’s arguments, that is), but…

> However, you’ve got to be quite careful to ensure that the aggregation algorithm terminates and can’t easily be DOSed. Do you see a reason why this cannot be done?

This is something where the burden of proof is on the claimant that such a protocol can be done, since it’s an extraordinary claim. I have yet to see a signature aggregation protocol that isn’t either directly DoSable, or introduces an easy way for a passive adversary to deanonymize participants, or requires a very very slow mixnet/tor or something.

---

**dankrad** (2021-11-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> or requires a very very slow mixnet/tor or something

Well seems like you’ve answered your own question. If O(n) signature aggregation exists, then O(n) consensus protocol exists. OP claimed those don’t exist, therefore FFG must be broken.

---

**kladkogex** (2021-11-25):

Guys - the fact that minimum running time of binary consensus is N^2  does not come from BLS.

Many existing provably secure binary consensus algorithms use BLS and are still N^2

N^2 comes simply from the fact that each node needs to contact each other node at least once.

---

**SebastianElvis** (2021-11-26):

The O(n^2) lower bound of deterministic consensus protocols has been proven by [Dolev and Reischuk](https://www.cs.huji.ac.il/~dolev/pubs/p132-dolev.pdf) back to 1985. The intuition is that to finalise a block, a quorum (i.e., 2f+1) of nodes need to obtain a quorum of votes. Any effort to build a linear deterministic consensus protocol eventually turns out to have some issues.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> If O(n) signature aggregation exists, then O(n) consensus protocol exists. OP claimed those don’t exist, therefore FFG must be broken.

By O(n) signature aggregation I assume you mean the communication complexity of signature aggregation. As deterministic consensus requires every node to aggregate O(n) signatures to a single aggregated one, the total communication complexity will be O(n^2).

![](https://ethresear.ch/user_avatar/ethresear.ch/levs57/48/7254_2.png) levs57:

> The fact that every node needs to communicate with ~everyone (>2/3) doesn’t enforce O(N^2) O(N2)O(N^2) , because they communicate indirectly, over their peers, and this communication is compressed using BLS aggregation.

Even with p2p communication, every node needs to receive O(n) signatures from peers in order to obtain a quorum of votes. The communication cost of all-to-all broadcast remains O(n^2) and cannot be compressed. The aggregate signature only allows to produce a constant-size and publicly verifiable quorum certificate.

---

**levs57** (2021-11-26):

Excuse me, I think your argument does not work. Sending aggregated signatures along binary tree to the leader clearly does allow for non fault tolerant O(n) total communication.

---

**SebastianElvis** (2021-11-26):

This is true if the network is structured, i.e., has a special topology. However, this is not always the case, especially in permissionless blockchains where nodes are equal and find peers randomly.

---

**kladkogex** (2021-12-03):

Well the entire point is that noone has proven liveliness of ETH2.

I personally think that ETH2 is not live under normal mathematical assumptions of asynchronous model. The attacker can keep it from finalizing forever. To do it the attacker simply needs to keep two competing alternative branches.

If ETH2 were live, then it would provide O(N) consensus which is impossible mathematically.

Note that ETH2 has never had a competition to keep it from finalizing by controlling 1/3 of validators.

There is no proof and there was never any kind of at least real life simulation.

