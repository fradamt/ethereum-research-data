---
source: magicians
topic_id: 15967
title: EIP-7531 Resolving Staked ERC-721 Ownership Recognition
author: sullof
date: "2023-10-01"
category: EIPs
tags: [nft, token]
url: https://ethereum-magicians.org/t/eip-7531-resolving-staked-erc-721-ownership-recognition/15967
views: 3939
likes: 15
posts_count: 34
---

# EIP-7531 Resolving Staked ERC-721 Ownership Recognition

**Abstract**: The ownership of ERC721 tokens when staked in a pool presents challenges, particularly when it involves older, non-lockable NFTs like, for example, Crypto Punks or Bored Ape Yacht Club (BAYC) tokens. This proposal introduces an interface to address these challenges by allowing staked NFTs to be recognized by their original owners, even after they’ve been staked.

**Motivation**: Recent solutions involve retaining the ownership of the NFT while “locking” it. However, this presupposes that all NFTs are “lockable”. For vintage or previously minted NFTs, like BAYC, this poses an issue. Once staked in a pool, the NFT’s ownership transfers to the staking pool, preventing, for example, original owners from accessing privileges or club memberships associated with those NFTs.

To circumvent this limitation, we propose an interface that exposes a function that allows to know the original owner of the staked NFT.

**Specification**: The proposed interface introduces a method, `holderOfRightsFor`, that enables callers to determine the original owner of a staked NFT.

```auto
interface ERC7531 {
  function holderOfRightsFor(
    address tokenAddress,
    uint256 tokenId
  ) external view returns (address);
}
```

**Flow**:

1. A user stakes an NFT in a pool.
2. As is customary, ownership of the NFT transfers to the staking pool as usual.
3. If the staking pool implements this interface, it exposes the holderOfRightsFor method.
4. Apps and other contracts can call this method to determine the original owner of the staked NFT or whoever has ownership rights on it.

**Rationale**: This approach provides a workaround for the challenges posed by non-lockable NFTs. By exposing the information about the original owner through the `holderOfRightsFor` method. This way it would ensure that staking does not hinder the utility or privileges tied to certain NFTs.

**Note on Non-Staking Contract Ownership**

