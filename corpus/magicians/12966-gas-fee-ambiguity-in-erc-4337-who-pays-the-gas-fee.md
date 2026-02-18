---
source: magicians
topic_id: 12966
title: Gas fee ambiguity in ERC-4337. Who pays the gas fee?
author: DavidKim
date: "2023-02-17"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/gas-fee-ambiguity-in-erc-4337-who-pays-the-gas-fee/12966
views: 735
likes: 1
posts_count: 1
---

# Gas fee ambiguity in ERC-4337. Who pays the gas fee?

Hi everyone, thanks for reading this question. This was a question I got while reading the AA standard proposal.

I hear that by imposing account abstraction specified in ERC-4337 EOA is not the only one that can initiate a transaction.

What I’m confused about is the actual entity that pays the gas fee and the relationship with the `paymaster`.

[![UserOperation mempool](https://ethereum-magicians.org/uploads/default/original/2X/1/1fc73c0e8f9fa6943b0bd33622542f22250d5bf2.png)](https://i.stack.imgur.com/mFcvN.png)

From [Vitalik’s article](https://medium.com/infinitism/erc-4337-account-abstraction-without-ethereum-protocol-changes-d75c9d94dc4a), it says that the **bundler** is paying for the transaction.

*The bundler pays the fee for the bundle transaction in ETH, and gets compensated though fees paid as part of all the individual UserOperation executions. Bundlers would choose which UserOperation objects to include based on similar fee-prioritization logic to how miners operate in the existing transaction mempool. A UserOperation looks like a transaction; it’s an ABI-encoded struct that includes fields such as*:

In this case, is the bundler an EOA that originates the transaction? Also, if the bundler pays the fee for transaction for each UserOperation what will it get in return? (e.g. Paymaster pays the bundler the transaction fee it gives?)

To sum up,

- Is bundler an EOA that monitors the mempool of UserOperation which initiates the transaction?(If it’s the case, then it’s still the EOA that originates the tx right?)
- What is the incentive model of Bundler? and the relationship between paymaster and bundler? (Why should the bundler pay the gas fee for Bundle transaction that includes UserOperation)
- If Paymaster pays for the gas fee on behalf of a user, should it hold native ETH balance to pay it? Can a Paymaster pay the Entrypoint Contract with an ERC20 token?

Thank you for answering in advance ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

----- UPDATE -----:

After doing some research with the AA and the history of it(e.g. EIP-3074 & EIP-2938) I noticed that the question was incorrect. The answer to it was that there is no consensus layer changes to the EVM so still contracts(CA) would not be able to initiate a transaction like EIP-2938 is proposing to do.

This EIP-4337 is using bundler as a relayer(decentralized) to make a transaction instead, and providing a standard interface of contracts & RPCs to standardize the system for this AA system (mempool + contracts - entrypoint, wallets, paymaster, etc).
