---
source: magicians
topic_id: 23067
title: "EIP-7904: Gas Cost Repricing to reflect computational complexity"
author: JacekGlen
date: "2025-03-05"
category: EIPs > EIPs core
tags: [evm, opcodes, gas, precompile]
url: https://ethereum-magicians.org/t/eip-7904-gas-cost-repricing-to-reflect-computational-complexity/23067
views: 464
likes: 6
posts_count: 9
---

# EIP-7904: Gas Cost Repricing to reflect computational complexity

Discussion topic for  [EIP-7904](https://github.com/ethereum/EIPs/pull/9454): Gas Cost Repricing to reflect computational complexity

This EIP revises the gas cost schedule for opcodes, precompiles, memory expansion, and data access, prioritizing computational complexity, while excluding network-related costs such as state persistence. The adjustments aim to enhance gas cost accuracy and rebalance the cost structure.

#### Update Log

- 2025-03-05: initial draft https://github.com/ethereum/EIPs/pull/9454

#### External Reviews

None as of 2025-03-05.

#### Outstanding Issues

None as of 2025-03-05.

## Replies

**pdobacz** (2025-04-10):

After quick scan of the proposal, one item caught my attention - opcodes DIV through MULMOD seem very modestly priced compared to rest of arithmetic. Did you ensure that the values of arguments were ~~non-zero~~ non-trivial (e.g. `y <= x` for DIV) when doing the measurements? I recall that these opcodes were consistently much more (eg. ~5 times for DIV, very roughly) costly to run than the ADD thought SUB ones, as [measured on the earlier stage of the project](https://github.com/imapp-pl/gas-cost-estimator/blob/master/docs/report_stage_ii.md#appendix-b-evm-opcodes-and-their-gas-cost-estimates) (see “`expensive_cost`” rows at the table bottom).

Also the proposed values align well with the ~~**zero**~~ **trivial** (e.g. `y <= x` for DIV) argument measurements of these DIV-MULMOD opcodes obtained earlier (top of that linked table), which makes me think that indeed ~~zero arguments might have been used~~ operations on non-trivial args might have been used.

(EDIT: apologies for confusion, I’ve meant trivial, not zero arguments, explained here and in reply below)

---

**JacekGlen** (2025-05-01):

The same approach was used for all arithmetic opcodes: first, to measure them with typical arguments and then with variable-length arguments. This allowed us to identify the worst-case scenarios. You can verify it by looking at the actual bytecodes used: [typical](https://github.com/imapp-pl/gas-cost-estimator/blob/master/src/stage3/pg_marginal_full5_c50_step5_shuffle.csv) and [variable-length](https://github.com/imapp-pl/gas-cost-estimator/blob/master/src/stage3/pg_arguments_arithmetic_c200_opc30.csv) accordingly. In any case, no zero arguments were ever used.

When looking at the more raw data in the [comparison spreadsheet](https://github.com/imapp-pl/gas-cost-estimator/blob/master/docs/reports/final_gas_schedule_comparison.csv), you can notice that indeed MUL/DIV is twice as expensive as ADD/SUB, and ADDMOD/MULMOD are 4 and 5 times more expensive. These results differ slightly from the original research for two reasons:

1. More clients have been taken into account, thus flattening the average
2. Many clients have improved execution performance a lot

The [final proposal](https://github.com/imapp-pl/gas-cost-estimator/blob/master/docs/gas-schedule-proposal.md#radical-gas-schedule-proposal) shows the fractional differences between ADD/SUB/MUL/DIV opcodes; still, after rescaling, they all end up with the gas cost of 1. Only ADDMOD and MULMOD have been repriced to 2 and 3, respectively.

In general, the rescale factor we used (`1/4.6 = 0.217391304`) flattens all basic opcodes, so their gas cost is 1, disregarding individual differences.

---

**JacekGlen** (2025-05-01):

I thought I can add this short summary to discuss the effects of EIP-7904.

This EIP is based on the research and proposal is evidence-based. It sets the balance between opcodes and precompiles to reflect true computational cost.

By using the `rescale factor` to flatten the gas cost, we cause two main effects:

1. The gas cost schedule is significantly simplified
2. The computations are cheaper compared to the storage costs

When thinking about the second point, we anticipate some effects on the network:

- Encouragement of Computationally Intensive Applications

It could make it more affordable to perform complex computations on-chain. This might enable new use cases, such as applications relying on cryptographic verifications (e.g., zero-knowledge proofs) or sophisticated smart contracts that were previously cost-prohibitive.
- Developers may have greater flexibility to design feature-rich contracts, potentially boosting innovation within the Ethereum ecosystem.
- It promotes computations over storage, opening doors to more storage-saving techniques

Efficiency in Gas Usage

- For existing smart contracts, the same computational tasks would require less gas, making transactions cheaper.
- This has a similar effect to EIPs increasing gas limit (e.g. EIP-7938)

Storage Costs as a Limiting Factor

- Since storage-related gas costs remain unchanged, operations like deploying large contracts or performing extensive state updates will retain their current expense. This design choice likely aims to prevent abuse of storage, a scarce resource on the blockchain, ensuring that the network’s storage capacity is not overwhelmed.

Uncertain Impact on Gas Prices

- Gas prices in Ethereum are driven by supply and demand. Lower computational costs might reduce gas consumption for certain tasks, potentially decreasing overall demand and gas fees. However, if reduced costs spur increased usage or more complex transactions, demand could rise, pushing gas prices higher. The net effect will depend on how developers and users adapt.

Also, this might have some potential, and unwanted, side effects:

- Increased computational load on nodes
- Risk of cheaper DoS attacks
- Increased smart contract complexity

Our analysis shows that those risks are sufficiently mitigated.

Additionally, the scope of the EIP changes the gas cost of most of the opcodes. This enforces the implementation of more flexible gas cost schedules, which might be beneficial in the future.

So, in conclusion, the effects of the EIP are largely positive, with the main downside being the effort of implementing it. This might vary significantly between clients. The question remains whether the perceived benefits outweigh the implementation costs.

---

**bbjubjub** (2025-05-01):

I am a bit concerned about ECPAIRING and the disparities between clients. As the graph on the report highlights, the geth and Erigon 2 implementations are comparatively quite slow. We must be sure that a slower client running on a reasonable machine is still able to get sufficient performance. As it stands, on my NUC with an i7-1360P which I run my nodes on, geth’s `BenchmarkPrecompiledBn256Pairing` benchmarks on the main branch go at around 60Mgas/sec. If we slash the gas cost of the precompile by ~5 as suggested, we can predict that the throughput would fall to 12Mgas/sec, which is worrying at current and planned gas limits. (I’m sure ethproofs will make some prover killers full of pairing checks so maybe we can reuse those ![:grin:](https://ethereum-magicians.org/images/emoji/twitter/grin.png?v=12))

Am I understanding things correctly? Do those numbers match what you are predicting?

With that being said, I know this benchmark somewhat and I believe it hasn’t moved much since EIP-1108 was implemented. There most likely exists a bn254 go implementation that is much faster than that. I would love to see this EIP go through because blocks full of Groth16 proofs are cool, I just want to flag this so it can be specifically addressed and we know that everything is safe.

---

**JacekGlen** (2025-05-02):

[@bbjubjub](/u/bbjubjub) You’re absolutely correct to highlight the performance disparities across clients, and your observations align with our data. As you’ve noted, Geth and Erigon rely on a less optimized implementation of the ECPAIRING algorithm, which can be up to ~5 times slower in extreme cases like ECPAIRING 317k (when compared to Nethermind, Besu, and Evmone).

So, what should happen if we see such a high discrepancy in implementation performance? We have the following options:

- Worst-case scenario:  Base the gas cost on the slowest implementation

Pros: Maximizes network security by ensuring all clients can keep up.
- Cons: Increases costs for contract callers and provides no incentive for clients to optimize their implementations.

Median approach:  Use the median performance across clients, filtering out outliers.

- Pros: Strikes a compromise, balancing security and cost for most cases.
- Cons: May leave slower clients vulnerable to throughput issues or attacks.

Average approach:  Average the performance across all clients.

- Pros: Reflects overall client performance.
- Cons: More sensitive to outliers, potentially skewing the gas cost unfairly.

Best-case scenario:  Set the gas cost based on the fastest implementation

- Pros: Minimizes costs for contract callers, ensures fair pricing.
- Cons: Risks network stability if slower clients dominate, until all implementations catch up.

We’ve calculated the proposed gas cost for ECPAIRING (and in fact all opcodes/precompiles) using the median approach. This method has been our standard, as it generally offers a reasonable compromise. We’ve detailed the reasoning in our paper, and for ECPAIRING specifically, the median ends up closer to the average anyway due to the distribution of the data. However, as you’ve highlighted, this still poses throughput challenges for slower clients, especially under higher gas limits.

Given this, should ECPAIRING be an exception? One potential solution is to delay updating its gas cost until all major clients achieve comparable performance levels. Worth discussing it further.

We should have highlighted this case more clearly in the EIP. I’ll add a note there to make sure it is not missed. Thanks for pointing this out!

I think ECPAIRING was the only case with such a high discrepancy between clients. But I’ll run some analysis again to make sure we didn’t miss anything.

---

**pdobacz** (2025-05-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jacekglen/48/11525_2.png) JacekGlen:

> In any case, no zero arguments were ever used.

Ouch, sorry, I miswrote in my post. It is not zero arguments being a potential problem, but `y >= x` arguments which may make DIV cheap and skew results. And I see in your typical bytecodes you’ve cited that DIV does indeed use `y = x = 3`. You also have the variable-length ones, but can you point me to the spot in the code showing how you account for `x > y` in the calculation of final proposed gas costs?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jacekglen/48/11525_2.png) JacekGlen:

> you can notice that indeed MUL/DIV is twice as expensive

Also maybe to clarify my original message and to zoom in on a particular case - my point is that cost of MUL is equal or larger than DIV. In the comparison spreadsheet many (majority) of EVM implementations have MUL more expensive to run than DIV, which is suspicious.

---

**weiihann** (2025-08-28):

Should `EXTCODESIZE` have a higher cost compared to other opcodes with `address_access_cost`? Referencing geth’s implementation, cold `EXTCODESIZE` results in 2 db reads, compared to cold `BALANCE` call which only results in 1 db read, but both of them have equal cost.

---

**JacekGlen** (2025-09-08):

Good point, but for this EIP, we consider warm access only. This was benchmarked and no significant difference was found for these opcodes.

