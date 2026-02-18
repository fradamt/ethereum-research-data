---
source: ethresearch
topic_id: 7043
title: Inactivity Penalty Quotient rationale and computation
author: hermanjunge
date: "2020-02-29"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/inactivity-penalty-quotient-rationale-and-computation/7043
views: 1240
likes: 0
posts_count: 2
---

# Inactivity Penalty Quotient rationale and computation

Looking to gain insight on the matter of the **inactivity penalty quotient**.

While the [Serenity Design Rationale](https://notes.ethereum.org/@vbuterin/rkhCgQteN) document states that

> With the current parametrization, if blocks stop being finalized, validators lose 1% of their deposits after 2.6 days, 10% after 8.4 days, and 50% after 21 days. This means for example that if 50% of validators drop offline, blocks will start finalizing again after 21 days.

If we examine the [current](https://github.com/ethereum/eth2.0-specs/blob/a14708afcb1728ecf309eea7546ac9261260e9f4/specs/phase0/beacon-chain.md#rewards-and-penalties) [parametrization](https://github.com/ethereum/eth2.0-specs/blob/a14708afcb1728ecf309eea7546ac9261260e9f4/specs/phase0/beacon-chain.md#rewards-and-penalties-1)  we have

```python
penalties[index] += Gwei(effective_balance * finality_delay // INACTIVITY_PENALTY_QUOTIENT)
```

with `INACTIVITY_PENALTY_QUOTIENT` = `2**25` (`33,554,432`).

Now, if we build and run a quick python script

```python
balance = 100.0

for i in range(4,4726):
    balance -= (i * balance) / 2**25
    print(str(i) + "\t" + str(balance))
```

our results are, for an initial balance of `100`

```auto
4   99.99998807907104
5   99.99997317791163
6   99.99995529652298

[snip]

4723    71.71416019772546
4724    71.70406383570766
4725    71.69396675817036
```

adjusting the exponent of `2` in the above script, with `2**23.94128` we get

```auto
[snip]

567 99.00533232662947
568 99.00184121683876
569 98.99834408404766

[snip]

1840    90.01886280962862
1841    90.00857450307387
1842    89.99828178458043

[snip]

4723    50.026236935763414
4724    50.01156578060706
4725    49.996895823295965
```

Which are *closer* to the statements in the rationale, namely, losing 1% at 2.6 days (568 epochs), 10% after 8.2 days (1841 epochs), and 50% after 21 days (4724 epochs).

So the **short question** is why **2**25** was chosen as the Inactivity Penalty Quotient instead of **2**24**. And the **long question** is about the methodology used to compute the coefficient .

---

For the latter, we tried an analytical approach and end up with the following equation to compute the exponent x:

Suppose we are looking for a value x such that if we apply B_i = B_{i-1}(1-\frac{i+4}{2^{x}}) we obtain that B_{4725} \approx 0.5B_0. In other words we want the balance B to be halved after 21 days, (4,725 epochs)

B\prod_{n=4}^{4725} (1-\frac{i}{2^{x}}) = 0.5B

Simplifying the product,

\prod_{n=4}^{4725} (1-\frac{i}{2^{x}}) = 1 - [\frac{4725 * 4726}{2}-6]\frac{1}{2^x}+...\approx1 - [\frac{4725 * 4726}{2}-6]\frac{1}{2^x}=1-\frac{11165169}{2^x}

Equaling to 0.5 and solving for x we have x=24.412. We can attribute the difference between this result and the ran experiment (23.94128) to the dismissed terms of the product.

## Replies

**hermanjunge** (2020-02-29):

Cross posted here https://github.com/ethereum/eth2.0-specs/issues/1633

