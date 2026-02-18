---
source: magicians
topic_id: 13471
title: Globally available tx opcodes in solidity
author: 0xTraub
date: "2023-03-21"
category: Magicians > Primordial Soup
tags: [opcodes, solidity]
url: https://ethereum-magicians.org/t/globally-available-tx-opcodes-in-solidity/13471
views: 694
likes: 1
posts_count: 4
---

# Globally available tx opcodes in solidity

I’ve been thinking a lot about the future of account abstraction now that ERC-4337 is live. Is there a reason why there aren’t more globally available variables in solidity. For example, we have tx.origin, which is useful for getting the EOA that initiated a transaction, but why not more? Is there a technical reason these aren’t included (other than a desire to maintain simplicity of the EVM)?

Example:

`tx.entryPoint` - `ENTRYPOINT` opcode - Define the top level contract a tx was initiated by calling

`tx.data` -  `TXDATA` - Define the top level calldata used in calling tx.entryPoint

`tx.value` - `TXVALUE` - The top level value in Ether used to call tx.entryPoint

`tx.sig` - `TXSIG` - first four bytes of the calldata used on tx.entryPoint

My main thoughts for how this would be used is to allow future proofing of application-whitelisting under account-abstraction. Currently the standard is to use `require(tx.origin == msg.sender || isWhitelisted(msg.sender))`. However once everyone switches to smart-wallets this will become unsustainable due to everyone not being able to be whitelisted at scale. Perhaps if you introduced a new opcode for this kind of information you could have whitelist implementations which use things like

`require(tx.entryPoint == ENTRYPOINT_CONTRACT && tx.sig == HANDLE_USEROPS_SIG)`

This would allow support for smartWallets interacted with through the ERC-4337 entryPoint contract. It would also allow contracts to screen out transactions to prevent attacks like flashloans. Since the top level call must be to the lending contract, no flash loan can occur to manipulate the oracle before the collateral is valued.

It seems like a pretty simple opcode to include without too much technical difficulty to implement by execution-client teams, so there must be some reason it doesn’t exist?

## Replies

**RobAnon** (2023-05-01):

[@SamWilsn](/u/samwilsn) this is pretty close to what you and I had previously discussed.

---

**SamWilsn** (2023-05-01):

I can’t really speak for the historical reasons why these opcodes don’t exist (I suspect it’s because no one has asked for them yet.)

If I were a core dev, I might push back on these suggestions simply because they increase the surface area of stuff that might break as Ethereum evolves. For example, `tx.entryPoint` might interact with a hypothetical specification for [rich transactions](https://eips.ethereum.org/EIPS/eip-2803).

---

**0xTraub** (2023-05-01):

[@SamWilsn](/u/samwilsn) That’s a very fair point about rich transactions. I think one way to handle this would to just have the opcode return `caller` if it’s from an EOA. I think the reason this opcode may be needed is because of the future difficulty in identifying the difference in wallet types due to AA. Then you could do things like "if (tx.entryPoint != tx.origin) {}`

I’m open to ideas on potential implementation if you think there’s a market for this kind of opcode.

