---
source: ethresearch
topic_id: 6957
title: Looking to the Stars for RNG
author: machinehum
date: "2020-02-16"
category: Consensus
tags: [random-number-generator]
url: https://ethresear.ch/t/looking-to-the-stars-for-rng/6957
views: 1753
likes: 2
posts_count: 6
---

# Looking to the Stars for RNG

I had this idea a while ago, there have been some publications.


      ![image](https://static.arxiv.org/static/browse/0.2.8/images/icons/favicon.ico)
      [arXiv.org](https://arxiv.org/abs/1706.02276)


    ![image]()

###

Photons from distant astronomical sources can be used as a classical source
of randomness to improve fundamental tests of quantum nonlocality,
wave-particle duality, and local realism through Bell's inequality and
delayed-choice quantum eraser tests...








In theory some open source cheap hardware could be developed to watch stars and get a RNG, it may be possible for multiple parties all over the world to also get the *same* random number.

The trick would be validation, it doesn’t work on like a VDF where anyone can validate the RNG with a PC. Not sure how to work around this.

Just a though, I’ve been thinking lots about distributed RNG where multiple parties can generate the same number, interesting daydreaming topic.

## Replies

**dankrad** (2020-02-16):

This idea is probably possible. However, there are some challenges that make it difficult:

- You need an extremely robust randomness extractor, as the incoming signal is analogue and not digital. You still want everyone to agree on the same output with very high probability (say 10^{-15} or so failure rate) but at the same time it should be truly random – that’s hard
- Because of this requirement, the hardware to do that would probably have to be pretty high quality and can’t be cheap
- Finally, you need to consider how you will handle cloudy days …

---

**Greg** (2020-02-16):

Why not just have everyone generate a random string and hash it N times (where N is like 1 million), and then publicly commit to that hash?

Then you can have any subset of your network generate a random number together by each one revealing the previous hash, and then combining them. You can use those resulting hashes as seeds for some random number generation.

This technique can also be used for many other things, including HOTP (hash based one time passwords), discovery of friends based on hashed phone numbers, etc. but if you want to generate random numbers without worrying about entropy and anyone able to predict the next number, just use this.

You need to kind of gossip and aggregate the commitments X. And each time the nodes reveal the previous input X_n = *hash^(-1) (X)*, you have to verify that *hash^N*(*X_n*) = X, and then use that to generate your random keys.

The only snag here is knowing which nodes get to provide the input. Because some nodes may be offline, and some may not be. It’s best if the random number is a function of what nodes are in the set. And after a while you stop listening to new X_n and you broadcast the ones you heard, so everyone can sort of find a union of all those nodes, and use that as the seed for the next random number.

Since Ethereum already has a special “baton” it passes around, to the miner who solves PoW, or some special nodes found with PoS, then you can just have THOSE nodes collect the random numbers from some set R of other nodes, signed by those nodes, and publish this combination as the random number. The only thing is you have to somehow be sure R is not completely under the control of the miner to select, otherwise they’ll have control of that random number. This is the tough part, because whatever criteria you choose, it has to be flexible enough for R to contain at least a few nodes. But it can’t be so flexible that the miner can eventually select their favorite group R and collude.

In fact you can probably replace Kademlia with just a global routing table (add whoever joins into a giant table) and use these random numbers to select the group of computers is going to be doing consensus about a certain thing. As the random numbers change (similar to a HOTP) you migrate the shard to the new consensus group.

(That’s an alternative routing system we’re building at [intercoin.org](http://intercoin.org), alternative to Kademlia, because it’s faster. But less private, because you have to know everyone’s IP address, so a malicious adversary can DDOS all the nodes. And yes, some countries would probably do that. So this alternative routing system would only really be good for private blockchains.)

---

**machinehum** (2020-02-17):

RE: Cloudy days, good point. I think you would need a high enough density of the hardware all over the world,   to get good coverage.

RE: Expensive, maybe. TBD, section b talks about using colour. Which could be as simple as two motors, a photo diode, mag, gyro, and some optics. That could easily be less than 10$

---

**machinehum** (2020-02-17):

I think you might be talking about a commit / reveal scheme. I may be incorrect, but I believe this can be manipulated by an malicious actor not revealing the hash.

The idea with stars (and VFD’s) is it should be impossible to pre-compute any of the RNG to prevent actors with malicious intent manipulating the output.

---

**dankrad** (2020-02-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/machinehum/48/3086_2.png) machinehum:

> I think you might be talking about a commit / reveal scheme. I may be incorrect, but I believe this can be manipulated by an malicious actor not revealing the hash.

I think you’re right, that does sound like RANDAO. That scheme has been well explored and is the basis of the current beacon chain implementation, now we are trying to find something better than that.

![](https://ethresear.ch/user_avatar/ethresear.ch/machinehum/48/3086_2.png) machinehum:

> RE: Cloudy days, good point. I think you would need a high enough density of the hardware all over the world, to get good coverage.

Then it wouldn’t be trustless anymore – you would have to trust those who can currently see the sky to correctly report the randomness to you, and you can’t independently verify.

![](https://ethresear.ch/user_avatar/ethresear.ch/machinehum/48/3086_2.png) machinehum:

> RE: Expensive, maybe. TBD, section b talks about using colour. Which could be as simple as two motors, a photo diode, mag, gyro, and some optics. That could easily be less than 10$

The difficulty is that you need everyone to agree on the output. So for example, let’s say you can measure some arbitrary quantity that fluctuates between 0 and 200, and you take whether that quantity is less than ore more than 100 to be the one bit of your randomness.

Most of the time, this will work great and everyone will have the same bit, but what if the actual value is exactly 100? Due to measurement errors, some people will see it as less and some as more, so you won’t have agreement which would be very bad. So instead you will have to run some sort of randomness extractor like low-influence functions. That means you will need to measure a lot of functions to get enough bits for your randomness.

This is just my intuition that this will mean expensive hardware, I may be wrong.

