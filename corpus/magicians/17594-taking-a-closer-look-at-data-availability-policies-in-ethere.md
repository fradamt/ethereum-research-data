---
source: magicians
topic_id: 17594
title: Taking a closer look at data availability policies in (Ethereum) rollups
author: eawosika
date: "2023-12-22"
category: Magicians > Primordial Soup
tags: [layer-2, rollups, data-availability]
url: https://ethereum-magicians.org/t/taking-a-closer-look-at-data-availability-policies-in-ethereum-rollups/17594
views: 1880
likes: 3
posts_count: 4
---

# Taking a closer look at data availability policies in (Ethereum) rollups

[Data availability](https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding) is a critical consideration for blockchain scaling designs; [rollups are the preferred scaling solution for Ethereum today](https://ethereum-magicians.org/t/a-rollup-centric-ethereum-roadmap/4698) because availability of data required to reconstruct the L2 state is guaranteed by the L1 network. But data availability—especially in the context of rollups—has many subtle, easy-to-miss details that are nevertheless important for security.

With “L2 summer” finally happening, and modular data availability layers moving from theory to production, educating the community on the implications of rollups’ approach to data availability for security and decentralization has become more important than ever. It is especially  important for users to know how differences in where transaction data is stored determines if a rollup is “secured by Ethereum” or not.

As a contribution to this effort, I [put together an article that covers the topic of data availability](https://research.2077.xyz/data-availability-or-how-rollups-learned-to-stop-worrying-and-love-ethereum) from first principles, discussing the (in)famous “data availability problem” in Layer 1 (L1) and Layer 2 (L2) blockchains—before exploring the different approaches rollup blockchains adopt to guarantee data availability, including publishing transaction data on Ethereum and using external data availability services.

Some other topics covered include:

1. [The relationship between economic security of a data availability layer and the security guarantees it provides to rollups using it.
2. Drawbacks and challenges around using alternative data availability layers, rather than Ethereum, to store rollup data.
3. Differences in approaches to storing transaction data on Ethereum (spoiler: not every “Ethereum rollup” stores state data on Ethereum the same way).

All feedback and comments are welcome. I’d also like to know what others in the community think of the movement towards alternate data availability layers, and how that impacts the future of Ethereum’s rollup-centric roadmap.

PS: Also adding some recent tweets from the L2Beat team for context on emerging issues around rollups on Ethereum integrating with modular data availability layers:

- Thread by @donnoh: x.com
- Thread by @Bartek: x.com
- Thread by @Bartek: x.com
- Thread by @Bartek: x.com

## Replies

**middlemarch** (2024-01-04):

Great article!

Curious to get your opinion on the limits of data availability—i.e., if our data availability implementation was perfect and L1 smart contracts knew everything about the L2 state at all times, would there be important things we still couldn’t do?

It seems to me that a very important thing we couldn’t do is figure out who owns what assets in the case of a full L2 shutdown.

E.g., if Arbitrum shut down and there was $6B in L1 bridges that Arbitrum controlled and Arbitrum needed to fairly distribute that $6B in (say) a week before it went out of business, what would it do?

With full knowledge of L2 state it could send all EOAs their L2 balances on the L1. But what about L2 smart contract balances? This would be billions of dollars and there is not enough information in L2 state to assign unambiguous ownership to this massive sum.

Consider a loan: suppose Alice borrows 100eth from Bob giving her bridged CryptoPunk as collateral. Alice either has to pay Bob 100eth and get the Punk back or not pay Bob back and forfeit the Punk. With six months left on the loan, the L2 shuts down. Alice doesn’t have the money to repay the loan now. What happens to the Punk?

Here’s a live example, though it’s more contrived:

https://basescan.org/address/0xe6479a2b7dfb60deebe25c6b0e082149ed371238#code

What happens to the ether in this contract if Base shuts down before someone wins the contest? Or rather how does Coinbase distribute the corresponding L1 ether without changing the terms of the contest?

Does the L2 owner need to adjust the terms on all contracts in a way they find “fair”? Or else how do they determine how to distribute the bridge funds.

Given Arbitrum’s major outage of only a few weeks ago, I think it’s clear that we can say “when, not if” about a large L2 shutting down. Perhaps forced inclusion could be used to run an L2 indefinitely, but I haven’t seen that idea suggested.

Is the space’s focus on data availability missing what users will actually want in the case of a disastrous shutdown? I.e., their money back?

---

**eawosika** (2024-01-12):

Hi [@middlemarch](/u/middlemarch). I admit this is an interesting problem that I haven’t thought about previously. Still, I can give my two gwei: The most feasible solution I can think of is that exiting funds “fairly” will require some coordination at the social layer (as opposed to what would happen if we were purely exiting funds from the rollup’s L1 bridge).

Is it correct to assume the `GuessTheMagicNumber` contract is a Ponz-like contract where anyone can pay a small fee per transaction–which accrues to the contract balance–and then, if they successfully guess the “magic number”, they can withdraw all the funds in the contract (i.e., funds contributed by users who failed to guess the number currently)?

If that’s the case, a developer might say something like “send a proof you sent `X` ETH to the contract” and match those proofs against the transaction data posted by the sequencer to L1. It’s a convoluted solution–and assumes the developer has administrative controls–but, at least, the availability of the rollup’s transaction history on L1 should make it easier to distribute those funds in a “verifiably fair” way. Of course, this means Coinbase has to change the terms of the contest like you suggest (I assume, in a normal scenario, only the caller that guesses the number gets the full payout).

The question of what happens to Alice’s punk would likely involve a similar off-chain agreement (e.g., bridge the Punk back to L1 and keep it an escrow contract until Alice pays back 100 ETH). But maybe you have a more technical solution to the problem that can be implemented at the base layer of the rollup? I’d be interested in hearing about it.

---

**middlemarch** (2024-04-07):

Thank you for this thoughtful response and my apologies for missing it!

My examples above I think could be resolved by good faith social-layer solutions, but I think there are other situations that couldn’t. Imagine a complicated Defi scenario where the value of two assets are connected and “who sells first” is important.

Here’s a reductive example: Contracts A and B each have 100eth in them. They both have the rule “If the other contract has 100eth in it, then my eth can be withdraw. Otherwise it’s locked.”

In such a scenario one contract is going to have 100eth locked forever. The contract that will be depends on whether A or B is withdrawn from first. But this is a non-deterministic question and can only be resolved by a sequencer. And by hypothesis the sequencer is down! There’s probably some protocol that could be invented at the social level to resolve this, but if you had that then couldn’t you run the L2 indefinitely? Or, put another way, that protocol is called Ethereum!

I have indeed been working on a technical solution to this problem, an approach to Ethereum scalability that guarantees 100% uptime, though it requires side-stepping the entire L2 paradigm, which makes it a tougher sell.

It’s called Facet (`https://facet.org`). The idea is to use the Ethereum L1 with no dependencies by sending transactions not to smart contracts, but rather to a burn address. Then, off-chain indexers can apply deterministic calculations to reconstruct state. Because all transactions are sequenced by the validators your transactions have the liveness and verifiability of the L1. And because the protocol requires only deterministic calculations there the state can be deterministically verified as well.

Would love to get your thoughts!

