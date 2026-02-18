---
source: magicians
topic_id: 15390
title: "Introducing: eth2-package - a tool for spinning up private testnets in a single command"
author: leeederek
date: "2023-08-09"
category: Magicians > Tooling
tags: []
url: https://ethereum-magicians.org/t/introducing-eth2-package-a-tool-for-spinning-up-private-testnets-in-a-single-command/15390
views: 852
likes: 5
posts_count: 1
---

# Introducing: eth2-package - a tool for spinning up private testnets in a single command

Hey everyone, I’m Derek from Kurtosis & I wanted to share the [Kurtosis eth2-package](https://github.com/kurtosis-tech/eth2-package), which is an environment definition for spinning up ephemeral, reproducible, private Ethereum testnets. This package comes out-of-the-box with Grafana & Prometheus and supports multi-node testnets in the cloud with any client combination you need.

This was written by the Ethereum Foundation to address the need for a private but full-feature testnet where protocol-level simulations could be run and tested. The Ethereum Foundation (EF) DevOps team has been using this for over a year now to simulate and test behavior at the network level ahead of hard forks like the Merge, Shapella, and now for Dencun (EIP4844). If folks are heading to ProtocolBerg in Sept, the EF team will be presenting their work on Kurtosis in a workshop!

Spinning up the network requires only the installed Kurtosis CLI, Docker, and a single command: `kurtosis run github.com/kurtosis-tech/eth2-package`. By default, this will bring up a network with Geth and Lighthouse clients, but this package natively supports all major EL and CL clients, including Reth!

Our roadmap includes adding Full MEV support via the Flashbots suite of products, the addition of more validator health monitoring tools, and extending support for longer-lived private testnets. For folks who want to build-their-own testnet using the composable pieces, check out our guide [here](https://docs.kurtosis.com/next/how-to-compose-your-own-testnet/#1-set-up-an-empty-kurtosis-package) on how to do so!

We welcome any and all questions and feedback & hope that this tool is useful for people in the community! ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)
