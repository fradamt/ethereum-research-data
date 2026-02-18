---
source: magicians
topic_id: 6640
title: "EIP 3651: Warm COINBASE"
author: wjmelements
date: "2021-07-12"
category: EIPs > EIPs core
tags: [evm, eth1x, shanghai-candidate]
url: https://ethereum-magicians.org/t/eip-3651-warm-coinbase/6640
views: 29921
likes: 7
posts_count: 12
---

# EIP 3651: Warm COINBASE

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/3651)














####


      `master` ← `wjmelements:warm-coinbase`




          opened 11:22PM - 12 Jul 21 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/2/297dfe2862bf68c18899dc01581a4784220865dd.jpeg)
            wjmelements](https://github.com/wjmelements)



          [+40
            -0](https://github.com/ethereum/EIPs/pull/3651/files)







#### Changes
Introduces EIP to initialize COINBASE address as warm.
Reviewer @li[…](https://github.com/ethereum/EIPs/pull/3651)ghtclient

## Replies

**axic** (2021-07-12):

FYI this was mentioned in [EIP-2929: Gas cost increases for state access opcodes - #52 by axic](https://ethereum-magicians.org/t/eip-2929-gas-cost-increases-for-state-access-opcodes/4558/52) and [@holiman](/u/holiman) answered it with [EIP-2929: Gas cost increases for state access opcodes - #55 by holiman](https://ethereum-magicians.org/t/eip-2929-gas-cost-increases-for-state-access-opcodes/4558/55).

---

**wjmelements** (2021-07-12):

I agree that it was an oversight. I don’t think it provides meaningful simplification.

---

**wjmelements** (2021-07-12):

The status quo also incentivizes me to sign a different transaction per miner, which favors the top miners at the expense of smaller miners.

---

**wjmelements** (2021-07-23):

COINBASE transfers are overpriced because the access list is not initialized with COINBASE. We already include ORIGIN, recipient, and the set of all pre-compiles, but not COINBASE. The proposal is to include COINBASE.

The main impact of a Warm COINBASE would be for transactions that pay miners conditionally. Such transactions specify a minimal gas price but pay the COINBASE a much larger fee if some conditions are met. Among other things, this flexibility allows users to avoid paying for transactions that would revert, and specialized systems have been developed to process such transactions outside of the mempool. The first and most popular such system is Flashbots, which is available to the public, but there are others, and several apps are building on top of it. The main benefit so far of the advent of these systems has been an end to the chaotic priority gas auctions and backrunning spam that clogged the network last year. Most blocks this year have had at least one COINBASE transfer, while many have 2 or 3, and some have more. Their frequency has been increasing steadily over time.

Block validators should have the COINBASE account loaded already in order to update its balance with the block rewards, and these increasingly frequent conditional payments justify automatic inclusion into the default access list. If gas should reflect the burden of validation, COINBASE transfers are overpriced, and this proposal should be an easy fix.

---

**sbacha** (2022-03-24):

How does this effect the cost of coinbase transfer when the coinbase address is a contract?

e.g.

```nohighlight
block.coinbase.call{value: _ethAmountToCoinbase}(new bytes(0));
```

---

**wjmelements** (2022-03-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sbacha/48/4661_2.png) sbacha:

> How does this effect the cost of coinbase transfer when the coinbase address is a contract?

Doesn’t matter if recipient is a contract. The first call to coinbase in a transaction will be cheaper.

---

**sbacha** (2022-11-10):

This is slated to be included in Shanghai, [execution-specs/shanghai.md at master · ethereum/execution-specs · GitHub](https://github.com/ethereum/execution-specs/blob/master/network-upgrades/mainnet-upgrades/shanghai.md)

---

**xinbenlv** (2022-11-28):

Hi [@wjmelements](/u/wjmelements) thank you for this EIP. Look forward to its improvement to gas and chain efficiency.

Just to clarify, IIRC clients before and after this EIP calculated gas cost differently assuming all clients shall by default treat coinbase as cold, right?

If that’s correct understanding, could you

1. Describe the differences of gas cost before and after
2. Clarify if this EIP requires a hard-fork. My understanding is it does, and if so please consider add some wording like “Upon FORK_BLKNUM”

If my understanding is incorrect, please help me understand better.

---

**wjmelements** (2022-11-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> Describe the differences of gas cost before and after

The EIP intentionally does not specify any difference in gas.

---

**wjmelements** (2022-11-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> Clarify if this EIP requires a hard-fork. My understanding is it does, and if so please consider add some wording like “Upon FORK_BLKNUM”

All Core EIPs require a hard fork. The specification of when the hard fork happens is outside the scope of the EIP.

From EIP-1:

```auto
  - **Core**: improvements requiring a consensus fork (e.g. [EIP-5](./eip-5.md), [EIP-101](./eip-101.md)), as well as changes that are not necessarily consensus critical but may be relevant to [“core dev” discussions](https://github.com/ethereum/pm) (for example, [EIP-90], and the miner/node strategy changes 2, 3, and 4 of [EIP-86](./eip-86.md)).
```

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> and if so please consider add some wording like “Upon FORK_BLKNUM”

Core EIPs don’t do that boilerplate anymore. It was never necessary or helpful.

---

**poojaranjan** (2022-12-12):

An overview of EIP-3651 by [@wjmelements](/u/wjmelements) in [PEEPanEIP #92: EIP-3651: Warm COINBASE with William Morriss](https://www.youtube.com/watch?v=-oEVebccI7I)

  [![image](https://i.ytimg.com/vi/-oEVebccI7I/hqdefault.jpg)](https://www.youtube.com/watch?v=-oEVebccI7I)