This interface is intended for staking pool contracts and other similar contracts that take ownership of tokens like NFTs. However, ownership of NFTs by other smart contracts like Gnosis Safe, ERC4337 or [ERC6551](https://ethereum-magicians.org/t/erc-6551-non-fungible-token-bound-accounts/13030/202) wallets would not necessarily implement this interface. In these cases, it is acceptable for the contract to have ownership without exposing original ownership information.

For example, if a smart wallet owns an NFT and receives an airdropped asset, this is fine since the original owner still has control of the smart wallet. The interface proposed here specifically targets staking contracts where obscuring original ownership poses problems.

**Backwards Compatibility**: This interface can seamlessly integrate with any upgradeable contract that owns NFTs, provided they choose to adopt it. It does not require changes to the ERC721 standard but acts as an enhancement for staking pools and other contracts that receive NFTs for any reason.

**Conclusion**: The `ERC7531` interface proposal offers a streamlined solution for recognizing the ownership of staked NFTs, especially those that are non-lockable. Adopting this proposal will ensure that NFT holders do not lose out on associated benefits when they stake their tokens.

## Replies

**andyscraven** (2023-10-02):

I like this idea but I think that **ownerOf** is not the right name for this as could cause confusion, if you think about ERC721, for example.

**ownerOfToken**, perhaps!

---

**sullof** (2023-10-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/andyscraven/48/8271_2.png) andyscraven:

> I like this idea but I think that ownerOf is not the right name for this as could cause confusion, if you think about ERC721, for example.

You raise a good point. While the signature prevents any technical conflicts, using “ownerOf” in the name could cause confusion conceptually when thinking about ERC721 contracts.

I asked ClaudeAI for some alternative naming suggestions, and it proposed several options that help differentiate this function from the standard ERC721 ownerOf():

- getStakedNFTOwner()
- stakedNFTOwner()
- ownerOfStakedNFT()

Since this interface is specifically for retrieving the owner of a staked NFT, I agree it makes sense to use a name that explicitly includes “NFT”.

Of the options, I think **stakedNFTOwner()** or **ownerOfStakedNFT()** would be the clearest. Using “staked” and “NFT” in the name distinguishes it from the ERC721 ownerOf() function, while making clear that it refers specifically to non-fungible tokens.

What do you think?

---

**sullof** (2023-10-02):

I want to clarify the flow from the point of view of a project. Let’s say that Yuga Labs wants to airdrop something to all the owners of a Mutant Ape. They can check the current owner of the Ape. If that owner is a contract, they may verify if that contract support this interface and if so, get the actual owner of the NFT and airdrop the new asset to them.

---

**urataps** (2023-10-02):

I agree that we need some naming alternatives to eliminate any confusion with ERC721. I would vote for `ownerOfStakedNFT()`, but perhaps we can consider the shorter `stakerOf()` as well, though we lose the reference to NFTs for conciseness.

---

**sullof** (2023-10-02):

I like `stakerOf`.

Actually it was my initial idea but I dismissed it for some reason that I don’t recall now ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

---

**sullof** (2023-10-02):

It was because it looked too focused on staking pool, while an NFT can be transferred to a contract in many contexts.

---

**urataps** (2023-10-03):

In that case we may drop any mention of staking and go for something like `actualOwnerOf()` or `originalNFTOwner()`.

---

**sullof** (2023-10-03):

Maybe we can converge on `ownerOfToken` proposed by [@andyscraven](/u/andyscraven), or go for `ownerOfNFT` that excludes tokens other than ERC721. Or putting things together `actualOwnerOfNFT` which is more verbose but makes things more clear.

---

**sullof** (2023-10-03):

If the name of interface refers explicitly to ERC721 we may avoid repeating it in the name of the function. We can just add something that specify that that is the real owner. So, we can use `realOwnerOf`, `actualOwnerOf`, `originalOwnerOf`… I will think about it and decide before opening a PR in the EIP repository. Thanks [@urataps](/u/urataps) and [@andyscraven](/u/andyscraven) for the precious feedback.

---

**sullof** (2023-10-03):

I thought more about the concept. Consider a scenario where Bob stakes an NFT in a pool giving Alice the right to unstake it. Our function should most likely return Alice as the “owner” of the token. In other words, the contract should return the address that has rights on that token. In this case, if that changes, the function can stay updated.

Maybe names like

```js
function holderOfRightsFor(
    address tokenAddress,
    uint256 tokenId
) external view returns (address);
```

could be more general, covering more sub-cases.

---

**sullof** (2023-10-05):

I considered the possibility that the contract emits an event to specify the holder of rights.

The pros

- The event would help NFT marketplaces and similar entities to get the actual owner without being forced to query the smart contract
- There would not be a need for emitting a new event when the token is unstaken if the new owner is the previous holder of rights

The cons

- There is an extra cost for the users anytime an NFT is staked in the contract
- An existing upgradeable staking pool upgrading the contract to support the interface would be forced to emit events for any staked token, which may be expensive for the contract’s owner

Considering that the goal of this interface, I concluded that it is better to not emit any event and just expose the view function.

---

**sullof** (2023-10-05):

I just raised a PR in the EIPs repository:

https://github.com/ethereum/ERCs/pull/30

Thanks [@andyscraven](/u/andyscraven) and [@urataps](/u/urataps) for the feedback.

---

**stoicdev0** (2023-10-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sullof/48/3709_2.png) sullof:

> holderOfRightsFor

This seems perfect to me.  I was wondering if this could be achieved through a stand alone repo for backwards compatibility, but it might be tricky to decide who gets to set the right holder.

We have a wrapper contract that adds extended NFT capabilities (Namely ERC-5773, ERC-7401 and ERC-6220), on regular 721s and this would fit perfectly there, since the wrapper contract holds the tokens and mints new ones.

Great proposal! Happy to give a hand if needed.

---

**stoicdev0** (2023-10-13):

Might wanna update the original description, it still refers to `ownerOf`.

```auto
Specification: The proposed interface introduces a method, ownerOf, that enables callers to determine the original owner of a staked NFT.
```

---

**sullof** (2023-10-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> Might wanna update the original description, it still refers to ownerOf.
>
>
>
> ```auto
>
> ```

Thanks. I have updated the description.

---

**sullof** (2023-10-26):

Due to the new ERCs repository, the PR has been moved to

https://github.com/ethereum/ERCs/pull/30

---

**dievardump** (2023-10-26):

To help indexers and other systems, I think any contract that implements this ERC should emit an event when the NFT is staked.

Indexer POV: Indexers (being marketplaces but also others) already have a lot of work to do when seeing a Transfer event, and asking them to automatically check if the recipient is a contract and check if it implements this EIP, and then call “holdersOfRightsFor” on the contract to save the information that the NFT rights are still held by another address might be complicated.

Builder POV: Same thing, it’s also not sustainable to expect builders who want to make an airdrop or something based on ownership to check each NFTs owner and see if they implement this EIP, to then retrieve the real ownership.

I wouldn’t do it. It’s a lot of RPC ![:man_shrugging:](https://ethereum-magicians.org/images/emoji/twitter/man_shrugging.png?v=12).

However, by emitting an event that says “this NFT is only staked, rights are however still owned by X”, with indexed contract address and tokenId and a third param being " `holderOfRights", you would make it way easier for them to get the information and respect it: as an indexers builder, I’m more open to add a new topic to index, since I already have the current block events, than to add several RPC calls to my “Transfer” handler

---

**sullof** (2023-10-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> To help indexers and other systems, I think any contract that implements this ERC should emit an event when the NFT is staked.

Initially, I thought an event might be a suitable solution. However, I decided against it because events only apply to newly deployed contracts. If we don’t mandate an event, then existing upgradeable staking pools can still adopt the interface. Given that most staking pools are upgradeable contracts, I believe that the benefits of using an event are offset by the drawbacks. I’m interested to hear your thoughts on this matter—what do you think?

---

**sullof** (2023-10-27):

A way to allow existing pools to still implement the interface even if emitting an event is required, would be adding a batch events for existing tokens. [@dievardump](/u/dievardump) What do you think about this?

---

**dievardump** (2023-10-27):

I see.

Imo, you shouldn’t target the existing pools with this, or at least it shouldn’t be a concern for the event:

Pools that would take the time to update to implement this can easily also add a function that allows users to emit all the events for all their already staked items (and offer an “upgrade” button on their interface for users to call this function)

I’ll again come with the “Indexer POV”, but as an indexer, when I index and I do introspection, I cache the results in my DB. So the first time I see a pool I will introspect for the different interfaces I’m looking for, but not later. So I would miss this EIP if it was only added after the first time I encountered the contract.


*(13 more replies not shown)*
