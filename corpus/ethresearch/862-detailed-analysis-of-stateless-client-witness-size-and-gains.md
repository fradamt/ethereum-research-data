---
source: ethresearch
topic_id: 862
title: Detailed analysis of stateless client witness size, and gains from batching and multi-state roots
author: vbuterin
date: "2018-01-23"
category: Sharding
tags: [stateless]
url: https://ethresear.ch/t/detailed-analysis-of-stateless-client-witness-size-and-gains-from-batching-and-multi-state-roots/862
views: 4907
likes: 3
posts_count: 10
---

# Detailed analysis of stateless client witness size, and gains from batching and multi-state roots

Let us consider simple ETH transfers from A to B as a base case. Suppose that we want each shard to have the same transactions-per-second as the mainnet. On the mainnet, the gas limit is 8m, and a simple transaction costs 21000 gas, so we have a maximum 380 transactions per block. In a shard, a period lasts for 5 main chain blocks, so shard blocks may have 1900 transactions. Each transaction requires a witness for the sender account and the recipient account, including a Merkle branch for both, as well as the code for both.

Let us assume that each shard has as many accounts as the current mainnet - roughly 24m, which we can round up to 2^25 for simplicity, so we will assume that a Merkle branch has ~32 bytes * 25 * 1.1 for overhead = 880 bytes (this is already assuming the Merkle branches are stored in a format that does not duplicate data by fully including the hash of an object which already appears elsewhere in the data; standard binary Merkle trees do this implicitly, but it can be done for Merkle Patricia trees as well). Let’s assume that the code of an account is 200 bytes long.

Naively, we might calculate the witness size as 1080 * 2 * 1900 = 4.10 MB, and the base transaction size would be ~110 * 1900 = 209 kB, so this bumps up the size of a block by about 20x. But we can already do a simple optimization: merge the Merkle branches for the different addresses. Between 3800 addresses, chances are that the top 11 rows of the tree will be fully used up, so we can replace 32 * 1.1 * 25 * 3800 with 32 * 1.1 * 14 * 3800 + 2047: savings of about 1.5 MB.

We can make a clearer estimate with this code:

```python
import random

def calctot(length, branches):
    o = [0] * (2 ** length + 1)
    for i in range(branches):
        pos = 1
        for j in range(length):
            o[pos] = 1
            pos = pos * 2 + random.randrange(2)
    return int(len([x for x in o if x == 1]) * 35.2)
```

This gives ~1.76 MB for 3800 branches, and adding account code gives 2.5 MB, confirming the rough estimate.

Now, let us look at the multi-state root proposal. Instead of having a single state root, each shard might have 256 state roots, one for accounts starting with 0x00, one for accounts starting with 0x01, etc. In a naive model, each sub-shard would only have 2^17 accounts, so the data size would go down to 3.0 MB (1 MB savings). But what happens if you take into account witness merging? Each sub-state root would only have ~14.85 accounts, so total data consumption (`sum([m.calctot(17, 14 if random.random() > 0.85 else 15) for i in range(256)])` as an approximation) gives ~1.76 MB. In short, multi-state roots give negligible additional savings.

This is explained by the fact that, in blocks with 3800 transactions, the top 8 rows of the Merkle tree are referenced so many times that they are there basically there “for free”.

We could make further 25% gains by reducing the Merkle tree width from 32 bytes to 24 bytes; this would cut us down to ~2.08 MB. We could also save more for simple sends by adding an opcode that sends money without running the destination account’s code, so we would only need the sender account’s code for each transaction and not the destination’s; this saves 200 * 1900 = 380 kb; in total, this gets us down to 1.7 MB witness size - only a 9x increase in bandwidth from statelessness.

The above is a maximum-entropy scenario, and pretty close to worst case. In the average case, we can get even larger gains. If a single address sends or receives multiple transactions (eg. because it’s making many sends, or because it’s a popular contract), then the entire branch for that address would be reused many times. The protocol could also have a protocol rule where publishing contracts in some address range (eg. 0x0000) is much more expensive in terms of initial setup cost, but then cheaper to include as a witness; this would encourage reuse of this range for some more limited set of popular contracts.

