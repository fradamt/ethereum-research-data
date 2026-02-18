---
source: ethresearch
topic_id: 3281
title: Use Cases of ETH in Ethereum 2.0 & Beyond
author: MaverickChow
date: "2018-09-09"
category: Economics
tags: []
url: https://ethresear.ch/t/use-cases-of-eth-in-ethereum-2-0-beyond/3281
views: 2437
likes: 6
posts_count: 11
---

# Use Cases of ETH in Ethereum 2.0 & Beyond

Today, I just learned that there is a new development ongoing regarding Beacon Chain and things related to it that will be different from current Ethereum network structure.

May I know what will be the use cases of ETH in the future of Ethereum 2.0?

How will anyone be incentivised to secure the network and facilitate transactions through ETH?

## Replies

**DB** (2018-09-09):

To the best of my understanding, the use cases are similar for the user. Gas for on-chain transactions and computation will still be paid using Ether. On the miner side, instead of buying expensive hardware and paying for electricity, one will be able to stake his Ether and get “interest” and fees from forging valid blocks (a random process will give this right in proportion to the Ether staked).

---

**vbuterin** (2018-09-10):

1. Paying transaction fees
2. Depositing into the PoS contract to collect revenue from other people paying transaction fees

---

**Danny** (2018-09-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Paying transaction fees
> Depositing into the PoS contract to collect revenue from other people paying transaction fees

So you mean the current tx fee would have a transition to the PoS validator’s incentive ?

---

**MihailoBjelic** (2018-09-10):

Put simply:

- Validators are the “miners” of Ethereum 2.0.
- Beacon chain will (probably and eventually) become the “main chain” of Ethereum 2.0.

If we agree that use cases for ETH in Ethereum 1.0 were:

1. Paying Tx fees
2. Sending/receiving/storing value

than in Ethereum 2.0 we have both 1) and 2) plus:

1. Validator staking

Hope this helped. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**Danny** (2018-09-10):

thx bro ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) If the full transition to the PoS called the Beacon chain, how do we overcome the high tx fee externality in the ethereum main-net?

For example, the tx-fee is going to the PoS validator and the validator always wants the more NPVs. If the fees from the tx senders aren’t that beneficiary for each validator’s preference, there could be a front-running or FOMO-like problem, which is similar with the currenct PoW mining’s externality.

That is, no removal of the first auctioning market system, the tx fee externality problem could not be solved exactly.

---

**MihailoBjelic** (2018-09-10):

If I got you right, you basically wanted to ask how can we get rid of high Tx fees in E 2.0?

If that is so, there are three main reasons why Tx fees should be much lower in E 2.0:

1. We will have at least an order of magnitude more validators than in E 1.0. (we might even have 1M+ validators compared to a couple of thousands that we have now)
2. We’re abandoning the practice that every miner/validator need to process/validate every Tx (we randomly sample committees of a few hundred validators instead)
3. Miners/validators will not have to waste resources performing expensive PoW (we use PoS instead).

---

**Danny** (2018-09-10):

Thanks for the great answer again ! It’s interesting.

• First, I totally agree with the number of the miner(validator) should be set more upper since the relationship betweeen the tx fee price and the number of miners is inversed. Just wondering how the +1M validators could be incentivized in a long run.

• Second, if I got you right, you mean that not every node is going to check the txs and the “delegated validation” model is implemented? I think this idea is opposite from the first one. If there is any randomly chosen commitee or validator pool,

i) the number of miners who has the real power to validate the block is going to be centralized like the dPoS.

ii) how do we protect the cartel between them ? What if the validator party sets their own rule like “+10gwei gas prices first, others second” ?

I think if the validator party doesn’t know each other and dynamic changes of validator set is built, maybe the two worries above are just misunderstanding.

---

**MihailoBjelic** (2018-09-10):

Yep, no room for worries at all. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Committee members can not know each other because they’re being selected randomly, and the committees are constantly reshuffled. It might doesn’t sound as secure as E 1.0. at first, but you can look at some numbers in slide 10 of [this Vitalik’s sharding presentation](https://vitalik.ca/files/Ithaca201807_Sharding.pdf), or in [this answer in Sharding FAQ](https://github.com/ethereum/wiki/wiki/Sharding-FAQs#how-is-the-randomness-for-random-sampling-generated), I believe you’ll understand how secure this model is. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**Danny** (2018-09-10):

Cool ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)  sharding is going to be a critical solution. I’ll check the paper and follow up ! Thx ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=9)

---

**MihailoBjelic** (2018-09-10):

No problem, glad if I could help. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

