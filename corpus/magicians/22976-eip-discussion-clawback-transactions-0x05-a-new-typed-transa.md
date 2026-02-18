---
source: magicians
topic_id: 22976
title: "[EIP Discussion] Clawback Transactions (0x05) – A New Typed Transaction for Delayed Finalization"
author: leonafrica
date: "2025-02-24"
category: EIPs > EIPs informational
tags: []
url: https://ethereum-magicians.org/t/eip-discussion-clawback-transactions-0x05-a-new-typed-transaction-for-delayed-finalization/22976
views: 191
likes: 11
posts_count: 6
---

# [EIP Discussion] Clawback Transactions (0x05) – A New Typed Transaction for Delayed Finalization

This proposal introduces a new Ethereum transaction type (0x05) for clawback-enabled transactions, allowing a sender (or authorized recovery address) to reclaim funds within a predefined clawback period **before final settlement**.

The goal is to enhance security against:

- Accidental transfers (e.g., sending ETH to the wrong address)
- Wallet hacks (e.g., reclaiming stolen funds before they are withdrawn)
- Exchange exploits (e.g., preventing large-scale thefts like Bybit’s $1.5B hack)

**Proposal Draft:** [PR](https://github.com/ethereum/EIPs/pull/9405)

---

## Why a New Transaction Type?

Ethereum supports typed transactions (EIP-2718), meaning we can introduce new transaction formats without modifying existing ones.

- EIP-1559 (0x02) doesn’t support delayed execution.
- EIP-2930 (0x01) only optimizes storage reads, not finalization.
- Smart contracts add extra gas costs and can’t protect EOAs.
- A new type (0x05) ensures clawback transactions are modular & efficient.

---

## Technical Overview

- ClawbackPeriod – Number of blocks before finalization (e.g., 30 mins).
- ClawbackAuth – A designated address that can reclaim funds (optional).
- Final Settlement – If no clawback occurs, the transaction is fully irreversible.
- Gas Refunds – Should clawbacks trigger partial gas refunds (EIP-3529)?

### Transaction Format (EIP-2718 Typed Transaction)

| Field | Type | Description |
| --- | --- | --- |
| chainId | uint256 | Ethereum chain ID |
| nonce | uint64 | Unique transaction nonce |
| recipient | address | Target recipient address |
| value | uint256 | Amount of ETH to transfer |
| clawbackPeriod | uint64 | Delay before finalization |
| clawbackAuth | address | Authorized recovery address (optional) |
| yParity, r, s | uint256 | ECDSA signature fields |

---

## Discussion Points

- Should clawback periods be fixed (e.g., max 1 hour) or flexible?
- Are there concerns about potential abuse (e.g., spam attacks)?
- How should wallets & clients handle clawback transactions UX-wise?
- Would an EVM precompile be more gas-efficient than a transaction type?

Looking forward to feedback from Ethereum devs, researchers, and the community!

## Replies

**jochem-brouwer** (2025-02-24):

How does the current proposal mitigate the attack scenario B? In this scenario, the attacker can use a default transaction to take the funds. If a clawback transaction is initiated instead, the attacker can clawback and immediately send all funds using a normal transaction. Alternatively it could lock up the funds forever, or being kept in the loop Clawback Tx → Clawback → Clawback Tx until all funds are spend on gas?

For this EIP I would strongly recommend to write this feature in a smart contract instead of adding a new transaction type.

---

**wjmelements** (2025-02-25):

Clawbacks can be done with smart contracts. Instant settlement is the default. There doesn’t need to be a transaction type.

---

**marchhill** (2025-02-25):

I agree that this seems like something best solved at the application level though smart contracts / accounts. For EOA support I would consider whether [EIP-7702](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7702.md) can be used.

I don’t really see the benefits that you mention. For accidental transfers if you go to the effort of specifying a clawback window and recovery address then why not instead take more care to double check the address you are sending to? For preventing attacks this would require the attacker to choose to send a clawback transaction, of course they would just send a normal one.

---

**bomanaps** (2025-02-25):

With all that was pointed out by [@marchhill](/u/marchhill) and [@jochem-brouwer](/u/jochem-brouwer) , this will also impact Ethereum’s settlement finality.

Ethereum’s current design emphasizes irreversible finality, which is a cornerstone of its trust model. And Introducing reversible transactions, even for a limited period, could undermine this principle.

Users and applications relying on immediate finality (e.g., DeFi protocols, exchanges) may face uncertainty during the clawback period.

It can be a Potential for Abuse

- Spam Attacks:
- Griefing:
And also need to track and manage clawback periods could add complexity to Ethereum’s state management.

---

**leonafrica** (2025-02-25):

Thank you all for your valuable insights and feedback so far!

I’m carefully reviewing the points raised, particularly around potential attack vectors, finality concerns, and the feasibility of handling clawbacks at the smart contract level versus the protocol level. These are critical considerations, and I want to ensure all perspectives are thoughtfully addressed.

In the meantime, I encourage you to review the [EIP draft](https://faint-stool-b93.notion.site/Clawback-Transactions-for-EOAs-1a5352c1ca2580f0888dfa89d202d332) - especially the section Hybrid Approach: Combining CeFi & DeFi Security, along with the surrounding discussion on the smart contract alternative and the rationale for a protocol-level approach.

I’ll be compiling a detailed response soon to address each concern individually. For those who haven’t weighed in yet, I’d love to hear your thoughts! Every piece of feedback will be considered as the proposal evolves.

Looking forward to continuing this discussion and refining the best approach together.

