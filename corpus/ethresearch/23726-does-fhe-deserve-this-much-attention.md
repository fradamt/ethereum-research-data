---
source: ethresearch
topic_id: 23726
title: Does FHE deserve this much attention?
author: miha-stopar
date: "2025-12-22"
category: Privacy
tags: []
url: https://ethresear.ch/t/does-fhe-deserve-this-much-attention/23726
views: 298
likes: 8
posts_count: 3
---

# Does FHE deserve this much attention?

# Does FHE deserve this much attention?

I’d like to warmly thank Keewoo Lee, Michal Zajac, Nam Ngo, Rand Hindi, Roman Walch, and Thore Hildebrandt for their helpful feedback.

## TL;DR

- FHE is receiving increased attention because it promises fully general, composable computation over encrypted state without relying on trusted hardware. In practice, however, many current FHE-based blockchain designs (e.g., FHEVM-style systems) still rely on MPC committees for key management and decryption. Recent research, such as Scalable Private World Computer via Root iO, explores advanced cryptographic constructions (based on indistinguishability obfuscation) that aim to reduce or remove these committee-based trust assumptions.
- Many proposed FHE use cases (confidential DeFi, private tokens, private AMMs) have alternatives such as ZKPs, MPC, or TEEs, but each comes with trade-offs in composability, trust assumptions, interaction requirements, or deployability.
- FHE or MPC? MPC can be highly efficient and has seen real-world deployment for privacy-sensitive tasks, but typically assumes interaction and some form of committee or non-collusion model.
- Verifiable FHE (vFHE) is essential for trustless FHE-based applications, especially when encrypted computation is performed off-chain. Beyond blockchains, vFHE could also play an important role in AI settings, where verifiable guarantees about correct inference or training on encrypted data become increasingly relevant.
- For AI and machine learning, FHE offers a compelling long-term vision for non-interactive, privacy-preserving computation, but remains constrained by performance and engineering maturity, particularly for advanced models and complex workloads.
- Does FHE deserve the attention? Yes—but not as a silver bullet. Its value lies in the unique capabilities it enables—especially composable computation over encrypted state and reduced reliance on hardware trust—rather than in immediate efficiency or universal applicability.

## The Questions Behind the FHE Hype

