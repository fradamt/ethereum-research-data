---
source: magicians
topic_id: 20735
title: "ERC-7752: Lot Token"
author: mrosendin
date: "2024-08-07"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7752-lot-token/20735
views: 663
likes: 17
posts_count: 19
---

# ERC-7752: Lot Token

## Overview

A token standard that treats every acquisition (lot) as its own on-chain record, enabling per-lot cost-basis, lineage, and regulatory controls.

### Why Lots?

- Precise handling of vesting, lock-ups, and wash-sale rules
- On-chain FIFO/LIFO tax reporting
- Easier partial sales or spin-offs without external databases

### Example Use-Cases

| Domain | How 7752 helps |
| --- | --- |
| Equity & options | Track every certificate / grant as its own lot; carry vesting metadata in uri or data. |
| Debt & convertibles | Coupon lots, note splits, or SAFE → equity conversion keep lineage via parentLotId. |
| Real-world assets | Home, boat, artwork—all represented as subdividable lots with transparent cost basis. |
| Fund accounting | Index 7752 events to generate investor K-1s or Form 8949 automatically. |

---

### TransferType Enum (semantic meaning)

| Value | Typical action | Tax context captured |
| --- | --- | --- |
| INTERNAL | Move between wallets you control | Usually non-taxable administrative action |
| SALE | Arm’s-length sale | Market transaction for consideration |
| GIFT | No-consideration transfer | Gratuitous transfer between parties |
| INHERITANCE | Transfer at death | Estate/probate distribution |
| INCOME | Payroll / airdrop / staking yield / RSU | Compensation or earned income |

*Each jurisdiction applies its own tax rules to these transfer contexts.*

---

### Minimal-core vs. Extensions

- Core: lot CRUD, TransferType, metadata, approvals
- Optional extension: customId (legacy certificate numbers)

Keeps the base spec lean for DeFi deployments
- Extension interface ILotTokenCustomId adds updateCustomId + event

---

### Solidity Interface (core only)

