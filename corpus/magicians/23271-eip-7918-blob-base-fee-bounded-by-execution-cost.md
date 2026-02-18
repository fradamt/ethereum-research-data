---
source: magicians
topic_id: 23271
title: "EIP-7918: Blob base fee bounded by execution cost"
author: aelowsson
date: "2025-03-26"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7918-blob-base-fee-bounded-by-execution-cost/23271
views: 2315
likes: 20
posts_count: 43
---

# EIP-7918: Blob base fee bounded by execution cost

Discussion topic for [EIP-7918](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7918.md); [PR](https://github.com/ethereum/EIPs/pull/9543); [Web](https://eips.ethereum.org/EIPS/eip-7918).

Relevant background on the current auction design: [Data Always](https://ethresear.ch/t/understanding-minimum-blob-base-fees/20489), [Wahrstätter](https://ethresear.ch/t/on-blob-markets-base-fee-adjustments-and-optimizations/21024), [Crapis](https://ethresear.ch/t/eip-4844-fee-market-analysis/15078), [Heimbach and Milionis](https://arxiv.org/abs/2502.12966).

---

- 2025-04-25: Children’s book
- 2025-05-20: Analysis of KZG proof verification cost
- 2025-05-20: Analysis of the return statement
- 2025-05-24: ACDE SFI decision
- 2025-05-26: ACDT decision, included in devnet-1
- 2025-06-19: Post on the setting for BLOB_BASE_COST
- 2025-06-19: ACDE BLOB_BASE_COST decision
- 2025-08-14: PR – current block’s blobSchedule applied
- 2025-08-15: Final revision to improve EIP clarity
- 2025-12-03: Explainer: EIP-7918 in Fusaka: 3 reasons and 1 trick

## Replies

**sbacha** (2025-03-28):

~~please dont post AI slop on here we are better than that~~

Edit: The OP comment has been edited to not be slop, I thank you. The EIP is certainly not slop.

---

**dataalways** (2025-03-28):

Thank you for the proposal. I like the idea and definitely think we should explore the solution space. I have a few question:

- This seems to be moving towards recoupling the two fee markets, is that something that we want? Like the two are already often entangled because demand drivers on one layer tend to drive demand on the others as well (i.e., price volatility driving more defi usage), but do we want to explicitly increase the entanglement?
- If we’re tying the two markets together, why did you choose this value? Does it make sense to tie the price to additional liveness risk of including blobs instead?
- The main blocker for EIP-7762 was a desire not to tinker with the blob fee market and not to add more complexity to Pectra. This seems more complicated than 7762 and the benefits over 7762 aren’t that clear to me. If in the long-term we want to have blob capacity > demand to keep price stability but then charge L2s a small amount, then wouldn’t it be better to have a fixed base fee that is easier to justify tuning?
- I’m curious to the historical empirical impact of this proposal. How often would it have been a major contributor v.s. being overshadowed by blob fees?

---

**aelowsson** (2025-04-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dataalways/48/16990_2.png) dataalways:

> Thank you for the proposal. I like the idea and definitely think we should explore the solution space. I have a few question:

Thanks for your question and your analytical work on blob base fees, which has been very valuable.

### Question 1: Coupling of fee markets

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dataalways/48/16990_2.png) dataalways:

> This seems to be moving towards recoupling the two fee markets, is that something that we want? Like the two are already often entangled because demand drivers on one layer tend to drive demand on the others as well (i.e., price volatility driving more defi usage), but do we want to explicitly increase the entanglement?

The price of blobspace depends on the price of execution gas, and this should be reflected in the fee market. Currently, the mechanism behaves as follows:

- Users purchase blobspace by spending execution gas and blob gas.
- The blob gas fee update mechanism is unaware of the cost of execution gas, and thus unaware of the cost of blobspace.
- A relatively high cost of execution gas renders changes to the blob gas fee subordinate in determining quantity demanded.
- The mechanism fails to timely converge on equilibrium whenever the cost of execution gas dominates the cost of blob gas.

In essence, the mechanism behaves as if it controlled the price of blobspace when it only controls the price of blob gas. EIP-7918 resolves this by adjusting the auction mechanism when the cost of execution gas dominates. The two fee markets still remain fully independent in the operational range where the blob base fee carries the price signal.

### Question 2: Alternative designs

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dataalways/48/16990_2.png) dataalways:

> If we’re tying the two markets together, why did you choose this value? Does it make sense to tie the price to additional liveness risk of including blobs instead?

