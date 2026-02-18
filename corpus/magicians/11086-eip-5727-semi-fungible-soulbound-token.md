---
source: magicians
topic_id: 11086
title: "EIP-5727: Semi-Fungible Soulbound Token"
author: AustinZhu
date: "2022-09-28"
category: EIPs
tags: [token, soul-bound, erc-3525]
url: https://ethereum-magicians.org/t/eip-5727-semi-fungible-soulbound-token/11086
views: 3908
likes: 6
posts_count: 10
---

# EIP-5727: Semi-Fungible Soulbound Token

## Abstract

An interface for soulbound tokens (SBT), which are non-transferable tokens representing a person’s identity, credentials, affiliations, and reputation.

Our interface can handle a combination of fungible and non-fungible tokens in an organized way. It provides a set of core methods that can be used to manage the lifecycle of soulbound tokens, as well as a rich set of extensions that enables DAO governance, privacy protection, token expiration, and account recovery.

This interface aims to provide a flexible and extensible framework for the development of soulbound token systems.

## Motivation

The Web3 ecosystem nowadays is largely dominated by highly-financialized tokens, which are designed to be freely transferable and interchangeable. However, there are many use cases in our society that require non-transferablity. For example, a membership card guarantees one’s proprietary rights in a community, and such rights should not be transferable to others.

We have already seen many attempts to create such non-transferable tokens in the Ethereum community. However, they lack the flexibility to support both fungible and non-fungible tokens and do not provide extensible features for critical use cases.

Our interface can be used to represent non-transferable ownerships, and provides features for common use cases including but not limited to:

- granular lifecycle management of SBTs (e.g. minting, revocation, expiration)
- management of SBTs via community voting and delegation (e.g. DAO governance, operators)
- recovery of SBTs (e.g. switching to a new wallet)
- fungible and non-fungible SBTs (e.g. membership card and loyalty points)
- the grouping of SBTs using slots (e.g. complex reward schemes with a combination of vouchers, points, and badges)

A common interface for soulbound tokens will not only help enrich the Web3 ecosystem but also facilitates the growth of a decentralized society.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

A token is identified by its `tokenId`, which is a 256-bit unsigned integer. A token can also have a value denoting its denomination.

A slot is identified by its `slotId`, which is a 256-bit unsigned integer. Slots are used to group fungible and non-fungible tokens together, thus make tokens semi-fungible. A token can only belong to one slot at a time.

### Core

The core methods are used to manage the lifecycle of SBTs. They MUST be supported by all semi-fungible SBT implementations.

