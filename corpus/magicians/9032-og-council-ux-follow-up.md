---
source: magicians
topic_id: 9032
title: OG Council UX follow up
author: dszlachta
date: "2022-04-24"
category: Uncategorized
tags: [ux, uxr]
url: https://ethereum-magicians.org/t/og-council-ux-follow-up/9032
views: 1525
likes: 5
posts_count: 6
---

# OG Council UX follow up

Hi, from the UX discussion that we had in AMS I got a feeling that we simply don’t know who our users are. Would anyone by interested in helping with Ethereum user survey?

## Replies

**chaals** (2022-04-28):

Here is a summary of the session that I wrote from the notes on the whiteboard…

# UX session notes - OG council, Amsterdam 2022-04-24

The session discussed UX in general. There is a “whiteboard note” that tried to capture some of the discussion, and I am attempting to decipher that here.

Questions / Topics:

- What do we mean by UX?

What are the problems?

What are examples of better UX, and why?
- And worse UX?

[Why does it matter?](#why-ux-matters)
[So what do we want to do?](#so-what-next)

## What do we mean?

What we mean is trivially described as “making things simple”. Key questions we noted include:

- Do users achieve what they want?
- Do users achieve what we want them to achieve?
- Are people spending time doing tasks that could be automated away?
- Are people comfortable working with the system? More than with other alternatives?

### What are the problems?

We identified a few barriers to usability:

- Fear…

…of the consequences of a mistake. Web3 systems are unforgiving compared to e.g. bank accounts or credit cards

…of being embarrassed

Language and accessibility issues

- Many systems are command line based, and often error messages are generic rather than informative, or are excessively “cryptic”.

The other major interface pattern is using Web apps. Here there is available knowledge and guidance on how to improve: WCAG, W3C’s i18n work, …

Technical issues:

- Performance is unpredictable, but also there is rarely feedback on how long things take, how they are progressing…

Errors are obscure (see above: accessibility and language issues)

### Better UX examples

- Uniswap
- Grid+
- Pryzm
- POAP
- Dappnode
- Wallets (but with the caveat that they aren’t generally great UX)
- “point and click” interfaces

These can be built with Web technology for which there is significant work avaialable on how to provide better user experience
- but there is a concern that these can hide problems, or make security properties hard to discover.

### Worse UX examples

- Ethereum clients

Essentially Eth1 / Execution clients

Command Line is not how people usually operate software in this century

Being surprised at fees for multiple transactions
Trying to run a node, and interact with it from other applications

## Why UX matters

- There are alternative platforms. If they are easier to work with, they will attract capital, projects, mindshare, and developers that would otherwise consider the Ethereum ecosystem as a natural home.
- Provides confidence in the ecosystem, which in turn encourages investment and the creation of a larger community of developers in a “virtuous circle” - a feedback loop that encourages growth of the ecosystem.
- It’s necessary to achieve the often-claimed goals of enabling decentralisation and improving democratisation
- It can help people understand security better, and so make fewer mistakes.

## So, what next?

- We encourage people to publish the results of research into usability in our space.
- It would be nice to see simplified interfaces that provide all the information a user needs to complete an action (i.e. they won’t be surprised halfway through), and does not require them to manually do things that are unnecessary.
- It would be nice to have more “easy entry simulations” - e.g. going through the process of a transaction, or of adding a contract to a network, without incurring the costs of it happening “for real”
…

---

**chaals** (2022-04-28):

And here is a picture of the whiteboard at the end:

[![EthMag-OG-UX-20220424](https://ethereum-magicians.org/uploads/default/optimized/2X/1/19d17bc735f5ea1265b4f8f00c5b837ba40df8e3_2_666x500.jpeg)EthMag-OG-UX-202204241920×1440 138 KB](https://ethereum-magicians.org/uploads/default/19d17bc735f5ea1265b4f8f00c5b837ba40df8e3)

---

**dszlachta** (2022-04-29):

Thank you for summarizing it. I think that anyone interested in Ethereum’s UX will find these notes interesting and helpful.

Regarding the user survey (or maybe better “community survey”), I’m happy to announce that a team has gathered and will soon start working on making it happen. Of course, anyone interested in helping can still join us.

---

**chaals** (2022-04-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dszlachta/48/5935_2.png) dszlachta:

> Regarding the user survey (or maybe better “community survey”), I’m happy to announce that a team has gathered and will soon start working on making it happen. Of course, anyone interested in helping can still join us.

Excellent! How do people join? What do you have as starting material, plan, …? (I’m looking for stuff written that we can share - beyond even this forum, e.g. in translation)

---

**dszlachta** (2022-04-29):

Right now people join by giving me their e-mail address ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) But we will for sure setup some kind of IM channel/forum/mailing list. We have some draft documents: rules (how to ask the questions, what not to ask, privacy, etc.), question ideas and a list of organizations that could have done UX research in the past (we want to contact them). I imagine that when these drafts are finalized and become internal set of guidelines for the team, we make them all public.

