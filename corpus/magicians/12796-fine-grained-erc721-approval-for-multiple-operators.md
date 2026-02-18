---
source: magicians
topic_id: 12796
title: Fine-grained ERC721 approval for multiple operators
author: arrans
date: "2023-02-01"
category: ERCs
tags: [token]
url: https://ethereum-magicians.org/t/fine-grained-erc721-approval-for-multiple-operators/12796
views: 2886
likes: 23
posts_count: 17
---

# Fine-grained ERC721 approval for multiple operators

Before submitting an EIP I’d like to get some feedback on an idea, please.

**Summary**: ERC721 “approval” for a specific token is currently limited to a single operator via the `approve()` function. Holders wishing to list assets for sale on multiple marketplaces must therefore use `setApprovalForAll()`, which goes against the principle of least privilege. I would like to propose a per-token, multiple-operator approval mechanism as an extension to ERC721.

**Motivation**: a number of phishing scams trick users into signing zero-ETH ask-side orders for fulfilment via marketplace contracts. A user wishing to legitimately sell only a single NFT therefore risks their entire portfolio of the respective contract. This is what happened to Kevin Rose, resulting in the theft of 25 Chromie Squiggles when he had legitimately intended to sell only one. I was on a call with him when it happened so am very familiar with the technical aspects of what happened.

**Additional requirements**: a solution must require minimal effort for adoption by marketplaces. Introduction of a per-token alternative to `isApprovedForAll()` => `setApprovalForAll()` would follow their existing technical flows as outlined after the interface definition in the below proposal.