```javascript
// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.20;

/**
 * @title ERC-7752 Lot Token (Core Interface)
 * @notice Core lot management
 */
interface IERC7752 {
    /*──────────────────────────────────
      Data Structures
    ──────────────────────────────────*/

    enum TransferType {
        INTERNAL,     // Administrative transfers, splits, merges
        SALE,         // Market transactions for consideration
        GIFT,         // Gratuitous transfers
        INHERITANCE,  // Estate/probate transfers
        INCOME        // Compensation, airdrops, staking rewards
    }

    struct Lot {
        bytes32 parentLotId;        // Parent lot for lineage tracking
        uint256 quantity;           // Amount in this lot
        address currency;           // Currency used for acquisition
        uint256 basis;              // Total cost basis (in currency)
        uint256 acquisitionDate;    // Unix timestamp of acquisition
        uint256 lastUpdate;         // Unix timestamp of last modification
        address owner;              // Current owner address
        TransferType transferType;  // How this lot was acquired
        string  uri;                // Metadata URI
        bytes   data;               // Additional lot-specific data
    }

    /*──────────────────────────────────
      Events
    ──────────────────────────────────*/

    /**
     * @notice Emitted when a new lot is created
     */
    event LotCreated(
        address indexed owner,
        bytes32 indexed lotId,
        bytes32 indexed parentLotId,
        uint256 quantity,
        address currency,
        uint256 basis,
        uint256 acquisitionDate,
        TransferType transferType,
        string  uri,
        bytes   data
    );

    /**
     * @notice Emitted when a lot is transferred (full or partial)
     */
    event LotTransferred(
        bytes32 indexed lotId,
        bytes32 indexed newLotId,
        address indexed from,
        address indexed to,
        uint256 quantity,
        uint256 newBasis,
        TransferType transferType,
        string  uri,
        bytes   data
    );

    /**
     * @notice Emitted when lots are merged into a new lot
     */
    event LotsMerged(
        bytes32[] sourceLotIds,
        bytes32 indexed newLotId,
        address indexed owner,
        uint256 totalQuantity,
        string uri,
        bytes data
    );

    /**
     * @notice Emitted when a lot is split into multiple lots
     */
    event LotSplit(
        bytes32 indexed sourceLotId,
        bytes32[] newLotIds,
        uint256[] quantities,
        address indexed owner
    );

    /*──────────────────────────────────
      Core Read Functions
    ──────────────────────────────────*/

    /**
     * @notice Returns the token name
     */
    function name() external view returns (string memory);

    /**
     * @notice Returns the token symbol
     */
    function symbol() external view returns (string memory);

    /**
     * @notice Returns lot details for a given lot ID
     * @param lotId The lot identifier
     * @return lot The lot data structure
     */
    function getLot(bytes32 lotId) external view returns (Lot memory lot);

    /**
     * @notice Returns all lot IDs owned by an address
     * @param owner The owner address
     * @return lotIds Array of lot identifiers
     */
    function getLotsOf(address owner) external view returns (bytes32[] memory lotIds);

    /**
     * @notice Returns total quantity across all lots for an owner
     * @param owner The owner address
     * @return totalQuantity Sum of quantities across all lots
     */
    function balanceOf(address owner) external view returns (uint256 totalQuantity);

    /**
     * @notice Checks if a lot ID exists and is valid
     * @param lotId The lot identifier
     * @return exists True if lot exists
     */
    function lotExists(bytes32 lotId) external view returns (bool exists);

    /*──────────────────────────────────
      Core Lot Operations
    ──────────────────────────────────*/

         /**
      * @notice Creates a new lot
      * @param owner Initial owner of the lot
      * @param quantity Amount in the lot
      * @param currency Currency used for acquisition (address(0) for native)
      * @param basis Total cost basis in currency
      * @param acquisitionDate Unix timestamp of acquisition
      * @param transferType How this lot was acquired
      * @param uri Metadata URI for the lot
      * @param data Additional lot-specific data
      * @return lotId The created lot identifier
      */
    function createLot(
        address owner,
        uint256 quantity,
        address currency,
        uint256 basis,
        uint256 acquisitionDate,
        TransferType transferType,
        string calldata uri,
        bytes calldata data
    ) external returns (bytes32 lotId);

         /**
      * @notice Transfers full or partial lot to another address
      * @param lotId Source lot identifier
      * @param to Recipient address
      * @param quantity Amount to transfer (must be ≤ lot quantity)
      * @param transferType Type of transfer for the new lot
      * @param newBasis Cost basis for the transferred portion
      * @param uri Metadata URI for the new lot
      * @param data Additional data for the new lot
      * @return newLotId Identifier of the newly created lot for recipient
      */
    function transfer(
        bytes32 lotId,
        address to,
        uint256 quantity,
        TransferType transferType,
        uint256 newBasis,
        string calldata uri,
        bytes calldata data
    ) external returns (bytes32 newLotId);

         /**
      * @notice Transfers lot on behalf of owner (requires approval)
      * @param lotId Source lot identifier
      * @param from Owner address
      * @param to Recipient address
      * @param quantity Amount to transfer
      * @param transferType Type of transfer
      * @param newBasis Cost basis for transferred portion
      * @param uri Metadata URI for new lot
      * @param data Additional data for new lot
      * @return newLotId Identifier of newly created lot
      */
    function transferFrom(
        bytes32 lotId,
        address from,
        address to,
        uint256 quantity,
        TransferType transferType,
        uint256 newBasis,
        string calldata uri,
        bytes calldata data
    ) external returns (bytes32 newLotId);

    /**
     * @notice Merges multiple lots into a single new lot
     * @param sourceLotIds Array of lot identifiers to merge (must have same owner)
     * @param uri Metadata URI for merged lot
     * @param data Additional data for merged lot
     * @return newLotId Identifier of the merged lot
     */
    function mergeLots(
        bytes32[] calldata sourceLotIds,
        string calldata uri,
        bytes calldata data
    ) external returns (bytes32 newLotId);

    /**
     * @notice Splits a lot into multiple new lots
     * @param lotId Source lot identifier
     * @param quantities Array of quantities for new lots (must sum to original)
     * @param uris Array of metadata URIs for new lots
     * @param dataArray Array of additional data for new lots
     * @return newLotIds Array of identifiers for new lots
     */
    function splitLot(
        bytes32 lotId,
        uint256[] calldata quantities,
        string[] calldata uris,
        bytes[] calldata dataArray
    ) external returns (bytes32[] memory newLotIds);

    /*──────────────────────────────────
      Approval System
    ──────────────────────────────────*/

    /**
     * @notice Approve an operator for a specific lot
     * @param lotId The lot identifier
     * @param operator Address to approve
     * @param approved True to approve, false to revoke
     */
    function approveLot(bytes32 lotId, address operator, bool approved) external;

    /**
     * @notice Approve an operator for all lots owned by caller
     * @param operator Address to approve
     * @param approved True to approve, false to revoke
     */
    function setApprovalForAll(address operator, bool approved) external;

    /**
     * @notice Check if operator is approved for a specific lot
     * @param lotId The lot identifier
     * @param operator Address to check
     * @return approved True if approved
     */
    function isApprovedForLot(bytes32 lotId, address operator) external view returns (bool approved);

    /**
     * @notice Check if operator is approved for all lots of an owner
     * @param owner The owner address
     * @param operator Address to check
     * @return approved True if approved for all
     */
    function isApprovedForAll(address owner, address operator) external view returns (bool approved);
}
```

---

### ERC Pull Request

https://github.com/ethereum/ERCs/pull/579

