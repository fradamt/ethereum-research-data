---
source: magicians
topic_id: 13366
title: "ERC-6982: Default Lockable Proposal"
author: sullof
date: "2023-03-17"
category: ERCs
tags: [nft, token]
url: https://ethereum-magicians.org/t/erc-6982-default-lockable-proposal/13366
views: 5766
likes: 52
posts_count: 58
---

# ERC-6982: Default Lockable Proposal

Many proposals for lockable ERC721 contracts exist in different phases of development:



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5192)





###



Minimal interface for soulbinding EIP-721 NFTs












      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5633)





###



Add composable soulbound property to EIP-1155 tokens












      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5753)





###



Interface for disabling token transfers (locking) and re-enabling them (unlocking).










and many others.

Unfortunately, any of them misses something or is too complicated and add extra functions that do not need to be part of a standard.

I tried to influence ERC-5192 making many comments and a PR that was closed by [@Pandapip1](/u/pandapip1) who suggested I make a new proposal. So, here we are.

The updated Interface (based on comment and discussions):

```auto
pragma solidity ^0.8.9;

// ERC165 interfaceId 0x6b61a747
interface IERC6982 {
  // This event MUST be emitted upon deployment of the contract, establishing
  // the default lock status for any tokens that will be minted in the future.
  // If the default lock status changes for any reason, this event
  // MUST be re-emitted to update the default status for all tokens.
  // Note that emitting a new DefaultLocked event does not affect the lock
  // status of any tokens for which a Locked event has previously been emitted.
  event DefaultLocked(bool locked);

  // This event MUST be emitted whenever the lock status of a specific token
  // changes, effectively overriding the default lock status for this token.
  event Locked(uint256 indexed tokenId, bool locked);

  // This function returns the current default lock status for tokens.
  // It reflects the value set by the latest DefaultLocked event.
  function defaultLocked() external view returns (bool);

  // This function returns the lock status of a specific token.
  // If no Locked event has been emitted for a given tokenId, it MUST return
  // the value that defaultLocked() returns, which represents the default
  // lock status.
  // This function MUST revert if the token does not exist.
  function locked(uint256 tokenId) external view returns (bool);
}
```

The primary limit in EIP-5192 (which I liked and I used in a couple of projects) is that

1. it has 2 events for Locked and Unlocked, which is not optimal.
To make a comparison, it’s like in the ERC721 instead of Transfer(from, to, id) used for mints, transfers and burns, there were Transfer(from, to, id), Mint(to, id), Burn(from, id), etc.
2. it forces you to emit an event even when the token is minted, causing a waste of gas when a token borns with a status and dies with it.

Take for example most soulbounds and non-transferable badges. They will be locked forever and it does not make sense to emit an extra event for all the tokens.

Using this interface, instead, the contract emits `DefaultLocked(bool locked)` when deployed, and that event sets the initial status of every token. Sometimes, as suggested by [@tbergmueller](/u/tbergmueller) in the comments, a token can have an initial status that changes at some point. If that happens, the DefaultLocked event can be emitted again. This implies that marketplaces and other observers must refer to last emitted DefaultLocked event if a Locked event has not been emitted for a specific tokenId.

The `Locked` events define the new status of any tokenId.

`locked` returns the current status, allowing other contracts to interact with the token.

`defaultLocked` returns the default status (since other contracts cannot get the event). The method also allows to have an interfaceId different than ERC5192, avoiding conflicts (thanks to [@urataps](/u/urataps))

This is an efficient solution that reduces gas consumption and covers most scenarios.

I think that functions to lock, unlock, lock approvals, etc. should be managed as extensions, and should be not included in a minimalistic interface about lockability.

The official EIP



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-6982)





###



A gas-efficient approach to lockable ERC-721 tokens










For an implementation, you can look at

https://github.com/ndujaLabs/erc721lockable

Notes:

