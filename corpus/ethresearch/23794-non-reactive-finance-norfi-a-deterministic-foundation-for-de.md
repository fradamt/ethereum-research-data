---
source: ethresearch
topic_id: 23794
title: Non-Reactive Finance (NoRFi) - A Deterministic Foundation for DeFi
author: hooftly
date: "2026-01-05"
category: Applications
tags: []
url: https://ethresear.ch/t/non-reactive-finance-norfi-a-deterministic-foundation-for-defi/23794
views: 154
likes: 2
posts_count: 1
---

# Non-Reactive Finance (NoRFi) - A Deterministic Foundation for DeFi

Hi ETH Research,

The following is an attempt to explore a different safety model for DeFi, one that does not depend on reacting to markets fast enough to survive them. This work is partly inspired by two posts that crystallized the direction I wanted to push toward: the Trustless Manifesto and Low-risk DeFi. They frame a clear challenge that I think DeFi still has not fully met: build financial primitives where safety comes from hard, inspectable invariants, and where users are not forced to outsource outcomes to indispensable intermediaries and adversarial market structure.

- The Trustless Manifesto
https://trustlessness.eth.limo/general/2025/11/11/the-trustless-manifesto.html
- Low-risk DeFi can be for Ethereum what search was for Google
https://vitalik.eth.limo/general/2025/09/21/low_risk_defi.html

What follows is a concrete attempt at that direction: protocols that react to commitments and time instead of price feeds and liquidation races, with deterministic state transitions, explicit accounting, and isolated Positions that bound risk by construction.