## Replies

**wjmelements** (2024-08-08):

I don’ think the batch interfaces are useful or necessary.

---

**wjmelements** (2024-08-08):

ok I see they are part of erc-3643. I don’t like them there either.

I think your specification can be simplified by explicitly requiring erc-3643 compliance. You can remove all of the erc-3643 spec thereby.

---

**mrosendin** (2024-08-09):

What do you see as the issue with the batch interfaces?

The original post didn’t mention that there are ERC-3643 breaking changes. I’ve updated the post with the details.

---

**wjmelements** (2024-08-09):

> What do you see as the issue with the batch interfaces?

Concatenation is the superior batch ABI. It even works for batching different methods. All of the top trading bots are doing it.

---

**Joachim-Lebrun** (2024-08-29):

i don’t agree on that, most users still use EOAs and as long as ERC-3074 is not integrated (should be part of Pectra upgrade) they cannot batch transactions natively, therefore it is good to have batch transactions defined on the ABIs, not everyone uses trading bots or smart accounts. Also, having an external contract implementing the batching logic and calling the token contract repeatedly is going to cost additional gas compared to the batch implemented on the token contract directly.

---

**wjmelements** (2024-08-29):

We disagree on the meaning of ABI. You are confusing this because the non-standard Solidity 4byte ABI is the most popular ABI, and because Solidity’s json output calls its list of methods “abi”. However, ABI is a more general term referring to the binary input format itself, not the list of methods.

You would like there to be separate methods for batching. I would like for all methods to be batchable.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joachim-lebrun/48/15462_2.png) Joachim-Lebrun:

> i don’t agree on that, most users still use EOAs

Both ABIs work for EOAs.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joachim-lebrun/48/15462_2.png) Joachim-Lebrun:

> they cannot batch transactions natively

Yes they can, if we adopt the concatenation batch ABI.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joachim-lebrun/48/15462_2.png) Joachim-Lebrun:

> Also, having an external contract implementing the batching logic and calling the token contract repeatedly is going to cost additional gas compared to the batch implemented on the token contract directly.

Irrelevant; this demonstrates you do not understand. My theory about why you do not understand heads this reply.

---

**Joachim-Lebrun** (2024-08-29):

Thank you for the clarification. I appreciate the insight into using ABI concatenation as a method for batching transactions. It’s definitely an interesting approach and I can see how it could be powerful in certain contexts, e.g. for advanced users like trading bots.

That said, in my experience developing in Solidity over the past six years, and working closely with a team of developers, this method of batching through ABI concatenation is not something we’ve commonly encountered or used. Most of the development community, from what I’ve observed, tends to favor more explicit and user-friendly interfaces, especially when it comes to contract interactions. The standard practice involves defining specific batch methods in the ABI to accommodate the needs of the majority of users and developers, particularly those using EOAs or relying on standard wallets and interfaces.

While ABI concatenation might offer more flexibility in certain scenarios, it also introduces a level of complexity that might not be necessary or practical for most use cases. The typical user interacting with smart contracts is not using raw ABI concatenation but rather calling clearly defined methods through familiar interfaces.

I agree that in a more abstract sense, ABI refers to the binary input format and not just the list of methods in a Solidity-generated JSON. However, for most real-world applications, especially those targeting a broad user base, the practical advantages of explicit batch methods in the ABI outweigh the theoretical flexibility provided by concatenation.

It’s certainly a technique worth being aware of, but in terms of practicality and adoption within the community, the current standard approach of defining batch methods seems to best serve the majority of users and use cases.

---

**wjmelements** (2024-08-29):

The fact that concatenation isn’t currently supported by solidity is not a reason to oppose it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joachim-lebrun/48/15462_2.png) Joachim-Lebrun:

> ABI concatenation is not something we’ve commonly encountered or used.

This EIP concerns the future. Past tendencies are gravitationally bound by the current limitations of solidity.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joachim-lebrun/48/15462_2.png) Joachim-Lebrun:

> The typical user interacting with smart contracts is not using raw ABI concatenation but rather calling clearly defined methods through familiar interfaces.

The concatenated methods are also clearly defined.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joachim-lebrun/48/15462_2.png) Joachim-Lebrun:

> the current standard approach of defining batch methods seems to best serve the majority of users and use cases.

Obviously not, because the batching deficiency is cited in the rationale of several EIPS like 3074.

---

**mrosendin** (2024-08-29):

[@wjmelements](/u/wjmelements) [@Joachim-Lebrun](/u/joachim-lebrun) thank you for the discussion. I think this thread will be helpful for others in consideration of batch interfaces in other specs.

That being said, I am updating the spec to remove partial freeze/unfreeze in favor of freezing a specified `securityId`. This simplifies the implementation and cuts down on the contract size.

