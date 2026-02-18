---
source: magicians
topic_id: 8822
title: "EIP-4972: Name Owned Account"
author: qizhou
date: "2022-04-04"
category: EIPs
tags: [nft, erc-721, social-media]
url: https://ethereum-magicians.org/t/eip-4972-name-owned-account/8822
views: 3100
likes: 6
posts_count: 11
---

# EIP-4972: Name Owned Account

---

## eip: 4972
title: Name Owned Account
description: Name Owned Account for Social Identity
author: Qi Zhou ()
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2022-04-04
requires: 20, 721

## Abstract

This ERC proposes a new type of account - name-owned account (NOA) that is controlled by the owner of the name besides existing externally-owned account (EOA) and contract account (CA). With the new account type, users will be able to transfer/receive tokens using the name-derived address directly instead of the address of the name owner. A NOA can be as a social identity with all states on-chain even under 3rd-party or self custody. It also simplifies porting the social identity from one custody to another.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/4972)














####


      `master` ← `qizhou:qizhou-noa`




          opened 06:35PM - 04 Apr 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/e/ec489df73b8873547715c8a2f21986ca2b83d33c.jpeg)
            qizhou](https://github.com/qizhou)



          [+148
            -0](https://github.com/ethereum/EIPs/pull/4972/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/EIPs/pull/4972)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

## Replies

**dongshu2013** (2022-04-05):

Can you update the code link? The link is not working.

---

**qizhou** (2022-04-05):

Just updated accordingly.

---

**jaglinux** (2022-04-11):

Does this conflict with ENS ?

---

**dongshu2013** (2022-04-11):

No, it doesn’t conflict with ENS. The idea is actually inspired by ENS. ENS can serve as the name service to prove the name ownership.

---

**SamWilsn** (2022-04-14):

Should this standard also include an [ERC-165](https://eips.ethereum.org/EIPS/eip-165) implementation?

---

**qizhou** (2022-04-14):

Yes, will update accordingly.

---

**Pandapip1** (2022-07-21):

I have one quick question: who pays for the gas to update the operators of an NOA?

---

**qizhou** (2022-07-25):

Thanks for the question.  Who pays for the gas depends on the application scenario.  One scenario is when a user wants to transfer all the assets from the platform-custodian operator to the self-custodian operator by sending an operator-transfer-request on the platform.  As a result, the platform will change the operator upon the user’s request and pay the gas fee to update the operator. (Note that the platform may charge the user’s gas fee as CEX does)

Another scenario is when the NOA is self-custodied and the user wants to sell the assets to a platform. by batch-transferring the assets owned by the NOA to the platform’s operator.  This can be done by sending a tx of changing operator at the cost of the user.

Hope this could explain your question.  Please let us know if you have further questions!

---

**dongshu2013** (2023-03-30):

I proposed a simplified version of EIP-4972 at [Update EIP-4972: Move to Draft by dongshu2013 · Pull Request #6804 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6804). Instead of creating a new account type whose namespace is not overlapped with existing CA/EOA, the new version assumes NOA is CA to avoid compatibility problems brought by the original proposal.

The new version extends ERC-137 and assign each ENS name a ready-to-use smart contract account, which we believe will help the smart contract account adoption.

With EIP-4972, we expand the “name” to a more comprehensive smart account so it can hold its own contexts and state. When transferring names, you are also transferring the account along with its state.

---

**dongshu2013** (2023-04-05):

EIP-6551 just proposed a similar idea for ERC-721 [ERC-6551: Non-fungible Token Bound Accounts - #40 by dongshu2013](https://ethereum-magicians.org/t/erc-6551-non-fungible-token-bound-accounts/13030/40).

