---
source: magicians
topic_id: 1028
title: Ethereum stratum mining protocol as a standard
author: jpitts
date: "2018-08-12"
category: Magicians > Primordial Soup
tags: [mining]
url: https://ethereum-magicians.org/t/ethereum-stratum-mining-protocol-as-a-standard/1028
views: 5285
likes: 1
posts_count: 2
---

# Ethereum stratum mining protocol as a standard

Stratum is used for mining pools.

NiceHash’s specification for Ethereum stratum mining protocol v1.0.0: [Specifications/EthereumStratum_NiceHash_v1.0.0.txt at master · nicehash/Specifications · GitHub](https://github.com/nicehash/Specifications/blob/master/EthereumStratum_NiceHash_v1.0.0.txt)

> Ethereum does not have official stratum protocol. It supports only GetWork, which is very resource hoggy as miners need to constantly poll pool to obtain possible new work. GetWork thus affects performance of miners and pools. Due to demand for more professional Ethereum mining, several versions of “stratum” for Ethereum emerged. These “stratums” utilize GetWork on server side (pool side) to obtain work, which would be fine, if careful considerations and precautions were taken when creating such protocols.

NiceHash May 2016 announcement: [Stratum mining protocol for Ethereum — Ethereum Community Forum](https://forum.ethereum.org/discussion/7091/stratum-mining-protocol-for-ethereum)

Bitcoin’s Stratum Protocol: [Stratum mining protocol - Bitcoin Wiki](https://en.bitcoin.it/wiki/Stratum_mining_protocol)

Bitcoin’s getwork Protocol: [Getwork - Bitcoin Wiki](https://en.bitcoin.it/wiki/Getwork)

## Replies

**chfast** (2018-08-12):

The EthereumStratum is not the one used the most, but is the only one with any documentation.

I proposed a change to the version 1.0.0: https://github.com/nicehash/Specifications/issues/5.

