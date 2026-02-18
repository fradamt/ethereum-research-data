---
source: ethresearch
topic_id: 23474
title: "Three Fundamental Problems in Ethereum Public Goods Funding: A Research Agenda"
author: dwddao
date: "2025-11-19"
category: Economics
tags: [public-good]
url: https://ethresear.ch/t/three-fundamental-problems-in-ethereum-public-goods-funding-a-research-agenda/23474
views: 621
likes: 16
posts_count: 10
---

# Three Fundamental Problems in Ethereum Public Goods Funding: A Research Agenda

**Authors:** [@dwddao](/u/dwddao) [@sejalrekhan97](/u/sejalrekhan97) [@qgolem](/u/qgolem) and Julian Zawistowski

## Abstract

Ethereum’s public-goods funding ecosystem has distributed over $150m through mechanisms such as Gitcoin’s quadratic funding, Optimism’s RetroPGF, and Octant’s staking-based allocations. After six years of experimentation, several important problems remain unresolved. This post highlights three of them where we believe a joint research agenda is needed:

1. Deployment Problem: when and how should funds flow?
2. Allocation Problem: whose preferences are reflected, and how are they aggregated?
3. Impact Problem: how are outcomes measured and fed back into future decisions?

Each of these is fundamentally a **mechanism design** problem: we are choosing rules that map signals and behaviour into allocations under strategic behaviour and noisy information. Ethereum is an unusually good testbed for mechanism design, but actual adoption in live systems is still shallow. The aim here is to outline questions that could guide theory, mechanism design, and empirical work across funding programs, especially as we move toward allocating **protocol-level capital** at larger scale.

## I. The Deployment Problem: when and how should funds flow?

Early Ethereum public goods funding relied on discrete quarterly rounds, Gitcoin’s GR1 (2019) distributed $38,000 to 200 contributors, eventually scaling to $4.4 million in GR15. These mechanisms created predictable problems: donor and project fatigue from “grueling two-week sprints,” capital sitting idle between rounds, builder uncertainty, and concentrated operational overhead.

### What We’ve Learned

The ecosystem has evolved from discrete quarterly rounds toward several parallel innovations: **streaming mechanisms** that eliminate idle capital and provide continuous matching; **hybrid epoch models** like Protocol Guild’s time-weighted vesting (channeling $30M+ to 190+ contributors) that balance predictability with sustainability; and **mechanism plurality** acknowledging no single mechanism optimizes across all contexts.

### A Selection of Critical Open Problems

Key questions remain unresolved: Can streaming mechanisms achieve robust collusion resistance without prohibitive computational complexity or friction for honest users? What timing models optimize across capital efficiency, donor retention and attack economics? How can we create accountability for funding decisions, through allocation bonds or other mechanisms, without creating plutocratic dynamics? Additionally, as multiple programs (Gitcoin, Optimism, Octant, EF grants) operate in parallel, how should the ecosystem coordinate to build complementary rather than duplicative funding infrastructure?

## II. The Allocation Problem: Whose Preferences and How to Aggregate?

Results like Arrow’s impossibility theorem, Gibbard–Satterthwaite, and related social-choice impossibility results prove no voting system can simultaneously satisfy non-dictatorship, Pareto efficiency, independence of irrelevant alternatives, and transitivity. Every allocation mechanism must compromise on legitimacy, efficiency and fairness criteria, the question is which tradeoffs are acceptable for pseudonymous, global communities with misaligned incentives.

### What We’ve Learned

Six years of experimentation reveal fundamental tradeoffs with no clear winners: **quadratic funding** evolved from pure formulas to pairwise-bounded (20-30% dominance reduction) to cluster-matching approaches that embrace rather than prevent coordination; **MACI** offers theoretical collusion resistance through receipt-free encrypted voting but remains limited to mid-sized settings due to usability challenges; **Gitcoin Passport** pragmatically weaponizes identity verification costs ; **conviction voting** enables continuous preference signaling with natural manipulation resistance now deployed by 1Hive and Gitcoin GG24; and **Optimism’s two-house system** explicitly operationalizes the democracy-technocracy tension through separate Token House (coin-weighted protocol decisions) and Citizens’ House (one-person-one-vote RetroPGF with 20% treasury committed).

