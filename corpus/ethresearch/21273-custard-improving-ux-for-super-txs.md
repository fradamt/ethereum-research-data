---
source: ethresearch
topic_id: 21273
title: Custard - Improving UX for Super TXs
author: jvranek
date: "2024-12-13"
category: Layer 2
tags: [based-sequencing]
url: https://ethresear.ch/t/custard-improving-ux-for-super-txs/21273
views: 345
likes: 9
posts_count: 1
---

# Custard - Improving UX for Super TXs

*Joint work with [Kubi](https://twitter.com/kubimensah). Thanks to [Drew](https://x.com/DrewVdW), [Justin](https://x.com/drakefjustin), [Ladislaus](https://x.com/lvdaniels), [Conor](https://x.com/ConorMcMenamin9), [Lin](https://x.com/linoscope) for their review and feedback. Feedback is not necessarily an endorsement.*

Custard ![:custard:](https://ethresear.ch/images/emoji/facebook_messenger/custard.png?v=14) (**C**onstraining **U**ser **S**tate **T**o **A**void **R**eneging **D**ownstream) is a technique for enabling atomically composable super transactions on based rollups through careful state management. The key insight is that by constraining specific parts of L1 state that a super transaction depends on, we can enable validators to safely issue L1 execution preconfirmations ahead-of-time without requiring control over the whole L1 block. This reduces the validator coordination needed to bootstrap preconf protocols and allows based rollups to offer super transactions sooner with fewer participating validators. This post explores three ways to implement Custard: through EIP-7702, smart contracts, and exclusion preconfirmations.

### Why does this matter?

A primary benefit of based sequencing is that it enables synchrony and atomicity between the L1 and based rollups (BRU). This means operations on both layers can be combined into what we call a “super transaction” - a bundle of transactions that works across both layers as if they were one.

### A Real-World Example

Let’s consider a practical example: L1→L2→L1 arbitrage. Imagine Alice wants to atomically:

1. Move her tokens from L1 to a BRU
2. Make a trade on the BRU
3. Move her tokens and profit back to L1

Currently, these would be separate steps with delays between them (e.g., normally 7 days between steps 2-3 for optimistic rollups). Applying *Custard*, Alice can bundle all of these actions into one super transaction that completes within a single Ethereum block.

To make super transactions widely adoptable, we need to address three key challenges:

1. Real-Time Proving: We need a way to settle the BRU’s state quickly enough to withdraw within a single L1 block
2. Guaranteeing Atomicity: We need mechanisms to ensure either all parts of the super transaction complete successfully or none of them happen
3. Validator Availability: We need sufficient validator participation to make super transactions reliably available for users

The rest of this post examines each of these challenges and existing approaches to solving them, before introducing *Custard* as a way to bring them together.

### Challenge #1: Real-Time Proving

**Traditional Approach and Its Limitations**

Until now, it was commonly believed that (trustless) instant withdrawals from rollups required “real-time proving” - essentially, the rollup’s state must first be settled via validity proof. For Alice’s super transaction to complete in one L1 block (12 seconds), the validity proof would need to be generated even faster. However, the technology to generate these proofs so quickly (real-time SNARKs) isn’t deployed in the market yet but there many amazing efforts in progress (![:soon_arrow:](https://ethresear.ch/images/emoji/facebook_messenger/soon_arrow.png?v=14)).

**Current Workarounds**

Some projects ([UniFi](https://x.com/puffer_unifi), [Gwyneth](https://x.com/gwyneth_taiko), [T1](https://x.com/t1protocol)) have turned to Trusted Execution Environments (TEEs) as an alternative to SNARKs for proving the rollup’s state transition function. While TEEs can generate proofs much faster than SNARKs, making real-time proving possible, they come with a significant drawback: they require trusting the hardware manufacturer and prover. This additional trust assumption introduces new risks to based rollups that traditional SNARK-based systems don’t have.

**A New Solution: The Solver Approach**

[Nethermind recently proposed](https://ethresear.ch/t/fast-and-slow-l2-l1-withdrawals/21161) a solution that achieves the UX of instant withdrawals without needing real-time proving. Their approach:

- Uses solvers to immediately provide users withdrawal liquidity on the L1 before the BRU state is settled
- Maintains atomicity (solvers and BRU bridge are protected from reorgs)
- Maintains trustlessness (no need to trust the solver or TEEs)
- Provides a practical path forward while we wait for real-time proving technology to mature (at the cost of capital efficiency)

### Challenge #2: Guaranteeing Atomicity

For Alice’s super transaction to work seamlessly, we need to ensure that either all sub-transactions complete successfully or none of them happen at all. This is where *execution preconfirmations* (EPs) come in.

**The Role of Execution Preconfs**

To guarantee the super transaction’s success, we need Ethereum validators to provide four specific guarantees:

1. L1 Deposit Guarantee: Confirms Alice’s funds will successfully move from L1 → BRU
2. L2 Swap Guarantee: Ensures Alice’s trade on the rollup will execute as expected
3. L2 Withdrawal Guarantee: Confirms Alice’s request to move funds back from BRU → L1 will be processed
4. L1 Solver Guarantee: Ensures a solver transfers Alice funds on the L1

**Why Ethereum Validators Matter**

A crucial insight is that these guarantees must come from Ethereum validators themselves. They are uniquely positioned to make these guarantees because they can be proposers for both layers:

- On Ethereum, they have a write-lock over the L1 since they have sole authority to propose the next block
- On the BRU, they can be configured to be the only ones with permission to sequence transactions during their slot

This dual write-lock is what makes based sequencing special - only Ethereum validators can credibly commit that a super transaction will execute exactly as planned. [Based preconfs](https://ethresear.ch/t/based-preconfirmations/17353) are the mechanism through which validators make these promises binding - by staking capital, validators become preconfers and face economic penalties if they fail to honor their commitments.

### Challenge #3: Validator Availability

**L1 EP constraints**

A critical limitation of L1 EPs is their “just-in-time” nature. Validators can only safely issue these L1 EPs when they’re the current block proposer. Why? Because a future validator doesn’t have a write-lock on the L1 and earlier validators could change L1 state in ways that break their L1 EPs.

This is different from L2 EPs on the rollup, where validators can safely make commitments “ahead-of-time” because the rollup’s smart contracts ensure only the designated preconfer can write to the state prior and during their turn.

[![image](https://ethresear.ch/uploads/default/optimized/3X/0/b/0b2b9aef6a1ebe1f45645bde939e8e235ceffb4d_2_690x265.jpeg)image1920×738 80.5 KB](https://ethresear.ch/uploads/default/0b2b9aef6a1ebe1f45645bde939e8e235ceffb4d)

**The Bootstrap Challenge**

This just-in-time constraint creates two significant problems:

1. Limited Availability: Super transactions can only happen during blocks where the
L1 validator has opted in as a preconfer
2. UX Issues: Unless every single Ethereum validator participates in the system, there will be slots where super transactions aren’t available

Getting 100% of Ethereum validators to participate is an enormous BD challenge. Therefore, we need an alternative solution: finding a way for validators to safely issue L1 EPs ahead-of-time.

### What is Custard?

Custard offers a solution to our timing problem by making a key observation: we don’t always need to control the entire L1 block to make safe guarantees. Instead, we can selectively lock just the specific pieces of L1 state that our super transaction needs to work with.

This insight is powerful because it means we can issue *some* types of L1 EPs ahead-of-time, as long as we can guarantee that the specific state we care about won’t change. By only locking what we need, rather than requiring control over everything, we can significantly reduce the number of validators needed as preconfers.

Note: The implementations we’ll describe next are intentionally simplified to clearly illustrate the mechanisms. In practice, these can be optimized for better capital efficiency and generality.

### Custard with EIP-7702

[EIP-7702](https://eip7702.io/) enables user accounts (EOAs) to set their own custom code based on any smart contract, effectively turning it into a smart account. We can use this to create time-locked guarantees about a user’s account state.

**How It Works**

Let’s walk through how Alice could execute her super transaction using EIP-7702:

1. Initial Lock (Slot S)

Alice locks her account’s nonce until a future slot S'
2. This prevents any changes to her account until the designated slot
3. Setup (Slot S + 1)

Alice requests her super transaction from a preconfer who will propose at a future slot S'
4. The transaction includes:

Depositing B ETH to the rollup
5. Executing the arbitrage trade
6. Withdrawing B + ε - f  ETH (original amount plus profit minus fee)
7. Having a solver complete the withdrawal on L1
8. Verification (Slot S + 1)

The preconfer checks that Alice’s account is properly locked
9. If verified, the preconfer issues all necessary preconfs
10. Execution (Slot S')

The preconfer executes the entire transaction:

Deposits Alice’s B ETH to the BRU
11. Commits the BRU blob to L1 containing Alice’s trade
12. Completes the solver’s transfer of B + ε - f ETH to Alice on L1
13. Settlement (Slot S' + Δ)

After Δ blocks, the BRU state is proven
14. The solver can recover B + ε + f ETH by withdrawing from BRU

**Key Insight**

By locking her account, Alice guarantees she’ll have sufficient funds (`B` ETH) when the super transaction executes. Preconfers can safely issue L1 EPs ahead-of-time if they require accounts to be first locked, solving our timing problem.

### Custard with Smart Contracts

While waiting for EIP-7702 to be released, we can achieve similar results using smart contracts. The key difference is that instead of modifying account behavior directly, users must first deposit their assets into an escrow contract that enforces the same guarantees:

- Assets are locked until the target slot
- The funds can only be deposited into the rollup
- No decreases in asset balance are allowed until then

[![image](https://ethresear.ch/uploads/default/optimized/3X/f/d/fdf3cfb392fbecb0ddb460ce989e680d54fe3aca_2_690x329.jpeg)image1920×916 86.9 KB](https://ethresear.ch/uploads/default/fdf3cfb392fbecb0ddb460ce989e680d54fe3aca)

The execution flow mirrors the EIP-7702 approach, but with one notable advantage: the escrow contract naturally accumulates a pool of locked assets, enabling potential capital efficiency optimizations in protocol design.

### Custard with Exclusion Preconfs

Exclusion preconfs represent a different kind of validator promise: instead of guaranteeing what they will do, validators commit to what they won’t do. Specifically, they promise to prevent certain state changes by disallowing specific account actions to take place. While exclusion typically goes against Ethereum’s values, when used carefully in this context, it serves a constructive purpose: locking specific account states to preserve ahead-of-time L1 EP validity. Importantly, these types of preconfs would only be permitted if explicitly authorized by the account owner to avoid censorship.

**How It Works**

Let’s walk through how Alice could execute her super transaction using exclusion preconfs:

1. Issuing Execution Preconfs

Alice gets exclusion preconfs from the validators ahead of her target super transaction slot
2. Each exclusion preconf promises not to:

Include transactions that would increase Alice’s nonce
3. Include transactions that would decrease Alice’s ETH balance
4. Execution

When the target slot arrives, Alice’s EOA is guaranteed to have the required ETH
5. The super transaction can proceed safely

[![image](https://ethresear.ch/uploads/default/optimized/3X/9/c/9c89a60055c3972a121f71747c5de9efd5216cfd_2_690x316.jpeg)image1920×881 88.7 KB](https://ethresear.ch/uploads/default/9c89a60055c3972a121f71747c5de9efd5216cfd)

An advantage of this approach is that all execution preconfs are issued off-chain, reducing gas costs. However, it introduces several complexities. Super transactions still require all earlier slot validators to be L1 exclusion preconfers - while easier than previous approaches, this remains a significant BD challenge. Additionally, paying for exclusion preconfs becomes tricky since nothing lands on-chain in the happy case and the collateral requirements and slashing conditions need to be carefully considered when assessing the risk of reneging.

### Limitations of this approach

A key distinction in Nethermind’s solver approach is that withdrawal requests have a simple “[L1 output condition](https://ethresear.ch/t/fast-and-slow-l2-l1-withdrawals/21161#p-51550-glossary-of-smart-contracts-and-transactions-used-5)” - they only need to verify that tokens arrive at a specific L1 address. This simplicity is what enables atomic withdrawals without real-time proving. However, more sophisticated super transactions might require L1 output conditions to depend on complex L2 state changes, in which case we may require real-time proving of L2 state. While Custard’s principles for managing L1 state dependencies still apply, implementations will either need to wait for real-time SNARKs to mature or accept the additional risks of TEE-based proving solutions.
