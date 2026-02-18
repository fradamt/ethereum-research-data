---
source: magicians
topic_id: 1282
title: "MUST READ: Leaning from RSS UX Failures"
author: Ethernian
date: "2018-09-09"
category: Web > User Experience
tags: []
url: https://ethereum-magicians.org/t/must-read-leaning-from-rss-ux-failures/1282
views: 1509
likes: 13
posts_count: 8
---

# MUST READ: Leaning from RSS UX Failures

A must read for UX designers in crypto-space.

[Learning from RSS Fauilure](https://twitter.com/varun_mathur/status/1038107664868208640)

Citate:

> RSS world pre-iPhone:
>
>
> Millions of websites published a feed (“tokens”)
> Dozens of feed readers popped up, optimizing on UI/UX & scalability (“wallets”)
> Millions of websites displayed these feed reader buttons (persistent free marketing for free products)
>
>
> Users didn’t adopt.

What can we do better?

Thoughts are welcome.

## Replies

**danfinlay** (2018-09-09):

Great thread, I think it’s entirely right, except in the general belief that this isn’t being worked on today in crypto.

There are a ton of teams working on exactly these problems, and I think most of us know that it won’t last if it isn’t usable by most people. We’re all racing to get there.

The major pain points I currently think of for MetaMask are these

- The extension installation
- Seed phrase backup
- Gas/eth transaction fees & wait time
- Transaction comprehensibility [1] [2]
- Developer/Vendor experience
- Combatting constant phishing attacks
- Currently only Eth/EVM blockchains.

We’re actively chipping at every one of them, and I do believe that we are slowly approaching an adoption process that has as little friction as anything else, it just takes a lot of time and energy, and in the meanwhile, everyone’s a critic, everyone’s got a lot of great ideas, and some of them have skills too, and they’re going to try to just do better than the current efforts.

The future is bright, especially because we have so many people thinking so deeply about how we could best go about making “reimagining society” an accessible concept.

---

**dpyro** (2018-09-12):

Good read. I think the more fundamental problem with RSS and really all new technology seeking adoption is that it did not offer **enough** of an improvement over the current experience. In contrast, news aggregation sites like Slashdot and Reddit or even something like a chan board allow linking to arbitrary urls and discussion. By curating communities of people with similar interests you offer a more comprehensive experience that could not be replaced by simply visiting web pages on your own.

---

**dpyro** (2018-09-12):

> The major pain points I currently think of for MetaMask are these
>
>
> The extension installation

Maybe it should be treated as a plugin instead of just as an extension?

> Seed phrase backup

I think you should be able to delegate storing this seed to an OAuth 2.0 provider for low/no value/dev accounts. If you don’t have even minimal functionality within 5 seconds of clicking on the extension you are already losing user interest.

> Gas/eth transaction fees & wait time

Users should not have to deal with handling maximum gas.

One major pain point I had when I was a newb was nonce management. I had sent out a transaction that was one wei below the current minimum accepted gas price. It got stuck in the mempool but didn’t get mined. This blocked all future transactions and it wasn’t obvious to me at all why this was happening since my future transactions had much higher gas pricing. I eventually solved the problem using MyEtherWallet with its cancel transaction feature but before that I thought my account got bugged and I was going to have to create a new one.

Maybe there should be some kind of simple queue visualizer for your transactions? Where it is in line compared to the rest of the mempool, for example.

> Combatting constant phishing attacks

Maybe MetaMask should be a software agent with application privileges and not just a user extension? I’m thinking of password managers.

---

**boris** (2018-09-13):

The author launched the 25th feed reader. Feed readers were also at a time when 1) less people had smartphones, so more blogging 2) less people in the world were actively using the Internet than today.

The analogy doesn’t really work.

Also, the death of feed readers led to centralized algorithms and total control over social media.

Initiatives like Micro Blog https://micro.blog and others are going back to RSS.

The “tech” never failed, societal adoption and context moved on.

---

**danfinlay** (2018-09-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dpyro/48/89_2.png) dpyro:

> Maybe it should be treated as a plugin instead of just as an extension?

Plugins are actually deprecated, WebExtensions are the new standard way to extend browser functionality. They do not have access to native code. This isn’t our choice, this is a limitation imposed by the browsers.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dpyro/48/89_2.png) dpyro:

> think you should be able to delegate storing this seed to an OAuth 2.0 provider for low/no value/dev accounts. If you don’t have even minimal functionality within 5 seconds of clicking on the extension you are already losing user interest.

I agree.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dpyro/48/89_2.png) dpyro:

> Maybe there should be some kind of simple queue visualizer for your transactions?

We actually have this already in development. It’s been a long time coming. We believe improving the UX of the transaction queue is key to making it usable.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dpyro/48/89_2.png) dpyro:

> Maybe MetaMask should be a software agent with application privileges and not just a user extension? I’m thinking of password managers.

That’s the tip of an interesting iceberg. We definitely think long term there are big benefits to becoming a system extension, and there are a lot of different ways that empowers us, like operating on other networking protocols, etc. I’m not completely sure how you’re suggesting it would alleviate phishing attacks. Virus detection?

---

**Cygnusfear** (2018-10-10):

In a way you could say RSS was ‘fixed’ by social media.

RSS suffered from the fact that the user aggregated a lot of content and would then have to personally curate (read: read) this content.

Social sharing features supplanted this issue (your friends / celebrities curate!). Henceforth users would find more relevant information scrolling through a feed of people they were interested in in the first place.

In a way it highlights how (traditional) news venues have a curatorial problem as they need to pander to a large audience and it’s hard to personalise without better personal data. Similarly, Netflix recommendations.

I’m not sure if this is historically correct, but I assume Reddit delivered the coup de grâce: socially curated RSS with subreddits being ‘categories’ that users can create at their whim.

---

**tjayrush** (2018-10-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> This isn’t our choice, this is a limitation imposed by the browsers.

Whenever I’m limited by something, I try to escape. Break out of the browser. There’s a big wide desktop out there.

