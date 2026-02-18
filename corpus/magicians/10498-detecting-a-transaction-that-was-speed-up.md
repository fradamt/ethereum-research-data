---
source: magicians
topic_id: 10498
title: Detecting a transaction that was speed up
author: ligi
date: "2022-08-23"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/detecting-a-transaction-that-was-speed-up/10498
views: 577
likes: 1
posts_count: 1
---

# Detecting a transaction that was speed up

What is the best practice to handle the following case:

- an app initiates a transaction and gets the tx hash.
- on the backend it waits for this tx hash to confirm

now in the case the user speeds up a transaction - the tx hash changes and step 2 will never finish.

What is now the best practice to detect the altered transaction? Ideally the wallet would tell the dapp about the alteration - but AFAIK there is no such mechanism (yet). Otherwise what is a good way/best practice here? Searching through all transactions to find the replacement tx sounds like a lot of waste.

Maybe I am missing something here - or should we bootstrap a mechanism that the wallet can tell the dapp about alterations?