### A Selection of Critical Open Problems

The deeper challenge is defining and evaluating “good” allocation. **Fairness** requires distinguishing healthy coordination from collusion, should mechanisms penalize all group behavior or embrace it? **Efficiency** demands rewarding impact magnitude, yet aggregation rules that resist conflicts of interest (e.g. median-based) compress variance. Rules with higher variance (mean, quadratic, etc.) carry more information but are more fragile. Can we recover some expressiveness without opening obvious attack vectors? **Legitimacy** creates the most fundamental tension: pure preference aggregation might suffer from rational ignorance and information asymmetry, while expert evaluation concentrates power and lacks democratic mandate. Can we design mechanisms where these tradeoffs become less sharp, or does Arrow’s theorem suggest any allocation mechanism must decide which properties to relax? And how do we compare and evaluate allocation strategies with each other?

## III. The Impact Problem: Measuring Outcomes and Creating Feedback Loops

Optimism’s founding insight, “it’s easier to agree on what was useful than what will be useful”, reduces uncertainty but doesn’t eliminate measurement challenges. Four rounds of RetroPGF distributing 71M+ OP reveal that even retrospectively, quantifying magnitude, attributing causality, and aggregating across diverse project types remains fundamentally difficult.

### What We’ve Learned

Even retrospective measurement proves difficult: **RetroPGF** evolved from Round 1’s 24 badgeholders unable to differentiate impact magnitude to Round 3’s cognitive overload to Round 4’s metrics-based pivot that reduced load but introduced selection bias. Analysis confirms no perfect mechanism, median voting resists conflicts but produces low variance (top 1% received only 6x median), while mean/quadratic are more manipulable. Incentive bias persists even retrospectively (tobacco research funded by tobacco companies is 90x more likely to find no harm). **Hypercerts** solve accounting but not evaluation bottlenecks. The vision of “impact markets” depends on creating credible feedback loops: allocation bonds where early funders/mechanism designers stake capital on their choices and profit if retrospective evaluation validates high impact, or lose stakes if allocations prove ineffective, sending economic signals backward in time to reward good judgment and penalize poor decisions.

### A Selection of Critical Open Problems

Fundamental questions remain: How do we attribute causality and quantify magnitude for public goods with long time horizons and compounding network effects, especially when measuring counterfactuals in complex sociotechnical systems? What institutions prevent incentive bias when evaluators have stakes in outcomes, should badgeholder track records be weighted over time? How should mechanisms account for downside risk and negative externalities when retrospective funding cannot impose penalties, only rewards?

## IV. A Coordinated Research Agenda

Progress on the three problems require:

1. Continued theoretical innovation bridging mechanism design, cryptography, and social choice theory
2. Rigorous empirical evaluation of live experiments with transparent sharing of failures
3. Coordinated experimentation across funding programs to test complementary approaches

## V. How to Get Involved

We propose three concrete next steps for the Ethereum research community:

**1. Coordinate empirical research across funding programs**

Gitcoin, Optimism, Octant, and others are running parallel experiments. We need shared evaluation frameworks, common metrics, and coordinated timing to enable cross-mechanism comparison. Researchers should engage with program operators to design studies that answer specific theoretical questions.

**2. Build open-source infrastructure for mechanism experimentation**

