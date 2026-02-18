---
source: ethresearch
topic_id: 20288
title: Censorship Insurance Markets for BRAID
author: jonahb27
date: "2024-08-16"
category: Proof-of-Stake > Block proposer
tags: [censorship-resistance]
url: https://ethresear.ch/t/censorship-insurance-markets-for-braid/20288
views: 1218
likes: 4
posts_count: 5
---

# Censorship Insurance Markets for BRAID

[![BRAID](https://ethresear.ch/uploads/default/original/3X/b/f/bf7665c93b36acdfa0cb7c8ed757aa3ef87f101f.jpeg)BRAID512×512 72.1 KB](https://ethresear.ch/uploads/default/bf7665c93b36acdfa0cb7c8ed757aa3ef87f101f)

By: [Jonah Burian](https://x.com/_jonahb_) and [Ben Levy](https://x.com/BenLevy0)

*Tl;dr: We point out that BRAID’s liquidity requirements lead to poor user UX and suggest censorship insurance markets as a potential solution.*

*Thanks to [Max Resnick](https://x.com/maxresnick1) and [Davide Crapis](https://x.com/davidecrapis) for the feedback.*

## Intro

> “The greatness of America Ethereum lies not in being more enlightened than any other nation blockchain, but rather in her ability to repair her faults.” - Alexis de Tocqueville

Censorship resistance (CR) is one of the core security properties of a blockchain.

[![CR](https://ethresear.ch/uploads/default/optimized/3X/c/7/c7e58a93fe9b45a91ecf29a6aefa91567c310262_2_690x180.png)CR1096×286 43.4 KB](https://ethresear.ch/uploads/default/c7e58a93fe9b45a91ecf29a6aefa91567c310262)

Ethereum gifts proposers with one-slot monopolies on transaction inclusion, creating a principal-agent problem and a single point of failure. A censoring party can bribe the current proposer to censor a transaction.

There has been considerable work to mitigate this problem. A key insight is that the weak link problem of a single proposer results in weak CR. Multi-proposer schemes like [BRAID](https://www.youtube.com/watch?v=mJLERWmQ2uw) and [FOCIL](https://ethresear.ch/t/fork-choice-enforced-inclusion-lists-focil-a-simple-committee-based-inclusion-list-proposal/19870/1) can correct this principal-agent problem.

In this piece, we focus on BRAID, a multi-proposer mechanism that has garnered significant recent attention. It aims to increase CR in a capital-efficient way via a conditional tipping mechanism (explained below).

One challenge in this approach, the need for a deterministic ordering rule, is already well understood. ***In this piece we identify another challenge—liquidity requirements that adversely affect UX—and propose a few potential solutions.***

## BRAID at a High Level:

BRAID runs k subchains in parallel, each with a unique proposer. Block n of Ethereum is the union of transactions from block n of the k subchains, with a special ordering rule applied to order this unordered set.

### Tipping in BRAID

Bidders submit a conditional twin tip (t,T) which depends on the number of proposers who include the transaction. If only a single proposer includes a transaction, they receive T; if multiple proposers include the transaction, they split t.

### Tipping Properties

Let ϕ(t,T) be the minimum cost to censor a BRAID transaction. It has been [shown](https://arxiv.org/abs/2301.13321) that ϕ(t,T)=kT.

The goal of BRAID is that users will most likely never actually have to pay T; instead, they pay t, which can be much lower than T.

This multi-dimensional tip disentangles the cost of inclusion (for the transacting party) from the cost of censoring such that t<<T.

Simply put, a user get’s kT worth of CR while (usually) only paying t.

**How Users Will Tip:**

- T: From a user’s perspective, they set T=\frac{V}{k} where V is the value the user places in their transaction not being censored.
- t: In current BRAID specs, the ordering of transactions depends on t, with more favorable ordering (i.e., coming first) given to those with the highest t. Therefore, a user will choose their t based on where they want to be in the ordering.

*Note that if a user does not care about CR, they can set T=t and send their transaction to just one proposer.*

## The UX Challenge:

While a user will only pay t for their transaction, they need to have T available to make a credible promise to the protocol that they can pay T. Hence a user needs to have T of additional available liquidity to make a transaction. We saw before that T \propto V: T tends to scale with the value of the transaction. This burdens users with a liquidity requirement.

For example, say a user wants to sell $5M of ETH due to impending interest rate fears and values censorship resistance at $1M. Let’s say there are 4 shards, i.e., k=4. The user needs to have $250k of additional unpledged liquidity available just to exit their position. This hampers the UX of on-chain finance by placing additional and obscure liquidity requirements on participants that scale with the value of their positions.

## Fixes:

### Proof of Post-State Liquidity

**Idea:** A user submits a transaction with a proof that they will have enough liquidity to pay T if necessary after their transaction. In the case before, the proof will show that the transaction will give the user $1M of liquidity so they could afford the T= $250k if necessary.

**Problem:** This assumes that a proposer has a good understanding of the post-state of a transaction. Most financial transactions interact with shared state, and as a result, transaction ordering is needed to know the post-state. This knowledge relies on the final ordering so we can’t include it as an input to the transaction. Even when there is a reasonable lower bound on post-state available liquidity, establishing it would (unrealistically) require bespoke proofs for each transaction type.

### Censorship Insurance (CI)

**Idea:** A third party–the CI provider–can sponsor the escrow of T for the transaction. Users will have to pay an insurance premium of rT to the CI provider, where r represents the rate (mostly) based on the likelihood of censorship. CI providers are thus assessing the rewards of censoring the transaction in real time to ensure it is below kT.

To prevent an attack where a user purchases insurance and then only sends their tx to one proposer whom they are colluding with, the CI should be (one of) the relayer(s) for the tx. This mirrors how gas sponsorship works and indeed CI insurance should likely just be included in a gas sponsorship service.

Effectively a user pays a total of t + rT for their transaction and only needs to have t + rT on hand as opposed to T, which is frequently more than t + rT.

An additional benefit of this scheme is that a marketplace of at least two CI providers will conveniently alert users when their T is too low and there is a high risk of censorship because they’ll refuse to censorship-insure the transaction at a reasonable rate.

**Problem:** It will be difficult to bootstrap a two-sided marketplace for this from scratch.

### CI Market Structure

In practice applications or wallets will likely claim jurisdiction over this issue. One possible solution to the bootstrapping problem, therefore, is for applications and/or wallets to sign wholesale agreements with CI providers à la PFOF.

While the above solution likely works fine, another option is to create a proper on-chain market with e.g. an RFQ for each transaction whose sender wishes to purchase censorship resistance for.

[![snake](https://ethresear.ch/uploads/default/original/3X/0/4/049237e341dc88cd24cde968c71e70ce689c3444.png)snake240×240 3.53 KB](https://ethresear.ch/uploads/default/049237e341dc88cd24cde968c71e70ce689c3444)

This market, fittingly, would benefit from the CR properties of BRAID.

## Conclusion

BRAID is still in its early days as a proposal. The UX issue of liquidity requirements has not been sufficiently explored, though there are promising signs that we can reasonably punt the issue to the application layer. For next steps, we suggest further exploration of the feasibility of CI markets.

## Previous work:

- Censorship Resistance in On-Chain Auctions: Elijah, Max, Mallesh
- Concurrent Block Proposers in Ethereum: Mike, Max
- Introducing Multiplicity: Duality blog
- ROP-9: Multiplicity gadgets for censorship-resistance RIG
- BRAID: Implementing Multiple Concurrent Block Proposers: Max
- Fork-Choice enforced Inclusion Lists (FOCIL): A simple committee-based inclusion list proposal: Thomas, Barnabé, Francesco and Julian

## Replies

**murat** (2024-08-19):

Thanks for the post and the exploration of a promising direction. I have two points of discussion:

1. CI censorship: let’s assume we have a tornado.cash transactor who is being censored by the current Ethereum setup. BRAID addresses their problem, yay. Now they’re looking to use a CI to get their tx on-chain. It seems that the CI providers would censor their tx just the same as providers will presumably comply with OFAC, so we haven’t moved the needle much. The transactor does have the option to have T though, but this defeats the purpose of CI as far as I understand. Basically, CI wouldn’t function in cases where it’s most needed?
2. can’t you have a CI instead of BRAID to achieve CR without protocol changes? Basically have potentially censored transactions be sent to a CI provider with a CI fee, they always get on chain within some block height limit. The market for this should be of similar size as the market for BRAID. It does raise questions about who would operate a CI as it seems like a one way ticket to go on the OFAC list though.

would love to hear your thoughts!

---

**benlevy0** (2024-08-21):

Thank you for the comments, [@murat](/u/murat).

1. This proposal would improve UX for the vast majority of users who are not looking to evade the law. You’re right that this would most likely not benefit those who are.
2. The current Ethereum doesn’t have a conditional tip so there is no possibility of CI. An analogous notion in the current regime is gas sponsorship, and the user can choose to pay a high tip for better CR. (But a gas sponsorship relayer would not be able to guarantee inclusion.)

---

**murat** (2024-08-21):

Thanks, censorship resistance spans much greater than to evade the law in a particular country. The example would apply for any censorship case, the point is that CI providers can censor, so if you’re a particularly censor-susceptible transactor who would be the #1 beneficiary of CR, this CI setup would still leave cases where you’re experiencing censorship. However this may be a fundamental problem with providing insurance than with this particular proposal (e.g. those who need car insurance the most are the most frequent crashers who are the most difficult to insure)

For #2, you could create a contract with this functionality that takes in an additional tip parameter. Even if we go in the protocol change direction, the surface area to change the protocol to add CI seems to be much lesser than for BRAID, for almost the same benefit of CR? Basically if we have CI with Ethereum today, do we not solve for most CR for a fairly small lift?

---

**EntropicRaven** (2025-02-23):

> Effectively a user pays a total of t+rT for their transaction and only needs to have
> t+rT on hand as opposed to T, which is frequently more than t+rT.

The escrow resembles a collateral—widely adopted by various DeFi lending protocols. However, they usually involve over-collateralization, which means t+rT>T. It might be worth borrowing the lesson from DeFi: the reason behind this excessive liquidity lock-up, which the insurance for BRAID aims to avoid, is due to a combination of (a) adverse selection: that users are anonymous, so a high collateral is required for high-capital-efficiency users to self-select into the market as means to warrant the repayment capabilities, or equivalently in your case, to insure; and (b) moral hazard: there is an ongoing need for users to maintain insurance asset value, so even more capital is required to hedge the asset value volatility and the risk of mismanagement, specifically if your mechanism cannot verify t+rT. It is also because users can misreport, or can dump some junk assets that will soon plunge in value.

