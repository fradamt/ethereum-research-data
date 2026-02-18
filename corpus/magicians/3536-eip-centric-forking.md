---
source: magicians
topic_id: 3536
title: EIP-centric forking
author: holiman
date: "2019-08-08"
category: Magicians > Process Improvement
tags: [eip-process]
url: https://ethereum-magicians.org/t/eip-centric-forking/3536
views: 3344
likes: 13
posts_count: 9
---

# EIP-centric forking

This is my proposal for EIP-centric forking: https://notes.ethereum.org/s/S1ELAYY7S .

I have voiced this in all-coredev-calls earlier, and in gitter, but finally took the time to write it down more properly.

## Replies

**timbeiko** (2019-08-08):

Thanks for sharing! When do you see the “community concerns” being evaluated as part of this process? For example. the whole asic-resistance discussion for ProgPow.

---

**holiman** (2019-08-08):

I think that would be in the first step. The first ‘blessing’ means that it’s highly likely to make it into mainnet if sufficient work is put in, so any non-technical issues should be sorted out before the blessing is given

---

**timbeiko** (2019-08-08):

Got it.

I’m strongly in favour of having a « conceptually accepted » / « blessed » status for EIPs because it can also serve as a strong signal for grants/funding for implementation.

It doesn’t solve how we fund people coming up with an EIP, but at least helps past that stage.

---

**carver** (2019-08-08):

> “Yes, let’s activate this EIP on testnet in one month (at block X), and on Mainnet two months from now (at block Y)”.

Does this imply that X and Y are chosen arbitrarily at acceptance time here, or are they selected from a predetermined schedule of upgrade slots?

I argue for the latter, because operators get a huge benefit from knowing upgrade times, even if the EIPs included are not known until later. For example: needing to schedule extra devops folks as on-call during upgrade-time, months in advance, around planned vacations, etc.

I love:

- the two-step acceptance process gets more formalized (and “tentatively accepted” is heavily downgraded semantically from “EIP likely included” to “we’ll talk when you’re done testing”)
- the added expectation that clients must support EIPs one-by-one, rather than fork-by-fork. Not all clients may be designed this way.
- that the testing team would decouple testing EIPs from testing forks

I think you get all those benefits without changing the release schedule.

---

**carver** (2019-08-08):

Also, some name suggestions for the statuses:

When you “bless” an EIP, it becomes “Eligible for Inclusion,” or just **Eligible** for short. This reinforces the idea that more work is certainly required. An EIP cannot become accepted by inertia, it requires active work. It should be no surprise if the EIP misses the next closest release date (as opposed to “Tentatively Accepted” which might carry that baggage).

When an EIP is finally accepted, it becomes “Scheduled for Inclusion,” or just **Scheduled** for short. This reinforces the idea that no EIP is ever “potentially scheduled”. An EIP is never prematurely paired with a particular release date, it only gets a date at acceptance time.

The decoupling of EIPs from forks (in clients and testing) is what makes this late scheduling option feasible.

---

**gcolvin** (2019-08-12):

I think (and have long thought) that we need to get clear on just what “non-technical” issues the core devs should consider at all, and how we should consider them.  The interminable  progPoW debate being an example of how that can go wrong.  “The heath of the network” is the standard I’ve put forward as not purely technical but still within our competence and duties.

---

**FrankSzendzielarz** (2019-08-13):

I also like the proposal.

Also, it seems one possible implication of the proposal is that the chainspec could offer fork block numbers per EIP (for future blocks). This would offer additional some flexibility:

- if a number of EIPs get the ‘blessing’ of the proposed process and get implemented, last minute changes would allow flexible configuration of what functionality to include.
- more flexible config of private networks
- Hive (or other) testing of p2p/sync/benchmarking prior to testnet inclusion

I understand that is not the main thrust of the proposal, which is more about workflow.

---

**jpitts** (2019-10-22):

[@holiman](/u/holiman)’s proposed process essentially separates the “accept” decision and work for EIP implementation / tests from the “final” decision to include in an upgrade. This takes some political pressure off of the process, and is similar to bills in parliament being worked on in committee, then going to the floor for final vote.

From my observation of ADC meetings this would ease the decision-making process. This also improves the analysis of new features by providing a stage to focus more on the technical merits before later considering other issues e.g. the effect on stakeholder group.

A difficulty might be that dev teams get tied up in a lot of work on accepted/blessed EIPs, but then these EIPs are never actually deployed because it has only delayed political contention.

**One way of mitigating contention is forming a separate committee, consisting of more representation from community groups** (e.g. DeFi, game devs, data providers, miners, exchanges). I would name this group “product” or perhaps “roadmap”.

The findings of this committee (basically a set of position points) would of course not have any binding effect on ACD decisions, but it could be a key artifact to consider in the acceptance of an EIP or the final scheduling of release.

