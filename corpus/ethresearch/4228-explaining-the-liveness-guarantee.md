---
source: ethresearch
topic_id: 4228
title: Explaining the liveness guarantee
author: jrhea
date: "2018-11-12"
category: Consensus
tags: []
url: https://ethresear.ch/t/explaining-the-liveness-guarantee/4228
views: 7779
likes: 26
posts_count: 14
---

# Explaining the liveness guarantee

One of the aspects that seem to surprise many people that only casually follow the progress of Ethereum Serenity is the quadratic leak that is imposed upon validators for being offline and missing a slot.  For those unwilling/unable to read the Casper FFG paper, I wrote up a quick explanation of how one could arrive at this solution using fairly conventional wisdom from distributed systems in computer science.

I am curious what others think of this explanation.  Any and all notes/insights/feedback are welcome.

# Liveness

One of Serenity’s main goals is to guarantee liveness (i.e. continue to finalize blocks) in the event of a major internet partition (e.g. [World War 3](https://twitter.com/josephdelong/status/1058398584331218950)).  This liveness guarantee comes at a steep cost which makes it important to understand the predicament and possible tradeoffs.

## The CAP Theorem

The [CAP Theorem](https://en.wikipedia.org/wiki/CAP_theorem) for distributed systems, tells us that:

> You can’t simultaneously guarantee more than two of the following:
>
>
> Consistency: Every read receives the most recent write or an error
> Availability: Every request receives a (non-error) response – without the guarantee that it contains the most recent write
> Partition Tolerance: The system continues to operate despite an arbitrary number of messages being dropped (or delayed) by the network

## The Assumption

By viewing the argument through the lens of the **CAP Theorem**, we can deduce the rationale for the **inactivity leak** by accepting the following assumption:

> No network can guarantee message delivery because the network itself is not safe from failures (e.g. client disconnects, data center outages, connection loss).

## Partition Tolerance

Since message delivery cannot be guaranteed, the logical thing to do is to tolerate prolonged message loss.  This is equivalent to **Partition Tolerance**.

> Sidenote: Think of the World War 3 scenario as a dysphemism for prolonged message loss between groups of validators.

With **Partition Tolerance** as a hard requirement, we are now limited to tradeoffs between **Consistency** and **Availability**.

## World War 3

In the **World War 3** scenario, where the network is severed, the validators are split into two partitions. From [Casper FFG](https://arxiv.org/pdf/1710.09437.pdf), we know that in order for both partitions to continue finalizing blocks, we need two-thirds majority of validators to be online in both partitions.  This is obviously not possible; however, we can prevent the chain from stalling forever if we are willing explore a compromise between our **Availability** and **Consistency** guarantees.

## The Compromise

This is accomplished by introducing an **inactivity leak** that drains the deposit of unresponsive validators each time a slot is missed until the remaining validators in each partition become the supermajority.

At this point, blocks in both network partitions can begin to finalize; however, if the network partition is healed we are left with two valid and separate networks.

## Replies

**nisdas** (2018-11-13):

It would take ~ 13 days for any single network partition for it to be mathematically possible for either partition to begin finalizing blocks assuming each partition contains 50% of the active validators each. Although this would require 100% of the validators in each partition to attest to the same blocks which would be very unlikely. Basically the only time we can realistically start finalizing blocks would be ~17 days.

I guess the assumption would be that if there were any `WW3` event where the network was partitioned, it would be resolved in less than 17 days.

---

**vbuterin** (2018-11-13):

I feel that 50/50 network partitions/splits are massively overrated as a threat. When has this historically happened, anywhere, and not been resolved soon? What would even be a coherent story by which two parts of the world stay coherent internally but communication between them is not possible? The incentives for maintaining global communication are massive, and there’s no reason why parts of the world that are still capable of maintaining communication internally would not be able to figure something out to talk to each other within a week or two. The thing that’s much more likely, whether in normal life, or due to government censorship, or due to a war, is nodes going offline, either because something happens to their operators or because their operators get cut off from the entire internet.

The inactivity leak is primarily there to deal with this “3/4 of the network goes offline at the same time” risk.

---

**MihailoBjelic** (2018-11-13):

Nice post, I love plain English. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/jrhea/48/1406_2.png) jrhea:

> At this point, blocks in both network partitions can begin to finalize; however, if the network partition is healed we are left with two valid and separate networks.

It will take some time for this to start happening (around 2 weeks, AFAIK). If that massive partition isn’t resolved within that period, the split becomes final/irreversible.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I feel that 50/50 network partitions/splits are massively overrated as a threat.

Totally agree.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The inactivity leak is primarily there to deal with this “3/4 of the network goes offline at the same time” risk.

I was always inclined towards consistency in general, but this is an extremely strong point.

Btw, I don’t quite understand why the term “liveness” (instead of “availability”) is almost always used on Ethresearch and elsewhere? My understanding was that “safety” and “liveness” are terms mainly related to FLP Impossibility? Or it simply doesn’t matter? ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**jrhea** (2018-11-13):

Thanks for the feedback!

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> It will take some time for this to start happening (around 2 weeks, AFAIK). If that massive partition isn’t resolved within that period, the split becomes final/irreversible.

This is a good suggestion…I am going to add some more detail about the partition, how long until the the chain can begin finalizing again, etc.

---

**jrhea** (2018-11-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The thing that’s much more likely, whether in normal life, or due to government censorship, or due to a war, is nodes going offline, either because something happens to their operators or because their operators get cut off from the entire internet.

Good point…I think this example will resonate with people much better than a doomsday scenario.  My goal is essentially to help people understand that these decisions were the end result of a logical and pragmatic train of thought. I attempted to address this in my sidenote where i call the WW3 scenario a dysphemism, but i think i need to augment this with some version of your explanation.

---

**mjackisch** (2020-08-13):

Sorry for digging this up, but as we just discussed the “WW3 assumption” in today’s [randomness summit](https://randomness2020.com/) I wanted to share my thoughts.

I feel the CAP theorem should not be used as guidance for designing complex blockchain systems. The theorem just lacks strict assumptions, for example regarding latency and is plainly: confusing. Which is why there has been [criticism](https://www.researchgate.net/publication/281895403_A_Critique_of_the_CAP_Theorem).

Back to the topic though:

**Why would you even prefer liveness/availability over consistency?**

If Ethereum was mainly a gaming platform and you wanted to accept the possibility of losing a magic sword because of a fork, then okay, favor availability. But Ethereum is currently being utilized to issue bonds worth millions of Euros and the recent DeFi craze implicates how important consistency is. If you consider a fork ending up in two separate networks as “healed”, what really is won here? Did my stable-coin assets simply double a few years after the war when the Internet fully came back?

---

**vbuterin** (2020-08-14):

One very concrete example of this actually happened last week at the start of the Medalla testnet launch. At the beginning, only ~57% of validators were online, because many validators did not yet realize the network had started (there were also some client failures accounting for a few percent). But the network did not stall as a result; instead, it kept on proceeding, though without finality, and the blocks were finalized once the percentage online got back up to 2/3. For plenty of applications this approach is sufficient, and would actually have given those applications much better performance than if the chain just completely stalled.

The general principle is that you want to give users “as much consensus as possible”: if there’s >2/3 then we get regular consensus, but if there’s <2/3 then there’s no excuse to just stall and offer nothing, when clearly it’s still possible for the chain to keep growing albeit at a temporarily lower level of security for the new blocks. If an individual application is unhappy with that lower level of security, it’s free to ignore those blocks until they get finalized.

---

**sachayves** (2020-08-14):

great explanation.

[this notebook](https://github.com/ethereum/rig/blob/a7fbca572b36c9734936fd04ffa1d7a699ab6370/eth2economics/code/beaconrunner2049/beacon_runner_2049.ipynb) by [@barnabe](/u/barnabe) complements it well.

---

**mjackisch** (2020-08-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> if there’s >2/3 then we get regular consensus, but if there’s <2/3 then there’s no excuse to just stall and offer nothing,

You are right that offering a running chain with some probability of eventual finality is indeed valuable and a great argument for most (low-value) transactions.  Being on the 57% side as in the Medalla case, you get some assurance regarding safety, so continuing without finality is acceptable.

But what about the unlikely major chain split condition, with n<2f?

Let’s say you’re online in a group of 40% of validators, with 20% of the total nodes being completely offline, and having another partition of 40% you don’t have any contact with.

Shouldn’t the consensus rather halt completely in this case instead of slashing the faulty nodes until you have two separate networks, as stated in the post? If I am not mistaken the Casper FFG paper calls this an open problem.

---

**vbuterin** (2020-08-15):

But if it halts completely how will it ever recover? What if those 60% are offline for good?

The goal of the leak mechanism is to enable eventual recovery even in extreme scenarios, and a limited level of service until then.

---

**mjackisch** (2020-08-17):

Intriguing question. Algorithmically speaking, the bonded Ether should drain at some point, so the blockchain can live on. However, in such a drastic event determining the fate of the world computer, which in 50 years might be more important than we could ever imagine, how to proceed could be resolved through a hard fork. To drain or to not drain ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

A hard-coded waiting period of two weeks or so could provide a sufficient time window to decide what is best to do. If we imagine terrorists or some state adversary cut all the sea cables in the world and we still have some communication, we might agree that we require a month to establish new connections that allow for most nodes to go back “online”.

If there is a good chance of the network becoming “one” again in the foreseeable future, I would prefer transacting on a partition that will not finalize until the reunion. Or some copied sister network, that can be utilized for the interim. And for those n copied-state networks that are needed to transact in local economies for that period, some merge protocol should be thought of, which probably requires a hard fork too. My intuition tells me, this would destroy less value than a chain split ending up with two Ethereum networks.

---

**kladkogex** (2020-08-18):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/m/49beb7/48.png) mjackisch:

> If there is a good chance of the network becoming “one” again in the foreseeable future, I would prefer transacting on a partition that will not finalize until the reunion.

Agree!

I understand there is a significant argument in favor of the leak, but the argument against overweights IMO.

In a real network 1/3 of people will not become irrational, since they have lots at stake, and a finalization problem will immediately cause a drop in ETH price, which will mean billions of dollars of loss for these people.

If finalization stops it will happen due to say network problems. In this case, punishing people makes little sense since they will have no control over it.   The best will probably be to pause finalizing until things improve.

One possibility would be to start the network without the leak.  One can always add it later. It is phase 0 anyway.  Try to run it without the leak and see what happens )

This is especially true since the network may have lots of bugs when it starts.

So a harsh punishment like this may not be fair and can lead to really bad PR.

When the software becomes solid, may be one can introduce the leak then .  There is no need to hurry since the beacon chain does not do much anyway.

---

**kladkogex** (2020-08-19):

Here is another proposal



    ![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png)

      [ETH2 inactivity leak: a compromise proposal](https://ethresear.ch/t/eth2-inactivity-leak-a-compromise-proposal/7868) [Proof-of-Stake](/c/proof-of-stake/5)




> Looks like many people are scared by the ETH2 inactivity leak.
> Here is a simple  compromise proposal (actuallu two!):
>
>
> Keep the leak, but instead of burning the money,  unstake it (transfer it to a separate account belonging to the same validator)
>
>
> Introduce two times - leak time and burn time.  Keep the leak time to two weeks (or make it even shorter) .  Make burn time much longer.

