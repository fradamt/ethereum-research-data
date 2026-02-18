---
source: magicians
topic_id: 22815
title: "EIP-XXXX: Increase Gas Utilization Target"
author: storm
date: "2025-02-10"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-xxxx-increase-gas-utilization-target/22815
views: 577
likes: 9
posts_count: 6
---

# EIP-XXXX: Increase Gas Utilization Target

[Link to EIP](https://github.com/ethereum/EIPs/pull/9354)

#### Update Log

- 2025-02-10: initial draft

#### External Reviews

None as of 2025-02-10.

#### Outstanding Issues

None as of 2025-02-10.

## Replies

**storm** (2025-02-10):

*space reserved for future faq*

---

**storm** (2025-02-10):

the EIP uses the gold double slope curve shown below

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/3/33c02032d5c3ae1a7ecc6e6d57b98e2648f5e8e0_2_509x500.png)image1118×1097 85.9 KB](https://ethereum-magicians.org/uploads/default/33c02032d5c3ae1a7ecc6e6d57b98e2648f5e8e0)

this EIP maintains the base fee update range to stay within [-12.5%, +12.5%] per block. this range isn’t necessarily optimal, but this EIP aims to change as few aspects of EIP-1559 as possible while still adjusting the gas target

there are other ways the update rule could be changed while still maintaining the range, such as the blue offset curve in the diagram

---

**benaadams** (2025-02-10):

Makes it completely off balance?

Especially the blue line; where gasprice can easily lose 12.5%; but can only gain 12.5% at 100% full. So gas price would end up at 0

Need to at least return to the curve; say an S-curve

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/b/b4992b7afad4e3c8fd2144e2a3cec64c8e2b8214_2_509x500.png)image1018×1000 121 KB](https://ethereum-magicians.org/uploads/default/b4992b7afad4e3c8fd2144e2a3cec64c8e2b8214)

So it has some chance of gaining back what it lost (though even then am not sure; as it will precipitously drop but only slowly rise if that is unbalanced)

Otherwise `∑ f(x) < 1` and it will inevitably end up at zero

---

**benaadams** (2025-02-10):

Gas price changes should also be based on an EMA rather than last block alone; so it changes sensibly rather than whipsawing after blocksizes of those with private order flow and those without private orderflow

---

**wjmelements** (2025-02-11):

I think what you really want is a higher gas limit, or perhaps lower gas prices.

The point of having a lower utilization than the block gas limit is to allow elasticity while keeping the same average. This leads to predictable gas prices via the base fee mechanism. You should read eip-1559, particularly its motivation.

Before eip-1559, the gas utilization was 100% of the block gas limit. Very rarely would blocks be less than full, but it was difficult to predict the gas price you would need for a transaction to confirm, because you would have to outbid the top margin of the mempool.

If you increase the target utilization, the gas limit would have to be lower. You’d be changing 2x elasticity to 4/3x and the gas price would become more volatile.

I think it would be better to **lower** the gas utilization target, as it would provide more flexibility under congestion. If the target utilization was 25%, the elasticity would be 4x, a number I supported when 1559 was originally being debated.