In the longer term, multisig transactions, post-quantum signatures, ringsigs, range proofs, SNARKs, etc, are both more space-intensive on the transaction side, but not on the witness size, so the bandwidth increase from statelessness will not be even as large as 9x.

Also, most contracts as currently written have a fairly large size, often significantly larger than 1 KB. If we want to make inroads on reducing witness size there, then there is basically only one logical path: breaking up the code into functions and making it into a Merkle tree; though even there, many complex transactions will execute functions that are a few hundred bytes long or even longer.

## Replies

**tawarien** (2018-01-23):

As the reduction from 32 to 24 Bytes was mentioned here XMSS (eXtended Merkle signature scheme)  popped into my head (it is based on Merkle Trees). It uses a construction that does allow to use hash functions that only have to be second preimage resistance instead of collision resistance and thus you only need half the bits for the same security margin (as the birthday paradox does not apply). But I’m not sure if this technique is generally applicable or if it roots in something specific in the way Merkle trees are used for signatures schemes (but I do not think so, but further research would be necessary). Sadly the Gover algorithm can still be applied to second preimage resistance, so if post-quantum security is a required property then this is no option.

The way how they do this is that they have 2 public but random Bitmasks per level of the tree and before hashing two nodes together to build a new one, one mask is XORed with the left child and the other with the Right child.

---

**vbuterin** (2018-01-23):

Unfortunately the way that hashes are used in ethereum (and realistically other blockchains), where hash(x) is liberally used as a stand-in for (x) in dozens of places, means that even hash collisions break its security. Hence, at 24 bytes the security would drop to 2^96; but this may be acceptable given that we already accept a 2^80 cost for address collisions, though you could argue that address collisions are much less bad than the whole system breaking. Perhaps if we want future proofness anything less than the full 32 really is too risky.

---

**JustinDrake** (2018-01-24):

I have extended your model with two functions:

- collation_witness_overhead() estimates the overhead of a single collation witness parametrised by multitries_exponent
- total_sync_overhead() estimates the total shard sync inbound overhead for a validator from a holistic perspective. I include:

the multi-roots
- collation witnesses for some number of “windback” periods
- the witnesses in the transactions for the single collation to be added to the VMC (this is a best case scenario; in practice I expect validators will have to download many more transactions than can fit in a single collation)

```python
def collation_witness_overhead(accounts_exponent, witnesses, multitries_exponent):
	floor = witnesses // (2 ** multitries_exponent)
	mantissa = float(witnesses) / (2 ** multitries_exponent) - floor
	return sum([calctot(accounts_exponent - multitries_exponent, floor if random.random() > mantissa else floor + 1) for i in range(2 ** multitries_exponent)])

def total_sync_overhead(accounts_exponent, witnesses, multitries_exponent, windback_periods):
	total = 32 * (2 ** multitries_exponent)

	for i in range(windback_periods):
		total += collation_witness_overhead(accounts_exponent, witnesses, multitries_exponent)

	return total + 32 * witnesses * (accounts_exponent - multitries_exponent)
```

The goal is to optimise `multitries_exponent` given the constraints:

- accounts_exponent = 25
- witnesses = 3800
- windback_periods = 4 (the same as LOOKAHEAD_PERIODS, although it could be set differently)

The optimal value given our model is `multitries_exponent = 15` yielding a collation witness overhead of 1.3 MB and a total sync overhead of 7.6 MB. While the model may need fixing to reflect real-world behaviour, the ballpark number seems about right. Certainly setting `multitries_exponent = 8` (to get 256 state roots) is suboptimal (it yields a total overhead of 9.1 MB).

Beyond merging Merkle paths and choosing an optimal value of `multitries_exponent`, I can see two optimisations:

1. When two trie nodes have the same parent node, the parent’s hash can be derived from the children and optimised away
2. Code can be deduplicated across accounts. I expect most accounts to use the exact same ECDSA template code, so the boilerplate code for that can be aggressively deduplicated across accounts.

