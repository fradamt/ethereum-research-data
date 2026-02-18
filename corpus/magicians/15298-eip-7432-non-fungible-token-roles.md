---
source: magicians
topic_id: 15298
title: "EIP-7432: Non-Fungible Token Roles"
author: ernani.eth
date: "2023-07-31"
category: EIPs
tags: [erc, nft]
url: https://ethereum-magicians.org/t/eip-7432-non-fungible-token-roles/15298
views: 2530
likes: 18
posts_count: 17
---

# EIP-7432: Non-Fungible Token Roles

## Abstract

This standard introduces role management for NFTs. Each role assignment is associated with a single NFT and expires automatically at a given timestamp. Inspired by ERC-5982, roles are defined as `bytes32` and feature a custom `_data` field of arbitrary size to allow customization.

https://github.com/ethereum/EIPs/pull/7432

## Motivation

The NFT Roles interface aims to establish a standard for role management in NFTs. Tracking on-chain roles enables decentralized applications (dApps) to implement access control for privileged actions, e.g., minting tokens with a role (airdrop claim rights).

NFT roles can be deeply integrated with dApps to create a utility-sharing mechanism. A good example is in digital real estate. A user can create a digital property NFT and grant a `keccak256("PROPERTY_MANAGER")` role to another user, allowing them to delegate specific utility without compromising ownership. The same user could also grant multiple `keccak256("PROPERTY_TENANT")` roles, allowing the grantees to access and interact with the digital property.

There are also interesting use cases in decentralized finance (DeFi). Insurance policies could be issued as NFTs, and the beneficiaries, insured, and insurer could all be on-chain roles tracked using this standard.

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

ERC-7432 compliant contracts MUST implement the following interface:

```solidity
/// @title ERC-7432 Non-Fungible Token Roles
/// @dev See https://eips.ethereum.org/EIPS/eip-7432
/// Note: the ERC-165 identifier for this interface is 0x851f3b3f.
interface IERC7432 /* is ERC165 */ {
    /// @notice Emitted when a role is granted.
    /// @param _role The role identifier.
    /// @param _tokenAddress The token address.
    /// @param _tokenId The token identifier.
    /// @param _grantee The user that receives the role assignment.
    /// @param _expirationDate The expiration date of the role assignment.
    /// @param _data Any additional data about the role assignment.
    event RoleGranted(
        bytes32 indexed _role,
        address indexed _tokenAddress,
        uint256 indexed _tokenId,
        address _grantee,
        uint64  _expirationDate,
        bytes _data
    );
    /// @notice Emitted when a role is revoked.
    /// @param _role The role identifier.
    /// @param _tokenAddress The token address.
    /// @param _tokenId The token identifier.
    /// @param _grantee The user that receives the role revocation.
    event RoleRevoked(
        bytes32 indexed _role,
        address indexed _tokenAddress,
        uint256 indexed _tokenId,
        address _grantee
    );
    /// @notice Grants a role to a user.
    /// @param _role The role identifier.
    /// @param _tokenAddress The token address.
    /// @param _tokenId The token identifier.
    /// @param _grantee The user that receives the role assignment.
    /// @param _expirationDate The expiration date of the role assignment.
    /// @param _data Any additional data about the role assignment.
    function grantRole(
        bytes32 _role,
        address _tokenAddress,
        uint256 _tokenId,
        address _grantee,
        uint64 _expirationDate,
        bytes calldata _data
    ) external;
    /// @notice Revokes a role from a user.
    /// @param _role The role identifier.
    /// @param _tokenAddress The token address.
    /// @param _tokenId The token identifier.
    /// @param _grantee The user that receives the role revocation.
    function revokeRole(
        bytes32 _role,
        address _tokenAddress,
        uint256 _tokenId,
        address _grantee
    ) external;
    /// @notice Checks if a user has a role.
    /// @param _role The role identifier.
    /// @param _tokenAddress The token address.
    /// @param _tokenId The token identifier.
    /// @param _grantor The role creator.
    /// @param _grantee The user that receives the role.
    /// @param _supportsMultipleAssignments if false, will return true only if account is the last role grantee.
    function hasRole(
        bytes32 _role,
        address _tokenAddress,
        uint256 _tokenId,
        address _grantor,
        address _grantee,
        bool _supportsMultipleAssignments
    ) external view returns (bool);
    /// @notice Returns the custom data of a role assignment.
    /// @param _role The role identifier.
    /// @param _tokenAddress The token address.
    /// @param _tokenId The token identifier.
    /// @param _grantor The role creator.
    /// @param _grantee The user that receives the role.
    function roleData(
        bytes32 _role,
        address _tokenAddress,
        uint256 _tokenId,
        address _grantor,
        address _grantee
    ) external view returns (bytes memory data_);
    /// @notice Returns the expiration date of a role assignment.
    /// @param _role The role identifier.
    /// @param _tokenAddress The token address.
    /// @param _tokenId The token identifier.
    /// @param _grantor The role creator.
    /// @param _grantee The user that receives the role.
    function roleExpirationDate(
        bytes32 _role,
        address _tokenAddress,
        uint256 _tokenId,
        address _grantor,
        address _grantee
    ) external view returns (uint64 expirationDate_);
}
```