On May 2nd, I added the suggestion to emit DefaultLocked() again if the default behavior changes, as suggested by @ [tbergmueller](https://ethereum-magicians.org/u/tbergmueller)

On May 6th, I added a `defaultLocked` function to avoid conflicts with ERC5192, thanks to [@urataps](/u/urataps)

**PS. I will keep the code of the interface above updated to avoid misunderstanding.**

## Replies

**andyscraven** (2023-03-19):

I like this approach as not all use cases need to allow for everything as not all use cases need everything. It is, after all, best practice to us the Single Responsibility principle when possible.

---

**tbergmueller** (2023-05-02):

Still on the search on “the” interface to expose transfer-locks in our [ERC-6956](https://ethereum-magicians.org/t/erc-6956-asset-bound-non-fungible-tokens/14056) … and since there are so many similar interfaces all doing the same I have the feeling I’m spamming the complete forum here, but nonetheless;

For us, also this interface would work with a small modification;

We do see use-cases, where the default lock-status changes over time, similar as the well-known mechnics of metadata-reveal. So a collection may be minted and the collection owner decides they cannot be transferred for the first 6 months. And after 6 months, tokens per default become transferable.

I suggest to define that DefaultLocked must be emitted whenever the default-lock status changes which includes at contract-deployment time.

---

**sullof** (2023-05-03):

Thanks. I like the suggestion.

I will include it in the EIP proposal, when (if) I will make it — I am so busy that I can’t find the time to make it ![:frowning:](https://ethereum-magicians.org/images/emoji/twitter/frowning.png?v=12)

For now I made an update here, and added a note about your suggestion.

---

**xtools-at** (2023-05-03):

thanks [@sullof](/u/sullof) for the work! i’m in the same boat, have used EIP-5192 before but don’t like it as of the stated limitations either, and the other examples are also not exactly appealing to me for various reasons. just implementing your proposal for my next project ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12) i hope this becomes an official standard, i’d also be happy to support with writing the EIP if you like.

---

**sullof** (2023-05-03):

I just created a PR on the EIP repo at

https://github.com/ethereum/EIPs/pull/6982

[@xtools-at](/u/xtools-at) if you have suggestion to improve the text, let me know. Any feedback is much appreciated.

---

**sullof** (2023-05-05):

I did what [@Pandapip1](/u/pandapip1) suggested (see post), but nobody is reviewing the PR above.

Has anyone any idea about the process?

---

**urataps** (2023-05-06):

I consider this idea simplistic and more efficient in many ways.

Using a single status event instead of two mirroring ones is easier to listen and index. Also, the `DefaultLocked` event is a smart way to avoid the burden of emitting upon each mint.

However, the modified `Locked` event introduces a backward compatibility issue with events from [EIP-5192](https://eips.ethereum.org/EIPS/eip-5192), which already left past the review stage and is used by multiple projects. It would be important to address this by either stating clearly that events are incompatible or change to the less efficient version ![:upside_down_face:](https://ethereum-magicians.org/images/emoji/twitter/upside_down_face.png?v=12)

Secondly, the `locked` function’s description should be more explicit in stating that it must return the latest default locked state if no token-specific lock actions have been performed, as in the observer and marketplaces example you provided.

Also, I’m curious to discover how the `locked` function would implement this functionality for unlockable tokens. One possible solution to think about would be to have the timestamp when the latest default state is changed, and disregard any outdated token-specific locks until then.

---

**sullof** (2023-05-06):

Those are good points. Thanks.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/urataps/48/9374_2.png) urataps:

> However, the modified Locked event introduces a backward compatibility issue with events from EIP-5192, which already left past the review stage and is used by multiple projects. It would be important to address this by either stating clearly that events are incompatible or change to the less efficient version

I think that this proposal is an alternative to EIP-5192. So, whoever implements it, should not implement the first. If someone must implement both, the contract will be forced to emit two events for the same action, which does not make much sense.

From the point of view of a marketplace, I assume that the marketplace first check the interfaceId and then, depending on it, listen to Locked(id) and Unlocked(id) or to Locked(id,isLocked).

The (painful) alternative would be to rename the event and call it some other way.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/urataps/48/9374_2.png) urataps:

> Secondly, the locked function’s description should be more explicit in stating that it must return the latest default locked state if no token-specific lock actions have been performed, as in the observer and marketplaces example you provided.

I totally agree on this. I added a note to the EIP.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/urataps/48/9374_2.png) urataps:

> Also, I’m curious to discover how the locked function would implement this functionality for unlockable tokens. One possible solution to think about would be to have the timestamp when the latest default state is changed, and disregard any outdated token-specific locks until then.

That depends on the specific project. There can be so many scenarios.

---

**sullof** (2023-05-06):

What if I use the world **sealed** instead of **locked**? The interface would become

