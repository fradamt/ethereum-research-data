---
source: ethresearch
topic_id: 14212
title: Building the first ZKVM based on a parallel execution architecture and achieving higher TPS
author: Sin7Y-research
date: "2022-11-16"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/building-the-first-zkvm-based-on-a-parallel-execution-architecture-and-achieving-higher-tps/14212
views: 2995
likes: 1
posts_count: 7
---

# Building the first ZKVM based on a parallel execution architecture and achieving higher TPS

**TL;DR**

We are working on building the first ZKVM based on a parallel execution architecture and achieving higher TPS through the improvement of ZK-friendly design and ZK algorithms. The technical features are as follows:

- Fast proof generation

 ZK-friendly: smaller circuit scale and simplified bottom constraint units
- Fast ZK: further optimization on Plonky2
- Fast execution: Utilizing parallel execution to significantly shorten the proof generation time

Current progress:

1. In July 2022, we released the OlaVM Whitepaper.
2. November 2022, completed instruction set design and development, and realized the OlaVM execution module of the virtual machine, you can check the link: GitHub - Sin7Y/olavm: A pure Rust Olavm implementation. to view our code, continuously updated.
3. For the ZK algorithm with the fastest execution efficiency, we have completed the circuit design and algorithm research of plonky2. You can check the link: plonky2/plonky2/designs at main · Sin7Y/plonky2 · GitHub to learn more about the design of plonky2, we will optimize and improve it in the next step. Please stay tuned.

### Coming soon

2022 Early December:

1. OlaVM DSL design.
2. Pre-Compilation Contract.
3. OlaVM Instruction Constraint, Context Constraint Pre-Compilation Contract Constraint.
4. First Upgrade of Plonky2.

## Replies

**Sin7Y-research** (2022-11-16):

### What are we up to?

**OlaVM is the first ZKVM that introduces parallel VM execution, it integrates the technical features of the two schemes to obtain faster execution speed and faster proof speed, thus** **bringing** **the highest TPS of the system.**