Doc Repo: [GitHub - EqualFiLabs/EqualFi: This Repo houses docs for EqualFi - A suite of deterministic anti-extraction permissionless financial protocols](https://github.com/EqualFiLabs/EqualFi)

### Abstract

Non-Reactive Finance (NoRFi) is a DeFi design direction that replaces oracle-triggered liquidations and reactive auctions with deterministic, time-parameterized state machines. Instead of positions that remain “healthy” until an external price feed flips them into a liquidation race, NoRFi agreements are defined at origination with explicit parameters, explicit transitions, and bounded terminal outcomes. The goal is not to remove market risk, but to make risk legible, local, and mechanically enforceable without relying on adversarial timing.

This work proposes a single-asset pool substrate where all activity is expressed as explicit encumbrances on balances (locked collateral, escrowed principal, offer reserves). On top of that substrate, three primitives emerge: (1) self-secured credit, where borrowing is constrained to a user’s own same-asset pooled balance, (2) direct bilateral credit funded from the same pools, optionally cross-asset, with deterministic settlement and optional early exercise, and (3) trading offers such as yield-bearing limit orders, where reserved liquidity can remain fee-accruing under the system’s accounting rules.

By eliminating liquidation races and making outcomes computable from local state plus time, NoRFi forms a cleaner execution layer for autonomous agents, whose planning and safety degrade sharply under instantaneous, oracle-driven failure modes. This post shares the thesis, core invariants, and open questions for scrutiny.

## Non-Reactive Finance (NoRFi)

NoRFi is a design space where a protocol’s safety and settlement do not depend on reacting to markets fast enough. Instead, the protocol enforces outcomes based on explicit commitments and time.

That sounds like wordplay until you look at what most DeFi systems actually do. The dominant pattern is reactive finance: positions survive until an oracle update and some threshold math says they do not, then the system scrambles to unwind risk through liquidations, auctions, and whatever MEV-sensitive microstructure happens to be available in that block. Outcomes become path-dependent. Two users with the same position can get different results because the market wick lasted 90 seconds, gas spiked, or an oracle updated one block earlier than expected.

NoRFi takes the opposite stance. Instead of using price as the trigger that decides whether a position lives or dies, NoRFi treats every position as a small deterministic machine whose behavior is defined at origination.

- Parties make explicit commitments: collateral posted, principal escrowed, term length, settlement rules, optional early exercise.
- Time advances.
- State transitions happen only when a party takes an allowed action or when the agreement reaches a defined boundary.

Markets still exist. Prices still move. Users are still taking economic risk. The difference is that the protocol is not trying to chase the market in real time to preserve solvency. It enforces a contract. The outcome is bounded and computable from local on-chain state plus time.

This matters because it changes the question from:

“How do we liquidate fast enough when something goes wrong?”

to:

“What outcomes are permitted, and what is the maximum loss that can occur, given the commitments that were made?”

That shift is not cosmetic. It is the foundation for building financial primitives that are predictable under stress, and for building agentic finance that does not require constant vigilance to avoid catastrophic, instantaneous failure.

The work shared here is an initial implementation of this idea: a deterministic substrate where lending, bilateral credit, and trading offers are all expressed as explicit encumbrances and time-based state transitions. The goal is not to claim perfection. The goal is to carve out a cleaner, more mechanical design point for DeFi that can be scrutinized, attacked, and improved.

## Account Isolation

If NoRFi is the philosophy, account isolation is the mechanical lever that makes it real.

Most DeFi lending systems are designed so depositors are protected conditional on reactive mechanisms working: timely oracle updates, sufficient on-chain liquidity, and liquidations that clear at expected prices. Under normal conditions, this generally works.

The shared-risk surface appears in tail events. If liquidations fail to fully cover debt due to extreme volatility, congestion, oracle disruption, or market dislocation, the resulting shortfall must be absorbed somewhere, typically via a shared backstop such as a pool loss, an insurance module, or governance-mediated recapitalization. This is not a moral critique. It is a dependency on reactivity as a safety assumption.

NoRFi is exploring a different assumption: depositor safety should not rely on real-time market reaction to preserve solvency.

In this implementation, every user interacts through isolated, transferable accounts (Positions). A Position is a self-contained unit represented as an NFTthat holds:

- its balances in single-asset pools
- the encumbrances against those balances (locked collateral, escrowed principal, reserved liquidity)
- the agreements it has entered (self-secured credit, direct credit, offers)
- the deterministic rules that define what it can do next and what settlement looks like

Isolation here means two very specific things:

1. No contamination
A Position cannot create an unbounded liability for other Positions. If something goes wrong, the blast radius is constrained to the accounts and agreements that explicitly opted into that risk.
2. Explicit encumbrance
Risk is expressed as a reduction in what a Position can withdraw, not as an implicit claim on a shared pool. If a Position escrows principal into a Direct credit agreement or reserves liquidity for a trade, that capital is marked as committed. It is not available to withdraw, and it is not available to be double-used elsewhere.

This is the key difference between “we track positions separately” and actual isolation. Isolation is not a UI feature. It is an accounting rule: commitments are first-class, and they reduce freedom elsewhere.

Account isolation also pairs naturally with determinism. Because each Position’s lifecycle is driven by local state and time, an observer can reason about it without reconstructing the global market story. You can answer concrete questions from the chain alone:

- What is committed?
- What is withdrawable?
- What states are reachable next?
- What are the terminal outcomes, and what is the maximum loss on each path?

That is the shape of safety NoRFi is aiming at: not “nothing bad can happen,” but “bad outcomes are bounded, explicit, and contained to the parties who chose them.”

## No Intermediaries

A lot of DeFi risk does not come from “smart contracts.” It comes from the people and processes you are forced to depend on when the contracts hit the real world.

Oracles are intermediaries. Liquidators are intermediaries. Keepers are intermediaries. Governance is often an intermediary wearing a decentralized costume. Even when these actors are economically incentivized rather than legally trusted, they are still indispensable. If they fail, get censored, get bribed, or simply stop showing up when conditions are worst, the user’s outcome changes.

NoRFi pushes in the opposite direction: design the primitive so it does not require a third party to keep it safe.

In this work, the protocol is not asking the network to constantly re-price your position and rescue the system through liquidation auctions. It is enforcing commitments that were made explicitly and can be verified mechanically.

- A Position becomes risky only by opting into a commitment (borrowing, escrowing, reserving).
- The protocol does not need a “who will liquidate this?” answer to remain solvent.
- Settlement is a defined state transition, not a market emergency.

This is not an argument that oracles are evil. It is an argument that oracle dependence is a control surface. If your core safety relies on an external feed staying honest and timely during stress, you have introduced an indispensable intermediary, even if the feed is decentralized.

Similarly, if solvency depends on a competitive swarm of liquidators behaving correctly under congestion and MEV, you have outsourced safety to adversarial market structure. That is still an intermediary, just one you do not get to sue.

The standard response is “incentives will handle it.” Sometimes they do. NoRFi tries to make that unnecessary for the core guarantees.

The result is a different definition of robustness:

Not “the system can be saved in real time by external actors,” but “the system’s worst-case outcomes are bounded by commitments and enforced by the chain.”

That is what “no intermediaries” means here. Not that nothing external exists, but that the core safety properties do not require an external actor to behave well at the exact moment the world is on fire.

## User Agency

A subtle thing happened as DeFi matured: we normalized extraction as a safety feature.

Liquidation penalties, auction discounts, priority gas auctions, MEV backruns, keeper rewards, oracle update games. Individually, each of these is often justified as “necessary for protection” or “required for solvency.” In aggregate, they create an environment where a user’s downside is not just market risk, but the protocol’s built-in permission for third parties to profit from your misfortune, especially when conditions are chaotic.

This is not an accusation. It is an observation about incentives. If a system’s safety relies on external actors showing up at the worst possible moment, then the system must pay them, and it must create opportunities for them to win. That payment is extraction, even if it is framed as protection.

NoRFi aims to restore a simpler form of user agency: your outcome should depend primarily on the commitments you chose, not on whether someone else got to your position first.

User agency in this context means:

- Bounded outcomes at origination: you can see the terminal paths and understand the worst case before entering.
- No forced race conditions: you are not dropped into a liquidation contest where speed and ordering decide your fate.
- Explicit choices instead of reactive punishment: actions like repayment, roll, or settlement are governed by defined rules and time boundaries.
- Optional early exercise where appropriate: in bilateral agreements, “settlement” can be an explicit, deterministic branch a user or agent may choose, not a chaotic failure state triggered by an oracle.

Markets will always be competitive. People will always try to extract. The point is not to eliminate competition, it is to stop embedding it into the safety model of a protocol in ways that systematically reduce user control.

The best version of DeFi is not just non-custodial. It is non-coercive: it enforces contracts, it does not manufacture crises that others are paid to exploit.

## Primitive Flexibility

NoRFi is not a single protocol. It is a design space.

The shared constraint is simple: the system does not defend itself by reacting to markets in real time. It enforces commitments through time, math, and user choice. Everything beyond that is implementation detail, and that is where the flexibility shows up.

When state transitions are deterministic, you can treat a protocol like a predictable machine rather than a fragile organism. That matters because it lets builders compose more intricate financial behavior without introducing hidden control surfaces or “someone must step in” moments.

A few examples of what becomes easier when outcomes are governed by explicit rules:

### Flexible, provable fee and revenue routing

In reactive systems, fees often depend on messy contingencies: auction outcomes, liquidation profitability, MEV conditions, oracle update timing. You can write rules for that, but reasoning about them is painful because the protocol’s behavior depends on adversarial, external dynamics.

In a NoRFi-style system, fees are typically triggered by discrete, enumerable events:

- agreement creation
- offer fills
- time-based rollovers
- repayment
- settlement or early exercise

Each event is a clean accounting moment. That means fee routing can be defined as math on known quantities:

- fixed bps on principal
- fixed bps on notional reserved
- fixed schedule-based fees
- deterministic penalties on specific branches

Once you have that, splitting revenue becomes a policy choice rather than an emergent accident. You can implement different “economic constitutions” without changing the safety model:

- route some portion to passive fee accrual
- route some portion to a reserve
- route some portion to protocol sustainability
- route some portion to active counterparties or market-makers

And because the triggers and formulas are explicit, the system is easier to audit, simulate, and reason about. You can compute what should have happened from state alone.

### More ways to create yield without hand-waving

Yield in DeFi often ends up being an opaque story told after the fact. In NoRFi, yield mechanisms can be made legible because they derive from explicit commitments:

- capital reserved for offers can accrue fees under clear accounting rules
- settlement penalties can be routed deterministically
- time-based commitments can be priced predictably
- revenue can be distributed by index formulas rather than discretionary action

This does not guarantee good yield. It makes the yield logic mechanically inspectable.

### Composability without “emergency exceptions”

Determinism also reduces the need for exception-handling logic that quietly adds trust. When a protocol depends on volatile external behavior, there is a temptation to add escape hatches: pausers, parameter changes, emergency governance, privileged liquidations.

NoRFi does not magically remove the desire for those tools, but it reduces the number of situations where they feel necessary. The more your system is “math and time,” the less it needs “humans and hope.”

The practical takeaway is that NoRFi principles can support a wide range of protocol designs, from extremely conservative to quite elaborate, while keeping the core safety story understandable:

- commitments are explicit
- transitions are enumerable
- outcomes are bounded
- revenue is computable

That is a very builder-friendly substrate. It is harder to hide surprises in it, and easier to build complex behavior on top of it without losing the plot.

## Agentic Finance

Agentic finance is not just “bots doing trades.” It is autonomous software managing capital over long horizons: allocating, hedging, rolling commitments, executing strategies, and responding to changing conditions without a human watching the health factor every hour.

That future collides head-on with the dominant DeFi safety model.

Reactive DeFi assumes a human-shaped workflow:

- watch a dashboard
- react to price moves
- top up collateral
- refinance
- scramble when the oracle flips
- hope the liquidation engine behaves under congestion

Agents do not “hope.” They need contracts that behave like machines.

NoRFi is a natural substrate for agentic finance because it turns risk from an adversarial timing game into a decision problem.

### Agents need determinism more than they need yield

In a liquidation-based system, the agent’s worst-case state transition is external, instantaneous, and adversarial:

- it can be triggered by oracle cadence
- magnified by block ordering and MEV
- worsened by gas spikes and congestion
- finalized by auctions that clear at whatever price the moment allows

This makes planning brittle. Even if the expected value is positive, the tail risk is ugly because the agent can lose control of the position at the worst possible moment.

In a NoRFi-style system, the lifecycle is enumerable:

- commitments are explicit
- transitions are known
- time boundaries are known
- terminal outcomes are bounded

An agent can actually model this. It can compute reachable states and choose actions that optimize across them.

### The key shift: “default” becomes a controllable branch

In many DeFi protocols, liquidation is an emergent failure state. In NoRFi primitives, settlement is a defined state transition.

In bilateral credit, optional early exercise is especially important: it lets an agent choose to trigger settlement under predefined terms instead of being forced into reactive liquidation dynamics. That turns “I got liquidated” into “I exercised the settlement branch because it was optimal given current conditions.”

That is the difference between:

- being punished by a market event
- executing a contract clause

Agents are built for the second world.

### Time is an API

This is an underrated point. Agents are good at scheduling, forecasting, and optimization under constraints. They are not good at surviving ambiguous, adversarial triggers that can happen at any instant.

When agreements are time-parameterized, time becomes a reliable interface:

- maturities
- windows
- roll periods
- known fee schedules
- known settlement boundaries

This makes strategies composable. An agent can chain actions together with confidence that the contract will still be in the expected state when it acts.

### Determinism reduces the need for “trusted ops”

Agentic finance at scale cannot depend on specialized operators keeping the system alive:

- keepers that must show up
- liquidators that must behave correctly
- oracle updaters that must remain honest and timely

Those are intermediaries, and intermediaries are operational risk. Agents do not want a dependency graph of human organizations and incentive schemes between them and their outcomes.

NoRFi reduces that dependency surface because the protocol is not outsourcing solvency to real-time market reactions. It enforces commitments. The agent only needs the chain to keep producing blocks.

### Why this matters beyond ideology

If agentic finance becomes real, protocols that require constant reactive defense will become less usable over time, not more. The more autonomy you push into software, the more you need the substrate to be stable, legible, and non-coercive.

NoRFi is built around that requirement. It is finance where the rules do not change based on market chaos, and where the worst-case outcome is something you can compute before you enter.

That is why I think NoRFi is not merely compatible with agentic finance. It is the direction DeFi may have to move to if we want autonomous capital to be more than a collection of bots fighting liquidation engines for scraps.

## The first NoRFi reference implementation

Equalis is the current reference implementation of these NoRFi ideas. It is not meant as “the one true design,” it is a concrete system you can inspect to see what falls out when you commit to determinism, explicit encumbrance, and isolated Positions.

In the current reference implementation, the following is available:

- Position NFT
User state is represented by an isolated, transferable Position (an NFT) that holds balances, encumbrances, and agreement state.
- Self-Secured Credit (Term and Revolving)
A Position can borrow only against its own pooled balances in the same asset. Both fixed-term and revolving forms exist.
- Direct Credit (P2P agreements)
Bilateral agreements funded from the same single-asset pools. These agreements can be same-asset or cross-asset and settle deterministically. In payoff terms, they can express bounded, option-like outcomes (call or put shaped exposure) without oracle-triggered liquidation.
- Early exercise and callable structures
Direct agreements can optionally allow early exercise (borrower-triggered deterministic settlement) and callable-like behavior (lender-triggered actions under predefined rules). The key point is that these are explicit state transitions, not reactive liquidations.
- Managed Pools (institutional configuration)
Pool variants that support constrained participation and policy controls for environments that require them, while still using the same underlying accounting model.

### Fee Index and Active Credit Index

Equalis separates “where yield comes from” into two deterministic accrual paths, each triggered by explicit events and accounting rules:

- Active Credit Index (ACI)
Capital that is actively participating in credit, both on the borrowed side and the lent side, earns ACI. This is the accounting path tied to active credit utilization.
- Fee Index
Passive depositors accrue Fee Index, and certain encumbered balances can also accrue it (for example, locked collateral posted for Direct agreements), because the system tracks withdrawal availability separately from fee accrual.

The important point is not the exact formulas in this section, it is that both indices are driven by discrete, enumerable actions and time. That makes them easier to model, audit, and reason about than yield mechanisms that depend on liquidation profitability or auction conditions.

### Yield-Bearing Limit Orders (YBLOs)

On top of the same pool substrate, Equalis also supports **Yield-Bearing Limit Orders (YBLOs)**. These are trading offers that reserve capital like a traditional limit order, but do so through explicit encumbrance rather than moving funds out of the yield surface.

Conceptually:

- A Position posts an offer to buy or sell at a specified ratio.
- The required balance is reserved (encumbered) so it cannot be withdrawn or double-used.
- While reserved, that balance can still accrue Fee Index, because fee accrual is accounted separately from withdrawability.
- When the order fills, the trade executes deterministically according to the offer terms, without turning into an open-ended credit position.

The practical effect is that you can keep liquidity “on the wall” without choosing between being a maker and earning protocol-distributed fees. It is another example of the NoRFi pattern: explicit commitments + deterministic execution, rather than reactive market making logic.

### Self-secured credit and high LTV without liquidation risk

Self-Secured Credit can support high LTV, for example 95%, because the system does not need a liquidation buffer in the traditional sense. There is no mechanism that tries to forcibly close you based on a price move. Instead, the design requires only that the Position maintain enough buffer to service the predetermined penalty on the settlement path.

Conceptually:

- You are not protecting the protocol from price; you are satisfying a known contractual requirement on the “settlement” branch.
- The worst-case outcome is bounded by the agreed rules, so the buffer is sized to deterministic costs, not market chaos.

### A chained leverage scenario (not “free yield,” but agent-plannable)

Because each Position and each pool interaction is isolated and deterministic, you can build chained strategies that would be terrifying in liquidation-based systems.

Example workflow:

1. User deposits Token A into Pool A
2. User borrows at 95% LTV in Token A (Self-Secured, same-asset)
3. User swaps borrowed Token A for Token B
4. User deposits Token B into Pool B
5. User borrows at 95% LTV in Token B
6. User swaps borrowed Token B for Token C
7. User deposits Token C into Pool C
8. User borrows at 95% LTV in Token C
9. Repeat across additional assets as desired

A few things to underline so this is not misread:

- This is not free yield. Borrowed amounts accrue interest (ACI), and swaps introduce spread, fees, and execution cost.
- The point is that the user can plan advanced, multi-leg strategies where each leg has deterministic terms and no liquidation race.
- Each leg is isolated in the sense that the protocol is not going to cascade-liquidate the entire structure because of a transient wick in one market. If a specific leg becomes uneconomic, the user’s downside is bounded by that leg’s commitments and settlement rules, not amplified by forced reactive unwind.

This is the kind of environment autonomous agents want: not an absence of risk, but a ruleset where risk is explicit, localized, and computable, making sophisticated chained strategies feasible without building a perpetual liquidation-defense machine around them.

## NoRFi Index Tokens

The current implementation also provides an **Index Token Factory**. The point is not “passive investing,” it is a deterministic way to mint and redeem multi-asset baskets without turning the protocol into a reactive price engine.

At a high level, the factory creates a new ERC20 index token whose backing is defined entirely by math:

- A fixed list of component assets
- A fixed bundle amount for each asset per 1e18 index units
- A fixed fee schedule for mint, burn, and flash loans
- A deterministic fee split between holders (fee pots) and a protocol treasury (optional)

There is no rebalancing logic. There is no “track an index price.” The basket is defined by composition, not by an oracle.

### What gets created

When you create an index, you are deploying a dedicated **IndexToken ERC20** and registering a corresponding **Index configuration** inside the factory.

The creation parameters define:

- name, symbol for the ERC20
- assets[]: the basket components
- bundleAmounts[]: how much of each asset backs 1e18 units of the index token
- mintFeeBps[] and burnFeeBps[]: per-asset fees on mint and burn
- flashFeeBps: fee for flash loans
- protocolCutBps: the split of collected fees between holders and protocol treasury (if enabled)

Creation is deterministic and defensive:

- Array lengths must match
- Assets must be unique
- Bundle amounts must be non-zero
- Fees are capped (mint, burn, flash each capped, protocol cut capped)

The factory returns:

- a new indexId
- the deployed IndexToken address

### Dual-balance accounting: why mint and burn are easy to reason about

Each index tracks two balances per asset:

1. Vault balance (NAV backing)
This is the core backing of the index token, the “real” underlying.
2. Fee pot balance (accumulated fees)
Fees paid during mint, burn, and flash loans accumulate here and are not immediately paid out. They are distributed pro-rata to holders when they burn.

This split is important because it makes the system’s behavior very legible:

- NAV is the backing.
- Fee pots are the accumulated “dividend pile.”
- Burning redeems your share of both.

### Minting: how new index units are issued

To mint `units` of an index token, the minter transfers the required basket amounts into the vault, plus fees.

For each asset in the bundle:

- required = bundleAmount * units / 1e18
- fee = required * mintFeeBps / 10_000
- User transfers required + fee

Then:

- required is credited to the vault balance
- fee is split deterministically:

potShare goes to the fee pot for that asset
- protocolShare goes to treasury if treasury is configured, otherwise it also goes to the fee pot

The mint is proportional and mechanical. For existing indexes with supply, issuance is based on preserving proportional ownership across the basket. The contract chooses the limiting proportional contribution across assets so supply cannot be inflated by under-funding one component.

Practical note: the implementation includes fee-on-transfer protection by checking received amounts against expected minimums. Overpayment is not refunded. That keeps mint deterministic under weird ERC20 behavior.

### Burning: how redemption works

To burn `units`, the holder returns index tokens and receives a pro-rata share of both NAV and accumulated fees.

For each asset:

- navShare = vaultBalance * units / totalSupply
- potShare = feePotBalance * units / totalSupply
- gross = navShare + potShare
- burnFee = gross * burnFeeBps / 10_000
- netOut = gross - burnFee

Then:

- navShare is deducted from vault balance
- potShare is deducted from fee pot
- burnFee is split using the same pot versus protocol rule
- netOut is transferred to the burner

This is why the fee pot model is clean: fee distribution happens naturally at burn, without needing periodic rebase logic, checkpoints, or external accounting.

### Flash loans: borrow the basket, pay deterministic fees

Flash loans are basket-proportional:

- You specify units
- For each asset, the loan amount is:

loanAmount = vaultBalance * units / totalSupply

Fee is:

- loanFee = loanAmount * flashFeeBps / 10_000

The receiver gets the assets, executes arbitrary logic, then must return principal plus fees in the same transaction. Fees again split deterministically into fee pots and optionally protocol treasury.

### Why this fits NoRFi

This index system is “NoRFi-aligned” for a simple reason: it does not need to react to market prices.

- The basket is defined by fixed composition and fixed quantities per unit.
- Mint and burn are just proportional accounting against on-chain balances.
- Fees and fee splits are explicit math on explicit events.

So you get an index-like primitive that is:

- non-custodial in the meaningful sense (backing is on-chain and redeemable)
- deterministic to reason about and test
- compatible with more complex systems, because “what happens” is always derivable from state plus the call parameters, not from external price updates

In other words, the factory produces index tokens that behave like clean mechanical objects. They do not require an oracle to be “correct,” because the definition of correctness is the bundle itself.

## What now?

This post is meant to be a public starting point, not a conclusion. The designs, specs, and supporting notes live here:

https://github.com/EqualFiLabs/EqualFi

I would value critique in the form DeFi research is best at: attack the assumptions, find the edge cases, and tell me where the invariants fail.

### What I am asking for

- Invariant review: Do the stated NoRFi goals actually hold under adversarial conditions, or do they collapse into hidden reactivity somewhere?
- Accounting review: Are the encumbrance and withdrawal constraints sound, especially under partial fills, multiple agreements per Position, and complex sequences of actions?
- Game theory: Where do incentives still create extraction or coercion, even without liquidation races?
- MEV and boundary conditions: What MEV strategies remain around fills, rollovers, maturity boundaries, and settlement execution?
- Safety surfaces: Where are the remaining trust assumptions (upgradeability, role-gated configuration, token allowlists, managed pools), and which ones are unacceptable if the goal is trust minimization?

### Potential blockers I can already see

These are areas I expect to be controversial or technically difficult:

- ERC20 weirdness: fee-on-transfer, rebasing, non-standard return values, and token hooks can break “clean math” systems unless aggressively constrained.
- Timestamp and time-window edges: time-based rules are predictable, but they also create boundary games that need careful handling.
- Complex composition risk: even if each leg is isolated, users can chain legs into high leverage structures. This is not a protocol solvency risk in the same way as liquidation systems, but it can create user-level blowups that will be blamed on the protocol.
- Upgradeable deployment vs walkaway test: if any part is upgradeable today, that is a real control surface. The path to immutable or tightly constrained deployments needs to be explicit.
- Institutional features: managed pools are useful, but they introduce policy controls. The separation between permissionless core and constrained variants has to be very clear.

### If you only review one thing

The most valuable feedback would be: identify the smallest concrete scenario where the system violates one of its intended guarantees (risk localization, deterministic settlement, no forced race conditions), and explain why.

If NoRFi is going to be useful as a design space, it needs to be falsifiable. I am here for that.