```solidity
/**
 * @title ERC5727 Soulbound Token Interface
 * @dev The core interface of the ERC5727 standard.
 */
interface IERC5727 is IERC3525, IERC5192, IERC5484, IERC4906 {
    /**
     * @dev MUST emit when a token is revoked.
     * @param from The address of the owner
     * @param tokenId The token id
     */
    event Revoked(address indexed from, uint256 indexed tokenId);

    /**
     * @dev MUST emit when a token is verified.
     * @param by The address that initiated the verification
     * @param tokenId The token id
     * @param result The result of the verification
     */
    event Verified(address indexed by, uint256 indexed tokenId, bool result);

    /**
     * @notice Get the verifier of a token.
     * @dev MUST revert if the `tokenId` does not exist
     * @param tokenId the token for which to query the verifier
     * @return The address of the verifier of `tokenId`
     */
    function verifierOf(uint256 tokenId) external view returns (address);

    /**
     * @notice Get the issuer of a token.
     * @dev MUST revert if the `tokenId` does not exist
     * @param tokenId the token for which to query the issuer
     * @return The address of the issuer of `tokenId`
     */
    function issuerOf(uint256 tokenId) external view returns (address);

    /**
     * @notice Issue a token in a specified slot to an address.
     * @dev MUST revert if the `to` address is the zero address.
     *      MUST revert if the `verifier` address is the zero address.
     * @param to The address to issue the token to
     * @param tokenId The token id
     * @param slot The slot to issue the token in
     * @param burnAuth The burn authorization of the token
     * @param verifier The address of the verifier
     * @param data Additional data used to issue the token
     */
    function issue(
        address to,
        uint256 tokenId,
        uint256 slot,
        BurnAuth burnAuth,
        address verifier,
        bytes calldata data
    ) external payable;

    /**
     * @notice Issue credit to a token.
     * @dev MUST revert if the `tokenId` does not exist.
     * @param tokenId The token id
     * @param amount The amount of the credit
     * @param data The additional data used to issue the credit
     */
    function issue(
        uint256 tokenId,
        uint256 amount,
        bytes calldata data
    ) external payable;

    /**
     * @notice Revoke a token from an address.
     * @dev MUST revert if the `tokenId` does not exist.
     * @param tokenId The token id
     * @param data The additional data used to revoke the token
     */
    function revoke(uint256 tokenId, bytes calldata data) external payable;

    /**
     * @notice Revoke credit from a token.
     * @dev MUST revert if the `tokenId` does not exist.
     * @param tokenId The token id
     * @param amount The amount of the credit
     * @param data The additional data used to revoke the credit
     */
    function revoke(
        uint256 tokenId,
        uint256 amount,
        bytes calldata data
    ) external payable;

    /**
     * @notice Verify if a token is valid.
     * @dev MUST revert if the `tokenId` does not exist.
     * @param tokenId The token id
     * @param data The additional data used to verify the token
     * @return A boolean indicating whether the token is successfully verified
     */
    function verify(
        uint256 tokenId,
        bytes calldata data
    ) external returns (bool);
}
```

### Extensions

All extensions below are OPTIONAL for ERC-5727 implementations. An implementation MAY choose to implement some, none, or all of them.

#### Enumerable

This extension provides methods to enumerate the tokens of a owner. It is recommended to be implemented together with the core interface.

```solidity
/**
 * @title ERC5727 Soulbound Token Enumerable Interface
 * @dev This extension allows querying the tokens of a owner.
 */
interface IERC5727Enumerable is IERC3525SlotEnumerable, IERC5727 {
    /**
     * @notice Get the number of slots of a owner.
     * @param owner The owner whose number of slots is queried for
     * @return The number of slots of the `owner`
     */
    function slotCountOfOwner(address owner) external view returns (uint256);

    /**
     * @notice Get the slot with `index` of the `owner`.
     * @dev MUST revert if the `index` exceed the number of slots of the `owner`.
     * @param owner The owner whose slot is queried for.
     * @param index The index of the slot queried for
     * @return The slot is queried for
     */
    function slotOfOwnerByIndex(
        address owner,
        uint256 index
    ) external view returns (uint256);

    /**
     * @notice Get the balance of a owner in a slot.
     * @dev MUST revert if the slot does not exist.
     * @param owner The owner whose balance is queried for
     * @param slot The slot whose balance is queried for
     * @return The balance of the `owner` in the `slot`
     */
    function ownerBalanceInSlot(
        address owner,
        uint256 slot
    ) external view returns (uint256);
}
```

#### Metadata

This extension provides methods to fetch the metadata of a token, a slot and the contract itself. It is recommended to be implemented if you need to specify the appearance and properties of tokens, slots and the contract (i.e. the SBT collection).

```solidity
/**
 * @title ERC5727 Soulbound Token Metadata Interface
 * @dev This extension allows querying the metadata of soulbound tokens.
 */
interface IERC5727Metadata is IERC3525Metadata, IERC5727 {

}
```

#### Governance

This extension provides methods to manage the mint and revocation permissions through voting. It is useful if you want to rely on a group of voters to decide the issuance a particular SBT.

