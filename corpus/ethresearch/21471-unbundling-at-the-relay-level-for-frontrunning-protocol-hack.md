---
source: ethresearch
topic_id: 21471
title: Unbundling at the Relay Level for frontrunning protocol hacks
author: meridian
date: "2025-01-17"
category: Security
tags: [mev, security]
url: https://ethresear.ch/t/unbundling-at-the-relay-level-for-frontrunning-protocol-hacks/21471
views: 405
likes: 1
posts_count: 2
---

# Unbundling at the Relay Level for frontrunning protocol hacks

---

## Abstract

We propose the implementation of two new Ethereum JSON-RPC methods, `eth_clandestineSubmitTransaction` and `eth_clandestineSubmitBlock` for MEV Relays. These methods allow direct interaction with MEV Boost Relays, providing advanced mechanisms for transaction and block submission that are ‘clandestine’ in nature.

The proposal aims to mitigate risks associated with malicious activities (i.e. hacks of projects) by front running the hacker’s transaction and ensuring that the block that includes the ‘clandestine transaction’ wins by *lying to the validator about the value of its proposed block*. This ensures exclusivity by the relay that the successful mitigation is completed. The funds that are recovered must be returned to the project, with an optional proportion being retained for a pooled insurance treasury less payments to participating security companies for their services.

This proposal requires multiple security firms to participate by fuzzing transactions and reaching a quorum such that there is some agreement as to a malicious transaction. This method need not also be used for frontrunning a transaction hack, as it can also be used by security collectives such as SEAL911 for submitting whitehack transactions.

## Motivation

Advances in fuzzing by various security companies have proven their ability to find just in time malicious transactions and attempt to ‘front run’ (i.e. outbid the gas and fees paid to validators) them to protect the vulnerable project. However, this leads to a tit for tat increase in gas costs and fees paid in an attempt to ‘front run the front run’. By leveraging the trusted nature of the MEV Relay we can ‘lie’ to the validator ensuring that our protected transaction (called ‘clandestine’) is chosen unambiguously.

1. ~95% of DeFi hacks would be eliminated.
2. Require multiple security companies to participate.
3. Additional benefits by ensuring intrablock state consistency (by virtue of fuzzing transactions).
4. Hacks can still occur, a hacker can spin up a validator and build a block locally to execute the attack.
5. A portion of the ‘recovered’ funds can be retained for funding a cooperative insurance pool for projects, to compensate the security firms for their work and development.
6. Adds explicit support for security cooperation with security groups like SEAL911 by providing a way to also submit transactions that are related to preventive measures such as a transaction that updates some protocols state (e.g. disabling depositing to the project because of a newly disclosed vulnerability).
7. LST Operators/Protocols no longer have contentious issues of ‘receiving stolen goods’, they can also be compensated from the ‘recovered funds’. Example: Validators would get 2% of the total recovered funds.

## Specification

> All methods must be signed with an address that is whitelisted ahead of time. Authorization: Requires the Ethereum-Signature header for permission.

### Methods

#### eth_clandestineSubmitTransaction

**Description:** Submits a confidential transaction directly to an MEV Boost Relay for prioritized block inclusion, with optional parameters for enhanced control.

**Parameters:**

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| from | string | Yes | Address sending the transaction. |
| to | string | Yes | Address receiving the transaction. |
| value | string | Yes | Amount of ether to send (in wei). |
| blockNumber | string | Yes | Block number for transaction inclusion (hexadecimal). |
| data | string | No | Data payload to send with the transaction (hexadecimal). |
| multiplier | number | No | Multiplier to modify relay bid. |
| blockGasLimitIncrease | number | No | Amount by which to increase the block gas limit. |
| TargetTransactionHashes | array of strings | Yes | Array of transaction hashes targeted for front-running protection. |

**Example Request:**

```json
{
  "jsonrpc": "2.0",
  "method": "eth_clandestineSubmitTransaction",
  "params": {
    "from": "0xYourAddress",
    "to": "0xRecipientAddress",
    "value": "0x9184e72a000",
    "blockNumber": "0x5BAD55",
    "data": "0xOptionalData",
    "multiplier": 1.2,
    "blockGasLimitIncrease": 2000000,
    "TargetTransactionHashes": [
      "0xTargetTransactionHash1",
      "0xTargetTransactionHash2"
    ]
  },
  "id": 1
}
```

**Example Response:**

```json
{
  "jsonrpc": "2.0",
  "result": "0xTransactionHash",
  "id": 1
}
```

#### eth_clandestineSubmitBlock

**Description:** Submits an entire block for exclusive processing by an MEV Boost Relay.

**Parameters:**

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| blockHeader | string | Yes | RLP-encoded block header. |
| transactions | array of strings | Yes | Array of RLP-encoded transactions. |
| uncles | array of strings | No | Array of RLP-encoded uncle headers. |
| blockNumber | string | Yes | Block number for submission (hexadecimal). |
| blockGasLimitIncrease | number | No | Amount by which to increase the block gas limit. |

