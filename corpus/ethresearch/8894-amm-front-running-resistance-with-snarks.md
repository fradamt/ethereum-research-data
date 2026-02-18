---
source: ethresearch
topic_id: 8894
title: AMM front-running resistance with SNARKs
author: 0xBeaver
date: "2021-03-11"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/amm-front-running-resistance-with-snarks/8894
views: 4152
likes: 9
posts_count: 12
---

# AMM front-running resistance with SNARKs

Front-running on AMMs is a big (and expensive) problem. It causes lost money during large swaps and also **raises gas prices unnecessarily** due to bidding wars between bots.

**I propose a simple method to mitigate AMM front-running by applying zero-knowledge proofs (ZKPs) for updating the swap ratio.**

### Abstract

Each swap transaction on an AMM can “hide” the updated pool ratio (and therefore resulting price) by means of a SNARK puzzle, thereby making price-prediction of a transaction in the mempool expensive and uncertain, significantly deterring front-running.

### Scenario

Let’s assume that we have a Uniswap-like pool for the ETH/BTC pair. The mechanism is pretty simple.

1. A trader executes a swap and updates the pool ratio but hides the details in a SNARK that proves the AMM mathematics remain consistent.
2. The trade transaction contains a hint that makes it possible to guess the ratio by n times of hash computation (where n should not be too large to prevent falling into limbo). So anyone can compute the updated pool ratio by solving the SNARK puzzle after n computations.
3. Front-runners will fail to predict the price change easily and will be deterred from making a sandwich attack due to uncertainty.

And here we can add some tokenomics to run the system more efficiently.

1. The trader can decide the SNARK puzzle difficulty n in the swap transaction.
2. The trader should stake x amount of tokens, where x should be proportional to n.
3. After the swap, one of two things can happen:
a. If the trader reveals within 10 minutes, the staked tokens go back to the trader.
b. If the trader does not reveal within 10 minutes, anyone can withdraw the staked tokens by submitting the SNARK puzzle answer.

### Difficulty Fee

Since increasing puzzle difficulty (`n`) protects the trader while imposing a potential cost on others, we can also implement a “difficulty fee”, taken from the staked tokens `x` if `n` is beyond a certain threshold.

