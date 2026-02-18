---
source: ethresearch
topic_id: 2367
title: "University project: visualization of periodic transactions on Ethereum"
author: menxit
date: "2018-06-27"
category: Applications
tags: []
url: https://ethresear.ch/t/university-project-visualization-of-periodic-transactions-on-ethereum/2367
views: 1113
likes: 2
posts_count: 1
---

# University project: visualization of periodic transactions on Ethereum

Hi, I’m a computer engineering student and this semester I had to design a “big data” project. I decided to analyze periodic transactions on Ethereum blockchain.

I downloaded the entire Ethereum blockchain and then I analyzed it using Spark.

The idea is to take all the transactions of each address, then I sort the blocks of each transaction, I calculate the difference between each block and finally I calculate the standard deviation of this array. In that way when an address has a low standard deviation, it means that, that address creates periodic transactions.

Now I’m visualizing the results and I’m a bit surprised.

Legend

Standard deviation: it indicates how the transactions are periodic. The more this value is low, the more the transactions are periodic.

Period: mean number of blocks between each transactions of an address

Number of blocks: number of blocks that contains transactions of the current address

Value: the whole value transacted by an address

Gas usage

As you can see there are a lot of address that received exactly 101 Ethereum, by a lot of little periodic transactions. Can you help me to understand what kind of activity these address were doing?

https://etherscan.io/address/0xc62a264EDc11B6da5D423A15445862edb72fDf15

https://etherscan.io/address/0xA8F72E52E80827Cb18bAb1bEC9eBeEc50F445aeD

https://etherscan.io/address/0xaE3182Ab2e21E005f39C0e6b4c0E3a08c1aFD5Bf
