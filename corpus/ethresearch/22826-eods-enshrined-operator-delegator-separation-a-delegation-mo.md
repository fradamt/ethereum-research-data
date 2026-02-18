---
source: ethresearch
topic_id: 22826
title: "eODS (Enshrined Operator Delegator Separation): a Delegation model proposal"
author: gorondan
date: "2025-07-28"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/eods-enshrined-operator-delegator-separation-a-delegation-model-proposal/22826
views: 321
likes: 1
posts_count: 1
---

# eODS (Enshrined Operator Delegator Separation): a Delegation model proposal

*Many thanks to Barnabé Monnot, Vlladin, Michail Kalinin, Alex Stokes and Potuz for productive

discussions over the last year (these are not endorsements). While the opinions and views presented in the following work are rooted in the protocol’s roadmap and R&D discourse of the last 18 months, they do not necessarily represent the view of the reviewers and protocol people that gave their input in this project. In what follows, I propose a delegation model for broader staking frameworks like [Rainbowstaking](https://ethresear.ch/t/unbundling-staking-towards-rainbow-staking/18683), outlining its logic, structure, and implementation pathway. This post is appended by the feature’s Pyspec, while eventual Pytest and POC would advance the model towards its maturity.*

[![SHUT_UP_ANDtake_my_money](https://ethresear.ch/uploads/default/optimized/3X/e/b/ebf96930d1e4b0bc1733bf382465f5d28b3b5870_2_690x460.jpeg)SHUT_UP_ANDtake_my_money1536×1024 119 KB](https://ethresear.ch/uploads/default/ebf96930d1e4b0bc1733bf382465f5d28b3b5870)

## 0. Abstract

Delegation—the process of assigning staking power or governance authority to a third party—is

fundamental in many blockchain ecosystems. Ethereum, however, lacks native delegation support at the protocol level, relying instead on contract-based staking services. While these services have been effective in attracting capital, they introduce centralization risks and governance challenges, that significantly weaken the protocol’s credible neutrality.

## 1. Current State of Delegation

In Ethereum, delegation is primarily informal and off-chain. Staking services abstract validator

responsibilities,offering liquid staking tokens (LSTs) to users. This results in a natural split of

staking in [two classes of participants, outside protocol level](https://notes.ethereum.org/@vbuterin/staking_2023_10#Protocol-and-staking-pool-changes-that-could-improve-decentralization-and-reduce-consensus-overhead):

- Node Operators: Manage the validators that execute the protocol and ensure network security
- Delegators: Provide capital but have limited influence over validator selection or governance

In contrast, other ecosystems like Cosmos, Solana, and Tezos incorporate delegation directly into

the protocol, allowing delegators to stake with validators and participate in governance, including

shared slashing risks (in Cosmos and Solana).

## 2. Effective components in existing models

These are elements from Ethereum and other PoS ecosystems that have demonstrated measurable utility or protocol-aligned outcomes. Their success can be attributed to tangible improvements in usability, capital efficiency, or protocol design alignment.

- Staking Abstraction: the abstraction of staking mechanics via middleware — most commonly liquid staking protocols (LSPs) — has significantly lowered the barrier to participation.
- LST Composability: liquid staking tokens (LSTs) such as stETH or rETH are ERC-20
representations of staked ETH that can be used as collateral or liquidity in DeFi systems while still accruing staking rewards.
- Validator Consolidation: Ethereum’s Pectra upgrade introduced EIP-7251, which
allows validators to hold balances up to 2048 ETH — far beyond the previous 32 ETH maximum.
- Protocol-level accountability: chains like Cosmos and Tezos implement in-protocol delegation and reward tracking. Delegation relationships are visible to the consensus protocol itself, allowing for validator selection, performance tracking, and slashing to be enforced directly at the base layer.This structure seems to has proven effective in aligning delegator incentives and maintaining decentralization through transparent stake distribution.

## 3. Identified challenges in existing models

These are some of the architectural and economic limitations in current Ethereum delegation

practices, emerging directly from the performance of today’s delegation models and their impact on the network’s decentralization and validator dynamics:

- Centralization of delegation: delegated stake is highly concentrated in a few liquid staking protocols. This centralization limits protocol-level diversity and validator set autonomy and creates an oligopolistic structure that undermines Ethereum’s decentralization goals.
- Limited influence for delegators: delegators have no protocol-recognized voice in validator selection or governance.Their only recourse is to exit and move their capital elsewhere, often incurring delays and opportunity costs. Without a mechanism to express validator preferences or governance positions, delegators become economically relevant but politically voiceless. This reduces the effectiveness of delegation as a security-enhancing mechanism.
- Increased validator churn: the frequency of validator entries and exits is artificially inflated today due to the delegation model’s lack of partial stake reallocation mechanisms. Without in-protocol support for faster redelegation, liquid staking protocols must exit validators entirely and create new ones just to reallocate capital. This causes redundant validator turnover, adding load to the consensus layer (activation queue, exit queue, validator sweep), and increases the total signature verification burden. While validator consolidation introduced by EIP-7251 independently reduces churn, it does not fully resolve churn related to delegation adjustments.
Current delegation models still cause unnecessary churn when stakes shift among validators. The consolidation feature improves scalability, but it remains orthogonal to delegation-specific churn issues.
- Lack of protocol visibility into Delegation: Ethereum’s consensus protocol does not track
delegation relationships. It does not “see” whether ETH is delegated, to whom, or for how long. Without visibility, the protocol cannot support delegation-aware validator selection or governance signaling. This limits its ability to evolve toward more responsive consensus and validator accountability models.

## 4. What’s to be required of a delegation model?

Outlining a (non-limitative) list of requirements and design constraints for any viable delegation

model:

### What should it achieve

- Removal of LSTs induced contracts (deposit, delegation) risks, while maintaining the protocol’s security guarantees.
- Protocol optimization for home operators. Delegation will level the field for new competitors in the staking market, including the home operators,  so it’s only logical a viable delegation model should support the participation of the most decentralised, most diverse, but the least financially sustainable set of validator operators to the economies of scale, without centralization
- A meaningful protocol role and voice for Delegators (ETH holders)
- Protocol-native support for future introduction of governance signaling, e.g. validator rating and selection
- Improved UX for both validator operators and capital providers

### Expected functionality:

- Seamless delegation operations initiated from the ETH holder’s wallet
- Faster reallocation of protocol weight (faster redelegations)
- Enshrined accountability for permissionless and safe delegation operations
 An extended feature functionality improves the ratio between the induced protocol complexity and it’s benefits, so that Delegation would be more than a safe pipeline for generating revenue from validator operations, but also a selection mechanism enabler, and a way for ETH holders to transmit governance signals to protocol.

### Constraints

The feature should introduce as low complexity as possible, while achieving the desired functionality. In every practical sense, Delegation, IMO, should be an optional protocol feature,

supporting indirect protocol participation.

Ideally, delegation would fit well with the upgrades in the roadmap and mitigate some of the trade-offs associated with:

- Implementing SSF: SSF-imposed validator set reduction, done either by capping the validator set or by implementing Orbit SSF, will prevent or reduce protocol participation of the entities controlling insufficient stake to make the cut. The probable introduction of light protocol roles separate from attesting, will mitigate this trade-off. A viable delegation model would be compatible with future validator role specialization
- Limiting the issuance curve while simultaneously optimizing for a large number of protocol participants, albeit light ones. In the scenario of an issuance curve limitation, the value proposition of staking might become less attractive to large operators, while many small validators might want to participate. With current issuance curve, staking ETH is normal, rational behavior of any ETH holder. With an eventual curve-capping, after a certain threshold of staking, just holding ETH the asset should suffice, in order to be economically feasible, so staking, or delegation for staking will likely morph into governance signaling, with ETH holders delegating to support resilience and decentralization, rather than strictly for capital efficiency reasons. A viable delegation model would offer a seamless, safe pipeline for delegation-weighted governance signaling.

### Trust expectations for validator operators

Commercial staking nodes, offering ETH holders staking services, are [apriori credible](https://ethresear.ch/t/paths-to-ssf-revisited/22052#p-53618-protocol-roles-and-types-of-nodes-part-two-1), because of their legal and commercial bounds to perform their Agent duties well and to maintain a good reputation.The differentiation between home operators and commercial ones is indeed, not one of performance, but of **trust**. Home operators gain trust for their agency by the means of cryptoeconomics, or “having skin in the game”.

A viable delegation model would offer a seamless way for validator operators to put down a bond and become eligible for receiving delegations. And while having “something at stake” will most likely persist in Ethereum, the protocol might accept in the future, with the proper infrastructure, other trust metrics than credibility, like alignment with community values.

---

## 5. Surrendering the model

eODS(enshrined Operator Delegator Separation) proposes the separation of Validator role between Operator and Delegator, functionally adding delegation to Ethereum’s consensus layer.

### Actors and Relationships

The following section illustrates the core roles within this delegation model:

#### EL side

- ETH holder as physical entity that provides capital and owns the withdrawal keys
- A Deposit to Delegate Contract
- A Delegation Operations Requests Contract (Precompile)

#### CL side

- Delegator as protocol entity
- Delegated Validator as protocol entity, serving as a wrapper around existing Validator entity, and
- Beacon-chain-accounting, a protocol accounting gadget

The above depicts a delegation construction, which would not modify how validators perform their protocol duties.

#### Inter-partes relationships

- ETH holder: physical entity providing capital, and possessor of the withdrawal credentials.
- ETH holder deposits to DEPOSIT_TO_DELEGATE_CONTRACT
- Delegator, as protocol entity is created, or if existing, its balance is topped-up
- Delegator is controlled by ETH holder’s withdrawal key
- The BeaconState’s registry of delegated validators formalizes the relationship between delegators and validators at protocol level. Under this model, the following conditions MUST be met for a validator to start receiving delegations:

Validator must exist in state registry
- It’s withdrawal credentials set to compounding and validator opts in on becoming Operator, i.e.validator.is_operator parameter set to True.

Upon delegation, the delegators are explicitly linked to delegated validators. The delegators registry inside each delegated validator object contains two parallel lists: `delegated_balances` and `delegators_quotas`
Beacon-chain-accounting, an enshrined accounting gadget responsible for keeping the delegation-specific balance sheets.

#### Capital Flow Diagram

[![CAPITAL FLOW](https://ethresear.ch/uploads/default/optimized/3X/f/6/f6f6a45cfb630004592da71a38d42f039ff2df2a_2_690x436.png)CAPITAL FLOW2731×1727 158 KB](https://ethresear.ch/uploads/default/f6f6a45cfb630004592da71a38d42f039ff2df2a)

#### Delegation Lifecycle

Delegation Lifecycle for this eODS model consists of the following possible delegation-specific

actions:

##### Deposit to delegate

```csharp
**ETH holder**
  └── sends ETH from execution address→ **Deposit to Delegate Contract** (ETH is burned)
       └── Contract emits → deposit to delegate event
            └── received by → **Consensus Client** via the execution payload
                 └── deposit to delegate request is processed during epoch_transition
                      └── creates new **Delegator** inside the Beacon State
                          tops-up existing **delegator**s balance with delegated amount
                            └── links → **ETH holder** ⇄ **Delegator** via ETH holder s execution address
```

##### Activate operator

```csharp
**Validator signs EL tx with withdrawal key**
  └── calls **Delegation Operations Requests Precompile**
       └── received by → **Consensus Client** via the execution payload
            └── activation request is processed during epoch_transition
                └── changes `validator.is_operator` parameter to `True`
                    └── appends the **Delegated Validator** inside the Beacon state registry
                      └── links → **Delegated Validator** ⇄ **target Validator**
```

##### Delegate (to validator)

```csharp
**User (Delegator) signs EL tx from execution address**
  └── calls **Delegation Operations Requests Precompile**
       └── received by → **Consensus Client** via the execution payload
            └── delegation request is processed during epoch_transition
                 └── asserts the delegation amount fits in the activation churn limit
                     └── invokes → **beacon-chain-accounting**
                          └── decreases **Delegator**s non delegated balance (available balance) with delegated amount
                          └── increases **Delegated Validator**'s total delegated balance and
                              the delegated balance from that specific Delegator with delegated amount
                          └── recalculates delegators quotas under that specific **Delegated Validator**
                          └── cumulates the **Validator**'s total delegated balance into its effective balance
```

##### Undelegate (from validator)

```csharp
**User (Delegator) signs EL tx from execution address**
  └── calls **Delegation Operations Requests Precompile**
       └── received by → **Consensus Client** via the execution payload
            └── undelegation request is processed during epoch_transition
                └── calculates the undelegation s exit and withdrawability epochs
                └── appends the undelegation in the undelegation exit queue
                    └── at withdrawal epoch, invokes → **beacon_chain_accounting** to settle undelegation
                        └── decreases **Delegated Validator**s total delegated balance and
                            the delegated balances from that specific Delegator with undelegated amount (includes validator fee)
                        └── recalculates delegators quotas under that specific **Delegated Validator**
                        └── credits **Delegator**s non delegated balance with the undelegated amount minus validator fee
                        └── credits **Validator**s actual balance with validator fee
```

##### Redelegate (from source validator to target validator)

*Note:* A redelegation is composed of one undelegation followed by one delegation.

```csharp
**User (Delegator) signs EL tx from execution address**
  └── calls **Delegation Operations Requests Precompile**
       └── received by → **Consensus Client** via the execution payload
            └── redelegation request is processed during epoch_transition
                └── calculates the redelegation s exit and withdrawability epochs before balance re-allocation to target validator
                └── the redelegation is appended in the undelegation exit queue
                    └── at withdrawal epoch, appends the redelegation in the delegations activation queue
                        └── delegation request processed during epoch_transition
                             └── asserts the delegation amount fits in the activation churn limit
                                 └── invokes → **beacon-chain-accounting**
                                      └── increases target validator s total delegated balance and
                                          the delegated balance from that specific delegator with delegated amount
                                      └── recalculates delegators quotas under that specific **Delegated Validator**
                                      └── cumulates the validator s total delegated balance into its effective balance
```

##### Withdraw from delegator (to execution address)

```csharp
**User (Delegator) signs EL tx from execution address**
  └── calls **Delegation Operations Requests Precompile**
       └── received by → **Consensus Client** via the execution payload
            └── withdraw from delegator request is processed during block processing
                └── the withdrawal is appended in a withdrawal queue
                    └──  the withdrawal from delegator is processed in next block → ETH minting to delegator’s address
```

---

### Internal accounting model

**Beacon-chain-accounting** is a group of methods in the eODS specification that keep the accounting of delegations. It is invoked by the protocol during state transition. It operates the “balance sheets” during delegation-specific operations like deposits, withdrawals from delegators, balance movements between delegators and delegated validators, as well as applying rewards, penalties and slashings.

This architecture ensures that beacon-chain-accounting functions as a protocol gadget, enshrined at protocol level but compatible with future upgrades, including validator role separation.

#### Quotas

Delegators and operator quotas, under a certain delegated validator, are maintained dynamically,

with rewards and penalties calculations reflecting proportional stake across delegators.

Quotas are recomputed in `DelegatedValidator` on each delegation-related state change, using

parallel lists (`delegated_balances`, `delegators_quotas`).

### Delegation Mechanics

Delegation operations are initiated through EL-triggered requests that are executed in the CL. This enables protocol-governed delegation flows.

#### Execution Layer (EL) Triggered requests

At the EL level, users interact with a delegation operations requests contract. Each

delegation-related operation emits an operations request that is committed into the

`execution_requests` list, in the execution bundle, built by EL for the proposer.

The supported EL-triggered delegation operations requests types are:

| Name | Subject to activation/exit churn |
| --- | --- |
| ACTIVATE_OPERATOR_REQUEST_TYPE | NO |
| DEPOSIT_TO_DELEGATE_REQUEST_TYPE | NO |
| DELEGATE_REQUEST_TYPE | YES |
| UNDELEGATE_REQUEST_TYPE | YES |
| REDELEGATE_REQUEST_TYPE | YES |
| WITHDRAW_FROM_DELEGATOR_REQUEST_TYPE | NO* |
| EARLY_LIQUIDITY_REQUEST_TYPE | NO* |

(*) Bounded to 16/block in order to keep to the minimum the overhead delegation-related withdrawals add to the execution payload’s footprint. This way, the gas cost for these system-level operations can be zero.

These operations requests are to be processed during epoch / block processing, with invalid requests being discarded.

#### Consensus Layer (CL) Processing

On the Consensus Layer, delegation operations requests are queued during block processing and executed at epoch, except for withdrawals from delegators balances, which are executed during block processing. The CL parses these requests and invokes the corresponding subroutines in beacon-chain-accounting. For delegation-related accounting purposes, delegation lifecycle logic is performed as modular accounting operations. The beacon-chain-accounting module does not initiate state transitions or manage registries directly; its subroutines are called by the beacon chain, which orchestrates the Beacon state transition.

Each of the following methods implement a single stage in the delegation lifecycle:

| Request Type | beacon-chain handler | beacon-chain-accounting handler | Functionality |
| --- | --- | --- | --- |
| ACTIVATE_OPERATOR_REQUEST_TYPE | process_pending_activate_operators(...) | - | Appends a new delegated validator to state.delegated_validators registry. The validator is now considered an operator and can receice delegations |
| DEPOSIT_TO_DELEGATE_REQUEST_TYPE | process_pending_deposits_to_delegate(...) | increase_delegator_balance(...) | Tops-up a delegator’s non delegated balance in state.delegators_balances by deposited amount. If the delegator does not exist, it appends a new one in state.delegators[] registry |
| DELEGATE_REQUEST_TYPE | process_pending_delegations(...) | delegate_to_validator(...) | Reduces delegator’s non delegated balance and increases delegated validator’s total_delegated_balance. Beacon-chain-accounting recalculates the ETH quotas of all stakeholders in the delegated validator |
| UNDELEGATE_REQUEST_TYPE | process_pending_undelegations(...) | undelegate_from_validator(...) | Reduces delegated validator’s total_delegated_balance, Credits the undelegated amount minus operator fee (amount * fee_quotient) back to the delegator. Credits operator fee to the delegated validator |
| REDELEGATE_REQUEST_TYPE | process_pending_redelegations(...) | settle_undelegation | Initiates a sequence of one undelegation followed by one delegation, from source validator to target validator. Credits operator fee to source delegated validator |
| WITHDRAW_FROM_DELEGATOR_REQUEST_TYPE | process_withdrawals_from_delegators(...) | decrease_delegator_balance(...) | Withdraws some amount of non delegated balance back to delegator’s execution address |
| EARLY_LIQUIDITY_REQUEST_TYPE | process_early_liquidity_request(...) | decrease_delegator_balance(...) | Validators that withdraw part of their balance or are voluntarely exiting, request early liquidity via delegator-facilitated transfer, against a fee. Delegator has to put down a bond, for accountable safety reasons |

### Accountable safety in eODS

Weak subjectivity period is not affected by the proposal. A detailed analysis of how this model

keeps the balances that enter and exit the protocol accountable, can be found [here](https://hackmd.io/@kboomro/SJ3MlAKZeg).

---

### Rewards and Penalties

Rewards and penalties are distributed each epoch, for all delegated validators and their delegators, proportionally to their participating quotas.

### Slashing

Slashing is a core security mechanism in proof-of-stake systems, penalizing validator misbehavior such as equivocation. It protects consensus integrity by imposing economic consequences on actors responsible for critical failures. In Ethereum today, slashing applies only to validators.

Delegators — typically users of staking pools — are not slashable at the protocol level. Any losses they incur are mediated by the terms of the staking service, not by the protocol itself. Other ecosystems like Cosmos, Tezos, and Solana implement native delegation tracking and apply slashing proportionally to delegators.

#### Slashing under eODS

This model proposes the introduction of slashing both the equivocating validator and its eventual

delegators, proportional to their participating quotas.

#### Comparison of Slashing Models

The proposed approach to slashing ensures that capital suppliers are directly exposed to validator risk, which strengthens alignment but also increases passive stakeholder exposure, with delegators being incentivised to delegate to validator operators that emit their requested levels of credibility signals.

| Protocol | Slashing Target | Protocol-Level Delegation | Delegators Slashable | Delegator Impact |
| --- | --- | --- | --- | --- |
| Ethereum (current) | Validators only |  |  | Indirect via pool policies |
| Ethereum (with this eODS model) | Validators & Delegators |  |  | Direct proportional slashing |
| Cosmos | Validators & Delegators |  |  | Direct proportional slashing |
| Tezos | Validators & Delegators |  |  | Shared loss on misbehavior |
| Solana | Validators & Delegators |  |  | Delegated stake slashed directly |

### Protocol-level redelegation

Protocol-level redelegation allows a delegator to shift part of their delegated stake from one

validator to another without performing a full withdrawal followed by a redeposit. This addresses

one of the core limitations of delegation via smart contract-based staking pools. It also helps

reduce validator churn, preserve network stability, and gives delegators agility in responding to

operator performance or governance preferences. At a high level view, a redelegation is composed of one undelegation operation, followed by one delegation.

The link to the work containing a deep dive into delegation, undelegation and redelegation form a developer’s perspective is provided in the *Appendix.*

---

## 6. User stories and lifecycle integration

To understand the practical implications of eODS, we frame its functionality through the lens of

participant experience. The following user stories exemplify how Ethereum stakeholders—ETH holders, validator operators, and protocol clients—interact with the delegation lifecycle under this model.

These are not hypothetical end-user interfaces, but role-grounded narratives structured around

protocol affordances proposed in eODS.

### ETH Holders (Delegators)

- As an ETH holder, I want to deposit ETH into the DEPOSIT_TO_DELEGATE_CONTRACT,
so that I become a protocol-recognized delegator with a registered execution_address and balance.
→ Lifecycle: DEPOSIT_TO_DELEGATE_REQUEST_TYPE → PendingDepositToDelegate, processed at epoch boundary via process_pending_deposits_to_delegate`.
- As a delegator, I want to delegate a portion of my non delegated balance to a validator, so that my stake contributes to protocol security and may accrue rewards via that operator.
→ Lifecycle: DELEGATE_REQUEST_TYPE → PendingDelegateRequest, added on block, processed on epoch via process_pending_delegations.
- As a delegator, I want to reallocate stake from one validator to another without exiting the system, so that I can react to operator performance or governance trends efficiently.
→ Lifecycle: REDELEGATE_REQUEST_TYPE → PendingRedelegateRequest, added on block, triggers a redelegation path through the DelegationExitQueue.
- As a delegator, I want to undelegate from a validator back into my non delegated balance, so that I retain the ability to reassign stake or withdraw it to EL later.
→ Lifecycle: UNDELEGATE_REQUEST_TYPE → PendingUndelegateRequest, added on block, drained on epoch, with staged withdrawal via DelegationExitItem.
- As a delegator, I want to withdraw ETH from my non delegated balance back to my execution address, so that I regain full liquidity outside the staking system.
→ Lifecycle: WITHDRAW_FROM_DELEGATOR_REQUEST_TYPE → PendingWithdrawFromDelegatorRequest, processed within block, via get_expected_withdrawals_from_delegators.
- As a delegator, I want my delegation relationships to be observable by the protocol, so thatnthey can serve as public signals for validator alignment and potential governance use.
→ Lifecycle: Delegation metadata is exposed in DelegatedValidator containers, viewable via state inspection, but not enforced.

### Validator Operators

- As a validator, I want to activate my operator status, so that I can receive delegated stake and serve as a delegated validator.
→ Lifecycle: ACTIVATE_OPERATOR_REQUEST_TYPE → PendingActivateOperator, verified on block and processed immediately via process_pending_activate_operators.
- As a validator, I want to receive delegated stake from multiple delegators, so that I can amplify my validator weight through reputation, not capital alone.
- As a validator, I want to coordinate early liquidity with a delegator during exit, so that I can access ETH before the full withdrawal queue delay.
→ Lifecycle: EARLY_LIQUIDITY_REQUEST_TYPE internally pairs a delegator-initiated withdrawal to operator credentials with a future validator-side repayment.

### Protocol Functions

- As the consensus layer, I want to receive structured delegation requests via execution_requests.delegation_operations, so that I can interpret, queue, and process them at the correct protocol-defined timing.
→ Lifecycle: DelegationOperationRequest dispatched on block, parsed by process_delegation_operation_request, routed to appropriate buffer.
- As the protocol state machine, I want to enforce timing discipline over delegations, so that churn and queues rate limitations are maintained.
→ Lifecycle: Draining of buffers (process_pending_*) occurs at epoch, except for withdraw_from_delegator which drains at block with cap of 16.
- As the accounting layer, I want to maintain delegator quotas dynamically, so that reward/penalty calculations reflect proportional stake across delegators and operator.
→ Lifecycle: Quotas recomputed in DelegatedValidator on each delegation-related state change, using parallel lists (delegated_balances, delegators_quotas).

## 7. Next steps

In this post I proposed a feature that would separate the Validator role between the Operator (the

Agent) and the Delegator (the Principal), bringing to light the idea of having delegation enshrined

at protocol level. I presented a possible delegation model for Ethereum, as a minimal specification of eODS, that can be tested and refined in the immediate future. This model offers delegation as an opt-in feature, that would not modify validator consensus duties or alter validator selection, the delegation mechanics being presented in the previous chapters. Further research efforts can be made to develop new mechanisms on top of the minimal model, like early liquidity for validators, or a way to track delegations and related metrics.

### Early Liquidity for Validators

Under constrained conditions, validators may request immediate access to liquidity by drawing from idle (non delegated) balances held by registered delegators.

- The validator would initiate an early liquidity request. Participating delegators agree to
transfer part of their balance to the validator’s address, against a fee.
- The delegator performs a partial withdrawal of its available balance, which sends ETH to the validator’s execution address.
- The validator, in turn, is expected to repay the delegator via standard partial withdrawals from its actual balance, routed through the validator exit queue.
- The repayment is not instant — it is handled via the existing protocol withdrawal mechanism, preserving all rate limitations and slashing guarantees. The early liquidity balance is made accountable safe from the protocol’s perspective, by imposing an extra bond of equal amount from the delegator’s remaining balance, which becomes slashable, until the validator’s withdrawal reaches exit_epoch, deterring delegator-validator sybil attacks.

This feature could allow validators to access ETH in time-sensitive scenarios (e.g., wanting to exit or cover penalties / liquidations in app layer) without compromising the safety of the consensus or requiring immediate exits.

### Initial Governance Integration

Delegators will submit their non-binding preferences for validators, proportional to their stake.

These metrics could be surfaced to delegators through beacon-chain-accounting extensions, so that the protocol can track and community can study over time, such observable governance preference signals. Protocol-visible delegation data can serve as the foundation for more dynamic validator accountability in the future. Drawing from the experience of chains like Cosmos, where validator uptime and misbehavior directly impact delegation decisions, similar mechanisms in Ethereum could encourage validators to maintain high performance and transparency, align to community values and thereby earning greater delegator trust. If and when new trust metrics are developed, validator selection could take this into account, allowing rational capital to flow toward reliable, aligned operators.

---

## APPENDIX

### eODS annotated specs

A deep-dive into eODS from a developer’s point of view, plus spec annotations, can be found [here](https://hackmd.io/Sw48H9qMQ0ukWZ08egkpkA).

### Execution Layer changes

On the execution layer, the additions are:

- DEPOSIT_TO_DELEGATE_CONTRACT, similar to the current DEPOSIT_CONTRACT. The events of this contract will be parsed in-protocol the same way the DEPOSIT_CONTRACT’s events are currently parsed:
ETH Flow Semantics

The contract receives ETH and emits an event.
- ETH funds are burned on EL.
- The CL credits equivalent Gwei to the delegator’s balance

Delegation Operations Requests Contract, a dedicated smart contract inspired from the design of the [EIP-7002](https://eips.ethereum.org/EIPS/eip-7002) Withdrawal Request Contract that  uses [EIP-7685](https://eips.ethereum.org/EIPS/eip-7685) format for request encoding.

### Consensus layer changes

#### The full consensus changes can be found in the following GitHub repository. They are split between:

- Beacon Chain changes.
- Beacon Chain Accounting new specification file.
- Fork choice changes.
- Honest validator guide changes.

---
