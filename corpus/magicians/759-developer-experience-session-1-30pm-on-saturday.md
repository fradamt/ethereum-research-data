---
source: magicians
topic_id: 759
title: Developer Experience Session - 1:30pm on Saturday
author: GriffGreen
date: "2018-07-17"
category: Protocol Calls & happenings > Council Sessions
tags: []
url: https://ethereum-magicians.org/t/developer-experience-session-1-30pm-on-saturday/759
views: 1224
likes: 1
posts_count: 3
---

# Developer Experience Session - 1:30pm on Saturday

These notes are a little disorganized. Its a random smattering of thoughts in the developer experience space, with a list of tools and a general wishlist at the end.

Notes:

Chatham house rules

Desired out come:

Next steps, what tooling do we need, best solutions to improve.

Status codes?

Prioritizing developers is important, could be part of apple’s success.

DX = Dev experience

Tooling, frameworks, languages.

Ethereum is at an inflection point and EWASM is a major piece

Why is smart contract writing important? Is it the core piece?

Smart contract writing is difficult, Solidity is a challenging language to work with.

On boarding people involves learning the language but also best practices and tooling.

Where is the line? Where do we limit people in the compiler?

Any language is going to be specialized to smart contract development.

Debugger? We need it! We use Remix to debug but it would be nice to have one tool to bring.

Would be nice to have an in remix editor.

What IDE’s do people use?

- Step  Debugging in remix
Truffle tests

Would be nice to have a matrix of different Tools? Can we have comparisons on different suites…

EthFiddle is a cool tool.

Are people building tools wasting their time if EWASM is coming?

There are just soooo many tools, we need to make a list to compare everything

React uses the power of defaults… maybe truffle or something can do that

Remix has a dapp.

webassembly ‘s app gives you a default to

Remix, and Play!!

Play will let people play with things

How do we follow the updates that happen that will break things

If someone wants to create a documentation systems for n00bs it would get funding.

Ethercamp had an IDE, it had a browser experience… VPS, AWS, Privatechain… the leads left and the project wasn’t well documented

DOCUMENTATION IS IMPORTANT

Sandbox ?

DAppNode and Remix

Needs to be there!!! - Running things in command line so that you can see the evm trace and the result without having to deploy it.

Truffle interprets things wrong sometimes.

The ecosystem is decentralized, truffle is a huge thing… we need hyper modular tools

Create react app combines a bunch of smaller tools.

Truffle doesn’t scale for large projects.

Solidity gas mapper turned to code coverage tool, if there is a revert on the tests you can see. The tools are on the

Sol-coverage is the tool

Assembly and Yule are better then solidity in some ways - the abiv2 generates yule code so we hand code in assembly. Writing in plain assembly in some ways is just more clear.

How important is it to have remix add other languages?

Source maps…. You can compute a bytecode

Viper is a future language with simple syntax… why are they not standardizing some things… it seems to be recreating everything…

What are you using now and what would you like to put on the wish list?

Tools you use:

- intellij, remix truffle
- atom, solidity,
- intellij, remix, truffle, solidity, i want a matrix
- vim,
- sublime, truffle, remix
- truffle remix
- atom, type script mocha, remix,
- atom, my own fork of some things, truffle, remix
- sol-c, mocha,
- emacs with solidity, remix, sol-c, truffle does wierd things, mocha,
- vscode on truffle and remix,

wish list

- support in IDE for atom and more features in Remis and easier options than infura, excited about dappnoe
- need a matrix of options to pick the stack
- create react dapp for devs, with different versions
- smaller modules
- modelling tools, turning legal contracts into smart contracts
- remix hangs with large contract, really fast test clients, fuzz testing and print lines in the console
- gas profilers
- compile time invariants (typ checking, checking for totality) better test framework, decentralized repo where you can play the github some of PRs and do code verification and all that.
- speeding up remix taking out features, create react version of remix as a dapp, where the source code has no frame works
- make a basic embeddable tool with a preview making it extensible (plugins) outside collaborators, can it work on mobile!??!?!
- starter projects

## Replies

**fubuloubu** (2018-07-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/griffgreen/48/408_2.png) GriffGreen:

> Viper is a future language with simple syntax… why are they not standardizing some things… it seems to be recreating everything…

Needs more explanation ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/griffgreen/48/408_2.png) GriffGreen:

> better test framework

I welcome all users: [GitHub - fubuloubu/pytest-ethereum](https://github.com/fubuloubu/pytest-ethereum/)

---

**theporpoise** (2018-07-19):

Hey!  I also responded on a reddit post, but wanted to let you know some of these things are in active development with support from the EF.

For “create react dapp for devs” and “starter projects” check out Browseth!

https://github.com/buyethdomains/browseth

We recently received a grant from the Ethereum foundation to build exactly that! And we already have a first version up that you can get a react app for ethereum connected on the blockchain in 5 lines from the command line:

Install @browseth/cli

yarn global add @browseth/cli

Create a simple site

browseth-cli create-simple-site

cd

Install dependencies and run

yarn

yarn start

We’re still in 0.1 version, and aiming to have a 1.0 by DevCon (although we may not finish that up until December, as specified in our Grant).

That’s it! Would love to know what you think, and we’re actively excepting PR’s for everything from hard code to community documentation. We also already have a docs page started here:

https://buyethdomains.github.io/browseth/