I am not sure what exact value you are referring to? A nice thing about this proposal is its minimalist nature. Fee parity and amortization across target blobs was the most neutral condition I could think of. The only other option I considered was amortization across max blobs instead of target blobs. I think both options are perfectly valid but favored target blobs for two reasons:

- It represents the equilibrium condition and can thus be perceived as slightly more neutral.
- It results in a slightly higher fee parity threshold, both in terms of its nominal level (see Figure 1 below) and the relative level that more execution-gas-intensive blob consumers operate on. Concerning the relative level, we can focus on the bump centered at around 126k in your informative analysis of execution gas used by block submitters. A gas-intensive L2 submitting a single blob would uses (6/1) × (21k/126k) = 36 times more execution gas than blob gas under Pectra settings before the bound on blob gas activates. With amortization across max blobs, the outcome is (9/1) × (21k/126k) = 54.

Concerning tying the price to liveness risk, I suppose it can make sense, but it is not something I have explored.

I have considered one other option, which I call a composite fee market. This would however be a much bigger change, also conceptually. It is not something we should be pursuing right now and would have to be part of a potential future harmonization of fee markets. The design can however be informative also for understanding EIP-7918, and it is therefore described briefly below.

### Composite fee market

The composite fee market updates the blob base fee based on the *real* demand function for blobspace, as previously specified in EIP-7918:

        *Q*(*b* + *c*).

In this equation, the long-run average per-block quantity of blobs demanded *Q* depends on the blob base fee *b* and the tx cost *c*, expressed per blob gas as specified in the EIP. The real demand function will reflect variations in blob submission strategies, but the same estimate for *c* as in EIP-7918 could potentially be used. Other options are to simply compute *c* for every block or to specify *c* as the long-run average.

Let *q* represent the desired fractional shift in the cost of blobspace, e.g., in the range [-0.125, 0.125], computed from the realized *Q* of the block and the target quantity for a block. Further, let *c*₀ define the tx cost of the previous slot, computed according to one of the options of the previous paragraph and expressed per blob gas. The composite fee auction then updates from *b*₀ to *b*₁ by accounting for *c*₀:

        *b*₁ = *b*₀ + *q*(*b*₀ + *c*₀)

To the user that employs the same execution gas per blob gas as in *c*₀, the maximal change in cost of blobspace per slot would still be 12.5%. The proportional change in *b* can however be dramatic whenever *b* << *c*. This is as intended, allowing the composite fee auction to quickly converge on equilibrium, no longer “getting stuck” at lower blob base fees.

As a general comment: to devise a sound fee market, it is important to model the real demand function.

### Question 3: Comparison with EIP-7762

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dataalways/48/16990_2.png) dataalways:

> The main blocker for EIP-7762 was a desire not to tinker with the blob fee market and not to add more complexity to Pectra. This seems more complicated than 7762 and the benefits over 7762 aren’t that clear to me. If in the long-term we want to have blob capacity > demand to keep price stability but then charge L2s a small amount, then wouldn’t it be better to have a fixed base fee that is easier to justify tuning?

The fee mechanism is currently unaware of the full price of the goods that it attempts to regulate the price for. It therefore fails to converge on equilibrium in a timely manner. To resolve this, the fee update should be made aware of the price of execution gas. The main blocker against EIP-7762 is arguably that it does not relay this price signal but instead specifies a hard-coded price floor. Such a fixed floor could perhaps be characterized as “tinkering”, and this was potentially why the EIP had difficulties gathering consensus. If the price of execution gas becomes much lower, say between `2**5` to `2**6` wei, it is hard to imagine that the price floor for blob gas of `2**25` wei specified in EIP-7762 would be considered appropriate. A price floor that adapts with the price of execution gas is more neutral. It can then adapt with the actual cost of blobspace to ensure a functioning fee market, while letting the price of blob gas evolve without restrictions within these technical limits. Framed within the current “price discovery” discourse, EIP-7918 identifies the inelasticity horizon as an impediment to effective “price discovery”, and keeps the price of blob gas sufficiently high to always influence blobspace equilibrium formation.

EIP-7762 indeed takes the cost of execution gas as its starting point:

> To set the parameter apropriately, one aproach is to look at the cost of simple transfers when base fees are low. The cost of a simple transfer when the base fee is 1 GWEI is ~5 cents USD at today’s prices (2,445.77$ ETH/USDC). We can try to peg the minimum price of a blob to that.

