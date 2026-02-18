---
source: magicians
topic_id: 2351
title: Documentation of Constantinople EIPs
author: jochem-brouwer
date: "2019-01-07"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/documentation-of-constantinople-eips/2351
views: 726
likes: 5
posts_count: 4
---

# Documentation of Constantinople EIPs

I love all Constantinople opcode EIPs, but find the documentation of them quite lacking. The EIPs give us a general overview about what these EIPs should do, but do not cover edge cases. For example, what should an `extcodehash` return on a contract which is selfdestructed on the same transaction? It returns the hash of the code which was there `before` it was selfdestructed. Of course, this might have to do with internal (and previous) logic which has to do with `extcodesize` where it returns the code size of the original code, even if it was selfdestructed in the same transaction.

A better example is CREATE2. In CREATE2 you are allowed to selfdestruct a contract and create a new one (which might even have different initial storage or different runtime code). This is not very intuitive to me.

These arguments might all be battled by choices which have been made by the Ethereum spec beforehand, such as: contracts are only allowed to be created on addresses with nonce zero and which do not have actual code there. But still, we can see a spreadsheet with a lot of test cases for Constantinople (state tests), but there is no documentation there about /why/ (in human terms) these tests should do exactly that.

This thread is mainly to raise the point that I think that documentation of the low level Ethereum protocol should be better - or it is a thread to call out to me if I lack the skills of finding the actual documentation where those are listed! =)

## Replies

**boris** (2019-01-07):

I think more documentation is absolutely needed. Right now it feels like things are a little bit diffuse and stale.

Here are OPCODE related resources I know of:

- https://github.com/trailofbits/evm-opcodes
- https://ethervm.io/

I *just* found that the new-ish Ethereum wiki has an [EVM Awesome List page](https://en.ethereum.wiki/ethereum-virtual-machine-evm-awesome-list), which I think is a good place to gather EVM and OPCODE related resources. I added the two links above to the specification section.

If anyone knows of *other* EVM OPCODE resources – please add them!

I’m also aware there is ongoing, current discussion by All Core Devs about updating the Yellow Paper, potentially making the Jello Paper the canonical version. There isn’t AFAIK a thread about this, it’s just various Gitter posts for now? [@gcolvin](/u/gcolvin) has been looking into this, perhaps a thread here to move that discussion along.

I also think that this layer of Ethereum – the EVM and its opcodes – is something that fits under a broader “All EVM” set of stakeholders, as there are other chains that run the EVM. Everyone benefits from a better spec and related documentation.

---

**gcolvin** (2019-01-07):

These should all be in the Yellow Paper.



      [github.com](https://github.com/ethereum/yellowpaper)




  ![image](https://opengraph.githubassets.com/0618990e19d9e9650dbbfd46300124a3/ethereum/yellowpaper)



###



The "Yellow Paper": Ethereum's formal specification

---

**jochem-brouwer** (2019-01-08):

They might all be in the Yellow paper but that is not the resource most people fall back on. We need a clear and more detailed development documentation. The yellow paper is too abstract to fall back on for simple development questions.

