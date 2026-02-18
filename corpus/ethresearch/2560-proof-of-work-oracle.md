---
source: ethresearch
topic_id: 2560
title: Proof-of-Work Oracle
author: themandalore
date: "2018-07-14"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/proof-of-work-oracle/2560
views: 2685
likes: 0
posts_count: 11
---

# Proof-of-Work Oracle

Hi Ethresearch,

Would love your thoughts on my idea, a proof-of-work oracle.  Basicatlly it works as an oracle schema that implements a mineable proof of work (POW) competition to eliminate reliance on trusted third parties for access to off chain data. Users engage in a POW competition to find a nonce which satisfies the requirement of the challenge. The users who find a nonce which correctly solves the POW puzzle input data for the POW Oracle contract and receive native tokens in exchange for their work. The oracle data submissions are stored in the smart contract for use by other on-chain operations

To give an even simpler explanation, think mineable token, but with each solution submission, you get to put in some data (say BTC/USD price).  The first n solutions are accepted and then the median is rewarded (neighboring answers get “uncle” rewards) in the form of a newly minted POW oracle (POWO) tokens.  The median value is then timestamped and placed into a time series array which can be accessed through a getter function which charges parties a small amount of POWO tokens.

Here’s a picture:[![pow_oracle](https://ethresear.ch/uploads/default/optimized/2X/1/14584ff6ec5dc984189a8b531c9fc836abe47085_2_690x482.png)pow_oracle1083×758 56.3 KB](https://ethresear.ch/uploads/default/14584ff6ec5dc984189a8b531c9fc836abe47085)

My team and I built a POC at a hackathon last weekend here : https://github.com/DecentralizedDerivatives/MineableOracle

(shockingly we lost the hackathon to an ERC20 token)

But I’d love to hear if you guys like the idea, have any questions or we’re just completely missing something

## Replies

**clesaege** (2018-07-16):

You may want to look at TruthCoin.

It propose to use a schelling coin like oracle but which could be appealed to the miners in last ressort:  https://www.google.com/url?q=https://www.truthcoin.info/papers/truthcoin-whitepaper.pdf&sa=U&ved=0ahUKEwijiIzIp6TcAhVTVsAKHW0VDwwQFggLMAA&usg=AOvVaw1gandPCx43PI78v3Jl5er-

---

**themandalore** (2018-07-16):

Thanks for the reply, this is a great system but in my mind it’s a different problem since its not on Ethereum.  Since it’s not on Ethereum, you actually need an Oracle to get Truthcoin data into your smart contracts…hence you need a centralized Oracle system to get decentralized info.  Augur and Gnosis have something similar on chain, but it’s more of the POS version of getting to the truth whereas I like to think of our solution as the PoW route.

---

**themandalore** (2018-07-16):

Thanks for the link then, and although I agree with the PoS sentiment, we’ll leave that challenge to the numerous projects working on it.  A PoW oracle is great because it’s vulnerabilities and downsides are pretty well known at this point

---

**vascoosx** (2018-08-24):

Hi, I really liked your idea.

I’m thinking of making a Dapp based on your idea but a bit different and presenting it to the Qtum hackathon. I already made a team of 3 including myself and we are looking for more. It would be awesome if you could join us. We are a team from the US, Egypt and Japan. Two of us are CS students and I’m a backend engineer. We have some experience in smart contracts. What do you say?

---

**nootropicat** (2018-08-24):

The assumption is that PoW solves the sybil risk by making duplicate identities more costly, did I get that right?

---

**themandalore** (2018-08-24):

Qtum?  But shoot me an email [nfett@decentralizedderivatives.org](mailto:nfett@decentralizedderivatives.org), we can discuss.

---

**themandalore** (2018-08-24):

You did.  By taking median values for each time period, you have to have a pretty high percentage of the network to really attack it properly.

---

**nootropicat** (2018-08-24):

The problem with that approach is that PoW rewards lower than possible profits from an attack are unsafe.

---

**themandalore** (2018-08-24):

Agreed, but that’s really the big problem with any PoW or PoS, how do you calculate ‘potential profits’ from an attack?  Obviously a competitor on any of these systems will likely have some discounted net potential profit that makes them all inherently unsafe.  We’re trying to address it by allowing parties to boost the mining reward.  So the obvious way to make mining more difficult is to mine yourself, but we’re also giving people the option of donating to the mining reward for their oracle.  This way if you have, for example, a prediction market with 100 million in it relying on the oracle value, you can actually have the prediction market contract donate to that oracle to increase the mining reward and theoretically the safety.

---

**vascoosx** (2018-08-25):

Hi, I already sent you an email but might have been filtered.

Send me an email to [vascoosx@gmail.com](mailto:vascoosx@gmail.com) if you are still interested.

