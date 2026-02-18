---
source: ethresearch
topic_id: 18444
title: On Block Sizes, Gas Limits and Scalability
author: Nero_eth
date: "2024-01-24"
category: Economics
tags: [scaling, fee-market, resource-pricing, eip-1559]
url: https://ethresear.ch/t/on-block-sizes-gas-limits-and-scalability/18444
views: 13664
likes: 48
posts_count: 22
---

# On Block Sizes, Gas Limits and Scalability

# On Block Sizes, Gas Limits and Scalability

> Thanks to Alex Stokes, Matt (lightclients) and Matt Solomon for feedback and review!

There has been much discussion about raising Ethereum’s block gas limit recently.

Some argue for bigger blocks based on Moore’s law, some based on a personal gut feeling, some are just trolling around and others are afraid that other chains like Solana will outpace Ethereum when it comes to widespread user adoption.

**In the following, I want to present some charts and figures that may be helpful in guiding us towards a decision that maxes out the gas limit without compromising Ethereum’s decentralization.**

## From the beginning

In contrast to Bitcoin, Ethereum doesn’t have a fixed block size limit. Instead, Ethereum relies on a flexible block size mechanism governed by a unit called “gas.” Gas in Ethereum is a unit that measures the amount of computational effort required to execute operations like transactions or smart contracts. Each operation in Ethereum requires a certain amount of gas to complete, and each block has a gas limit, which determines how many operations can fit into a block.

