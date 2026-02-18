---
source: magicians
topic_id: 13654
title: "EIP-6821: Support ENS Name for Web3 URL"
author: qizhou
date: "2023-04-03"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/eip-6821-support-ens-name-for-web3-url/13654
views: 1801
likes: 7
posts_count: 6
---

# EIP-6821: Support ENS Name for Web3 URL

---

## eip: 6821
title: Support ENS Name for Web3 URL
description: A mapping from an ENS name to the contract address in web3://
author: Qi Zhou (), Qiang Zhu ()
discussions-to:here
status: Draft
type: Standards Track
category: ERC
created: 2023-04-02
requires: 137, 4804



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/6821)














####


      `master` ← `qizhou:patch-16`




          opened 05:43AM - 03 Apr 23 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/e/ec489df73b8873547715c8a2f21986ca2b83d33c.jpeg)
            qizhou](https://github.com/qizhou)



          [+42
            -0](https://github.com/ethereum/EIPs/pull/6821/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/EIPs/pull/6821)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

## Replies

**fewwwww** (2023-04-03):

One example given in EIP-4804 is `web3://vitalikblog.eth:5/`. Does this example require the EIP in this post?

---

**qizhou** (2023-04-03):

The resolving part will depend on this EIP.  However, after discussing with EIP editors on EIP-4804, we agree to defer the detailed resolving part to another EIP (i.e., for ENS, EIP-6821).

---

**SamWilsn** (2023-04-04):

Instead of `web3` for the key name, what about something like `contentscript` or `contentcontract` to go with the already existing `contenthash` from [ERC-1577](https://eips.ethereum.org/EIPS/eip-1577)?

---

**qizhou** (2023-04-04):

Looks like a good idea.  Let me check with others in the circle ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**qizhou** (2023-04-05):

Thanks for the comment.  After discussing with other community members, we agree to replace the `web3` text record with `contentcontract`.  The EIP is also updated accordingly.  Pleaes check.

