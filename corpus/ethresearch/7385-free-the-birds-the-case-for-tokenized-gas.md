---
source: ethresearch
topic_id: 7385
title: "Free the Birds: the Case for Tokenized Gas"
author: aliatiia
date: "2020-05-10"
category: Economics
tags: [fee-market, gas-token, gas-abstraction]
url: https://ethresear.ch/t/free-the-birds-the-case-for-tokenized-gas/7385
views: 5574
likes: 0
posts_count: 28
---

# Free the Birds: the Case for Tokenized Gas

Ethereum could potentially open a few bird cages with one key: **ETH-collateralized GAS tokens.**

### How TLDR

- There are 3 contracts:

ERC20 GAS token contract
- Credit facility (CF) contract (~oracle-less govern-less auto-pilot Sai).
- Automatic market making (AMM) contract (~Uniswap V2).

The base protocol accepts GAS tokens for **fee payment**. This does **not** undermine ETH enshrined status because GAS is ETH-backed (details below). If [this EIP](https://github.com/Arachnid/EIPs/blob/f6a2640f48026fc06b485dc6eaf04074a7927aef/EIPS/EIP-draft-rich-transactions.md) goes through, then buying gas from the AMM can become a typical 1st instruction (fill up on gas at the beginning of tx).

Anyone can **deposit** ETH into the CF to mint new GAS tokens up to a minimum over-collateralization threshold \alpha% such that \alpha \times (\frac{GAS\_minted}{ETH\_deposited})\geq a moving average (MA) GAS/ETH price. Setting \alpha  =125% is sufficient of a cushion because MA is smooth compared to the spot price.  In contrast \alpha is 133% and 150% on Compound and MakerDao, respectively.

Minters can **pool** GAS:ETH in the AMM and collect fees from traders/users (who “load up on GAS” at the beginning of the tx JIT style), as well as interest from non-pooling minters.

Anyone can **liquidate** GAS minters whose ETH collateral value falls below the over-collateralization threshold, and get a **reward** from delinquent’s ETH collateral.

A manipulation-resistant **moving average** of GAS/ETH price over `z` blocks is **maintained** as a global variable in the AMM.

GAS `transfer()` is **disabled** to incentivize GAS/ETH market depth in the AMM.

A synthetic instrument that tracks GAS price, as well as futures/options markets of said synthetic, may spawn extra-protocol, on DeFi and/or CeFi, which should further support the listed benefits below.

### Expected benefits to the protocol and its stakeholders

1. Risk-minimization: Ethereum stakeholders have access to credit without custody, oracle, or governance risk. They keep their ETHs, while still being able to pay their GAS costs or pay for other expenses by selling minted GAS for more ETH and/or stablecoins.
2. Capture-resistance: in case of a contentious fork, the community can fork off knowing they have an uncontrollable credit facility available to them, along with an uncontrollable DEX, Uniswap. These  “auto-pilot public financial utilities” are essential in case current custory-, oracle- and/or governance-centralized CFs/stablecoins choose to use their weight to decide the winning fork against community consensus.
3. Added PoS security: the CF/AMM are sinks for non-staking ETH once ETH2.0 launches. The CF interest rate and AMM trading fees can be made partially proportional to the amount of staked ETH. The extent to which non-staking ETH represents a security threat is debatable, it is however better to have this lever rather than not.
4. Incentive alignment between the protocol and high-throughput gas consumers (HTGCs) who are long ETH the token and Ethereum the protocol:

 If HTGCs believe GAS/ETH is too low, they go long: deposit ETH \rightarrow mint GAS. Spend GAS later when it’s expensive.
5. If they believe it’s too high they go short: deposit ETH \rightarrow mint GAS \rightarrow sell GAS into more ETH. Buy GAS later when it’s cheap.
6. Predictable capital expenditure by HTGCs to plan their gas budget: they can “lock-in” the price of their future gas expenditure.
7. Efficient discovery of gas macro-price: GAS/ETH discovers ~the floor price of a gas unit, i.e. the material cost of 1 gas worth of computation. The aforementioned shorting/longing in (4) contributes to this efficiency. This may also eliminate potential deadweight issues with current JIT gas production/consumption.

---

### Design goals

1. Depth of GAS/ETH market .
2. Minimalism.  Fully auto-pilot with no oracle and/or governance components.
3. Backward compatibility. ETH can still be used to JIT pay for gas as it is now.

### Contracts

- A) GAS Token
An admin-keyless non-upgradable standard ERC20 contract. Its transfer() reverts unless _to is the block producer’s address.  Hence, in v1 GAS can only be pooled, or spent on tx fees. This ensures max AMM depth \rightarrow better discovery of base gas prices. In the distant future, if the depth of GAS market exceeds a certain high threshold,transfer() can be enabled through a hardfork. Meanwhile, the market can still trade it extra-AMM by proxy through a synthetic that tracks its AMM price.
 This does not undermine the enshrined status of ETH as the sole acceptable currency for tx fees because for every GAS spent there is >=1.25x-GAS-worth of ETH locked as collateral. i.e. GAS is “marked ETH”.