```solidity
/**
 * @title ERC5727 Soulbound Token Governance Interface
 * @dev This extension allows issuing of tokens by community voting.
 */
interface IERC5727Governance is IERC5727 {
    enum ApprovalStatus {
        Pending,
        Approved,
        Rejected,
        Removed
    }

    /**
     * @notice Emitted when a token issuance approval is changed.
     * @param approvalId The id of the approval
     * @param creator The creator of the approval, zero address if the approval is removed
     * @param status The status of the approval
     */
    event ApprovalUpdate(
        uint256 indexed approvalId,
        address indexed creator,
        ApprovalStatus status
    );

    /**
     * @notice Emitted when a voter approves an approval.
     * @param voter The voter who approves the approval
     * @param approvalId The id of the approval
     */
    event Approve(
        address indexed voter,
        uint256 indexed approvalId,
        bool approve
    );

    /**
     * @notice Create an approval of issuing a token.
     * @dev MUST revert if the caller is not a voter.
     *      MUST revert if the `to` address is the zero address.
     * @param to The owner which the token to mint to
     * @param tokenId The id of the token to mint
     * @param amount The amount of the token to mint
     * @param slot The slot of the token to mint
     * @param burnAuth The burn authorization of the token to mint
     * @param data The additional data used to mint the token
     */
    function requestApproval(
        address to,
        uint256 tokenId,
        uint256 amount,
        uint256 slot,
        BurnAuth burnAuth,
        address verifier,
        bytes calldata data
    ) external;

    /**
     * @notice Remove `approvalId` approval request.
     * @dev MUST revert if the caller is not the creator of the approval request.
     *      MUST revert if the approval request is already approved or rejected or non-existent.
     * @param approvalId The approval to remove
     */
    function removeApprovalRequest(uint256 approvalId) external;

    /**
     * @notice Approve `approvalId` approval request.
     * @dev MUST revert if the caller is not a voter.
     *     MUST revert if the approval request is already approved or rejected or non-existent.
     * @param approvalId The approval to approve
     * @param approve True if the approval is approved, false if the approval is rejected
     * @param data The additional data used to approve the approval (e.g. the signature, voting power)
     */
    function voteApproval(
        uint256 approvalId,
        bool approve,
        bytes calldata data
    ) external;

    /**
     * @notice Get the URI of the approval.
     * @dev MUST revert if the `approvalId` does not exist.
     * @param approvalId The approval whose URI is queried for
     * @return The URI of the approval
     */
    function approvalURI(
        uint256 approvalId
    ) external view returns (string memory);
}
```

#### Delegate

This extension provides methods to delegate (undelegate) mint right in a slot to (from) an operator. It is useful if you want to allow an operator to mint tokens in a specific slot on your behalf.

```solidity
/**
 * @title ERC5727 Soulbound Token Delegate Interface
 * @dev This extension allows delegation of issuing and revocation of tokens to an operator.
 */
interface IERC5727Delegate is IERC5727 {
    /**
     * @notice Emitted when a token issuance is delegated to an operator.
     * @param operator The owner to which the issuing right is delegated
     * @param slot The slot to issue the token in
     */
    event Delegate(address indexed operator, uint256 indexed slot);

    /**
     * @notice Emitted when a token issuance is revoked from an operator.
     * @param operator The owner to which the issuing right is delegated
     * @param slot The slot to issue the token in
     */
    event UnDelegate(address indexed operator, uint256 indexed slot);

    /**
     * @notice Delegate rights to `operator` for a slot.
     * @dev MUST revert if the caller does not have the right to delegate.
     *      MUST revert if the `operator` address is the zero address.
     *      MUST revert if the `slot` is not a valid slot.
     * @param operator The owner to which the issuing right is delegated
     * @param slot The slot to issue the token in
     */
    function delegate(address operator, uint256 slot) external;

    /**
     * @notice Revoke rights from `operator` for a slot.
     * @dev MUST revert if the caller does not have the right to delegate.
     *      MUST revert if the `operator` address is the zero address.
     *      MUST revert if the `slot` is not a valid slot.
     * @param operator The owner to which the issuing right is delegated
     * @param slot The slot to issue the token in
     */

    function undelegate(address operator, uint256 slot) external;

    /**
     * @notice Check if an operator has the permission to issue or revoke tokens in a slot.
     * @param operator The operator to check
     * @param slot The slot to check
     */
    function isOperatorFor(
        address operator,
        uint256 slot
    ) external view returns (bool);
}

```

#### Recovery

