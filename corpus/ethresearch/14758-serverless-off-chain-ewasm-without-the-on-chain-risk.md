---
source: ethresearch
topic_id: 14758
title: "Serverless: Off-chain EWASM without the on-chain risk"
author: zdanl
date: "2023-02-05"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/serverless-off-chain-ewasm-without-the-on-chain-risk/14758
views: 1731
likes: 0
posts_count: 1
---

# Serverless: Off-chain EWASM without the on-chain risk

Would like to suggest Off-Chain XMLHTTPRequest capable [1] support to EWASM, seperate from Smartcontract execution, calling it Serverless or so

Should cost gas to deploy, but not to call. If that is too much computational tax, should be offloaded to WebWorkers, in part at least.

That’s all I think.

[1] [GitHub - deislabs/wasi-experimental-http: Experimental outbound HTTP support for WebAssembly and WASI](https://github.com/deislabs/wasi-experimental-http)
