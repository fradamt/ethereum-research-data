---
source: magicians
topic_id: 20245
title: "ERC-7720: Deferred Token Transfer"
author: bizliaoyuan
date: "2024-06-08"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7720-deferred-token-transfer/20245
views: 699
likes: 0
posts_count: 1
---

# ERC-7720: Deferred Token Transfer

## Abstract

The standard enables users to deposit ERC-20 tokens that can be withdrawn by a specified beneficiary at a future timestamp. Each deposit is assigned a unique ID and includes details such as the beneficiary, token type, amount, timestamp, and withdrawal status.

### Motivation

Sometimes, we need deferred payments in various scenarios, such as vesting schedules, escrow services, or timed rewards. By providing a secure and reliable mechanism for time-locked token transfers, this contract ensures that tokens are transferred only after a specified timestamp is reached. This facilitates structured and delayed payments, adding an extra layer of security and predictability to token transfers. This mechanism is particularly useful for situations where payments need to be conditional on the passage of time.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/465)














####


      `master` ← `chenly:Deferred-Token-Transfer`




          opened 06:56PM - 08 Jun 24 UTC



          [![](https://avatars.githubusercontent.com/u/13716?v=4)
            chenly](https://github.com/chenly)



          [+256
            -0](https://github.com/ethereum/ERCs/pull/465/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/ERCs/pull/465)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.
