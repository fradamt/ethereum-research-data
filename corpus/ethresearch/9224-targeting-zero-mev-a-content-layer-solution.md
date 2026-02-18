---
source: ethresearch
topic_id: 9224
title: Targeting Zero MEV - A Content Layer Solution
author: pmcgoohan
date: "2021-04-19"
category: Security
tags: [mev]
url: https://ethresear.ch/t/targeting-zero-mev-a-content-layer-solution/9224
views: 11981
likes: 66
posts_count: 45
---

# Targeting Zero MEV - A Content Layer Solution

*MEV is not inevitable*. It is an **exploit** caused by a **vulnerability** that we can **fix**.

It is going to cost Ethereum users around 1.4 billion dollars this year alone. I have shown that this money will be taken [by the rich from the poor](https://ethresear.ch/t/mev-auctions-will-kill-ethereum/9060) who will be powerless to protect themselves.

Having been concerned about this issue since I first discovered it [pre-genesis in 2014](https://www.reddit.com/r/ethereum/comments/2d84yv/miners_frontrunning/), I am so happy to offer a solution.

All of my work on this is [open source](https://en.wikipedia.org/wiki/MIT_License). If you use any of my ideas I only ask for acknowledgement. I’m available for discussion, talks/presentations, brainstorming, specifications, modeling, tea drinking, etc to anyone sincerely wanting to fix this vulnerability, whether you are Flashbots, founders, Optimism, core devs, the EF, a private/public company etc or are just fans of Ethereum and concerned citizens like me.

Please pm me on this forum or discord:pmcgoohan#9435 or contribute to the docs on github. With love, pmcgoohan.

UPDATE: in this [talk for EthGlobal](https://youtu.be/zf2l3veT9EI) I discuss more recent ideas for Plain, Dark and Fair variants of the Alex Content Layer protocols [(slides)](https://drive.google.com/file/d/1-czxCNNt7Wkir6FN8jrGPzTgJXT1eEsY/view?usp=sharing) as well as the root causes of MEV with some [real world examples](https://twitter.com/pmcgoohanCrypto/status/1410870866670460928?s=19) given here.

Now, let’s decentralize…

[Targeting Zero MEV - A Content Layer Solution](https://github.com/pmcgoohan/targeting-zero-mev/blob/d550cbd9e7d5fd84ca719ae783add79f10906280/content-layer.md)

[Relevant proof for fairness assumptions concerning transaction ordering](https://github.com/pmcgoohan/alex-latency-width)

# Targeting Zero MEV - A Content Layer Solution

## Introduction

### No Satisfaction Guaranteed

A projected 1.4 billion dollars will be taken from Ethereum users in 2021 as Miner Extractable Value (MEV). For the first time this will surpass the amounts made in High Frequency Trading (HFT) in the traditional financial markets at around 1 billion dollars.

It seems odd that a decentralized blockchain like Ethereum could suffer worse exploits than it’s traditional centralized competitors. Wasn’t decentralization meant to fix this?

Well our instincts are correct. Decentralization will fix the problem. The reason these problems have not yet been fixed is that Ethereum has not yet fully decentralized.

### Hidden Centralization

A network is only as decentralized as its weakest point.

Blockchain structure is fully decentralized. Blocks are proposed and validated by consensus across tens of thousands of nodes. But there is a dirty secret at the heart of each block. While the blockchain *structure* is created collaboratively, the *content* of each block is not.

This fact is not obvious because it happens in private in the few milliseconds it takes for a miner/validator to create a block and because it is couched in the elegantly distributed data structure that surrounds it.

But the fact is that the *content* of each block is created by a centralized authority without recourse, the miner. As long as a proposed block is *structurally* sound, the *content* of the block is undisputed by the consensus.

This distinction between *structure* and *content* is profound because nothing about block *structure* creates the problem of MEV. Frontrunning, backrunning, sandwiching and other attacks all come from the centralized way in which block *content* is produced.

Block content is not trustless.

### Content By Consensus

There’s nothing wrong with the existing structural consensus layer in Ethereum, it works beautifully. But look at how block content creation sits uncomfortably within it, sneakily centralized in the miner.

[![ASLayers](https://ethresear.ch/uploads/default/original/2X/5/5c738814904dd455e13d35e3510e01cd36995210.jpeg)ASLayers389×170 9.54 KB](https://ethresear.ch/uploads/default/5c738814904dd455e13d35e3510e01cd36995210)

Consider the famous double spending problem that blockchain technology was designed to solve: if one computer has complete control of a financial ledger, how can you stop it spending the same money twice? The answer is that you can’t. Instead you build a structural consensus where no single computer is in complete control of currency transfers, and the problem is solved.

MEV is the equivalent of the double spending problem for executable blockchains. If one computer has complete control of transaction inclusion and ordering, how do you stop it from frontrunning, backrunning, sandwiching and generally exploiting everybody else? Again, you can’t. Instead you build a content consensus layer where no single computer is in complete control of transaction inclusion and ordering, and the problem of MEV is solved.

So let’s free content from miner control and give it a dedicated consensus layer. Now we have a content layer within a consensus protocol stack. No-one is in control, and everybody is. We have decentralized. Now *that* feels good.

[![ACSLayers](https://ethresear.ch/uploads/default/original/2X/7/7d745184cb89e903c31349abd313c1b17115ef75.jpeg)ACSLayers389×227 9.79 KB](https://ethresear.ch/uploads/default/7d745184cb89e903c31349abd313c1b17115ef75)

### Advantages

We remove control over the content of a block from a single party and distribute it across the network.

#### Fairness

By stripping any one agent of their ability to manipulate content, applications become fair and equitable to all users by default. Fairness becomes an innate property of the network without the need for difficult and obstructive workarounds at the application level that are rarely implemented.

Our mechanisms for fair inclusion and ordering are provably close to optimal. They are certainly far more equitable than the current worst case of total miner control.

#### Integrity

MEV is all but eradicated because there is no centralized authority to bribe.

#### Auditable

As with the structural layer, the consensus layer is publicly auditable. Any observer is able to recreate the content of any given block using publicly available content consensus messages.

#### Impact

Block content protocols are a layer on top of existing block structure protocols. Tcp/Ip didn’t need to be revised when p2p messenger apps came along. We don’t need to revise the underlying block structure protocol to add the block content protocol beyond a few integration changes.

#### Interoperability

The protocol does not change whether we are creating content for an eth2 validator, a rollup sequencer, eth1 miner or any other Ethereum structural layer. A single content consensus implementation may be used across all of these networks and more. Solve it for one and we solve it for all.

#### Price Discovery

Inter-market mechanisms like simple arbitrage that are important for price discovery are still permitted. MEV as the exploitation of a helpless victim by a privileged actor due to a network vulnerability is not.

#### Philosophy

There is currently a centralized aspect to the network and it is causing harm. We need to fix it if we are serious in our ambitions for full decentralization.

##

## Alex - A Block Content Consensus Protocol

What follows is an overview of one possible block content consensus protocol called Alex.

### Overview

Here is a simplified view of the protocol. Pickers choose transactions. Shufflers mix them up. The printer manages it all and prints the chunks to the blockchain (or rollup).

[![AlexSteps](https://ethresear.ch/uploads/default/original/2X/2/2142a0c5b22cc429169d077418526523cbe4190c.jpeg)AlexSteps531×461 28.1 KB](https://ethresear.ch/uploads/default/2142a0c5b22cc429169d077418526523cbe4190c)

### In Brief

- A scheduler allocates a set of roles at random from a pool of nodes to work on each chunk of content:
- Pickers each provide their unique view of the mempool by bundling pending transactions.
- These are combined to prevent transaction censorship.
- Shufflers each provide entropy.
- These are combined to randomize each chunk of transactions and prevent transaction reordering.
- Shufflers share their entropy with vaults who then reveal it if the shufflers don’t to prevent withholding.
- If the process halts because a participant has gone offline or is being obstructive, skippers act to jump the set and prevent denial of service.
- eth2: if a validator proposes a block that diverges from this consensus content, it fails attestation and is not included and the validator may be slashed
- centralized rollup sequencer: if the sequencer fails to write the consensus content, they are slashed and possibly voted out
- distributed rollup sequencer: as with eth2, their block is not be validated by the consensus and fails and/or they are slashed

Full text here…

[Targeting Zero MEV - A Content Layer Solution](https://github.com/pmcgoohan/targeting-zero-mev/blob/d550cbd9e7d5fd84ca719ae783add79f10906280/content-layer.md)

[Relevant proof for fairness assumptions concerning transaction ordering](https://github.com/pmcgoohan/alex-latency-width)

## Replies

**thatbeowulfguy** (2021-04-20):

You have some typos (they are TO be slashed") in the “in brief” section.

Interesting proposal.

---

**pmcgoohan** (2021-04-20):

Thanks [@thatbeowulfguy](/u/thatbeowulfguy). I’ve updated the doc

---

**marioevz** (2021-04-22):

What if we force a pseudo-random transaction ordering for each block at protocol level?

For example, take H(txn_hash, previous_block_hash), and then transactions have to be ordered by the sorted values of these hashes.

Miners would still get to pick what transactions get in the block, but front-running becomes less deterministic, and sandwiching transactions much harder.

Gas prices would only guarantee that your transaction ends up in the block, but doesn’t guarantee it’s executed before any other transaction in the block.

---

**pmcgoohan** (2021-04-22):

Unfortunately while the miner (or picker) can still insert txs the entropy must remain unknown.

If not then it is trivial for them to try slight variations of the same tx that hash differently (eg: adding a gwei each time) until the RNG places the inserted tx exactly where they want it.

This is why in Alex the [Shuffler Queue](https://github.com/pmcgoohan/targeting-zero-mev/blob/00b51b08001446a76204ad6c05e1481dd14c3ca3/content-layer.md#shufflers-and-shuffler-queue) always lags the Picker Queue (another reason being [withholding attacks](https://github.com/pmcgoohan/targeting-zero-mev/blob/00b51b08001446a76204ad6c05e1481dd14c3ca3/content-layer.md#shuffler-withholding)).

Also, Alex preserves time order much better than randomizing whole blocks. Tx order is only randomized within a chunk and there are multiple chunks per block (maybe 10-12).

---

**stri8ed** (2021-04-23):

What if the ordering hash was derived from the transaction sender address? e.g. H(txn.sender, previous_block_hash)

To arbitrarily order a block of such transactions, Would require having sufficient balances on a range of addresses, which makes it less efficient.

In such a scheme, it seems it would be impossible to sandwich a transaction, since two transactions from the same sender would necessarily need to be ordered sequentially without interruption.

---

**pmcgoohan** (2021-04-23):

I wish it were that simple! Here’s the problem:

#### You don’t need that many choices to greatly improve your outcome

If you try to frontrun a Uniswap tx when the order is randomized, you have a 50% chance of winning and a 50% chance of losing. Your win expectation is $0, so there’s no point trying.

If you can give yourself just one more shot at randomization (one more funded account in your proposal), you give yourself a 75% chance of winning and only a 25% chance of losing.

Immediately, you have a positive win expectation. As you can see below you only need 7 accounts to give you a >99% chance of winning!

| funded accounts | outcome count | p |
| --- | --- | --- |
| 1 | 2 | 0.5 |
| 2 | 4 | 0.75 |
| 3 | 8 | 0.875 |
| 4 | 16 | 0.9375 |
| 5 | 32 | 0.96875 |
| 6 | 64 | 0.984375 |
| 7 | 128 | 0.9921875 |

#### The wealthier the attacker is the more they can manipulate transaction order

The wealthy can best afford to fund the multiple accounts that grant them this preferential tx order.

The most wealthy can even afford the number of accounts required to position two txs and sandwich a trade. In fact, *only* they can. In this sense, it is less equitable than what we have now.

This is reason that Alex never gives any one participant a choice over outcomes. It is the reason that shufflers [cannot withhold](https://github.com/pmcgoohan/targeting-zero-mev/blob/00b51b08001446a76204ad6c05e1481dd14c3ca3/content-layer.md#shuffler-withholding), that we only [skip sets by consensus](https://github.com/pmcgoohan/targeting-zero-mev/blob/00b51b08001446a76204ad6c05e1481dd14c3ca3/content-layer.md#skippers), and that we never skip individual roles.

---

**stri8ed** (2021-04-25):

https://pdaian.com/blog/mev-wat-do

Fascinating article regarding MEV and attempts to mitigate it.

---

**pmcgoohan** (2021-04-26):

The MEV Auctions defended by this article do not mitigate MEV they *maximize the exploitation* of it.

They allow order flow attacks that would be unworkable without them and these are not tracked by MEV-Inspect.

I think the reason people are so into MEV Auctions right now is that they reduce the txn bloat caused by price gas auctions. Put another way, MEVA exploits the users to save the network. It should be the users that exploit the resources of the network. It is completely back to front and no kind of a medium to long term solution.

Imagine if when the [Heartbleed](https://heartbleed.com/) vulnerability was discovered, the OpenSSL devs decided it was too difficult to fix. Instead they released code that enabled everyone to read everyone else’s encrypted passwords, emails, messages, etc because at least that would democratize access to the vulnerability. I doubt anyone would still be using OpenSSL.

That is where we are right now with MEVA and Ethereum.

---

**pmcgoohan** (2021-04-28):

I have published a Medium article in response to Phil Daian’s post “Mev… wat do?”

[“Mev… do this.”](https://pmcgoohan.medium.com/mev-do-this-beb2754bca63)

---

**tim0x** (2021-05-09):

im confused based on this comment. It seems like your system just randomizes the ordering… doesn’t this mean with 7 accounts (as you say) in a random order mean 99+% of the time the initial transaction will be frontrun?

I don’t see how two layers of pickers helps mitigate this in any way. Sure it eliminates collusion by the block orderer, but don’t you still get frontrun? I’m still reading through your full documentation, so maybe this is answered somewhere or I am missing something.

---

**pmcgoohan** (2021-05-10):

Hi [@tim0x](/u/tim0x). Thanks for reading.

You are right that this is an issue, although unlike at the moment it is possible to protect yourself against it. There has been some discussion of this on the [other thread](https://ethresear.ch/t/mev-auctions-will-kill-ethereum/9060/32)…

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png)[MEV Auctions Will Kill Ethereum](https://ethresear.ch/t/mev-auctions-will-kill-ethereum/9060/32)

> Alex is way fairer than what we have now and mitigates a lot of MEV, but the problem is tx bloat.
>
>
> Essentially with random ordering an attacker can give themselves a better chance of a good outcome by adding n txs.
>
>
> However if another attacker does the same thing, they end up with no better chance and higher tx fees.
>
>
> If a third (or more) attacker does the same thing, they all end up losing big.
>
>
> If the would be victim also splits their tx into multiple txs they can protect themselves again.
>
>
> So Alex fixes inequality, but at the cost of increasing the tx rate (by approx: extra tx count = arb value / failed tx cost)
>
>
> I don’t think the community is ready for a solution which leads to this level of tx bloat, and I’m not sure I’d want to be responsible for it.
>
>
> That’s what got me thinking about encrypted mempool/fair ordering variants of Alex.
>
>
> What finally turned me off random ordering (for L1- it could still work on L2) was being shown this issue #21350  where Geth randomly ordered txs with the same gas price.
> Apparently it led to tx bloat from backrunning attacks, so is quite a good real world proxy for the kind of issues random ordering systems may have.

re this:

![](https://ethresear.ch/user_avatar/ethresear.ch/tim0x/48/6138_2.png) tim0x:

> I don’t see how two layers of pickers helps mitigate this in any way. Sure it eliminates collusion by the block orderer, but don’t you still get frontrun? I’m still reading through your full documentation, so maybe this is answered somewhere or I am missing something.

So the answer is not really because you can split your transactions as much as any attacker can. We have fairness but at the cost of tx bloat and raised costs. Hence looking at enc mempool and fair ordering variants.

The thing to focus on with Alex is the idea of bringing order to the mempool by chunking it up, and the flexibility this gives you with trying different consensus ordering schemes/MEV mitigations without harming UX.

---

**tim0x** (2021-05-10):

thanks for the in-depth answer… as an average user I don’t think I would want to split my transaction/ run multiple transactions to fight off attackers. This sort of tx bloat is overall a bad thing for the network as you say.

Maybe the payoff for an attacker goes down if they are competing but I can’t imagine it would drive away attackers if there is still an opportunity for an economic incentive. If their chance is really so low of winning then perhaps it does disincentivize MEV a lot. I could also see it driving collusion (if this is even possible?) or new strategies.

I see *an* advantage to this Alex method, but I am not convinced it would solve the issue (or benefit the end-user) in any meaningful way personally. I am also curious how this would work with validators instead of miners. However, I concede I am no expert, simply interested in the topic.

I think I am closer to Phil Daian’s opinion on the topic at the present moment.

I appreciate your research on the topic! Keep up the good work.

---

**pmcgoohan** (2021-05-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/tim0x/48/6138_2.png) tim0x:

> I think I am closer to Phil Daian’s opinion on the topic at the present moment.

That’s fine of course, and thank you for engaging. I also do not want tx bloat so I am looking at fair ordering/enc tx versions of Alex.

Phil’s opinion is essentially to leave things as they are. I predict that the more use cases expand for Ethereum the worse the situation will become (ie: the more exploits of transaction order corruption will emerge) until it is becomes clearly intolerable. Over the same time workable solutions to MEV will be getting closer all the time.

So I just ask non-interventionists to continue to keep an open mind about this issue. The situation is changing all the time.

---

**tim0x** (2021-05-10):

Totally, I am still curious about any solutions to the issue or how the dynamics change over the next several months with EIP-1559 and moving to the PoS chain.

Implementing some solutions that mitigate MEV as much as possible would be great! Maybe that’s your proposal, who knows.

---

**pmcgoohan** (2021-05-11):

Re: my suggestion that non-intervention will become intolerable, here is a relevant piece I just had published on coindesk.

When you have data corruption in your system you are bound to get wild and unpredictable negative effects. MEV and GPAs *cause* high transactional data corruption. Here are some [possible outcomes](https://www.coindesk.com/ethereum-mev-frontrunning-solutions).

---

**CodeForcer** (2021-05-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> For the first time this will surpass the amounts made in High Frequency Trading (HFT) in the traditional financial markets at around 1 billion dollars.

Do you have a source on HFT in traditional markets being valued at only 1 billion? That seems way too low considering the insane amount of HFT firms around the world and the billions of dollars they invest into frivolous activities like straightening fiber-optic cables undersea (https://www.popularmechanics.com/technology/infrastructure/a7274/a-transatlantic-cable-to-shave-5-milliseconds-off-stock-trades/)

---

**wminshew** (2021-06-01):

[@pmcgoohan](/u/pmcgoohan) have you looked at mining_dao? https://twitter.com/IvanBogatyy/status/1394339110341517319?s=20

pretty interesting solution (not yet decentralized) where the user produces the full block & pays the miner for PoW only (yes not a solution for eliminating MEV but imo a step forward from status quo)

---

**pmcgoohan** (2021-06-05):

Hi CodeForcer,

![](https://ethresear.ch/user_avatar/ethresear.ch/codeforcer/48/6351_2.png) CodeForcer:

> Do you have a source on HFT in traditional markets being valued at only 1 billion

This number is from the [Financial Times](https://www.ft.com/content/d81f96ea-d43c-11e7-a303-9060cb1e5f44) (paywall)

*“In 2017, aggregate revenues for HFT companies from trading US stocks was set to fall below $1bn for the first time since at least the financial crisis, down from $7.2bn in 2009, according to estimates from Tabb Group, a consultancy.”*

Looking at it again, it seems to be US stocks only, so the amount for all financial instruments will be higher.

However, it is not hard to see why MEV is a much bigger problem for Ethereum than HFT is for trad-fi.

Even when Flash Trading was ubiquitous in 2009, it only gave a 5ms advantage on order visibility. NASDAQ and BATS have since banned even this. Transaction reordering has never been possible in the traditional financial markets in orders sent directly to the exchanges. Brokers like Robinhood might frontrun you- look how it’s ended up for them. I want better than that for Ethereum.

The maximum latency advantage you can get from laying your $1 billion dollar cable is probably around 300ms. As I write this there are 167,540 pending transactions in the mempool. As a miner/MEVA winner I get to pick any combination of those transactions to build a block that is entirely to my advantage as well as adding in any number of my own. Imagine if Nasdaq allowed the highest bidder to pick and reorder what is probably many hours worth of transactions. It is unthinkable, and yet that is the situation with Ethereum today.

Crucially, HFT has declined almost by an order of magnitude over the last decade, whereas MEV is rising exponentially.

Did you read further- what do you make of my ideas for a content layer bound to block attestation? (ignoring the random ordering part which is problematic)

---

**Shymaa-Arafat** (2021-06-07):

1- In all proposed solutions here, u make ur target to wave away the control of transaction ordering from miners hands, right?

-Doesn’t this imply that users too cannot pay for a certain order in the block anymore?ie users have to understand that higher bids for transaction fees now, or for miner tips after EIP-1559, only increases the probability of inclusion in the current block but has nothing to do with the relative order inside it???

-Did I miss something or am I getting this right? and u think users will be OK with that???

.

2-with the same randomization problem existing in ur protocol as the simple hashing idea of

[@stri8ed](/u/stri8ed) stri8ed

[@marioevz](/u/marioevz) marioevz

Can u explain what makes ur protocol better as opposed to the simplicity of just the order of hashes?

»Infact I think the probability of controlling the order of a resulting hash is much less?

---

**pmcgoohan** (2021-06-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/shymaa-arafat/48/6377_2.png) Shymaa-Arafat:

> Doesn’t this imply that users too cannot pay for a certain order in the block anymore? ie users have to understand that higher bids for transaction fees now, or for miner tips after EIP-1559, only increases the probability of inclusion in the current block but has nothing to do with the relative order inside it

I would prefer to take it futher and have no auction at all (whether GPA or MEVA). In this situation, you keep the EIP 1559 base fee to reflect overall demand and mitigate DDOS, but eradicate the tip (thanks [@barnabe](/u/barnabe)).

It is way better for users because:

- no need to set/guess tx fees (which users dislike and which EIP 1559 is trying to address)
- visible guarantees of order execution  (tx order is quickly visible in the content layer before entering the block)
- exploitative MEV is greatly reduced (simplest content layer=limited MEV auctions possible) or eradicated (enc/fair ordered content layer)
- low gas costs

The low gas costs observation is potentially huge and is only just occuring to me. I am actively researching it and would love to stimulate a debate around it.

Essentially, any auction (whether GPA or MEVA) *creates* MEV by allowing users to bid on transaction order. In doing so we are not only auctioning off tx execution, we are also auctioning off tx priority (which is far more valuable as the MEV crisis has shown).

It is this extra value that makes it worth attackers bidding up gas costs to extract MEV. Users that are not trying to extract MEV then have to raise their bids to compete with the very attackers that are exploiting them.

Put simply, not only do auctions corrupt transaction order, they also raise gas costs (I suspect by a lot- I aim to quantify this).

Yeah what I am proposing is a systemic change. High gas prices and MEV are systemic problems.

Thoughts?


*(24 more replies not shown)*
