---
source: ethresearch
topic_id: 5007
title: Maximally simple account abstraction without gas refunds
author: vbuterin
date: "2019-02-18"
category: Sharding
tags: [account-abstraction]
url: https://ethresear.ch/t/maximally-simple-account-abstraction-without-gas-refunds/5007
views: 4203
likes: 4
posts_count: 6
---

# Maximally simple account abstraction without gas refunds

For background, see [Tradeoffs in Account Abstraction Proposals](https://ethresear.ch/t/tradeoffs-in-account-abstraction-proposals/263?page=2)

In this post I’ll make an account abstraction proposal that I would argue achieves significantly greater simplicity, and greater generality, than anything proposed so far, but at a price: transactions whose gas costs are not completely static may end up overcharging gas.

The proposal is simple. We add an opcode `BREAKPOINT`, with the property that a function call that fails after a `BREAKPOINT` reverts only up to the `BREAKPOINT`. User account code would in general be structured as follows:

```python
verify_nonce()
verify_signature()
send(coinbase, x)
breakpoint()
do_stuff()
do_more_stuff()
```

After the execution hits the `BREAKPOINT` opcode, the block proposer is certain that they will get compensated for including the transaction. Note that in this model, refunds for unused gas are **not** possible.

To add more flexibility, we can add another opcode, `DECREASE_LIMIT`, which decreases the remaining gas limit without consuming gas. This would allow for account code where the gas limit of a transaction can be determined in the “header” (ie. before the `send` and `BREAKPOINT`).

### Consequences

- apply_msg and apply_tx become identical (fee market reform can be done at the per-block level), greatly reducing complexity
- The ABI would need to specify the max gas consumption of each function call, so that tight maximums can be more easily computed
- Does not require static analysis of code
- Would lead to some inefficiency in cases where gas costs truly are variable (the most common use case being CREATE2’ing a contract if and only if it does not exist yet), as the user would need to pay for the higher level of consumption even if the lower level of consumption is more frequent
- Implements full abstraction, so we would lose the tx hash uniqueness guarantee

## Replies

**ChengWang** (2019-02-20):

How would you price the code after failure for the following case:

```auto
verify_nonce()
verify_signature()
send(coinbase, x)
breakpoint()
fail()
lots_of_unused_code() // would waste space for opcodes
```

---

**vbuterin** (2019-02-22):

It would revert to the breakpoint, cost the full amount of gas, and the payment to the miner would be the `x`.

---

**ChengWang** (2019-02-22):

Another thing I am not sure about is: are users motivated to use this breakpoint opcode? Normally, users would expect its transaction to get fully executed.

Miners are indeed motivated to accept these partially executed transactions.

---

**vbuterin** (2019-02-25):

Miners and p2p nodes would run the following algorithm to verify transactions:

Run the transaction, running the code for a max of 100000 gas until you hit one of four cases:

1. The transaction pays the miner enough and hits the breakpoint
2. The transaction hits a breakpoint but does not pay the miner enough
3. The transaction exits with an exception
4. The transaction execution hits the 100k gas maximum

In case (1), accept the transaction, in cases (2, 3, 4) reject it.

Transaction senders would construct their code in a compatible way to get included.

---

**PhABC** (2019-02-26):

Other than efficiency, why isn’t smart contract level account abstraction sufficient?  I.e. your contract manages your funds with whatever authentication, logic and cryptographic scheme it wants.