- B) The GAS/ETH AMM Exchange

 zMA_GAS_PRICE: a global variable representing a volume-weighted moving average of median GAS/ETH (GAS tokens per Wei) price over z blocks, updated before the first call to trade() in a given block. Subsequent trades within said block don’t get factored in just yet in zMA_GAS_PRICE, but they will be the moment trade() is called again in a future block which inspects []latestTrades.
- []latestTrades: an array of GAS/ETH prices during block n which was the block where the AMM’s trade() was last called. When trade() is called for the first time in a block, the zMA_GAS_PRICE is updated with the previous []latestTrades, and []latestTrades is emptied out. The GAS/ETH price of this current trade() call in this current block, as well as every other trade() call within the current block, is appended to []latestTrades, to be consumed in whichever next block trade() is called, and so on. In brief, trades within block n get factored-in in the zMA_GAS_PRICE at block m>n where block m is the first time the AMM’s trade() was called since it was last called in block n. TODO: All trades within a block are executed as one big aggregate order to thwart any miner shenanigans w.r.t. the ordering the trades (hence latestTrades becomes a uint value instead of an array).
- pool(): deposit ETH and GAS into the AMM to collect trading fees and and interest.
- trade(): buy GAS with ETH or vice versa, the quote given is according to the curve.

**C) The ETH-collateralized GAS credit facility**

