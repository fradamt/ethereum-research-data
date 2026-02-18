---
source: magicians
topic_id: 26032
title: Diamond Contract Gas Efficiency Challenge
author: mudgen
date: "2025-10-31"
category: Uncategorized
tags: [solidity, gas-saving]
url: https://ethereum-magicians.org/t/diamond-contract-gas-efficiency-challenge/26032
views: 30
likes: 0
posts_count: 1
---

# Diamond Contract Gas Efficiency Challenge

The `DiamondLoupeFacet.sol` implementation in the Compose smart contract library is too gas inefficient. I challenge anyone to write the most gas efficient, sensible code, to implement this.

See this issue for details:



      [github.com/Perfect-Abstractions/Compose](https://github.com/Perfect-Abstractions/Compose/issues/155)












####



        opened 04:06PM - 30 Oct 25 UTC



        [![](https://avatars.githubusercontent.com/u/49092?v=4)
          mudgen](https://github.com/mudgen)





          new feature







## Feature Request

The general [diamondCut implementation](https://github.com/P[…]()erfect-Abstractions/Compose/blob/main/src/diamond/DiamondCutFacet.sol), which is used to add/replace/remove functions on a diamond during deployment and upgrades, is gas efficient.

The diamond loupe consists of 4 functions that tell what is in a diamond -- what functions, and facets a diamond currently has.

Our current [DiamondLoupeFacet implementation](https://github.com/Perfect-Abstractions/Compose/blob/main/src/diamond/DiamondLoupeFacet.sol) is very  gas inefficient. The functions in DiamondLoupeFacet are view functions that are only meant to be called off-chain, so they don't have to be gas efficient. However our implementation is very, very gas inefficient, and maybe, just maybe, that might cause problems in the future for very very large diamonds with many many functions and facets.

So we need a more gas efficient DiamondLoupeFacet implementation without changing our current diamondCut implementation and without changing our `compose.diamond` diamond storage. **THIS IS THE CHALLENGE!**

### The winning implementation must meet these points the best:

1. Must balance code complexity with gas savings. Code complexity that saves a lot of gas is accepted. Code complexity that saves a little gas is no good, and it is better to refactor it to make it more readable, if that only costs a little more gas.

2. In the source file, in comments, you must describe the general approach and algorithm to implement the functionality. Must also say how it saves gas. How clear and understandable your description is matters.

3. No matter the complexity of the code, it must be well documented (with comments in the code) so people can still read and understand it, with minimal understanding of assembly.

I invite as many people that want to work on this challenge to do it.

If you do this challenge then leave a comment in this issue with a link to your implementation.

The best implementations, or parts of implementations will be added to the new `DiamondLoupeFacet.sol`

I am working on this challenge myself. I challenge you to do better than me.

## Helpful Information

**Have a question?** Please check our  [CONTRIBUTING](https://github.com/Perfect-Abstractions/Compose/blob/main/CONTRIBUTING.md) file first - your answer might already be there!

**Want to discuss something?** For general questions, ideas, or brainstorming, please browse our [discussions](https://github.com/Perfect-Abstractions/Compose/discussions) or start a new one.

You can also join our [Discord](https://discord.gg/DCBD2UKbxc) to discuss the issue.
