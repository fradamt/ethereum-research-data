---
source: ethresearch
topic_id: 20591
title: Modeling Security for Cross Rollup Interoperability
author: shakeshack
date: "2024-10-08"
category: Layer 2
tags: []
url: https://ethresear.ch/t/modeling-security-for-cross-rollup-interoperability/20591
views: 777
likes: 5
posts_count: 1
---

# Modeling Security for Cross Rollup Interoperability

## Introduction

The goal of this post is to describe a mental model for the security of cross rollup interoperability (interop). To start, we’ll use [Sreeram’s model](https://x.com/sreeramkannan/status/1683735133835370499?s=20) for determining the security of a chain or in this case a rollup.

There are five properties that determine the security of a rollup:

1. Ledger growth. The ledger keeps growing.
2. Censorship resistance. New honest transactions are included if the ledger is growing.
3. Data availability. Ledger transaction data is published and not withheld from actors attempting to verify the network.
4. Re-org resistance. Confirmed transactions stay confirmed.
5. Validity. Only valid state transitions are accepted by the ledger.

The first two properties ensure the liveness of the chain while the latter three properties ensure safety. The combination of liveness and safety makes up the security of the chain.

[![](https://ethresear.ch/uploads/default/optimized/3X/3/6/36fd4ad601353c3ec708f7d5bc5a6298d9516a0b_2_433x333.png)1036×796 18.2 KB](https://ethresear.ch/uploads/default/36fd4ad601353c3ec708f7d5bc5a6298d9516a0b)

Based on this model for rollup security, we’ll attempt to derive a security model and set of security stages for cross rollup interop. There are three interop security properties that map to the five security properties of a rollup.

1. Validity. Only valid cross rollup transactions are accepted by connected rollups.
2. Local Ordering. Local or sequencer made guarantees that the ordering of cross rollup transactions will not change. This is the only ordering guarantee available until batch data is published to the L1.
3. Global Ordering (Data Availability). This represents a globally enforced ordering of the rollup. Ledger data containing cross rollup transactions are published to the L1 and not withheld from actors attempting to verify connected rollups.

The validity guarantee is the most commonly discussed security property and where the entire industry has been primarily investing their time. The reason local and global ordering are separated below is because local ordering accounts for both liveness properties and partially re-org resistance. The censorship resistance and liveness mechanism of a rollup is implementation and configuration specific which impacts local or sequencer made ordering guarantees potentially resulting in reorgs. Global ordering is the final security property where ordering is enforced by the L1 or Ethereum.

[![](https://ethresear.ch/uploads/default/optimized/3X/f/c/fca632e44efb9d3479e31e4bbcd0af9d07fc48ed_2_624x336.png)1436×774 21.6 KB](https://ethresear.ch/uploads/default/fca632e44efb9d3479e31e4bbcd0af9d07fc48ed)

These three interop security properties map to the three security stages for rollup interop protocols.

1. Stage 0. Validity guarantee.
2. Stage 1. Local ordering guarantee.
3. Stage 2. Global ordering guarantee.

In the interop space today, every existing interop protocol is still stuck at stage 0. Let’s explore how each of these interop security stages and properties apply to cross rollup interop. But first, we need to define the different interop models.

## Interoperability Models

There are a number of interop models used across rollups:

1. Point to point (e.g. Rollup Ecosystem Native, Layerzero, Hyperlane)

[![](https://ethresear.ch/uploads/default/optimized/3X/3/9/399b86d64698b96bb5abbde1277f30d595531280_2_467x149.png)1476×468 10.7 KB](https://ethresear.ch/uploads/default/399b86d64698b96bb5abbde1277f30d595531280)

1. Sovereign / L1 hub and spoke (e.g. Wormhole, Axelar)

[![](https://ethresear.ch/uploads/default/optimized/3X/b/2/b27f21123446d7259e48a08b596f8070a24efdf0_2_479x254.png)1534×820 16.5 KB](https://ethresear.ch/uploads/default/b27f21123446d7259e48a08b596f8070a24efdf0)

1. Rollup hub and spoke (e.g. Polymer)

[![](https://ethresear.ch/uploads/default/optimized/3X/7/2/72594b91f5dcb293652867051a3013ab4c059595_2_476x138.png)1464×428 11.8 KB](https://ethresear.ch/uploads/default/72594b91f5dcb293652867051a3013ab4c059595)

Each of these interop models come with different implications for the security and performance of an interop protocol. The rest of this post will visit each security property in the context of each of these interop models.

## Security Properties

### Validity

Let’s start with the most talked about security property. Validity in this context is defined as the valid execution of the state transition function (STF) of a rollup based on inputs from both the L1 and L2 transaction data. Strong validity guarantees improve the trust model after global ordering has been achieved.

The most secure (trust-minimized) verification methods are:

- Verifying a ZK validity proof of the counterparty L2 STF.
- Optimistically verifying fraud proofs within some challenge window.
- Verifying counterparty L2 settlement on the L1 against the latest L1 state it knows about.

Less secure verification methods are:

- Sequencer attestation.
- Reputationally secured third party attestation.
- Cryptoeconomically secured third party attestation.

Before global ordering has been achieved, stronger validity guarantees beyond that of a sequencer attestation do not improve the trust model as the sequencer retains control of ordering during that period.

To summarize, the L2 has the option of either directly verifying the validity of a counterparty L2 or indirectly verifying by waiting for the L1 to verify. For direct verification, very secure options leverage ZK validity or optimistic fraud proofs and other less secure options are secured by attestations. Next let’s look at validity in the context of what’s being used within each interop model.

#### Point to Point

Both LayerZero and Hyperlane predominantly use reputation based M of N muti-sigs for validity. In practice, this has been shown to be [small quorums starting ranging from 1/1 to 3/7](https://x.com/sandmanarc/status/1823898977668047303) in production today. Both [LayerZero](https://medium.com/layerzero-official/layerzero-x-eigenlayer-the-cryptoeconomic-dvn-framework-68af27ca2040) and [Hyperlane](https://docs.hyperlane.xyz/docs/protocol/economic-security/hyperlane-avs) are currently exploring adding crypto economic security to this model via EigenLayer.

Point to point protocols can support trust-minimized verification methods described earlier. However, this would greatly increase the total cost of these protocols as N^2 verifications are required for N connected chains and these more secure proofs are very expensive. For example, verifying raw storage proofs into the state of the L1 on an L2 to verify L2 settlement can be > 800k gas.

#### Sovereign Hub and Spoke

Wormhole also uses a reputation based M of N multi-sig but with a higher signer set. In production today, Wormhole runs [19 guardians](https://wormhole-foundation.github.io/wormhole-dashboard/#/?endpoint=Mainnet) and requires a supermajority of guardians to vote.

Axelar is its own L1 which can be thought of as an economically secured dynamic M of N multi-sig in terms of security. Axelar has [75 validators](https://axelarscan.io/) which use threshold signatures under the hood. However, the size of the threshold signing set varies depending on the connected chain. Axelar is currently exploring adding crypto economic security from other assets such as [BTC and ETH via Babylon and EigenLayer](https://www.axelar.network/blog/mobius-development-stack-launch).

Sovereign hub and spoke protocols cannot support trust-minimized verification of L2 settlement. They have to start by verifying Ethereum execution by either running full nodes or leveraging an [ethereum light client](https://prestwich.substack.com/p/altair) neither of which is trust minimized. Since doing so doesn’t improve the trust model, most sovereign hub and spoke protocols choose to verify L2 execution directly instead by running full nodes for connected rollups.

#### Rollup Hub and Spoke

Polymer hub supports a number of different verification modes that allow developers to tradeoff between security, cost and latency. As an L2, Polymer derives its blocks from L1 blocks allowing it to use L1 block information to prove the settlement of counterparty L2s. Proving partial settlement is possible as well such as proving a configurable fraud window over the full fraud window of an optimistic rollup. This approach is generally expensive with long latencies (hours - days) but is trust-minimized assuming the presence of fraud and/or validity proofs.

Polymer also supports faster verification modes such as [Lagrange State Committees](https://www.lagrange.dev/state-committees) which can run as fast as batch data publishing (mins). This is a crypto economically secured dynamic M of N multi-sig in terms of security. Lagrange allows for near unbounded growth in the size of the state committee while retaining constant verification costs via ZKPs. Unlike other multi-sig solutions, their attestations are chained together so you can trace both rollup state and committee history. They then recursively prove the full chain of attestations using ZKPs.

The fastest verification method uses sequencer signatures. This is a reputation based 1 of 1 multisig in terms of security. A sequencer attestation could be considered relatively more secure than the 1 of 1 third party attestations used in point to point protocols as many L2s operate their own sequencers and have significant reputational risks on the line. This method has the lowest latencies which can be almost as fast as the block time of the L2 (ms - secs).

### Local Ordering

Cross rollup ordering guarantees are the hardest security property to achieve and currently not being discussed at all. This is because ordering covers three fundamental security properties of a rollup - liveness, censorship resistance and re-org resistance.

Local ordering is guaranteed by the sequencer and deals with L2 blocks where batch data has not yet been posted to the L1. Stronger validity guarantees at this level of ordering do not improve the trust model as the sequencer defines final ordering posted to the L1. Sequencer guaranteed ordering has the lowest latencies but is extremely nuanced and highly implementation and configuration dependent. The following configuration and implementation details are relevant.

- Which L1 block is an L2 block built upon?

Communicating across L2 blocks requires those blocks to be created from the same history of Ethereum or L1.

What are the censorship resistance guarantees?

- In some designs, force transaction inclusion will trigger an L2 reorg.

What are the chain liveness guarantees?

- To inherit liveness from its L1, L2s generally trigger large reorgs to allow for block production via the L1.

An L2 block is created from both L1 and L2 inputs. Most L2s build blocks off of sub finality Ethereum L1 blocks which significantly affects the behavior of L2 ordering guarantees. Different L1 histories can have different L1 inputs resulting in an entirely different L2 chain. [![](https://ethresear.ch/uploads/default/optimized/3X/1/1/11ae81f1dad240d611c636465a8f47156caa431f_2_624x360.png)1600×924 131 KB](https://ethresear.ch/uploads/default/11ae81f1dad240d611c636465a8f47156caa431f)

The OP stack has a configuration option for SequencerConfDepth that sets the L1 depth upon which it reads L1 inputs. Arbitrum Nitro has a slow (delayed) inbox for L1 inputs which can be configured to read from a specific L1 depth (like the OP stack) or read from the “merged” or “finalized” head.

L2 blocks have a temporal relationship to each other based on how L2 block production is configured above. There is a past, present and future based on the L1 history. Like in any time travel movie, the past can leave messages for the future but the future cannot communicate with the past. From the past’s POV, the future has not happened yet and any number of futures are possible (e.g. sub-finality Ethereum forks).

[![](https://ethresear.ch/uploads/default/optimized/3X/4/4/446690dee876f398b2b47ae6df636ef6ffedcc80_2_624x227.png)1600×580 71.7 KB](https://ethresear.ch/uploads/default/446690dee876f398b2b47ae6df636ef6ffedcc80)

We also need to account for the censorship resistance mechanism and guarantees as it may trigger an L2 reorg. Here, the OP stack and Arbitrum Nitro differ significantly. The OP stack has better short term censorship resistance guarantees than Arbitrum Ntiro.

In the OP stack, forced included transactions can take the path of L1 deposits which are associated with a specific L1 block. These later get included as L1 inputs in the normal path of chain derivation. There is a MaxSequencerDrift configuration option which is generally set at around ~10 mins. This means that the L2 sequencer can censor L1 inputs for a maximum of 10 mins before it can no longer produce valid L2 blocks. No L2 reorgs are triggered in this process.

[![](https://ethresear.ch/uploads/default/optimized/3X/6/1/61b8d81eaea1288ee5597754740eea584dbff471_2_585x500.png)1430×1222 54.7 KB](https://ethresear.ch/uploads/default/61b8d81eaea1288ee5597754740eea584dbff471)

Arbitrum Nitro takes a different approach. There is a slow and a fast inbox on the L1. The slow inbox represents L1 inputs while the fast inbox represents L2 inputs. After a configurable delay period (24 hours in Arbitrum One), censored transactions in the slow inbox may be force included into the fast inbox. These force-included transactions generate their own sequencer batch which creates a new L2 block. This mechanism triggers a reorg of all L2 blocks that have not been posted to the L1 yet.

**[![](https://ethresear.ch/uploads/default/optimized/3X/7/0/70e748673f74e3a56543c1f0696f3ccbf7f5a393_2_608x500.png)1400×1152 58.5 KB](https://ethresear.ch/uploads/default/70e748673f74e3a56543c1f0696f3ccbf7f5a393)**

Liveness is the last property we need to cover. In order to inherit liveness from its L1, L2s must have a mechanism for which blocks can be produced solely based on L1 inputs. The liveness guarantees in Arbitrum Nitro and the OP stack result in similar guarantees depending on configuration but are functionally different.

In the OP stack, there is a SequencerWindowSize config option that specifies the upper time bound for batch data submission. This is generally configured to be 12 hours. If the L2 sequencer is down or unable to submit batch data for 12 hours, all L2 blocks in that range become deposit-only blocks. This allows for block production to occur solely from L1 inputs resulting in a 12 hour liveness guarantee. If the L2 sequencer is not down, this can cause a large 12 hour reorg on the L2.

[![](https://ethresear.ch/uploads/default/optimized/3X/a/8/a83759ce546561e816a8ab74a447293c01c52886_2_624x317.png)1438×730 35.1 KB](https://ethresear.ch/uploads/default/a83759ce546561e816a8ab74a447293c01c52886)

Arbitrum Ntiro inherits liveness from the L1 using its force transaction inclusion mechanism. If the Nitro sequencer is down for longer than the delay period (24 hours in Arbitrum One), any user can trigger L2 block production by force including transactions from the slow inbox into the fast inbox. If the L2 sequencer is not down, this can cause a large 24 hour reorg on the L2. Refer to Nitro’s force transaction inclusion diagram above for how this works.

**[![](https://ethresear.ch/uploads/default/optimized/3X/1/5/1511e455c080c38113b506dc98565a175bce589a_2_624x339.png)1376×748 77.3 KB](https://ethresear.ch/uploads/default/1511e455c080c38113b506dc98565a175bce589a)**

With all of this background context covered, we can move on to how local ordering guarantees are managed today within various interop models.

#### Point to Point

LayerZero allows builders to [configure the number of L2 block confirmations](https://docs.layerzero.network/v2/developers/evm/protocol-gas-settings/default-config#setting-receive-config) to wait before relaying a message. Hyperlane has some arbitrary and [unsafe defaults](https://docs.hyperlane.xyz/docs/guides/latencies) for the number of L2 confirmations which can be made configurable if you create your own deployment. Both approaches ignore local ordering considerations completely and places reorg risk solely on the application builder to handle. These protocols are unaware of the chain liveness and censorship resistance mechanisms of connected L2s which carry the greatest risk to application builders as these can trigger extremely large reorgs.

#### Sovereign Hub and Spoke

Wormhole supports low latency messaging via an[“instant” configuration or consistency level](https://wormhole.com/docs/build/reference/consistency-levels/) using their terminology. Like the point to point protocols above, this approach does not account for any local ordering considerations explained earlier. This can expose apps to both small and large reorgs. Axelar does not support low latency messaging.

#### Rollup Hub and Spoke

Polymer is the only interop protocol that accounts for all aspects of L2 ordering guarantees at low latencies. To solve this problem, Polymer builds a dependency graph of cross rollup transactions sub Ethereum finality. This dependency graph is then committed or reverted based on the L1 history that gets finalized. The diagram below visualizes this dependency graph across three L2s that are all building off the same L1 history in L1’.

[![](https://ethresear.ch/uploads/default/optimized/3X/1/6/1612d137a3ee7995fcad56cd711578c184ee423f_2_624x400.png)1600×1026 229 KB](https://ethresear.ch/uploads/default/1612d137a3ee7995fcad56cd711578c184ee423f)

Polymer names this approach “cross rollup contingent transactions” which is somewhat similar to Prestwich’s proposal of [cross rollup contingent blocks](https://prestwich.substack.com/p/contingency). Polymer’s approach is lighter weight and does not require rollup level opt-in. The dependency graph only spans a subset of transactions across blocks. Polymer is building additional mechanisms in place to cover both the chain liveness and censorship resistance mechanisms for Arbitrum Nitro and the OP stack. This protects application builders from extremely large reorgs.

### Global Ordering (DA)

Global ordering is established when data availability (DA) is published to the L1. DA is the reliable broadcast of L2 batch data that is required for the prevention of data withholding attacks. For rollups, the availability of batch data is required for a third party to either generate a fraud proof in an optimistic rollup or a ZK proof of validity in a ZK rollup. Stronger validity guarantees at this level of ordering do improve the trust model as there’s already a global source of truth (Ethereum) for ordering.

We’ll define global ordering here as a guarantee made by the L1 that the order of the transactions within an L2 block stay in that order without being reorged. There are two levels of global ordering guarantees. The “merged” level is true as long as the L1 does not reorg while the “finalized” level is true in perpetuity.

- Merged → An L2 block where batch data has been posted to the L1.
- Finalized → An L2 block where batch data on the L1 has finalized.

To ensure that global ordering has been achieved, we need to check for DA published on the L1 which varies depending on the DA layer that the rollup uses. This can be any of the following:

- Calldata on Ethereum
- Blobs on Ethereum
- Alt-DA (e.g. EigenDA, Celestia)

Proving calldata inclusion in an execution header would require

- Proving that batch publishing transaction in the transaction root
- Comparing RLP encoded transaction data against the transaction hash committed to within the root
- Unpacking the batch data (this is rollup specific) to derive information around which L2 block(s) were posted

Proving blob inclusion in an execution header would require

- Proving that blob publishing transaction in the transaction root
- Proving the blob against the relevant blob versioned hash
- Unpacking the blob data (this is rollup specific) to derive information around which L2 block(s) were posted

Proving batch inclusion in an alt-DA layer would require

- Proving batch data against the DA commitment (e.g. Merkle root or KZG commitment)
- Unpacking the batch data (this is rollup specific) to derive information around which L2 block(s) were posted

DA checks are also useful in securing some of the more nuanced ordering properties such as chain liveness. Delayed or halted DA publishing can result in large reorgs of 12-24 hours or more depending on rollup configuration. For example, the degen chain reorg occurred due to its [inability to publish batch data](https://x.com/0xCygaar/status/1793056013446226200).

#### Point to Point

LayerZero and Hyperlane can be configured to wait for a sufficiently large number of L2 confirmations but do not actually check for DA. Hyperlane requires a custom deployment to configure the number of confirmations. Since DA is not checked, global ordering is not 100% guaranteed exposing apps to potential large reorgs as mentioned above.

Performing DA checks on-chain would add significant costs to their protocols as both verification and the proof data associated would need to be published to connected L2s. The proving logic described above is quite involved.

#### Sovereign Hub and Spoke

Wormhole can be [configured to work off a “safe” or “finalized” consistency level](https://wormhole.com/docs/build/reference/consistency-levels/) which should correspond to when batch data is published to the L1 and when that data is finalized. Axelar waits an [arbitrarily long number of L2 confirmations](https://docs.axelar.dev/learn/txduration/) before relaying a message. Setting a fixed number of L2 confirmations to wait works in the happy path but does not cover for the unhappy path where batch submission is delayed or halted.

#### Rollup Hub and Spoke

Polymer supports verification modes that check for when batch data is published to the L1 as well as when that batch data is finalized. This accounts for edge cases where batch submission is delayed or halted protecting apps from large reorgs.

The cross rollup contingent transaction protocol also applies here during the “merged” phase of global ordering. This is when DA has been published to the L1 but that L1 block has not yet been finalized.

## Conclusion

Existing interop protocols are all stuck at stage 0 or only providing validity guarantees today. We would like to see efforts made to advance the security of interop protocols to stage 1 and 2 to provide both local and global ordering guarantees. This would effectively make interop protocols respect safety critical implementation details of rollups such as how they inherit censorship resistance and liveness from the L1 or Ethereum.
