---
source: ethresearch
topic_id: 11057
title: The Safe Merge Proposal
author: saulius
date: "2021-10-20"
category: The Merge
tags: []
url: https://ethresear.ch/t/the-safe-merge-proposal/11057
views: 2576
likes: 1
posts_count: 9
---

# The Safe Merge Proposal

For the last couple of months, we were experimenting with another parallelization stage in [Grandine](https://github.com/sifraitech/grandine) - multiple hardforks support that could be used for The Safe Merge - a safer approach for The Merge. The idea is pretty simple - run two hardforks in parallel instead of doing a regular hardforking process when at any given time only one hardfork is running. Let’s see how The Safe Merge would look:

The Happy Case

```auto
PoW            ------o~~~~X (Social consensus to stop building on PoW)
                      \
The Safe Merge      -- o~~-------- (Party)
                   /
Altair         ---o-------X (Social consensus to stop building on Altair)
```

The Not So Happy Case

```auto
PoW            ------o~~~~-------- (Eth PoW keeps running until successful merge)
                      \
The Safe Merge      -- o~~X (Social consensus to cancel the failed attempt)
                   /
Altair         ---o--------------- (Altair keeps running until successful merge)
```

The pros:

- This approach decreases motivation to mount a coordinated attack as The Safe Merge can be repeated until it’s successful;
- Unlike a regular hardforking approach, a failure is not a big deal. Lessons learned and next attempt rescheduled;
- It’s possible to achieve this scheme using existing clients with small changes - run two instances of clients (one is dedicated for The Safe Merge chain, another one for Altair).
- May allow merging earlier as it’s OK to attempt to merge without covering attacks that are targeting the big-bang approach of The Merge.

The cons:

Some of the below were already given as a feedback on the Eth 2.0 Implementers call.

- Client teams are used to hotfixing broken hardfork instead of playing safe, so a safer approach of The Safe Merge may be an unusual experience for involved parties;
- The Safer Merge has a window (~) when transactions need to be accepted both on PoW and The Safe Merge chain until the social consensus, otherwise there is a risk that the transaction is only on the chain that social consensus decides to drop;
- Such social consensus is not that easy to coordinate;
- Consumes more resources, but the increase is a relatively low problem given then costs of 32 ETH and the resources needed to run EL client;
- More configuration. Unless clients decide to implement multiple parallel hardforks support, but from our experience with Grandine it was a major rework even in the case of our lightweight approach.

Would like to hear more feedback on this proposal.

## Replies

**mkalinin** (2021-11-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/saulius/48/7673_2.png) saulius:

> This approach decreases motivation to mount a coordinated attack as The Safe Merge can be repeated until it’s successful;

If it states that the Merge is delayed because of attack it could increase an incentive of attacking the network during or before the transition process to pushback the Merge and do this multiple times. In any attacking scenario the Merge should rather be accelerated than delayed.

![](https://ethresear.ch/user_avatar/ethresear.ch/saulius/48/7673_2.png) saulius:

> The Safer Merge has a window (~) when transactions need to be accepted both on PoW and The Safe Merge chain until the social consensus, otherwise there is a risk that the transaction is only on the chain that social consensus decides to drop;

The huge problem of it is for the infrastructure to follow two different chains and match them. There is a number of factors that could potentially cause diverging of the state on one chain from the other and lead to eventual inconsistency. These factors are different block times in PoW and PoS, miner rewards, and some others. Ideally, it would require to stop transacting the network before the transition and continue to send transactions after the Merge is considered as done.

---

**dankrad** (2021-11-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkalinin/48/4799_2.png) mkalinin:

> The huge problem of it is for the infrastructure to follow two different chains and match them. There is a number of factors that could potentially cause diverging of the state on one chain from the other and lead to eventual inconsistency. These factors are different block times in PoW and PoS, miner rewards, and some others. Ideally, it would require to stop transacting the network before the transition and continue to send transactions after the Merge is considered as done.

I would claim this part is actually impossible to coordinate. Let’s remember that this is exactly what blockchains are built to do – give a canonical time-ordering of transactions so that everyone agrees which one came first. This does not matter as much when Alice sends ETH to Bob and Bob isn’t intending to do anything with these funds for hours or days. But for many applications it matters a lot. Say there’s an NFT drop and different people got the NFTs on different chains. Or there are large liquidations, etc. Choosing whether the merge was successful or not is a choice with potentially huge economic consequences. So who makes it?

Whoever makes it would essentially be the custodian of the Ethereum chain during that process and that’s something that we definitely don’t want.

---

**saulius** (2021-11-03):

The Safe Merge proposal doesn’t have the intention to align the states between PoW and The Safe Merge. I don’t think that’s possible because of multiple reasons (some of them already mentioned). However, users will be informed about this and it should not be too big issue because:

1. It’s a blockchain and everyone is aware of reorgs, especially during such event. It’s not wise to do NFTs drops during the transition no matter is it The Merge or The Safe Merge approach. The block proposal issues and reorgs during Altair transition confirmed that there may be issues with The Merge approach too so users should not be too naive and expect turbulence, it’s a blockchain with reorgs and other cons after all;
2. The unhappy case in The Merge proposal is more tricky than The Safe Merge. What happens if after The Merge state gets broken so much that the only realistic way to fix it quickly is to fork again from the TTD? The Safe Merge turns the worst case scenario into a no big deal situation.

The Safe Merge isn’t perfect, but it has serious advantages.

---

**saulius** (2021-11-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkalinin/48/4799_2.png) mkalinin:

> If it states that the Merge is delayed because of attack it could increase an incentive of attacking the network during or before the transition process to pushback the Merge and do this multiple times. In any attacking scenario the Merge should rather be accelerated than delayed.

I had an impression that most attacks The Merge is addressing require significant resources. It’s much lower motivation to mount an expensive coordinated attack if the attacker is aware that successfully attacked fork will be simply dropped by social consensus. However, if The Merge can be easily attacked by a low cost attack, then this should be addressed in The Merge first.

---

**dankrad** (2021-11-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/saulius/48/7673_2.png) saulius:

> The unhappy case in The Merge proposal is more tricky than The Safe Merge. What happens if after The Merge state gets broken so much that the only realistic way to fix it quickly is to fork again from the TTD? The Safe Merge turns the worst case scenario into a no big deal situation.

I would disagree. The worst case in the merge is a few hours of downtime. There is no possible scenario “the state gets broken so much” – that is simply not how blockchains work. Re-starting from a known good state is always a (nuclear) possibility.

However, in the “safe merge” proposal, you make the state of several hours of downtime the *default* option – because noone can safely transact as long as both chains exist.

Also you haven’t answered who is taking the responsibility to make the call which of the two chains is the valid one. That is a pretty huge responsibility that would come with huge legal risk as well – anyone who lost money because they were transacting on the other chain could potentially sue. As I said you basically make the Ethereum chain custodial for that timeframe, and I think nobody sane would accept that.

---

**saulius** (2021-11-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> I would disagree. The worst case in the merge is a few hours of downtime. There is no possible scenario “the state gets broken so much” – that is simply not how blockchains work. Re-starting from a known good state is always a (nuclear) possibility.

My point of view is more practical - there can be a bug in (some of) clients and/or some unexpected scenario that after The Merge makes the network to split or even worse - conflicting chains get finalized. Doesn’t sound like a few hours easy task that makes everyone happy at the end. How blockchains work is not only about how they should work theoretically, it’s how the implementation screws the things at the end.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> However, in the “safe merge” proposal, you make the state of several hours of downtime the default option – because noone can safely transact as long as both chains exist.

It’s not downtime. It’s a landing period when passengers should fasten the seatbelts instead of keep partying with NFTs drops.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Also you haven’t answered who is taking the responsibility to make the call which of the two chains is the valid one. That is a pretty huge responsibility that would come with huge legal risk as well – anyone who lost money because they were transacting on the other chain could potentially sue. As I said you basically make the Ethereum chain custodial for that timeframe, and I think nobody sane would accept that.

Interesting legal topic. The Safe Merge would be part of the protocol. Everyone would be aware that *reorg* is possible during the specified time window. How can one win a lawsuit against someone for a *reorg* that is part of the protocol and that’s pretty much the same as we have today with PoW chain, except that the probability of PoW chain to reorg for such long chunk of the chain is low? Sure, it’s possible to sue anyone, but not much point to complain that something expected happened.

Regarding the responsibility to decide whether The Safe Merge was successful or not is an interesting topic itself. The rule of thumb is that PoS chain wins unless disaster happened. But I agree that it’s not a comfortable position. However, I don’t see that it’s a more difficult task than making a decision on which deposit contract is the right one.

---

**dankrad** (2021-11-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/saulius/48/7673_2.png) saulius:

> It’s not downtime. It’s a landing period when passengers should fasten the seatbelts instead of keep partying with NFTs drops.

You can name it whatever you like, that’s just putting lipstick on the pig. From a practical perspective, from many user’s point of view, it’s downtime.

![](https://ethresear.ch/user_avatar/ethresear.ch/saulius/48/7673_2.png) saulius:

> Interesting legal topic. The Safe Merge would be part of the protocol. Everyone would be aware that reorg is possible during the specified time window. How can one win a lawsuit against someone for a reorg that is part of the protocol and that’s pretty much the same as we have today with PoW chain, except that the probability of PoW chain to reorg for such long chunk of the chain is low? Sure, it’s possible to sue anyone, but not much point to complain that something expected happened.

This is very short sighted thinking. Examples:

- The SEC has made a clear statement that due to it’s decentralisation, Ether is not a security. However, it can easily be argued that any committee that is responsible for deciding whether the merge was successful or not would be in custody of these assets, and they are thus a security. Definitely not a position that I would want to be in.
- Next imagine a big DeFi hack happened on the PoS side just after the merge. The committee has the opportunity to turn this back by calling off the merge. What would they decide? Could they be made legally liable if they decide not to turn it back?

I think this proposal will open a can of worms that you definitely don’t want to open.

---

**saulius** (2021-11-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> You can name it whatever you like, that’s just putting lipstick on the pig. From a practical perspective, from many user’s point of view, it’s downtime.

An app (built on top of blockchain) that doesn’t handle a reorg is a pig with lipstick, not the blockchain that reorgs according to the protocol.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> This is very short sighted thinking. Examples:
>
>
> The SEC has made a clear statement that due to it’s decentralisation, Ether is not a security. However, it can easily be argued that any committee that is responsible for deciding whether the merge was successful or not would be in custody of these assets, and they are thus a security. Definitely not a position that I would want to be in.
> Next imagine a big DeFi hack happened on the PoS side just after the merge. The committee has the opportunity to turn this back by calling off the merge. What would they decide? Could they be made legally liable if they decide not to turn it back?

Are there any real world examples of something like that in reality? If that’s a real risk, then make a decentralized committee, otherwise even core devs can be sued by fixing a glitch on the network anytime.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> I think this proposal will open a can of worms that you definitely don’t want to open.

It’s a can of worms like a lot of other proposals. The question is the worms inside are interesting enough.

