---
source: magicians
topic_id: 11759
title: EIP-5982 Role-based Access Control
author: xinbenlv
date: "2022-11-16"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/eip-5982-role-based-access-control/11759
views: 3013
likes: 4
posts_count: 17
---

# EIP-5982 Role-based Access Control

Hi all, we are proposing a Role-based ACL EIP

- Github PR for draft: Add EIP-5982: Role-based Access Control Interface by xinbenlv · Pull Request #5982 · ethereum/EIPs · GitHub
- After draft PR merged: https://eips.ethereum.org/EIPS/eip-5982 (currently doesn’t exist yet)

## Replies

**ThunderDeliverer** (2022-11-16):

Hi, the link that you included points to a page that doesn’t exist. Would you mind updating it (if your PR hasn’t been merged yet, I think that a link to it might be ok)?

---

**xinbenlv** (2022-11-16):

Good point. I updated the links

---

**frangio** (2022-11-28):

There is a “core” interface that is compatible with OpenZeppelin’s `AccessControl`, but then the events are incompatible. Why is that?

What is the motivation to add `bytes data` arguments to each function? This isn’t explained.

The behavior of functions isn’t specified.

In my opinion this EIP is in a state where it shouldn’t even be accepted as a Draft.

---

**xinbenlv** (2022-11-28):

GM [@frangio](/u/frangio) thank you for the comment

### 1. Why “incompatible” events?

> There is a “core” interface that is compatible with OpenZeppelin’s AccessControl , but then the events are incompatible. Why is that?

I assue you are referring to the ones in `IERC_ACL_GENERAL`

```solidity
    event RoleGranted(address indexed grantor, bytes32 indexed role, address indexed grantee, bytes _data);
    event RoleRevoked(address indexed revoker, bytes32 indexed role, address indexed revokee, bytes _data);
```

These events helps indexers and off-chain users to get information about change of Roles.

Please note that the mandate in the specification is

> Compliant contracts MUST implement IERC_ACL_CORE
> It is RECOMMENDED for compliant contracts to implement the optional extension IERC_ACL_GENERAL.

Which means OZ’s `AccessControl.sol` is considered compliant to this EIP (it complies with the MUST interfaces). It’s ok that a compliant ignore specs that’s marked as “RECOMMENDATION”.

The recommendations are left there so that future clients, e.g. MetaMask and future contracts, and start to implement better features provided by this new EIP

### 2. Why “bytes” field in methods?

> What is the motivation to add bytes data arguments to each function? This isn’t explained.

