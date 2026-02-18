---
source: ethresearch
topic_id: 5928
title: Viability of Time-Locking in Place of Burning
author: sina
date: "2019-08-05"
category: Economics
tags: []
url: https://ethresear.ch/t/viability-of-time-locking-in-place-of-burning/5928
views: 2521
likes: 5
posts_count: 8
---

# Viability of Time-Locking in Place of Burning

Burning has a lot of potential as a general cryptoeconomic primitive as an expensive way to signal something. For example, recent threads like [Spam resistant block creator selection via burn auction - #5 by barryWhiteHat](https://ethresear.ch/t/spam-resistant-block-creator-selection-via-burn-auction/5851/5) or [Burn relay registry: Decentralized transaction abstraction on layer 2](https://ethresear.ch/t/burn-relay-registry-decentralized-transaction-abstraction-on-layer-2/5820) describe using burning as a costly signal for sybil/spam resistance.

I am interested in whether time-locking capital (or Ether) has been considered in place of burning in various situations as a potentially cheaper and more accessible signaling mechanism that still enacts a tangible “cost”. Time-locking your Ether, even if you can sell the future right to it, can have a tangible cost, perhaps roughly calculable by comparing to Compound or staking over the lockup time. Here would be my naive framing:

Burning is expensive because you’re spending the money on nothing except for the signal you’re trying to send. The lever you have to increase or decrease the signal’s strength is the amount you burn. A “burn” could be considered a time-lock with a lockup of forever. However, time-locking in place of burning gives you the lockup period as an additional lever to adjust the strength of the signal more finely. For instance, a lockup of 1 ETH for 1 week is a weaker signal then a lockup of 1 ETH for 1 month. Both of these would be far weaker signals than a burn of 1 ETH.

A concrete application where time-locking may make more sense than burning: an on-chain registry of IPFS hashes, and IP addresses claiming to have the files available. For this kind of registry system, popular or sensitive files may be vulnerable to bad IP addresses being spammed as fake hosts; the problem ends up looking similar to the meta-tx-relayer problem, where you need at least one of the posted IP addresses to be honest.

Initially I thought the burn mechanism was the best way to fight spam for this sort of thing, but am now wondering whether time-locking instead breaks the security model, or is a free UX win. The advantage I have in mind is that relayers may be more willing to signal repeatedly with the same money, knowing that in a week (or however long ends up being a reasonable lockup period), they’ll get their money back. Of course, files with only weakly signaling hosts are still vulnerable to spam, so stronger signaling would be needed in those cases.

My hesitation is that the burn could be done with arbitrarily small amounts of money, which may defeat the need for the additional lever to get such fine-grained control of the signal strength. But seems there may be a real UX gain of not actually losing any money when signaling that may be worth the added complexity. Or maybe there’s something else important I’m missing ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=14)

Appreciate any thoughts!

## Replies

**sina** (2019-08-05):

I just noticed this could be used with something like [Conditional proof of stake hashcash](https://ethresear.ch/t/conditional-proof-of-stake-hashcash/1301) as well; instead of having the binary decision of burning or not burning the sender’s money, a more fine-grained decision can be made about how spammy a message is, and a corresponding decision made on a spectrum from [release the funds right away] to [lock the funds for a week] to [burn the funds forever] (and everything in between).

---

**bgits** (2019-08-05):

In a rational market the two should even out in value. Either people will lock up more value or burn less where `BURN == LOCK_COST`

---

**barryWhiteHat** (2019-08-06):

So this is similar to the original ens domain name auction. The idea was that you could buy a name as long as your locked your capital up for a certain amount of time. The winner of an auction locked up the most capital for a given time.

The problem that ENS ran into was that everyone had different opportunity costs for locking their eth up. For example people who were holding eth anyway decided to buy ENS names as they had no opportunity cost on locking their funds for that time as they would be holding the funds anyway.

For this reason I prefer the burn. Because burning eth everyone has the same cost for it. Its the market price at the time.

---

**tchitra** (2019-08-11):

I think this is the main problem with choosing time-locks — a choice of time lock parameter implicitly defines the risk-adjusted cost for a user instead of an absolute cost. That is, if the lockup time is \tau \in \mathbb{R}_{\geq 0}, then for users whose capital costs are measured at time horizons \tau_{\text{user}} < \tau, this will look like a burn, whereas for other users, there might be more complicated strategies for them to participate with. This means that those with longer term risk horizons will not provide direct revelation of their true valuation / preferences (akin to a first-price auction) because they can estimate their risk to a longer horizon.

However, if you have enough randomness, one could imagine trying to make time-locks that have random times that are only revealed upon capital commitment. This will force people with varied risk horizons to enter at the same time, provided that there is enough variance in the expected time-locking time. I should note that this is precisely what regulated exchanges in futures and equities do when they add randomization into the routing of an order from a colocated facility to ensure that all participants engender the same latency for their orders. This ensures, to some extent, that different market makers with different risk profiles still participate.

---

**kladkogex** (2019-08-13):

As people above mentioned, if risk-free annual return on investment is X, time locking funds M for a year is somewhat equal to burning X*M immediately.

There may be some diffs though, it would be interesting to figure them out. Psychologically two things may be different.

---

**tchitra** (2019-08-13):

The measure of risk aversion in terms of duration risk (e.g. the different between your maximum risk-holding time window and the lock up time) is a first-order measure of the psychological difference, modeled on rational behavior in normal markets [*]. I’m sure there will be more complicated phenomena, especially as transaction fee liabilities are financialized via staking derivatives and their ilk, but we’re not very close to that realization.

[*] Irrational behavior seems less likely for those earning transaction fees, although it may happen if there is too much concentration in a small number of staking pools and the yields shrink dramatically

---

**sina** (2019-08-13):

> Psychologically they may be different

This is largely what I’m poking at to see if anything meaningful is there. For example, the recent popularity around Pool Together systems for donating funds seems to be a similar vein; instead of donating directly, pool funds and donate the interest. This potentially* feels like a nicer UX, since users don’t technically lose their funds. The interest they lose feels negligible.

Similarly, burning and time-locking can be framed as equivalent due to being able to calculate the cost of the time-lock, but I’m wondering if there’s a UX win due to average users being more willing to time-lock than to burn. Perhaps you could even copy Pool Together with regards to having uncoordinated actors time-locking together to strengthen a signal, for which they may not have been willing to burn.

So distilling the question, does the potential* UX win of going from direct donation to time-value donation translate cleanly to signaling via burn vs time-locking?

My instinct is that it may not be possible to quantify; seems like something that’d need to be tested at scale in the wild (ie. Do more people signal, and is there more aggregate signal generated when time-locking is an option?).

* I say potentially because I think it’s worth waiting for more such systems to be explored and seeing what the outcomes are like before concluding the UX win is there.

