---
source: ethresearch
topic_id: 19323
title: Mining attacks on PoRA (Proof of Random Access)
author: snjax
date: "2024-04-17"
category: Layer 2
tags: []
url: https://ethresear.ch/t/mining-attacks-on-pora-proof-of-random-access/19323
views: 3659
likes: 0
posts_count: 9
---

# Mining attacks on PoRA (Proof of Random Access)

## Abstract

This article analyzes the security of [Proof of Random Access (PoRA)](https://file.w3q.w3q-g.w3link.io/0x67d0481cc9c2e9dad2987e58a365aae977dcb8da/dynamic_data_sharding_0_1_6.pdf) consensus mechanism against potential mining attacks. The focus is on two main attack vectors: the shrink attack, where an attacker uses cheaper or smaller storage devices with the same throughput to gain an economic advantage, and the Moore attack, where an attacker leverages advancements in technology to increase throughput while maintaining the same cost. The article examines these attacks under both unlimited and limited mining throughput scenarios and provides mathematical analysis to determine the conditions under which the attacks could be economically viable for miners.

## Security model

In our security model, we consider an attacker who aims to optimize their mining procedure to gain an economic advantage over honest miners. The attacker can employ various strategies to achieve this goal:

1. Equipment replacement: The attacker may replace their storage equipment with more efficient or cost-effective alternatives. This strategy allows the attacker to maintain or increase their mining performance while reducing costs.
2. Partial fraction mining: The attacker can utilize a portion of their storage space and throughput for one client while using the remaining resources for another client. This allows the attacker to optimize their resource allocation and potentially gain an advantage by serving multiple clients simultaneously.

We will analyze two specific attack vectors:

1. Shrink attack: In this attack, the attacker replaces their storage device with a cheaper one that offers the same performance. For example, an attacker might replace a more expensive 1TiB NVMe drive with a cheaper 1TB drive that has the same throughput. This allows the attacker to reduce their storage costs while maintaining their mining performance. The key idea behind the shrink attack is that the attacker can take advantage of the fact that the consensus mechanism may not distinguish between storage devices of different sizes as long as they offer the same throughput.
2. Moore attack: This attack involves the attacker replacing their storage equipment with a newer, more advanced version that offers better performance at the same cost. For example, an attacker might replace a gen 4 storage device with a gen 5 device that has twice the throughput at the same cost. This allows the attacker to increase their mining performance without incurring additional expenses.

It is important to note that the Proof of Random Access (PoRA) consensus mechanism is well-scalable, meaning that there is no single machine limitation. This scalability allows for the possibility of using RAM rigs on tiny devices, such as single-board computers or even smartphones, to participate in the mining process. The absence of a single machine limitation opens up new opportunities for attackers to optimize their mining setups and potentially gain an advantage over honest miners.

Furthermore, the ability to perform partial fraction mining, where an attacker can allocate a portion of their storage space and throughput to one client while using the remaining resources for another client, adds another layer of complexity to the security model. This flexibility in resource allocation allows attackers to optimize their mining strategies and potentially gain an edge by serving multiple clients simultaneously.

Throughout the following sections, we will examine these attack vectors in detail, considering both unlimited and limited mining throughput scenarios. Our analysis will focus on determining the conditions under which these attacks could be economically viable for miners, and we will provide mathematical derivations to support our findings

## Shrink attack

In the following sections, we consider three different attacks. The first attack assumes that the mining throughput is not limited and shows how in this case the adversary can gain advantage over honest miners by using a different hardware configuration. In the follwing two attacks, we assume that the mining throughput was limited to mitigate the first attack, but we show that new issues arise: adversary can be economically incentivised to drop some part of the stored file, and perform Moore attack using more efficient hardware than that of honest miners.

In our costs analyses we make a few reasonable assumptions about the relationship between the costs and make conservative estimates of adversary advantage.

### Unlimited throughput: achieving advantage over honest miners

In this scenario, we consider the case where an attacker reduces the size of their memory module to gain an economic advantage. We make a pessimistic assumption that if the memory size is reduced by half, the maintenance cost (energy consumption) and throughput will remain the same, while the cost will be reduced by half. In reality, the energy consumption would likely be lower, but this assumption can only make our analysis more conservative.

To compare the cost efficiency of the attacker and the reference miner, we normalize the values by the cost and present them in the following table:

|  | Cost | Maintenance | Throughput |
| --- | --- | --- | --- |
| reference | 1 | A | 1 |
| attacker | 1 | \chi A | \chi |

- The reference miner’s cost of purchasing one unit of hardware is set to 1 as a baseline; this is without loss of generality as we normalize other values with respect to this, eliminating a free variable.
- A \sim 1 represents the maintenance cost (energy consumption) per time unit for the reference miner, which is assumed to be close to 1 for simplicity.
- The reference miner’s throughput is also normalized to 1.
- The attacker’s cost is set to 1, assuming that one unit of attacker’s hardware has the same cost as that of a reference miner. This is a conservative estimate, since one unit of attacker’s hardware is assumed to be less efficient than that of a reference miner.
- The attacker’s maintenance cost is \chi A, where \chi > 1 represents the throughput advantage of the attacker. This is because the attacker’s memory size is smaller, but the energy consumption per unit of memory remains the same.
- The attacker’s throughput is \chi, reflecting their advantage in terms of throughput per unit cost.

To compare the total cost efficiency, we calculate the throughput per unit of total cost (cost + maintenance) for both the reference miner and the attacker:

Reference miner: \frac{1}{1+A}

Attacker: \frac{\chi}{1+\chi A} = \frac{1}{1/\chi+A}

Since \chi > 1 when the attacker reduces the memory size, we can conclude that:

\frac{1}{1+A} < \frac{\chi}{1+\chi A} = \frac{1}{1/\chi+A}

This inequality demonstrates that the attacker has a better total cost efficiency compared to the reference miner.

Therefore, the original PoRA is not resistant to shrink attacks under unlimited mining throughput conditions. The only way to protect against this vulnerability is to limit the mining rewards, which would discourage attackers from exploiting this weakness.

### Limited throughput: not storing part of the file

In this scenario, we consider the case where the mining throughput is limited to an optimal value of 1, and we analyze the cost efficiency for an attacker who uses only a fraction p of their memory.

Let’s define the following variables:

- n: the number of random accesses
- q = 1 - p \ll 1, assuming qn \lesssim 1
- n_e: the efficient average number of accesses, given by n_e = (1-p^n)/(1-p) \approx (1 - \exp(-qn)) / q
- p_s: the success probability, given by p_s = p^n \approx \exp(-qn)
- \tau: the slowdown of sampling, given by \tau = n_e/(n \cdot p_s) = (\exp(qn)-1)/(qn)
- B: the sampling cost, assumed to be much smaller than 1 (B \ll 1) to ensure that the main cost of the algorithm is not CPU PoW

We can compare the reference miner and the attacker using the following table:

|  | Cost | Maintenance | Sampling | Throughput |
| --- | --- | --- | --- | --- |
| reference | 1 | A | B | 1 |
| attacker | 1 | \chi A | \chi B | \chi |
| attacker | p | \chi p A | \chi p B\tau | \chi p |

- The reference miner’s costs and throughput are normalized to 1.
- The attacker’s cost and throughput are scaled by \chi when using the full memory.
- When the attacker uses only a fraction p of their memory, their cost, maintenance, and throughput are scaled by p, while the sampling cost is scaled by p\tau to account for the slowdown in sampling.

For qn \lesssim 1, we have \tau \sim 1, which means B\tau \ll 1.

To consume all throughput, the attacker must satisfy the equation: \chi p = 1.

For efficient mining, the following condition must be met:

p\cdot (1 + \chi A) + B \tau < 1 + A + B

Simplifying this condition, we get:

p + (\tau - 1) B < 1

q > (\tau - 1) B \approx qnB/2

n B \lesssim 2

To estimate B, let’s consider the example of a Samsung 970 SSD with a throughput of 2GB/s, TDP of 6W, and a value size of 1MB. The hash efficiency for CPU is 30MH/J, and for ASIC, it is 3GH/J.

The additional TDP for sampling will be:

- For CPU: 2e9/1e6/30e6 = 6\text{e-5}W
- For ASIC: 2e9/1e6/3e9 = 6\text{e-7}W

By dividing these values by the TDP, we can roughly estimate B to be in the range of 1\text{e-}5 to 1\text{e-}7.

This means that n should be greater than 1\text{e}5 to 1\text{e}7 to make the shrink attack inefficient, which may not be practical in real-world scenarios.

When qn \lesssim 1, p can take any value. For example, with a storage size of 1TB, value size of 1MB, n=1\text{e}4, and B=1\text{e-}5, we get q=1\text{e-}4, which means that 100 MB of data could be forgotten while still providing economic benefits for the miner.

## Limited throughput: Moore attack

When considering the Moore attack, it’s important to note that miners will align their throughput to the limit imposed by the system. Let’s analyze the cost efficiency of the reference miner and the attacker in this scenario.

|  | Cost + Maintenance | Sampling | Throughput |
| --- | --- | --- | --- |
| reference | 1 | B | 1 |
| attacker | 1 | B | \chi |
| attacker | p | \theta Bp\tau | \theta \chi p |

- The reference miner’s cost, maintenance, and throughput are normalized to 1, with a sampling cost of B.
- After upgrading their hardware, the attacker’s cost and maintenance remain the same, but their throughput increases by a factor of \chi.
- When the attacker uses only a fraction p of their upgraded hardware, their sampling cost is scaled by \theta p\tau, where \theta is a throughput utilization parameter, and their throughput is scaled by \theta \chi p.

\theta represents the throughput utilization parameter, which indicates the fraction of the attacker’s upgraded throughput that they actually use. For example, if \theta = 0.8, the attacker is utilizing 80% of their upgraded throughput. This parameter allows us to model situations where the attacker may not be using their full upgraded capacity, either intentionally or due to technical limitations.

To consume all available throughput, the attacker must satisfy the equation: \theta \chi p = 1.

For efficient mining, the following condition must be met:

p \cdot (1 + \theta B \tau) < 1 + B

Expanding this condition using the approximations for \tau and p_s from the previous chapter, we get:

(1-q) (1 + \chi^{-1} B (1 + qn/2)) < 1 + B

Simplifying further:

\chi^{-1} nB/2 - 1 - B - \chi^{-1} qnB/2 < 0

\chi^{-1} pnB/2 < 1 + B

n B \lesssim 2 \chi

To find the optimal values for the arbitrary parameters \theta and p, we need to perform additional calculations. Taking the partial derivative of p \cdot (1 + \chi^{-1} B \tau) with respect to q, we get:

\partial_q (p \cdot (1 + \chi^{-1} B \tau)) \approx -(1 + \chi^{-1} B (1 + qn/2) + \chi^{-1} Bn/2 \cdot (1 + qn/3)) = \chi^{-1} Bn/2 - (1 + \chi^{-1} B) + \chi^{-1} B q n (n / 3 - 1/2) = 0

Solving for q, we get:

q = \frac{-Bn/2 + \chi + B}{B n (n / 3 - 1/2)} > 0

This result suggests that n should be greater than 1\text{e}5 to 1\text{e}7 to make the Moore attack inefficient.

For example, consider a storage size of 1TB, value size of 1MB, n=1\text{e}4, B=1\text{e-}5, and \chi=2. Plugging these values into the equation for q, we get q=0.005, which means that 5GB of data could be forgotten while still providing economic benefits for the attacker.

## RAM rig

In the original PoRA paper, the authors compare the performance of a Samsung 970 EVO NVMe SSD and 256GB DDR4-3200 RAM. Based on the calculations in the previous sections, we arrive at a counterintuitive conclusion: when there are no throughput limitations, only the throughput matters, not the size of the storage. To further illustrate this point, let’s compare the efficiency of a Crucial T705 1TB NVMe SSD and Crucial 8GB DDR5-4800 RAM.

|  | Cost (USD) | TDP (W) | Throughput (GB/S) |
| --- | --- | --- | --- |
| NVMe | 188 | 15 | 13.7 |
| DDR5 | 25 | 10 | 72 |

The table above compares the cost, thermal design power (TDP), and throughput of the two storage devices. The NVMe SSD has a higher cost and TDP but a lower throughput compared to the DDR5 RAM.

To calculate the cost efficiency of each device, we need to consider the maintenance cost and the amortization of the equipment over its lifetime. Let’s assume that the maintenance cost for 1W of power is about 4.4 USD per year and that the equipment is amortized over 4 years.

For the NVMe SSD, the cost per 1 GB/s of throughput per year is:

(188/4 + 15*4.4) / 13.7 = 8.25 USD

For the DDR5 RAM, the cost per 1 GB/s of throughput per year is:

(25/4 + 10*4.4) / 72 = 0.70 USD

The results show that the DDR5 RAM is significantly more cost-efficient than the NVMe SSD when considering the cost per 1 GB/s of throughput per year. This finding supports the idea that, in the absence of throughput limitations, using high-throughput RAM can be more economically viable for mining than using NVMe SSDs, despite the difference in storage capacity.

## Conclusion

The analysis of the shrink and Moore attacks on the PoRA consensus mechanism highlights potential vulnerabilities in the system. The article demonstrates that without proper limitations on mining rewards and a sufficiently high number of random accesses, attackers could gain economic benefits by using cheaper, smaller storage devices or leveraging advancements in technology to increase throughput. To mitigate these risks, the PoRA mechanism should be designed with appropriate parameters, such as limiting mining rewards and ensuring a high number of random accesses. Additionally, the comparison between NVMe storage and RAM suggests that RAM-based mining rigs could pose a significant threat to the security of the system, as they are more cost-effective per unit of throughput.

## Further research

We are planning to publish soon an article with green (no PoW inside) proofs of storage, based on statistics, economics, and zkSNARK cryptography, suitable for our decentralized storage research, available at:

- Blockchain Sharded Storage: Web2 Costs and Web3 Security with Shamir Secret Sharing
- Minimal fully recursive zkDA rollup with sharded storage

## Links

- Qi Zhou. Decentralized Storage on Large Dynamic Datasets with Applications for Large Decentralized KV Store.

## Replies

**qizhou** (2024-04-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/snjax/48/2945_2.png) snjax:

> For efficient mining, the following condition must be met:
>
>
> p\cdot (1 + \chi A) + B \tau  To consume all throughput, the attacker must satisfy the equation: \chi p = 1

For the limited throughput case, our design is not to limit the device throughput but to limit the rate of success of the candidates.  One implementation to put this constraint is to limit the nonce range of the sampling.  An implementation can be found here [storage-contracts-v1/contracts/StorageContract.sol at f1c9c17ef16b59c0495388672f11797eeec7848a · ethstorage/storage-contracts-v1 · GitHub](https://github.com/ethstorage/storage-contracts-v1/blob/f1c9c17ef16b59c0495388672f11797eeec7848a/contracts/StorageContract.sol#L216)

---

**snjax** (2024-04-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/qizhou/48/1953_2.png) qizhou:

> Should the objective of efficiency analysis be
>
>
> the cost of a successful random-sampling candidate of reference > the cost of a successful random-sampling candidate of attack?

We take into account not only random sampling costs but all costs, including electricity and equipment amortization. So, here we overview the case when the attacker’s costs are lower than reference costs.

![](https://ethresear.ch/user_avatar/ethresear.ch/qizhou/48/1953_2.png) qizhou:

> n_a = \sum_{i=1}^{n} 1/p^n

Yes. And it exactly equals n \tau.

I think sampling is not related to the storage device because you can just keep on CPU miner, that everything with offset 0.9 and more is not ok and brute force the suitable nonce (with no storage utilization at this step). \chi in my note is related to a storage device (in Shrink attack) and storage with CPU (in Moore attack).

In case you have no throughput limits per miner (= reward is a linear function on throughput), the best strategy is:

- store all data honestly
- The bottleneck is the bus. so, the best miner is a cluster of small devices, for example with 8gb DDR5 RAM. The cluster can compute hashes in parallel and utilize the bus with the cheapest devices with a lot of throughput (but minimal storage, it does not matter, just buy more devices to store everything). Also maybe GPU is more efficient than RAM, but I have not checked it.

So the issue, in this case, is not that miners will forget something, but the usage of the cluster of tiny devices, optimized for throughput but unoptimized for storage, which increases the price of the storage for end users.

![](https://ethresear.ch/user_avatar/ethresear.ch/qizhou/48/1953_2.png) qizhou:

> For the limited throughput case, our design is not to limit the device throughput but to limit the rate of success of the candidates.

Limiting the nonce is not limiting the throughput, it is just scale recalibration. I mean, limiting the throughput means implementing things with which two x GB/s miners will receive more reward than one 2x GB/s miner. If you do not implement limiting the throughput, the issue is only RAM or GPU cluster, which is suboptimal for storage, but it will maintain 100% of data.

![](https://ethresear.ch/user_avatar/ethresear.ch/qizhou/48/1953_2.png) qizhou:

> attack 3	2560	1	8/16	5120

64 RAMs have 64 times more throughput than single RAM because it will be maintained on 64 separate tiny machines.

---

**qizhou** (2024-04-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/snjax/48/2945_2.png) snjax:

> Limiting the nonce is not limiting the throughput, it is just scale recalibration. I mean, limiting the throughput means implementing things with which two xxx GB/s miners will receive more reward than one 2x2x2x GB/s miner. If you do not implement limiting the throughput, the issue is only RAM or GPU cluster, which is suboptimal for storage, but it will maintain 100% of data.

I am not sure what is the definition of **scale recalibration**.  In fact, the rate-limiting approach in EthStorage will allow up to 1M (2^20) nonces per Ethereum block.  Given n = 2 and sampling size = 4K, this essentially limits the throughput of a device to 1M * n * 4K = 8GB in 12s (Ethereum block time).  That said, any storage device with a throughput 8GB/12 = 682MB/s can achieve the full hash rate, however, a **device with a higher rate (e.g., memory) will be capped by this rate**.  (Unless the device can encode the data at 682MB/s at a much lower cost compared to storage. Such attack can be addressed by using an expensive SNARK-friendly encoding function).

![](https://ethresear.ch/user_avatar/ethresear.ch/snjax/48/2945_2.png) snjax:

> We take into account not only random sampling costs but all costs, including electricity and equipment amortization. So, here we overview the case when the attacker’s costs are lower than reference costs.

I guess we need to clarify the definition here.  Here, a **successful random-sampling candidate** is computed by fully sampling n random location, computing the sampled data, and returning a hash that compares with the difficulty parameter.  If any random location is not stored by the node, we cannot get such a candidate and the previous random accesses (sampling) will be wasted.

The cost per candidate will contain both amortized device cost (both storage device and sampling device) and the electricity cost per candidate.  This is similar to Bitcoin mining.

---

**snjax** (2024-04-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/qizhou/48/1953_2.png) qizhou:

> The cost per candidate will contain both amortized device cost (both storage device and sampling device) and the electricity cost per candidate. This is similar to Bitcoin mining.

For small nonces limit (for example, 2^{20} per Ethereum block) sampling device is not a bottleneck, and costs for \sim100 KH/s will be negligible less than storing costs. If for some cases we found, that the sampling is failed, we just break the process for this nonce and do not consume the throughput.

![](https://ethresear.ch/user_avatar/ethresear.ch/qizhou/48/1953_2.png) qizhou:

> I am not sure what is the definition of scale recalibration. In fact, the rate-limiting approach in EthStorage will allow up to 1M (2^20) nonces per Ethereum block.

I see, you limit the number of samples per block by the nonce on the solidity contract level. I have not found this constraint in the paper, but it changes the algorithm, making it more Filecoin-like.

If we limit nonce by m with difficulty d, the probability to get a reward per block will be:

p_r=1 - (1-p_s/d)^m \approx 1 - \exp(-p_s m /d)

To make any q>0 economically inefficient, we need \partial_q p_r |_{q=0} < -1 .

\partial_q p_r |_{q=0}  = -n \cdot m/d \cdot \exp(-m/d) < -1.

So, \theta \exp(-\theta) > 1/n, where \theta = m/d

![image](data:image/gif;base64,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)

If \theta \sim 1 and n>10, it’s enough to make q>0 economically inefficient.

But there are no lower limits on throughput, if m is small enough, HDD mining is possible, and it is more like Filecoin, not Bitcoin.

---

**qizhou** (2024-04-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/snjax/48/2945_2.png) snjax:

> I see, you limit the number of samples per block by the nonce on the solidity contract level. I have not found this constraint in the paper, but it changes the algorithm, making it more Filecoin-like.

No matter whether it likes the challenge-response protocol of Filecoin or PoRA of Arweave, the key goal  is to achieve

an **efficient** on-chain distributor to reward the storage nodes by

 \frac{\text{the number of replicas of the node}}{\text{total number of replicas in the network}}

where the replicas can be dynamic over time, and the data in the replicas can be slowly changed.

For this goal, the challenge-response protocol of Filecoin has

- reward each replica in exact 1/r per challenge-response window (30 mins), where r is number of replicas in the network
- the communication cost is O(r) per challenge-response window
- the minimum change unit is 32GB (sector size in Filecoin), which is unfriendly for dynamic storage (e.g., KV-store) with a much smaller value size

The design of EthStorage uses limited throughput of PoRA or data-availability sampling over time (DASoT) such that

- reward each replica 1/r statistically over time
- the communication cost is O(1) per target proof-interval (e.g., our testnet is about 3 hours) no matter what r is
- the minimum change unit is 128KB (EIP-4844 BLOB size), which is friendly for dynamic storage like KV-store.

So I would say the limited throughput of PoRA harvests the benefits of both the challenge-response protocol of Filecoin (exact per replica reward) and PoRA (efficient in O(1) communication cost)).  Note that the latest version of Arweave also uses a limited throughput of PoRA ([see](https://2-6-spec.arweave.dev/)).

![](https://ethresear.ch/user_avatar/ethresear.ch/snjax/48/2945_2.png) snjax:

> If we limit nonce by mmm with difficulty ddd, the probability to get a reward per block will be:
>
>
> p_r=1 - (1-p_s/d)^m \approx 1 - \exp(-p_s m /d)pr=1−(1−ps/d)m≈1−exp(−psm/d)p_r=1 - (1-p_s/d)^m \approx 1 - \exp(-p_s m /d)
>
>
> To make any q>0q>0q>0 economically inefficient, we need \partial_q p_r |{q=0}
>
> \partial_q p_r |{q=0} = -n \cdot m/d \cdot \exp(-m/d)
>
> So, \theta \exp(-\theta) > 1/nθexp(−θ)>1/n\theta \exp(-\theta) > 1/n, where \theta = m/dθ=m/d\theta = m/d
>
>
> [image]
>
>
> If \theta \sim 1θ∼1\theta \sim 1 and n>10n>10n>10, it’s enough to make q>0q>0q>0 economically inefficient.
>
>
> But there are no lower limits on throughput, if mmm is small enough, HDD mining is possible, and it is more like Filecoin, not Bitcoin.

I have not quite followed the analysis here. In our design, m/d << 1 with m = 2^{20}, and d \approx r * 900 * 2^{20}, where 900 * 12 = 3 hours is the target proof interval.  In our [testnet](https://grafana.ethstorage.io/d/es-node-mining-state-sepolia/ethstorage-monitoring-sepolia?orgId=2&refresh=5m) on Ethereum Sepolia, d = 120e9, where r \approx 127.

---

**qizhou** (2024-04-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/snjax/48/2945_2.png) snjax:

> HDD mining is possible

HDD is possible with a proper access pattern and data organization on a disk (e.g., using a random offset of a sequential read).  Further, we may allow the algorithm to support detecting both HDD and SSD storage and distribute different rewards to them.

---

**snjax** (2024-04-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/qizhou/48/1953_2.png) qizhou:

> I have not quite followed the analysis here. In our design, m/d  So I would say the limited throughput of PoRA harvests the benefits of both the challenge-response protocol of Filecoin (exact per replica reward) and PoRA (efficient in O(1) communication cost)).

zkSNARKs can solve this issue also. What do you think about the following alternative:

1. Rare challenges
2. Each challenge should be replied or the miner will be slashed

The issue is how to force miners to maintain the infrastructure during market stress. For example, if the protocol token price falls 10 times during a day, it should not lead to a spiral of death, when the miners instantly switch to competitors and deal damage to the network, because they lose short-term economic incentives.

Slashing is working as a dollar auction in this case.

---

**qizhou** (2024-04-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/snjax/48/2945_2.png) snjax:

> zkSNARKs can solve this issue also. What do you think about the following alternative:
>
>
> Rare challenges
> Each challenge should be replied or the miner will be slashed
>
>
> The issue is how to force miners to maintain the infrastructure during market stress. For example, if the protocol token price falls 10 times during a day, it should not lead to a spiral of death, when the miners instantly switch to competitors and deal damage to the network, because they lose short-term economic incentives.
>
>
> Slashing is working as a dollar auction in this case.

That is why we use ETH as the protocol token so that the sudden price drop should not be the problem.

In the long term, any significant price drop would hurt the system even like BTC / ETH.

One main cost of challenge-response is the communication cost O(r), which is not scaled if r is large or the on-chain verification is expensive (e.g., when ETH is congested).

