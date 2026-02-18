---
source: magicians
topic_id: 17696
title: "Discussion: Standardizing ERC-4337 Account Execution Interface"
author: karandeep
date: "2023-12-27"
category: Web > Wallets
tags: [erc, wallet, account-abstraction, eip-4337, accounts]
url: https://ethereum-magicians.org/t/discussion-standardizing-erc-4337-account-execution-interface/17696
views: 1442
likes: 4
posts_count: 3
---

# Discussion: Standardizing ERC-4337 Account Execution Interface

# Standardizing ERC-4337 Account Execution Interface

We’d like community feedback on implementing a minimal smart contract account with standardized execution methods for ERC-4337 accounts. This proposal does not suggest any change on ERC-4337 but a separate ERC if needed.

## Motivation

ERC-4337 abstracts account validation and execution by introducing userops and specifying how they should be validated. Different smart account standards (ERC 6900, 6551, 7579) specify their execution interface. ERC-4337 provides flexibility for account builders to design custom execution methods. It suggests a workflow but lacks a standardized execute() method or specific execution functionality, as intended.

Developers are creating different types of execution workflows using some combination of these methods, along with the ERC-4337 standard.

- execute(target, value, calldata): This method enables the execution of a single transaction. It requires specifying the target address, value, and calldata.
- executeBatch(target[], value[], calldata[]): This method supports the execution of a batch of transactions. It expects arrays of target addresses, values, and calldata.
- delegateExecute(target, calldata): This method facilitates transaction execution through delegate calls. It involves specifying the target address and calldata for delegate execution.

## Problems

Not standardized, not compatible: Developers may use the same methods, but each team is naming them differently. If a provider names methods differently, their call data will differ from another provider with their execution method names. Developers using the account provider SDK can’t use another SDK to interact with the same account. They must use multiple SDKs to create the same features (execute), even if everything else remains identical except for the name difference.

## Solution: Minimal Smart Contract Account Which Executes

Developers require a standardized interface defining the execution functionality of ERC-4337 accounts. We can use the same method names and create a standard for a minimal smart contract account. We propose naming execution methods as follows.

- execute(target, value, calldata): This method enables the execution of a single transaction. It requires specifying the target address, value, and calldata.
- executeBatch(target[], value[], calldata[]): This method supports the execution of a batch of transactions. It expects arrays of target addresses, values, and calldata.
- delegateExecute(target, calldata): This method facilitates transaction execution through delegate calls. It involves specifying the target address and calldata for delegate execution.

## Replies

**zeroknots** (2023-12-29):

Why does this need another standard vs. just adopting ERC-7579 exec functions.

Sidenote: there is a reason why ERC-7579 and ERC-6900 is **not** using `(target[], value[], calldata[])`.

using structs for batched Tx is cheaper on gas.

---

**karandeep** (2023-12-29):

Thanks [@zeroknots](/u/zeroknots) for your comments.

By *listing methods execute, executeBatch, or delegateExecute*, I just wanted to convey the pattern being used. Using structs for batched transactions can save gas costs. If creating a separate ERC, it should have the most gas-efficient way of doing it.

On *Why does this need another standard vs. just adopting ERC-7579 exec functions*, did you mean why not just adopt ERC-7579 instead of creating a new standard? Or is there another intention behind *just adopting ERC-7579 exec functions*? I’m confused. Are you suggesting that developers should create an account which uses just ERC-7579 exec functions for creating a minimal smart contract account? If so, this may not be clear to developers as it involves selecting specific functionalities from the other standards

On *why a separate standard*, I think it would make things clear and standardized for developers when implementing the standard. They would know exactly what to implement in order to create a minimal usable smart contract account.

If the community agrees on this, then why not make this standard a starting point for modular accounts (6900 or 7579 as both have version of this inside there standard)? This would be a more general transition and will also simplify the modular standards to focus exactly on making account modular.

Any feedback is welcomed! I’m eager to learn and understand more.

