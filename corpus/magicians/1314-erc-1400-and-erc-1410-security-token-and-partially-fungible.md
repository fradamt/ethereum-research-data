---
source: magicians
topic_id: 1314
title: ERC-1400 and ERC-1410 - Security Token and Partially Fungible Token
author: jpitts
date: "2018-09-12"
category: EIPs
tags: [security-token, erc-1400, finance]
url: https://ethereum-magicians.org/t/erc-1400-and-erc-1410-security-token-and-partially-fungible-token/1314
views: 6540
likes: 16
posts_count: 15
---

# ERC-1400 and ERC-1410 - Security Token and Partially Fungible Token

*Important update: after feedback, ERC-1400 (Security Token Standard) was split, so that now there is a related proposal ERC-1410 (Partially Fungible Token Standard).*

---

From Adam Dossa, Pablo Ruiz [@pabloruiz55](/u/pabloruiz55), Fabian Vogelsteller [@frozeman](/u/frozeman), Stephane Gosselin [@thegostep](/u/thegostep):

> ## Motivation
>
>
>
> Accelerate the issuance and management of securities on the Ethereum blockchain by specifying a standard interface through which security tokens can be operated on and interrogated by all relevant parties.
>
>
> Security tokens differ materially from other token use-cases, with more complex interactions between off-chain and on-chain actors, and considerable regulatory scrutiny.
>
>
> Security tokens should be able to represent any asset class, be issued and managed across any jurisdiction, and comply with the associated regulatory restrictions.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/1411)












