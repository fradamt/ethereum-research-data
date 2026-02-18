---
source: ethresearch
topic_id: 11182
title: "DeFi: Recourse and tail risks"
author: cc7768
date: "2021-11-04"
category: Economics
tags: []
url: https://ethresear.ch/t/defi-recourse-and-tail-risks/11182
views: 4225
likes: 16
posts_count: 7
---

# DeFi: Recourse and tail risks

DeFi executes fast and capital efficient liquidations and other similar transactions by using flash loans and real-time price oracles. However, the cost of this efficiency is that there are rarely options available for recourse when something goes wrong. Recourse is useful because it gives parties a way to address deviate outcomes ex-post.

Consider the following examples where recourse might have resulted in a different, more anticipated, outcome:

- Incorrect prices provided to contracts (1) (2) (3)
- Incorrect liquidations due to manipulated prices (1) (2)
- Auctions accepting zero bids due to network congestion (1)
- Governance bugs (1) (2)
- Flash loan attacks (1) (2)

The intent of these examples is not to denigrate any of the protocols involved, but rather to demonstrate that DeFi users accept significant tail risk by operating in an environment without recourse. This type of tail risk is not present in TradFi, so why do we accept these risks in DeFi?

In this article, we attempt to formalize some of our internal discussions about this tail risk by focusing on the trade-off between three properties of financial systems:

1. Anonymity: Anyone can interact with anyone in a trustless manner; whether or not they know their counterpart
2. Instant resolution: A transaction is settled as soon as it has been processed. For example, a liquidation in DeFi is processed in the same block that it is sent.
3. Recourse: Ability to dispute the validity of a particular transaction and seek reparation.

These properties apply differently to various financial systems:

### TradFi

TradFi has instant resolution and recourse, but does not have anonymity.

For example, consider the purchase of a stock. When an individual purchases a stock, it appears in their portfolio. If the stock does not show up in their portfolio then the individual can take legal action against their broker. Anonymity in this system is impossible because participants must be able to identify one another in order to seek compensation through the judicial system.

### Fast DeFi

The vast majority of DeFi today operates under what we call “Fast DeFi”. Fast DeFi provides instant resolution and anonymity, but does not have recourse options available.

In order to have instant resolution, Fast DeFi needs access to instantaneous and robust price feeds. This can be difficult because there can be manipulations of the actual market price even when the price feed reports the price correctly.

Flash loans are a powerful innovation created for DeFi. They allow any individual, independent of their personal access to capital, to borrow the capital required to liquidate even the largest positions. Flash loans require instant resolution which is one reason why Fast DeFi prioritizes instant resolution over recourse.

Regarding the lack of recourse, consider how a liquidation on a protocol like AAVE or Compound works: One (anonymous) user determines that another (anonymous) user’s position is under-collateralized according to a price reported by a real-time price oracle. The first user submits a transaction (possibly using flash loans) to repay a fraction of the second user’s debt and, in return, is given some fraction of the users collateral. There is instant resolution and both users remain anonymous, however, liquidated users have no opportunity for recourse if the liquidation occurred at an inaccurate price.

### Slow DeFi

There are some pieces of DeFi where we can create delays without degrading the user experience. We refer to these types of DeFi applications as “Slow DeFi”. Slow DeFi sacrifices instant resolution to achieve anonymity and recourse.

For example, a predictions market, like Augur or Polymarket, allows users to take positions on relatively bespoke questions like, “Will there be a named tropical system Wanda that forms before November 1, 2021?” A user can trade on these outcomes using the prices implied by the demand for each token. Individuals who trade this type of an asset are often operating on a longer time-horizon so instant resolution is a lower priority for them.

A small percentage of DeFi applications currently operate in the Slow DeFi environment, but Slow DeFi has been successful in settling certain types of smart contracts where users value recourse over resolution.

## The future of DeFi

The question is, what is the future of DeFi if the status quo regarding recourse continues? Or what if DeFi seeks wider availability of recourse? The above framework for how to think about financial systems emphasizes the trade off between instant resolution and recourse in the DeFi space, where anonymity is usually prioritized. Over the next few years, there are a few ways that DeFi could evolve:

### The lack of recourse is embraced

While a system without recourse is incompatible with today’s traditional finance systems, this may not be a catastrophic blow. There are significant benefits to DeFi and it is plausible that the tail risks are perceived to be sufficiently small that it is not worth the investment required to establish a recourse-compatible Fast DeFi system.

