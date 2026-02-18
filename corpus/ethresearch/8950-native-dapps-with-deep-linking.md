---
source: ethresearch
topic_id: 8950
title: Native Dapps with Deep Linking
author: edsonayllon
date: "2021-03-18"
category: Applications
tags: []
url: https://ethresear.ch/t/native-dapps-with-deep-linking/8950
views: 2294
likes: 3
posts_count: 2
---

# Native Dapps with Deep Linking

Currently, Dapps via phone is done with wallets that have an embedded browser. While we are now able to interact with Dapps on mobile, this solution means there are still no native Dapps. This applies to both PC/Mac and iOS/Android.

Native Dapps should be possible as long as an app can communicate with a wallet. One possible way to do this is with deep linking.

- Linking · React Native

> For example, when you get a Magic Link email from Slack, the Launch Slack button is an anchor tag with an href that looks something like: slack://secret/magic-login/other-secret.

It’s a little different than how wallets are done now, but theoretically, you should be able to call `ethereum://web3/eth/accounts`, etc.

A full spec and implementation should allow for downloadable Dapps. I know deep linking is compatible with at least React Native and ElectronJS.

I’m not too sure how to move this forward, but am willing to collaborate with others, or have someone else move this idea forward. I assume this would probably involve an update to both Wallets and dev tools (web3.js library).

## Replies

**lekssays** (2021-03-29):

I thought about this a while ago when I struggled to make a dApp for Android. It’s a promising idea.

The workaround that is used now is to use linking to MetaMask or any other wallet (this is available on react, Kotlin, java, etc.), but the issue remains that the app does not have any update on the transactions (e.g. confirmed, failed), so listening to transactions on the expected payment address is still (up to my knowledge) the way to do it.

This small introduction reveals one main issue: **There is no callback from wallets after processing a transaction, so dApps will never know what the status of the transaction unless they listen to the network for new transaction on a specific address.**

I believe that some solutions to this problem would be to develop a lightweight wallet integration/library for the dApps (so linking will no longer needed) since the account handling will be inside the Native dApp or Wallet providers should work on features to return a callback after processing a transaction.

As a last note, I am open to discussion/collaboration in this topic as well.

