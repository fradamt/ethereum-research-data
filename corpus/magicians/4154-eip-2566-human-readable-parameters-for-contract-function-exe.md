---
source: magicians
topic_id: 4154
title: EIP 2566 - Human-Readable Parameters for Contract Function Execution
author: jstoxrocky
date: "2020-03-23"
category: EIPs
tags: [json-rpc]
url: https://ethereum-magicians.org/t/eip-2566-human-readable-parameters-for-contract-function-execution/4154
views: 2454
likes: 1
posts_count: 1
---

# EIP 2566 - Human-Readable Parameters for Contract Function Execution

Hey all, hope everyone is staying safe out there! I had some ideas about human readable parameters for contract function execution. As a new user to Ethereum Magicians I am not able to post a topic with more than one link or image so I am linking to the [EIP’s github issue](https://github.com/ethereum/EIPs/issues/2567) for the full description.

## Simple Summary

This EIP proposes a new Ethereum RPC method `eth_sendTransactionToContract` that accepts a human readable version of `eth_sendTransaction`'s `data` field. This change will allow ProviderWallets (hybrid Ethereum provider / wallet software) like Metamask and Geth to display confirmation screens with human readable details of a function call to a contract.

## Abstract

When a dapp prompts a user to execute a smart contract function via a ProviderWallet, confirmation screens displayed in the ProviderWallet layer cannot display the human readable details of the function to be called and the arguments to be passed. This is because the Ethereum RPC method used for contract function execution (`eth_sendTransaction`) accepts information about what function to call in a non-human readable (and non-recoverable) format. As such, when a ProviderWallet receives this non-human readable information from a dapp, they are unable to display a human readable version since they never received one and cannot recover one from the data.
