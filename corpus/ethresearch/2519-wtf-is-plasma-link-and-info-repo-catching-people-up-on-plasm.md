---
source: ethresearch
topic_id: 2519
title: WTF is Plasma? (Link and info repo catching people up on plasma)
author: Mekyle
date: "2018-07-10"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/wtf-is-plasma-link-and-info-repo-catching-people-up-on-plasma/2519
views: 7219
likes: 43
posts_count: 26
---

# WTF is Plasma? (Link and info repo catching people up on plasma)

I am having an extremely hard time getting caught up on plasma. But the information is very low level and it’s hard to get a grasp on what is going on and how can I implement plasma into my own project.

I want this post to help newcomers learn plasma from a beginner stand point. Beginner being understanding how to create dApps and understand Ethereum to a good extent.

What type of content should you link here?

- ELI5: Plasma (Explain Plasma like I’m 5)
- Article Links and Videos/PodCasts
- Github Repos on plasma implementations

Or anything else that you want that you believe can assist newbies get into Plasma.

## Replies

**rodneywitcher** (2018-07-10):

Hi Mekyle,

We’re implementing plasma cash as a way to provide bandwidth and storage to blockchains wishing to build “fast” dApps.  The following Github Repo is a good starting point for understanding what we’re doing: https://github.com/wolkdb/deepblockchains/tree/master/Plasmacash

There you’ll find our Rootchain contract and other materials.  Happy to answer further questions you may have.

-Rodney

---

**tpmccallum** (2018-07-11):

Here is list of GitHub repos which are implementing Plasma

