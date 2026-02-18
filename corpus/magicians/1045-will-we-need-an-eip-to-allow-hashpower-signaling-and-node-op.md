---
source: magicians
topic_id: 1045
title: Will we need an EIP to allow Hashpower signaling, and Node operator Signaling?
author: MadeofTin
date: "2018-08-13"
category: Working Groups > Signaling Ring
tags: []
url: https://ethereum-magicians.org/t/will-we-need-an-eip-to-allow-hashpower-signaling-and-node-operator-signaling/1045
views: 1135
likes: 3
posts_count: 11
---

# Will we need an EIP to allow Hashpower signaling, and Node operator Signaling?

I am working on the signalling team and two of the signals we want to include is Miner Hash-rate Signaling, and Node Operator signalling. I was listening in on last weeks [core-dev call](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2044.md) and there was discussion about the competing mining reward reductions, and a communicated desire to hear how the mining community felt about these changes. Seeing as this sort of signaling is on our Roadmap I am doing some digging into what we would need if any EIP development to support these two signals.

## Requirements Draft

- Signal support for an arbitrary set of EIPs

Any set up EIPS can be signaled
- It is okay if that set be size limited due to implementation requirements

Three positions supported

- Yay
- Nay
- Either

On the ethereum governance gitter I was pointed to this having already existed.


      [github.com](https://github.com/ethereum/ethereumj/blob/165fe6060ca40325debcc3356b02c634f1f945ee/ethereumj-core/src/main/java/org/ethereum/config/blockchain/AbstractDaoConfig.java#L67)




####

```java

1. this.constants = parent.getConstants();
2. this.forkBlockNumber = forkBlockNumber;
3. BlockHeaderRule rule = new ExtraDataPresenceRule(DAO_EXTRA_DATA, supportFork);
4. headerValidators().add(Pair.of(forkBlockNumber, new BlockHeaderValidator(rule)));
5. }
6.
7. /**
8. * Miners should include marker for initial 10 blocks. Either "dao-hard-fork" or ""
9. */
10. @Override
11. public byte[] getExtraData(byte[] minerExtraData, long blockNumber) {
12. if (blockNumber >= forkBlockNumber && blockNumber < forkBlockNumber + EXTRA_DATA_AFFECTS_BLOCKS_NUMBER ) {
13. if (supportFork) {
14. return DAO_EXTRA_DATA;
15. } else {
16. return new byte[0];
17. }
18.
19. }
20. return minerExtraData;
21. }

```








There was some open questions regarding whether an arbitrary set would affect consensus.

A formalized system for encoding these may fit for an EIP. Also, if we needed to make any changes would any of them require a hard fork?

I am happy to cowrite an EIP with anyone for either of the two signals.

Cheers,

James (madeof_tin)

## Replies

**AtLeastSignificant** (2018-08-15):

I will never support a signalling proposal that doesn’t have these options:

• Yay

• Nay

• Abstain

• No vote

Having data on how many “voters” actively choose to abstain from the vote as opposed to not participating at all is a critical signal.

Also, I don’t see why “node operator” signalling is or even can be a real thing.  How is this possible sybil resistant?  You can lock coins in contracts, do some proof of work, or be a public figure who openly displays their vote, but I really can’t think of any other valid signals.

---

**MadeofTin** (2018-08-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/atleastsignificant/48/219_2.png) AtLeastSignificant:

> • Abstain
> • No vote

Can you clarify the difference between these?

I envisioned “either” representing those who don’t care if it is Yay, or Nay, but choose to vote. Abstain may be a better word for this.

---

**MicahZoltu** (2018-08-16):

I believe “abstain” means you are actively voting, but you are not picking a side while “no vote” means you never even showed up (you likely don’t know how to vote, or you don’t care enough to pay attention, or similar).

---

As I have argued elsewhere I am against miner signalling because we *shouldn’t care* what they want.  They are a service provider, not economic participants.

---

To echo what [@AtLeastSignificant](/u/atleastsignificant)  said, node signalling is not Sybil resistant.  I can simulate running as many nodes as I want.

---

**jpitts** (2018-08-16):

Not every signal has to be an aggregate; an important sources of signals could be from a stakeholder group or working group / Ring. Such a group would come to consensus about what to signal internally by their own governance, and the result recorded in a contract that they control.

I agree that signals from individuals and especially groups should have options (e.g. Yay, Nay, Abstain). And also a short text statement explaining the rationale behind their signal.

And ultimately it is up to the client implementers and other readers/users of signals to determine how to interpret signals, whether aggregated or from a stakeholder group.

---

**MadeofTin** (2018-08-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> I agree that signals from individuals and especially groups should have options (e.g. Yay, Nay, Abstain). And also a short text statement explaining the rationale behind their signal.

I really like the addition of an optional statement being included. That will be something else I will investigate.

---

**MadeofTin** (2018-08-16):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> node signalling is not Sybil resistant. I can simulate running as many nodes as I want.

If you simulate running a full node does it require the same amount of resources as running a full node?

---

**AtLeastSignificant** (2018-08-17):

I can’t think of a good way to prove that you’re running multiple full nodes rather than just 1 without doing some kind of Proof of X, but then you need to incentivize doing Proof of X because doing it inherently has a cost, and oh wait now we are just talking about miners XD

---

**AtLeastSignificant** (2018-08-17):

[@jpitts](/u/jpitts) I agree that having signals from private/non-aggregate parties is important, and the inclusion of a message would go well with that sort of thing.  However, I see some potential for confusion/manipulation with this because anybody can then create a signal for whatever and talk about it as if it holds the same weight as others, simply because they are both valid signals.

Can’t these private/non-aggregate entities simply make a public statement instead?  Or what is the added value of “signalling” as opposed to anything else for these groups?

---

**AtLeastSignificant** (2018-08-17):

That is the correct difference between “abstain” and “no vote”.  I honestly find this data to be some of the most important because it allows clients to have a valid default setting for users - no vote.

We can then observe the level of signalling participation, which is immensely important when trying to measure decentralization and creating governance processes.  It dispels a lot of FUD (or confirms it) whenever there is a contentions decision, and would highlight what I think is one of the biggest issues with this network (that the vast majority of miners/users/coin holders/or otherwise “valid voters” are completely apathetic).

> I am against miner signalling because we shouldn’t care what they want

I still believe this is a bit more nuanced, but as the market grows miners lose power to make decisions by themselves and shape the landscape for the market in their favor.  I think it’s fair to say they are slaves at this point, and miner signalling is really just as valid as full-node operator signalling.

However, we can actually *do* miner signalling since there is sybil resistance built-in. I think that alone is a good enough reason to include it in any signalling effort.

---

**sorpaas** (2019-01-21):

I actually [wrote a spec](https://github.com/ethereumproject/ECIPs/pull/62) for hashpower signaling based on BIP-9 back in 2017. Just re-submitted this [as an EIP](https://github.com/ethereum/EIPs/pull/1715) in case this is useful.

