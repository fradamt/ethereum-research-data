---
source: magicians
topic_id: 7074
title: EmbeddedMultiCall (Multicall without onchain contract deployment)
author: sergio_lerner
date: "2021-09-17"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/embeddedmulticall-multicall-without-onchain-contract-deployment/7074
views: 1311
likes: 4
posts_count: 4
---

# EmbeddedMultiCall (Multicall without onchain contract deployment)

I created a Multicall code that can be used to collect information from several contracts (offchain) using eth_call() but with a single RPC call for all. This is similar to Makerdaos’ [Multicall](https://github.com/makerdao/multicall) but it doesn’t need the deployment of the Multicall contract onchain, and therefore you can modify it to gather other information.



      [github.com](https://github.com/Defi4Bitcoin/EmbeddedMultiCall)




  ![image](https://opengraph.githubassets.com/1ca6bec698dc5800737b199248dcafdc/Defi4Bitcoin/EmbeddedMultiCall)



###



Embedded MultiCall










You can find more information on how it works in the project readme.

If you want to contribute adding web3 interfaces (web3.js or nethermind), please do it with a PR.

## Replies

**sergio_lerner** (2021-09-17):

I made the repo public now (it was private by mistake)

---

**miohtama** (2021-09-18):

Out of curiosity: How does executing any inline code (not just this example) works for Ethereum JSON-RPC? What kind of code payloads are supported?

---

**sergio_lerner** (2021-09-19):

You can execute any payload. Your can simulate any transaction. You don’t need  to sign the transaction in order to pass it to eth_call()

