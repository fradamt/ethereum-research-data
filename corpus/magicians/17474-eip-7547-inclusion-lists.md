---
source: magicians
topic_id: 17474
title: "EIP-7547: Inclusion lists"
author: mikeneuder
date: "2023-12-18"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7547-inclusion-lists/17474
views: 6084
likes: 19
posts_count: 19
---

# EIP-7547: Inclusion lists

Discussion thread for [Add EIP: Inclusion lists by michaelneuder · Pull Request #7943 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7943)

## Abstract

Censorship resistance is a core value proposition of blockchains. Inclusion lists aim to provide a mechanism to improve the censorship resistance of Ethereum by allowing proposers to specify a set of transactions that must be promptly included for subsequent blocks to be considered valid.

## Motivation

Since the merge, validators have started outsourcing almost all block production to a specialized set of builders who compete to extract the most MEV (this is commonly referred to as Proposer-Builder Separation). As of October 2023, nearly 95% of blocks are built by builders rather than the proposer. While it is great that all proposers have access to competitive blocks through the `mev-boost` ecosystem, a major downside of externally built blocks is the fact that the builders ultimately decide what transactions to include or exclude. Without any forced transaction inclusion mechanism, the proposer is faced with a difficult choice: they either have no say on the transactions that get included, or they build the block locally (thus have the final say on transactions) and sacrifice some MEV rewards.

Inclusion lists aim to allow proposers to retain some authority by providing a mechanism by which transactions can be forcibly included. The simplest design is for the `slot N` proposer to specify a list of transactions that must be included in the block that is produced for their slot. However, this is not incentive-compatible because builders may choose to abstain from building blocks if the proposer sets some constraints on their behavior. This leads to the idea of “forward” inclusion lists, where the transactions specified by the `slot N` proposer are enforced in the `slot N+1` block. The naïve implementation of the forward inclusion lists presents a different issue of potentially exposing free data availability, which could be exploited to bloat the size of the chain without paying the requisite gas costs. The free data availability problem is solved with observations about nonce reuse and allowing multiple inclusion lists to be specified for each slot. With the incentive compatibility and free data availability problems addressed, we can more safely proceed with the implementation of inclusion lists.

**Related work** – [inclusion-lists-related-work.md · GitHub](https://gist.github.com/michaelneuder/dfe5699cb245bc99fbc718031c773008)

## Replies

**Mani-T** (2023-12-20):

It provides a mechanism for proposers to retain some control over transaction inclusions, offering them authority in the block production process. ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

---

**wjmelements** (2023-12-20):

Ideally the proposer also has plausible deniability.

---

**themandalore** (2024-01-22):

Super cool idea.  Let me see if I get it straight though:  We have two groups: validators and builders.  Builders are censoring at a rate of X and Validators at a lower rate of Y.  The idea here is to make it so that Validators can remove the ability of builders to censor their transactions, thus moving the whole system to min(X,Y) vs the current situation of max(X,Y)?

I think it is a win, but the big issue I have is that the reason validators weren’t/ aren’t censoring is that the legal culpability falls on the builders if they just “take the built block”.  By adding in the ability to select the transactions, you could change the dynamic to where validators are now responsible for the transactions, thus making them more likely to censor (like the builders) and more of a regulatory target.

---

**0xEvan** (2024-01-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mikeneuder/48/10625_2.png) mikeneuder:

> As of October 2023, nearly 95% of blocks are built by builders rather than the proposer.

What do you think is a better split - 50/50? 33/67? 80/20?

Should it be closer to 50/50 or does this aim to give validators more than 50% authority in blocks built?

---

**nflaig** (2024-01-26):

Thanks for all the writeups on inclusion lists, after reading through the material, I have a few questions / concerns and have not found a lot of discussion around this so far.

1. Should the protocol be opinionated about transactions, especially since there does not seem to be a objective criteria to proof (onchain) that a transaction is being censored. I really dislike the fact that another proposer can force me to include transactions, e.g. what if the transaction I am forced to include will have legal consequences. Imagine a proposer in the US having to include OFAC txs, they either have to go to jail or miss the block?
2. Currently, the only reason transactions are censored is due to legal reasons as far as I know. Let’s assume the US sanctions more smart contracts, wouldn’t this make builders in the US less competitive due to a reduced pool of transactions to choose from? If that assumption is true, then the problem would likely resolve itself as builders would have to relocate. I don’t see a economic reason for censoring transactions, it might even be the opposite as those transactions could pay higher fees due to delayed inclusion as not all builders process them.
3. How much value would ILs provide if we assume that the vast majority of transactions will be on L2 in the future?
4. I know this was quickly discussed in the CL meeting this week but it would be good to better understand why shouldOverrideBuilder is considered to be insufficient and something like IL is required, assuming there is a majority of honest / non-censoring proposers that care about the health of the network.

---

**mikeneuder** (2024-01-26):

for sure, but at some point, we need someone to push the txn in. the question becomes, who do we depend on for CR? builders or proposers?

---

**mikeneuder** (2024-01-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/themandalore/48/6725_2.png) themandalore:

> I think it is a win, but the big issue I have is that the reason validators weren’t/ aren’t censoring is that the legal culpability falls on the builders if they just “take the built block”. By adding in the ability to select the transactions, you could change the dynamic to where validators are now responsible for the transactions, thus making them more likely to censor (like the builders) and more of a regulatory target.

thanks for your response! i don’t think the MIN/MAX thing is quite the right way of thinking about it though. the distinction comes from the fact that with inclusion lists, there are now multiple “versions” of a censoring proposer. A censoring proposer could (1) not use the IL, but still accept blocks from non-censoring builders, or (2) not use the IL AND not accept blocks from non-censoring builders.

While I agree that there will certainly be a lot of proposers in (1), I don’t think the addition of ILs will make any proposer change the set of builders they connect to (hope that makes sense). If that is the case, then ILs *can only increase the CR of the protocol*. Because some validators will opt in to using them, while some will leave them empty and maintain their setup of today.

It is worth mentioning that the honest specification will be to build the IL, so any proposer who wants to change this will need to modify their client directly and act “dishonestly” from the PoV of the protocol.

---

**mikeneuder** (2024-01-26):

thanks for the reply!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nflaig/48/9390_2.png) nflaig:

> Should the protocol be opinionated about transactions, especially since there does not seem to be a objective criteria to proof (onchain) that a transaction is being censored. I really dislike the fact that another proposer can force me to include transactions, e.g. what if the transaction I am forced to include will have legal consequences. Imagine a proposer in the US having to include OFAC txs, they either have to go to jail or miss the block?

one really cool thing about 1559 is it does provide an objective truth about what txns are being censored. namely, if the txn is in the mempool, pays the base fee, has a non-zero tip, and there is gas remaining in the block, it is being censored. regarding your second point, yes! that is the entire point of ILs. if as a validator, i have no choice but to include a transaction, then i have deniability from the protocol perspective. if you choose to miss blocks because you dont want to include transactions, then that is just the price of censoring, which should be high!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nflaig/48/9390_2.png) nflaig:

