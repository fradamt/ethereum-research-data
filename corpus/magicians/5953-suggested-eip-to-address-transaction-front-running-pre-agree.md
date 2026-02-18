---
source: magicians
topic_id: 5953
title: "Suggested EIP to address transaction front running: Pre-Agreed Secured Transactions"
author: JosiahR
date: "2021-04-10"
category: EIPs
tags: [defi, front-running]
url: https://ethereum-magicians.org/t/suggested-eip-to-address-transaction-front-running-pre-agreed-secured-transactions/5953
views: 675
likes: 1
posts_count: 1
---

# Suggested EIP to address transaction front running: Pre-Agreed Secured Transactions

EIP Details:

Users can generate a special transaction that includes the following: hash of secured transaction, gas limits for it

Once mined the secured transaction can be sent to blockchain. The consensus protocol mandates they must be processed Before normal transactions, and in the order the Pre-Agreed transactions were executed. If there is still room for normal transactions after ALL secured transactions have been processed in the correct order, they may be included as normal.