![difficulty fee](https://i.imgur.com/5Ri1CYcl.png)

### Implementation

With this idea, I designed an anti-front-running AMM protocol “Snarkswap” based on Uniswap math. You can see the detail protocol design [here](https://github.com/0xBeaver/snarkswap-specification), and the implementation [here](https://github.com/0xBeaver/snarkswap).

### I need your feedback

Please let me know what you think of this idea, thank you!

## Replies

**0xkangaroo** (2021-03-11):

Funny seeing two threads at the top trying to tackle the same problem. Here’s the other thread I’m referring to: [A simple strategy for Uniswap? - #7 by Mister-Meeseeks](https://ethresear.ch/t/a-simple-strategy-for-uniswap/8329/7)

I like this approach because it’s a very elegant and novel, since not many people are looking at using ZKPs for this purpose. However, I think there are a few economic issues that still need to be figured out. And also, I am wondering if you have an estimate for how much gas this would take?

---

**0xBeaver** (2021-03-11):

Here is the gas reporter result. I expect `swapInTheDark` can be reduced roughly to 350K by packing up the input signals. I expect users may use `swap` (exactly same as Uniswap’s) in general and use `swapInTheDark` only sometimes.

```auto
·---------------------------------------|---------------------------|----------------|----------------------------·
|          Solc version: 0.8.1          ·  Optimizer enabled: true  ·  Runs: 999999  ·  Block limit: 9500000 gas  │
········································|···························|················|·····························
|  Methods                                                                                                        │
·····················|··················|·············|·············|················|··············|··············
|  Contract          ·  Method          ·  Min        ·  Max        ·  Avg           ·  # calls     ·  eur (avg)  │
·····················|··················|·············|·············|················|··············|··············
|  ERC20Tester       ·  approve         ·      44513  ·      44525  ·         44525  ·          86  ·          -  │
·····················|··················|·············|·············|················|··············|··············
|  ERC20Tester       ·  transfer        ·      36126  ·      51138  ·         48831  ·         111  ·          -  │
·····················|··················|·············|·············|················|··············|··············
|  NotePool          ·  deposit         ·     186830  ·     186854  ·        186850  ·          45  ·          -  │
·····················|··················|·············|·············|················|··············|··············
|  NotePool          ·  initialize      ·      65501  ·      65525  ·         65522  ·          55  ·          -  │
·····················|··················|·············|·············|················|··············|··············
|  NotePool          ·  withdraw        ·     353517  ·     368577  ·        358130  ·          23  ·          -  │
·····················|··················|·············|·············|················|··············|··············
|  Sandglass         ·  initialize      ·     149448  ·     149472  ·        149469  ·          55  ·          -  │
·····················|··················|·············|·············|················|··············|··············
|  SnarkswapFactory  ·  createPair      ·    4034723  ·    4034745  ·       4034737  ·          55  ·          -  │
·····················|··················|·············|·············|················|··············|··············
|  SnarkswapFactory  ·  setFeeTo        ·          -  ·          -  ·         43458  ·           2  ·          -  │
·····················|··················|·············|·············|················|··············|··············
|  SnarkswapFactory  ·  setFeeToSetter  ·          -  ·          -  ·         28437  ·           1  ·          -  │
·····················|··················|·············|·············|················|··············|··············
|  SnarkswapPair     ·  burn            ·     101526  ·     171737  ·        132802  ·           8  ·          -  │
·····················|··················|·············|·············|················|··············|··············
|  SnarkswapPair     ·  mint            ·     150345  ·     173647  ·        151482  ·          51  ·          -  │
·····················|··················|·············|·············|················|··············|··············
|  SnarkswapPair     ·  swap            ·      77320  ·     107344  ·        103564  ·          24  ·          -  │
·····················|··················|·············|·············|················|··············|··············
|  SnarkswapPair     ·  swapInTheDark   ·     598040  ·     598136  ·        598078  ·          35  ·          -  │
·····················|··················|·············|·············|················|··············|··············
|  SnarkswapPair     ·  sync            ·      54211  ·      84211  ·         74211  ·           3  ·          -  │
·····················|··················|·············|·············|················|··············|··············
|  SnarkswapPair     ·  transfer        ·      36227  ·      36239  ·         36235  ·           3  ·          -  │
·····················|··················|·············|·············|················|··············|··············
|  SnarkswapPair     ·  undarken        ·     182177  ·     182249  ·        182201  ·          14  ·          -  │
·····················|··················|·············|·············|················|··············|··············

```

---

**0xkangaroo** (2021-03-11):

So it’s basically 598078 gas to `swapInTheDark` and then 182201 to `undarken` (or `reveal`), right?

That’s 780k gas on average, which is a lot. But I guess this would mostly be used for larger amounts anyway.

---

**dankrad** (2021-03-11):

An interesting idea. But the transaction needs to not just hide the updated pools and ratios, but also the transaction size itself. It may be possible when applied to fully private versions of the cryptocurrencies/tokens.

The primitive you are looking for is actually not a hash, but a verifiable delay function or “VDF”. The hash/proof of work puzzle you suggest can be easily parallelized and thus a frontrunner with large resources can still frontrun. Since you want the puzzle to be solvable, it isn’t really possible to take this out of reach of well resourced attackers.

A VDF however has the property that it can’t be parallelized and takes a minimum amount of time to be solved. If the transaction thus gets included before that time has expired, you can be sure that it can’t be frontrun.

---

**0xBeaver** (2021-03-12):

That’s correct. It’s expected to be useful for large amount swap & maybe on L2.

---

**0xBeaver** (2021-03-12):

Firs of all thank you so much for your valuable feedback.

> An interesting idea. But the transaction needs to not just hide the updated pools and ratios, but also the transaction size itself. It may be possible when applied to fully private versions of the cryptocurrencies/tokens.

Private pool will be perfect for this. However, hiding the trade is a sell or a buy can be enough to confuse the front-runner.

> The primitive you are looking for is actually not a hash, but a verifiable delay function or “VDF”. The hash/proof of work puzzle you suggest can be easily parallelized and thus a frontrunner with large resources can still frontrun. Since you want the puzzle to be solvable, it isn’t really possible to take this out of reach of well resourced attackers.

For example if the seed of the VDF is a commitment on chain, the front runner can prepare theft transactions behind the mempool everytime. And if a profitable swap is catched on the mempool then they will just release it or abandon. So this cannot protect the trade from front-running.

To be specific,

1. Commitment submitted on chain
2. A trader Tom creates a swap tx and starts to compute the VDF. Simultaneously, a front-runner Frank creates a sell tx and a buy tx together and starts to compute VDFs for each.
3. Tom sends the tx with his VDF to the mempool and Frank catches it and sends the prepared transaction.

By the way, in this snarkswap protocol, undarkening also can be front-run to steal the staking reward after 10 minutes. In this case, I think VDF will be definitely helpful.

> proof of work puzzle you suggest can be easily parallelized and thus a frontrunner with large resources can still frontrun

If any front-runner appears, I expect people will increase the difficulty and use higher gas price to be included in the block in a few seconds. But to avoid the difficulty imposes too much cost on other users, governance can adjust the fee structure for it.

---

**Mister-Meeseeks** (2021-03-15):

It’s a clever idea, but completely impractical unless I’m missing something. From skimming the implementation it seems that any individual party can unilaterally shut down trading for 10 minutes, just by “darkening” the pair.

What’s to stop someone from DoS-ing everyone’s liquidity by repeatedly darkening the contract? Why would anybody prefer to add liquidity to a venue where it can be arbitrarily locked up? (Remember front running is not a downside for liquidity providers.) Even without an intentional DoS, a highly active pair like ETH/USDC would pretty much be locked up 24/7.

Predatory bots would wind up abusing this mechanism as a free option. Wait until a volatile period, then buy in the dark. Wait ten minutes. If the price moved in your favor, buy the token at the earlier locked in price. If the price moved against you, just abandon the SNARK.

I think sooner or later someone will come up with a solution to front-running. Or at least a series of improvements that makes it so minor of an issue that hardly anyone cares. But any sort of protocol that relies on shutting down, or even slowing down trading will never catch on in the broader market.

> However, hiding the trade is a sell or a buy can be enough to confuse the front-runner.

Probably not for the majority cases. Practically speaking front runners are only interested in front-running buys, since there’s no easy way to short sell and they don’t want to carry inventory. 95%+ of buys are for more a buyer who’s currently holding zero tokens. So if I see that Alice sent a transaction for one million tokens, but I’m not sure if it’s a buy or a sell, I can guess with pretty high accuracy just by checking whether she’s currently holding a million or more tokens right now.

---

**0xBeaver** (2021-03-16):

Thanks for pointing out good points.

1. Trade frequency.
 Except ETH/USDT pool, the trade frequency is pretty low for almost pools. ETH/WBTC is the top 5 pool and it took 1.8 minutes per tx during last 15 hours. In addition, the main target of this protocol is a small pool that has a high slippage rate thus many chances exist for front-runners. ETH/RARI Uniswap pair is a good example which trade volume is top 22 today. Its trade frequency was 2.3 minutes per tx during last 20 hours and 13 front-running drained up to 5%. It means that most transactions are safe to use swap(that does not freeze the pool) and only 13 txs needed to use the swapInTheDark feature. Therefore, pools will be remained undarkened in general.
2. DoS
 Before starting to talk about DoS, let me clarify a little bit about darkening. Darkening does not always lock the pool for 10 minutes. The 10 minutes is just a prioritized period for the darkener of reveal. If anyone reveals the resulting ratio in a few minutes, then it unlocks the pool immediately. But as you pointed out, DoS is still possible. So we can use a fee model just like fee = darkenedPeriod * Difficulty. Then, the darkener will try to reveal the trade as soon as possible to save the fee, and it may not affect the average trade frequency.
 Let’s see the case, You can see the latest sandwich attacks here, and front-runners drained about 2 ETH using 4 txs in this case.
1020×211 22.2 KB
Here’s the calculation of the expense. Let’s assume that

hashRate = 33000 hash / second
3. difficulty = 30 (MAX)
4. expectedSolvingTime = 9 hours (2^(difficulty)/hashRate)
5. fee = darkenedPeriod * difficulty * k
6. k = 0.0001 ETH(The governance can decide this rate)
7. feePerMinute = 0.18 ETH
8. feePerBlock = 0.036 ETH
9. gas price for fast confirmation = 439 GWei (This data are from the trade tx))
10. avg gas price = 240 GWei (Ethereum Transaction Hash: 0xbd2b150d5d... | Etherscan)
11. Darkening tx fee = 598K * 230GWei = 0.14 ETH
12. Undarkening tx fee = 182K * 439GWei = 0.08 ETH
13. At least 6 darkening tx = 0.84 ETH.
14. At least 6 undarkening tx = 0.48 ETH.
15. 1 hour of darkening fee = 10.8 ETH.
16. ~= 12.1 ETH
17. Buy/Sell guess

> I can guess with pretty high accuracy just by checking whether she’s currently holding a million or more tokens right now.

 It is a really important point that you are just guessing. I can buy more RARI while holding a bunch of RARI. Or I can sell my whole RARI. How will you do? Only holding a small amount of token can confuse you.

---

**0xkangaroo** (2021-03-16):

**1. 10 minutes delay**

![](https://ethresear.ch/user_avatar/ethresear.ch/0xbeaver/48/5514_2.png) 0xBeaver:

> The 10 minutes is just a prioritized period for the darkener of reveal. If anyone reveals the resulting ratio in a few minutes, then it unlocks the pool immediately.

Interesting, so anyone can `undarken`, even if less than 10 minutes? But that person won’t get the staked amount, right? What will happen to the staked amount?

**2. Public tx Info on “dark” txs**

![](https://ethresear.ch/user_avatar/ethresear.ch/0xbeaver/48/5514_2.png) 0xBeaver:

> Private pool will be perfect for this. However, hiding the trade is a sell or a buy can be enough to confuse the front-runner.

What is the actual information that the frontrunner gets when a swap is made? I was under the impression that the amounts could be hidden as well (without use of a completely private pool).

**3. Frontrun losses and volume**

Just curious, but do you have any data about how often large transactions are frontrun? I think it gives us a better idea of the potential size and usage of the proposed AMM.

---

**0xBeaver** (2021-03-16):

> Interesting, so anyone can undarken, even if less than 10 minutes? But that person won’t get the staked amount, right? What will happen to the staked amount?

Right, it goes back to the original staker if it’s revealed within 10 minutes. Otherwise the staked amount goes to the revealer. Please note that it will return the remaining amount after charging the fee. (I need an idea about how to call this fee ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12) .) Anyway the 10 minutes of prioritized period is to protect the staker. It’ll be good for the protocol to make pools undarkened as soon as possible. But if there’s no protection period for the staker, people will front-run the revealing tx to steal the staked amount.

> What is the actual information that the frontrunner gets when a swap is made

1. Hashes of 2 input notes and 2 output notes.
Whole information of a note which is just deposited is public. I’ll call this kind of note as a ‘deposit note’. Except the deposit notes, front-runner cannot know the exact amount of the note and its token address but can guess its minimum amount or possible token addresses. To guess the details, the front-runner may have to label all notes in own database system.
2. A mask, hReserves, and hRatio.
The front runner will get hReserves. hReserves are manipulated new resulting reserve values(a.k.a. the swap details) by randomly manipulating the bits which is masked by the given mask. And for the SNARK puzzle, the darkener gives hRatio that is a hash of the new reserves and a salt. You can see more details about them in the spec repo.
About hRatio: GitHub - 0xBeaver/snarkswap-specification
About hReserves & mask: GitHub - 0xBeaver/snarkswap-specification

> Just curious, but do you have any data about how often large transactions are frontrun?

I am sorry that I don’t have the exact data, but it seems that the front-runners are draining ETH usually in small pools and targeting swaps which amount is over 10 ETH.

---

**sunset1919** (2021-04-15):

Interesting idea,  i don’t know zksnark very well.   What the zero knowledge proof is used for?  I mean is it used to check:

Swap parameters of client are the same  to  that on chain while transaction execute on chain ?

