---
source: magicians
topic_id: 24088
title: Community Consensus, Fork Headliners & ACD Working Groups
author: timbeiko
date: "2025-05-08"
category: Magicians > Process Improvement
tags: [eip-process]
url: https://ethereum-magicians.org/t/community-consensus-fork-headliners-acd-working-groups/24088
views: 1467
likes: 38
posts_count: 12
---

# Community Consensus, Fork Headliners & ACD Working Groups

One of the most consequential decisions in Ethereum governance is selecting the flagship feature for network upgrades. Billions of dollars are at stake, literally. Moreover, every decision we make constrains our future design space and indecisiveness carries real costs because Ethereum doesn’t exist in isolation. **If we falter, by prioritizing the wrong things or failing to execute, we risk ceding ground to ecosystems with very different values.**

**Ensuring we pick the right “headliners” for hard forks is therefore the single most important responsibility AllCoreDevs has to optimize around.** We shouldn’t merely evaluate proposals by whether they are beneficial or not, but justify their value relative to other efforts to [scale](https://vitalik.eth.limo/general/2025/02/14/l1scaling.html), [harden](https://stark.mirror.xyz/A9csRsDaAJHJCCWa2Vv16bmxl0BgDqiLdupASxBT2r4), or [simplify](https://vitalik.eth.limo/general/2025/05/03/simplel1.html) Ethereum.

This post builds on my previous proposal, [Reconfiguring AllCoreDevs](https://ethereum-magicians.org/t/reconfiguring-allcoredevs/23370), by assessing Ethereum governance through this lens and suggesting practical improvements to our decision-making processes, specifically around aligning on the core focus and headline features for hard forks.

Note that this is my individual perspective: it should not be treated as the “EF opinion” or "AllCoreDevs consensus.” I fully expect, and welcome, differing opinions from across the Ethereum community!

## Rough (Community) Consensus

Ethereum’s governance philosophy is inspired by the Internet Engineering Task Force (IETF), notably the concept of “rough consensus”, whose subtleties are well articulated in [RFC 7282](https://www.rfc-editor.org/rfc/rfc7282.html). In short, rough consensus aims to pragmatically iterate towards solutions all stakeholders can accept, even if imperfect, while carefully considering all informed opinions. At its best, it produces higher quality solutions through a legitimate process, while rejecting Kings, Presidents and Shahs.

“Again, coming to consensus is not the goal in itself. Coming to consensus is what we do during our processes to arrive at the best solution. In particular, “declaring” consensus is not an end goal. Attempts to declare consensus at the end of a discussion just for the sake of being able to say that there is consensus often get us back into the voting mentality that we’re trying to avoid.” — RFC 7282

Ethereum’s approach has historically centered around core developers’ consensus, which implicitly assumes broader community alignment. However, core devs, while responsible for writing the code that secures the Ethereum network, do not have a monopoly on it. Ethereum’s [governance structure](https://www.youtube.com/live/HoclxIBR2EM?si=rAtbJtEv0NbbXptb) includes many more stakeholders, from node operators, to application developers, users, and more.

To remain legitimate, especially as the ecosystem matures, AllCoreDevs’ decisions must actively consider and align with the broader Ethereum community.If we fail to achieve and clearly communicate this alignment, we risk stakeholders moving from “voice” to “exit,” either through contentious upgrades or gradual migration to competing ecosystems.

Rough consensus amongst core devs, though necessary, is thus insufficient.. For major protocol changes, we need clear, documented consensus from affected stakeholders across Ethereum. If complete consensus isn’t achievable, we should at least transparently document dissenting opinions and explain clearly why we’ve accepted certain trade-offs.

Doing this will help ensure Ethereum continues to deliver meaningful improvements through a legitimate process.

---

## EOF & Fusaka

This context hopefully explains my rationale for unconventionally[removing EOF from Fusaka](https://github.com/ethereum/EIPs/pull/9703).

Different variants of EOF have been proposed, included, and subsequently removed from network upgrades over the years (see [Shanghai](https://github.com/ethereum/pm/blob/master/AllCoreDevs-EL-Meetings/Meeting%20152.md?plain=1#L336), [Dencun](https://github.com/ethereum/pm/blob/master/AllCoreDevs-EL-Meetings/Meeting%20160.md?plain=1#L323)), often reflecting shifting consensus about its urgency relative to other core features. Last year, EOF was scheduled for the Pectra upgrade until the fork was split to minimize scope, moving both PeerDAS and EOF into Fusaka.

While core developers broadly supported EOF, even then [some expressed strong opposition](https://mariusvanderwijden.github.io/blog/2024/07/12/EOF/). EOF champions diligently worked to address these objections, expanding technical specifications and modularizing proposals for clearer decision-making. At the same time, it became increasingly clear across the Ethereum community that shipping PeerDAS needed to be the priority for Fusaka.

As implementation continued, [complexity concerns](https://hackmd.io/@pcaversaccio/eof-when-complexity-outweighs-necessity) re-emerged from multiple stakeholders across the Ethereum stack. Core developers reaffirmed EOF’s inclusion in Fusaka at [ACDE 208](https://ethereum-magicians.org/t/all-core-devs-execution-acde-208-march-28-2025/23058), explicitly backing the most comprehensive version of EOF. However, [numerous ecosystem participants](https://ethereum-magicians.org/t/ethereum-is-turning-into-a-labyrinth-of-unnecessary-complexity-with-eof-lets-reconsider-eof/23136/24) continued voicing objections on grounds ranging from specific design choices to broader concerns about complexity, ecosystem fragmentation, and allocation of scarce engineering resources.

Shortly before [ACDE#210](https://ethereum-magicians.org/t/all-core-devs-execution-acde-210-april-24/23502), some core developers realized that their preferred [EOF Option](https://notes.ethereum.org/@ipsilon/eof_fusaka_options) (Option A) had unexpectedly significant negative developer experience consequences. While these had been flagged before, their magnitude hadn’t been fully appreciated. Client teams agreed to urgently review these implications and resolve them by the next [Testing/Interop #34](https://ethereum-magicians.org/t/interop-testing-34-april-28-2025/23822) call.

On that call, client teams and ecosystem participants generally agreed to move forward with a different, less comprehensive EOF version (Option D). However, towards the end of the call, it became apparent that there was still uncertainty about the implications of that version, with the Reth team becoming strongly opposed once they better understood the interactions with legacy contracts. This general confusion so late in the process and extreme shifts in opinions were the final data points that ultimately led me to remove EOF’s SFI designation for Fusaka.

I recognize a late removal negatively impacts the perceived legitimacy of our current governance process. However, strictly following [“the letter”](https://eips.ethereum.org/EIPS/eip-7723#scheduled-for-inclusion) of our current approach, by keeping EOF despite significant unresolved concerns, would have violated the spirit of the more inclusive governance we want to evolve towards.

Put another way, considering only the call where EOF was ultimately removed paints a very different picture than taking a more holistic view of the process, one where:

- Decisions on upgrade headliners are the single most critical output from AllCoreDevs;
- Ethereum’s immutability means changes are essentially permanent, requiring conservative caution against inclusion of potentially regrettable complexity;
- EOF repeatedly struggled to secure robust “rough consensus” within the broader community, even as core developers’ positions shifted over time;
- Community consensus that PeerDAS should be the #1 priority was clear and consistent;
- A more inclusive, structured governance process would likely have highlighted these issues earlier, preventing a last-minute reversal.

Our process ultimately failed in many ways. It failed core developers, who invested time and resources into developing EOF. It failed the broader community, who didn’t feel like they could impactfully communicate their concerns or have a say about the final prioritization decision. It also failed to adequately communicate when and how certain decisions would be taken, adding unnecessary turbulence to an already complex situation, impacting developers’ morale and momentum toward broader EVM improvements.

Going forward, it is critical we agree on a better way to set priorities for network upgrades, one that explicitly and consistently aligns our decision-making with Ethereum’s broader goals to scale, harden, and simplify the protocol. If EOF is indeed Ethereum’s highest priority, this evolved process should help it emerge with a clearer, stronger consensus. If it isn’t, improved prioritization will clarify what truly is, allowing core devs and the broader community to confidently invest their resources in the highest-leverage initiatives for Ethereum’s future.

## Selecting Hard Forks’ Focus & Headliner

Again, selecting the flagship feature for a network upgrade is Ethereum’s highest-stakes governance decision. Despite this, our current approach lacks explicit structure for evaluating and prioritizing these critical features. We therefore need a more rigorous, transparent, and community-aligned process.

Below, I propose an approach to make this headliner selection more thoughtful and focused, explicitly welcoming structured input from across the Ethereum community, not just core developers, while upholding AllCoreDevs’s commitment to keeping Ethereum secure.

### Defining the Fork Focus

At the outset of each upgrade cycle, AllCoreDevs should clearly define the strategic priority. or “Fork Focus”, of the upcoming fork. This provides a shared, community-aligned goal that guides the evaluation of candidate headliner features.

Defining this Fork Focus should explicitly invite structured input from across Ethereum’s ecosystem. While not necessarily formalized as a standalone artifact, this shared goal should offer strategic clarity and early alignment around priorities.

Illustrative examples of potential Fork Focuses include:

- Scalability & Lower Fees: Meaningfully increase throughput, lower transaction costs, and unlock new use cases.
- Developer & User Experience: Simplify protocol complexity, enhance smart contract security, and reduce development friction.
- Security & Resilience: Strengthen the network’s security posture, enhance attack resistance, and mitigate emerging threats without compromising decentralization or censorship resistance.

Community consensus around the Fork Focus should be actively sought, especially among stakeholders most impacted by the outcome. While AllCoreDevs ultimately owns implementation specifics, clearly defining the Fork Focus should reflect broad, credible input from the community, directly addressing Ethereum’s highest-priority needs.

### Converging towards Headliners

Once the Fork Focus is established, we can align on specific headline features. In practice, this will often be an iterative process, where initial proposals further clarify and refine the overall focus. Ultimately, AllCoreDevs must select only one or, at most, two (one per layer) flagship feature(s) per upgrade.

The existing PFI → CFI → SFI framework remains applicable here. Counterintuitively, our technical bar for CFI/SFI status on flagship features may be lower than for regular EIPs, but only if they strongly align with the chosen Fork Focus and enjoy robust community support. Some features (e.g., The Merge) are critical enough to justify an all-in effort despite imperfect initial specifications. Others, such as EOF, may be presented as a set of EIPs, or even non-Core EIPs, like for those related to the gas limit.

Once a feature is declined as a potential headliner, it cannot return as a regular EIP within the same fork cycle to prevent back-door reprioritization.

Headliner proposals (starting at PFI) should be structured explicitly via Ethereum Magicians threads that follow a clear template such as this:

### Headliner Proposal Template

- Summary (ELI5): Concise, plain-language explanation of the proposal, why it matters, and who benefits directly.
- Detailed Justification:

 What are the primary and secondary benefits, ideally supported by data or concrete rationale?
- Clearly articulate “Why now?”—Why should this feature take priority today?
- Justify this specific approach versus alternative solutions (lower risk, higher value).

**Stakeholder Impact:**

- Positive: Clearly identify beneficiaries and document explicit support.
- Negative: Identify those potentially negatively impacted, outline objections, and describe mitigations or explain accepted trade-offs.

**Technical Readiness:** Clearly assess technical maturity with links to specifications, tests, client implementations, etc.

**Security & Open Questions:** Explicitly document known security risks, open issues, or unclear aspects. Include threat models, preliminary audit plans, or next steps.

This structured selection process explicitly targets major protocol improvements. Smaller, incremental EIPs should continue through the existing lightweight governance process, maintaining agility and minimizing overhead.

---

## Community Input & Iterative Review

It can be challenging for stakeholders outside core developer teams to know when and how deeply to engage with Ethereum governance. To address this, I propose a two-stage community input process—a “barbell” strategy: explicit, structured community engagement at the beginning, paired with a community testnet for validation near the end of the implementation cycle.

Initially, we should actively solicit headliner proposals from across Ethereum’s ecosystem, clearly signaling when community input is most valuable. Using the Headliner Proposal Template outlined above, this structured early input ensures that core developers’ attention is focused on proposals clearly aligned with Ethereum’s strategic priorities. At the end of the implementation cycle, a dedicated ephemeral testnet provides the broader community with an explicit opportunity to practically validate the proposed changes, reserving late-stage objections primarily for critical implementation or security issues.

### Review and Decision Mechanics

The selection of hard fork headliners should explicitly integrate with the broader Ethereum upgrade planning cycle laid out in the [Reconfiguring AllCoreDevs](https://ethereum-magicians.org/t/reconfiguring-allcoredevs/23370) post. By anchoring headliner selection within the established PFI → CFI → SFI framework and clearly defining its relationship to the restructured AllCoreDevs calls (ACD{E|C} and ACDT), we can provide a clear, predictable governance process.

Here’s how this process would explicitly unfold each cycle:

- Open Call for Proposals: At the start of each upgrade cycle, as the previous fork approaches final implementation, AllCoreDevs clearly announces an open call for headliner proposals. Champions submit structured proposals asynchronously on Ethereum Magicians, explicitly aligning their proposal with the established Fork Focus.
- Focused Community Engagement: Core devs, infrastructure teams, Layer 2 projects, application developers, and other stakeholders provide structured feedback, explicitly highlighting their support or concerns. Clearly marking this review window ensures stakeholders know precisely when their input can be most impactful, incentivizing high-quality, well-articulated responses.
- Async & Sync Reviews: Proposals initially undergo asynchronous reviews, allowing champions to refine their ideas based on structured community input. These refined proposals are then presented and debated synchronously during dedicated ACD{E|C} roadmap planning calls, enabling direct clarification and focused debate.
- Iterative Refinement & Last Call: Following synchronous discussions, champions further iterate their proposals based on feedback. A formal “Last Call” asynchronous review provides a clear final opportunity for comprehensive community assessment.
- Final Selection & Rough Consensus: Ultimately, AllCoreDevs selects the headliner(s) in a dedicated synchronous call, clearly considering stakeholder input proportional to each group’s impactedness and alignment with Ethereum’s stated Fork Focus. For instance, DeFi-focused changes should explicitly weigh feedback from DeFi teams and users heavily.

### Community Testnet

Following headliner selection and initial implementation, a dedicated ephemeral testnet (similar to [Mekong](https://blog.ethereum.org/2024/11/07/introducing-mekong-testnet)) is launched to provide an implementation testing ground for the community. This should be the “Last Call” for the ecosystem to engage with a feature and propose spec changes. After this stage, the expectation is that only substantial security issues or severe unforeseen problems will delay or halt deployment.

Explicitly sequencing decision-making and clearly communicating expectations at each step helps avoid unnecessary turbulence and improves legitimacy. As emphasized in the Reconfiguring AllCoreDevs post, most of this iterative planning and testing will occur in parallel to the previous fork’s implementation, enabling Ethereum to incrementally deliver upgrades without lengthy delays.

## Formalizing ACD Working Groups

Ethereum’s biggest upgrades—like EIP-1559, The Merge, and EIP-4844—required years of dedicated work before shipping on mainnet. Most of these efforts emerged from recurring breakout rooms and focused community discussions, often without explicit alignment or clear checkpoints from AllCoreDevs. While this informal approach provides flexibility, it also risks significant resources being spent on ideas that stall or drift from Ethereum’s core priorities.

To address this, I propose formalizing the existing breakout structure into clearly defined Working Groups (WGs): teams explicitly chartered to coordinate longer-term protocol improvements, with regular touchpoints for feedback and alignment with AllCoreDevs.

### Working Group Proposals

Teams seeking to formalize existing breakout rooms or initiate new Working Groups would submit a lightweight proposal closely following the Headliner Proposal Template. Unlike headliner proposals, WG proposals explicitly target future network upgrades rather than immediate inclusion in the next hard fork.

These proposals provide an important mechanism for Working Groups to receive early strategic alignment from AllCoreDevs, without restricting independent experimentation or development outside formal endorsement.

### AllCoreDevs Endorsement

AllCoreDevs would review active Working Groups shortly after each headliner selection to ensure ongoing alignment. This endorsement serves as a “lightweight CFI,” clearly signaling that a WG aligns with Ethereum’s strategic priorities. A rare explicit rejection would indicate that an effort is misaligned or premature.

Practically, endorsed Working Groups would receive visibility on Ethereum’s protocol calendar and dedicated space within the GitHub /pm repository. Efforts not explicitly rejected or endorsed may continue informally, but without formal calendar representation or ACD visibility.

### Regular Check-ins

Endorsed Working Groups provide concise, periodic updates to AllCoreDevs, ideally timed just after each fork’s headliner selection. These check-ins confirm ongoing alignment, validate approaches, and offer opportunities for early course correction.

Check-ins should remain lightweight and strategic, not bureaucratic. Working Groups briefly share progress updates, highlight significant milestones, and explicitly raise critical questions or risks. ACD’s role is simply to reaffirm strategic alignment, provide targeted feedback, or suggest necessary adjustments.

### Clear Signaling & Community Confidence

By clearly formalizing Working Groups, providing explicit signals of strategic alignment, and maintaining regular lightweight check-ins, we reduce ambiguity around Ethereum’s long-term roadmap. Independent research and experimentation remain fully encouraged, but formally endorsed Working Groups can confidently allocate resources knowing they have community backing and explicit alignment with Ethereum’s priorities.

This balanced approach addresses previous shortcomings without sacrificing Ethereum’s flexible, community-driven culture.

## Where We Go From Here

Ethereum governance decisions carry uniquely high stakes. Billions of dollars, the network’s security, and our entire ecosystem’s alignment hinge on each upgrade we deploy. We need clear guardrails to manage these irreversible changes, but also enough flexibility to sustain Ethereum’s pragmatic, community-driven ethos.

The EOF experience clearly highlighted gaps in our current process: ambiguity around the upgrade’s core goal, insufficient structured feedback early on, and unclear checkpoints for major features. Without refining our approach, we risk repeating similar issues—even when everyone involved acts with good intentions.

To address this, I propose we explicitly strengthen our process around these core areas:

- Establish a clear Fork Focus: At the outset of each upgrade cycle, AllCoreDevs should define and communicate a clear strategic priority informed by community input, providing shared clarity around the upgrade’s core goal.
- Select at most one Headliner per layer: Using a structured template and the existing PFI → CFI → SFI approach, we ensure rigorous early reviews and explicitly prevent previously rejected proposals from returning as lower-stakes EIPs.
- Implement the “Barbell” approach to community review: Structured community input at the earliest stage—when changes are still flexible—paired with practical validation through community testnets as a final checkpoint, limiting late-stage objections to security and critical implementation issues.
- Formalize Working Groups: Provide formal, yet lightweight structure for existing breakout rooms and dedicated working groups, including periodic checkpoints with AllCoreDevs, to ensure long-term efforts remain aligned with Ethereum’s strategic priorities.
- Document the full governance approach: Clearly document the entire process in one canonical place with clearly defined feedback channels, removing ambiguity about how stakeholders can provide meaningful input.

This framework doesn’t guarantee perfect outcomes. However, it meaningfully reduces uncertainty, strengthens accountability, and preserves Ethereum’s ability to move forward confidently without sacrificing what makes Ethereum unique.

---

Thank you to everyone who gave feedback, both direct and indirect, on the contents of this post. It was a lot to distill, but your perspectives were extremely helpful ![:heart_on_fire:](https://ethereum-magicians.org/images/emoji/twitter/heart_on_fire.png?v=15)

## Replies

**storm** (2025-05-08):

thank you for the thoughtful post

everyone can agree that we need better processes to minimize the chances of an EOF-like incident from happening in the future. many of the new processes you propose seem worth trying

but in experimenting with new processes, let’s also remain cautious of falling into the opposite failure mode of overcorrection. each additional policy comes with cost and risks. things like

1. imposing too much bureaucracy can cripple efficiency+execution in non-obvious ways
2. imposing policies that are too rigid will eventually put the letter of the law in conflict with spirit of the law, similar to what you mention in your post
3. it’s important to maintain the ability to update or discard suboptimal processes. it’s hard to design processes upfront in one shot. probably lots of iteration will be required to get them right

I think everyone should be excited to experiment with Tim’s proposed processes and to help figure out ways that they could be improved. just want to make sure everyone stays mindful of the tradeoffs that we’ll need to optimize around

---

**timbeiko** (2025-05-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/storm/48/11361_2.png) storm:

> but in experimenting with new processes, let’s also remain cautious of falling into the opposite failure mode of overcorrection. each additional policy comes with cost and risks

Agreed, [@storm](/u/storm)!

The post is quite verbose (I want to be clear in explaining the context/rationale), but you can distill it to:

1. Open up ACD to broader participation than core devs & researchers, including explicit solicitation (vs. relying on whoever just shows up)
2. Aligning on a high level goal for hard forks in parallel to figuring out its core feature, and focusing on that before anything else, given the stakes of the decision
3. Being clear to the community about when they should pay attention and raise concerns + objections
4. Not defaulting to keeping breakout rooms around “forever”

We already do ~half of these things and the other half is mostly a coordination/comms effort. I agree that we don’t want to be overly rigid in our approach and exercise good judgement about implementing it. However, historically we’ve had very little formalization of the process, which makes it hard for those not “in the weeds” to meaningfully engage.

Please call us out if you feel things are too bureaucratic ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

---

**MicahZoltu** (2025-05-09):

A little bit of a tangent follows, but I do circle back to the primary topic of discussion (sort of) at the end.  TL;DR: I think the real problem is ethos misalignment among core devs.  The process we have in place works well when there is ethos alignment, it falls apart when there is not ethos alignment.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Billions of dollars are at stake

I think this hints at the root of the problem.  Many people consider “billions of dollars at stake” to be the meaningful metric, and this leads them to make choices that try to maximize short to medium term ETH price movement.  Are we trying to build a money printer, or are we trying to solve financial censorship, surveillance, and exclusionism?  How many core devs or other stakeholders would be happy to work on Ethereum if ETH price was guaranteed to decline with time as we do a better and better job of solving financial censorship/surveillance/exclusionism?  How many would be happy to work on Ethereum if the price was guaranteed to climb while it got worse at those other things?

While the current design of Ethereum has the price of ETH is part of a complex economic defense system against various attack vectors, it shouldn’t be the primary metric of success we use to make decisions like what to work on and when.

To put this another way: not all stakeholders are created equal.  A Silicon Valley Venture Capitalist is a stakeholder that I personally think we should care very little about, while a journalist, free speech advocate, or a woman in Iran are stakeholders that I personally think we should care a lot about.  If a change makes us lose all of those VCs but provides better service to more of the latter group then I think that is a good change, even if it would cause the price of ETH to decline significantly.

Regardless of whether one agrees with my personal preferences, I think as long as we fail to align on what it is we are trying to build, we will repeatedly butt heads on topics like whether EVM improvements are better/worse than DAS.

---

**kdenhartog** (2025-05-13):

I really like where this is going! One thing I’ve noticed with WGs in other organizations like IETF is that having deadlines and clear scope of works determined at the beginning is very helpful. These can help immensely to help WGs drive towards completing work in a semi efficient manner and prevent scope creep. Obviously WGs can be rechartered/scopes can be modified after work is completed but having a rough idea around this helps keep discussions focused.

As I’ve heard Justin Richer the author of OAuth 2 put it, “Standards aren’t done because people run out of time, nor do they run out of ideas they only run out of patience”.

---

**timbeiko** (2025-05-15):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> . Many people consider “billions of dollars at stake” to be the meaningful metric, and this leads them to make choices that try to maximize short to medium term ETH price movement. Are we trying to build a money printer, or are we trying to solve financial censorship, surveillance, and exclusionism?

My phrasing was a bit vague, but the “billions at stake” isn’t just the $ETH price: there are billions in economic activity and assets secured happening on Ethereum. If the network becomes a less attractive place for either of those things, then they likely end up happening in less ethos-aligned ecosystems.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> While the current design of Ethereum has the price of ETH is part of a complex economic defense system against various attack vectors, it shouldn’t be the primary metric of success we use to make decisions like what to work on and when.

Agreed, but my personal opinion is that it also shouldn’t be completely ignored, as it directly impacts the security of the network.

---

**Bruce_LXDAO.io** (2025-05-26):

Thank you for this thorough proposal! The structured approach to **headliner** prioritization and process design provides a clear path to resolving the current chaos. However, in my view, there’s still **one critical component missing**:

> When a previously “consensus-reached” decision later faces major divergence—e.g., EOF was initially included in Fusaka and then rolled back—
>
>
> Who has the authority to overturn the original decision?
> What are the criteria for reversal?
> Who bears the cost—both in human resources and on-chain risk—after a reversal?

You’ve explained the process of *Final Selection & Rough Consensus*, but the mechanism for “reopening closed cases” has not yet been clearly defined. This is precisely what the EOF case revealed — we lack a decision **exception handler**.

---

Ethereum’s upgrade governance references IETF RFC 7282’s “rough consensus” model, which is a solid starting point. However, we can’t be limited by it, because EIPs and RFCs differ fundamentally:

- EIPs must reach absolute agreement among major clients and be implemented and deployed at the same time. Otherwise, Ethereum could face hard fork issues. RFCs, on the other hand, are recommendations. Once finalized, IETF’s job is done, and adoption is optional—it doesn’t affect the overall function of the Internet.
- In Ethereum, “considering all informed opinions” currently centers on ACD’s technical perspectives, lacking broader ecosystem input.

Ethereum’s protocol layer is far from the Internet’s level of maturity, where it has become a de facto standard infrastructure. Ethereum still faces competition from more centralized, commercially driven alternatives. Without a more efficient mechanism for building consensus and coordinating efforts, Ethereum’s competitiveness may decline.

---

The EOF case also exposed a **lack of information transparency**. As you mentioned in your EOF recap, the relevant discussions were scattered across GitHub, personal blogs, HackMD notes, Ethereum Magicians, ACDE meeting notes, and EIPs—and some even happened on Twitter and Discord. This fragmentation makes it very difficult for other stakeholders to follow everything and participate effectively.

In addition, **time zone barriers** remain an issue. Since I live in the same time zone as [@kdenhartog](/u/kdenhartog), I can fully relate to his point:

[https://ethereum-magicians.org/t/reconfiguring-allcoredevs/23370/4?u=bruce_lxdao.io](https://ethereum-magicians.org/t/reconfiguring-allcoredevs/23370/4)

---

Comparing Ethereum’s current process with traditional tech project workflows helps us identify the main problems and optimization opportunities:

| Stage | Traditional Tech Projects | Ethereum |
| --- | --- | --- |
| Source of Needs | User feedback / market needs | Roadmap / Researchers / ACD / Ecosystem |
| Decision Makers | Product Managers, Leads | AllCoreDevs |
| Execution Team | Company R&D | Multiple client teams |
| Accountability | Assigned to individuals/teams | No strict enforcement |

From this, the main issues are:

1. Technical upgrades are decoupled from business needs. Misalignment of upgrade timelines and ecosystem realities causes friction and inefficiency.
2. Upgrade decisions heavily rely on core researchers, placing high pressure on ACD. Making informed decisions requires integrating market trends, long-term vision, technical feasibility, product iteration, and app compatibility—roles usually handled by dedicated PMs and project managers in traditional companies (with professional skills).
3. No accountability for plan changes. When things shift, no one takes responsibility, making it hard to trace wasted resources.

---

Given the above, I propose the following:

### 1. Build a Consensus Platform for Upgrades

There is already a related post: https://ethereum-magicians.org/t/for-an-acd-platform/24098. However, my view differs slightly: this platform should enable consensus-building across **multiple ecosystem participants**, not just within ACD.

Here’s why I think [@abcoathup](/u/abcoathup)’s idea of simply starting from the Magicians forum isn’t sufficient—we need a **new platform**:

1. We are already using forums, and they clearly have a high participation barrier for external stakeholders.
2. Discussions about EOF and past upgrades are scattered across various channels, leading to confusion. Even with new templates and processes, without structured workflows, things may become more chaotic.
3. The goal of coordination is not to minimize our own workload but to lower the barrier of entry for others. It’s worth the effort to optimize this.

The platform could resemble **L2Beat**, offering multi-dimensional information displays and feedback collection for each upgrade:

- Technical cost and security impact: Assessed by Core Devs and client teams—e.g., estimated dev time, risk to network stability, etc. This is the highest-priority metric. If an EIP introduces major cost or security concerns, it should be delayed—even if the community demands it—until a safer solution is found.
- Stakeholder feedback: Support / Oppose / Neutral options with rationale. Ecosystem participants (e.g., institutions, VCs, Dapps, wallets, L2s, staking providers, node operators, KOLs) can receive badges for wallet-based voting. Results help reflect community sentiment.
- Transparency scoring: e.g., Was there sufficient discussion? Did key stakeholders across different regions participate?
- Additional materials: Quality articles, controversy summaries, link aggregation (Twitter, Ethereum Magicians, Ethresearch, Discord, etc.)

The platform could extend https://eips.ethereum.org/ or https://github.com/ethereum/pm, or be a standalone interactive site—that part isn’t critical. What matters is that it improves transparency and provides a space for open participation. Votes and opinions on the platform wouldn’t be binding but would **inform ACD decisions** and provide a trusted reference in cases of dispute.

---

### 2. Define a Final or Important Dispute Resolution Process or Committee

It’s best to separate and clarify the roles and scope of ACD vs. final decision-making. When it comes to major features, relying solely on technical perspectives is insufficient. Broader strategic thinking and ecosystem-wide input are needed.

As mentioned before, Ethereum differs from IETF fundamentally. While I personally favor decentralization, given the current state of Ethereum’s R&D and the competitive pressure, I lean toward a **pragmatic** approach: set up a **reasonable and efficient decision process** grounded in diverse feedback, rather than clinging to decentralization ideals (but actually ACD centered) alone. Until Ethereum ossified, like [@zengjiajun](/u/zengjiajun) mentioned here https://x.com/zengjiajun_eth/status/1926067592621367402

This new process should be **triggered only when necessary** to avoid disrupting existing mechanisms.

A related community idea: https://x.com/ameensol/status/1917263883502240158

---

### 3. Increase Inclusivity in Feedback Loops

A simple example: ACD Calls are mostly scheduled in European-friendly time zones, creating barriers for APAC participants—even though the region includes over **half the global population**.

I observed fewer than five individuals who appear to be of East Asian in the photo of the Pectra Upgrade contributors shared here: https://x.com/TimBeiko/status/1920145795430727686. This highlights a diversity issue within the Ethereum ecosystem, if we truly aim for Ethereum to be a world computer, we might need to solve it.

Last year, [@xinbenlv](/u/xinbenlv) organized AllERCDevs meetings that included **EMEA-friendly** and **APAC-friendly** sessions, which was a good attempt at global inclusion: https://github.com/ercref/AllERCDevs/issues

I don’t claim this is the best solution, but this direction is worth pursuing, as also mentioned here: [https://ethereum-magicians.org/t/reconfiguring-allcoredevs/23370/4?u=bruce_lxdao.io](https://ethereum-magicians.org/t/reconfiguring-allcoredevs/23370/4)

---

### 4. Try Layered Upgrades and Iterative Deployment

In my previous experience at major Web2 companies, fast iteration was critical to product success. With good automated testing in place, weekly releases were the norm—faster is better, and small steps reduce risk.

For non-core-protocol upgrades (i.e., those not requiring forks), we could design a **fast-track implementation flow**, avoiding the current 1-2 yearly fork constraint. Due to Ethereum’s immutability, this would need custom testing and deployment processes.

---

**jhfnetboy** (2025-05-27):

Cool, let’s do it!

we need some meetup from tech to real world questions to extend the Ethereum utility in human digital future.

---

**gcolvin** (2025-06-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bruce_lxdao.io/48/6420_2.png) Bruce_LXDAO.io:

> You’ve explained the process of Final Selection & Rough Consensus, but the mechanism for “reopening closed cases” has not yet been clearly defined. This is precisely what the EOF case revealed — we lack a decision exception handler.

The current mechanism is that the removed proposal reenters the process as if it were a new proposal.  [@sorpaas](/u/sorpaas) has re-proposed EOF, which I support in any of its variations, but so far as I know its original authors have mostly moved on, the Foundation has dropped its support, and it’s not clear to me that the proposal can be rescued without them.  I’d be happy to learn otherwise.

For years now the precedent has been set and reinforced – removing an EIP so late in the process risks it never being included at all.  We need a way to delay upgrades while we resolve late-arriving objections, or failing that, to create a high-priority, rapid upgrade for that specific purpose.  Asking authors and their financial supporters (if any) to commit to the expensive, uncertain work of an entire upgrade cycle is simply not a fair or workable approach.  Not fair to the authors, their supporters, or to members of the community who were counting on the proposal to further their own work.

---

**sorpaas** (2025-06-14):

In my opinion, a slow and steady process is itself not a problem. To put EOF as an example, I personally think it must have EIP-9384 (or a variant of that) to make it useful for the later RISC-V roadmap (or another faster instruction set like EVM64). Had we deployed EOF in Fusaka, this will never have chance to be discussed and if we ever want to do something similar, the only option is to add another “EOFv2”, which is messy.

We must always consider the fact that anything, once deployed in production, becomes immutable and it’ll be really hard to change afterwards. As a result, especially for big changes, a thorough discussion is a must. Yes, the authors and their financial supporters may get annoyed because things are always delayed, but I would say this is probably unavoidable. The alternative is that we deploy rushed specifications on-chain and the community constantly arguing about “had we done something differently”.

---

However, I would say an important thing we can do is to make sure that the technical proposers of a headliner/EIP can always focus on the technical part of the specification. Right now this is not the case, the proposer basically has to do all the other work as well – coordinate with teams, call for external reviews, address non-technical questions, etc. This is not good because it’s usually a single person (or a small group of people), and the result is that **the proposer gets really emotionally engaged**. Then you have the problem like with the EOF – the proposal still has its full technical merits, but just because the original proposers get so exhausted, no one want to champion it any more. This is currently the real problem of the delay. I pretty much feel the same thing when originally I was championing account versioning until I couldn’t handle the pressure and dropped, and it took me a long time to learn the importance of not being “emotionally engaged”.

A thing we can try is to separate the role of “core devs” and “project managers”. We can call for additional “champions” from the ecosystem once a headliner/EIP is opened, who would then handle the coordination work, and the original core dev champion can focus on the technical details. We probably also want to change a bit of the process when a headliner gets removed and re-enters a subsequent fork. **This must not be considered an exception but it should be the norm.** This way we ensure that no proposer is under huge emotional pressure to get their proposals approved – we can always take time to address the concerns and go to the next hard fork.

---

**gcolvin** (2025-06-15):

I agree with you almost completely.  But I also believe that failing to release a feature is a failure to be avoided, and rectified with high priority.  Being decentralized doesn’t mean we can’t be professional.  In this case I still would prefer that you had the high-priority support to be working *right now* with the original team to *deliver to the community what we promised*.

---

**gcolvin** (2025-06-15):

Another aspect of “billions of dollars are at stake” is that it’s our technical responsibility not to lose them – whether the ETH belongs to a whale or a refugee is irrelevant, the network must not falter.

And yes, in the aftermath of the US defeat in Afghanistan crypto was king in the markets.  They still had cell service, but government fiat had no value.

So indeed, not all stakeholders are created equal.  I suspect the best way to serve them all is to “Maintain credible neutrality.”

