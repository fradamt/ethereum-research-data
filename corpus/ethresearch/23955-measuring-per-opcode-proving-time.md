---
source: ethresearch
topic_id: 23955
title: Measuring Per-Opcode Proving Time
author: linoscope
date: "2026-01-27"
category: Execution Layer Research
tags: [zk-roll-up, rollup, execution, real-time-block-proving]
url: https://ethresear.ch/t/measuring-per-opcode-proving-time/23955
views: 339
likes: 9
posts_count: 3
---

# Measuring Per-Opcode Proving Time

[![A picture of a prover proving blocks one opcode at a time](https://ethresear.ch/uploads/default/optimized/3X/d/0/d09cce60cfec40f23f6eb84e12a1a2355363ab63_2_690x460.jpeg)A picture of a prover proving blocks one opcode at a time1536×1024 208 KB](https://ethresear.ch/uploads/default/d09cce60cfec40f23f6eb84e12a1a2355363ab63)

By [Lin Oshitani](https://x.com/linoscope) ([Nethermind Research](https://www.nethermind.io/nethermind-research)).  Thanks to [Matteo](https://www.linkedin.com/in/matteolisotto/), [Ahmad](https://x.com/smartprogrammer), [Michal](https://x.com/mpfzajac), [Conor](https://x.com/ConorMcMenamin9),  [Gustavo](https://x.com/gusgonzalezs), [Daniel](https://x.com/realdantaik),  [David](https://github.com/davidtaikocha), Yuewang, and [Ignacio](https://x.com/ignaciohagopian) for the discussions and/or reviews, and thanks to [Musa](https://x.com/wisemrmusa) for the discussions and for helping run the benchmarks.

This work is funded by [Taiko](https://taiko.xyz/) as part of the [strategic Taiko<>Nethermind partnership](https://paragraph.com/@taiko-labs/taiko-x-nethermind-building-ethereum-aligned-based-rollup-infrastructure).

# TL;DR

What is each opcode’s isolated proving cost? To answer this question, we benchmark the per-gas proving time of individual EVM opcodes and precompiles in a multi-GPU setup, building on the EF’s zkEVM benchmarking tooling and the imapp team’s Gas Cost Estimator marginal method. We also evaluate whether zk cycles are a meaningful proxy for actual proving time using actual proving-time measurements.

# Introduction

As ZK rollups move toward further decentralization, both in terms of [rollup stages](https://medium.com/l2beat/introducing-stages-a-framework-to-evaluate-rollups-maturity-d290bb22befe) and in the decentralization of sequencers and provers, mitigating *prover-killer blocks* becomes critical for their security and economic sustainability. These adversarial blocks are constructed to maximize proving time while remaining within the EVM gas limit, [creating potential denial-of-service vectors](https://arxiv.org/abs/2509.17126) or rendering proving economically unviable. Moreover, as Ethereum L1 itself [moves toward ZK-based scaling](https://zkevm.ethereum.foundation/), it will face the same challenge.

Traditional EVM gas metering accounts only for execution costs such as CPU time, storage access, and state growth, but it fails to capture proving costs altogether. As a result, ZK rollups require additional safeguards. A leading approach is to explicitly meter proving costs and enforce block limits based on this metric. Building such mechanisms, however, requires accurate models of how individual operations contribute to overall proving time, precise enough to prevent adversarial blocks without overly harming usability.

To model proving time, we focus on the following core question: *how does each EVM opcode or precompile individually contribute to total proving time?* Concretely, ***if we add a given opcode or precompile that consumes an additional X gas, holding all else equal, how much additional proving time does it add?*** From this, we estimate the marginal proving time per unit of gas for each opcode or precompile.

Prior [zkEVM benchmarking efforts](https://eth-act.github.io/zkevm-benchmark-runs/benchmarks/) by the Ethereum Foundation provide valuable end-to-end measurements by constructing blocks densely filled with a specific opcode or precompile via a loop. This approach works well for identifying and analyzing operations with very high proving cost, where the cost of the target operation dominates overall proving time. However, because these benchmarks do not explicitly separate per-operation cost from the surrounding overhead (e.g., pushing arguments to the stack, popping return values, and control flow), they are less informative for lower-cost operations, where the surrounding code can significantly affect the measurement. As a result, they are insufficient for building a comprehensive model of proving time across all opcodes and precompiles.

To overcome this limitation, we adopt the *marginal* measurement approach from the imapp team’s [Gas Cost Estimator](https://github.com/imapp-pl/gas-cost-estimator/) project, which isolates the contribution of each opcode or precompile from surrounding overhead by creating test cases that vary only the target operation count while holding all other execution context constant. We then fit a linear regression and take the slope to estimate the proving time per unit of gas.

Our benchmark implementation is built on and made possible by the foundation of the Ethereum Foundation’s [zkEVM Benchmarking Workload](https://github.com/eth-act/zkevm-benchmark-workload) tooling. We created [a suite of custom execution-spec tests](https://github.com/linoscope/execution-specs/pull/1/changes) following the gas-cost-estimator’s marginal methodology, with extensions to better fit the ZK proving context (e.g., an amplification method to prevent fixed ZK proving setup overhead from dominating the measurements). These fixtures were then executed using a [custom fork](https://github.com/NethermindEth/ere/pull/1) of EF’s benchmarking tooling with multi-GPU support added for SP1.

Furthermore, we use the benchmarking results to evaluate whether zk cycles are a meaningful proxy for actual proving time using direct proving-time measurements. We find that the relationship between proving time and zk cycles varies widely across opcodes and precompiles, limiting the accuracy of zk cycle-based estimates.

# Key Results

*We present the results first; readers interested in assumptions and experimental setup can find details in the  [Methodology section](#methodology).*

In this section, we present the key results of the benchmarks, which were run in the following environment (for more details on the setup, see the methodology section below).:

- Prover: sp1-v5.2.3 (with sp1-cluster) and risc0-v3.0.4 (with RISC0_KECCAK_PO2=15 flag to prevent provers from crashing)
- GPUs: 4 x NVIDIA GeForce RTX 4090
- Execution Client: reth-v1.9.3

**Note:** Proving time depends heavily on the run configuration (e.g., prover flags and configurations, hardware/runtime settings, the condition of GPUs at the time of proving, etc.). As such, these results should be interpreted as configuration-specific measurements.

**Note:** These benchmarks were run without block header validation. Local testing suggests validation has little effect on most opcodes; LOG-related opcodes see a 4–5× increase, though they remain relatively cheap to prove.

## Proving Time per Gas

Below is the “proving time per gas” for each opcode/precompile in both SP1 and RISC0. This metric represents the additional proving time incurred by using 1 additional gas unit for a specific opcode or precompile. The R^2 value indicates the fit of the linear regression.

More detailed data (e.g., regression plot for each opcode) is hosted here: [SP1](https://nethermindeth.github.io/zkevm-benchmark-workload/marginal-gas-benchmark/sp1), [RISC0](https://nethermindeth.github.io/zkevm-benchmark-workload/marginal-gas-benchmark/risc0)

[![Proving Time per Gas](https://ethresear.ch/uploads/default/optimized/3X/2/d/2d939b8e4d6c1ea4992be2a51f1ecf0ce00ef1f2_2_258x500.jpeg)Proving Time per Gas1781×3448 321 KB](https://ethresear.ch/uploads/default/2d939b8e4d6c1ea4992be2a51f1ecf0ce00ef1f2)

Some preliminary observations:

- Cryptographic precompiles (e.g., modexp, point_evaluation) in general have high per-gas proving time.
- Mod/division-related opcodes (mulmod, mod, div, sdiv) have relatively high proving time, as well as selfbalance.
- Opcodes around log/create (log1, log2, log3, create, create2) have the fastest per-gas proving time for both SP1 and RISC0, likely because their gas costs are dominated by data and storage rather than computation.
- In general, the relative ranking of opcodes by proving time is similar between RISC0 and SP1, but there are several notable exceptions (e.g., keccak256 is ~12x slower in RISC0, sha256 is ~10x times faster in RISC0). This is likely due to zkvm precompiles of certain opcodes/precompiles existing in one but not the other (for more comparison between the provers, see the chart in Appendix: SP1/RISC0 Comparison ).

## Proving Time per ZK Cycle

ZKVMs have the concept of *ZK cycles*, which represent the number of computational steps the ZKVM executes to prove a program, analogous to CPU cycles in traditional computing. A natural question is: how good a proxy are ZK cycles for actual proving time? If ZK cycles correlate linearly with proving time across all operations, they could serve as a simpler metric for ZK gas metering. However, if the relationship is non-linear or varies significantly across operation types, then proving time must be measured directly for accurate DoS protection.

To answer this question, we fit a linear regression of proving time against zk cycles for each opcode/precompile. Below are the findings.

Within a given operation, the relationship is strongly linear (high R^2): doubling cycles roughly doubles proving time. But the conversion rate from cycles to time is not universal—it depends heavily on the operation.

The bar chart below shows this per-operation “time per zk cycle.” If cycles were a good proxy, all bars would largely align; instead, they spread widely—likely because some operations are implemented in different circuits (e.g., custom zkVM precompiles). For example, in SP1, `bn128_add` takes ~930 ns per zk cycle while `pop` takes only ~63 ns, a ~15× gap. This suggests zk cycles alone are insufficient for accurate metering of proving time. Mitigations include:

- Meter using measured proving time (as done in this post)
- Improve cycle accounting to better reflect proving time (e.g., improve zk cycle conversion between different circuits)
- Use ZK cycles as a proving time proxy, but be conservative, i.e., use numbers from the slowest time per ZK cycle operation.

[![Proving TIme per ZK Cycle](https://ethresear.ch/uploads/default/optimized/3X/e/c/ec01872733e150805129ab95e610ee2257970a36_2_258x500.jpeg)Proving TIme per ZK Cycle1783×3448 419 KB](https://ethresear.ch/uploads/default/ec01872733e150805129ab95e610ee2257970a36)

# Methodology

We adopt a marginal-cost approach, [originally developed](https://github.com/imapp-pl/gas-cost-estimator/blob/07c5af9d5b53cb0dd8e9054b41aaef4e3caa4ff8/docs/report_stage_ii.md) by the imapp team for L1 gas repricing as part of the Gas Cost Estimator project, to isolate the proving cost of individual operations.

First, we create 4-7 blocks for each opcode/precompile with varying operation counts (0, N, 2N, 3N, etc.), while maintaining constant overhead by keeping all other factors identical across variants—stack setup, memory initialization, control flow, and cleanup operations.

The table below is an example bytecode structure for the ADD opcode. Notice that each variant has exactly 20 PUSHes and 10 POPs—Only the ADD count varies.

| op_count | Setup | Main | Cleanup |
| --- | --- | --- | --- |
| 0 | PUSH×20 | — | POP×10 |
| 3 | PUSH×20 | ADD + (POP + ADD)×2 | POP×8 |
| 5 | PUSH×20 | ADD + (POP + ADD)×4 | POP×6 |
| 10 | PUSH×20 | ADD + (POP + ADD)×9 | POP×1 |

Next, we execute each block variant and record the total proving time and gas consumed by the whole block. Then, we fit `proving_time = α × gas_used + β` across all variants. Here is an example for the ADD opcode in SP1:

[![](https://ethresear.ch/uploads/default/optimized/3X/e/4/e4bd04b4f9042e3be13f838fb3540f2b89b02709_2_690x427.png)790×489 24.7 KB](https://ethresear.ch/uploads/default/e4bd04b4f9042e3be13f838fb3540f2b89b02709)

The slope `α` represents the marginal proving time per unit of gas for the opcode or precompile under consideration. Because only the target operation count varies while all other execution context is held constant, `α` isolates the contribution of that operation. In the example above, we have `α = 3.78µs`, implying a per-gas proving time of `3.78µs` for ADD in SP1 with 4 GPUs.

## Opcode/Precompile Arguments

For opcode/precompile arguments, we use fixed inputs chosen to be representative and, where applicable, “worst‑case” on a best‑effort basis. Our choices are guided by known worst-case patterns from [existing benchmarking suites](https://eth-act.github.io/zkevm-benchmark-runs/benchmarks/). Using worst-case inputs helps avoid inadvertently measuring optimized fast paths that occur only for special inputs (e.g., all-zero buffers).

Our working assumption is that proving time scales linearly with gas consumption for a given operation, not only across different operation counts, but also across different argument choices within the same operation (i.e., if you double the gas, you double the proving time). This assumes that (1) gas accurately reflects computational complexity, and (2) proving time scales proportionally with that complexity.

In practice, this assumption can fail, e.g., because gas does not accurately reflect computation complexity or because ZKVMs exhibit different behavior for certain arguments. Our measurements should therefore be interpreted as specific to the tested inputs and only as approximations for other inputs. A more fine-grained analysis of argument-dependent proving costs, examining how proving time varies across the whole argument space for each operation, is left for future work.

Finally, for operations like LOG and CREATE, where gas is primarily driven by data size and memory expansion rather than computation, we use standard arguments (e.g., 32-byte payloads) and not worst-case arguments in terms of gas. Using large payloads would inflate gas costs without meaningfully increasing proving work, underestimating the computational proving overhead per gas unit.

## Integration with EF Benchmarking Tooling

Our benchmarking pipeline builds on the Ethereum Foundation’s [zkEVM Benchmarking Workload](https://github.com/eth-act/zkevm-benchmark-workload), and we introduce two key extensions:

- Custom EEST marginal tests/fixtures: We add custom execution-spec-tests (EEST) that follow the marginal methodology.
- Multi-GPU SP1 support: We extend the EF’s ZKEVM benchmark tooling to support SP1 cluster execution, allowing the same workload to be proven using 4 GPUs.

With these additions, we generate EEST fixtures, convert them to zkEVM witness inputs using the EF tooling, run proving through the EF host runner (SP1 on 4 GPUs or RISC0), and then post-process the resulting metrics (proving time, gas, zk cycles) to fit regressions and extract marginal proving time per gas (or per zk cycles).

# Applications & Next Steps

Here are some potential practical applications of these measurements:

- ZK-aware block metering for ZK rollups: The per-gas proving-time measurements can be used to directly meter and cap the proving cost of blocks. Concretely, one can define a “ZK Gas” metric by weighting the gas consumed by each opcode/precompile with a multiplier derived from its measured proving-time-per-gas. By capping the total ZK Gas per block, the protocol can cap worst-case proving time and mitigate prover-killer blocks.
- Guidance for zkVM implementers: The per-operation breakdown highlights which opcodes/precompiles need improvements, helping zkVM teams prioritize optimizations (e.g., specialized circuits). It also provides a concrete signal for improving ZK cycle accounting so that the ZK cycle number tracks proving time more uniformly across different circuit paths.
- Guidance for client implementers: Client teams can use these measurements to identify ZK-unfriendly hotspots and optimize specific opcode/precompile implementations or execution patterns to reduce proving overhead.

For the next steps of the project:

- Argument-dependent benchmarking: Extend the methodology to sweep across all inputs.
- Continuous performance monitoring: Automate the pipeline end-to-end (fixture generation → witness generation → proving → regression → reporting) so per-opcode/precompile zkVM/client performance can be tracked over time.
- Multi-dimensional metering: Investigate how these measurements can be incorporated into multi-dimensional gas metering.

# Links

- Detailed data of our benchmarks (e.g., regression plot for each opcode/precompile):

 SP1: https://nethermindeth.github.io/zkevm-benchmark-workload/marginal-gas-benchmark/sp1
- RISC0: https://nethermindeth.github.io/zkevm-benchmark-workload/marginal-gas-benchmark/risc0/

Custom execution-spec tests used for the benchmarks: https://github.com/linoscope/execution-specs/pull/1/changes

PRs for SP1 cluster support in EF tooling:

- https://github.com/NethermindEth/ere/pull/1
- https://github.com/NethermindEth/zkevm-benchmark-workload/pull/14

Nice talk about EF’s ZK Benchmark Tooling by Ignacio: https://youtu.be/D2TpmD62tjQ?si=D4mzEagb2MXX1QXy&t=1510

Nice talk about the marginal approach by Jacek: https://www.youtube.com/watch?v=KmaFpyV9jvM

# Appendix: SP1/RISC0 Comparison

The graph below shows the `(RISC0 proving_time_per_gas) / (SP1 proving_time_per_gas)`, where `proving_time_per_gas` is the regression slope for the opcode for each prover. The reference line at 1.0× means equal performance. Values > 1.0× indicate RISC0 is slower (takes more proving time per gas than SP1 for that opcode/precompile), and values < 1.0× indicate SP1 is slower.

[![](https://ethresear.ch/uploads/default/optimized/3X/e/1/e1679409b130a7f230dd46d2874f6b36a678d073_2_162x500.png)1786×5496 491 KB](https://ethresear.ch/uploads/default/e1679409b130a7f230dd46d2874f6b36a678d073)

## Replies

**jochem-brouwer** (2026-01-28):

Hey, very nice report, we are working on similar benchmarks reports but now for the current “classic” (?) EL architecture in the context of gas repricing.

Some questions:

1. I do not see BLOCKHASH opcode. I know this is a rather “special” opcode as pre-EIP-2935 you need to do a database inspection (now you can do a storage read from the EIP-2935 contract). Is there a specific reason why this opcode is not in these zk benchs?
2. AFAIK the difference between SHA256 and KECCAK256 is only a few constants. The difference (as mentioned in your report) is huge here. This should however be somewhat easy (?) to solve? I am mainly baffled by this huge difference (but, I’m a super novice to the zk-world so I’m treating those as black box)
3. You mention argument-dependent benchmarking. For the EL side we have, especially for the ModExp precompile, really went in the rabbit hole to construct the worst case inputs to get the worst case execution time, per client (as this depends on the implementation of that precompile and certain assumptions/optimizations). I assume that the “worst case” situations for zkVMs might be different than those in “classic” VMs (live VMs as executed now). How would one find these worst case situations and is there any way we can help in this effort?

Thanks ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=14) ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=14)

---

**linoscope** (2026-01-29):

Thanks for the comment & questions!

> I do not see BLOCKHASH opcode. I know this is a rather “special” opcode as pre-EIP-2935 you need to do a database inspection (now you can do a storage read from the EIP-2935 contract). Is there a specific reason why this opcode is not in these zk benchs?

Good find! Actually, this was accidental, I ran this run with blockhash commented out ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=14) . But from previous runs, blockchash didn’t really stand out, its per-gas proving time was around the same as the PUSH opcodes.

> AFAIK the difference between SHA256 and KECCAK256 is only a few constants. The difference (as mentioned in your report) is huge here. This should however be somewhat easy (?) to solve? I am mainly baffled by this huge difference (but, I’m a super novice to the zk-world so I’m treating those as black box)

Yeah, was surprised to see this too (I am also no expert in zkvms or ZK/cryptography in general, so it’s a black box too ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=14) ). From the data, I can see that:

- The huge difference is only in RISC0, in SP1 it’s more consistent.
- The RISC0 per-gas proving time for SHA256 is 10 times faster than SP1’s.

So maybe RISC0 has some strong optimization specifically for SHA256?

> I assume that the “worst case” situations for zkVMs might be different than those in “classic” VMs (live VMs as executed now)

One thing I wonder is whether the “worst case” for zkVMs is fundamentally different from that of classic VMs. If classic gas accurately reflects execution time, and proving time scales proportionally with execution, then in principle the same benchmark models could carry over to the ZK setting, or ZK metering could even be done through a simple multiplier on execution gas. That said, zkVM implementations can have quirks that make proving time respond differently to argument changes than execution time. So definitely still worth testing ZK separately.

> How would one find these worst case situations and is there any way we can help in this effort?

Tbh haven’t put too much thought on it so far - You probably need to model proving time in terms of arguments and fit is using actual benchmarks. I assume we will need similar effort for “classic” VM execution, and that it will be applicable to ZK setting too (actually, Ignacio made a good point that we should just have one benchmark suite both for ZK and execution, which makes sense). So looking forward to what you all do here, and also happy to help out in any way too!

