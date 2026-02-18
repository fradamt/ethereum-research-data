---
source: ethresearch
topic_id: 1888
title: Sharding designs compendium
author: jamesray1
date: "2018-05-01"
category: Sharding
tags: []
url: https://ethresear.ch/t/sharding-designs-compendium/1888
views: 4950
likes: 14
posts_count: 25
---

# Sharding designs compendium

I’ll make this post a community wiki, people can update this and https://github.com/ethereum/wiki/wiki/Alternative-blockchains,-randomness,-economics,-and-other-research-topics.

The wiki includes (with more details for each in the wiki):

- Dfinity
- Ziliqa
- PHANTOM and SPECTRE

---

RFC: SPECTRE and PHANTOM by Aviv Zohar and Yonatan Sompolinsky.

Introductory articles:

- https://medium.com/@avivzohar/the-spectre-protocol-7dbbebb707b5
- https://www.coindesk.com/spectre-creators-propose-phantom-blockchain-protocol/

I just read these articles, I haven’t had time to read the papers yet.

Papers:

- PHANTOM: https://eprint.iacr.org/2018/104.pdf
- SPECTRE: https://eprint.iacr.org/2016/1159.pdf

I see parallels between the discussions we have had on DAG design and voting. Thanks [@ChosunOne](/u/chosunone) for suggesting to read this.

---

Changelog:

- added Dfinity, Truebit, PHANTOM and SPECTRE with some details on each
- added other blockchains, e.g. Cardano, Algorand, OmniLedger
- added Snowflake to Avalanche: A Novel Metastable Consensus Protocol Family for Cryptocurrencies

## Replies

**naterush** (2018-05-02):

Thanks for the links! The same people also came up with [GHOST](http://www.avivz.net/pubs/15/btc_ghost_full.pdf), which I believe is the inspiration for the name “Casper” ![:stuck_out_tongue:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue.png?v=9) .

As a meta-question, any ideas on good ways of collecting papers that are maybe less taxing on communication channels than new threads? It’s great to collect them where people can read them, but I also think it might be good to limit the number of threads we start just based on papers that might be relevant, as there’s probably a ton.

---

**jamesray1** (2018-05-02):

Yeah, I realised about GHOST and Casper ;). You could put them in a wiki or hack MD note, and perhaps refer to it from a meta post on this site to increase the chance that people will see it.

https://github.com/ethereum/wiki/wiki

---

**maxvolt** (2018-05-03):