There are a few things we should take into account if DeFi ends up on this path:

- There are certain subsets of the population that will be crypto-hesitant while recourse is unavailable. In other words, it is hard to imagine a CFA putting client’s life savings into DeFi without a viable option for recourse.
- We should allow tail risk to be priced in. Right now, tail risk is not priced in because assets typically are forced to trade at their off-chain market value. Importantly, this off-chain value does not account for on-chain risk. For example, a synthetic representation of an equity on the blockchain may trade at a discount relative to fair-value because there is a higher probability that the DeFi synthetic is lost in an attack. This doesn’t mean that this synthetic will trade at a discount, though, because there are also benefits in DeFi that might lead the synthetic to trade at a premium.

### Options for recourse emerge

It is also plausible—whether through innovation or regulation—that providing options for recourse becomes the standard for many DeFi protocols.

We have a few ideas for how recourse could be provided:\

- The expansion and broader uptake of existing insurance protocols. Protocols like Nexus Mutual already provide insurance for certain types of smart contract failure and other hacks.
- More slow DeFi. Slow DeFi is clearly not a good fit for all types of DeFi applications, but it could be used more widely than it currently is. Contracts that operate on a longer time-horizon and don’t require liquidations make good candidates.
- Another alternative is to create “insured oracles” which would align incentives between the user and the oracle. Currently, risk is fully assumed by the users, whereas the oracle is insulated from the consequences of their reported prices. An insured oracle might operate in the following way:

A user requests a price that they can use to liquidate a position of size $X. (off-chain)
- The insured oracle responds with two things: A fee that they would need to be paid to provide a price, and, a price that they would be willing to insure for the liquidation. This price might be higher than the market price if there is uncertainty or suspicious fluctuations. (off-chain)
- The user then utilizes that message on-chain to obtain a price that they can perform the liquidation with and the oracle’s message is used to lock $X of the insured oracle’s capital into a recourse contract.
- If the person liquidated feels that the price was inaccurate, they could seek recourse against insured oracle’s locked $X.

## What to do?

In a space as fast-moving as DeFi, no doubt more refined and robust solutions for recourse will emerge. Or they will not, and tail risk will be accounted for in other ways. Exploring whether or not recourse should be available highlights areas for growth in DeFi and the potential pitfalls of an ever evolving financial landscape.

Chase (UMA)

This article benefited from discussions with the entire team at UMA. A special thanks to Hart Lambur, Clayton Roche, and Kevin Chan for comments on this post. Any remaining lack of judgement or other errors are solely my own.

## Replies

**bowaggoner** (2021-11-05):

Great post, thanks! I’ll have some comments/questions, let me start with this one:

If we stick to the ethos/philosophy that ‘the code is the law’, I’m not clear on the distinction between recourse and just a change in the incentives of the protocol. In other words, to have the concept of recourse, it seems like we need a set of rules that it is possible to break (i.e. norms that are not enforced by the code) and consequences for breaking them. This opens up lots of questions - who makes these rules, who gets to decide when they’re broken, and how does it happen if not code? Would love your thoughts.

---

**cc7768** (2021-11-06):

Thanks for the response. Glad you enjoyed it.

> If we stick to the ethos/philosophy that ‘the code is the law’, I’m not clear on the distinction between recourse and just a change in the incentives of the protocol.

I agree that this should be viewed as a change in incentives. One of my favorite concepts from game theory is that off-equilibrium paths determine equilibrium behavior. If we could find a way to prevent “undesirable behavior” from being rewarded then in equilibrium we would not see the behavior (or at least less of it).

> In other words, to have the concept of recourse, it seems like we need a set of rules that it is possible to break (i.e. norms that are not enforced by the code) and consequences for breaking them. This opens up lots of questions

> who makes these rules

Short answer: I don’t know. Maybe DeFi as a whole? Maybe created case-by-case for each protocol?

Longer answer: Every community eventually establishes certain norms on its own. I think there are already some norms in DeFi about what is an “acceptable arbitrage opportunity” and what isn’t. This doesn’t mean that people aren’t willing to exploit these opportunities, but some actions seem to be generally frowned upon. Part of the goal of this article was to start a conversation about whether these rules should exist.

> who gets to decide when they’re broken