- deposit(uint collateralETH): deposit collateralETH Wei’s into the facility contract
- mint(uint amount): mint amount GAS tokens where 1.25*amount/collateralETH > zMA_GAS_PRICE. I.e. collateral maintenance level is 125%.
- liquidate(uint partial): aka bite, anyone can deposit GAS tokens, which are burnt, and get 0.1 * collateralETH reward from delinquent’s ETH collateral (i.e. biter gets a reward equivalent to 10% of ETH collateral). Remaining ETH is sent back to the delinquent. Implementation wise, it is simpler to require liquidators to pay the full amount of debt. However, if we imagine massive debt positions, it might be good idea to allow “partial biting”. In this case, a biter gets 0.1 * partial (note partial zMA_GAS_PRICE
- No Oracle is needed as zMA_GAS_PRICE is always updated every block the trade() function is called.

### Changes to Ethereum Clients

The gas metering functionality in clients is amended to accept GAS as payment for transactions. Backward compatibility is maintained; users choosing to pay with ETH in JIT style as is the case now can do so. If `gasprice` > 0 \rightarrow the client interprets the tx as v1, and v2 otherwise (v2 = pay from GAS in AMM.balance_of[msg.sender]).

## Cryptoeconomics

#### Interest

Interest on minted GAS is fundamentally a fee that the Ethereum protocol charges minters in return for a valuable service: a guaranteed access to its commodity (block space) at any future moment of time if they keep holding that GAS, or access to immediate liquidity if they short sell it today. **The interest formula it TBD** but it factors in:

- A utilization ratio (amount/zMA_GAS_PRICE:collateralETH ratio).
- B AMM depth (pool size). The amount of minted GAS that is being pooled.
- C total ETH staked in ETH2.0, interest rate can be made to inversely track TOTAL_ETH_STAKED, such that depositing ETH to mint GAS is more attractive the less ETH staked.

#### Trading fee:

The fees can be determined [numerically](https://twitter.com/tarunchitra/status/1242497780771426304) following, e.g., section 4.1 in [this paper](https://arxiv.org/abs/2003.10001).

#### The GAS/ETH Moving Average (MA)

The higher time frame the MA is (in units of blocks, but those can be mapped to approximate number of hours/days/weeks etc) the more prohibitive it becomes for the GAS/ETH price to be manipulated (for the sake of liquidating minters for example), but the farther away from price it will be (whether above or below). The lower time frame it is (the extreme case being 1 block, at which point the MA is basically just the price itself) the cheaper it is to manipulate the MA but the closer it is to price.

The idea of **tracking** the price of an asset as opposed to **pegging** to it [has](https://twitter.com/nmushegian/status/1240763267133423617) and [still is](https://ethresear.ch/t/metacoin-governance-minimized-oracle/7293) being seriously considered for fiat-tracking crypto assets.

There is no “peg” here as GAS/ETH floats, and the integrity of the CF is guaranteed by the safe assumption that ETH has and will continue to have a monetary premium and as such the market will be more than willing to take delinquent’s discounted ETH and bring CF to >= 125% collateral:debt ratio.

The daily MA is potentially the sweet spot between manipulation-resistance and GAS/ETH-price sensitivity, but more analysis of this is needed.

#### GAS futures and options market:

It is expected that a GAS futures market will pop up. The futures market allow someone buying (selling) GAS today to hedge against an increase (decrease) in GAS prices from now till futures contract’s expiry.

### Potential Risks

- The GAS/ETH pool is illiquid: users simply fall back to the current auction mechanism. Since only GAS contributed to the AMM pool accrues interest and fees, minters are incentivized to keep stock GAS pooled and withdraw from the pool JIT style when transacting.

mitigation: The tx fees collected by the pool could be made dynamic, inversely proportional to the amount of GAS in the pool.

Attacker stocks up on GAS when it’s cheap, launches DDoS on the network when its congested and the GAS price is high*

- mitigation: (1) block size elasticity (2) There is an incentive during this attack to mint GAS and short sell it, which will bring its price down, thereby dampening the advantage the attacker has (i.e. GAS becomes cheaper, so eventually block space becomes as cheap for everyone else as it is for the attacker), (3) The same can be said about an attacker stocking up on cheap ETH.

GAS volatility against fiat: (1) This should not be worse that ETH volatility against fiat since GAS is a less complex an instrument than ETH (assuming it becomes liquid enough) (2) The elastic block size should help counter this.

- mitigation: transfer() is disabled. GAS can only be minted, pooled, and spent on tx fees. EIP1559 or equivalent may also help.

### Future work

1. The exact interest and trading fees formulas, and the MA period.
2. Survey of traditional commodity markets esp. price stabilization strategies if there’s something to be learned there.

## Replies

**meridian** (2020-05-10):

you should look at my GasEVO thread in the EIP forum, its basically this but without the need for actually tokenizing it

**edit** I got ether magicians forum mixed up with this forum, here is the link to that: https://ethereum-magicians.org/t/gasevo-embedded-volumetric-optionality-forward-gastoken/4222

---

**meridian** (2020-05-10):

https://www.authorea.com/users/285079/articles/445804-gasevo-a-tradeable-forward-instrument-enabling-options-pricing-on-ethereum-transaction-settlement

---

**aliatiia** (2020-05-17):

Your GasEVO instrument is an interesting example of the extra-protocol instruments I mentioned:

![](https://ethresear.ch/user_avatar/ethresear.ch/aliatiia/48/4784_2.png) aliatiia:

> A synthetic instrument that tracks GAS price, as well as futures/options markets of said synthetic, may spawn extra-protocol, on DeFi and/or CeFi, which should further support the listed benefits below.

I don’t recommend that your instrument tracks [GasToken](https://gastoken.io) though. IMO GasToken is not viable generally for a couple of reasons:

- it brings more uncertainty when what  high-throughput gas consumers (HTGCs) and DeFi users actually need is more certainty. You don’t know in advance if/when gas prices will fluctuate sharply to the extend that makes acquiring/freeing junk on-chain storage economical.
- The delta of mint-free is arguably a leak/rent paid unnecessarily to the miners when in fact it’s the full node runners who should receive that delta. So it’s kind of unproductive/inefficient an asset.
- The very act of “minting” GasToken (acquiring junk storage when gas prices is cheap) quickly brings gas prices up, eating away at that delta. Its success would be its own enemy in a way.

---

**dankrad** (2020-05-17):

I don’t understand one thing here. There is no mechanism to force a block producer to accept any transaction that pays GAS instead of ETH, right? Doesn’t that mean that:

- Whenever the MA is below the current blocks gas price (defined as the lowest gas transaction that still gets included), block producers would not accept any transactions paying gas
- Whenever the MA is above the current blocks gas price, block producers would just fill up with the GAS-paying transactions

So the first one seems to make it useless as an instrument to hedge against short term gas price fluctuations. And the second one means that you will effectively always overpay when paying using GAS. Or is there something I don’t see here?

[Both of these can be overcome using EIP1559 which gives you a working gas price oracle, which the MA is not, but as far as I know you’re against it’s implementation]

---

**aliatiia** (2020-05-18):

The MA is not the spot GAS price, it’s a moving average of the spot GAS/ETH price used in the credit facility to determine liquidations / withdrawal / minting eligibility.

GAS spot price is in the AMM. And the market forces should bring it to where it should be.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> There is no mechanism to force a block producer to accept any transaction that pays GAS instead of ETH, right?

Correct. Backward compatibility is one of the design goals.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> but as far as I know you’re against [EIP1559] implementation

I am actually in support of the individual parts of EIP1559 (fee burn, block size elasticity), I just don’t think the way they are currently wired together has been proven safe beyond a reasonable doubt.

---

**dankrad** (2020-05-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/aliatiia/48/4784_2.png) aliatiia:

> GAS spot price is in the AMM. And the market forces should bring it to where it should be.

Well how could it be where it “should” be on a per block basis? I don’t see where your system includes anything resembling a per-block gas price oracle. In fact, if it did, then in a first-price auction where block producers receive all fees, they can manipulate GAS price to be anything they like and get windfall profits.

![](https://ethresear.ch/user_avatar/ethresear.ch/aliatiia/48/4784_2.png) aliatiia:

> Correct. Backward compatibility is one of the design goals.

Once again, the result of that is that it cannot be used as a hedge for urgent transactions, am I right? It feels like the only thing you would get out of this is a “hedge” for *non-urgent* transactions against permanently high gas prices.

(again, these are for non-EIP1559-implementations. In EIP1559, instead of using the MA, the price can be set to the current EIP1559 basefee plus a minimal tip and that should work as a gas hedge)

---

**aliatiia** (2020-05-18):

I should clarify: this proposal is **not** a fee market proposal. Tokenizing gas is just a way to build an auto-pilot credit facility as a public financial utility; basically a MakerDao without governance or oracle.

“Price” in this proposal is that of a bus ticket if it were market-based (i.e. not fixed by the bus authority). It’s **not** about how much to bribe the bus driver to let you take **this** next bus when there are more people than seats available:

![](https://ethresear.ch/user_avatar/ethresear.ch/aliatiia/48/4784_2.png) aliatiia:

> Efficient discovery of gas macro-price : GAS/ETH discovers ~the floor price of a gas unit, i.e. the material cost of 1 gas worth of computation. The aforementioned shorting/longing in (4) contributes to this efficiency. This may also eliminate potential deadweight  issues with current JIT gas production/consumption.

If EIP1559 is implemented in its current form, people paying the fee with GAS tokens can pay the tip by offering extra tokens to the miners.

EDIT: regarding forcing the miners to accept GAS … that’s a good point, it may be the case that the demand side of the AMM GAS/ETH is only robust if paying in GAS is mandatory, in which case for backward compatibility v1 transactions have their ETH swapped into GAS JIT style.

---

**dankrad** (2020-05-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/aliatiia/48/4784_2.png) aliatiia:

> EDIT: regarding forcing the miners to accept GAS … that’s a good point, it may be the case that the demand side of the AMM GAS/ETH is only robust if paying in GAS is mandatory, in which case for backward compatibility v1 transactions have their ETH swapped into GAS JIT style.

Well, if gas can only be paid using GAS, how do you determine the GAS/ETH exchange rate?

---

**aliatiia** (2020-05-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> how do you determine the GAS/ETH exchange rate?

The market determines that, supply and demand. The AMM is a Uniswap-like constant-function market maker (CFMM) … so the price moves along the curve.

Supply: short sellers (mint and sell), as well as miners immediately liquidating fees into ETH.

Demand: users loading up on GAS to pay JIT style and HTGCs stocking up on GAS for future use when the believe it’s at an attractive rate.

Extra-protocol synthetic instruments may also influence the AMM price as well.

---

**dankrad** (2020-05-18):

I’m talking about how you determine it if gas has to be paid using GAS tokens. Then you lose any signal about it’s current value from which transactions are included in blocks. So your “moving average” oracle would have no inputs …

---

**aliatiia** (2020-05-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> So your “moving average” oracle would have no inputs …

The input to the formula updating the MA at block n are the last trades (`[]latestTrades`) that were executed at block m<n.

The MA is by definition a lagging indicator, and is even made to lag at least 1 block back so that only trades that have been realized already can affect it, not those in-flight during the current block.

Recall the MA is only relevant to the credit facility (CF)'s minting/liquidation/withdrawal functions. It doesn’t affect the AMM in anyway.

---

**dankrad** (2020-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/aliatiia/48/4784_2.png) aliatiia:

> Recall the MA is only relevant to the credit facility (CF)'s minting/liquidation/withdrawal functions. It doesn’t affect the AMM in anyway.

It doesn’t directly, but it does indirectly, because if I can get gas cheaper than at the Uniswap price, then I will use that method to get gas. So the Uniswap price will be within a close range of the credit facility.

Once again, there is no MA in your new construction – if all gas has to be paid using GAS tokens, then you do not get any kind of oracle that tells you how to value GAS/ETH. So what price will your credit facility use to determine the correct collateral ratio?

---

**aliatiia** (2020-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> if I can get gas cheaper than at the Uniswap price, then I will use that method to get gas

And someone else would get that cheap gas and sell it at the AMM, bringing its price down. This arbitrage is what makes Uniswap work essentially.

(note: remember that GAS’s `transfer()` is disabled so you can’t get GAS anywhere else anyway, except maybe OTC where the seller hands over the private key. In the future if the GAS/ETH market is extremely deep, `transfer()` can be enabled through a hard fork).

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> you do not get any kind of oracle that tells you how to value GAS/ETH

You do, the miners/validators are obligated by consensus rules to update the moving average (MA) every block.

The longer the MA’s period (hourly, daily, weekly etc) the farther away MA is from AMM’s spot price. As mentioned in the proposal, Daily may be the sweet spot between manipulation-resistance and price-sensitivity.

---

**dankrad** (2020-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/aliatiia/48/4784_2.png) aliatiia:

> You do, the miners/validators are obligated by consensus rules to update the moving average (MA) every block.
>
>
> The longer the MA’s period (hourly, daily, weekly etc) the farther away MA is from AMM’s spot price. As mentioned in the proposal, Daily may be the sweet spot between manipulation-resistance and price-sensitivity.

Once again, what value do they update the MA with if all gas is payed in GAS tokens? There would literally be no ETH value to use.

---

**aliatiia** (2020-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Once again, what value do they update the MA with if all gas is payed in GAS tokens?

If an asset is not bought/sold at time t, its MA at t+1 stays where it was at t-1, as it should. The MA at the credit facility doesn’t lose a signal when there was no signal to be lost.

The AMM is an open market bustling with different kinds of buyers and sellers, so it’s unlikely even 1 block passes without some GAS being bought and/or sold:

1. Alice deposits ETH  and mints GAS at the CF  \rightarrow selling it at the AMM DEX for ETH \rightarrow depositing new ETH in the CF \rightarrow  minting more GAS \rightarrow …repeat (leverage longing ETH)
2. Bob is stocking up on GAS, buys truck loads from AMM
3. Charlie mints a truck load of GAS, short sells it at AMM
4. MetaRelay Inc’s GAS_slow_accoumulator() lambda function on AWS submits a buy order, as it has been doing over the past couple of months (accumulating GAS slowly).
5. Dave deposits ETH  and mints GAS at the CF  \rightarrow sells it at AMM for ETH \rightarrow swaps ETH for stablecoins at Uniswap or Kyber  \rightarrow spends stablecoin on food and shelter expenses.
6. A few hundreds casual users buy GAS from AMM to cover the fee of this very tx in this in-flight block JIT style.

**The AMM is not resticted to case no. 6**

---

**dankrad** (2020-05-20):

OK, so my assumption previously was that the MA was computed from the actual gas payments on transaction, instead of from the AMM prices. I re-checked your original post and saw why I misinterpreted this.

So I want to clarify one more thing: My assumption is that one GAS token is always used to pay for one gas unit, i.e. there is no additional bidding on gas as there is in the current system?

If this is the case, I don’t see how you can prioritise between different transactions, as they now all pay exactly the same (1 GAS token/gas unit) instead of being able to bid different amounts of ETH/gas unit.

---

**aliatiia** (2020-05-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> there is no additional bidding on gas as there is in the current system?

No, but the ~same first-price auction mechanism can work for GAS as it does with ETH now (or any other mechanism such as that of EIP1559). For example, under the first-auction regime, if a transaction is paying with GAS, its `gasPrice` field is interpreted as a `tip` percentage on each GAS unit consumed. Example if `tip=10%` then the miner can take 1.1 GAS tokens per 1 gas worth of computation. And it may be necessary that, by consensus rules, `tip` cannot be negative (i.e. the minimum payment for 1 gas worth is 1 GAS token), to make sure there is a robust floor to the GAS/ETH market.

The miner can then calculate expected ETH revenue from such transactions buy multiplying `(1+(tip/100))xQ` where `Q` is the GAS/ETH price quote at the AMM (how much ETH per 1 GAS token). So `(1+(tip/100))xQ` is the equivalent of `gasPrice` for transactions paying with ETH.

---

I should mention, however, that there was indeed a bidding mechanism in this proposal originally but I decided to decouple that part into its own post (out soon) because:

**(a)** The scope of this proposal was becoming too large

**(b)** It’s a general mechanism not specific to a tokenized gas regime

---

**dankrad** (2020-05-21):

In this case, I just don’t see why the price of GAS should reflect the real gas price at all. Instead of the tip being 10%, it may as well be 500%. There is no mechanism in your proposal to ensure that the value of GAS reflects the cost of gas.

I think it just introduces a second free-floating cryptocurrency that is used to pay gas.

---

**aliatiia** (2020-05-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> I just don’t see why the price of GAS should reflect the real gas price at all

We discussed this already:

![](https://ethresear.ch/user_avatar/ethresear.ch/aliatiia/48/4784_2.png) aliatiia:

> this proposal is not a fee market proposal. Tokenizing gas is just a way to build an auto-pilot credit facility as a public financial utility; basically a MakerDao without governance or oracle.
>
>
> “Price” in this proposal is that of a bus ticket if it were market-based (i.e. not fixed by the bus authority). It’s not about how much to bribe the bus driver to let you take this next bus when there are more people than seats available:
>
>
> Efficient discovery of gas macro-price : GAS/ETH discovers ~the floor price of a gas unit, i.e. the material cost of 1 gas worth of computation. The aforementioned shorting/longing in (4) contributes to this efficiency. This may also eliminate potential deadweight  issues with current JIT gas production/consumption.

Discovering the “intrinsic” value of GAS (again, the bus ticket, not the driver’s bribe) is just a small benefit of ETH-collaterlized GAS … the big benefits imo are:

**(a)** access to credit without governance, custody, or oracle risk. Public financial utilities FTW.

**(b)** Predictable capital expenditure by high-throughput gas consumers to plan their gas budget: they can “lock-in” the price of their future gas expenditure.

---

So that’s the tokenization of the bus ticket. For bribing the driver of **this next bus** there are a few ways of doing it:

(1) Current first-auction mechanism

(2) [EIP1559](https://github.com/ethereum/EIPs/blob/2661ee520373cd2cc8b6e93c8d177ca41caecc3e/EIPS/eip-1559.md)

(3) [Escalator algorithm](https://github.com/danfinlay/EIPs/blob/ddb7a6afc477705ffdd8ba8b57774954a7955871/EIPS/eip-x.md)

(4) upcoming proposal which as I said before was left to its own post to keep the scopre here manageable. It does use some of the plumbing in this proposal but the two are independent and either can be implemented without the other necessarily.

---

**dankrad** (2020-05-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/aliatiia/48/4784_2.png) aliatiia:

> “Price” in this proposal is that of a bus ticket if it were market-based (i.e. not fixed by the bus authority). It’s not about how much to bribe the bus driver to let you take this next bus when there are more people than seats available:

I just don’t see how it even achieves this. In my opinion, you are just introducing an additional completely arbitrary unit. There is no reason why it should track anything like transaction costs.

I also dispute the notion that there is such a thing as a bus that’s not full here. This may happen at the moment, as Ethereum is still in a very early phase. Once it’s a well-used network, there will always be a transaction with very marginal value waiting. Why shouldn’t there be? Why should there be a finite number of valuable transactions? It’s much more likely that there’s a power law of infinitely many, less and less valuable transactions potentially waiting.


*(7 more replies not shown)*
