---
source: magicians
topic_id: 6064
title: Transactions without gas?
author: coinfreak
date: "2021-04-20"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/transactions-without-gas/6064
views: 2268
likes: 4
posts_count: 15
---

# Transactions without gas?

Can someone explain to me how these transactions do not paying for gas? (0 gwei)

https://etherscan.io/tx/0xea7c2955c2f4757fcb8f82f0f4118059d5c37c1a22d48fb93d8e492160023d8e

https://etherscan.io/tx/0x8100381c8b1914694b4e8be29bf7a20cc65f1647d48200459bb97d85c35902cd

In fact, every transaction from this address:

https://etherscan.io/address/0x66f1c77db874d72e6645f1dced8eea05819b4388

has paid 0 in gas but collected $140k in GasTokens …

I would appreciate to find out how this works!

## Replies

**timbeiko** (2021-04-20):

They pay the miner directly off-chain (or on-chain in another token than ETH) and the miner includes the transaction at a 0 gwei price. See [MEV and Me | Paradigm Research](https://research.paradigm.xyz/MEV) or [GitHub - flashbots/pm: Everything there is to know about Flashbots](https://github.com/flashbots/pm).

---

**coinfreak** (2021-04-20):

Thanks Tim!

(Btw, this makes no sense for the miner, as the user prints ~1 Eth worth of GasToken each time, and the miner loses ~2-4 Eth in fees)

---

**timbeiko** (2021-04-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/coinfreak/48/3395_2.png) coinfreak:

> (Btw, this makes no sense for the miner, as the user prints ~1 Eth worth of GasToken each time, and the miner loses ~2-4 Eth in fees)

The miner doesn’t lose 2-4 ETH in fees: those fees are for the entire block, which contains 100-200 txns. Also, those transactions do get paid for, but just not via the transaction fee. It could be done off-chain, via a one-time payment to the miner on chain, etc.

I haven’t looked into it too deeply, though, so may be missing some details.

---

**merlinux** (2021-04-21):

I’ve also seen many 0 gas transactions exploiting the swapping on Uniswap (frontrunning, arbitraging, see [Exploiting miners or security concern? 0-Fee Frontrunners](https://ethereum-magicians.org/t/exploiting-miners-or-security-concern-0-fee-frontrunners/5942)).

Seems the miners are cashing in by including 0-gas tx and manipulating transaction-ordering.

---

**kladkogex** (2021-06-09):

Well I see this constantly on Uniswap.

Just submit a transaction with a tiny gas fee. It will get executed anyway.

With EIP1559 this will get worse.

---

**coinfreak** (2021-06-13):

> Just submit a transaction with a tiny gas fee. It will get executed anyway.

Wait what? How come?

Also, why do you believe 1559 will make this worse?

---

**kladkogex** (2021-06-14):

Well - if you do a transaction on Uniswap it is vulnerable to front running meaning that bots steal some of your money by inserting a transaction in front of it.

Since in many cases miners are front runners, it makes sense for them to pay for your gas.

---

**mass59** (2021-07-04):

In my opinion, more can be done without gas

---

**Shymaa-Arafat** (2021-07-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> With EIP1559 this will get worse

Why do u think so when with EIP-1559 there will be a Fee-cap determined by the system, ie miners will not be able to arrange TXs with off-chain agreements?

That’s one of the widely promoted advantages of it

---

**edmundedgar** (2021-07-09):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/f0a364/48.png) Shymaa-Arafat:

> Why do u think so when with EIP-1559 there will be a Fee-cap determined by the system, ie miners will not be able to arrange TXs with off-chain agreements?
> That’s one of the widely promoted advantages of it

Without blaming anyone for this, the EIP1559 discussions were quite mysterious in that it was promoted for one set of things on Magicians, and a totally different set of things on Reddit and Twitter. Broadly speaking everything it was promoted for here it actually delivers, but the same is not true of what highly-followed people with bat emojis said about it on Reddit and Twitter.

With 1559 miners will still be able to choose which transactions they select for blocks, and we can expect them to select the ones that make them the most money. There will also be no particular change in the marginal cost of including any given transaction to the miner; Previously to include Transaction X would cost the miner in terms of fees foregone from leaving out Transaction Y to make room for it, whereas now they don’t get the fees for either X or Y, but they have to pay ETH holders an equivalent amount (by burning ETH) to include X. The cost changes from being an opportunity cost to being a regular cost, but the impact on the bottom line is the same.

Equally, there’s no change in what you will have to do to incentivize a miner to include Transaction X. If the miner was happy to accept a chicken as payment before, they should be happy to accept a chicken as payment after. The *is* a difference related to economic abstraction in that *someone* will have to provide ETH for the protocol to burn to pay the transaction, so you can’t completely cut the “ETH” currency out of the loop in the way that you otherwise could in PoW Ethereum. But if they’re making 100 DAI from including a transaction by MEV, or getting the equivalent in chickens, there’s nothing to stop the miner paying the cost of the ETH that need to be burned as the cost of earning that revenue, any more than miners’ need to pay electricity bills in Chinese Yuan forced Ethereum users to use Chinese Yuan.

There does seem to be one little glitch in the way the thing has been specified, in that it seems to be required that there be enough ETH in the sender’s account to pay the basefee at the point the transaction is made. This wasn’t necessary economically, but it’s how it was implemented. But if the miner is stumping up the ETH in any case and taking payment in MEV or chickens, there’s nothing to stop them adding a transaction to credit it to the sender’s account to make the transaction go through and unlock the MEV or the chicken.

---

**Shymaa-Arafat** (2021-07-11):

-First I read about EIP-1559 from Tim Roughgarden technical report and heard Vitalik Buterin discussion with him, few others for Vitalik & Justin Drake in Bankless/twitter/…etc, it’s everywhere.

-2nd, u did say it a transaction fee min must be burned by the user to the system; the block min fee is defined by an EQ depends on all TXs ( a demand Vs supply matter)

Yes, there are tips for miners but even the Fee-cap (total burned + tip) is public; why would a miner pay ur fee instead of u!!!

Unless there’s a much larger MEV he will gain, like u r making an exchange that will increase the value of his savings for example.

-I mean sure miners will find a way to do some off chain agreements, but it should be less than previously. I think a miner can only favor u for an off chain money if no one is paying publicly more than u ( he can’t put ur TX before a TX with a higher fee cap, because it will statistically increase the required to burn amount + decrease the block size; and maybe the TX which paid off chain cannot be admitted to this block at all)

---

**edmundedgar** (2021-07-11):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/f0a364/48.png) Shymaa-Arafat:

> -First I read about EIP-1559 from Tim Roughgarden technical report and heard Vitalik Buterin discussion with him, few others for Vitalik & Justin Drake in Bankless/twitter/…etc, it’s everywhere.

This is the distinction I’m talking about: Tim Roughgarden’s analysis is an excellent piece of work based on sound economics that matches the claims that have been made and tested here. The (really interesting) Justin Drake interview on Bankless is in a different category, although he works for the EF they’re his own opinions and a lot of them haven’t been posted and discussed here at all, since they’re generally not considered the point of the EIP, as it was presented here.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/f0a364/48.png) Shymaa-Arafat:

> why would a miner pay ur fee instead of u!!!
> Unless there’s a much larger MEV he will gain, like u r making an exchange that will increase the value of his savings for example.

It seems like you know the answer to your question? The miner would pay the fee instead of you because they make more than it cost them some other way. That could be a that they can make money through MEV, or because your transaction pays them in another token and the sender account doesn’t have gas, or because you have some other arrangement with them. They would only normally include your transaction if the revenue from doing this is greater than the cost to them.

As I’ve explained, economically the situation is the same now: **There is already a cost to the miner including your transaction**. The reason people some people don’t fully appreciate this is because it’s an *opportunity* cost, ie it takes the form of revenue that they had to give up by leaving out a different fee-paying transaction, rather than money they actually have to pay someone. But the impact on the miner’s bottom line is the same. Consider this example where a miner is trying to decide whether to include a transaction with no gas but `2` of the currency of your choice in MEV, in a block where it would normally have cost `1`:

Pre-1559: Get `+2` in MEV and `0` in gas, give up `1` in gas for the next transaction you leave out, basefee is `0` since it doesn’t exist yet, so net gain from taking the zero-gas tx rather than the next in the queue is

> 2 +0 -1 -0 = 1

Post-1559: Get `+2` in MEV and `0` in gas, give up `0` (except a trivial tip) for the next transaction you leave out (since that would have been burned rather than given to you), subtract the basefee of `1` that you’ve stumped up on behalf of the sender, so net gain is

> 2 +0 -0  -1  = 1

Does that make sense?

---

**Shymaa-Arafat** (2021-07-11):

I think u mean what u used to consider a lost gain (by not taking say Tx B) is now considered paid cost and the net value is the same

-First is not exactly the same

-Second u r ignoring the effect of the fee on the block size; I mean if all users have the same behavioral pattern, miners could try to like move the real auction off chain and all agree to submit fixed fees&tips, but users r not all the same, some could refuse to cooperate offline, some could have conflicting interests,…etc.

-For example if Tx B notices miner malicious cooperation with Tx A, it could also cooperate with others to shrink the block size,…

.

-Look, I’m kind of busy-minded & not fully concentrating in this topic RightNow; but if what u say is true miners would haven’t made all this angery & rejecting reactions against EIP1559, and described by some from the other side as becoming too greedy.

I remember specifically that pools which allows Privately Mined Transactions, sparkle pool is an example, clearly rejected 1559

---

**edmundedgar** (2021-07-11):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/f0a364/48.png) Shymaa-Arafat:

> -Look, I’m kind of busy-minded & not fully concentrating in this topic RightNow; but if what u say is true miners would haven’t made all this angery & rejecting reactions against EIP1559, and described by some from the other side as becoming too greedy.

To be clear, 1559 does cost them revenue, and that’s why they’re upset. Filling out the previous example:

Pre-1559, no MEV: Revenue 1 (gas fee from non-MEV tx)

Pre-1559, take MEV: Revenue 2 (MEV revenue from MEV tx)

Post-1559, no MEV: Revenue 0 [+ teensy tip] (non-MEV pays tx gas but it’s burned)

Post-1559, take MEV: Revenue 1 (MEV revenue from MEV tx - burn)

But the loss of revenue is nothing to do with MEV, and the gain from taking the MEV is the same in both cases, because 2-1 = 1, and 1-0 also = 1.