Thanks for the comment, I tried to explained that but maybe that’s not obvious enough. These extra `bytes` are meant to support [EIP-5750 General Extensibility](https://eips.ethereum.org/EIPS/eip-5750),

*EIP-5982 Role-based Access Control*

> ## Rationale
>
>
>
> …
> 2. The methods in IERC_ACL_GENERAL conform to EIP-5750 to allow extension.

So they could support future expansions, for example:

- Compared to GovernerAlpha, The new GovernerBravo adds new methods castVoteWithReason and castVoteWithSig which can be supported without change of method if they have an extra bytes.
- Compared to ERC-20’s transferm, ERC-721 and ERC-1155’s transferFrom has an extra bytes to support future extensions.

Example of of possible future extension include:

- Commit-Reveal scheme, using bytes to supply a salt, see EIP-5732 and an Reference Implementation of CommitableERC721
- Endorsement to supply signatures, replacing the need for creating GovernerBravo.castVoteWithSig or ERC-2612: Permit Extension for EIP-20 Signed Approvals

```auto
function permit(address owner, address spender, uint value, uint deadline, uint8 v, bytes32 r, bytes32 s) external
```

And since you () are the author of EIP-1271 and EIP-2612, I am hoping to put these examples hopefully resonate with these areas of your great efforts:

- with GovernerBravo.castVoteWithSig and ERC2612.permit, imaging in the future we need multi-sig to do threshold signing, they will need to create new methods. Using EIP-5750, we get the benefit of not needing to create new methods.

### Why are behavior of functions not specified?

> The behavior of functions isn’t specified. In my opinion this EIP is in a state where it shouldn’t even be accepted as a Draft.

I agree with you we shall provide more details about behavior of functions as an EIP.  I will add more details soon.

That said, this snapshot is to go for DRAFT status which is before REVIEW status. Hence we are putting here for early feedback, hopefully the name of these functions are largely self-explanatory. But I think based on the definition of DRAFT status in [EIP-1](https://eips.ethereum.org/EIPS/eip-1#eip-process) *EIP Process Section*, it should be ok for publication as Draft status,

[@frangio](/u/frangio), I greatly appreciate your feedback and looking for your advices in this EIP draft. ![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=15)

---

**frangio** (2022-11-28):

If there is a goal of compatibility with OpenZeppelin, compatible events should be part of `IERC_ACL_CORE`.

---

**xinbenlv** (2022-11-28):

We are definitely happy to add these events into `IERC_ACL_CORE` if getting your support, but if I may take sometime to clarify and make sure we are on the same page about the implications.

We want this new EIP to be compatible to OpenZeppelin, more specifically we are looking at [IAccessControl.sol](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/8f8fd84f1e60426a5e785d6b5b2524938271bb05/contracts/access/IAccessControl.sol) between OZ v4.4.1 - v.4.8.0

Therefore the methods and events of `IERC_ACL_CORE` needs to be a *subset* of `AccessControl.sol`

$$

S_{IERC_ACL_CORE} \subset S_{OZAcessControl.sol}

$$

The events of question are similar and inspired by [openzeppelin-contracts/IAccessControl.sol at 8f8fd84f1e60426a5e785d6b5b2524938271bb05 · OpenZeppelin/openzeppelin-contracts · GitHub](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/8f8fd84f1e60426a5e785d6b5b2524938271bb05/contracts/access/IAccessControl.sol#L26-35)

But not entirely the same such as `bytes` and `grantor` to allow off-chain approval and extending behavior.

If OZ find these events critical and is interested in committing to support these new version of event definition and commit to change to new version, we are happy to consider moving such events to `IERC_ACL_CORE` to make them a mandatory.

---

**frangio** (2022-11-28):

My point is that if there is an interest in making this compatible with AccessControl from OpenZeppelin the event definitions should be changed to match that contract and moved into the core interface.

---

**xinbenlv** (2022-11-28):

That is the purpose of this draft: to start early discussion of design choices like this.

OZ IAccessControl.sol v4.4.1-4.8.0

```auto
event RoleGranted(bytes32 indexed role, address indexed account, address indexed sender);
```

EIP-5982 Draft `I_ERC_GERNERAL`

```auto
event RoleGranted(address indexed grantor, bytes32 indexed role, address indexed grantee, bytes _data);
```

The current snapshot EIP demonstrated a technical opinionated view that OZ’s current IAcessControl.sol 's events are not sufficiently designed to cover future cases, and hence, until other-wised convinced, this EIP made a design choice to go for different event definitions as demonstrated in its IERC_GENERAL.

Let me know which is the case:

1. You think there is editorial unclarity that EIP-5982 wants to comply with OZ’s IAccessControl but creates events with different name / parameters than what’s already in OZ IAccessControl.sol v4.4.1 and you thought the EIP Author is not conscious that such different parameters will cause OZ’s IAccessControl event to be non-compliant with EIP-5982’s optional interface IERC_GENERAL at current snapshot,
2. You understand the EIP is consciously making a design choice to propose a different event definition debating the design choices made in EIP-5982 to use different name and parameters for these events and is choose not to mandate it so OZ IAccessControl.sol v4.4.1 can remain compatible with EIP.

---

**frangio** (2022-11-28):

I understand this might be a choice but I am questioning that choice: I believe function-only compatibility is too reduced a form of compatibility. Event compatibility is also important, otherwise the functions might as well be entirely different. Additionally, I don’t think forgoing event compatibility is justified in this case: personally, I doubt the usefulness of EIP-5750, but even if we take it as a given to be a good idea, I don’t see strong reasons for including it in the events, in fact that EIP doesn’t mention events.

---

**xinbenlv** (2022-11-28):

Per private discussion with [@frangio](/u/frangio), we are align on the terminology of *compliance*. Going to (2), we are debating **design choices**of

## Design Choice A: what shall event signature of RoleGranted be?

### Option 1. same as of OZv4.4.1-OZv.4.8.0

```auto
event RoleGranted(bytes32 indexed role, address indexed account, address indexed sender);
```

- Pros: simple, backward compatible with OZv.4.41-v4.8.0 which is widely adopted
- Cons: didn’t indicate who granted the role, and didn’t add bytes for future extension.

Option 2. use new events

```auto
event RoleGranted(address indexed grantor, bytes32 indexed role, address indexed grantee, bytes _data);
```

- Pros:

indicate who granted the role, allowing use cases e.g. off-chain approval signatures
- add bytes for future extension, allowing use cases .e.g reasoning, commit-reveal, endorsement-approval

Cons: aren’t the same as OZv.4.41-v4.8.0. Will require OZ to change IAccessControl if they want to also conform to `IERC_ACL_GENERAL`

Is this a good summary of our diverging preferences and pros and cons? [@frangio](/u/frangio)

---

**frangio** (2023-01-04):

Something looks odd about that. In Option 1 you list “Cons: didn’t indicate *who* granted the role”, but the event includes a `sender` parameter which is in fact who granted the role, isn’t it?

You also say “didn’t add *bytes* for future extension”, but as I’ve expressed in the discussion for [EIP-5750](https://ethereum-magicians.org/t/erc-5750-extra-data-parameter-in-methods/11176/11) I still don’t see any compelling reasons to include `bytes data`.

I’m biased but I don’t think these are strong enough reasons to break compatibility.

If the concern about the `sender` parameter is that it doesn’t account for the case where the grant was made via a signature instead of via a transaction (so `msg.sender` is some other account who just has a signed approval), I’d be open to repurpose the `sender` parameter and extend its meaning so that it isn’t necessarily the msg.sender and is whoever allowed the role grant through whatever means. I think that was the original intended meaning for the parameter anyway.

---

**xinbenlv** (2023-01-04):

[@frangio](/u/frangio) appreciate your comment.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> Something looks odd about that. In Option 1 you list “Cons: didn’t indicate who granted the role”, but the event includes a sender parameter which is in fact who granted the role, isn’t it?

With the trend of account abstraction / smart contract wallet, or permit-based actions, it will be more and more the case when `sender` is not the `grantor`. Just like ERC20 first start off with `transfer(to, amount)` assuming the transferer is always the sender, and then later shift to a model with `approve` + `transferFrom(from, to, amount)`. I believe this is going to be a general trend. Therefore, I specifically propose this design choice of specifying a `grantor`.

–

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> If the concern about the sender parameter is that it doesn’t account for the case where the grant was made via a signature instead of via a transaction (so msg.sender is some other account who just has a signed approval), I’d be open to repurpose the sender parameter and extend its meaning so that it isn’t necessarily the msg.sender and is whoever allowed the role grant through whatever means. I think that was the original intended meaning for the parameter anyway.

I think we are on the same page: we both think `sender` is going to not aways be `grantor`.  I propose to call it grantor, and I am also open to use the same format with existing OZ 4.4.1’s `RoleGranted ` but repurpose `sender` to `grantor`.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> You also say “didn’t add bytes for future extension”, but as I’ve expressed in the discussion for EIP-5750 I still don’t see any compelling reasons to include bytes data.
>
>
> I’m biased but I don’t think these are strong enough reasons to break compatibility.

EIP-5750 opens up all sorts of extensionability, e.g.

1. Supplying secret salt with EIP-5732 Commit Service for Commit-Reveal scheme
2. Supplying endorsement for same-TX permit using EIP-5453, or aviding what needs a separate TX as in ERC-2612 or ERC-4494.
3. Avoid the limitation of EIP-1271 which is being solved by Add EIP-6066: Signature Validation Method for NFTs by boyuanx · Pull Request #6066 · ethereum/EIPs · GitHub
4. Avoid the limitation of original domain separator lacking “extensions” in EIP-712 being addressed by ERC-5267: Retrieval of EIP-712 domain which is proposing an uint256[] extensions

Let’s continue the discussion on EIP-5750.

---

**radek** (2023-07-15):

Is this a pure goal? Frankly speaking OZ’s RBAC is space inefficient for its purpose.

Esp. the bytes32 roles. Look at Solmate / Solady / Huffmate, that uses bitmapping for roles. Thus having 256 roles, which can be assumed enough for most cases.

Can this standard be generic enough to capture such cases? Or is that only OZ specific standard?

---

**xinbenlv** (2023-07-16):

Standard is different from Implementation. Efficiency in this case is largely determined by the implementation.

I think the ERC-5982 is generic enough to support the bitmap roles, you could just ignore the first 24bits and only assume the input will be uint8 or bytes8.

The interface ERC-5982 only provides “hasRole”, “grantRole”, “revokeRole” but doesn’t care how it was implemented.

For example

```plaintext
interface IERC_ACL_CORE {
    function hasRole(bytes32 role, address account) external view returns (bool);
    function grantRole(bytes32 role, address account) external;
    function revokeRole(bytes32 role, address account) external;
}

interface BitmapAuth is IERC_ACL_CORE {
    mapping(address => bytes32) _roles;
    function hasRole(bytes32 role, address account) external view returns (bool) {
      require(role > role) & 1 != 0;
    }
    function grantRole(bytes32 role, address account) external {
      require(role <= 0xffffffff);
      _roles[account] |= bytes32(1 << role);
      // emit
    }
    function revokeRole(bytes32 role, address account) external {
      require(role <= 0xffffffff);
      _roles[account] &= ~bytes32(1 << role);
      // emit
    }
}
```

Just like people can just assume there will be at most 10000 NFTs and use ERC721 with internally an array of 10000 rather than a map. This interface of ERC-5982 is generalized enough to be compatible with when people use uint8 bitmap roles.

---

**radek** (2023-07-25):

I appreciate that you elaborated the mapping approach. ![:clap:](https://ethereum-magicians.org/images/emoji/twitter/clap.png?v=12)

Would you mind to adjust the wording in the EIP to reflect such option?

> A role in a compliant smart contract is represented in the format of bytes32. It’s RECOMMENDED the value of such role is computed as a keccak256 hash of a string of the role name, in this format: bytes32 role = keccak256(""). such as bytes32 role = keccak256("MINTER").

e.g. to

> A role in a compliant smart contract is represented in the format of bytes32. It’s RECOMMENDED the value of such role is computed as a keccak256 hash of a string of the role name, in this format: bytes32 role = keccak256(""). such as bytes32 role = keccak256("MINTER"). To support the bitmap based roles, it’s RECOMMENDED to ignore the first 24bits and only assume the input will be uint8 or bytes8.

---

**xinbenlv** (2023-07-27):

Here is a reference implementation for “createRole”

```auto
mapping roleRegistry;
function createRole(bytes32 role, bytes32 adminOfRole, string name, string desc, string uri, bytes32 calldata _data) external {
  roleRegistry[role] = adminOfRole;
  // also store name, desc, uri in each own storage
}

function roleName(bytes32 role) returns (string) {
  return roleNames[role];
}
```

You can also do ENS-based Role / NFT-based Role

```auto
function createRole(bytes32 role, bytes32 adminOfRole, string name, string desc, string uri, bytes32 calldata _data) external {
  _mintNFT(role/*nftID*/, adminOfRole/*address of Owner / parentNFTId*/);

}
```