This extension provides methods to recover tokens from a stale owner. It is recommended to use this extension so that users are able to retrieve their tokens from a compromised or old wallet in certain situations. The signing scheme SHALL be compatible with EIP-712 for readability and usability.

```solidity
/**
 * @title ERC5727 Soulbound Token Recovery Interface
 * @dev This extension allows recovering soulbound tokens from an address provided its signature.
 */
interface IERC5727Recovery is IERC5727 {
    /**
     * @notice Emitted when the tokens of `owner` are recovered.
     * @param from The owner whose tokens are recovered
     * @param to The new owner of the tokens
     */
    event Recovered(address indexed from, address indexed to);

    /**
     * @notice Recover the tokens of `owner` with `signature`.
     * @dev MUST revert if the signature is invalid.
     * @param owner The owner whose tokens are recovered
     * @param signature The signature signed by the `owner`
     */
    function recover(address owner, bytes memory signature) external;
}
```

#### Expirable

This extension provides methods to manage the expiration of tokens. It is useful if you want to expire/invalidate tokens after a certain period of time.

```solidity
/**
 * @title ERC5727 Soulbound Token Expirable Interface
 * @dev This extension allows soulbound tokens to be expirable and renewable.
 */
interface IERC5727Expirable is IERC5727, IERC5643 {
    /**
     * @notice Set the expiry date of a token.
     * @dev MUST revert if the `tokenId` token does not exist.
     *      MUST revert if the `date` is in the past.
     * @param tokenId The token whose expiry date is set
     * @param expiration The expire date to set
     * @param isRenewable Whether the token is renewable
     */
    function setExpiration(
        uint256 tokenId,
        uint64 expiration,
        bool isRenewable
    ) external;
}
```

## Rationale

### Token storage model

We adopt semi-fungible token storage models designed to support both fungible and non-fungible tokens, inspired by the semi-fungible token standard. We found that such a model is better suited to the representation of SBT than the model used in EIP-1155.

Firstly, each slot can be used to represent different categories of SBTs. For instance, a DAO can have membership SBTs, role badges, scores, etc. in one SBT collection.

Secondly, unlike EIP-1155, in which each unit of fungible tokens is exactly the same, our interface can help differentiate between similar tokens. This is justified by that credential scores obtained from different entities differ not only in value but also in their effects, validity periods, origins, etc. However, they still share the same slot as they all contribute to a person’s credibility, membership, etc.

### Recovery mechanism

To prevent the loss of SBTs, we propose a recovery mechanism that allows users to recover their tokens by providing a signature signed by their owner address. This mechanism is inspired by EIP-1271.

Since SBTs are bound to an address and are meant to represent the identity of the address, which cannot be split into fractions. Therefore, each recovery should be considered as a transfer of all the tokens of the owner. This is why we use the `recover` function instead of `transferFrom` or `safeTransferFrom`.

## Backwards Compatibility

