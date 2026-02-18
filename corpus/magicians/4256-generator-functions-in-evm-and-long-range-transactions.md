---
source: magicians
topic_id: 4256
title: Generator functions in EVM and long-range transactions?
author: Ethernian
date: "2020-05-04"
category: Magicians > Primordial Soup
tags: [evm]
url: https://ethereum-magicians.org/t/generator-functions-in-evm-and-long-range-transactions/4256
views: 860
likes: 0
posts_count: 5
---

# Generator functions in EVM and long-range transactions?

Just a crazy and quick idea:

What if the EVM could suspend/resume its execution like the Javascript VM can do?

Something like js generator functions?

```auto
function* gen() public returns (uint) {
  yield 1;
  yield 2;
  yield 3;
}
```

It could enable some kind of long-range transaction that could last for multiple blocks. It could be useful for cross-shard calls.

EVM runtime could keep the tx memory state between blocks without storing it to disk. If the tx doesn’t finish in Nmax blocks, it fails. To recover the execution state of some long-range transaction running at block N, a node could always replay it from the beginning at some previous block.

Most probably the idea is not new, but I have not found any similar discussions.

Do you have any hints?

## Replies

**wjmelements** (2020-05-15):

You could implement this with the current EVM using state.

For the EVM you should be thinking about CPU-level instructions. Javascript doesn’t require additional CPU instructions; it just defines an async syntax that uses the same instructions as C. There’s nothing you can do in JS that you can’t do in assembly.

What I think you want is a solidity programming language feature that would manage the state for you. I’m generally opposed to that because it hides from the programmer the gas costs of their abstractions.

---

**Ethernian** (2020-05-22):

I suppose, you don’t understand me yet.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> You could implement this with the current EVM using state.

No, unfortunately you can’t do it now because the EVM memory doesn’t persist between transaction calls.

My idea is exactly to let the memory persist between transaction calls (for the limited time of some blocks) by keeping it in the memory, but without persisting it into the contract state. It will make the generator-like functions in solidity and “long-range” transactions in ethereum possible.

The JS generator function in my post above is just an example.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> What I think you want is a solidity programming language feature that would manage the state for you. I’m generally opposed to that because it hides from the programmer the gas costs of their abstractions.

As I mentioned, I don’t suppose to write the suspended EVM state into the contract state. I suppose the EVM can just keep it in memory without to dispose it. Yes, the total memory footprint grows because many transactions can go into the suspended state at the same time, but for every single transaction there is no additional resource usage. So I see no problem with gas calculation.

---

**wjmelements** (2020-07-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> No, unfortunately you can’t do it now because the EVM memory doesn’t persist between transaction calls.

I said state, not memory.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> My idea is exactly to let the memory persist between transaction calls (for the limited time of some blocks) by keeping it in the memory, but without persisting it into the contract state. It will make the generator-like functions in solidity and “long-range” transactions in ethereum possible.

You want state? You should pay state prices. Memory is not persisted on purpose. The gas refund from clearing the state should be sufficient to offset your costs.

---

**Ethernian** (2020-07-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> I said state, not memory.

I mean exactly the state *in transient memory, not in the permanent  storage*.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> You want state? You should pay state prices. Memory is not persisted on purpose. The gas refund from clearing the state should be sufficient to offset your costs.

I don’t want use the state, I don’t want to pay the state price.

I want use transient memory or *already running client* for that, which is much cheaper.

A freshly started client should rebuild the transient state of the long-term EVM by replaying the tx from the block in the past, where the long-term tx was started. It implies, a long term-tx may last only few blocks to keep the memory consumption and client starting time reasonable.

