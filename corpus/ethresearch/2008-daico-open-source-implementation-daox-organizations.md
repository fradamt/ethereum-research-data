---
source: ethresearch
topic_id: 2008
title: "DAICO open-source implementation: Daox organizations"
author: bulgakovk
date: "2018-05-15"
category: Better ICOs
tags: []
url: https://ethresear.ch/t/daico-open-source-implementation-daox-organizations/2008
views: 3160
likes: 6
posts_count: 3
---

# DAICO open-source implementation: Daox organizations

The DAICO concept [suggested](https://ethresear.ch/t/explanation-of-daicos/465) by Vitalik Buterin is a reasonable and necessary step in the development of an ICO. The next step should be setting up a standard approach or framework to launch decentralized organizations of that kind. For this reason we would like to suggest our own approach towards the decentralized fundraising, namely Daox organizations.

**What are Daox organizations?**

A Daox organization is an implementation of the DAICO concept described by Vitalik Buterin, which preserves all the best features of the above-mentioned concept, as well as enhances it with new characteristics. The source code of such organizations is open and can be used freely.

**Why would I use the source code of Daox organizations?**

We believe that the best products are created only through joint efforts of involved in the project development. It is much more simple to explore, change and develop the existing code base than to create one’s own from scratch. Our common goal is to make the DAO concept widely used.

**Where can I review the source code of Daox organizations?**

The source code is under MIT license that guarantees permissive access, and is located at: https://github.com/daox/daox-contracts.

**Features in common with the DAICO concept:**

Raised funds do not belong to anyone and are stored in a smart contract;

The team has a limited access to the raised funds;

Investors can switch a contract to the refund mode and get the remaining proceeds proportionally with the number of their tokens.

**Added functionality:**

1. All the decisions within an organization are automatically made by means of decentralized votings

- Currently, there are the following 4 types of votings in Daox organizations: Proposal, Withdrawal, Refund, Module;

1. Mechanism of decentralized voting that does not affect any storage variables

- The DAO concept implies decentralized management. As the project evolves investors might need to hold a transparent voting in order to exchange perspectives on the project development and reach a decentralized decision as to its further growth. Regular type of voting can be used for that;

1. Mechanism of decentralized voting designed to change DAO’s functionality

- Software developers make mistakes, and some of them can be critical. Daox organizations are implemented by means of a delegatecall low-level function, which allows to delegate execution of a function to an external contract using its address. As of now, the main features of a Daox organization are implemented by 4 independent contracts (modules), each in charge of a specific functionality. With Module type of voting one can change the address of the contract that the call is delegated to; it allows to extend functionality of the organization and fix bugs;

1. Tap mechanism is substituted by decentralized ‘Withdrawal’ proposals (tranches) indicating a specific sum

- A solution suggested by Vitalik is great for teams of developers, however it limits widespread use of an ICO by projects with other objectives;
- In addition, the team of developers might need withdrawal of a large sum for marketing or operating costs;

1. Additional mechanism for protection against 51% attack

- The most important types of voting use quorum, which is a minimum number of tokens that should vote positively in order for the proposal to be accepted. So, the intruder will have to buy too many tokens in order to make an attack, which makes the whole idea difficult economically wise and even unprofitable;

**Where can I ask a question about using the source code?**

Feel free to ask any questions right in this topic or through github issues. For additional details you can also follow series of [How Daox Works](https://medium.com/daox/how-daox-works-part-1-a1d2a456cbe7) blogposts.

## Replies

**vbuterin** (2018-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/bulgakovk/48/1340_2.png) bulgakovk:

> The most important types of voting use quorum, which is a minimum number of tokens that should vote positively in order for the proposal to be accepted. So, the intruder will have to buy too many tokens in order to make an attack, which makes the whole idea difficult economically wise and even unprofitable;

I don’t think that this is sufficient. It’s definitely possible to buy up 51% of tokens of a given type and then start trying to expropriate the other 49%.

I recommend having some kind of “splitting” function so users have some way to protect themselves.

---

**bulgakovk** (2018-05-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I don’t think that this is sufficient. It’s definitely possible to buy up 51% of tokens of a given type and then start trying to expropriate the other 49%.
>
>
> I recommend having some kind of “splitting” function so users have some way to protect themselves.

The funds that are stored in Daox DAOs could be transferred either to the pre-defined Ethereum addresses of the team behind the startup, or to the token holders in case of the funds return. So, even if an attacker will manage to buy up 51%, the worst he could do is to keep declining all withdrawals proposed by the startup team. For that matter, there is a functionality that switches the DAO to the refund mode if no withdrawals were approved in a course of two months.

We were also considering the “splitting” function but since each DAO is built around the particular project, team, and brand there is no purpose of splitting away (to nowhere). Splitting is useful if a DAO is built around the idea instead of the concrete team though.