####



        opened 09:22PM - 13 Sep 18 UTC



          closed 07:09AM - 11 Jun 22 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/c/c98b36137960f8d631813de8a2a586ca0b836961.jpeg)
          adamdossa](https://github.com/adamdossa)





          stale







---

eip: ERC-1400
title: Security Token Standards
author: Adam Dossa (@adam[…]()dossa), Pablo Ruiz (@pabloruiz55), Fabian Vogelsteller (@frozeman), Stephane Gosselin (@thegostep)
discussions-to: #1411
status: Draft
type: Standards Track
category: ERC
created: 2018-09-09
require: ERC-1410 (#1410), ERC-1594 (#1594), ERC-1644 (#1644), ERC-1643 (#1643), ERC-20 (#20), ERC-1066 (#1066)

---

## Simple Summary

Represents a library of standards for security tokens on Ethereum.

In aggregate provides a suite of standard interfaces for issuing / redeeming security tokens, managing their ownership and transfer restrictions and providing transparency to token holders on how different subsets of their token balance behave with respect to transfer restrictions, rights and obligations.

## Abstract

Standards should be backwards compatible with ERC-20 (#20) and easily extended to be compatible with ERC-777 (#777).

ERC-1410 (#1410): differentiated ownership / transparent restrictions
ERC-1594 (#1594): on-chain restriction checking with error signalling, off-chain data injection for transfer restrictions and issuance / redemption semantics
ERC-1643 (#1643): document / legend management
ERC-1644 (#1644): controller operations (force transfer)

## Motivation

Accelerate the issuance and management of securities on the Ethereum blockchain by specifying standard interfaces through which security tokens can be operated on and interrogated by all relevant parties.

Taken together, these security token standards provide document management, error signalling, gate keeper (operator) access control, off-chain data injection, issuance / redemption semantics and expose partially fungible subsets of a token holders balance.

## Requirements

Moving the issuance, trading and lifecycle events of a security onto a public ledger requires having a standard way of modelling securities, their ownership and their properties on-chain.

The following requirements have been compiled following discussions with parties across the Security Token ecosystem.

- MUST have a standard interface to query if a transfer would be successful and return a reason for failure.
- MUST be able to perform forced transfer for legal action or fund recovery.
- MUST emit standard events for issuance and redemption.
- MUST be able to attach metadata to a subset of a token holder's balance such as special shareholder rights or data for transfer restrictions.
- MUST be able to modify metadata at time of transfer based on off-chain data, on-chain data and the parameters of the transfer.
- MUST support querying and subscribing to updates on any relevant documentation for the security.
- MAY require signed data to be passed into a transfer transaction in order to validate it on-chain.
- SHOULD NOT restrict the range of asset classes across jurisdictions which can be represented.
- MUST be ERC-20 compatible.
- COULD be ERC-777 compatible.

## Rationale

### ERC-1594: Core Security Token Standard

Transfers of securities can fail for a variety of reasons in contrast to utility tokens which generally only require the sender to have a sufficient balance.

These conditions could be related to metadata of the securities being transferred (i.e. whether they are subject to a lock-up period), the identity of the sender and receiver of the securities (i.e. whether they have been through a KYC process, whether they are accredited or an affiliate of the issuer) or for reasons unrelated to the specific transfer but instead set at the token level (i.e. the token contract enforces a maximum number of investors or a cap on the percentage held by any single investor).

For ERC-20 tokens, the `balanceOf` and `allowance` functions provide a way to check that a transfer is likely to succeed before executing the transfer, which can be executed both on and off-chain.

For tokens representing securities the standard introduces a function `canTransfer` / `canTransferByPartition` which provides a more general purpose way to achieve this when the reasons for failure are more complex; and a function of the whole transfer (i.e. includes any data sent with the transfer and the receiver of the securities).

In order to provide a richer result than just true or false, a byte return code is returned. This allows us to give a reason for why the transfer failed, or at least which category of reason the failure was in. The ability to query documents and the expected success of a transfer is included in Security Token section.

In order to support off-chain data inputs to transfer functions, transfer functions are extended to `transferWithData` / `transferFromWithData` which can optionally take an additional `bytes _data` parameter.

### ERC-1410: Partially Fungible Tokens

There are many types of securities which, although they represent the same underlying asset, need to have differentiating data tied to them.

This additional metadata implicitly renders these securities non-fungible, but in practice this data is usually applied to a subset of the security rather than an individual security. The ability to partition a token holder's balance into partitions, each with separate metadata is addressed in the Partially Fungible Token section.

For example a token holder's balance may be split in two: those tokens issued during the primary issuance, and those received through secondary trading.

Security token contracts can reference this metadata in order to apply additional logic to determine whether or not a transfer is valid, and determine the metadata that should be associated with the tokens once transferred into the receiver's balance.

Alternatively a security token can use this mechanism simply to be able to transparently display to investors how different subsets of their tokens will behave with respect to transfer restrictions. In this case, the balances could be determined programatically.

### ERC-1643: Document Management Standard

Security tokens usually have documentation associated with them. This could be an offering document, legend details and so on.

Being able to set / remove and retrieve these documents, and having events associated with these actions allows investors to stay up to date with documentation on their investments.

This standard does not provide any way for an investor to signal on-chain that they have read, or agree, with any of these documents.

### ERC-1644: Controller Token Operation Standard

Since security tokens are subject to regulatory and legal oversight (the details of which will vary depending on jurisdiction, regulatory framework and underlying asset) in many instances the issuer (or a party delegated to by the issuer acting as a controller, e.g. a regulator or transfer agent) will need to retain the ability to force transfer tokens between addresses.

These controller transfers should be transparent (emit events that flag this as a forced transfer) and the token contract itself should be explicit as to whether or not this is possible.

Examples of where this may be needed is to reverse fraudulent transactions, resolve lost private keys and responding to a court order.

## Specification

This standard does not specify any additional functions, but references ERC-1410 (#1410), ERC-1594 (#1594), ERC-1643 (#1643) and ERC-1655 (#1644) as an underlying library of security token standards, each covering a different aspect of security token functionality.

In order to combine these two standards, the additional constraints are specified.

### operatorTransferByPartition

If the token is controllable (`isControllable` returns `TRUE`) then the controller may use `operatorTransferByPartition` without being explicitly authorised by the token holder.

In this instance, the `operatorTransferByPartition` MUST also emit a ControllerTransfer event.

Correspondingly, if `isControllable` returns `FALSE` then the controller cannot call `operatorTransferByPartition` unless explicitly authorised by the token holder.

### operatorRedeemByPartition

If the token is controllable (`isControllable` returns `TRUE`) then the controller may use `operatorRedeemByPartition` without being explicitly authorised by the token holder.

In this instance, the `operatorRedeemByPartition` MUST also emit a ControllerRedemption event.

Correspondingly, if `isControllable` returns `FALSE` then the controller cannot call `operatorRedeemByPartition` unless explicitly authorised by the token holder.

### Default Partitions

In order for `transfer` and `transferWithData` to operate on partially fungible tokens, there needs to be some notion of default partitions that these functions apply to. The details for how these are determined (e.g. either a fixed list, dynamically, or using `partitionsOf`) is left as an implementation detail rather than defined as part of the standard.

When transferring tokens as part of a `transfer` or `transferWithData` operation, these transfers should respect the invariant of partially fungible tokens, namely that the sum of the balances across all partitions should equal to the total balance of a token holder.

## Interface

``` solidity
/// @title IERC1400 Security Token Standard
/// @dev See https://github.com/SecurityTokenStandard/EIP-Spec

interface IERC1400 is IERC20 {

  // Document Management
  function getDocument(bytes32 _name) external view returns (string, bytes32);
  function setDocument(bytes32 _name, string _uri, bytes32 _documentHash) external;

  // Token Information
  function balanceOfByPartition(bytes32 _partition, address _tokenHolder) external view returns (uint256);
  function partitionsOf(address _tokenHolder) external view returns (bytes32[]);

  // Transfers
  function transferWithData(address _to, uint256 _value, bytes _data) external;
  function transferFromWithData(address _from, address _to, uint256 _value, bytes _data) external;

  // Partition Token Transfers
  function transferByPartition(bytes32 _partition, address _to, uint256 _value, bytes _data) external returns (bytes32);
  function operatorTransferByPartition(bytes32 _partition, address _from, address _to, uint256 _value, bytes _data, bytes _operatorData) external returns (bytes32);

  // Controller Operation
  function isControllable() external view returns (bool);
  function controllerTransfer(address _from, address _to, uint256 _value, bytes _data, bytes _operatorData) external;
  function controllerRedeem(address _tokenHolder, uint256 _value, bytes _data, bytes _operatorData) external;

  // Operator Management
  function authorizeOperator(address _operator) external;
  function revokeOperator(address _operator) external;
  function authorizeOperatorByPartition(bytes32 _partition, address _operator) external;
  function revokeOperatorByPartition(bytes32 _partition, address _operator) external;

  // Operator Information
  function isOperator(address _operator, address _tokenHolder) external view returns (bool);
  function isOperatorForPartition(bytes32 _partition, address _operator, address _tokenHolder) external view returns (bool);

  // Token Issuance
  function isIssuable() external view returns (bool);
  function issue(address _tokenHolder, uint256 _value, bytes _data) external;
  function issueByPartition(bytes32 _partition, address _tokenHolder, uint256 _value, bytes _data) external;

  // Token Redemption
  function redeem(uint256 _value, bytes _data) external;
  function redeemFrom(address _tokenHolder, uint256 _value, bytes _data) external;
  function redeemByPartition(bytes32 _partition, uint256 _value, bytes _data) external;
  function operatorRedeemByPartition(bytes32 _partition, address _tokenHolder, uint256 _value, bytes _operatorData) external;

  // Transfer Validity
  function canTransfer(address _to, uint256 _value, bytes _data) external view returns (byte, bytes32);
  function canTransferFrom(address _from, address _to, uint256 _value, bytes _data) external view returns (byte, bytes32);
  function canTransferByPartition(address _from, address _to, bytes32 _partition, uint256 _value, bytes _data) external view returns (byte, bytes32, bytes32);

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

  // Document Events
  event Document(bytes32 indexed _name, string _uri, bytes32 _documentHash);

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

  event ChangedPartition(
      bytes32 indexed _fromPartition,
      bytes32 indexed _toPartition,
      uint256 _value
  );

  // Operator Events
  event AuthorizedOperator(address indexed _operator, address indexed _tokenHolder);
  event RevokedOperator(address indexed _operator, address indexed _tokenHolder);
  event AuthorizedOperatorByPartition(bytes32 indexed _partition, address indexed _operator, address indexed _tokenHolder);
  event RevokedOperatorByPartition(bytes32 indexed _partition, address indexed _operator, address indexed _tokenHolder);

  // Issuance / Redemption Events
  event Issued(address indexed _operator, address indexed _to, uint256 _value, bytes _data);
  event Redeemed(address indexed _operator, address indexed _from, uint256 _value, bytes _data);
  event IssuedByPartition(bytes32 indexed _partition, address indexed _operator, address indexed _to, uint256 _value, bytes _data, bytes _operatorData);
  event RedeemedByPartition(bytes32 indexed _partition, address indexed _operator, address indexed _from, uint256 _value, bytes _operatorData);

}
```

### Notes

#### On-chain vs. Off-chain Transfer Restrictions

The rules determining if a security token can be sent may be self-executing (e.g. a rule which limits the maximum number of investors in the security) or require off-chain inputs (e.g. an explicit broker approval for the trade). To facilitate the latter, the `transferByPartition`, `transferWithData`, `transferFromWithData`, `canTransferByPartition` and `canTransfer` functions accept an additional `bytes _data` parameter which can be signed by an approved party and used to validate a transfer.

The specification for this data is outside the scope of this standard and would be implementation specific.

#### Identity

Under many jurisdictions, whether a party is able to receive and send security tokens depends on the characteristics of the party's identity. For example, most jurisdictions require some level of KYC / AML process before a party is eligible to purchase or sell a particular security. Additionally, a party may be categorized into an investor qualification category (e.g. accredited investor, qualified purchaser), and their citizenship may also inform restrictions associated with their securities.

There are various identity standards (e.g. ERC-725 (#725), Civic, uPort) which can be used to capture the party's identity data, as well as other approaches which are centrally managed (e.g. maintaining a whitelist of addresses that have been approved from a KYC perspective). These identity standards have in common to key off an Ethereum address (which could be a party's wallet, or an identity contract), and as such the `canTransfer` function can use the address of both the sender and receiver of the security token as a proxy for identity in deciding if eligibility requirements are met.

Beyond this, the standard does not mandate any particular approach to identity.

#### Reason Codes

To improve the token holder experience, `canTransfer` MUST return a reason byte code on success or failure based on the EIP-1066 application-specific status codes specified below. An implementation can also return arbitrary data as a `bytes32` to provide additional information not captured by the reason code.

| Code   | Reason                                                        |
| ------ | ------------------------------------------------------------- |
| `0x50` | 	transfer failure                                             |
| `0x51` | 	transfer success                                             |
| `0x52` | 	insufficient balance                                         |
| `0x53` | 	insufficient allowance                                       |
| `0x54` | 	transfers halted (contract paused)                           |
| `0x55` | 	funds locked (lockup period)                                 |
| `0x56` | 	invalid sender                                               |
| `0x57` | 	invalid receiver                                             |
| `0x58` | 	invalid operator (transfer agent)                            |
| `0x59` |                                                               |
| `0x5a` |                                                               |
| `0x5b` |                                                               |
| `0x5a` |                                                               |
| `0x5b` |                                                               |
| `0x5c` |                                                               |
| `0x5d` |                                                               |
| `0x5e` |                                                               |
| `0x5f` | 		token meta or info

These codes are being discussed at:
https://ethereum-magicians.org/t/erc-1066-ethereum-status-codes-esc/283/24

## References
- [EIP 1410: Partially Fungible Token Standard](https://github.com/ethereum/EIPs/issues/1410)
- [EIP 1594: Core Security Token Standard](https://github.com/ethereum/EIPs/issues/1594)
- [EIP 1643: Document Management Standard](https://github.com/ethereum/EIPs/issues/1643)
- [EIP 1644: Controller Token Operation Standard](https://github.com/ethereum/EIPs/issues/1644)
- [EIP Draft](https://github.com/SecurityTokenStandard/EIP-Spec)

_Copied from original issue_: https://github.com/ethereum/EIPs/issues/1400














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

## Replies

**fubuloubu** (2018-09-12):

Very well written, I see no technical (read: software) problems with the proposal.

However, this is definitely a case of a proposal with the need for strong legal technicalities. I am sure the proposer has done due diligence as the proposal is well written, but I am curious from which jurisdictions this has been evaluated from a legal standpoint. SEC is a big one, ESMA for Europe, Hong Kong SFC, etc.

I think adoption of this proposal is likely to hinge on the answers to various legal questions, so I think this should be determined first.

---

Also, another nitpicky thing: I think semi-fungible tokens (the denomination of a user’s balance by tranches, and the possibility of restriction of transferrability by tranches) should be a separate standard. There is a lot being proposed here, and I think the separation of this functionality from security- and custodian-specific functionality would make this proposal better off.

It’s funny, because I was making a similar suggestion for reputation tokens (to be semi-fungible) just the other day.

---

**ben-kaufman** (2018-09-12):

I agree this standard should be separated into a partially fungible token and security token. I think the partially fungible standard can be very useful in a lot of cases.

---

**boris** (2018-09-13):

I’ve reached out to the team to schedule a community call.

They’re requiring [#erc-1066](https://ethereum-magicians.org/tags/erc-1066) as a dependency – which is great! [@expede](/u/expede) came up with it because we were trying to solve issues around security tokens and messages around whitelisting.

Looks like one of the authors [@thegostep](/u/thegostep) joined us here. Welcome!

Legal should be considered a SEPARATE layer. I know everyone is freaked out about this, but we need technical interoperability as a foundation to tweak the legal bits. So far, lawyers have tweaked implementation of security tokens on a one off basis (no joke), which is not the way to make for interoperability.

Yes the work needs to be done to review, but I have found that I’m the one suggesting *technically* how things can be done to meet legal needs, not the other way around.

---

**AdamDossa** (2018-09-13):

Thanks for the feedback (this is Adam, one of the EIP authors from Polymath).

re. splitting the proposal into a partially fungible token standard (e.g. tranches) & security token standard (`checkSecurityTokenSend` etc.) - this is something we debated internally and in fact was the original way we structured the EIP (as two separate related standards). In the end we decided we didn’t want to fracture the conversation across two EIPs so combined.

The PFT standard has some interesting non-securities applications (e.g. token provenance, in-game bonus mechanics) which we are putting together as a fun medium article right now.

A community call would be great - very interested in more discussion around #1066 which we’ve discussed a lot internally (and which led to the return argument specification for `checkSecurityTokenSend`).

One question I have for more experienced forum members - currently we see the conversation being split between Ethereum Magicians and the GitHub Issue - is there prior art on the best way to manage this to keep the conversation in one place?

---

**pabloruiz55** (2018-09-13):

Hey [@Boris](/u/boris), Pablo here, one of the authors as well.

I have been lurking this forum for long now and joined the Token Ring a while ago. I know there will be some action going on prior to Devcon, at the Council of Prague and I was wondering how we could bring up this EIP over there to get even more discussion around it. What would be the process for organizing this up?

---

**boris** (2018-09-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/adamdossa/48/817_2.png) AdamDossa:

> One question I have for more experienced forum members - currently we see the conversation being split between Ethereum Magicians and the GitHub Issue - is there prior art on the best way to manage this to keep the conversation in one place?

No, sorry, people will use both ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12) There is the discussion-to in the head of the EIP so you can create a forum thread here if you like.

You can request technical points in GitHub and choose eg this thread for broader points.

Re: community call. Great — it’s something I’ve been thinking of for a while so can help schedule / get the word out. Basically a live call, get people to share questions in advance, and then authors answer questions.

Just like Core Dev calls, I think this can be a useful pattern to follow.

---

**boris** (2018-09-13):

Add it to the agenda! There is some [discussion here](https://ethereum-magicians.org/t/council-of-prague-agenda-topics/1308), I think this is a broad topic of interest so you can have space set aside to gather people.

Also: EIPs & Interoperability track at the Status Hackathon the days before council.

I submitted a talk to Devcon around the broad security token topic but didn’t get approved. We’ll have to see if there is anything in the schedule when it goes live, and encourage people to come earlier if they really want to dig in.

---

**pabloruiz55** (2018-09-13):

Thanks [@boris](/u/boris) I added the topic under the Token Ring on [@ChainSafe](/u/chainsafe) 's doc. Is that the right place, though? [Pre Council Call For Rings](https://ethereum-magicians.org/t/pre-council-call-for-rings/1289)

We submitted a bunch of Security Token related talks for Devcon. Sadly none of them were approved. No love for STs over there ![:frowning:](https://ethereum-magicians.org/images/emoji/twitter/frowning.png?v=9)

---

**boris** (2018-09-13):

Huh. OK, good to know on Devcon. But, that’s why we have EthMagicians. I’ll dig a bit more.

Yeah, that pre-council call is a good start. Need to find out who the Token Ring organizers are. Gathering signaling that there are groups that want to talk about this is a good start – we can point people there for now and mention it in the community call.

---

**AdamDossa** (2018-09-14):

Based on feedback here and on GitHub, we’ve split the EIP into two separate standards - the [Partially Fungible Token Standard](https://github.com/ethereum/EIPs/issues/1410) and [Security Token Standard](https://github.com/ethereum/EIPs/issues/1411).

There was a further discussion as to whether other parts (forced transfers, document management, verified transfers) should be further split out, but this seems to have more trade-offs in terms of adoption and consistency for security tokens, so leaving this as a possible future change rather than including it in this change.

---

**AdamDossa** (2018-09-14):

@ [jpitts](https://ethereum-magicians.org/u/jpitts) if you’re able to update the reference in the title post to reference the new link above that would be very useful (and hopefully stop the conversation from forking). We are going to close the original issue shortly to move the conversation over to this new one https://github.com/ethereum/EIPs/issues/1411 and of course we hope it will continue here as well!

---

**jpitts** (2018-09-14):

[@AdamDossa](/u/adamdossa), thanks for the heads-up. I have updated the title and my topic intro.

---

**AdamDossa** (2018-09-29):

We have a second community call scheduled for this Tuesday (4th October).

Details at:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/adamdossa/48/817_2.png)
    [2nd Community Call: ERC1400 Feedback, Discussion & Questions](https://ethereum-magicians.org/t/2nd-community-call-erc1400-feedback-discussion-questions/1475) [Tokens](/c/tokens/18)



> We would like to have a second community call related to ERC1400 following on from the previous call documented at:
>
>
> When: Tuesday, October 2nd, 11AM EST world time check
> Call Details: Zoom
> Join from PC, Mac, Linux, iOS or Android: https://zoom.us/j/963516600
> Or iPhone one-tap :
> US: +16465588656,963516600#  or +16699006833,963516600#
> Or Telephone:
> Dial(for higher quality, dial a number based on your current location):
> US: +1 646 558 8656  or +1 669 900 6833
> Meeting ID: 963 516 600
> I…

When: Tuesday, October 2nd, 11AM EST [world time check](https://www.timeanddate.com/worldclock/fixedtime.html?msg=ETHMagicians+Community+Call+ERC1400&iso=20181002T08&p1=224&ah=1&am=30)

Call Details: Zoom

Join from PC, Mac, Linux, iOS or Android: [Launch Meeting - Zoom](https://zoom.us/j/963516600)

Or iPhone one-tap :

US: +16465588656,963516600# or +16699006833,963516600#

Or Telephone:

Dial(for higher quality, dial a number based on your current location):

US: +1 646 558 8656 or +1 669 900 6833

Meeting ID: 963 516 600

International numbers available: [Zoom International Dial-in Numbers - Zoom](https://zoom.us/u/acB6ZYvJ6)

---

**pkrasam** (2019-08-03):

Where can I find the latest update on ERC-1400 and ERC-1410

