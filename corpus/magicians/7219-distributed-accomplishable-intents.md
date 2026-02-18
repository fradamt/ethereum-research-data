---
source: magicians
topic_id: 7219
title: Distributed Accomplishable Intents
author: michaeldunwort1
date: "2021-10-06"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/distributed-accomplishable-intents/7219
views: 609
likes: 0
posts_count: 1
---

# Distributed Accomplishable Intents

I’m a new user so limited on the content/links I can post, but you can find the unedited version [here](https://github.com/MikeD123/Stuff/tree/master/Distributed%20Accomplishable%20Intents)

###  Distributed Accomplishable Intents

#### tl;dr - We’re should aim to turn the address bar into a search engine. Encoding the function calls and search terms for desired outcome into a natural language system.

![examplesearch](https://ethereum-magicians.org/uploads/default/original/2X/7/7273cb536076b39c8358eb68cb5c05d6a525d163.gif)

Can I borrow your brain for a second? I need you to try and wipe the idea of the address bar as a way to send and receive assets. Pasting in the janky addresses. Going through triple checking a bunch a characters to make sure they’re correct, then finally pulling the trigger and clicking confirm.

In fintech these are referred to as “payment intents” where we have a finite path that user can go down to checkout. Sort of how you present different fields based on what payment method you choose, it’s like a pre-defined path to collect the necessary information as seamlessly as possible to complete your checkout.

An example for crypto would be with MakerDAO. “Deposit collateral and generate DAI”. Because it’s a common use-case, a pre-defined intent of users opening CDP’s it means that we can build a one click behaviour.

It’s a common theme, and will only trend more and more toward repeated value adding intents.

Think of it more as a way to “communicate” your goals and intentions of your payment to a distributed system.

Example Language

- “Deposit.ToSavings.eth” (this deposits into compound, and returns CUSDC)
- “dai.toBitcoin.eth” (converts DAI to WBTC as outlined in the example above)

If you are looking for a simple mental model think of it this way…

New users get something like an Amazon 1 click checkout for Ethereum smart contract interactions.

New users get a familiar “Google” like interface UX/UI flow.
