---
source: ethresearch
topic_id: 2554
title: Batch auctions with uniform clearing price on plasma
author: josojo
date: "2018-07-14"
category: Decentralized exchanges
tags: []
url: https://ethresear.ch/t/batch-auctions-with-uniform-clearing-price-on-plasma/2554
views: 8217
likes: 18
posts_count: 23
---

# Batch auctions with uniform clearing price on plasma

In the recent months, Gnosis put a lot of effort into developing market mechanisms on plasma. Today, we are excited to share two papers and we are looking forward to your feedback.

**Multi-batch auctions with uniform clearing prices** We developed a trading

mechanism between several ERC20 tokens on plasma. Each batch accepts orders to buy any ERC20

token with any other ERC20 token for a maximum specified limit price. All orders are

collected over some time interval and then a uniform clearing price over all token pairs is

calculated for the settlement of all orders.

There are three major advantages of this new market mechanism:

1. Using batch auctions and DKG encrypted orders eliminates front-running possibilities.
2. Batch auctions allow accumulating liquidity over time.
3. Uniform clearing prices allow advanced ring trades between several tokens. This is a useful feature, as it allows to bundle the liquidity between different tokens.  Considering the rise of many stable tokens, this will become a great feature: trades between a stable coin and a target token benefit from the liquidity between other stable coins and this target token.

We published two papers. One paper is focused on the plasma implementation and the other one is focused on the optimization of uniform clearing prices.

