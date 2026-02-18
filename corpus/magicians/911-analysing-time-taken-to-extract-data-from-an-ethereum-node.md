---
source: magicians
topic_id: 911
title: Analysing time taken to extract data from an ethereum node
author: ankitchiplunkar
date: "2018-07-31"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/analysing-time-taken-to-extract-data-from-an-ethereum-node/911
views: 999
likes: 6
posts_count: 10
---

# Analysing time taken to extract data from an ethereum node

Reposting the discussion from [ethresearch](https://ethresear.ch/t/analysing-time-taken-to-extract-data-from-an-ethereum-node/2755/2) here.

We analyse the time-taken to extract data from an Ethereum node. Block time of the Ethereum mainnet is ~15 seconds, if certain data extraction functions take more than 15 seconds to pull data then a block explorer using these functions will fall behind the ethereum chain.

We take one such heavy function, which is used commonly in block explorers to access the internal transactions, and demonstrate that if gas used increases to more than 12 million units, getting internal transactions will take greater than 15 seconds and the block explorers will start lagging behind the main chain. This means that **we should constraint gas limit to 12M**, for a block explorer to easily follow the mainnet.

The following [notebook](https://github.com/analyseether/research/blob/master/data_extraction_regression/data_gathering.ipynb) can be used to rerun the analysis.

## Key findings:

1. Even at the current 8M gas limit we sometimes overshoot the 15 second time limit.
2. The time taken to extract transaction traces depends on complexity of the contract codes and gas used in the block.
3. If gas used increases to more than 12M then we would consistently start hitting this time limit.
4. The above value of gas limit assumes that transactions in the block are not complex contract calls.
5. It is possible to find specific OPCODE’s which might create complicated contracts making the extraction exceed the time-limit at lower gas limits.
6. One method to bypass this bottleneck is developing Ethereum nodes optimized in data-delivery.

## Presentation:

## How to rerun the notebook

1. Have an archive node synced upto 5M blocks.
2. Install python3
3. Clone the research repo with notebook
4. Install dependencies from requirements.txt: $ pip install -r requirements.txt
5. Open the notebook using: >>> jupyter notebook

## Questions:

Tweet to @AnalyseEther

## Replies

**ligi** (2018-07-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ankitchiplunkar/48/581_2.png) ankitchiplunkar:

> One method to bypass this bottleneck is developing Ethereum nodes optimized in data-delivery.

maybe replacing RPC with GraphQL might be an option. There was a interesting talk about this at dAppcon: https://twitter.com/dappcon_berlin/status/1017436965803909120

---

**ankitchiplunkar** (2018-07-31):

[@ligi](/u/ligi) Can you provide a video link to this talk/workshop?

To my understanding, EthQL uses JSON-RPC to feed data in its GraphQL indexer. https://github.com/ConsenSys/ethql/blob/13ee8107e2b8ba92a5f26ec498bc10f0cce7c0f2/src/config.ts#L16.

Keeping the above analysis still valid, since the bottleneck is introduced due to JSON-RPC calls.

---

**ligi** (2018-07-31):

looks like this video is not yet released - they are still in the process of cutting. You can find the videos here: https://www.youtube.com/channel/UCruCCeCNWBAM7JI-xAMtXpQ/videos

Yea - in the end the detour over json-rpc needs to vanish in the end - but it can be a nice PoC as it looks that GrapQL can reduce overhead nicely for this use-case.

---

**tjayrush** (2018-08-01):

The bottle neck is not the RPC calls per-se. It’s the shape of the data and the fact that the data is an append-only time-ordered log. GraphQL (or any scraper for that matter) must convert that time-ordered log into an indexed database. This means it must extract not only all the blocks and all the transactions but all the traces (internal messages or internal transactions) as well. Since the traces are not physically stored on the hard drive, they must be re-generated when requested (via RPC or IPC) or, as noted, by modifying the internals of the node.

Not to speak for AnalyzeEther, but once the data is extracted, I’m sure most modern databases are more than capable of delivering the data. The issue is in the extraction and indexing.

---

**ankitchiplunkar** (2018-08-03):

As [@tjayrush](/u/tjayrush) said, getting the data out of a node is the issue. After the data is extracted and indexed and modern database, GraphQL, PostgreSQL or MySQL would return the data at speed.

---

**dontpanic** (2018-08-03):

The way it is done with [etherhub.io](http://etherhub.io) is to export blocks into a mongoDB and process data from there. I’ve had similar experience with hyperledger fabric and couch db, and Microsoft workbench(parity poa) with azure sql. The node is used for write operations, the db is used for trivial reads and analytics.

---

**ankitchiplunkar** (2018-08-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dontpanic/48/98_2.png) dontpanic:

> export blocks into a mongoDB

[@dontpanic](/u/dontpanic) the above analysis demonstrates that the process of extracting trace data from a node can take more than 15 seconds for a block.

---

**dontpanic** (2018-08-05):

export of raw blocks  is done in a  synchronous manner, not at the time of query. a script is constantly calling the node for the ‘latest’ block and if it is > the last block store it is processed and appended in the db. traces and lookups  only happen in the mongodb stored data so you dont have the latency of the node. nodes are processing a lot of other info besides the requests, using mongo or couch makes dynamic reads more efficient than leveldb of a node.

separate schema store block data & transactions.

---

**tjayrush** (2018-08-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ankitchiplunkar/48/581_2.png) ankitchiplunkar:

> the above analysis demonstrates that the process of extracting trace data from a node can take more than 15 seconds for a block

Do you have a sense for the percentage of such blocks there are? Does this occur for 1% of blocks, 10%, 20%? I’m sure it happens for some blocks, but I wonder how many?

Also, I see you’re using the `w3.parity.traceReplayBlockTransactions`.  Have you tried other methods? (We use Parity’s `trace_transaction`.) I wonder if that affects the performance.

