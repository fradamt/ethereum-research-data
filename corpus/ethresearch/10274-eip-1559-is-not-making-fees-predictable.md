---
source: ethresearch
topic_id: 10274
title: EIP-1559 is not making fees predictable
author: DimOK
date: "2021-08-05"
category: Miscellaneous
tags: [eip-1559]
url: https://ethresear.ch/t/eip-1559-is-not-making-fees-predictable/10274
views: 1809
likes: 4
posts_count: 5
---

# EIP-1559 is not making fees predictable

Long-anticipated EIP-1559 is up and running, but I am disappointed.

During discussion of EIP-1559 proposal, it was looking like great way to simplify end user interactions with network (besides a lot of other cool effects).

We have some number, provided by network, which determines “normal gas price at the moment”, i.e. BASE_FEE and everyone can use it: developers to rely on fast and efficient trasnsactions, end-users has predictable network fees, miners… oh well, miners didn’t like this EIP anyway ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=14)

So we’ve got this:

[![image](https://ethresear.ch/uploads/default/optimized/2X/c/c5b73d11e603621f884847f9f8df5f9fb9619872_2_517x243.png)image1514×715 56 KB](https://ethresear.ch/uploads/default/c5b73d11e603621f884847f9f8df5f9fb9619872)

But hey, why it looks like a chainsaw? Why gas price can change by 20% within a minutes? Of course, the problem are empty (more or less) blocks, but it doesn’t help to the fact, that we can not blindly take BASE_FEE from network and use it as a gas target.

User wants to send some ETH, wallet takes BASE_FEE and renders “your transfer will incur 10$ fee”. User is OK with that, checks transfer details for 30 seconds and boom, now it is 12$. And in 30 seconds it is 10$ again, how can we call this “predictable”?

In theory, we were aiming to “50% filled blocks”. In reality, there are almost no blocks filled for 40-60%. Here is the sample of gas used limit for 50 blocks starting from [12967650](https://etherscan.io/block/countdown/12967650) (it is a typical distribution).

|  |  |  |
| --- | --- | --- |
| <5% | ++++++++++ | 20% |
| 5-25% | +++++++++ | 18% |
| 25-75% | ++++++++++++++++++++ | 40% |
| 75-95% | ++ | 4% |
| 95%+ | ++++++++++++++ | 28% |

Base fee on blocks 12967650 and 12967700 is equal to 42 GWEI, but it was changing from 37 to 51 (almost 20% difference from “correct” value) during this 10 minutes, just because of the way how it is calculated and the way how miners fill blocks.

I would like to discuss with community, if you see the problem with current unconsistency of BASE_FEE value as well? If it is a problem - we can discuss various solutions (it looks like they should be quite easy to implement), if it is by design or doesn’t matter - well, it still works and helps to estimate current network usage, if you have average BASE_FEE for last N blocks, but maybe it will be better if BASE_FEE calculated by network would be more stable?

## Replies

**mtefagh** (2021-08-06):

I have been predicting and explaining the “chainsaw” you mentioned besides many other issues for more than two years. For instance, see the section “An unintentional uncoordinated attack”:



      [fee](https://mtefagh.github.io/fee/)





###



EIP-3416










BTW, apart from numerous discussions in this forum, I previously commented [here](https://hackmd.io/@timbeiko/1559-resources) and just asked to include a link to my simulation under the “1559 Simulations” section. My comment was simply removed without even adding my link.

---

**MicahZoltu** (2021-08-06):

EIP-1559 was not expected to have any affect on long term gas price volatility.  The UX improvement it provides is around short term gas pricing and enabling users to get into a block reliably without overpaying, without needing to use oracles that have strong future prediction powers.

Most users aren’t using 1559 transactions yet so we can’t say for sure if this goal has been achieved, but so far I haven’t see anything to suggest that it hasn’t been achieved.

---

**DimOK** (2021-08-06):

So BASE_FEE high volatility helps to react faster on network congestion, while very unprecise estimation of current gas price is not considered as a problem.

Still, I don’t understand, as long, as EIP-1559 targets to make blocks on average 50% full, why it doesn’t use average block load for calculations? Using moving average of last N blocks load with relatively small N (around 5-7, even 2-3 would greatly help) will still allow to react quickly to spikes in transactions amount, while BASE_FEE changes will be much smoother.

I guess [ethereum-magicians.org](http://ethereum-magicians.org) was a better place for this discussion, sorry about that.

---

**MicahZoltu** (2021-08-06):

The goal of EIP-1559 isn’t to smooth gas prices either, though we do get a little bit of that naturally as a side effect but it is very short lived (like over a few blocks).

The goal is to make it so a user can submit a transaction with a max fee that is the highest they are willing to pay and be sure that their transaction will be included at the *lowest price possible*.  This gives users much more confidence and reliability and makes it so users don’t have to try to “guess” exactly how much they need to pay to get included in the next block(s).

The previous system made it so every user had to try to guess what the going rate for block space would be in the upcoming blocks and this is a *really hard problem*.  If you guessed too high, you would over-pay.  If you guessed too low, you wouldn’t get included at all.  Now users can just set their willingness to pay and they’ll pay the minimum required to get included ASAP.

