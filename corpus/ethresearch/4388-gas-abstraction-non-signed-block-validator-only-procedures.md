---
source: ethresearch
topic_id: 4388
title: "Gas Abstraction: Non signed \"block validator\"-only procedures"
author: 3esmit
date: "2018-11-27"
category: Applications
tags: []
url: https://ethresear.ch/t/gas-abstraction-non-signed-block-validator-only-procedures/4388
views: 3104
likes: 3
posts_count: 6
---

# Gas Abstraction: Non signed "block validator"-only procedures

This proposal would be for an improvement on Gas Abstraction proposal, and embed it within layer 0/1.

If a transaction that don’t uses `msg.sender` and uses `gas.price == 0`, the signature verification is just bloating and the result of it is never effectely used to a state change.

To improve this, EVM would support a new type of call, which considers `gas.price == 0`  and `msg.sender` is not available (throws if called, would also fails to compile).

The gas abstraction contract would then be able to pay the ERC20 gas directly to `block.coinbase`, as the block don’t uses any ETH (as gas.price is zero) and don’t reads `msg.sender` it could be valid with no risk to consensus.

Ethereum Block Validators (PoS) would be able to test if those transactions are valid, and insert them in the block transactions which pay ERC20 they accept.

I would like feedback from devs to see if this makes sense and if (and how) I should continue with this EIP.

## Replies

**3esmit** (2019-09-16):

Gas Abstraction is possible thanks to CREATE2. An update of the mining/validator node (no hard fork required) would be important to enable gas abstraction, so this “meta transactions” can be included directly by miners, which configure ERC20 they accept.

An optional EVM consensus change can be implemented to support “validator functions” in the contracts, which would enable block creators to call a contract without a sender, this special transactions cannot use `msg.value` or `msg.sender` and requires `gas.price == 0`, and only have destination and data, and if fails, then it would cause an invalid block. This transactions would be used to call the gas relay functions, which would use `block.coinbase` for the meta-transaction ERC20 gas payment.

Is this idea bad? Seems so possible and good to end users.

---

**MicahZoltu** (2020-09-09):

I would rather see other solutions being discussed to address the problem of gasless transactions (like Rich Transactions).  The benefits of adding this don’t feel like they are worth the complexity, as they only decrease the cost of executing these transactions by a tiny margin compared to just having a signed message that has to be recovered.

---

**MicahZoltu** (2020-10-27):

How would this interact with [EIP-1559](https://eips.ethereum.org/EIPS/eip-1559)?

---

**3esmit** (2020-10-28):

It doesn’t interacts with EIP-1559.

In case EIP 1559 get’s approved, COINBASE CALLs wouldn’t change, meaning that contracts using this won’t be affected, but also do not benefit from EIP-1559.

This might be desirable for some contract, e.g. a contract that uses coinbase calls for some type of “merged mining” in ethereum, where there is no payment of gas, instead the execution of a function in the contract is in the best interest of coinbase to include.

For account contracts, their nonce and rules for transaction validation are programmed in their own code, and some could be made as a Upgradable Proxy, so they could also upgrade their logic to be in a equivalent format as EIP-1559.

For reference, Coinbase calls are not even compatible with EOA transactions, the whole use-case is defined as smart contract logic. Coinbase calls can be used to take advantage of mining properties, in case of “Gas Abstraction”, it uses the availability & randomness of participants, and miner economical incentives to execute something that makes coinbase get a fee.

---

**MicahZoltu** (2020-10-29):

EIP-1559 requires that all transactions burn some ETH.  Which account would supply the ETH required for burning if this were accepted in an EIP-1559 world?

