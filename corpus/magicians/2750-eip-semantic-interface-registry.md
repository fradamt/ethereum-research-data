---
source: magicians
topic_id: 2750
title: "EIP: Semantic Interface Registry"
author: gh1dra
date: "2019-02-26"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-semantic-interface-registry/2750
views: 756
likes: 0
posts_count: 1
---

# EIP: Semantic Interface Registry

Hi all,

Would love some feedback on a semantic registry EIP I’ve been working on the past couple months. It was heavily inspired by the work done here: [ERC-1456 - Address Metadata JSON Schema](https://ethereum-magicians.org/t/erc-1456-address-metadata-json-schema/1491)

But adds a validation layer that dapp developers can use with defined ontologies for their contracts. Expands support of contract metadata to include Semantic Web formats like RDFS/JSON-LD. Eventually would be interested in robust ways to actually cache this data and run SPARQL queries for governance model simulations.

https://github.com/ethereum/EIPs/pull/1780
