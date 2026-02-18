---
source: ethresearch
topic_id: 17445
title: Wallet Abstraction - is not Account Abstraction
author: wenzhenxiang
date: "2023-11-16"
category: Applications
tags: []
url: https://ethresear.ch/t/wallet-abstraction-is-not-account-abstraction/17445
views: 2337
likes: 8
posts_count: 11
---

# Wallet Abstraction - is not Account Abstraction

First of all, we have to understand that accounts and wallets have always been two things, but the initial development of blockchain made everyone think they are the same concept.

I think Wallet Abstraction include Asset management abstraction, payment abstraction, Identity abstraction.

In real life, a wallet is an item or tool used to store, manage, and conduct currency transactions. Its meaning includes the following aspects:

1. Currency Storage and Management: A wallet is where people store notes, coins, and other forms of currency. It allows individuals to carry a certain amount of cash with them at all times in order to cover daily expenses and purchase goods and services(like erc20).
2. Payment Instruments: Wallets typically include credit cards, debit cards, and other payment cards that enable individuals to make electronic payments. These cards can be used with POS terminals, ATM machines and other devices to facilitate shopping and cash withdrawals (like different token trasfer,approve).
3. Personal Items and Photos: Some people keep family photos, small keepsakes, or other personal items in their wallets to carry with them and display(like nft).
4. Identity Verification and Personal Information: Wallets usually contain important identity and personal information proof documents such as personal ID cards, driving licenses, membership cards, and health cards. These documents are used for identity verification and proof of personal identity when required(like did).

The same is true in WEB2，This is WeChat, with screenshots of its account, wallet UI.

The picture on the left is like the existing AA function, and the right is the wallet function, so the account abstraction and wallet abstraction should be completely **different** function and UI.

