---
source: magicians
topic_id: 3738
title: Skinny EIP 1559
author: vbuterin
date: "2019-10-31"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/skinny-eip-1559/3738
views: 5876
likes: 15
posts_count: 11
---

# Skinny EIP 1559

This is a proposal to implement a greatly simplified transaction fee reform mechanic that is intended to have similar (though slightly less optimal) effects to EIP 1559 but at ~1/5 the implementation complexity.

### Parameters

- ADJUSTMENT_COEFFICIENT: 8

### Protocol changes

- We interpret a particular storage slot in the state (eg. as storage key 0 of address 0x0100) as the BASEFEE. "Set BASEFEE" means to SSTORE to that storage slot, and when using BASEFEE in equations we mean to SLOAD from that storage slot to read the value.
- At the start of processing block FORK_BLKNUM, set BASEFEE to 1
- Let diff = block.gas_used - block.gas_limit // 2. At the end of processing a block:

After applying block rewards and fees, reduce the miner’s balance by BASEFEE * block.gas_used. If the resulting balance would be below zero, the block is invalid.
- If diff > 0, set BASEFEE += max(1, BASEFEE * diff // block.gas_limit // ADJUSTMENT_COEFFICIENT)
- If diff  1, set BASEFEE -= max(1, BASEFEE * abs(diff) // block.gas_limit // ADJUSTMENT_COEFFICIENT)

### Rationale

Currently, miners generally have some internal `mingasprice`, and accept any transactions with `tx.gasprice >= mingasprice`, accepting the highest-fee transactions if there are more than enough transactions available to fill the block. The `mingasprice` reflects the miner’s cost in processing the transaction and the marginal increment that the transaction adds to the risk that the block will not propagate quickly enough to join the main chain.

The “rational” `mingasprice` has been calculated to be about 0.8 gwei (uncle blocks lose ~0.33 ETH = 330m gwei, 10 million gas blocks add ~0.025 to the uncle rate over empty blocks, so expected cost of 1 gas = 330m / 10m * 0.025 = 0.825 gwei)  and miners do actually set about this value (see table at the [bottom of the ethgasstation page](https://ethgasstation.info/)).

This mechanism adds a fee that miners are required to pay (that gets burned), which adjusts their interests so that they will want to set their `mingasprice` dynamically, to equal the `BASEFEE` plus 1 gwei (client devs can just set miner settings so they do this automatically without needing to change anything). Users can now send transactions setting a gasprice of the current head’s BASEFEE (which will be correct for the next block) + 1-2 gwei, and get a high likelihood that their transactions will be included in the next block, without needing to do complex calculations based on recent fees and mempool stats to compute fees and even then only getting included a few blocks later. Hence, most of the simplicity gains of full-on EIP 1559 carry over, though during spikes users may need to set higher fees as they do now to ensure their transactions get included quickly.

## Replies

**kaiynne** (2019-10-31):

One of the main challenges as I understand it, and costs, with 1559 (I guess we now call it the fat version?) is the effort to model the change, particularly with two fee markets operating simultaneously. How much do you think this will lower the need for modelling to be performed before this can be implemented?

---

**stobiewan** (2019-11-01):

The last point under protocol changes, I think you meant ‘if diff < 0’ rather than ‘if diff > 0’.

---

**basco** (2019-11-01):

Is that

```python
if diff > 0
    set BASEFEE += max(1, BASEFEE * diff // block.gas_limit // ADJUSTMENT_COEFFICIENT)
else if diff > 0 and BASEFEE > 1
    set BASEFEE -= max(1, BASEFEE * abs(diff) // block.gas_limit // ADJUSTMENT_COEFFICIENT)
```

Or

```python
if diff > 0
    BASEFEE += max(1, BASEFEE * diff // block.gas_limit // ADJUSTMENT_COEFFICIENT)
    if BASEFEE > 1
        BASEFEE -= max(1, BASEFEE * abs(diff) // block.gas_limit // ADJUSTMENT_COEFFICIENT)
```

---

**AFDudley** (2019-11-01):

We are already implementing what Slipper and I designed. The issue has never been implementation complexity, the issue has always been the cost of everything else. Lowering the implementation complexity doesn’t lower the simulation costs, it doesn’t lower the cost of economic analysis. It may lower the cost of testing.

---

**vbuterin** (2019-11-01):

Thanks [@stobiewan](/u/stobiewan) [@basco](/u/basco) for the fix. Added.

So this approach does NOT do the “two fee markets operating simultaneously” approach; it directly changes how existing transactions work, in a completely backwards-compatible way that doesn’t require eg. hardware wallets or the p2p layer to change any code.

If implementation complexity is not the bottleneck and simulation and analysis costs are the big issue then that’s fine, and maybe the simplification is not necessary. I’d also be curious to see what kinds of simulations/analysis you have in mind that needs to be done that has these high costs.

---

**edmundedgar** (2019-11-02):

Do you have a simple write-up of what you’re implementing? (Or a link to the code you’re working on that implements it.)

It’s currently hard for anybody except yourself to compare the “full” version and this “skinny” version because the original “full” EIP as currently written leaves out important details like how the target gas usage is decided. It sounds like you actually have a complete specification, at least in your head - it doesn’t matter if you make some mistakes when posting it, [@stobiewan](/u/stobiewan) and [@basco](/u/basco) will spot them…

---

**AFDudley** (2019-11-03):

I’m not entirely sure how to respond to this given that most of the cost in simulation is in the fixed costs of doing the tooling required to do the analysis. I’m sure the Gauntlet team would be happy to speak with you directly about what they were offering to do and where costs could be reduced.

If both transaction types are equally available, what prompts users to switch?

---

**AFDudley** (2019-11-03):

I’ll post the link to the repo here when it’s “ready”.

---

**Agusx1211** (2019-11-04):

This “skinny” version of EIP 1559 is 100% compatible with the way that existing clients build and sign transactions, that’s awesome.

> Let  diff = block.gas_used - block.gas_limit // 2

This mechanism changes the real gas limit of the network to be `block.gasLimit / 2`, because in the long run, the rules will be optimizing `BASEFEE` until blocks are always half full.

Maybe it should be included with this change, a doubling of the current default target gas limit set by the miners, currently would be from `10000000` to `20000000`.

---

**Agusx1211** (2019-11-22):

If we move forward with this EIP, we should consider providing a way to read `BASEFEE` from the EVM context, maybe ['EXTSLOAD' opcode proposal](https://ethereum-magicians.org/t/extsload-opcode-proposal/2410) could be passed alongside this EIP

