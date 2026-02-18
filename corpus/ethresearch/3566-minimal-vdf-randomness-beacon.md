---
source: ethresearch
topic_id: 3566
title: Minimal VDF randomness beacon
author: JustinDrake
date: "2018-09-26"
category: Sharding
tags: [random-number-generator]
url: https://ethresear.ch/t/minimal-vdf-randomness-beacon/3566
views: 22495
likes: 47
posts_count: 39
---

# Minimal VDF randomness beacon

**TLDR**: We present a minimal randomness beacon using a Verifiable Delay Function (VDF). We argue for the safety and liveness of the RANDAO + VDF scheme and conclude with some discussion points.

*Thanks to [@prateek](/u/prateek) and [@mihailobjelic](/u/mihailobjelic) for feedback.*

# Construction

Assume a global clock and split time into contiguous 8-second blocks and 128-slot epochs. Each epoch i produces 32 bytes of (biasable) entropy e_i to which correspond 32 bytes of (unbiasable) randomness r_i. In a recursive fashion, the beacon chain proposers of epoch i (one per slot) are sampled using past randomness r_j (i.e. j = i - N for some suitable constant N).

**Biasable entropy (RANDAO)**

Every beacon chain proposer is committed to 32 bytes of local entropy. (In practice a chain of commit-reveals is setup with a hash onion for validator registration.) Beacon chain proposers may reveal their local entropy by extending the canonical beacon chain with a block. Honest proposers are expected to keep their local entropy private until their assigned slot.

The beacon chain maintains 32 bytes of onchain entropy by XORing the local entropy revealed at every block. Denote by e_i the onchain entropy at the last slot of epoch i.

**Unbiasable randomness (VDF)**

Let D be a (verifiable) delay function which takes 32-byte inputs x and integer time parameters T, and which returns 32-byte outputs y = D(x, T). We assume commodity VDF hardware can evaluate outputs no slower than A_{max} times what an attacker can do with proprietary hardware. That is, A_{max} is the maximum attacker advantage.

We fix the time parameter T so that the commodity hardware takes A_{max} epochs (i.e. 8\times 128\times A_{max} seconds) to evaluate outputs and we define r_i = D(e_i, T). Anyone can run the commodity VDF hardware to compute and broadcast the r_i (with the evaluation proofs allowing fast verification) to become a so-called evaluator. Honest beacon chain proposers are expected to include the r_i (and corresponding evaluation proofs) onchain.

# Safety and liveness arguments

We make three further assumptions:

- Majority validator honesty: We assume 2/3 of the validators are honest. (This assumption is also made for sharding.)
- Minority validator liveness: We assume up to 3/4 of the honest validators are offline, possibly permanently. (This assumption also captures validator censorship, e.g. networking DoS.)
- Altruistic evaluator: We assume at least one altruistic evaluator runs the commodity VDF hardware and broadcasts r_i = D(e_i, T) (with an evaluation proof) at the end of epoch i + A_{max}.

**Safety argument**

We argue that the randomness r_i is unbiased. Using a recursion argument, let’s assume that r_j (where j = i - N) is itself unbiased. (The first few values of r_i can be set using a PoW blockhash.) Then using the validator honesty and liveness assumptions the probability that epoch i has no honest proposer is bounded above by \big(1-\frac{2}{3}\times\frac{1}{4}\big)^{128} < 2^{-33}, i.e. is negligible.

Now assume an attacker runs proprietary hardware that is A_{max} times faster than the commodity hardware. Such an attacker can compute D(e_i, T) for varying e_i in exactly one epoch. Because the honest proposer in epoch i reveals his local entropy no earlier than epoch i, and the attacker grinding opportunity on e_i is limited to epoch i, grinding is impossible and r_i is unbiased.

**Liveness argument**

The altruistic evaluator assumption guarantees that the randomness r_i (with an evaluation proof) corresponding to epoch i is available offchain by the end of epoch i + A_{max}. As argued above, each epoch has at least one honest proposer who can guarantee inclusion of r_i by the end of epoch i + A_{max} + 1.

# Justifying the assumptions

**Safety argument**

The key assumption for the safety argument is the existence of commodity VDF hardware that is no slower than A_{max} times what proprietary hardware can achieve. The current plan is for the Ethereum Foundation and Filecoin (and possibly others like Chia and Solana) to jointly develop a VDF ASIC to get a reasonable A_{max}.

