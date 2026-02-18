---
source: magicians
topic_id: 8289
title: Sharding-format blob-carrying transactions
author: vbuterin
date: "2022-02-14"
category: Magicians > Primordial Soup
tags: [sharding]
url: https://ethereum-magicians.org/t/sharding-format-blob-carrying-transactions/8289
views: 1755
likes: 5
posts_count: 2
---

# Sharding-format blob-carrying transactions

This thread is to discuss the sharding-format blob-carrying transactions pre-EIP:

https://notes.ethereum.org/@vbuterin/blob_transactions

## Replies

**tynes** (2022-02-28):

During ETHDenver, there was some good progress made on implementing this. See



      [twitter.com](https://twitter.com/protolambda/status/1495538286332624898)



    ![image](https://pbs.twimg.com/profile_images/1753297001842675713/qHUNZ634_200x200.jpg)

####

[@protolambda](https://twitter.com/protolambda/status/1495538286332624898)

  At @EthereumDenver we hacked together a full data-blob-transaction prototype! (a.k.a. mini-danksharding)

Data blobs are the first milestone towards full ethereum sharding, enabling rollups like @optimismPBC to grow 100x in capacity.

Here's a tweet thread about the prototype 🧵

  https://twitter.com/protolambda/status/1495538286332624898










The code contains a file that is responsible for creating a trusted setup, see [go-ethereum/cmd/kzg_dummy_setup/main.go at a922276f31f130a83493a0406bae345ec1e19324 · protolambda/go-ethereum · GitHub](https://github.com/protolambda/go-ethereum/blob/a922276f31f130a83493a0406bae345ec1e19324/cmd/kzg_dummy_setup/main.go)

The implementation of the code that generates the trusted setup is here - _github.com/protolambda/go-kzg/blob/master/setup.go (can only post 2 links per post so evading the linking). Its not super complex code, but I am curious about how this trusted setup could be expanded to be multiparty and also have a 1 of n security model, where there only needs to be 1 participant that doesn’t defect for the trusted setup to be secure. Is that possible and what does the math look like for that?

