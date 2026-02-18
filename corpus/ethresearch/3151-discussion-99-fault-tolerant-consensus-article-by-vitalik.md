---
source: ethresearch
topic_id: 3151
title: "Discussion: \"99% Fault Tolerant Consensus\" (article by Vitalik)"
author: AnthonyAkentiev
date: "2018-08-30"
category: Consensus
tags: [fault-tolerance]
url: https://ethresear.ch/t/discussion-99-fault-tolerant-consensus-article-by-vitalik/3151
views: 3345
likes: 12
posts_count: 10
---

# Discussion: "99% Fault Tolerant Consensus" (article by Vitalik)

Here is what i would like to discuss - https://vitalik.ca/general/2018/08/07/99_fault_tolerant.html.

Vitalik proposed (or better - described the tradeoff between the latency and fault tolerance) what is called the **latency-dependent consensus**.

As far as i understood:

1. We have a PBFT consensus that has a 50% (or even 33%) “fault tolerance”.
2. The goal of the consensus is this: all nodes should get the same list of proposals. For example, node 1 should get {a,b,c} list and node 2 should get {c,a,b} list. After each node selects the proposal with the lowest hash, for example b, so it is selected and consensus is reached.
So we would like to avoid situations when node1 gets {a,c} and node2 gets a {b,a}.
3. To improve the situation described above we can add Observers - nodes that can only watch and retransmit messages.
4. But adding Observers without increasing the consensus time frame is not enough. So we increase the time frame. For example, before we required all msgs to settle in 5 seconds, now we increased this to 15 seconds.
5. And Vitalik states that adding more Observers (plus increasing the time frame) - CAN increase the fault tolerance up to 99+%.

Questions:

1. Is everything correct above?
2. So am i right that in order to increase the fault tolerance Vitalik proposed to add more Observers AND increase the consensus time frame?
3. And that will slow down the consensus
4. And that will decrease the max number of nodes that can work in such system (because even the number of messages are the same, we highly increased the time for consensus to be reached).

We can’t have both: “fault tolerance” AND “fast consensus”, right? That articleshows that such a tradeoff exists and can be exploited. So 50% (33%) fault tolerance can be manually changed (increased/decreased) at will.

Am i right?

Thx

## Replies

**kladkogex** (2018-08-30):

I think Vitalik’s paper  misses a discussion of the hadest problem  - any synchronous protocol assumes finite time to deliver messages.  Then the question is what is going to happen during a network split;

The very point of the blockchain protocol is that it is asyncronous and survives under network splits.

I think all of synchronous protocols are doomed - they are not resilent enough function longterm in the presence of network splits.  The future belongs to asynchronous protocols such as HoneyBadger.

The  99% tolerance will not work simply because in the case of a network split it will lead to 100 different baby networks - very bad!

---

**vbuterin** (2018-08-31):

> The 99% tolerance will not work simply because in the case of a network split it will lead to 100 different baby networks - very bad!

Agree, hence why I described the hybrid mechanism, which can survive either a network split or >33% malicious, as long as both do not happen at the same time.

---

**MihailoBjelic** (2018-09-04):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> I think all of synchronous protocols are doomed - they are not resilent enough function longterm in the presence of network splits.

I personally (both as a protocol designer and a user) would always choose CP over AP, and I really like the fact that (weakly) synchronous protocols like PBFT/Tendermint halt when the network splits (or in general, when large portion of validators is not participating). To me, it’s much better for a ledger that holds (a large amount of) value to stop when the network cannot agree on the state, than to produce two conflicting states and eventually discard one of them. If we halt the chain - we lose some time but no one loses money, if we continue with two versions of chains - we preserve liveness but a lot of people will eventually lose money, that’s inevitable.

The main problem here is how to resume the consensus/block production after a halt happens, and that often has to be done by an off-chain consensus/action. If we can design a secure way to do that on-chain, IMHO such protocols would be superior to those that favor liveness.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> HoneyBadger

Thank you for pointing this out, just reading the paper, a great team of authors, very interesting.. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

---

**dlubarov** (2018-09-06):

> The very point of the blockchain protocol is that it is asyncronous and survives under network splits.

Let’s say the Bitcoin network splits into three partitions, with 40%, 30%, and 30% hash power. The 40% fork should prevail, but since nobody can tell whether their fork will prevail, is there really much use in the system being available?

If recipients are being diligent, they’ll notice the low hash rate, and not consider any transactions confirmed until it returns to normal (at the very least >50%). If they aren’t diligently examining the hash rate, then they might lose money, as Mihailo says.

Likewise if senders want to make sure their transactions really went through, they’ll also need to wait until the hash rate returns to normal, and possibly repeat the transaction on the prevailing fork. Even if a transaction gets in the prevailing partition’s mempool automatically, it’s possible that miners will decide not to include it.

So I don’t really see the utility in non-final ledger data. I guess it could be used to keep users updated, like an email saying “We saw your transaction, but need extra time to confirm it.” Are there other uses?

---

**MaverickChow** (2018-09-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Agree, hence why I described the hybrid mechanism, which can survive either a network split or >33% malicious, as long as both do not happen at the same time.

What is the probability of both network split and >33% malicious attack(s) happening at the same time?

And just in case that happens, what remedy will be available to prevent or resolve the situation?

---

**kladkogex** (2018-09-12):

Since all synchronous protocols need to somehow deal with network splits, all protocols are arguably asynchronous. If your protocol knows how to deal with networks splits, it is asynchronous since network splits can take any time.

So people who think are designing synchronous protocols are in fact designing asynhcronous protocols they moment they add a “separate mechanism” to handle a network splits.

The asynchronicity may though be manual since some protocols will require humans restarting servers if the protocol is stuck ))

---

**vbuterin** (2018-09-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickchow/48/2858_2.png) MaverickChow:

> And just in case that happens, what remedy will be available to prevent or resolve the situation?

Manual client updates ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

The inherent limitations of byzantine fault tolerance theory effectively prove that this is our only choice.

---

**kladkogex** (2018-09-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> The 40% fork should prevail, but since nobody can tell whether their fork will prevail, is there really much use in the system being available?

For most people, if they are aware of network split, the best is to pause.  The problem is that network split detection is only vaguely defined. There will always be people unaware of the network split and people that submitted transaction just before the split happened.

---

**MihailoBjelic** (2018-09-13):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> For most people, if they are aware of network split, the best is to pause. The problem is that network split detection is only vaguely defined. There will always be people unaware of the network split and people that submitted transaction just before the split happened.

If you’re talking about miners/validators, than this is true only for networks with unknown validator sets, e.g. Bitcoin. In every PoS network, each validator is aware of the current validator set and it’s size, so they can easily know if the network is in good health or not.

If you’re talking about end users (“people that submitted transaction just before the split happened”), than I would argue that it’s much better for these transactions to be immediately rejected, than to be accepted initially and then later rejected (once the split/fork resolves).

