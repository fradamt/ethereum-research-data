---
source: ethresearch
topic_id: 22278
title: A Roadmap for Funding Ethereum’s Open Source Infrastructure
author: sejalrekhan97
date: "2025-05-07"
category: Economics
tags: []
url: https://ethresear.ch/t/a-roadmap-for-funding-ethereum-s-open-source-infrastructure/22278
views: 2132
likes: 50
posts_count: 10
---

# A Roadmap for Funding Ethereum’s Open Source Infrastructure

Authors: [@sejalrekhan97](/u/sejalrekhan97), [@devansh76](/u/devansh76)

Special thanks to Audrey Tang for her thoughtful feedback, Jason Chaskin, [@owocki](/u/owocki) and Julian Zawistowski for the review, Clement Lesaege for his provocative insights and David Dao for valuable discussions.

This proposal does not represent any particular entity, nor does it aim to promote any specific individual organization. It is a response to a prompt given by [@vbuterin](/u/vbuterin) recently: *“What can we do to push Ethereum’s public goods funding and governance ecosystem to the next level this year, ideally something that major L2s, DAOs, even NFT projects would be willing to deploy? Basically, “rally the troops” within Ethereum land and really push funding across Ethereum to a much higher standard by the end of 2025"*

Note: This is designed as a structured experiment. And like any good experiment, it aims to elicit feedback, iterate, and evolve based on what actually works.

## I. The Problem

The Ethereum Foundation currently acts as a stopgap for the ecosystem, funding the core open source repos that make Ethereum work. At current prices under $2000, the EF has a finite runway remaining. So it is imperative that we solve the public goods funding challenge within the Ethereum ecosystem by each L2/DAO/dapp funding the software that it relies on, else we risk falling into a self-reinforcing spiral where

a) People are scared Ethereum is gonna lack funding in the future.

b) They decrease their estimates of Ethereum’s success.

c) They decrease their valuation of ETH.

d) ETH price decreases.

e) EF has even less funding.

And then cycles back to a)

If we talk about the EF underfunding, it risks FUD and makes it even more underfunded.

If we don’t talk about it, nothing will be done to fix it. We can look at the case study of BTC core development, without any impartial, neutral foundation. This has created a conflict of interest into not scaling BTC itself; for example, Blockstream funds BTC core developers at risk of bias towards creating demand for their Liquid Network

And BTC development is at least two orders of magnitude less complex and expensive than Ethereum. Without the Foundation, Ethereum would have similar issues as BTC but far worse. If we don’t find a way to pay the consensus and execution clients, dev tooling repos, and other EF grantees, down the road, someone else will (or the project dies), and they may not have the same incentives.

Overall, Ethereum’s public goods ecosystem requires a scalable, legitimate, and sustainable funding system independent of the EF that:

- Respects Cultural Pluralism: Accommodates the various ways in which L2s and DAOs support the ecosystem, such as Arbitrum funding Prysm, ENS having its public goods track, Optimism support via retro funding, etc
- Ensures Legitimate Governance: Good processes for deciding what should be funded and for how much, including clear mapping of shared infrastructure and community consensus on its relative importance
- Secures Financial Stability: Taps reliable, long-term funding streams like staking or sequencer revenue, MEV, and other recurring revenue to ensure funding predictability
- Provides Funding Transparency: Offer a clear, unified view of who relies on which repos and how much they are funding it.

## II. The Solution (TLDR)

We propose a three-phase roadmap:

- Phase 1: Broad Listening
-Surface what Ethereum values, what needs funding, and what orgs consider critical shared infrastructure.
- Phase 2: L2Beat-Style Dashboard
-Visualize who’s funding what, identify gaps, and publicly track contributions across Ethereum.
- Phase 3: Ethereum Pledge to Fund Your Dependencies
-Get a commitment from apps, chains, or DAOs to create their own unweighted dependency graph, assign weights using mechanisms of their choice (deep funding, QF, futarchy, etc) and allocate 2% revenue to it

## III. Phased Rollout

### Phase 1: Broad Listening Pilot