Rough estimates suggest that a budget of $20m-$30m is sufficient for the commodity ASIC to support A_{max} = 10 for 5 years. This ASIC would be replaced within 5 years as part of an upgrade to a quantum-secure VDF. (Similar to BLS signature aggregation, the [initial VDF scheme](https://eprint.iacr.org/2018/623.pdf) is not quantum-secure.)

**Liveness argument**

The key assumption for liveness is the existence of an altruistic evaluator. Assuming the commodity hardware is widely distributed for free across the Ethereum community, it is reasonable to assume at least one altruistic evaluator despite the lack of in-protocol rewards.

Indeed, similar to how [14,000+ nodes](https://www.ethernodes.org/network/1) are operated without in-protocol rewards, we can expect the community (enthusiasts, developers, investors, dApp operators, the Ethereum Foundation, etc.) to altruistically run VDF evaluators around the world. Similar to enthusiasts overclocking CPUs and GPUs, we can expect some VDF ASICs to get overclocked.

# Discussion

*Other randomness constructions*

- Biasable randomness: Most known randomness beacons are biasable via last revealer(s) attacks. This includes PoW (Bitcoin, Ethereum 1.0), RANDAO + VRF (Algorand, Cardano), RANDAO + PVSS (Tezos), RANDAO + low-influence functions (Polkadot).
- Dfinity’s randomness: The threshold relay scheme stands out as not being biasable. Unfortunately, the beacon can stall if even a minority (e.g. 15%) of honest players go offline. A design goal for Ethereum 2.0 is to survive WW3 making strong liveness non-negotiable.
- VDF-based randomness: The only known randomness beacons that have both strong safety and strong liveness use a VDF.

*Practical considerations*

- Baseline security: If the VDF breaks down completely (e.g. a quantum computer makes outputs computable with no delay) the randomness beacon falls back to RANDAO security.
- Validator/evaluator decoupling: Validators only need to verify VDF outputs using evaluation proofs, hence do not need to be evaluators. Evaluators do not need to be registered or collateralised, hence do not need to be validators.
- Ethereum 2.0 roadmap: The Ethereum 2.0 roadmap is independent of the VDF ASIC. A VDF upgrade strengthening RANDAO can come with phase 1 (sharding data layer), phase 2 (sharding state layer), or later. The development of commodity hardware will likely take at least 18 months.
- ASIC power usage: It is estimated that each evaluation core in the VDF ASIC would consume less than 10 Watts even under extreme voltage and temperature. Assuming 10,000 active VDF cores running at 10 Watts, that is ~23,000 times less power consumption than today’s PoW mining in Ethereum 1.0.
- Bandwidth overhead: The beacon chain must include one VDF output and evaluation proof per epoch. With the Wesolowski VDF (using a 2048-bit RSA modulus, or a 2048-bit class group discriminant) that corresponds to 512 bytes of overhead per epoch, i.e. 0.5 bytes per second.
- Computation overhead: Verifying a VDF output against an evaluation proof takes ~1 ms of CPU time for the suggested VDF (see above). That corresponds to ~30 seconds of CPU time overhead per year. No significant network-level DoS vector is introduced thanks to the low verification overhead per VDF output.

*Optional infrastructure*

- Inclusion rewards: It is particularly easy to give an inclusion reward (e.g. 0.1 ETH) to the first beacon chain proposer that includes randomness r_i. This reward would help prevent rational proposers slipping into laziness. It may also incentivise sophisticated validators to overclock the commodity VDF ASIC as an indirect evaluation reward (see below).
- Evaluation rewards: At the cost of added protocol complexity, VDF evaluators can receive direct in-protocol rewards. Watermarking the evaluation proofs to evaluator identities would be required (and is easily done). Note that if evaluation rewards are non-existent or small (e.g. $3K per day, ~$1m per year) the development of a proprietary VDF ASIC seems unlikely.
- Difficulty mechanism: At the cost of added protocol complexity, a difficulty scheme (e.g. see discussion here) can be added to dynamically adjust the time parameter T over long timescales (e.g. decades) without making use of hard forks every few years. Until a quantum-secure VDF is implemented a difficulty adjustment mechanism is likely unnecessary.

*Benefits of unbiasability*

- Consensus parameters: With unbiasable randomness the relevant consensus parameters (e.g. honesty and liveness assumptions, committee sizes and thresholds) do not have to include safety margins to mitigate bias. Alternatively, the safety margins can stay, making the design stronger.
- Formal analysis: With unbiasable randomness the analysis of the consensus layer is greatly simplified allowing for rigorous safety proofs and formal verification. When validators can bias the randomness complicated games arise and it is unclear whether such games are fully understood.
- Randomness opcode: dApps (e.g. lotteries) get programmatic access to unbiasable randomness via an opcode. Replicating an equivalent layer 2 randomness beacon without protocol-level support is hard.
- Competitiveness: Unbiasable randomness at the protocol-level keeps Ethereum 2.0 competitive with other third-gen blockchains (e.g. Dfinity and Filecoin).

## Replies

**Mikerah** (2018-09-26):

Would it be valuable to try to construct a VDF that is not dependent on choosing a secret modulus or more generally not dependent on some secret? Would it be possible to construct a VDF based on groups of known order?

With the current direction, it would require a carefully designed ceremony (a la Zcash) in order to make sure that no one knows the modulus and its factorization.

---

**kladkogex** (2018-09-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> The threshold relay scheme stands out as not being biasable. Unfortunately, the beacon can stall if even a minority (e.g. 15%) of honest players go offline.

It loos like one can actually design a threshold signature scheme where half of the good guys guys can go off line

A simple example:

1. You have less than 1/3  N bad guys
2. The random beacon R is “1/3 N out of N” threshold signature of the epoch number.
3. Everyone first pre-commits a hash of the signature share (pre-commit phase)
4. Everyone reveals the signature share S_i (reveal phase)
5. Once 1/3N signature shares are revealed they are combined into a threshold signature.

In this scheme only half of the good guys need to be online in order for the system to work …

Bad guys can not derive the number unless at least one good guy reveals his share

---

**denett** (2018-09-27):

I guess you assume all live validators will participate in every round. If you use committees (like of size 128 as proposed above), the chances of failure are not negligible.

With the VDF beacon you only need 1 honest validator per committee of size 128. With your proposed threshold signatures you need at least 43 honest validators per committee of size 128.

With a third of the validators being honest and live, the chance to get a bad committee is around 50%. With half of the validators honest and alive the chance is 0.006% (according to my quick and dirty excel sheet).

It will do better with bigger committees, but that will increase the overhead.

---

**terence** (2018-09-28):

Will VDF output & evaluation proof be part of crystallized state?

Also, what happens in an event all proposers fail to include R1 or its proof during epoch 1? When epoch 2 starts, the proposers will have to include R2 right?

---

**Mikerah** (2018-09-28):

Also, [@JustinDrake](/u/justindrake) have you given any thoughts to Tor’s randomness beacon? I know the use case is different but how does it compare to the other blockchains’ randomness beacons and would it be possible to analyze it to determine if it could be an alternate candidate in addition to the current RANDAO+VDF scheme.

---

**kladkogex** (2018-09-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> With the VDF beacon you only need 1 honest validator per committee of size 128. With your proposed threshold signatures you need at least 43 honest validators per committee of size 128.

This may be either good or very bad.

For VRF if there is a split between Europe and the States, there will be two different random numbers generated R_1 and R_2 and this is bad. There will be no way to put R_1 and R_2 together again! You will have an unfixable fork!

Therefore,  the fact that you only need one good guy to generate a random number can be a catastrophe under some circumstances.

Basically in case of a network split you will end up with two groups of good guys generating two different random numbers, these two random numbers leading to a selection of two different sets of validators and then the entire system irrecoverably splitting and crashing!

Contrary to that, the threshold signature algorithm will stall for the duration of the split, and then work again perfectly, which is actually exactly the behavior you want!

---

**JustinDrake** (2018-09-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/mikerah/48/1616_2.png) Mikerah:

> Would it be valuable to try to construct a VDF that is not dependent on choosing a secret modulus or more generally not dependent on some secret?

In [the family of VDFs we are considering](https://eprint.iacr.org/2018/712.pdf) there are at least 4 setups which could work in practice. Two are fully trustless (class groups, [nothing-up-my-sleeve RSA moduli](https://ethresear.ch/t/generating-rsa-ufos/3401)), one is quasi-trustless (RSA MPC), and one is trusted-in-theory-but-ok-in-practice ([RSA-2048](https://en.wikipedia.org/wiki/RSA_numbers#RSA-2048)). IMO the best-case scenario is for the RSA MPC to be feasible.

(As a side note, the modulus is always public. It’s the factorisation of the modulus that should be secret.)

![](https://ethresear.ch/user_avatar/ethresear.ch/_charlienoyes/48/2322_2.png) _charlienoyes:

> PoT ceremony to proceed publicly

Note that the ceremony for an RSA modulus uses different crypto to the Powers of Tao ceremony.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> one can actually design a threshold signature scheme where half of the good guys guys can go off line

As indicated by [@denett](/u/denett) this does not work because the sampling process will weaken your honesty assumption. (Dfinity’s sampling weakens the global 2/3 honesty to 1/2 local honesty.) Sampling is required because the Distributed Key Generation (DKG) scales quadratically with the number of participants, and in practice you can’t get much more than 1,000 participants.

Another thing to consider is that there are two ways in which the Dfinity beacon can fail. Citing the whitepaper: “We treat the two failures (predicting and aborting) equally”. By improving liveness you make the readomness beacon easier to predict.

Finally, the RANDAO + VDF approach allows for arbitrarily low liveness assumptions. (For example, we could have a 1% liveness assumption by making the RANDAO epoch longer.)

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> Will VDF output & evaluation proof be part of crystallized state?

In practice the actual randomness (as returned by the randomness opcode) will be a 32-byte hash of the VDF output. As such, the VDF outputs and the evaluation proofs are just “witnesses” and do need to be part of the beacon state. As for VDF output hashes, it may make sense to store the last n (e.g. n = 1024) in the state and push the rest to a [double-batched Merkle accumulator](https://ethresear.ch/t/double-batched-merkle-log-accumulator/571).

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> what happens in an event all proposers fail to include R1 or its proof during epoch 1? When epoch 2 starts, the proposers will have to include R2 right?

The VDF output r_i should get included by epoch i + A_{max} + 1. From the point of view of the application layer, the randomness opcode will return `0x0` until r_i is included onchain. So any delay should be handled by the application.

From the point of view of RANDAO using the r_i we can set N be to conservative, e.g. N = A_{max} + 3. In case of a catastrophic failure we need the spec to specify some sort of behaviour. My gut feel is that gracefully falling back to RANDAO is perfectly OK.

![](https://ethresear.ch/user_avatar/ethresear.ch/mikerah/48/1616_2.png) Mikerah:

> have you given any thoughts to Tor’s randomness beacon?

I had a quick look and it seems to be [basically RANDAO](https://lists.torproject.org/pipermail/tor-dev/2015-August/009189.html).

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> there will be two different random numbers

Right, forkfulness at the RANDAO level is a grinding opportunity for RANDAO + VDF. Applications that need to protect themselves from this grinding opportunity (e.g. billion-dollar lotteries) need to wait until Casper finality of the randomness to get the similar guarantees to Dfinity/Tendermint.

Strong liveness allows dApps (if they so choose to) to operate in the context of weak finality when  strong finality is not available. In other words, strong liveness pushes the “safety vs liveness” tradeoff to the application layer instead of stalling all dApps unnecessarily when finality cannot be reached.

---

**seresistvan** (2018-09-29):

Is there any known ongoing research in evaluating and applying permutation polynomials over finite fields as VDFs? Why are not they considered as potential candidates [@JustinDrake](/u/justindrake)? Is there some strong security assumption which is kinda prohibitive? Or is it just too complex for the EVM?

---

**MihailoBjelic** (2018-09-29):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Basically in case of a network split you will end up with two groups of good guys generating two different random numbers, these two random numbers leading to a selection of two different sets of validators and then the entire system irrecoverably splitting and crashing!

I fail to understand why would the fork be unfixable and why would the system crash? As far as I know, Eth 2.0 has the “bleed out” model for offline validators, which gives us around 12 days to resolve the partition? Only after that period is when the fork will become permanent, and the system will not crush in any of these two cases.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Contrary to that, the threshold signature algorithm will stall for the duration of the split, and then work again perfectly, which is actually exactly the behavior you want!

I generally favor consistency over availability (that’s why I like e.g. Dfinity’s beacon or Tendermint consensus), but there’s a really strong argument in favor of Ethereum’s (and Bitcoin’s) “WW3-proof” approach - if you keep your assets on a blockchain, you want them to be available all the time, **especially** if there’s some sort of catastrophe going on. Unfortunately, Dfinity and Tendermint can not guarantee that. How do you argue that?

---

**denett** (2018-09-29):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> For VRF if there is a split between Europe and the States, there will be two different random numbers generated R1R_1 and R2R_2 and this is bad. There will be no way to put R1R_1 and R2R_2 together again! You will have an unfixable fork!

Generating two different numbers when there is a chain split is not a problem when the chain’s have not yet been finalized. After a reconnect, one chain can win and the other is discarded.

I think the splitting does not depend on the random number beacon, but is a design choice of Casper. Even with your beacon the chain can split, because you will only need one third of the validators on every chain to continue. After Casper slashed validators on the other side of the ocean for not participating, the random numbers will diverge en we might end up with two finalized blockchains.

If you use the 1/2N threshold, you can not have a chain split, but the chain can halt when less than half of the validators are good and online.

---

**JustinDrake** (2018-09-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/seresistvan/48/1649_2.png) seresistvan:

> research in evaluating and applying permutation polynomials over finite fields as VDFs

The permutation polynomials have been considered:

1. Sloth: Only provides a constant gap between evaluation time and verification time. For it to be practical to build a Sloth VDF ASIC the multiplier needs to be of reasonable size (say, at most 4096 bits, yielding a ~2048 gap). This 2048 gap only applies if the evaluator and verifier run on the same hardware, making CPU verifiers useless in practice (unless you use intermediate values, but then bandwidth becomes an issue). This means you now need VDF ASICs for verifiers as well. You could have a cryptoeconomic scheme (e.g. see here) but a cryptographic scheme is clearly preferable (less trust, less complexity).
2. MiMC: Basically the same as Sloth but worse: smaller gap for equivalently sized multipliers, and more complex intermediate non-arithmetic operations.
3. Guralnick and Muller: I was told by various experts (Dan Boneh, Benedikt Bünz) that these polynomials are too risky because no one has seriously tried to break them. A promising approach, though.
4. Sloth++ with SNARKs: Based on the research on ASIC multipliers my guess is that the basic step in Sloth++ (e.g. 256-bit modular squaring) can be done in ~1 nanosecond. So the SNARK prover stands no chance to keep up unless it is itself implemented as an ASIC. It’s unclear building a SNARK ASIC that is fast enough is practical.
5. Sloth++ with STARKs: This is currently our best candidate for a quantum-secure VDF. The situation is similar to the above except 1) STARKs are quantum-secure, 2) STARKs provers are faster, 3) recursive STARKs are harder 4) STARKs are not as mature.

Is there a permutation polynomial you think should be (re)considered?

![](https://ethresear.ch/user_avatar/ethresear.ch/seresistvan/48/1649_2.png) seresistvan:

> Or is it just too complex for the EVM?

The EVM has no bearing on VDFs (other than the randomness opcode yielding hashes of VDF outputs). The VDF logic is implemented at the consensus layer.

---

**seresistvan** (2018-09-30):

Wow! what a thorough summary! Thanks a lot! I do not have any specific attack or proposition yet but really like  **Guralnick and Muller** polynomials. I want to have a closer look at them in the next few weeks.

---

**kladkogex** (2018-09-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Right, forkfulness at the RANDAO level is a grinding opportunity for RANDAO + VDF. Applications that need to protect themselves from this grinding opportunity (e.g. billion-dollar lotteries) need to wait until Casper finality of the randomness to get the similar guarantees to Dfinity/Tendermint.

Can you illustrate how this is going to work even if Casper is added to the picture?

My understanding is that if there is a network split, two random numbers are generated.

Then these two numbers will cause different block proposers to be selected on two different sides of the split - correct?  In this case I am not sure how Casper validators should behave. Casper validators assume that block proposals are made by valid proposer, but if there are two different sets of valid block proposers, I am not sure Casper validators can help to resolve it.

May be it is going to work, the problem will be that the system may end up so complex, that current ETH developers - the guys that develop geth, parity, cpp-ethereum etc. will not be able to understand it or debug it … If something goes wrong, they will have to analyze potential interplay of validators,  proposers, network splits etc.

I am keeping my money on the PoW network!!!![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=12)![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=12)

---

**JustinDrake** (2018-09-30):

I suggest we take this discussion offline—feel free to DM me—as it is not specific to VDFs, or even randomness beacons.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Can you illustrate how this is going to work even if Casper is added to the picture?

It is natural for general-purpose consensus protocols to favour liveness. (In that sense, Dfinity got it “wrong”.) [@naterush](/u/naterush) puts it eloquently:

> An available consensus protocol (that is aware of what is safe) can simulate a consistent one (just by only showing finalized blocks), but not the other way around.

Casper FFG is that layer of detectable safety that dApps can rely upon (if required). In other words, a consensus protocol that favours availability is generic in the sense that it pushes the safety vs liveness tradeoff to the application layer:

- Liveness is available out of the box for dApps that require liveness.
- Safety is available by filtering out non-finalised blocks for dApps that require safety.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> I am not sure how Casper validators should behave.

Casper validators should subjectively follow the fork choice rule.

---

**jamesray1** (2018-10-12):

You could fund the ASIC as a public good with [liberal radicalism](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3243656)!

---

**jamesray1** (2018-10-18):

Why wouldn’t you use VDF with say, a blockhash N blocks ago? There are probably issues around using a public piece of data for an input to the VDF.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Honest proposers are expected to keep their local entropy private until their assigned slot.

I guess it may be to do with that other proposers may jump in to someone else’s slot and use the public piece of data to compute the VDF, potentially more quickly the assigned proposer. I’m asking because Harbour MVP are looking to use this (with PoW for the mean time). FMI see [here](https://gitter.im/metacartel/collision-problem#utm_source=notification&utm_medium=email&utm_campaign=unread-notifications).

---

**JustinDrake** (2018-10-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> Why wouldn’t you use VDF with say, a blockhash N blocks ago?

We want the beacon’s safety to fallback to RANDAO if the VDF is (partially or fully) broken. Blockhashes are a much weaker fallback than RANDAO. Also we want to launch the beacon chain in 2019 and the VDF ASICs will not be ready until 2020, so RANDAO is a bootstrapping mechanism.

---

**LeapM** (2018-10-26):

If a bad guy can do VDF that is Amax times faster, will this give the bad guy plenty time to prepare a DDoS attack against committee member at the future epoch?

---

**JustinDrake** (2018-10-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/leapm/48/2533_2.png) LeapM:

> If a bad guy can do VDF that is Amax times faster, will this give the bad guy plenty time to prepare a DDoS attack against committee member at the future epoch?

The amount of time the randomness is known before it is used is called the “lookahead”. People running the commodity ASIC have one epoch of lookahead. An attacker with hardware that is A_{max} times faster than the commodity ASIC has A_{max} epochs of lookahead.

Adaptive attacks (e.g. DoS, bribing, …) on proposers and committees is largely orthogonal to the randomness beacon for two reasons:

1. Hardening against adaptive attacks is done with “private elections” (and hence private lookahead). There are various schemes (e.g. see my proposed scheme using ring signatures) that work regardless of the randomness beacon.
2. Adaptive attacks (especially networking DoS attacks) are possible even for randomness beacons with small public lookahead (e.g. Dfinity’s scheme).

PoW and Algorand’s cryptographic sortition are two private election schemes but neither is unbiasable.

---

**coventry** (2019-01-08):

Thanks for the great design and [talk](https://www.youtube.com/watch?v=zqL_cMlPjOI#t=14m31s), Justin. I’m super curious about the design of the MPC for trustless construction of the RSA modulus. Is that described in more detail anywhere, at this point?

I think it’s worth pointing out, with Algorand, that while the last potential revealer *can* bias the result, there is no incentive for them to do so, and there will be many applications of random beacons where that is the case. It would only make sense for them to do so if the outcome they can predict from their last revelation would be unfavorable to them.


*(18 more replies not shown)*
