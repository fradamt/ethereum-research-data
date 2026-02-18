---
source: magicians
topic_id: 21234
title: "EIP-7778: Prevent Block Gas Smuggling"
author: benaadams
date: "2024-10-01"
category: EIPs > EIPs core
tags: [evm]
url: https://ethereum-magicians.org/t/eip-7778-prevent-block-gas-smuggling/21234
views: 215
likes: 1
posts_count: 5
---

# EIP-7778: Prevent Block Gas Smuggling

Exclude Discounts & Refunds for Block GasLimit Enforcement

Complementary to to



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png)

      [EIP-7623: Increase Calldata Cost](https://ethereum-magicians.org/t/eip-7623-increase-calldata-cost/18647) [EIPs core](/c/eips/eips-core/35)




> By increasing the calldata cost for users that do not spend more than a certain threshold on EVM computation we can achieve the following:
>
> Reduce maximum possible blocksize from ~1.7 MB to 0.55 MB without effects on current throughput.
> Reduce block size variance
> Reduce inefficienty from big gap between avg. block size and max. possible block size.
> Make room for raising gas limit and/or blob count
> Differentiate between users that need calldata inside the EMV vs pure DA.
>
> This is achieved by inc…

Prevent the circumvention of the block gas limit by excluding certain gas discounts and refunds from block gas accounting, except for those reflecting actual reductions in computational work.

This proposal aims to align the block gas usage with the Ethereum Virtual Machine’s (EVM) real workload, preventing “block gas smuggling.” It complements [EIP-7623](https://github.com/ethereum/EIPs/pull/eip-7623) by further reducing the maximum block size and its variance, enhancing network stability and efficiency.

Link:

https://github.com/ethereum/EIPs/pull/8918

## Replies

**jochem-brouwer** (2024-10-06):

Regarding receipt encoding, what should be encoded in the receipt of the tx? We have a `cumulative gas used` field there. I think the encoded `cumulative gas used` here should reflect what gas was used in the block, i.e. `evm_gas_used`?

---

**benaadams** (2024-10-10):

It should be the gas used without refunds (i.e. the value used for the block gaslimit/target check); so would be higher than the sum of the gas charged per tx

---

**milos** (2025-12-04):

I think that receipts should have both value, as both are useful:

- higher value (before refund) - when calculating/validating total gas used in the block
- lower value (after refund) - block explorers when showing how much user paid for transaction

When it comes to naming, I suggest:

- keep cumulativeGasUsed and gasUsed be the values used for block limit calculations (keep consistent naming)
- add new field for gas after refund, e.g.: gasPaid

---

**Nerolation** (2025-12-04):

Right now, even though this is not very clearly spec’d in the EIP, the gas_used in the receipt would represent the gas used after applying the refund.

For validating the block gas limit using the receipts, you would need to keep track of the refund of each transaction during execution and when doing the cumulative sum, add every refund to the gas used of the respective transaction.

Thanks for bringing this up. I’ll make a PR to clarify that in the EIP.

EDIT: PR as promised:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/10872)














####


      `master` ← `nerolation:clarify-receipts-7778`




          opened 11:07PM - 04 Dec 25 UTC



          [![](https://avatars.githubusercontent.com/u/51536394?v=4)
            nerolation](https://github.com/nerolation)



          [+1
            -0](https://github.com/ethereum/EIPs/pull/10872/files)







The `gas_used` in receipts is the value after applying the refund.