---

**vbuterin** (2018-01-24):

OK, I admit I have not considered `multitries_exponent` values that are that large. At an exponent of 15, that’s an extra 1 MB of data that would need to be downloaded; though I suppose if it saves more than 1 MB of total downloading then it’s worth thinking about.

BTW my guess for average `windback_periods` would be something like 25, not 4. `windback_periods = 4` implies that it takes one period to evaluate a collation in one period, which basically means zero safety margin.

---

**JustinDrake** (2018-01-24):

Here’s my updated model. It yields an optimal value of `multitries_exponent = 16` for a total overhead of 32.4 MB with a windback of 25. When `multitries_exponent = 0` (a single trie) the total overhead is 47.1 MB, about 45% larger.

```python
import random

def calctot(length, branches):
    o = [0] * (2 ** length + 1)
    for i in range(branches):
        pos = 1
        for j in range(length):
            o[pos] = 1
            pos = pos * 2 + random.randrange(2)
    return int(len([x for x in o if x == 1]) * 35.2)

def collation_witness_overhead(accounts_exponent, witnesses, multitries_exponent):
	floor = witnesses // (2 ** multitries_exponent)
	mantissa = float(witnesses) / (2 ** multitries_exponent) - floor
	return sum([calctot(accounts_exponent - multitries_exponent, floor if random.random() > mantissa else floor + 1) for i in range(2 ** multitries_exponent)])

def total_sync_overhead(accounts_exponent, witnesses, multitries_exponent, windback_periods):
	# Download multi-trie roots
	total = 32 * (2 ** multitries_exponent)

	# Add windback collation witnesses
	total += windback_periods * collation_witness_overhead(accounts_exponent, witnesses, multitries_exponent)

	# Add transaction witnesses for collation to be produced
	return int(total + 32 * witnesses * (accounts_exponent - multitries_exponent))

for i in range(0, 21):
	print(i, total_sync_overhead(25, 3800, i, 25))
```

The output is

```auto
(0, 47113057)
(1, 47139339)
(2, 47047678)
(3, 46753706)
(4, 46707937)
(5, 46577024)
(6, 46537148)
(7, 46336871)
(8, 46099892)
(9, 46315959)
(10, 45780293)
(11, 45580611)
(12, 45412497)
(13, 42359944)
(14, 38336638)
(15, 35405376)
(16, 32437352)
(17, 32789404)
(18, 33064908)
(19, 37177291)
(20, 51062832)
```

---

**JustinDrake** (2018-01-24):

Other things to consider:

- For users and non-validating nodes the bandwidth to broadcast and gossip transactions is significantly reduced when multitries_exponent = 16 compared to multitries_exponent = 0 (transaction sizes are more than halved).
- Beyond the quantitative differences in total overhead, there are qualitative differences to consider, both of which favour multi-tries over just batching:

Critical path: For a validator the critical path to build a collation includes the previous collation plus recent transactions broadcasted after that previous collation. This means that the bandwidth savings are disproportionality important towards the tail end.
- Parallelism: Unlike collations and transactions, multi-trie roots can be downloaded in parallel from different nodes.

While downloading lots of multi-trie roots may seem unappealing, the incentives are stronger than presented because multi-trie roots are both not in the critical path and can be downloaded in parallel. So my gut feel is that, all things considered, the optimal value for `multitries_exponent` is likely 17 or 18.

---

**vbuterin** (2018-01-24):

If we’re going with this, I like 16 because it’s a clean “first two bytes of the address”; the difference between 16, 17 and 18 is likely small in any case.

---

**tawarien** (2018-02-14):

How would the added bandwidth and history bytes from the witnesses affect transaction gas cost?

I assume that costs for accessing contract code as well as storage slots would be reduced as they no longer have to go to disk.

Would this two balance each other out or would the stateless model have a significant impact on the gas costs?

---

**vbuterin** (2018-02-15):

There would be no gas cost component accounting for disk access cost, but there **would** be a gas cost component for the Merkle branch for whatever you’re accessing, and this gas cost may well be even larger.

