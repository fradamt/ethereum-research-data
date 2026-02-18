---
source: magicians
topic_id: 10526
title: EIP1705 - An account bound token with permission based minting
author: arjn
date: "2022-08-26"
category: EIPs
tags: [nft, eip]
url: https://ethereum-magicians.org/t/eip1705-an-account-bound-token-with-permission-based-minting/10526
views: 951
likes: 4
posts_count: 7
---

# EIP1705 - An account bound token with permission based minting

NFTs are becoming widely adopted for their use as collectable, profile avatars, etc.

But NFTs have much more use cases apart from just buying and selling ape jpegs.

**Problem Statement** :

1. NFTs today are used for their financial value rather than their use cases which include event passes, identities, degrees, etc. The ERC721 and ERC1155 NFT standards are not capable of serving these use cases since their ownership can be transferred which makes it unusable to be used for identity or degree, etc
We need a standard which does not permit the users to transfer the ownership of their NFTs. These tokens have to be attached to the address it is minted to.

The solution is an Address Bound Token.

1. The inherent problem with ERC20/ERC721/ERC1155 or any ERC token standard is that bad actor can target the users with fake/thrashy/spam NFTs or Fungible Tokens. The user does not have a way to prevent anyone from doing so. In order to get rid of these spam tokens, they will have to transfer the tokens to someone else or burn it by transferring it to the null address.

The downside to this is that the users need to call the `transfer()` function which takes up gas, ultimately having the users pay for something which they never intended to have in their wallet in the first place.

The solution is to have a contract which requires the signature of the user for anyone to transfer an NFT to their address.

**Solutioning** :

1. Create a contract which is an extension of ERC721 which does not have a transfer() or transferFrom() function.
2. When this contract wants to mint an SBT for some address, it will require the user’s EIP721 signature.
3. Once the user’s signature is available, the contract can mint tokens for the user.
4. When the user provides the signature, the user can specify if the signature provided is for one time or forever. If the signature provided is forever, then the contract address will be whitelisted for the user.
5. The mint function in the contract can check the validity of the signature before minting any tokens in the future.

## Replies

**arjn** (2022-08-26):

I am proposing something on this forum for the first time.

I am hoping to get some feedback from the experts and see this proposal to its finality…

Cheers…!! ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

---

**Pandapip1** (2022-08-26):

FYI - this wouldn’t be assigned EIP-1705

---

**Pandapip1** (2022-08-26):

Also, there are a lot of soulbound EIPs:



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5484)





###



Interface for special NFTS with immutable ownership and pre-determined immutable burn authorization












      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5192)





###



Minimal interface for soulbinding EIP-721 NFTs












      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5114)





###



A badge that is attached to a "soul" at mint time and cannot be transferred after that.












      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5516)





###



An interface for non-transferrable, Multi-owned NFTs binding to Ethereum accounts












      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-4973)





###



An interface for non-transferrable NFTs binding to an Ethereum account like a legendary World of Warcraft item binds to a character.












      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-4671)





###



A standard interface for non-tradable tokens, aka badges or souldbound NFTs.










I would highly recommend waiting for one of those to become the most commonly-used standard and then extend *that*.

---

**arjn** (2022-08-28):

[@Pandapip1](/u/pandapip1)

Yes, you are right. But I was looking from the PoV of having a standard where the receiver has some control over the SBTs minted to their account.

I am talking about Permission based token minting and am currently working on the base contract. Will keep this thread active by posting about the updates.

---

**toledoroy** (2022-09-03):

I’d suggest that for the sake of composibility and standartization, which is IMHO what we should be aspiring to, we’d try to come up with a standard that’s as similar as possible to ERC1155 & 721.

Also, since both of these can have a non-transferable version, it would probably be best to just make modifications to them (something like ERC721_SOUL) that would still be compatible with other token.

We’ve had lots of success just blocking the transfer functions and adding a reverse mapping (tokenByAddress) which seems to be important for SBTs

You can take a look here: [ERC1155Tracker/Soul.sol at main · VirtualBlock/ERC1155Tracker · GitHub](https://github.com/VirtualBlock/ERC1155Tracker/blob/main/contracts/Soul.sol)

---

**TimDaub** (2022-09-04):

First post: What you are describing in steps 1.-5. is pretty much what we have described in EIP-4973 where both sender and receiver consent for a token to be minted. A reference implementation was made available by us: [GitHub - rugpullindex/ERC4973: Reference Implementation of EIP-4973 "Account-bound tokens"](https://github.com/rugpullindex/ERC4973)

