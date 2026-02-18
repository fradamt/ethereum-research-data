---
source: magicians
topic_id: 9105
title: "EIP-6366: A standard for permission token"
author: chiro-hiro
date: "2022-05-01"
category: EIPs
tags: [erc, token, permission, proposal]
url: https://ethereum-magicians.org/t/eip-6366-a-standard-for-permission-token/9105
views: 3131
likes: 4
posts_count: 7
---

# EIP-6366: A standard for permission token

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/6366)














####


      `master` ← `orochi-network:master`




          opened 06:44AM - 22 Jan 23 UTC



          [![](https://avatars.githubusercontent.com/u/8078873?v=4)
            chiro-hiro](https://github.com/chiro-hiro)



          [+900
            -0](https://github.com/ethereum/EIPs/pull/6366/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/EIPs/pull/6366)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.












## Abstract

This EIP offers an alternative to Access Control Lists (ACLs) for granting authorization and enhancing security. Each permission is represented by a single bit in `uint256` from which we can defined up to `256` permissions and `2²⁵⁶` roles. This approach use bitwise operator and bitmask to determine the access right which is much more efficient and flexible than `string` comparison or `keccak()`. We are able to specify the importance of permission based on the bit order.

## Motivation

Special roles like `Owner`, `Operator`, `Manager`, `Validator` are common for many smart contracts because permissioned addresses are used to administer and manage them. It is difficult to audit and maintain these system since these permissions are not managed in a single smart contract.

Since permission and role are reflected by the permission token balance of the relevant account in the given ecosystem, cross-interactivity between many ecosystems will be made simpler.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

*Note* The following specifications use syntax from Solidity `0.8.7` (or above)

### Interface ERC6366 Core

Compliant contracts MUST implement `IERC6366Core`.

```auto
interface IERC6366Core {

event Transfer(address indexed _from, address indexed _to, uint256 _value);

event Approval(address indexed _owner, address indexed _delegatee, uint256 _permission);

function transfer(address _to, uint256 _permission) external returns (bool success);

function approve(address _delegatee, uint256 _permission) external returns (bool success);

function permissionOf(address _owner) external view returns (uint256 permission);

function permissionRequire(uint256 _required, uint256 _permission) external view returns (bool isPermission);

function delegated(address _owner, address _delegatee) external view returns (uint256 permission);

}

```

It is RECOMMENDED to define each permission as a power of `2` so that we can check for the relationship between sets of permissions using the bitwise operator and bitmask.

*Example*

```plaintext
const PERMISSION_NONE = 0;

const PERMISSION_READ = 1; // 2⁰

const PERMISSION_WRITE = 2; // 2¹

const PERMISSION_EXECUTE = 4; // 2²

// Role admin = 4 | 2 | 1 = 7

const ROLE_ADMIN = PERMISSION_READ | PERMISSION_WRITE | PERMISSION_EXECUTE;

// Role operator = 1 | 2 = 3

const ROLE_OPERATOR = PERMISSION_READ | PERMISSION_WRITE;

```

The most important permission SHOULD be greater than the lesser one.

#### transfer

Transfers a subset of `_permission` permission to address `_to`, and MUST emit the `Transfer` event.

The function SHOULD `revert` if the message caller’s account permission does not have the subset of the transferring permission. The function SHOULD `revert` if any of transferring permission is existing on target `_to` address.

*Note* Transfers of `0` permission MUST be treated as normal transfers and emit the `Transfer` event.

```auto
function transfer(address _to, uint256 _permission) external returns (bool success);

```

#### approve

Allows `_delegatee` to act for the permission owner’s behalf, up to the `_permission` permission. If this function is called again it overwrites the current granted with `_permission`.

*Note* `_permission` MUST be a subset of all available permission of permission owner.

*Note* `approve()` method SHOULD `revert` if granting `_permission` permission is not a subset of all available permission of permission owner.

```auto
function approve(address _delegatee, uint256 _permission) external returns (bool success);

```

#### permissionOf

Returns the account permission of the given `_owner` address.

```auto
function permissionOf(address _owner) external view returns (uint256 permission);

```

#### permissionRequire

Return `true` if `_required` permission is a subset of `_permission` permission otherwise return `false`.

```auto
function permissionRequire(uint256 _required, uint256 _permission) external view returns (bool isPermission);

```

#### delegated

Returns the subset permission of the `_owner` address were granted to `_delegatee` address.

```auto
function delegated(address _owner, address _delegatee) external view returns (uint256 permission);

```

#### Transfer

MUST trigger when permission are transferred, including zero permission transfers.

A token contract which creates new tokens SHOULD emit a `Transfer` event with the `_from` address set to `address(0x00)` when tokens are created.

```auto
event Transfer(address indexed _from, address indexed _to, uint256 _value)

```

#### Approval

MUST trigger on any successful call to `approve(address _delegatee, uint256 _permission)`.

```auto
event Approval(address indexed _owner, address indexed _delegatee, uint256 _permission)

```

### Interface ERC636 Metadata

It is RECOMMENDED for compliant contracts to implement the optional extension `IERC6366Meta`.

```auto
interface IERC6366Meta {

struct PermissionDescription {

uint256 index;

uint256 permission;

string name;

string description;

}

event UpdatePermissionDescription(uint256 indexed _permission, string indexed _name, string indexed _description);

function name() external view returns (string memory);

function symbol() external view returns (string memory);

function getDescription(uint256 _index) external view returns (PermissionDescription memory description);

function setDescription(uint256 _index, string memory _name, string memory _description) external returns (bool success);

}

```

#### name

Returns the name of the token - e.g. `"OpenPermissionToken"`.

```auto
function name() external view returns (string memory);

```

#### symbol

Returns the symbol of the token. E.g. `"OPT"`.

```auto
function symbol() external view returns (string memory);

```

#### getDescription

Return a description of a permission, at a given `_index`.

```auto
function getDescription(uint256 _index) external view returns (PermissionDescription memory description);

```

#### setDescription

Return `true` if the description was set otherwise return `false`. It MUST emit `UpdatePermissionDescription` event.

```auto
function setDescription(uint256 _index, string memory _name, string memory _description) external returns (bool success);

```

SHOULD define a relationship between `index` field and `permission` field in `PermissionDescription`. It is RECOMMENDED to define `permission` is 2 to the power of `index`.

#### UpdatePermissionDescription

MUST trigger when description is updated.

```auto
event UpdatePermissionDescription(uint256 indexed _permission, string indexed _name, string indexed _description);

```

### Interface ERC6366 Error

SHOULD NOT expected `IERC6366Error` interface was implemented.

```auto
interface IERC6366Error {

error AccessDenied(address _owner, address _actor, uint256 _permission);

error DuplicatedPermission(uint256 _permission);

error OutOfRange();

}

```

## Rationale

Needs discussion.

## Reference Implementation

First implementation of EIP-6366 could be found here:

- ERC-6366 Core implementation
- ERC-6366 Meta implementation

## Security Considerations

Need more discussion.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**davidc** (2022-05-03):

I just quickly glanced over this proposal, but wouldn’t it be a common desire that the entity granted permission to perform an action is not the same as the entity in control for choosing who holds this permission?

For example, a smart contract may have permission to do some basic actions, but a separate election/governance smart contract would be in control of changing ownership of this permission.

This is crucial for separation of concerns, and provides increased security when we separate these requirements into different smart contracts.

How can this be achieved using your proposal?

Perhaps the implementation itself could have some sets of permissions for transfer etc. which are then controlled by other permission tokens.

---

**chiro-hiro** (2022-05-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/davidc/48/5181_2.png) davidc:

> I just quickly glanced over this proposal, but wouldn’t it be a common desire that the entity granted permission to perform an action is not the same as the entity in control for choosing who holds this permission?
>
>
> For example, a smart contract may have permission to do some basic actions, but a separate election/governance smart contract would be in control of changing ownership of this permission.

The entity perform an action can be different from the entity in control of these permissions. This proposal allow permissions to be managed (transfer/grant/revoke) in a much more flexible and secure manner. In the reality, a DAO contract SHOULD hold the SUPER_USER_ROLE and grant a subset of its permission to any authorized operator via a weighted voting process.

```auto
mapping (address => uint256) delegatedPermission;

function grant(address operator, uint256 permissions) {
   require(balances[msg.sender] & permissions ==  permissions, 'Access Denied');
   delegated[operator] = delegated[operator] | permissions;
}

function revoke(address operator, uint256 permissions) {
   require(balances[operator] & permissions == permissions, 'Access Denied');
   delegated[operator] = (delegated[operator]  | permissions) ^ permissions;
}
```

E.g: `permissionToken.grant(childDAO, PERMISSION_CREATE | PERMISSION_EXECUTE)`

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/davidc/48/5181_2.png) davidc:

> This is crucial for separation of concerns, and provides increased security when we separate these requirements into different smart contracts.
>
>
> How can this be achieved using your proposal?
>
>
> Perhaps the implementation itself could have some sets of permissions for transfer etc. which are then controlled by other permission tokens.

We have 256 bits to store a given role (it can represent for 256 different permissions). This approach is flexible to adapt with new changes, we can introduce new permissions without breaking anything.

```auto
contract PermissionV1 {
    uint256 private constant PERMISSION_TRANSFER = 2**0;
    uint256 private constant PERMISSION_DELEGATE = 2**1;
    uint256 private constant PERMISSION_UPGRADE = 2**2;
}

contract EcosystemPermissionTokenV1 is PermissionToken, PermissionV1 {
    function transfer(address to, uint256 permission) external onlyAllow(PERMISSION_TRANSFER);
    function grant(address operator, uint256 permission) external onlyAllow(PERMISSION_DELEGATE);
}

contract PermissionV2 is PermissionV1 {
    uint256 private constant PERMISSION_CREATE = 2**3;
    uint256 private constant PERMISSION_EXECUTE = 2**4;
    uint256 private constant PERMISSION_SIGN = 2**5;
}

contract EcosystemV2 is PermissionV2 {
     // Permission V1 and V2 can be verified
     // without any changes from PermissionTokenV1
}
```

We can combine more than one permission tokens if needed.

---

**davidc** (2022-05-04):

What I mean is that the governance process should have permission to transfer permission rather than the contract that bears the permission, e.g. the `transfer` method might look something like this:

```auto
function transfer(address to, uint256 permissions) onlyAllow(ROLE_MANAGE_PERMISSIONS) ...
```

Delegating permissions is good here because it prevents the contract using these permissions from accidentally changing ownership. However, theoretically, the governance process which manages the ownership of the permissions could accidentally invoke the smart contract, which is perhaps a security risk. Of course, if it didn’t have this ability, it could just give itself permission, but at least this extra step would reduce the likelihood of this occurring.

---

**chiro-hiro** (2022-05-04):

Noted, thank you. This proposal will focus on how we organize and manage permissions and roles. So we need to draw a line between the implementation and the standard.

---

**chiro-hiro** (2023-01-19):

I’ve just updated the proposal and added my implement. Please help me to review, thank you.

---

**chiro-hiro** (2023-01-28):

[@davidc](/u/davidc) I’ve updated the implementation and write an example, please check and let me know if it resolved the issue that your raised [GitHub - orochi-network/EIP-6366: Implemente EIP-6366: Permission Token](https://github.com/orochi-network/EIP-6366/)

