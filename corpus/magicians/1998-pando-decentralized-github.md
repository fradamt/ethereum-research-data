---
source: magicians
topic_id: 1998
title: "Pando : Decentralized GitHub"
author: xanthos
date: "2018-11-24"
category: Magicians > Tooling
tags: [dao, github, aragon, pando]
url: https://ethereum-magicians.org/t/pando-decentralized-github/1998
views: 2120
likes: 23
posts_count: 11
---

# Pando : Decentralized GitHub

Hi! I create this topic connected to the project called @pando_network witch is currently developing a decentralized GitHub where each repo can be controlled by an AragonDAO.

As the project is open-source [GitHub - pandonetwork/pando: A distributed remote protocol for git based on IPFS, ethereum and aragonOS](https://github.com/ryhope/pando) I thought it would be nice to create a dedicated topic

A first description of the tool is available here : [Pando. The genesis of a fully distributed VCS | by Olivier Sarrouy | Pando Network | Medium](https://medium.com/ryhope-network/pando-b5e1a2af3152)

And in more general way here : [The Pando Network. THE INFRASTRUCTURE FOR DISTRIBUTED… | by Nolwenn Jollivet | Pando Network | Medium](https://medium.com/ryhope-network/the-pando-network-ff385f2be05a)

This project contains many new features that can’t be found on any other VCS that you may want to discuss. Such as « individuation » / « Lineage » and so on.

You can take a look at those functions here:


      ![image](https://blog.aragon.org/content/images/size/w256h256/2023/03/60.png)

      [Aragon's Blog – 5 Aug 20](https://blog.aragon.org/nest-pando-q3-update/)



    ![image](https://uploads-ssl.webflow.com/5eafd02eb8d39c21817c6a27/5ebb4a24c85a590826a7e064_nest_pando_wide.png)

###



This second milestone was quite busy










The project has also already implemented governance KIT for the collective management of repo such as **DictatorKit**

(Enforce a maintainer-based governance à-la GitHub )

**VotingKit** (Enforce a Native Lineage Token-backed democratic governance to sort and valuate requests)

These governance kits for the collective management of repo is a major step forward regarding to GitHub’s workflow and I think that this will eventually lead to discussions or participations.

## Replies

**jpitts** (2019-01-02):

I finally read the summary article about Pando Network and am very excited about this project. I will definitely keep it in mind for a near-future project.

https://medium.com/ryhope-network/the-pando-network-ff385f2be05a

---

**xanthos** (2019-01-03):

Thank a lot for the feedback. If you are interested our TecLead Olivier Sarrouy recently held a long discussion here about Pando. You will find additional information there.



      [github.com/aragon/nest](https://github.com/aragon/nest/pull/31)














####


      `master` ← `pandonetwork:master`




          opened 06:33PM - 19 Mar 18 UTC



          [![](https://avatars.githubusercontent.com/u/86822?v=4)
            osarrouy](https://github.com/osarrouy)



          [+88
            -0](https://github.com/aragon/nest/pull/31/files)







# Request for Nest membership and funding ([#3](https://github.com/aragon/nest/i[…](https://github.com/aragon/nest/pull/31)ssues/3))

**Team name**: wespr / pando

**Proof of concept**: [https://github.com/wespr/pando](https://github.com/wespr/pando) and [https://www.youtube.com/watch?v=lOcElty7zIw](https://www.youtube.com/watch?v=lOcElty7zIw)

**Research white paper**: [https://docs.google.com/document/d/1dNVniSPUlZrPwHs0qXC4qmHQcpD2RAurKtuuXTQxb7w/edit?usp=sharing](https://docs.google.com/document/d/1dNVniSPUlZrPwHs0qXC4qmHQcpD2RAurKtuuXTQxb7w/edit?usp=sharing)

**Burn rate**:
17800 $/month for 8 months plus an additional $50000 ANT success bonus:

- 10000 $/month for 8 months for full-time team.
- 6000 $/month for 8 months for third-time team.
- 1800 $/month for 8 months for part-time team.

**Legal structure**:
Aragon DAO (for now)

**[Team and roadmap](31/files)**

## Proposal

The goal of wespr is to offer a distributed cooperation, distribution and valuation infrastructure to Commons Creative Contents (CCC) i.e. any kind of content produced through an open process such as - but not restricted to: Open Source Software, Books licensed under Creative Commons, Music licensed under Creative Commons, etc.  wespr thus intends to be the cultural infrastructure of the distributed web. To do so we plan to provide: a. a distributed cooperation and versioning infrastructure; b. a distributed governance infrastructure; c. a distributed publishing infrastructure; d. a distributed valuation network.

The goal of these infrastructures is to provide economic and organizational autonomy to CCCs and thus to incentivize cultural openness and cooperation. We do believe that such an infrastructure will expand the ethos of Open-Source Software to the whole cultural realm: cooperating over books, writing or music composition the same way people fork or contribute to open source projects. For that reason, Open-Source Software is not just another field of application of wespr. Its inner core protocols are tightly inspired by Open-Source Software habits, practices and apparatuses.

What we do propose for the Aragon Nest #3 grant proposal is thus to develop a. distributed cooperation and versioning infrastructure; b. a distributed governance infrastructure based on IPFS and AragonOS and; c. a dApp relying on these infrastructures and dedicated to Open-Source Software development.

Though we aim to rely on these infrastructures to build our own valuation network, the distributed cooperation and versioning infrastructure and the distributed governance infrastructure developed with this grant aim to be as generic, modular, content-agnostic and token-agnostic as possible. They will basically consist of a distributed git-like versioning system whose governance protocols are enforced through an AragonOS-based DAO. Thus, the core of the proposal we submit for the [Aragon Nest #3](https://github.com/aragon/nest/issues/3) is:

- A cooperation and versioning infrastructure: pando. This infrastructure will rely on:
  - An IPFS-based storage layer to keep track of each file’s version in a repository.
  - A set of formalized data structures to describe the history graph of this repository.

- An AragonOS-based set of apps to enforce token-driven governance over a pando repository. This set of apps will provide:
  - A modular pando repository app.
  - A default governance app allowing project’s members to enforce access control over their repository through liquid democracy.
  - An interface with the reward engine proposed by the Aragon Planning App.
  - An interface with the payout engine proposed by the Aragon Planning App.

- This infrastructure will come up with:
  - An npm library allowing developers to interact with pando repositories.
  - A cli tool to create and manage pando repositories.
  - A set of standard interfaces to develop repository plugins for the reward engine and the payout engine.

- [Stretch Goal] An Open-Source Software dApp based on this infrastructure: PandoHub.












I’ll keep you informed.

---

**xanthos** (2019-01-09):

You will find a new article here entitled **“DAO & The future of content”**. Inside is also quickly discussed the impact that Pando could have on GitHub workflow.

https://medium.com/pando-network/dao-the-future-of-content-fd9349d94b24

---

**xanthos** (2019-01-22):

Hy everyone,

[@osarrouy](https://twitter.com/osarrouy) the tech lead of Pando organize a hackathon during Aracon to create an **Aragon Package Manager**.

To participate in this adventure from the NPM to APM you can see all the details here :



      [github.com](https://github.com/AragonDAC/APMHackathon)




  ![image](https://opengraph.githubassets.com/204259763b22fcd60b0a85b765748ad5/AragonDAC/APMHackathon)



###



Submissions for Aragon Remote Hackathon










And chat on the `#apm-hackathon`  channel of [Aragon’s chat](https://aragon.chat/channel/apm-hackathon)

---

**xanthos** (2019-01-27):

Hy, everyone

here is a  sneak peek to pando before #AraCon2019



      [twitter.com](https://twitter.com/pando_network/status/1089573682907922432)



    ![image](https://pbs.twimg.com/profile_images/1072871617707950083/UXzxCDzu_200x200.jpg)

####

[@pando_network](https://twitter.com/pando_network/status/1089573682907922432)

  A sneak peek to pando before #AraCon2019 https://t.co/KPwTEpEDM7

  https://twitter.com/pando_network/status/1089573682907922432










![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=12)![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=12)![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=12)

---

**xanthos** (2019-01-28):

A new article related to Pando and it’s licence project have been published here, it also quickly present the futur API :

**A decentralized autonomous licence for content-DAOs**

https://medium.com/@alex_71247/a-decentralized-autonomous-licence-for-content-daos-5a03ad9b2eb2

---

**xanthos** (2019-01-28):

# Pando_network is running for Flock as Aragon Black.

Below is the proposal

https://medium.com/pando-network/announcing-pandos-agp-proposal-aragon-black-78ce0b805dae

---

**xanthos** (2019-03-30):

**[Pando - Decentralized GitHub- live on Rinkeby]**

You can browse the test DAO there: https://rinkeby.aragon.org/#/0xe048d120Be1aEf0D198437f7f8752F64618FD02A/

In this DAO you will find [at least] two pando repositories. The first one is a pando how-to: it will guide you in how to use Pando. The second in a small experimentation: a distributed repo to collaboratively produce a non-dev Aragon on-boarding guide. We’re waiting for you contributions here!

You can browse the test DAO there: https://rinkeby.aragon.org/#/0xe048d120Be1aEf0D198437f7f8752F64618FD02A/

Installation guide : https://rinkeby.aragon.org/#/0xe048d120Be1aEf0D198437f7f8752F64618FD02A/0xa80ad65ff3801dfd088e044c498a3f9a90366b50

You can play with it and you’ll find other informations on the Aragon Forum where you can ask your questions : (https://forum.aragon.org/t/pando-live-on-rinkeby/712)

---

**xanthos** (2019-04-05):

Using pando with Ledger-nano & @frame_eth to push data on a repo controlled by an AragonDAO and stored on #IPFS !

---

**xanthos** (2019-04-20):

A visual summary of AGP-34 where there is a presentation of Pando



      [twitter.com](https://twitter.com/AragonBlackTeam/status/1119640026063806465)



    ![image](https://pbs.twimg.com/profile_images/1118071345655447552/IqadaHUW_200x200.png)

####

[@AragonBlackTeam](https://twitter.com/AragonBlackTeam/status/1119640026063806465)

  A visual summary of AGP-34 🚀 @AragonProject https://t.co/9HS9EzXsO1

  https://twitter.com/AragonBlackTeam/status/1119640026063806465

