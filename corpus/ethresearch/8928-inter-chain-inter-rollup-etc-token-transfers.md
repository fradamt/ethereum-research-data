---
source: ethresearch
topic_id: 8928
title: Inter-chain/inter-rollup/etc token transfers
author: kladkogex
date: "2021-03-15"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/inter-chain-inter-rollup-etc-token-transfers/8928
views: 1834
likes: 0
posts_count: 5
---

# Inter-chain/inter-rollup/etc token transfers

Consider a set of decentralized solutions connected to ETH main net. It could be blockchains, rollups, or something else.

For each solution X  suppose there is a way to transfer tokens (say USDT) back and forth between the main net and X.  This means that there is a smart contract on the main net that freezes tokens on deposit, clones are printed on X and then burnt on exit.

Note, that in the worst case when X is hacked,  money lost is limited to what was deposited on X.

Now, lets suppose you have X, Y, Z etc. and you want to enable inter-solution token transfers.

Clearly, **you do not want to burn on X and print on Y**, since it couples the security. A hack in X breaks the entire system globally, not just the funds deposited on X.

Therefore, it seems that **the only satisfactory solution** is atomic swaps, where some interested parties keep funds (USDT) on all chains and help you quickly transfer. The interested parties assume the risk and get reimbursed by the fee.

The atomic swaps may be hash-locked or simply reputation-based (you could transfer in small chunks to minimize counterparty risk )

The question is, how to build an efficient market so that there are many parties (not just one) and the fees are dynamically changed (maybe in a curve-like style) so higher risk and higher demand lead to higher fees …

## Replies

**chris.whinfrey** (2021-03-17):

We originally faced this problem with [Hop protocol](https://ethresear.ch/t/hop-send-tokens-across-rollups/8581) but came up with a pretty simple solution.

We track the total number of tokens entering and exiting each scaling solution and require that the number of tokens that have exited does not exceed the number that have entered. This allows scaling solutions with weaker trust models to be supported while limiting the liability of any given solution to the participants of that solution.

This is possible for Hop because the settlement of all the tokens being minted and burned on each scaling solution happens through layer-1 and the layer-1 smart contract can track the balance of each scaling solution and enforce these rules.

---

**kladkogex** (2021-03-18):

Hey Chris,

Can you explain more?

How you track exited vs. entering? Wouldnt it require a main net transaction each time?

At SKALE we have a separate main-net deposit boxes for each SKALE chain.

Moving funds between 2 chains does seem to require main net transactions to

adjust the corresponding deposit balances …

That’s why it seems like using liquidity providers on each chain and atomic swaps is cheaper …

---

**chris.whinfrey** (2021-03-18):

> Moving funds between 2 chains does seem to require main net transactions to
> adjust the corresponding deposit balances

This is true. You can do this in a scalable way by aggregating many transfers on the origin chain and then sending them through layer-1 as a large batch. The data representing the batch contains:

1. A Merkle root of all of the transfers
2. The total amount of tokens being transferred in the batch

That way the balance adjustments on layer-1 can be done just once for each batch which can contain many transfers.

---

**kladkogex** (2021-03-26):

Chris -  I see …

This is pretty cool … You could essentially wait for some time and transfer them all in a batch … May be once a day …

The problem if a particular pair of chains does not have much transfers,  cost per transfer will grow …

