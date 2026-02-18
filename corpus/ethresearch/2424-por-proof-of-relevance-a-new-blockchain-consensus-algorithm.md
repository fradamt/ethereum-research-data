---
source: ethresearch
topic_id: 2424
title: PoR ( Proof of Relevance ) - A New Blockchain Consensus Algorithm
author: ninanoo
date: "2018-07-03"
category: Proof-of-Stake > Block proposer
tags: [proposal-commitment]
url: https://ethresear.ch/t/por-proof-of-relevance-a-new-blockchain-consensus-algorithm/2424
views: 4299
likes: 1
posts_count: 3
---

# PoR ( Proof of Relevance ) - A New Blockchain Consensus Algorithm

Hello, I introduce a new blockchain consensus algorithm, **PoR ( Proof of Relevance )**.

https://github.com/ninanoo/PoR

This algorithm, based on computational complexity theory, can solve many problems of the current blockchain.

I hope this algorithm will be discussed and improved with the people who study and develop the blockchain.

## Replies

**mattisstenejohansen** (2018-07-05):

Hello,

Here are my notes (questions, rather, to create discussion) on the occurring concerns and issues I found regarding the proposed algorithm. Note that I skipped some of the paragraphs for the sake of time. I assume that the math is correct as I have not had the time to formally go through it.

For anyone else reading, the complete paper regarding the algorithm is available [here](https://github.com/ninanoo/PoR).

> “The relevance is obtained from the proprietary information of each block between adjacent blocks. The relevance can also be created from the work of PoW or the stake of PoS.”

- Is the algorithm defining relevance based on both ‘proprietary information’ AND the work of PoW / stake of PoS? If so, does that imply that the algorithm is ‘built upon’/requiring another PoW/S algo?
- Assuming the above is true: Why? Is there a need for a PoR if we already have an implemented, functional PoW/S?

> It uses a hash chain of Bitcoin, but has a dual chain structure such as Bitcoin-NG. There are a key block chain and an authentication block chain linked each other. In the key block chain, a candidate that can generate an authentication through consensus is registered. In the authentication block chain, the authentication for a ledger is registered.

- What is the reason for a dual-chain design? Would it not be possible to perform both tasks (“generate an authentication” and “register authentication for a ledger”) on a single chain?
- If the algorithm requires a dual-chain architecture, assuming you would want this algorithm to be applied to Ethereum, wouldn’t that require a lot of restructuring of the whole blockchain (aka hard fork)?

> With the use of a dual chain, the registered candidate can generate a real authentication after a very long time and there is also competition at that time.

What is meant by this? Is ‘the registered candidate’ a normal network node? What is a “very long time”?

> Relevance is used for competition to be registered as a candidate to generate an authentication. Reverse relevance is used for competition to create real authentication. Both competing situations are competition for time based on relevance and they are all for personal benefit. This prevents problems such as ‘nothing at stake’.

- “Candidate to generate an authentication” - if I’ve understood this correctly, is this (a ‘candidate’) to be compared to an EOS-style dPoS block producer?
- Being ‘all for personal benefit’ will very likely open up for malicious incentives.

> It is not the computational complexity that simply solves the hash, but there are numerical parts related to the operation of the algorithm such as many candidate blocks or very large threshold value, and they are all designed based on computational complexity theory. As a result, all attacks on the algorithm are probabilistically impossible

- That attacks on the algorithm being “probabilistically impossible” may not be true.

The words ‘proprietary information’ is used a lot throughout the proposal:

> Proprietary information may include memories that can be forgetful or possessions that can be lost, such as passwords or hardware tokens, and this information can be linked with your wallet. As an alternative to this, proprietary information such as biometric information can be used without risk of loss.

- As previously mentioned, “the relevance is obtained from the proprietary information of each block”, and above it suggests that ‘proprietary information’ is rather personal (such as passwords, biometrical info, and the alikes). Should such data be (i) publically available, (ii) stored permanently, and (iii) used to determine the next block?
- Assuming one need the blocks to be determined by its relevance to personal data stored on the previous block, how does the data (‘proprietary information’) of the previous block have any relevance/affect on what transactions should be included in the next block (if we’re talking transactions, which I would assume). This would be a huge privacy issue as well as being irrelevant.
- The solution would be encrypting all the data, but then it would be hard for nodes on the network to ‘validate’ the ‘relevance’.

> If you can not remember this information or you lose it, you can lose your ownership for that block forever. As an alternative to this, proprietary information such as biometric information can be used without risk of loss.

- “you can lose your ownership for that block forever” - what ownership? No one owns the blocks, and thus “loosing” ownership would not be possible, as everyone/no one owns them.
- Loosing biometric information would not be possible unless one physically looses a biometric tool (your eye, finger, etc.  ) - if you “lost” the block (e.g. can’t find the block hash corresponding to your info), you could simply upload them again to a new block.

Please correct me if I interpreted the paper wrong or missed some info.

Lastly, quick question: what software did you use to create the blockchain architecture diagram? It looks cool.

---

**ninanoo** (2018-07-06):

Hello.

I am going to have English epidemic these days.

The following is a reply to a question in r/ethereum of reddit.


      ![](https://ethresear.ch/uploads/default/original/3X/e/1/e1ae42106c51c881c83b6e2219e4b0c9d2aa617d.png)

      [reddit.com](https://www.reddit.com/r/ethereum/comments/8v92qc/por_proof_of_relevance_a_new_blockchain_consensus/)





###










```auto
A pool for a very large number of candidate blocks to issue the authentication is operated.
The blocks in the pool are also connected by a hash chain.
Mathematical techniques such as exponential distribution and computational complexity theory are used in consensus to be registered in this pool.
These techniques make it impossible to falsify an already confirmed authentication, and authentication is issued in real time to the extent that network bandwidth is supported.
In addition to consensus to be registered in the pool, blocks also compete in issuing authentication.
Due to this competition, problems such as 'nothing at stake' do not occur.
Due to the use of dual chain, authentication to the ledger is deterministic and problems such as double spending do not occur.
After a block is added to the pool, it takes a very long time to issue the authentication.
The block can issue authentication when it wins all the competition that lasts that long time.
This long time consensus minimizes localization problem.
There is only one reward for the participation of a majority of legitimate users.
This is the basic function provided by this algorithm and there is proprietary information that is separate from this.
You can find out about the proprietary information at the link below.
Depending on what the proprietary information is used as, another characteristic may be given to the algorithm.
The work of PoW may be used or the stake in PoS may be used.
```

As mentioned at the end of the article above, the proprietary information has not yet been researched and is only about the future directions.

First of all, I am also looking for ways that this algorithm can be applied to Etherium.

But, from the conclusion, I have not found yet.

One of the easiest ways to use stake as proprietary information is as follows.

Below is the current expression.

 \displaystyle r = \sum_{n=0}^{c-1} {2^{m_n}} {a^{-\frac{n}{c}}}

Below is a modified formula for stake.

 \displaystyle r = \sum_{n=0}^{c-1} {m_n} {a^{-\frac{n}{c}}}

Since self relevance calculation has to change when proprietary information changes, `2^m` is replaced by `m`.

`m` is the stake of each user who wants to be a candidate block.

This is a simple structure that all users compete to become a candidate block with their own stake.

I posted here to look for ways together to avoid the hardfork.

Etherium already has a lot of great developers.

I do not want developers to be more confused by the new consensus algorithm.

I would like to find out together how to apply this algorithm to further develop Etherium.

Due to the lack of English and insufficient time, this is not the answer to all the questions.

I will answer the lacking parts every time I think about it.

