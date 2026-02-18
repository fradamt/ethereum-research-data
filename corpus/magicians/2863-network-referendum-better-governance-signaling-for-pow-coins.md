---
source: magicians
topic_id: 2863
title: "Network Referendum: Better Governance/Signaling for PoW-coins"
author: sneg55
date: "2019-03-05"
category: Working Groups > Signaling Ring
tags: []
url: https://ethereum-magicians.org/t/network-referendum-better-governance-signaling-for-pow-coins/2863
views: 1404
likes: 13
posts_count: 15
---

# Network Referendum: Better Governance/Signaling for PoW-coins

I was working on Governance/Signalling concept recently. Looking for your thoughts on it.

## Summary

Ethereum, Ethereum Classic, and other PoW-coins need an agreed and clear voting/signaling workflow before the next difficult decisions occur.

This paper proposes a voting/signaling concept that can be developed and implemented in a short period of time and on a low budget.

The system divides the key stakeholders of PoW-coin’s Network into 3 branches([separation of powers](https://en.wikipedia.org/wiki/Separation_of_powers)):

- Core Developers(Contributors). Those who actually creating underlying software and technology used in Network.
- Coin Holders. Those who invested own fiat money thus bought coins and holding it now.
- Miners. Those who securing PoW network.

Agreed acceptance criteria for Referendum it is any TWO of branches passing representation threshold and gain more than 50% of YES votes for Referendum proposal.

**Referendum voting mockup**:

[![Pasted_Image_3_9_19__6_34_PM](https://ethereum-magicians.org/uploads/default/optimized/2X/1/12eac14757da8d457c219806ae0a52f63cfaf562_2_628x500.png)Pasted_Image_3_9_19__6_34_PM749×596 48.4 KB](https://ethereum-magicians.org/uploads/default/12eac14757da8d457c219806ae0a52f63cfaf562)

## Full description at this gdoc:



      [docs.google.com](https://docs.google.com/document/d/10RdAL1OaReGJcLP3F9OhMsKiMlkz4RgerjaQzbQmenY/edit?usp=sharing)



    https://docs.google.com/document/d/10RdAL1OaReGJcLP3F9OhMsKiMlkz4RgerjaQzbQmenY/edit?usp=sharing

###

Network Referendum: Better Governance for PoW coins   Summary Ethereum, Ethereum Classic, and other PoW-coins need an agreed and clear voting/signaling workflow before the next difficult decisions occur.  This paper proposes a voting/signaling...

## Replies

**boris** (2019-03-06):

[@AFDudley](/u/afdudley)’s talk touched on this at ETHCC and I’m pretty convinced that more stakeholder voting is needed.

[@phillux](/u/phillux) and I talked about related items.

---

**AFDudley** (2019-03-09):

If there is revived interest in Signaling, might I suggest looking at:

https://github.com/vulcanize/ethersignal which was develop with help from Vlad Zamfir.

---

**burrrata** (2019-03-10):

Do you have a link to that talk I could check out?

---

**burrrata** (2019-03-10):

I’m doing research on signalling and mechanisms for communication in decentralized communities. Is there a write up explaining this repo, what it does, and who it’s for? Thanks ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**AFDudley** (2019-03-11):

No real write up. You’d pretty much just need to use the solidity source to figure out what’s going on.

---

**shemnon** (2019-03-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sneg55/48/1524_2.png) sneg55:

> Agreed acceptance criteria for Referendum it is any TWO of branches passing representation threshold and gain more than 50% of YES votes for Referendum proposal.

A less charitable way to view this is that any two branches, if in majority agreement, can compel action by the third branch, even if it is against the third branch’s majority agreement.

The reason I chose the less charitable phrasing was to illustrate the main conflict: how to incentivize a “branch” to a unified action when their majority opinion is against it.  Realistically miners and developers cannot compel coin holders to act one way if they don’t want to, or for any other majority branch against a minority branch.  The minority branch always has the option of walking away/forking and taking the minority of those other two branches to form their own coin.  Even a three way minority can do that too. (ETC?)

My opinion is that unless there is fairly uniform agreement between the three branches in this model that any non-unified change would then be contentions.  Only a change that would be in agreement to all three branches would work long term, so it would be better to spend time persuading the minority branch to act than compelling any action by any branch.

---

**sneg55** (2019-03-12):

I think nothing can prevent minorities from forking away; it’s impossible both from a political and technical point of view.

We only could reduce possible disturbance inside community providing clear procedures for voting/signaling on important decisions for all stakeholders.

I believe that if such voting workflow is clear and accepted by the majority, (most of) people will follow the given decision.

---

**phillux** (2019-03-14):

It all started here: https://ethereum-magicians.org/t/lightning-talks-signaling-technical-challenges-with-measuring-sentiment/

---

**phillux** (2019-03-14):

> I believe that if such voting workflow is clear and accepted by the majority, (most of) people will follow the given decision.

Not sure if this is what you mean, but…

I’m not certain that voting methods being “accepted by the majority” is a requirement to get started on using these mechanisms. If people begin using signaling methods before they are legitimized, they must prove that they are valid by their own merit in order to be legitimized by other members of the community.

E.g., if there were a coin vote with 70% turnout, that would in itself be a quite legitimate signal **on behalf of coin holders**.

---

**boris** (2019-03-14):

I kind of love that we have content all here we can reference.

I’ll make a note and see if I can get the source video, so you can edit it to just your talk.

---

**phillux** (2019-03-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sneg55/48/1524_2.png) sneg55:

> I believe that if such voting workflow is clear

This is a must. Trade-offs must be presented clearly before, during and shown in the result of each vote.

e.g., “Coin-voting favors participants with a greater share of coins, however is sybil-resistant…”

---

**burrrata** (2019-03-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/phillux/48/900_2.png) phillux:

> I’m not certain that voting methods being “accepted by the majority” is a requirement to get started on using these mechanisms. If people begin using signaling methods before they are legitimized, they must prove that they are valid by their own merit in order to be legitimized by other members of the community.

Yeah isn’t that kind of how EIPs work? People build stuff, and if it’s useful and lots of people use it then it can be officially incorporated into the platform. At least that’s how they described the NFT process [here](https://www.zeroknowledge.fm/62)

---

**phillux** (2019-03-15):

Thank you for the insights, [@sneg55](/u/sneg55)!

When I’ve been thinking about signaling, I’ve avoided defining thresholds in order to keep the signals “signals” rather than votes. Determining that 51% simple majority is the way to go creates further arguments for delegitimizing such votes, such as, if 51% miners say AYE, and 49% say NAY, will this cause a network split or will the entire population accept the validity of the vote? Such a result will not signal that “rough consensus” has been reached, and therefore no “winner” should be determined.

On a completely separate note, we should have a note on **coin-voting precedent**, using the DAO carbon vote as an example:

- DAO Carbon vote finished at block 1,894,000 http://v1.carbonvote.com/
- Supply at block 1,894,000 (July 20th, 2016) was around 82,000,000 https://etherscan.io/chart/ethersupplygrowth
- Turnout was 4,542,416.51 ETH, amounting to around 5.54% of total ETH supply
- AYEs got 87%

… Result was 97% market cap remaining with ETH, and 3% market cap with ETC. It was however, a different time with a much more concentrated community and distribution of ETH. Also, market cap is not an ideal metric, but in my opinion, the best we have for the health of a network and determining the success of a chain after a chain split.

---

**sneg55** (2019-03-15):

Thanks for feedback [@phillux](/u/phillux) !

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/phillux/48/900_2.png) phillux:

> Determining that 51% simple majority is the way to go creates further arguments for delegitimizing such votes, such as, if 51% miners say AYE, and 49% say NAY, will this cause a network split or will the entire population accept the validity of the vote?

As I said before, there is no way to prevent forking away and chain splits. It’s the nature of OSS and especially blockchain projects.

The idea behind separation of powers is that any TWO of 3 branches(miners, contributors, holders) should pass representation threshold and gain over 51% Yes votes. This signaling concept balanced for interests of all Network stakeholders.

