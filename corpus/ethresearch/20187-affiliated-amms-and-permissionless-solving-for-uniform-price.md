---
source: ethresearch
topic_id: 20187
title: Affiliated AMMs and permissionless solving for uniform price batch auctions
author: sergioyuhjtman
date: "2024-07-31"
category: Decentralized exchanges
tags: [mev]
url: https://ethresear.ch/t/affiliated-amms-and-permissionless-solving-for-uniform-price-batch-auctions/20187
views: 4201
likes: 6
posts_count: 7
---

# Affiliated AMMs and permissionless solving for uniform price batch auctions

The idea of mitigating MEV through batch auctions is as old as the concept of MEV itself. They can both be traced back to [this Reddit post](https://www.reddit.com/r/ethereum/comments/2d84yv/miners_frontrunning/) from August 2014[[1]](#footnote-49420-1). Today, ten years later, this is still an ongoing discussion (see for instance [[UNIX]](#references), [[COW]](#references)). To what extent can we reduce MEV by using batch auctions? Can we build batch auction protocols that are better than those existing today? In this article we propose an optimistic point of view for the first question and a candidate affirmative answer to the second question through concrete mechanisms.

**Note:** This article was primarily conceived while working at Flashbots Research for a year spanning 2023 and 2024. Special thanks to Christoph Schlegel.

The article assumes that the reader is familiar with the concepts of MEV, batch auctions and AMMs in the context of decentralized exchange (DEX).

### A cooperative endeavour between traders

In the long term, on-chain traders will use those DEX protocols that are most convenient for them. Ideally, they would trade at market prices with no fee other than the gas cost, equalling the gas price of a transfer. Even though Ethereum’s reality is far from this, in my opinion we shouldn’t rush to dismiss the possibility. Carefully designed smart contracts jointly with off-chain mechanisms might help traders get close to this ideal[[2]](#footnote-49420-2). It is likely that these clever designs are not out there yet.

A very powerful idea is that the smart contract that settles trade orders does so in batches, enforcing uniform clearing prices. This has two fundamental properties:

(a) The execution does not depend on the ordering of the trade orders.

(b) Uniform clearing prices ensure that a user trading in one direction receives the same price as the other users trading in that same direction, and is a direct counterpart to the users trading in the other directions, with no room for intermediaries between them.

The most famous (or even the only) live system implementing this mechanism on a blockchain is CoW protocol [[COW]](#references) (see also [[SPEEDEX]](#references)). Unfortunately, the sole existence of a uniform price batch auction mechanism is not enough to reach the ideal situation described above. MEV occurs through the reordering, censoring, or insertion of data by a privileged player. While according to (a) reordering trade orders has no effect in our case, it is still possible that privileged players censor and insert data. As a matter of fact, for the players who write a transaction or a block, it will always be physically possible to ignore some data and to include their own data, maybe even pretending that this new data was produced by someone else. Therefore, here we will simply abandon the search of a protocol that logically guarantees no censorship nor privileged insertions. Nevertheless, we will not rule out the possibility of a mechanism such that in normal market conditions and assuming wide adoption, the privileged players will be incentivized not to censor, and enjoy only a marginal advantage from last moment inclusions.

While CoW protocol has achieved an interesting degree of adoption, it represents only a small fraction of Ethereum DEX activity —[around 1% these days](https://defillama.com/aggregators/chains/ethereum). CoW runs a centralized solving protocol.

### Uniform clearing prices and Walrasian equilibrium

A trade order can be understood as a mathematical function of the clearing prices. The output of the function is the traded amounts for each asset. Given a set of trade orders, there is typically only a limited set of valid clearing price vectors, maybe even only one. This situation perfectly corresponds to the concept of Walrasian equilibrium in a pure exchange market (see [[RGGM]](#references), [[FY]](#references) and references therein). A Walrasian equilibrium is a vector of prices at which the supply of each good equals the demand for that good.

Under very mild hypothesis, we can guarantee the existence of at least one equilibrium. The computational problem of finding equilibrium price vectors translates to the search of fixed points of a certain mapping.

### Affiliated AMMs

Decentralized exchange predominantly occurs through automated market makers (AMMs). Many researchers and industry actors have pointed out that AMM liquidity providers (LPs) typically receive worse prices than what the market has to offer at each time. This phenomenon is usually referred to as loss vs. rebalancing (LVR) and described as MEV suffered by the liquidity providers [[LVR]](#references), [[WLVR]](#references).

There is a natural mechanism to attack this issue that no one seems to have considered yet[[3]](#footnote-49420-3). Special AMMs may participate in a uniform price batch auction just like any other trader. These would be the affiliated AMMs. They would allow certain swaps depending on their state and execution price, only admitting the price from the batch. We can think of the allowed swaps as preprogrammed trade orders. To implement this, the contract that executes batches should be prepared to call affiliated swaps passing the batch prices. From now on, let us call *W* the smart contract that executes batches, i.e. the main contract of the system under consideration. Specially designed affiliated AMMs may be added *a posteriori* following specifications determined by the *W* contract[[4]](#footnote-49420-4). It is possible that affiliated AMMs benefit by only allowing swaps coming from *W*. However, we do not need to discuss it at this point: the scheme allows to decouple the problem of choosing a specific AMM design. A multiplicity of them may coexist, and liquidity migration can happen seamlessly at any time. The existence of multiple AMMs affiliated to the same *W* contract does not entail liquidity fragmentation.

Assuming wide adoption of the *W* contract and low incidence of censorship, we have clearing prices that are actual market prices, thus mitigating LVR and MEV.

[![diagram](https://ethresear.ch/uploads/default/original/3X/4/8/4824aef76acd0078806fd0c5418d95c44555a648.png)diagram642×451 9.61 KB](https://ethresear.ch/uploads/default/4824aef76acd0078806fd0c5418d95c44555a648)

### Permissionless solving

Once we have truly accepted that we cannot enforce censorship resistance for trade orders at code level, we may reasonably conjecture that the best we can do is to open the gates as much as possible in order to minimize censorship and democratize the system. The proposal is to let *W* allow anyone to execute a batch, as long as there are no price inconsistencies within each block. The block proposers, as always, will exercise their right to choose the transactions they prefer, possibly through a PBS mechanism [[PBS]](#references), [[MEV-BOOST]](#references). This feature achieves the maximum degree of decentralization possible at smart contract level for a batch auction system. The auction will occur at block building level. This is analogous to the usual permissionless access to AMMs, which is only regulated by the PBS apparatus or whatever mechanism adopted by the block proposers. Another example is UniswapX: their reactors allow anyone to be a [filler](https://docs.uniswap.org/contracts/uniswapx/guides/createfiller), though they don’t enforce uniform clearing prices.

Let us explain why it is reasonable to expect that this mechanism will work well, i.e., that potential price manipulations by censoring orders are expected to be under control. The flow of the reasoning is as follows. We will first imagine the system flourished, running a large portion of Ethereum’s DEX volume. We will try to visualize this scenario and assess whether it is stable or if we should expect frequent price manipulations. Let us list some properties of the flourished scenario:

**(1)** Since there are many important tokens on Ethereum blockchain, we expect to have a main cluster of several tokens interconnected by swaps at each batch. This is desirable because it means the liquidity in one pair can benefit traders in other pairs (e.g., an order in pair A/B can be settled against orders in pairs B/C and C/A).

**(2)** By looking at how prices vary, it turns out that very-short-term volatility is easy to estimate. Only as an example, on a normal day the price of ETH measured in USD typically varies less than 0.1% in a 12s period, with some larger jumps occasionally. Uninformed traders may use this kind of magnitude for the slippage tolerance. Furthermore, public tools that monitor real time price movements can aid users to reduce the slippage tolerance depending on their preferences. Meanwhile, informed traders doing statistical arbitrage or plain arbitrage are expected to use very low values for the slippage tolerance when trading liquid assets. This will set a tight bound on the bounty that a malicious solver can obtain by deviating the price.

**(3)** We may assume the existence of honest solvers. As usual, the batch that generates more income for the block proposer should make it to the chain. Honest solvers will aim to maximize that income by maximizing inclusion. They will frequently need to discard some orders for various reasons, such as limited block space, or computation deadlines. As a result, we will often have more than one honest proposed batch. Trusted execution environments can be useful in increasing the transparency of honest solvers.

When a malicious solver tries to manipulate the price, they have to beat the best honest solution. To this end, they will censor every order in one direction for a given pair A/B exceeding certain price threshold. By doing so, they will not only miss out on the gas fees of the censored orders, but also on orders in other pairs due to operating away from the market equilibrium prices (recall (1)). Because of this and (2) it is possible that in most cases it will not be profitable to manipulate the prices of the batch. In addition, we may have other off-chain mechansims to further prevent malicious solving. One such mechanism can be to use private channels between traders and honest solvers in certain cases.

### MEV: a zoom-out analysis

Total MEV extraction from Ethereum has been stable during the last two years, at levels above 250 kETH per year[[5]](#footnote-49420-5). During this period, there haven’t been many innovations generating optimism about MEV reduction. This has led many people to believe that such levels of MEV are inevitable. The fundamental economic reason for the existence of MEV can be summarized by the concept of block proposer monopoly. If traders want to improve their situation, they need to coordinate by adopting a mechanism that gives them more bargaining power, a trade union. This is the principle underlying the concrete proposals presented here. A system that integrates the different types of liquidity and unifies the execution prices helps traders coordinate their orders around true market prices as described in (2).

Reducing the incidence of MEV would be a great achievement, since it would allow the DEX volume to grow. On-chain trading would become more convenient than centralized alternatives in many cases, thus increasing the global value of the blockchain.

### Final remarks

(I) The above description of *W* is incomplete. Possibly the most important undefined aspect is how to cover gas and trade fees (by *gas fee* we mean the cost of gas usage as if it were a transfer). What kind of regulations should *W* implement regarding the operational cost or trade fees? Can the system work well at zero trade fee? See footnote [2]. These questions don’t seem very easy to answer. Fortunately, we will be able to continue iterating theory and practice.

(II) If there are non-affiliated AMMs coexisting with *W*, the solvers of *W* can extract profit from them. Every time there is a price movement, it will be possible to find surplus-generating solutions. To find them, they need to consider non-affiliated AMMs as virtual agents of the batch, following a procedure explained in [[FY]](#references). This mathematical fact should act as an attractor of liquidity from traditional to affiliated AMMs.

### References

**[COW]** CoW protocol, [CoW Protocol | CoW Protocol Documentation](https://docs.cow.fi/cow-protocol);

Felix Leupold, *Gnosis Protocol v2 Fighting the MEV Crisis with Batch Auctions one CoW at a time*, https://www.youtube.com/watch?v=6MfcZGVeQsQ

**[CF]** Andrea Canidio, Robin Fritsch, *Arbitrageurs’ profits, LVR, and sandwich attacks: batch trading as an AMM design response*, [[2307.02074] Arbitrageurs' profits, LVR, and sandwich attacks: batch trading as an AMM design response](https://arxiv.org/abs/2307.02074)

**[FB2]** Philip Daian, Steven Goldfeder, Tyler Kell, Yunqi Li, Xueyuan Zhao, Iddo Bentov, Lorenz Breidenbach, Ari Juels, *Flash Boys 2.0: Frontrunning, Transaction Reordering, and Consensus Instability in Decentralized Exchanges* [[1904.05234] Flash Boys 2.0: Frontrunning, Transaction Reordering, and Consensus Instability in Decentralized Exchanges](https://arxiv.org/abs/1904.05234)

**[FY]** Sergio Yuhjtman, Flashbots, *Walraswap: a solution to uniform price batch auctions*, [[2310.12255] Walraswap: a solution to uniform price batch auctions](https://arxiv.org/abs/2310.12255)

**[LVR]** Jason Milionis, Ciamac C. Moallemi, Tim Roughgarden, Anthony Lee Zhang, *Automated Market Making and Loss-Versus-Rebalancing*, https://arxiv.org/pdf/2208.06046

**[MEV-BOOST]** Flashbots, *MEV-Boost in a Nutshell*, https://boost.flashbots.net/

**[PBS]** Ethereum Foundation, *Proposer-builder separation*, [Proposer-builder separation | ethereum.org](https://ethereum.org/en/roadmap/pbs/)

**[RGGM]** Geoffrey Ramseyer, Mohak Goyal, Ashish Goel, David Mazières,

*Augmenting Batch Exchanges with Constant Function Market Makers*, [[2210.04929] Augmenting Batch Exchanges with Constant Function Market Makers](https://arxiv.org/abs/2210.04929)

**[SPEEDEX]** Geoffrey Ramseyer, Ashish Goel, and David Mazières, *SPEEDEX: A Scalable, Parallelizable, and Economically Efficient Decentralized EXchange*, https://www.usenix.org/conference/nsdi23/presentation/ramseyer, [Stellar | Building SPEEDEX – A Novel Design for a Scalable Decentralized Exchange](https://stellar.org/blog/developers/building-speedex-a-novel-design-for-decentralized-exchanges)

**[UNIX]** Hayden Adams, Noah Zinsmeister, Mark Toda, Emily Williams, Xin Wan, Matteo Leibowitz, Will Pote, Allen Lin, Eric Zhong, Zhiyuan Yang, Riley Campbell, Alex Karys, Dan Robinson, *UniswapX* https://uniswap.org/whitepaper-uniswapx.pdf

**[WLVR]** Cow DAO, *What is Loss-Versus-Rebalancing (LVR)?*, https://cow.fi/learn/what-is-loss-versus-rebalancing-lvr

1. Though the origin of the name MEV and its systematic study started at [FB2]. ↩︎
2. An example of a scenario close to this ideal is to allow a small trade fee that is sublinear in the traded amount. ↩︎
3. The same general approach can be found in [CF], as is apparent from the title. However the concrete mechanism described there is different from the one proposed here. Additionally, [RGGM] studies uniform price batches where AMMs swap at the prices of the batch. ↩︎
4. This can be implemented without calling ERC20 approvals between contracts. ↩︎
5. Most of the extracted MEV is being distributed through MEV-BOOST. See some numbers at https://mevboost.pics/ and https://eigenphi.io/. ↩︎

## Replies

**r4f4ss** (2024-07-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/sergioyuhjtman/48/12388_2.png) sergioyuhjtman:

> The proposal is to let W allow anyone to execute a batch. The block proposers, as always, will exercise their right to choose the transactions they prefer, possibly through a PBS mechanism

Can you elaborate more please? Does it means block proposer will be able to reorder, exclude and include transactions in the batch? Can any order be freely matched with any affiliated swap?

---

**sergioyuhjtman** (2024-08-01):

[@r4f4ss](/u/r4f4ss) Thanks, I added a small clarification:

“The proposal is to let *W* allow anyone to execute a batch, as long as there are no price inconsistencies within each block.”

-Following the fundamental property (a), reordering is meaningless.

-Which batch gets included in the block is decided at block building level.

---

**r4f4ss** (2024-08-01):

Thanks for the clarification, I got it better now.

Correct me if I am wrong, but the main difference between your purpose and [COW](https://cow.fi/cow-protocol) is that W only allows authorized affiliated AMM to be used, and it prevents some MEV attacks.

I had not noted that MEV attacks were possible in COW, and I wonder if they are performed for real since COW uses a deposit and can punish bad actors. Anyway, your solution seems more decentralized and resilient, also limiting the block proposer from searching for “cheap” swaps outside affiliated ones.

The fees of W and also rewards for block builders are relevant, I am looking forward to how this will be designed.

---

**sergioyuhjtman** (2024-08-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/r4f4ss/48/17060_2.png) r4f4ss:

> Correct me if I am wrong, but the main difference between your purpose and COW is that W only allows authorized affiliated AMM to be used, and it prevents some MEV attacks.

This is wrong indeed. W allows to use other AMMs in the batch. This is mentioned in the “final remarks” and represented in the diagram. The uniform price constraint does not apply to non-affiliated AMMs, allowing solvers to take advantage of them.

---

**quintuskilbourn** (2024-08-16):

It seems as though your argument that honest batches may be the most profitable batches to submit in large part rests on the idea that the value of censoring orders (and in so doing improving the censor’s own price) will be less valuable than the sum of censored trade fees. However, this is not clear to me. These quantities are related but can be very separated. Consider that a swap of 1 ETH and another of 1K ETH both consume the same amount of gas (keeping the pools fixed).

---

**sergioyuhjtman** (2024-08-21):

Thanks [@quintuskilbourn](/u/quintuskilbourn)! This touches the core of the issue, so it leads me to clarify and re-explain some points and also add a few things.

In general terms, I consider your statement correct and this is why I’ve left open the possibility of a trade fee. This means a fee –beyond the gas fee– that is increasing (possibly sublinearly) in the traded amount. See the first of the “final remarks”. The way I would implement this according to what I think today, is to allow trade orders to specify freely the maximum gas+trade fee. There are however good reasons to believe that the market will permit low trade fees. Moreover, I wouldn’t rule out zero trade fee as a common practice. Notice that each of the following two facts contradicts your first statement, strictly speaking. Allow me to repeat myself here and there.

-Since the mechanism clusters together the most liquid tokens, once you mess with the price of one token you break the equilibrium of the whole cluster. Thus you may miss not only censored trade orders but also trade orders corresponding to different pairs that fell off because you moved the price.

-The presence of honest solvers will enable users to send their orders exclusively to them. As a result, dishonest solvers will be at a significant disadvantage, as they will miss out on a crucial portion of the order flow.

The role of honest solvers would likely converge with that of block builders. This role is inherently oligopolistic: since the total revenue will only represent a marginal portion of the block’s value due to the proposer’s monopoly, a large number of honest solvers would be unsustainable. The permissionless feature gives fluidity to the system, allowing the replacement of the members of this oligopoly.

A nice feature of this picture is that it naturally defines what is a honest solving algorithm. If it converges with block building, it would be way more transparent than current status quo where it is even unclear which behaviors are ethically acceptable, and the algorithms used by top block builders are hidden.

