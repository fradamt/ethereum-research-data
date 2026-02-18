---
source: magicians
topic_id: 27363
title: ERC-XXXX Conditional Tokens
author: serverConnected
date: "2025-12-31"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-xxxx-conditional-tokens/27363
views: 194
likes: 5
posts_count: 3
---

# ERC-XXXX Conditional Tokens

| eip | title | description | author | status | type | category | created | requires |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| XXX | Conditional Tokens | An interface for tokens representing positions on outcomes that can be split, merged and redeemed based on oracle reported results | shafu (@shafu0x), Behzad (@bitnician), Sarvad (@serverConnected), Ynyesto (@ynyesto), lajarre (@lajarre) | Draft | Standards Track | ERC | 2025-12-16 | 1155 |

## Table of Contents

- Abstract
- Motivation
- Adoption and Usage
- Specification

Condition Lifecycle
- Position Operations
- View Functions
- Events

[Example Lifecycle](#example-lifecycle)
[Security Considerations](#security-considerations)
[Copyright](#copyright)

## Abstract

This ERC extends [ERC-1155](https://github.com/ethereum/ercs/blob/master/ERCS/erc-1155.md) with conditional tokens that allow participants to create and settle positions on future outcomes.

It introduces three core operations. Splitting collateral into outcome positions, merging positions back into collateral and redeeming positions after oracle resolution.

## Motivation

Prediction markets have demonstrated product market fit through platforms like Polymarket. The Gnosis Conditional Tokens framework from 2019 pioneered the core primitives of splitting, merging, and redeeming positions based on oracle outcomes. But there is no formal ERC standard, limiting interoperability.

To enable a thriving ecosystem of prediction markets we need a standard interface. This ERC addresses this through three core operations:

1. Condition Preparation: Registers a condition with an oracle, question identifier and outcome count.
2. Position Splitting & Merging: Converts collateral into outcome tokens (split) or recombines them (merge).
3. Redemptions: Token holders can claim collateral proportional to the reported payout weights after oracle resolution.

This ERC formalizes patterns that the prediction market industry has battle-tested for years. Providing one interface will accelerate adoption across chains and applications.

## Adoption and Usage

This section is non-normative.

### Adoption

- Polymarket: Prediction markets using CTF on Polygon
- Seer: Prediction and futarchy markets using CTF (Gnosis and Ethereum)
- Forkast: Sports/gaming prediction markets using CTF-style conditional tokens (Arbitrum)
- Omen: Early CTF + Reality.eth prediction markets (legacy frontend; onchain markets persist)
- Predict Fun: Prediction markets using conditional token contracts (BNB Chain and Blast)
- OPINION: Prediction exchange using a CTF-derived conditional tokens design (BNB Chain)

### Nested conditionals

Nested positions (via `parentCollectionId`) allow conditioning a position on

multiple conditions. This is used for (i) decision markets / futarchy, where

downstream markets are only meaningful under a particular decision branch, and

(ii) outcome refinement, where an existing outcome set is further split by

introducing a child condition under that set (instead of mutating the parent

condition).

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

### Condition Lifecycle

#### prepareCondition

Initialize a new condition with a fixed number of outcomes. The function generates a `conditionId` which is the `keccak256(abi.encodePacked(oracle, questionId, outcomeSlotCount))` and initializes a payout vector associated to the `conditionId`

##### Parameters

- oracle: Account used to resolve a condition by reporting its result by calling reportPayouts. The conditionId is bound to the oracle address, so only that oracle can resolve the condition.
- questionId: Identifier for the question to be answered by oracle
- outcomeSlotCount: Number of outcomes for a condition. MUST BE > 1 and  0. The payout fraction for
outcome slot i is payouts[i] / payoutDenominator.

**NOTE**:

`msg.sender` is enforced as the oracle, because conditionId is derived from `(msg.sender, questionId, payouts.length)`.

```js
function reportPayouts(bytes32 questionId, uint[] calldata payouts) external
```

### Position Operations

#### splitPosition

Convert one `parent` stake into multiple `child` outcome positions defined by `partition`. If `parentCollectionId == bytes32(0)` and `indexSetUnion == fullIndexSet`, transfers `amount` collateral from the message sender; otherwise, burns `amount` of the position being split. In both cases, mints `amount` of each child position defined by `partition`.

##### Parameters

- collateralToken: The address of the position’s backing collateral token
- parentCollectionId: Outcome collection ID common to the position being split and the split target positions, or bytes32(0) if there’s no parent outcome collection.
- conditionId: Condition being split on.
- partition: Array of disjoint index sets defining a non-trivial partition of an indexSetUnion, where
fullIndexSet = (1  0 and
`amount`: Amount of collateral (only if `parentCollectionId == bytes32(0)` and `indexSetUnion == fullIndexSet`) or position tokens to convert into the partitioned positions.

**NOTE**

`bytes32(0)` means “no parent outcome collection”. When `indexSetUnion != fullIndexSet`, the position being

split is the subset position for `indexSetUnion` (not collateral), even if `parentCollectionId == bytes32(0)`.

A `parent` outcome collection represents a position already conditioned on prior outcomes, while a `child` outcome collection represents an additional condition on top of it.

E.g. Assume to condition statements C1 and C2 where C1 is the parent condition of C2 where:

1. C1 is “ETH > $3k?”
2. C2 is “ETH > $4k?”

The outcomes of `C1` are prior outcomes for `C2`, because `C2` is only evaluated within the branch where `C1` is valid.

```js
function splitPosition(
        IERC20 collateralToken,
        bytes32 parentCollectionId,
        bytes32 conditionId,
        uint[] calldata partition,
        uint amount
    ) external
```

#### mergePositions

The inverse of `splitPosition`: burn multiple child positions to recreate a parent or subset position, or get back collateral.

##### Parameters

- collateralToken: The address of the position’s backing collateral token
- parentCollectionId: Outcome collection ID common to the positions being merged and the merge result position, or bytes32(0) if there’s no parent outcome collection.
- conditionId: Condition being split on.
- partition: Array of disjoint index sets defining a non-trivial partition of the outcome slots.
- amount: Burns amount of each child position defined by partition

**NOTE**

Let `indexSetUnion = partition[0] | partition[1] | ...` and `fullIndexSet = (1 << outcomeSlotCount) - 1`.

- If indexSetUnion == fullIndexSet, either collateral is sent back to the caller (if parentCollectionId == bytes32(0)) or amount of the parent position token is minted.
- If indexSetUnion != fullIndexSet, amount of the merged subset position token for indexSetUnion is minted (even if parentCollectionId == bytes32(0)).

```js
function mergePositions(
        IERC20 collateralToken,
        bytes32 parentCollectionId,
        bytes32 conditionId,
        uint[] calldata partition,
        uint amount
    ) external
```

#### redeemPositions

After a condition is resolved, redeem outcome position tokens for their payout share.

##### Parameters

- collateralToken: The address of the position’s backing collateral token
- parentCollectionId: Either bytes32(0) for direct redemption for collateral or identifier of the parent collectionId for nested redemption
- conditionId: resolved condition
- indexSets: List of outcome collections (bitmasks) whose positions the caller wants to redeem.

**FLOW**

For each `indexSet`, computes the caller’s balance of the corresponding `positionId`, burns it, and adds

`payout += stake * payoutNumerator(indexSet) / payoutDenominator`. `payoutNumerator(indexSet)` is defined as

the sum of the per-outcome `payouts[i]` for which `indexSet` has the i-th bit set. Finally, transfers

collateral payout to the caller if (`parentCollectionId == bytes32(0)`) or mints the parent position token if

nested.

```js
function redeemPositions(IERC20 collateralToken, bytes32 parentCollectionId, bytes32 conditionId, uint[] calldata indexSets) external
```

### View Functions

#### getOutcomeSlotCount

Returns outcome slot count of a `conditionId`

##### Parameters

- conditionId: ID of the condition

```js
function getOutcomeSlotCount(bytes32 conditionId) external view returns (uint)
```

#### getConditionId

Returns generated `conditionId` which is the `keccak256(abi.encodePacked(oracle, questionId, outcomeSlotCount))`

##### Parameters

- oracle: The account assigned to report the result for the prepared condition
- questionId: An identifier for the question to be answered by the oracle
- outcomeSlotCount: The number of outcome slots which should be used for this condition. Must not exceed 256

```js
function getConditionId(address oracle, bytes32 questionId, uint outcomeSlotCount) external pure returns (bytes32)
```

#### getCollectionId

Returns `collectionId` constructed by a parent collection and an outcome collection.

##### Parameters

- parentCollectionId: Collection ID of the parent outcome collection, or bytes32(0) if there’s no parent
- conditionId: Condition ID of the outcome collection to combine with the parent outcome collection
- indexSet: Index set of the outcome collection to combine with the parent outcome collection

```js
function getCollectionId(bytes32 parentCollectionId, bytes32 conditionId, uint indexSet) external pure returns (bytes32)
```

#### getPositionId

Returns positionID from collateral token and outcome collection associated to the position

##### Parameters

- collateralToken: Collateral token which backs the position
- collectionId: ID of the outcome collection associated with this position

```js
function getPositionId(IERC20 collateralToken, bytes32 collectionId) external pure returns (uint)
```

### Events

#### ConditionPreparation

Emitted when a new condition is initialized

```js
event ConditionPreparation(
        bytes32 indexed conditionId,
        address indexed oracle,
        bytes32 indexed questionId,
        uint outcomeSlotCount
    )
```

#### ConditionResolution

Emitted when oracle executes `reportPayouts` with payouts for a certain `questionId`

```js
event ConditionResolution(
        bytes32 indexed conditionId,
        address indexed oracle,
        bytes32 indexed questionId,
        uint outcomeSlotCount,
        uint[] payoutNumerators
    )
```

#### PositionSplit

Emitted when a user splits collateral or position into multiple outcome positions

```js
event PositionSplit(
        address indexed stakeholder,
        IERC20 collateralToken,
        bytes32 indexed parentCollectionId,
        bytes32 indexed conditionId,
        uint[] partition,
        uint amount
    )
```

#### PositionsMerge

Emitted when a user merges multiple positions back into a parent position or collateral

```js
event PositionsMerge(
        address indexed stakeholder,
        IERC20 collateralToken,
        bytes32 indexed parentCollectionId,
        bytes32 indexed conditionId,
        uint[] partition,
        uint amount
    )
```

#### PayoutRedemption

Emitted when a user redeems positions after resolution

```js
event PayoutRedemption(
        address indexed redeemer,
        IERC20 indexed collateralToken,
        bytes32 indexed parentCollectionId,
        bytes32 conditionId,
        uint[] indexSets,
        uint payout
    )
```

## Example Lifecycle

This section illustrates the lifecycle of a simple binary conditional market, from condition preparation to redemption.

### Scenario

An oracle creates a condition for the question: “Will ETH trade above $3,000 on 2026-01-01?”, with two possible outcomes: **Yes** and **No**.

### Condition Preparation

The oracle calls `prepareCondition` with:

- oracle = O
- questionId = Q
- outcomeSlotCount = 2

This initializes a condition identified by: `conditionId = getConditionId(O, Q, 2)`

### Position Splitting

A participant deposits `100` units of collateral token `C` and splits it into outcome positions by calling `splitPosition` with:

- collateralToken = C
- parentCollectionId = bytes32(0)
- conditionId = conditionId
- partition = [0b01, 0b10]
- amount = 100

This transfers `100` units of collateral `C` to the conditional tokens contract and mints two ERC-1155 outcome positions representing:

- outcome Yes (indexSet = 0b01)
- outcome No (indexSet = 0b10)

Each position token represents a claim on the collateral conditional on the corresponding outcome. Each outcome position corresponds to `positionId = getPositionId(C, getCollectionId(bytes32(0), conditionId, indexSet))`.

### Oracle Resolution

After the resolution time, the oracle reports the result by calling `reportPayouts` with:

- questionId = Q
- payouts = [1, 0]

This assigns the full payout weight to the **Yes** outcome and zero to **No**.

### Redemption

A holder of the **Yes** position token calls `redeemPositions` with:

- collateralToken = C
- parentCollectionId = bytes32(0)
- conditionId = conditionId
- indexSets = [0b01]

The contract burns the redeemed position token and transfers `100` units of collateral `C` to the caller, proportional to the reported payout weights. Holders of the **No** position token receive no payout.

This example is illustrative and does not prescribe application-level behavior.

## Security Considerations

### Oracle Trust

The oracle has absolute authority over payout distribution. A malicious or compromised oracle can direct all collateral to chosen outcomes with no on-chain dispute mechanism. Implementers SHOULD consider multi-sig oracles, time-locked reporting, or staking with slashing conditions.

### External Calls and Collateral Tokens

Functions interacting with collateral tokens via `transfer` and `transferFrom` are susceptible to reentrancy if the token has callbacks (e.g., ERC-777). Implementations MUST follow checks-effects-interactions or use reentrancy guards.

Non-standard tokens (fee-on-transfer, rebasing) may cause accounting discrepancies. Implementations SHOULD document supported token types or measure actual balance changes.

### Front-Running

Oracle resolution transactions are visible in the mempool. Attackers can front-run `reportPayouts` to acquire winning positions before resolution. Applications SHOULD consider commit-reveal schemes or private mempools.

### Denial of Service

`prepareCondition` is permissionless and allocates storage. Attackers can spam condition creation to bloat storage. Implementations MAY require deposits or restrict creation to authorized registries.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

*As this is our initial draft, We’d greatly appreciate feedback. Suggestions are welcome.*

## Replies

**0xBerry** (2025-12-31):

This is exciting!

By standardizing conditional tokens, we solve the liquidity fragmentation problem that’s holding prediction markets back. Once audited, developers get a secure foundation to build on rather than starting from scratch every time.

Good job!

---

**jamesmccomish** (2026-01-06):

A few thoughts

### ERC1155

- I don’t know if this is something to specify. As long as condition preparation, splitting, and reporting conform to this ERC, projects could be left open to whatever tokenisation they like.

### Adoption

This doesn’t fit in the ERC. Maybe develop a site with more info on condition tokens / update the existing docs from Gnosis.

### Specification

- Terms need defined up front.

Things like condition, question id, outcome slot, splitting, parent/child condition

Need a clearer ‘Methods’ section with all required methods clearly explained.

- This section needs to be more strict. There is little indication of what events or errors MUST be emitted in each case.

### Security

- ‘Denial of Service’ isn’t really a concern

