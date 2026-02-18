---
source: magicians
topic_id: 4621
title: "EIP-2982: Serenity Phase 0"
author: djrtwo
date: "2020-09-16"
category: EIPs > EIPs informational
tags: [core-eips, consensus-layer, eip-2982]
url: https://ethereum-magicians.org/t/eip-2982-serenity-phase-0/4621
views: 4425
likes: 14
posts_count: 14
---

# EIP-2982: Serenity Phase 0

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/2982)














####


      `master` ← `djrtwo:phase0`




          opened 02:51AM - 16 Sep 20 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/0/0230cb932b5871173c338dc2456b5e9485d1848a.png)
            djrtwo](https://github.com/djrtwo)



          [+194
            -0](https://github.com/ethereum/EIPs/pull/2982/files)







EIP for Phase 0 of Serenity (eth2) major upgrade of Ethereum's consensus mechani[…](https://github.com/ethereum/EIPs/pull/2982)sm from Pow to a sharded PoS.












Discussions for Serenity (eth2) Phase 0.

In addition to the EIP, see the [eth2 specs repo](https://github.com/ethereum/eth2.0-specs) for technical content and discussion.

## Replies

**adlerjohn** (2020-09-16):

I disagree with committing to using Serenity as a sharded PoS chain to transition Ethereum to at this nascent stage. It has yet to be proven theoretically (analysis of phase 0 alone is insufficent), and has certainly not been demonstrated to be viable in practice. There are a number of alternatives, some of which are on mainnet today, that would fulfil the same goal.

The EIP should also make it clear that Serenity is not inherently eth2 (i.e. the future of Ethereum), but rather a separate and Independent layer-1 that is planning to hard spoon the Ethereum state at a future time. And that the EIP suggests this new chain to be eth2, rather than starting from the assumption that Serenity is eth2.

---

**vbuterin** (2020-09-16):

> It has yet to be proven theoretically (analysis of phase 0 alone is insufficent)

So this (especially the parenthetical) is actually not true! The reason is that if fundamental flaws are discovered in sharding for whatever reason, it’s always possible to instead just do the eth1 → eth2 merge after phase 0. Phase 0 by itself is equally open to both of these future paths, so it’s not strictly speaking a hard commitment to anything but PoS itself.

And to be clear, the PoS part of eth2 is precisely the part that’s gone through quite heavy analysis and review. The Medalla testnet has been running for ~6 weeks, of which 4 weeks have been nonstop without issue (that was the original release condition for the eth1 frontier launch), and will run for considerably longer before phase 0 mainnet. Basically the main remaining uncertainty in the PoS is the economics, which by definition cannot be tested except on a live value-bearing network in any case…

> The EIP should also make it clear that Serenity is not inherently eth2

Not sure what this is trying to say. Of course a proposed change to ethereum is not part of ethereum until it’s actually fully implemented and rolled out; that’s part of the definition of “proposal”. The fact that this particular proposal involves changing the ethereum system to temporarily be made up of two chains with one linking to the other (with a goal of later changing to yet another hub-and-spoke architecture of 64 shard chains that all link into a beacon chain) is a technical detail, not really any fundamental philosophical difference.

---

**jpitts** (2020-09-16):

I would argue that EIP-2982 should include the entire specification of Serenity Phase 0, rather than summarizing and linking to external specifications. One key reason is that ACCEPT and FINAL status need to precisely indicate what is accepted, what is deployed.

Perhaps such a complete, single-page specification can be built from a tagged release of the [Eth2 specification repo](https://github.com/ethereum/eth2.0-specs), and subsequent, forking changes later submitted as new EIPs.

Serenity Phases 1 and 2 could work the same way when they are ready to be submitted as proposals.

More thoughts on this are further elaborated in this [PR comment](https://github.com/ethereum/EIPs/pull/2982#issuecomment-693709865).

---

**djrtwo** (2020-09-16):

Does a specific release/commit of the spec repo not “precisely indicate what is accepted, what is deployed”?

Releases can easily be downloaded as a single zip file and that included *or* if we must, we could write a script to compile all markdown files into a single markdown file. That said, I’m not sure if this provides any additional value to the process than a release reference would

---

**jpitts** (2020-09-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/djrtwo/48/859_2.png) djrtwo:

> Does a specific release/commit of the spec repo not “precisely indicate what is accepted, what is deployed”?

It does not as it points to an external resource; the URL may eventually break, repo deleted, or legal restrictions imposed for example. And I probably should have used the term concise rather than precise!

From [EIP-1](https://eips.ethereum.org/EIPS/eip-1): “The EIP should provide a concise technical specification of the feature and a rationale for the feature.”

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/djrtwo/48/859_2.png) djrtwo:

> Releases can easily be downloaded as a single zip file and that included or if we must, we could write a script to compile all markdown files into a single markdown file. That said, I’m not sure if this provides any additional value to the process than a release reference would

Perhaps a zip file is actually best, this would be the least work while fulfilling the requirement of fully specifying.

The additional value is providing all that is needed to develop an implementation from within the content of the EIP.

---

**matt** (2020-09-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> I would argue that EIP-2982 should include the entire specification of Serenity Phase 0, rather than summarizing and linking to external specifications.

I agree with this, however, I don’t know if this needs to be done for EIP-2982, as nothing on mainnet changes with it. I would think this consolidation would happen whenever PoW is retired and replaced with PoS.

---

**MicahZoltu** (2020-09-22):

A concern was brought up elsewhere that Phase 0 introduces ETH lockup in an ETH1 contract, and the depositors will then come to consensus on ETH2 chain state.  What is the purpose of real capital lockup on ETH1 during this period?  Why not just mint some new valueless toy token?  What do we gain by having real value here?  What happens to all of that locked ETH if something goes wrong during Phase 0?  If everything goes smoothly, will users gain any ETH or is it a zero sum game for the duration of Phase 0?

The specific concern that was brought up is that if real capital is not necessary for this process, then we are entering dangerous territory where one might interpret the capital lockup as the purchase of a security (per US securities laws) since essentially you are “investing” in the future success of the ETH2 development team and will potentially profit if it is successful and lose if it is not (depending on answers to above questions).

If real money is necessary for this process (can’t just be some random minted token) or the game is zero sum, then I suspect the risks of that concern are lower than if this *could* be some toy token and the game has potential future yields.

---

**matt** (2020-09-22):

[@MicahZoltu](/u/micahzoltu) at what point should real capital be used to secure the PoS chain? Goerli ether has been securing it for several months now. Eventually real assets need to be used to secure the chain.

It would be valuable to get some insight on the legal ramifications of locking up ether for eth2. I believe that this has been an important, on-going discussion over the last 1-2 years, but I’m not sure if any outcome has been shared.

---

**MicahZoltu** (2020-09-22):

Ideally, the point at which ETH is used to secure layer 2 is when layer 2 is providing real value to end users.  When layer 2 is essentially just being tested but not actually providing value (yet) is when you get into the “promise of future value” territory.

I think the useful question to ask is, “if all development stopped right now, would capital permanently locked in ETH2 be valuable/useful to people?” If the answer is yes, then I think that there is a strong argument that the returns are not dependent on the actions of core developers/ETH2 researchers.  In the case of Serenity Phase 0, if we launched it and then all development on ETH2 stopped I believe that locked ETH would be totally worthless (effectively burned).  Thus, anyone depositing into that contract is “investing in the success of the ETH2 development team”.

It is worth noting that I’m not a citizen/resident of a country who cares about these things so I don’t actually care about most of this stuff personally.  However, I know there *are* several people from the US and EU countries where these types of details matter, and so I’m arguing a bit on their behalf.  If everyone continues to go through with the current plan I will continue to contribute.  ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**vbuterin** (2020-09-23):

ETH2 is expected to start being useful to ETH1 in phase 1, when we have a sharded data space for rollups, and when we have both (i) BLS-12-381 support on eth1 and (ii) light client committees on eth2. That said, if there is demand for it, it’s entirely possible to add light client committees before phase 1, which would make ETH2 as a light client of ETH1 valuable quite a bit earlier! This is value that of course could be provided only if the ETH on the eth2 side is “real value”.

Additionally, there is the explicit goal of having a network running with real value on it to test the economics for some period of time before major applications start depending on it.

---

**gcolvin** (2020-09-23):

[@vbuterin](/u/vbuterin)  My question is whether and how the ETH submitted to the Deposit Contract can be withdrawn (or the submitter otherwise compensated) in case the Eth2 team does not - for any reason - make sufficient progress after that contract goes live.  I’m not asking about possible reasons for or probabilities of that happening.

---

**vbuterin** (2020-09-24):

If eth2 never goes live, then it would require another hard fork to make that eth accessible again.

---

**gcolvin** (2020-09-24):

Thanks [@vbuterin](/u/vbuterin).  That sounds like an invitation to be locked into a casino with uncertain egress.  It leaves the stakers at the mercy of the Eth2 team, whose failure could then create a DAO-like dilemma for the Eth1 team.

Further, as I discussed with [@djrtwo](/u/djrtwo) on the PR,

> I fear this is exactly the sort of thing that could make ETH look like a security to the SEC and similar authorities - we could pass the infamous Howey test that we have flunked so far.
>
>
> It is an investment of money.
> There is an expectation of profits from the investment.
> The investment of money is in a common enterprise
> Any profit comes from the efforts of a promoter or third party.

I strongly urge your team to find a way to “test the economics” without creating this risk and uncertainty.  If that is not possible I urge you to seek legal advice.

So far as this EIP goes, I think risks can be avoided by careful editing to keep the proposal technically informative without making commitments.

