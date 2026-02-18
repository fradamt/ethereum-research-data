---
source: magicians
topic_id: 6097
title: "EIP 3529: reduction in refunds (alternative to EIP 3298 and 3403) that better preserves existing clearing incentives"
author: vbuterin
date: "2021-04-25"
category: EIPs > EIPs core
tags: [opcodes, gas]
url: https://ethereum-magicians.org/t/eip-3529-reduction-in-refunds-alternative-to-eip-3298-and-3403-that-better-preserves-existing-clearing-incentives/6097
views: 59299
likes: 4
posts_count: 8
---

# EIP 3529: reduction in refunds (alternative to EIP 3298 and 3403) that better preserves existing clearing incentives

## Simple Summary

Remove gas refunds for SELFDESTRUCT, and reduce gas refunds for SSTORE to a lower level where the refunds are still substantial, but they are no longer high enough for current “exploits” of the refund mechanism to be viable.

## Link



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/3529)














####


      `master` ← `vbuterin-patch-1`




          opened 05:28PM - 24 Apr 21 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/1X/882285f3628ea3784835c306639dd8f62179a6d9.png)
            vbuterin](https://github.com/vbuterin)



          [+136
            -0](https://github.com/ethereum/EIPs/pull/3529/files)







An alternative way to reduce refunds to deal with the issues addressed in EIPs 3[…](https://github.com/ethereum/EIPs/pull/3529)298 and 3403.

## Replies

**holiman** (2021-04-26):

Comment from [@chfast](/u/chfast) via ACD discord:

> Why NEW_MAX_REFUND_QUOTIENT not MAX_REFUND_QUOTIENT?

Valid point, I guess

---

**jochem-brouwer** (2021-05-02):

I am slightly confused by the test cases. This effective gas used is **before** we apply this new max quotient rule, right?

---

**jochem-brouwer** (2021-05-02):

Is there a test case where we can hit this max refund? I tried clearing 100 storage slots and this did not yield a refund which is larger than 1/5th of the gas used.

---

**BoringCrypto** (2021-05-03):

This will still lead to plenty of cases where it will encourage me as a coder to leave a value instead of clearing state. Not ideal.

Why not simple cap the refund to 20% or 25% of the tx cost? That will make gas tokens pretty inefficient, to the point where they aren’t so relevant. Also reduces the max gas limit you can push, dealing with DoS attack issues.

In practice, most real contract calls don’t get close to the 50% limit, but gas tokens exploit this to the limit. Some analysis could be done here to see what a good max refund value is, but my feeling is that somewhere around 25% will be very acceptable.

Love the low costs of 0 > value > 0 within a tx… also dropping SELFDESTRUCT refunds are fine by me.

---

**geoknee** (2021-05-06):

The EIP aims to strike a balance between on the one hand reversing the unexpected harmful consequences of gas refunds (namely, gas tokens and block size variance) and on the other hand maintaining the benefits of original motivation for refunds (good state hygiene).

Part of that balance is to maintain a strong incentive to restore storage slots to zero, if those same slots were zero at the beginning of the transaction. I would like to suggest modifying the EIP so that the analogous refund is available for creating and destroying the same contract in a single transaction.

Such “ephemeral” contracts are an elegant pattern for state channel contract architecture: a (mostly) private interaction between a small number of parties who unanimously agree should not need to leave any trace on the L1 chain. In such a pattern, parties pay assets to a predictable `CREATE2` address, and after their off-chain interactions proceed to launch a transaction which i) deploys a contract  at the `CREATE2` address which then  ii) verifies their signatures , iii) pays out the funds and iv) self destructs.

I’m a contributor to [statechannels.org](https://statechannels.org/), where we are seriously considering the use of ephemeral contracts. I estimate that under this EIP gas costs for state channels using this pattern may increase by approximately 20%. It would also disincentivize our current efforts at good state hygiene and result in many contracts remaining in state unnecessarily.  Furthermore, because (as is) the EIP is somewhat asymmetric with respect to modifying state-based refunds and contract based-refunds, the differential gas cost with respect to other state channel contract architectures (that we have considered) might lead to neglecting the ephemeral contract pattern entirely, which may lead to even more state bloat.

Under my proposed modification, the incentives and gas would remain mostly as they are now for the ephemeral contract pattern (since the `NEW_MAX_REFUND_QUOTIENT` allows for the 20% refund we currently enjoy).  It does not re-allow gas tokens, since self-destructs would only be allowed for contracts created earlier in the same transaction. More gas will have been spent creating the contract than will be refunded.

I am unsure, however, if it is as straightforward for clients to avoid writing to storage at all in such transactions (the analogue of the “prudent optimisation” of the EIP). Perhaps someone with more knowledge can comment?

---

**k06a** (2021-06-09):

Came up to one interesting related issue. On reverting subtrace gas refund counter gets erased while it could be made equal to `MAX(0, SSTORE_GAS_SPENT_INSIDE_THIS_REVERTED_CALL)`. This would make a lot of transactions reasonably cheaper.

---

**k06a** (2021-07-06):

I see an issue with the following flow within single transaction:

1. Write non-zero to zero storage slot
2. Write zero to the same storage slot
3. Revert both actions

Gas cost of the following solution would be approximately 25k without any gas refund (revert erases gas refunds). But actual job of doing nothing should not cost that high.

I propose instead of erasing gas refund on revert keep it equal to cost of all the reverted SSTORE operations.