[![微信截图_20231117012107](https://ethresear.ch/uploads/default/optimized/2X/7/713f344f7c20c35d8059216ad27c2a8482fd8829_2_516x499.jpeg)微信截图_20231117012107944×914 130 KB](https://ethresear.ch/uploads/default/713f344f7c20c35d8059216ad27c2a8482fd8829)

The wallets and accounts we designed are all in the form of plug-ins, but the wallet mainly implements these functions.

**Asset Manage(include all ERC20 & ERC721)**

Assets, **Approve**, Legacies are genuinely managed by user wallets.

**Payment**

Abstracted payments, customized payment, blacklists

**Identification Info**

Verification of identity information and personal information.

We transfer all token management functions and transaction functions to the wallet plug-in itself，as plug-in, it can support more customized functions and improve security.

**It’s necessary to separate wallet abstraction and account abstraction. I’d like to hear everyone’s suggestions.**

## Replies

**MicahZoltu** (2023-11-17):

I have also been bothered by how crypto-currency wallet providers try to jam everything into their wallet.  For example, most now include on/off ramps, currency conversion tools, and some even include trading tools.

I want my wallet provider to focus *exclusively* on security of my private keys and protection of my assets.  I don’t want them to be distracted by adding a bunch of stuff that really should just be a separate web app into my wallet.

---

**wenzhenxiang** (2023-11-17):

I’m delighted to see your reply.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I have also been bothered by how crypto-currency wallet providers try to jam everything into their wallet. For example, most now include on/off ramps, currency conversion tools, and some even include trading tools.

Agree with this point, but my reason is that the functions you mentioned are entirely designated by a particular wallet, not control by users themselves. Moreover, these functions might not be decentralized; they could just be centralized services. If these features are optional and implemented based on a decentralized approach, it would be a different story.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I want my wallet provider to focus exclusively on security of my private keys and protection of my assets. I don’t want them to be distracted by adding a bunch of stuff that really should just be a separate web app into my wallet.

My view is actually the opposite. While I also want my wallet to focus on my assets, I wish the wallet could do more. Current trends in assets are becoming increasingly complex. You can refer to the final state of ERCs. Most ERCs are just continuously expanding the functions of ERC20 and ERC721. I want assets keep to be simple. Asset protection and management should be the responsibility of the wallet. In comparison, as a user, I need to trust all tokens and intermediary DApps.

whether a single asset should implement all functions or whether the user’s wallet should choose customized features.

Clearly, the latter is better.

---

**MicahZoltu** (2023-11-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/wenzhenxiang/48/9876_2.png) wenzhenxiang:

> I wish the wallet could do more

To me, this is similar to wanting your browser to do more.  Ideally your browser focuses all of its energy on allowing you to *safely* interact with any webpage/webapp on the internet.  Your browser spending its time, instead, on building apps that could have just been webpages takes away time that it could spend building a safer, faster, and generally better browsing experience of third party pages.

Rather than building asset management features into the wallet directly, the wallet should be focusing on how it can make interacting with third party websites and apps safer so the user doesn’t need to trust the application they are interacting with.

---

**wenzhenxiang** (2023-11-24):

Thank you for your response. Indeed, our use of Google Chrome also supports plugins, which don’t consume user time. My point about wallet and account abstraction essentially refers to the same smart contract address.

DeFi’s future narrative is about customized hooks, and the wallet’s future should offer customized hooks for user  transfers. and asset management. This allows for more convenient user management. For example, a user can choose to approve a single asset, approve all NFT assets under a smart contract, or approve all NFT assets.

Under a single smart contract, it’s possible to view and manage all of a user’s approve statuses, making management much more convenient.

---

**Zergity** (2023-12-01):

Exactly my point (for a long time).

Problem is, I can’t find a good web wallet dapp to view and send my tokens. zapper.xyz is the closest thing, but it does not let you send transaction. Beside, dapp webview in mobile wallets has horible experience, except for Brave, because it is a browser with a first-class-citizen wallet.

---

**MicahZoltu** (2023-12-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/zergity/48/5716_2.png) Zergity:

> Problem is, I can’t find a good web wallet dapp to view and send my tokens.

We built https://lunaria.dark.florist/ *specifically* because of this problem.  It is a privacy friendly static file hosted app that makes no external requests and has no backend server.  It uses your injected browser-wallet for all RPC requests.  You can check out its traffic in the browser’s networking tab and verify that it makes no external requests (other than fetching HTML, JS, CSS, and images for the site).

We are in the process of getting it deployed to IPFS right now, at which point you can access it entirely locally.

We also made https://nftsender.dark.florist with the same principals and purpose.  Caveat for this one is that we don’t fetch NFT images (because that would require external requests).

---

**Zergity** (2023-12-01):

That’s nice.

What do you think about listing all available token in the wallet? We do it all the time in DEX’s front-end using only etherscan API, and nothing else.

---

**MicahZoltu** (2023-12-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/zergity/48/5716_2.png) Zergity:

> What do you think about listing all available token in the wallet? We do it all the time in DEX’s front-end using only etherscan API, and nothing else.

The set of all tokens changes regularly, so we would have to go to an external source to fetch them and thus break our rule of “no external requests”, which is why we just provide some common tokens and let users manually add whatever else they want.  We have talked about adding support for tokenlists, with a UI that makes it very clear to the user that we will be fetching the list from an external source.  We would then only update when the user agreed again to hit an external site.

---

**Zergity** (2023-12-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> our rule of “no external requests”

Oh, I get it. So this is exactly why wallets should only do their essential jobs: keeping private keys and singing txs to preserve the user privacy.

But I still think a portfolio/asset/history manager dapp is needed for some accounts that doesn’t need to be private. For this, external requests to public 3rd party APIs are acceptable. Accounts that don’t want to be tracked, can stay away from these dapps.

---

**MicahZoltu** (2023-12-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/zergity/48/5716_2.png) Zergity:

> But I still think a portfolio/asset/history manager dapp is needed for some accounts that doesn’t need to be private.

One can certainly build privacy un-friendly (to varying degrees) portfolio management dapps!  Our team’s entire ethos though is maximally privacy preserving and censorship resistant.  We are building for those users who care about privacy.

