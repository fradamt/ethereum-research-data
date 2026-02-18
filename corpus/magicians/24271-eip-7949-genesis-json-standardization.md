---
source: magicians
topic_id: 24271
title: "EIP-7949: genesis.json standardization"
author: jflo
date: "2025-05-19"
category: EIPs > EIPs informational
tags: [configuration]
url: https://ethereum-magicians.org/t/eip-7949-genesis-json-standardization/24271
views: 98
likes: 1
posts_count: 1
---

# EIP-7949: genesis.json standardization

Discussion thread for a new EIP that offers an optional standard for the network genesis file.

There are a number of outstanding EIPs that are unable to refer back to the cannonical way to define a genesis, because it does not exist. Examples include:


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7840)





###



Include a per-fork blob parameters in client configuration files











      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7892)





###



Defines a mechanism for scaling Ethereum’s blob capacity via specialized hard forks that modify only blob-related parameters.











      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7910)





###



A JSON-RPC method that describes the configuration of the current and next fork










etc.

I propose doing this in an iterative fashion, adopting a json schema that defines the status quo, with the expectation that it would be built upon for future improvements to genesis management. Concepts like:

Named EIPs in the protocol schedule

Initial state provided outside of json, for large pre-states

Deprecation of older features

Are all popular among client devs, and should be pursued once a baseline standard is established.