## Caveats

- Compliant contracts MUST implement the IERC7432 interface.
- A role is represented by a bytes32, and it’s RECOMMENDED to use the keccak256 of the role’s name for this purpose: bytes32 role = keccak256("ROLE_NAME").
- grantRole function MUST revert if the _expirationDate is in the past, and MAY be implemented as public or external.
- revokeRole function MAY be implemented as public or external.
- The hasRole function MAY be implemented as pure or view.
- The hasRole function SHOULD return false if _supportsMultipleAssignments is false and last role assignment is not to _grantee (see Unique and Non-Unique Roles for more).
- The roleData function MAY be implemented as pure or view.
- Compliant contracts SHOULD support ERC-165.

## Rationale

ERC-7432 IS NOT an extension of ERC-721 or ERC-1155. The main reason behind this decision is to keep the standard agnostic of any NFT implementation. This approach also enables the standard to be implemented externally or on the same contract as the NFT, and allow dApps to use roles with immutable NFTs.

### Automatic Expiration

Automatic expiration is implemented via the `grantRole` and `hasRole` functions. `grantRole` is responsible for setting the expiration date, and `hasRole` checks if the role is expired by comparing with the current block timestamp (`block.timestamp`). Since `uint256` is not natively supported by most programming languages, dates are represented as `uint64` on this standard. The maximum UNIX timestamp represented by a `uint64` is about the year `584,942,417,355`, which should be enough to be considered “permanent”. For this reason, it’s RECOMMENDED using `type(uint64).max` when calling the `grantRole` function to support use cases that require an assignment never to expire.

### Unique and Non-Unique Roles

The standard supports both unique and non-unique roles. Unique roles are roles that can be assigned to only one account, while non-unique roles can be granted to multiple accounts simultaneously. The parameter `_supportsMultipleAssignments` was included in the `hasRole` function to support both use cases. When `_supportsMultipleAssignments` is `true`, the function checks if the assignment exists and is not expired. However, when `false`, the function also validates that no other role was granted afterward. In other words, for unique roles, each new assignment invalidates the previous one, and only the last one can be valid.

Assuming that the **role was granted and is not expired**, the following table shows the result the `hasRole` function MUST return:

| Role Type | _supportsMultipleAssignments | Is last Role granted? | Result of hasRole |
| --- | --- | --- | --- |
| Non-Unique Role | false | Irrelevant | true |
| Unique Role | true | true | true |
| Unique Role | true | false | false |

In conclusion, the `_supportsMultipleAssignments` argument only affects the result when `true`, and if the queried assignment is not the last one granted.

### Custom Data

DApps can customize roles using the `_data` parameter of the `grantRole` function. `_data`  is implemented using the generic type `bytes` to enable dApps to encode any role-specific information when creating a role assignment. The custom data is retrievable using the `roleData` function and is emitted with the `RoleGranted` event. With this approach, developers can integrate this information into their applications, both on-chain and off-chain.

### Metadata Extension

The Roles Metadata extension extends the traditional JSON-based metadata schema of NFTs. Therefore, DApps supporting this feature MUST also implement the metadata extension of ERC-721 or ERC-1155. This extension is **optional** and allows developers to provide additional information for roles.

Updated Metadata Schema:

```js
{

  /** Existing NFT Metadata **/

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
    }
  },

  /** Additional fields for Roles **/

  "roles": [
    {
      "id": {
        "type": "bytes32",
        "description": "Identifies the role"
      },
      "name": {
        "type": "string",
        "description": "Human-readable name of the role"
      },
      "description": {
        "type": "string",
        "description": "Describes the role"
      },
      "supportsMultipleAssignments": {
        "type": "boolean",
        "description": "Whether the role supports simultaneous assignments or not"
      },
      "inputs": [
        {
          "name": {
            "type": "string",
            "description": "Human-readable name of the argument"
          },
          "type": {
            "type": "string",
            "description": "Solidity type, e.g., uint256 or address"
          }
        }
      ]
    }
  ]

}
```

