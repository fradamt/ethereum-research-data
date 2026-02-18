---
source: ethresearch
topic_id: 22841
title: "The Signal: Ethereum - Casper FFG Finality Proofs"
author: Willem-ChainSafe
date: "2025-07-30"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/the-signal-ethereum-casper-ffg-finality-proofs/22841
views: 161
likes: 0
posts_count: 1
---

# The Signal: Ethereum - Casper FFG Finality Proofs

# The Signal: Ethereum - Casper FFG Finality Proofs

Thanks to a number of factors namely:

- EIP-7549[1] inclusion in the Electra hardfork
- Efficient precompiles for SHA256 hashing and BLS operations being added to the RISC Zero zkVM
- A huge reduction in zkVM proving costs

our team at Boundless has been able to realize what we have been gradually working toward for a number of years: [ZK proofs of beacon chain finality.](https://github.com/boundless-xyz/Signal-Ethereum)

As part of The Signal initiative the Boundless network will produce these proofs in step with the beacon chain as a public good to be consumed anywhere that can verify a RISC Zero proof (EVM, SVM, browser, etc.).

We anticipate that once fully mature this will have applications in bridging and light-clients, spanning the gap until Verkle trees and statelessness are fully implemented.

## Goal

The goal is to create zkVM program that, given a current view of the finalized state of the beacon chain and a number of attestations, can produce a proof of the form:

> I know attestations + witness such that
> Starting from finality state A
> There is a valid transition to finality state B

We term this program a finality client.

What seems like a straightforward problem hides a number of complexities when it comes to implementation. This article will gradually expand on these, share our proposed solutions, and show how we landed on our current design. It will also include the shortcomings of our current design and suggest improvements to be added in the future.

> ### Some notes on safety and liveness
>
>
>
> Since the goal of the finality client is not to be a consensus system in itself but to follow another system (the beacon chain) with restricted information, we define safety and liveness in a relative way.
>
>
> In this case ideal safety means that the finality client will never finalize a checkpoint unless it is finalized by the beacon chain.
>
>
> Ideal liveness means the finality client is able to finalize any checkpoint that the beacon chain finalizes (i.e. it is always able to follow the chain).

## Beacon chain finality state

Before continuing readers should familiarize themselves with the Gasper paper[[2]](#footnote-55606-2). In particular the concepts of checkpoints and supermajority links as these are the primary abstractions we will be working with.

In summary, a checkpoint becomes *justified* if there is a supermajority link targeting it from a source checkpoint that is already justified. A justified checkpoint then becomes *finalized* if a new supermajority link is accepted from that checkpoint to its direct child checkpoint in the very next epoch. This is the most common path to finality, often called “1-finality”.

The beacon state tracks several fields to manage this process. While it stores a `finalized_checkpoint` and a `current_justified_checkpoint`, it also includes a `previous_justified_checkpoint` and `justification_bits`. These additional fields are primarily used to enforce timing constraints on attestations and to enable the specific, simplified version of 2-finality that is implemented in the consensus specification.

```python
class BeaconState(Container):
    // ~snip~
    justification_bits: Bitvector[JUSTIFICATION_BITS_LENGTH]
    previous_justified_checkpoint: Checkpoint
    current_justified_checkpoint: Checkpoint
    finalized_checkpoint: Checkpoint
```

## Verifying attestations

For a link to be considered a supermajority link it must be attested to by a super-majority of the stake. Attestations in the beacon chain are BLS signatures over a link source and target (plus some other data) made by a staked validators.

To verify the attestations we require:

- The validator state as of the epoch the attestation occurs in. This includes:

public keys
- activation status
- slashed status
- effective balances

A way to compute the committee shuffling.

All of this data is contained within the beacon state and since our starting point contains a finalized checkpoint which commits to a beacon state, it is trivial to construct an SSZ Merkle multi-proof to read this data.

This is where we encounter our first major hurdle. Unlike a beacon node which is continuously following the chain, finalized or not, our program will only progress between finalized checkpoints and can only know and trust the state at the most recently finalized epoch.

To illustrate why this is a problem the below diagram shows where attestations typically fall in the chain for advancing the finality state.

[![image](https://ethresear.ch/uploads/default/optimized/3X/4/1/41e3591e717b3ac84be866a2cad41cf178515d22_2_690x221.jpeg)image2262×726 93.5 KB](https://ethresear.ch/uploads/default/41e3591e717b3ac84be866a2cad41cf178515d22)

The attestations for the link to advance the consensus state fall in blocks 2-3 epochs ahead of the trusted finalized epoch. We need to find a way to progress our trusted state forward to these epochs in such a way that a malicious prover cannot manipulate it to finalize an incorrect epoch even if they control a large fraction of the validators.

## State Lookahead

In the intermediate epochs between our trusted state and the attestations the following changes can occur in the beacon state

- New RANDAO values will be provided.
- Validators can enter/exit.
- Validator balance can change due to rewards/penalties/consolidations/hysteresis.
- Validators can be slashed.

This section will discuss how we account for the following changes in such a way to maintain safety relative to the beacon chain.

### RANDAO

New RANDAO is provided by block proposers in each epoch and aggregated into the state.

The RANDAO values for future epochs are required to compute committee shuffles. While a malicious prover could supply incorrect RANDAO values in the witness, this provides no advantage for attacking finality. An incorrect shuffle would simply cause the provided attestations to fail validation against the wrong committees. To succeed, the prover must supply the *correct* RANDAO values that correspond to the provided attestations. We therefore treat them as verifiable components of the witness.

### Validator Churn

It is important that entries/exits are accounted for otherwise the committee calculations for future epochs will be incorrect. This is also where a malicious prover could attack the finality client by exiting honest validators while activating new malicious validators.

Fortunately the beacon chain has a couple of features we can use to prevent these kinds of attacks.

#### Activations

Validators enter the active validator set by first making a deposit which triggers a sequence of events over the next number of epochs.

Fortunately, the beacon chain protocol provides a strong guarantee against malicious validator activations. For a validator to become active, the epoch in which it was added to the activation eligibility queue must first be finalized.

Since our finality client begins from a trusted state with a fixed finalized checkpoint, any validator not already in the activation pipeline cannot become active during the lookahead period. This means all activations can be precisely calculated from the trusted state, removing it as a source of unpredictable balance drift.

#### Exits

If we are looking ahead more than `MAX_SEED_LOOKAHEAD`, it is possible for a validator exit to be processed and take effect before the next checkpoint is finalized. Therefore, to ensure committee calculations are correct, this exit information must be provided to the zkVM program as part of the witness.

The protocol’s churn limit restricts the amount of stake that can exit in a single epoch. To prevent a malicious prover from supplying fraudulent exit data, the finality client strictly enforces this limit on the provided witness. This check guarantees that even if a malicious prover attempts to exit the maximum amount of honest stake, the impact on the total attesting balance is capped. Our formal safety analysis then accounts for this worst-case, bounded drift by increasing the required super-majority threshold, as detailed in the “Balance Drift” section.

Providing the correct exits as viewed by the beacon chain will result in the correct shuffling, allowing valid beacon chain attestations to be processed and a proof to be generated. This ensures the committee calculation remains secure and the finality proof is sound.

> Note that exits due to slashings are treated the same as voluntary exits by the beacon chain.

### Slashings

Once a validator is slashed their active balance is no longer counted toward the attesting balance, but it is counted toward the total active balance.

We currently read the slashed status out of the beacon state for current slashed-but-active validators but do not account for new slashings that occur. This is because a malicious prover may opt not to include them anyway as they have no effect on the shuffle.

If a slashing event does occur on the beacon chain that is large enough to prevent finality, this may result in a safety violation where the finality client finalizes a checkpoint the beacon chain has not. This happens if a supermajority is only reached by including the weight of these newly-slashed validators.

Due to our higher supermajority threshold of 85%, the scale of the slashing event required would be enormous — equivalent to around 20% of the total active stake. On the Ethereum mainnet today, this would mean validators with a combined value of several billion dollars would have to be slashed in order to trick the finality client.

Nevertheless, this is a recognized limitation and an area we are actively exploring for future improvements.

### Balance Drift

As mentioned prior validator active balances can change due to rewards, penalties, consolidations and hysteresis. We term all of this together *balance drift*.

Instead of accounting for all of these factors, which would require processing every block, we elected to account for the worst case balance drift per epoch and adjust the finality threshold accordingly.

In summary, we assume that the worst confluence of factors occurs that leads to a maximal decrease in honest validator balance and a maximal increase in dishonest validator balance. These are bounded thanks to the limits in rewards/penalties and the churn limit.

We derive a new safety margin on the finality threshold and require this threshold to be exceeded to reach a new finality state.

See the full analysis in the Signal Ethereum book[[3]](#footnote-55606-3). We propose a safe participation threshold of 85% with a maximum 10 epoch lookahead. This means that the chain can fail to finalize for ~7 epochs and the finality client can still follow.

These values can be traded-off with decrease in lookahead permitting a lower threshold.

## Atomic Finalization

An additional property we want from our finality client is that it will never need to roll back its state. That is to say that it will always be able to continue on from the result of any valid state transition provided the beacon chain also continues.

A direct implementation of the beacon chain consensus state transition rules does not result in a system with these properties.

We instead use what we call atomic finalization as the consensus state transition. This has a simplified consensus state of

```python
class ConsensusState:
    current_justified_checkpoint: Checkpoint
    finalized_checkpoint: Checkpoint
```

and it processes a chain of supermajority links, succeeding only if the final link in that chain fulfills the 1-epoch finality condition - that is, its source and target checkpoints are in sequential epochs.

See our full analysis of atomic finality and when this is compatible with Casper FFG[[4]](#footnote-55606-4). In summary this can follow the beacon chain provided only the 1-finality case occurs.

We may extend this to support the 2-finality case in the future if the need arises however this adds complexity to the state and to the protocol overall and rarely occurs in practice.

## Q&A

### What are the liveness guarantees?

We opted for the safety over liveness as we expect the main applications of The Signal will be bridges.

The finality client will experience a liveness failure if:

- The beacon chain experiences a period of non-finality greater than epoch_lookahead_limit - 3. This is configurable, but our analysis of balance drift suggested no more than 10 epochs
- Attestation participation drops below the safety threshold of 85%
- The beacon chain performs a 2-finality state transition. This is extremely rare and will only sometimes occur upon recovery from a period of non-finalizing

In each of these cases it will become impossible to build a state transition proof. Any bridge relying on these proofs would safely halt and require a restart from a new trusted finality state.

### What about accountable safety / economic finality?

The beacon chain is able to make the economic finality argument that if the chain ever finalizes two conflicting checkpoints then at least 1/3 of all staked Eth will be slashed.

This does not extend to finality client proofs in isolation. This is for two reasons:

- The attestations are hidden inputs to the ZKVM and so there are no guarantees about their availability. This means there are no guarantees they can be used to perform slashing.
- There are no synchrony guarantees between a finality client and the beacon chain. Meaning that the offending validators may have withdrawn. This is closely related to long-range attacks.

With these points in mind it is possible to create an instance of the finality client (a bridge contract for example) that performs additional checks on DA and synchrony and is able to make this argument.

This is outside the scope of this document but will be considered in the future.

### What are the proving costs?

A typical state transition for Ethereum mainnet at the time of writing (around slot 12143000) takes about 40 billion RISC Zero zkVM cycles to prove. Of this ~20% is SHA256 hashing and around 40% is BLS operations. This advances the finalized state by 1 epoch.

We expect to be able to reduce this as we move to focus on performance.

At the time of writing this cost ~$30 to prove, but this value will likely be out of date by the time of reading.

## Conclusion

We present a design for a zkVM based finality client for the Ethereum beacon chain. This is able to follow the beacon chain under typical operating conditions and will safely halt otherwise.

This can be proven in a zkVM for reasonable time/cost and this is expected to drop rapidly as we improve the program and the ZKVM itself.

1. EIP-7549: Move committee index outside Attestation ↩︎
2. [2003.03052] Combining GHOST and Casper ↩︎
3. Safety Analysis of Balance Drift - The Signal: Ethereum ↩︎
4. Formalization of the Consensus Algorithm - The Signal: Ethereum ↩︎