[![流程图](https://ethresear.ch/uploads/default/optimized/2X/9/95f7a60fd6293d384e51619664cce9bbb921bed1_2_690x410.jpeg)流程图854×508 25.2 KB](https://ethresear.ch/uploads/default/95f7a60fd6293d384e51619664cce9bbb921bed1)

There are two main reasons why Ethereum has a low transactional throughput:

1. Consensus process: each node executes all the transactions repeatedly to verify the validity of the transactions.
2. Transaction execution: transaction execution is single-threaded.

In order to solve our first problem, whilst still possessing programmability at the same time, many projects have conducted ZK (E) VM research, that is, transactions are completed off chain, and only leave the state verification on the chain (of course there are other capacity expansion schemes, but we won’t go into depth on that in this post). In order to improve the systems throughput, **proofs must be generated as fast as possible.** In order to solve our second problem, Aptos, Solona, Sui and other new public chains introduced virtual machines with parallel execution(PE-VM) (Of course, it also includes a faster consensus mechanism) to improve the systems overall TPS.

At this stage, for ZK (E) VM, the bottleneck that affects TPS of the entire system is the generation of proofs. However, when Parallel Prove is used to accelerate the throughput, the faster the block is generated, the earlier the corresponding proof generation starts (with the evolution of ZK algorithms and the improvement of acceleration means, the shorter the proof generation time and more efficient and significant improvement provided by this).

---

**Sin7Y-research** (2022-11-16):

### How do you improve the systems throughput?

Increasing the speed of proof generation is the single most important aspect to increasing the overall throughput of the system, and there are two means to accelerate proof generation, keeping your circuit scale to a minimum and using the most efficient ZK algorithm. You further breakdown the meaning of an efficient algorithm, as this can be divided into improving the tuning of parameters such as selection of a smaller field, and secondly, the improvement of the external execution environment, utilizing specific hardware to optimize and scale the solution.

1. Keeping your circuit scale to a minimum

As described above, the cost of proof generation is strongly related to the overall size of the constraint n, hence, if you are able to greatly reduce the size of the constraint, your generation time will be significantly reduced as well. This is achievable by utilizing different design schemes in a clever way to keep your circuit as small as possible.

- We’re introducing a module we’ll be referring to as “Prophet”

There’s many different definitions of a prophet, but we’ve focused on “Predict” and then “Verifiy”, the main purpose of this module is to, given some complex calculation, we don’t have to use the instruction set of the VM to compute these calculations. Why this is, is because it may consume a lot of instructions, thus increasing the execution trajectory of VM and the final constraint scale. Instead, this is where the Prophet module would come into play, it is a built-in module that performs the calculation for us, sends the results to the VM, which will perform a legitimacy check, and verify the result. The Prophet is a set of built-in functions with specific computing functions, such as division, square root, cube root, etc. We will gradually enrich the Prophets library based on actual scenarios to maximize the overall constraint reduction effect for most complex computing scenarios.

- ZK-friendly

Dealing with complex calculations the Prophet module can help us reduce the overall size of the virtual machines execution trace, however, it would be convenient and preferred if the actual calculations themselves are ZK-friendly. Therefore, in our architecture we’ve opted for designing the solution around ZK-friendly operations(Choice of hash algorithms and so on), some of these optimizations are present in other ZK(E)VMs as well. In addition to the computing logic that the VM itself performs, there are other operations that also need to be proven, such as RAM operations. Given a stack-based VM, POP and PUSH operations have to be executed at every access. At the verification level, it is still necessary to verify the validity of these operations, they will form independent tables, to then use constraints to verify the validity of these stack operations. Register-based VMs on the other hand, executing the exact same logic, would result in a smaller execution trajectory and therefore a smaller constraint scale.

---

**Sin7Y-research** (2022-11-16):

1. ZK Algorithms & efficiency

[![截屏2022-11-16 11.01.44](https://ethresear.ch/uploads/default/optimized/2X/e/eafea09970d257f5c755373d326ecde6696e9b26_2_690x183.png)截屏2022-11-16 11.01.441288×342 44.1 KB](https://ethresear.ch/uploads/default/eafea09970d257f5c755373d326ecde6696e9b26)

acceleration from CPU to GPU/FPGA/ASIC implementation, such as Ingonyama FPGA accelerated design and Semisand ASIC design, etc.

Due to the amazing performance of Plonky2, we temporarily use Plonky2 as the ZK backend of OlaVM. We’ve conducted an in-depth analysis of Plonky2’s Gate design, Gadget design and core protocol principles, and identified areas of design where we can contribute and further improve efficiency. Check out our Github Repo: [Plonky2 designs](https://github.com/Sin7Y/plonky2/tree/main/plonky2/designs) for more information.

Faster transaction execution (**Currently not a problem)**

---

**Sin7Y-research** (2022-11-16):

In OlaVM’s design, the Prover is unlicensed and anyone can access it, therefore, when you have many Provers, you can generate proofs for these blocks in parallel, and then aggregate these proofs together and submit them to the chain for verification. Since the Prover module is executing in parallel, the faster the block generation(the faster the transactions in the corresponding block are executed), the corresponding proof can be generated in advance, resulting in the final on-chain verification time being significantly reduced.

[![流程图 (1)](https://ethresear.ch/uploads/default/optimized/2X/1/148fa80a7ce3526ea050f57c07f535b85f3bac2a_2_495x500.jpeg)流程图 (1)2170×2188 229 KB](https://ethresear.ch/uploads/default/148fa80a7ce3526ea050f57c07f535b85f3bac2a)

When the proof generation is very slow, e.g several hours, the efficiency improvement from utilizing the design of parallel execution is not obvious. There are two scenarios that can improve the effect of parallelism, one being that the number of aggregated blocks becomes larger, so that quantitative change causes qualitative change, and another is that the proof time is greatly reduced. Combined, this can greatly increase efficiency.

---

**Sin7Y-research** (2022-11-16):

### What about compatibility?

In the context of ZKVMs, achieving compatibility is to facilitate the connection to the development efforts already made on certain public blockchains. After all, many applications have already been developed on top of the existing ecosystems we have today, e.g, the Ethereum ecosystem. Therefore, if we can utilize these abundant resources already present by achieving compatibility with these already developed ecosystems, enabling projects to migrate seamlessly, it will greatly increase the speed of adoption of ZKVMs and scale those ecosystems. OlaVM’s main objective is currently to build the most efficient ZKVM with the highest transactional throughput. If our initial development turns out well, our following goals will be considering achieving compatibility with different blockchain ecosystems, aside from the Ethereum ecosystem, which is already included in our roadmap, supporting Solidity at the compiler level.

**All Together**

**With all the above modules integrated, the dataflow diagram of the whole system is shown in the figure below.**

[![Lark20221109-101654](https://ethresear.ch/uploads/default/optimized/2X/5/5259e6f6b9cacffde84a2995ed17590abd036162_2_520x500.png)Lark20221109-1016541961×1885 302 KB](https://ethresear.ch/uploads/default/5259e6f6b9cacffde84a2995ed17590abd036162)

---

**Sin7Y-research** (2022-11-16):

Welcome to discuss with us in the chat group:


      ![](https://ethresear.ch/uploads/default/original/2X/6/60a0dd1195aa91677b6f00e7a4eb29555e45506b.svg)

      [Telegram](https://t.me/+Ygy2fzgGqgQyOWFl)



    ![](https://ethresear.ch/uploads/default/original/2X/2/2e03754511eeb21f33466adc8eb6896d61c7e928.jpeg)

###



An Earning-Enhancing Network, Incentivized by the Bitcoin Ecosystem.		Website: https://olavm.org	Twitter: https://twitter.com/ola_zkzkvm	Discord: https://discord.gg/olavm2024	Email: contact@olavm.org

