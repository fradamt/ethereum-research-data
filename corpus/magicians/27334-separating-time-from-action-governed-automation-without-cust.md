---
source: magicians
topic_id: 27334
title: "Separating Time from Action: Governed Automation Without Custody"
author: recurmj
date: "2025-12-27"
category: Magicians > Primordial Soup
tags: [erc-8103, erc-8102, permissioned-pull]
url: https://ethereum-magicians.org/t/separating-time-from-action-governed-automation-without-custody/27334
views: 41
likes: 0
posts_count: 1
---

# Separating Time from Action: Governed Automation Without Custody

*Mats Heming Julner — December 28, 2025*

Most on-chain automation today implicitly collapses **time**, **authority**, and **execution** into a single actor.

Whether it’s a bot, a keeper network, a cron-style scheduler, or a multisig, the pattern is the same:

someone (or something) both decides *when* things happen and *forces* them to happen.

That coupling creates familiar problems:

- custodial risk
- discretionary execution
- fragile failure modes
- difficulty reasoning about safety when the operator disappears

I want to propose, and demonstrate, a different execution model.

---

## Core idea

**Time advances publicly. Actions occur only as a consequence of time + pre-authorized rules.**

In this model:

- Advancing time does not force execution
- Execution cannot occur without time advancing
- No actor can choose outcomes
- No actor holds custody

The only thing anyone can do is **apply time**.

---

## What changes when time is separated from action

Traditional automation works like this:

> At the right time, execute these actions.

This system works like this:

> Advance time. If rules permit actions at this time, they may occur. Otherwise nothing happens.

That distinction sounds subtle, but it has concrete consequences:

- “Downtime” does not break the system, it only pauses time
- No scheduler can force transfers
- No bot has discretionary power
- Revocation immediately stops future flows
- Misbehavior is contained by construction

Automation becomes **governed**, not commanded.

---

## Continuum: a live demonstration

Continuum is a minimal, continuously running demonstration of this execution model.

What it shows:

- A closed economic loop

*(Employer → Workers → Merchants → Treasury → Employer)*

- All value movement executed via permissioned pulls (ERC-8102 / ERC-8103)
- Time enforced by a public crank
- No private key with unrestricted transfer authority

What it does **not** rely on:

- No cron job deciding payments
- No treasury wallet pushing funds
- No bot holding custody
- No hidden operator

If the runner goes offline, nothing breaks.

Time simply stops advancing until someone applies it again.

---

## Why this isn’t “just automation”

This is not about payments per se.

It’s about **execution structure**.

Instead of automating *actions*, the system automates the **application of time**.

Actions are not triggered by an operator, they are *revealed* as allowed once time advances and rules already exist.

In other words:

- Time is public
- Authority is pre-bounded
- Execution is conditional, not imperative

---

## Relation to ERC-8102 / ERC-8103

The permissioned-pull primitives (ERC-8102 / ERC-8103) make this model possible by ensuring:

- All transfers are bounded
- All flows are revocable
- No executor ever gains custody
- Authorization is explicit and inspectable

Continuum combines these primitives with a public time mechanism to show how governed automation can operate without custody or discretion.

---

## Live instance

A live instance of Continuum is running here:

**https://pullbased.finance**

The dashboard shows balances, agents, and time progression.

It is evidence of behavior, not a control surface.

---

## Closing

This is not a proposal to replace keepers, bots, or schedulers outright.

It’s an exploration of a different execution invariant:

> Time can be advanced by anyone, but outcomes can be bent by no one.

I’ve written a longer observational paper documenting what emerged from running this live, for those interested.

Feedback, critiques, and alternative framings are very welcome.
