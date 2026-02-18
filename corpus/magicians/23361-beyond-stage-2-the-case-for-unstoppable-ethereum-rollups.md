---
source: magicians
topic_id: 23361
title: "Beyond Stage 2: The Case for Unstoppable Ethereum Rollups"
author: middlemarch
date: "2025-04-02"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/beyond-stage-2-the-case-for-unstoppable-ethereum-rollups/23361
views: 165
likes: 4
posts_count: 1
---

# Beyond Stage 2: The Case for Unstoppable Ethereum Rollups

*Note: I’m sharing this paper to discuss the limitations of the Stage 2 framework and the concept of Unstoppable Rollups. Any feedback is greatly appreciated!*

## Introduction

Ethereum rollups secure billions in user assets, yet nearly all of them can be shut down or censored by privileged actors. Many of these centralized controls are intended to be removed as rollups progress through the Ethereum community’s “[stages framework](https://medium.com/l2beat/introducing-stages-a-framework-to-evaluate-rollups-maturity-d290bb22befe).” However, even at **Stage 2**—the highest maturity level currently defined—rollups are still permitted to censor users or halt entirely. The only requirement is a 30‑day “exit window” before such changes take effect, theoretically allowing users to withdraw their assets in time.

While a 30-day exit window can provide meaningful protection, it is still a weaker safety guarantee than that provided by the Ethereum L1 itself, which cannot be stopped by any group, with or without notice.

How large is this gap in practice? Can Stage 2 rollups with exit windows justifiably claim they inherit the security of the L1? We will argue that exit windows are insufficient for creating L1-equivalent security as they are crippled by:

- Prohibitive exit costs
- Interaction with application‐level constraints on withdrawals
- A lack of trust‐minimized withdrawals for L2‐native assets

Addressing these issues demands a level of decentralization that goes beyond Stage 2—a design in which the chain cannot be forcibly halted or censored under any conditions. We call such a design the **Unstoppable Rollup**.

## The Problem With Exit Windows

We begin by examining whether a 30‑day exit window is effective at mitigating forced shutdown or censorship in the event of a hostile governance upgrade—an exploitative change to the rollup’s protocol rules by a privileged party.

Although no major rollup currently satisfies Stage 2 requirements (nor enforces a binding exit window), governance interventions are not uncommon. For example:

- In March 2024 Blast blocked three addresses from force-including transactions to prevent them from withdrawing stolen funds.
- In June 2024 Linea responded to a DEX hack by halting block production and censoring attacker accounts.
- In January 2025 Sonieum blocked trading of the potentially trademark-infringing memecoin $AIBO. This block occurred at the sequencer level and could be bypassed via forced inclusion, but Sonieum could have disabled forced inclusion as well (as Blast did)

How much protection will a 30-day exit window provide users if rollups decide to implement it?

### Withdrawing Bridged Assets

Consider first the cost of withdrawing bridged assets in a mass exit scenario. In a recent post, [Vitalik Buterin modeled such a scenario](https://vitalik.eth.limo/general/2025/02/14/l1scaling.html). Applying his assumptions, we arrive at the following cost model for exiting:

- Cost per asset withdrawal per user: $30 (assuming 120k L1 gas per withdrawal, 100 gwei L1 gas price, 36M L1 gas limit, and a $2,500 ETH price)
- Potential total cost to the community: $900 million (assuming 3M users, each holding 10 assets)

Even under ideal conditions, users collectively spend nearly a **billion dollars** to secure their assets. Meanwhile, an attacker pays only a small Ethereum transaction fee to initiate the hostile upgrade. This asymmetry enables two attack vectors:

- Pure Disruption: Force a shutdown with minimal cost.
- Governance “Tax”: Demand a fee lower than the user’s exit cost, effectively extorting them.

Increasing Ethereum’s gas limit might lower individual withdrawal costs, but does not solve the fundamental cost imbalance—especially given ongoing demand for L1 blockspace.

#### Contract Lockups: Timing Misalignments

A more fundamental problem facing the 30-day exit window’s effectiveness is that most assets aren’t sitting idle in user wallets but are actively deployed in smart contracts, some of which have their own withdrawal constraints. These contract-level restrictions create additional “withdrawal windows” that must align with the protocol’s exit window.![](https://docs-image-cacher.facet-8d2.workers.dev/https%3A%2F%2Flh7-rt.googleusercontent.com%2Fdocsz%2FAD_4nXfHjx1av3nWbu8OzO2e8ISeLj0wmdWh4QPaCXXz8hoc4olrGj7ZOLk0VLPwOefa2CTqWAU4FRbH588nuln9kPtRySeBi6VZPlJoAOHiP_WkPTU5J7JCG6EVWCmMDfmq_yP0vt1rQK8%3Fkey%3DS3Kfwhe-1JAQSSdiW-i5Tj9A)

Consider a vesting contract that releases tokens weekly. In a hostile governance upgrade, users must exit during the overlap of the 30-day exit window and their contract’s withdrawal schedule. With weekly vesting, the effective window might shrink to about 23 days; quarterly vesting could eliminate it entirely.

Perpetual futures illustrate a more challenging case. These derivatives have no expiration and rely on continuous margin checks and funding payments tied to real-time market conditions. Unlike halted vesting contracts perpetual markets cannot be fairly “paused and resumed,” because ownership of assets depends on real-time user actions and market fluctuations, neither of which can be accurately reconstructed retroactively.

Users must either avoid dynamic DeFi protocols—negating a core benefit of rollups—or attempt to **migrate entire DeFi states back to Ethereum L1** under time pressure. That migration is both costly and complex, involving addresses, contract state, and execution context changes.

### “Withdrawing” Native Assets

When you withdraw an L1-bridged asset from an L2, the L1 contract already holds that asset in escrow. The rollup provides trust-minimized proof of ownership, and the L1 can transfer the asset back to its rightful owner. This is an unambiguous “withdrawal.”

However, L2-native assets (assets minted on the L2) have no L1 equivalent escrowed. Even if the L2 supplies trust-minimized state data showing “Alice owns 100 tokens,” there’s no single “correct” way to represent those tokens on the L1. One natural approach is an “automatic ERC20 factory” like the [OptimismMintableERC20Factory](https://github.com/ethereum-optimism/optimism/blob/develop/packages/contracts-bedrock/src/universal/OptimismMintableERC20Factory.sol) that creates or mints a generic new L1 token whenever an L2 user tries to withdraw. This would preserve L2 token ownership information, provided there is social consensus on which of the possible L1 tokens is the “correct” L1 representation.

![](https://docs-image-cacher.facet-8d2.workers.dev/https%3A%2F%2Flh7-rt.googleusercontent.com%2Fdocsz%2FAD_4nXe833Z9ZdIluelqBJhJLM9GvAEnKVwW4fDup0tPozDITiTorud2NlSMns1ZqsK6aMVYbaCNfu8wqHZoAIBK4tOlFIZ9V1KjSPF5RgaETfr04-oYQQMXNqzNaHp-MQtcwTApjgOqc3o%3Fkey%3DS3Kfwhe-1JAQSSdiW-i5Tj9A)

However, a token’s value hinges on its behavior and internal logic, not merely the mapping of who owns how many tokens. Therefore, for a true L2-issued asset “withdrawal,” we need an L1 representation of its behavior in addition to its internal state.

#### Challenges Representing L2-Issued Assets on the L1

L2s have fundamentally different execution environments with unique chain IDs, block times, gas limits, and opcode behavior. These contextual differences, accessible to L2 contracts via opcodes or Solidity globals, make direct L1 replication impossible.

Another source of indeterminacy arises when an L2-issued asset’s internal state references specific L2 contract addresses. The same address on L1 might point to a blank account or an unrelated contract with different logic. If an L2 token internally references (for example) an L2 liquidity pool contract at address X, a naive attempt to “port” that balance to L1 could render those tokens unusable if X is a different contract (or a blank account) on the L1.

Another example is the [“address aliasing”](https://docs.optimism.io/stack/differences#address-aliasing) that rollup stacks like Optimism use to distinguish L1 contracts from L2 contracts in `msg.sender` and `tx.origin`. If an L2 token contract directly stores balances under these aliased addresses, simply copying them to L1 is problematic: the aliased addresses refer to accounts that either don’t exist or have different logic on L1. To resolve this, the aliased addresses would need to be “un-aliased” into valid L1 accounts—an operation requiring coordination and consensus.

Finally, there’s the practical issue of cost. Earlier, we estimated withdrawal costs per user, per asset. But lower L2 transaction fees encourage richer interactions and far more state than just asset balances. Migrating this larger state back to L1’s limited and expensive storage quickly becomes prohibitively costly, especially in a fixed time window.

##### Social Consensus & L2 Asset Dependencies

L2‐native tokens are often integrated into DeFi via:

- Collateral in Lending Protocols
- Wrapped Derivatives
- Liquidity Pairs with L1 Assets

Each integration adds another stakeholder whose agreement is required for any L1 token representation to be accepted. For example, a lending protocol cannot accept a new version of collateral without agreement from its borrowers and lenders.

The complexity introduced by these dependencies creates systemic risk. If stakeholders fail to reach consensus on a new L1 representation:

1. The L2 asset may become effectively worthless due to uncertainty about its canonical representation
2. This can trigger liquidations in protocols using it as collateral
3. Liquidations may impact other assets paired with or dependent on the L2 token
4. The effects can cascade through the broader DeFi ecosystem, potentially affecting even protocols with no direct exposure

A hostile governance upgrade provides an ideal trigger for such a cascade. As [Vitalik Buterin notes](https://vitalik.eth.limo/general/2025/02/14/l1scaling.html):

> If an L2 goes through a hostile governance upgrade, then an ERC20 launched on that L2 could start issuing an unlimited number of new tokens, and there would be no way to stop those tokens from leaking into the rest of the ecosystem.

#### Issuing Assets on L1: A Workaround?

Vitalik proposes issuing assets on L1 and bridging them to L2 to preserve a canonical withdrawal path, but this faces significant limitations. Many tokens have already been issued on L2s, and migrating them would require complex redeployment and user coordination. More fundamentally, even L1-issued assets become exposed to L2 governance risk the moment they interact with any L2-native component in DeFi protocols.

![](https://docs-image-cacher.facet-8d2.workers.dev/https%3A%2F%2Flh7-rt.googleusercontent.com%2Fdocsz%2FAD_4nXeTxfiy6jB6cN-FUZ2ScGFApIX7qEBJ1ujOmqwTba8U0E3ffOvWsLv8YIldWlDQAbQ_Q98GVZx2GXDHQ47zdLHtRzXYuzaOEvXdzhSkbvtjnhM-2yM5LYz_UOF14gUZbj-xzGt0G8c%3Fkey%3DS3Kfwhe-1JAQSSdiW-i5Tj9A)

#### L2-Native Asset Adoption

[Hayden Adams](https://x.com/haydenzadams/status/1890432415132217595), creator of the Uniswap protocol and Unichain rollup, said this in response to Vitalik’s suggestion:

> You can issue an asset on L2, and the L2 is still using L1 for [data availability] + execution proofs, and the asset can still be withdrawn to L1 if the L2 fails. Many / most assets should and will be issued on L2 bc it’s expensive to do on L1 and there are going to be many assets. Let’s not create the incorrect narrative that L2 native assets are bad for ethereum when they’re actually critical for ethereum to succeed on its current roadmap.

While we’ve shown that his claim about L2 assets being withdrawable to L1 holds only in limited cases, his broader point stands: economic forces will drive most new assets to launch directly on L2s, where deployment and transaction costs are dramatically lower.

## Beyond Exit Windows: Reconciling Rollup Promises with Practice

Exit windows impose substantial burdens on users. To protect themselves from hostile upgrades, users must:

- Monitor governance actions and be prepared to withdraw on short notice
- Accept losing assets whose withdrawal costs exceed their value
- Avoid contracts with time-locked assets that might restrict withdrawals
- Issue assets on L1, or accept heightened risks with L2-native assets

### The Marketing Gap

Rollups are marketed as providing L1-equivalent security guarantees. Vitalik Buterin consistently emphasizes this promise:

> If you have an asset inside the layer 2, you should be able to follow some procedure to unilaterally withdraw it, even if everyone else in the layer 2 system is trying to cheat you. (Oct 2020)

> The core of being a rollup is the unconditional security guarantee: you can get your assets out even if everyone else colludes against you. (Jan 2024)

> “inherits L1 security” is not just a hash link, it’s a claim that assets on the L2 are safe and can be withdrawn as long as the L1 is secure, even if 99% of the L2 nodes are malicious and colluding against you. (August 2024)

While technically accurate only for L1-bridged assets in EOAs, this nuance is probably lost on most readers. A typical user would reasonably assume all assets on a rollup—including L2-issued tokens and assets in smart contracts—share these unconditional guarantees.

This gap between rollup behavior and rollup marketing can be resolved in two ways:

1. Align marketing with reality: Instruct users to treat rollups as temporary “work zones,” where bridged assets can be manipulated and traded as long as they are ready to withdraw.
2. Align reality with marketing: Eliminate exit windows by making rollups unstoppable.

The first option is impractical—users have already embraced low-cost, general-purpose L2s and are unlikely to revert to a conservative “temporary usage” model.

This leaves Option 2. Enter Unstoppable Rollups.

## Introducing Unstoppable Rollups

### What Does “Unstoppable” Mean?

A rollup is *unstoppable* if no single actor or small group can forcibly halt or censor the chain. Concretely, an Unstoppable Rollup provides two guarantees:

1. Continuous and Uncensorable Transaction Inclusion: No one can indefinitely halt block production or selectively censor transactions. There must always be a fallback (forced inclusion) that cannot be disabled.
2. Gas Token Integrity: No one can disable or manipulate the rollup’s gas token, e.g., freezing issuance or inflating supply. Either scenario effectively blocks normal chain usage.

Under these conditions, users cannot be compelled to accept an upgrade that violates them. While all blockchains allow *voluntary* forks, being “unstoppable” means you can always stay on a fork that preserves block production and gas token integrity.

This stands in contrast to Stage 2, which **permits** forced upgrades that break these guarantees—so long as there’s a 30‐day exit window. An Unstoppable Rollup disallows such forced changes entirely.

Finally, all rollups depend on Ethereum L1 for security. If Ethereum itself halts or censors transactions, the rollup inherits that stoppage. Hence, “unstoppable” here means unstoppable **beyond** the baseline of Ethereum L1.

### 1. Continuous and Uncensorable Transaction Inclusion

To meet this guarantee, there must be a permanent mechanism for block production and forced inclusion that no admin can disable via configuration or upgrade. Today’s major rollups violate it:

- Admin‐controlled L1 Contracts: Centrally sequenced rollups often store the sequencer address in an upgradable L1 contract. Setting it to 0x0 (or otherwise disabling it) halts block production, unless users have a hard‐wired alternative. The Sonieum and Linea censorship cases described above were achieved through this mechanism.
- Forced‐Inclusion Upgrades: A forced‐inclusion mechanism might exist to circumvent a malicious sequencer, but if that mechanism is controlled by an upgradable contract, an attacker (or admin) can remove it. The Blast case described above relied on modifying forced inclusion functionality via contract upgrade.
- Decentralized/Based Sequencing: Even in a based-sequenced rollup in which anyone can propose blocks, an upgradeable L1 contract can still disable the acceptance of proposed blocks[1].
- Configuration Toggles: Another rollup design uses immutable contracts but leaves configuration fields that can effectively turn off block production. For example if there is an admin-controllable per-transaction gas limit on forced transactions an admin could set this value to 0[2].

A straightforward fix is to ensure the chain’s forced‐inclusion logic does not rely on an upgradable L1 contract. If no single party can modify the chain’s core path for transaction submission, then no one can halt or censor block production indefinitely.

### 2. Gas Token Integrity

Even if users can include transactions, they still must **buy gas**. If an admin can disable or corrupt the gas token, they can effectively halt the chain. Most rollups use *bridged Ether* as the gas token to mimic the familiar L1 experience. But a bridged ETH balance is only as secure as the L1 bridge contract. If that contract is upgradeable, an attacker or admin could:

- Disable issuance: Prevent new users from obtaining the gas token via the rollup protocol.
- Inflate selectively: Mint tokens for favored addresses, letting them monopolize blockspace.

Securing a gas‐token bridge is challenging because it must handle withdrawals—meaning it must track the rollup’s evolving protocol rules. If the bridge is immutable, there is no straightforward mechanism for  improvements and bug fixes. If the bridge is upgradeable, an admin can manipulate it.

An alternative is to use a *non‐bridged* gas token, i.e. a purely L2‐native token defined by the rollup’s protocol. This removes reliance on a deposit contract but requires users to learn a new asset for fees. It also means bridging ETH into that rollup is an application‐layer process, which must be secured separately.

Interestingly, the gas‐token bridge also acts as a coordination point—everyone must withdraw through the same contract that recognizes the “canonical” state root. Removing that single control point boosts censorship resistance but complicates how users coordinate around valid forks.

### Achieving Unstoppability

Ultimately, the vulnerabilities behind “stoppability” all trace back to **rollups’ reliance on L1 smart contracts** that can be upgraded (or reconfigured) at any time. Nodes running the rollup software can’t be upgraded forcibly, but if they must accept commands from an upgraded L1 contract, the effect is the same.

To make a rollup unstoppable, we must eliminate or drastically reduce the ability for privileged L1 contracts to alter sequencing or gas issuance.

There are three primary architectural approaches to eliminate these administrative control vectors:

1. Immutable L1 Contracts with User-Driven Migration: Use L1 contracts for bridging/sequencing but make them non‐upgradeable. When protocol upgrades are needed, deploy a new rollup with new immutable contracts. Users who want the upgraded logic must withdraw from the old rollup and redeposit into the new one. While inconvenient, the old rollup never forcibly shuts down.
2. Sovereign Rollups (No L1 Contracts for Core Logic): Eliminate reliance on L1 contracts entirely and define the rollup’s state transition function entirely off-chain. Sovereign rollups rely on social consensus for upgrades and handle bridging as an application-layer function without any privileged canonical bridge. Unstoppable sovereign rollups adopt a native gas token to remove dependence on an L1 bridge contract.
3. Native Rollups (Validation Integrated with Ethereum Protocol): Embed rollup validation logic directly into Ethereum’s consensus/protocol. Here, Ethereum’s social consensus governs upgrades via L1 hard forks—no single rollup admin has the power to force changes. This enables native rollups to use immutable L1 contracts without requiring users to withdraw and redeposit on protocol upgrades. Native rollups promise the most UX-friendly path to unstoppability, but require major Ethereum protocol modifications.

Each of these approaches removes the possibility of forced halts or censorship, satisfying the two unstoppable guarantees. We will explore these architectures in detail in a future paper.

## Conclusion

There is a significant difference between the protections afforded by a 30-day exit window and those afforded by an Unstoppable Rollup. At the same time, achieving unstoppability requires trade-offs whose costs might outweigh the benefits of these higher protections. For this reason, Unstoppable Rollups are not necessarily “better” for all users or use cases. However, for any scenario where unconditional censorship resistance, economic security, and absolute chain continuity are paramount—such as high-value DeFi applications or politically sensitive transactions—Unstoppable Rollups offer the strongest possible guarantees.

In upcoming work, we will delve deeper into immutable contract rollups, sovereign rollups, and native rollups, comparing their complexities, performance, and governance implications. Ultimately, our goal is to give the Ethereum community a practical roadmap toward truly unstoppable L2 systems, empowering users to choose the security model that fits their needs.

*Special thanks to [Norswap](https://x.com/norswap), [donnoh.eth](https://x.com/donnoh_eth), [Kev](https://x.com/kevaundray), [jesus.eth](http://jesusdoteth), [Ilia Shirobokov](https://x.com/ilia_shirobokov), [Max Gillett](https://twitter.com/maxgillett), [mteam.eth](https://x.com/mteamisloading) for feedback.*

**About the Author**

*Tom Lehman is the co-founder of [Facet](https://facet.org), an unstoppable sovereign rollup. He previously co-founded [Genius.com](http://Genius.com) where he served as CEO from 2009–2021.*

1. Taiko is an example of a based rollup whose inbox can be upgraded by admins. ↩︎
2. The unreleased Signet rollup displays this vulnerability to configuration-based stoppage. ↩︎
