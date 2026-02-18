---
source: ethresearch
topic_id: 2755
title: Analysing time taken to extract data from an ethereum node
author: ankitchiplunkar
date: "2018-07-31"
category: Data Science
tags: []
url: https://ethresear.ch/t/analysing-time-taken-to-extract-data-from-an-ethereum-node/2755
views: 2144
likes: 3
posts_count: 4
---

# Analysing time taken to extract data from an ethereum node

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
3. Clone the repo
4. Install dependencies from requirements.txt: $ pip install -r requirements.txt
5. Open the notebook using: >>> jupyter notebook

## Questions:

Tweet to @AnalyseEther

## Replies

**Ethernian** (2018-07-31):

[@ankitchiplunkar](/u/ankitchiplunkar), a lot of thanks for your job done!

IMHO, [ethereum-magicians](https://ethereum-magicians.org) is more suitable forum because it is more “engineering oriented”. It would be great if you could publish your post there too.

Please have a look at the discussion about [modifying the TLOAD opcode for reading from other contracts’s storage](https://ethereum-magicians.org/t/eip-transient-storage-opcodes/553/18). Would it help to avoid unneccessary serialization in internal calls and thus lower the execution load?

---

**ankitchiplunkar** (2018-07-31):

[Done](https://ethereum-magicians.org/t/analysing-time-taken-to-extract-data-from-an-ethereum-node/911) ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**nootropicat** (2018-08-01):

It doesn’t seem to be a serious problem because it’s easily parallelizable. Divide the work load among n nodes (or just verification threads) and each node only traces 1/n of all transactions.

