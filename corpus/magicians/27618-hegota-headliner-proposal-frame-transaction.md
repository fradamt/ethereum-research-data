---
source: magicians
topic_id: 27618
title: "Hegota Headliner Proposal: Frame Transaction"
author: matt
date: "2026-01-29"
category: Magicians > Primordial Soup
tags: [hegota, headliner-proposal]
url: https://ethereum-magicians.org/t/hegota-headliner-proposal-frame-transaction/27618
views: 402
likes: 11
posts_count: 5
---

# Hegota Headliner Proposal: Frame Transaction

Frame Transaction EIP: [Add EIP: Frame Transaction by fjl · Pull Request #11202 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/11202)

## Summary (ELI5)

A new transaction type where validation and gas payment are defined by smart contract code instead of enshrined ECDSA signatures. This enables:

- Post-quantum security: Accounts can use any signature scheme
- Native account abstraction: Flexible wallets with social recovery, multi-sig, spending limits
- Gas sponsorship: Someone else can pay your fees natively

**Beneficiaries:** End users (better UX and safety), wallet developers, the network (PQ migration path)

## Champion

Felix Lange ([@fjl](/u/fjl)) and lightclient (@lightclient)

## Justification

### Why This Matters

| Benefit | Rationale |
| --- | --- |
| PQ security | ECDSA will break; users can migrate to quantum-resistant signatures at their pace |
| Native AA | More efficient than ERC-4337; eliminates intermediaries for mempool/bundler infrastructure. Better at “walk away” test |
| Gas flexibility | Native sponsorship support; ERC-20 gas payments without trusted intermediaries |

### Why Now

- Quantum threat requires proactive migration (10+ year timeline, but migration is slow).
- ERC-4337 validated demand and design patterns. Time to enshrine.
- EIP-7702 already changed ORIGIN semantics, reducing this proposal’s disruption.

### Why This Approach

| Alternative | Limitation |
| --- | --- |
| ERC-4337 | Separate mempool, bundlers, higher overhead |
| EIP-7701 | Overly specific about particular flows, not easy to generalize in client impl |
| EIP-7702 | Useful but solves different problem; not PQ |
| PQ tx type | Simpler, but there may be many PQ schemes that are desirable. And, it doesn’t allow us to achieve other long term goals, like key rotation. |

## Stakeholder Impact

### Positive

- Users: Better wallet UX, flexible security, gas sponsorship
- Wallet/dApp devs: Native AA infrastructure, easier onboarding
- ERC-4337 ecosystem: Natural migration path

### Negative

| Impact | Mitigation |
| --- | --- |
| Node DoS vectors from arbitrary validation | ERC-7562-style opcode restrictions; MAX_VALIDATION_GAS |
| ORIGIN behavior change | Already precedented by EIP-7702; pattern was discouraged |

## Technical Readiness

| Aspect | Status |
| --- | --- |
| Transaction format | Complete |
| New opcodes (APPROVE, TXPARAM*) | Complete |
| Gas accounting | Complete |
| Mempool rules | Defined in ERC-7562 |
| Reference implementation | Not started |
| Test vectors | Not started |

## Security & Open Questions

### Known Risks

1. Mempool DoS: Mass invalidation via shared state. This is mitigated by validation restrictions from ERC-7562.

### Open Questions

1. Paymaster support: paymasters are established under ERC-4337. While this EIP aims to be compatible with them via same mempool rules, it is open question to see that materialize. It will require working through the design with existing bundlers.

## Replies

**oxshaman** (2026-01-29):

Great read!

One question - does this imply that the plan is to continue down the path of 4337-Bundler-Style restrictions to state access. As I see the DoS mitigation is approached via ERC-7562 and `MAX_VALIDATION_GAS`.

Is full state access being considered anymore or is it out of scope?

---

**matt** (2026-01-29):

Thank you!

I would say it’s important to make the distinction between *what does the protocol allow* and *what is allowed in public transaction pool*. Our aim is to make the protocol maximally flexible, but start small and carefully expand what the public tx pool will allow.

Concretely to your question: full state access before the payer is approved in this proposal, however, you will need to find a builder who will include such a transaction. Our goal is to support self-sponsored transactions in the beginning and over time allow sponsor transactions (or other variants that gain popularity).

---

**vbuterin** (2026-01-30):

4337 already supports full state access via the paymaster mechanism.

A paymaster also serves as a de-facto custom mempool acceptance rule, and the protocol acts as a sort of “meta-mempool-acceptance-rule” where anyone can stake ETH to add their mempool acceptance rule to the list, and if too many transactions pass that rule but do not get included onchain, then it gets throttled and then delisted (as a subjective decision by mempool nodes).

Since 8141 is a modification on 7701, and 7701 is itself an onchain version of 4337, this design can be applied as-is to make a mempool for 8141 transactions.

---

**oxshaman** (2026-01-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> A new transaction type where validation and gas payment are defined by smart contract code instead of enshrined ECDSA signatures. This enables:
>
>
> Post-quantum security: Accounts can use any signature scheme
> Native account abstraction: Flexible wallets with social recovery, multi-sig, spending limits
> Gas sponsorship: Someone else can pay your fees natively
>
>
> Beneficiaries: End users (better UX and safety), wallet developers, the network (PQ migration path)
>
>
>
> ## Champion

[@matt](/u/matt) [@vbuterin](/u/vbuterin) thanks you for the responses!

I will then look into expanding the “paymaster-esque” spec to include a use-case of accessing quite complex arbitrary state for a use-case very important to us commercially. Will open a separate thread for these efforts.

