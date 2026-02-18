---
source: magicians
topic_id: 9201
title: "EIP-5058: ERC-721 Lockable Standard"
author: TylerMeta
date: "2022-05-08"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-5058-erc-721-lockable-standard/9201
views: 3478
likes: 0
posts_count: 7
---

# EIP-5058: ERC-721 Lockable Standard

Keywords: Lockable, non-fungible tokens, NFTs,  ERC-721

- EIP-5058 DRAFT: EIP-5058:Lockable ERC-721 Standard by radiocaca · Pull Request #5058 · ethereum/EIPs · GitHub

This standard makes NFTs more suitable for NFTFi, such as locking, staking, lending, crowdfunding, etc.

## Replies

**TimDaub** (2022-09-29):

Hi,

[EIP-5192: Minimal Soulbound NFTs](https://eips.ethereum.org/EIPS/eip-5192) is not final and features similar functionality albeit without an approval function for locking.

---

**AurelianoDiaz** (2022-10-25):

How can I write the smart contract code for ERC 721 implementing EIP 5058?

Is there any source code?

---

**TimDaub** (2023-02-06):

IMO this almost the perfect SBT standard to date if it was slimmed down a bit (it is potentially already better than my attempts EIP-5192 and EIP-4973) The name “Lockable tokens” is also very good. Here’s what would make it golden:

- Focus on Lock and lock approval
- remove the expiry feature as it doesn’t directly map to EIP721 transfer+transferapprove (could be optional)
- make boundNFT an optional extension
- clearly state in the Specification section that when the function locked returns true, what the other functions then have to return (e.g. that transfers have to throw etc). Allow no undefined behavior in the spec (here’s how that could look: ERC5192/ERC5192.t.sol at main · attestate/ERC5192 · GitHub (I didn’t do a great job in EIP-5192 admittedly).

Then in security section, I’d also add:

- If a token implements EIP-5058 and then there exists a vault contract that e.g. allows to do a trade of: “I lock token, you give me 1 ether. I unlock token when you give me 1 ether back”, then the vault contract must allow listing the EIP-5058 token as purely relying on the interface of a contract isn’t prove that the contract correctly implemented EIP-5058. But IMO this is already fairly standard with EIP-20 etc., so I think it’s not a deal breaker with EIP-5058

---

**sullof** (2023-02-18):

I like this interface. I don’t like, however, when we — the development community — is forced to choose between similar interfaces. So, I would suggest a change.

If instead of

```auto
interface IERC5058 {
  event Locked(address indexed operator, address indexed from, uint256 indexed tokenId, uint256 expired);
  event Unlocked(address indexed operator, address indexed from, uint256 indexed tokenId);
  event LockApproval(address indexed owner, address indexed approved, uint256 indexed tokenId);
  event LockApprovalForAll(address indexed owner, address indexed operator, bool approved);
  function lockerOf(uint256 tokenId) external view returns (address locker);
  function lock(uint256 tokenId, uint256 expired) external;
  function unlock(uint256 tokenId) external;
  function lockApprove(address to, uint256 tokenId) external;
  function setLockApprovalForAll(address operator, bool approved) external;
  function getLockApproved(uint256 tokenId) external view returns (address operator);
  function isLockApprovedForAll(address owner, address operator) external view returns (bool);
  function isLocked(uint256 tokenId) external view returns (bool);
  function lockExpiredTime(uint256 tokenId) external view returns (uint256);
}
```

You extend [ERC5192](https://ethereum-magicians.org/t/final-eip-5192-minimal-soulbound-nfts/9814) — which is in the final stage and will most likely be used in standard contracts — and change the code as

```auto
interface IERC5192 {
  event Locked(address indexed operator, address indexed from, uint256 indexed tokenId, uint256 expired);
  event Unlocked(address indexed operator, address indexed from, uint256 indexed tokenId);
  function locked(uint256 tokenId) external view returns (bool);
}

interface IERC5058 is IERC5192 {
  event LockApproval(address indexed owner, address indexed approved, uint256 indexed tokenId);
  event LockApprovalForAll(address indexed owner, address indexed operator, bool approved);
  function lockerOf(uint256 tokenId) external view returns (address locker);
  function lock(uint256 tokenId, uint256 expired) external;
  function unlock(uint256 tokenId) external;
  function lockApprove(address to, uint256 tokenId) external;
  function setLockApprovalForAll(address operator, bool approved) external;
  function getLockApproved(uint256 tokenId) external view returns (address operator);
  function isLockApprovedForAll(address owner, address operator) external view returns (bool);
  function lockExpiredTime(uint256 tokenId) external view returns (uint256);
}
```

The only change is that the function `isLocked` is renamed `locked`. That will of course change the interfaceId, but since it is in a draft stage, it would make a lot of sense and would also facilitate the approval of EIP 5058.

---

**tbergmueller** (2023-04-30):

Although still in draft, I already referenced this (among others) as a possible extension to our proposed [Asset-bound NFT](https://ethereum-magicians.org/t/draft-erc-xxxx-asset-bound-non-fungible-tokens/14056) for DeFi applications.

A feedback we got received from DeFi when discussing our EIP was that multiple accounts should be able to lock a tokenId, and only if all locks are removed, the token can be transferred. We thought about proposing such an interface ourselves, but figured it would be better to enable extending our Asset-bound NFTs with other ERCs such as yours.

- Would locking by multiple accounts be be worth considering?
- If you have time, could you please confirm this could indeed be used to extend our Asset-bound NFT?
- What are the plans to move this further?

---

**xinbenlv** (2023-09-08):

Hi authors, thank you for your proposal.

Apparently, locking an NFT is an important use-case. It turns out it’s interesting enough that there are 3 related / competing ERCs!

- ERC-5753
- ERC-5058
- ERC-7066

We at [#allercdevs](https://github.com/ercref/AllERCDevs) is a community for bringing ERC Authors Builders to advocate for adoption and/or solicit technical feedback. We meetup bi-weekly and the timezone rotates between Thursday UTC1500 and Tuesday UTC2300, such as

- Thursday, Sep 21, 2023 15:00 UTC
- Tuesday, Oct 3, 2023 23:00 UTC

I wonder if we have a session to discuss lockable NFTs would you be interested in joining the discussion?

Email me if you are interested zzn+allercdevs@zzn.im

