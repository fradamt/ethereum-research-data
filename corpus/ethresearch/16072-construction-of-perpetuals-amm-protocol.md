---
source: ethresearch
topic_id: 16072
title: Construction of Perpetuals AMM Protocol
author: Zergity
date: "2023-07-08"
category: Decentralized exchanges
tags: [short-selling]
url: https://ethresear.ch/t/construction-of-perpetuals-amm-protocol/16072
views: 1303
likes: 2
posts_count: 1
---

# Construction of Perpetuals AMM Protocol

Following up on this [old discussion](https://ethresear.ch/t/token-sales-and-shorting/376), we propose a construction of leverage perpetual AMM liquidity pools using an asymptotic power curve pair.

[![Asymptotic Power Curves](https://ethresear.ch/uploads/default/optimized/2X/2/2339a946214d04e9284d0a512aebf95b51c2bebe_2_494x375.png)Asymptotic Power Curves3840×2912 382 KB](https://ethresear.ch/uploads/default/2339a946214d04e9284d0a512aebf95b51c2bebe)

Necessary differences from conventional unique-position perpetual exchanges:

- payoff function is compound leverage {P\over{M}}^K instead of constant leverage M+K\times(P-M)
- smooth Auto-Deleverage curve instead of manual ADL cutoff.

## Derivative Payoff Functions

At any time or market state, the pool reserve is split between 3 sides: r_A, r_B and r_C. With `P` as the index price feed from an external oracle and `M` is a constant mark price selected by a pool, we have: x = {P\over M}

Long payoff:

r_A=\begin{cases}
    ax^K                    &\quad\text{for }ax^K\le{R\over 2} \\
    R-\dfrac{R^2}{4ax^K}    &\quad\text{otherwise}
\end{cases}

Short payoff:

r_B=\begin{cases}
    bx^{-K}                 &\quad\text{for }bx^{-K}\le{R\over 2} \\
    R-\dfrac{R^2}{4bx^{-K}} &\quad\text{otherwise}
\end{cases}

LP payoff:

r_C = R - r_A - r_B

## State Transition

A pool state is represented by a 3-tuple ⟨R,α,β⟩, and it can be changed by user transactions.

[![image](https://ethresear.ch/uploads/default/optimized/2X/6/6e9586b4a5313c205449a0314b466685dc8da0ef_2_300x375.png)image2006×2506 203 KB](https://ethresear.ch/uploads/default/6e9586b4a5313c205449a0314b466685dc8da0ef)[![image](https://ethresear.ch/uploads/default/optimized/2X/d/d2fcaeeb77baaf3339cd10d5f3f5846bf2677e89_2_293x375.png)image1998×2554 207 KB](https://ethresear.ch/uploads/default/d2fcaeeb77baaf3339cd10d5f3f5846bf2677e89)

State transition can change the curves which affect the effective leverage of its derivative tokens but can not change the value of other existing “positions” in the pool.

## Paper

In this [whitepaper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4581048), our analysis demonstrates that, when properly initialized, the derivative tokens are optimally exposed to both sides of power leverages, and the market provides infinite liquidity in all market conditions, rendering it everlasting.