This EIP proposes a new token interface which is compatible with [ERC-721](https://eips.ethereum.org/EIPS/eip-721), [ERC-3525](https://eips.ethereum.org/EIPS/eip-3525), [ERC-4906](https://eips.ethereum.org/EIPS/eip-4906), [ERC-5192](https://eips.ethereum.org/EIPS/eip-5192), [ERC-5484](https://eips.ethereum.org/EIPS/eip-5484).

This EIP is also compatible with ERC-165.

## Test Cases

Our sample implementation includes test cases written using Hardhat.

## Reference Implementation

You can find our sample implementation [here](https://github.com/soularis-protocol/EIPs/blob/master/assets/eip-5727/contracts/ERC5727Example.sol).

## Security Considerations

This EIP does not involve the general transfer of tokens, and thus there will be no security issues related to token transfer generally.

However, users should be aware of the security risks of using the recovery mechanism. If a user loses his/her private key, all his/her soulbound tokens will be exposed to potential theft. The attacker can create a signature and restore all SBTs of the victim. Therefore, users should always keep their private keys safe. We recommend developers implement a recovery mechanism that requires multiple signatures to restore SBTs.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**lanlan3322** (2022-10-04):

Nice, this is what we are looking for to build next-generation NFT! Do you have a demo product implementation?

---

**AustinZhu** (2022-10-13):

Yes, we are working on a project featuring DAO governance tools, event badges and on-chain identity.

---

**SamWilsn** (2022-12-14):

We’re trying a new process where we get a volunteer peer reviewer to read through your proposal and post any feedback here. Your peer reviewer is [@ThunderDeliverer](/u/thunderdeliverer)!

If any of this EIP’s authors would like to participate in the volunteer peer review process, [shoot me a message](https://ethereum-magicians.org/new-message?username=SamWilsn&title=Peer+Review+Volunteer)!

---

[@ThunderDeliverer](/u/thunderdeliverer) please take a look through [EIP-5727](https://eips.ethereum.org/EIPS/eip-5727) and comment here with any feedback or questions. Thanks!

---

**AustinZhu** (2022-12-14):

Nice, thank you [@SamWilsn](/u/samwilsn) !

Hello [@ThunderDeliverer](/u/thunderdeliverer) ! Nice to have you here.

---

**ThunderDeliverer** (2022-12-17):

Thank you [@SamWilsn](/u/samwilsn) for making the introduction!

Nice to meet you [@AustinZhu](/u/austinzhu)! I’m looking forward to reviewing your proposal in the coming week! ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

---

**ThunderDeliverer** (2022-12-28):

Sorry that it took longer than expected, but I needed to finish another proposal before the year’s end.

I’ll try to be as nitpicky as possible, so that I am as helpful as I can be. ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)

1. I think that private assets could be ommited as an example of possible SBT use cases: They are the only example that usually gets inherited when a person dies.
2. Just a minor linguistic comment for the first paragraph of Motivation: requires → require.
3. I get that calling the SBT’s owner soul is in line with the title of the proposal, but still feel this would be easier using owner as this is the term we are used to in other finalized proposals.
4. Would it make sense to enforce that oldSlot equals 0 if it doesn’t exist when emitting SlotChanged event?
5. I’m not sure what isValid  method is supposed to do. I think it could use another @dev tag, to explain it better.
6. Could you explain emittedCount method of the enumerable extension? How and why is a token emitted?
7. What is the benefit of tokenByIndex how would that differ from the token ID?
8. In the Governance extension, would it make sense to return approvalRequestId when using createApprovalRequest?
9. Would it make sense to omit the non-batch methods from Governance extension? When building complex smart contract systems, we often face issues with file size. Having them seems a bit redundant, as you can always use a batch with a size of 1.
10. Same consideration goes for setting expiry dates in Expirable extension.

I’ll take a look at the example implementation in the following days and I will follow up on that as well, but I think this is a good starting point ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

---

**AustinZhu** (2022-12-29):

Thank you for the comments!

1. Agree
2. Oops, will fix that
3. Initially I used owner but later decided to change to soul. I agree that owner is the more widely used term for that purpose, and people are more comfortable with that.
4. Of course. In the actual implementation, when a new slot is created, oldSlot in the SlotChanged event is 0. I’ll document this behavior in the proposal.
5. The isValid method tells whether a SBT is revoked (or expired, or one might have custom logic).
6. emittedCount refers to the current total supply of SBTs. A token can be emitted by minting, which is not standardized in the proposal but in actual implementation one will have a mint method. (Just as how you mint NFTs)
7. It helps to get the token ID of a token as token IDs could be discontinuous. For example, if we want to list all tokens, we can use the method with index in range [0,…,emittedCount-1] to get the token IDs.
8. Sure, thank you for pointing out.
9. I agree. But in practice, both are quite useful. Plus, the singular one costs less gas than using batch method with a size of 1
10. Same as above.

Thank you for reviewing! I will improve the proposal accordingly.

---

**0xTimepunk** (2023-01-06):

I feel this standard is exactly what I need for my game soul bound tokens. Is there a reference implementation available? Where it says ‘here’ is not clickable.

Thanks!

---

**LI-YONG-QI** (2023-04-26):

Hi! the implementation page is not found, what happended?

