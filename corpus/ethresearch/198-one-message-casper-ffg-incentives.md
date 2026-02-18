---
source: ethresearch
topic_id: 198
title: One-message Casper FFG Incentives
author: nate
date: "2017-11-07"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/one-message-casper-ffg-incentives/198
views: 1801
likes: 6
posts_count: 9
---

# One-message Casper FFG Incentives

Now that Casper is moving from a prepare/commit scheme to a simpler single vote scheme, the incentive structure can change (and hopefully be simplified!) as well.

At a high level, the protocol has rounds of voting (called “epochs”) where two consecutive rounds with \geq 2/3 votes (by weight) lead to finality. In each round, we know which validators voted and which didn’t, and we can summarize the liveness strategies for validators as “Vote. No seriously, vote!”

For each epoch, let us consider a couple of parameters that may be interesting to our analysis of incentives:

F_v: the fraction of validators who voted, by weight.

TSF: number of epochs, since the last finalized epoch, that we have failed to finalize. For example, if the epoch previous to the current one was finalized, then TSF = 0.

TD: the total sum of all the deposits of the all the validators.

We can now define two functions (names a WIP ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) ):

Y(F_v, TSF, TD)

N(F_v, TSF, TD)

In some epoch, each validator who votes gets Y(F_v, TSF, TD) applied to their balance, and the same for a validator who did not vote and N(F_v, TSF, TD). For example, if a validators votes during an epoch, and Y(F_v, TSF, TD) return .001, then the validators balance grows during that epoch by .001.

From here, our goal is to specify reasonable constraints on Y and N so the incentives encourage what we want. Many thanks to Vitalik for these initial thoughts and encouraging me to start a thread here ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=9)

Here are some basic examples of possible constraints:

1. Validators who are not voting should not make a profit. So, N(F_v, TSF, TD) \leq 0.
2. If finality is consistently reached (which means F_v = 2/3 and TSF = 0), a validator should be net punished if they are voting less than  2/3 of the time. Thus, as this validator will be rewarded with Y( 2/3, 0, TD)  two-thirds of the time, and N( 2/3, 0, TD) one-third of the time, thus we can say that  Y( 2/3, 0, TD) * 2/3 + N(2/3, 0, TD) * 1/3 = 0.
3. Validators who are online and voting should never be penalized to much.
4. As TSF increases, the punishments on the offline validators should increase as well. This implements the “leak” mechanism, where if some coalition of validators goes offline (or is censored), their deposits will decrease until finality can be achieved again.
5. We should bound greifing factors wherever possible and explore the trade-offs between them. For example, Y(x, y, z) < Y(1, y, x), for all x < 1. Otherwise, a coalition of validators can make a profit if they censor other validators, which is not good! In general, a goal should be to characterize the tradeoffs with these greifing factors.

As an example of exploring the tradeoffs, consider that the “leak” mechanism affects the “length” of the weak subjectivity synchrony assumption. For example, if 2/3 of offline weight can “leak away” in 2 weeks, then we could end up with two chains, one with the 2/3 of the original weight and the other with 1/3 the original weight, where both chains are reaching finality, and no validators were slashed. On the other hand, this mechanism stops the FFG from getting stuck if some large amount of validators go offline, and also make it possible for a censored minority of validators to start their own chain!

## Replies

**vbuterin** (2017-11-08):

Thanks for starting the thread!

In general, I have a bipartite model for the way something like this should work. Beyond some threshold T (perhaps expressed as a value of TSF), if >= 1/3 of validators are not voting on a chain for that long then this is an issue that should be resolved by waiting for the leak to run its course, if the not-voting-on-chain validators are the faulty ones, and via a user-activated soft fork if those validators are actually honest victims of a 51% attack blocking their votes. Before T, the low-grade aggression of blocking those votes is not worth forking over, and so to discourage that behavior we want to simply penalize both sides, including the majority. Hence, before T, the best model seems to be one that minimizes the maximum griefing factor; beyond T, it seems logical for the reward for seemingly-online validators to be zero, and for seemingly-offline validators to lose more and more until they lose everything.

---

**nate** (2017-11-09):

Cool! To make sure I follow, if finality is delayed for > T epochs, then we either a) let the offline validators “leak” until we can achieve finality again, or b) soft fork the online validators away, depending on if the offline validators are being censored or not. This does require a synchrony assumption for clients, though - that they receive the messages from the offline validators (or not) and can determine if censorship is occurring.

While this occurs, all offline validators are increasingly punished, while online validators make zero profits. I wonder if profits being zero for online validators (no matter what portion is offline) might not-disincentivize a majority coalition from censoring more. By reducing the size of their coalition to the minimum size required to continue censoring, this coalition can reduce the cost of enforcing their coalition strategy, and so they would essentially be incentivized censor to this minimum point. (This minimum coalition size is probably 51%, as this coalition can “coerce” the miners to censor other validators tx with a promise of “first” control of the fork choice. . . after all the “leaking” occurs). I guess this isn’t really an issue if we are making a synchrony assumption about clients, though, and has the benefit of being super simple ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**nate** (2017-11-09):