Interesting reads. I looked around for an implementation (the SPECTRE papers mentions that an optimized implementation **will be released**) but my search results came back dry from Github and DuckDuckGo. I then reached out to the author who recommended I look at [DAGlabs](https://www.daglabs.com/), who are currently building the implementation but I couldn’t find any open source code xD.

As an aside: I think its a great idea to collect interesting links together. Why not put them in a Github MD file like the `awesome` lists? You could make it `awesome-blockchain-papers` for instance.

---

**jamesray1** (2018-05-03):

![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) I added it to here: https://github.com/ethereum/wiki/wiki/Sharding-introduction-R&D-compendium#alternative-scaling-approaches-to-sharding.

---

**ns2808** (2018-05-03):

Thanks for sharing [@jamesray1](/u/jamesray1)

The Spectre paper claims that the protocol is ‘secure’ (as defined by them i.e. satisfying Properties 1-3) if the attacker controls less than 50% of the computational power.

I believe Lamprot, Shostak & Pease showed that this is only possible in a world without firewalls, else any distributed network is only safe if an attacker controls less than 1/3rd of the computational power.

(Theorem 3 in https://people.eecs.berkeley.edu/~luca/cs174/byzantine.pdf).

Do Sompolinsky and Zohar simply assume that there aren’t any firewalls? If not, how do they get to 50%?

---

**kladkogex** (2018-05-03):

Looking at the blog post they have a DAG not a blockchain

So there seem to be no global ordering of transactions and the theorem does not apply.

But if there is no global ordering,  you cant really run smart contracts on it …

---

**jamesray1** (2018-05-04):

Hence why they introduced PHANTOM, which has global ordering, AIUI.

---

**ChosunOne** (2018-05-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/ns2808/48/19637_2.png) ns2808:

> I believe Lamprot, Shostak & Pease showed that this is only possible in a world without firewalls, else any distributed network is only safe if an attacker controls less than 1/3rd of the computational power.
>
>
> (Theorem 3 in https://people.eecs.berkeley.edu/~luca/cs174/byzantine.pdf ).
>
>
> Do Sompolinsky and Zohar simply assume that there aren’t any firewalls? If not, how do they get to 50%?

Appendix E of the SPECTRE paper spends a significant amount of space to proving the security threshold, I suggest you look over it and see what assumptions they make and whether or not they are valid.  To my knowledge, they make no assumptions of firewalls, but I would like to see where that assumption is made implicitly.

---

**ChosunOne** (2018-05-04):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> But if there is no global ordering,  you cant really run smart contracts on it …

You can also deviate from their specification and create a past ordering ex post facto by combining the DAG into a summarized version that becomes a chain. You can have a separate rule for resolving cyclic precedence of transactions.

---

**kladkogex** (2018-05-04):

Re-read the  paper … The ordering these guys are proposing does not have any upper time bound so it is useless, since an attacker can make it arbitrary long.

Essentially there is no time T after which  you can assume a particular region of the chain to be stable. Therefore, the ordering is useless since an attacker can wait an arbitrary long time before screwing a particular part of the chain.

As [@ns2808](/u/ns2808) noted this thing if true would contradict existing proofs for consensus ordering.

---

**ChosunOne** (2018-05-04):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Essentially there is no time TT after which  you can assume a particular region of the chain to be stable. Therefore, the ordering is useless since an attacker can wait an arbitrary long time before screwing a particular part of the chain.

But this is only true for the attacker’s transactions.  Honest participants can get very high probability their activities will not be reversed very quickly.  You can attach a block to the genesis block, but that doesn’t mean the rest of the DAG will accept your block.  In fact, most of the blocks will vote against your block, so I don’t see how you can “screw with the chain” as easily as you make it sound.

---

**kladkogex** (2018-05-04):

Unfortunately you can not separate honest guys from bad guys.

If an unfinalized attacker transaction is at a later time finalized in front of a previously finalized honest user transaction, it could be a double spend or all kinds of other things.

Essentially for smart contracts to run one needs to have a chain which is reasonably settled and stable.

This comes to the point I guess that there is no free lunch.

For a usable consensus less than 1/3 of nodes can be byzantine, it is a math theorem.

If you relax that you get a mess which one hardly understands at all, and is, therefore, not secure.  Hashgraph is a good example.

---

**ChosunOne** (2018-05-04):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Unfortunately you can not separate honest guys from bad guys.
>
>
> If an unfinalized attacker transaction is at a later time finalized in front of a previously finalized honest user transaction, it could be a double spend or all kinds of other things.

I’m not sure I follow.  An attacker can be defined as trying to spend the same tokens twice.  If that happens, then as noted previously you cannot accept one of the transactions robustly.  If you add a rule to reject non-robustly accepted transactions after some period T, then you can resolve the double spend and it will fail.  If there is no double spend, then there is no conflict to cause the transaction to not be accepted robustly.

The only times where transactions are not accepted robustly is when a double spend is attempted, and the paper goes to considerable length to show that if an attacker does not have a majority hashpower they cannot create a DAG that is robustly accepted.

Could you perhaps explain what you mean in more detail?

---

**kladkogex** (2018-05-05):

This is what the paper  says at the end

“. It is of yet unclear whether we can further achieve a linear ordering without compromising the fast confirmation times.”

Things without linear ordering have little use, definitely before a smart contract runs you got to have linear ordering

Smart contracts are trusted programs that require linear ordering before operation.  Maybe one can introduce smart contracts on DAG without linear ordering - they will probably be so exotic though few people will use them …

---

**ChosunOne** (2018-05-05):

Right, which is why I suggest some deviations from their spec (in the case of SPECTRE), namely a time to finality that rejects non-robustly accepted transactions, or you can go the route suggested in PHANTOM and use a k-clustering technique of the block headers to get a linear ordering.  In either case, it seems like there are some improvements in both protocols that can be integrated into future versions of Ethereum to improve scalability.

---

**naterush** (2018-05-06):

I think we can totally have a smart contracts in a system w/out a total linear order on TXs without making our smart contracts exotic at all. Imagine if we insisted on a liner order for TXs interacting with any specific smart contracts - but if two transactions touch totally unrelated accounts, we don’t have to order them (and the blocks can be mined concurrently).

In many ways, this would be preferable to the system we have currently - it’s probably more scalable! That being said, I don’t think this is what the above papers suggest.

---

**ChosunOne** (2018-05-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/naterush/48/4241_2.png) naterush:

> In many ways, this would be preferable to the system we have currently - it’s probably more scalable! That being said, I don’t think this is what the above papers suggest.

You are right, they aren’t exactly what the above papers suggest, but I think they inspire a line of thought that is good for scalability in general.  That is exactly why I suggested we take a look at them :).

---

**kladkogex** (2018-05-07):

Nate - I agree

An simple example of a  system without total ordering is a system of multiple blockchains that interact using asynchronous messages  (such as sharding) - as you said it is much more scalable that a single chain …

---

**jamesray1** (2018-05-08):

I updated the post to make it a wiki to refer to not just PHANTOM and SPECTRE, but alternative sharding and other protocol designs.

---

**jamesray1** (2018-05-08):

Ethereum should have a dataflow programming smart contact language, Ziliqa style.


*(4 more replies not shown)*
