---
source: magicians
topic_id: 18985
title: Target constant throughput by tracking unused throughput (extending EIP 4396)
author: g11in
date: "2024-02-28"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/target-constant-throughput-by-tracking-unused-throughput-extending-eip-4396/18985
views: 665
likes: 2
posts_count: 8
---

# Target constant throughput by tracking unused throughput (extending EIP 4396)

(thanks [@jochem-brouwer](/u/jochem-brouwer) for inputs and feedback to get things a bit right here)

[EIP 4396](https://eips.ethereum.org/EIPS/eip-4396) (cc: [@adietrichs](/u/adietrichs)) provides for a way to compensate missed blocks by having an `parent_adjusted_gas_target` to factor into the base fee calculations. While it accommodates the unused capacity by missed slots and delivers the benefit to N+2 for the block missed at N (by expanding the gas target  at N+1) upto a limit, we can go further and track unused target gas  and pay it forward to the next blocks.

*note: its possible to modify the calculations to pay the benefit to N+1, but then it increases incentive for N+1 to not build on N even if it has seen it*

### New proposal

(Old proposal tracks  and accumulates even the unused target in a block but thanks to feedback and discussions with [@MicahZoltu](/u/micahzoltu) realized that unused target of a block is already benefiting and lowering baseFee for the next block. however unused target of a block can still be used to raise the gasLimit of the next block but there is a problem that builders could try to under-utilize space to provide them the ability to pack more at the next block on lower fees. So the new proposal doesn’t attempt accumulating the unused target of a block in any way)

So new proposal just tracks and accumulates the unused targets because of the missed blocks.

```python
BLOCK_TIME_TARGET = 12

# no change in previous constants
ELASTICITY_MULTIPLIER = ...
BASE_FEE_MAX_CHANGE_DENOMINATOR =

def buildBlock(...)
  # make the extra target available to the block upto gasLimit
  blockGasTarget = block.gasLimit // ELASTICITY_MULTIPLIER
  blockAvailableGasTarget = min (blockGasTarget + parent.unusedGasTarget, block.gasLimit)
 ...
  # update unusedGasTarget by accumulating if there are any misses and removing extra target available to this block
  block.unusedGasTarget =
  max(0,
   parent.unusedGasTarget
   # if there are no missed block, the following segment evals to 0
   + (block.timestamp - parent.timestamp - BLOCK_TIME_TARGET) // BLOCK_TIME_TARGET * blockGasTarget
  - (blockAvailableGasTarget - blockGasTarget))
  return block
```

base fee calculation changes as below

```python
def calcBaseFee (...)
  ...
  parentBlockGasTarget = parent.gasLimit // ELASTICITY_MULTIPLIER
  parentAvailableGasTarget = min (parentBlockGasTarget + parent.parent.unusedGasTarget, parent.gasLimit)

  gasUsedDelta = parent.gasUsed - parentAvailableGasTarget
  gasUsedDeltaDenominator  = parent.gasLimit // ELASTICITY_MULTIPLIER

  feeDelta = parent.baseFee * gasUsedDelta / gasUsedDeltaDenominator / BASE_FEE_MAX_CHANGE_DENOMINATOR

  # min feeDelta is enforced as before is gas used > available gas target
  if (parent.gasUsed > parentAvailableGasTarget)
    feeDelta = max(feeDelta, 1)

  # min base fee is enforced as before
  baseFee = max (parent.baseFee + feeDelta, MIN_BASE_FEE)
  return baseFee
```

### Old proposal

So a block builder not fully utilizing the blockspace wouldn’t mean lost capacity to the network. We can do this by tracking `unusedGasTarget` on the lines of `excessBlobGas`, i.e. a cumulative tracker of the previous unused blockspace capacity (limited by some max limit since blocks in a slot need to be build under a strict window)

so essentially:

```python
BLOCK_TIME_TARGET = 12

# no change in previous constants
ELASTICITY_MULTIPLIER = ...
BASE_FEE_MAX_CHANGE_DENOMINATOR =

# we allow the block to expand to some `hardGasLimit` than the provided `block.gasLimit` i.e. bigger blocks than usual to compensate for past missed slots or less throughput i.e. only when there is some unused available gas
HARD_GAS_LIMIT_MULTIPLIER = 3

def buildBlock(...)
  # block's normal gas limit tracking remains unchanged (as provided by fcU)
  block.gasLimit = ...
  hardGasLimit  = block.gasLimit * HARD_GAS_LIMIT_MULTIPLIER
  # however modified gas limit is available to build the block
  availableGasTarget = min (parent.unusedGasTarget + (block.timestamp - parent.timestamp) // BLOCK_TIME_TARGET * (block.gasLimit // ELASTICITY_MULTIPLIER), hardGasLimit)
  # if ELASTICITY_MULTIPLIER=2 this can be collapsed into a smaller calc
  availableGasLimit = min ( availableGasTarget + block.gasLimit - block.gasLimit // ELASTICITY_MULTIPLIER, hardGasLimit)
  ...
  #
  block.unusedGasTarget = max (availableGasTarget - block.gasUsed, 0)
  return block
```

block validations are now

```python
def validateBlock(...)
  ...
  # calculate the available gas limit  as above
  availableGasLimit = ...
  assert ( block.gasUsed  available gas target
  if (parent.gasUsed > parentAvailableGasTarget)
    feeDelta = max(feeDelta, 1)

  # min base fee is enforced as before
  baseFee = max (parent.baseFee + feeDelta, MIN_BASE_FEE)
  return baseFee
```

Open to improving the calculations and make them more precise/better to reflect the intend

## Replies

**MicahZoltu** (2024-02-28):

How do we differentiate between “demand was low” and “block producer didn’t fill the block when they could have”?

Low demand is already accounted for by the base fee movement, and we should not double-account for it by also expanding block size.  Block producers *choosing* to leave their blocks empty however is not accounted for by base fee movement and we *should* account for it by expanding future block size.

---

**g11in** (2024-02-28):

yes i modified calculations to expand the available target (and not gasLimit), so calc for a block’s gasLimit is:

available target + gasLimit - gasLimit // ELASTICITY_MULTIPLER

that is essentially used to allow block to be packed bigger than gasLimit, but essentially doesn’t change gasLimit

could you see if this addresses the problem you highlighted

---

**MicahZoltu** (2024-02-28):

Could we simplify things greatly by having the `availableGasLimit` remain unchanged, and *only* transiently change the gas target (which would only matter for end-of-block base-fee calculations)?

If a block is missing from slot `n`, the block proposed in slot `n+1` would process exactly as normal.  The block in slot `n+2` however would have its base fee adjusted as though the block in slot `n+1` had a `gasTarget` of 2x (because of the missing block).  This means if the block in slot `n+1` is full, the base fee would not change.  If the block in slot `n+1` is half full, the base fee would decrease.  The idea here being that we expect the block after a missing block to be double full, and if it isn’t then it means demand is down.

We can accumulate multiple missing blocks in a row, but I think we should cap the synthetic gas target to `block.gasLimit // ELASTICITY_MULTIPLIER` and just carry over the unused missing space into future blocks akin to what you have done here.  So if we miss 3 blocks in a row, the first block would have its synthetic gas limit doubled, which would drop the missed block count to 2, then the following block would consume another one dropping it to 1, and the third would finally consume the last missing block.

This means after 3 missed blocks, the baseFee cannot increase, it can only decrease for the next 3 blocks.  I think we could fiddle around to fix this if we wanted, but it would add complexity.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/g11in/48/3906_2.png) g11in:

> could you see if this addresses the problem you highlighted

I don’t think this addresses the problem.  The core of my issue is that block builders leaving stuff out is indistinguishable from block builders that had nothing else to put in the block, and if there was just nothing to put in the block we should *not* expand the limit and instead lower the base fee.  The base fee already accounts for demand changes, we just want this mechanism to account for slot misses (which are distinguishable from demand changes).

---

**barnabe** (2024-02-29):

Thanks for writing it up! It would take more time than I have right now (it’s a bit more involved than I understood initially), but ideally one would obtain a proof that the dynamical system you set up here does converge to a target you expect, for instance this is [some work](https://arxiv.org/pdf/2212.07175.pdf) we did, though you can convince yourself with [simpler arguments too](https://notes.ethereum.org/@barnabe/HkUg2pLUK).

The risk with messing around with the target dynamically is that the system becomes very chaotic. You don’t actually need to tell the system to catch up on unused gas today, it will decrease base fee so more people use the gas and you get back towards the target. If you want to make up for lost time as EIP-4396 does, you can then adjust the target based on how much capacity has been lost, but not based on the realised demand signal (how much gas you included). It may be that what you have also works, but I don’t see the intuitive argument given that the feature you want to obtain is imo already obtained by EIP-1559 in its current form, it makes up for “lean” times by decreasing price and letting more demand in.

If I get a few cycles I will try to write a more proper argument, or could pitch that as an extension to [previous simulation work](https://ethereum.github.io/abm1559/) to see what obtains.

---

**g11in** (2024-02-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> You don’t actually need to tell the system to catch up on unused gas today, it will decrease base fee so more people use the gas and you get back towards the target. If you want to make up for lost time as EIP-4396 does, you can then adjust the target based on how much capacity has been lost, but not based on the realised demand signal (how much gas you included)

yes after conversations with [@MicahZoltu](/u/micahzoltu) I have realized the same and hence will exclude the “unused capacity of a proposed block”. the problem is we can’t differentiate between if the period was “lean” (so base fee should go down) or if builder (most probably mev builder) didn’t include txs because it didn’t want to/care to as its goals were met (in which case next block’s limit and target should increase).

But i would still like to modify the EIP-4396 by tracking the “cumulative unused capacity” because of missed slots, and pay it forward to future series of the blocks (limited by gas limit at each block).

---

**gakonst** (2024-03-01):

Thanks for the writeup! This is an interesting idea.

How should we think about worst / adversarial cases here?

For example, thinking about periods alternating between empty blocks and gigablock bursts?

Would all nodes be able to run a “giga”-block fast enough to stay with the tip consistently?

Or (maybe this is too far out) is there a world where a MEV Builder would try to get a few empty blocks to execute a block and perhaps benefit from broadcasting it faster than others, and that might end up in some kind of bad outcome?

---

**g11in** (2024-03-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gakonst/48/50_2.png) gakonst:

> Would all nodes be able to run a “giga”-block fast enough to stay with the tip consistently?

yes a valid question, although the “giga” block can be bound by some higher “hard limit” as proposed in original proposal, but as such there could be further gamification. so have modified the proposal to not track unused target of empty blocks (so tracks only missed blocks unused target) and also kept the gasLimit unmodified so passing the benefit of only missed slots to the future blocks in form of keeping base fee low

