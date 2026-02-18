---
source: magicians
topic_id: 20280
title: Why is ERC-1400 not listed on eips.ethereum.org?
author: ivica
date: "2024-06-12"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/why-is-erc-1400-not-listed-on-eips-ethereum-org/20280
views: 567
likes: 5
posts_count: 3
---

# Why is ERC-1400 not listed on eips.ethereum.org?

I was wondering, why ERC-1400 family (ERC-1410, ERC-1594, ERC-1644, ERC-1643) is not listed on [eips.ethereum.org](http://eips.ethereum.org)? Has it been stagnant and pulled back?

## Replies

**abcoathup** (2024-06-12):

ERC discussions used to take place in the issues & ERCs used the issue number for their ERC number.  Looks like PRs were never created for them, so they were never merged and hence aren’t on eips website.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/1410)












####



        opened 09:22PM - 13 Sep 18 UTC



          closed 09:11PM - 18 Dec 21 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/c/c98b36137960f8d631813de8a2a586ca0b836961.jpeg)
          adamdossa](https://github.com/adamdossa)





          stale







---

eip: ERC-1410
title: Partially Fungible Token Standard (part of the ERC-[…]()1400 Security Token Standards)
author: Adam Dossa (@adamdossa), Pablo Ruiz (@pabloruiz55), Fabian Vogelsteller (@frozeman), Stephane Gosselin (@thegostep)
discussions-to: #1411
status: Draft
type: Standards Track
category: ERC
created: 2018-09-13
require: ERC-1066 (#1066)

---

## Simple Summary

A standard interface for organising an owners tokens into a set of partitions.

## Abstract

This standard sits under the ERC-1400 (#1411) umbrella set of standards related to security tokens.

Describes an interface to support an owners tokens being grouped into partitions, with each partition being represented by an identifying key and a balance.

Tokens are operated upon at a partition granularity, but data about the overall supply of tokens and overall balances of owners is also tracked.

This standard can be combined with ERC-20 (#20) or ERC-777 (#777) to provide an additional layer of granular transparency as to the behaviour of a token contract on different partitions of a token holders balance.

## Motivation

Being able to associate metadata with individual fungible tokens is useful when building functionality associated with those tokens.

For example, knowing when an individual token was minted allows vesting or lockup logic to be implemented for a portion of a token holders balance.

Tokens that represent securities often require metadata to be attached to individual tokens, such as restrictions associated with the share.

Being able to associate arbitrary metadata with groups of tokens held by users is useful in a variety of use-cases. It can be used for token provenance (i.e. recording the previous owner(s) of tokens) or to attach data to a token which is then used to determine any transfer restrictions of that token.

In general it may be that whilst tokens are fungible under some circumstances, they are not under others (for example in-game credits and deposited balances). Being able to define such groupings and operate on them whilst maintaining data about the overall distribution of a token irrespective of this is useful in modelling these types of assets.

Having a standard way to identify groupings of tokens within an overall balance helps provides token holders transparency over their balances.

## Rationale

A Partially-Fungible Token allows for attaching metadata to a partial balance of a token holder. These partial balances are called partitions and are indexed by a `bytes32 _partition` key which can be associated with metadata on-chain or off-chain.

The specification for this metadata, beyond the existence of the `_partition` key to identify it, does not form part of this standard. The token holders address can be paired with the partition to use as a metadata key if data varies across token holders with the same partition (e.g. a "restricted" partition may be associated with different lock up dates for each token holder).

For an individual owner, each token in a partition therefore shares common metadata.

Token fungibility includes metadata so we have:
  - for a specific user, tokens within a given partition are fungible
  - for a specific user, tokens from different partitions may not be fungible

Note - partitions with the same `bytes32` key across different users may be associated with different metadata depending on the implementation.

## Backwards Compatibility

This standard is un-opinionated on ERC-20 vs. ERC-777. It can be easily combined with either standard, and we expect this to usually be the case. We don't define the standard token view functions (`name`, `symbol`, `decimals`) as a consequence.

In order to remain backwards compatible with ERC-20 / ERC-777 (and other fungible token standards) it is necessary to define what partition or partitions are used when a `transfer` / `send` operation is executed (i.e. when not explicitly specifying the partition). However this is seen as an implementation detail (could be via a fixed list, or programatically determined). One option is to simple iterate over all `partitionsOf` for the token holder, although this approach needs to be cognisant of block gas limits.

## Specification

### Token Information

#### balanceOf

Aggregates a token holders balances across all partitions. Equivalent to `balanceOf` in the ERC-20/777 specification.

MUST count the sum of all partition balances assigned to a token holder.

``` solidity
function balanceOf(address _tokenHolder) external view returns (uint256);
```

#### balanceOfByPartition

As well as querying total balances across all partitions through `balanceOf` there may be a need to determine the balance of a specific partition.

For a given token holder, the sum of `balanceOfByPartition` across `partitionsOf` MUST be equal to `balanceOf`.

``` solidity
function balanceOfByPartition(bytes32 _partition, address _tokenHolder) external view returns (uint256);
```

#### partitionsOf

A token holder may have their balance split into several partitions (partitions) - this function will return all of the partitions that could be associated with a particular token holder address. This can include empty partitions, but MUST include any partitions which have a non-zero balance.

``` solidity
function partitionsOf(address _tokenHolder) external view returns (bytes32[]);
```

#### totalSupply

Returns the total amount of tokens issued across all token holders and partitions.

MUST count all tokens tracked by this contract.

``` solidity
function totalSupply() external view returns (uint256);
```

### Tokens Transfers

Token transfers always have an associated source and destination partition, as well as the usual amounts and sender / receiver addresses.

As an example, a permissioned token may use partition metadata to enforce transfer restrictions based on:
  - the `_partition` value
  - any additional data associated with the `_partition` value (e.g. a lockup timestamp that may be associated with `_partition`)
  - any details associated with the sender or receiver of tokens (e.g. has their identity been established)
  - the amount of tokens being transferred (e.g. does it respect any daily or other period-based volume restrictions)
  - the `_data` parameter allows the caller to supply any additional authorisation or details associated with the transfer (e.g. signed data from an authorised entity who is permissioned to authorise the transfer)

Other use-cases include tracking provenance of tokens by associating previous holders with destination partitions.

#### transferByPartition

This function MUST throw if the transfer of tokens is not successful for any reason.

When transferring tokens from a particular partition, it is useful to know on-chain (i.e. not just via an event being fired) the destination partition of those tokens. The destination partition will be determined by the implementation of this function and will vary depending on use-case.

The function MUST return the `bytes32 _partition` of the receiver.

The `bytes _data` allows arbitrary data to be submitted alongside the transfer, for the token contract to interpret or record. This could be signed data authorising the transfer (e.g. a dynamic whitelist), or provide some input for the token contract to determine the receivers partition.

This function MUST emit a `TransferByPartition` event for successful transfers.

``` solidity
function transferByPartition(bytes32 _partition, address _to, uint256 _value, bytes _data) external returns (bytes32);
```

#### operatorTransferByPartition

Allows an operator to transfer security tokens on behalf of a token holder, within a specified partition.

This function MUST revert if called by an address lacking the appropriate approval as defined by `isOperatorForPartition` or `isOperator`.

This function MUST emit a `TransferByPartition` event for successful token transfers, and include the operator address.

The return data is interpreted consistently with `transferByPartition`.

``` solidity
function operatorTransferByPartition(bytes32 _partition, address _from, address _to, uint256 _value, bytes _data, bytes _operatorData) external returns (bytes32);
```

#### canTransferByPartition

Transfers of partially fungible tokens may fail for a number of reasons, relating either to the token holders partial balance, or rules associated with the partition being transferred.

The standard provides an on-chain function to determine whether a transfer will succeed, and return details indicating the reason if the transfer is not valid.

These rules can either be defined using smart contracts and on-chain data, or rely on `_data` passed as part of the `transferByPartition` function which could represent authorisation for the transfer (e.g. a signed message by a transfer agent attesting to the validity of this specific transfer).

The function will return both a ESC (Ethereum Status Code) following the EIP-1066 standard, and an additional `bytes32` parameter that can be used to define application specific reason codes with additional details (for example the transfer restriction rule responsible for making the transfer operation invalid).

It also returns the destination partition of the tokens being transferred in an analogous way to `transferByPartition`.

``` solidity
function canTransferByPartition(address _from, address _to, bytes32 _partition, uint256 _value, bytes _data) external view returns (byte, bytes32, bytes32);
```

### Operators

Operators can be authorised by individual token holders for either all partitions, or a specific partition.

  - a specific token holder and all partitions (`authorizeOperator`, `revokeOperator`, `isOperator`)
  - a specific token holder for a specific partition (`authorizeOperatorByPartition`, `revokeOperatorByPartition`, `isOperatorForPartition`)

#### authorizeOperator

Allows a token holder to set an operator for their tokens across all partitions.

MUST authorise an operator for all partitions of `msg.sender`

This function MUST emit the event `AuthorizedOperator` every time it is called.

``` solidity
function authorizeOperator(address _operator) external;
```

#### revokeOperator

Allows a token holder to revoke an operator for their tokens across all partitions.

NB - it is possible the operator will retain authorisation over this token holder and some partitions through `authorizeOperatorByPartition`.

MUST revoke authorisation of an operator previously given for all partitions of `msg.sender`

This function MUST emit the event `RevokedOperator` every time it is called.

``` solidity
function revokeOperator(address _operator) external;
```

#### isOperator

Returns whether a specified address is an operator for the given token holder and all partitions.

This should return TRUE if the address is an operator under any of the above categories.

MUST query whether `_operator` is an operator for all partitions of `_tokenHolder`.

``` solidity
function isOperator(address _operator, address _tokenHolder) external view returns (bool);
```

#### authorizeOperatorByPartition

Allows a token holder to set an operator for their tokens on a specific partition.

This function MUST emit the event `AuthorizedOperatorByPartition` every time it is called.

``` solidity
function authorizeOperatorByPartition(bytes32 _partition, address _operator) external;
```

#### revokeOperatorByPartition

Allows a token holder to revoke an operator for their tokens on a specific partition.

NB - it is possible the operator will retain authorisation over this token holder and partition through either `defaultOperatorsByPartition` or `defaultOperators`.

This function MUST emit the event `RevokedOperatorByPartition` every time it is called.

``` solidity
function revokeOperatorByPartition(bytes32 _partition, address _operator) external;
```

#### isOperatorForPartition

Returns whether a specified address is an operator for the given token holder and partition.

This should return TRUE if the address is an operator under any of the above categories.

``` solidity
function isOperatorForPartition(bytes32 _partition, address _operator, address _tokenHolder) external view returns (bool);
```

## Interface

``` solidity
/// @title ERC-1410 Partially Fungible Token Standard
/// @dev See https://github.com/SecurityTokenStandard/EIP-Spec

interface IERC1410 {

    // Token Information
    function balanceOf(address _tokenHolder) external view returns (uint256);
    function balanceOfByPartition(bytes32 _partition, address _tokenHolder) external view returns (uint256);
    function partitionsOf(address _tokenHolder) external view returns (bytes32[]);
    function totalSupply() external view returns (uint256);

    // Token Transfers
    function transferByPartition(bytes32 _partition, address _to, uint256 _value, bytes _data) external returns (bytes32);
    function operatorTransferByPartition(bytes32 _partition, address _from, address _to, uint256 _value, bytes _data, bytes _operatorData) external returns (bytes32);
    function canTransferByPartition(address _from, address _to, bytes32 _partition, uint256 _value, bytes _data) external view returns (byte, bytes32, bytes32);

    // Operator Information
    function isOperator(address _operator, address _tokenHolder) external view returns (bool);
    function isOperatorForPartition(bytes32 _partition, address _operator, address _tokenHolder) external view returns (bool);

    // Operator Management
    function authorizeOperator(address _operator) external;
    function revokeOperator(address _operator) external;
    function authorizeOperatorByPartition(bytes32 _partition, address _operator) external;
    function revokeOperatorByPartition(bytes32 _partition, address _operator) external;

    // Issuance / Redemption
    function issueByPartition(bytes32 _partition, address _tokenHolder, uint256 _value, bytes _data) external;
    function redeemByPartition(bytes32 _partition, uint256 _value, bytes _data) external;
    function operatorRedeemByPartition(bytes32 _partition, address _tokenHolder, uint256 _value, bytes _operatorData) external;

    // Transfer Events
    event TransferByPartition(
        bytes32 indexed _fromPartition,
        address _operator,
        address indexed _from,
        address indexed _to,
        uint256 _value,
        bytes _data,
        bytes _operatorData
    );

    // Operator Events
    event AuthorizedOperator(address indexed operator, address indexed tokenHolder);
    event RevokedOperator(address indexed operator, address indexed tokenHolder);
    event AuthorizedOperatorByPartition(bytes32 indexed partition, address indexed operator, address indexed tokenHolder);
    event RevokedOperatorByPartition(bytes32 indexed partition, address indexed operator, address indexed tokenHolder);

    // Issuance / Redemption Events
    event IssuedByPartition(bytes32 indexed partition, address indexed operator, address indexed to, uint256 amount, bytes data, bytes operatorData);
    event RedeemedByPartition(bytes32 indexed partition, address indexed operator, address indexed from, uint256 amount, bytes operatorData);

}
```














      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/1594)












####



        opened 10:24AM - 19 Nov 18 UTC



          closed 12:18PM - 06 Dec 21 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/c/c98b36137960f8d631813de8a2a586ca0b836961.jpeg)
          adamdossa](https://github.com/adamdossa)





          stale







---

eip: ERC-1594
title: Core Security Token Standard (part of the ERC-1400 […]()Security Token Standards)
author: Adam Dossa (@adamdossa), Pablo Ruiz (@pabloruiz55), Fabian Vogelsteller (@frozeman), Stephane Gosselin (@thegostep)
discussions-to: #1411
status: Draft
type: Standards Track
category: ERC
created: 2018-09-09
require: ERC-20 (#20), ERC-1066 (#1066)

---

## Simple Summary

This standard sits under the ERC-1400 (#1411) umbrella set of standards related to security tokens.

Provides a standard to support off-chain injection of data into transfers / issuance / redemption and the ability to check the validity of a transfer distinct from it's execution.

## Abstract

Incorporates error signalling, off-chain data injection and issuance / redemption semantics.

This standard inherits from ERC-20 (#20) and could be easily extended to meet the ERC-777 (#777) standard if needed.

## Motivation

Accelerate the issuance and management of securities on the Ethereum blockchain by specifying a standard interface through which security tokens can be operated on and interrogated by all relevant parties.

Security tokens differ materially from other token use-cases, with more complex interactions between off-chain and on-chain actors, and considerable regulatory scrutiny.

The ability to provide data (e.g. signed authorisation) alongside transfer, issuance and redemption functions allows security tokens to more flexibly implement transfer restrictions without depending on on-chain whitelists exclusively.

Using ERC-1066 (#1066) to provide reason codes as to why a transfer would fail, without requiring a user to actually try and execute a transfer, allows for improved UX and potentially saves gas on what would otherwise be failed transfers.

Formalising issuance and redemption semantics (similar to minting / burning) provides visibility into the total supply of the token and how it has changed over time.

## Requirements

See ERC-1400 (#1411) for a full set of requirements across the library of standards.

The following requirements have been compiled following discussions with parties across the Security Token ecosystem.

- MUST have a standard interface to query if a transfer would be successful and return a reason for failure.
- MUST emit standard events for issuance and redemption.
- MAY require signed data to be passed into a transfer transaction in order to validate it on-chain.
- SHOULD NOT restrict the range of asset classes across jurisdictions which can be represented.
- MUST be ERC-20 (#20) compatible.
- COULD be ERC-777 (#777) compatible.

## Rationale

### Transfer Restrictions

Transfers of securities can fail for a variety of reasons in contrast to utility tokens which generally only require the sender to have a sufficient balance.

These conditions could be related to metadata of the securities being transferred (i.e. whether they are subject to a lock-up period), the identity of the sender and receiver of the securities (i.e. whether they have been through a KYC process, whether they are accredited or an affiliate of the issuer) or for reasons unrelated to the specific transfer but instead set at the token level (i.e. the token contract enforces a maximum number of investors or a cap on the percentage held by any single investor).

For ERC-20 / ERC-777 tokens, the `balanceOf` and `allowance` functions provide a way to check that a transfer is likely to succeed before executing the transfer, which can be executed both on and off-chain.

For tokens representing securities the standard introduces a function `canTransfer` which provides a more general purpose way to achieve this when the reasons for failure are more complex; and a function of the whole transfer (i.e. includes any data sent with the transfer and the receiver of the securities).

In order to support off-chain data inputs to transfer functions, transfer functions are extended to `transferWithData` / `transferFromWithData` which can optionally take an additional `bytes _data` parameter.

In order to provide a richer result than just true or false, a byte return code is returned. This allows us to give a reason for why the transfer failed, or at least which category of reason the failure was in. The ability to query documents and the expected success of a transfer is included in Security Token section.

## Specification

### Restricted Transfers

#### canTransfer / canTransferFrom

Transfers of securities may fail for a number of reasons, for example relating to:
  - the identity of the sender or receiver of the tokens
  - limits placed on the specific tokens being transferred (i.e. lockups on certain quantities of token)
  - limits related to the overall state of the token (i.e. total number of investors)

The standard provides an on-chain function to determine whether a transfer will succeed, and return details indicating the reason if the transfer is not valid.

These rules can either be defined using smart contracts and on-chain data, or rely on `_data` passed as part of the `transferWithData` function which could represent authorisation for the transfer (e.g. a signed message by a transfer agent attesting to the validity of this specific transfer).

The function will return both a ESC (Ethereum Status Code) following the EIP-1066 standard, and an additional `bytes32` parameter that can be used to define application specific reason codes with additional details (for example the transfer restriction rule responsible for making the transfer operation invalid).

If `bytes _data` is empty, then this corresponds to a check on whether a `transfer` (or `transferFrom`) request will succeed, if `bytes _data` is populated, then this corresponds to a check on `transferWithData` (or `transferFromWithData`) will succeed.

`canTransfer` assumes the sender of tokens is `msg.sender` and will be executed via `transfer` or `transferWithData` whereas `canTransferFrom` allows the specification of the sender of tokens and that the transfer will be executed via `transferFrom` or `transferFromWithData`.

``` solidity
function canTransfer(address _to, uint256 _value, bytes _data) external view returns (byte, bytes32);
function canTransferFrom(address _from, address _to, uint256 _value, bytes _data) external view returns (byte, bytes32);
```

#### transferWithData

Transfer restrictions can take many forms and typically involve on-chain rules or whitelists. However for many types of approved transfers, maintaining an on-chain list of approved transfers can be cumbersome and expensive. An alternative is the co-signing approach, where in addition to the token holder approving a token transfer, and authorised entity provides signed data which further validates the transfer.

The `bytes _data` allows arbitrary data to be submitted alongside the transfer, for the token contract to interpret or record. This could be signed data authorising the transfer (e.g. a dynamic whitelist) but is flexible enough to accomadate other use-cases.

`transferWithData` MUST emit a `Transfer` event with details of the transfer.

``` solidity
function transferWithData(address _to, uint256 _value, bytes _data) external;
```

#### transferFromWithData

This is the analogy to the `transferWithData` function.

`msg.sender` MUST have a sufficient `allowance` set and this `allowance` must be debited by the `_value`.

``` solidity
function transferFromWithData(address _from, address _to, uint256 _value, bytes _data) external;
```

### Token Issuance

#### isIssuable

A security token issuer can specify that issuance has finished for the token (i.e. no new tokens can be minted or issued).

If a token returns FALSE for `isIssuable()` then it MUST always return FALSE in the future.

If a token returns FALSE for `isIssuable()` then it MUST never allow additional tokens to be issued.

``` solidity
function isIssuable() external view returns (bool);
```

#### issue

This function must be called to increase the total supply.

The `bytes _data` parameter can be used to inject off-chain data (e.g. signed data) to authorise or authenticate the issuance and receiver of issued tokens.

When called, this function MUST emit the `Issued` event.

``` solidity
function issue(address _tokenHolder, uint256 _value, bytes _data) external;
```

### Token Redemption

#### redeem

Allows a token holder to redeem tokens.

The redeemed tokens must be subtracted from the total supply and the balance of the token holder. The token redemption should act like sending tokens and be subject to the same conditions.

The `Redeemed` event MUST be emitted every time this function is called.

As with `transferWithData` this function has a `bytes _data` parameter that can be used in the token contract to authenticate the redemption.

``` solidity
function redeem(uint256 _value, bytes _data) external;
```

#### redeemFrom

This is the analogy to the `redeem` function.

`msg.sender` MUST have a sufficient `allowance` set and this `allowance` must be debited by the `_value`.

The `Redeemed` event MUST be emitted every time this function is called.

``` solidity
function redeemFrom(address _tokenHolder, uint256 _value, bytes _data) external;
```

## Interface

``` solidity
/// @title IERC1594 Security Token Standard
/// @dev See https://github.com/SecurityTokenStandard/EIP-Spec

interface IERC1594 is IERC20 {

    // Transfers
    function transferWithData(address _to, uint256 _value, bytes _data) external;
    function transferFromWithData(address _from, address _to, uint256 _value, bytes _data) external;

    // Token Issuance
    function isIssuable() external view returns (bool);
    function issue(address _tokenHolder, uint256 _value, bytes _data) external;

    // Token Redemption
    function redeem(uint256 _value, bytes _data) external;
    function redeemFrom(address _tokenHolder, uint256 _value, bytes _data) external;

    // Transfer Validity
    function canTransfer(address _to, uint256 _value, bytes _data) external view returns (bool, byte, bytes32);
    function canTransferFrom(address _from, address _to, uint256 _value, bytes _data) external view returns (bool, byte, bytes32);

    // Issuance / Redemption Events
    event Issued(address indexed _operator, address indexed _to, uint256 _value, bytes _data);
    event Redeemed(address indexed _operator, address indexed _from, uint256 _value, bytes _data);

}
```

## References
- [EIP 1400: Security Token Standard With Partitions](https://github.com/ethereum/EIPs/issues/1411)
- [EIP Draft](https://github.com/SecurityTokenStandard/EIP-Spec)














      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/1643)












####



        opened 04:49PM - 10 Dec 18 UTC



          closed 05:10AM - 05 Dec 21 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/c/c98b36137960f8d631813de8a2a586ca0b836961.jpeg)
          adamdossa](https://github.com/adamdossa)





          stale







---

eip: ERC-1643
title: Document Management Standard (part of the ERC-1400 […]()Security Token Standards)
author: Adam Dossa (@adamdossa), Pablo Ruiz (@pabloruiz55), Fabian Vogelsteller (@frozeman), Stephane Gosselin (@thegostep)
discussions-to: #1411
status: Draft
type: Standards Track
category: ERC
created: 2018-09-09
require: None

---

## Simple Summary

This standard sits under the ERC-1400 (#1411) umbrella set of standards related to security tokens.

Provides a standard to support attaching documentation to smart contracts, specifically security token contracts in the context of ERC-1400 (#1411).

## Abstract

Allows documents to be associated with a smart contract and a standard interface for querying / modifying these contracts, as well as receiving updates (via events) to changes on these documents.

Examples of documentation could include offering documents and legends associated with security tokens.

## Motivation

Accelerate the issuance and management of securities on the Ethereum blockchain by specifying a set of standard interfaces through which security tokens can be operated on and interrogated by all relevant parties.

Since security tokens and their ownership usually entails rights and obligations either from the investor or the issuer, the ability to associate legal documents with the relevant contracts is important. Doing this in a standardised way allows wallets, exchanges and other ecosystem members to provide a standard view of these documents, and allows investors to subscribe to updates in a standardised manner.

## Requirements

See ERC-1400 (#1411) for a full set of requirements across the library of standards.

The following requirements have been compiled following discussions with parties across the Security Token ecosystem.

- MUST support querying and subscribing to updates on any relevant documentation for the security.

## Rationale

Being able to attach documents to a security token allows the issuer, or other authorised entities, to communicate documentation associated with the security to token holders. An attached document can optionally include a hash of its contents in order to provide an immutability guarantee.

## Specification

These functions are used to manage a library of documents associated with the token. These documents can be legal documents, or other reference materials.

A document is associated with a short name (represented as a `bytes32`), a modified timestamp, and can optionally have a hash of the document contents associated with it on-chain.

It is referenced via a generic URI that could point to a website or other document portal.

### getDocument

Used to return the details of a document with a known name (`bytes32`). Returns the URI associated with the document (`string`), the hash (of the contents) of the document (`bytes32`), and the timestamp at which the document was last modified via `setDocument` (`uint256`).

``` solidity
function getDocument(bytes32 _name) external view returns (string, bytes32, uint256);
```

### setDocument

Used to attach a new document to the contract, or update the URI or hash of an existing attached document.

`setDocument` MUST throw if the document is not successfully stored.

`setDocument` MUST emit a `DocumentUpdated` event with details of the document being attached or modified.

``` solidity
function setDocument(bytes32 _name, string _uri, bytes32 _documentHash) external;
```

### removeDocument

Used to remove an existing document from the contract.

`removeDocument` MUST throw if the document is not successfully removed.

`removeDocument` MUST emit a `DocumentRemoved` event with details of the document being attached or modified.

``` solidity
function removeDocument(bytes32 _name) external;
```

### getAllDocuments

Used to retrieve a full list of documents attached to the smart contract.

Any document added via `setDocument` and not subsequently removed via the `removeDocument` function MUST be returned.

``` solidity
function getAllDocuments() view returns (bytes32[]);
```

## Interface

``` solidity
/// @title IERC1643 Document Management (part of the ERC1400 Security Token Standards)
/// @dev See https://github.com/SecurityTokenStandard/EIP-Spec

interface IERC1643 {

    // Document Management
    function getDocument(bytes32 _name) external view returns (string, bytes32, uint256);
    function setDocument(bytes32 _name, string _uri, bytes32 _documentHash) external;
    function removeDocument(bytes32 _name) external;
    function getAllDocuments() external view returns (bytes32[]);

    // Document Events
    event DocumentRemoved(bytes32 indexed _name, string _uri, bytes32 _documentHash);
    event DocumentUpdated(bytes32 indexed _name, string _uri, bytes32 _documentHash);

}
```

## References
- [EIP 1400: Security Token Standard With Partitions](https://github.com/ethereum/EIPs/issues/1411)
- [EIP Draft](https://github.com/SecurityTokenStandard/EIP-Spec)














      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/1644)












####



        opened 04:50PM - 10 Dec 18 UTC



          closed 05:10AM - 05 Dec 21 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/c/c98b36137960f8d631813de8a2a586ca0b836961.jpeg)
          adamdossa](https://github.com/adamdossa)





          stale







---

eip: ERC-1644
title: Controller Token Operation Standard (part of the ER[…]()C-1400 Security Token Standards)
author: Adam Dossa (@adamdossa), Pablo Ruiz (@pabloruiz55), Fabian Vogelsteller (@frozeman), Stephane Gosselin (@thegostep)
discussions-to: #1411
status: Draft
type: Standards Track
category: ERC
created: 2018-09-09
require: None

---

## Simple Summary

This standard sits under the ERC-1400 (#1411) umbrella set of standards related to security tokens.

Provides a standard to support controller operations (aka forced transfers) on tokens.

## Abstract

Allows a token to transparently declare whether or not a controller can unilaterally transfer tokens between addresses.

## Motivation

Accelerate the issuance and management of securities on the Ethereum blockchain by specifying a set of standard interfaces through which security tokens can be operated on and interrogated by all relevant parties.

Since security tokens are subject to regulatory and legal oversight (the details of which will vary depending on jurisdiction, regulatory framework and underlying asset) in many instances the issuer (or a party delegated to by the issuer acting as a controller, e.g. a regulator or transfer agent) will need to retain the ability to force transfer tokens between addresses.

These controller transfers should be transparent (emit events that flag this as a forced transfer) and the token contract itself should be explicit as to whether or not this is possible.

Examples of where this may be needed is to reverse fraudulent transactions, resolve lost private keys and responding to a court order.

## Requirements

See ERC-1400 (#1411) for a full set of requirements across the library of standards.

The following requirements have been compiled following discussions with parties across the Security Token ecosystem.

- MUST be able to perform forced transfer for legal action or fund recovery.

## Rationale

Given the conflict between this functionality and the decentralised nature of Ethereum, making such actions, and the ability to execute these transactions, as transparent as possible allows different use-cases to comply with the standard.

## Rationale

A token representing ownership in a security may require authorised operators to have additional controls over the tokens.

This includes the ability to issue additional supply, as well as make forced transfers of tokens. The standard allows these controls to be managed and also critically ensures their transparency. If an issuer requires the ability to issue additional tokens, or make controller transfers (forced transfers) then these rights can be transparently assessed rather than being implemented in a bespoke or obfuscated manner.

## Specification

In some jurisdictions the issuer (or an entity delegated to by the issuer) may need to retain the ability to force transfer tokens. This could be to address a legal dispute or court order, or to remedy an investor losing access to their private keys.

#### controllerTransfer

This function allows an authorised address to transfer tokens between any two token holders. The transfer must still respect the balances of the token holders (so the transfer must be for at most `balanceOf(_from)` tokens) and potentially also need to respect other transfer restrictions.

`controllerTransfer` MUST emit a `ControllerTransfer` event.

``` solidity
function controllerTransfer(address _from, address _to, uint256 _value, bytes _data, bytes _operatorData) external;
```

#### controllerRedeem

This function allows an authorised address to redeem tokens for any token holder. The redemption must still respect the balances of the token holder (so the redemption must be for at most `balanceOf(_tokenHolder)` tokens) and potentially also need to respect other transfer restrictions.

`controllerTransfer` MUST emit a `ControllerRedemption` event.

``` solidity
function controllerRedeem(address _tokenHolder, uint256 _value, bytes _data, bytes _operatorData) external;
```

#### isControllable

In order to provide transparency over whether `controllerTransfer` / `controllerRedeem` are useable, the function `isControllable` can be used.

If a token returns FALSE for `isControllable()` then it MUST:
  - always return FALSE in the future.
  - `controllerTransfer` must revert
  - `controllerRedeem` must revert

In other words, if an issuer sets `isControllable` to return FALSE, then there can be no further controller transactions for this token contract.

``` solidity
function isControllable() external view returns (bool);
```

## Interface

``` solidity
/// @title IERC1644 Controller Token Operation (part of the ERC1400 Security Token Standards)
/// @dev See https://github.com/SecurityTokenStandard/EIP-Spec

interface IERC1644 is IERC20 {

    // Controller Operation
    function isControllable() external view returns (bool);
    function controllerTransfer(address _from, address _to, uint256 _value, bytes _data, bytes _operatorData) external;
    function controllerRedeem(address _tokenHolder, uint256 _value, bytes _data, bytes _operatorData) external;

    // Controller Events
    event ControllerTransfer(
        address _controller,
        address indexed _from,
        address indexed _to,
        uint256 _value,
        bytes _data,
        bytes _operatorData
    );

    event ControllerRedemption(
        address _controller,
        address indexed _tokenHolder,
        uint256 _value,
        bytes _data,
        bytes _operatorData
    );

}
```

## References
- [EIP 1400: Security Token Standard With Partitions](https://github.com/ethereum/EIPs/issues/1411)
- [EIP Draft](https://github.com/SecurityTokenStandard/EIP-Spec)

---

**AccessDenied403** (2026-01-14):

Hello,

I am “re-open” the conversation around ERC-1400.

Since this ERC has been in use for a long time to tokenize assets on-chain (RWA), it would make sense to finalize it.

For ERC-1643, I made also a specific topic since the standard is independent from the underlying token: [ERC-1643: Document Management Standard (ERC-1400)](https://ethereum-magicians.org/t/erc-1643-document-management-standard-erc-1400/27437)

See also [ERC-1400 and ERC-1410 - Security Token and Partially Fungible Token](https://ethereum-magicians.org/t/erc-1400-and-erc-1410-security-token-and-partially-fungible-token/1314)

Best!

