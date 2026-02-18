---
source: magicians
topic_id: 12182
title: "EIP-6268: UNTransferability Indicator for EIP-1155"
author: yuki-js
date: "2022-12-17"
category: EIPs
tags: [erc1155, sbt]
url: https://ethereum-magicians.org/t/eip-6268-untransferability-indicator-for-eip-1155/12182
views: 2898
likes: 3
posts_count: 9
---

# EIP-6268: UNTransferability Indicator for EIP-1155

I submitted an EIP, that is inspired by EIP-5172 and have a similar simple interface.

This is something like EIP-5172 for EIP-1155.



      [github.com](https://github.com/AokiApp/EIPs/blob/eip-draft-unti/EIPS/eip-6268.md)





####



```md
---
eip: 6268
title: Untransferability Indicator for EIP-1155
description: An extension of EIP-1155 for indicating the transferability of the token.
author: Yuki Aoki (@yuki-js)
discussions-to: https://ethereum-magicians.org/t/sbt-implemented-in-erc1155/12182
status: Draft
type: Standards Track
category: ERC
created: 2022-01-06
requires: 1155
---

## Abstract

The following standard is an extension of [EIP-1155](./eip-1155.md). It introduces the interface for indicating whether the token is transferable or not, without regard to non-fungibility, using the feature detection functionality of [EIP-165](./eip-165.md).

## Motivation

We propose the introduction of the UNTransferability Indicator, a universal indicator that demonstrates untransferability without regard to non-fungibility. This will enable the use of Soulbound Tokens (SBT), which are untransferable and fungible/non-fungible entities, to associate items with an account, user-related information, memories, and event attendance records, in a universal manner. The [EIP-5192](./eip-5192.md) specification was invented for this purpose, but SBT in [EIP-5192](./eip-5192.md) is non-fungible and has a tokenId, allowing them to be distinguished from each other using the tokenId. However, for example, in the case of event attendance records, it is not necessary to distinguish between those who attended the same event using the tokenId, and all participants should have the same indistinguishable entity. Rather, the existence of the tokenId creates discriminability.
```

  This file has been truncated. [show original](https://github.com/AokiApp/EIPs/blob/eip-draft-unti/EIPS/eip-6268.md)

## Replies

**yuki-js** (2023-01-06):

I made a PR.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/6268)














####


      `master` ← `AokiApp:eip-draft-unti`




          opened 12:25PM - 06 Jan 23 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/5/5db9ef47755442147abe34e3f0b362871f84eac9.png)
            yuki-js](https://github.com/yuki-js)



          [+88
            -0](https://github.com/ethereum/EIPs/pull/6268/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/EIPs/pull/6268)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

---

**Pandapip1** (2023-01-06):

Make sure to use the latest eip-template!

---

**yuki-js** (2023-01-06):

Thank you for pointing out. I’ve corrected the problem. If the problem is still there, please let me know.

---

**tinom9** (2023-01-08):

Thoughts on renaming `LockedSingle` and `UnlockedSingle` to `Locked` and `Unlocked` for backwards EIP-5192 compatibility?

---

**yuki-js** (2023-01-08):

It is inspired by EIP-5192 but it’s for EIP-1155. I thought the function/events naming convention should be conform to that of EIP-1155. It would be better to change it if other existing contracts use the name.

---

**TimDaub** (2023-02-06):

This looks really good! ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

A minor comment on the title: I think the best possible title for all these standards (after having one year of time to think about this) is “Lockable NFTs.” It is because “Lockable” allows all the following states:

- permanently locked (Soulbound or account bound or non-transferable)
- temporarily or conditionally locked/transferrable (loaned)
- permanently transferrable

Lockable has the added benefit that it hasn’t been social-media captured by some special interest group wanting to push their solution for X (as has been done with SBTs and NTTs). People have genuinely no understanding yet of lockable tokens. But already the name implies: “This thing is lockable, but it also means that it is potentially unlockable.” It can, however, also mean: “this thing is permanently lockable.”

Then, let me please explain a different feature that you may want to consider that has been implemented in: [ERC-5058: Lockable Non-Fungible Tokens](https://eips.ethereum.org/EIPS/eip-5058) approving locks.

See, with transfers on EIP-20 and EIP-721 tokens, we can approve a contract or another account to make a transfer on our behalf. And the nice thing about it is that this isn’t hard coded with respect to the approved account. And it translates into e.g. Uniswap contracts managing my EIP20 tokens for trading (which is a very nice feature).

Now, with EIP-5192, I had intended to build something like that by allowing the users to implement the locked function themselves and to revert to transfer as they saw fit. But then, this forces hard coding of the values in the respective implementation. So what [ERC-5058: Lockable Non-Fungible Tokens](https://eips.ethereum.org/EIPS/eip-5058), by allowing to approve an operator to manage the lock function, is much better because it generalizes the lock operator instead of the developer hard coding it.

I’d consider implementing this [@yuki-js](/u/yuki-js) unless you see very big drawbacks to this.

---

**LI-YONG-QI** (2023-04-14):

Hello, I think that eip is good, I’ve been considering eip similar recently

But I found “created” date field is weird, Is that 2022?

---

**yuki-js** (2023-04-15):

Thank you for pointing out. Yes, indeed this is incorrect. I made a mistake because it spans 2022 and 2023. It’s a subtle mistake, but to avoid confusion, I will create a pull request later.

