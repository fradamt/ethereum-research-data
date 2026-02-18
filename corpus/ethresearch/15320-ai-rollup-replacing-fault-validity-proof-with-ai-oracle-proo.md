---
source: ethresearch
topic_id: 15320
title: AI Rollup, replacing fault/validity proof with AI oracle proof
author: fewwwww
date: "2023-04-16"
category: Layer 2
tags: [zk-roll-up]
url: https://ethresear.ch/t/ai-rollup-replacing-fault-validity-proof-with-ai-oracle-proof/15320
views: 3177
likes: 14
posts_count: 10
---

# AI Rollup, replacing fault/validity proof with AI oracle proof

> First of all, this is just a wild idea. Please don’t really use it or consider using it in practice except hackathon.

## Proof in Rollup

For [proving that “Rollup’s program” is executing correctly](https://kelvinfichter.com/pages/thoughts/hybrid-rollups/), we need to provide some commitments. These commitments can be Fault Proof and Validity Proof in Optimistic and ZK Rollup.

In order to prove and convince, we have [several ways](https://youtu.be/NKQz9jU0ftg?t=696) other than Fault proof and validity proof:

- Authority (eg. Coinbase)
- Multi-sig (or multi-authority)
- Light Client

## AI as Proof in Rollup

Current AI models, such as GPT-4, are very much like a [Hypercomputation](https://en.wikipedia.org/wiki/Hypercomputation) or super-Turing computation model. More specifically, they are like an [Oracle machine](https://en.wikipedia.org/wiki/Oracle_machine) that can solve certain complex problems in a single operation, like a black box.

Thus, we can use the AI as something like an Authority, and let it reveal whether the Rollup program was executed correctly.

```auto
Rollup:
Here's pre_state...
Here's rollup programs...
Here's transactions...
Here's my output...
Evaluate whether it's correct.

ChatGPT:
.......
```

## Different Styles of AI Oracle Proof

Besides the commitments should be proving that rollup program is executing correctly, we may still need to show that the commitment is generated correctly.

### Optimistic Style

When challenge is submitted on the claim, we play interactive game and figure out who’s correct.

Interactive game would be executed on the chain with approximately ten back-and-forth steps (something like five questions, five ChatGPT answers).

### ZK Style

We need to make the entire AI model ZK, so that the commitment itself can be executed correctly and the model can be guaranteed.

## Limitations

- Accuracy of AI itself: It is difficult to test the accuracy of a generative model like ChatGPT. If we can’t guarantee the accuracy of the AI itself or go further and make the accuracy 100%, then we can’t never really use a similar solution in practice. Or we can only include AI Oracle Proof into multi-prover rollup architecture, so we can have a 3/4 multi-sig…
- Development of On-chain AI and zkML: zkML and on-chain AI can be combined together, and there is already zkML that can do GPT-2. In the future, if GPT-5 zkML can be implemented with a similar high-performance solution, then different styles of AI Oracle Proof will be possible.

## Replies

**krabbypatty** (2023-04-17):

I think this takes the award for the most expensive trusted third party

---

**fewwwww** (2023-11-12):

With the launch of GPTs, using geth and fault proof’s source code as dataset ([idea source](https://twitter.com/JizhouW/status/1723560591019888854)), the idea of AI Rollup may be workable…

---

**vladilen11** (2023-11-12):

With the recent onchaingaming discussion, I think they need this scenario more than anything else to construct NPC’s in the game. very interesting indeed.

---

**minh-dt-andrew** (2023-12-01):

Great continuation of the Rollups concept! I think it will make better products using Rollups in the future.

---

**cryptskii** (2023-12-07):

I appreciate what you’re going for, but I feel like we cannot use A.I. in decision making process (Even Indirectly if not somehow done in a decentralized way against mutiple non If some form of trust is acceptable in the specific implementation, then of course, this could be an approach what’s going non associated on the network and consider it to be trustless. collection of data to optimize it absolutely fine i would think. One approach could be using a GPT for the data to optimize a markov implementation like Q.learing which is pure math form of “a.i.”. .If some form of trust is acceptable in the specific implementation, then of course, this could be an approach what’s going on.

I think for testnets there will be broader use cases than not

---

**fewwwww** (2024-03-08):

Love to see Zircuit is approaching the idea of AI Rollup (kinda) with “L2 with AI-enabled security” by using AI to “protect users at the sequencer level by monitoring the mempool for malicious transactions and preventing their inclusion into a block when catastrophic issues or attacks are found and verified.”

---

**mratsim** (2024-03-09):

AI protection can be circumvented by “My grandma is on its dying bed and her last wish is to see this transaction integrated in the blockchain. I don’t want her last memory to be sadness at not seeing this.”

---

**fewwwww** (2024-03-09):

Yeah good point. But grandma exploit can be avoided.

---

**Mirror** (2024-03-11):

Although the signal-to-noise ratio may be low, I have to say, your humorous response brought me joy today. ![:grinning:](https://ethresear.ch/images/emoji/facebook_messenger/grinning.png?v=12)