> Currently, the only reason transactions are censored is due to legal reasons as far as I know. Let’s assume the US sanctions more smart contracts, wouldn’t this make builders in the US less competitive due to a reduced pool of transactions to choose from? If that assumption is true, then the problem would likely resolve itself as builders would have to relocate. I don’t see a economic reason for censoring transactions, it might even be the opposite as those transactions could pay higher fees due to delayed inclusion as not all builders process them.

one thing to get straight here. we don’t know how builders will respond to ILs. For example, the builders have deniability in that they have to include a set of transactions in order for their block to be valid, so “censoring builders” of today may well build blocks that conform to ILs. we just don’t know. as to your second point, yes! running a censoring builder should be a competitive disadvantage! this is a great feature for improving the CR of the protocol.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nflaig/48/9390_2.png) nflaig:

> How much value would ILs provide if we assume that the vast majority of transactions will be on L2 in the future?

potentially immense value considering L2 batch transactions could be censored in the future! the core protocol is the place to have CR, not the L2s IMO. i expect L2s to start censoring ofac transactions very soon. if the core protocol cannot provide CR properties, then no one can and i don’t think there is much value in the chain in that case.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nflaig/48/9390_2.png) nflaig:

> I know this was quickly discussed in the CL meeting this week but it would be good to better understand why shouldOverrideBuilder is considered to be insufficient and something like IL is required, assuming there is a majority of honest / non-censoring proposers that care about the health of the network.

fair! will write about this asap, thanks for bringing it up!

---

**themandalore** (2024-01-27):

Thanks for your response too!  Any reason why the IL needs to be from the proposer?  Why not give each of the a beacon commitees a txn in the IL and make it something the winning aggregator gets to choose? Especially with the MEV auction idea (or just in general) that proposers will become more sophisticated and centralized over time, this would mean that the inclusion list could remain sort of blue collar if that makes sense

---

**Tudmotu** (2024-02-03):

1. What incentive do validators have to submit an IL other than goodwill?
2. Was there any analysis done on potential game-theoretic attack vectors? Validators backrunning next block, forcing loss-making txs, etc?

---

**lettucer** (2024-03-14):

DO NOT include this EIP please. I explain why.

1. Do you know who likes guaranteeing inclusion in the next block? MEV transactors with on-chain logic. They do not know if some setting will be triggered now or in 5 blocks, so they fill every IL with their tx until it happens, without paying top dollar after the trigger transaction hits the mempool. With ILs you will now create a mev-boost-il market. Validators do not care about censorship and would gladly modify their client for the gains. Plus this market can not be trusted due to the IL design. So now big sets of validators which are “trusted” can participate in this market. Small validators can not and will have lower payoffs, leading to MORE validator centralization.
2. The complexity to the protocol introduced by this EIP is staggering. We already have a hard time knowing how proof of stake works. Having to parse regular blocks plus inclusion lists is going to be a headache for any Ethereum developer. How many P2P networks are we at now? Do we really need to introduce more in order to make Ethereum run? I see consensus issues waiting to happen.
3. What ever happened to proposer-builder separation? Now proposers are going to build. Assuming they will not censor or modify their client because it is “built into the protocol by default” is not right.

