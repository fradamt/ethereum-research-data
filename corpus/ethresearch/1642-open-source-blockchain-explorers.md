---
source: ethresearch
topic_id: 1642
title: Open Source Blockchain Explorers
author: GriffGreen
date: "2018-04-07"
category: Tools
tags: []
url: https://ethresear.ch/t/open-source-blockchain-explorers/1642
views: 29451
likes: 33
posts_count: 27
---

# Open Source Blockchain Explorers

Block Explorers are one of the most fundamental tools needed for any blockchain to thrive, and amazingly, Ethereum is extremely centralized in this. Everyone goes to Etherscan 10x a day.

I love Etherscan, and am so impressed with how it works… I also love the USA and am soo impressed at the quality of life there… But both of these are centralized golden cages, and we are trying to do something different, better, an open field with rainbows butterflies and real customization.

There are 2 AWESOME Open Source Block Explorers currently under development, and every 2 weeks on Friday we have an open call (Inspired by the plasma call) where the people working on projects similar projects can feel welcome to attend ;-D

If you would like an invite to the telegram where we organize, please message me ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=9)

Links!

**First 2 calls:**

#1: https://youtu.be/CXtkv-HzEso

#2: https://youtu.be/Kry1PNp7TJk

I have sooooo many more… but i can only put 2 links in a post ![:frowning:](https://ethresear.ch/images/emoji/facebook_messenger/frowning.png?v=9)

## Replies

**GriffGreen** (2018-04-08):

POA Network is one of the 2 teams working on this, if you are interested in what they are working on:

Github: https://github.com/poanetwork/poa-explorer

Timeline: https://github.com/poanetwork/poa-explorer/wiki/Timeline-for-POA-Block-Explorer

Overview: https://github.com/poanetwork/poa-explorer/wiki/POA-Block-Explorer-and-Web3-Grant-Overview

Stack: https://github.com/poanetwork/poa-explorer/wiki/Development-Stack

Block Explorer: https://explorer-sokol.poa.network/en

(Dockyard) - Project 1: https://github.com/poanetwork/poa-explorer/projects/1

(Gaslight) - Project 2: https://github.com/poanetwork/poa-explorer/projects/2

(Plataformatec) Project 3: https://github.com/poanetwork/poa-explorer/projects/3

---

**GriffGreen** (2018-04-08):

EthVM is the 2nd block explorer being worked on by MyEtherWallet


      ![image](https://github.githubassets.com/favicon.ico)
      [GitHub](https://github.com/enKryptIO/)


    ![image](https://avatars1.githubusercontent.com/u/47159500?s=280&v=4)

###

Org by MyEtherWallet. GitHub is where enKrypt builds software.








Database: RethinkDB

Backend: Modified Geth, Stateless websockets for scaling

Frontend: Vuejs

Feature Requests: https://github.com/enKryptIO/ethvm/issues

---

**GriffGreen** (2018-04-20):

New Call just started ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=9)

---

**GriffGreen** (2018-05-04):

The Fourth OSBE call happened live at EDCON. We had some serious sound issues ![:frowning:](https://ethresear.ch/images/emoji/facebook_messenger/frowning.png?v=9) but some of it worked great! See the updates below ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9)

Quick update on Shokku (I’ll include VulcanizeDB code into the project? I’m not sure yet) - Aldo https://youtu.be/lIrxWIgSprQ?t=7m48s

Update from POA Network -Igor (BAD SOUND ![:frowning:](https://ethresear.ch/images/emoji/facebook_messenger/frowning.png?v=9) )

Update From MEW - Kosala https://youtu.be/lIrxWIgSprQ?t=15m32s

At the end there was a fun conversation with people from Infura, Quickblocks, Ubiq, POA Network and the Ethereum foundation… That part of the video worked out well and was fun: https://youtu.be/lIrxWIgSprQ?t=41m7s

Quick update on Web3Scan:

Last week Emiel from Web3Scan joined our little community and he had this to say:

After watching the first 3 episodes of our initiative he believes Web3scan complements the group by focussing on de DB layer, specifically by building large dbs by harvesting and indexing all data of the various networks. This should result in (SQL) queryable dbs aimed to assist developers, academia, researchers and operators of consortium networks. In the short term they do not plan to develop a user interface (public web interface or API), or a method to decentralize building the DB. In our opinion this distracts from the #NOW component. In the short term they aim to solve an immediate service management problem to distribute harvested and indexed >TB level databases to our audience. They are aware that this requires some trust in our services, but data can of course be verified by making sample tests with other sources. The idea with access to these large DB is of course that you can find answers to questions that the clients (Parity/Geth) or the block explorers (etherscan/etherchain) do not provide easily.

And specifically as far as work they did last week, they sync’d about 10 different networks with Parity nodes in archive/trace/fatdb mode. Amongst others Poanetwork, Kovan, Ropsten, Mix, Musicoin, Expanse, Ella, Toma, Ether Classic. His next move is to make preparations to harvest and index these networks in their relational DB model.

---

**GriffGreen** (2018-05-16):

This next friday will be a really good one, lots of demos ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=9) If you want to join, please reach out to me! If you want to watch, I will post the link here ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=9)

---

**GriffGreen** (2018-05-18):

The 5th Open Source Blockchain Explorers NOW! Call is happening in 15 minutes!

Agenda:

Mitch In Depth Intro

EthVM Update - Aldo

POA Network Update- Andrew (Many updates but will try and keep them short)

Prysmatic Labs Intro - Preston Van Loon (5 minutes or less)

Quickblocks screen share demo (5-7 minutes)

Then a Fireside chat to finish it off ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=9)

---

**GriffGreen** (2018-06-01):

The 6th Open Source Blockchain Explorers NOW! Call is happening… NOW!

Agenda:

EthVM Update - Griff

POA Network Update - Mitch

Introduction to Analyse Ether https://github.com/analyseether - Ankit

---

**timjp87** (2018-06-02):

I just want to mention https://github.com/Magicking/Clixplorer.

I set up a POA Testnet with Puppeth which doesn’t support deploying a block explorer if you opt for Clique consensus. With Clixplorer I was able to deploy a testnet on a single small cloud instance with all major components since there is no need for PoW and the CPU can serve all the different webservices from the same instance instead of being busy doing the mining.

---

**kladkogex** (2018-06-02):

I am a bit curious on the choice of the frameworks you guys are using.

Shouldnt it be AngularJS/Typescript or ReactJS?  A bit strange to see things like Erlang …

---

**GriffGreen** (2018-06-07):

POA is using Erlang, but ETHVM ( https://github.com/enKryptIO/ ) is using Vue and I think OST is using something normal as well ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9)

---

**GriffGreen** (2018-06-07):

Awesome are you a developer on that project?

---

**timjp87** (2018-06-08):

No I found it because I was searching for an open source explorer and also found your thread this way, too. I will only do a pull request for Clixplorer to have better installation and configuration documentation.

---

**timjp87** (2018-06-08):

PoA is using Elixir (which runs on Erlang VM) which is only for the Backend (think of it like Go Lang). Elixir is very nice for web servers. For the frontend you’ll still use something like React, Vue or Angular if you are developing an Elixir application. Elixir + VueJS is a really progressive web stack.

---

**GriffGreen** (2018-06-11):

Thx for clarifying [@timjp87](/u/timjp87) !

---

**GriffGreen** (2018-06-11):

This Week we are likely going to do #7 on Friday at 4pm New York Time… In case you haven’t seen the community growing here, the projects that are there collaborating and talking are:

**3 Block Explorers:  **

**Explorer by POA Network**



      [github.com](https://github.com/blockscout/blockscout)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/8/b/8b2ef0ad1fbf458eaf4f77a694da9cbecbb14f5c_2_690x344.png)



###



Blockchain explorer for Ethereum based network and a tool for inspecting and analyzing EVM based blockchains.










Elixir, erlang, postgres

Block Explorer: https://explorer-sokol.poa.network/en

(Dockyard) - Project 1: https://github.com/poanetwork/poa-explorer/projects/1

(Gaslight) - Project 2: [Contributors Section · GitHub](https://github.com/poanetwork/poa-explorer/projects/2)

(Plataformatec) Project 3: https://github.com/poanetwork/poa-explorer/projects/3

**EthVM - MyEtherWallet**

https://github.com/enKryptIO/

Database: RethinkDB

Backend: Modified Geth, Stateless websockets for scaling Frontend: Vuejs

**OST VIEW - Focus on Tokens**



      [github.com](https://github.com/ostdotcom/ost-view)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/8/c/8cff683aa5eabfabcdeaaa32c6c5234be2547b50_2_690x344.png)



###



OST VIEW is the custom-built block explorer from OST for OpenST Utility Blockchains










- Hosted version for OST testnet : https://view.ost.com

**Other interesting complimentary projects:**

**Open source Infura Clone: Shokku**



      [github.com](https://github.com/ubiq/shokku)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/6/2/62eb162e099f3998b0b2875e6a434919d0338a2c_2_690x344.png)



###



An open source scalable blockchain infrastructure for Ubiq, Ethereum, POA and IPFS that runs on Kubernetes










**VulcanizeDB**



      [github.com](https://github.com/vulcanize/vulcanizedb)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/2/5/258406414ad0558e74a9bb42a9fd7dffd8c4f37b_2_690x344.png)



###



Contribute to vulcanize/vulcanizedb development by creating an account on GitHub.










**QuickBlocks**


      ![](https://ethresear.ch/uploads/default/original/3X/7/b/7bcf6f37b118855c90b9f3e47281e27f3a5cf11d.png)

      [TrueBlocks](https://trueblocks.io/)



    ![](https://ethresear.ch/uploads/default/original/3X/6/6/66b6874a937a08f37152ba15a17b90886eb1f79f.png)

###



Build a local-first index of the Ethereum Blockchain.










GitHub:[GitHub - TrueBlocks/trueblocks-core: The main repository for the TrueBlocks system](http://github.com/Great-Hill-Corporation/quickBlocks)

White Paper: [trueblocks-core/src/other/papers/README.md at main · TrueBlocks/trueblocks-core · GitHub](https://github.com/Great-Hill-Corporation/quickBlocks/blob/master/src/other/papers/README.md)

**Analyse Ether**


      ![](https://ethresear.ch/uploads/default/original/2X/b/bad3e5f9ad67c1ddf145107ce7032ac1d7b22563.svg)

      [GitHub](https://github.com/analyseether)



    ![](https://ethresear.ch/uploads/default/original/3X/1/9/195481d9ecf41c5284f0de2d454a673943b541c2.png)

###



Come let us analyse ether together. Analyse Ether has 4 repositories available. Follow their code on GitHub.










Website: https://www.analyseether.com/

MVP: https://mvp.analyseether.com/

Even More projects

**Web3Scan**: Query-able SQL DB

**eth.events**: (Konrad of BrainBot’s baby…) an elasticsearch cluster with and ABI translator that enriches the raw blockchain data: A generic way of querying all eth events

**Prysmatic Labs**: Sharding and Casper research

**ETHPrize**: Funding POA’s Explorer and helping Giveth manage this Community

**Giveth**: A community focused on #Blockchain4Good, looking to support ETH Commons

TrueBit, Aragon, UBIQ, [Balance.io](http://Balance.io), Infura, Ethereum Foundation and other orgs have people participating as well.

---

**GriffGreen** (2018-06-15):

Our seventh call… and maybe the most exciting one yet goes live in 5 minutes ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9)

---

**cooganb** (2018-07-09):

Hey [@GriffGreen](/u/griffgreen)! I am a teacher running a blockchain school. We’re about to start our section on Ethereum and the students are about to start their sync.

We wrote the curriculum before we found your group and we are asking the students to build a block explorer with “extended functionality.” I’m going to send them to as many of the Open Block Explorer resources as possible.

Quick logistical question: When undergoing the rite of passage known as First Ethereum Sync Attempt, are there any flags that make EVM traversal easier in the future? We are using the latest Geth release (I know Parity has tracing, but I’m more familiar with Geth) and are hoping to do tracing (if possible).

Any suggestions from you or anyone in the community would be greatly appreciated! Thanks so much for your work.

---

**GriffGreen** (2018-07-13):

Our ninth call… lots of fun things on the agenda ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=9)

---

**GriffGreen** (2018-07-27):

#10 is up! ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=9)

---

**sjalq** (2018-09-12):

Hey guys, looks like it’be been a quiet 7 weeks.

I’m really in need of this solution, is development still ongoing?


*(6 more replies not shown)*
