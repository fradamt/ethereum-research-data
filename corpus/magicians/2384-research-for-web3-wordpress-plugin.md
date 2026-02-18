---
source: magicians
topic_id: 2384
title: Research for Web3 Wordpress Plugin
author: markoprljic
date: "2019-01-10"
category: Magicians > Primordial Soup
tags: [research, web3, plugin, wordpress]
url: https://ethereum-magicians.org/t/research-for-web3-wordpress-plugin/2384
views: 2642
likes: 0
posts_count: 3
---

# Research for Web3 Wordpress Plugin

Hi all!

A friend of mine had the idea of creating a Wordpress plugin for Web3. Specifically, we’re looking to build a  **Wordpress Plugin to create and manage front end around blockchain functionality** .

Before stepping into it we would like to do as much research and create an outline of all possible options, features, functions etc. Best way to do that is to start with use cases and scenarios, so I’m calling all who do any work in Web3 space to share their experience, needs, stories and contribute.

For this specific purpose I created a Github project https://github.com/markoprljic/Web3-WP-Plugin We’re using this issue for research https://github.com/markoprljic/Web3-WP-Plugin/issues/1 where you can post your comments, or if you don’t have a Github account you can post in this topic directly. We’ll be using this repo to build out the plugin eventually.

Looking forward to hear your ideas!

Thanks.

## Replies

**jpitts** (2019-01-11):

Some questions come to mind:

1. Is the intention of the plugin to provide Wordpress instance with access to the blockchain, or is it only for Wordpress deployers to integrate access in various ways for the users of that Wordpress instance?

Wordpress being able to have a key and live access to contracts on the server side would be interesting for website devs, and of course risky if there is a lot of fin and data value in that key & related contracts.

1. Would you leave user key management to a browser extension like Metamask, and have the Wordpress plugin manage certain useful traditional web integrations e.g. login w/ Ethereum account? Or are you going to store keys using the browser store?

You’re probably well aware of it, but def. pay heed to [@tay](/u/tay)’s warnings about keys etc. stored in the various methods available to browsers.



      [twitter.com](https://twitter.com/MyCrypto/status/1057653449473421314)





####

[@MyCrypto](https://twitter.com/MyCrypto/status/1057653449473421314)

  This is a call to action: stop letting people use these methods in the browser!!! #devcon

  https://twitter.com/MyCrypto/status/1057653449473421314

---

**markoprljic** (2019-01-14):

Hi Jamie, thanks for your feedback and sorry for my late reply.

Here are my answers:

1. The intention is to provide any kind of blockchain functionality to WP deployers (users who will install a theme and plugin). I guess the answer is yes to: “Wordpress deployers to integrate access in various ways for the users of that Wordpress instance”
2. Big NO to private keys in WP (or elsewhere). MM to handle that part.

The idea came from my friend Gendrey from https://theflightplan.io/ They have an UI where you paste your smart contract and it pulls out all attributes needed for you to manage/adjust your dApp settings and publish it (testnet).

We were also testing https://oneclickdapp.com/ just to see how it works. Although nice, it’s missing a lot of functionality and didn’t find it very useful.

We also had the idea of the possibility to create the actual smart contract from the interface (rather than code), something like drag&drop website builder but for smart contracts. Maybe there’s a such thing already and I missed it.

To go back to WP plugin, all said above would probably translate into something manageable from WP. The question is, how many people would use this, or is there even a need for it?

I think if not right now, there will be a need for it and why not start building it now?

Let me know if that makes sense to you.

Thanks.