In the case where finality is not delayed for more than T epochs, the goal is to minimize the maximum greifing factor. What “direction” of greifing do we want to minimize for here?

If we want to minimize “both ways”, then the best we can do is 1 (if we limit the greifing factor of a censoring majority to G, then a going-offline minority coalition has a greifing factor of 1/G). If so, then we can say the money lost by the majority must be equal to the money lost by the minority. In this case, both groups started off making Y(1, TSF, TD), the majority now makes Y(x, TSF, TD), and the minority makes N(x, TSF, TD). So it seems like we can say that for a greifing factor of 1 both directions, we must have x(Y(1, TSF, TD) - Y(x, TSF, TD)) = (1 - x) * (Y(1, TSF, TD) - N(x, TSF, TD)).

Also making the assumption here that 2/3 < x < 1, as the finality would stall otherwise. There might be more complex strategies of censoring/going offline for T-2 epochs, then not for 2 to achieve finality, but let’s pretend there isn’t for now ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

That being said, it might be more likely a minority coalition is offline (?maybe as the start of a discouragement attack?), so we might want to limit the greifing factor of an offline minority coalition on a majority to .5 or something. In this case, we can just say that x(Y(1, TSF, TD) - Y(x, TSF, TD)) \leq .5 * (1 - x) * (Y(1, TSF, TD) - N(x, TSF, TD)), 2/3 < x < 1. A symmetrical point can be made the opposite way as well.

---

**vbuterin** (2017-11-10):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/n/e95f7d/48.png) nate:

> Cool! To make sure I follow, if finality is delayed for >T epochs, then we either a) let the offline validators “leak” until we can achieve finality again, or b) soft fork the online validators away, depending on if the offline validators are being censored or not. This does require a synchrony assumption for clients, though - that they receive the messages from the offline validators (or not) and can determine if censorship is occurring.

Yep, exactly!

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/n/e95f7d/48.png) nate:

> By reducing the size of their coalition to the minimum size required to continue censoring

Suppose the coalition size is 50% + epsilon. Then, if this coalition censors, they make their own rewards go down, and they make others’ rewards go down by more. The ratio between the two is a key parameter. However, this is only true in the <= T zone; in the >T zone, censoring will get you forked off.

---

**vbuterin** (2017-11-10):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/n/e95f7d/48.png) nate:

> In the case where finality is not delayed for more than T epochs, the goal is to minimize the maximum greifing factor. What “direction” of greifing do we want to minimize for here?

Optimize to minimize both. Ideally keep both below 2; this seems like it should be fairly easy to do.

---

**nate** (2017-11-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Suppose the coalition size is 50% + epsilon. Then, if this coalition censors, they make their own rewards go down, and they make others’ rewards go down by more. The ratio between the two is a key parameter. However, this is only true in the T zone, censoring will get you forked off.

In the case where there is a coalition of size  2/3 > x > 50 censoring, in the greater than T zone, as the online validators are already making 0 profit, censoring more will not cause them to lose any profits. In this case, the coalition can reduce the cost of maintaining their coalition (and increase their profits) by censoring more and reducing the size of their coalition to 50% + epsilon.

It’s maybe more relevant if T is 0 (essentially, described in your gitter comments ). I’ll copy those comments over ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=12) !

---

**nate** (2017-11-13):

Copying over some comments from Vitalik on the [Casper Scaling Gitter](https://gitter.im/ethereum/casper-scaling-and-protocol-economics) on Nov. 11 (want to make the convo is complete [for history]! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9))

**[Vitalik Buterin] so I have some new thoughts on casper FFG incentivization**

**first of all, in the case where TSF > 0, it seems reasonable to set the reward to voters to 0, and the penalty to non-voters can be negative and increase, say, quadratically or via some other formula**

**then, we need to separately just handle the TSF = 0 case**

**the reasoning is that to get to the TSF > 0 case, >1/3 need to be offline or >1/2 need to be censoring**

**and so you don’t really need to think as much about griefing because the actions needed to get to that situation are themselves griefing**

**for the TSF = 0 case, I realized that some of our desiderata are incompatible; but will say more about this later**

---

**nate** (2017-11-13):

Ok, so essentially, the above describes a case where T = 0

In this case, it seems like the optimal size of any censoring coalition is 50% + epsilon by the arguments above (if this is the minimal size of a coalition that can censor sucessfully, not totally sure it is though). Essentially, in the case that a coalition of validators is planning on censoring, they know “too much” censoring (TSF > than some amount) will cause them to get soft forked away - and so they will attempt to censor less than this (this probably makes the most sense in the context of a discouragement attack). Because there is some cost to maintaining the coalition strategy, but as they are making zero profits (and thus no disincentive to censoring more), the coalition can increase their profits by censoring more, which doesn’t seem good.

After all, it seems like we want (in as many cases as possible) all validators to be able to make more profits if more validators are online.

