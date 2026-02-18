---
source: magicians
topic_id: 6921
title: "EIP-3756: Gas Limit Cap"
author: matt
date: "2021-08-21"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-3756-gas-limit-cap/6921
views: 3665
likes: 10
posts_count: 14
---

# EIP-3756: Gas Limit Cap

[Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-3756)





###



Set an in-protocol cap for the gas limit

## Replies

**tmk** (2021-08-22):

I’m not sure how much EIPs usually go into the motivation, but it seems to me like this section in the *rationale*

> The gas limit is currently under the control of block proposers. They have the
> ability to increase the gas limit to whatever value they desire. This allows
> them to bypass the EIP and All Core Devs processes in protocol decisions that
> may negatively affect the security and/or decentralization of the network.

is missing something like “… and block proposers are not sufficiently incentivized to take into account long-term effects, so we cannot trust them to set a reasonable limit.” Or whatever the reasoning is for why it’s bad that block proposers have the power to set the gas limit freely.

---

**JekaMas** (2021-08-23):

If we’d like to restrict gas limit to a particular value, shall we have a good benchmark first for all clients? And then discuss the real gas limits of the clients. Also by my understanding, we have to have quite a formal process of changing this limit in future.

---

**aliatiia** (2021-08-23):

+1 for this sanity ceiling limit, it has two advantages (a) leaves the current miner-voted gas limit change mechanism in place which is useful in case of DoS attack (e.g. push it to the floor, 5k, then push back up after attack) and (b) it is [easy](https://github.com/aliatiia/go-ethereum/commit/5876bc97c89f28b9d8cfb2cfcfd39e8b06cca977) to implement.

Im wondering if the floor of 5k should be changed to 10k … because a malicious vote by the miners to 5k would render the chain unusable, so it itself is kind of an attack vector.

---

**AuthenticSybil** (2021-08-23):

If I might suggest - the community concerns of this causing a replication of the forever frozen BTC block size limit might be assuaged if this limit had an explicit expiration on it - say after `N` million blocks. At that point a new consensus on what the limit (if any) would have to be determined. Alternatively, an automatic increase in the block size of a largish amount (25%) at a regular interval could also be put in place.

---

**wjmelements** (2021-08-25):

30m limit is a 15m target. 15m gas per 15s is far too low. BSC does 85m every 3s.

I don’t want ACD setting the limit. The limit should be governed by miners (soon stakers), who actually produce and validate blocks. If those validators leave slow clients behind, that is fine with me. Clients should be competing on performance, and not be holding back the protocol. As evidenced by the 15m proposal, they are *really* bad at setting such limits. If you had asked them a few months ago they would have set it at 12.5m. An earlier iteration of EIP-1559 would have set it to 10m. Worse, failure to reach consensus on a future increase would ossify 15m forever (see Bitcoin Core).

---

**ultratwo** (2021-08-26):

I have a few quibbles with the EIP.

Firstly, the EIP currently does not specify what happens if, at block `N`, the gas limit is greater than 30m by a sufficient margin that it cannot be lowered below 30m. The literal reading of the EIP is that it is not possible to create a legal successor block in those circumstances, which is obviously undesirable.

Secondly, I would appreciate some discussion about the fact that this is a highly contentious issue that is being implemented by a soft fork. While I expect the probability of the chain splitting over this is remote, if it does the situation could get quite unpredictable and confusing if some users refuse to upgrade to clients supporting the EIP in protest.

More generally, I am not convinced that the current mechanism is broken in a way that justifies changing it in a hurry. EGL is unlikely to succeed at it’s goals anyway and I would be mildly concerned about the potential for ACD to get bogged down in rows over the gas limit if it is given that power.

If there is a more formal process for control I would support calls for more in depth investigations about the gas limit.

---

**matt** (2021-08-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ultratwo/48/4080_2.png) ultratwo:

> the EIP currently does not specify what happens if, at block N, the gas limit is greater than 30m by a sufficient margin that it cannot be lowered below 30m

1. The ideal route is to collaborate with miners to bring the gas limit under 30mm, then activate a soft fork to cap the limit.
2. The alternative is override the normal gas limit manipulation mechanisms on the fork block and allow the miner to choose 30mm regardless of what the limit was in the parent block.

The second option can only be done via a hard fork and so I think we will want to discuss the trade offs between the two.

---

**ultratwo** (2021-08-26):

Option 3:

After block `N`, a block is invalid unless the gas limit either:

1. Less than 30,000,000
2. Equal to gas_limit - gas_limit/1024 (the largest decrease allowed under current rules).

This preserves the soft fork property while handling the edge case where the gas limit is above `30,000,000` correctly.

---

**axic** (2021-08-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aliatiia/48/2724_2.png) aliatiia:

> Im wondering if the floor of 5k should be changed to 10k … because a malicious vote by the miners to 5k would render the chain unusable, so it itself is kind of an attack vector.

What can you do with 10k that you cannot with 5k? Nothing can be executed on 10k, since the base cost of a transaction is 21k.

---

**aliatiia** (2021-08-26):

sorry, 5M and 10M, not 5K/10K

---

**matt** (2021-08-26):

To be clear, the current min gas limit is actually `5,000` gas.

---

**edmundedgar** (2021-08-27):

Yes, because the rationale isn’t clear it’s also impossible to say whether the proposed mechanism is the best way to achieve it.

If the thought is that developer consensus (backstopped by the need to persuade users to run the fork the developers recommend) is just a better way to handle this than staker voting then that needs justifying, given the history of that method of controlling this particular parameter leading to stagnation and/or economic forks.

If the goal is to mitigate the damage in the event that staker voting suddenly starts failing for some reason then there are probably better ways to do it; For example, you might want to put a cap on the medium-term *rate* of increase - for example say that the limit should not double in less than three months. That way if staker voting suddenly starts to malfunction and it looks like a developer-led hard fork is required then there’s some time to do it before the chain becomes unusable, but you avoid routinely sucking core devs’ time into endlessly arguing about it, and you also avoid the stagnation that’s likely to occur if you require consensus on an issue about which different teams disagree.

---

**axic** (2021-09-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ultratwo/48/4080_2.png) ultratwo:

> Option 3:
> After block N, a block is invalid unless the gas limit either:
>
>
> Less than 30,000,000
> Equal to gas_limit - gas_limit/1024 (the largest decrease allowed under current rules).
>
>
> This preserves the soft fork property while handling the edge case where the gas limit is above 30,000,000 correctly.

You mean the following?

> Equal to previous_block.gas_limit - previous_block.gas_limit/1024 (the largest decrease allowed under current rules)

That sounds like a good idea. I’d also change your first criteria to `less than or equal`.