The following JSON is an example of ERC-7432 Metadata:

```js
{
  // ... Existing NFT Metadata

  "roles": [
    {
      // keccak256("PROPERTY_MANAGER")
      "id": "0x5cefc88e2d50f91b66109b6bb76803f11168ca3d1cee10cbafe864e4749970c7",
      "name": "Property Manager",
      "description": "The manager of the property is responsible for furnishing it and ensuring its good condition.",
      "supportsMultipleAssignments": false,
      "inputs": []
    },
    {
      // keccak256("PROPERTY_TENANT")
      "id": "0x06a3b33b0a800805559ee9c64f55afd8a43a05f8472feb6f6b77484ff5ac9c26",
      "name": "Property Tenant",
      "description": "The tenant of the property is responsible for paying the rent and keeping the property in good condition.",
      "supportsMultipleAssignments": true,
      "inputs": [
        {
          "name": "rent",
          "type": "uint256"
        }
      ]
    }
  ]

}
```

The properties of the `roles` array are SUGGESTED, and developers should add any other relevant information as necessary (e.g., an image for the role). However, it’s highly RECOMMENDED to include the `supportsMultipleAssignments` field, as shown in the example. This field is used in the `hasRole` function (refer back to **Unique and Non-Unique Roles**).

## Backwards Compatibility

On all functions and events, the standard requires both the `tokenAddress` and `tokenId` to be provided. This requirement enables dApps to use a standalone ERC-7432 contract as the authoritative source for the roles of immutable NFTs. It also helps with backward compatibility as NFT-specific functions such as `ownerOf` and `balanceOf` aren’t required. Consequently, this design ensures a more straightforward integration with different implementations of NFTs.

## Security Considerations

Developers integrating the Non-Fungible Token Roles interface should consider the following on their implementations:

- Ensure proper access controls are in place to prevent unauthorized role assignments or revocations.
- Take into account potential attack vectors such as reentrancy and ensure appropriate safeguards are in place.
- Since this standard does not check NFT ownership, it’s the responsibility of the dApp to query for the NFT Owner and pass the correct _grantor to the hasRole function.
- It’s the responsibility of the dApp to check if the role is unique or non-unique. To ensure the role was not assigned to another account when the role is unique, hasRole should be called with _supportsMultipleAssignments set to false.

## Reference Implementation

