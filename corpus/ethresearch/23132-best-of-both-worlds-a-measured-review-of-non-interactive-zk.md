---
source: ethresearch
topic_id: 23132
title: Best of Both Worlds? A Measured Review of Non-Interactive ZK Fraud Proofs
author: GCdePaula
date: "2025-09-29"
category: Layer 2 > Optimisitic Rollup
tags: [fraud-proofs]
url: https://ethresear.ch/t/best-of-both-worlds-a-measured-review-of-non-interactive-zk-fraud-proofs/23132
views: 980
likes: 22
posts_count: 8
---

# Best of Both Worlds? A Measured Review of Non-Interactive ZK Fraud Proofs

*Coauthored with [Augusto Teixeira](https://w3.impa.br/~augusto/).* *Special thanks to [Diego Nehab](https://w3.impa.br/~diego/) and [Luca Donno](https://twitter.com/donnoh_eth) for reviewing this piece.*

Recent ZK advances have reignited interest in Non-Interactive (NI) ZK Fraud Proofs like Kailua and OP Succinct Lite, pitched as a “*best of both worlds*”: no refutation costs when there is no fraud, and a single ZK proof to invalidate fraud when it occurs. Projects like [Eclipse](https://www.eclipselabs.io/blogs/fraud-proofs-the-eclipse-perspective), [BOB](https://blog.gobob.xyz/posts/first-hybrid-zk-rollup), [SOON](https://x.com/0xrahulk/status/1955246006355775830), and [MegaETH](https://x.com/megaeth_labs/status/1948030099665666446) have embraced this model, and even Arbitrum has [signaled interest](https://research.arbitrum.io/t/fraud-proof-protocols-bold-dave-and-other-alternatives/9748).

This enthusiasm led us to ask a simple question: if Interactive Fraud Proofs are “ancient technology” and NI fraud proofs “just solve fraud proofs”, should optimistic rollups be re-architected around NI?

We took this question with genuine curiosity and began our investigation with high hopes that NI Fraud Proofs could be the path forward for optimistic rollups. To that end, we went beyond a simple evaluation and undertook the significant effort of proposing our own mitigations and exploring adjacent designs. In essence, we constructed the strongest possible case for NI Fraud Proofs.

Meanwhile, public discourse has often misrepresented alternatives to NI. To avoid talking past each other and ensure productive dialogue, we anchored our analysis in a shared threat model (used by both Arbitrum’s BoLD and Cartesi’s Dave) and rigorously tested the strongest NI argument we could assemble. There is, however, a line between steel-manning and devising a new protocol. The responsibility to specify concrete, resilient mechanisms, and to engage charitably with alternatives, ultimately rests with NI proponents.

After this steel-manning exercise and rigorous analysis, our conclusion is mixed at best.

In permissionless, adversarial environments, current NI designs are vulnerable to Sybil attacks that compromise both chain progress and decentralization, and to censorship attacks that compromise security. Such attacks make NI systems underperform compared to state-of-the-art Interactive Fraud Proofs, or push them into ZK-rollup costs but without its benefits. It does not achieve the advertised *best-of-both-worlds* under our threat model, instead **inheriting the disadvantages of both approaches**.

Layer-2 protocols must meet the same high security standards that make Ethereum worth scaling. A proof system that falls short becomes the weakest link in the protocol’s overall security. This is not hypothetical: public protocols are already targeted by well-funded, nation-state-level actors. Resilience in the face of such adversaries is the very purpose of decentralization.

With this in mind, there are three properties we want from any fraud proof protocol:

1. 1-of-N Security and Progress: A single honest validator must be able to both secure the chain and progress it. This means invalid claims should never finalize, and state continues to move forward.
2. Accessibility (N is large): Anyone should be able to act as that validator, including you. The role must be accessible without requiring specialized hardware, significant capital, or delegated trust.
3. Liveness: Settlements should suffer little delay.

In the spirit of our [previous critique of Interactive Fraud Proofs](https://ethresear.ch/t/fraud-proofs-are-broken/19234), we’re again examining Sybil resistance in optimistic systems, this time focusing on NI fraud proofs. That earlier analysis helped catalyze improvements through rigorous [research and design](https://dl.acm.org/doi/10.1145/3734698); we believe NI approaches can also mature under comparable scrutiny. With institutional finance moving onchain, the bar for rigor must rise accordingly. NI may well be promising, but responses to this analysis should meet a level of thoroughness on par with [Arbitrum’s BoLD](https://arxiv.org/abs/2404.10491), [Cartesi’s PRT](https://arxiv.org/abs/2212.12439), and [Cartesi’s Dave](https://dl.acm.org/doi/10.1145/3734698). As Vitalik has argued, [the ecosystem’s standards must become stricter](https://vitalik.eth.limo/general/2024/03/28/blobs.html) — we offer this piece in that spirit.

# Threat Model

To compare fairly, we adopt the threat model used by state-of-the-art Interactive Fraud Proofs like BoLD and Dave. This is the default, established model in both academic literature and the broader blockchain community. In it, attackers are assumed to be highly resourceful, capable of launching coordinated, large-scale Sybil attacks. We refer collectively to an attacker and their mob of perfectly coordinated Sybils as **the adversary**.

For these protocols, the number of honest agents is less important than the resources they command. Inspired by Vitalik’s framing of [trust models](https://web.archive.org/web/20240606160330/https://vitalik.eth.limo/general/2020/08/20/trust.html), we therefore define “one honest validator” not as an individual agent, but as a single **unit of honest resources** (e.g., capital and computation) committed to securing the Layer 2. We assume the existence of at least one honest validator.

We also assume that, while the base layer is live and secure (i.e. all transactions are eventually processed correctly), the resourceful adversary can subvert the L1 to a limited extent by:

1. Censorship: The adversary can delay arbitrary sets of transactions, subject to a total censorship budget capped at one week. This assumption enables the Layer 2 to invoke a social response if hard censorship persists, thereby preventing permanent loss of funds. (See further discussion here.)
2. Transaction Reordering: The adversary can reorder transactions submitted to the blockchain at will, enabling tactics such as front-running honest validators.

These assumptions match those used for Dave and BoLD, so the comparison is apples-to-apples. They also reflect the setting we care about: resiliency under resourceful attackers.

# Benchmarks

To evaluate the “best of both worlds” claim, we first need to understand the worlds NI fraud proofs aim to combine: Interactive Fraud Proofs and Validity Proofs. These serve as our benchmarks for what a robust and scalable proof system should achieve.

We’ll provide the pros and cons of each approach, and in later sections, we will show that Non-Interactive ZK Fraud Proofs inherit the cons of both.

## Benchmark I: Interactive Fraud Proofs

Dave, a state-of-the-art Interactive Fraud Proof algorithm, will serve as our benchmark. For technical details, see its [peer-reviewed paper](https://dl.acm.org/doi/10.1145/3734698) and [ethresearch post](https://ethresear.ch/t/the-dave-fraud-proof-algorithm/21844).

Dave is an example of a protocol that satisfies the three fraud proof properties:

1. 1-of-N Security and Progress: A single honest validator is sufficient to keep the chain secure and live, even against a nation-state adversary.
2. Accessibility: The validator role is highly accessible, requiring only a laptop and a 1 ETH collateral that is always recovered, meaning this honest validator can be you.
3. Liveness: State settles in one week under normal conditions and within 3-5 weeks under a multi-billion-dollar Sybil attack, ensuring settlement delays are, realistically, bounded.

The underlying mechanism in Dave makes launching a Sybil attack exponentially expensive for an attacker relative to the resources a defender must commit. This forces the adversary to spend vastly more than the defender to cause even minor disruptions. Because of this cost asymmetry, **resource exhaustion attacks are eliminated**. This same mechanism also enables “in-line” refunds of gas expenses, effectively reducing the defender’s rolling cost to nearly zero. As a result, the worst the adversary can achieve is to cause settlement delays that grow logarithmically with the number of Sybils, while ultimately losing all funds committed to the attack.

Additionally, as chain throughput increases (e.g. gigagas per second), the dispute effort increases only logarithmically, ensuring the system gracefully scales with throughput.

This combination of decentralization, security, and liveness is one standard to beat.

### Common misconceptions about Interactive proofs

[![The Interactive Fraud Proof Straw Man](https://ethresear.ch/uploads/default/optimized/3X/4/d/4dbee8fdee8a42083acc140ef2db60c52bac98b7_2_690x449.jpeg)The Interactive Fraud Proof Straw Man1920×1252 189 KB](https://ethresear.ch/uploads/default/4dbee8fdee8a42083acc140ef2db60c52bac98b7)

*The Interactive Fraud Proof Straw Man*

Earlier protocol designs have led to persistent misconceptions about interactive fraud proofs. While these criticisms were once valid, modern algorithms like Dave were specifically designed to address these historical problems.

- “They are centralized due to high costs”: This misconception comes from early designs that required large bonds or imposed high dispute costs. In contrast, Dave requires only a small collateral and a laptop, regardless of the number of Sybils.
- “They are unsafe due to resource exhaustion”: In earlier interactive protocols, attackers could win by depleting the defender’s funds. Dave solves this by giving honest validators an exponential resource advantage, making resource exhaustion impossible in practice. Furthermore, this exponential advantage enables in-line gas refunds, effectively reducing the defender’s rolling costs to zero. This completely eliminates resource exhaustion as an attack vector.
- “They are slow due to interactions”: It’s a common misconception that the 7-day challenge window is a flaw unique to interactive protocols. In reality, this window is a fundamental requirement for censorship resistance in any optimistic system. Its purpose is to ensure an honest validator has enough time to get a transaction onchain even if a powerful adversary tries to block them.

## Benchmark II: Validity Proofs

Validity proofs, used on ZK rollups, represent a different paradigm. Using a cryptographic *witness*, a validity proof allows the L1 to verify a computation’s result directly. There is no challenge period; results are final once the proof is accepted onchain.

This design offers powerful advantages over fraud proofs, most notably **fast settlement**. Settlements conclude in hours or minutes, not a week. This speed is possible because the system’s security model is fundamentally different: a prover going offline is a liveness failure, not a safety failure. Since there is no challenge window, L1 censorship poses no risk to the system’s funds.

Unfortunately, these benefits come at a [steep price](https://a16zcrypto.com/posts/article/secure-efficient-zkvms-progress/). The algorithms for producing the required witnesses are orders of magnitude more computationally expensive than simply running the computation itself. To generate proofs for a workload that an ordinary laptop could process, a ZK rollup requires a supercomputer.

This has two major consequences: **proving becomes centralized *and* liveness becomes expensive**, which in turn introduces coordination challenges. To understand these issues, we’ll first estimate the cost of proving an L2.

### Estimating the costs of ZK

Estimating precise ZK proving costs is complex, as the field evolves at an incredible pace. Our goal isn’t to provide a definitive accounting — that’s not our job. Instead, our aim is to navigate the trade-offs and arrive at a reasonable, conservative estimate to use in the following sections.

On [public dashboards](https://ethproofs.org), the average cost for proving an L1 block is around $0.06. However, this figure requires more scrutiny about security. Ideally, a zkVM should target [at least 128 bits of security and be quantum secure](https://a16zcrypto.com/posts/article/secure-efficient-zkvms-progress/). Of the VMs often benchmarked, only [ZisK](https://ethproofs.org/zkvms/zisk) is above this target, and it costs on average ~$0.075 to prove an L1 block. However, ZisK is not quantum secure. The VMs that are quantum secure present their own trade-offs: [R0VM](https://ethproofs.org/zkvms/r0vm) costs more at ~$0.21 per L1 block, while [Pico](https://ethproofs.org/zkvms/pico) is cheaper at ~$0.03, but both are currently below the 128-bit security target. [SP1 Hypecube](https://ethproofs.org/zkvms/sp1-hypercube)’s proving cost is the lowest, at an average of ~$0.02, but it’s neither quantum secure nor at the 128-bit target nor open source.

Moreover, these figures are for L1 blocks. Proving L2 blocks, like those in the OP Stack, introduces additional overhead. The Kailua team, for instance, notes a [4x overhead](https://risczero.com/blog/kailua-how-it-works) for OP Mainnet execution. A similar dynamic applies to Succinct, growing from ~$0.02 per L1 block to [~$0.21](https://docs.google.com/spreadsheets/d/1C4OejyMRBFYvZrmU_yIEDQXbzHocJaQq7iXT_R-cMxI) per OP Mainnet block (target gas 5M). Using the Bonsai proving service to prove OP Mainnet blocks may cost [$14 to $22](https://risczero.com/blog/kailua-how-it-works). Arbitrum has separately [estimated](https://research.arbitrum.io/t/fraud-proof-protocols-bold-dave-and-other-alternatives/9748) an annual proving cost of **~$14 million** for Arbitrum One.

Given this complexity, and to ensure our analysis is as charitable as possible, we will not use the highest estimates of Bonsai. Instead, we will fix the cost at **$0.33 per L2 block** with a 5M gas target, give or take. Additionally, we’ll consider [500k gas](https://vitalik.eth.limo/general/2025/02/14/l1scaling.html) for onchain verification of a ZK proof.

Additional factors further increase these costs, though we’ll set them aside for now. For ZK rollups to safely achieve Stage 2, multiple independent proof systems are recommended. This multi-prover of zkVMs approach would at least double proving costs, as well as verification costs that cannot be aggregated. Furthermore, these proving cost estimates are based on today’s modest throughput. Since L2s exist to scale Ethereum, the goal is to [increase the gas target four-hundredfold](https://blog.ethereum.org/2025/07/31/lean-ethereum), which would proportionally increase proving costs.

### ZK has a liveness and coordination problem

Using our $0.33 estimate for an L2 block produced every two seconds (throughput 2.5M gas/second), ZK proving a rollup costs $100,800 weekly and nearly $5.2 million annually — just to operate a single rollup with modest throughput.

This cost raises two important questions: **who operates this expensive infrastructure, and who pays for it**? These questions map directly to the two consequences we mentioned before — proving is centralized *and* liveness is expensive.

We’ll explore some designs. Everyday users are certainly not able to operate such an infrastructure because of the extensive hardware requirements. They must delegate liveness to third parties, leading to centralized proving.

Ideally, we’d at least want a permissionless design where any third party can submit a proof and receive compensation. One approach is for users to cover proving costs through transaction fees (incurring extra costs to users), while offchain agents operate the infrastructure and earn these fees as rewards for their work.

Unfortunately, this permissionless design has coordination problems. Since generating proofs is only worthwhile when rewards exceed costs, provers naively face a dilemma: either no one submits a proof when the reward is too small, or everyone rushes to submit when it’s profitable. However, only the first submission receives compensation, leaving all other provers operating at a loss.

A detailed analysis of these coordination issues is presented in a later section, but in the context of NI fraud proofs. We also explore potential mitigations, such as locking mechanisms and random delays, but our analysis concludes they are ineffective. Developing a robust solution to these challenges is a significant undertaking that falls beyond the scope of this paper. To our knowledge, no ZK rollup currently implements this permissionless model as its primary path.

To address these coordination issues, ZK rollups typically employ a centralized sequencer that collects user fees to subsidize their own prover. This centralized model is problematic as it creates a single point of failure, making the system vulnerable to everything from government pressure to cyberattacks and even violence, the very risks decentralization is meant to prevent. This also leads to an over-reliance on a centralized sequencer, which has issues of its own. To mitigate these challenges, ZK rollups generally allow permissionless proving as a fallback mechanism, though this fallback operates under impaired capacity due to the coordination challenges mentioned earlier.

---

Non-Interactive ZK fraud-proof protocols like Kailua and OP Succinct Lite were explicitly created to mitigate these cost issues facing ZK rollups.

## Benchmark Tally

TL;DR

- In Dave, a single validator with small requirements can secure and progress the chain.

However, there’s a 7-day withdrawal delay, which grows logarithmically under attack to a maximum of 3 weeks under a multi-billion-dollar attack.

In ZK, withdrawals are quick.

- However, liveness is centralized and chain progress is expensive.

# The Promises of NI Fraud Proofs

[![Knights Who Say Ni!](https://ethresear.ch/uploads/default/optimized/3X/6/8/68abdfb56192b039980798d017d09029e156352e_2_250x250.jpeg)Knights Who Say Ni!761×761 54.8 KB](https://ethresear.ch/uploads/default/68abdfb56192b039980798d017d09029e156352e)

*Knights Who Say Ni!*

NI fraud proofs start from an agreed initial state and a deterministic state transition function. A proposer submits a claim during the challenge window, consisting of:

- the final state after G state transitions and
- the full list of all G intermediate states posted onchain.

The claim is backed by a bond. In the context of EVM L2s, this state transition consists of several L2 blocks, which in turn may require billions of zkVM instructions.

Conflicting claims implicitly create a dispute; no explicit challenge transaction is needed. Given a dishonest claim with an invalid transition at index i \in \{1, \ldots, G\}, any party can produce a ZK proof for state transition i to refute the entire claim. Upon successful refutation, the claimant’s bond is forfeited and awarded to the refuter. When the challenge window closes and a single claim remains, that claim is accepted as the correct result.

This setup has an upper bound on refutation work for a single settlement: in the worst case, at most G step proofs are enough to determine the correct state. If proofs for all G steps are produced, the off-chain computational work becomes cost-equivalent to a ZK rollup.

The choice of G presents an important trade-off. If G is set too small, it requires increasing bond sizes to maintain rewards, which in turn centralizes liveness by raising the barrier to participation. Conversely, if G is made significantly larger, it increases data availability costs even during normal operation, while also expanding the maximum number of potential refutations needed. Both the higher refutation ceiling and increased DA usage ultimately reduce the number of L2s that can fit on Ethereum.

---

Proponents of NI claim that they solve three core challenges of optimistic rollups:

1. Resource Exhaustion: A refutation receives the dishonest claimant’s bond. As such, all proving costs are paid by the adversary.
2. Accessibility: Bonds are small and validator hardware requirements are modest, which lowers participation barriers and improves decentralization.
3. Withdrawal Delays: A single proof can resolve a dispute, making dispute resolution faster than Interactive Fraud Proof protocols. This enables withdrawals to settle in just a few hours, rather than the minimum 7-day window required by interactive protocols.

These three claims hinge on an alleged Sybil and censorship resilience, as Sybil attacks and L1 censorship are the source of those three challenges in optimistic proof systems. However, under our defined threat model, these resiliencies do not hold, and as a result, none of the three claims hold either.

The underlying flaw is that the honest validator must respond to every single Sybil individually, which creates a cost structure where the **defender’s effort scales linearly with the adversary’s resources**, up to a weekly maximum that corresponds to full ZK validation. This single property is the source of several cascading issues that prevent the NI approach from delivering on its core promises.

In the following sections, we describe each of these issues in detail. We show that validators must bear high upfront proving costs, which undermine accessibility and result in centralized liveness (2). Alternatively, proving capacity is under-provisioned, which causes withdrawal delays linear on attacker funds (3). We also describe a self-refutation strategy that allows an adversary to prevent honest validators from ever being reimbursed, leading to resource exhaustion that compromises liveness (1, 3).

These issues become more pronounced as chain throughput increases.

## Running example: BOB on Kailua

To make our analysis concrete, we will use BOB, an OP Stack rollup that uses the Kailua protocol, as our running example.

It’s worth noting that Kailua is a hybrid protocol that can operate in either validity or optimistic modes. Our critique specifically addresses the **optimistic mode**, where claims of Sybil resilience are made. If this mode can’t meet its promises, then a pure ZK rollup or a pure Dave rollup would be a more logical architecture.

Let’s establish the parameters for this example, based on BOB’s architecture running on optimistic mode, and our one-week challenge window assumption:

- BOB has a gas target of 5M gas per block, and generates one block per 2 seconds.
- A single settlement covers a sequence of L2 computation of 12 hours, consisting of 21,600 blocks.
- Each settlement is broken down into G = 3600 slices, where each slice represents 6 blocks of execution.
- Under a 7-days challenge window and with settlements every 12 hours, there are at least 14 open concurrent settlements at any given time.
- A proposer must post a 0.5 ETH bond to back their claim.

# Finding 1 — Challenge window must still be long

Under the same censorship assumptions used for interactive protocols like Dave, NI fraud proofs do **not** enable withdrawals in “a few hours.” The duration of the challenge window in optimistic systems is set by the *censorship budget of the adversary*, not by how many onchain transactions a dispute requires.

If finality arrived within hours, an attacker could post a fraudulent claim and then suppress any honest refutation for the length of that short window — long enough to steal all TVS. Whether refutation takes one transaction per Sybil (NI) or several (Interactive) is irrelevant: if the adversary can censor one critical transaction for the full window, safety fails. Therefore, under an apples-to-apples threat model that allows sustained L1 censorship, NI requires a challenge window on the order of a week, **inheriting the same cons as Dave**. This is unlike ZK rollups.

If the community later decides that a one-day censorship assumption is acceptable, *both* NI and Interactive systems can shorten their windows accordingly. For the remainder of this analysis, we adopt the standard seven-day window to ensure a fair comparison.

# Finding 2 — Liveness is not 1 of N

Let us start by observing a very positive aspect of NI Fraud Poofs: their security is 1-of-N, meaning that it is guaranteed as long as a single honest validator is running. In this sense, they are not behind Dave, which also has 1-of-N security. But we now argue that this is not the case for the liveness of the chain.

To illustrate the argument, let us imagine a situation that sounds extreme, but reflects exactly the assumption behind the 1-of-N model. Suppose that the chain is being defended by a single honest validator with a modest hardware and the attack is being mounted by a very well funded agent that posts G wrong claims per settlement period (each claim with an incorrect transition at a different interval of the computation). In such a scenario, the single honest validator will not be able to refute all the false claims in a timely manner. Consequently, **the chain will progress at a fraction of its intended speed**.

For example, if the single honest validator has 1/100th of the computing capacity necessary for a full ZK proof, then the chain will run at 1/100th of its designed speed while the attack is maintained. In this under-capacity scenario, delays would grow linearly with attacker funds, while in Dave they grow logarithmically with attacker funds.

Therefore, NI systems require the same proving capacity as a ZK rollups because the adversary can force the honest validator to generate ZK proofs for all state transitions in a settlement window. Even under the optimistic scenario of no disputes, validators must still be able to meet the compute power — whether actively used or not — simply to be prepared for potential attacks.

### Counterarguments

Several counterarguments could be raised against Finding 1. We’ll address these briefly here and explore them more thoroughly in the subsequent Findings.

---

#### Argument 1 - Delegated Proving

*Assuming that there is profit to be made in refuting wrong claims, it should be easy for the honest party to outsource the task of building proofs to a specialized service.*

#### Counterargument

This approach inherits the trust assumptions of the proving service, which may be considerable. This is a risk that doesn’t exist in our benchmark Dave.

Moreover, these costs are substantial. The single honest validator must have enough capital to front the potential proving costs for all concurrent open settlements. With a one-week challenge window, this means covering 14 settlements simultaneously before being reimbursed for each, as the alternative of proving serially is not a viable option (see Argument 2).

Using our Kailua example, validated through an external service at $0.33 per block, the honest validator must have at hand $100,800 (3600 slices/settlement × 6 blocks/slice × $0.33/block × 14 settlements/week). This is significantly more resource requirements than our Dave benchmark, and becomes worse as chain throughput increases (see Finding 3 below). This adds to the difficulty of building an economic layer to incentivize the protection of the chain.

---

#### Argument 2 - Serial Proving

*To reduce the burden of generating all proofs simultaneously within a week, the single honest validator could instead build proofs sequentially. In a delegated proving scenario, the validator could potentially use the reward from one successful refutation to fund the next proof in the sequence.*

#### Counterargument

This would render the system unusable. Using a conservative estimate of 3.5 minutes per block, **it would take about 1 year to generate all proofs for one week** (3600 slices/settlement × 6 blocks/slice × 3.5 minutes/block × 14 settlements/week).

To reiterate, Non-Interactive ZK systems require the same proving capacity as full ZK rollups. Without this capacity, the system would experience significant settlement delays — refutations must be processed in parallel.

---

#### Argument 3 - Expensive to launch such an attack

*By setting up the right economic setup, it could be made very expensive to launch such an attack, by imposing penalties to wrong claims.*

#### Counterargument

As we argue in Finding 5 below, it is not easy to design such punishments without also imposing extra bond costs to honest parties. Moreover, an attacker can profit from delaying the finality of the chain and this should be measured against the cost of the attack.

The underlying issue is that the burden on honest validators generated by such an attack scales linearly with attacker funds. This is unlike our benchmark Dave, where burden grows logarithmically with attacker funds.

---

#### Argument 4 - Profitable to honest parties

*With the right incentive layers in place, it should be very profitable for the honest party to fight such an attacker.*

#### Counterargument

As argued in Finding 5 below, it is hard to create such an incentive without making the attack cheaper to launch.

---

#### Argument 5 - Honest parties can join forces

*Assuming that there is profit to be made in refuting wrong claims, it should be easy to make many honest parties cooperate in the task of refuting the wrong claims.*

#### Counterargument

Relying on multiple validators means we’re not in 1-of-N territory anymore.

Additionally, it faces similar coordination challenges as ZK rollups under a permissionless design, as mentioned earlier. We argue in Finding 4 below that when multiple validators are present (some of which could be controlled by the adversary), coordinating who receives the reward for refuting a claim becomes difficult enough to undermine incentives for validation. This coordination is not only slow and wasteful but also creates opportunities for the attacks we detail in Finding 5.

---

None of these counterarguments address the fundamental issue: the chain’s liveness is not truly 1-of-N. Validators must maintain sufficient proving capacity and be prepared to front the costs of proving for an entire week.

# Finding 3 — Impractical at scale

The previous liveness finding grows as throughput increases. Our Kailua example, which estimates a potential ~$100 thousand weekly cost for an honest validator, is based on the modest throughput of today’s systems. As rollups move toward processing gigagas per second, this problem becomes dramatically worse.

The core issue is that the amount of computation an adversary can challenge is directly proportional to the chain’s throughput. If a rollup’s throughput increases by 400x, the work an honest validator must be prepared to prove also increases 400x.

Consequently, the capital required to guarantee liveness scales linearly. In a 400x throughput scenario (gigagas/second), our estimated ~$100 thousand weekly defense cost would **increase to ~$40 million**. No system that requires a **$40 million capital commitment for liveness** can claim to be decentralized.

While it’s true that improvements in ZK technology — cheaper and faster provers — will mitigate these costs, this hope misjudges the severity of the linear scaling problem. For the security budget to remain stable, ZK proving costs must decrease at the *same rate* that rollup throughput increases. A 400x increase in throughput would require a 99.75% decrease in proving costs just to maintain today’s already high defense budget. A system that relies on technological advancements of this magnitude merely to tread water is not ideal and locks us away from future scalability.

This is unlike Dave, which scales gracefully (i.e. logarithmically) at higher throughput.

# Finding 4 — Open coordination games waste resources (and don’t fix liveness)

We have shown that NI designs achieve 1-of-N security but not 1-of-N liveness.

A natural relaxation is to aim for an H-of-N liveness model, where H honest solvers participate in refutation. Unfortunately, since proving is open and permissionless, this creates coordination issues that undermine incentives to participate.

The problem echoes the two coordination questions we raised for permissionless ZK rollups: who operates the expensive ZK infrastructure, and who pays for it?

Addressing the second question first: NI systems cannot predict when disputes will occur, and proving costs materialize only during disputes. If users were preemptively charged proving fees, then from the user’s perspective NI becomes cost-equivalent to a ZK rollup, except with an additional seven-day withdrawal delay. This is not a compelling trade. Instead, NI systems typically funds refutations *a posteriori* with forfeited bonds from incorrect claims.

The question then becomes: who actually captures these bonds? Here the race begins. Naively, in a permissionless setting, multiple parties can compute the same refutation, but only the first onchain inclusion earns the payout. MEV and potential censorship already make transaction ordering adversarial for honest participants. Even without these complications, validators must compete in a winner-takes-all race, with **expected waste growing with the number of honest participants**.

Concretely, if there are H honest solvers who each spend cost c to produce a refutation for a given divergence, then the total honest cost is  H\cdot c while, at most, one party is compensated. The net waste is (H-1)\cdot c per disputed claim. Under Sybil pressure, where an attacker fans out K conflicting claims, the honest side faces aggregate waste on the order of K\cdot(H-1)\cdot c.

## Mitigation attempts

In the spirit of presenting the best possible argument for NI fraud proofs, we explore a few mitigation strategies.

### Locking

To address the race condition, we could introduce a locking mechanism where validators lock L funds to secure exclusive rights to receive rewards corresponding to a specific refutation. If the lock times out, L is burned as a collateral.

However, this approach remains vulnerable to Sybil attacks. In its simplest form, the system would experience delays proportional to the attacker’s funds, as they could continuously purchase locks to prevent chain progress.

Moreover, since honest validators must also purchase locks, increasing the lock price increases centralization: in addition to the proving costs, in Kailua honest validators would need to acquire 50,400 locks (3600 slices × 14 settlements).

A more sophisticated approach could introduce a progressive lock pricing mechanism, where each subsequent lock becomes more expensive. For example, if the price increases linearly (the first lock costs L, the second 2L, the third 3L, and so on), an attacker wanting to buy T consecutive locks to stall the chain would face a total cost proportional to T^2. This would reduce delays by depleting the adversary’s funds more quickly.

Despite this improvement, the model remains flawed. First, the delays it allows, while better than linear, are still worse than the logarithmic delays offered by Dave. Second, the honest validator must still bear a high cumulative cost of L \cdot(T+1) to acquire the final lock, creating additional centralization pressure that grows with the adversary’s funds.

### Random submission

A random submission strategy could be implemented to mitigate race conditions as the number of honest validators H grows. Let us reasonably suppose that validators are trying to maximize their rewards, and that they’ll choose their own submission delay rationally. Moreover, let us suppose that H is known, which is an advantage that can only help the honest validators.

To analyze the optimal random submission strategy, we model it as a game with **H** rational, honest validators. Each validator adopts a mixed strategy, choosing to generate a ZK proof with probability **p**. The cost of this action is **c**, and the reward for being first is **r**.

An equilibrium is reached when validators are indifferent to participating, meaning the expected cost of generating a proof is equal to the expected reward they’d get from that action. The equilibrium condition is therefore expected\ cost = expected\ reward.

The expected reward can be formally modeled using a Poisson distribution, leading to the equilibrium equation:

p \cdot c = r \cdot \frac{1 - e^{-H \cdot p}}{H \cdot p}

We approximate this equation to p \cdot c \approx r / (H \cdot p + 1). This leads to the quadratic equation H \cdot p^2 + p - r/c = 0, whose asymptotic solution for large H is p \approx \sqrt{r / (c \cdot H)}. Therefore, the equilibrium in a random submission strategy, has total expected number of ZK proofs submitted in each round of this game be H \cdot p \approx H \cdot \sqrt{r / (c \cdot H)} = \sqrt{H \cdot r/c}. This means that while individual validators rationally become more timid as H grows, the total number of competing proofs still increases.

As such, even with randomized submissions, the total wasted cost across all honest validators c \cdot (\sqrt{r \cdot H/c} - 1) still increases with the validator count, resulting in wasted computational resources and capital.

This unfortunate equilibrium undermines validator incentives, as participation is not particularly attractive: expected profits hover near zero while carrying significant variance.

# Finding 5 — Nothing-at-Stake Self-Refutation

NI are vulnerable to a resource exhaustion attack reminiscent of the “nothing at stake” problem found in Proof-of-Stake consensus protocols.

The same race that wastes honest work can be weaponized. Recall that our threat model assumes the adversary controls transaction ordering on L1, consistent with the model used in our analysis of Interactive Fraud Proofs.

The attack proceeds as follows:

1. An honest validator expends resources (computation, time, and money) to generate a valid ZK proof. This effort can be substantial under Sybil attacks; using our Kailua example, it could cost approximately $100K/week at current scale, and scale to $40 million weekly at 1G gas/second.
2. They broadcast their transaction containing this valuable proof to the mempool.
3. The adversary, seeing this transaction, copies the proof from the honest validator and wraps it in their own transaction, front running the honest validator.

Ultimately, **the adversary self-refutes their own claim, recovering their bond in the process, and denying the honest validator the reward from their work**, while paying nothing. By repeating this cycle, the attacker can continually bleed honest validators of resources, eventually draining all resources of the honest validators and indefinitely halting chain progress. This compromises the system’s liveness.

Moreover, this race takes place in the adversarial “[Dark Forest](https://www.paradigm.xyz/2020/08/ethereum-is-a-dark-forest)” of Ethereum’s mempool. This means the front-running attack is not merely a strategy available to the adversary, but an inevitable, automated outcome of the environment itself. Any unprotected refutation will be treated as a profitable opportunity and will almost certainly be sniped by MEV bots, guaranteeing the honest validator receives no compensation for their work.

It is worth noting that Dave’s cost structure is fundamentally different, which is why it avoids these specific coordination problems. Dave’s expenses are dominated by on-chain L1 gas, while in ZK-based systems they are dominated by a large, *a priori* investment in off-chain compute. Reimbursing an in-protocol gas fee is an easier mechanism, while refunding a large, out-of-protocol cost that has already been sunk by a prover is not.

We struggle to see a workable reward mechanism under this threat model. The mitigations we explore later, such as bond burning, function only as penalties to the adversary rather than rewards to the honest validator.

## Mitigation attempts

In the spirit of presenting the best possible argument for NI fraud proofs, we explore a few mitigation strategies.

### Embed Beneficiary Address in Proof

A natural first-line defense against this sniping attack is to embed the beneficiary’s address in the validity proof, with the L1 contract enforcing that the reward is only paid to the address embedded within the proof. This mitigation is effective and necessary against the Dark Forest. It successfully prevents the direct theft of a validator’s completed proof, as a copied proof would still pay the original author.

However, while embedding an address protects a validator’s proof from being stolen, it does not protect the validator from being out-raced by the adversary with a different proof. In this new scenario, the adversary precomputes their self-refutation (embedding *their own* address) before submitting their claim onchain. Then, when the honest validator submits their refutation, the adversary simply front-runs it, submitting their own pre-computed proof first and reclaiming their bond.

This re-introduces the resource exhaustion attack. Ignoring gas costs, the adversary’s cost to self-refute is at most equal to the honest validator’s, establishing a **resource ratio of 1**. This scenario of resource parity is fragile; an adversary with greater resources will win a war of attrition, draining the defender’s funds and halting the chain.

Worse still, the adversary can structure their dishonest claim to maximize the resource ratio to their benefit. They can introduce a fraudulent divergence at the most expensive point to prove, and afterward append a second, much cheaper divergence later in the computation. This second divergence is entirely fabricated by the attacker, and doesn’t even have to be part of the computation. As a result, an honest validator who attempts a genuine refutation will be forced to target the first divergence, while the adversary can always choose to self-refute at the second, inexpensive one. This further tilts the economics: honest validators pay the highest proof cost, while the adversary reclaims their bond for much less.

### Enforce first divergence

A strategy to restore the resource ratio to 1 is to award the refutation reward only to the proof of the *earliest* invalid state transition, This mechanism requires delaying the bond payout until the state is finally settled, which isn’t ideal. This delay would prevent validators from using rewards from a previous refutation to fund costs of subsequent refutations within the same challenge window, even without an attacker present.

However, resource parity is an insufficient guarantee for liveness. In any realistic scenario where the adversary, such as a nation-state, has greater resources, the defender will slowly be drained of resources, and eventually the chain progress will halt. A truly resilient system must provide a significant advantage to defenders, not just a level playing field.

### Distribute bonds

A potential solution would be to distribute the forfeited bond among all parties submitting valid refutation proofs. Unfortunately, this approach is easily exploitable.

The adversary can submit a fraudulent claim, then self-refute with k valid proofs instead of just one. If there is one honest refuter, the adversary simply collects k / (k+1) of their own bond back. The honest party is forced to pay the full cost of a proof while receiving a reward that the attacker can dilute to near zero. Additionally, the bond value would need to scale proportionally with the expected number of refutations to keep rewards attractive.

### Burn Half the Bond

Perhaps the most effective mitigation is to burn half of the forfeited bond and award the other half to the refuter. This creates a configurable resource advantage for the honest validator, equal to a constant of bond\_value / (2 \cdot proof\_cost). We strongly recommend that NI systems adopt a bond-burning mechanism as a necessary improvement.

First, it should be noted that this mechanism increases the bond for the honest party as well, adding to the centralization concerns that we have been discussing. Moreover, this mitigation doesn’t fix the reward system, but only introduces a penalty to the adversary.

Ultimately, the underlying resource function remains **linear**, albeit with a more favorable constant. This means the defender’s costs for liveness still grow linearly with the adversary’s spending. To achieve resilience against a nation-state adversary with a linear resource function, a protocol must set its constant extremely high.

For example, to give defenders a 100x advantage — which we’d argue is the bare minimum — the bond must be set to 200 times the proof cost. In our Kailua example, this translates to an $26K bond for gigagas, which reduces accessibility. In contrast, our Interactive Fraud Proof benchmark offers an **exponential** resource function without requiring high bonds.

Under our threat model, we see no compelling reason not to burn 100% of the bond. However, burning 50% might be advisable in case an attacker lacks the resources necessary to control ordering.

# Tally

In this section, we compare Non-Interactive ZK Fraud Proofs against our benchmarks. To provide the fairest evaluation of NI systems, we’ve incorporated the strongest mitigations:

- Embed Beneficiary Address in Proof;
- Enforce First Divergence;
- Burn Half the Bond.

Our analysis examines four solutions:

- Low-capacity NI: 2.5 megagas/second target with 0.5 ETH bond and G=3600, matching BOB+Kailua’s implementation;
- High-capacity NI: 1 gigagas/second target with 20 ETH bond and G=3600;
- Dave: 1 gigagas/second target with 1 ETH bond, using group size of 4 and the continuous variant;
- Validity Proofs: 1 gigagas/second target.

|  | NI (low capacity) | NI (high capacity) | Dave | Validity Proofs |
| --- | --- | --- | --- | --- |
| Throughput target | 2.5 megagas/s | 1 gigagas/s | 1 gigagas/s | 1 gigagas/s |
| Resources for Security | Laptop + 0.5 ETH | Laptop + 6.6 ETH | Laptop + 1 ETH | None |
| Hardware reserved for Liveness | Supercomputer | Supercomputers | Laptop | Supercomputers |
| Funds reserved for Liveness | $100K + 0.5 ETH | $40M + 6.6 ETH | ~$0 + 1 ETH | $40M/week |
|  |  |  |  |  |
| Steady-state |  |  |  |  |
| Cost of progressing chain | ~$0 | ~$0 | ~$0 | $40M/week |
| Withdrawal Time | 1 week | 1 week | 1 week | Hours |
| Transactions per Settlement | 1 | 1 | 1 | 1 |
|  |  |  |  |  |
| Sybil attack |  |  |  |  |
| Adversary Bond Expenses | 12.5K ETH/week | 500M ETH/week | 1M ETH/week | - |
| Cost of Progressing Chain | $100K/week | $40M/week | ~$0 | $40M/week |
| Costs Recovered After Dispute? | No | No | Yes | - |
| Withdrawal Time | 1 week | 1 week | 3 weeks | Hours |
| Transactions per Settlement | 50K/week | 50K/week | 700/week | 1 |

Our analysis concludes that under attack — perhaps the most critical scenario for any decentralized protocol — the overwhelming advantage in resilience and cost efficiency belongs to Interactive Fraud Proofs like Dave. Moreover, even in steady-state scenarios, chain progress in such systems is more accessible, and thus more decentralized. If fast settlements are an absolute requirement, then Validity Proofs are the only viable choice. Consequently, **in no scenario do current NI designs emerge as the optimal solution**

# Conclusion

Our analysis leads us to conclude that current Non-Interactive ZK Fraud Proof designs, under the default security model, do not allow faster withdrawals nor are Sybil-resistant.

The underlying cause for Sybil vulnerability is that the honest validator must personally refute every bad claim, causing their effort to scale linearly with an attacker’s resources. This is untenable in a permissionless setting.

As a consequence, NI do not deliver the advertised “best of both worlds.” Our analysis indicates that (i) the challenge window **continues to be 1 week**; (ii) **liveness is not 1-of-N**; (iii) open-race refutation **wastes honest effort** that grows with the number of honest validators; and (iv) adversarial ordering enables self-refutation, causing **resource exhaustion attacks that compromise liveness**. All these are made worse as throughput increases to gigagas.

## Moving Forward

Our analysis was motivated by a genuine curiosity to understand if Non-Interactive (NI) fraud proofs could be the path forward for optimistic rollups. To that end, we went beyond a simple evaluation and constructed the strongest possible case for NI systems.

This process has reinforced our belief that research in this domain requires a higher standard of rigor. Progress for the entire ecosystem depends on researchers engaging charitably with alternative designs and carefully testing proposals against well-established threat models. This is the spirit in which we offer this analysis.

We hold ourselves to this same standard. For our work on Interactive Fraud Proofs, we chose formal peer review as one way to validate our findings and invite public scrutiny. To be clear, the specific method is less important than the principle: we are calling for stricter standards, not for academic gatekeeping.

The most promising way for this conversation to move forward is for the responses to our analysis to meet such standards. Counterarguments should be presented with concrete mechanisms that credibly address the findings detailed here under the same threat model. We hope that this analysis serves as a constructive step toward a new generation of Non-Interactive designs that can overcome current shortcomings.

## Afterword

I extend my deepest gratitude to [Felipe Argento](https://x.com/felipeargento), [Pedro Argento](https://x.com/PedroArgento8), and [Claudio Silva](https://x.com/claudioengdist) for their insights in writing the article.

I also extend my gratitude to [Cartesi](https://cartesi.io/) for funding the research and for providing the environment where the development could take place. We invite the reader to join us on [our Discord](https://discord.gg/uqejyBBD), where we continuously engage in public research and debate these topics constantly.

## Replies

**rami** (2025-09-30):

Hey [@GCdePaula](/u/gcdepaula)! Kailua guy here from Boundless. I wanted to mention a few missed points that could strengthen your analysis and improve your proposed steel-man arguments and conclusion.

- OP Succinct Lite (OPSL) does not work like Kailua (and isn’t even NI). If you actually look at how it works, each bad proposal has to be explicitly challenged, leading to standard interactive protocol vulnerabilities. At best, it’s a one-round protocol. Anyway..
- Delegating proving doesn’t have to be to a centralized protocol. Boundless exists. Bonsai proving costs are a very outdated metric. We’ve been fully proving several Mainnet rollups on Boundless, such as Base, OP, Unichain, etc, almost for free. Not to mention The Signal (full eth consensus) proofs.
- Kailua works natively enables permissionless proving, not as a fallback as you mention. This is an OPSL-only thing.
- The claimant’s bond is split three-ways in Kailua between the prover, the winning proposer, and this guy. With proving power being clearly abundant as shown on Boundless (10s of trillions of cycles per day), the griefing vector you mention isn’t at all impactful given our approach to locking (explained below).
- Increasing the number of published transitions in a claim in practice presents a negligible overhead in DA costs. BOB Mainnet submits one extra blob every 12 hours for example. Having a large “G” isn’t as impactful as you mention and is actually independent of the maximum total refutation work in a given period so you might want to reword this.
- Your 1 of N argument assumes that bonds exactly cover refutation costs, which is incorrect. If the bond covers twice cost for example, then a single honest validator can delegate two new proofs for each bond it consumes instead of the sequential strategy you suggest.
- Just like your DA/infra/whatever cost, your security budget should be relative to your throughput, not “stable” (fixed) as you say. It’s more realistic to think of the cost per transaction being the stability target here.
- Your sequential locking mechanism with increasing costs isn’t the best approach here. Instead, our Hydra orders model is a better approach and achieves liveness. In this model, when a lock expires, the locked bond is used to subsidize two new proof requests instead of one. Each request is only for half the work.

I believe this analysis could be made much more accurate when you consider the points I mentioned above.

---

**GCdePaula** (2025-09-30):

Hey! Thank you for taking the time to read our article and engage with the arguments. We’re glad that you’re engaging here in a more constructive way, and not like this: [(1)](https://x.com/hashcashier/status/1972992416421704072), [(2)](https://x.com/hashcashier/status/1972986349461631054), [(3)](https://x.com/hashcashier/status/1972935267473580062), [(4)](https://x.com/hashcashier/status/1972934214128705855), [(5)](https://x.com/0xEverly/status/1972767855163945240), [(6)](https://x.com/hashcashier/status/1973035314890616991). We were indeed expecting a more productive approach from the team behind RISC Zero and Boundless, which we deeply respect.

Try not to think of us as a competing L2 (in a sense, we’re not), but as a member of the wider community trying to figure out the trade-off of various mechanisms. This effort had to be made against all odds: no clear designs written down, no sources for the costs, etc.

Even though this reply indeed contains hints on how to address our findings, the answer still falls short of the higher standard that the community deserves. Mechanisms like the bond-burning you mention or the “Hydra orders” model are prime examples that warrant a full specification. A two-sentence description on a forum is not a substitute for that.

**wen whitepaper**

---

With that context in mind, I’ll address your points in order.

### OPSL

Our article analyzes a steel-manned, generalized version of a Non-Interactive mechanism. Its goal is not to critique any specific, named protocol. Whether our model perfectly matches the implementation details of OPSL is secondary to the analysis of the core mechanism itself.

### Proving Costs & Boundless

You’ve mentioned that the proving costs we use are inaccurate. We made every effort to search publicly available numbers (ethproofs, Succint self reports, Bonsai), supplied by credible third parties. We were careful to be fair, deliberately using a conservative estimate and not the significantly higher numbers from Bonsai (which can be over 50x more expensive). If the sources we linked in the article are not accurate, we ask you to supply alternative links instead of the vague sentence saying that it’s “almost for free”.

**wen whitepaper**

### Permissionless Proving

This is a misreading of our argument. Our article *assumes from the start* that any proof system should be permissionless if it is to be taken seriously. This principle is precisely what introduces the coordination challenges, resource exhaustion, and race conditions that we analyze. Our findings were never about permissionless proving being a “fallback”; it was about the vulnerabilities of a permissionless proving model under an adversarial threat model.

### Bond Splitting & Burning

We’re glad to hear Kailua implements a bond-burning mitigation as we recommended other projects to implement. As part of our steel-man exercise, our final analysis in the “Tally” section already accounts for a version of NI with this mitigation included, so it does not change our conclusions. However, this mechanism does not appear to be documented publicly, which again points to the need for stricter standards for research and specification.

**wen whitepaper**

### Large “G”

Increasing `G` does not resolve the core issues we raised (the 1-week challenge window, 1-of-N liveness failures, self-refutation attacks, etc.). It presents a trade-off between bond sizes and DA usage. While DA is cheap now, it’s unrealistic to assume it will remain so as demand increases. More importantly, there is a practical ceiling on `G` imposed by L1 blockspace. Refuting all 3,600 state transitions in our example would already require filling ~90 L1 blocks with proofs. This number cannot be increased indefinitely. The burden of proof remains on NI proponents to provide a rigorous analysis showing how a larger `G` solves these fundamental problems without negative externalities.

**wen whitepaper**

### Liveness is not 1-of-N

Our definition of liveness being 1-of-N is based on the idea that a regular honest validator can progress the chain, even under attack. You could have a different definition in which regular users have a supercomputer, but we’d argue that’s not a reasonable definition.

That said, our argument does not assume that bonds exactly cover refutation costs, as you claim it does. It’s based on a simple fact: if you don’t have the proving capacity to fully verify the chain in real time, delay attacks are inevitable.

### Double Refund

We have in fact steel-manned NI already, included bonds set significantly higher than proof costs, giving defenders a strong resource advantage.

Of course, higher refunds are not useful if self-refutation is still allowed, so let us continue discussing this below, in the Hydra-locking point below. We are trying to interpret your message and turn it into a design in our heads. It looks like it could be something useful, if it ever got explained in more than a sentence.

**wen whitepaper**

### Security Budget vs. Throughput

This is a misrepresentation of our analysis. We did not say the security budget should be “stable (fixed).” In our “Tally” table, we explicitly increased the bond and requirements for the “High-capacity NI” example in proportion to its higher throughput. Our argument is that the **total capital commitment required for liveness** scales linearly with throughput, which is a powerful centralizing force.

When you say “your security budget should be relative to your throughput”, you are implicitly assuming that every proof system naturally becomes more centralized as it scales in throughput. You may be able to reach a better design than this. For example, in Dave, the security budget is not a function of throughput.

### Hydra Order

Your comment that the naive locking mechanisms we explored are insufficient simply reinforces one of our article’s own conclusions. After exploring the design space, we showed that no obvious, simple locking mechanism appears to be resilient to Sybil attacks.

On “our Hydra orders model is a better approach”. This sounds interesting, where is this mechanism described? Searching Google/chatGPT for “Hydra orders model” didn’t lead us anywhere. We have discussed internally, and Hydra indeed sounds promising. This is yet another indication that the community desperately needs to have access to these specifications.

**wen whitepaper**

---

## Conclusion

Our post is based on available informations in the internet. And as such, we believe the findings of our article stand.

This is not to say that there isn’t a design out there (e.g., on your desk) that would mitigate many of the above shortcomings. You’re very well positioned to publish this. The scarce designs sketches you provided in your reply point to something that could become a net positive to the industry. But we cannot stop there.

---

> I believe this analysis could be made much more accurate when you consider the points I mentioned above.

We fully agree with this sentence, but this is not our job.

**wen whitepaper**

---

**sergeyshemyakov** (2025-10-01):

Hi! I am Sergey, ZK researcher at L2BEAT. I think Gabriel is starting a very interesting and important discussion on non-interactive ZK fraud proofs. This post challenged me, so I wanted to share my personal perspective on the arguments.

Quick disclaimer: I don’t know the specifics of Dave and Kailua, my perception is more of conceptual interactive and non-interactive fraud proofs and I am interested in high-level observations.

### I agree with these points

1. Challenge window must still be long because everyone should get a chance to participate in the dispute game. I think this is important to understand and highlight, because NI fraud proofs provide the user experience of fraud proofs, not of validity (ZK) proofs. NIFP systems must be judged by the standards of optimistic systems, which is reflected by L2BEAT labeling BOB as Optimistic Rollup.
2. Liveness is not 1 of N. In the worst case (everything is challenged by an attacker) the defender is forced to prove every single transaction on L2. No matter the specific costs / hardware requirements, this is out of scope for regular users. This attack vector is unique to NIFP and IMO it presents the biggest challenge.

Out of these points, 1 is an intrinsic property of NIFP that we must accept, however I think that 2 can be mostly mitigated with a good design.

### How to mitigate Liveness problem (aka points I disagree with)

1. First things first, under the Transaction Reordering assumptions of the blogpost, the NIFP game indeed fails the liveness in the sense that a regular user will never be able to secure the L2. If an attacker can steal any ZKP submitted by a defender onchain (e.g. by frontrunning), they can overcome (some) slashing by pretending to be the honest party and not bearing any costs of generating ZKP. To me, good news is that in this case L2 essentially becomes a validity L2, where the chain progresses at the price of proving all trxs. I think this is still a good outcome for L2 in the scenario when a single entity controls L1 block building, but I disagree that we should work under this threat model. @GCdePaula could you please elaborate on how Dave would perform under such conditions?
2. I disagree that “single unit of honest resources (e.g., capital and computation) committed to securing the Layer 2“ is a good definition of one honest validator for NIFP. Proving markets are already live, and IMO it is reasonable to assume that an honest validator can outsource proof generation (one can also rent a cloud GPU). The cost of generation must be paid by the malicious attacker in the end, so an honest defender can afford pay a prover up front (consider it a part of defender’s bond). A conclusion I make here is: challenger bond must be bigger than proving costs for a disputed batch and at least a part of it must be given to the defender to cover proving costs.

### Additional points to highlight

1. Prover killer blocks is an attack surface for NIFP. Prover killer blocks are blocks that are extremely hard / expensive to proof, or they could even crash the prover due to a bug (see Unaligned Incentives: Pricing Attacks Against Blockchain Rollups on arXiv for more info). If a malicious attacker recognizes that a proposed batch contains such a block, they could exploit the fact that defender will struggle greatly with proving this block. Attacker could potentially create prover killer blocks on L2 themselves. I think, this is the biggest risk for ZK-based NIFPs and more research is needed to mitigate it.
2. Simplified NIFP game lifecycle. Once a challenge for a particular state transition is resolved with a ZKP, there could be no other parallel disputes, this game is immediately  finalized. Also, a single defender can dispute multiple challengers for the same game by submitting a single ZKP. IMO this feature of ZK-based FP games makes the design a bit simpler and also reduces challenger attack surfaces.

### Conclusion

I don’t view ZK-based NIFP as critical as Gabriel. IMO they offer a nice alternative for interactive FP, simplifying the challenger / defender design but introducing ZK-related risks. None of these is ultimately superior, but we need more comparative data to tell good designs from bad designs.

---

**GCdePaula** (2025-10-02):

Hi Sergey! Thank you for the thoughtful and constructive reply.

We’re glad to see we are in strong agreement on two of the most critical findings: that **the challenge window must still be long** and that NIFP systems must be judged by the standards of optimistic systems.

Furthermore, your characterization of the **1-of-N progress** as the “biggest challenge” and a vector “unique to NIFP” captures the issue we raised. This is a great starting point.

---

### On Chain Progress

You noted that under our assumptions, the NIFP game fails liveness for a regular user. To be precise, a regular user can *secure* the L2, but they cannot guarantee its *progress*. We were careful in our article to state that while NIFPs are 1-of-N for security, they are not 1-of-N for progress.

This 1-of-N liveness gap is not solved by delegation. While tools like cloud services are powerful, they don’t change the fact that somewhere over the rainbow, there must be a supercomputer. Using a cloud service is a form of centralization, and prover markets introduce their own trust assumptions.

You suggested the “good news” in the worst-case scenario is that the L2 becomes like a validity L2. We believe this is not a good outcome; the system inherits the **costs of a validity L2 without its benefits** like fast finality. Since these costs are substantial, we have to ask: who operates this expensive infrastructure, and who funds it?

As we argued in the article, the answers to these questions are different for NIFPs versus ZK-rollups, leading to the unique coordination challenges we identified.

---

### On The Threat Model

You are right to pinpoint that our primary disagreement stems from the **threat model**. In our view, the ecosystem has a choice between two standards: a weak, overly optimistic model where transactions are processed without adversarial interference, or the strong, adversarial model that protocols like Arbitrum’s BoLD and our own Dave are built for. Our article exclusively uses the latter.

Dismissing a threat model as “too pessimistic” is not a substitute for a security analysis. If one believes an intermediate model is more realistic, the burden is on them to formally define it and prove their system is resilient under it. This raises a critical question: **why should the ecosystem accept a weaker security guarantee when protocols already exist that withstand this stronger, more realistic adversarial environment?**

Nevertheless, we continue to believe this stronger model is essential for several practical reasons:

- The “Dark Forest” is not a theoretical concept; adversarial transaction ordering via MEV and front-running is a daily reality on Ethereum.
- The current state of L1 block building is sufficiently centralized to make transaction ordering a threat.
- Most importantly, the ability to reorder transactions is a subset of the censorship power that all optimistic systems must assume an adversary possesses. To discard this assumption is to argue for a weaker security guarantee than the current industry standard.

You asked how Dave performs under these conditions. It was **designed precisely for this adversarial environment**. Its cost structure is fundamentally different from NI systems — Dave’s expenses are dominated by “in-protocol” fees (L1 gas), not *a priori* “out-of-protocol” costs (offchain compute). Mechanisms for this kind of in-protocol gas-sponsoring are possible, meaning that Dave is less vulnerable to the specific front-running and self-refutation attacks we described. Nevertheless, in the Dave paper, we described Dave’s costs without such a sponsoring mechanism; you can check in detail how Dave operates there!

---

### On Liveness Costs Mitigations

This brings us to your proposed mitigations for the cost of progressing the chain. Your argument that an honest validator can outsource proving and be reimbursed by the bond overlooks the central finding of the second half of our article: the **self-refutation attack**.

Because an adversary with reordering capabilities can effectively steal the reward, **reimbursement is not guaranteed.** Without guaranteed reimbursement, the entire economic model of outsourcing collapses, and the honest validator is exposed to the resource exhaustion attack, even if bonds are much larger than proving costs.

---

### On Your Additional Points

- Prover Killer Blocks: This is an excellent and important point. Thank you for raising it. We agree this is a significant, related risk for ZK-based systems and a valuable area for further research.
- Simplified NIFP Game: Can you expand on this?

---

Thank you again for the high-quality engagement. We agree with your conclusion that more comparative data is needed. We believe that this kind of open, rigorous debate, based on clearly defined security assumptions against nation-state adversaries, is the best way to tell the good designs from the bad.

Looking forward to continuing the discussion ![:heart:](https://ethresear.ch/images/emoji/facebook_messenger/heart.png?v=14)

---

**RogerPodacter** (2025-10-03):

Great post, [@GCdePaula](/u/gcdepaula)! I want to challenge you on two points.

## Worst-case “ZK costs without ZK benefits.”

In the worst case, must an NI system pays ZK costs **without** ZK benefits (fast finality). I agree it pays ZK costs; I disagree it loses the ZK benefit.

If you accept ZK proving costs as the price of admission, the worst case should also deliver the ZK upside: **finality immediately when a proof is included on L1**.

[The system we deployed for Facet](https://etherscan.io/address/0x686E7d01C7BFCB563721333A007699F154C04eb4#code) (better described as “single-round ZK-fault proof hybrid” than “NI”) attempts to achieve this by supporting two concurrent methods for advancing the chain. The chain can be advanced in a fixed interval by either:

**Validity path (baseline).** Anyone can post a validity proof for the next interval. This requires no bond and withdrawals against that root settle immediately. This is indistinguishable from a traditional validity rollup.

**Optimistic path (cheap path).** Anyone (or a whitelisted proposer, depending on config) can submit an optimistic proposal for the next interval by posting a **proposer bond**. Anyone can **challenge** with a **challenger bond**

- A challenged valid claim can be defended by posting a validity proof (with embedded beneficiary address). The prover receives the challenger’s bond, the original proposer receives their bond back.
- A challenger of an invalid claim receives the proposer’s bond. Your bond burning suggestion would be an improvement here.
- If someone proves the same L2 block on the validity path, the proof immediately resolves all fault proof games targeting the same L2 block.
- To keep spam bounded:

Fixed-interval cadence caps forward-looking proposals
- One proof wipes all bad same-height proposals; an improvement here might be “challenge-once ⇒ all same-height proposals count as challenged” so nothing at that height can timeout-finalize while any dispute/proof is in progress.

Overall:

1. Worst case costs and benefits of a ZK rollup (pay to prove but withdrawals are instant)
2. When there’s no controversy, nobody has to prove.

## (2) Threat model and “1‑of‑N.”

You describe a model where a single honest validator must be capable of defending against a powerful adversary. How does BoLD (as an example) meet this in practice? Today the deployed system can be overridden by a security‑council, and if you include them as an “actor” in the threat model, the proof system’s security is not 1-of-N but rather 4-of-12 (because at least 4 honest actors are required to block).

This isn’t unique to BoLD—most live systems have security councils and NI systems are no exception. My objection is only to using an idealized “1-of-N” benchmark to evaluate NI when established proof systems do not meet this criterion in the context where it matters most: protecting assets of real users.

So I’d reframe the question from “should optimistic rollups be re‑architected around NI?” to “how do we actually achieve 1‑of‑N end‑to‑end?” My view: progress likely comes from combining fault proof and validity proof mechanics, not picking “the best one” in isolation.

---

**GCdePaula** (2025-10-04):

Hi Tom, thank you for the thoughtful and substantive reply. Your points get to the core of the design trade-offs, and this is a great opportunity to clarify our perspective.

### 1. On the Hybrid Design and its Trade-offs

You’re right that a hybrid design offers a choice between two worlds. In a sense, this is true: the system provides a choice between **expensive speed** (by using the validity path, which is functionally a ZK-rollup) and **cheap slowness** (by using the optimistic path, which requires a long challenge window).

This flexibility is an interesting engineering trade-off. However, it’s important to distinguish this from the “best of both worlds” narrative of achieving *cheap speed*. Our analysis focuses on the properties of that “cheap, slow” optimistic path, which, as we’ve established, requires a long challenge window to be safe against censorship under the established threat model.

### 2. On the Path to 1-of-N Security and Progress

You raised a great question about how any system, including Dave, can achieve 1-of-N security and progress in practice against a well-funded adversary. This is a common and understandable point of skepticism. The intuition is that a rich attacker can always overwhelm an honest defender through resource exhaustion.

Resource exhaustion attacks become viable when an honest validator must personally refute every bad claim. This causes the defender’s effort to scale **linearly** with an attacker’s resources, which is untenable in a permissionless setting.

Dave is designed to invert this dynamic. Instead of a linear 1-vs-N fight, its interactive game forces the adversary’s own Sybils to dispute one another. This makes the defender’s effort scale **logarithmically** with the number of Sybils, giving them an exponential resource advantage over the adversary. This cost asymmetry makes resource exhaustion attacks economically impossible in practice, allowing a single honest party with modest resources to secure and progress the chain, even against a nation-state-level adversary. Take a look at the [paper](https://dl.acm.org/doi/10.1145/3734698) for more details.

This brings us to your point about security councils. Our discussion focused on the **theoretical properties of the underlying algorithms,** rather than the current development stages of specific protocols that may have “training wheels”. Our point is that if the underlying algorithm isn’t provably 1-of-N resilient against the established threat model, then the training wheels can never be reasonably removed:

- Algorithms with 1-of-N guarantees like Dave have a credible path to removing their training wheels after sufficient testing and auditing.
- Protocols that lack this underlying resilience may not have a viable path to ever operating without a multisig override.

Our research focuses on these theoretical properties because they are the necessary foundation for achieving true, trust-minimized security in the future.

### A Collaborative Path Forward

We believe the work ZK teams are doing on reducing the costs of proving is impressive and vital for the entire ecosystem. Our hope is that the same level of innovation and rigor can be applied to the designs of the fraud proof game itself.

We are confident that NI systems and their theoretical guarantees can be significantly improved. We look forward to engaging with future work that formally specifies and rigorously analyzes the resilience of their systems against the established adversarial models.

---

**RogerPodacter** (2025-10-06):

## Hybrid Designs

I agree the “fast-cheap” narrative is wrong, though if the ZK Fault proof approach can be part of an overall proof system that improves on the straight validity proof benchmark that’s a great result!

At least the steel man should be modeled this way unless there’s a compelling reason to ever *not* have a hybrid system.

## Security Councils

I believe the existence of security councils presents a larger problem for your position than you suggest because their prevalence *is* *itself* evidence as to the theoretical properties of Dave et al.

Your claim is that Dave (or BoLD or similar) offers 1-of-N security and your evidence is the arguments in your paper and the fact that these arguments have been scrutinized by other experts.

On the other hand, there is the evidence that rollup operators, who have the maximum incentive to get this right and who are also experts in proof systems, refuse to run any of these things without a back door that has 4-of-12 security.

From a Bayesian perspective, this is significant evidence against the claim that Dave is 1-of-N, even in theory!

Is there another explanation? Maybe Dave is great in theory but untested and unaudited in practice. But do security councils fare better? Where is the peer-reviewed whitepaper on *them*, anyway?

Without a theory explaining the revealed preferences of today’s rollup operators I don’t think we can confidently claim *both* that certain algorithms achieve better than 4-of-12 security and also that this fact will play a foundational role in delivering trust-minimized security to real users.

