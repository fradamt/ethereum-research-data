---
source: ethresearch
topic_id: 20167
title: Ethereum + Industry of Integrations (IOI)
author: knev
date: "2024-07-28"
category: Layer 2
tags: []
url: https://ethresear.ch/t/ethereum-industry-of-integrations-ioi/20167
views: 2686
likes: 4
posts_count: 7
---

# Ethereum + Industry of Integrations (IOI)

(This is my first post here, so I hope that I have not missed any protocol)

I’ve been integrating systems using IPSME, which lead to the Industry of Integrations concept [IOI](https://root-interface.se/IOI). IPSME defines an evolutionary architecture for integrations developed by the community.

Demos of my work can be found here:



The concept of the IOI is such that: if any two system interfaces (APIs) are known and accessible, that (via the conventions of [IPSME](https://ipsme.dev)) a translation can be created integrating the two APIs …​ And! That that translation can be monetized.

The Ethereum blockchain is often linked to Oracles or Oracles services that are off-chain. AFAIK, Ethereum already support a pubsub (the basis for IPSME). The question is then if an IOI can be created within the Ethereum network. Namely, can integrations to external services be smart contracts so that integrations are on-chain and are re-usable by other developers. Is it possible that smart contract integration contains the logic so that the original developer can possibly monetize off building the integration. If the integrations can be reused, then the complexity for integrating with external systems can be reduced through the property of transitivity i.e., if A integrates with B and B with C, then A is integrated with C.

I’m interested in doing exploratory research to see if IOI can be applied to Web3. I would like to ask here:

- Does this idea sound feasible with the Ethereum network?
- Are smart contacts powerful enough for protocol communication?
- Is it correct that Ethereum supports pubsub and can it be utilized for this?
- Would this idea alleviate the need for Oracle services/networks?

I’m looking forward to your feedback.

## Replies

**MicahZoltu** (2024-07-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/knev/48/17256_2.png) knev:

> if any two system interfaces (APIs) are known and accessible

I think the big problem you are going to run into is the bolded bit.  Nothing off-chain is *directly* accessible from on-chain, so you need a mechanism for getting that off-chain data on-chain.  There are many proposed solutions to this, but they all have their own problems.

If you are just talking about two contracts both on Ethereum (each with their own API), then you definitely can integrate them and lots of people do so.  The caveat here is that everything is public so you cannot monetize via trade secrets, IP, etc. in a purely on-chain environment.  At best you could obfuscate your code, but this just delays replication at best (and often not by much).

---

**knev** (2024-07-29):

Thank you for your response.

My idea behind this is this. If an an off chain service has an API implemented in X. Have a smart contract (that follows the IPSME conventions) that speak protocol X read the data and put it on-chain. Is this naive?

Can you name a few of these proposed solutions you mentioned, so that I can read up?

---

**MicahZoltu** (2024-07-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/knev/48/17256_2.png) knev:

> Have a smart contract (that follows the IPSME conventions) that speak protocol X read the data and put it on-chain.

This is the part that isn’t possible without introducing some kind of oracle system.  Here are a handful of previous ideas that have been explored:

1. TLS Notary.  You generate a proof that some content was fetched over a TLS connection with a particular certificate holder.
2. Data sources publish data directly on-chain.
3. Data sources sign their publications with a signature that can be verified on-chain, then anyone can bring the data on-chain and the contract just validates the signature.
4. A trusted third party publishes the data on-chain that they grabbed from an off-chain source and says “trust me bro”.
5. Same as (4) but with a group of people instead of one person (multisig), “trust us bro”.
6. One person publishes the data on-chain, and others can dispute its authenticity.  Others can then dispute that and it goes back and forth until some “final oracle” is reached that makes a decision (final oracle is some other system).
7. All possible results are virtually “published” on-chain, and every user decides what they believe to be in line with reality and follows the fork that matches that.  Assumption is that people will pick the fork that aligns with reality because it isn’t useful to play in a sandbox by yourself.

---

**knev** (2024-07-31):

Thank you so much!

> This is the part that isn’t possible without introducing some kind of oracle system.

Again, pardon my naivety. If a smart contract is triggered, what prevents it from fetching data and publishing it on-chain? Is it because the way the signatures work?

---

**MicahZoltu** (2024-07-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/knev/48/17256_2.png) knev:

> If a smart contract is triggered, what prevents it from fetching data and publishing it on-chain?

Contracts execute within the Ethereum virtual machine, which needs to be in consensus across thousands of nodes (all must agree *exactly* on the output) and execute all contracts in a block within milliseconds.  Thus, there is no access to external resources outside of the EVM.  The only input into a contract’s logic is network state, some block information (like timestamp and block number), and the input into the contract.

---

**knev** (2024-07-31):

Thank you. Now I have enough to mull over.

