---
source: ethresearch
topic_id: 2926
title: Challenge Bond Pricing Concerns
author: kfichter
date: "2018-08-14"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/challenge-bond-pricing-concerns/2926
views: 2891
likes: 1
posts_count: 5
---

# Challenge Bond Pricing Concerns

This is a set of notes from discussions with David Knott and Vi.

---

Users who successfully challenge an action on a Plasma contract should generally receive a bond for doing so. Current thinking on the actual magnitude of this bond has assumed that the bond should simply cover the gas cost of challenging. So, although challenges aren’t supposed to be profitable, challenges are supposed to be free. If users are already required to monitor the Plasma chain and challenges are free, then users have no real incentive to disable automatic challenges in their client software.

Unfortunately, bond pricing isn’t as simple as it seems. Whenever multiple challenges are submitted simultaneously, only one challenge can actually be successful. **Each unsuccessful challenge still needs to pay at least the base transaction gas cost (21000 gas)**. Depending on network congestion, this base cost alone can range from anywhere from <$0.01 to >$0.50.

We can try to limit the number of challenges submitted at the same time by having clients strategically wait to see if other challenges are submitted, but this won’t work in every case. We run into further issues if miners choose to front-run challenge transactions. **A front-running miner would place their own challenges in front of other challenges in order to collect the bond**. Challenges by other users would always fail and always have to pay at least the base gas fee. It’s unlikely that front-running will happen if the bond is sufficiently low and the cost of modifying client software is high, but it’s something to consider.

**If challenges are not free, then users may choose to only challenge if the exiting UTXO would directly impact the safety of their funds**. As a result of exit priority, the safety of a user’s UTXO is only threatened when the total funds stolen is greater than the total sum of valid UTXOs with a lower priority than the user’s UTXO. If the sum stolen is less than this amount, the user can be sure that their UTXO will be processed with enough funds in the contract.

In practice, these problems probably aren’t as bad as they seem. The cost of submitting an invalid exit is pretty high for even a low bond on the order of a few USD. On the high end, a failed challenge submitted every Ethereum block (that’s a lot of challenges) would only run on the order of ~$100k annually. Certain parties will probably have external incentives to challenge. With changes in Ethereum 2.0, it may be possible to block these double-challenges automatically in a way that doesn’t charge gas for the second challenge.

**So we’re probably fine for now**. However, these are problems that don’t currently have a convincing economic solution. We definitely need to consider these things going forward and come up with a stronger protocol that addresses these concerns without relying on extra-protocol assumptions.

## Replies

**gakonst** (2018-08-15):

Couldn’t payouts to challengers as well as fees being paid to the operator can be implemented via a DAO that holds any challenges-bonds-fees and distributes them at the end of some time period, proportionally to their contributions, fees paid etc?

---

**ldct** (2018-08-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> Each unsuccessful challenge still needs to pay at least the base transaction gas cost (21000 gas) .
>
>
> A front-running miner would place their own challenges in front of other challenges in order to collect the bond .
>
>
> As a result of exit priority, the safety of a user’s UTXO is only threatened when the total funds stolen is greater than the total sum of valid UTXOs with a lower priority than the user’s UTXO.

I think these are fine, IMO. We can model this as a game that behaves kind of like a multi-round (fixed number of rounds) all-pay-a-minimum-fee auction of the bond, where players initially bid 0 and at every round players can increase their bid. Any nonzero bid must pay the fixed base transaction fee (regardless of whether it wins or not). The auctioneer (ie the block producer) can at any round accept any bid, including their own. If no bid is accepted, a certain subset of players (the subset is known in advance) experience a large penalty.

I don’t think the expected outcome of this game is one where there is a high probability that no bid gets accepted, but I haven’t worked it out and it would be interesting if that were the case!

---

**kfichter** (2018-08-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> Couldn’t payouts to challengers as well as fees being paid to the operator can be implemented via a DAO that holds any challenges-bonds-fees and distributes them at the end of some time period, proportionally to their contributions, fees paid etc?

Yes, possibly. Should definitely be trustless and we don’t want too much security to rely on an external mechanism, but I’d be interested in exploring this. Most important thing is to keep the bond as small as possible for the sake of UX.

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> I don’t think the expected outcome of this game is one where there is a high probability that no bid gets accepted, but I haven’t worked it out and it would be interesting if that were the case!

This is a really good way to break the situation down. It seems like the result of the game might almost be miners being the only users to challenge in most cases, although the reward is relatively low. That seems dangerous under bribery attacks.

---

**kfichter** (2018-08-24):

So there is a solution to this problem that some might consider a little brutal…

In MVP we’re only interested in the case where an exit is clearly challengeable but doesn’t get challenged. We can give people a *very* strong incentive to challenge by allowing anyone to burn the entire contract if they prove an exit should’ve been challenged but wasn’t.

If the spend came before the exit, then we can immediately burn the whole contract. If the spend came after the exit, then the operator must’ve cheated, so we place the burn in the priority queue with priority of the second spend. This second case is the equivalent of an invalid tx that tries to steal the entire contract balance.

The end result here is that everyone on the Plasma chain has an extremely large direct incentive to challenge every invalid exit.