Lower barriers to deploying new mechanisms through composable smart contracts, simulation tools, and evaluation dashboards. Modular designs such as Octant v2’s[TokenizedAllocationMechanism](https://github.com/golemfoundation/octant-v2-core/blob/2abd3b84de99d5f7837b2b7d6cad7ac50b6f46cb/src/mechanisms/TokenizedAllocationMechanism.sol), exposes a hook-based interface so different allocation rules can be deployed and tested quickly on the same underlying accounting system.

**3. Bridge academic research and practical implementation**

The game theory, economics, and mechanism design communities contain deep expertise not yet engaged with Ethereum. Events like the [Iceland Research Retreat](https://researchretreat.org) and [AI4PG](https://recerts.org/ai4pg2025) aim to connect researchers with builders. We need more such bridges, workshops at academic conferences, funding for applied research, clearer pathways from theory to deployment.

### Call for Feedback and Collaboration

This post represents an attempt to classify three important problems for public goods funding. **We need your input:**

- Are we framing the problems correctly?
- What critical research we’ve missed?
- What experiments are you running that could inform the broader ecosystem?
- What theoretical frameworks might unlock progress?

The public goods funding problem is fundamentally one of **knowledge aggregation under deep uncertainty with misaligned incentives**.

**Join the conversation:** Comment below with your thoughts, DM researchers working on these problems, or reach out if you’re building tools or running experiments. The ecosystem succeeds when we learn together.

---

*This research synthesis builds on work by teams at Gitcoin, Optimism, Octant, Protocol Labs, and numerous academic researchers. All errors and omissions are mine.*

## Replies

**bellgutu** (2025-12-01):

Thank you for opening this critical discussion. I agree that these three problems measuring impact, securing sustained funding, and developing accurate evaluation metrics are fundamental bottlenecks to growth.

Here is my feedback, informed by my experience building infrastructure for Real-World Assets (RWAs) and the Continuous Verifiable Reality (CVR) framework.

```
    1. Are we framing the problems correctly?
```

Yes, you are. The problems are correctly framed around the **measurement of non-speculative value** and the **allocation mechanism** to support it. The difficulty of translating deep ecosystem value (e.g., security, L2 scalability) into quantifiable, fundable metrics remains the central challenge.

```
    2. What critical research we’ve missed?
```

The critical missing link is a mechanism to **quantify and certify the real-world economic importance and future impact** of a project.

It is currently extremely difficult to establish a universal “value proposition” metric that is accepted both within the Ethereum ecosystem and by external actors (regulators, institutional finance, large industry).

We need research into **“Verified Externalities”**:

1. Quantification of Risk Reduction: Public goods funding should prioritize projects that mathematically reduce systemic risk or solve fundamental friction points for the global economy.
2. Ecosystem Metrics: We should fund based on quantifiable external impact (e.g., a formal reduction in Basel III collateral risk weights, as modeled in my CVR proposal), rather than solely internal metrics (e.g., number of active users, TVL).
3. Auditable Value: The research agenda should seek frameworks to prove the dollar-value impact of a public good, making the allocation defensible and understandable to external capital.

```
3. What experiments are you running that could inform the broader ecosystem?
```

I hope this is not self-promoting. My 20+ years of experience in financial and economics analysis and now building the CVR framework informs this discussion on quantifying external value.

I am building infrastructure that solves a **trillion-dollar friction problem** that traditional finance cannot: real-time asset verification. The CVR framework is an experiment that proves this thesis. It uses a reputation-first oracle and formal mathematics to:

- Mathematically Reduce Systemic Risk: Proving a 40-60% reduction in collateral risk weights for verified assets (see my post on Ethresear.ch).
- Show Utility of L2: Demonstrating that high-frequency IoT data (167 events/sec) can be securely anchored to an L2, unlocking new commercial applications.

This type of “new builder” project one that solves a fundamental, external problem and relies on the core value proposition of Ethereum’s technical upgrades is what Public Goods Funding should focus on. **Funding projects that prove Ethereum’s external utility is the ultimate public good.**

```
4. What theoretical frameworks might unlock progress?
```

I believe progress is locked within the intersection of **Mechanism Design** and **Impact Certification**.

The theoretical framework that could unlock progress is **Reputation-Weighted Quadratic Funding (RWQF) tied to Auditable Externalities**:

1. Mechanism Design (Reputation):  Project evaluation should adopt a robust, incentivized mechanism similar to decentralized protocols. Your funding allocation system could use a formal model similar to our Reputation Formula to weigh factors like team history, demonstrated utility, and continued engagement:
 R(i,t) = (alpha * Accuracy) + (beta * Uptime) + (gamma * Stake) - (delta * Disputes)
2. Impact Certification: Projects must be able to submit a mathematically or economically auditable proof of impact (the “externality”). This moves beyond subjective judgment, making the funding system more resilient and defensible to external capital.

By linking Public Goods Funding to formally verified, reputation-weighted inputs that certify real-world economic value, we can create a sustainable and powerful funding ecosystem.

---

**defitricks** (2025-12-03):

Given that long-term public-goods impact is so hard to measure and often only shows up years later, do you think Ethereum’s funding ecosystem should lean more on staged, milestone-based funding with community oversight or clawbacks - basically treating public-goods more like ‘long-horizon investments’ rather than one-off grants? Would that actually reduce uncertainty, or just add more governance overhead?

---

**dwddao** (2025-12-15):

Great question [@defitricks](/u/defitricks)! I believe this falls into the **deployment problem**, specifically *what’s the best way to deploy funding when impact measurement is delayed and ill-defined?*

Public goods funding in Ethereum is fundamentally a [wicked problem](https://en.wikipedia.org/wiki/Wicked_problem). Breaking it into subproblems (deployment, allocation, impact) helps, but each remains wicked in nature. I believe our field needs clearer ways to measure “progress” in PGF.

One approach I see for now as the impact problem is still unsolved: evaluate deployment mechanisms using **proxy metrics** rather than “impact”. Some metrics could be:

- Capital efficiency: Measure time-to-deploy (treasury → wallet) and idle capital ratio (% of funds dormant between rounds)
- Administrative burden: Measure hours spent on applications/reporting relative to funding received (grant science shows high burden creates selection bias against high-risk work)
- Builder retention: Measure churn rate (% who leave after funding ends) and “gap days” (periods builders have zero funding)

Octant is experimenting with [StreamVote](https://streamvote.octant.build/) to collect empirical data comparing continuous funding streams vs. one-time grants. We need more data-driven experiments, but most importantly, we need better evaluation frameworks to know that we as field/community are moving forward. I’m optimistic that we can solve this together.

---

**mbarbosa30** (2025-12-15):

This framing is really helpful. From a builder perspective, one thing that kinda feels missing across programs is a simple, shared way to log “what shipped” and “how to verify it” so we can actually learn across rounds and mechanisms.

I’ve been prototyping a small tool in this direction called **ShipLog**: basically packaging each deliverable as a single verifiable bundle (evidence + reproducibility notes + a metric target + before/after snapshots) and anchoring it under a CID.

Not trying to propose a new mechanism here ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=14) just curious what the “minimum viable” dataset should be. If we could standardize 3–5 fields for deployment, allocation, and impact that programs would adopt, what would you include?

---

**WillRuddick** (2025-12-19):

Thanks for this topic. Where I live, “public goods” are neighbors keeping neighbors whole .. water that runs, clinics that open, food that moves, dignity that lasts. So my first question is: **who is “the public” here?** In Ethereum, many cultures of “public” share one bus …. protocol engineers, validators, treasury stewards, builders, mutual-aid organizers. Like a BaFa’ BaFa’ situation, we sometimes collide because our languages differ. Let’s learn to talk *with* (not past) each other.

**Ethereum’s core gift, to me, is agreement infrastructure.** ‘Anyone’ (more and more people) can deploy contracts; anyone can enter verifiable, exit-friendly commitments. That is a public good. It’s why I treat **validator service** as sacred public work, and **ETH** as a token of **commitment** securing that work. When we start using ETH primarily as a pot for biz-dev and grants, we blur cultures: we treat security commitments like discretionary budgets. Communities don’t need our allocations as much as they need **interoperable rails** to build their *own* versions of “public” goods.

I want to give a gentle warning from the field: **top-down grants and cash drops often backfire** … dependency, gatekeeping, rumor, harm (*Dead Aid* is painful but real). Competition… lists make favorites; favorites have costs; anger finds a human target. I’ve had friends buried in that fallout. Please hear the love in this caution: fund **reciprocity**, not gatekeeping.

---

… I appreciate the “Verified Externalities” framing. +1 to funding what *reduces systemic risk*. I’d anchor this inside Ethereum’s gift: finance the **rails** that let communities prove reductions themselves (public memory, open attestations, dispute hooks) so impact is auditable *without* a priesthood.

**[@defitricks](/u/defitricks)** …. Yes to staged funding, but make it feel like **endowments for reciprocity**, not one-off grants. Stream funds against **verifiable agreements** (contracts that communities co-own), with clawbacks only on process failures (no delivery, no transparency), not on honest iteration.

**[@dwddao](/u/dwddao)** …Your proxy metrics are super useful. I’d add two “rail-first” ones:

- Agreement Density: # of live contracts (and users) per funded $ that communities rely on week-to-week. (This is how we should as well look at TVL Total Value Locked and # transactions).
- Exit Friendliness: % of programs where participants can leave with no penalty/shame because agreements (and recourse) are on-chain.

… I also love *ShipLog*. A minimal, shared bundle would keep us honest and light (you might already have most of this):

1. CID of the Deliverable (code/artifact) + Repro steps (≤10 lines).
2. Before/After snapshot of the one metric that matters (with the query link).
3. Counterfactual note (what would have happened otherwise) + known caveats.
4. Verifier & timestamp (who checked, when; human or automated).
5. Dependency links (contracts/PRs/issues this builds on).

---

### A structural way forward (reciprocity over allocation)

- Fund the rails, not the lists. Seed pooled commitments (cash, goods, services) governed by clear, public rules (value indices, caps, circuit breakers) and auditable ledgers with simple grievance paths.
- Prefer streams & endowments to drops. Let programs become self-replenishing pools that keep serving after the ribbon-cutting.
- Back standards, not favorites. Open interfaces for mutual-aid pools, community credit, and dispute resolution … so many cultures can thrive without a single gate.
- Guard the base layer. Treat validator service and ETH’s security role as non-negotiable public goods; don’t raid security to fund marketing.

This is why Grassroots Economics built **Sarafu.Network**: agents issue and redeem commitments (food, transport, clinic visits) under public limits and receipts; DEXs and routers make those promises interoperate. That’s **cosmo-localism** in practice: local governance, global agreements.

If we keep Ethereum’s center (**agreements as a public good**) I believe that the rest follows: less drama, more dignity, and more neighbors staying whole.

With care and gratitude,

**Will Ruddick**

Founder, Grassroots Economics Foundation

---

**Ashish-Web3** (2025-12-22):

This can be a valuable exploration, compliments to the team. And the research agenda is well framed.

I am suggesting three ideas

**1. Adding a 4****th** **pillar: The “Mandate or Role” of the program**

**Why this is important:** While the thought is somewhere inherent in the proposal, making this am independent pillar by can be valuable. I believe this should be the first pillar, before allocation deployment and impact. Agreeing on the program’s role upfront could act as a foundational guide for items in the subsequent buckets.

There isn’t one singular way to run such a program, and therefore having an agreed mandate provides valuable guardrails for the later steps, aligns people and also helps define a dashboard to make changes mid-way during a process (i.e. process design, impact assessment, north star people voting / co-donating)

A secondary output from this exploration, could also be a broader understanding of the roles that the different programs can play (i.e. Ethereum grants. Octant programs)

**How this can work can be approached:** The inputs can be from

- Past performance analysis can tell us what has worked
- Inputs from stakeholders and large donors
- Analysis of other public goods funding initiatives in tech and Web3 space

**2. A process suggestion: Taking feedback from grant recipients**

The note above speaks about checking out research available and looking at past performance. I believe it will help to add feedback from founders who received grants, Ethereum leaders and prior voters / donors

**3. A smaller idea: Stakeholder relationship management**

If you undertake #1, a corollary would be to identify key stakeholders and their expectations (i.e. for one person it could be about supporting progress of Web3, for another person it could be about Ethereum).

You’ve mentioned donor fatigue, and we have all witnessed it ourselves. Maybe knowing people’s motivators can help define an engagement strategy. And hopefully define a full closed loop that keeps them motivates donors to stay continually involved over a longer term (i.e. you participated, here is the updated, next round is more aligned to what you want to support)

**My intro:** While I am a Web3 OG, I am new here. So just sharing a brief intro. Not shilling, just so you know the context on how I have seen different sides of the funding and building journey

- Was a Corporate VC with a $100+ bn business house
- A Web3 co-founder. Built a community analytics tools that is backed by Techstars. I cannot paste company website link here, you can just google TogetherCrew
- Our venture has several received grants (Polygon, Web3 foundation, Arbitrum, etc)
- You can find me on X at a_gangrade

If I can help this exploration in any manner, it will be my pleasure

---

**Oba-One** (2026-01-22):

Thanks for sharing this insightful and concise research on public goods funding and generally agree with the sentiment and issues detailed.

![](https://ethresear.ch/user_avatar/ethresear.ch/dwddao/48/19872_2.png) dwddao:

> Ethereum’s public-goods funding ecosystem has distributed over $150m through mechanisms such as Gitcoin’s quadratic funding, Optimism’s RetroPGF, and Octant’s staking-based allocations

One question I have based on this quote to start the report is $150m was allocated to drive what outcomes?

I feel the issues are two things defining Ethereum Public Goods is very hard, what does that mean OSS, Regen, Education etc. and what are the outcomes not outputs these ecosystems are trying to manifest. When we say Ethereum public goods is it to build open tools just for the ecosystem and/or get Ethereum tooling/mechanisms adopted in traditional public goods contexts.

This google search is what Gemini stated as Ethereum Public Goods, high level seems accurate but not sure everyone would agree.

> Ethereum public goods refer to the foundational, open-source infrastructure, tools, and resources (like core software, libraries, documentation) that benefit the entire ecosystem, acting as a shared digital commons that’s non-rivalrous (one person’s use doesn’t stop others) and non-excludable (anyone can use them). They are crucial for innovation but face funding challenges, leading to innovative models like Quadratic Funding and retroactive rewards to support these essential, often invisible, public utilities that power decentralized applications (dApps) and the broader Web3 space.
>
>
> Key Characteristics
>
>
>
>
> Non-Rivalrous: Your use of Ethereum’s core infrastructure doesn’t prevent others from using it.
>
>
>
>
> Non-Excludable: No one can be blocked from accessing or building upon it.
>
>
>
>
> System-Enabling: They create the neutral groundwork (like the early internet) for decentralized economic activity.
>
>
>
>
> Shared Commons: They are tended to by the community, much like a shared resource.
>
>
>
>
> Examples of Ethereum Public Goods
>
>
>
>
> Core Software: Ethereum clients, developer tools, and open-source libraries.
>
>
>
>
> Standards & Protocols: Open standards, common languages, and foundational APIs.
>
>
>
>
> Civic Infrastructure: Tools for governance, data, and community coordination (e.g., ENS, Gitcoin).
>
>
>
>
> Education: Tutorials and documentation that onboard new users and developers.
>
>
>
>
> Funding Mechanisms
>
>
>
>
> Quadratic Funding (QF): A democratic way to fund public goods, matching small donations more effectively than large ones (e.g., through Gitcoin).
>
>
>
>
> Retroactive Public Goods Funding (RPGF): Rewarding projects after they’ve proven their value (e.g., Optimism’s approach).
>
>
>
>
> Protocol Revenue Sharing: Using fees generated by a network (like Public Goods Networks) to fund public goods.
>
>
>
>
> Why They Matter
>
>
> Public goods are vital because they foster a robust, decentralized ecosystem, ensuring that critical infrastructure remains open, accessible, and neutral, preventing reliance on centralized entities or private interests, as explained in this CoinDesk article and this Nasdaq article.

If we’re not starting with the problems being solved with this funding how will we find the right solutions?

---

**vpabundance** (2026-01-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/oba-one/48/21463_2.png) Oba-One:

> If we’re not starting with the problems being solved with this funding how will we find the right solutions?

This is a fair question, and it’s intentionally left unresolved in the agenda.

The $150m figure is meant to illustrate scale, not success. Across Gitcoin, RetroPGF, Octant, etc., funding has flowed into a wide mix of things, OSS, education, governance tooling, and other experiments, with their own explicit definition of *what outcomes the system is trying to produce*. That ambiguity is exactly what makes evaluation and coordination hard across these different programs.

The reason the agenda starts with deployment, allocation, and evaluation (and I would add one more that is “Onboarding”) is that outcome definitions tend to fragment very quickly across domains. Before we can agree on *what success looks like*, we need better mechanisms for deciding *who decides*, *with what information*, and *how feedback feeds back into future funding*. Without that, outcome debates tend to collapse into values or narratives rather than testable system behavior.

So the agenda isn’t arguing outcomes don’t matter, it’s arguing that we don’t yet have the machinery to converge on them coherently. The goal is to make those outcome conversations tractable, not to pre-decide them.

---

**Citrullin** (2026-01-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/vpabundance/48/19905_2.png) vpabundance:

> That ambiguity is exactly what makes evaluation and coordination hard across these different programs.

Not really. Especially not in the age of AI agents. Let’s get real here for a moment.

This space is infested with sociopaths of all sort. And you all have been exploited by them.

You either get serious and step up your game here. And stop to look at humans as these magical unicorns. Pun intended and another example of this nonsense casino holdl p*rn culture.

Or you see this whole thing collapsing, since “normal people” are not willing to play these games over the long run. Low-trust systems, as the Ethereum ecosystem is one, deliver very underwhelming results at best. Think nomad and family oriented societies. As uncomfortable as these realities are for some people, they are a fact of life.

![](https://ethresear.ch/user_avatar/ethresear.ch/vpabundance/48/19905_2.png) vpabundance:

> Before we can agree on what success looks like, we need better mechanisms for deciding who decides, with what information, and how feedback feeds back into future funding.

There are enough ideas floating around that try to account for human nature. Some of them are so obvious, it’s almost embarrassing having to spell it out. To answer who decides. The peers, the collective. Wasn’t that the whole point of DeFi once? Democratize finance, open it, distribute the power across more people, so it leads to less malicious exploitation. Not much left of that vision any more. Reputation systems have to play an important role in this future if you want to succeed. [Ethos](https://app.ethos.network/) certainly takes the lead here, as of this moment. As much as people dislike the idea of social scoring and enforcement models. They fear the dystopian vibes. Yet, absolute privacy tokens that enable money laundering, terror financing and island boys type of stuff are celebrated in this space. Big game of pretend and just a meaningless attention show.

**The embarrassing part that apparently has to be spelled out:**

You are surprised why all of this is failing? The underlying infrastructure is flawed at the core.

### To bring this into a simple tldr;

You are all looking at a human problem with technical tools and a math mindset.

Humans are emotional creatures though and driven by other factors.

Therefore, stop looking at humans like a computer you can program.

When all you got is a hammer, everything looks like a nail.

But you are looking at a screw type of situation here. Your tools are wrong.

**This is a sociological and psychological challenge, NOT A STEM ONE!**

