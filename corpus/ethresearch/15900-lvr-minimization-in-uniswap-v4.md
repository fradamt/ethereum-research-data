---
source: ethresearch
topic_id: 15900
title: LVR-minimization in Uniswap V4
author: The-CTra1n
date: "2023-06-16"
category: Decentralized exchanges
tags: [mev]
url: https://ethresear.ch/t/lvr-minimization-in-uniswap-v4/15900
views: 7088
likes: 14
posts_count: 12
---

# LVR-minimization in Uniswap V4

*This research has received funding from the Uniswap Foundation Grants Program. Any opinions in this post are my own.*

The long-anticipated [release of Uniswap V4](https://github.com/Uniswap/v4-core/blob/main/whitepaper-v4-draft.pdf) is upon us. This blog post sketches a straightforward combination of a singleton pool and hooks within the new V4 framework to tackles cross-domain MEV at the source: the block producer, or searchers paying for that privilege.

Recently, I’ve been doing research on cross-domain MEV sources within the DEX ecosystem, and it almost always came back to the same term: *Loss-versus-rebalancing* or *LVR*. LVR put a name to the face of one of the primary costs incurred by DEX liquidity providers. Block builders on any chain are being goose-stepped into profit-maximizing machines. To do this requires a knowledge of the most recent state of the primary exchanges and market-places. Typically, these take the form of centralized exchanges and other large-volume DEXs, not to mention the swaps in the mempool (discussion for another post).

The first, **guaranteed** cost that a DEX must pay each block is that of arbitraging the DEX’s stale reserves to line up with the block builders best guess of where the underlying price is. From here, the builder then sequences the DEX swaps in a way so as to maximize the builders back-running profits. This proceeding sequence of back-runs pays fees to the pool, but are not guaranteed to take place.

It is only the arbitrage of the pool reserves that is guaranteed. *Luckily, this can be addressed with hooks*.

The exact implementation of hooks hasn’t been nailed down yet, but in this article we assume, as in the whitepaper, that a hook implements custom logic before or after 4 key phases in the pool contract:

1. Initialize: When the pool is deployed
2. Modify Position: Add or remove liquidity.
3. Swap: Execute a swap from one token to another in the V4 ecosystem.
4. Donate: Donate liquidity to a V4 pool.

**The Solution: Low-Impact re-addition of retained LVR into the liquidity pool**

Our proposed solution is based on techniques formalized as the [Diamond protocol](https://arxiv.org/abs/2210.10601), with similarities to [another ethresearch post](https://ethresear.ch/t/mev-minimizing-amm-minmev-amm/13775). We are only interested in hooks before and after swaps. For a particular pool, we need to make a distinction between the first swap interacting with the pool in a block and all other swaps.

For our solutions we introduce an LVR rebate function \beta: \{1,...,Z \} \rightarrow [0,1]. It suffices to consider \beta() as a strictly decreasing function with \beta(Z)=0, for some Z \in \mathbb{N}. Whenever we call a hook, let B_\text{current} be the current block number when the hook is called, and B_\text{previous} be the number of the block in which the most recent swap occurred. We also need to introduce the idea of a vault contract \texttt{vault}, and a hedging contract \texttt{hedger}.

Depositing x_A token $A$s to \texttt{hedger} increases a contract variable \texttt{hedgeAvailableA} by x_A (likewise \texttt{hedgeAvailableB} for token B deposits).  At all times, the block builder can submit a transaction removing some amount of tokens x_A from \texttt{hedger} if at the end of the transaction \texttt{hedgeAvailableA}>x_A. If the builder withdraws x_A tokens, reduce  \texttt{hedgeAvailableA}  by  x_A.

**Solution Description**

In this solution, consider the following logic(described algorithmically as \texttt{beforeSwap()} and \texttt{afterSwap()} hooks in Algorithms 1, 2, and 3):

- \textbf{If}  \ B_\text{current}-B_\text{previous}>0, the swap is the first swap in this pool this block. Send any remaining tokens in \texttt{hedger} to pool. After this, add some percentage of the tokens in \texttt{vault} back into the pool. The correct percentage is the subject of further research, although we justify approximately 1% later in this post. Set the \texttt{hedgeAvailable} variables to 0.
 Execute 1-\beta(B_\text{current}-B_\text{previous}) of \texttt{swap}_1, and remove the required amount of token A from the pool so the implied price of the pool is equal to the implied price given \texttt{swap}_1 was executed. This is necessary because if only 1-\beta(B_\text{current}-B_\text{previous}) of \texttt{swap}_1 is executed the price of the pool will not be adjust to reflect the information of \texttt{swap}_1. Add the removed tokens to \texttt{vault}.
- \textbf{Else}, it must be that B_\text{current}-B_\text{previous}==0, which implies the swap is a \texttt{swap}_2. Let \texttt{swap}_2 be buying some quantity x_A of token A. One of the following three conditions must hold:

 \textbf{If }\texttt{hedgeAvailableA}\geq x_A  AND x_A>0, then execute \texttt{swap}_2 and decrease \texttt{hedgeAvailableA} by x_A, but do not remove any tokens from \texttt{hedger}. Increase \texttt{hedgeAvailableB} by x_B.
- \textbf{Else if } \texttt{hedgeAvailableB}\geq x_B  AND x_B>0, then execute \texttt{swap}_2 and decrease \texttt{hedgeAvailableB} by x_B, but do not remove any tokens from \texttt{hedger}. Increase \texttt{hedgeAvailableA} by x_A.
- \textbf{Else} there is not enough tokens deposited to perform the swap, then revert.

**What does this solution solve?**

This solution allows the producer to move the price of the block to any level with \text{swap}_1, although only executing 1-\beta(B_\text{current}-B_\text{previous}) of \text{swap}_1. This \text{swap}_1 can be thought of as the LVR swap, and is such it is discounted. From there, the producer is forced to match buy orders with sell orders. Orders are only executed against the pool if they can also be executed against the tokens in the hedge contract \texttt{hedger}. If the price does not return to the price set after \text{swap}_1 (the tokens in \texttt{hedger} don’t match the \texttt{hedgeAvailable} variables,) there are sufficient tokens in \texttt{hedger} to rebalance the pool, and these tokens in the hedging contract are used to do so in the next block the pool is accessed.

An ideal solution would allow the producer to execute arbitrary transactions, and then repay \beta of the implied swap between the start and end of the block, as this is seen as the true LVR (the end of block price is the no-arbitrage price vs. external markets, otherwise the producer has ignored a profitable arbitrage opportunity). Our solution does this in a roundabout way, although using hooks. The producer moves the price of the block to the no-arbitrage price in the first swap, and is then forced to return the price here at the end of the block, all through hooks.

**Does the solution work?**

\texttt{yes}

How? This solution differs from the theoretical proposal of that of Diamond in 2 important functional ways. Firstly, Diamond depends on the existence of a censorship-resistant auction to convert some % of the vault tokens so the vault tokens can be re-added into the liquidity pool. The solution provided above directly readds the vault tokens into the pool. Through simulation, we have identified the solution provided in this post approximates the returns of Diamond and its perfect auction when the amount being re-added to the pool is less than 5% per block.

**Don´t just take our word for it!** The simplest solution in Diamond periodically re-adds the retained LVR proceeds from the vault into the pool at the pool price. We include the graph of the payoff of this protection applied to Uniswap V2 pool vs. a Uniswap V2 pool without this protection. The payoff of this protocol is presented below. [![](https://ethresear.ch/uploads/default/optimized/2X/8/825779a183459ee004ee83281fcfa6e67ea402be_2_666x500.png)3200×2400 269 KB](https://ethresear.ch/uploads/default/825779a183459ee004ee83281fcfa6e67ea402be).

(The core code used to generate these simulations is [available here](https://github.com/The-CTra1n/LVR/blob/main/ReAdd.py).)

We ran some simulations to compare our solution to the theoretical optimal of Diamond. We chose a $300M TVL ETH/USDC pool at a starting price of $1844, and a daily volatility of 5%. These simulations were run The expected returns of the Diamond-protected pool relative to the unprotected pool over 180 days (simulated 1,000 times) is 1.057961. This is almost exactly equal to the derived cost from [the original LVR paper](https://arxiv.org/pdf/2208.06046.pdf) of 3.125bps per day, computed as  \frac{1}{(1-0.0003125)^{180}} \approx 1.05787. That’s a saving of $17M over half a year!

Unfortunately, 100% LVR retention is unrealistic. Let’s instead assume an average LVR retention of 75% (LVR rebate value \beta of 0.75). Through simulation, the Diamond-protected UniV2 pool gives a relative return vs the unprotected UniV2 pool of 1.0431.

Compare this to the relative returns of the protocol described in this post applied to a UniV2 pool vs the unprotected UniV2 pool. These simulations are plotted below for several re-add percentages (the amount of the vault tokens (retained LVR) to be re-added to the pool each block). The average relative returns are 1.0456, 1.0436, and 1.0335, for re-add percentages of 1%, 5%, and 12.5% respectively. [![](https://ethresear.ch/uploads/default/optimized/2X/d/d10fd96626fd581b32e3ae9c76cca0c4129c1d6c_2_666x500.png)3200×2400 256 KB](https://ethresear.ch/uploads/default/d10fd96626fd581b32e3ae9c76cca0c4129c1d6c)

From this, we can see that the 1% re-add strategy each block actually *outperforms* the optimal conversion strategy (1.0456 for % re-adding vs. 1.0431 in Diamond). This is because for simulations with large moves, converting the pool is less profitable. Without fees, HODLing is optimal, and re-adding less tokens approaches some form of HODLing. If we introduce fees related to pool size, we can counteract this out-performance.

In the following graph, we include a representation of the performance of the theoretical conversion protocol of Diamond (pink), the low-impact re-adding protocol of this post with re-add % of 1% (blue), and HODLing (orangey). All of these returns are vs. the corresponding unprotected UniV2 pool.

[![](https://ethresear.ch/uploads/default/optimized/2X/3/3ca157d0afb08050e451b6eee35c2eded92ebbd6_2_666x500.png)3200×2400 236 KB](https://ethresear.ch/uploads/default/3ca157d0afb08050e451b6eee35c2eded92ebbd6)

**Considerations and Limitations**

Re-adding tokens from the pool to the vault creates an expected arbitrage opportunity in the next block, so re-adding less tokens intuitively reduces the losses (increases the profitability of the pool).

To access the pool, someone must submit the initial pool swap, and then deposit tokens to the \texttt{hedger} contract. However, as we typically expect searchers to be profit maximizing, we should then expect these same searchers to back run any set of buy or sell orders to the no-arbitrage price.

It is possible that the tokens in \texttt{hedger} can be used for this back-running. The balance of \texttt{hedger} can also be updated mid-block before all swaps are executed. This may be necessary if tokens are required mid-block, with benefits outweighing the gas cost to exit and re-enter tokens to \texttt{hedger}.

There are lots of other quirky potential possibilities with hooks on top of this core LVR-retention framework. This post is intended to demonstrate one of the many possibilities that hooks give us.

**Algorithm Pseudocode**

[![image](https://ethresear.ch/uploads/default/optimized/2X/c/cb7bf91d55b56e359a6cfda5ba8b54220bb1a590_2_649x500.png)image970×747 167 KB](https://ethresear.ch/uploads/default/cb7bf91d55b56e359a6cfda5ba8b54220bb1a590)

[![image](https://ethresear.ch/uploads/default/optimized/2X/5/59c7b37dc121efb7d2db48d37892fe71e0fceaed_2_690x338.png)image1190×584 88.2 KB](https://ethresear.ch/uploads/default/59c7b37dc121efb7d2db48d37892fe71e0fceaed)

[![image](https://ethresear.ch/uploads/default/optimized/2X/0/0ea3028e27c59698499308513b2e3ee15f8a2a02_2_690x303.png)image957×421 59 KB](https://ethresear.ch/uploads/default/0ea3028e27c59698499308513b2e3ee15f8a2a02)

## Replies

**The-CTra1n** (2023-06-19):

Another variation of this protection is for the afterSwap() hook to ensure the hedger contract has \beta of the removed tokens from the start of the block. These tokens are then re-added to the pool at the start of the next block, while \beta of the tokens added in the last block are sent to the builder controlling the hedger contract in the previous block. Tokens are then added to the vault from the pool to ensure the price at the end of the previous block is now the price of the pool (in the same way the vault is updated in the main post).

Assuming the builder leaves the pool at the profit-maximising price, both the protocol in the main post, and this simple variation have the same payoff and token requirements for the builder. The variation described here gives a stronger feeling that the pool LPs are doing something, effectively providing 1-\beta of the liquidity on every order.

An important open question still remains: If the pool wants to retain \beta of the LVR, can the pool deploy more than 1-\beta of its liquidity?

Solutions auctioning off the right to execute the first transaction in a pool, [such as McAMMs](https://ethresear.ch/t/mev-capturing-amm-mcamm/13336), beg the same question. All of these solutions are forcing the builder (or winning searcher) to repay some \beta of the (expected in the case of McAMMs) LVR.

Latency reduction is [proven to tackle LVR](https://moallemi.com/ciamac/papers/lvr-fee-model-2023.pdf), but effective solutions to this for slow, secure L1s (such as a [shared sequencers](https://dba.mirror.xyz/NTg5FSq1o_YiL_KJrKBOsOkyeiNUPobvZUrLBGceagg)) are still being theory-crafted. (h/t Dan Robinson for in-depth conversations on this).

---

**dcrapis** (2023-08-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/the-ctra1n/48/9792_2.png) The-CTra1n:

> For a particular pool, we need to make a distinction between the first swap interacting with the pool in a block and all other swaps.

I’m curious if beyond the simulation you’ve also looked at historical data on, say, some ETH/USDC pool, looking at first “guaranteed” swaps versus next.

I liked the paper+sims, but still trying to navigate the details of the solution implementation here. Also curious if there was any update to this since the initial post? Thanks!

---

**The-CTra1n** (2023-08-10):

Hey Davide. I never had the chance to look at real-world data, but my intuition was definitely shifting more to a protocol like that mentioned in my [response](https://ethresear.ch/t/lvr-minimization-in-uniswap-v4/15900/2). This takes the “pressure” off of the first transaction. There are several works out there on LVR estimation ([Frontier have something like it](https://frontier.tech/a-new-game-in-town), thiccythot had something similar but the query doesn’t work anymore). These look at the net trades.

It would definitely be nice to be more granular here, ranking the trades based on the implied LVR, and identify where they are taking place in the block.

I’m currently working on implementing Diamond as a Uniswap V4 pool. There are some interesting problems related to adjusting pool liquidity as required in the proposed Diamond solution. Overall though, the skeleton has remained the same, for now at least.

---

**sm-stack** (2023-08-12):

Thanks for deep research and effort to improve LP earnings!

I have a question about a possible vulnerability in this hook. What happens if a block producer deliberately doesn’t put his transaction at the very first of a block? What I thought was, a transaction of a common user will be regarded as the transaction of block producer, and then the AMM cannot fulfill the initial requirements of swap he requested.

So I’d ask you if there is an effective way to detect the user is arbitrageur or not in the contract code.

---

**TheNonEconomist** (2023-08-15):

[@The-CTra1n](/u/the-ctra1n) This is wonderful work. I highly recommend you look at how stock exchanges pay rebates to market makers (It’s TradFi equivalent of what you’re trying to implement).

You can’t predict price so why not do it post-fact?

On the other hand, have you thought about who would operate the vault? There’s actually a quite a bit of issue with exchanges paying rebates because it comes at a pretty high cost to them so it incentivizes them to start discriminating LPs based on how much “quality” they add/value they bring to exchanges.

---

**The-CTra1n** (2023-08-31):

With the Uniswap V4 Hook framework, you can do a straightforward check that the first transaction in the block is designated as the arbitrage transaction (first depositing collateral in the hedger contract for example). This forces the block builder to play by our rules.

---

**The-CTra1n** (2023-08-31):

The vault is intended to be non-discriminatory, allowing anyone to contribute/receive rebates. Saying that, it is there to protect users (and incentivize users) providing liquidity around the current pool price.

When the vault fills up with LVR rebates, these rebates are simply retained tokens from LP positions that would otherwise have been traded against if the LVR rebate param was 0. Thus, every time the vault fills up with some amount of tokens X_i for block i, the %s of X_i owed to the respective LPs are in direct proportion to the % of liquidity that each LP provided over the pool move in block i.

If an LP was providing liquidity outside of the [starting pool price in block i, final pool price in block i] range, that LP doesn’t own/is not owed any of the X_i.

Does that address your concern?

---

**TheNonEconomist** (2023-08-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/the-ctra1n/48/9792_2.png) The-CTra1n:

> If an LP was providing liquidity outside of the [starting pool price in block i, final pool price in block i] range, that LP doesn’t own/is not owed any of the Xi.

It makes sense that you’re reducing down good LPing (good for price efficiency) into a simple operation where LPs just have to know the bounds - therefore complexity of becoming a high quality LP (again measured by how much price efficiency is provided from) is fairly low (in theory at least).

Just recommend making sure the starting and final pool prices are easily accessible at reasonable latencies for everyone.

As for potential “unseen” problems to think about, some thoughts are - 1) Again with starting and final pool prices being accessible at different latencies (gated by infra, cost, dev capability, etc…) could effectively cause discrimination of LPs; 2) Active LPing causing toxic returns for Passive LPs still not really solved at the fundamental level. Just rebates are paid so they have sth to make up for it. This isn’t strictly LVR and is a market quality issue it’s a step beyond LVR.

Some notes:

Problem 1: Given where blocktime is now, doubt it’s an issue but once blocktime goes down might come up. So keeping in the backlog is important IMO. (This is an engineering problem clearly)

Problem 2: Getting rid of JIT (essentially getting rid of toxicity caused by active LPs) turns an AMM into a more batch auction like market, which is not desirable.

---

**anirudhreddyrachamal** (2024-11-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/the-ctra1n/48/9792_2.png) The-CTra1n:

> Send any remaining tokens in \texttt{hedger}hedger\texttt{hedger} to pool

These tokens are added by the arbitrageur right but why are these tokens added to the pool. shouldn’t they go back to the arbitrageur at the start of the next block?

---

**The-CTra1n** (2024-11-28):

An arbitrageur should only put in the amount of tokens they need. They can also withdraw themselves, better for the arbitrageur themselves to pay for it, rather than charging the following arbitrageur for the transfer.

---

**keroshanpillay** (2025-03-04):

How does this perform under more volatile conditions? The simulation are for moderate vol (5% daily) – would this still operate nominally in a flash crash / liquidation cascade?