```auto
interface IERC6982 /* is IERC165 */ {

    // MUST be emitted when the contract is deployed,
    // defining the default status of any token that will be minted.
    // It may be emitted again if/when the default behavior changes.
    event DefaultSealed(bool sealed);

    // MUST be emitted any time the status of a specific tokenId changes
    event Sealed(uint256 indexed tokenId, bool sealed);

   // Returns the status of the tokenId.
   // If no Locked event occurred for the tokenId, it MUST return the default status.
   // It MUST revert if the token does not exist.
    function sealed(uint256 tokenId) external view returns (bool);
}

```

I like it, but I see it as an extreme scenario, because I have already implemented that interface in production in a couple of projects and updating the contracts to change the event would create a lot of issues in the services that listen to the events.

---

**urataps** (2023-05-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sullof/48/3709_2.png) sullof:

> From the point of view of a marketplace, I assume that the marketplace first check the interfaceId and then, depending on it, listen to Locked(id) and Unlocked(id) or to Locked(id,isLocked).

If that’s the case then it should have a separate `interfaceId` from the EIP-5192 in order to identify it. Since the 5192 one is already decided by the selector of the `locked` function, I think we need a different signature for default lockable tokens. Going with the `sealed` version would solve this issue and still make sense naming-wise. If incompatibility with EIP-5192 is assumed, I would go for it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sullof/48/3709_2.png) sullof:

> I like it, but I see it as an extreme scenario, because I have already implemented that interface in production in a couple of projects and updating the contracts to change the event would create a lot of issues in the services that listen to the events.

However, this is a valid argument for keeping the original `locked` signature. Also, there might be other projects that desire interface compatibility with 5192 since marketplaces and off-chain services are used to it, which would force them to choose one version of the two.The only way I see to keep supporting this and also identify default lockable tokens is to add an extra method.

To avoid boilerplate and keep things simple, I would propose a `defaultLocked(uint256 tokenId) external view returns(bool) ` method which returns false whenever a token-specific lock status is changed since the last default lock, and true if none happened. This would also prove that the smart contract is keeping track of the status correctly and “resets” all tokens to the default state. For tokens that don’t support token-specific locks this method could just easily return `true` every time. In this way the interface is still compatible with EIP-5192 and also identifiable such that marketplace know what types of events to listen.

---

**sullof** (2023-05-06):

That is a great suggestion. I will add it, thanks.

Considering how minimalistic is the proposal, I would be happy to add you as a contributor to the EIP, if you are interested. If so, just let me know.

But I would prefer to add a

```auto
function defaultLocked() external view returns (bool);
```

which returns the default status.

---

**urataps** (2023-05-08):

Returning the default status is also a good solution, and it would be even simpler.

I would be glab to be a contributor to this EIP, thank you for the proposal, [@sullof](/u/sullof).

---

**sullof** (2023-05-10):

I changed the status of the PR from Draft to Review.

---

**SamWilsn** (2023-06-02):

Why do you limit changing the default to only before the first token event? Should probably explain the reasoning behind that in the rationale section.

---

**hiddenintheworld** (2023-06-02):

Could you modify it in a way so it is more customizable, maybe adding a threshold decided by the owner, or decided by voting power? Adding something like allowing the use of ZK proof to lock and unlock could also be something that add modularity.

---