*If* DeFi ends up choosing to go a route with recourse then I think a variety of options will emerge. Each of these options will face certain trade-offs and individual protocols (or their users) will be able to make a choice to best fits their needs.

> and how does it happen if not code

Human judgement is surprisingly robust because, while we can’t always describe exactly what might go wrong, we “know it when we see it”. I think we can maintain a trustless environment if we complement the human judgement with thoughtful code to manage the outcomes.

For example, consider Nexus Mutual. I can choose to insure assets stored in {some protocol} and, if a hack were to occur, then I could submit a claim and humans would vote to approve or deny my claim based on the details submitted.

---

**SUPERCYCLIST77** (2021-11-17):

If a project mis-reports data feeds to a lending protocol the matter of damages is between the data provider (usually Chainlink or one of the large data providers) and the data consumer (usually a project). Projects that have risk and want to insure these specific damages should seek specific protection around the relevant claims to damages they may have as a result of the other party’s behavior. The responsibility does not fall on an ambiguous collective of people but specific people on specific teams arranging these operations to ensure their systems work. If their systems don’t work competition should provide opportunity for someone else to step in and do things better. When users are harmed projects should think about best techniques to make users whole if possible or just risk losing lots of users like Nuo did. If your liquidation systems suck and have janky architecture people will use other stuff.

---

**cc7768** (2021-11-22):

> The responsibility does not fall on an ambiguous collective of people but specific people on specific teams arranging these operations to ensure their systems work.

The point of this post isn’t to establish an ambiguous collective of people that should take responsibility for all non-price risk in DeFi.

The fact that there are outcomes that the community broadly views as “undesirable” means that there is an opportunity for DeFi protocols/researchers to explore what recourse means, evaluate the costs/benefits of recourse, and innovate in ways that make the space less risky. No project would, or should, be forced to adopt tools that they don’t want, but there are many projects that might be interested in collaborating on how they can better protect their users.

> If their systems don’t work competition should provide opportunity for someone else to step in and do things better… If your liquidation systems suck and have janky architecture people will use other stuff.

Maybe. I think it’s more complicated than that because the quality of a new project isn’t always clear and by the time that a vulnerability is found by the team, it’s often too late.

The links at the top of my post illustrate a variety of failures, many of which occurred to projects that are among the top tier of DeFi projects. It’s really hard to foresee all possible code paths that end in failure.

---

**bowaggoner** (2021-12-01):

A second question. I learned from [@kelvin](/u/kelvin) to rethink whether everything DeFi should necessarily happen “on chain” (or at “layer 1”). E.g. “Fast DeFi” needs to happen quickly, but perhaps it can happen quickly at some higher level and be settled more slowly on the chain. I think some of what he writes in this post is relevant: [High-frequency trading and the MEV auction debate](https://ethresear.ch/t/high-frequency-trading-and-the-mev-auction-debate/10004)

I generally expect to see proliferation of “semi-trusted” exchanges and platforms in the future. I picture these being cheaper and more efficient than anything based on smart contracts on-chain. They could offer anonymity and instant resolution through DeFi-like APIs, but they would be less secure as you’d have to put some trust in the institution (not the other participants) which syncs regularly to the main chain.

So my question is, do you see that as a desirable option, and do you think they might help achieve anonymity/instant resolution/recourse at a cost of security/trust?

---

**cc7768** (2022-02-04):

Hey [@bowaggoner](/u/bowaggoner) - Sorry for the big time spike on this. I put it on my todo list to read the link and then respond then the holidays happened and it fell off my radar ![:sleeping:](https://ethresear.ch/images/emoji/facebook_messenger/sleeping.png?v=10)…

Thanks for linking that post! I found it quite interesting on a number of dimensions (even beyond its scope for this post).

In terms of your question, I have mixed feelings on “semi-trusted” exchanges.

On one hand, this isn’t so far from how L2 chains currently operate and I think L2s have already made a big positive impact on Ethereum. I don’t understand 100% how they operate, but I think (for now) they have a single sequencer that executes transactions in a “fair” (as defined by them) order.

I would worry a little about how censorable/subject to government intervention a “semi-trusted” exchange might end up being. i.e. Will they be forced to try and KYC which weakens the anonymity aspect and moves us closer to TradFi.

In the context of recourse, it seems like the main advantage would be that the semi-trusted exchange could manually revert suspicious transactions/outcomes before they were propogaged back to the chain? Is that what you had in mind?

