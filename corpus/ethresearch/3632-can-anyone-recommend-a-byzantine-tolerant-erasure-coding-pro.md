---
source: ethresearch
topic_id: 3632
title: Can anyone recommend a Byzantine-tolerant erasure coding protocol?
author: kladkogex
date: "2018-09-30"
category: Consensus
tags: []
url: https://ethresear.ch/t/can-anyone-recommend-a-byzantine-tolerant-erasure-coding-protocol/3632
views: 1467
likes: 5
posts_count: 3
---

# Can anyone recommend a Byzantine-tolerant erasure coding protocol?

We have the following problem that may be interesting to other people:

1 There are N servers out of which less than 1/3N are Byzantine.

2  We want to save a file F to these servers, so that a client later can pull the file from the servers.

3 Ideally the client attempts to open N TCP connections in parallel to all of these servers and starts downloading  erasure coded segments.  Then nomatter what the bad guys do (they can fail to respond or respond with corrupt data), the client should be able to reconstruct the file and there should be no timeouts in the protocol

A trivial solution without erasure coding is to make N parallel attempts to pull the entire file from all of the servers,  but this will introduce lots of wasteful network traffic.

Ideally you ask each server for a verifiable erasure coded segment, and once you receive 2/3N segments you verify each of them and reconstruct the file while minimizing the  network traffic.

Does anyone know what is the most optimal algorithm/protocol for this?

## Replies

**vbuterin** (2018-09-30):

The client locally computes an erasure code of F, extending it to N chunks of size |F| * \frac{1.5}{N} each. The client sends a chunk to each server. The client also stores the hashes of each chunk locally. When the client needs to recover the file, it can ask each server for a chunk, download the chunks, verify each chunk against the hashes, and then recombine the file from the correct chunks.

There is also such a thing as error-correcting decoding (eg. using the [Berlekamp-Welch algorithm](https://en.wikipedia.org/wiki/Berlekamp%E2%80%93Welch_algorithm)), but IMO it’s overrated; using hashes to authenticate chunks will in many cases work just fine.

---

**MaxC** (2018-09-30):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> 2/3N segments you verify each of them and reconstruct the file while minimizing the network traffic.

Let R be the number of requests made for pieces of the file.

Let x be the number of requests that were incorrect in the experiment.

Let t be the threshold for correctness given by the  code, i.e the code admits t/R errors but no more.

t will probably be somewhere between 1/3 and 1/2 depending on the code.

You want to ensure P(x<t* R) =CDF-BIN(t*R;p=1/3) < 0.00001 or some other small threshold.

I think an optimal code can admit t=floor(n/2) errors and might be based on a hamming code? The Reed Solomon also has some threshold t of errors based on the size of the object you wish to encode and the redundancy in the code, but can’t recall what the bound is off the top of my head.

But authenticating against a hash makes more sense.