**Example Request:**

```json
{
  "jsonrpc": "2.0",
  "method": "eth_clandestineSubmitBlock",
  "params": {
    "blockHeader": "0xRLPEncodedBlockHeader",
    "transactions": [
      "0xRLPEncodedTransaction1",
      "0xRLPEncodedTransaction2"
    ],
    "uncles": [
      "0xRLPEncodedUncle1"
    ],
    "blockNumber": "0x5BAD55",
    "blockGasLimitIncrease": 2000000
  },
  "id": 1
}
```

**Example Response:**

```json
{
  "jsonrpc": "2.0",
  "result": "0xBlockHash",
  "id": 1
}
```

### eth_sendPriorityTransaction

> This is meant for preventive measures not for front running.

> [!NOTE]
> This method is optional and really not necessary, I only include it for soliciting feedback

**Purpose**: Broadcast a transaction at the top of a target block, bypassing certain conventional mempool checks to enable ultra-low-latency inclusion.

**Key Features**:

- Priority Inclusion: Ensures the transaction appears at the block’s top.
- Bypass Checks: Ignores nonce and gas price validations; the user is responsible for correctness.
- Optional Multiplier: Adjusts the relay’s bid or payment mechanism.

```json
{
  "jsonrpc": "2.0",
  "method": "eth_sendPriorityTransaction",
  "params": {
    "from": "0xYourAddress",
    "to": "0xRecipientAddress",
    "value": "0x9184e72a000",
    "blockNumber": "0x5BAD55",
    "data": "0xOptionalData",
    "multiplier": 1.2,
  },
  "id": 1
}
```

## Security Company Participation Requirements

### Quorum Definition

1. Threshold Value: A quorum is a pre-defined threshold of participants (e.g., “at least 2 out of 3,” “3 out of 5,” or some other n-of-m formula). This threshold is typically set by the relay operator or via on-chain governance.
2. Qualified Voters: Only whitelisted parties (in this context, vetted security providers) are permitted to participate in the quorum.

### Purpose of the Quorum

1. Shared Risk and Validation: By requiring multiple providers to submit matching front-run requests for the same transaction hash, the network ensures that:

No single party can exploit the mechanism unilaterally.
2. Multiple trusted entities corroborate the same target.
3. Fraud Mitigation: Requiring multiple participants to cooperate limits the likelihood of malicious or frivolous front-run attempts (e.g., spamming the relay with unrelated target hashes).
4. Collective Decision-Making: Because providers must agree on which transaction to front-run or protect, the final submission reflects a collective judgment rather than an individual’s unilateral action.

---

### How a Quorum is Formed

1. Target Hash Agreement:

Each whitelisted provider independently identifies a transaction hash (the frontRunTargetHash) they believe warrants front-running.
2. Providers submit this hash, along with their own credentials and signature, via eth_clandestineSubmitTransaction.
3. Matching Logic:

The relay’s Quorum Manager compares incoming requests.
4. When multiple requests reference the same transaction hash, they are grouped together.
5. Threshold Check:

The Quorum Manager checks if the number of providers referencing the same hash meets or exceeds the threshold (e.g., 2 or 3).
6. If below the threshold, the request either stays in a pending state until more providers confirm the same hash or it is simply rejected.
7. If equal to or above the threshold, the group is deemed to have formed a valid quorum.

---

### Request Selection (Round Robin)

1. Round-Robin Scheduling:

Once quorum is reached for a particular target hash, the Quorum Manager will select the “winning” request using a round-robin approach among providers who submitted that hash.
2. This ensures fair rotation and prevents one single provider from always monopolizing front-run opportunities.

### Transaction Execution and Proceeds Allocation

1. Transaction Finalization:

Once a front-run transaction is selected to proceed (i.e., becomes the “winning” request), it is forwarded to the validator through the relay as a clandestine transaction.
2. The transaction will then execute with the specified front-running logic (e.g., outbidding a certain other transaction, or exploiting an arbitrage).
3. Proceeds Distribution:

A portion of any recovered MEV or proceeds is then allocated to the “winning” submitter, as specified in the proceedsAddresses, which is a MultiSig address controlled by the participating security companies and relay operators.
4. The recovered funds are returned to the project. Providers who participated in reaching quorum may also receive a smaller or proportional share.
5. Quorum Re-Entry:

After the front-run request is processed, the relay updates its internal state to reflect that the winning provider has just exercised their slot in the round-robin.

## Concluding remarks

I would like to thank Justin Drake for entertaining the idea when first discussed, and to Vasily ([p2p.org](http://p2p.org)) for the most helpful suggestion of the quorum agreement. I would also like to thank fuzz.land, dedaub, and blocksec for their helpful input.

MEATBAL may not be the best name, maybe the world computer needs a CPU: a Clandestine Protection Unit.

## Replies

**meridian** (2025-01-24):

I re-named this proposal to make the title more informative, cheers