Bankex



      [github.com](https://github.com/BANKEX/PlasmaParentContract)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/7/d/7df7aa332589e4d9a9a3929f93d967741fff28ad_2_690x344.png)



###



Main chain smart contract for Bankex Plasma implementation










Cosmos, Peg Zone Implementation



      [github.com](https://github.com/cosmos/gravity-bridge)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/e/0/e088142414b84c9e19994d01eb47e70eaa1359f0_2_690x344.png)



###



A CosmosSDK application for moving assets on and off of EVM based, POW chains










Taiwan Team, Javascript implementation of Plasma MVP



      [github.com](https://github.com/ethereum-plasma/plasma)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/4/5/451f1d3ca858bbc27dd1efeb1ad97615c7967c83_2_690x344.png)



###



Contribute to ethereum-plasma/plasma development by creating an account on GitHub.










Blockchain at Berkeley


      ![](https://ethresear.ch/uploads/default/original/2X/b/bad3e5f9ad67c1ddf145107ce7032ac1d7b22563.svg)

      [GitHub](https://github.com/FourthState)



    ![](https://ethresear.ch/uploads/default/original/3X/8/1/81b96493955905085f1370855e3b89b5544565b4.png)

###



Blockchain Scalability Research Lab. FourthState Labs has 4 repositories available. Follow their code on GitHub.










LayerXcom (Plasma using Vyper instead of Solidity)

https://github.com/LayerXcom/plasma-mvp-vyper

Loom Network



      [github.com](https://github.com/loomnetwork/plasma-cash)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/8/6/8675b675e1c5d3fbdde2d56804749653656f4ea1_2_690x344.png)



###



Plasma Cash Contract & Client. ERC721, ERC20, and ETH compatible










OmiseGO, Plasma Cash



      [github.com](https://github.com/omgnetwork/plasma-cash)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/7/b/7b7fcf826b0c0c89c09512f0215a259468916242_2_690x344.png)



###



Contribute to omgnetwork/plasma-cash development by creating an account on GitHub.










OmiseGO, Plasma MVP



      [github.com](https://github.com/omgnetwork/plasma-mvp)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/a/d/ada332cde0e3ff8e30b6f9ec848cc2b386b5d67f_2_690x344.png)



###



OmiseGO's research implementation of Minimal Viable Plasma










Voltaire Labs



      [github.com](https://github.com/voltairelabs/plasma)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/c/d/cd5e8532daac2f8a2a6c7a1e01d7fe25b75e2bde_2_690x344.png)



###



Ethereum plasma implementation










Wolk

https://github.com/wolkdb/deepblockchains/tree/master/Plasmacash

---

**tpmccallum** (2018-07-11):

This is not an exhaustive list, these are just the ones which I know about. I have also added a pull request at https://github.com/ethereum/plasma/pull/3 so that the list can be more dynamic and authoritative (updated and vetted on an ongoing basis rather than having to scroll through comments sections like this).

Hope this helps ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**kfichter** (2018-07-12):

Hey - I’m currently working on putting together a website that will attempt to be an all-in-one resource for this. Some questions:

- What sort of information would be most helpful to get a better understanding of Plasma?
- What’s most confusing when you first interact with Plasma?
- What’s still confusing to you about Plasma?

Other general feedback or questions would be much appreciated!

---

**lucusfly** (2018-07-12):

I found this very useful video to explain Plasma. https://www.youtube.com/watch?v=jTc_2tyT_lY

---

**Mekyle** (2018-07-13):

Thanks for all the links guys. I understand Plasma a lot better now and I’ll try and create some documentation with the links to make it really easy for beginners.

---

**Mekyle** (2018-07-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> What sort of information would be most helpful to get a better understanding of Plasma?

Videos are great for getting a quick grasp but the biggest thing would be articles on specifics of one particular section of plasma. Creating an “Understanding Plasma” series would be the best approach.

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> What’s most confusing when you first interact with Plasma?

Understanding how to implement Minimum Viable Plasma in projects is difficult since there’s no step by step approach. I’m not asking for a step by step approach but breaking down MVPlasma into it’s components and explaining the logic behind it would be extremely helpful.

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> What’s still confusing to you about Plasma?

Understanding exiting strategies is something that still troubles me but that’s normal since it’s still being worked on.

---

**kfichter** (2018-07-13):

Awesome, this is great feedback, thank you! Will try to incorporate all of this.

---

**Mekyle** (2018-07-15):

Hi,

I’ve been reading and trying to understand everything. I don’t understand implementing child_chains and building a client and also how they interact together.

---

**rodneywitcher** (2018-07-15):

Hi [@Mekyle](/u/mekyle)

Let’s setup some time to maybe chat on Hangout or via email to discuss specific questions.  At Wolk, we’re specifically building a Layer 2 Plasma chain that offers storage and bandwidth.  There are numerous Layer 3 (child) chains that can be built to utilize this and would be interested in learning what use case / client you’re working on.  Please send me a note at [rodney@wolk.com](mailto:rodney@wolk.com) and we can discuss.

---

**tpmccallum** (2018-07-16):

Hi [@kfichter](/u/kfichter),

A resource as you have suggested would be brilliant! It would be great if this could be done at ethereum/plasma GitHub [1] so that Ethereum GitHub could carry the torch.

I think that the all-in-one resource it should cover things like:

- terminology for the root chain. This is because the root chain can also be called the base layer protocol, or the parent chain etc
- terminology for the side chains. This is because the side chains can also be called child chains, layer 2 … layer n and so forth
- cover the fact that Plasma is an abstract design, not a product
- cover the fact that implementations that adhere to the general Plasma designs can be deeper than one level. This is because the side chains can have their own side chains and so on
- cover the fact that these second layer solutions do not use PoW but still produce blocks in other ways
- introduce block-producers and validators to the design ecosystem - for example how do block-producers jump from chain to chain to perform their work. Can this be automated in the future?
- get some sort of advice/guidance from @vbuterin and/or @jcp about whether future developers (who code up concrete implementations of the abstract Plasma design patterns) should use the word “Plasma”. Perhaps we could give developers more appropriate descriptors like:
a) Second Layer Side Chain (SLSC) or
b) Second Layer Peg Zone (SLPZ) or
c) Second Layer Lightning Network (SLLN) and so forth.
This would leave room for more acronyms as the design patterns progress. It is my guess that there will be a lot more implementations and that they will all have different attributes and operations. Only problem is that there might be overlap i.e. Side Chain and State Channel are both “SC”. Perhaps someone can come up with a better idea of how to describe implementations without overusing the word “Plasma”.

I will try and think of some more points. Love your work!

Kind regards

Tim

[1]  https://github.com/ethereum/plasma/pull/3

---

**kfichter** (2018-07-16):

Hey Tim, we’re starting to put together content over at [ethsociety/plasma-website](https://github.com/ethsociety/plasma-website). We’re gathering content over the course of this week, website should look less empty soon! We want to make this an open process, so we’re adding discussions in issues. I’m going to port the suggestions made here as well.

Note:

This is a project coming out of the IC3 Bootcamp, so most of the contributors are new to Plasma! Please feel free to contribute, even if that’s just by asking questions in the issues!

---

**mratsim** (2018-07-19):

I found this article quite good about explaining Plasma at a high-level: https://medium.com/l4-media/making-sense-of-ethereums-layer-2-scaling-solutions-state-channels-plasma-and-truebit-22cb40dcc2f4

---

**hernandp** (2018-07-23):

Hi guys, what do you think is the most advanced project being developed,in terms of the MVP specification? . I downloaded the OmiseGO Plasma Project but seems quite crude, and in a very early stage of development.  Thanks.

---

**tpmccallum** (2018-07-25):

Hi [@kfichter](/u/kfichter)

The plasma-website is looking really great, congratulations.

I have a bunch of questions. I am really happy to list them all on the plasma-website. I am also happy to write up the answers and create a PR on the plasma-website (so that I can contribute to the content).

I just need this brilliant bunch of researchers to provide some answers ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) first

… here goes:

1. Are all Plasma designs UTXO based? I would hazard a guess that those using Cosmos/Tendermint (or like a peg zone approach) would be account based; not sure about this.
2. Are there any Plasma designs which do not use a Plasma Operator?
3. Does a Plasma Operator have to be controlled by a person? Can it be a machine (a deterministic rules engine)?
4. Do all Plasma designs require a set of validators and/or block producers? If so, are they self organizing or deterministically chosen or randomly chosen (to perform validation/block production)?
5. Can a Plasma design logically separate validation from consensus?
6. Do Solidity Plasma implementations need to use DELEGATECALL to succeed in their interactove games etc.? I ask this because I believe that Vyper does not offer DELEGATECALL [1]. I guess I am ultimately asking if one could build a Plasma implementation in Vyper
7. What is the drawback of not being able to categorically identify overall smart contract ownership?

Apologies for having more questions than answers, with so many designs coming at this from different angles it would be great to get some clarity on the above.

Kind regards

Tim

[1] https://github.com/ethereum/vyper/issues/960

---

**kfichter** (2018-07-26):

[@tpmccallum](/u/tpmccallum) Thanks! Let’s find a place to put these Q/As on the website…

Answers first:

![](https://ethresear.ch/user_avatar/ethresear.ch/tpmccallum/48/1486_2.png) tpmccallum:

> Are all Plasma designs UTXO based? I would hazard a guess that those using Cosmos/Tendermint (or like a peg zone approach) would be account based; not sure about this.

Nope! I believe [FourthState Labs](https://github.com/fourthstate) was working on an account based Plasma chain. It’s entirely feasible, although it’s a little more complicated than a UTXO chain.

![](https://ethresear.ch/user_avatar/ethresear.ch/tpmccallum/48/1486_2.png) tpmccallum:

> Are there any Plasma designs which do not use a Plasma Operator?

Lots! It seems like most projects are starting off with PoA for simplicity but are planning to move to PoS or something similar once their designs are off the ground.

![](https://ethresear.ch/user_avatar/ethresear.ch/tpmccallum/48/1486_2.png) tpmccallum:

> Does a Plasma Operator have to be controlled by a person? Can it be a machine (a deterministic rules engine)?

Of course - It would probably be weird if the operator were actually a person. I’m guessing almost all (if not all) “operators” will really just be a machine that automatically selects transactions and submits blocks.

![](https://ethresear.ch/user_avatar/ethresear.ch/tpmccallum/48/1486_2.png) tpmccallum:

> Do all Plasma designs require a set of validators and/or block producers? If so, are they self organizing or deterministically chosen or randomly chosen (to perform validation/block production)?

All Plasma designs require that at least *something* is validated, but it doesn’t necessarily have to be entire blocks (see Plasma Cash).

![](https://ethresear.ch/user_avatar/ethresear.ch/tpmccallum/48/1486_2.png) tpmccallum:

> Can a Plasma design logically separate validation from consensus?

In the sense that users can (and should) validate the chain without participating in the consensus mechanism.

![](https://ethresear.ch/user_avatar/ethresear.ch/tpmccallum/48/1486_2.png) tpmccallum:

> Do Solidity Plasma implementations need to use DELEGATECALL to succeed in their interactove games etc.? I ask this because I believe that Vyper does not offer DELEGATECALL [1]. I guess I am ultimately asking if one could build a Plasma implementation in Vyper

DELEGATECALL isn’t a requirement, but it could be useful in certain circumstances (contract upgrades). I would think about the use case before selecting your language.

![](https://ethresear.ch/user_avatar/ethresear.ch/tpmccallum/48/1486_2.png) tpmccallum:

> What is the drawback of not being able to categorically identify overall smart contract ownership?

I’m currently writing some new material about this. Gist is that we have to change how we think about smart contracts to make them really work inside Plasma, but I don’t think it’s unfeasible.

---

**tpmccallum** (2018-07-27):

Wow, thanks [@kfichter](/u/kfichter)

I will go through the GitHub and find a spot for these (probably start issues and then action them with a PR yeah?).

Thanks again

Very useful information.

Kind regards

Tim

---

**tpmccallum** (2018-07-29):

Hi [@kfichter](/u/kfichter)

I just addressed issue #40 over on learn-plasma with a new PR #44

It got me thinking about how a particular Plasma design is essentially offering a temporary alternative to the underlying blockchain, and as such ultimately needs to offer characteristics which are no less favorable to the mainchain’s core blockchain characteristics (censorship resistant, permissionless, trustless etc).

Interestingly though, as it turns out Plasma can offer additional characteristics such as privacy. I guess in reality there are going to be technical limitations which mean that the Plasma implementation will be more application/use-case specific and will utilize trade-offs in order to achieve scalability for certain scenarios.

Just think it would be healthy to acknowledge and document any of the blockchain characteristics nuances in a Plasma implementation.

Can we build a visual matrix or a checklist etc which could reveal the fundamental blockchain characteristics of each Plasma design/implementation?

Kind regards

Tim

---

**tpmccallum** (2018-07-30):

One example of how a particular Plasma implementation could vary significantly from the mainchain’s blockchain attributes is when the Plasma Protocol requires an explicit static set of block proposers up-front (as described at the 8 minute mark of Plasma Implenters Call #8 < https://m.youtube.com/watch?v=2GgoYSFdTtQ >). This would work extremely well from a efficiency standpoint (and prevent withholding if participants were staking) however it could potentially change the implementation’s attributes i.e. permissionless, censorship resistant etc.

---

**tpmccallum** (2018-08-25):

Just added a link (above in the links section) to the Vyper implementation of Plasma by LayerXcom

https://github.com/LayerXcom/plasma-mvp-vyper


*(5 more replies not shown)*
