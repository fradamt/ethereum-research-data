---
source: magicians
topic_id: 2196
title: Future Options for EVM + eWASM
author: boris
date: "2018-12-12"
category: Working Groups > Ethereum 1.x Ring
tags: [evm, evm-evolution, ewasm]
url: https://ethereum-magicians.org/t/future-options-for-evm-ewasm/2196
views: 1630
likes: 1
posts_count: 5
---

# Future Options for EVM + eWASM

[![7evmewasmoptions](https://ethereum-magicians.org/uploads/default/optimized/2X/4/4b967407a16d59822497174988fffd76c9ca7bcd_2_305x500.jpeg)7evmewasmoptions1786×2920 1.04 MB](https://ethereum-magicians.org/uploads/default/4b967407a16d59822497174988fffd76c9ca7bcd)

This is a quick sketch of the 7 options for EVM / eWASM going forward, as roughly explained to me by [@expede](/u/expede)

I will turn this into some diagrams, and come back and edit this post with descriptions of each of these options.

We’re sharing this to provide background and material to have useful discussions.

## Replies

**gcolvin** (2018-12-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> I will turn this into some diagrams, and come back …

At which point I can see how much these overlap with the ones I’ve considered.

---

**gcolvin** (2019-01-03):

Well?  Still waiting.  I really can’t make sense of that whiteboard.

[@boris](/u/boris) [@expede](/u/expede)

---

**expede** (2019-01-04):

They’re just different permutations of where you could stick eWASM and the EVM during a transition period. Not all of them make sense, but are there for completeness.

1. Run them in parallel
2. Have an EVM hosted on WASM as a precompile
3. Add an AS_WASM opcode to the EVM spec; accept WASM bytecode as args
4. Have WASM as a precompile in an EVM environment
5. Write an EVM in WASM, and use that until ETH 2.0; then use it in option 2
6. Drop the WASM idea all together and just improve the EVM
7. Drop the EVM completely; find migration strategy (transpile or manual migration)

---

**gcolvin** (2019-01-08):

OK.  And there is 8–do nothing. And 7 can’t happen because existing EVM code and the code it generates must keep running.  The rest are pretty much just different ways of implementing a client–unless we go with 6 or 8 then clients need to run both eWasm and EVM somehow.  One way to make that easy for wasm-only clients–which might amount to 7–is to place a canonical evm2wasm transpiler on the blockchain for them to use.  (This might also be a convenient way to compute gas for EVM operations.)

