---
source: magicians
topic_id: 14425
title: "EIP-7066: Lockable Extension for ERC721"
author: piyushchittara
date: "2023-05-25"
category: EIPs
tags: [erc, nft, token, evm, erc-721]
url: https://ethereum-magicians.org/t/eip-7066-lockable-extension-for-erc721/14425
views: 2987
likes: 18
posts_count: 19
---

# EIP-7066: Lockable Extension for ERC721

Keywords: Lockable, non-fungible tokens, NFTs, ERC-721

## EIP-7066

Various ERC721 Lockable implementations have been discussed but there is no standardization yet. This feature enables a multiverse of NFT liquidity options like peer-to-peer escrow-less rentals, loans, buy now pay later, staking, etc. Solana has a similar capability to lock approved assets and this proposal shall build the capability on the EVM ecosystem enabling more NFT use-cases.

[ERC-7066: Lockable Extension for ERC721](https://github.com/streamnft-tech/EIPs/blob/ERC721Lockable/EIPS/eip-7066.md)

[Pull Request #7066](https://github.com/ethereum/EIPs/pull/7066)

## Reference Lockable Discussions

- [EIP-5753] Filipp Makarov (@filmakarov), “ERC-5753: Lockable Extension for EIP-721 [DRAFT],” Ethereum Improvement Proposals, no. 5753, October 2022. [Online serial]. Available: ERC-5753: Lockable Extension for EIP-721.
- [EIP-5058] Tyler (@radiocaca), Alex (@gojazdev), John (@sfumato00), “ERC-5058: Lockable Non-Fungible Tokens [DRAFT],” Ethereum Improvement Proposals, no. 5058, April 2022. [Online serial]. Available: ERC-5058: Lockable Non-Fungible Tokens.

Please let us know what your thoughts are on this proposal and if our motivation seems useful! ![:crossed_fingers:](https://ethereum-magicians.org/images/emoji/twitter/crossed_fingers.png?v=15)

## Replies

**BoneyS** (2023-05-25):

Much required functionality. Been looking for such token capability for some time.

I would love to contribute to this proposal if possible.

---

**piyushchittara** (2023-05-25):

sure, let us know how we can make it better! ![:raised_hands:](https://ethereum-magicians.org/images/emoji/twitter/raised_hands.png?v=12)

---

**yugal03** (2023-05-25):

It can enable a plethora of use cases in the NFTFi space. Super excited to follow the progress and standard coming to light. Our game can make use of this proposal.

---

**tmoindustries** (2023-05-28):

we could use all of this functionality for our 721 contract. How can we help?

---

**stoicdev0** (2023-05-30):

Hey could you add the interface implementation on the specification? It is currently hard to read (unless you go to the reference implementation, which it’s great that you have!)

It feels similar to 5753 and 5058, what makes this one different?

---

**piyushchittara** (2023-05-30):

Thanks!!

We are pushing for this proposal as of now. You can help review our code and help us identify any more utility. We are building our rental and lending protocol as of now using ERC-7066. Existing upgradeable ERC-721 can also migrate to ERC-7066.

---

**piyushchittara** (2023-05-30):

Thanks for the input, shall work on that!!

Also for your query:

1. ERC-5058: Supports additional utility like time-bound locking, which we feel is great idea but can be achieved without the specified functionality. Locking and Unlocking can be based on any conditions (for e.g: repayment, expiry). Therefore time-bound unlocks a relatively specific use-case that can be achieved via smart-contracts themselves without that being a part of the token contract.
2. ERC-5753: We are proposing a separation of rights via locker and approver. Both users can lock an asset but approvers can unlock and withdraw tokens (opening up opportunities like: renting, lending, bnpl etc), and lockers lack the rights to revoke token yet can lock and unlock if required (opening up opportunities like: account-bound NFTs).

Also both EIPs are in draft and not accepted yet, therefore we are trying to push this functionality via our proposal (which we have tried to simplify and optimize more on existing proposals). Hope that answers your query! ![:raised_hands:](https://ethereum-magicians.org/images/emoji/twitter/raised_hands.png?v=12)

---

**stoicdev0** (2023-06-01):

Thanks for adding the interface there, much easier to check.

Suggestion here:

```auto
/**
     * @dev Lock the token `id` if msg.sender is approved
     */
    function lockApproved(uint256 id) external;

    /**
     * @dev Unlock the token `id` if msg.sender is approved
     */
    function unlockApproved(uint256 id) external;
```

Are these actually setters? The name suggests to me that they are getters, but the dev comment suggest the opposite. If they are getters, you should receive the address you want to check so it does not need a signer.

---

**piyushchittara** (2023-06-02):

hello [@stoicdev0](/u/stoicdev0) !

these are setters, for user with approval to lock/unlock token-id. Should I rename these functions to something else?

---

**stoicdev0** (2023-06-02):

I did not expect two `lock` and `unlock` methods, why not merge them?  so `lock` should lock if sender is locker or approved, similarly `unlock`. WDYT?

---

**piyushchittara** (2023-06-07):

[@stoicdev0](/u/stoicdev0) I chose abstraction over here, considering the possibility locker might call ‘lock’ by mistake when the asset is already locked, this shall unlock the token and provide all rights to user again. But this implementation shall save us some gas. Let me know if you think this abstraction is not required ![:raised_hands:](https://ethereum-magicians.org/images/emoji/twitter/raised_hands.png?v=12)

Also, we shall be pushing some major functionality and optimizations to the EIP in next couple of days ![:crossed_fingers:](https://ethereum-magicians.org/images/emoji/twitter/crossed_fingers.png?v=12)

---

**stoicdev0** (2023-06-08):

I did not mean to join `lock` and `unlock`, but `lock`+`lockApproved` and `unlock`+`unlockApproved`.

Looking forward to the new functionality.

---

**piyushchittara** (2023-06-08):

[@stoicdev0](/u/stoicdev0) agree with you, locker/approver can be internally checked on lock/unlock. If a user is locker and approved both, approved shall take priority. I shall think more and implement this.

In new update, we have created: transferAndLock transferAndApprove

so that for rental like usecases:

1. transferAndApprove → transfer and setApproval to self/contract
2. lock → lock the asset

Problem in previous implementation was, after transfer rental contract will need approval but that will need new onwer to approve hence creating a scenario, renter hold asset without lock and approval provided to actual owner. This implementation shall take care of that, let me know your thoughts ![:raised_hands:](https://ethereum-magicians.org/images/emoji/twitter/raised_hands.png?v=12)

---

**stoicdev0** (2023-06-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/piyushchittara/48/9568_2.png) piyushchittara:

> Problem in previous implementation was, after transfer rental contract will need approval but that will need new onwer to approve hence creating a scenario, renter hold asset without lock and approval provided to actual owner. This implementation shall take care of that, let me know your thoughts

Really nice catch! I agree it’s important.

---

**piyushchittara** (2023-06-09):

[@stoicdev0](/u/stoicdev0) Have updated the code to support lock, unlock and transferAndLock. All delegations based on locker and approve are taken care internally. Thanks for the feeback, code is much simpler to understand and integrate.

---

**piyushchittara** (2023-06-13):

Major updates made on EIP, removed redundancies, optimized approach and enabled transferWithLock. Please check it out [@BoneyS](/u/boneys) [@tmoindustries](/u/tmoindustries) [@stoicdev0](/u/stoicdev0) ![:raised_hands:](https://ethereum-magicians.org/images/emoji/twitter/raised_hands.png?v=12)

---

**piyushchittara** (2023-06-16):

I am thinking to rename

```auto
transferAndLock(address from, address to, uint256 tokenId, bool setApprove)
```

to

```auto
safeTransferFrom(address from, address to, uint256 tokenId, bool lock, bool setApprove)
```

so locking and approval are optional after the transfer, and function signature remains similar to what everyone is already familiar with. Any thoughts on this [@stoicdev0](/u/stoicdev0)?

---

**xinbenlv** (2023-09-08):

Hi authors, thank you for your proposal.

Apparently, locking an NFT is an important use-case. It turns out it’s interesting enough that there are 3 related / competing ERCs!

- ERC-5753
- ERC-5058 - link fixed
- ERC-7066

We at [#allercdevs](https://github.com/ercref/AllERCDevs) is a community for bringing ERC Authors Builders to advocate for adoption and/or solicit technical feedback. We meetup bi-weekly and the timezone rotates between Thursday UTC1500 and Tuesday UTC2300, such as

- Thursday, Sep 21, 2023 15:00 UTC
- Tuesday, Oct 3, 2023 23:00 UTC

I wonder if we have a session to discuss lockable NFTs would you be interested in joining the discussion?

Email me if you are interested zzn+allercdevs@zzn.im

