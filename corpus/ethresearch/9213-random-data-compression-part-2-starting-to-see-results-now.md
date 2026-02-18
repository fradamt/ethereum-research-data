---
source: ethresearch
topic_id: 9213
title: Random data compression part 2 -- starting to see results now
author: Uptrenda
date: "2021-04-18"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/random-data-compression-part-2-starting-to-see-results-now/9213
views: 1163
likes: 0
posts_count: 5
---

# Random data compression part 2 -- starting to see results now

Hello everyone at Ethereum Research, a while back I spoke to you all about random data compression and how I believe it may be possible. I’ve since made considerable progress from that point, including getting to the point where I believe I can demonstrate my approach. Though my code is designed to run on a Spark cluster – I use 240~ cores for testing 1 / 61 completion of the algorithm which takes a while. In practice a full run of the algorithm would benefit from a larger cluster.

The link to the paper I wrote for my approach is here: [16 Apr, 2021 - An algorithm for random data compression](https://roberts.pm/index.php?p=article&path=rand&category=cryptography)

My attempt to give a simple el5:

1. Store data in 17 bit words in a golomb-coded set (GCS) – this has the same properties of a bloom filter but it’s smaller.
2. Entire algorithm is then based on recreating words stored in the set.
3. Make a list for each word filled by brute forcing every value in a 17 bit word at each offset. These are the candidates.
4. Write down the offsets in these lists to the correct word. These are the nodes.
5. Break down the nodes into lists of 8 elements. Inside these 8 element lists, break them into pairs.
6. Hash each pair, to make a hash list of four hashes.
7. Do proof-of-work on each hash, look for patterns that are highly unlikely. Find a nonce that makes the most unlikely pattern.
8. Store information about the nonce patterns in meta data with the nonce.
9. You can now use the meta-data to build a list of possible 8 element offset lists.
10. You write down the correct offset of the 8 element set you want.

I’ve defined a new algorithm for representing information in a probabilistic fashion that can be used to compress random data. It relies on using the unlikely prefixes in nonce patterns as heuristic filters to recreate indexes that serve as data pointers into a list of tables. Collisions are an expected property of the GCS – and the algorithm is all about reducing result sets in two main stages – the GCS candidates and the q set candidates.

People are going to ask me how this addresses the pigeon hole principle and the answer is that I don’t know. In my mind the GCS structure is a super-position that allows for multiple over-lapping pieces of data to be re-mapped to smaller keys. That’s an inherent properly of what a GCS allows. The collisions are resolved by addressing the indexes to the right words, and then the right list of index lists at the end. This bypasses the address-size restrictions with the counting argument. That’s how I visualize it… maybe I’m wrong though.

At the very least this heuristic algorithm can do things within space restrictions that I’ve never before seen with any other algorithm and I think this makes this a new approach that could be potentially useful. I don’t claim to have all the answers and parts of the paper might make no sense. I’d appreciate it if some smart people could give this a look though! P.S. will be writing basic how-tos for my code experiments on Github but you will need a small cluster to run them!

## Replies

**Uptrenda** (2021-04-23):

I’ve slowly been turning my experiments into a CLI program that will allow any 1 KB files to be re-arranged / compressed and decompressed. Hoping to get most of it done over the weekend. It will be a while before I can secure access to a cluster large enough to run my full proof though. I’ve only proven the general approach works by testing the heuristic algorithm for a q set and that it can be encoded in its reserved space. In reality, I also cheated there by skipping a step that would have made it 14 times as difficult, but statistically there’s no reason why that wouldn’t have worked, too.

My goal will be to get this all to run on Google Cloud using a spark cluster easily so people can verify my proof. I’ll need to give some idea of the cost too which I suspect will be a few hundred. But it’s worth it to prove that something ‘impossible’ has a practical approach that works. If people accept the general idea works then there may be enough interest to optimize this for a GPU implementation. Then, perhaps that would run on a single card?

---

**Uptrenda** (2021-05-02):

I’ve added measures for detecting and resolving collisions. The remarkable property of an algorithm like this is there can be multiple solutions for the same value so in the unfortunate case that a collision arises another pathway can be used. I’ve also added in a simple checksum feature which will help to steer away collisions, too. It will not be possible to prevent collisions entirely (they are a mathematical certainty of moving large ranges into smaller ones) but these measures help improve practicality.

I’m not able to do any more research until I secure a larger cluster. I’m aiming to acquire the resources to put together a 2048 core cluster and run the full compression and decompression cycle. But depending on luck – this may take quite a number of months. In the mean time, I’ll just be aiming to improve test coverage and quality of my code. So when I do get access to compute resources everything goes as smoothly as possible. That’s all for now.

---

**Mister-Meeseeks** (2021-05-03):

Have you considered just running on cheap elastic cloud VMs? A 2048 core preemptible cluster costs $13/hour on Google Cloud.

---

**Uptrenda** (2021-05-03):

Definitely worth considering. I’m impatient so I might end up running the software on Google Cloud for like a week~ (hopefully shorter). It’s expensive though, and if I owned the hardware myself I’d only have to pay like $100 AUD a day for electricity.

Edit: I think I will just use Google Cloud then as you suggest. The money to run it constantly for a week seems like a lot at first but trying to organize a cluster this large and maintain it for a single person… starts to look crazy. I see the advantages here. Thanks a lot

