---
source: magicians
topic_id: 11558
title: "solidity-template: a modern Solidity contract template utilizing Foundry and Hardhat"
author: mattstam
date: "2022-11-01"
category: Magicians > Tooling
tags: [solidity]
url: https://ethereum-magicians.org/t/solidity-template-a-modern-solidity-contract-template-utilizing-foundry-and-hardhat/11558
views: 872
likes: 1
posts_count: 1
---

# solidity-template: a modern Solidity contract template utilizing Foundry and Hardhat

Introducing [solidity-template](https://github.com/mattstam/solidity-template), a Solidity template for Ethereum smart contracts. It optimally combines two extremely powerful frameworks:

- Foundry
- Hardhat

Most contract repositories out there in the wild choose either one or the other. Both offer powerful tools for contract development, and although there is *some* overlap in their functionality, there is a multitude of reasons that you should be utilizing both:

- Complete test coverage using Forge to cover the raw contract logic and basic scenarios, and Hardhat the complex user interactions.
- Maximum suite of tools for contract debugging, deployment, gas measurements, etc.
- Reference for on-chain developers writing contracts that call these contracts in your Unit Test files to see the expected usage in Solidity.
- Reference for off-chain developers writing clients that call these contracts in your Integration Test files to see the expected usage in JavaScript (TypeScript) and Ethers.js.

The latter case has already proven to be extremely useful for a new project [Git Consensus](https://github.com/git-consensus/contracts), where just pushing integration test code gave examples for the frontend devs concurrently to know how they need to prepare input parameters for the contract functions. This will only be more relevant as the community shifts to [patterns](https://github.com/dragonfly-xyz/useful-solidity-patterns/tree/main/patterns/off-chain-storage) that encourage loaded input parameters for gas savings.

Of the repositories that *do* combine try to combine both Foundry and Hardhat, none are optimized together in a way that makes them convenient to develop in. This is due to the split between how Foundry handles dependencies (git submodules located in `/lib`) and Hardhat handles dependencies (managed with [NPM](https://www.npmjs.com/)). Nothing felt up-to-date with contract development best practices in 2022.

This gap in a fully-featured, modern Solidity template that utilizes both frameworks inspired me to publish [solidity-template](https://github.com/mattstam/solidity-template) - not only is it optimized for using both, but it also offers a lot of the boilerplate a project will be able to utilize to streamline development: GitHub Actions, interactive CLI, linting, doc generation, deployment address tracking, contributor guides, etc.

This template includes an easy-to-follow example [Counter.sol](https://github.com/mattstam/solidity-template/blob/master/contracts/Counter.sol), with its interface [ICounter.sol](https://github.com/mattstam/solidity-template/blob/master/contracts/interfaces/ICounter.sol), Unit Test file [Counter.t.sol](https://github.com/mattstam/solidity-template/blob/master/contracts/test/Counter.t.sol), and Integration Test file [counter.test.ts](https://github.com/mattstam/solidity-template/blob/master/integration/counter.test.ts).

If you like it, definitely give it a ![:star:](https://ethereum-magicians.org/images/emoji/twitter/star.png?v=12) so you can remember to use it for your next project!