Ethereum started with a gas limit of 5000 gas per block [in 2015](https://blog.ethereum.org/2015/07/22/frontier-is-coming-what-to-expect-and-how-to-prepare).

This limit was then quickly raised to ~3 million and then to ~4.7 million [later in 2016](https://soliditydeveloper.com/max-contract-size).

With the Tangerine Whistle hardfork and, more specifically, [EIP-150 in 2016](https://github.com/ethereum/EIPs/blob/6572e92dccb2a581c0082befb953050f75d0ece5/EIPS/eip-150.md), the gas limit was raised to 5.5 million, based on a repricing of various IO-heavy opcodes as a response to DoS attacks. After these attacks, the limit was continuously raised by miners to [~6.7 million in July 2017](https://www.preethikasireddy.com/post/blockchains-dont-scale-not-today-at-least-but-theres-hope), then [~8 million in December 2017](https://vitalik.eth.limo/general/2017/12/17/voting.html), then [~10 million in September 2019](https://cryptomode.com/news/crypto/ethereum-mining-pools-push-for-a-block-gas-limit-increase/), then [12.5 million in August 2020](https://twitter.com/etherchain_org/status/1273912037274537984?s=20) and finally to [~15 million in April 2021](https://www.coindesk.com/tech/2021/04/22/ethereum-gas-limit-hits-15m-as-eth-price-soars/).

[![gas_used_over_time](https://ethresear.ch/uploads/default/optimized/2X/1/145723ec93a20a9d9742f5ca0c9db811c5b67649_2_690x229.png)gas_used_over_time1200×400 35 KB](https://ethresear.ch/uploads/default/145723ec93a20a9d9742f5ca0c9db811c5b67649)

Further on, with the Spurious Dragon, Byzantium, Constantinople, Istanbul and Berlin hardforks, the pricing of certain opcodes was further refined. Examples of these refinements are [EIP-145](https://eips.ethereum.org/EIPS/eip-145), [EIP-160](https://eips.ethereum.org/EIPS/eip-160), [EIP-1052](https://eips.ethereum.org/EIPS/eip-1052), [EIP-1108](https://eips.ethereum.org/EIPS/eip-1108), [EIP-1884](https://eips.ethereum.org/EIPS/eip-1884), [EIP-2028](https://eips.ethereum.org/EIPS/eip-2028), [EIP-2200](https://eips.ethereum.org/EIPS/eip-2200), [EIP-2565](https://eips.ethereum.org/EIPS/eip-2565) and [EIP-2929](https://eips.ethereum.org/EIPS/eip-2929).

The most significant change to Ethereum’s fee market happened with the London hardfork in August 2021 and more specifically [EIP-1559](https://eips.ethereum.org/EIPS/eip-1559).

EIP-1559 introduced a base fee that dynamically adjusts over time/blocks depending on the demand for blockspace. At the same time a so called target has been introduced and set to 15 million gas per block. This target is used to guide the dynamic adjustment of the base fee. If the total gas used in a block exceeds this target, the base fee increases for the subsequent block. Conversely, if the total gas used is below the target, the base fee decreases. This mechanism aims to create a more predictable fee market and improve the user experience by stabilizing transaction costs. Additionally, EIP-1559 also introduced a burning mechanism for the base fee, permanently removing that portion of ether from circulation. This hardended the protocol’s sustainability while creating the [ultra sound money meme](https://ultrasound.money/).

Under EIP-1559, there is also a maximum (or “hard cap”) gas limit, set to twice the target, which is 30 million gas. This means that a block can include transactions using up to 30 million gas.

[![gas_used_since_london](https://ethresear.ch/uploads/default/optimized/2X/9/914266869767e73371d402c01f4ede5a03b77d66_2_690x229.png)gas_used_since_london1200×400 19.3 KB](https://ethresear.ch/uploads/default/914266869767e73371d402c01f4ede5a03b77d66)

**Since then Ethereum’s block gas limit remained the same and, as of 2024, it is still at 30 million gas per block.**

## Are we ready for an increase?

Recently, some raised concerns about Ethereum’s gas limit and demanded it to be increased. In the most recent [Ethereum Foundation AMA](https://www.reddit.com/r/ethereum/comments/191kke6/ama_we_are_ef_research_pt_11_10_january_2024/) on Reddit, Vitalik [considered](https://www.reddit.com/r/ethereum/comments/191kke6/comment/kh7ekx3) the idea of increasing the gas limit by 33% to 40 million. He based his reasoning on [Moore’s law](https://en.wikipedia.org/wiki/Moore%27s_law) which states that the number of transistors on a microchip doubles approximately every two years, leading to a corresponding increase in computational power. This principle suggests that network capabilities, including processing and handling transactions, could also increase over time.

Support came from [Dankrad](https://x.com/dankrad/status/1745406611202437356?s=20) and [Ansgar](https://x.com/adietrichs/status/1745190417254003123?s=20), both researchers at the Ethereum Foundation, who like the idea of increasing the gas limit after evaluating the situation after the Dencun upgrade. In addition, [Pari](https://twitter.com/parithosh_j) from the Ethereum Foundations published [a post](https://ethresear.ch/t/testing-path-for-a-gas-limit-increase/18399) exploring paths for a potential gas limit increase.

Others like [Peter](https://x.com/peter_szilagyi/status/1745374731824439531?s=20) and [Marius](https://x.com/vdWijden/status/1745463453345788352?s=20) from Geth raised concerns about increasing the gas limit, especially without having appropriate tooling/monitoring in place. These concerns were specifically based on accelerating state growth, syncing times and reorged block rates.

## What is the block size?

The size of a block can be measured in two ways:

- Gas Usage
- Block size (in bytes)

While both of these measures correlate, they must be considered independently.

For example, a block that contains much non-zero calldata bytes might be big in terms of its size in bytes while the actual gas usage (16 gas for non-zero bytes) may still be relatively small.

Ignoring compression, the maximum block size that can be achieved today while still obeying the [128 KB per transaction limit of Geth](https://github.com/ethereum/go-ethereum/blob/830f3c764c21f0d314ae0f7e60d6dd581dc540ce/core/txpool/legacypool/legacypool.go#L49-L53) is ~6.88 MB. Such a block would max out the number of 128 KB transactions in a block. In practice, these are 55 transactions containing ~130,900 bytes of zero-byte calldata (4 gas per byte) and one transaction filling up the remaining space. However, after snappy compressing such a block we end up at ~0.32 MB, which is negligible.

The largest possible block after compression contains 15 transactions filled with non-zero calldata and can have a size of ~1.77 MB.

**So, as of today, 1.77 MB represents the realistic upper-bound block size for an execution layer block.**

Focusing on this maximum block size, we can identify several factors that influence it:

- Gas limit: Of course, the gas limit has an impact on the maximum block size. The higher it is, the more data can be put into a block.
- Pricing of operations and data: The cheaper an operation in terms of gas, the more often the operation can be executed within a block. While operations such as CALLDATALOAD or CALLDATACOPY, both costing 3 gas, are relatively cheap, other opcodes such as CREATE are more expensive. The more expensive the opcodes used in a block, the less space for calldata (or other operations) in that block.
- Client limits: While not that obvious, client limits such as the 128kb limit per transaction of Geth can also impact the final block size. Since every transaction costs 21k gas as a fixed fee, the lower the client limit per transaction, the more often one has to pay the fixed fee, thus “wasting” gas that could otherwise be used for calldata. As a result, this limit can cause the maximum block size to be reduced by ~0.07 MB. Importantly, the client limits only impact the broadcasting of transactions and do not affect blocks that have already been confirmed.

**Let’s focus on the gas limit per block first:**

[![impact_block_gas_limit](https://ethresear.ch/uploads/default/optimized/2X/6/62b3a72ef38d38d671d2ce799ac36005fda41a60_2_690x229.png)impact_block_gas_limit1200×400 17.1 KB](https://ethresear.ch/uploads/default/62b3a72ef38d38d671d2ce799ac36005fda41a60)

The most straightforward and apparent way to scale a blockchain like Ethereum is increasing the block gas limit. A higher limit means more space for data. However, this also comes with larger blocks that everyone running a full node needs to propagate and download.

As visible in the chart above, the “worst-case” block size increases more or less linearly with the block gas limit. Those limits can be reached by creating blocks that use as many non-zero byte calldata transaction of maximum size.

**Next, let’s shift our focus to the second point - Ethereum’s pricing mechanism.**

More specifically, we look at the costs for non-zero byte calldata that is currently set to 16 gas:

[![impact_calldata_price](https://ethresear.ch/uploads/default/optimized/2X/7/7e6e8162df4e1a136e48ab4ee458973eb33e0e85_2_690x229.png)impact_calldata_price1200×400 20.4 KB](https://ethresear.ch/uploads/default/7e6e8162df4e1a136e48ab4ee458973eb33e0e85)

As we can see in the above chart, increasing the costs for non-zero calldata leads to decreasing block sizes. On the other hand, reducing the costs to, e.g. 8 gas per byte, doubles the size of worst-case blocks. This is very intuitive as halving the price allows to put double the amount of data into a block.

## What about EIP-4844 (Proto-Danksharding)?

I won’t cover the details of 4844 here as there exists great documentation on [eip4844.com](https://www.eip4844.com/), but simply speaking, EIP-4844 introduces “sidecars” that are named “blobs” with each blob carrying ~125kb of data. Similar to EIP-1559, there exists a “target” which determines the targeted number of blobs available. With the Dencun hardfork the target is set to 3 blobs with a maximum set to 6 blobs per block.

Importantly, blobs come with their own fee market, creating a so-called [multidimensional fee market](https://ethresear.ch/t/multidimensional-eip-1559/11651). This means that blobs don’t have to compete with standard transactions but are decoupled from the EIP-1559 fees.

So far, so good. Let’s see how this upgrade affects the average block size of Ethereum.

[![blobs](https://ethresear.ch/uploads/default/optimized/2X/0/03635041be05187bbf9579de9a135220b2cdff5f_2_690x229.png)blobs1200×400 64 KB](https://ethresear.ch/uploads/default/03635041be05187bbf9579de9a135220b2cdff5f)

As of today, the average block size of beacon chain blocks after employing snappy compression is around 125 KB. With 4844, we add another 375 KB to each block, thus 4x’ing the current avg. block size. By reaching the maximum number of blobs, we essentially increase the current block size by sevenfold.

The worst-case block increases from ~1.77 MB to ~2.5 MB. This estimation does not take into account the CL parts of a block. Nonetheless, in the event of a DoS attack, we must be prepared to deal with such maximum size blocks.

## Conclusion

Finally, increasing the current block gas limit requires thorough research and analysis before implementation. While sophisticated entities like Coinbase, Binance, Kraken, or Lido Node Operators might manage block gas limits over 40 million, solo stakers could struggle.

Thus, such decisions must be well-considered to make sure we do not hurt decentralization.

In the end, it’s rather easy to build something that is as scalable as Facebook but what matters is to not lose the property that most of us signed up for: decentralization.

---

Find the code for the above estimates and charts [here](https://github.com/nerolation/eth-gas-limit-analysis).

## Replies

**MicahZoltu** (2024-01-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> While sophisticated entities like Coinbase, Binance, Kraken, or Lido Node Operators might manage block gas limits over 40 million, solo stakers could struggle.

Nitpick, should say (emphasis mine):

> While sophisticated entities like Coinbase, Binance, Kraken, or Lido Node Operators might manage block gas limits over 40 million, censored Ethereum users could struggle.

---

**Keccak255** (2024-01-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> While sophisticated entities like Coinbase, Binance, Kraken, or Lido Node Operators might manage block gas limits over 40 million, solo stakers could struggle.

Appreciate a bit more elaboration on this. why sophisticated entities might manage block gas limits over 40 million, solo stakers could struggle

---

**Nero_eth** (2024-01-24):

Solo stakers usually don’t have the same tech skills or the fancy hardware and bandwidth that the big guys do. It’s tough to keep up with large companies that throw a lot of money at hardware and bandwidth and have teams focused solely on keeping their nodes up and running.

And when I talk about solo stakers, I mean even those using Raspberry Pis to run nodes, which is something you wouldn’t see big staking operators do, especially with millions in customer funds.

Plus, there are stakers in parts of the world where bandwidth is pretty scarce, which adds another layer of challenge.

But of course, the exception proves the rule: there are solo stakers that are very sophisticated and staking pools that aren’t.

---

**cryptoaicoder** (2024-03-03):

With all respect, while Raspberry Pis and remote low bandwidth internet connections are fantastic and better very year, Ethereum cannot limit its growth potential by catering only to the lowest common denominator of hardware and connectivity. Because then an argument can go further, why not using a Raspberry Pi Pico or Arduino Nano or even slow satellite internet connections.

Solo staking requires 32 ETH hence an investment of around $50,000 at current prices, which justifies allocating funds for reliable infrastructure beyond bare minimums. A good 100 Mbps connection can be purchased for less than $100 a month in many locations globally. And capable hardware like an 8-core AMD/Intel CPU with NVMe storage can be had for less than $1000.

Therefore, in 2024 it make sense that an Ethereum node should rely on a good quality internet connection and mid-range consumer PC hardware. With these more reasonable minimums, the average block size and max block size can easily be increased. At 12 second block times, 2MB represents roughly 15% utilization of a 100 mbps connection.

In conclusion an increase of the block size or average size, will not reduce decentralisation.

An increase of block size will lower the fees per transactions on the network, increase usage, and last but not least make Ethereum even more deflationary as the sum of the fees burned will be likely higher.

---

**Nero_eth** (2024-03-03):

I agree with most parts that you say but I won’t agree to the let’s scale through increasing hardware requirements.

As soon as you start doing that, it’s not a decentralized blockchain that is then your main competitor for the services you’re able to offer, but Google, Amazon, Facebook, etc.

It is super easy to create a system that has high throughput (e.g. visa/mastercard).

It is super easy to create a system that has high data storage capacities (Google Cloud, Amazon S3, etc.)

The USP we got is decentralization and all the cool features it entails like credible neurality or censorship resistance. And one won’t get decentralization through data centers.

![](https://ethresear.ch/user_avatar/ethresear.ch/cryptoaicoder/48/15497_2.png) cryptoaicoder:

> In conclusion an increase of the block size or average size, will not reduce decentralisation.
> An increase of block size will lower the fees per transactions on the network, increase usage, and last but not least make Ethereum even more deflationary as the sum of the fees burned will be likely higher.

The block size in bytes doesn’t necessarily impact the amount of gas spent in a block. So, an increase in block size will not directly lower transaction fees. An increase of block gas limit would do.

---

**jamesmorgan** (2024-03-19):

How does this impact solo stakers bandwidth consumption? Any thoughts on if the gas limits raises the bandwidth by much?

---

**Mirror** (2024-03-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> Finally, increasing the current block gas limit requires thorough research and analysis before implementation. While sophisticated entities like Coinbase, Binance, Kraken, or Lido Node Operators might manage block gas limits over 40 million, solo stakers could struggle.

Do you know who is working on this? Trying to increase the gas limit.

---

**Nero_eth** (2024-03-20):

EIP-7623 should not change anything regarding the median block size → what the avg. validator can expect. Therefore the avg. bandwidth consumption should remain the same.

The worst case block size would be reduced, which is one of the EIP’s goals.

Being implemented together with a gas limit increase would cause the avg. block size to rise. We’re currently at 125KB on average, thus we’d probably go towards 180-200KB depending on the final setting.

---

**Nero_eth** (2024-03-20):

Yeah, the gas limit increase is coordinted within the community. Check this tweet for details:

https://x.com/econoar/status/1770136717401419859?s=20

---

**kladkogex** (2024-03-20):

Call data size could be significantly decreased if EVM had powerful decompression precompiles.

So one possibility is to synchronously increase call data gas, and introduce decompression precompiles.

---

**kevin-hs-sohn** (2024-04-05):

Considering that you’re using the “worst-case block size” as a key metric for ensuring decentralization, why can’t we make an explicit hard cap on the block size and substantially increase the block gas limit instead?

Would solo stakers struggle if we increase block gas limits to like 100 million while limiting the block size to under 1MB?

---

**MicahZoltu** (2024-04-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/kevin-hs-sohn/48/15901_2.png) kevin-hs-sohn:

> Would solo stakers struggle

Stakers are not the target userbase of Ethereum, they are a service provider.  While we want solo over centralized stakers, stakers are far from the most impacted demographic when it becomes harder to run a client.

The people we care about are *users*, and these people don’t have the time/resources to buy special/exclusive hardware just for running an Ethereum client.

---

**kevin-hs-sohn** (2024-04-05):

Personally, I think individuals running full nodes just to make sure they’re getting correct data from Etherscan doesn’t make sense. Even for the ones that are obsessed with decentralization to the max, it is already economically not feasible to do so unless you hold huge capital on-chain – in which case, buying tons of SSDs won’t be a problem.

Besides, I think it’s a totally different subject to discuss. What you’re saying is about the end-user verifiability side of decentralization, not about decentralization in the consensus mechanism.

---

**MicahZoltu** (2024-04-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/kevin-hs-sohn/48/15901_2.png) kevin-hs-sohn:

> it is already economically not feasible to do so

Exactly, which is why we should be lowering the gas limit, not raising it.

![](https://ethresear.ch/user_avatar/ethresear.ch/kevin-hs-sohn/48/15901_2.png) kevin-hs-sohn:

> What you’re saying is about the end-user verifiability side of decentralization, not about decentralization in the consensus mechanism.

Changing the gas limit and size of the blockchain affects end-user ability to run a local node, so it is very much an important part of the discussion that should not be ignored.

---

**Nero_eth** (2024-04-05):

I do agree with Micah. In the end, it’s the users running nodes that can defend the chain against all kind of majority attacks. I really like the story of Segwit2x playing out, as it showed the power of users in the governance process.

Regarding the 100m gas limit with a artificial cap at 1MB:

In the end there are many bottlenecks, if it’s not bandwidth, then it’s computation or storage. 100m gas would fit too many operations into one block such that small validators are not able to keep pace. So, not a bandwidth problem (or history size) but computation: An attacker would check the benchmarks, indentify the “worst” opcode and then fill the block with as much computational load as possible, without even requiring much calldata.

So yes, at 100m gas, I’m very certain we’d open Ethereum to DoS attacks.

Regarding the cap: basically all clients have limits already. E.g. the geth limit at 128kb per transactions is an example for it. Though, this doesn’t mean that txs cannot be larger than 128kb and that everything larger is reorged out by geth nodes - it’s just that geth node would reject such txs (=not forward it to others) if they see such a tx i the mempool.

As soon as we’re talking about size limits, we’re basically talking about calldata limits as it’s the calldata that makes up the “size” of a block. Thus, increasing/decreasing the gas limit directly impacts the maximum calldata (=max size) of a block.

---

**kevin-hs-sohn** (2024-04-09):

I actually disagree with the perspective. Why would you bother running your own full node when you’re not participating in the consensus and don’t even hold a lot of capital on-chain? I think the fact that anyone with an adequate amount of capital can permissionlessly verify the chain data and even participate in the consensus itself is enough to prevent industrial node operators (wallets, block explorers, node indexers, centralized exchanges, etc) from malacting.

But let’s agree to disagree on this matter.

Then, what if we simply double the blobspace size? If the networking overhead becomes an issue, we may add an artificial cap to the block size (which won’t affect the L1 throughput in most cases since most of the blocks aren’t even using 0.3MB)

---

**MicahZoltu** (2024-04-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/kevin-hs-sohn/48/15901_2.png) kevin-hs-sohn:

> But let’s agree to disagree on this matter.

This is a very fundamental point that *must* be agreed on if we are to come to any agreement on how and where to scale.  As long as you are building clients designed to run in a datacenter and I am building clients designed to run on consumer hardware, we will not be able to come to any agreement on how to architect and scale the system or which tradeoffs should be made.

---

**Zebbr** (2024-05-31):

People that can afford 32 eth to stake, can afford a decent computer

---

**CleanPegasus** (2024-06-08):

I live in a country with very few node operators around me. The sync times for a full node are abysmal even with a decent internet connection. I think we should not increase the block gas limit more than 40 million until we have verkle trees and stateless clients.

---

**ben-lilly** (2024-11-15):

Very nice summary and post [@Nero_eth](/u/nero_eth) .

I’m trying to get caught up on the recent discussions surrounding gas limits and fees.

For background, been working on creating a “CPI Index” as it relates to Ethereum fees. Part of this requires bucketing transactions into buckets/categories based upon their Method IDs. Then tracking the frequency of those transaction types over time to compile a basket of typical transactions over time.

Then from there, creating a weighted basket of what is a normal TX over time in terms of gas usage and the avg gas cost.

Our v1 did shed some interesting insights which I’ve written about on espresso(.)jlabsdigital(.)com (post called Ethereum’s Great Depression).

What becomes apparent when doing this is that gas limits tend to get adjusted (or blob fees added) when congestion is high. This reduction in the cost to transact has economic spillover effects that in turn, create deflationary conditions as that congestion subsides. And I don’t believe there has been enough attention or focus on how this impacted Ethereum… Especially as it looks to push some usage/users to L2s.

What I’m working up to here is a question on whether there has been exploration about targets being more dynamic, and allowing that target gas usage to drop below 15 million.

The goal would be to create better price stability on the ecosystem.

Additionally, there does appear to be heightened price volatility to the upside for a variety of reasons… More recently we saw gas costs jump from sub 10 to 112 in a day. This is a lot of price instability/volatility in the gas market, which hinders app development, revenue forcasting, and other builders to function in more predictable environments.

If the goal for Ethereum is to maximize usage and production of its platform, it needs greater price stability. W/o, you lose users and builders.

So my question here is based upon how to maximize this through the fee market with a goal to create a CPI index for ethereum… With the ultimate goal to propose a solution that can also respect the need to combat ddos of the network.

I’m still catching up to the most recent dialogues, so any help in pointing me in the right direction would be greatly appreciated. Thanks


*(1 more replies not shown)*
