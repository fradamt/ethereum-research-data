---
source: magicians
topic_id: 4810
title: "EIP-3030: BLS Remote Signer HTTP API Standard"
author: hermanjunge
date: "2020-10-09"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-3030-bls-remote-signer-http-api-standard/4810
views: 2659
likes: 2
posts_count: 2
---

# EIP-3030: BLS Remote Signer HTTP API Standard

Discussion thread for  [BLS Remote Signer HTTP API Standard](https://github.com/ethereum/EIPs/pull/3030/)

## Simple Summary

This EIP defines a HTTP API standard for a BLS remote signer, consumed by validator clients to sign block proposals and attestations in the context of Ethereum 2.0 (eth2).

## Abstract

A [validator](https://github.com/ethereum/eth2.0-specs/blob/dev/specs/phase0/validator.md) client contributes to the consensus of the Eth2 blockchain by signing proposals and attestations of blocks, using a BLS private key which must be available to this client at all times.

The BLS remote signer API is designed to be consumed by validator clients, looking for a more secure avenue to store their BLS12-381 private key(s), enabling them to run in more permissive and scalable environments.

## Replies

**raullenchai** (2022-09-14):

This is a useful proposal. But one thing that has to be considered is the latency that gets introduced during the process of remote signing, e.g., usually 200ms - 1000ms, which reduces the actual time that validator can spend on processing transactions/blocks. What are your thoughts here [@hermanjunge](/u/hermanjunge)?

