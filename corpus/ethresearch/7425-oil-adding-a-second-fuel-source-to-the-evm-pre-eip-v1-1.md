---
source: ethresearch
topic_id: 7425
title: "Oil: adding a second fuel source to the EVM (pre-EIP v1.1)"
author: suhabe
date: "2020-05-14"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/oil-adding-a-second-fuel-source-to-the-evm-pre-eip-v1-1/7425
views: 2275
likes: 6
posts_count: 2
---

# Oil: adding a second fuel source to the EVM (pre-EIP v1.1)

This post is version 1.1 of the [original proposal](https://ethresear.ch/t/oil-adding-a-second-fuel-source-to-the-evm-pre-eip). The summary of changes are:

- Exceptional halts do not burn oil.
- ETH refund is based on the remaining oil exchanged at gasPrice.
- Meta-transactions can still work with oil.

# Introduction

This proposal for adding a second fuel source to the EVM called **oil** that is unobservable and works in parallel with gas. The idea was originally devised by [Alexey Akhunov](https://ethresear.ch/u/AlexeyAkhunov/), and the name of oil was suggested by Griffin Hotchkiss. Thanks to Martin Swende for the encouragement to pursue the idea.

# Motivation

- Gas is currently being used for two different purposes:

To pay for compute, memory, and storage resources
- To prevent re-entrancy by hardwiring the amount of gas a call can use.

Adjusting the gas schedule to better reflect resource usage causes unintended consequences because contracts may be written in a way such that correctness depends on a specific gas schedule.

- Making an instruction cheaper may make a re-entrancy path feasible
- Making an instruction more expensive may make a call fail because the amount of gas hard-wired to it is now insufficient to execute the call

Oil is a new fuel source that works very similarly to gas, but works in parallel to it.

# Specification

- A transaction has a gasLimit and gasPrice.
- Currently, a transaction pays E ether for allocating gasLimit amount of gas to the transaction based on the gasPrice.
- With oil, a transaction pays E ether for allocating gasLimit amount of gas to the transaction based on the gasPrice, and additionally oilLimit amount of oil to the transaction where oilLimit is set equal to gasLimit.
- A transaction still only specifies a gasLimit. The EVM will internally set the oilLimit to be the same as the gasLimit specified by the transaction.
- Gas metering and gas semantics do not change.
- If the transaction runs out of oil at any point during execution, the transaction reverts. Unlike with gas, where out-of-gas reverts only the current frame, and lets the caller examine the result, out-of-oil always reverts the entire transaction (all frames).
- A caller contract cannot restrict how much oil a callee contract can use, unlike gas.
- The oil cost of all instructions is exactly the same as the gas cost, until further EIPs to modify oil schedule to reprice EVM operations.
- An OIL instruction to read current oil will not be added, and this is intentional.
- The amount of ETH refunded for a transaction is now calculated based on the remaining oil, rather than remaining gas.

If the transaction has an EVMC_SUCCESS status code, the sender is refunded the amount of ETH that is the remaining oil exchanged at the gasPrice.
- Similarly, if the transaction has an EVMC_REVERT status code, the state is reverted as usual, and the sender is refunded the amount of ETH that is the remaining oil exchanged at the gasPrice.

The EVM handles exceptional halts by burning the remaining gas so the caller does not get a gas refund. An exception halt occurs when the EVM encounters an 1) an opcode which currently does not correspond to any instruction, 2) the `INVALID` opcode, 3) stack underflow, or 4) jump to an invalidation destination. In contrast, oil is never burned even in exceptional halts. Thus, for some contracts invocations the oil cost will be less than gas cost.

# Meta-transactions

