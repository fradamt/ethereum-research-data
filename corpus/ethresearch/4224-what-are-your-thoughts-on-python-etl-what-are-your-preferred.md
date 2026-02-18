---
source: ethresearch
topic_id: 4224
title: What are your thoughts on Python ETL? What are your preferred methods of aggregating data from Ethereum chain?
author: tucker-chambers
date: "2018-11-12"
category: Data Science
tags: []
url: https://ethresear.ch/t/what-are-your-thoughts-on-python-etl-what-are-your-preferred-methods-of-aggregating-data-from-ethereum-chain/4224
views: 3060
likes: 2
posts_count: 6
---

# What are your thoughts on Python ETL? What are your preferred methods of aggregating data from Ethereum chain?

Hi there,

I have used the Python Ethereum ETL to do some network analyses and other data projects. It is a great project, but I wanted to know if anyone has different preferred methods. Python ETL does not  (currently) support internal transactions and some other features, so I have interacted directly with the JSON RPC package via a geth node.

https://github.com/blockchain-etl/ethereum-etl

Thanks.

## Replies

**quickBlocks** (2018-11-12):

You can check out QuickBlocks.  It’s C++ code, but it extracts all the data (including internal transactions) and has a built in cache, So the second time you query, it’s way faster.

---

**tucker-chambers** (2018-11-13):

Nice, thank you. Appreciate the tip.

---

**medvedev1088** (2018-11-15):

Hi there. I’m the author of Ethereum ETL. You can export internal transactions with the export_traces command https://github.com/blockchain-etl/ethereum-etl#export_traces. Only works with Parity. For geth traces use https://github.com/blockchain-etl/ethereum-etl#export_geth_traces

You can also query all internal transactions in the public BigQuery dataset. Here is how you can retrieve balances for all addresses https://medium.com/google-cloud/how-to-query-balances-for-all-ethereum-addresses-in-bigquery-fb594e4034a7.

---

**tucker-chambers** (2018-11-15):

[@medvedev1088](/u/medvedev1088) Thank you for the response. I really love the python ETL package and will look into those commands.

---

**ChristopherLey** (2023-02-09):

If your interested I wrote a python package for access block data through etherscan (you just need an api key) heres the github its call [pyetherscan](https://github.com/ChristopherLey/pyetherscan)

