---
source: ethresearch
topic_id: 22607
title: "Flex Liquidity Pools: Where Capital Efficiency Meets Legal Requirements"
author: 0xrwx
date: "2025-06-13"
category: Applications
tags: []
url: https://ethresear.ch/t/flex-liquidity-pools-where-capital-efficiency-meets-legal-requirements/22607
views: 559
likes: 0
posts_count: 1
---

# Flex Liquidity Pools: Where Capital Efficiency Meets Legal Requirements

*By [Tigran Bolshoi](https://x.com/Tigr_B), [Mike Shishko](https://x.com/0xrwx) and Aleksei Bogdanov on behalf of [Swaps.io](http://Swaps.io)*

***Disclaimer***

*Development is actively ongoing. Many of the components and features described below are WIP and may be subject to change.*

*For the latest implementation details, refer to the smart contracts repository:*

![:link:](https://ethresear.ch/images/emoji/facebook_messenger/link.png?v=14) [github.com/swaps-io/flex-pool-contracts](https://github.com/swaps-io/flex-pool-contracts)

---

## Background

In recent years, the DeFi ecosystem has seen an accelerated shift from direct on-chain interactions to architectures based on intents – user-defined desired outcomes executed by a decentralized network of solvers. Protocols such as UniswapX, 1inch Fusion, CowSwap, Bebop and Velora are increasingly replacing traditional DEX interfaces by enabling users to delegate execution logic to professional actors.

One of the key drivers behind this transition has been the need to abstract away low-level transactional complexity from users, eliminating the requirement to manually manage routing, bridge and DEX selection, and transaction execution. [Studies](https://arxiv.org/abs/2503.00738v3) of intent-based execution models show that solver-based competition leads to better price discovery through price auctions, while mitigating direct MEV extraction.

This trend has also expanded into the cross-chain domain with intent-based protocols like Across, 1inch Fusion+, [Swaps.io](http://Swaps.io), Squid, Mayan and others. However, despite their growing adoption, the supporting liquidity infrastructure remains fragmented and non-standardized.

## Operational Bottlenecks for Cross-Chain Solvers

Although the intent paradigm offers clear advantages in execution efficiency and complexity abstraction, it places a substantial operational overhead on solvers.

### Capital and Liquidity Fragmentation

In most existing cross-chain protocols, solvers must pre-fund liquidity across multiple chains, manage asset rebalancing, and bear the risks associated with custody and cross-chain execution. These responsibilities are not only technically demanding but also capital-inefficient and economically risky.

### Counterparty and Credit Dependencies

To operate efficiently, solvers often seek external credit arrangements to support their inventory needs, forcing them to operate under the logic of traditional financial instruments. This effectively places them in the role of institutional borrowers, taking on the complexity of credit negotiations and repayment management. These arrangements involve trusted lenders with fixed-rate terms that are inefficient when capital is unused.

### Regulatory and Legal Exposure

Engaging with trusted and regulated entities, adhering to compliance procedures significantly increases exposure to legal and financial regulation. In many cases, it requires broker licenses and may lead to legal liabilities in case of disputes. Such requirements stand in direct contrast to the principles of permissionless and decentralized systems.

### Need for a Unified Liquidity Layer

What is missing is a unified, permissionless, and programmable liquidity layer that enables solvers to borrow capital permissionlessly, securely, and on demand, while allowing liquidity providers to earn additional yield from solver execution activity in a transparent and risk-isolated environment. Flex Pools is designed to address this gap.

## Flex Pools: Unified Liquidity for the Solver Economy

Flex Pools introduces a unified, cross-chain liquidity layer designed for intent-based protocols. Instead of relying on fragmented, self-managed inventories or centralized credit lines, solvers can borrow and return assets through various providers that access liquidity (i.e. borrow and return it) in standardized way. Liquidity providers, in turn, earn additional yield from solver execution flows in a secure, permissionless environment.

The system aligns the interests of three core participant groups:

- Solvers gain instant, on-demand access to liquidity with no need to manage cross-chain inventory or borrow from external creditors. Each interaction follows transparent on-chain contract logic, with the solver accessing liquidity only at the moment it is needed and paying solely for the duration of use. This eliminates long-term debt, fixed interest obligations, and regulatory exposure. The protocol abstracts away inventory management, rebalancing, and cross-chain verification, allowing solvers to focus purely on execution algorithms and routing logic – similar to on-chain solving.
- Liquidity Providers benefit from a scalable, multi-chain investment model with on-chain guarantees replacing legal liabilities. Flex Pools offer programmable liquidity and capital efficiency that goes beyond what common liquidity pools can offer, enabling LPs to earn additional yield from solvers’ activity.
- Solver-based systems and infrastructures – including intent-driven protocols and networks, chain-abstraction smart wallets and dapps, fast-fill bridges, and clearing layers – gain access to a shared liquidity infrastructure that lowers entry barrier and improves execution efficiency. By decoupling liquidity from solvers and clearly separating roles, Flex Pools enables greater decentralization and composability across the intent-based stack.

## Architecture

### Overview

Flex Pools is a modular liquidity protocol designed for intent-based cross-chain execution. It allows solvers to borrow assets on one chain and return them on another using standardized *borrow-and-return* operations. These operations are carried out through a variety of secure whitelisted *taker* adapters to third-party providers.

[![Example of workflow for asset-locking protocol](https://ethresear.ch/uploads/default/optimized/3X/e/e/ee2ebe9aa1d48933f2e346f52b40cd1d7d5a471e_2_690x376.png)Example of workflow for asset-locking protocol2034×1110 174 KB](https://ethresear.ch/uploads/default/ee2ebe9aa1d48933f2e346f52b40cd1d7d5a471e)

The system is organized into *enclaves* – sets of EIP-4626 tokenized vaults deployed across multiple chains for a single logical asset. Each vault manages deposits, withdrawals, and share accounting on its respective chain. The vaults within an enclave are connected through a common infrastructure that handles cross-chain messaging and verification, leveraging *event verifiers* backed by *oracles* to ensure execution validity.

The protocol is designed to be composable, enabling integration with various *taker* adapters, *event verifiers*, and *tuners* defining fee models.

### Infrastructure

The core of the infrastructure is the `FlexPool` contract, which maintains a strict whitelist of approved taker adapters. Each taker is linked to a specific third-party provider and paired with a tuner that defines execution and rebalancing fees. Together, the *taker-tuner* pair governs how liquidity is moved across chains for a given provider and enclave.

[![Flex Pool Infrastructure](https://ethresear.ch/uploads/default/optimized/3X/4/a/4a97562c53ae145d1549407a9f8d4ad6d19970dd_2_359x500.png)Flex Pool Infrastructure728×1013 96 KB](https://ethresear.ch/uploads/default/4a97562c53ae145d1549407a9f8d4ad6d19970dd)

Taker contracts are typically scoped to a specific chain-to-chain channel for better security. In many cases, the taker relies on a helper `Giver` contract deployed on the opposite chain, which emits verifiable events to prove that liquidity has been locked and committed for return to the pool. As a result, there may be several instances of one provider in the router – each deployed with different parameters to serve a specific enclave chain.

Some providers require validation of events from other chains to confirm asset return. To support this, the protocol uses an `IEventVerifier` abstraction that validates cross-chain proofs and ensures the correctness of `take` and related operations.

### Enclave Model

An **enclave** is a set of vaults deployed across multiple chains that manage liquidity for a single logical asset (e.g., USDC, ETH). Each chain hosts one vault – a standalone `FlexPool` contract – which operates independently but shares accounting logic with other vaults in the same enclave.

Enclaves are liquidity-isolated by design: assets deposited into a vault remain on that chain unless explicitly moved via a `take` operation and later returned either through a `give` call in a `Giver` helper contract or by direct token transfer back to the pool address.

While enclaves operate independently, they are logically connected through the protocol’s infrastructure. If liquidity becomes unevenly distributed – for example, when one chain is drained due to solver activity – the rebalancing mechanism incentivizes redistribution back to equilibrium.

### Asset Accounting

Each `FlexPool` vault manages a single ERC-20 token. Across chains, the same logical asset (e.g., USDC) may have different token contracts, but must retain equivalent value and fungibility. The protocol supports varying decimals and optionally wrapped or yield-bearing tokens.

[![Flex Pool Assets](https://ethresear.ch/uploads/default/optimized/3X/3/9/3945881d1b5e726a8e7a4b34c43408ad97b96ceb_2_690x234.png)Flex Pool Assets801×272 22.5 KB](https://ethresear.ch/uploads/default/3945881d1b5e726a8e7a4b34c43408ad97b96ceb)

Each pool tracks the following key asset states:

- Total Assets: The total amount of the asset managed by the pool, including all deposits and protocol fees. Represents the full obligation to liquidity providers.
- Current Assets: The amount of the asset currently held in the vault on the local chain. Includes both available liquidity and the rebalance reserve.
- Available Assets: The portion of current assets that is not reserved and can be used immediately for take or withdraw.
- Rebalance Assets: A separate reserve held within the vault and used to pay solvers for restoring cross-chain balance. Funded from take operations that increase imbalance.
- Equilibrium Assets: The difference between the vault’s current asset balance and its ideal share of the total liquidity. A positive value means the vault holds excess liquidity; a negative value means it is underfunded relative to the enclave total. This metric is used by tuners to calculate rebalancing incentives during take.

Together, these values ensure accurate accounting and safe liquidity usage across chains. They also serve as inputs for protocol fee logic and share-to-asset conversion formulas.

### Operations

Flex Pools implement both standard EIP-4626 vault operations and cross-chain liquidity transfer mechanics.

#### Vault operations

Liquidity providers interact with the pool through familiar functions:

- deposit / mint: deposit assets in exchange for shares
- withdraw / redeem: burn shares to receive underlying assets
- Preview and limit functions (previewDeposit, maxWithdraw, etc.) follow the EIP-4626 spec

Shares are ERC-20 tokens representing proportional ownership. Their value increases over time as protocol fees accumulate from solver activity.

#### Cross-chain operations

- take: transfers assets from the pool to a whitelisted taker caller. The taker is responsible for forwarding or locking these assets on the current chain and ensuring a corresponding return (minGiveAssets) on another chain. Associated fees (protocolAssets, rebalanceAssets) are calculated by the assigned tuner.
- give: returns liquidity back into an enclave. In most cases, this is implemented as a simple ERC-20 transfer to the vault, optionally wrapped in a helper giver contract to emit proof-validatable events.
- Rebalancing is handled implicitly via the rebalanceAssets value in the take operation. Solvers that relieve excess liquidity may receive a rebate, while those that increase imbalance may incur an additional fee.

These operations form the core lifecycle of liquidity in Flex Pools – from provisioning and usage to redistribution across chains.

### Takers & Givers

Takers are adapter contracts responsible for handling the execution logic of a take operation. Each taker is linked to a specific third-party provider or routing system and is approved through the pool’s internal whitelist. Takers receive the borrowed assets from the pool and must guarantee that a corresponding repayment occurs on another chain.

Takers may rely on paired `Giver` contracts deployed on the opposite chain. These contracts wrap a `give` operation, emitting verifiable events used to confirm that liquidity has been returned. Givers may enforce additional logic or safety checks required by the taker’s provider.

### Tuner System

Tuners define the economic parameters of each `take` operation. They are modular contracts assigned per taker and are responsible for calculating:

- Protocol Fee (protocolAssets) – the portion of assets paid to the pool, distributed to liquidity providers
- Rebalance Fee (rebalanceAssets) – the incentive or penalty based on how the operation affects cross-chain liquidity balance

Tuners implement a standardized interface:

`tune(assets) → (protocolAssets, rebalanceAssets)`

The most basic implementation is the current `LinearTuner`, which

applies:

- A fixed fee component
- A percentage-based fee on the requested assets
- A dynamic rebalance adjustment based on the enclave’s equilibriumAssets

More advanced tuner types – such as multi-slope models or tuners with off-chain inputs (e.g. market data, solver scoring) – can be plugged in without changing the pool logic.

Tuners ensure that fees are adaptive, fair, and aligned with current liquidity conditions across chains. They also serve as the mechanism for redistributing execution cost and maintaining systemic balance.

### Verifier Layer

Most taker providers require proof that a `give` operation has occurred on another chain before allowing a `take`. To support this, Flex Pools use a pluggable `IEventVerifier` interface – an abstract verification layer that checks cross-chain proofs that confirm the presence of specific events, exposing a single function:

`verifyEvent(chain, emitter, topics, data, proof)`

If the event is valid and final, the call succeeds; otherwise, it reverts. This mechanism allows takers to safely depend on cross-chain execution results without introducing trust assumptions or centralized relayers.

Multiple verifier implementations can coexist, enabling support for different proof systems and oracles.

### Rebalancing Logic

As solvers move liquidity across chains using `take` and `give`, imbalances can occur within an enclave. To correct this, the protocol includes a built-in rebalancing incentive mechanism, fully integrated into the `take` operation. Each `take` call returns a `rebalanceAssets` value from the tuner:

- Positive – the solver pays an additional fee, increasing the enclave’s rebalance reserve
- Negative – the solver is rewarded with surplus assets from the reserve for restoring balance

These incentives are based on the enclave’s `equilibriumAssets`, which measure how far the current state deviates from ideal state – where all total assets on the chain are fully available for `take` and `withdraw` operations.

In addition to solver-driven arbitrage, the protocol is designed to support native rebalancing via external bridges – like Circle CCTP, LayerZero, and Everclear, allowing direct movement of assets within enclaves. Each enclave may be configured with its own set of rebalancers, enabling flexible strategies per asset and chain.

### Provider Integration

The system supports integration with multiple execution providers, each with their own `Taker` and optional `Giver` contracts. These adapters implement strict on-chain validation flows, often relying on event proofs or deterministic conditions to ensure solvency and delivery guarantees. Currently, native support exists for direct asset transfers, 1inch Fusion+, and Across. Future integrations are planned for protocols like [Swaps.io](http://Swaps.io), Debridge, Squid, Mayan and others.

The system may also support universal, provider-agnostic collateral models, where solvers lock collateral once and access multiple taker routes across chains and providers.

### Liquidity Extensions

To improve capital efficiency and reduce idle funds, Flex Pools are designed to support advanced liquidity sources beyond static ERC-20 balances. Planned extensions include:

#### Yield-bearing asset support

Pools may accept deposits in wrapped or interest-generating tokens such as *aTokens* (AAVE), *cTokens* (Compound), *LST/LRT*, *ERC-4626* vault shares and others. These assets can be automatically unwrapped when used for `take` operations, allowing the pool to earn passive yield while maintaining on-chain availability.

#### Dynamic buffer management

A background allocator adjusts the ratio between yield-bearing tokens and native assets based on on-chain and off-chain signals (e.g., utilization, volatility, rebalance demand). This ensures that each enclave always holds an accessible buffer of base liquidity for immediate solver usage.

### Execution Coordination

In high-load or adversarial environments, coordinating access to shared liquidity becomes critical. Flex Pools are designed to optionally support external coordination layers that manage the timing and fairness of `take` and `give` operations.

#### Take Sequencer

An optional mechanism to queue or rate-limit `take` operations across solvers. This can help avoid race conditions, overlapping intents, or liquidity exhaustion in highly contested environments. It can operate off-chain and coordinate access based on fairness or solver priority rules.

#### Give Pre-Approver

A validation mechanism for inbound `give` operations ensures that returned assets match expectations and align with prior `take` activity. When combined with `take` coordination, it can help prevent liquidity shortfalls caused by competing solvers by maintaining an ordered queue of `give` and `take` operations based on actual availability.

### Multi-Token Support

A transition to a single pool per chain with multi-token support – replacing multiple isolated enclaves – is being considered for future implementation. This would enable more efficient liquidity management and unified accounting across assets with shared valuation logic, such as stablecoins.

## Risk Management

Flex Pools incorporate multiple mechanisms to reduce operational and protocol-level risks across chains and integrations:

### Event Validation and Finality Thresholds

All events are verified through the abstract `IEventVerifier` interface, which delegates proof checking to the underlying oracle. The finality threshold – the number of confirmations required before accepting a proof – should be configured at the oracle level, allowing flexibility per chain without modifying the verifier itself. This setting must balance fast solver execution with protection against chain reorgs.

Event verifiers provide common event verification logic, which is agnostic from taker implementation specifics. The verifier interface requires a taker to provide basic components of an expected event: *emitter contract* and *chain*, *event topics* and *data*, as well as a *proof* (usually forwarded from call params). Event verifiers can be upgraded, audited, or replaced independently, subject to governance via a DAO voting or multisig. All changes may include time delays or staging mechanisms to prevent sudden trust shifts and allow monitoring before activation.

### Liquidity Provider Scoping

In future versions, liquidity providers may define the set of takers or providers they trust when depositing into a pool. For example, a provider may choose to support only 1inch Fusion+, only [Swaps.io](http://Swaps.io), or both. This trust scope is enforced during `take` operations, ensuring that a provider’s capital is only used within approved execution flows.

### Liquidity Buffers and Withdraw Queue

To protect solvency, each enclave maintains a buffer of available liquidity. Withdrawals are placed into a queue when instant fulfillment is not possible. This mechanism ensures that solver operations and withdraw requests do not exhaust funds simultaneously.

### Emergency Controls

Core contracts include pausability features for emergency response. In case of unexpected behavior, security threats, or verifier failures, the protocol can:

- Pause take flows per enclave
- Disable specific takers or verifiers
- Temporarily restrict withdrawals

A dedicated emergency role may be authorized to execute critical pauses instantly, enabling rapid response to active threats or ongoing attacks.

### Fair Frontrunning-Resistant Rewards

The initial implementation is built on the ERC-4626 standard, which inherently carries a frontrunning issue – where large deposits can manipulate the share price to their advantage. To address this, our roadmap includes the introduction of a time-based reward distribution mechanism, based on insights from the 1inch team and their [farming contracts](https://github.com/1inch/farming) design.

This mechanism will ensure that rewards are allocated continuously and proportionally, based not only on the staked amount but also on the duration of each deposit. By incorporating time-weighted distribution, we aim to eliminate frontrunning incentives while preserving the core mechanics of ERC-4626.

## Fee Model

Each `take` operation incurs a fee calculated by the assigned tuner.

This fee can include:

- Protocol fee, directed to the pool as retained value
- Rebalance fee, if applicable. Used to incentivize rebalancers and maintain cross-chain liquidity balance
- Solver reward, if applicable.

The exact structure is defined by the tuner assigned to the taker and may be fixed, percentage-based, or dynamically calculated.

Liquidity providers earn returns through:

- Accumulation of protocol fees within the pool
- Optional yield from yield-bearing tokens or integrated LP positions
- Potential partner incentives from integrated protocols

As the pool grows and is used more actively, the value of LP shares increases, reflecting both base asset accumulation and system-level integrations.

## Ecosystem Growth

Flex Pools are designed as foundational infrastructure for the growing ecosystem of intent-based protocols, enabling scalable cross-chain execution with shared liquidity. The protocol is positioned to evolve along multiple strategic directions:

### Intent Protocol Integration

Flex Pools provide a universal liquidity infrastructure for different protocols like Fusion+, [Swaps.io](http://Swaps.io), Across, Squid and others. Any project can plug into the *give/take* model without managing its own inventory.

As user demand for intent-based execution grows across domains like swaps, bridging, and automation, more protocols emerge to support these flows, and more solvers enter the market seeking efficient access to capital. Flex Pools serve as a shared liquidity layer for this expanding ecosystem – the more protocols integrate, the more demand for solver liquidity rises – driving organic growth of the pools themselves as LPs respond to yield opportunities linked to real liquidity demand.

### Project Bootstrapping

Projects can deploy native Flex Pools to bootstrap cross-chain liquidity for their tokens, enabling seamless use across networks and protocols. These pools allow solvers to access project tokens for execution, supporting permissionless trading and automated rebalancing.

Flex Pools supports major standards – including *OFT* (LayerZero), *NTT* (Wormhole), *Warp* (Hyperlane), *CCT* (Chainlink), *ITS* (Axelar), *xERC20*, and more – enabling compatibility with external DeFi and bridge infrastructure.

This approach lets projects make their tokens natively available across chains, enabling seamless access and flexible exchange for users – without relying on centralized market makers or delayed bridging solutions.

### Partner Pools

Flex Pools can integrate with partner liquidity pools, which can offer users the option to auto-deposit their yield-bearing tokens into existing Flex Pools that support those assets, enabling additional yield from solver activity.

This creates a win-win dynamic:

- Flex Pools attract liquidity from partner ecosystems
- Partners enhance yield returns for their LPs
- Providers earn dual yield with minimal setup

### OpenIntents (ERC-7683) Support

Flex Pools are designed with forward compatibility for OpenIntents-based protocols via an abstract `IEventVerifier` that validates standardized `Open` events emitted as part of the OpenIntents specification. This design allows solvers to interact with Flex Pools across any OpenIntents-compliant protocol through a unified interface – simplifying integration, enabling shared liquidity access, and reducing the cost of supporting new protocols.

### Beyond EVM

Flex Pools are designed to operate on any network with a programmable VM. While initial deployments focus on EVM-compatible chains, expansion to high-performance environments like Solana is a priority.
