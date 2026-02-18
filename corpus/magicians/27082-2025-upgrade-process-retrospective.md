---
source: magicians
topic_id: 27082
title: 2025 upgrade process retrospective
author: nixo
date: "2025-12-11"
category: Protocol Calls & happenings > Process Improvement
tags: [glamsterdam, upgrade-retro, hekota, fusaka]
url: https://ethereum-magicians.org/t/2025-upgrade-process-retrospective/27082
views: 293
likes: 14
posts_count: 4
---

# 2025 upgrade process retrospective

As we did for the Pectra fork, we should reflect on how the process proposed earlier this year has served Ethereum governance so far.

For a general reminder about the process that dictated the Glamsterdam upgrade, a [Pectra retrospective](https://ethereum-magicians.org/t/pectra-retrospective/22637) & a [proposal to reconfigure ACD](https://ethereum-magicians.org/t/reconfiguring-allcoredevs/23370) were published, followed by a [headliner process proposal](https://ethereum-magicians.org/t/community-consensus-fork-headliners-acd-working-groups/24088) and [a timeline for the Glamsterdam](https://ethereum-magicians.org/t/eip-7773-glamsterdam-network-upgrade-meta-thread/21195) ‘headliner process’.

This helped ACD choose Glamsterdam’s major features, one for the consensus layer (ePBS) and one for the execution layer (BALs). Minor features (“non-headling EIPs”) were then proposed with a deadline to submit. We are currently in the process of selecting Glamsterdam’s minor features from the [total list of Proposed EIPs](https://forkcast.org/upgrade/glamsterdam/#proposed-for-inclusion).

Fusaka was a unique fork in that it split out of Pectra’s original scope. This scope being unmanageably broad was the instigator for a more formalized process with a goal to efficiently deliver forks with tightly defined scopes. Because this essentially predefined what was included in Fusaka, the process improvement proposal was applied to Glamsterdam as its pilot.

While structure and formal process has the potential to make things more efficient, it’s an inherently difficult problem to solve in decentralized governance because the structure has to be based in consensus rather than top-down *rules to be followed*. As such, formal process should be reflective of *what works* and *what governance participants will follow because they’re good processes that make consensus less painful* as nothing can reasonably be ‘enforced’.

To address what did and did not work, I’ll lay out a high level overview of what was proposed and whether or not we followed these goals. I think it would be useful to reflect on:

1. If the goal was effectively followed, was it useful?
2. If not followed, should we have pushed harder to apply these goals or were they just improbable?
3. After having gone through this process, would we add new goals, reconfigure the entire proposal, …?

As [noted](https://ethereum-magicians.org/t/community-consensus-fork-headliners-acd-working-groups/24088/2) by [@storm](/u/storm):

> it’s important to maintain the ability to update or discard suboptimal processes. it’s hard to design processes upfront in one shot. probably lots of iteration will be required to get them right

| Goal | Followed? |
| --- | --- |
| Defining the fork focus prior to headliner selection | ?* |
| Open call for proposals | Yes |
| Select at most one headliner per layer | Yes** |
| PFI → CFI → SFI for all features | Yes |
| Headliner proposals (starting at PFI) structured explicitly in clear template | Yes |
| Structured community engagement at the beginning | Yes |
| Community testnet for validation near the end of the implementation cycle | No(t yet?) |
| Formalize working groups | Yes(?)*** |
| Document the full governance approach | Yes(?) |

*I’m unsure if anyone feels that we actually attempted this for Glamsterdam. It is my perspective that this turns out to be an unrealistic goal because the reality is that the community often has their eyes set on specific proposals long before we can decide on directions, so ‘fork focuses’ will likely be retrofitted to fit the desired EIPs.

**Though ePBS+BALs fits this, we actually did CFI FOCIL and then end up DFI’ing for fork scope, so we *attempted* to not follow this guideline though we ended up needing it

***Breakout rooms that revolve around features with dedicated champions seem to continue to be successful, while more generalized breakout rooms like RollCall didn’t seem to have the momentum needed to continue

for some added visualization:

[![GOV2](https://ethereum-magicians.org/uploads/default/optimized/3X/0/4/04cf0ddeb887351c6580e7bd417d1bf8ebe4ecba_2_690x284.png)GOV22337×965 181 KB](https://ethereum-magicians.org/uploads/default/04cf0ddeb887351c6580e7bd417d1bf8ebe4ecba)

### all links:

1. Pectra retrospective
2. Reconfiguring ACD
3. Headliner Process proposal
4. Glamsterdam Meta Thread
5. Glamsterdam’s PFI EIPs
6. Community feedback for headliners proposals

## Replies

**abcoathup** (2025-12-11):

I’m the editor of [Ethereal news](https://ethereal.news) and former editor of Week in Ethereum News.  I’ve been summarizing ACD calls async for 4+ years.

I’m using the **Better**, **Worse**, **Start**, **Stop**, **Do differently**, **Not compromise** and **legacy process debt** format proposed by Tim for the Pectra retro (see my [Pectra Retrospective - #2 by abcoathup](https://ethereum-magicians.org/t/pectra-retrospective/22637/2))

## Better

### Two upgrades a year

Cadence and momentum really matter. Whilst Fusaka was Pectra part 2, it was still a big effort to deliver two upgrades.

### Headliner process

[Converging towards Headliners](https://ethereum-magicians.org/t/community-consensus-fork-headliners-acd-working-groups/24088#p-58740-converging-towards-headliners-5): Limiting upgrades to **at most one headliner per layer** means that we can have smaller upgrades that are easier to plan, less complex to test and faster to deliver.

### Forkcast ()

Forkcast is a massive improvement for ACD transparency and upgrade info.

[ACD](https://forkcast.org/calls) transcripts (though they struggle with our variety of accents and poor audio) and chat logs are easily accessible within hours of each call.  This is a massive improvement for call transparency.  Keen to see [breakouts added to Forkcast](https://github.com/ethereum/forkcast/issues/84).

Summary of EIPs for network upgrades.  AI is a little hit and miss, but generally adds to community understanding.

## Worse

### ACD summaries:

Actions/decisions written by ACD moderators have tailed off, but Forkcast AI generated summaries aren’t yet ready to fully replace (or need human curation).

Recent examples of timely info gaps: short list of non-headliner EIPs for CFI/DFI and list of non-headliner EIPs that have been CFI/DFI.

Previously ACD{E/C} moderator summaries had been shared on Eth R&D Discord and Eth Magicians (or I have copied them there) within ~24 hours.

I appreciate that we need to lighten the load on moderators, so we need to find a way of quickly gathering/sharing this info.  See: [Call moderator summary of decisions & action items · Issue #39 · ethereum/forkcast · GitHub](https://github.com/ethereum/forkcast/issues/39)

---

## Start

### Defining the Fork Focus

[Fork focus](https://ethereum-magicians.org/t/community-consensus-fork-headliners-acd-working-groups/24088#p-58740-defining-the-fork-focus-4) is meant to be the step before selecting headliners.  We didn’t really do this for Fusaka (L2 scaling was the default focus due to PeerDAS) or for Glamsterdam.

Answering the question on whether Heka/Bogotá should be focused on **L1 scaling**, **L2 scaling**, **UX**, **decentralization** or **something else** would help with which headliners should be selected and which non-headliner EIPs should be included.

## Stop

### Saying yes

FOCIL was proposed as a headliner for Glamsterdam.  When it wasn’t chosen it should have been DFIed like the other non-selected headliners but was instead CFIed.

When scoping non-headliner EIPs for Glamsterdam, FOCIL’s CFI status mean the options were to give up the ideal of six monthly upgrades by extending the timeline by weeks to months or DFI.  We have then had multiple ACDs discussing whether FOCIL should be given special status as SFId for Heka/Bogotá, which will then repeat the problem again.

FOCIL supporters are rightly annoyed & frustrated, but this could have all been avoided if we just followed the process and DFId when FOCIL wasn’t selected as the Glamsterdam headliner.

FOCIL should be treated as any other candidate headliner.  It’s support will likely see it as the headliner for Heka or I-star (depending on the **Fork focus**).

## Do differently

### Non-headliner EIPs

Glamsterdam had 50+ non-headliner EIPs.

EIP champions needed feedback earlier on if their EIP had a chance and what else they needed to do.  **Fork focus** could help here to suggest EIPs shouldn’t be proposed for a particular upgrade.  Perhaps we need **upgrade office hours** to give this feedback or a **working group**.  We could try this for Heka/Bogotá?

Client teams provided preferences but in a variety of formats and preference tiers.  Making it a challenge to curate.   We should ask teams to update a shared DFI list and CFI list along with reasoning/questions.  Though we need to be careful that we don’t lose rough consensus.

### Minimum mainnet timeline

We should define a minimum mainnet timeline from testnet releases

*(based on [pm/processes/protocol-upgrade.md at master · ethereum/pm · GitHub](https://github.com/ethereum/pm/blob/master/processes/protocol-upgrade.md))*

It should be as short as possible (but also match the reality).  In Fusaka we didn’t give enough time between the last testnet upgrade and when client releases were expected.  Teams suggested that 7 days would be required.

| Event | Min days | Total elapsed |
| --- | --- | --- |
| testnet release(s) |  | 0 |
| 1st testnet upgrade | 14 | 14 |
| 2nd testnet upgrade | 14 | 28 |
| mainnet date set | 2 | 30 |
| mainnet client releases | 7 | 37 |
| mainnet upgrade | 30 | 67 |

This helps set expectations of when releases are required when targeting specific timeframes.

*Completely hypothetical mainnet targets (for illustration purposes only)*

**Glamsterdam** : June 24, 2026, testnet release(s) required by April 18, 2026 (at the latest).

**Heka-Bogotá** : December 9, 2026, testnet release(s) required by October 3, 2026 (at the latest).

### Named public devnet

We should provide a named public devnet prior to public testnets.  We didn’t do this for Fusaka but have done it previously. (e.g. [Mekong](https://blog.ethereum.org/2024/11/07/introducing-mekong-testnet) for Pectra).

Some L2s were surprised when the Fusaka upgrade of Sepolia testnet had a breaking change ([blob proofs to cell proofs](https://blog.ethereum.org/2025/10/15/fusaka-blob-update)).

A named public devnet invites the developer community to test earlier, prior to upgrading public testnets.

### Upgrade mascots


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-8066)





###



Process for assigning a mascot to each Ethereum network upgrade










## Not compromise

*(Similar to [my Pectra retro](https://ethereum-magicians.org/t/pectra-retrospective/22637/2#p-55105-not-compromise-7))*

### Rough consensus

Clients have a variety of owners, including an L2, a VC/alt-L1 and the EF.  Decisions should be by rough consensus and avoid ACD being captured by any one group.

### Informal veto

ethPandaOps/testing should have an informal veto if an EIP is going to be to make a network upgrade too complex or risky to test.

## Legacy process debt

*(Similar to [my Pectra retro](https://ethereum-magicians.org/t/pectra-retrospective/22637/2#p-55105-legacy-process-debt-8))*

### EIP process

EIP process should work for ACD.  It should be fast & easy to get an EIP to draft status and to propose for an upgrade.

Ideally we would have an EIP editor from every client team.  I’d also like to see a funded EIP coordinator to make the process as smooth as possible.  To focus on ACD, EIPs should be completely split from ERCs.

---

**jimmychu0807** (2025-12-19):

Just want to share that forkcast is such a cool project! It put all the ACD* calls in a very organized fashion and we can refer back to the discussion and information in a very efficient manner.

If there is anything I could help make forkcast better, I am willing to help and contribute. Thanks again.

---

**abcoathup** (2025-12-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jimmychu0807/48/15578_2.png) jimmychu0807:

> I am willing to help and contribute



      [github.com](https://github.com/ethereum/forkcast?tab=contributing-ov-file)




  ![image](https://opengraph.githubassets.com/f00d62e79281a3224e11792e68605179/ethereum/forkcast?tab=contributing-ov-file)



###



Experiments in visualizing Ethereum network upgrades

