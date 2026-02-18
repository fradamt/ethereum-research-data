---
source: ethresearch
topic_id: 11433
title: Light-Client Custom Token Creation Proposal
author: jeyakatsa
date: "2021-12-06"
category: Architecture
tags: []
url: https://ethresear.ch/t/light-client-custom-token-creation-proposal/11433
views: 2213
likes: 2
posts_count: 4
---

# Light-Client Custom Token Creation Proposal

### Light-Client Custom Token Creation Proposal

#### Why can’t we create custom tokens on top of Light-Clients?

As it seems, the next evolution (as relating to Ethereum 2: POS Consensus) will be mobile-devices in regards to running the necessary nodes needed to maintain the ecosystem, and Light-Clients are the best arbiter to such a proposal.

As I’ve gathered, the best way to create custom tokens on top of Ethereum is to avoid dealing with *Light-Clients*, ***but***, Light-Clients are built to interact with mobile phones (and other minimal devices) thus:

> building the Infrastructure to create Custom Tokens & Tokenomics on top of Ethereum 2’s Light-Clients

…seems like the next best evolution to further expand Ethereum and its ecosystem.

> The beautiful aspect of creating such custom tokens on top of Light-Clients is that such tokens can be created with multiple languages (Typescript, Go, Rust, Java, Nim, C#, etc) as opposed to learning a new language just to create an Ethereum token.

This I believe will onboard a plethora of new developers into the Ethereum ecosystem as *the Research and Development needed to create such tokens in multiple languages has already commenced via the light-client building process:*

#### Live Light-Clients:

- Typescript  Light Client (for Lodestar)

#### Needed Light-Clients:

- Go Light Client (for Prysm) <~ (vacant link to-be-assigned)
- Rust Light Client (for Lighthouse) <~ (open for collaboration)
- Java Light Client (for Teku) <~ (open for collaboration)
- Nim Light Client (for Nimbus) <~ (vacant link to-be-assigned)
- C# Light Client (for Cortex) <~ (vacant link to-be-assigned)

This will most likely be a multi-year pronged experiment & project and is ever-so evolving as more information is gathered.

I am very open to more thoughts, ideas and collaborations.

## Replies

**ralexstokes** (2021-12-09):

glad to see you engaging w/ ethresear.ch ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=10)

this post seems to confuse how you interact w/ the network (full vs. light client) with what you use the network to do (make a token, etc.).

unless i am misunderstanding your proposal (perhaps to add some kind of incentivization layer to facilitate a light client ecosystem?), all types of clients have some sort of means for accessing the ethereum network and based on how many resources they dedicate to this task, they will be able to take advantage of certain guarantees stemming from the underlying trust model. as a light client you can access the same set of data as e.g. a full client but you just verify less of that set of data (and likely are only processing/manipulating a small subset of the full set). so it doesn’t make sense to talk about a separate network for just light clients that somehow maintains a token ledger.

feel free to clarify if i’m misunderstanding or ask for my to clarify if i’m not clear enough!

---

**jeyakatsa** (2021-12-09):

Hi [@ralexstokes](/u/ralexstokes) ! Thanks for the response!

This proposal is still very early in its phase as all the data/research on how to oversee this project is still being gathered.

I was thinking of creating a network on top of each client (I.e a Java Token Creation network, a Rust Token Creation network, so on and so forth).

But by the way it’s looking, it seems like I may have to start articulating entire full notes (clients) in order for a new Token Creation network to function sufficiently.

I’ll be publishing a new paper [about this new proposal] (with as much detail gathered about this topic in a few weeks), and let you know once it’s published.

---

**jeyakatsa** (2021-12-19):

Hi Alex! Hope you’ve been well man. I just completed a more in-depth proposal here: [New-ERC Token Proposal](https://ethresear.ch/t/a-new-erc-token-proposal/11540).