[NFT Roles](https://github.com/OriumNetwork/ERC7432-reference-implementation) - A reference implementation created by Orium Network.

- CC0 License.
- 100% test coverage.

## Replies

**PHAN** (2023-08-03):

This is nice and simple. It can also extend to lots of use cases, like lending in-game assets, delegating staking rewards to other wallets…

---

**Mani-T** (2023-08-04):

The extension of the metadata schema to include role-specific information is a stroke of genius.  Now, NFTs can carry not just their artistic value but also detailed descriptions of their roles and utilities.  It’s like turning NFTs into digital Swiss Army knives!

---

**ernani.eth** (2023-08-04):

Thanks for the feedback [@Mani-T](/u/mani-t)!

We initially thought on storing the role metadata on-chain, just like ERC-5982 (Access Control). But it’s difficult to manage, and requires that only privileged actors can manage roles. Extending the existing metadata extensions will definitely make things easier as it’s already something NFT projects are used to manage.

---

**karacurt** (2023-08-07):

We just finalized ERC-7432 reference implementation, check it out [here](https://github.com/OriumNetwork/ERC7432-reference-implementation)!

---

**timlrx** (2023-08-08):

Hi, any reasons why this exists as a standalone interface rather than extending ERC-5982? It would make 5982 useless if every token standard implements its own role access layer with a non-conforming interface.

---

**ernani.eth** (2023-08-08):

Hi [@timlrx](/u/timlrx)

We started the implementation using an extension of ERC-5982. The problem is that we can’t “natively” associate an NFT with a granted role nor make it automatically expire. We can potentially encode all this information in bytes and use the `IERC_ACL_GENERAL` extension to implement this behavior, but that would present another set of challenges:

1. Overcomplicate the implementation: EIP-7432 has two events and five functions, while ERC-5982 IERC_ACL_GENERAL has five events and nine functions.
2. Redundancy and waste of gas: If we extend ERC-5982, we will have to emit both events from EIP-7432 and ERC-5982. Is it beneficial to emit two RoleGranted events? One with the NFT indexed, and the other not?
3. Metadata Approach: ERC-5982 metadata extension can only be implemented on-chain, while EIP-7432 follows the standard approach for NFTs metadata, which is more flexible and can accommodate more use cases.

In short, we can extend ERC-5982, but for the above reasons, it wouldn’t be our preferred approach.

---

**SamWilsn** (2023-08-22):

Would it make sense to rename `_supportsMultipleAssignments` to `_onlyLatest` and invert its meaning? Or split it into two functions?

What does `roleData` do if the assignment doesn’t exist? Revert? Return an empty `bytes`?

Would it make sense to match the naming convention of ERC-721? So `roleExpiryOf(...)`, for example.

How does the concept of “last role assignment” interact with revoking roles? If I create two non-expired assignments, then revoke the most recent one, is the earlier unrevoked assignment the “last role assignment” now?

---

**ernani.eth** (2023-08-22):

Hi [@SamWilsn](/u/samwilsn),

As you suggested earlier, we split the `hasRole` function into `hasRole` and `hasUniqueRole`. This greatly simplified the docs, and removed the `_supportsMultipleAssignments` parameter.

The `roleData` function should return an empty array of bytes when there is no role assignment. We added this to the `Caveats` section (thanks for pointing it out).

Regarding revoking assignments of unique roles, when a new assignment is created it should invalidate the previous one. Meaning that even if the new role assignment is revoked, the previous one should remain invalid (the previous assignment shouldn’t go back to being valid). Hopefully this was described in the `Unique and Non-Unique Roles` section.

---

**ernani.eth** (2023-08-23):

Hello everyone!

The initial PR was merged today, and the EIP is now available at the website: [ERC-7432: Non-Fungible Token Roles](https://eips.ethereum.org/EIPS/eip-7432)

I recommend everyone reviewing this version instead of the forum post (as it’s hard to keep adding changes to the forum post).

---

**ProphetZX** (2023-08-23):

I personally reject such suggestions because ethereum has already more than enough sharing-related incidents, where roles and ownership rights get diluted.

---

**SamWilsn** (2023-08-23):

Is there another standard that already covers this use case, or are you saying that roles for NFTs are a bad idea in general? I’m sure the authors would appreciate specific examples of how roles might cause issues so they can add them to the Security Considerations section.

---

**ProphetZX** (2023-08-23):

Well, I personally find roles a bad idea in general. We had many problems with role-based access for client-specific purposes in the past. For example, instead of creating new NFTs/Tokens for assets or for access which client’s profited from, they created access rights after access rights without proper ownership. This does not only make it harder to clearly see who actually controls/owns an NFT, but also makes automated analytics harder to implement.

---

**Weixiao-Tiao** (2023-08-24):

The official document llink of ERC-7432:



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7432)





###



Role Management for NFTs. Enables accounts to share the utility of NFTs via expirable role assignments.

---

**ernani.eth** (2023-08-24):

Thanks for sharing [@Weixiao-Tiao](/u/weixiao-tiao)! It would also be great to hear what you think of the proposed ERC.

[@ProphetZX](/u/prophetzx), regarding your comment, [Role-based Access Control](https://en.wikipedia.org/wiki/Role-based_access_control) is a widely used approach in computer systems. ERC-7432 was inspired by [ERC-5982](https://eips.ethereum.org/EIPS/eip-5982), which is incredibly popular despite being under review.

I believe the best example of how much roles are being used in smart contracts is the [OpenZeppelin’s AccessControl module](https://docs.openzeppelin.com/contracts/4.x/api/access#AccessControl), which is probably the most popular solidity library out there.

It’s also important to note that ERC-7432 is agnostic of any implementation of NFTs and **does not deal with custody**.

---

**ernani.eth** (2023-09-08):

Hello Everyone,

After some community feedback, we introduced ERC-721-style approvals to the standard. Here are the PR with the changes: [Update EIP-7432: Add Approval Interface by karacurt · Pull Request #7674 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7674)

We also updated our reference implementation: [GitHub - OriumNetwork/ERC7432-reference-implementation: Referene implementation of ERC-7432](https://github.com/OriumNetwork/ERC7432-reference-implementation)

---

**SamWilsn** (2024-09-03):

> For this reason, it’s RECOMMENDED using type(uint64).max to support use cases that require a role never to expire.

Are implementations allowed to assume `type(uint64).max` is permanent, or do they have to expire at that far future time?