We need a shared understanding of what Ethereum considers open source infrastructure worth sustaining, particularly who is using it and should contribute to its maintenance. This exercise will determine the eligibility set of what projects should be included in a funding round.

We begin with ‘[broad listening](https://www.youtube.com/watch?v=k6bZ2qayBQA&t=1462s),’ a concept introduced by Audrey Tang, using tools like [Polis](https://pol.is) or [Talk to the City](https://talktothecity.org/) to run structured deliberation processes across Ethereum’s key coordination layers, including preconfirmation calls, All Core Devs, L2 syncs, governance forums, and dApp collectives. Eg of talk to the city that we ran [here](https://talktothe.city/report/https%3A%2F%2Fstorage.googleapis.com%2Ftttc-light-dev%2Fef5687b7fb5df5010eff0f3697ba0a1710381a2eac70b2beb868d9ab09302fd2) & [here](https://talktothe.city/report/https%3A%2F%2Fstorage.googleapis.com%2Ftttc-light-dev%2Fa6b8855788bff90af3fb2e943c6f318600b2cc7a636a295ca511017620c8ea86)

Together, we’ll surface answers to core questions:

- What does the ecosystem value? E.g.: here
- What kinds of open source work are most worth supporting?
- What principles, outcomes, or metrics should guide how funds are allocated?
- What do different orgs already fund and what do they believe should be funded?
- Which organizations are relying on what open source repos that they need for their product to work?

Broad Listening will help us:

- Identify categories of infrastructure that need funding (e.g., ZK-EVMs, light clients, high-level languages, mechanism R&D)
- Understand how different communities define “shared” vs “local” infrastructure
- Highlight underfunded categories that Ethereum as a whole relies on
- Gather structured input that can be the training dataset for AI models and determine the eligibility set for various ecosystem funding rounds and dependency graphs

It sets the stage to rally the ecosystem around what actually matters so we can align, act, and evolve together. We see Broad Listening not as a one-off exercise, but as the foundation for a culture of continuous sensemaking helping Ethereum stay in tune with its evolving needs and values. This complements Gitcoin 3.0 and Octant’s vision of identifying and funding Ethereum’s biggest problems through repeated cycles of listening to create a more coordinated and adaptive ecosystem.

Results from Broad Listening will power phase 2, an L2Beat style dashboard providing a public view into which categories and priorities need support, what’s already being funded by whom and for how much, and where gaps remain

### Phase 2: An Ecosystem-Wide Open Source Funding Dashboard

Right now, there’s little visibility into what open-source infrastructure is being funded across Ethereum and by whom. For example, is Arbitrum spending more to maintain Ethereum or Optimism?

We propose building a transparent, real-time dashboard that tracks organizations (L2s, DAOs, dApps) and the funding they provide to repos they depend on

This dashboard would:

- Aggregate ecosystem-wide funding data (e.g., Arbitrum funding Gitcoin Grants or paying salaries to Prysm developers, EigenLayer contributing to Protocol Guild, etc)
- Decide on which open source repos and categories surfaced via Broad Listening are valuable to Ethereum’s long-term resilience, and contributions to it should be included in the funding leaderboard
- Track contributions across shared infra, mechanism R&D, and local dependency graphs
- Present a leaderboard-style view, inspired by L2Beat, that makes contributions to Ethereum public goods visible and comparable between L2s, dApps, and DAOs

In 2023, the[Practical Pluralism](https://practicalpluralism.github.io/) prototype attempted to visualize what people believed should be funded. Our goal now is to go from belief to action, mapping what is getting funded, what isn’t, who is stepping up, and who needs to be pulling more weight.

This will:

- Help the ecosystem recognize gaps and overlaps in support
- Create reputational incentives to contribute
- Provide a live pulse on what the ecosystem values in practice
- Provide a shared map of support and neglect, helping guide coordinated funding

### Phase 3: Ethereum Pre-Commitment

**3.1. Ethereum’s Ecosystem-Wide Funder**

With visibility from Phase 2 (dashboard) and clarity from Phase 1 (Broad Listening), we invite L2s, DAOs, and EVM apps to make their Ethereum alignment more legible by committing to a recurring, public commitment funding the open-source infrastructure they rely on.

Protocol Guild is an inspiration for solving Ethereum’s looming public goods crisis. We propose augmenting their pledge as follows;

- To Protocol Guild: We encourage ecosystems to contribute 1% of their token airdrop supporting them, aligning with PG’s stated need for volatile assets to fill the risk/reward gap for L1 maintainers.
- To Their Own Dependencies: We propose a separate, recurring contribution of 2% protocol revenue or fees toward their own key open source dependencies (e.g., libraries, ZK tooling, clients, etc).

This bifurcation allows ecosystems to support both critical protocol maintenance (via PG) and the broader open source commons, both of which would receive visibility on the funding dashboard

This pre-commitment (enforceable at the code level in later stages) enables any revenue-generating entity to give back to their dependencies and create a self-sustaining ecosystem independent of exogenous capital injections from the EF. The alternative is a looming crisis of underfunding the shared dependencies that the EVM universe depends on. Some promising ideas have been proposed over the years by [Vitalik](https://ethresear.ch/t/developer-incentivization-in-protocol-contract-author-fee-rebates/6179), [Karl](https://ethresear.ch/t/mev-auction-auctioning-transaction-ordering-rights-as-a-solution-to-miner-extractable-value/6788), and others.

Ethereum has spent over a decade proving that decentralized, permissionless infrastructure can change the world. But now, we must demonstrate that the [Ethereum](https://vitalik.eth.limo/general/2024/05/23/l2exec.html) community can not only build infrastructure but also fund, govern, and grow their own public goods that keep it alive.

The larger strategy we propose is a clarion cry to “fund your own dependencies”, with the specific tactics being a leaderboard showing who is doing so and any revenue generating entity on Ethereum being able to easily generate a dependency graph to channel revenue to their specific dependencies.

**3.2. Dependency Graphs**

While Protocol Guild and dev tooling libraries support infrastructure that benefits the entire Ethereum ecosystem, many dependencies are local to specific protocols and often underfunded despite being critical. For example, Curve finance uses Vyper more than Solidity so relatively more of their revenue should go to supporting Vyper compared to other dependencies. But they currently have no easy way to do so despite it being in their self-interest: a more secure Vyper is a more secure Curve finance.

More generally, we should reframe the current discourse of public goods funding as being a “donation” to tighter integration between revenue & cost centers

Twitter (X) is able to fund a cost center such as community notes, without any veto by the ad division profit center to create an overall better product for customers. They can do so because the C-suite exerts dominance over all centers, but we do not have any equivalent in networks where profit centers hold all the cards.

To stay competitive with corporate networks we need to fund our cost centers without

- Expecting them to become a revenue center
- Dominance over cost centers by the revenue center

To address this, ecosystems will be encouraged to deploy their own dependency graph that maps out all the core dependencies specific to their stack, some of which would include shared key Ethereum dependencies, but also other open source repos more generally used in their product. 2% of revenue earned should flow through the graph. These instances can be:

- Run independently or linked to a common interface, example prototype: deepfunding.app
- Open to anyone who wants to search, explore, and fund key pieces of infra as easily as using Google

After project eligibility is set by generating a graph of all dependencies important to the revenue generating dapp, DAO or L2, weights can be assigned using various mechanisms such as;

- Those with knowledge of how important each package is use various voting mechanisms such QF, conviction voting, pairwise, deepgov etc to get weights between repos
- Use metrics agreed upon by core team members, which then auto-assign weights across the graph
- Start a deep funding style contest where models compete with one another to predict the weights on the dependency graph, ranked by how well they align with judgments made on a subset of repos
- Getting a list of all contributors to the eligible repos and using Protocol Guild style time weighting to compensate them directly
- Other experimental methods that might prove themselves in the future, such as prediction market-based funding to repos

However, the weights are determined, the most important aspect by far is the tight eligibility requirements. That way, even if the weights are not fully accurate, the harm is mitigated since only cost centers which are actually contributing to your protocol or product’s success are given money.

Here are some rough estimates for varied revenue generating apps and what the 2% revenue ask would consist of;

- ENS earned $31 million in a 12 month period, of which $620,000 should be allocated between their dependencies
- BUIDL by Securitize (BlackRock distributor) distributed $25.4 million in dividends for the one year since launch, ~92% of it on Ethereum; roughly $467,360 should go to its dependencies
- Nouns DAO sells one NFT every day, with recent sales being around 2 ETH. Projecting this number across a year, around 14.6 ETH would go towards dependencies that Nouns uses
- Arbitrum Timeboost (MEV auctions) is projected to earn $2 million per year for the DAO; 2% to funding the dependencies of this product are around $40,000

## IV: We need to do for game theory what we did for cryptography.

There is an entire under-tapped community of game theorists, economists, public goods theorists who are deeply aligned with Ethereum values but avoid engaging with crypto due to the negative reputation of our industry. Many of these researchers:

- Don’t yet realize how open and curious the Ethereum community is to mechanism innovation
- Don’t see how Ethereum is uniquely positioned to fund and implement their ideas
- Don’t know the urgency with which Ethereum needs to solve its public goods problem

The [Iceland Research Retreat](https://www.researchretreat.org/ierr-2025/), which we are organizing under Juan Benet’s leadership, is one step toward addressing the above issues in person. We have a short window of time (around 4 years) before we hit a crisis. Even if runway goes up, we only kick the football down the road before we need to inevitably tackle this issue.

We’d love your feedback and support.

If you have ideas, questions, or suggestions, or if you know teams who might want to help implement this, contribute tooling, please leave a comment with your thoughts.

You can also DM us on X: @[Sejal](https://x.com/sejal_rekhan) and @[Devansh](https://x.com/TheDevanshMehta).

This is a starting point. Our next step is to share the metrics and KPIs we’ll use to measure the execution of each phase, so your feedback now will help shape what success looks like.

Let’s make this real, together.

## Replies

**thelastjosh** (2025-05-10):

Appreciate the ambition and thoughtfulness of this proposal. A few notes from someone deep in DAO infrastructure research:

1. We’re already building the kind of dashboard described here. We already maintain the largest data lake of grants-related data in Web3 as part of the DAOIP-5 grants data standard (I would link something here, but the forum settings won’t let me). Happy to collaborate or integrate—no need to reinvent the wheel.
2. More generally, L2Beat works not just because of its dashboard, but because of a standard—i.e. a credible, evolving decentralization framework that DAOs and L2s are motivated to meet. The dashboard is only as powerful as the standard it tracks.
3. Last thought. Frankly, I think the EF needs to stop chasing diminishing returns in infra and invest in new use-cases. I see the need for research across a wide portfolio, but the deep funding strategies you’re talking about fundamentally miss a lot of forward-looking research and innovation, which tends to fall under use-case development rather than infra. If all you’re looking at is past data in repos, all you’re going to fund is the past, not the future. You’re not funding growth. E.g. take DAOs. DAOs are the companies of Web3. But basic innovation with DAOs has been way underfunded despite the centrality of the DAO use-case to Ethereum’s long-term health. I wrote Open Problems in DAOs two years ago and feel like there has been almost 0 progress on the major questions. So what’s EF’s plan here? Speaking as a game theorist / institutional economist / social scientist… many of my colleagues (incl. both young and senior profs at prestigious universities) are already starting to leave / disengage because they’re losing faith in the tech, the narrative, and the commitment to funding. I say this as someone who is also getting more AI grants. If you want research in DAOs to still happen, you’re going to need more investment and a focused strategy that supports existing talent, e.g. on the level of a $20M FRO, or this space is going away in less than 4 years.

Side note: I’ve also been talking with the CEOs of all the major DAO tooling companies about a “GovBeat” modeled on L2Beat (credit Yitong for the name), and I think those companies might be interested in supporting this kind of dashboard / contribute tooling, especially if it feels like a collective project backed by EF.

Warmly,

Josh

---

**brucexu-eth** (2025-05-12):

**Thank you for this thought-provoking proposal!** I’m Bruce, co-initiator of LXDAO — a research-driven DAO focused on building a sustainable loop for supporting open-source and public goods in China over the past three years. I have some reflections and questions below:

---

![](https://ethresear.ch/user_avatar/ethresear.ch/sejalrekhan97/48/19871_2.png) sejalrekhan97:

> What can we do to push Ethereum’s public goods funding and governance ecosystem to the next level this year?

If we want to tackle the broad question, I believe focusing only on open-source dependencies and distribution mechanisms such as dependency graphs presents an incomplete picture.

Protocol and tooling dependencies are undoubtedly essential, but they are not the whole of what makes Ethereum run. This perspective misses the contributions of other critical roles, like: testers, developer educators, community organizers, onboarding efforts, and more — all of which are hard to capture in a dependency graph.

That said, I agree this is a valuable mechanism *within* the broader ecosystem of funding models, especially for open-source software. For the sake of staying on topic, I’ll limit this feedback to the scope of this proposal. I plan to publish a more comprehensive proposal for this broad question on LXDAO forum soon, based on our experiments over the past three years.

---

![](https://ethresear.ch/user_avatar/ethresear.ch/sejalrekhan97/48/19871_2.png) sejalrekhan97:

> Overall, Ethereum’s public goods ecosystem requires a scalable, legitimate, and sustainable funding system independent of the EF that:

However, the proposal focuses heavily on *distribution mechanisms* and governance, while barely touching on the more fundamental question: **Where does the money come from, and why would anyone willingly give it?**

You mention encouraging contributors (e.g. 1% to Protocol Guild, 2% to dependencies), but I worry this approach lacks long-term sustainability:

- There’s no closed incentive loop for funders. Many current projects benefit from open-source work without contributing back. Unless they see tangible, recurring value in funding, the motivation to sustain it is low — especially when managing such a system might require dedicated personnel.
- We might need to dig deeper into what different stakeholders want, and design mutually beneficial value loops. One example: I’ve heard from a project that donated a significant 1% token share to Protocol Guild and only received a couple of thank-you tweets in return — leading to diminished interest in future giving.

We need to shift from “funding as altruism” to “funding as rational strategy.” Unless we can make **“funding public goods = long-term ROI”** an obvious equation, adoption will remain shallow.

I’ve been exploring ideas like incentivizing contributors through reputation mechanisms that translate into business value, and extending open-source license to embed funding rules into the license layer — but that’s a longer discussion for another time.

---

![](https://ethresear.ch/user_avatar/ethresear.ch/sejalrekhan97/48/19871_2.png) sejalrekhan97:

> Phase 2: An Ecosystem-Wide Open Source Funding Dashboard

In LXDAO, we once explored a similar idea: a *Public Goods Directory*, combining multiple indicators to map out valuable public goods. We also published a comprehensive *Web3 Public Goods Report* collecting and categorizing many projects.

What we found: **data on public goods is highly unstructured**. Unless efforts are made to deeply standardize and contextualize the data, dashboards become misleading or unusable. But if we *do* invest in rigorous standardization, the labor costs are significant.

We had a similar experience working with [@thelastjosh](/u/thelastjosh) on DAO dataset curation — aligning definitions and metrics across projects proved to be a major challenge.

Compared to L2Beat — which aggregates relatively clean onchain metrics — deps funding graphs are harder to quantify meaningfully. Some challenges include:

1. Invisible runtime dependencies. A component might be technically listed as a dependency but only used in rare edge-case scenarios, such as exception handling. In such cases, I believe actual runtime invocations are a more accurate indicator of the component’s value to the project than static file references.
2. Non-code contributions are ignored. For instance, if a component’s community drives adoption for your project (e.g. Laravel helping Vue adoption), that impact won’t show up in a dependency graph.

---

As mentioned by [@thelastjosh](/u/thelastjosh):

> “If all you’re looking at is past data in repos, all you’re going to fund is the past, not the future.”

Totally agree. We need to sustain successful projects, *and* create pathways for emerging ones.

Take Viem as an example — it’s rapidly cheasing Ethers.js in developer adoption and DX quality. I saw many devs said will replace Ethers.js in the new version of app. Without Paradigm support, would it have taken off? Could our current models have detected and funded it in the early stage? I think we cannot for now, but it should.

I think we could also learn from the governance and funding mechanisms of traditional foundations like Linux or Apache — both have weathered decades of open-source evolution. If we can translate their best practices into Ethereum-native, transparent, and efficient mechanisms, it would be a huge leap forward. That’s one of our key directions at LXDAO.

---

### In summary:

- We need more discussion — and viable strategies — around funding sources, not just distribution mechanisms.

Moral persuasion (e.g. “it’s the right thing to do”) is fragile. Value-aligned incentives are essential for sustainability and scale.

**Dashboard efforts must carefully consider data quality, standardization, and usability.**
**A universal funding model should go beyond just code and dependencies.** It should include broader contributions and enable innovation, not just maintain the status quo. Deps Funding and Protocol Guild are good ways in RetroFunding style, we still need new ways for innovation, if we are solving the problem “Funding Ethereum …” rather than just “Retro funding Ethereum …”.

Thanks again for the inspiring work.

---

**bumblefudge** (2025-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/thelastjosh/48/19851_2.png) thelastjosh:

> L2Beat works not just because of its dashboard, but because of a standard—i.e. a credible, evolving decentralization framework that DAOs and L2s are motivated to meet. The dashboard is only as powerful as the standard it tracks.

I would go even further-- what Josh is calling a “standard” is just a “specification” unless it has a stable working group behind it.  I’ve been saying this for years[[1]](#footnote-54256-1)– without working groups, no RFCs would ever get “final” status at IETF, or be deprecatable/updatable. AllCoreDevs and RollCall are the only working groups with enough funding and authority to function as such.

On a more meta-level, I also want to +1 Josh’s point that DAOs have a big role to play in developing alternate value flows for OSS infra (just look at argot .org!). Anything that supports DAOs will be a big tailwind to AllWalletDevs and AllERCDevs functioning more like IETF working groups, IMHO.

1. see https:// learningproof .xyz/ lifecycle-of-a-blockchain-standard/ , which I don’t have privvies to link to directly here ↩︎

---

**ellierennie** (2025-05-13):

I am pleased to see this being discussed. For those who don’t know me, I am a Professor at RMIT University and a Research Director in Metagov. I have been doing ethnographic work on contribution systems, collaborating with Prof Jason Pott (Economics).

Some high level thoughts:

It’s valuable to distinguish between dependency graphs and guilds as distinct contribution system types, each serving complementary roles in the Ethereum ecosystem. Dependency graphs operate retrospectively, recognizing and rewarding contributions based on their subsequent impact. The incentives here are indirect - participants build in anticipation of future rewards/recognition. In contrast, guilds like Protocol Guild are explicitly mission-oriented, distributing resources proactively to support a defined membership actively working on a defined thing. Importantly, such missions need not be innovative or novel; routine maintenance is equally vital.

Ideally, these two contribution system forms - dependency graphs and guild-based structures - should evolve together and become interoperable. Guilds can produce structured knowledge graphs documenting their contributions, providing data that may be used in dependency graphs over time. Guilds might include mechanisms to sell options on future rewards to give them funding now/in advance, providing them with the means to do things like employment contracts and bridging the gap between long-term value creation and immediate compensation.

Ultimately, contribution systems are methods for generating value from commons-based processes, designed explicitly with longevity and resilience in mind. They must be capable of preserving long-term horizon value - in this case ensuring Ethereum remains a secure, active infrastructure far into the future (a futurality current economic systems deal with poorly). Additionally, they must prioritise the security and integrity of what is genuinely valuable and reward that above all else. In Ethereum’s context, this means protecting consensus mechanisms from external social signals or gameable information, aligning closely with principles articulated in Vitalik Buterin’s “don’t overload consensus” perspective.

In essence, the Ethereum ecosystem relies on contribution systems at every level. It’s contribution systems all the way down - or it could be ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**vpabundance** (2025-05-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/brucexu-eth/48/12202_2.png) brucexu-eth:

> Protocol and tooling dependencies are undoubtedly essential, but they are not the whole of what makes Ethereum run. This perspective misses the contributions of other critical roles, like: testers, developer educators, community organizers, onboarding efforts, and more — all of which are hard to capture in a dependency graph.

Agreed, but I think we need to take this one step at a time.

![](https://ethresear.ch/user_avatar/ethresear.ch/brucexu-eth/48/12202_2.png) brucexu-eth:

> However, the proposal focuses heavily on distribution mechanisms and governance, while barely touching on the more fundamental question: **Where does the money come from

Ethereum’s core infrastructure historically has relied too heavily on short-term grants and donations, creating instability especially during market downturns.

**DeFi exists…so why isn’t it funding Ethereum’s public goods?**

We are convinced that yield-generated funding works based upon our last 18 months…and so Octant v2 provides the rails allowing our entire ecosystem to source via DeFi and route that capital in an efficient and transparent way.

![](https://ethresear.ch/user_avatar/ethresear.ch/brucexu-eth/48/12202_2.png) brucexu-eth:

> and why would anyone willingly give it?

The lack of transparency and coordination around funding is causing more issues than some may realize. Currently, a large portion of funds for Ethereum dependencies come indirectly from ecosystems building on ethereum that explicitly pay client teams, tooling libraries, and explorers etc etc to ensure compatibility, uptime, among others. This cost structure reveals two critical realities:

**Explicit Costs**: Projects must pay significant amounts for critical services like client team support and infrastructure, whose services are essential to maintain compatibility and user trust

**Implicit Dependencies**: Many of these costs are hidden or not fully transparent, making it challenging to manage them sustainably or strategically.

IMO the willigness shouldn’t come from altruism, it should come from business decisions to coordinate and potentially save a lot of money.

---

**Powers** (2025-05-14):

Thank you [@sejalrekhan97](/u/sejalrekhan97) and [@devansh76](/u/devansh76) for a thoughtful proposal. As well to [@thelastjosh](/u/thelastjosh) and [@brucexu-ETH](/u/brucexu-eth) for perspectives on the current market given your experience.

Like [@brucexu-ETH](/u/brucexu-eth) rightly pointed out, without closed incentive loops and long-term ROI, it’s hard to expect sustainable engagement. Even if the “2% pledge” idea succeeds, how do we avoid it becoming a short-lived feel-good effort that depends on good vibes and grants?

Ethereum already has a model that does not rely on charity, good vibes, or grants: fees and staking. This model ensures validators are paid, the network remains secure, and value is distributed to maintain the system.

What we’re lacking is the economic equivalent for the application and infrastructure layer — a deterministic system that binds funding to requisite maintenance and development activity. By linking funding of infrastructure directly to network usage, we can make the network intrinsically sustainable in the near and long term.

The “2% pledge” outlined in this roadmap is a step in the right direction, but it ultimately depends on external social norms and enforcement. This reliance makes it vulnerable to non compliance. This vulnerability is similar to the [Open Source Pledge,](https://opensourcepledge.com/) which inadvertently frames open source software as a charitable contribution, rather than a foundational asset. Of course, highly profitable companies exploit and thrive on top of these open source products. These profitable businesses have an economic incentive to pass back barely enough value to sustain the underlying infra, but not enough to ensure long term growth, development, or sustainability.

Ideally, we would create a system where such reciprocation is an innate feature. For example, consider Staking. Staking returns value to users who support the underlying security of Ethereum. The economic structure of staking promotes the security of Eth through defined economic incentives. These incentives allow us to reasonably predict staking activity a week from now, but also, to reasonably predict participation a year into the future. By baking incentives into the desired behaviors, we ensure products directly receive value flows from the ecosystem. There’s no need to convince or beg users to fund validators — participants act in an economically rational manner consistent with the system architecture. We should aspire to create the same certainty, predictability, and economic incentives for the broader Ethereum infrastructure layer.

At [Powerhouse](https://www.powerhouse.inc/), we’ve been exploring these questions under the umbrella of what we call [Open-Source Capitalism](https://x.com/PowerhouseDAO/status/1898007728422871231) — the idea that open systems need not only transparency and access, but also enforceable economic alignment between contributors, users, and capital.

In my opinion, we need to figure out how we can *capture* value more than how we *distribute* it

---

**kladkogex** (2025-05-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/sejalrekhan97/48/19871_2.png) sejalrekhan97:

> Arbitrum funding Gitcoin Grants or paying salaries to Prysm developers, EigenLayer

Hey ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) I disagree with Arbitrum or other projects funding Ethereum—it creates a direct conflict of interest. Ethereum is a for-profit network; validators and stakers are making millions of dollars per day.

Ethereum should embrace capitalism, not communism. A portion of transaction fees and inflation should go to a few star developers who earn substantial rewards. With AI, you only need a handful of exceptionally talented people. Telegram, for example, has fewer than 30 engineers and serves a billion users.

Developer hiring could be managed by a board elected through stake-based voting.

---

**james-prysm** (2025-05-30):

![:wave:](https://ethresear.ch/images/emoji/facebook_messenger/wave.png?v=12) prysm engineer here, not sure if it’s appropriate for me to chime in here but I believe all client teams are funded by other projects/companies in ethereum. We’re part of offchain labs and offchain labs does get funded by arbitrum, but we get to focus on working on ethereum development and it really hasn’t been a conflict of interest. Other teams too, teku and besu funded by consensus, etc with teach team funded in this way. most client developers aren’t paid by the EF.  I also don’t understand the board elected developer hiring.

---

**Matlemad** (2025-08-13):

My name is Mat, researcher at ECF and co-founder of SpaghettETH.

I would like to contribute to this thread with something ECF has just released.

(Apologies for the hiccup before. I tried to edit my post by adding dapp screenshots but it ended up halting me for 24h)

Data on public goods can be unstructured, politically contested, or just incomplete. Without a shared, credible mechanism to validate and update this knowledge base, dashboards risk favouring bias.

We want truths about Web3 projects, but in practice what we have one-man-band tunes, and we have to measure community sentiment separately from the records.

So no truths, but versions of it, partially grounded in onchain data, partially in unverifiable claims.

**Pensieve** is a decentralized-wiki attempt to fill this gap. It is a protocol for decentralized knowledge bases, designed so that what we know about projects (transparency, governance, maintenance activity, dependencies) is maintained via bottom-up consensus rather than by a single curator, or a team of them.

The current alpha, Pensieve ECF, applies this mechanism to the Ethereum ecosystem. It uses two primitives:

- Contribution Points (CP): a reputation measure earned through accepted contributions
- ItemWeight: a CP threshold required to publish or update a fact

The more consensus an item has, the harder it is to change. This produces a living record that reflects collective agreement, with a public edit trail and planned onchain dispute resolution.

This matters for funding and dependency mapping:

- Transparency: anyone can verify how a project’s profile was built and who contributed to it
- Ranking: projects with consistent community traction and strong transparency records rise naturally in visibility
- Accountability: updates and disputes are tied to contributor histories, making manipulation attempts visible

A robust, auditable knowledge layer like this would strengthen dependency graph–driven funding architectures, ensuring that eligibility and funding flows are grounded in open, community-governed data.

While our alpha focus is Ethereum’s project ecosystem, the protocol is domain-agnostic and could be adapted to any other high-stakes knowledge domain: legal, governance, education.

Current **alpha** limitations and mitigation plans:

- Malicious or offensive entries (e.g., targeted defamation, spam): introduce public “red-letter” marking of contributor addresses that post verified-offensive content; expand community flagging tools
- Coordinated CP attacks: weight votes by domain-specific historical contributions; require higher quorums for key fields.
- Low initial participation: targeted onboarding of diverse curators, bug bounty programs, and integrations into funding dashboards to create incentives.
- Off-chain trust dependency: migrate key operations onchain, including CDR staking in ETH; progressively integrate with Sablier for onchain verification of claims and contributions.

