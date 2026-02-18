---
source: magicians
topic_id: 26532
title: Delivering an impactful 2026
author: ralexstokes
date: "2025-11-12"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/delivering-an-impactful-2026/26532
views: 627
likes: 23
posts_count: 10
---

# Delivering an impactful 2026

*slow is smooth and smooth is fast*

(slow as in how we add things to scope)

Disclaimer: These are only my personal views, and I wanted to get something out in writing ahead of upcoming ACD calls where we will be making scoping decisions.

## it’s an important year

With Fusaka imminent, we will have landed two network upgrades this year. This is big and our progress should be celebrated. Many have said that Ethereum is not iterating fast enough to remain relevant in 2025 (and beyond) and the core developer community has shown them otherwise. If we want Ethereum to continue being relevant, we should double down on our momentum.

This means learning from this year’s lessons, particularly around fork scoping. Fusaka is in [some sense Pectra Part II](https://hackmd.io/@ralexstokes/pectra-in-two). Pectra grew quite large in scope and a natural solution was to just defer important features under discussion to the next fork.  Along the way, we have started building muscles as core researchers and developers around better pipelining of hard fork delivery. These skills are paramount to our ability to remain flexible as stewards of the core protocol as we navigate the complex, messy future that unlocks the promise of trustless compute for the entire world.

## regarding glamsterdam

We are soon going to be making scoping decisions for Glamsterdam, the network upgrade after Fusaka. Up for discussion are some CL EIPs, a large number of EL EIPs, and notably a cross-layer EIP with FOCIL. FOCIL in particular has wide community support and deeply aligns with Ethereum’s core values. Keeping in mind that we already have selected Glamsterdam headliners of ePBS and BALs, we should not add too much additional work in the form of further EIPs on either layer. Complexity scales superlinearly with each additional feature, and it is easy to say yes to something today and then be surprised when the bill comes due later.

Thus, I urge everyone involved in the governance process to keep in mind that we should not ignore lessons of the past and keep scope reasonably sized. This lets us ship more efficiently, so that we can be more responsive to community needs and also deliver more impact over time. Combining this view with our newly found skills of parallelization presents a compelling opportunity to the present scoping challenge: only add a very small number of non-headliner EIPs, and defer FOCIL to the Heka/Bogota network upgrade.

## regarding heka/bogota

I will let ACD deliberate over which other non-headliners ex-FOCIL it chooses to select for Glamsterdam, keeping in mind the goal is as tight a scope as possible. The deferral of FOCIL is a note-worthy choice, so I’ll expand on it here.

If we commit to including FOCIL in Heka/Bogota, we should first ask: what else are we implicitly excluding? One possible headliner that has been discussed is EIP-7782; the move to six second slots (SSS). If you have another headliner in mind, please chime in below, but it should suffice for now to assume SSS or something like it.

The immediate question from here: are we not repeating the same scoping mistakes over and over by doing FOCIL + SSS in one fork? It may seem so at first glance; however, this time is unironically different thanks to the skills mentioned above around working in more fluid, parallelizable ways. We can take the lessons learned from Pectra - Fusaka and apply them now to Glamsterdam - Heka/Bogota. Given that we have a good idea FOCIL and SSS would be the target for Heka/Bogota, we can start work *today* around derisking specs, implementation, and get a head start on testing. Our ability to process more per unit time as a decentralized institution is new, but we should not shy away from our enhanced capabilities.

Another fair question: if we are going to defer FOCIL to Heka/Bogota, can ACD credibly make this commitment? The governance body does not have a great track record around reasoning about multiple forks at once. Changes to Ethereum are complex, the world around it even more complex, and the stakes at hand demand the utmost care. For these reasons, scheduling multiple forks out from the present moment can be difficult. We can point to examples like Verkle or EOF where a lot of hard work by very talented people went into the given proposals and ultimately the ambient context changed around them such that they were no longer attractive at the time of selection.

By way of summary, Verkle was not selected due to technical risk (different state schemes became more attractive given other technological developments) and EOF was not selected due to social risk (the change was deemed too big by the community for something so central as Ethereum’s core virtual machine). FOCIL has none of these risks. There is currently no research on the horizon that would result in a compelling alternative on a technical basis over the next ~1 year. And FOCIL indeed has wide community support so I would be very surprised if sentiment changed that much over a similar time horizon. All in, it seems like ACD has a great chance at Heka/Bogota inclusion being a credible claim.

This is an exciting opportunity we should take advantage of. We can continue flexing our capacity for high impact while reinforcing Ethereum’s core values. The alternative pushes us back to an environment with high thrash, low efficiency, and less ability to clearly communicate what makes Ethereum so special. Here’s to an impactful 2026 ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

## Replies

**tvanepps** (2025-11-12):

well written, i echoed similar thoughts [here](https://x.com/trent_vanepps/status/1988253618626044304?s=20)

> it’s a bit confounding we might be repeating the same mistakes of pectra
>
>
> we shd prioritize scope mgmt / delivery timelines rather than including as several large features together (however nice they may be). this will increase testing and devnet complexity, based on what i’ve heard from the people who focus on this area eg. pari https://x.com/parithosh_j/status/1988231458830295517?s=20
>
>
> historically, we do not have a good track record of 1. estimating EIP implementation complexity or 2. accounting for unknowns
>
>
> let’s maintain discipline and ship glamsterdam mid next year!

---

**LukaszRozmej** (2025-11-12):

To be honest FOCIL on EL is managable in Glamsterdam. So I will leave that decision to CL devs as they are probably more bottlenecked than we are.

I would love to do FOCIL in 2026 if not in Glamsterdam than in H*.

If we are close to enshrining SSS, than I would advocate for EIP-7843 in Glamsterdam for smart contract devs to prepare for it (it is small EIP).

---

**tim-clancy.eth** (2025-11-12):

I’ve given my [thoughts on FOCIL](https://ethereum-magicians.org/t/soliciting-stakeholder-feedback-on-glamsterdam-headliners/24885/10) quite publicly in a number of [different places](https://x.com/_Enoch/status/1988254213176955075?s=20).

My point remains the same every time: FOCIL is by far the most important undelivered EIP and should have shipped earlier. Builders are inherently centralized, builder censorship is not a theoretical attack, Ethereum has been attacked by censoring builders. Given that code is law and we did not slash censoring builders, FOCIL is the mechanism we need to solve this problem.

FOCIL is special. It is also unironically different thanks to its importance. Nobody cares if the next fork is delayed by six months if they are censored from using Ethereum in the first place.

---

**abcoathup** (2025-11-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png) ralexstokes:

> if we are going to defer FOCIL to Heka/Bogota, can ACD credibly make this commitment?

FOCIL shouldn’t get pre-committed as a headliner Heka-Bogotá, we should avoid another Verkle.

Headliner discussions for Heka-Bogotá are likely to start in January (at the latest), assuming Glamsterdam scope is wrapped up in November or early December.  (Based on [Reconfiguring AllCoreDevs](https://ethereum-magicians.org/t/reconfiguring-allcoredevs/23370#p-56785-network-upgrade-timelines-8)).

FOCIL + SSS, or FOCIL alone as a headliner for Heka-Bogotá can be proposed, with potential for delivery in late 2026/early 2027.

Given the lead that FOCIL has in specs and development, it is likely to be the leading headliner contender.

---

**aelowsson** (2025-11-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png) ralexstokes:

> Changes to Ethereum are complex, the world around it even more complex, and the stakes at hand demand the utmost care. For these reasons, scheduling multiple forks out from the present moment can be difficult. We can point to examples like Verkle or EOF where a lot of hard work by very talented people went into the given proposals and ultimately the ambient context changed around them such that they were no longer attractive at the time of selection.
>
>
> By way of summary, Verkle was not selected due to technical risk … FOCIL has none of these risks. There is currently no research on the horizon that would result in a compelling alternative on a technical basis over the next ~1 year.

Note that the censorship resistance (CR) of FOCIL is significantly weaker under a multidimensional fee market, as discussed in [EIP-7999](https://eips.ethereum.org/EIPS/eip-7999) and [EIP-8046](https://eips.ethereum.org/EIPS/eip-8046). This was one of the primary reasons for designing [FOCILR](https://eips.ethereum.org/EIPS/eip-8046), which provides strong censorship resistance (immediate inclusion for IL-transactions willing to pay for it) and does not rely on the slack in the block for CR.

FOCILR can be implemented as an extension of FOCIL. This means that we can always include FOCIL first, and then include FOCILR in a later upgrade. In this respect, the existence of FOCILR makes shipping FOCIL an easier decision (and the existence of FOCIL makes FOCILR possible). However, if we only implement FOCIL and a multidimensional fee market, then FOCIL can be circumvented, and we do not actually have proper CR. I think a deeper discussion about the strategy on this would be suitable.

A reasonable approach is to go for a “full EIP-7999” (extending into the EVM) and EIP-8046 in the same future hard fork. Under such an approach, shipping FOCIL earlier is perfectly compatible (and even desirable), with the caveat that our [scaling pains](https://eips.ethereum.org/EIPS/eip-8075#potential-concerns-with-current-eip-8037) around [EIP-8037](https://eips.ethereum.org/EIPS/eip-8037) must be resolved in a “FOCIL attentive” manner.

---

**Ankita.eth** (2025-11-19):

I think this thread captures the right tension we’re all feeling: we want to move fast, but we can’t afford another Pectra-level sprawl. From my side, working mostly on protocol-adjacent tooling and infra, a few things stand out clearly:

### 1. Scope discipline has to be non-negotiable

Every additional EIP we squeeze into a fork doesn’t just add “one more feature.”

It multiplies:

- testing surface
- cross-client coordination
- devnet chaos
- unknowns we only discover too late

Glamsterdam already has ePBS + BALs, which are both heavy lifts. Trying to squeeze more headliners in feels like we’re trading velocity for short-term satisfaction.

### 2. FOCIL is important — but importance ≠ urgency

FOCIL absolutely matters.

But pretending that “important” means “must ship in the next fork” is how we set ourselves up for delays.

If including it threatens the timeline or stability of Glamsterdam, punting to Heka/Bogota is a rational move, not neglect. Especially now that we’re finally building healthier parallelization habits.

### 3. Planning two forks ahead should be normal, not exceptional

We keep acting like planning beyond a single fork is impossible.

It shouldn’t be.

If we know for a fact that the likely Heka/Bogota headliners are:

- FOCIL
- SSS (6-second slots)

…then starting derisking today is simply good engineering.

Not committing to the future is exactly how we ended up in “Verkle limbo.”

### 4. FOCILR gives us breathing room

Given the interaction with multidimensional fee markets, it’s worth emphasizing that:

- shipping FOCIL first doesn’t block FOCILR
- FOCILR strengthens the censorship-resistance story
- and implementing the two in sequence reduces risk, not increases it

That sequence alone is a strong argument for deferring FOCIL without diluting its importance.

### 5. Shipping cleanly matters more than shipping everything

The most productive forks in Ethereum’s history weren’t the ones that tried to solve everything — they were the ones that shipped with minimal drama.

If Glamsterdam can land mid-2025 cleanly, and we follow up with a focused Heka/Bogota in 2026 with FOCIL + SSS, that’s a healthier long-term rhythm than front-loading everything now.

---

**aelowsson** (2025-11-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ankita.eth/48/15393_2.png) Ankita.eth:

> That sequence alone is a strong argument for deferring FOCIL without diluting its importance.

You are perhaps referring here broadly to the four arguments in combination? So (1) scope, (2) importance, (3) planning, (4) FOCILR, leads you to the conclusion?

Because I would not count (4) by itself as an argument for deferring FOCIL (setting the other arguments aside).

My point was to look ahead a bit and try to analyze where we might go. I first noted that the CR of FOCIL can be diminished under a multidimensional fee market. This is good to know when we consider how to scale Ethereum. However, we can then extend FOCIL by shipping FOCILR to achieve even stronger CR than before. I note that these CR gadgets can be shipped after each other, meaning that much of what is implemented in FOCIL can be used also for FOCILR later.

If we like FOCILR, then this is another argument in favor of FOCIL, which provides the path there. If we do not like FOCILR, then we can consider whether a multidimensional fee market feels important to us (we might be satisfied with multidimensional metering), or if it can be achieved with better adherence to FOCIL in some other way. I like FOCILR and a multidimensional fee market (and FOCIL).

---

**Ankita.eth** (2025-11-20):

[@aelowsson](/u/aelowsson) Thanks for the clarification, but here’s where your framing still doesn’t hold up.

You’re treating FOCILR as something that only matters once fee-market work is underway. That’s too narrow. The real issue is the **risk surface**, and sequencing directly affects that.

### FOCIL without FOCILR creates a design trap

If we ship FOCIL first without aligning it to where fee markets are clearly heading (multi-dimensional, more expressive gas semantics), then we’re betting that FOCIL’s constraints will age cleanly. Nothing in current research suggests that.

FOCILR is not future polish; it’s what prevents FOCIL from locking the fee market into a structure we’ll outgrow.

### Glamsterdam should not absorb path-dependent changes blindly

You’re assuming Glamsterdam “isn’t affected” because FOCILR can come later. But fork sequencing isn’t just code delivery; it’s architectural commitment.

Once FOCIL is live, all future fee-market work will be forced to bend around its constraints. That’s the wrong direction. A censorship-resistance primitive shouldn’t dictate economics-layer flexibility.

### The dependency chain is straightforward

If the long-term fee-market design is multi-dimensional — and every serious proposal is pointing that way — then the logical order is:

1. define the economic constraints,
2. design FOCILR around them,
3. implement FOCIL as the minimal CR upgrade,
4. extend to FOCILR when ready.
Reversing that order isn’t sequencing — it’s guessing.

#### My position, clearly stated

FOCIL today is acceptable only if we acknowledge the likelihood of redesigning it later.

If we want to avoid reworking a core censorship primitive mid-cycle, then FOCILR’s assumptions need to be accounted for before Glamsterdam commits to anything on this path.

Saying the order doesn’t matter ignores the architectural lock-in that happens the moment FOCIL ships.

---

**aelowsson** (2025-11-21):

I brought up how FOCIL interacts with a multidimensional fee market in this thread because I think it is important to highlight right now, and I want to make researchers aware of it. There is however then good news since we can implement FOCILR on top of FOCIL for strong CR—also something researchers should be aware of. It’s best to now let the rest of the community absorb these points and continue the discussion from there.

