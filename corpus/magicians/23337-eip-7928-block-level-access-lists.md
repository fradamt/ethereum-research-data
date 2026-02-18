---
source: magicians
topic_id: 23337
title: "EIP-7928: Block-Level Access Lists"
author: Nerolation
date: "2025-04-01"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7928-block-level-access-lists/23337
views: 1459
likes: 18
posts_count: 35
---

# EIP-7928: Block-Level Access Lists

The EIP:


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7928)





###



Enforced block access lists with state locations and post-transaction state diffs










Discussion topic for EIP-7928: https://github.com/ethereum/EIPs/pull/9580

#### Update Log

- 2025-04-01: Initial Commit
- 2025-04-22: Discord Channel
- 2025-04-23: Design Space Exploration
- 2025-05-26: execution-specs implementation (draft)
- 2025-08-12: see Linktree for further updates

#### External Reviews

TBD

#### Outstanding Issues

TBD

## Replies

**dajuguan** (2025-04-17):

We ran some initial benchmarks using a block-level access list (providing only account addresses and storage keys, without balance diffs or post-execution write values) on Geth. After introducing BAL, Geth’s live sync performance improved by approximately 30%.

---

**wjmelements** (2025-04-24):

I wish the Specification wasn’t entirely code.

> The BAL MUST be complete and accurate. It MUST NOT contain too few entries (missing accesses) or too many entries (spurious accesses).

The access list *should* be complete, ~~but this may be impossible because of `PREVRANDAO`~~.

I like this spec a lot. It should also deprecate transaction-level access lists and remove the warm/cold distinction.

---

**jochem-brouwer** (2025-04-24):

Is the code used for this experiment available somewhere? Would love to see it!

---

**jochem-brouwer** (2025-04-24):

Why “The access list *should* be complete”? Why not “The access list **must** be complete”?

The BAL should be generated during block building. The verifier should then re-run the block and then verify that the BAL is complete (nothing misses, and there is nothing added which is not accessed).

Note that the contents of the BAL do not influence execution paths, so the EVM execution itself has no knowledge of the BAL. This is possible with tx-level access lists and in particular the divergence in gas costs if a slot/address is warm or cold, which could yield situations where it is impossible to generate a complete access list (which is also why `eth_createAccessList` has a retry-limit, because otherwise you could find yourself in an infinite loop ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12) )

---

