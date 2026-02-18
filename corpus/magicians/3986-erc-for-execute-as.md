---
source: magicians
topic_id: 3986
title: ERC for "Execute as"
author: fubuloubu
date: "2020-02-07"
category: ERCs
tags: [wallet]
url: https://ethereum-magicians.org/t/erc-for-execute-as/3986
views: 1176
likes: 4
posts_count: 5
---

# ERC for "Execute as"

I’ve been tossing around this concept of being able to perform actions as different types of smart contracts with group memberships like Multi-sigs, DAOs, and Smart Contract wallets, and I think there really needs to be a standard built for how this works.

Here’s a tweet for teh lulz:

https://twitter.com/fubuloubu/status/1225476091642548228

---

# The Problem

Smart contracts can’t do things by themselves, only with outside parties (with private keys) initiating a transaction and paying the gas. However, we’ve devised many different types of “group” contracts that require 1 or more keys with certain permissioned rights to perform an operation for assets under the contract’s control.

The problem is that sometimes the actions I want to perform in dapps (like upgrading a Resolver in an ENS entry my Multi-sig owns) where the asset is owned by the “group” contract, but almost all applications assume the keyholder is the party of interest when using their interface. This is not a good assumption!

I want to be able to go to an interface, have some mechanism of stating “Execute as”, and then have the transaction I would normally perform as a keypair “translated” into how the group contract I am interacting with expects to receive and interact with this action, whether it be a number of confirmations (multi-sig), voting (DAOs), or simply authentication that the keypair is allowed to perform this action (smart contract wallets, limits and beneficiaries for multi-sigs and DAOs).

---

# The Solution

I have no idea what the solution should look like, I wanted to talk about it here to garner a better idea of how this might best be implemented between various wallets, dapps, or ERC interfaces. The problem is made harder that multiple such types of contracts are in moderate use, and almost nothing is standardized. I think this puts an ERC out of the question, at least one that attempts to standardize interfaces for these actions.

A better attempt might be at creating a “registry” of how to check and perform a few basic things, such as:

1. Lookup/authentication that a keypair is an owner/member of a given contract; or, which contract(s) a keypair is a owner/member of
2. How to translate an Ethereum transaction into a transaction that is suitable for submission to the contract
3. How to get feedback on the state of that transaction, and whether it requires further action on behalf of the user to process (or otherwise is waiting on some confirmation/voting process to continue)

I have no idea if this makes sense to integrate at the wallet level, but that seems to be an attractive option, allowing people to “Add” group membership of some contract they are party to and have the ability to perform actions as that group in exactly the same way they would their normal keypairs. This would reduce the work required of dapp makers, but increase the burden on wallet makers as an advanced feature.

I also have no idea how to integrate this proposal into various dashboards that these group contracts use, like a DAO’s voting dashboard, or a Multi-sig’s management dashboard. I feel like they could just as easily be overlays on what a wallet does (at least a minimally functional overlay that links to the full dashboard), but that also requires a degree of standardization I don’t think exists.

---

If someone wants to talk further about this at ETHDenver, please let me know.

## Replies

**Amxx** (2020-02-07):

You should have a look at [ERC734](https://github.com/ERC725Alliance/erc725/blob/master/docs/ERC-734.md) (the old ERC725). FYI, this effort was made about 2 years ago, and lead nowhere but to many incompatible solutions.

I’ll be un EthDenver

---

**fubuloubu** (2020-02-07):

Yeah, I noticed there were quite a few attempts made at this that didn’t seem to pan out. I think with the rise of “Just DAO it” and Gnosis Safe/Argent gaining so much traction, now might be a really good time to get this working though.

---

**3esmit** (2020-02-15):

What do you think about EIP-1271?

For me it seems to solve this problem.

---

**fubuloubu** (2020-02-16):

It seems… Related, but not quite what I was going for. The general idea is to build a standard where it would be possible to build a mechanism where a smart wallet and an EOA could perform the same action, by having a lookup of how to make that happen.

So, it’s not a signature standard persay, merely a “translation” standard for how to convert a transaction (that an EOA would directly sign) into something useful for smart wallets, DAOs, meta-txns, etc. by “converting” to another transaction format. A secondary part of the standard would be another “translation” for how to view it’s progress and completion status.

I don’t want to specify the “how” of the conversion, just have a standard way of referring to what would be many different ways of performing that conversion.