One difference is that EIP-7918 allows this type of comparison to take place automatically every block, such that the protocol no longer needs to rely on developers to adjust the floor, should the cost of execution gas change going forward. You mention that the fixed floor of EIP-7762 makes it easier to justify tuning the floor to keep price stability, but I would argue that this is rather a drawback. A self-adjusting dynamic floor is the ideal to strive towards. I would further argue that the change is specifically to ensure a functioning fee market, as opposed to the protocol charging L2s some specific amount for blob gas. EIP-7918 will indeed increase protocol income, just like EIP-7762, but this is mainly a necessity to allow the protocol to operate under more stable resource consumption, without having longer periods of successive blocks consuming above-target blob gas.

A second difference is that EIP-7918 accounts for the potential to amortize the cost of execution gas across blobs when setting the floor. It is reasonable to account for improved future gas efficiency derived via scaling. As stipulated in the EIP:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aelowsson/48/14632_2.png) aelowsson:

> To understand why potential future blob scaling is important to account for when designing the mechanism, consider how the price of storing a fixed amount of data has fallen over the last 80 years.

The discussion regarding the fixed floor in EIP-7762 has focused on whether it is sufficiently low to account for potential future ETH price appreciation. The computer scientist in me would like to remark that this is a bit like trying to predict the appropriate cost of 128 kB of storage 50 years into the future based on the ability of the dollar to retain its value. It can be assumed that the cost of a fixed amount of data availability will fall drastically over the next half-century, both due to improvements in hardware and software, while Ethereum’s income from data availability still rises. Thus, we cannot ascertain the appropriate minimum price for one 128 kB blob based on ETH price considerations, but should instead codify the economic relationship between blob gas and execution gas, allowing the minimum price to adapt with future scaling. To be fair, the change in blob count might take place during a hard fork, and developers could then readjust the EIP-7762 threshold. But as argued, this is undesirable “tinkering”, and changes in blob count migh also happen automatically in the future.

Figure 1 shows how the blob base fee floor adapts with the execution base fee in EIP-7918, while remaining fixed in EIP-7762. The price floor in EIP-7918 varies along the fee parity line, as indicated by arrows. When the target is 6 blobs, the floor has a higher baseline (black arrows) than when the target is 12 blobs (grey arrows), reflecting different opportunities to amortize execution costs across consumed blobs.

