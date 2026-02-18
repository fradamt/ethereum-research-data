---
source: magicians
topic_id: 25382
title: "InheritableEOA: inheritance/recovery over inactivity (with EIP-7702)"
author: zergity
date: "2025-09-08"
category: Magicians > Primordial Soup
tags: [social-recovery, eip-7702, smart-account]
url: https://ethereum-magicians.org/t/inheritableeoa-inheritance-recovery-over-inactivity-with-eip-7702/25382
views: 164
likes: 2
posts_count: 2
---

# InheritableEOA: inheritance/recovery over inactivity (with EIP-7702)

This proposal outlines a trustless EOA inheritance mechanism using EIP-7702, enabling key recovery for lost keys (not stolen) while preserving the familiar EOA and hardware wallet UX. This `7702` contract allows any EOA (including hardware wallets) to opt-in for a trustless inheritance solution.

The core principle is the “*proof of unchanged nonce*” over a pre-configured inactivity period. Any transaction from the original private key during this period invalidates the inheritance process. This means that even if the inheritor account is quietly stolen, regular activity from the original private key is sufficient to cancel any rogue inheritance attempt.

The main convenience of this solution is that it only requires a single 7702 delegate transaction for preparation. Any inheritance or recovery work can be done **AFTER** the key is lost.

## Implementation

InheritableEOA is a Solidity contract designed to be delegated to by an EOA using EIP-7702 transactions. It implements inheritance logic where an inheritor can assume full access to an account after proving the account nonce hasn’t changed over a specified delay period.

The project verifies account state (nonce, balance, storage root, code hash) against Ethereum’s state root using Merkle Patricia Trie proofs and RLP decoding.

## Why InheritableEOA?

- Zero disruption to normal usage - The EOA continues to work exactly as before. Send transactions, sign messages, interact with dApps - nothing changes. EIP-7702 delegation is purely additive.
- Automatic protection against hijacking - Any regular activity from the EOA (sending a transaction, deploying a contract, etc.) increments the nonce and automatically invalidates any pending inheritance claims. Simply using your wallet cancels hijacking attempts.
- No trusted third parties - Inheritance is verified entirely on-chain using Merkle Patricia Trie proofs against Ethereum’s state root. No oracles, multisigs, or centralized services required.
- Configurable and revocable - The EOA owner can change the inheritor, adjust the delay period, or clear the configuration entirely at any time.
- Lightweight preparation - All the heavy works can be done AFTER the key is lost. Hence the preparation steps are super convenient: 1 tx for 7702, 1 tx for setup the parameters.

## Source Code



      [github.com](https://github.com/Zergity/ieoa)




  ![image](https://opengraph.githubassets.com/61f3f6d069795a849b192f1ac5e00fd8/Zergity/ieoa)



###



Contribute to Zergity/ieoa development by creating an account on GitHub.

## Replies

**zergity** (2025-11-21):

[github.com](https://github.com/Zergity/ieoa)




  ![image](https://opengraph.githubassets.com/a12427bcc9ddec690eb15c87c4da4683/Zergity/ieoa)



###



Contribute to Zergity/ieoa development by creating an account on GitHub.










An implementation is finished with:

- A minimal BareAccount code
- A standalone BlockHashRecorder for old blockhash tracking
- Merkle proof logic from solidity-merkle-trees

Contract is properly test with `anvil` via 7702 delegation transaction and actual merkle data from `eth_getProof`.

