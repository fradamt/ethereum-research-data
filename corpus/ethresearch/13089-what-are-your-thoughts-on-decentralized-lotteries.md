---
source: ethresearch
topic_id: 13089
title: What are your thoughts on decentralized lotteries?
author: PeterTakahashi
date: "2022-07-19"
category: Applications
tags: []
url: https://ethresear.ch/t/what-are-your-thoughts-on-decentralized-lotteries/13089
views: 3705
likes: 7
posts_count: 12
---

# What are your thoughts on decentralized lotteries?

By using ERC20 tokens on an EVM-compatible public blockchain to play the lottery Lotteries can be conducted at low cost, with strict privacy, high return rates, and traceability guaranteed, without having to go through a lottery management organization. Winners are determined by randomly generated numbers on the blockchain.

During the three months between March and July 2022, we were developing a decentralized lottery.

However, every country has laws regulating lotteries, and although we negotiated with the organizations that issue lottery licenses in each country, we were unable to obtain a license.

We are shutting down this business and will open source all source code.

whitepaper

https://whitepaper.foxlottery.org/

official web

https://www.foxlottery.org/ja

## Replies

**MicahZoltu** (2022-07-19):

Random number generation on a blockchain that cannot be gamed are incredibly hard.  While lotteries are certainly a popular gambling mechanism, you would need to use a VDF to secure it and those are largely theoretical still.

---

**bshramin** (2024-01-06):

I have seen lottery applications that use oracles for generating random numbers, isn’t that a good solution?

---

**MicahZoltu** (2024-01-07):

It isn’t trustless.  The oracle can simply provide whatever number it wants.  You are essentially just delegating trust to the oracle operator.  You can *try* to build a trustless oracle, but that is nearly impossible (depending on what your datasource is).

---

**ziyinlox-purple** (2024-01-17):

Hmmm,maybe a public blockchain can integrate multiple oracle services to generate random numbers, and then use the majority of these values to decide on a final number？

---

**MicahZoltu** (2024-01-18):

This is essentially a multisig at that point, and `m` services can collude to corrupt the results.

---

**ziyinlox-purple** (2024-01-24):

Or can we use some ways to avoid mu service colluding?

1. Building decentralized oracle network, which can have built-in mechanisms to punish dishonest or inaccurate nodes；
2. Building random number verification mechanism, by using cryptographic proofs (such as zero-knowledge proofs) to verify the correctness and integrity of random numbers without the need to trust a single oracle

---

**Zergity** (2024-01-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/ziyinlox-purple/48/14799_2.png) ziyinlox-purple:

> Or can we use some ways to avoid mu service colluding?
>
>
> Building decentralized oracle network, which can have built-in mechanisms to punish dishonest or inaccurate nodes；
> Building random number verification mechanism, by using cryptographic proofs (such as zero-knowledge proofs) to verify the correctness and integrity of random numbers without the need to trust a single oracle

Currently, there’s no good solution for both of them.

---

**Uptrenda** (2024-02-13):

1. Have all parties pick a large random number and commit to it.
2. After the lottery closes everyone reveals their numbers.
3. They are hashed together to form a new number.
4. The number is hashed with every commitment and the lowest result is taken as the winner.
5. If there are somehow multiple winners the reward could be split between them.

There’s already a ‘DAO’ that I think uses commitments to create provably fair random numbers. It’s used as a solution to the randomness problem where you can’t use block hashes since miners have power over their outcome.

I think lotteries would be appealing to many crypto people and I’m surprised I haven’t heard more about them.

---

**MicahZoltu** (2024-02-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/uptrenda/48/4308_2.png) Uptrenda:

> After the lottery closes everyone reveals their numbers.
> They are hashed together to form a new number.

This requires all users show up to complete this step.  For small lotteries with a couple of participants or a single participant plus a house this may work, but it doesn’t work well for large lotteries with many people.  You can do things like have a timeout after which people are excluded, but this can lead to exploitation where you wait until everyone else has revealed then at the last minute (in the last block before timeout) you reveal the set of bets that results in one of your bets being the lowest.  Whoever can manage to be last in block prior to deadline wins.

You can make it so each new participant extends the deadline, but this then becomes a game of chicken between bots, where each manipulates the outcome until either they win and no one manipulates after them, or they run out of bets to leverage.  Perhaps an interesting and fun game, but not a lottery.

---

**Uptrenda** (2024-02-14):

Yes, I agree its not a good design.

One thing that comes to mind is time-lock encryption. If instead everyone submitted an IV (random number) and a function were applied to all submitted results lasting well until after the lottery closes. The participants wouldn’t have to reveal anything. Instead, the result would be known automatically based on the inputs and no one who submits inputs would be able to know what inputs to choose to influence the results since the results would only be available after a certain amount of time. This would prevent race conditions to the lottery.

Then you can just use the original idea of min(H(IV, VDF(IV, …)), …) → winner. While you can make it easy to verify the validity in parallel – I’m not sure if you can make proofs for the whole thing fast and small. That’s outside of what I know.

---

**MicahZoltu** (2024-02-14):

Yes, this problem gets *much* easier as soon as we have functional time lock encryption/witness encryption.  Last I checked (maybe a year ago), there are still some hard unsolved math problems before we can actually do this.