The [Head of Protocol at OpenSea has lent support](https://twitter.com/Slokh/status/1620233893675962369?s=20&t=J0zIeOMFVYGuYV3LPl3rHw).

**Alternatives considered**: the majority of negative feedback I’ve received (to the above-linked tweet) has been that `approve()` fulfils this requirement. It does *not*, however, allow for approval of more than one operator. NFT traders would therefore be limited to selling via  a single marketplace.

**Proposal**:

EDIT: add `ApprovalFor` event.

An interface along the lines of:

```auto
interface IERC721PerTokenApproval {
    /**
     * @notice Emitted when an operator is enabled or disabled for a token.
     */
    event ApprovalFor(
        address indexed _operator,
        uint256 indexed _tokenId,
        bool _approved
    );

    /**
     * @notice Approves the operator to manage the asset on behalf of its owner.
     * @dev Throws if msg.sender is not the current NFT owner.
     * @dev Approvals set via this method MUST be cleared upon transfer of the
     *      token to a new owner.
     */
    function setApprovalFor(
        address _operator,
        uint256 _tokenId,
        bool _approved
    ) external;

    /**
     * @notice Returns true if any of the following criteria are met:
     *         1. _operator was approved via setApprovalFor() on `_tokenId`
     *            and the token has not since been transferred; OR
     *         2. isApprovedForAll(ownerOf(_tokenId), _operator) == true; OR
     *         3. getApproved(_tokenId) == _operator.
     */
    function isApprovedFor(address _operator, uint256 _tokenId)
        external
        view
        returns (bool);

    // ERC-165
    function supportsInterface(bytes4 interfaceID) external view returns (bool);
}
```

The requirement to clean up approvals on transfer can be done efficiently [with an incrementing nonce, as described here](https://twitter.com/dievardump/status/1620467635266920448?s=20&t=J0zIeOMFVYGuYV3LPl3rHw).

Marketplaces wishing to check approvals prior to listing assets would follow this pattern:

```auto
if (nft.supportInterface(type(IERC721PerTokenApproval).interfaceId)) {
  if (!nft.isApprovedFor(marketplace, tokenId)) {
    // initiate user to setApprovalFor(marketplace, tokenId, true)
  }
} else {
  // fallback to existing setApprovalForAll()
  if (!nft.isApprovedForAll(nft.ownerOf(tokenId), marketplace)) {
    // initiate user to setApprovalForAll(marketplace, true)
  }
}
```

**For further consideration**: should `setApprovalFor(…,false)` override `setApprovalForAll()`? This complicates `isApprovedFor()`, which suggests that the 3 positive criteria *may* be too broad, *or* that there could be an `isExplicitlyApprovedFor()` that only returns true if criterion (1) is met.

## Replies

**arrans** (2023-02-01):

Hat tip to @crisgarner who I hadn’t realised had [posted about this a few days before me](https://twitter.com/crisgarner/status/1620185419714560000).

---

**Slokh** (2023-02-01):

In support of making this an EIP. At OpenSea we can easily support this vs other similar proposals and it addresses all the major issues at the moment (biggest concern is really just in-product UX for supporting both approval paths).

Particularly a fan of “Approvals set via this method MUST be cleared upon transfer of the token to a new owner.”. Not often do people actually clean up their approvals and should just be done in the background.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arrans/48/8479_2.png) arrans:

> should setApprovalFor(…,false) override setApprovalForAll()? This complicates isApprovedFor(), which suggests that the 3 positive criteria may be too broad, or that there could be an isExplicitlyApprovedFor() that only returns true if criterion (1) is met.

I actually don’t think it should overrides because then it muddies the clarity of `isApprovedForAll` as well

---

**crisgarner** (2023-02-01):

To add more context for people not familiar with current implementations of the ERC721 token standard. ERC721 wasn’t designed for the current environment of multiple marketplaces, signatures, and bidding.

The approve function uses a mapping that saves only the **id** and the **address** of one approved contract, there is no way to approve two different contracts without replacing the previous approval, approving Open Sea, Blur, x2y2, and Looks Rare at the same time is currently impossible without using handler contracts and obfuscate the information to users.

This is where `setApprovalFor` comes in handy. Here is the ERC721 Approve code for reference:

```auto
// Mapping from token ID to approved address
mapping(uint256 => address) private _tokenApprovals;

function approve(address to, uint256 tokenId){
   _tokenApprovals[tokenId] = to;
}
```

---

**0xInuarashi** (2023-02-01):

nice methods for single-to-many approvals proposed by [@dievardump](/u/dievardump) and [@cxkoda](/u/cxkoda) for revoking and transfers.

also, i would like to suggest interfaces for quanitity-based approvals (non tokenid specific) for operators using sort of these other functions as well

```auto
interface IERC721PerTokenApproval {
    /**
     * @notice Emited when a user approves an operator for an amount
     */
    event ApprovalForAmt(
        address indexed _operator,
        uint256 _amount
    );

    /**
     * @notice Approves an operator for an amount of tokens
     * @dev The amount should decrease each time the operator transfers the user's token
     */
    function setApprovalForAmt(
        address _operator,
        uint256 _amount
    ) external;
}
```

rationale being some folks may want to list ~10 NFTs and do not want to specifically approve each one, but also may be holding ~250 NFTs of the same contract.

---

**0xInuarashi** (2023-02-01):

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/f/f3c79b4d319f4de0517824526e5d06f27532ef46_2_690x347.jpeg)image1133×570 53.8 KB](https://ethereum-magicians.org/uploads/default/f3c79b4d319f4de0517824526e5d06f27532ef46)

A small visualization of the different methods

---

**crisgarner** (2023-02-01):

For ERC721 might be complicated as you would need to specify which tokens as the transfer function requires the Id. An array of ids could be passed as a parameter to fix this issue.

```auto
interface IERC721PerTokenApproval {

    /**
     * @notice Approves an operator for an amount of tokens
     * @dev The amount should decrease each time the operator transfers the user's token
     */
    function setApprovalForIds(
        address _operator,
        uint256[] memory _tokenIds,
        bool _approved
    ) external;
}
```

While this solution fixes current issues, must be noted that in the future, with Account Abstraction and smart contract wallets, it’s possible to batch `setApprovalFor` and execute it in one transaction.

---

**0xInuarashi** (2023-02-01):

I know I’m deviating a lot but gonna throw some more ideas out there:

How about lists? For example, a user can store their own specified “list” in a mapping

```auto
/**
 * @notice: Example mapping
 * owner -> list id -> operator -> approved
 */

mapping(address =>
mapping(uint256 =>
mapping(address => bool))) ownerToListIdToApprovalList;

/**
 * @notice Configures a list of approved operators for the user at ListID index
 * @dev Throws if list ID is 0 as it should be the default "empty" list.
 */
function setListApproval(
    uint256 listId,
    address operator,
    bool approved) external;
```

They can specify their own list and then approve to it using an approve function

```auto
/**
 * @notice Example mapping
 * token id -> approval list
 *
 * @note This example would look up to:
 * ownerToListToApprovalList[ownerOf(tokenId)][tokenId][tokenIdToApprovalList[tokenId]][operatorAddress]
 * to obtain an approved boolean
 */
mapping(uint256 => uint256) tokenIdToApprovalList;

/**
* @notice Approves a token to a user-specified list of pre-approved addresses.
* @dev Throws if the msg.sender is not the NFT owner.
*/
function approveTokenToList(
    uint256 tokenId,
    uint256 listId) external;
```

On a transfer, the approved token list is set to 0.

Although this may be a bit difficult to integrate with.

---

**cxkoda** (2023-02-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xinuarashi/48/8484_2.png) 0xInuarashi:

> also, i would like to suggest interfaces for quanitity-based approvals (non tokenid specific) for operators using sort of these other functions as well

I like your ideas about quantity-based approvals. But I think they are a bit beside the goal of this proposal: making marketplace approvals safer by explicitly stating which tokens are transferable. This explicitness would be lost with quantities.  Also, it feels more like a marketplace feature to me than a token’s core functionality.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/crisgarner/48/8482_2.png) crisgarner:

> For ERC721 might be complicated as you would need to specify which tokens as the transfer function requires the Id. An array of ids could be passed as a parameter to fix this issue.

I like the extension to arrays of IDs. I think account abstraction is still far away, so this would be a good solution for the meantime.

---

**arrans** (2023-02-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/slokh/48/8480_2.png) Slokh:

> I actually don’t think it should overrides because then it muddies the clarity of isApprovedForAll as well

Good point! We’ll think more closely about the interplay between the two when we right a reference implementation.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xinuarashi/48/8484_2.png) 0xInuarashi:

> also, i would like to suggest interfaces for quanitity-based approvals (non tokenid specific) for operators using sort of these other functions as well

Hey [@0xInuarashi](/u/0xinuarashi) ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) I agree with [@cxkoda](/u/cxkoda) that quantities probably belong in a separate EIP. The goal of this one is for an owner to be able to be very precise in their granting of approvals. Lists are an interesting way of doing this… I’ll get a repo set up soon and we can explore them in there.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/crisgarner/48/8482_2.png) crisgarner:

> An array of ids could be passed as a parameter to fix this issue.

I think the `setApprovalForIds()` function should take a `bool` like the single-token equivalent. Again, we can explore this in the repo.

---

**0xInuarashi** (2023-02-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arrans/48/8479_2.png) arrans:

> Hey @0xInuarashi  I agree with @cxkoda that quantities probably belong in a separate EIP. The goal of this one is for an owner to be able to be very precise in their granting of approvals. Lists are an interesting way of doing this… I’ll get a repo set up soon and we can explore them in there.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cxkoda/48/6228_2.png) cxkoda:

> I like your ideas about quantity-based approvals. But I think they are a bit beside the goal of this proposal: making marketplace approvals safer by explicitly stating which tokens are transferable. This explicitness would be lost with quantities. Also, it feels more like a marketplace feature to me than a token’s core functionality.

Thats completely fine! Just firing my brain cannons hehe

As for the functionality of such proposal I think whatever we have now seems very nice as PoC from [@dievardump](/u/dievardump) and [@cxkoda](/u/cxkoda)

It can get more complex with lists and delegations but I think that’s also beyond-scope for this EIP

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/crisgarner/48/8482_2.png) crisgarner:

> ```auto
> interface IERC721PerTokenApproval {
>
>     /**
>      * @notice Approves an operator for an amount of tokens
>      * @dev The amount should decrease each time the operator transfers the user's token
>      */
>     function setApprovalForIds(
>         address _operator,
>         uint256[] memory _tokenIds
>     ) external;
> }
> ```

This is nice! Similarly, a single-to-many interface can also be added with

```auto
interface IERC721PerTokenApproval {

    /**
     * @notice Approves a token to multiple operators
     * @dev The token approvals should be cleared on a transfer
     */
    function setApprovalForOperators(
        uint256 _tokenId,
        address[] memory _operators,
        bool approved
    ) external;
}
```

---

**arrans** (2023-02-02):

Here’s a [fork of the EIPs repo](https://github.com/proofxyz/EIPs); we will merge to `erc721-per-token-approvals` in this repo to collaborate and then I’ll issue a PR to the original when ready.

---

**crisgarner** (2023-02-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arrans/48/8479_2.png) arrans:

> I think the setApprovalForIds() function should take a bool like the single-token equivalent. Again, we can explore this in the repo.

You are right! Fixed it.

---

**lukasz-glen** (2023-07-17):

Hello. Hope you are doing great. It’s been a while since the last update in the proposal. Any difficulties?

I was working with approvals recently and I find this proposal very interesting. Here are some my remarks.

You proposed the interface `IERC6464AnyApproval` to query a contract if a transfer is approved without getting into details of approval mechanisms. But an owner of a token is not checked. Is it on purpose? I can imagine a situation that an owner is not permitted to transfer a token - in some renting schema for instance, or soul-bound tokens.

The interface `IERC6464AnyApproval` is general purpose. I wonder if it does deserve a separate proposal. I can come up with two other approval mechanisms that fall under it. One is approvals with expiration date. There is a short [demo](https://gist.github.com/lukasz-glen/c1768ecb0d5138f10d52a07c23e16140) but it boils down to: instead of bool (approved/not approved) use timestamp/uint (allowance is valid until a given timestamp). The other is renting - it can be restricted that a token can only be returned to an origin owner. Yet another idea soul-bound tokens. All of these mechenisms can utilize the interface `IERC6464AnyApproval`. So placing it in the EIP with token id based approvals can be misleading. What do you think?

---

**lukasz-glen** (2023-07-17):

I guess this is it: ERC-6454: [Minimal Transferable NFT detection interface](https://eips.ethereum.org/EIPS/eip-6454)

---

**RenanSouza2** (2023-07-17):

I’m not comfortable on how error prone an implementation would be

I suggest something like

```auto
funtion isApproved(address owner, address spender, uint id) returns (bool)
```

So this token is only transferable by `spender` as long is token `tokenId` is owned by `owner`

---

**arrans** (2023-09-26):

> It’s been a while since the last update in the proposal. Any difficulties?

Sorry, we’ve had to prioritise other work temporarily but will be picking this up again soon. As soon as we do I’ll read through the rest of your post and reply (yours too [@RenanSouza2](/u/renansouza2)).