During Devconnect in Buenos Aires, there were [numerous](https://fheorg.substack.com/p/fheorg-digest-36-fhe-at-devconnect) [discussions](https://www.youtube.com/watch?v=mGfx2EBckjI&t=76s) on **FHE**. I think FHE didn’t stand out as much at previous events.

The discussion often centered around questions such as:

1. What are some really convincing use cases for FHE in Web3?
2. For confidential tokens, do we really need fully homomorphic encryption? Isn’t homomorphic encryption enough? Aren’t confidential tokens just about additions and subtractions (balances)?
3. Isn’t FHE just a technique for MPC?
4. How important is verifiable FHE (vFHE), and when will it become practical to use in real-world applications?

I think all of these questions point toward an underlying concern: **does FHE deserve this much attention?**

I’m also adding a fifth point that was casually mentioned in several non-FHE-focused talks. I’m still wondering whether people meant it seriously or were simply echoing the current **AI hype**:

1. Ethereum can provide cryptographic assurances that AI models are trained and executed as intended.

Let’s take a closer look at each of the topics. In fact, they are more interconnected than they might seem at first glance.

## 1. Convincing Use Cases

We’ve already discussed potential FHE use cases in [this post](https://ethresear.ch/t/open-application-driven-fhe-for-ethereum/23044), but the truth is that there are many challenges, and it’s fair to question whether FHE is always the right approach. Some concerns are:

- Confidential DeFi needs mechanisms to safely handle events like liquidations without exposing private positions, which is difficult when state is encrypted.
- Private AMMs must retain enough market signal for prices and liquidity to function; without this, markets become harder to coordinate and less efficient.
- Sealed-bid voting and similar applications already have simpler alternatives such as MPC, encryption, commit–reveal, or even zk-based tallying.
- FHE-EVM represents, in my view, the necessary and “ultimate” direction for private on-chain computation. But today it still faces practical constraints—especially performance, latency, and the overhead of executing encrypted state transitions.

However, alternatives such as ZKPs, MPC, and TEEs each have important limitations and trade-offs:

- ZKPs can enforce constraints such as solvency or liquidation without revealing full positions, but they face well-known composability and modularity issues: complex multi-step state transitions often must be encoded as a single monolithic circuit; combining proofs across independent modules typically requires heavy aggregation; and dynamic or arbitrary logic over private data must be anticipated in advance, limiting flexibility. FHE, by contrast, naturally supports arbitrary composition of encrypted computations without circuit coordination or redesign.
- Threshold encryption and MPC can enable controlled disclosure or multi-party computation, but generally require interaction, timing assumptions, or fixed committees, making them less suitable for open, permissionless, asynchronous environments.
- TEEs offer strong performance but rely on significantly weaker trust assumptions, with a long history of side-channel attacks and broken attestation flows; in contrast, FHE provides privacy rooted entirely in cryptography rather than hardware.

While alternative techniques can approximate certain privacy properties, FHE stands out for enabling fully general, composable computation over encrypted state with significantly reduced cryptographic trust assumptions compared to hardware-based approaches.

At the same time, many practical FHE-based blockchain designs today—most notably [FHEVM-style systems](https://github.com/zama-ai/fhevm/blob/f2bcf811aa536cc59db08a52965c3a8443efd888/fhevm-whitepaper.pdf)—do not rely on FHE alone. In these architectures, a **trusted ad-hoc committee is still required to manage secret key shares and to perform decryption of output ciphertexts via MPC**, typically using threshold decryption protocols. While this construction prevents any single party from learning plaintext values, it reintroduces **committee assumptions, coordination requirements, and liveness dependencies** at the boundary of encrypted computation. The recent work [Scalable Private World Computer via Root iO](https://eprint.iacr.org/2025/2139.pdf) aims to reduce or remove these committee-based trust assumptions by applying advanced cryptographic constructions (based indistinguishability obfuscation).

## 2. Confidential Tokens and (F)HE

At first glance, **confidential tokens** seem remarkably simple. When Alice wants to transfer some amount of ETH to Bob, the operations involved appear to be nothing more than basic arithmetic:

- adding the transferred value to Bob’s encrypted balance
- subtracting the value from Alice’s encrypted balance

In practice, however, a confidential transfer must also ensure that the sender’s balance is **sufficient**. One approach, used in many **zero-knowledge–based designs** (e.g., [Zether](https://eprint.iacr.org/2019/191.pdf)), is to prove in zero knowledge that the value of newly created notes does not exceed the available balance. While effective, this treats balance sufficiency as an **external authorization check** and requires careful sequencing to avoid race conditions when multiple transfers are constructed concurrently.

By contrast, an **FHE-based approach** allows the balance check to be performed *within the encrypted state itself*. The transfer logic can be expressed as a **conditional encrypted update**—for example, subtracting the transfer amount *if and only if* it does not exceed the encrypted balance, and otherwise producing a zero-value transfer. This ensures that **overspending cannot occur**, even transiently, and reduces correctness conditions that depend on transaction ordering by enforcing **atomic updates over encrypted state**.

More broadly, **homomorphic comparison** enables balance checks to compose naturally with other encrypted control-flow logic, rather than being enforced via standalone proofs. This distinction becomes increasingly important in **stateful and programmable confidential applications** beyond simple payments.

However, this additional expressiveness comes with a cost. **Comparisons are substantially more expensive than simple arithmetic** in homomorphic encryption. In FHE schemes, comparisons typically require evaluating the **sign of an encrypted value**, which in turn involves **sequential bootstrapping operations**. As a result, comparison incurs significantly higher computational cost than additions or subtractions, and this cost generally grows with the **precision or magnitude** of the values being compared. Techniques for homomorphic sign evaluation are studied in works such as [Large-Precision Homomorphic Sign Evaluation using FHEW/TFHE Bootstrapping](https://eprint.iacr.org/2021/1337.pdf) and related literature, which consistently identify comparison as a **challenging primitive**.

That said, **recent engineering advances**—particularly **GPU-accelerated implementations of TFHE-style schemes**—can make comparisons practical in concrete settings, often bringing their cost closer to that of large-precision arithmetic operations.

## 3. MPC instead of FHE?

At a high level, **FHE and MPC** both aim to enable computation on private data, which naturally raises the question of whether FHE is simply a specialized form of MPC. While there are conceptual connections, the two paradigms differ in where privacy is enforced, how computation proceeds, and what assumptions are required in practice.

**MPC** protects data by splitting it into secret shares held by multiple parties who compute collaboratively. This approach can achieve excellent performance. However, MPC fundamentally relies on **non-collusion assumptions**, **multiple online participants**, and **interactive communication during computation**, which can be challenging in fully permissionless or highly asynchronous environments.

**FHE**, by contrast, enables computation directly over encrypted state. A single party can apply arbitrary programs to ciphertexts without interacting with others during execution, making FHE conceptually well aligned with blockchain execution models. This allows **general, composable, and stateful computation over private data**, including dynamic control flow that does not need to be fixed in advance—something that is difficult to achieve with ZK proofs or interactive MPC alone.

In practice, however, FHE systems face additional challenges. As discussed earlier, **key management and output decryption are often handled via threshold MPC**, meaning that many deployed FHE designs still rely on **non-collusion and committee coordination** at the decryption boundary, even if the computation itself is non-interactive.

On **verifiability**, MPC currently has an advantage. Proving correctness of MPC executions is comparatively straightforward because most SNARK systems are naturally compatible with MPC-style computation. This has enabled practical systems where MPC execution can be paired with optional zero-knowledge proofs—for example, collaborative proving using MPC-oriented tooling such as [TACEO’s co-SNARK library](https://github.com/TaceoLabs/co-snarks). By contrast, **verifiable FHE remains an active research and engineering problem**, with higher overheads and less mature tooling.

Both **FHE** and **MPC** are being actively explored as foundations for privacy-preserving computation in Web3, with a growing ecosystem of projects pushing each approach toward practical deployment.

On the **FHE** side, [Zama](https://zama.ai) is developing the FHEVM stack, which aims to enable confidential smart contracts by allowing EVM programs to operate directly over encrypted state. [Fhenix](https://www.fhenix.io) is pursuing a similar goal, focusing on confidential execution for EVM-compatible environments through FHE coprocessors and developer tooling designed to integrate with existing smart-contract workflows. [Enclave](https://enclave.gg) explores encrypted execution from a more protocol-oriented perspective, combining FHE with cryptographic verification techniques to support correctness and controlled output disclosure in decentralized settings.

On the **MPC** side, [Partisia Blockchain](https://partisiablockchain.com) operates a standalone Layer 1 that integrates secure multi-party computation directly into its execution model, enabling smart contracts that can process private inputs across a distributed set of MPC nodes. [Nillion](https://nillion.com) takes a different approach, offering a dedicated off-chain network for private computation and storage based on MPC-style techniques, designed to interoperate with existing blockchains rather than replace them. Soda Labs’ [gcEVM](https://www.sodalabs.xyz/solutions-gcevm/) explores how MPC—specifically garbled-circuit–style protocols—can be embedded into an EVM-compatible execution environment, allowing smart contracts to handle confidential values while retaining familiar Ethereum tooling.

Together, these projects illustrate two parallel directions for privacy in Web3: FHE-based systems that emphasize non-interactive computation over encrypted state, and MPC-based systems that rely on distributed execution among multiple parties. In practice, both approaches are increasingly explored side by side, and in some cases combined, as the ecosystem searches for scalable and composable ways to bring confidentiality to decentralized applications.

## 4. Why vFHE Matters

There seems to be general agreement that **verifiable FHE (vFHE)** is an important direction. To understand why, let’s examine what it would mean for FHE to enable private smart contracts on Ethereum.

**Ethereum is a world computer:** a decentralized platform that executes arbitrary programs and reaches global consensus over a shared state. But all inputs, state, and execution traces are **public by default**. FHE offers a path toward privately computing over encrypted data, potentially enabling a **“private world computer”** where users contribute confidential inputs without revealing them.

In practice, however, FHE is **not as naturally aligned with blockchains as SNARKs**—ciphertexts are large, bootstrapping is expensive, and on-chain execution is infeasible. As a result, most FHE designs today rely on off-chain coprocessors that perform encrypted computation and return results back to the chain.

This introduces a key problem: **how do we trust the result of an encrypted computation?** FHE alone offers no way to verify correctness.

**Verifiable FHE (vFHE)** solves this: it allows a compute node to produce a succinct proof that the encrypted output is the result of correctly executing the intended computation.

But vFHE unlocks other important capabilities:

- iO (Indistinguishability Obfuscation): In Root iO, indistinguishability obfuscation is used within an FHE-based evaluation pipeline to eliminate the need for a dedicated decryption committee, with verifiable FHE serving as one of the crucial components.
- Web3 + AI: private inference and collaborative learning on encrypted models.
With vFHE, the output of these encrypted computations becomes trustless, auditable, and verifiable, enabling decentralized AI systems that do not rely on trusted execution or replication.

How practical this is — and how soon it will become practical — remains an open question, and people have [different opinions](https://youtu.be/C-kF0gplCto?t=7813) about that.

## 5. Ethereum + AI

Let’s now move to the question of how Ethereum and AI intersect.

Today’s most prominent AI use case is **large language models (LLMs)**. They are trained on unencrypted data, and this will likely remain the case. However, user queries are also **not encrypted**, and hopefully this will not remain so.

It’s a terrifying thought that, in the near future, as we increasingly interact through calls or virtual-reality spaces, an LLM could reconstruct a **disturbingly accurate digital twin** of ourselves. All the data needed to build such a twin sits on the LLM provider’s servers, entirely outside our control, which means they could instantiate and use it at any time. An agent based on our digital twin could then move through the Internet **as if it were us**.

FHE could prevent this, but today’s implementations are still far too slow to run advanced AI models. Would vFHE be needed in this setting? It certainly wouldn’t hurt, but in many cases LLM providers are **incentivized to return correct inferences** — producing the best answers is in their own interest. Still, as we will see below, there are scenarios where this incentive is weaker or ambiguous, and **verifiability becomes far more important**.

But there are other **unsettling scenarios**. For instance, robotics will likely become a **significant part of our daily lives**. It’s easy to imagine small household robots handling tasks such as repairing appliances, cooking meals, doing laundry, cleaning hard-to-reach areas, monitoring home safety, organizing clutter, tending indoor gardens, or assisting elderly family members.

These activities are far more complex for AI than anything current LLMs can handle. Indeed, Yann LeCun [has recently launched](https://www.cnbc.com/2025/11/19/meta-chief-ai-scientist-yann-lecun-is-leaving-the-company-.html) a new effort focused on AI systems that learn through **spatial and embodied interaction**. Training such models will require vast amounts of real-world data.

The question is: **are we willing to reveal the full layout of our home, the state of our appliances, our cooking habits, our laundry routines, our clutter patterns, our safety-monitoring needs, or even how we care for elderly family members — all just to train these systems?**

These data should, of course, be **encrypted before being sent out**. But encryption alone is not enough: **who will verify that people are actually submitting real, unaltered data?** Who will ensure that the information hasn’t been manipulated or fabricated to game the system?

And beyond data integrity, **who will check that the training process itself is carried out correctly**—that the model isn’t being subtly biased, tampered with, or optimized in ways that serve the provider rather than the user?

Finally, **who will guarantee that inference results are produced faithfully**, without hidden filtering, ranking, surveillance, or other invisible interventions?

Taken together, these questions suggest that **verifiability in AI** could play an increasingly important role. While encryption alone protects privacy, verifiability—when coupled with **a blockchain as an independent, transparent audit layer**—offers a path to ensuring that data submission, training, and computation are all performed correctly. So yes, I think people are right when they draw connections between AI and Ethereum.

## Replies

**auryn** (2025-12-23):

Great write-up, [@miha-stopar](/u/miha-stopar)!

There are two nuances which I think are worth making more explicit:

1. ZKPs, MPC, and FHE (along with iO if/when it becomes practical) do not directly compete with one another. They are different tools with distinct properties. There is some overlap, but I’d position them as complementary technologies much more than competitive. I gave a talk on this at CC2 last month.
2. iO is presented as somewhat of a silver bullet to “reduce or remove committee-based assumptions”. This is true only for a limited class of programs—where (i) all sensitive individual output is encrypted to keys specified by those individuals and (ii) no aggregate output is produced if any of the committed to inputs are omitted—and implies a trade-off between fault tolerance, composability, and privacy.

---

**SeunghwanLee257** (2026-02-04):

Hi [@miha-stopar](/u/miha-stopar) — on the **vFHE** point: we strongly agree this is a key missing piece, and we’ve been actively exploring SNARK-friendly paths.

We’ve run hands-on experiments that prove the RLWE encryption/logging step inside SNARKs (both in PLONK-style and Groth16-style constraint systems) as a warm-up to understand where prover time concentrates in practice.

Building on this experience, we’re also beginning to incrementally prove larger components, including attempts toward proving the full gate bootstrapping procedure.

While the end-to-end pipeline is not fully practical yet, we’re exploring whether we can improve efficiency by targeting the Plonky3 stack, especially over the BabyBear field (prime p = 15·2^27 + 1) or M31 as prime field. Our modulus is a composite q = 12289·13313 (two 14-bit primes), and we suspect that this “small-integer / CRT-friendly” structure may map more favorably to BabyBear/M31-style arithmetization, enabling more efficient proofs of selected FHE sub-steps compared to proving an entire FHE pipeline on the characteristic p >>= 2^{64}.

We’ll be happy to share progress and benchmarks as the work evolves.

Seunghwan Lee (X: @scarrots) — waLLLnut

