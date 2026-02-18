---
source: ethresearch
topic_id: 6039
title: Another tool for interactive verification
author: augustoteixeira
date: "2019-08-27"
category: Layer 2
tags: []
url: https://ethresear.ch/t/another-tool-for-interactive-verification/6039
views: 1356
likes: 5
posts_count: 4
---

# Another tool for interactive verification

I would like to bring attention to a project that we have been developing at [Cartesi](https://cartesi.io)

We are building a strong platform for the scaling of computations on Ethereum, using interactive verification “à la TrueBit”.

The main contribution of our project is to replace the specialized virtual machines (such as EVM or WASM) with a more realistic architecture based on RISC-V. Our reproducible RISC-V emulator is able to boot a full fledged Linux operating system, so that developers can benefit from various languages, libraries, services and so on.

Our alpha release includes all the necessary infrastructure (both on-chain and off-chain) to handle interactive disputes. Take a look at our [GitHub page](http://github.com/cartesi)

All our software is open source and released under a very permissive license. We have designed our architecture to be modular, easy to integrate with and resilient to power and connection failures.

We are providing tools to assamble machines on-chain: insert-remove drives, boot, halt and read outputs. Moreover our design is modular and we offer optional economic tools to outsource verification. Moving forward, we plan to provide many other tools to facilitate development, such as integration with other scaling solutions for high transaction throughput.

Our vision is that DApps should be mainly developed in Linux, with only a few economic incentives written in Solidity. This way, the Web 3.0 will benefit from the existing infrastructure over which the Web 2.0 was built.

A more in-depth overview of the project can be found in [Medium](https://medium.com/cartesi/on-linux-and-blockchains-a955a49a84e1)

We are very much looking forward to input, criticism, questions and requests from the comunity! Here is the link to our [Discord channel](https://discord.gg/Pt2NrnS)

## Replies

**adlerjohn** (2019-08-28):

If I understand your model correctly, for a particular computation you need to supply 1) a VM specification and 2) input data. Where are these supplied? On-chain?

What applications do you see for your proposed technique? One-off expensive computations (*e.g.*, verifying Scrypt PoW), or long-running off-chain systems (*e.g.*, side chains).

---

**augustoteixeira** (2019-08-28):

Good point.

So, our first release is “barebones” with respect to data scalability, as you well observed. Nevertgeless, let us try to describe a possible application that could be implemented right away.

Syppose you create a game that contains a very convoluted logic, but the input from users is quite small (like a tower defense game). Then you could distribute the game code (large files) with your reference software, while user input goes on-chain.

In the near future we plan to integrate our software with some solution for the scalability of transactions, and in this case the number of possible applications is limitless.

---

**felipeargento** (2019-09-02):

I am very proud to be working on and contributing to this project, each day I get more and more excited by the possibilities that running a “linux on-chain” would grant us.

One of the main improvements that Cartesi brings, in my opinion, is a clear distinction between the application’s development and it’s financial incentives design. The current Ethereum infrastructure is phenomenal for building and coding these complex financial structures, which are paramount to almost any decentralized application, but it is also very lackluster when it comes to building the everyday aspects of applications.

By bridging this gap between Ethereum and full fledged operational systems we not only increase the scalability of computation but also potentially help onboarding a bunch of veteran developers that can start using their everyday normal software stacks to create a much wider array of dapps.

I dont want it to sound like I am just tooting our own horn (which I am, being a contributor and all), but I can’t state enough how excited the development of Cartesi makes me and how I feel like it can be a great contribution to the Blockchain ecosystem as a whole.

[@augustoteixeira](/u/augustoteixeira)  linked a lot of interesting resources that can be used by those without a very deep technical background. To better understand the project, I would recommend taking a look at the techpaper (for the brave and tech savvy):


      [cartesi.io](https://cartesi.io/cartesi_whitepaper.pdf)


    https://cartesi.io/cartesi_whitepaper.pdf

###

503.15 KB

