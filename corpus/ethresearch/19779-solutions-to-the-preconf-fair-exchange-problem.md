---
source: ethresearch
topic_id: 19779
title: Solutions to the Preconf Fair Exchange Problem
author: yaonam
date: "2024-06-11"
category: Layer 2
tags: [preconfirmations, based-sequencing]
url: https://ethresear.ch/t/solutions-to-the-preconf-fair-exchange-problem/19779
views: 3828
likes: 4
posts_count: 4
---

# Solutions to the Preconf Fair Exchange Problem

### tldr

Solutions for dealing with the fair exchange problem in leader-based preconfirmation setups.

Reputation can incentivize preconfers to act honestly.

Alternatively, use order to dictate who gets the PER tip. One can invalidate a PER by sending it to a preconfer with higher priority.

# Fair Exchange?

The fair exchange problem can be summarized as two untrusted players blindly giving up something in hopes that the other party will do the same. The goal is to try to find a method to ensure that both will cooperate. In the context of preconfirmations, the requesting party (gateway) has no guarantee that their preconfirmation enforcement request (PER) will receive a signed commitment. The preconfer has every right to not return a commitment, hold onto the PER until the last second, and include it if profitable (pocketing the tip for free).

# Solution 1: Reputation

One solution to this is by tracking reputation. More specifically, leveraging the promise of future PERs to incentivize preconfers to respond promptly via either commitments or non-commitments (slash-able promises to NOT include). The gateway can throttle or simply ignore preconfers if they misbehave.

Reputation is a tried method and exists today in mev-boost relays (see [Switchboard’s Sauna Appendix](https://ethresear.ch/t/the-preconfirmation-sauna/19762)). While this might work, it still requires certain economic conditions for security. If for whatever reason it becomes really profitable to behave dishonestly, the guarantees fall apart.

# Can we do better?

In an ideal scenario, without any limitations of technology, one would simply invalidate the PER if the preconfer takes too long to respond. With blockchains, this is complicated, and time-based approaches require some sort of additional consensus, breaking the based paradigm. However, we can indirectly access “time” by using order. Blocks are ordered, so preconfers can be as well. If we take advantage of this, we arrive at a new solution that avoids the Fair Exchange problem altogether.

# Solution 2: Last Right

Determine an order for preconfers. This can be done per block (or even intra-block). Send the PER optimistically to the first preconfer. If they commit, then great. If they return a non-commitment, or do not respond, then send the PER to the next preconfer.

But wait, they can still include my PER and pocket my tip! Yes, they can but they won’t be able to keep the tip. This is due to the central idea of this solution: **the last preconfer to include the PER has the right to the tips**. If two preconfers attempt to include the PER, the second preconfer has the right to the preconf tip. For example, the last preconfer submits a proof and transfers the PER tip to their balance. Other mechanisms are also possible and should be explored.

One consideration here is the cost. If claiming the tip is more expensive than the tip itself, then the model falls apart. The good news is this cost is directly tied to the technology and should decrease exponentially (e.g. zk proof). Preconfirmation tips on the other hand are tied to the value of the transaction itself, which is not as dependent on the tech. So perhaps this mechanism will become more and more economically favorable.

One great side effect of this method is that it preserves the possibility of execution promises. If the first preconfer acts honestly, then it can guarantee the execution state for the PER. Execution guarantees fall apart if there’s any dishonesty (same as Solution 1).

# Solution 3: First Right

If we are willing to forgo execution promises, then the gateway can instead request commitments from preconfers in reverse order. Forward the PER to a preconfer down the list, and then move up until one commits. **The first preconfer to include the PER gets the tip.** In the case where L1 proposers are preconfers, this is enforced by the L1 replay protection. This is a much simpler version of Solution 2.

One downside is the “real” latency before the transaction is actually included since the default preconfer is not the current one. But one could argue that for important transactions where L1 settlement is important (e.g. buying a house), preconfirmations in general are probably not a priority.

Note that execution promises are technically still possible if all the state transitions up to the point of inclusion has already been determined. (e.g. All block space has already been filled by PERs or similar.)

# Final Thoughts

We can even perhaps use these Solutions in tandem. For smaller preconf tips, we can rely on Solution 1, let the first preconfer pocket it and “slash” their reputation. For larger preconf tips, we can fallback to Solution 2 and let the next preconfer steal it back. Or just use them at the same time.

Thanks to @mteam for getting me up to speed and providing feedback. We at Spire Labs are actively researching preconfirmations and related topics, and building towards a better, unified Ethereum.

## Replies

**murat** (2024-06-17):

Great post exploring options - the first right approach closely resembles [mev-commit’s decaying preconfirmation bids](https://docs.primev.xyz/concepts/bid-decay-mechanism), but in a more winner takes all manner and requires multiple parties to participate to be viable. One underlying area to pay attention here is if all state transitions are determined publicly before the block is confirmed, then we open up a lot of mev angles that can lead to centralization, particularly if one or more entities that are responsible to commit are vertically integrated.

On the other hand the last right approach can create a lot of noise in real world settings. If we double click into why the first entity didn’t commit, we may extrapolate that the reason would be similar for the following entities. So a lot of bandwidth and network resources could be wasted presenting an unmarketable bid to multiple entities only for all of them to reject it. Moreover this takes away optionality from the entity in that they can’t revisit their decision and commit once they identify some other factor in the market, they essentially lose their right. It’s also unclear how this approach would deal with bid updates or resubmissions, would the first entity receive all updates first?

Fill or kill bids could avoid a lot of the back and forth required in these mechanisms, but then they’re unidimensional in the type of experience they provide and come with their own problems as actors can resubmit/spam these if they don’t receive a commitment.

Overall, this is an exciting exploration in directions for the fair exchange problem leader-based designs come with

---

**14mp4rd** (2024-06-19):

Great post - this is just a silly thought besides your proposed solutions. Preconfers are incentivized to delay preconfirmation promises because they know the detail of transactions they are preconfering. If we use encrypted mempools, then the motivation for such delayness is removed. Does this make sense?

I know that there are a lot of both theoretical and technical challenges with encrypted mempools like how to allow atomic execution with encrypted mempools (atomic inclusion might be an easier one) or the performance degradation.

---

**yaonam** (2024-06-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/murat/48/12986_2.png) murat:

> winner takes all manner

Could you elaborate? In a simple First Right design where preconfs are forwarded to the nth next L1 proposer, that proposer will get all the preconf tips for the current slot, optimistically. This extends for all proposers, so they all get their fair share.

![](https://ethresear.ch/user_avatar/ethresear.ch/murat/48/12986_2.png) murat:

> presenting an unmarketable bid to multiple entities only for all of them to reject it

This is a good point and we definitely need more research on preconf selection/pricing. Maybe an overly simple solution would be for preconfers to broadcast their min tip?

![](https://ethresear.ch/user_avatar/ethresear.ch/14mp4rd/48/8042_2.png) Thanh Nguyen:

> If we use encrypted mempools, then the motivation for such delayness is removed.

Encryption solves a different problem I think, which is only somewhat related to fair exchange. Encrypted requests take up block space, so preconfers can still delay to see if more profitable block space usage appear. (e.g. other higher tipped encrypted preconfs, mev bundles, etc.)

