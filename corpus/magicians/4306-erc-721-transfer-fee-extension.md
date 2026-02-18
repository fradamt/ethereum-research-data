---
source: magicians
topic_id: 4306
title: ERC-721 Transfer Fee Extension
author: Nokhal
date: "2020-05-21"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/erc-721-transfer-fee-extension/4306
views: 1023
likes: 0
posts_count: 1
---

# ERC-721 Transfer Fee Extension

Hello. Here is yet another proposal for an ERC-721 extension aiming at allowing publishers to collect a fee when an NFT change hand. What is different this time ?

This standard proposal only aim at defining the most generic, interoperable interface and come with a way to guarantee that a future Transfer transaction would not fail due to the lack of an appropriate fee amount being paid.

Nft creators are free to implement any ecosystem they want, and as long as they properly expose their token with this standard, third parties will be able to interact with their pricing mechanism in a “Black-Box” fashion, without having to specifically craft a solution adapted to a single NFT project.

This EIP is gonna be championed by a soon to launch ERC-721 token featuring it’s own, complex pricing mechanism and separate, publisher controlled marketplace, but integrators and third party marketplaces would only need to be aware of this relatively simple ERC-721 extension (Only one new function added, no transaction flow differences) to be able to manipulate this token without issues.

Any input you may have is appreciated, be it technical or conceptual, be it coming from an another NFT publisher or a Wallet/Marketplace.

Once again, the goal is to foster interoperability for NFTs that want a Transfer Fee to be the publisher decision and not the owner’s decision.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/2665)