[@wjmelements](/u/wjmelements), I suppose the concatenation you mention would further reduce compiled contract size (please correct me if I’m wrong) because the batch methods would not need to be explicitly implemented.

Edit: Are you referring to something like [Multicall3](https://wiki.iota.org/build/multicall/)?

---

**hiddenintheworld** (2024-10-09):

[@mrosendin](/u/mrosendin) I highly recommend for `recoveryAddress` or `setCompliance` considering adding storing a zk-hash that can be used later to recovery instead of directly pushing addresses, balances,etc.

---

**wjmelements** (2024-10-10):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/c37758/48.png) mrosendin:

> Edit: Are you referring to something like Multicall3

No

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/c37758/48.png) mrosendin:

> However, I don’t have an understanding of how concat works in practice. Can you please refer me to some reading material on usage?

Two examples

- https://etherscan.io/address/0x00000000009e50a7ddb7a7b0e2ee6604fd120e49
- https://etherscan.io/address/0x0000e0ca771e21bd00057f54a68c30d400000000

The bytecode is pretty straightforward (examine with [evm -d](https://github.com/wjmelements/evm?tab=readme-ov-file#disassembler)) but there aren’t any docs and it’s impossible within solidity today. I have a WIP proposal for solidity 4byte that would look like

```solidity
function transfer(address to, uint256 value) external batchable;
```

If a method is `batchable`, then check after the calldata for that method for the next method in the batch, which must also be `batchable`. The main issue I’m having with this design are current constructs like `msg.value`.

---

**mrosendin** (2024-11-08):

I’ve revised the design. This new specification came along with helpful feedback from [@Joachim-Lebrun](/u/joachim-lebrun).

The proposed new spec is based on the [ERC-1155 Multi-Token Standard](https://ethereum.org/en/developers/docs/standards/tokens/erc-1155/). Each asset class gets its own ERC-1155 token and each equity issuance has a unique token ID. Benefits include easier tax lot tracking, compliance restrictions targeting a specific issuance, and OCF adherence. I am testing this for startup companies and SPVs and scaling for large enterprises and investment funds.

---

**Arvolear** (2024-12-09):

The beauty of ERC-20 compliant RWA tokens category is that they allow permissioned dex, lending, voting, etc, protocols to be built *relatively* easily. If we are sticking to ERC-1155 standard, not only the token management together with its permissions will become exponentially more complex, but also we will lose the future integration potential.

P.S.

Having struggled a lot with ERC-3643, we have built [TokenF](https://github.com/dl-tokenf) on-chain RWA framework. You will find there a list of projects with different RWA approaches including ERC-1155.

---

**mrosendin** (2024-12-15):

ERC-7752 uses a linked ERC-1155 `tokenId` list, making it super easy to audit the history of any given token, including unique URIs for each transfer of a token, which can point to an offchain contract. This functionality is efficient and adds a major compliance benefit for private RWA issuers.

Edit: ERC-7752 is purposely not backwards compatible ERC-20 RWAs as a tradeoff for the benefit of detailed tracking of token lots.

---

**SamWilsn** (2024-12-23):

A couple non-editorial comments:

- Why define mint/burn functions? The only actor that will be able to call those will likely be the contract’s deployer. The deployer of a contract knows the contract’s API. By defining mint/burn in your standard, you limit the flexibility of implementations. You’ll note that none of the major token standards define these functions. If you choose to keep these functions as part of ERC-7752, I’d strongly recommend including your reasoning in your Rationale section.
- Similar comments about pause/unpause, forcedTransfer, and the freeze family of functions. Just define the events and the criteria for emitting them.

The only argument I can envision for making these functions part of the core standard is because you expect someone *other than the contract’s deployer* to call them. I could maybe imagine a `RestrictedTokenPolicy` interface with standard implementations like `CanadianRestrictedTokenPolicy` and `NorwegianRestrictedTokenPolicy` that you could give `AgentRole` to to manage your ERC-7752 token. Is that kind of what you have in mind?

---

**theBigRevolution** (2024-12-24):

Good work ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12) it seems to be similar to the features in CeFi

---

**mrosendin** (2025-01-29):

Hi [@SamWilsn](/u/samwilsn), thank you for your comments! FYI, I have been working on a refined proposal for the new token standard that will address these points, among others.

I agree with your recommendation. The new proposal will introduce a base token contract without access control, because the updated ERC proposal will encompass any asset with token [lots](https://www.investopedia.com/terms/t/taxlotaccounting.asp). There currently is no token standard that does this.

Access control can be added to the token, and in many cases will be, but this does not have to be a part of the core standard. I’ll be updating this post and the GitHub PR to reflect this.

---

**mrosendin** (2025-06-09):

Hi [@SamWilsn](/u/samwilsn), the updated post and PR incorporates your feedback, addresses the concerns, has all checks passing, and awaiting a review.

