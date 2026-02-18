---
source: magicians
topic_id: 18647
title: "EIP-7623: Increase Calldata Cost"
author: Nerolation
date: "2024-02-14"
category: EIPs > EIPs core
tags: [gas]
url: https://ethereum-magicians.org/t/eip-7623-increase-calldata-cost/18647
views: 5803
likes: 28
posts_count: 76
---

# EIP-7623: Increase Calldata Cost

By increasing the calldata cost for users that do not spend more than a certain threshold on EVM computation we can achieve the following:

- Reduce maximum possible blocksize from ~1.7 MB to 0.55 MB without effects on current throughput.
- Reduce block size variance
- Reduce inefficienty from big gap between avg. block size and max. possible block size.
- Make room for raising gas limit and/or blob count
- Differentiate between users that need calldata inside the EMV vs pure DA.

This is achieved by increasing cost for DA users (who can move towards using blobs).

PR:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/8218)














####


      `master` ← `nerolation:master`




          opened 09:19PM - 13 Feb 24 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/d/d4f2263996da2d20c2cfa6fa7537c3849f106b12.jpeg)
            nerolation](https://github.com/nerolation)



          [+87
            -0](https://github.com/ethereum/EIPs/pull/8218/files)







This EIP aims to reduce the maximum possible blocksize without impacting regular[…](https://github.com/ethereum/EIPs/pull/8218) users.
This is achieved through a conditional expression that is used to determine the gas used.
Thereby, users that consume more than a certain threshold EVM gas per calldata byte will still have 16 gas calldata while DA users pay 68 gas per calldata byte.












More info:


      ![](https://ethresear.ch/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_32x32.png)

      [Ethereum Research – 5 Feb 24](https://ethresear.ch/t/on-increasing-the-block-gas-limit/18567?u=nerolation)



    ![image](https://ethereum-magicians.org/uploads/default/original/2X/e/e3d43baa3aafc8a2f9fb9b1b61af7212f4db6855.png)



###





          Economics






            data-availability







On Increasing the Block Gas Limit by Toni and Vitalik.  special thanks to the Starkware team for feedback and data!  The TL;DR  By increasing the block gas limit and the price for nonzero calldata bytes, a smaller and less variable block size can...



    Reading time: 8 mins 🕑
      Likes: 48 ❤












      ![](https://ethresear.ch/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_32x32.png)

      [Ethereum Research – 24 Jan 24](https://ethresear.ch/t/on-block-sizes-gas-limits-and-scalability/18444?u=nerolation)



    ![image](https://ethereum-magicians.org/uploads/default/optimized/2X/b/bbff5cd4085bae3a991ee097e391e6a62baf7956_2_690x229.png)



###





          Economics






            scaling
            eip-1559
            resource-pricing
            fee-market







On Block Sizes, Gas Limits and Scalability  Thanks to Alex Stokes, Matt (lightclients) and Matt Solomon for feedback and review!   There has been much discussion about raising Ethereum’s block gas limit recently.  Some argue for bigger blocks...



    Reading time: 8 mins 🕑
      Likes: 48 ❤

## Replies

**storm** (2024-02-19):

`TOTAL_COST_FLOOR_PER_TOKEN` seems like a good heuristic for penalizing call data heavy txs and nudging them toward blobs

to red-team this a bit, are there any circumstances where allowing larger amounts of call data is important or necessary for security? examples:

1. large number of users might need to submit fraud proofs for optimistic rollup(s) over a short period of time. what might that realistically look like in terms of total EL call data requirements? and is there any other situation where users might need to replicate lots of blob data into regular execution call data?
2. what are the other unlabeled points in the lower half of the transaction_dist.png in On Increasing the Block Gas Limit? are any of those use cases both 1) important and 2) difficult to convert to blobs?
3. has any bridge dev team encountered difficulty in converting their architecture over to blobs? what is a reasonable timeline to expect most/all of them to blobify?

---

**MariusVanDerWijden** (2024-02-20):

Draft implementation in geth: [[wip] core: implement eip-7623: increase calldata cost by MariusVanDerWijden · Pull Request #29040 · ethereum/go-ethereum · GitHub](https://github.com/ethereum/go-ethereum/pull/29040)

One issue I came across is that the EIP is kinda underspecified wrt. the gas costs for contract creation vs normal transactions. A normal transaction costs `21000 + Tokencost * Tokens + evm_gas`, a contract creation costs `53000 + Tokencost * Tokens + 2 * Initcode_Wordsize + evm_gas`.

I’ve interpreted the EIP as follows:

```auto
tx.gasUsed = {
    21000 + 32000 * isContractCreation // 21000 or 53000
    +
    max (
        STANDARD_TOKEN_COST * tokens_in_calldata + IsContractCreation * (InitCodeWordGas *  words(len(calldata))) + evm_gas_used,
        TOTAL_COST_FLOOR_PER_TOKEN * tokens_in_calldata
    )
)
```

Where IsContractCreation is 1 if the transaction is a contract creation and 0 otherwise.

---

**Nerolation** (2024-02-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/storm/48/11361_2.png) storm:

> large number of users might need to submit fraud proofs for optimistic rollup(s) over a short period of time. what might that realistically look like in terms of total EL call data requirements? and is there any other situation where users might need to replicate lots of blob data into regular execution call data?

The formula is applied for each transaction, so it doesn’t matter if multiple use have to execute transations with much calldata at the same time. They are only limited by the block gas limit. I don’t see scenarios where many regular users suddenly need to post 1MB calldata transactions.

Regarding 2, I’ll do further analysis on those outliers but I expect that 99.9% of all transactions using enough evm resources to “qualify” for the 16 gas calldata cost. Then this EIP would basically reduce the max possible block size without impacting regular users at all. Only DA via calldata should become more expensive, preventing the EVM having to deal with Inscriptions, or rollup data.

Regarding 3. I think some of the rollups will start using blobs from day one while the majority plans to shift in the following days/weeks. I’ve only seen a few announcing that they will not yet move to blobs. In the end, rollups know that this is coming and all of them are prepared.

---

**Nerolation** (2024-02-21):

Yeah, you’re right.

The `initcode` cost of currently 2 gas per word might be negligiable low compared to the calldata costs but it makes full sense to put them into the formula, treating it similar as the base cost.

One could even go one step further and adjust the formula to distinguish between CREATE and CREATE2 deployments:

```python
tx.gasUsed = {
    21000 \
        + (32000 + InitCodeWordGas *  words(calldata)) * isContractCreation  \
        + isCreate2Creation * Keccak256WordGas *  words(calldata)
    +
    max (
        STANDARD_TOKEN_COST * tokens_in_calldata + evm_gas_used,
        TOTAL_COST_FLOOR_PER_TOKEN * tokens_in_calldata
    )
)
```

I’d still keep the gas involved with contract creations outside the conditional part of the formula.

---

**vbuterin** (2024-02-28):

I would actually go for Marius’s interpretation!

My reasoning is that `Keccak256WordGas` and `InitCodeWordGas` are “actually” not data-related costs, but rather execution-related costs. Those costs were introduced because of issues that have to do with the expense of processing the CREATE and CREATE2 *opcodes*, and were added to transaction-level creates for symmetry. So they should be put in the same bucket as `evm_gas_used`.

I would even go so far as to put `32000 * isContractCreation` into the same bucket as execution-related costs (since a contract creation by itself isn’t any heavier on calldata than a regular transaction), but I’m happy to go either way on that.

---

**Nerolation** (2024-02-28):

I see! Based on that the formula would look like this:

```python
tx.gasUsed = {
    21000 \
    +
    max (
        STANDARD_TOKEN_COST * tokens_in_calldata \
           + evm_gas_used , \
           + isContractCreation * (32000 + InitCodeWordGas *  words(calldata)),
        TOTAL_COST_FLOOR_PER_TOKEN * tokens_in_calldata
    )
```

Ive skipped the CREATE2 part, so the difference to [@MariusVanDerWijden](/u/mariusvanderwijden) approach is the 32k base cost inside the `max()`.

I agree that the 32k contract creation could be put into the `evm_gas_used` side of the `max()` , contributing towards the standard token cost. Also, the CREATE opcode is different from the 21k base cost and one can argue that it must therefore be treated differently in the gasUsed formula.

---

**chfast** (2024-03-15):

How about we remove the special zero-byte cost from the formula as it make no sense?

---

**qizhou** (2024-03-27):

Would the gas cost for EIP-2930 also need to be adjusted since the storage data cost under EIP-7623 is `32 * 68 = 2176`, which exceeds `1900` in EIP-2930.

---

**Nerolation** (2024-04-02):

With respect to snappy compression rates it does make sense, as many consecutive zeros can be compressed very well. The formula assumes that zero bytes are less expensive than non-zero bytes.

There’s more info on that here:

https://eips.ethereum.org/EIPS/eip-2028

---

**Nerolation** (2024-04-02):

Could you elaborate on that?

The access list gas in charged in addition to the base tx cost, why would it be affected?

Or are you comparing them as a DA layer now?

Edit: We were thinking about 48 (instead of 68) as a better price anyway (because of merkle proof, post quantum crypto, etc.) and 48 happens to not be vulnerable to the scenario you describe.

It’s fixed in the current version of the EIP. Thanks!

---

**wjmelements** (2024-04-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> If someone wants to publish data just for availability, they will switch to logs.

How will they publish to the logs without calldata?

---

**qizhou** (2024-04-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> The access list gas in charged in addition to the base tx cost, why would it be affected?
> Or are you comparing them as a DA layer now?

My point is that the tx access list in 2930 is charged independently compared to calldata cost (see [go-ethereum/core/state_transition.go at 35fcf9c52b806d2a7eba0da4f65c97975200a2b2 · ethereum/go-ethereum · GitHub](https://github.com/ethereum/go-ethereum/blob/35fcf9c52b806d2a7eba0da4f65c97975200a2b2/core/state_transition.go#L113)), but **it** **takes the same block space as calldata**.  That means that if the tx access list is under-charged vs calldata cost, an attack will use the tx access list to create a larger block that circumvents the limit of EIP-7623.

For example, a storage key in the tx access list takes at least 32 bytes (let’s ignore the overhead of RLP encoding); thus, the gas cost per byte of the storage key is 1900 / 32 = 59.37. That said, if the calldata per gas cost is 68, then an attacker can still create a larger block size post-EIP-7623 by filling a large number of storage keys in the tx.

Reducing the gas cost of calldata per byte to 48 should alleviate the issue as using access list to create a large block is less cost-efficient than using calldata.

---

**dror** (2024-04-09):

The motivation for this EIP looks great.

A side-effect is that it clears out the cost of a transaction.

It *could* be written just as “never charge less than 48*tokens_in_calldata”, but instead, it tries also to spell out the existing gas cost

What I miss in the document are some examples of the impact on TXs that use cpu-gas: That is, what kind of non-L2 transaction might get hurt by this change.

---

**Nerolation** (2024-04-09):

Thanks for pointing that out. I could have linked to some more analysis here but didn’t (yet).

There’s this “post-4844” analysis that highlights the impact of the EIP on post-4844 Ethereum:


      ![](https://ethresear.ch/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_32x32.png)

      [Ethereum Research – 3 Apr 24](https://ethresear.ch/t/eip-7623-post-4844-analysis/19199)



    ![image](https://ethereum-magicians.org/uploads/default/original/2X/f/f4de385119c7fceddf740fd319d49281b35a0a05.png)



###





          Execution Layer Research






            fee-market







EIP-7623 - Post-4844 Analysis EIP-7623 proposes to increase the calldata cost for transactions that use Ethereum mainly for DA.  This is done by setting a floor price for non-zero bytes at 48 gas and zero-bytes at 12 gas.  The goal is to reduce...



    Reading time: 1 mins 🕑
      Likes: 6 ❤











**It also includes a site where the most commonly used functions are listed together with stats on gas usage and indicating if they’d be affected by this EIP.**

**Find it here:**

**[EIP-7623 - Impact](https://nerolation.github.io/eip-7623-impact-analysis/index2.html)**

In summary, there aren’t many non-DA use cases for big-calldata transactions. One of them are big zk-proofs like STARKs, as well as very large merkle proofs.

As visible in the above table, the number of transactions affected is very small and those non-DA that are affected are not impacted drastically (e.g. certain STARK transcation increase by ~30%).

The largest part of affected users are those attaching additional data to their transaction (messages). For them, the increase in gas cost is negligible as those messages are usually very small (and, to be fair, there are better ways to do messaging than using Ethereum L1 anyways).

---

**Nerolation** (2024-04-11):

# Quick summary/faq on

# What?

- EIP-7623 proposes to introduce a floor cost for calldata.
- Transactions that use Ethereum mainly for DA will pay 12 (zero bytes) and 48 (non-zero bytes) gas per byte.

# Why?

- The main goal is to reduce the maximum possible block size form 3.5 MiB to 1.9 MiB (incl blobs).
- Reduce history growth (theoretically as avg. block size might remain the same).

# How?

The new formula to calculate the gas used per tx would be:

```auto
tx.gasUsed = {
    21000 \
    +
    max (
        STANDARD_TOKEN_COST * tokens_in_calldata \
           + evm_gas_used \
           + isContractCreation * (32000 + InitCodeWordGas * words(calldata)),
        TOTAL_COST_FLOOR_PER_TOKEN * tokens_in_calldata
    )
```

with `STANDARD_TOKEN_COST` = 4,

and `TOTAL_COST_FLOOR_PER_TOKEN` = 12,

and `tokens_in_calldata = zero_bytes_in_calldata + nonzero_bytes_in_calldata * 4` (in order to one-dimensionalize calldata).

# Who would be affected?

- Largest part: users putting messages into their transactions (negligible).
- DA users (negligible because they have blobs).
- Certain use cases such as STARK proofs, or very large merkle proofs that are heavy in calldata but don’t require much computation.
- Simply speaking, every transaction that pays 2x on EVM computation than what it spends on calldata will be unaffected. Around 3% of transaction would be affected. Regular users who are sending ETH, tokens, swapping, etc. are unaffected.

# Why floor ar 12?

- This makes sure that access lists don’t become cheaper than calldata (otherwise one could again produce “big block” by filling access lists. (h/t @qizhou)

# When?

- proposed for inclusion in the Pectra hardfork

# Useful links

- Implementation EL specs
- Implementation Geth
- Post 4844 Analysis

---

**wjmelements** (2024-04-26):

There is a problem with this floor gas pattern: the marginal cost of additional execution can be zero. This means it is free for a transaction with lots of calldata to package additional operations. This allows such transactions to sell this free gas on the market, which could cause all sorts of havoc. Gas should therefore never be structured this way.

---

**shemnon** (2024-04-26):

Can you provide a worked example of how this might be done?  I don’t think we need EVM code but a description of what the contracts would do should suffice.

---

**wjmelements** (2024-04-26):

Suppose there is a protocol whose recurring transactions require lots of calldata but do little execution. Several L2s are in this category, but there could also be graffiti apps. Many of their transactions will have gasUsed based entirely on their calldata due to the `max` calculation. They can auction out additional `CALL`s or even `AUTHCALL`s to their periodic transaction, specifying a total gas limit according to their `CALLDATASIZE`. The marginal cost of these auctioned calls to the operator is only their additional calldata, which can even be zero if the auctioning mechanism is implemented on-chain.

So, a calldata operator has been forced to buy extra gas by this EIP, but they can sell it, and this can offset their gas costs.

The maximum price a reasonable buyer would pay for the auctioned gas is the base fee, but the operator should be willing to sell their gas for much less than the base fee to offset their costs, according to demand. They will sell it at any price because from their perspective, it is free gas.

---

**wjmelements** (2024-04-26):

There is a parallel problem: a transaction with a lot of gasUsed but not much calldata could sell extra calldata. This additional calldata costs the gasUsed operator according to the `STANDARD_TOKEN_COST` schedule, so they could sell it to someone who would otherwise pay `TOTAL_COST_FLOOR_PER_TOKEN`.

So in summary this EIP creates a gas loophole that incentivizes heavy gasUsed operators who don’t use much calldata to pair up with heavy calldata operators who don’t have much gasUsed, combining into one transaction. It creates separate markets for both kinds of gas.

---

**Nerolation** (2024-04-26):

First, I don’t think that using a lot of calldata to then sell off operations is a serious threat.

It’s not free gas because the respective entity still pays the standard price for it. Selling EVM operations on a second market to potentially offset the floor cost might work but I don’t see something like that ever happening.

Even in the case that there are transactions (remember, it’s currently 2% of all tx that would hit the floor price with most of them being regular user posting comments of a few bytes into the calldata) that can sell of EVM operations, the goal of reducing the max block size is achieved.

So, I see your point but I don’t believe these are practical concerns. Writing the software to trustlessly outsource EVM operations or storage space in someone else’s calldata doesn’t seem very viable.


*(55 more replies not shown)*