**wjmelements** (2025-04-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> Why “The access list should be complete”? Why not “The access list must be complete”?

I thought *must* was impossible because I misremembered `PREVRANDAO`. It’s less random (and useful) than I remembered.

---

**dajuguan** (2025-04-26):

yeah, we will publish a full post on the code, core ideas and basic benchmarks next week

---

**Nerolation** (2025-05-26):

Great question, and still very much open for discussion.

If we introduce Block Access Lists (BAL), then transaction-level access lists could be deprecated, as they’d no longer be necessary. In that case, we could reduce storage access costs to match the current discounted rate provided by access lists (1900 + 100 gas), and compensate by raising the gas limit to make transactions cheaper overall.

Another idea worth exploring is using BAL to enable fairer cost distribution for block-level warming. Instead of a naive “first access warms for the whole block” approach, or doing post-execution cost accounting to distribute warming costs, we could restructure execution like this:

1. Check the BAL.
2. Determine all storage accesses in the block.
3. Pre-split the warming cost among all accesses.
4. Then start executing txs and use the costs determined in (3).

This would eventually let us adopt block-level warming to lower transaction costs, without relying on the “first access pays for everyone” model, which is arguably unfair.

---

**jwasinger** (2025-06-02):

SSZ unions are not present in the existing eth specs, and AFAICT they are not supported by production-grade SSZ implementations.  I’ve opened a PR to remove the use of union for account code from this spec in favor of using a list of bytes:  [Update EIP-7928: convert contract code field from union type to list of bytes by jwasinger · Pull Request #9848 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9848)

---

**jwasinger** (2025-06-04):

Also, it feels like we should separate out code into it’s own lookup keyed by hash, and reference it elsewhere in the BAL via the hash.  This way we are deduplicating things as much as possible.

---

**Nerolation** (2025-06-04):

I merged the SSZ Union fix and for the code, you’re right yeah. I havr an open PR with some changes that I’m going to merge today.

---

**raul** (2025-06-04):

I’m concerned about the size and verbosity of the BAL. At 40KiB, this represents a non-negligible overhead that causes block sizes to increase by 2x, and p95 grows by 1.55x (below is a chart showing mainnet stats over the last). This creates an opportunity cost, as the additional bandwidth could alternatively be used to increase gas limits.

### Proposed exploration: Deterministic execution plans

I propose exploring whether we can replace the diff traces in blocks (the BAL itself as defined today) with a deterministic, canonical, parallelizable tx execution plan calculated by the proposer based on traces generated during sequential execution.

Instead of embedding complete differential traces in blocks, we would include a double-nested list containing positional references to txs: `[[txidx1, txidx2, …], [txid3], […], …]`. This structure can be accompanied by a version identifier to enable logic updates over time.

This approach can be regarded as extremely efficient compression, by enshrining a version of the parallelism heuristics within the protocol (which also reduces the risk of state mismatches between clients due to disparate logic, if this was left up to implementations).

Under this model, we could offload the full BAL from the block, while maintaining a commitment to it for verifiability. The BAL paylaod could propagate through a separate, less critical network path, while light clients could still request it when needed to update their local state, preserving the related EIP’s benefits.

Validators would execute transactions following the specified execution plan while detecting data races or conflicts (this detection mechanism requires further research, but a priori it appears feasible). If a conflict is detected, the validator would immediately reject the block. If validators additionally generate differential traces, they could sequentialize them and verify against the commitment.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/1/1d50f5031b81a86df97ee8a4846ac7f53df463b5_2_600x500.jpeg)image1920×1598 191 KB](https://ethereum-magicians.org/uploads/default/1d50f5031b81a86df97ee8a4846ac7f53df463b5)

---

**aelowsson** (2025-06-04):

To the extent that BALs are designed to facilitate parallel execution and that the associated block size increase is a concern, we can improve the average case significantly by simply ignoring txs that do not have any dependencies? A valid BAL would then cover all txs in the block with dependencies, and all other txs would be ignored. Each client are to use this information as efficiently as possible for the specific machine they run on.

The recent proposal by [@raul](/u/raul) is also interesting, but I worry about the fact that it does not help to break up dependency chains, thus not facilitating parallel execution in the worst case. The idea from [@raul](/u/raul) of propagating the BAL through a separate channel can however still be used if deemed desirable. But in the proposal of the previous paragraph, a BAL consisting only of txs without dependencies can be propagated there (these were left out in the block).

---

**aelowsson** (2025-06-04):

In your approach, would it be reasonable to break up tx dependency chains consuming more than $X$ gas? So there can be (potentially, in some blocks) a BAL for specific txs, for breaking long dependency chains, thus facilitating “sufficient” parallel execution in the worst case.

---

**Nerolation** (2025-06-05):

I agree, the overhead of the current BAL design is definitely non-negligible, and we need to carefully weigh the trade-offs.

Your proposal is interesting. It would certainly reduce the data footprint needed for parallel execution. However, compared to the current BAL format (which includes full state diffs), it lacks a key feature: executionless state updates. With full diffs, we can not only parallelize transaction execution, but also decouple execution from state root computation, something we’d lose with the proposed execution plan format.

Another implication is that without state diffs, we can no longer use this data for purposes like syncing, as a replacement for the healing phase, for [block-level warming](https://ethresear.ch/t/block-level-warming/21452), or for [FOCIL](https://eips.ethereum.org/EIPS/eip-7805), that rely on running post-execution checks, which become impossible if we move to a system where post-execution reasoning is replaced by pre-execution plans. (imagine having something like `apply_bal(pre_state, bal) -> post_state`.

So while your approach is kinda elegant and reduces data overhead, I’m not sure that *only* improving parallel execution is worth losing these capabilities, especially given that we’d still rely on nondeterministic state prefetching from disk. That said, if execution parallelism turns out to be the primary bottleneck, this is definitely the best idea I’ve seen so far. I also appreciate the simplicity of the data structure.

I also agree with [@aelowsson](/u/aelowsson)’s point: this helps with average-case blocks, [which often have minimal dependencies](https://dependency.pics/) and are naturally well parallelizable. But it won’t help in the worst-case scenario, like when we have 10 large, interdependent transactions consuming all available gas.

[@jochem-brouwer](/u/jochem-brouwer) has been thinking about using inter-transaction state diffs to improve parallelism in those cases, but for now it looks like the next fork (Fusaka) will introduce a [gas limit cap per transaction (EIP-7825)](https://eips.ethereum.org/EIPS/eip-7825) to enforce a minimum degree of parallelism directly at the protocol level, which I think is a reasonable change.

---

**raul** (2025-06-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aelowsson/48/14632_2.png) aelowsson:

> it does not help to break up dependency chains, thus not facilitating parallel execution in the worst case.

Would you mind elaborating on this? What’s specifically meant by “dependency chains”, and what’s the worst case scenario in this case?

The assumption of the original BAL proposal is that by providing the state diffs inline, the validator can calculate data/state dependencies between txs, and figure out a parallelizable execution plan subjectively.

My proposal should be, in principle, in no way inferior to expressing the BALs inline (for the purposes of parallelization). It just moves the calculation of the dependencies to the builder/proposer by applying some canonical logic to the same traces, so we can save the bandwidth required by transferring the full BAL inline in the block (and offload it to a secondary channel).

Note that it’s still possible to statically validate that the execution plan is coherent with the transaction order, e.g.

- you can validate that txs from the same sender preserve nonce order
- you can validate that txs from non-existent EOA are not happening in the first parallel block
- and more

---

**raul** (2025-06-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> But it won’t help in the worst-case scenario, like when we have 10 large, interdependent transactions consuming all available gas.

Would you mind explaining how the original BAL proposal addresses the challenges of the worst-case scenario (for parallelization purposes), and why it outperforms in that case?

---

**Nerolation** (2025-06-05):

The current proposal allows transactions to be executed in any order. In theory, clients could even process a block from bottom to top without worrying that earlier transactions might affect the state relied on by later ones. This is possible thanks to the inclusion of post-transaction state diffs - which capture changes to storage, nonce, balance, and code - on a per-transaction basis.

As a result, even if a block contains transactions that depend on one another in sequence, we can achieve the same level of parallelization as if all transactions were completely independent.

---

**misilva73** (2025-07-08):

Now that there have been a few changes to the BAL design, we performed a new back-of-the-envelope calculation to estimate an upper bound on the size of Block-level Access Lists (BALs). We consider specific scenarios for each component of the BAL and compute the sizes under various block limits. The following table summarizes the BAL sizes in MiB:

|  | 36M | 45M | 60M | 100M |
| --- | --- | --- | --- | --- |
| Storage changes |  |  |  |  |
| Multiple SSTORE to same account | 0.44 | 0.55 | 0.73 | 1.22 |
| Single SSTORE to multiple accounts | 0.38 | 0.47 | 0.63 | 1.05 |
| Multiple SSTORE to same account w/ gas refunds | 0.26 | 0.33 | 0.44 | 0.73 |
| Multiple SSTORE to same account w/ EIP-2930 | 0.45 | 0.56 | 0.75 | 1.25 |
| Storage reads |  |  |  |  |
| Multiple SLOAD to same account | 0.52 | 0.65 | 0.87 | 1.45 |
| Single SLOAD to multiple accounts | 0.38 | 0.47 | 0.63 | 1.05 |
| Multiple SLOAD to same account w/ EIP-2930 | 0.55 | 0.69 | 0.92 | 1.53 |
| Balance changes |  |  |  |  |
| Send multiple transfers w/ CALL | 0.12 | 0.15 | 0.20 | 0.33 |
| Send multiple transfers  w/ SELFDESTRUCT | 0.22 | 0.27 | 0.37 | 0.61 |
| Nonce & Code changes |  |  |  |  |
| Deploy multiple contracts | 0.16 | 0.21 | 0.28 | 0.47 |

With the current pricing, storage reads are the operations that lead to the worst-case BAL size. At the current gas limit of 36 million units, this worst-case BAL has an uncompressed size of 0.55 MiB. For comparison, we can construct a theoretical worst block using a combination of call data and the [EIP-2930](https://eips.ethereum.org/EIPS/eip-2930) access list, which results in a block size of 1.95 MiB. We should note, however, that since the worst-case BAL also uses an access list, this list will occupy space in the block payload. As there is a significant amount of repetition between the access list and the BAL, Snappy should be able to compress this. However, we should test how much we gain from this compression.

The full description and derivation of each scenario can be read [here](https://notes.ethereum.org/@misilva/r1CyZf_Vlx).

---

**etan-status** (2025-07-09):

Would recommend EIP-7916 ProgressiveList / EIP-7495 ProgressiveContainer so that it remains nice across forks that may introduce new kind of access lists.

---

**peersky** (2025-08-10):

If seems could be quite useful from security monitoring standpoint, as we can easier access state changes and do block-level assessments;

Would it make sense to have 7702 delegation designation traced there as well?


*(14 more replies not shown)*
