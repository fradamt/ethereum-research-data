---
source: ethresearch
topic_id: 11924
title: Optimizing cross-chain swaps
author: Mike
date: "2022-02-02"
category: Layer 2
tags: []
url: https://ethresear.ch/t/optimizing-cross-chain-swaps/11924
views: 4694
likes: 17
posts_count: 8
---

# Optimizing cross-chain swaps

As layer 2s and alternative chains gain traction, we have seen a number of new bridging projects. Some examples are [nxtp](https://github.com/connext/nxtp), [Hop](https://hop.exchange/), [Thorchain](https://thorchain.org/), [Across](https://across.to/) and [Multichain](https://app.multichain.org/#/router).  Considering the high fees users pay to use these systems, we at [Magmo](http://www.magmo.com) wondered how low we could drive down the cost of cross-chain swaps.

The output of our research is SAFE, the Secure Asymmetric Frugal Exchange. SAFE is a simple and efficient technique for batching cross-chain swaps with the following desirable properties:

- Secure — the protocol is as secure as the weakest chain in the swap.
- Frugal — the protocol attempts to minimize the cost of an individual swap.
- Asymmetric — frugality is achieved by batching swaps. Many swap requests on the From Chain are batched and redeemed in one transaction on the To Chain.

While SAFE is a generalized cross-chain swap protocol, the protocol is especially cost-effective in an environment where the transaction fees on the From Chain are lower than the fees on the To Chain. An example of this scenario is a swap from a rollup to L1 Ethereum.

#  Cost comparison

We used the [SAFE prototype](https://github.com/statechannels/safe-protocol) to compare SAFE to [nxtp](https://github.com/connext/nxtp), which we chose as it also uses HTLCs. Our comparison focuses on 2 benchmarks. In the first benchmark, 100 unique addresses each swap an asset from Optimism to mainnet. In the second benchmark, the swap is from Optimism to an Optimism clone. Note we assume L1 gas cost of 150 gwei.

|  | nxtp total cost for 100 swaps | SAFE total cost for 100 swaps |
| --- | --- | --- |
| Optimism to mainnet | 3.78 ETH | 0.266 ETH |
| Optimism to OP clone | 1.07 ETH | 0.111 ETH |

It should also be noted that nxtp is a more feature rich implementation than SAFE. In addition, nxtp contracts are production code whereas SAFE is a prototype. As a result, we expect SAFE costs to increase as feature are added and contracts are hardened. Nevertheless, the initial benchmarks are very promising! Full benchmark data can be found [here](https://github.com/statechannels/SAFE-protocol/tree/main/doc/benchmark.md).

#  SAFE in a nutshell

[Hashed Timelock Contracts](https://en.bitcoin.it/wiki/Hash_Time_Locked_Contracts) are a proven technique for atomic swaps.

[![htlc](https://ethresear.ch/uploads/default/optimized/2X/4/4534be2ea4b34634cdae47a516513cf81583827b_2_690x400.png)htlc1345×781 56 KB](https://ethresear.ch/uploads/default/4534be2ea4b34634cdae47a516513cf81583827b)

HTLC sequence of calls

SAFE expands on HTLCs by introducing batching. Batching groups many swap requests on the From Chain into one transaction on the To Chain, making SAFE particularly cost effective in asymmetric cost environments. There are 2 roles in SAFE:

1. A customer — the customer wishes to swap assets from the From Chain to the To Chain.
2. A liquidity provider (LP) — the LP holds assets on the To Chain and is willing to trade those assets for From Chain assets (for a fee).

During normal operation, customers continually submit withdrawal tickets to the From Chain. Periodically, a batch of tickets is created and authorized by the LP. The authorized batch is then used to:

1. Distribute batch funds to customers on the To Chain.
2. Transfer batch funds to the LP on the From Chain.

[![safe](https://ethresear.ch/uploads/default/optimized/2X/6/6e05311eb0e9013be51d66048e3404f3727507ae_2_690x202.png)safe2694×789 157 KB](https://ethresear.ch/uploads/default/6e05311eb0e9013be51d66048e3404f3727507ae)

 SAFE sequence of calls

#  Cost model

In SAFE, the following transactions must take place:

1. The customer submits a single transaction to the From Chain.
2. To service a swap for a customer, the LP must submit two From Chain transactions plus one To Chain transaction. However, the LP may service a batch of n swaps with this triplet of transactions, amortizing the bulk of the cost across many swaps.
3. In addition, the LP would periodically move funds from the From Chain to the To Chain. We expect these transactions to be infrequent relative to (1) and (2), so these are ignored.

Thus, the customer’s swap is serviced with `1 + 2/n` transactions on the From Chain and `1/n` transactions on the To Chain, where `n` is the number of swaps serviced per batch.

#  Safety

SAFE protects customers against a malicious liquidity provider. The customer must have the ability to monitor and submit transactions to both the From and To Chains. The customer is guaranteed that either:

- Their swap is completed, and they receive assets on the To Chain.
- The swap is abandoned, and they reclaim assets on the From Chain.

Details and an informal security analysis are found in [the SAFE spec](https://github.com/statechannels/SAFE-protocol/blob/a48197afd15b7f621cb476d00f86fc956e490573/doc/SAFE.md). Obvious extensions to SAFE can include logic on the From Chain to incentivize good behaviour.

#  Limitations of SAFE

As described in the spec, SAFE focuses on asset swaps where one asset on the From Chain maps to one asset on the To Chain. Other projects like Thorchain combine AMM and swaps to allow, for example, swapping native Bitcoin to native Ethereum. We have not explored in detail how to add features like this to SAFE.

In addition, our current contracts do not include the necessary checks to prevent common blockchain attacks. This choice is intentional, aiming for clarity and understanding of the core protocol at the prototype stage.

## Replies

**rjdrost** (2022-02-02):

Nice writeup and great to have useful diagrams for vanilla HTLCs vs. SAFE!

HTLC-like protocols have important security and trustlessness properties when bridging consensus domains. It’s helpful that this work points to potential headroom for further gas optimizations with bridging systems that build on HTLC-like protocols already (for other good reasons).

There’s also an important point that’s useful to highlight in the diagrams. The SAFE diagram illustrates the nice asymmetry (the “A” in SAFE) in the transactions which, during L2 withdrawals to Mainnet, reduces the L1 transactions from the 2 in an HTLC to only 1 here. Batching then provides even more gas savings by amplifying this asymmetry. Minimizing friction from L1 gas costs when moving around liquidity by using synergistic mechanisms is a really helpful protocol research direction!

---

**yahgwai** (2022-02-06):

Nice! Have you thought how fees would fit into this model? If batch sizes are dynamic it might be difficult to give a good estimate to a user at the time they make their deposit.

I think there’s also a simpler variation of SAFE which is applicable to only rollup->mainnet withdrawals but which would remove the need for users to watch for fraud:

Users submit funds to an L2 withdrawal contract. This L2 withdrawal contract will only allow withdrawal by the users after a specified amount of time (*INACTION_TIME*), or withdrawal to any address by the L1 counterpart to this L2 contract.

Once enough user deposits have built up in the L2 contract the LP sends a tx the counterpart withdrawal contract on L1. They specify the ids, amounts and to addresses for the withdrawals and the contract sends these funds out on L1. As part of the same transaction the L1 withdrawal contract sends an L1-to-L2 message specifying what withdrawals took place. When this L1-to-L2 message arrives on the L2, the L2 withdrawal contract checks that the message was sent by the correct L1 contract, and that the ids, amounts and addresses that were sent on L1 correspond to the deposits made on L2. It then sends out an amount to the LP’s address on L2 equal to the sum of the correct withdrawals that were.

This variation involves sending an amount, an id and address for each withdrawal in the L1-to-L2 message, but this could be made cheaper by making it 2-stage. Just a hash of the L1 withdrawals is sent in the message and stored in the L2 withdrawal contract. The LP can then provide the pre-image of this hash on L2 to prove which withdrawals were made.

This variation relies on the atomicity of L1-to-L2 messages, which should be guaranteed by any L2. It also requires the message to be processed before *INACTION_TIME* has expired to avoid the user withdrawing their funds due to perceived in inaction on the part of the LP.

**Pros vs SAFE:**

- Users don’t have to watch for fraud
- LP gets L2 capital faster - as quick as an L1-to-L2 message rather than waiting for the fraud period in SAFE to expire

**Cons vs SAFE:**

- Slightly more expensive on L1 as an L1-to-L2 message needs to be sent
- Only works in the rollup->mainnet case, not the rollup->rollup case

---

**Mike** (2022-02-07):

[@yahgwai](/u/yahgwai) That’s a very valuable insight! An interesting exercise would be to implement and benchmark rollup-specific SAFE (rSAFE). With rSAFE, the simplifications are:

1. One timeout instead of two. In SAFE, AuthWindow and SafetyWindow are necessary. rSAFE only needs an L1ApprovalWindow (aka inactivity timeout).
2. trustedAmount and trustedNonce can be removed, simplifying logic in from.sol contract.
3. As you point out, fraud mechanism can be removed in rSAFE.

With regard to SAFE fees, this is a great question. For an LP, the total cost of processing a batch is `2 * FromChain transaction cost + ToChain transaction cost`. One approach is to evenly split the batch cost between all swaps in a batch. Or a swap can be charged some portion of the batch cost based on the ratio of the amount swapped to total batch amount. The LP also charges a fee for the service. The total amount the customer receives on the `ToChain` is `swap amount - share of batch cost - service fee`.

One option is to introduce user-driven fees. A customer would set the maximum that the swap will pay (for `share of batch cost + service fee`). The LP can then skip swaps that are underpriced. Note that SAFE currently does not allow LP to skip swaps, but this feature can be added.

Another option is for LP to set a static fee that can be periodically adjusted. This fee can be based on batch sizes over the past day/week/month. Since SAFE is so much cheaper than non-batched swap technologies, it is likely that, at first, the LP can overcharge customers for swaps while remaining cheaper than alternatives. Over time, as the LP establishes a history of swap volume, the LP can set fees that are more inline with cost of running the service + fixed service fee.

---

**yahgwai** (2022-02-08):

Yeah, I think the user-driven fees (although they need to be guided by the LP) or a static fee would be best. The users will want to have a quote for the fee before they deposit into the L2 contract, because they’ll want to compare between different fast exit providers.

Whilst SAFE may be cheaper than non-batched swaps, it’s possible that there’ll be multiple LPs running the SAFE protocol and trying to compete (using fee price and latency) with each other for users.

---

**Mike** (2022-02-08):

Completely agreed with the points above! The goal of SAFE is to minimize customer costs, so creating a predictable and competitive fee structure is important research. I would definitely love to hear any and all ideas!

---

**kurtz121** (2022-02-09):

Hey Mike, love the cost-effective innovation this cross-chain protocol brings. It’s much needed in the space right now.

Just want to flag that the SAFE abbreviation might cause confusion for both users and developers in the multi-chain ecosystem - where 10+ chains are using the ‘Gnosis Safe’ as the account standard for holding their assets collectively. I’m part of team there and we also plan to drop the ‘Gnosis’ from the name completely and rename to the Safe protocol. Would be great to discuss how we can minimise user / dev confusion when the timings right in your research.

---

**Mike** (2022-02-09):

[@kurtz121](/u/kurtz121) Thanks for flagging the name conflict! Gnosis Safe is a well established technology with a great track record. We’ll brainstorm a new name for our research.