**sullof** (2023-06-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Why do you limit changing the default to only before the first token event? Should probably explain the reasoning behind that in the rationale section.

Thank you for bringing up this concern. I can see how my original explanation may have led to some confusion. I will update the ERC.

The proposal does not, in fact, restrict changes to the default status solely to before the first token event. Rather, the `DefaultLocked` event can be triggered anytime there is a change in the default status applicable to all tokens.

The primary area of uncertainty pertains to whether a newly emitted `DefaultLocked` event should supersede all previously emitted `Locked` events, or whether it should only apply to tokens that have not yet been impacted by a `Locked` event.

To address this, I’m contemplating the introduction of an `override` parameter to the `DefaultLocked` event. This modification would look like this:

```auto
event DefaultLocked(bool status, bool override);
```

Here, if `override` is set to true, the event will take precedence over any previously emitted `Locked` events, effectively resetting the status of all tokens. However, if `override` is false, the event will only influence tokens that have yet to be subjected to a `Locked` event. I would appreciate your thoughts on this potential solution.

---

**sullof** (2023-06-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hiddenintheworld/48/9658_2.png) hiddenintheworld:

> Could you modify it in a way so it is more customizable, maybe adding a threshold decided by the owner, or decided by voting power? Adding something like allowing the use of ZK proof to lock and unlock could also be something that add modularity.

Thank you for your input. I appreciate your suggestions to enhance the modularity of the proposal. However, I believe that the interface should primarily focus on providing a broad approach that can be readily applied in a variety of scenarios. It would be more prudent for the implementer to optimize it further based on specific use-cases.

Adding conditions on who can lock or unlock tokens might complicate the implementation, especially in simpler scenarios. For instance, in the case of badges and soulbound tokens, the status is usually fixed at the start and remains unchanged. Additional complexities could make the application of this standard unnecessarily burdensome.

When you mention making the proposal more customizable, could you clarify what aspects you’re referring to? If the goal is to manage more granular details of token transferability, you might find ERC-6454 more suitable. It provides a comprehensive framework for managing transferability and would not conflict with this proposal.

As an additional note, I’d like to direct your attention to an example implementation of this proposal available at:



      [github.com](https://github.com/ethereum/EIPs/blob/721d967b4f27f2d644117f8c578166e274b7171f/assets/eip-6982/contracts/ERC721Lockable.sol)





####



```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// Authors: Francesco Sullo

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/utils/Address.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./IERC721Lockable.sol";
import "./IERC6982.sol";

// This is an example of lockable ERC721 using IERC6982 as basic interface

contract ERC721Lockable is IERC6982, IERC721Lockable, Ownable, ERC721, ERC721Enumerable {
  using Address for address;

  mapping(address => bool) private _locker;
  mapping(uint256 => address) private _lockedBy;

```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/721d967b4f27f2d644117f8c578166e274b7171f/assets/eip-6982/contracts/ERC721Lockable.sol)










This implementation showcases a system managing NFTs that can be locked in place as opposed to being staked. This approach affords the token owner the benefit of retaining ownership while still imposing a lock on the token. It’s worth noting that this implementation has been utilized effectively in production for several months.

However, despite the success of this specific implementation, I am of the opinion that further additions or complexities to ERC-6982 may not necessarily be advantageous. The proposal aims to maintain a balance between functionality and simplicity, and I believe it achieves that as it currently stands.

Thus said, I am totally available to change it if there is a strong support for it.

---

**hiddenintheworld** (2023-06-02):

You could make the criteria for locking and unlocking tokens more customizable. For instance, rather than having a fixed locking status for each token, it could depend on certain conditions or be modified by specific users. Ideas like controlling the lock status dynamically via bytecode. However, be aware that it’s a complex task with many potential pitfalls, and potentially security risks, which I’m outlining in a simplified manner below.

We will create a contract that accepts bytecode and executes it to determine if a tokenId is locked or not. The owner can set the bytecode logic.

```auto
contract DynamicLockERC721 is ERC721, Ownable {
    // Mapping from token ID to bytecode
    mapping (uint256 => bytes) private _logic;

    constructor(string memory name, string memory symbol) ERC721(name, symbol) {}

    // Function to set the logic of a token
    function setLogic(uint256 tokenId, bytes memory bytecode) public onlyOwner {
        _logic[tokenId] = bytecode;
    }

    // Function to check the lock status of a token
    function isLocked(uint256 tokenId) public view returns (bool) {
        bytes memory bytecode = _logic[tokenId];
        bytes32 result;

        assembly {
            result := mload(add(bytecode, 0x20))
        }

        // Assuming that the bytecode returns a boolean, convert the result into a boolean
        return result != bytes32(0);
    }

    // Override transfer function to include lock status check
    function _transfer(address from, address to, uint256 tokenId) internal override {
        require(!isLocked(tokenId), "ERC721: token is locked");

        super._transfer(from, to, tokenId);
    }
}
```

---

**SamWilsn** (2023-06-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sullof/48/3709_2.png) sullof:

> The primary area of uncertainty pertains to whether a newly emitted DefaultLocked event should supersede all previously emitted Locked events, or whether it should only apply to tokens that have not yet been impacted by a Locked event.

Personally I would not expect the status of already minted tokens to change when the default changes. Doing otherwise would mean tokens exist in one of three states: locked, unlocked, and undefined. That behaviour might be a little unexpected.

---

**sullof** (2023-06-02):

I am not sure I got it. The proposal does not give any recommendation about how to lock/unlock tokens, leaving a lot of freedom to the user.


*(37 more replies not shown)*
