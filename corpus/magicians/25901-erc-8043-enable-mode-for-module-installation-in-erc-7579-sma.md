---
source: magicians
topic_id: 25901
title: "ERC-8043: Enable Mode for module installation in ERC-7579 Smart Accounts"
author: ernestognw
date: "2025-10-21"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8043-enable-mode-for-module-installation-in-erc-7579-smart-accounts/25901
views: 50
likes: 0
posts_count: 1
---

# ERC-8043: Enable Mode for module installation in ERC-7579 Smart Accounts

Hi everyone! ![:waving_hand:](https://ethereum-magicians.org/images/emoji/twitter/waving_hand.png?v=15)

I’m excited to share **ERC-8043**, a new standard that solves a major UX friction in ERC-7579 smart accounts.

## The Problem

Current ERC-7579 implementations require **two separate transactions** for module installation and usage. Users must:

1. Install a module (wait for confirmation)
2. Use the module in another transaction

This creates poor UX, especially for session keys and spending limits.

ERC-8043 introduces **“Enable Mode”** to install and use modules in a **single user operation** by installing the module during the validation phase of the user operation

### How it works:

![:wrench:](https://ethereum-magicians.org/images/emoji/twitter/wrench.png?v=15) **Magic Nonce**: `0x01` prefix in user operation nonce triggers enable mode

![:locked_with_key:](https://ethereum-magicians.org/images/emoji/twitter/locked_with_key.png?v=15) **EIP-712 Auth**: Secure module installation via typed signatures

![:package:](https://ethereum-magicians.org/images/emoji/twitter/package.png?v=15) **Structured Encoding**: Clean separation of installation and validation data

```solidity
// Signature format
abi.encode(
    uint256 moduleTypeId,
    address module,
    bytes initData,
    bytes installationSignature,  // EIP-712
    bytes userOpSignature        // Normal validation
)
```

### Validation Flow:

1. Detect 0x01 nonce prefix
2. Decode structured signature
3. Validate EIP-712 installation signature
4. Install module during validation phase
5. Continue normal user operation validation



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1253)














####


      `master` ← `ernestognw:erc/erc7579-enable-mode`




          opened 05:47PM - 13 Oct 25 UTC



          [![](https://avatars.githubusercontent.com/u/33379285?v=4)
            ernestognw](https://github.com/ernestognw)



          [+248
            -0](https://github.com/ethereum/ERCs/pull/1253/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/ERCs/pull/1253)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.
