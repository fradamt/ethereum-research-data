---
source: magicians
topic_id: 7371
title: "ERC-4400: ERC-721 Consumer Extension"
author: Daniel-K-Ivanov
date: "2021-10-30"
category: ERCs
tags: [nft, token]
url: https://ethereum-magicians.org/t/erc-4400-erc-721-consumer-extension/7371
views: 6104
likes: 13
posts_count: 25
---

# ERC-4400: ERC-721 Consumer Extension

## Abstract

This specification defines standard functions outlining a `consumer` role for instance(s)

of [ERC-721](https://eips.ethereum.org/EIPS/eip-721). An implementation allows reading the current `consumer` for a

given NFT (`tokenId`) along with a standardized event for when an `consumer` has changed. The proposal depends on and

extends the existing [ERC-721](https://eips.ethereum.org/EIPS/eip-721).

## Motivation

Many [ERC-721](https://eips.ethereum.org/EIPS/eip-721) contracts introduce their own custom role that grants permissions

for utilising/consuming a given NFT instance. The need for that role stems from the fact that other than owning the NFT

instance, there are other actions that can be performed on an NFT. For example, various metaverses use`operator`

/`contributor`

roles for Land (ERC-721), so that owners of the land can authorise other addresses to deploy scenes to them (f.e.

commissioning a service company to develop a scene).

It is common for NFTs to have utility other than simply owning it. That being said, it requires a separate standardized

consumer role, allowing compatibility with user interfaces and contracts, managing those contracts.

Having a `consumer` role will enable protocols to integrate and build on top of dApps that issue ERC721 tokens.

Example of kinds of contracts and applications that can benefit from this standard are predominantly metaverses that

have land and other types of digital assets in those metaverses (scene deployment on land, renting

land/characters/clothes/passes to events etc.)

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and

“OPTIONAL” in this document are to be interpreted as described in RFC 2119.

Every contract compliant to the `ERC721 Consumer` extension MUST implement the `ERC721Consumer` interface. The **consumer extension** is OPTIONAL for ERC-721 contracts.

```solidity
/// @title ERC-721 Consumer Role extension
/// Note: the ERC-165 identifier for this interface is 0x953c8dfa
interface ERC721Consumer /* is ERC721 */ {
    /// @notice This emits when consumer of a _tokenId changes.
    /// address(0) used as previousConsumer indicates that there was no consumer set prior to this event
    /// address(0) used as a newConsumer indicates that the consumer role is absent
    event ConsumerChanged(address indexed previousConsumer, address indexed newConsumer);
    /// @notice Get the consumer of a token
    /// @dev address(0) consumer address indicates that there is no consumer currently set for that token
    /// @param _tokenId The identifier for a token
    /// @return The address of the consumer of the token
    function consumerOf(uint256 _tokenId) view external returns (address);
    /// @notice Set the address of the new consumer for the given token instance
    /// @dev Throws unless `msg.sender` is the current owner, an authorised operator, or the approved address for this token. Throws if `_tokenId` is not valid token
    /// @dev Set _newConsumer to address(0) to renounce the consumer role
    /// @param _newConsumer The address of the new consumer for the token instance
    function changeConsumer(address _newConsumer, uint256 _tokenId) external;
}
```

Every contract implementing the `ERC721Consumer` extension is free to define the permissions of a `consumer` (e.g. what

are consumers allowed to do within their system) with only one exception - consumers MUST NOT be considered owners,

authorised operators or approved addresses as per the ERC721 specification. Thus, they MUST NOT be able to execute

transfers & approvals.

The `consumerOf()` function MAY be implemented as `pure` or `view`.

The `changeConsumer(address _newConsumer, uint256 _tokenId)` function MAY be implemented as `public` or `external`.

The `ConsumerChanged` event MUST be emitted when a consumer is changed.

## Rationale

Key factors influencing the standard:

- Keeping the number of functions in the interfaces to a minimum to prevent contract bloat.
- Simplicity
- Gas Efficiency
- Not reusing or overloading other already existing roles (e.g. owners, operators, approved addresses)

### Name

The chosen name resonates with the purpose of its existence. Consumers can be considered entities that utilise the token

instances, without necessarily having ownership rights to it.

The other name for the role that was considered was `operator`, however it is already defined and used within

the `ERC721` standard.

### Restriction on the Permissions

There are numerous use-cases where a distinct role for NFTs is required that MUST NOT have owner permissions. A contract

that implements the consumer role and grants ownership permissions to the consumer renders this standard pointless.

## Backwards Compatibility

There are no other standards that define a similar role for NFTs and the name (`consumer`) is not used by other ERC721

related standards.

## Reference Implementation

The following is a snippet for reference implementation of the ERC721Consumer extension. The full repository can be

found [here](https://github.com/Daniel-K-Ivanov/eip-721-consumer-extension)

```solidity
//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./IERC721Consumer.sol";
contract ConsumerImpl is IERC721Consumer, ERC721 {
    mapping(uint256 => address) consumers;
    constructor() ERC721("ReferenceImpl", "RIMPL") {
    }
    function consumerOf(uint256 _tokenId) view external returns (address) {
        return consumers[_tokenId];
    }
    function changeConsumer(address _newConsumer, uint256 _tokenId) external {
        require(msg.sender == this.ownerOf(_tokenId), "IERC721Consumer: caller is not owner nor approved");
        address previousConsumer = consumers[_tokenId];
        consumers[_tokenId] = _newConsumer;
        emit ConsumerChanged(previousConsumer, _newConsumer);
    }
    /**
     * @dev See {IERC165-supportsInterface}.
     */
    function supportsInterface(bytes4 interfaceId) public view virtual override(IERC165, ERC721) returns (bool) {
        return interfaceId == type(IERC721Consumer).interfaceId || super.supportsInterface(interfaceId);
    }
}
```

## Replies

**Daniel-K-Ivanov** (2021-11-03):

Link to the EIP PR - [Optional ERC721Consumer Extension by Daniel-K-Ivanov · Pull Request #4400 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/4400)

---

**MindfulFroggie** (2021-11-04):

Hi Daniel, I’m super happy you’re promoting this EIP.

I think we should promote both this EIP and [this one](https://ethereum-magicians.org/t/erc-standard-for-held-non-fungible-token-nfts-defi/7117) in parallel.

One comment I have is that with the current proposal, only the owner of the NFT can call the `changeConsumer` function. I think it would be good to add (or use) the mechanism of the ERC721 to aprove third parties to be able to use this function.

I imagine that there will be 3rd parties platforms (dapps) which NFT owners will use in order take advantage of this feature. Therefore the contract should give the 3rd parties the permission to change the consumers without the NFT owner having to do any action.

What do you think?

---

**Daniel-K-Ivanov** (2021-11-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mindfulfroggie/48/4805_2.png) MindfulFroggie:

> One comment I have is that with the current proposal, only the owner of the NFT can call the changeConsumer function. I think it would be good to add (or use) the mechanism of the ERC721 to aprove third parties to be able to use this function.

Thank you for the feedback!

Are you referring to the `approved` and `operator` addresses that can be authorised by the `owner` of the ERC-721 to spend/manage the tokens? If yes, I think that we can do that and will update the reference implementation with your suggestion

---

**MindfulFroggie** (2021-11-04):

Yes. That would be great.

From the [openzeplin implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol):

```auto
    // Mapping from token ID to approved address
    mapping(uint256 => address) private _tokenApprovals;

    // Mapping from owner to operator approvals
    mapping(address => mapping(address => bool)) private _operatorApprovals;
```

I do wonder if the approved  addresses should be the same as the ERC721 approved addresses. Or should it be a different dictionary instead → let’s say `_tokenConsumeApprovals`.

I think I’d go with the 1st option, but it is worth a thought.

---

**MindfulFroggie** (2021-11-12):

Just found this [EIP](https://eips.ethereum.org/EIPS/eip-2615).

It is much more elaborate and as you can see it is stagnant and has no activity for a long time.

edit: probably because it is gas expansive.

I keep studying solidity, and I think that there’s no way to use your proposed standard for current ERC721 projects without migrating the contracts, so this is a major drawback.

---

**Daniel-K-Ivanov** (2021-11-24):

The EIP has been updated with comments received from the community and implementors of the proposal.

[@MindfulFroggie](/u/mindfulfroggie) I’ve addressed your feedback by enabling approved address + operators to be able to change the consumer. Let me know what you think ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=10)

---

**wschwab** (2021-11-28):

Hey there! I was looking over your EIP (I left a review earlier which you resolved), and was wondering if you might want to switch the current setup so that there can be an array of addresses that are consumers instead of just one, since the current setup only allows for one address per `tokenId`. This doesn’t contradict cases where only one `consumer` is desired, since the implementing contract can always set a cap on how many addresses can be pushed to the array.

---

**Daniel-K-Ivanov** (2021-11-30):

At some point, I was thinking the same thing. Indeed there might be use-cases where you would like to have more than one consumer. I will think about it and maybe even update the proposal with your suggestion. I would like to see how much overhead it would introduce implementation/gas cost wise.

Thank you for the feedback though!

---

**Daniel-K-Ivanov** (2022-02-07):

The EIP has been updated with reference implementations in LandWorks (already live on mainnet). I have updated the use-cases to include nft staking as-well, since other than no collateral NFT renting, there are other use-cases for this standard which are implemented in the NFT staking mechanism of LandWorks here:



      [github.com](https://github.com/EnterDAO/LandWorks-YF-Contracts/blob/main/contracts/LandWorksDecentralandStaking.sol)





####



```sol
// SPDX-License-Identifier: MIT
pragma solidity 0.8.10;

/******************************************************************************\
* Custom implementation of the StakingRewards contract by Synthetix.
*
* https://docs.synthetix.io/contracts/source/contracts/stakingrewards
* https://github.com/Synthetixio/synthetix/blob/develop/contracts/StakingRewards.sol
/******************************************************************************/

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./interfaces/ILandWorks.sol";
import "./interfaces/IDecentralandEstateRegistry.sol";

```

  This file has been truncated. [show original](https://github.com/EnterDAO/LandWorks-YF-Contracts/blob/main/contracts/LandWorksDecentralandStaking.sol)










The EIP has been marked as “for review”. Any feedback is greatly appreciated!

---

**ilanolkies** (2022-02-22):

Hi, how are you? I was discussing about this EIP these days.

### Idea

I think maybe more robust way to face the problem of a standard way of understanding a role that is not the owner could be like `roleOf(bytes32 tokenId, bytes4 roleId) returns (address)` (or `address[]` as mentioned above).

### Considering

This came up while reading

> various metaverses use operator /contributor roles for Land

And also considreing “Mortgage/rental” use case mentioned above.

### Result

So this EIP would have a list of standard roles for NFTs (different than owner role) and the specification for each role could reside on newer EIPs linked from here.

This way wallets can then implement standard controls for standard behaviours on standard roles on NFTs.

### Use case

Now you could say *owner* can make use of `transfer` and `approve`. With this EIP we could then say `role: CONSUMER` can utilise the token instances, without necessarily having ownership rights to it (as mentioned in the EIP). Then, other roles like `role: TENANT`, might add standard functions to query how long the rental is for or a function to extend rental, thus showing these operations in standard way in all wallets and platforms.

---

**Daniel-K-Ivanov** (2022-02-24):

Hi [@ilanolkies](/u/ilanolkies)

Thanks for the suggestion / feedback. You are right that this proposal introduces new EIP for every role it would require, yes and its not scalable approach. From a first look your proposal sounds good as it can be applied to many roles. The only thing that concerns me is the fact that when a protocol wants to integrate a ERC721 implementing the EIP, they will need to know the exact roleId that has certain permissions and since the roleId can be arbitrary, we will not actually enforce a standard that will help procotols utilise the EIP.

Example → Generic NFT renting protocol wants to support `ERC721`s that implement the EIP and have a `renter` role. What would be the `roleId` that the protocol will be looking for when changing the role / querying the role?  Each NFT issuer can define their own `ID`. In order for this to work, we must define all roles explicitly and their ID. F.e defining that `bytes4(keccak("renter"))` is the `roleId` for someone that has permissions to utilise the NFT, but not be able to transfer it.

What do you think would be the mitigation of this issue?

---

**ilanolkies** (2022-02-24):

Yes. I really assumed it was clear that roles should have standard ids too

Role for “renter” should have same behavior and same id in any token supporting ERC-4400. Then other roles will have other standard accepted IDs associated with other standard behaviors specified on later EIPs that are accepted as standard by ERC-4400

Similar to what ERC-165 does with interface IDs

Then workflow for having a new standard interface would be

1. Get the EIP for the standard ERC-4400 extension approved
2. Propose PR to the list in ERC-4400 adding the interface id and a link to the EIP

This is similar to what ENS does for supporting standard records that can be queried by any wallet. See EIP-137

---

**Daniel-K-Ivanov** (2022-02-25):

That’s an interesting concept. I will circle that to other NFT discussions in the forum to gather more feedback.

---

**ArthurBraud** (2022-03-10):

Hey Daniel,

I like your proposal. One observation that I had is that this interface requires the consumer to trust the owner/operator as they are no guarantee that the rental agreements will be honored. For example, after a consumer pays the rental fees, the owner or an approver will still be able to change the consumer.

Or I am missing something?

I spent some time looking at NFT rental and to address this trust issue, I thought to delegate the rental agreement logic to a contract `IERC721RentalAgreement`. This contract controls whether the rent can be started or stopped.

The rent is initiated and stopped from the `ERC721` and a callback function to `IERC721RentalAgreement` can guarantee that the rental terms are fulfilled.  For example, `IERC721RentalAgreement` can enforce that the renter cannot be changed when there is an active rent.

(Also maybe `IERC721RentalAgreement` contract could handle the role definition?)

Here is the more concrete idea: [ERC721 extension to enable rental](https://ethereum-magicians.org/t/erc721-extension-to-enable-rental/8472)

---

**ilanolkies** (2022-03-11):

Do you think it is worth it to discuss the standard way of generically querying extension for roles in another thread? I mean, in a separate thread of how renting should be implemented.

---

**Daniel-K-Ivanov** (2022-03-13):

Hi [@ArthurBraud](/u/arthurbraud)

Thank you for the reply and feedback! You are right that the owner is able to change the consumer after he pays for the rent, however, the owner would be actually a smart contract/protocol, meaning that unless there is a bug in the implementation of the protocol, the rents will be honoured.

In order for generic NFT renting to be implemented, we need only the primitive that enables it. It would be easier to have the required “primitive” as standard (aka consumer/delegator etc) and utilise that for the implementation of renting than to propose and finalise a whole renting spec. Maybe I am missing something, but the renting protocol itself can decide on the renting agreements as it would be part of the business logic of the protocol. The only thing it would need is the ability to delegate the utility of the NFT to the renter which is tackled by the consumer role.  Actually focusing on the primitive aka “consumer” role, enables other use-cases compared to focusing on rent specification solely. F.e one can implement delegation to 3rd parties or NFT staking.

Let’s keep iterating on the ideas so that we can come up with **a** solution for this problem. All of us think that it is a pain point and will be an enabler for the NFT community so we are all in the same boat ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**Daniel-K-Ivanov** (2022-03-13):

I was thinking about the generic role extension that you’ve proposed. To me it seems that it can be applied generally to all types of contracts, f.e not only ERC721s but ERC20 or any contract for that matter. The spec for defining “roles” if described as the ENS reference that you’ve provided can be applied to **everything**. I am not stating that this is a negative thing. The drawback that I am seeing is that if we define a spec for “Generic Contract Role querying” and have specs for “Consumer Role” or any other type of role, we end up with a spec that overlaps (is a subset) with the existing ERC165 spec. Both of them address the same need: providing information on what is supported by the target contract.

Going with a concrete example. Let’s say that one way is to go with the same existing proposals:

- ERC165 support + Role-specific extension

and the other way is:

- “Generic Role Querying” + “Role-specific extension”

Wouldn’t it be the same whether we use ERC165 to figure out whether something is supported or not vs using the “generic role querying” to figure that out?

Maybe I am missing something. Can you please provide your thoughts on my concerns?

---

**awnyrvan** (2022-03-17):

Hello Daniel [@Daniel-K-Ivanov](/u/daniel-k-ivanov)

We are trying to use this erc4400 standard in our dapp. Would love you have your guidance. Would you be available for a call?

Cheers,

Anir

---

**ilanolkies** (2022-04-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/daniel-k-ivanov/48/4799_2.png) Daniel-K-Ivanov:

> ERC165 support + Role-specific extension

It is not just for querying what interfaces the contract support. It is for accessing the given role via its role ID. Maybe I am being to generic but this will enable easier integration from wallets and dapps if need to support different role type

---

**MissieBish** (2022-05-18):

Hello,

I was wondering why the consumer should be reset to address(0) when there is a transfer.

Wouldn’t it make more sense to default it to the owner’s address?

I have in mind projects who refer to the consumer address to give out benefits, like airdrops or whatever. I guess it would make more sense for the owner to be the default consumer when he/she isn’t renting out the token.

Cheers,

Aloys


*(4 more replies not shown)*