[Here are the links to the papers.](https://github.com/gnosis/dex-research/releases/tag/v0.1.0)

We are looking forward to your feedback.

## Replies

**cpfiffer** (2018-07-14):

[Here](https://faculty.chicagobooth.edu/eric.budish/research/HFT-FrequentBatchAuctions.pdf) is a paper written about a similar topic, though the goal of that paper is to reduce the arm’s race of high-frequency trading. It’s relevant here because Budish et al. propose frequent batch auctions. I think you could make the case that this frequent auction type market is exceptionally well suited to a blockchain due to it’s sequential and discrete nature. Thought you might want to flick through it, but it looks as though you have hit on a lot of very similar points.

---

**MicahZoltu** (2018-07-15):

I would be interested in seeing a version of the paper written in plain English, rather than formalized mathematical proofs.  For most of these sort of things I can make the jump from a simple English description (written using language anyone can understand without having to lookup words) to the mental proof that it is sound/works.  However, trudging through a formal proof is a task so painful that I almost never bother.

---

**josojo** (2018-07-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/cpfiffer/48/1504_2.png) cpfiffer:

> Here  is a paper written about a similar topic, though the goal of that paper is to reduce the arm’s race of high-frequency trading. It’s relevant here because Budish et al. propose frequent batch auctions. I think you could make the case that this frequent auction type market is exceptionally well suited to a blockchain due to it’s sequential and discrete nature. Thought you might want to flick through it, but it looks as though you have hit on a lot of very similar points.

Yes, I agree. Batch auctions should be exceptionally well suited to plasma chains, due to their discrete nature. In continuous-trading models on plasma chains, this is even worse than outlined in the article, as the single, unregulated plasma operator would be able to front-run their own markets as they wish.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I would be interested in seeing a version of the paper written in plain English, rather than formalized mathematical proofs. For most of these sort of things I can make the jump from a simple English description (written using language anyone can understand without having to lookup words) to the mental proof that it is sound/works. However, trudging through a formal proof is a task so painful that I almost never bother.

Currently, we are in the process to generate blog posts with technical writers and presentations. We will also present this topic at Dappcon in Berlin this week.

---

**mkoeppelmann** (2018-07-26):

20 min summary of the concept:

---

**josojo** (2018-08-01):

For convenience, here are also the slides used at dappcon:


      [docs.google.com](https://docs.google.com/presentation/d/1vRCzam7Jeqacgw7g1Vc-3a1if_PdrM3UlWGPZfPdIbs/edit?usp=sharing)


    https://docs.google.com/presentation/d/1vRCzam7Jeqacgw7g1Vc-3a1if_PdrM3UlWGPZfPdIbs/edit?usp=sharing

###

Batch Auctions on Plasma

---

**paborre** (2018-08-22):

This is very interesting work.  Thanks for sharing!

Have you considered using a commit-reveal scheme similar to the ENS auction registrar as an another alternative to DKG-based encryption for bid submission?  Since users are already required to remain online for the double signing, it seems like the reveal phase could probably be integrated with that.  The main benefit is that, as commit-reveal depends on a hash, the complexities of key generation and broadcast are avoided.

---

**mkoeppelmann** (2018-08-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/paborre/48/2014_2.png) paborre:

> Have you considered using a commit-reveal scheme similar

The problem with commit/reveal is that you can NOT reveal based on the additional information you get (the revealed orders of others). With the double signing you still can opt out of your trade but only at a moment when you still do not have any information about the other trades.

---

**paborre** (2018-08-23):

> The problem with commit/reveal is that you can NOT reveal based on the additional information

One way to mitigate that problem is to require a deposit with the commit which is forfeited if the reveal does not follow.  ENS does this.  But I can see in this case that would require some reworking of the utxo exit rules on the plasma chain and maybe becomes untenable, not sure.  It also takes away the free option to exit the auction after initial submission, but it’s not obvious to me if that is an essential feature.  Thanks for your response and I appreciate any further thoughts on this.

---

**josojo** (2018-08-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/paborre/48/2014_2.png) paborre:

> One way to mitigate that problem is to require a deposit with the commit which is forfeited if the reveal does not follow.

Probably, it is not this straight forward. Where would people post their reveal msg? If people are supposed to post it only on the plasma chain, then this is tricky, as the plasma chain operator has some incentive to exclude your reveal-msg and get your bond. Hence, users should then also have a chance to publish it on the ethereum main chain. But since also the ethereum chain can be censored for some blocks, we would have to wait several blocks looking for the reveal msg. All that would slow everything down significantly and increases the complexity.

DKG has the advantage that ALL orders are revealed with only one private key. This is very favorable, as we do not need to care about a reveal process for single orders. It allows us to cut out quite some complexity and data compared to a simple commit-reveal process.

---

**paborre** (2018-08-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> If people are supposed to post it only on the plasma chain, then this is tricky, as the plasma chain operator has some incentive to exclude

i agree we do not want to incentivize the plasma operator to intentionally exclude reveals, so paying the full deposit to the operator is probably not a good idea.  The operator shouldn’t receive more than whatever the standard fee is for participating in the auction.  What to do with the remainder of the deposit is an open question.  If nothing else, you could certainly burn it.  Or maybe forfeitures can be used to subsidize subsequent auctions.   I’m not arguing that commit/reveal is superior to DKG encryption, I was mainly curious how far you explored that possibility.

DKG encryption does place a burden on the user to verify that the DKG participants are currently bonded and that the bonds are appropriate for the estimated value likely to transact in the auction.  And, if I understand correctly, the bonds are only slashed if the private key is prematurely revealed on the plasma chain.  There is nothing really deterring the DKG participants from colluding over private back channels to generate the private key for just themselves.  Conceivably, they could simultaneously be submitting multiple bids into the auction and then selectively double signing a subset of those bids once they have an early peek at the decrypted order book. Perhaps it is assumed that the DKG participants are sharing in the auction fees and therefore have some incentive to maintain the long-term integrity of the auction?

---

**josojo** (2018-08-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/paborre/48/2014_2.png) paborre:

> DKG encryption does place a burden on the user to verify that the DKG participants are currently bonded and that the bonds are appropriate for the estimated value likely to transact in the auction.

This would be part of the client software. The usual client will not worry about it, as it is all checked by the client software.

![](https://ethresear.ch/user_avatar/ethresear.ch/paborre/48/2014_2.png) paborre:

> There is nothing really deterring the DKG participants from colluding over private back channels to generate the private key for just themselves.

There is: If someone asks you to participate in their malicious front-running activity and sends you over their secret DKG messages, then you have the change to call him out on the blockchain. You can publish his secret DKG message before the closing of the auction and then you will get his bonds.

If the DKG participants would trust each other completely, then they could front run. But since they don’t trust each other, as the system is set up in such a way, that there is a huge reward for calling out any misbehavior, I think collusion is very very unlikely.

![](https://ethresear.ch/user_avatar/ethresear.ch/paborre/48/2014_2.png) paborre:

> What to do with the remainder of the deposit is an open question. If nothing else, you could certainly burn it.

Even that would open a door for griefing attacks, and push DKG participants out of the system.

Thanks for posting your thoughts, it helps a lot think thorugh a possible commit, reveal scheme.

---

**paborre** (2018-08-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> But since they don’t trust each other, as the system is set up in such a way, that there is a huge reward for calling out any misbehavior,

This is a great point I did not pick up on reading the paper the first couple of times.  Basically, you are incentivizing defection from any potential collusive ring. Actually the ring is never established in the first place if its would-be members have to unilaterally surrender their secrets and risk getting slashed before they in turn receive a secret.  But is there maybe a fair exchange protocol the members could deploy to work around this problem?  I suppose if the group of DKG participants is very dynamic, then it is unlikely they could ever set up a protocol for effective collusion.  What’s the process for electing DKG participants and how often does that happen?

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> Even that would open a door for griefing attacks, and push DKG participants out of the system.

Not sure what you have in mind here.  If there’s a griefing attack with commit/reveal, it would be on the bidders.  Like maybe a griefer could stuff plasma chain blocks to prevent reveals from being accepted by the operator before the deadline.

---

**josojo** (2018-08-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/paborre/48/2014_2.png) paborre:

> But is there maybe a fair exchange protocol the members could deploy to work around this problem?

This is really a tricky question. If there would be a completely trust less oracle, the DKG participants  could commit themselves to not slash anyone in the original DKG slashing system. The commitment would just be organized via a smart contract, where the participants would need to post big bonds. These bonds are slashed, if anyone gets slashes in the original DKG bonding sytsem. If this new commitment-bond is much higher than the bond of the original bonding system of the DKG participants, then you can make it unprofitable for anyone to slash someone else in the original DKG bonding contract.

But I am unsure, whether people would commit to such a second bonding scheme, as the risk associated with it is quite high.

![](https://ethresear.ch/user_avatar/ethresear.ch/paborre/48/2014_2.png) paborre:

> josojo:
>
>
>
> Even that would open a door for griefing attacks, and push DKG participants out of the system.

Not sure what you have in mind here. If there’s a griefing attack with commit/reveal, it would be on the bidders. Like maybe a griefer could stuff plasma chain blocks to prevent reveals from being accepted by the operator before the deadline.

Sry, yes I got confused. Burning would be okay, it would only introduce a griefing vector for the plasma operator against the traders. But for sure, the operator would not use it, as otherwise, he will lose traders of his system.

---

**kfichter** (2018-09-01):

Hi! Appreciate all the work you’re doing with batch auctions. They’re a great mechanism and need a lot of love.

I just got around to reading your paper. I have a question about a specific scenario that might occur. Imagine a user joins a batch auction with a specific `order input`. The operator is behaving, the order is filled completely, the user now has `order output`. The user does not spend `order output` further.

What happens if the user attempts to exit from `order input`?

---

**josojo** (2018-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> What happens if the user attempts to exit from order input ?

If the `order output` was just created by the operator and has not been spent, then the `order output` can be exited. For this, we start the exit game by providing the `order input`, the `double signature` and the `auction price` and potentially the `order volume` . The output of this exit request will then result in the `order output`  - the auction payout.

`Order outputs` will only be able to be withdrawn, by providing the `order inputs`.

`Order inputs`, which were not touched by the auction, can be withdrawn as the original `order inputs`.

---

**kfichter** (2018-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> then the order output can be exited.

What happens if the operator withholds the order output block? Does the user get to exit from the input to the order?

---

**josojo** (2018-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> What happens if the operator withholds the order output block? Does the user get to exit from the input to the order?

Generally, the output of an order needs to be withdrawn. If the operator withholds the order output block, then we need to calculate the output of the auction  on the root-chain by providing the order input and the auction prices to the exit.

---

**kfichter** (2018-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> calculate the output of the auction on the root-chain by providing the order input and the auction prices to the exit.

Ah okay. Another question: What happens if the operator publishes an invalid block before the DKG private key is generated and immediately tries to exit? If the operator has control over the DKG participants, then I guess the exit period would need to be long enough for the operator to publish the DKG key and then to publish the auction prices?

---

**josojo** (2018-09-01):

Yes, these cases are taken care by setting the right time frames:

If the DKG private key or  the bitmap or the snarks proofs are not available, anyone can request the operator to publish them onchain. Then, the operator needs to publish these data within a short time-frame, much shorter than the 7 day exit period. While we have not yet defined this timeframe, we want to keep as short as some hours.

If the operator fails to publish the data, then the chain will be stopped on the root-chain and the last auction will be undone.

---

**AFDudley** (2019-07-01):

**Multi-batch auctions with uniform clearing prices** is a fun problem, I recently started looking at it again. I was somewhat shocked to see the approach that was taken in the paper, I basically started my design with the “extensions” in place. your 5th constraint regarding arbitrage, i’d assume one would get for free. I also have a bunch of other constraints you folks don’t have that I *think* makes the problem a lot easier to solve:

- A single order can’t cross the previous clearing price.
- I don’t have a reference token.
- There is no difference between Buy and Sell.
- I picked “fairness” over volume.
- I constrain the amount of volume that can be traded per auction.

I don’t read math notation as well as I read code, so maybe I’m missing this but you can solve the problem incrementally. by that I mean, we don’t need solve for all rings at once.

There are a bunch of other things I did that result in a dramatically more simplified plasma construction as well.


*(2 more replies not shown)*