[![Figure 1](https://ethereum-magicians.org/uploads/default/optimized/2X/3/3f13b7f6ecaf60fab0a315a77aa06ac4043f20f3_2_690x471.png)Figure 12658×1816 463 KB](https://ethereum-magicians.org/uploads/default/3f13b7f6ecaf60fab0a315a77aa06ac4043f20f3)

**Figure 1.** Comparison between EIP-7762 and EIP-7918. EIP-7762 stipulates a fixed threshold at `2**25`wei. EIP-7918 stipulates a fee-parity threshold that varies with the execution base fee (the cost of the blob-carrying transaction) and the blob target (the opportunity to amortize the blob-carrying transaction).

Concerning implementation complexity:

- EIP-7762 changes one constant and adds block_timestamp as an input variable to calc_excess_blob_gas(). This input is included in an if statement evaluating timestamps, returning 0 if TRUE.
- EIP-7918 adds one if statement to calc_excess_blob_gas() evaluating computed gas prices, altering the return to be parent.excess_blob_gas + parent.blob_gas_used // 3 if TRUE.

Whether one change brings more complexity than the other is hard for me to tell. They should both be fairly similar and both be straightforward.

### Question 4: Request for empirical analysis

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dataalways/48/16990_2.png) dataalways:

> I’m curious to the historical empirical impact of this proposal. How often would it have been a major contributor v.s. being overshadowed by blob fees?

Figures 2-3 show price evolution over three weeks in November 2024, when the average execution base fee was around 16 gwei, as well as in March 2025, when the average was around 1.3 gwei. Thresholding of EIP-7762 (blue) and EIP-7918 (green) is applied directly to the original data, without accounting for its potential effect on the equilibrium fee. The equilibrium blob base fee would in reality rise from the threshold level once demand at this fee is above target supply. A target of 6 blobs was used as the amortization factor to make the comparison applicable to Pectra settings. As evident and in line with the previous Figure 1, the floor in EIP-7918 becomes higher than the floor in EIP-7762 when execution gas is more expensive, and lower when execution gas is cheaper.

[![Figure 2](https://ethereum-magicians.org/uploads/default/optimized/2X/a/adce0cd7c7d89d4437ca1473f50f5a930183a282_2_689x441.png)Figure 22581×1650 326 KB](https://ethereum-magicians.org/uploads/default/adce0cd7c7d89d4437ca1473f50f5a930183a282)

**Figure 2.** Blob base fee evolution with the current fee market (black), with EIP-7762 (blue), and with EIP-7918 (green), during three weeks of November 2024 when the average execution base fee was around 16 gwei. Thresholding is applied directly to the original data, without accounting for its effect on the equilibrium fee.

[![Figure 3](https://ethereum-magicians.org/uploads/default/optimized/2X/9/98706296bd55c61e93964b1cd59ba8e8eca2e98a_2_689x440.png)Figure 32581×1648 333 KB](https://ethereum-magicians.org/uploads/default/98706296bd55c61e93964b1cd59ba8e8eca2e98a)

**Figure 3.** Blob base fee evolution with the current fee market (black), with EIP-7762 (blue), and with EIP-7918 (green), during three weeks of March 2025 when the average execution base fee was around 1.3 gwei. Thresholding is applied directly to the original data, without accounting for its effect on the equilibrium fee.

Figure 4 shows histograms for the four-month period from the start of Figure 2 to the end of Figure 3, corresponding to approximately 900k blocks beginning at block number 22075724. The histograms employ 100 log-spaced bins per decade (factor-of-ten increase), which are smoothed using a Hanning window of width 41 with mirror-reflected edges. The threshold set by EIP-7918 (green) can operate both below or above the threshold set by EIP-7762 (blue), depending on the cost of execution gas.

[![Figure 4](https://ethereum-magicians.org/uploads/default/optimized/2X/8/8645495529fb8383af494957e9971b6f26eed166_2_596x500.png)Figure 42644×2217 206 KB](https://ethereum-magicians.org/uploads/default/8645495529fb8383af494957e9971b6f26eed166)

**Figure 4.** Histogram of the blob base fee when applying EIP-7762 (blue) or EIP-7918 (green), with light smoothing applied. A four-month period from November 2024 through March 2025 was analyzed. Thresholding is applied directly to the original data, without accounting for its effect on the equilibrium fee.

---

**potuz** (2025-04-10):

I’ll leave the same comment as in ACD, rather than using `TX_BASE_COST`  use a function of it, that can be set to be equal to `TX_BASE_COST` at the first implementation, but allows for a simple change in case this limit proves inadequate.

---

**aelowsson** (2025-04-11):

Thanks for your suggestion! I saw the comment quite late and did not have time to respond. I can see the benefit of allowing for a simple change. This is the current if-clause

```python
if TX_BASE_COST * parent.base_fee_per_gas > TARGET_BLOB_GAS_PER_BLOCK * get_base_fee_per_blob_gas(parent):

```

The left-hand side accounts for the minimum tx cost and the right-hand side represents the blob cost when including target blobs in the tx. An intuitive point for flexibility would also be the blob gas parity condition on the right side of the if-clause, currently set to `TARGET_BLOB_GAS_PER_BLOCK`.

There are several ways to do this. We could appy the same idea as in your suggestion on the right-hand side, assign target blob gas (or any other choice) to `BLOB_GAS_PARITY` (can also be a function), and execute:

```python
if TX_BASE_COST * parent.base_fee_per_gas > BLOB_GAS_PARITY * get_base_fee_per_blob_gas(parent):

```

Another option is to instead rely on a `PARITY_FACTOR` that scales the fee parity condition. An example under a cap `MAX_BLOB_GAS_PER_TX` on the blob gas (it seemed to have fairly strong support during the last ACDE) is:

```python
if TX_BASE_COST * parent.base_fee_per_gas > MAX_BLOB_GAS_PER_TX * PARITY_FACTOR * get_base_fee_per_blob_gas(parent):

```

At `PARITY_FACTOR = 1`, the blobs can at most represent 50% of the total cost—applicable when using a simple tx and maximum (capped) blobs. In all other cases the blobs will represent less than 50% at the threshold. Setting `PARITY_FACTOR = 4` instead shifts that limit down to 20%. If the cap scales with max blobs, EIP-7918 would still ensure that whatever proportion that is specified through `PARITY_FACTOR` remains intact.

Do any of these solutions make sense to you?

---

**benaadams** (2025-04-12):

Could we add a lower floor cap in addition; so combine EIP-7918 and EIP-7762; but with a lower level for the EIP-7762 part; say at 0.1gwei

`TX_BASE_COST = Max(TX_BASE_COST, 0.1Gwei)`

They are 128kB txs after all; so there is a higher cost to them on the network vs a regular 21k gas tx at 100 bytes.

0.1Gwei absolute floor would be 762wei per byte, or 0.8gwei per MB (or about 1c per blob); so isn’t an onerous floor

---

**benaadams** (2025-04-13):

Or maybe https://x.com/VitalikButerin/status/1911223517728698690

`TX_BASE_COST = Max(TX_BASE_COST, 1Gwei)`

---

**pintail** (2025-04-14):

Wouldn’t the most neutral approach be to change the blob base fee update rule to intrinsically account for the cost of execution? So in times when execution cost dominates the blob base fee would quickly fall to zero (since it can’t be negative) but when demand picks up the blob base fee would initially rise much faster because the update rule targets the total fee including execution cost.

This would be slightly more complex than the rule proposed above but I think it would be more neutral and would more precisely reflect the actual market for blobspace.

---

**pintail** (2025-04-14):

Tried to edit original post but can’t seem to do this on Android. Anyway to illustrate I’m suggesting that we change the update rule something like:

`next_blob_premium = (current_execution_cost + current_blob_premium) * (blob_count - blob_target) * update_factor - next_execution_cost`

---

**benaadams** (2025-04-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pintail/48/11152_2.png) pintail:

> ... update_factor - next_execution_cost

That’s doing the opposite of what is suggested?

A blob transaction is much larger than a regular Eth transfer tx; which is what it generally pays on EL gas side.

Both from the blobs themselves at 128kb each vs 100 bytes for an Eth transfer and the KcgCommitments which it’s getting for free as they aren’t even priced as calldata.

So the proposal is suggesting the price of a blob shouldn’t fall below the EL tx cost.

You are proposing to discount further.

---

**pintail** (2025-04-14):

The problem isn’t that the blob fee goes too low, the problem is that it takes too long to ramp up when demand increases. The formula I propose (admittedly in rough pseudo code) would ensure that the blob fee much more quickly rises to match demand once execution no longer dominates the costs.

---

**benaadams** (2025-04-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pintail/48/11152_2.png) pintail:

> The problem isn’t that the blob fee goes too low,

Is a blob more work to the protocol than a simple Eth transfer?

The answer is definitely yes; regardless of data the EL is also validating their proofs, so they should not be dropping below this price as an example

---

**pintail** (2025-04-14):

I would argue that the basic “cost” to the network is captured by the EL fee, but it would be interesting to consider what other ways there might be to model the cost.

I’m just saying that Anders’ proposal was based on the observation that in periods of low blob demand, the cost to post blob data is dominated by the EL fee, but this is not captured in the blob fee update formula, which is why it takes so long for the blob base fee to catch up when demand increases.

He has proposed one option which is to say that the blob fee should never go below the EL fee and argues that’s the most neutral proposal. I’m saying that the ultimate neutral proposal would be to include both EL and blob fees in the update rule, and I think that although it’s more complex, it would better reflect the market and respond better to the transition from EL-dominated to blobfee-dominated regimes.

---

**aelowsson** (2025-04-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pintail/48/11152_2.png) pintail:

> Wouldn’t the most neutral approach be to change the blob base fee update rule to intrinsically account for the cost of execution? So in times when execution cost dominates the blob base fee would quickly fall to zero (since it can’t be negative) but when demand picks up the blob base fee would initially rise much faster because the update rule targets the total fee including execution cost.

This is the composite fee market, as I already proposed above:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aelowsson/48/14632_2.png) aelowsson:

> ### Composite fee market
>
>
>
> The composite fee market updates the blob base fee based on the real demand function for blobspace, as previously specified in EIP-7918:
>
>
> Q(b + c).
>
>
> In this equation, the long-run average per-block quantity of blobs demanded Q depends on the blob base fee b and the tx cost c, expressed per blob gas as specified in the EIP. The real demand function will reflect variations in blob submission strategies, but the same estimate for c as in EIP-7918 could potentially be used. Other options are to simply compute c for every block or to specify c as the long-run average.
>
>
> Let q represent the desired fractional shift in the cost of blobspace, e.g., in the range [-0.125, 0.125], computed from the realized Q of the block and the target quantity for a block. Further, let c₀ define the tx cost of the previous slot, computed according to one of the options of the previous paragraph and expressed per blob gas. The composite fee auction then updates from b₀ to b₁ by accounting for c₀:
>
>
> b₁ = b₀ + q(b₀ + c₀)
>
>
> To the user that employs the same execution gas per blob gas as in c₀, the maximal change in cost of blobspace per slot would still be 12.5%. The proportional change in b can however be dramatic whenever b  int:
    if parent.excess_blob_gas + parent.blob_gas_used  TARGET_BLOB_GAS_PER_BLOCK:
        q_Up = fake_exponential(Up, parent.blob_gas_used - TARGET_BLOB_GAS_PER_BLOCK, BLOB_BASE_FEE_UPDATE_FRACTION) - Up
        return fake_log(MIN_BASE_FEE_PER_BLOB_GAS, b0 + q_Up * (b0+c0) // Up, BLOB_BASE_FEE_UPDATE_FRACTION)
    else:
        q_Up = fake_exponential(Up, TARGET_BLOB_GAS_PER_BLOCK - parent.blob_gas_used, BLOB_BASE_FEE_UPDATE_FRACTION) - Up
        return fake_log(MIN_BASE_FEE_PER_BLOB_GAS, b0 - Up * (b0+c0) // q_Up, BLOB_BASE_FEE_UPDATE_FRACTION)
```

Note the new function `fake_log()`. As mentioned in the description for this proposal, the change is conceptual in nature, and not something I intended for Fusaka, but rather suggested as a potential part of a wider harmonization of fee markets. If there is support for a composite fee market, we can of course push for it, but my intuition is that the proposed simple solution following the same principle was more suitable at this stage, also due to its ability to establish a neutral price floor for blobs. Such a price floor has been suggested as a goal in itself among some members of the community. EIP-7918 is designed to be “the best of both worlds” in this respect, establishing a neutral price floor that ensures a functioning fee market, adhering to economic efficiency.

---

**benaadams** (2025-04-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pintail/48/11152_2.png) pintail:

> I would argue that the basic “cost” to the network is captured by the EL fee

It is demonstratablely not because the EL fee for 3 blobs is the minimum tx fee of 21k gas

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/5/51287ff940a1bd30eabdbd833c8db22145658a24_2_689x215.png)image1290×403 46.6 KB](https://ethereum-magicians.org/uploads/default/51287ff940a1bd30eabdbd833c8db22145658a24)

---

**pintail** (2025-04-14):

Ah ok, I think I had not understood the composite alternative proposal. Still seems to me like a much better function and in enforcing that the min blob fee should be equal to the EL fee seems a bit arbitrary. But still an improvement on a hard floor.

---

**pintail** (2025-04-14):

How would you model the cost?

---

**benaadams** (2025-04-14):

I’d probably go for that the cost of a blob shouldn’t fall below the `Point Evaluation Precompile` cost at `50000 gas * EL base fee`, we already have a price for it; or you are getting the EL work cheaper than a smart contract does.

The blob submitter is still getting a good deal as they only have to pay the priority fee on the 21k gas for basic tx cost (and deeply discounted data vs calldata on both commitments/proofs and the blobs themselves)

---

**pintail** (2025-04-14):

Seems reasonable - and could be achieved by repricing blob transactions on the EL.

---

**benaadams** (2025-04-15):

Specifically; rather than using `TX_BASE_COST` use `POINT_EVALUATION_PRECOMPILE_GAS` and also enforce floor first so an individual blob cost shouldn’t stay under the cost of EL verification

So changing to

```auto
def calc_excess_blob_gas(parent: Header) -> int:
    base_blob_fee = get_base_fee_per_blob_gas(parent) * GAS_PER_BLOB
    base_verification_fee = parent.base_fee_per_gas * POINT_EVALUATION_PRECOMPILE_GAS

    if base_verification_fee > base_blob_fee:
        # Fee too low relative to execution cost
        # increase, but not by more than a max fill would (e.g. div 3 for 6/9)
        return parent.excess_blob_gas + parent.blob_gas_used // 3

    if parent.excess_blob_gas + parent.blob_gas_used < TARGET_BLOB_GAS_PER_BLOCK:
        # Below target usage; blob fee sufficiently high; reset excess
        return 0
    else:
        # Above target usage; normal EIP-4844 excess gas logic
        return parent.excess_blob_gas + parent.blob_gas_used - TARGET_BLOB_GAS_PER_BLOCK
```


*(22 more replies not shown)*