####



        opened 10:48AM - 21 May 20 UTC



          closed 02:02PM - 29 May 22 UTC



        [![](https://avatars.githubusercontent.com/u/13810287?v=4)
          Nokhal](https://github.com/Nokhal)





          stale







---
eip: 2665 ?
title: ERC-721 Transfer Fee Extension
author: Guillaume Gonna[…]()ud  <g.gonnaud@perpetual-altruism.org>
discussions-to: https://github.com/ethereum/EIPs/issues/2665 [ethereum-magicians Thread](https://ethereum-magicians.org/t/erc-721-transfer-fee-extension/4306)
status: WIP
type: Standards Track
category: ERC
created: 2020-05-21
---

In the following, it is assumed that the attributed EIP number will be 2665, as it is traditionnally the issue number of this thread. However, an EIP number has yet to be formally attributed.

Simple Summary
===============

An ERC-721 extension allowing publishers to specify if a transfer fee should be paid with every transfer. The fee currency is defaulted to ETH, but ERC-20 tokens or even non-crypto currencies are within the scope of the standard.

Abstract
===============

The following standard is an extension of the ERC-721 standard. It exposes a queryable Transfer Fee that needs to be paid for a transfer to be processed.

In order to allow for the same transaction flow as a non-payable Transfer ERC-721 implementation, an *eval to 0 remanence guarantee* on the Transfer Fee is introduced, as well as the possibility for an operator/owner to use the `approve` function to pay the Transfer Fee.

Motivation
===============

Some processes and products require third parties to be properly incentivized in order to be perennial.  *E.g.* gas fee and block reward paid to miners on the Ethereum blockchain. Content creator remuneration is not a new problem, with multi-billion dollar industries being created and destroyed around the various solutions that have emerged to tackle it. Ethereum, and blockchains in general, are most likely going to be the backbone of the next paradigm shift.

Previous ERC-721 extension EIPs describe new ways to incentivise content creators. However, they often require a fundamental change in the transaction flow of NFTs. The current NFT ecosystem and standards are already proven, and fundamental changes are not needed to solve this issue.

**A very minor extension of the ERC-721 specification would allow both wide interoperability and strong creator incentivization.**

*Author's note: As the NFT ecosystem is developing at an astonishing pace, a standard that allows a reliable incentivization structure may be what is needed to unlock a trustless digital ownership revolution pushed by media majors, marketplaces and creators.*

ERC-721 allows for `safeTransferFrom` and `transferFrom` to be *payable* as a weak mutability guarantee; it allows, for example, the creator of the token to collect a fee. However the *payable* being the weakest guarantee and the lack of specification for an explorable fee led to most ERC-721 token ending up being transferrable for free.
`Approve` also has *payable* as the weakest guarantee. While `Approve` has a different use case than `TransferFrom`, sellers could use `Approve` to pay in advance a potential transfer fee on behalf of the operator.

Specification
===============

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" are to be interpreted as described in RFC 2119.
​

**Every ERC-2665 compliant contract MUST implement the `ERC721`, `ERC165` and `ERC2665` interfaces** (subject to "caveats" below):

```solidity
pragma solidity ^0.6.6;

/// @title ERC-2665 NFT Transfer Fee Extension
/// @dev See https://github.com/ethereum/EIPs/issues/2665
///  Note: the ERC-165 identifier for this interface is 0x509ffea4.
///  Note: you must also implement the ERC-165 identifier of ERC-721, which is 0x80ac58cd.
interface ERC2665 /* is ERC165, is ERC721 but overide it's Design by contract specifications */ {
    /// @dev This emits when ownership of any NFT changes by any mechanism.
    ///  This event emits when NFTs are created (`from` == 0) and destroyed
    ///  (`to` == 0). Exception: during contract creation, any number of NFTs
    ///  may be created and assigned without emitting Transfer. At the time of
    ///  any transfer, the approved address for that NFT (if any) is reset to none.
    event Transfer(address indexed _from, address indexed _to, uint256 indexed _tokenId);

    /// @dev This emits when the approved address for an NFT is changed or
    ///  reaffirmed. The zero address indicates there is no approved address.
    ///  When a Transfer event emits, this also indicates that the approved
    ///  address for that NFT (if any) is reset to none.
    event Approval(address indexed _owner, address indexed _approved, uint256 indexed _tokenId);

    /// @dev This emits when an operator is enabled or disabled for an owner.
    ///  The operator can manage all NFTs of the owner.
    event ApprovalForAll(address indexed _owner, address indexed _operator, bool _approved);

    /// @notice Count all NFTs assigned to an owner
    /// @dev NFTs assigned to the zero address are considered invalid, and this
    ///  function throws for queries about the zero address.
    /// @param _owner An address for whom to query the balance
    /// @return The number of NFTs owned by `_owner`, possibly zero
    function balanceOf(address _owner) external view returns (uint256);

    /// @notice Find the owner of an NFT
    /// @dev NFTs assigned to zero address are considered invalid, and queries
    ///  about them do throw.
    /// @param _tokenId The identifier for an NFT
    /// @return The address of the owner of the NFT
    function ownerOf(uint256 _tokenId) external view returns (address);

    /// @notice Transfers the ownership of an NFT from one address to another address
    /// @dev Throws unless `msg.sender` is the current owner, an authorized
    ///  operator, or the approved address for this NFT. Throws if `_from` is
    ///  not the current owner. Throws if `msg.value` < `getTransferFee(_tokenId)`.
    ///  If the fee is not to be paid in ETH, then token publishers SHOULD provide a way to pay the
    ///  fee when calling this function or it's overloads, and throwing if said fee is not paid.
    ///  Throws if `_to` is the zero address. Throws if `_tokenId` is not a valid NFT.
    ///  When transfer is complete, this function checks if `_to` is a smart
    ///  contract (code size > 0). If so, it calls `onERC2665Received` on `_to`
    ///  and throws if the return value is not
    ///  `bytes4(keccak256("onERC2665Received(address,address,uint256,bytes)"))`.
    /// @param _from The current owner of the NFT
    /// @param _to The new owner
    /// @param _tokenId The NFT to transfer
    /// @param data Additional data with no specified format, sent in call to `_to`
    function safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes calldata data) external payable;

    /// @notice Transfers the ownership of an NFT from one address to another address
    /// @dev This works identically to the other function with an extra data parameter,
    ///  except this function just sets data to "".
    /// @param _from The current owner of the NFT
    /// @param _to The new owner
    /// @param _tokenId The NFT to transfer
    function safeTransferFrom(address _from, address _to, uint256 _tokenId) external payable;

    /// @notice Transfer ownership of an NFT -- THE CALLER IS RESPONSIBLE
    ///  TO CONFIRM THAT `_to` IS CAPABLE OF RECEIVING NFTS OR ELSE
    ///  THEY MAY BE PERMANENTLY LOST
    /// @dev Throws unless `msg.sender` is the current owner, an authorized
    ///  operator, or the approved address for this NFT. Throws if `_from` is
    ///  not the current owner. Throws if `_to` is the zero address. Throws if
    ///  `_tokenId` is not a valid NFT. Throws if `msg.value` < `getTransferFee(_tokenId)`.
    ///  If the fee is not to be paid in ETH, then token publishers SHOULD provide a way to pay the
    ///  fee when calling this function and throw if said fee is not paid.
    ///  Throws if `_to` is the zero address. Throws if `_tokenId` is not a valid NFT.
    /// @param _from The current owner of the NFT
    /// @param _to The new owner
    /// @param _tokenId The NFT to transfer
    function transferFrom(address _from, address _to, uint256 _tokenId) external payable;

    /// @notice Change or reaffirm the approved address for an NFT
    /// @dev The zero address indicates there is no approved address.
    ///  Throws unless `msg.sender` is the current NFT owner, or an authorized
    ///  operator of the current owner. After a successful call and if
    ///  `msg.value == getTransferFee(_tokenId)`, then a subsequent atomic call to
    ///  `getTransferFee(_tokenId)` would eval to 0. If the fee is not to be paid in ETH,
    ///  then token publishers MUST provide a way to pay the fee when calling this function,
    ///  and throw if the fee is not paid.
    /// @param _approved The new approved NFT controller
    /// @param _tokenId The NFT to approve
    function approve(address _approved, uint256 _tokenId) external payable;

    /// @notice Enable or disable approval for a third party ("operator") to manage
    ///  all of `msg.sender`'s assets
    /// @dev Emits the ApprovalForAll event. The contract MUST allow
    ///  multiple operators per owner.
    /// @param _operator Address to add to the set of authorized operators
    /// @param _approved True if the operator is approved, false to revoke approval
    function setApprovalForAll(address _operator, bool _approved) external;

    /// @notice Get the approved address for a single NFT
    /// @dev Throws if `_tokenId` is not a valid NFT.
    /// @param _tokenId The NFT to find the approved address for
    /// @return The approved address for this NFT, or the zero address if there is none
    function getApproved(uint256 _tokenId) external view returns (address);

    /// @notice Query if an address is an authorized operator for another address
    /// @param _owner The address that owns the NFTs
    /// @param _operator The address that acts on behalf of the owner
    /// @return True if `_operator` is an approved operator for `_owner`, false otherwise
    function isApprovedForAll(address _owner, address _operator) external view returns (bool);

    /// @notice Query what is the transfer fee for a specific token
    /// @dev If a call would returns 0, then any subsequent calls witht the same argument
    /// must also return 0 until the Transfer event has been emitted.
    /// @param _tokenId The NFT to find the Transfer Fee amount for
    /// @return The amount of Wei that need to be sent along a call to a transfer function
    function getTransferFee(uint256 _tokenId) external view returns (uint256);

    /// @notice Query what is the transfer fee for a specific token if the fee is to be paid
    /// @dev If a call would returns 0, then any subsequent calls with the same arguments
    /// must also return 0 until the Transfer event has been emitted. If _currencySymbol == 'ETH',
    /// then this function must return the same result as if `getTransferFee(uint256 _tokenId)` was called.
    /// @param _tokenId The NFT to find the Transfer Fee amount for
    /// @param _currencySymbol The currency in which the fee is to be paid
    /// @return The amount of Currency that need to be sent along a call to a transfer function
    function getTransferFee(uint256 _tokenId, string calldata _currencySymbol) external view returns (uint256);

}

interface ERC165 {
    /// @notice Query if a contract implements an interface
    /// @param interfaceID The interface identifier, as specified in ERC-165
    /// @dev Interface identification is specified in ERC-165. This function
    ///  uses less than 30,000 gas.
    /// @return `true` if the contract implements `interfaceID` and
    ///  `interfaceID` is not 0xffffffff, `false` otherwise
    function supportsInterface(bytes4 interfaceID) external view returns (bool);
}
```

**Every ERC-2665 compliant contract SHOULD implement the following interface if they wants to provide a standardized way for marketplaces to provide a royalty fee as a percentage of a sale** :

```solidity
pragma solidity ^0.6.6;

/// @title ERC-2665 NFT Transfer Fee as percent of sale Extension
/// @dev See https://github.com/ethereum/EIPs/issues/2665
///  Note: the ERC-165 identifier for this interface is 0xf4bcaa86.
interface ERC2665PercentOfSale /* is ERC2665 */ {

    /// @dev This emits when ownership of any NFT changes when following a sale on a trusted marketplace.
    event Sale(uint256 indexed _tokenId, uint256 _price);

    /// @notice Query if an address is an trusted marketplace for NFT sales
    /// @param _marketplace The address that is trusted to report an NFT sale truthfully
    /// @param _tokenId The token ID the marketplace is queried of.
    /// @return True if `_marketplace` is an approved marketplace for the NFT, false otherwise
    function isTrustedMarketplace(address _marketplace, uint256 _tokenId) external view returns (bool);

    /// @notice Query the numerator of sale fee that is a percentage of the sale price for a given token
    /// @param _tokenId The token ID the fee is queried of.
    /// @dev Throws if `_tokenId` is not a valid NFT.
    /// @return 0 if no percent fee are defined, the saleFeeNumerator of the fee such as
    /// salePrice * saleFeeNumerator/saleFeeDenominator = TransferFee otherwise.
    function saleFeeNumerator(uint256 _tokenId) external view returns (uint256);

    /// @notice Query the denominator of sale fee that is a percentage of the sale price for a given token
    /// @param _tokenId The token ID the fee is queried of.
    /// @dev Throws if `_tokenId` is not a valid NFT.
    /// @return 0 if no percent fee are defined, the saleFeeDenominator of the fee such as
    /// salePrice * saleFeeNumerator/saleFeeDenominator = TransferFee otherwise.
    function saleFeeDenominator(uint256 _tokenId) external view returns (uint256);

    /// @notice callable by a marketPlace once a sale have been agreed but before the NFT transfer.
    /// @dev Throws if `_tokenId` is not a valid NFT.
    /// Throws if isTrustedMarketplace(msg.sender, _tokenId) == false.
    /// Throws if msg.value != _price * saleFeeNumerator / saleFeeDenominator.
    /// May throws if msg.value < getTransferFee(_tokenId) -up to your implementation-
    /// Emit the Sale event.
    /// Once called succesfully, set getTransferFee(uint256 _tokenId) to 0.
    function settleSale(uint256 _tokenId, uint256 _price) external payable;

}

```

A wallet/broker/auction application MUST implement the wallet interface if it will accept safe transfers.

```solidity
/// @dev Note: the ERC-165 identifier for this interface is 0xac3cf292.
interface ERC2665TokenReceiver {
    /// @notice Handle the receipt of an NFT
    /// @dev The ERC2665 smart contract calls this function on the recipient
    ///  after a `transfer`. This function MAY throw to revert and reject the
    ///  transfer. Return of other than the magic value MUST result in the
    ///  transaction being reverted.
    ///  Note: the contract address is always the message sender.
    /// @param _operator The address which called `safeTransferFrom` function
    /// @param _from The address which previously owned the token
    /// @param _tokenId The NFT identifier which is being transferred
    /// @param _data Additional data with no specified format
    /// @return `bytes4(keccak256("onERC2665Received(address,address,uint256,bytes)"))`
    ///  unless throwing
    function onERC2665Received(address _operator, address _from, uint256 _tokenId, bytes calldata _data) external returns(bytes4);
}
```

The following "ERC2665 Metadata JSON Schema" is proposed as an extension to the "ERC721 Metadata JSON Schema". ERC-2665 compliant tokens implementing the ERC-721 Metadata extension MUST return this schema instead of the one described in "ERC721 Metadata JSON Schema".

```json
{
    "title": "Asset Metadata",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Identifies the asset to which this NFT represents"
        },
        "description": {
            "type": "string",
            "description": "Describes the asset to which this NFT represents"
        },
        "image": {
            "type": "string",
            "description": "A URI pointing to a resource with mime type image/* representing the asset to which this NFT represents. Consider making any images at a width between 320 and 1080 pixels and aspect ratio between 1.91:1 and 4:5 inclusive."
        },
	"feeCurrency": {
            "type": "string",
            "description": "A comma separated list of the symbol of the currencies accepted as payment of the Transfer Fee"
        },
	"feeDescription": {
            "type": "string",
            "description": "Information on the Transfer Fee to be displayed to potential owners of the NFT"
        }
    }
}
```

Please refer to EIP-721 for the **metadata extension** and **enumeration extension**.

https://github.com/ethereum/EIPs/blob/master/EIPS/eip-721.md

Due to the nature of payable fees, the **metadata extension** SHOULD be implemented in order to inform users about the nature and amount of the fees.

## Caveats

The 0.6.6 Solidity interface grammar is not expressive enough to document the ERC-2665 standard. A contract which complies with ERC-2665 MUST also abide by the following:

- A contract that implements ERC-2665 MUST also abide by the ERC-721 standard. Functions defined in `interface ERC721` are all overridden by the function and specifications defined in `interface ERC2665` above.

- If `getTransferFee(uint256)` is implemented as something else than a `pure` function always returning `0`, then `safeTransferFrom` (both versions), `transferFrom` and `approve` MUST be implemented as `payable`. This takes precedence over the mutability guarantees of ERC-721.

- Any function call MUST throw if the conditions described in their interface are met. They MAY throw in other, additional conditions too.

## Non specified functions in the standard that contracts should implement for full functionality.

The interface defined above exist for inter-operability purposes. However, smart contract publishers are reminded to implement the following features in their contracts :

- Standard ERC-721 features, such as minting, and desirable genric smart contract features, such as an "owner" property.

- A way to set up and modify fixed and percent based trading fee for their tokens. eg : `setPercentSaleFees(uint256 _tokenId, uint256 _saleFeeNumerator,  uint256 _saleFeeDenominator) external`

- A way to nominate and edit marketplaces trusted to handle royalties are percent of sales. eg :  `function setTrustedMarketplace(address _marketplace) external`

Rationale
===============

This EIP is a first draft on how to give publishers more options on what kind of NFTs can be created and the fees that can be collected whilst still maintaining the same flow of trade for users, platforms and wallet providers. Only minimal changes to existing code would be necessary to implement this EIP to previous ERC-721 compatible software solutions.

### Summarized additions compared to the ERC-721 Specification

1.  A new function : `getTransferFee(uint256 _tokenId) external view returns (uint256)`. It is overloaded with `getTransferFee(uint256 _tokenId, string _currencySymbol) external view returns (uint256)` if the fee need to be paid with a different currency than ETH.

2.  If a call to `getTransferFee(_tokenId, _currencySymbol)`  would have returned `0` at any point, then any posterior call with the same arguments MUST return `0` until a `Transfer` event has been emitted for `_tokenId`. This is called in the rest of this EIP the *eval to 0 remanence guarantee*.

3.  Successfully calling `approve{value : getTransferFee(_tokenId)}(address _approved, uint256 _tokenId)` will atomatically make `getTransferFee(_tokenId)` eval to `0`.

4.  All `safeTransferFrom` variants now call `onERC2665Received` instead of  the ERC-721 specific function. `ERC2665TokenReceiver` is derived from `ERC721TokenReceiver` accordingly.

5.  Changing the mutability of `safeTransferFrom` & overloads, `transferFrom` and`approve` to always be *payable* if `getTransferFee` can return non-zero values.

6.  Changing the sufficient throw conditions of the `transferFrom` functions. More specifically adding: `Throws if msg.value < getTransferFee(_tokenId)`.

7.  "ERC2665 Metadata JSON Schema" extended from the "ERC721 Metadata JSON Schema" to provide fee information without polluting the description of an NFT.

8.  Extension compatibility preserved. If something extends ERC-721, it can extend ERC-2665.

### Discussion

- Whether ERC-2665 follows ERC-721 could be debated because of change #4. This change is important, as some smart contracts designed to only handle free `Transfer` ERC-721 tokens could get an ERC-2665 stuck. The actual consequence of the spec extension is that the `safeTransferFrom` functions will throw more than the minimum required by ERC-721, which is already covered in the ERC-721 spec itself. Therefore, ERC-2665 follows ERC-721 and is simply an extension of it.

    >From ERC-721 Specifications:
    >
    >The transfer and accept functions’ documentation only specify conditions when the transaction MUST throw. Your implementation MAY also throw in other situations.



- The `getTransferFee` function is where most of the engineering work for publishers lies. The function is `view`, meaning no state changes can happen when it's being called. Moreover, the *eval to 0 remanence guarantee* is extremely important in order for an ecosystem to be built around this standard, as it guarantees that the next Transfer can follow feeless ERC-721 behavior and that a Transfer Fee can be paid in advance.

- A more subtle consequence of `getTransferFee` being `view` is that it shall not depend on `msg.sender`, but rather only of non-manipulable parameters such as the current owner and operators of the token.

- The *eval to 0 remanence guarantee* is specifically worded so that the change of ownership could be done through a mechanism that is not related to ERC-2665 (e.g. the publisher’s own trading system). However, the specifications of `Transfer` must still be respected even if the change of ownership is not done through a call to an ERC-2665 related function. ERC-2665 does not specify any Transfer Fee refund mechanism should the token change owner through a mechanism other than ERC-2665.

- `getTransferFee` can be restricted to pure (e.g : if the fee is static like always 0 wei, aka typical ERC-721 tokens).

- While publishers are free to implement whatever behavior they want behind the `getTransferFee` function, it is impossible to guarantee a fee calculated as a direct percentage of an actual sale price. The money exchange for that transfer, if any, could simply be happening off-chain. Therefore, rather than implementing a complex "fee calculation and distribution" protocol, ERC-2665 is generic enough to be easily interactable by third parties. This gives publishers the freedom to specify the fee, which can be complex, variable and potentially oraclized (e.g. the fee is always 10 USD), and standardized entry-points for the fee to be paid and distributed.

- `getTransferFee` can be implemented to return 0 if the token is owned/operated by an address owned by a partner of the publisher. This incentivizes publishers and marketplaces to partner-up : The publisher gets more exposure and an UX tailored to its product, and the marketplace becomes cheaper than its competitors for these tokens. **The Transfer Fee could then be supplanted by a real-world commercial contract, or something in chain, like for example, *a direct percentage of the sales proceeds*. This allow token publishers to guarantee a fee in trustless environments while pushing trades to happens on marketplace that is gonna remunerate them fairly.**

- As long as an ERC-2665 smart contract is accessed in a read-only fashion or that the `safeTransfer` functions are not used, any software designed to interact with feeless ERC-721 can interact with ERC-2665 without any update necessary. However, if the `Transfer` functions were assumed to always be free/non-payable (i.e. if the software implementation was only compatible with a subset of ERC-721), then problems might arise. A few ways to mitigate such issues are suggested in the Backwards Compatibility section below.

- Due to the addition of `getTransferFee`, the ERC-165 signature of the `ERC2665` interface is different from the one of the `ERC721` interface. However, all of the ERC-721 function signatures are implemented unchanged. Should an ERC-2665 smart contract be declared as implementing `ERC721` when being asked about it through ERC-165 `supportsInterface` ? The answer is yes, as ERC-2665 is fully ERC-721 compliant, and only limitations in the Solidity language *(Namely lack of Interface inheritance and design-by-contract programming abilities)* or the chosen method of computing ERC-165 identifiers could suggest a different answer that ultimately do not have a use case.

- What should be the gas limit of `getTransferFee`, if any ? Its behaviour needs to be implementable as more complex than an ERC-165 check, but nonetheless gas spending should be kept low to prevent accidental locking in a custodian wallet.

- Regarding non-ETH currency fees, the Standard is on purpose extremely generic, as there is no limit on what these currencies could be, nor would they need to be in-chain currencies.

- If the fee is not in ETH, token publishers SHOULD implement the *ERC-721 metadata* extension with the *ERC2665 Metadata Json Schema* and provide informations on how to pay the fee there.

- Suggested flow for ERC-20 fees is that the fee payer gives an `allowance` of the currency to the ERC-2665 contract, then a subsequent call to `transferFrom` or `approve` will make the ERC-2665 collect the fee from `msg.sender`. An implementation example of a contract requiring such a fee will be provided.

Backwards Compatibility
===============

Every ERC-2665 contract is fully compliant with the ERC-721 standard, meaning backwards compatibility issues can only arise if the software interacting with an ERC-2665 contract was in fact not ERC-721 compliant in the first place.

## Upgrading from ERC-721 to ERC-2665

### Token publisher

- ERC-2665 is an extension of ERC-721, meaning that any ERC-721 contract can be extended to be also ERC-2665. The minimal work necessary is to implement `getTransferFee()`, the relevant ERC-165 codes and the proper handling of the fee in the approval/transfer functions, as well as changing any `onERC721Received` call to `onERC2665Received`.

- `getTransferFee` could be reading a price oracle smart contract averaging the last transactions on a marketplace, relying on an original price discovery mechanism, be it a fixed wei amount, or be it obtained by calling a smart contract specified by the token creator, depends on a complex interaction with another marketplace, simply set to 0, etc...

- The fee MUST be able to be paid either using `approve()` or `transferFrom()` if the fee is in ETH, but apart from this you MAY implement any extra fee collection and distribution mechanism you want. e.g : give the ability for a marketplace you trust is gonna give you 10% of the sale the ability to pay 0 wei as an actual transfer fee.

- No particular behavior for overpaying/refunding a fee is specified in ERC-2665. The only real constraint is the *eval to 0 remanence guarantee*  of `getTransferFee`.

- ERC-2665 token publishers SHOULD make it so that sending more than the `TransferFee` when transferring a token makes it so that the next TransferFee can be waived. The exact behavior is left to the creativity of the publisher, but atomicity of the `Transfer{value}() => getTransferFee() == 0` sequence is sought after for an ERC-2665 token to be easily traded at custodial third party marketplaces.

- Similarly, ERC-2665 token publishers SHOULD also make it possible for `Approve()` to pay the subsequent Transfer Fee, so that `Approve{value}() => Transfer(){0} => getTransferFee() == 0` can also be an atomic sequence.

### Frontend, UX, and other off-chain interactions.

##### Minimal implementation

Make users send a `value` of `getTransferFee(_tokenId)` Wei when calling `Transfer` or `Approve` functions if the token is ERC-2665.

##### Suggested implementation for Wallet/Broker/Auction applications

Due to the very nature of a transfer fee, gasless listings would place the burden of paying the transfer fee on the buyer. Informations on the amount and nature of this fee SHOULD be clearly communicated to any potential sellers and buyers. There is no guarantee in the ERC-2665 standard that any two subsequent, non atomic `getTransferFee()` calls will return the same value, except if this value is `0` due to the *eval to 0 remanence guarantee* .

If you want for a seller to pay the transfer fee in advance, you might have to simulate a post-transactions state so that a potential future recipient of the token can receive it without having to pay the transfer fee. This is of course non-trivial and varying with ERC-2665 implementations, but some paths are explored below.

### Wallet/Broker/Auction Smart Contracts

##### Subsequent Transfer Fee paid by the seller (if any)

The simplest way to make your (awesome) decentralized auctioning smart contract that was working just fine with feeless ERC-721 compatible with ERC-2665 is to add an implementation of `onERC2665Received` just like this :

```solidity
function onERC2665Received(address _operator, address _from, uint256 _tokenId, bytes _data) external returns(bytes4){

    // Require the transfer fee to have already been prepaid. Throw if it is not the case.
    require(ERC2665(msg.sender).getTransferFee() == 0);

    // Here do whatever you already do for feeless ERC721

    returns(bytes4(keccak256("onERC2665Received(address,address,uint256,bytes)")));

}
```

Keep in mind though that the safeTransferFunction is now calling `onERC2665Received` on any potential new owners, which might require a few more changes in your code. Do not forget about updating your ERC-165 code either.

##### Transfer Fee paid by the buyer (if any)

Assuming you have some `win(uint256 _tokenId, address _tokenContract, address _from, address _to, uint _fee, bytes _data)` function that is used by the buyer to get the token. (Unoptimized code and separated cases for clarity).
This function signature is just given as an example, and it's parameters could come from other sources such as internal variables/function calls/msg.sender/etc...

```solidity
function win(uint256 _tokenId, address _tokenContract, address _from, address _to, uint _fee) external{

    // Do a preliminary check on the recipient being able to properly handle an ERC-721 token
    // 0x150b7a02 is the ERC-165 identifier for the ERC721TokenReceiver interface
    require(!isContract(_to) || ERC165(_to).supportsInterface(0x150b7a02), "The recipient is not able to handle ERC721 tokens");


    //Do your normal winning/paying logic here


    //Time to transfer

    // Case where your recipient is a smart contract that does not handle the EIP-2665 extension but implements
    // a feeless ERC-721 just fine
    // 0xac3cf292 is the ERC-165 identifier for the ERC2665TokenReceiver interface
    if(isContract(_to) && !ERC165(_to).supportsInterface(0xac3cf292)){

        // Unsafe transfer to prevent throwing
        ERC2665(_tokenContract).transferFrom{
                value: _fee //Pay the fee
            }(
                _from,
                _to,
                _tokenId
            );

        // Call onERC721Received just like a feeless safeTransfer from an ERC-721 would
        assert(ERC721TokenReceiver(_to).onERC721Received(address(this), _from, _tokenId, _data) ==
            bytes4(keccak256("onERC721Received(address,address,uint256,bytes)")));

        // Verify that the next transfer is feeless as to not hinder the next Transfer
        assert(ERC2665(_tokenContract).getTransferFee(_tokenId) == 0);

        // Please note that the ERC2665 token will not get stuck if the _to contract does not lie about
        // properly implementing the ERC721 standard, as a call to safeTransferFrom() on a non ERC-2665
        // compatible _to will throw

    } else{
        // ERC-2665 is properly implemented in this case :
        // _to is either an ERC2665TokenReceiver smart contract or a human
        ERC2665(_tokenContract).safeTransferFrom{
                value: _fee //Pay the fee
            }(
                _from,
                _to,
                _tokenId
        );
    }

    // Do more stuff post transfer if you need to

}
```

Test Cases
===============

To be provided once sufficient discussion happened

Implementations
===============

-    Cryptograph. A soon to be launched publishing and trading platform of NFTs created by famous individuals and artists called Cryptographs. The platform is centered around the concept that each token generates revenue for its creator and for a charitable cause of the creator’s choice in perpetuity by always collecting fees on transactions and transfers. Cryptograph implements ERC-2665, which was designed specifically to follow the ERC-721 standard whilst enforcing payable transfer fees.

References
===============

1.	The ERC-721 Standard https://github.com/ethereum/EIPs/blob/master/EIPS/eip-721.md
2.	The ERC-165 Standard https://github.com/ethereum/EIPs/blob/master/EIPS/eip-165.md

Copyright
===============

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
