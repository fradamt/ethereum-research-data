---
source: ethresearch
topic_id: 2928
title: "Chronos: A Quirky Application Proposal for Plasma"
author: PaulRBerg
date: "2018-08-14"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/chronos-a-quirky-application-proposal-for-plasma/2928
views: 9306
likes: 9
posts_count: 14
---

# Chronos: A Quirky Application Proposal for Plasma

## Introduction

[@markbmilton](/u/markbmilton) and I have been experimenting with the prospect of creating a money “streaming” protocol, as discussed in this [keynote talk](https://www.youtube.com/watch?v=gF_ZQ_eijPs) by Andreas Antonopoulos. We bashed our heads against the wall trying to design a feasible solution on LN, Raiden and other state channels, eventually landing on Plasma. We have seen the light at the end of the tunnel - for now, at least!

## Project Goals

- Standardise continuous value transfers between peers, which we shall further refer to as “streams”
- Enable the usage of ERC20 tokens, with a focus on stable coins such as DAI
- Achieve fast finality and low fees when interacting with the ledger
- Reduce reliance on human promises (Ricardian contracts) and increase awareness about “blockchain as a court” (Plasma child-chain with streams in our case)

## Rationale

It is counter-intuitive to imagine financial commitments over non-trivial periods of time as not being set at fixed intervals (such as a month or a year). And rightly so! Fixed interval payments alleviate [mental transaction costs](https://nakamotoinstitute.org/static/docs/micropayments-and-mental-transaction-costs.pdf). However, if we imagine the time factor of recurring payments as an arbitrary variable, a series of unexpected benefits can be observed.

1. Increased flexibility: if the payment isn’t taken once per month, rather once per hour, or minute, or even less, customers are afforded increased consumption flexibility.
2. Reduced counterparty risk: in situations where pricing is contingent on time (e.g. consultations), both parties would benefit from running a stream. In lieu of creating counterparty risk by pre/post paying for the consultation, the consultant knows they are getting paid for every time unit elapsed. Similarly, the customer doesn’t have to pay upfront and can cancel the stream immediately based on their subjective view of the consultant (expert or charlatan).

There are many examples where granular recurring payments would align the incentives of all parties involved, but we haven’t included them for brevity.

## Plasmatic Approach

The key question in our research was: how do we design an ecosystem where money flows continuously, i.e. it is a function of time, but that does not require users to sign a transaction every interval i (which should approach a very low number)? We concluded that we could reach logarithmic scalability by crafting a blockchain which understands *some* transactions as actions of starting and closing a stream. This blockchain would have its own consensus mechanism and use PoS as its Sybil protection mechanism, but it would periodically publish updates to a Plasma smart contract to inherit Ethereum’s security.

## How It Works

Below is the general sequence of steps used for setting up a stream between Alice, a payer, and Bob, a payee. Funds can only flow from Alice to Bob, but Bob can also propose state updates. The following heuristics assume a Plasma Cash model.

1. At time s, Alice and Bob agree on a price p, payment interval i and stream closing time c
2. Alice deposits funds worth:

p * ((c - s) / i)

1. Alice now controls a coin cid representing her funds on the root chain
2. Alice and Bob initiate the stream by creating a pseudo-escrow account
3. Alice and Bob can optionally mutate the state to p', i' and c' and later hand over a cryptographic proof which redeems:

p' * ((c' - s) / i')

1. The stream is closed by Alice, before or when block c is generated, or by Bob, only when or after block c is generated

Importantly, Alice can close the stream at any time before block c. If she does so, the protocol performs an atomic swap by making Bob give Alice her chargeback in the form of a Plasma coin (it’s assumed Bob has additional funding on the root chain if he doesn’t have an exact denomination on the side chain). Otherwise, the stream is closed normally and Bob receives cid without any further obligations. Here’s a visual representation:

[![image](https://ethresear.ch/uploads/default/original/2X/a/a58d0b89657d1a5a839e18b079180b0540680bf0.png)fig3.png555×261 13 KB](https://ethresear.ch/uploads/default/a58d0b89657d1a5a839e18b079180b0540680bf0)

## Notes

One might draw similarities between [ERC948](https://github.com/ethereum/EIPs/issues/948) and Chronos, but the fundamentals are different. ERC948 focuses on recurring monthly payments (going lower would not be feasible to the accrual of fees), while Chronos aims to be much more flexible and target any peer-to-peer interactions, not just customer-business relationships.

We are keeping abreast of the latest discussions on [Plasma Debit](https://ethresear.ch/t/plasma-debit-arbitrary-denomination-payments-in-plasma-cash/2198), the [viability](https://ethresear.ch/t/why-smart-contracts-are-not-feasible-on-plasma/2598) of smart contracts on Plasma and the [ideation](https://ethresear.ch/t/state-channels-and-plasma-cash/1515) on state channels + Plasma Cash. The Chronos implementation currently being buidled will only have a single Plasma operator and the minimum viable procedures applied.

The goals of this post are to let us share our ideas as well as provide a non-exhaustive introduction to a protocol which enables money streaming. The assumptions we made, along with encountered bottlenecks and in-depth technical details can be checked out in this draft white paper:

[chronos-white-paper.pdf](http://chronosprotocol.org/chronos-white-paper.pdf)

---

*We’re standing on the shoulders of giants, so we’d like to address huge kudos to all people involved in researching Plasma, state channels and Ethereum itself! The quality of the stuff posted here is insane.*

*Paul Berg*

## Replies

**gakonst** (2018-08-15):

Nice to see that more channel-like applications on top of plasma are being researched.

Some questions:

- In which cases would this be better than Plasma Debit?
- Will exits and challenges be the same as in plasma cash or will the exit game need to be modified?
- What do you mean in pg16 by ‘pseudo-escrow account’?
- How would you implement the atomic swap that gives the chargeback as described in pg17?

---

**androolloyd** (2018-08-15):

This looks really cool and sounds like a similliar design we’re working on at Groundhog(apart of ERC-948 working group) for our future state, as our plans encompass a plasma like system to act as our payment gateway for “streaming” payments as you’ve r ferried to. I haven’t heard of the talk by Andreas, will have to watch it.

Will follow intently.

---

**PaulRBerg** (2018-08-15):

Hey [@gakonst](/u/gakonst),

> In which cases would this be better than Plasma Debit?

Plasma Debit focuses on letting users exchange divisions of coins, i.e. 0 < a <= v, while we don’t do a at all. The “scripting language” will only accept basic coin transfers + updates related to streams, which conclude with either Bob getting the whole coin or issuing a chargeback. Moreover, we wanted to specifically propose (and later use in our code) Plasma Cash as it’s a more mature implementation.

> Will exits and challenges be the same as in plasma cash or will the exit game need to be modified?

The only significant difference is that the user cannot exit whilst streaming, as their funds will be in “limbo mode”. The token id in the sparse Merkle tree can be transferred to the operator as their cooperation is marked by inclusion in blocks.

> What do you mean in pg16 by ‘pseudo-escrow account’?

Pseudo-escrow was our way of conveying that Alice doesn’t hold the funds anymore, but she is able to cancel the stream at any time and redeem funds back. This is not escrow per se, as traditionally that requires either a third party arbiter or a strict set of rules for getting out and redeeming the funds.

> How would you implement the atomic swap that gives the chargeback as described in pg17?

Bob deposits funds equal to the value of the chargeback and then there’s a process similar to the one described in the Plasma Debit post (or even similar to LN) - Bob will get his coin from the operator only when he provides Alice the chargeback and both transactions occur successfully.

*Note: alternatives for 2 are being considered e.g. the coin may not be passed on to the operator, but rather sent to a burn address (like 0x00… on Ethereum). The protocol could issue “coinbase” transactions when a stream is ended. However, this would potentially create latent states and short the supply, and it generally feels it adds more assumptions to the table.*

---

**PaulRBerg** (2018-08-16):

Nice to hear that, Andrew! Pretty cool what you’re doing with Groundhog, too; a wallet which supports subscriptions is much needed.

Re Andreas’ talk - it’s insightful and entertaining as always, but his proposed example is salaries. Excluding volatility risks, the Lightning Network works fine for that as a business could theoretically run a node and sign cheap transactions once per hour, day, week or whenever the employee demands the salary (with a specific threshold as the interval shortens). The problem is with peer-to-peer or peer-to-company scenarios, where individuals cannot be online around the clock.

As a general idea, I think it’s important to draw a line between unit-based and time-based financial interactions. Payment channels work great for the former, i.e. paying for a coffee when you go out, but not so much for the latter, where time is a proxy for value.

---

**nud3l** (2018-08-16):

Thanks for sharing this! I am wondering about your proposed PoS consensus you’ll have on your separate chain. I gather you are going to use Tendermint with an adjusted Ethermint VM. Basically, when you are using collateral I am assuming you are going to have a changing set of validators as mentioned in [Tendermint’s documentation](https://tendermint.readthedocs.io/projects/tools/en/master/specification/validators.html).

Can anyone be a validator in your network and what are your thoughts regarding collateral size?

> Chronos is a secure and consistent state replication machine, with blocks
> achieving fast finality in seconds. It is Byzantine Fault Tolerant (BFT),
> thus it stays functional if less than a third of the nodes fail in arbitrary
> ways. Proof of Stake (PoS) is used as a Sybil control mechanism. In order
> to run on a Validator node, one needs to own CHR tokens and hold them
> as collateral against misbehaviour.

---

**androolloyd** (2018-08-16):

Thanks Paul, something we haven’t talked about much yet as it pertains to our future roadmap is the notion of The Groundhog Operator network, groundhog operators run a node similliar to what you’re proposing.

Users stake their tokens and then proceed to transact their pro-rata ownership of the networks tx volume.

Leveraging Delegated execution users sign a message and broadcast it to the network for later processing by one of the nodes.

Plasma Cash is where we’ve been focusing our research as well.

Glad to see the payment space getting some love.

---

**danrobinson** (2018-08-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/paulrberg/48/17405_2.png) PaulRBerg:

> Alice now controls an ERC721 representing her funds on the main-net

![](https://ethresear.ch/user_avatar/ethresear.ch/paulrberg/48/17405_2.png) PaulRBerg:

> making Bob give Alice her chargeback in the form of an ERC721

I don’t understand these references to ERC721 tokens. Why are you referring to ERC721 at all when the payments are necessarily being made in a fungible currency? Is this being used as a synonym for a Plasma Cash coin? If so, where does Bob get a coin that has the exact amount of the chargeback, for any arbitrary chargeback that could occur during the interval?

For example, if Alice locks up a 5 ETH coin in a 1 ETH / day stream to Bob, then Alice could potentially halt the stream after 1, 2, 3, or 4 days to force a chargeback in the amount of either 4, 3, 2, or 1 ETH. What if Bob doesn’t already have a coin in that precise denomination on the Plasma chain?

 (from paper):

> In the event of chain halting, Stream states are lost. Users can mass exit to the root chain, but balances are distributed according to the each Stream’s state at either initialisation or most recent mutation time. Alice and Bob can reach an agreement to fairly distribute funds.

This seems both damning (it gives extraordinary power to the Plasma chain operator) and avoidable. When someone withdraws from a stream directly to the main chain, why not use the time of their attempted withdrawal as the closing time of the stream, and compute the required partial payment from there?

For example, if there’s a 1 ETH / day stream from Alice to Bob with 1000 ETH locked up, and 600 days later the Plasma chain halts, either Alice or Bob should be able to initiate a withdrawal on the main chain that (after a delay for challenges) gives 400 ETH to Alice and 600 ETH to Bob. Or they could just let the stream continue and withdraw 200 days later to give 200 ETH to Alice and 800 ETH to Bob. Or after 400 days, Bob could just withdraw the entire 1000 ETH for himself.

---

**PaulRBerg** (2018-08-16):

Hey [@nud3l](/u/nud3l), thanks for your interest! Indeed, Tendermint with an adjusted Ehermint VM, but we’re also keeping our eye on the latest developments of WASM (Polkadot, Dfinity). There’s a long way ahead before implementing the consensus engine, and we’re taking our time to build something useful and grow a community of interested people around it.

![](https://ethresear.ch/user_avatar/ethresear.ch/nud3l/48/15112_2.png) nud3l:

> I am assuming you are going to have a changing set of validators as mentioned in Tendermint’s documentation.

Also correct. In particular, Cosmos has been doing great work on this with their Gaia testnets and we may end up following their footsteps (not reinventing the wheel), while keeping in mind that there has to be strong incentives for broadcasting blocks just like in the Nakamoto consensus. Also, slashing procedures might need to be more severe to preclude collusions. This is mentioned in chapter 6.4.2:

> It is crucial for Chronos to prevent Stream payees from colluding with Validators. Game-theoretical slashing mechanisms are in place but further research on stricter consensus mechanisms, such as Casper, has to be conducted to ensure maximum safety.

Then:

![](https://ethresear.ch/user_avatar/ethresear.ch/nud3l/48/15112_2.png) nud3l:

> Can anyone be a validator in your network and what are your thoughts regarding collateral size?

The first versions of the protocol will have only one Plasma operator, but testnets will ideally have around ~100 nodes, with many others sitting on the side to maintain fault tolerance. This great [article](https://medium.com/@davekaj/how-to-become-a-cosmos-validator-276862d5bfc7) provides in-depth details and specific figures.

Feel free to reach out via PM if you want to further ideate on this!

---

**PaulRBerg** (2018-08-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> I don’t understand these references to ERC721 tokens. Why are you referring to ERC721 at all when the payments are necessarily being made in a fungible currency? Is this being used as a synonym for a Plasma Cash coin?

Indeed, the references there were to the non-fungible Plasma Cash coins. Will update the original post and the white paper accordingly to make it clearer.

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> What if Bob doesn’t already have a coin in that precise denomination on the Plasma chain?

The assumption is that Bob has additional funds sitting on the main chain (that is, at least the maximum worth of the stream) and he deposits the value of the chargeback if Alice halts the stream. Although a bit far-fetched for now, we could imagine a future where liquidity providers (in this case, chargeback providers) run a profitable business on these Plasma chains - that is, they provide a service* by keeping a plethora of denominations on the side chain and doing atomic swaps on the main chain with many Bobs. This would mean though there is a commonly agreed minimum threshold, and all parties use it as a gcd.

Also (maybe pre-empting you here), it might be possible to apply the a and v model from Plasma Debit. Bob has an undercapitalised coin, ergo he’s able to receive funds from Alice via the operator, and Alice doesn’t need to get a chargeback coin because her a could be depleted instead. There seem to be trade-offs in each design, but this definitely sounds cool and something we’ll further explore.

** the fee for paying for these interactions with the ledger(s) are at the market’s whim, but, if Bob is a business, it is presumed that they will include them in the service and keep customers happy.*

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> This seems both damning (it gives extraordinary power to the Plasma chain operator) and avoidable. When someone withdraws from a stream directly to the main chain, why not use the time of their attempted withdrawal as the closing time of the stream, and compute the required partial payment from there?

This is a very good question and something which we want to carefully craft over the next months. In a perfect world, Alice and Bob should indeed receive 400 and 600 ETH, respectively, at the time of halting, but here’s what happens:

1. If the chain halts because the operator’s server crashes*, Alice is able to publish a proof of ownership for 1000 ETH and no one can contest that, as only the Chronos chain can understand the stream between Alice and Bob.
2. If the operator is malfeasant, they can just exit and enjoy the funds on the main chain. Alice cannot challenge the exit, because she agreed to “spend” their coin to the operator when the stream was started. Just like above, this pseudo-escrow is *only* reliable inside the Chronos scripting language, which understands a commitment of starting a stream and allocates funds based on elapsed time measured in block heights.

Importantly, if any of the two above are not definitive, i.e. the chain will come back alive before the challenge period on the main chain, parties may be able to get proofs for their coins and later challenge any fraudulent counterparties.

The halting scenario is deeply intertwined with the implications of the second question asked by [@gakonst](/u/gakonst) and, up to this point, a plausible workaround is a combination of:

1. Periodic public updates from either party involved in a stream; that way, Bob would get partial payments although the stream continues.
2. Strong cryptoeconomics by heavy penalising nefarious actions. The incentives for acting as a fair operator need to be higher than the ones for exiting an ongoing stream, hence parties may need to be severely slashed.

** We may make an update to clearly specify that stream states are lost, i.e. Alice gets 1000 ETH back, only when the operator’s server crashes.*

---

**danrobinson** (2018-08-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/paulrberg/48/17405_2.png) PaulRBerg:

> The assumption is that Bob has additional funds sitting on the main chain (that is, at least the maximum worth of the stream) and he deposits the value of the chargeback if Alice halts the stream.

This would require an on-chain transaction every time a stream is closed early. Since it also probably requires an on-chain transaction every time a stream is opened (unless Alice happens to have the right denomination to open it), why not just do the stream logic in a smart contract on the mainchain? What exactly is the Plasma chain giving you, other than (apparently, as described below) a central point of failure?

![](https://ethresear.ch/user_avatar/ethresear.ch/paulrberg/48/17405_2.png) PaulRBerg:

> Alice is able to publish a proof of ownership for 1000 ETH and no one can contest that, as only the Chronos chain can understand the stream between Alice and Bob.

![](https://ethresear.ch/user_avatar/ethresear.ch/paulrberg/48/17405_2.png) PaulRBerg:

> Just like above, this pseudo-escrow is only reliable inside the Chronos scripting language, which understands a commitment of starting a stream and allocates funds based on elapsed time measured in block heights.

Why not just have the exit function understand streams? It seems pretty simple to me—the Plasma coin (or the co-signed off-chain stream update, if they changed it off-chain) says the start time, the total amount (1000 ETH), the sender (Alice), the recipient (Bob), and the payment rate (1 ETH/day). The mainchain contract knows the early close time (the time when the attempted withdrawal of the coin happens on the main chain). So it can just do the math.

---

**PaulRBerg** (2018-08-19):

Thanks so much for thinking this through! It’s a really helpful discussion.

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> Since it also probably requires an on-chain transaction every time a stream is opened (unless Alice happens to have the right denomination to open it), why not just do the stream logic in a smart contract on the mainchain?

I guess you’re referring to something like this:

https://github.com/ChronosProtocol/poc/blob/master/contracts/Stream.sol

The rationale for choosing the infrastructure as proposed in the OP over an on-chain smart contract is:

1. Fast finality via a single operator/ PoS set of validators, getting rid of reorgs and uncles
2. Better time measurement, due to shorter interval blocks
3. Cheaper state updates

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> The mainchain contract knows the early close time (the time when the attempted withdrawal of the coin happens on the main chain). So it can just do the math.

Hmm you’re completely right! I was unconsciously imagining the Plasma contract as a black box, probably because of this excerpt:

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png)[Plasma Cash: Plasma with much less per-user data checking](https://ethresear.ch/t/plasma-cash-plasma-with-much-less-per-user-data-checking/1298/3)

> I’m not sure it would work to use a ZK-snark for the non-existence proofs, unless the parent chain is willing to accept ZK-snarks for the exit transactions. Otherwise, you don’t have enough information to respond to a challenger, right?

zk-SNARKs are a different beast though. For streams, you can just do the difference between the closing and starting times and multiply by the rate - and indeed, the closing block could be the withdrawal attempt time. The chains have different block numberings, but you could potentially agree on a rough estimation of time/value of money if you keep a block height scaling coefficient in the contract (and update that accordingly over time, similar to how retargeting works in PoW).

The only problematic edge case I see is when the rate is calculated at smaller intervals than the block time on the main chain. That is, if the agreed off-chain rate is x units per y seconds and we consider the main chain to have z seconds blocks, where z>y by a non-trivial margin, the potential loss could be as high as (z-y)*x (“loss” as in Bob would get that money instead of Alice, because she tried to exit exactly y seconds after a block was generated on the main chain). I admit though that this potential loss is negligible in most cases, especially when building an MVP.

---

**sid** (2018-08-27):

Hey guys,

Thanks for sharing this. Great work.  Just a quick question - would this work for DAICOs?

---

**PaulRBerg** (2018-08-28):

Hey [@sid](/u/sid), potentially, but not in the near future. The model in the OP works well for peer-to-peer streams, that is, maximum 2 parties involved.

The topology is different with DAICOs, as they require constant coordination among many investors and there’s definitely a lot of voting sessions. However, we thought about SICOs - Streamed Initial Coin Offerings.

You scratch the global `tap: num(wei/ sec)` and set up a stream between every individual and the token creators. Now, all investors can arbitrarily mutate the state of their own stream, based on project’s performance. Just like with DAICOs, funds already streamed belong to the token creators and no one can take it from them, but investors also have the power to lower the rate or even close the stream whenever they want.

*Note: the above is merely a random idea posted as a comment on a forum, there is no fully-fledged proposal describing these “SICOs”*