- A meta-transaction is a payload that is sent to a relayer smart contract, which is then tasked with converting the payload into an actual transaction by funding it with gas and executing it. Systems like the GnosisSafe depend on this mechanism. Meta-transaction relayers need to be able to inspect the result of the relayed transaction in order to make that result conditional on certain payment to the relayer.
- One concern with oil is whether it breaks meta-transactions since an out-of-oil exception that occurs inside the relayed transaction deprives the relayer contract from the ability to extract payment for its service. This opens up a griefing vulnerability where a malicious sender may cause the meta-transaction relayer run out of funds by paying for gas/oil, but not being able to receive any compensation. However, this vulnerability can be addressed by over-estimating how much oil the relayed transaction will need so that an out-of-oil exception does not occur.
- One can calculate a naive upper bound on the amount of oil needed for the relayed transaction by comparing the gas schedule and oil schedules, and finding the operation that has the largest ratio of oil-to-gas cost, maxR. Then, the value gas*maxR is a naive upper bound for oil consumption.
- Calculating a tighter upper bound is possible by leveraging additional information such as the graph of JUMPDESTs and stack convergence.

# Example

Consider the following two contracts where contract `A` is stored at address a and contract `B` is stored at b. Initially, let the gas cost of each instruction equal the oil cost of each instruction.

```auto
contract A {
    function set(B b) public {
        b.set();
    }
}
contract B {
    uint public amount;
    function set() public {
        amount = address(this).balance;
    }
}
```

Suppose a transaction TX_1 is sent to A to invoke `A.set` on B with initial gas G_{init}, where G_{init} is set to exactly the gas cost of executing  a`.set(`b`)`. Then, the initial oil O_{init} would be equal to G_{init} and the transaction would be accepted.

Now, suppose the oil cost of the `BALANCE` opcode is increased and that a TX_2 is sent that is identical to TX_1. This transaction TX_2 would get rejected with an out-of-oil error because the total oil cost would exceed O_{init}.

## Replies

**matt** (2020-05-14):

As requested on the eth 1.x call, I will give an initial take on how Quilt sees oil affecting account abstraction (AA). To do so, I’ll enumerate every area where gas values are used in AA decision making then note how oil changes the behavior. This should all generally be taken with a grain of salt as we’re still understanding and defining the scope of AA ourselves. We also haven’t yet looked into how witness accounting will affect AA and we assume, by definition, that AA contracts are not susceptible to reentrancy.

### Transaction validation (no change)

We expect nodes to have some predetermined gas limit they plan to expend while validating AA transactions. In order to support the same set of transactions, the gas limit would need to be adjusted proportionally to any changes in the gas schedule. This would also need to happen if oil is introduced, but since it is an out-of-band requirement set by individual nodes, it would not be an issue.

### PAYGAS op code (no change)

The `PAYGAS` opcode is a breakpoint between the validation logic (and post validation and accounting, like incrementing a nonce) and the normal execution of a transaction. It accepts a single parameter which determines the price to pay for the gas limit specified in the overall transaction. The switch to oil won’t affect this process.

### Applications of AA (some change)

There are two general categories of AA accounts: owned and unowned.

- owned - an AA contract whose balance is owned by the user(s) transacting with it (e.g. smart contract wallet, multisig).
- unowned - an AA contract whose underlying balance is not explicitly owned by any particular user (e.g. a dapp contract which pays for transactions).

Since we can attribute any action from an owned account to its owner, there is no need for a gas safeguard. However there are some scenarios where an unowned account would benefit from such a guard against calls to untrusted contracts. This would be more difficult with the introduction of oil once the schedule for oil deviates from gas s.t. in the future gas is several orders of magnitude cheaper than oil for the same computation. There are other ways of solving this and this safeguard technique really isn’t a solution to the underlying problem of identifying sybils. So this is most likely okay to lose.

#### A note on meta-transactions with respect to AA

Although oil would remove the ability for developers to rely on the breakpoint-like property of `CALL` on out-of-gas traps, AA would give back some flexibility by allowing developers to perform operations before calling `PAYGAS`. These operations (e.g. payment for a meta-tx) would be persisted even in the event of an out-of-oil trap.