---

**bertmiller** (2024-03-22):

What work has been done already on out-of-protocol markets impacts the presence of a forward IL?

I imagine there are two immediate angles:

- Paying a proposer to include something in their IL, thus forcing it into the next block. How does the mechanism change things if a proposer is paid to include a very high gas transaction for the next block, as an example?
- Paying a proposer to not include something in their IL, thus giving builders the maximum degrees of freedom.

I’ve of course read “fun and games” with inclusion lists, curious if there is any other work I should be aware of.

---

**lettucer** (2024-04-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bertmiller/48/12107_2.png) bertmiller:

> Paying a proposer to include something in their IL, thus forcing it into the next block. How does the mechanism change things if a proposer is paid to include a very high gas transaction for the next block, as an example?

My opinion is that truly censored transactions will be priced out by these other “MEV” like transactions, since forced inclusion is so very valuable. I wish there would be more research on this topic.

Especially I foresee MEV parties bribing censoring validators to include their transactions in a forward inclusion list immediately before an honest validator every time, to create the guaranteed inclusion MEV market where honest validators ordinarily would not provide one.

---

**supernovahs** (2024-04-05):

Let the market decide which transaction to include or not. Imo forcing txs will add too much complexity .

Anyway no validator will take the risk of forcing to include a OFAC tx.

And for txs other than OFAC, market will care itself

---

**poojaranjan** (2024-04-29):

[PEEPanEIP-7547:Inclusion lists](https://youtu.be/oRjG0RMnK5U) with [@mikeneuder](/u/mikeneuder) [@terence](/u/terence) and Francesco

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/e/edc96e97871f04f1274bd0d71fa883f12cb18be1.jpeg)](https://www.youtube.com/watch?v=oRjG0RMnK5U)

---

**lettucer** (2024-05-29):

The more I think about this, the more I am convinced that inclusion lists would be a terrible addition to the Ethereum ecosystem. We should be careful not to force it in just because it was on the roadmap and just because work was put into the idea.

I strongly feel that inclusion lists would rarely see actual anticensorship use. If implemented, what is going to happen is that shared sequencing systems will turn these inclusion lists into preconfirmations and profit from that. terence briefly alluded to this in the video. Think about it: validators have no rational incentive to include censored transactions in their inclusion lists. Rational validators must sell this block space. Worse, validators who don’t want to participate in shared sequencing or MEV will have their blocks walked all over by the previous validator who takes the profit from them, encouraging validator centralization and increasing their sophistication requirements to remain competitive. Also, the problem of validators “sabotaging” the next one’s profits still hasn’t been addressed: [Spec'ing out Forward Inclusion-List w/ Dedicated Gas Limits - #3 by terence - Block proposer - Ethereum Research](https://ethresear.ch/t/specing-out-forward-inclusion-list-w-dedicated-gas-limits/17115/3). Ironically, inclusion lists become a censorship tool in this case.

There is too much additional complexity in this proposal (another gossip protocol??) for something that affects Ethereum users “basically not at all” according to franceso in the video (https://youtu.be/oRjG0RMnK5U?t=2778). Censored users can just increase their priority fee, and non-censoring builders can hold onto the censored transactions until one of their blocks gets included. EIP-1559 naturally makes blocks that include censored transactions eventually profitable over blocks that censor them.

Further, there are myriad ways for censorship to remain. If in this model, block builders have so much control over the network, then what’s to stop them from denying block-building services to validators who have a history of creating transaction inclusion lists that conflict with their censorship policy. Then validators would decide not to include censored transactions in their inclusion lists, defeating the whole purpose of them. This proposal makes it seem like block builders have this much control.

The “95% of blocks produced by a single builder” statistic might sound shocking, but there’s no protocol risk to that. I will reiterate my bid against inclusion lists - too much complexity, and another network protocol, for something with little effect, for which competitive transaction pricing and a little bit of waiting fix the issue already, today.

[@poojaranjan](/u/poojaranjan), as you asked at the end of the video, these are my comments.

---

**poojaranjan** (2024-05-30):

Thanks for following the talk.

As of date, the proposal isn’t Included in the Pectra upgrade. Inclusion in any future upgrade will be based on further research, analysis, and decisions based on client teams and community feedback.

We appreciate your sharing comments.

---

**zemse** (2024-10-28):

> This leads to the idea of “forward” inclusion lists, where the transactions specified by the slot N proposer are enforced in the slot N+1 block.

If the block’s base fee spike in `slot N+1` too much such that the tx added in the IL in `slot N` has an insufficient base fee, then what is going to happen? Will the TX be included regardless of gas fees?

