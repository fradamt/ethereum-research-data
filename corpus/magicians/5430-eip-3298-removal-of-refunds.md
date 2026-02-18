---
source: magicians
topic_id: 5430
title: "EIP 3298: Removal of refunds"
author: vbuterin
date: "2021-02-26"
category: EIPs
tags: [opcodes, gas]
url: https://ethereum-magicians.org/t/eip-3298-removal-of-refunds/5430
views: 9853
likes: 21
posts_count: 30
---

# EIP 3298: Removal of refunds

## Simple Summary

Remove gas refunds for SSTORE and SELFDESTRUCT.

## Link



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/3298)














####


      `master` ← `vbuterin-patch-1`




          opened 01:59PM - 26 Feb 21 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/1X/882285f3628ea3784835c306639dd8f62179a6d9.png)
            vbuterin](https://github.com/vbuterin)



          [+95
            -0](https://github.com/ethereum/EIPs/pull/3298/files)







Remove gas refunds for SSTORE and SELFDESTRUCT.

## Replies

**bgits** (2021-02-26):

Rather than remove gas refunds it might be worth trying to educate developers on the usage first. Gas refunds seem like a viable solution to reduce user costs until L2 solutions are more established.

For example there are DeFi protocols that issue contracts (both in the legal and onchain sense) whose operating period has an expiration date. Such protocols also issue new contracts periodically as old ones expire, having a strategy to `SELFDESTRUCT` expired contracts upon creating new ones will not only prevent state bloat but reduce gas costs for the users that make these calls.

---

**wjmelements** (2021-02-26):

Relevant prior discussions: [EIP-2751](https://ethereum-magicians.org/t/eip-for-disabling-selfdestruct-opcode/4382)

As a holder of millions of dollars worth of refunds, tokenized and otherwise, I would be strongly interested in a [compensation plan](https://github.com/ethereum/EIPs/pull/2751#issuecomment-649855638). I can prepare an EIP for this. The search for parties to compensate can coincide with cleanup, which would reduce the amount of state formerly dedicated to this purpose. Hence I suggest postponing this change until the ETH2 merge.

My current refund compensation plan would use a 50,000-block average of the gastoken’s Uniswap-V2 WETH token ratios pre-fork to determine their compensation eth value, then replace their contract with another holding that much ETH. The new contracts would replace the `free`, `freeUpTo`, `freeFrom`, and `feeFromUpTo` methods to “burn” those tokens and send ETH to sender according to the ratio of burned supply to the remaining. The `mint` function would become a no-op. Then, all of the gastoken state could be removed with the hard fork. The supply-weighted average of GST2 and CHI’s resulting price can be used to value SSTORE refunds as well, such as GST1 and Cancel contracts.

An alternative way to disable refunds gently would be to phase them out, with the refund decreasing by 1 every 1,000 blocks after activation. This approach would not require compensation, and they would clean themselves up automatically over time.

Without compensation, I would be incentivized to floor the gas price to increase the likelihood that my refunds get purchased or used before they are deactivated, and/or seek legal action off-chain. But I suspect cleanup and compensation would be agreeable to all parties.

> particularly in exacerbating state size

Quantitatively the space consumed is very minimal, several MB. There are [ways](https://github.com/ethereum/EIPs/issues/911) to reduce this to about 1 MB that have been proposed in the past; they take advantage of the fact that gastoken contracts are all identical. I mentioned this optimization in the Motivation section of [EIP-2185](https://github.com/ethereum/EIPs/pull/2185/files).

> inefficiently clogging blockchain gas usage

They only “clog” blockchain gas usage during times of lesser congestion. During that time they are outbidding other activity that would also create space; but unlike that activity, the space is eventually cleaned up. Unlike a hypothetically-functional EIP-1559 variant, state growth is normalized and counter-balanced from the resulting block elasticity.

> inefficiently

It can be made more efficient by increasing the refund ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=12)

> Refunds increase block size variance. The theoretical maximum amount of actual gas consumed in a block is nearly twice the on-paper gas limit (as refunds add gas space for subsequent transactions in a block, though refunds are capped at 50% of a transaction’s gas used). This is not fatal, but is still undesirable, especially given that refunds can be used to maintain 2x usage spikes for far longer than EIP 1559 can.

It is not a problem that ethereum can use double it’s current target because it’s currently **far** below its capacity, which is good for sync times and state growth. But Binance Smart Chain is demonstrating that modern hardware can still sync the blockchain when the gasLimit/minute is >16x higher. It seems 4x is a recent concern due to EIP-1559, but since we are so very far below capacity I would pitch it as a strong advantage: block elasticity means lower highs during peak gas congestion from the additional capacity. Gastokens are also massively under-utilized, despite efforts to [democratize their usage](https://1inch-exchange.medium.com/1inch-introduces-chi-gastoken-d0bd5bb0f92b). Next, the duration that gastokens can be used to 2x capacity is limited by the current supply; gastokens are relatively scarce. Shortly, 4x is a non-issue because gas targets are coordinated around sync time and state-growth, not processing time. This is also why the miner-coordinated increase from 10m to 12.5m coincided with an unpredicted decrease in uncle rate.

I’m skeptical that EIP1559 will improve block elasticity, but that is another discussion. For the case that it doesn’t, this should be delayed until after London. The gas price estimation user experience would be much worse with more volatility.

---

**wjmelements** (2021-02-26):

It has been suggested to keep metered refunds, where we refund SSTORE gas when you clear storage you set in the same transaction. I want to extend that suggestion: I suggest keeping a metered refund for `SELFDESTRUCT` so that if the contract is recreated in the same transaction, or destroyed in the same transaction it is created, the `CREATE` cost is offset. I suspect these would be the most-common use of `SELFDESTRUCT` post EIP-3298.

---

**jochem-brouwer** (2021-02-26):

I have two points here:

(1) If we do this EIP then `eth_estimateGas` will return the right gas values, since originally it returned the used gas minus the refunds, but now since the refunds are zero, it returns the actual gas limit value. So this is a good improvement. (Unless I am missing another point where EVM refunds gas, which is not removed in this EIP).

(2) Currently, it is theoretically possible to run a block which executes (almost) twice the gas limit of the block. To do this, each transaction in the block has to have the maximum refund in gas (which is 50%), so we can execute twice as much gas in the block. If we remove the refunds, then this will definitely impact the amount of transactions which fit in a block, since any transaction which originally claimed a refund, will now use up more gas space of the block. This thus halves the amount of gas we can execute in the worst case of a block.

---

**wjmelements** (2021-02-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> (1) If we do this EIP then eth_estimateGas will return the right gas values, since originally it returned the used gas minus the refunds, but now since the refunds are zero, it returns the actual gas limit value. So this is a good improvement. (Unless I am missing another point where EVM refunds gas, which is not removed in this EIP).

You are mistaken. `eth_estimateGas` already returns the correct gas limit.

---

**wjmelements** (2021-02-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> (2) Currently, it is theoretically possible to run a block which executes (almost) twice the gas limit of the block. To do this, each transaction in the block has to have the maximum refund in gas (which is 50%), so we can execute twice as much gas in the block. If we remove the refunds, then this will definitely impact the amount of transactions which fit in a block, since any transaction which originally claimed a refund, will now use up more gas space of the block. This thus halves the amount of gas we can execute in the worst case of a block.

This is fine; miners can adjust the gas target. Historically tho, they haven’t.

---

**jochem-brouwer** (2021-02-26):

> You are mistaken. eth_estimateGas already returns the correct gas limit.

Since when was this changed? Is there an EIP for this one or did clients just upgrade their estimate gas logic?

> This is fine; miners can adjust the gas target. Historically tho, they haven’t.

Hmm yeah you are right.

---

**wjmelements** (2021-02-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> Since when was this changed? Is there an EIP for this one or did clients just upgrade their estimate gas logic?

For go-ethereum it’s been a gasLimit binary search since at least 2017. Perhaps it behaved differently on other clients tho.

---

**thabaptiser** (2021-02-27):

As of right now, refunds incentivize both the use of gastokens and the clearing of state when possible. The storage savings from breaking gastokens would be miniscule compared to the cost of de-incentivizing the clearing of state.

When a user transfers their entire balance  of an ERC-20, they transfer `balanceOf(...)`, that storage slot gets cleared, and they get a refund. However, if there were no refund, they would be incentivized to not clear the storage slot, and only transfer `balanceOf(...) - 1`, to save gas in case they ever wanted to re-acquire some of this ERC-20. The same logic can be applied to approvals, deposits/withdrawals into DeFi protocols, deployed contracts, and so on.

Given how high gas prices are, and the competition to be “gas efficient” between DeFi projects, most projects would rush to implement patterns that keep storage slots open to save gas. The size of this state growth would likely be significantly larger than the impact gastokens have. In the worst case of no refunds, every storage slot a user touches would be permanently occupied, as clearing it would be inefficient with regards to gas.

Additionally, gastokens are fairly sustainable. They are created with the purpose of deletion. Looking at [CHI](https://etherscan.io/token/0x0000000000004946c0e9f43f4dee607b0ef1fa1c), the total supply today (1.6mm) is less thant it was on October 8th, 2020 (1.9mm). It peaked around December, at 3mm. The market cap of gastokens will be limited by gas volatility and the number of transactions per block. There is no reason to have excessive amounts of gastoken on-chain, as there is no profit to be had in minting gastokens that probably won’t be used.

---

**wjmelements** (2021-02-27):

I wrote up the phase out alternative, now [EIP-3300](https://ethereum-magicians.org/t/eip-3300-phase-out-refunds/5434)

---

**vbuterin** (2021-03-01):

> Additionally, gastokens are fairly sustainable. They are created with the purpose of deletion. Looking at CHI , the total supply today (1.6mm) is less thant it was on October 8th, 2020 (1.9mm). It peaked around December, at 3mm.

One other problem that I see with gastokens is that they are inherently inefficient. You need 20000 gas to make a gastoken but you only get 10000 gas from using it (the ratio for GST2 [is similar](https://gastoken.io/#comparison)), and so there’s an extra 10000 gas that gets spent that provides no actual value to the network. Because the gas limit is bounded primarily by worst-case DoS attack limits, and not by average usage, we suffer the penalty of this wasted gas being part of the gas limit that everyone can use without getting any benefits out of it.

> When a user transfers their entire balance of an ERC-20, they transfer balanceOf(...), that storage slot gets cleared, and they get a refund. However, if there were no refund, they would be incentivized to not clear the storage slot, and only transfer balanceOf(...) - 1, to save gas in case they ever wanted to re-acquire some of this ERC-20. The same logic can be applied to approvals, deposits/withdrawals into DeFi protocols, deployed contracts, and so on.

If we want to mitigate this, one idea is to just reduce the SSTORE gas cost in the nonzero → zero case down to some very minimal value (eg. 100); note that the cold-storage-load cost introduced in EIP 2929 would still be applied on top of this. This would increase the worst-case write count to be about the same as the worst-case read count, but it would fix some of the mispricing issues.

---

**wjmelements** (2021-03-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> If we want to mitigate this, one idea is to just reduce the SSTORE gas cost in the nonzero → zero case down to some very minimal value

This is insufficient because the difference is dwarfed by `SSTORE_SET_GAS`. Once you’ve paid for that you should never give it up.

---

**vbuterin** (2021-03-02):

Here is a more comprehensive proposal. This *does* cut back some of the “simplicity” benefits of removing refunds, but OTOH it does allow us to retain most of the benefits of refunds while achieving the goals of (i) breaking gastoken, and (ii) removing block size variance.

---

Replace the “refund” counter with two counters: (i) a `new_storage_slots_filled` counter that increments every time a storage slot goes from zero to nonzero, and (ii) a `storage_slots_cleared` counter that increments every time a storage slot goes from nonzero to zero. At the end of a transaction, refund `15000 * max(storage_slots_cleared - new_storage_slots_filled, 0)` gas. So every 15000 gas refunded must be matched by 15000 gas storage-increase gas paid, and so the maximum amount of gas *spent on execution* would not be able to exceed the gas limit.

---

**wjmelements** (2021-03-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> (i) breaking gastoken

I should hope that’s not the explicit goal, but you don’t achieve it here; GST1 would still work.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> (ii) removing block size variance

You would still have block size variance because you have refunds.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> 15000 * max(storage_slots_cleared - new_storage_slots_filled, 0)

Based on the text I think you got the subtraction backward but it’s problematic either way.

---

Meaningful refunds seem necessary to incentivize good smart contract architectures where approvals and balances are zeroed when possible. These refunds currently introduce up to 2x block elasticity, which is good. From the Motivation it sounds like there is concern that 4x could be a DoS vector, but since Ethereum is so far under capacity, so-long as the opcodes are correctly priced I don’t think DoS is an issue. With more than 2x elasticity we can have more stable gas prices, reliable confirmations, and handle the irregularities in demand.

I agree that as a gas storage mechanism, current refunds are inefficient and waste storage, but if we had another refund mechanism that was slightly more efficient and didn’t waste storage, classic gas tokens would be out-competed. We would lose the constant state growth property, but the elasticity would come much cheaper in both storage and computation.

This can be done with three opcodes and a persistent account gas refund counter, which could implement a better gas token:

- SELFGAS which pushed the current account’s refund counter onto the stack
- USEGAS which reduces the contract’s refund count by up to the amount popped from the stack, adding the amount to the refund counter
- STOREGAS which increases the current account’s refund counter and consumes additional gas by the amount popped from the stack

This would preserve the gas market and the stability it provides, while phasing out usage of inefficient and wasteful alternatives.

---

**wjmelements** (2021-03-04):

I wrote up the efficient gas storage approach [here](https://github.com/ethereum/EIPs/pull/3322).

---

**vbuterin** (2021-03-04):

> I should hope that’s not the explicit goal, but you don’t achieve it here; GST1 would still work.

Now that I think about it, you are right; the refunds would be still able to cancel out the portion of gas usage that is new-storage-fills. The refund rule would have to be more restrictive (refund only if `0 = original = new != current`) to solve that issue.

> You would still have block size variance because you have refunds.

But this is not true, because the key invariant that remains is that *gas spent on execution* would not go above the gaslimit. Every 15000 gas refund would be matched by 15000 gas spent on filling a new storage slot.

> Based on the text I think you got the subtraction backward but it’s problematic either way.

I don’t think it’s backward! You refund only if you cleared more storage slots than you fill.

Another thing worth considering is that clearing storage is going to be less useful in the future, if we are implementing [either weak statelessness or state expiry](https://ethereum-magicians.org/t/weak-statelessness-and-or-state-expiry-coming-soon/5453). In fact, truly clearing storage would not even be possible; you would need to leave a stub to show that the value is zero, as opposed to the slot being not-yet-edited and the value needing to be dug up from the past. So in the longer term, having less good incentives to clear storage is not even such a useful thing.

---

**wjmelements** (2021-03-19):

The [EIP 3403](https://github.com/ethereum/EIPs/pull/3403/) discussions-to link points here.

I do prefer 3403 to 3298 because it fixes 3298’s storage misincentive, though my preference is still 3322 because I support block elasticity.

> Remove the SSTORE refund in all cases except for one specific case: if new value and original value both equal 0 but current value does not, refund 15000 gas.

The 15000 number should probably be higher. I think the Istanbul refund for this scenario is 19800. Since this is a “warm read” it should be cheap and also refund the bulk of the 20000 cost from `SSTORE_SET`.

Since the proposal removes all refunds except for this case, it doesn’t make sense to maintain a refund counter. Instead, the gas should be added to current gas counter. Should the gas used by a `*CALL` be negative, the surplus gas is returned to the gas counter, so that the cost negation works recursively. Then the refund counter can be removed entirely.

---

**saurik** (2021-04-01):

> You are mistaken. eth_estimateGas already returns the correct gas limit.

Huh… if I have a case where this isn’t true–due to refunds–is this a bug I could thereby file and it would get fixed? I’d looked through other issues and I was under the impression that the eth_estimateGas issues were just “this is known to not work and we aren’t going to fix it” ;P.

---

**saurik** (2021-04-01):

So, I work on a layer 2 payments system that has to use storage to prevent replays (and the order is intrinsically arbitrary, so it can’t use a monotonic nonce). I use one storage slot per payment. Right now, I’ve got everything set up so that everyone would naturally “want to” delete expired replay prevention slots. (Yes: I also added a way to “forge” replay prevention slots, as it also forms a gas token ;P. I don’t care at all about this behavior.)

The result of this is that, over time, usage of the contract is going to result in O(number of users) storage, as it will be something like “the only storage slots in use are for the payments that haven’t yet been expired, and each user has some small number of payments in flight at any one moment”. Without refunds of any form, this is going to be O(number of payments), which is much much much bigger (something Ethereum obviously itself avoids with its account model).

FWIW, the “viability” of a gas token is strongly related to the “power” of the refund. Have you considered making it so that deleting a storage slot just makes the storage cost non-existent and gives you maybe a tiny 500-800 gas refund? This wouldn’t be viable for a gas token, as you’d need ~500 gas to even specify and find/calculate the storage slot that is storing the gas token you are freeing: the goal of this refund (and associated subsidy) is just to make it economically reasonable to be a bit altruistic and clean up old state.

Put differently, I think there’s something valuable in strategies that don’t necessarily “reward” people for messing with storage state in potentially-weird ways but at least doesn’t *penalize* people for cleaning up state: without refunds–and with deletions costing thousands of gas–I’d actually be punished pretty hard for bothering to clean up state, and I feel like I should want to clean up state even if it isn’t making me money, as long as it isn’t hurting me.

(edit: And like, I appreciate that maybe in the future state doesn’t matter as much, or it will naturally expire and I won’t need strategies for expiring it myself; I definitely think maintenance of state perpetually isn’t sustainable… but, given the speed of how changes happen, it could be years before we get there, and I want to think that systems like mine should have at least not be disincentivized from avoiding spamming state ;P.)

---

**wjmelements** (2021-04-02):

3403 still ruins any incentive to clean up state outside of the same transaction. The misalignment of incentives should offset any perceived gains on the storage-bloat motivation, but with real storage that would need to be rented under any state rent scheme. The concerns described by [@thabaptiser](/u/thabaptiser) have only been addressed in the same-transaction case. Here are some specifically incentivized behaviors, which I listed in ACD.

- Storage arrays should use 1-indexing such-that length-zero is stored as 1 so adding anther element does not incur SSTORE_SET. Additionally, popped elements should not be cleared for the same reason
- UI-prompted approvals should always be infinite.
- When selling all tokens you should leave 1 in your wallet, which will change the “Sell MAX” behavior on most DEX interfaces.

I’m also opposed to 3403’s motivation because I favor elasticity. 4x is the best part of 1559 and as a power user who transacts during congestion I don’t want to see larger spikes.

In ACD, [@holiman](/u/holiman) mentioned that miners have been mining blocks that are only gas tokens. [F2Pool clarified](https://twitter.com/bitfish1/status/1372218378350305285) this was because this is their default candidate block and it is only mined if they have not yet sealed another.

In ACD it was mentioned that miners may increase the gas limit under 1559 to fight against the base fee. The possibility of 4x may discourage that behavior since they will struggle to capitalize on MEV if 4x exceeded their full capacity. Because of this and sync-time concerns for the node failure case, I don’t expect miners to target the gas limit above 4x their capacity.


*(9 more replies not shown)*
