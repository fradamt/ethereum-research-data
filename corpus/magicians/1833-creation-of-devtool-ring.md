---
source: magicians
topic_id: 1833
title: Creation of Devtool ring
author: yann300
date: "2018-11-07"
category: Magicians > Tooling
tags: []
url: https://ethereum-magicians.org/t/creation-of-devtool-ring/1833
views: 1545
likes: 19
posts_count: 15
---

# Creation of Devtool ring

After a technical discussion with Truffle team about having a standardization around debugging support, it might worth setting up a ring involving teams building developer tools.

I m sure we will find plenty of other topics (like the standardization of the vm trace).

Make sense?

## Replies

**iurimatias** (2018-11-08):

You can count on the Embark team for this ring.

---

**ChainSafe** (2018-11-08):

Sounds awesome! [@noot](/u/noot) and I talked about it yesterday and you can count us in. We are working on golang tools for compiling, deploying, testing, and interacting with smart contracts (https://github.com/ChainSafeSystems/leth).

---

**gnidan** (2018-11-08):

Count in all of us working on the Truffle Suite!

On the topic of creating a standard debugging data format, please find the initial discussion’s [meeting notes](https://docs.google.com/document/d/1IHaS-jSLIAaXnf9NMAkf_TE2aaPjTgM3YdlCapDY-lA/edit#heading=h.3owp6qv3msru), as well as the new [ethdebug GH organization](https://github.com/ethdebug). More to come.

Looking forward to this ring. Thanks [@yann300](/u/yann300)!

---

**0mkara** (2018-11-08):

I am in. Helping remix tools integration into Atom editor. ![:robot:](https://ethereum-magicians.org/images/emoji/twitter/robot.png?v=9)

---

**jpitts** (2018-11-08):

I see a lot of support for this and will create a topic category here in the Forum.

Perhaps it should be called “**Dev Tools Ring**” (in order to match how this term is widely used).

---

**jpitts** (2018-11-09):

What are some of the collaboration opportunities that stand-out for this Ring? These can be called out in the Dev Tools Ring wiki page…

---

**0mkara** (2018-11-10):

remix tools can be divided into few basic groups :

1. development, debugging & testing tools
2. development UI/UX
3. integration of dev tools into various editors
4. development of independent plugins & integration into Remix IDE

based on these groups we can specify several collaboration opportunities. [@yann300](/u/yann300) [@iurimatias](/u/iurimatias) let us know your thoughts.

---

**yann300** (2018-11-12):

Sure let’s call it “Dev Tools Ring”

---

**yann300** (2018-11-12):

[@0mkara](/u/0mkara) thanks for the summing up,

I would also like to point out that the purpose of this Ring is to discuss about how to together approach some general issues around tooling, how to address the need of standard (very important), to share experience on UX and implementation details.

Having teams working/integrating mutual work exists but that should not (imho) be the focus here.

---

**spalladino** (2018-11-12):

Hey, Santiago from Zeppelin here. Though we’re not working on a debugger, we are interested in storage layout information from the compiler (to ensure compatibility during upgrades), and have [this conversation](https://github.com/ethereum/solidity/pull/4017#issuecomment-410331891) ongoing with the Solidity team. I’d like to know if this format is useful for debugging purposes as well, so we don’t duplicate efforts!

---

**nrryuya** (2018-11-28):

Hi, I’m Ryuya, the author of [Vyper plugin for remix](https://github.com/LayerXcom/vyper-remix) and currently working on [FVyper](https://github.com/LayerXcom/verified-vyper-contracts) project which aims to develop a collection of Vyper contract and formally verify them with KEVM.

Ping me if you have some topics about Vyper, then I will bring the discussion to Vyper team.

---

**nrryuya** (2018-11-28):

I’m interested in the standard of compiler artifacts which make it easier for frameworks and tools to support new languages like Vyper, Flint, etc.

---

**Cygnusfear** (2018-11-28):

I’d love to join in, currently working on new features for ethtective that will make it easier for developers to use it to debug contract(-to-contract) interaction. Would love to have insight in how I can better help developers understand what happens to deployed contracts.

---

**yann300** (2018-11-28):

Thanks for all your reply ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

[@Cygnusfear](/u/cygnusfear) [@nrryuya](/u/nrryuya)  feel free to ad yourself to [Dev Tools Ring · ethereum-magicians/scrolls Wiki · GitHub](https://github.com/ethereum-magicians/scrolls/wiki/Dev-Tools-Ring)

