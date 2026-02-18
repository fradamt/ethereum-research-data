---
source: ethresearch
topic_id: 1431
title: "Internalise costs: storage, and bandwidth"
author: jamesray1
date: "2018-03-19"
category: Economics
tags: []
url: https://ethresear.ch/t/internalise-costs-storage-and-bandwidth/1431
views: 4014
likes: 16
posts_count: 9
---

# Internalise costs: storage, and bandwidth

For internalising the costs of storage, [Gas Token](https://gastoken.io/) is a method of doing that by arbitraging gas prices, filling up the state with SSTORE with junk data (which obviously has disadvantages) when gas prices are low, and  emptying the state with SLOAD when gas prices are high. Note that internalising costs are necessary for sustainability, however doing so can have adverse side effects. For instance in the case of internalising storage costs it increases the complexity for users and developers, or complexity can somehow be reduced with intermediaries that provide some improvements, e.g. storage providers that have a token, but in turn that may not be trustless, so you’d need ways to deal with that, e.g. slashing conditions. Nevertheless, these costs should be internalised, otherwise the protocol will suffer.

Also note that there are gas costs for storing data and a refund for clearing it, as defined in the [Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf#appendix.G):

[![Screenshot%20from%202018-03-20%2009-23-52](https://ethresear.ch/uploads/default/optimized/1X/9734b2ad90c18b132d37279458a9c28a3dad497c_2_690x124.png)Screenshot%20from%202018-03-20%2009-23-52707×128 17.4 KB](https://ethresear.ch/uploads/default/9734b2ad90c18b132d37279458a9c28a3dad497c)![Screenshot%20from%202018-03-20%2009-32-49](https://ethresear.ch/uploads/default/optimized/1X/6df6785b1f7784c7bc094b1911296be54b7f0a9f_2_690x82.png)

With optional metering in eWASM these gas costs could be more cost-reflective. These gas fees and refunds internalise computation and I think also I/O or disk reads and writes.

It would also be good to consider how to internalise the cost of bandwidth, although I don’t know how.

Internalising these costs could also somehow incentivise full nodes (which validate/execute transactions), which is also discussed here: [Incentives for running full Ethereum nodes - #23 by jamesray1](https://ethresear.ch/t/incentives-for-running-full-ethereum-nodes/1239/23).

## Replies

**phil** (2018-03-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> It would also be good to consider how to internalise the cost of bandwidth, although I don’t know how.

Just posted a new thread on this.  Would love your feedback.

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> With optional metering in eWASM these gas costs could be more cost-reflective. These gas fees and refunds internalise computation and I think also I/O or disk reads and writes.

I don’t think ewasm solves the problem entirely; miners/proposers may be incentivized to provide storage for cheaper than it’s worth if they don’t plan on storing it long term.  Also, you need to somehow take into account the fact that permanent storage *should* cost more than ephemeral storage.  The refund is a hacky way of accomplishing this, but I’m not sure what a solution would look like in the context of ewasm metering & would be curious to hear your thoughts.

---

**jamesray1** (2018-03-20):

Phil, I agree that EWasm doesn’t solve this as it stands, and I agree that you still need to charge storage rent, and you can deal with the UX and DX with other solutions like secondary    markets and archival nodes. I’ll have a look at your new thread on bandwidth. And I’m glad that you’re jumping in on this.

---

**veox** (2018-04-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> Gas Token is a method of doing that by arbitraging gas prices, filling up the state with SSTORE with junk data (which obviously has disadvantages) when gas prices are high, and  emptying the state with SLOAD when gas prices are low.

~~I think you meant the other way around: filling up when prices are low, emptying when high. ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12)~~

Fixed!..

---

**veox** (2018-04-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> Nevertheless, these costs should be internalised, otherwise the protocol will suffer.

Before I begin: I fully agree with this statement.

If the cost is not internalised, it doesn’t mean there’s no cost: it’s just external, “dumped on the commons”.

So, if what follows gets you conflicted – please start reading from the beginning. ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12)

---

When discussing storage rent, one must take into account existing application-layer use patterns. Just about everything on this layer has been built with the assumption there is no rent. A change on the underlying layer means these patterns will have to be re-evaluated.

**Exhibit A: the ERC-20 standard**, and all tokens built on it. (I’d assert these make a sizeable portion of the ecosystem.)

[According to the standard](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20.md#approve), anyone can set any `allowance` to anyone else, even if it’s above their `balance`, or if they have no `balance` at all.

In the spirit of creative mischief that’s essential to the day of March 32, – and to more clearly demonstrate my point! – I’ve filled Aragon token `allowance`s from a contract ([etherscan](https://etherscan.io/address/0x4fd482142099f53613bc3a78948d6db93fd84dff), [etherchain](https://www.etherchain.org/account/4FD482142099F53613bC3A78948d6db93Fd84DFF)) to the precompiles in the `0x00 .. 0x3f` range, with lyrics to a song I find wholly fitting the situation.

(There’s a simple way to see what was posted, but it requires use of one of the centralised services linked.)

Now, the contract has self-destructed upon completing its task, so it won’t be setting the `allowance`s back to zero.

The precompiles won’t be calling the Aragon token to withdraw their `allowance`s – and, in either case, there’s nothing to withdraw.

So – the graffiti is there forever!.. (Well, “until the landlord calls”.)

---

Imagine there was storage rent. Who pays it?

If the answer is “Aragon”, then they’ll have to seriously re-consider managing the storage footprint, – especially since the token’s using `MiniMe` under the hood.

If the answer is “the sender”, then how and where do you do accounting? Do the users pay for their own accounting, too? Will the use case still be viable if accounting is taken into account?.. (Pun intended.)

Just about every other token will have to do the same. The effort required to “upgrade” the existing ecosystem to the new rent paradigm will be tremendous. This is not just existing contracts, but also *standards*.

---

(Got to run - will have to stop here.)

Happy Fools’ day! I’m afraid that’s us. ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=12)

---

**jamesray1** (2018-04-02):

![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9) yep, I’ll edit that.

---

**jamesray1** (2018-04-02):

That was cheeky! An alternative is to launch a completely new blockchain, but I don’t think that offers much benefit to changing the current one, or continuing with business as usual. The longer we delay, the more expensive it will be to make a transition to a rent model. Those lyrics are ironic!

---

**phil** (2018-04-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/veox/48/240_2.png) veox:

> Exhibit A: the ERC-20 standard, and all tokens built on it. (I’d assert these make a sizeable portion of the ecosystem.)

There’s a much simpler and more intuitive (IMO) question about ERC20 that highlights the core issue of sustaining today’s commons-based model in a rentful world, which is for tokens that have a uint256 e.g. _totalSupply counter (read: any global state, which today is often assumed to be all state even in mappings for security purposes), who pays for that?

I’d be in support of:

- Decay and throw by default and let community members be responsible for rent / resurrection on an as-needed basis; this could be OK if resurrection is painless and some commons-based archiving is available.
- Smart grandfathering of existing storage; one option is to do dirty deletion on any contract’s storage before some date, forcing a token’s users to pay as if they were constantly paying rent and resurrecting but actually keeping the data in state regardless of whether it was paid-for or not.  This will prevent data that’s in the system from disappearing permanently (though it will make it more expensive to access, nobody said this would be cheap forever), while not allowing for profitable “landlord contract” type arbitrage for users who create contracts / allocate storage before the switchover.

I’m kind of leaning to the latter; hard/incompatible change to the fee / economic model, backwards-compatible/grandfathered change to the more technically optimal pruning it supports.

Of course this still provides some bad incentives to fill the space with junk to later act pseudo-archival; this can be disincentivized through a price curve for the “pseudo-revival” detailed above that increases to above the cost of actual future-based commons revival.  Eventually, accessing existing contracts that rely on this mechanism should probably become more expensive than using contracts in the new mode, even if revival is invoked every time storage is used.

Vitalik also had another nice backwards-compatible method in a previous thread where users are required to top up a contract’s TTL to 1 year every time they transact with it, and a contract only disappears if untouched for a year; I like this more from a practical/technical/engineering standpoint, but a little less from a philosophical standpoint of preserving existing guarantees.

Regardless there is a wide space of possible solutions here and the decision will likely be made on political/devUX grounds.

---

**veox** (2018-04-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/phil/48/18_2.png) phil:

> Vitalik also had another nice backwards-compatible method in a previous thread where users are required to top up a contract’s TTL to 1 year every time they transact with it, and a contract only disappears if untouched for a year;

For ref:

- Improving the UX of rent with a sleeping+waking mechanism - general description of TTL mechanism;
- A simple and principled way to compute rent fees - #57 by vbuterin - 1-year TTL.

---

Thanks for mentioning this! It’ll take me a while to catch up with the previous body of work. (I see also that my concern’s been voiced here and there, albeit without a demo; and that the answer to “this will require a massive re-engineering effort!..” seems to be “yup”.)

