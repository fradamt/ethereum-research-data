---
source: ethresearch
topic_id: 2365
title: Verifiable delay functions and attacks
author: vbuterin
date: "2018-06-27"
category: Proof-of-Stake
tags: [random-number-generator, signature-aggregation]
url: https://ethresear.ch/t/verifiable-delay-functions-and-attacks/2365
views: 17736
likes: 7
posts_count: 14
---

# Verifiable delay functions and attacks

Verifiable delay functions have been popular recently as a strategy for getting entropy for validator and committee selection in PoS networks. A VDF is a function that takes some medium-large quantity of *non-parallelizable work* to compute, but can be verified very quickly.

The best known “proto-VDF” is the “iterated modular square root” strategy, where `f(x) = g(g(g(g(....g(x)....))))` where `g(x) = xor(x^((p+1)/4), 1) mod p`. Because each application of `g` depends on the result of the previous, the computation cannot be parallelized. Furthermore, `g` has an inverse: `h(x) = xor(x, 1)^2 mod p`, and this inverse can be computed more quickly (think ~100x more quickly) than `g`. Hence, the function `f` can be computed in the backward direction ~100x more quickly than in the forward direction, allowing a solution to `f` that takes ~5 seconds to compute to take ~0.05 seconds to verify. However, more recently there have been VDFs with much stronger properties, that can be verified almost instantly.

VDFs have the following advantages:

- Relative to RANDAO and similar schemes, they cannot be manipulated.
- Relative to BLS threshold signatures and similar VRFs, they do not depend on any specific fraction of nodes to be online, and do not require a complicated setup procedure.

Now, enter reality. It seems very plausible that there will be one actor who manages to create ASICs for any given VDF, and be N times faster (eg. N = 20) than the top-of-the-line CPU/GPU implementations. The acceleration factor won’t be remotely close to as high as it is for Bitcoin proof of work, because a large portion of the speedup factor in that case comes from parallelization, but one absolutely can imagine ASICs that involve circuits specifically designed to loop back into themselves as fast as possible.

Suppose that this happens. There are two possibilities:

1. The attacker can compute the VDF so quickly that they can predict its output before they have to commit to some value, giving them the ability to choose the result from a set of possible outputs.
2. The attacker can allow the difficulty adjustment process to adjust to their presence, then suddenly go offline, greatly slowing down the system.

Suppose that we use a VDF as follows. A participant is expected to submit data that determines the *source data* for a VDF computation, together with other source data that was revealed at time T, and the submission must appear before time T+D (eg. if the participant waits longer than T+D, then they will lose their chance to get included into the canonical chain). The data starts being used at time T+W. Suppose that the difficulty adjustment algorithm is designed in such a way that it targets the data being computed at time T+N.

Let the attacker speedup (“advantage”) over the rest of the network be A. The attacker can perform the first attack if A > N/D, and the second attack if A > W/N. Hence, we can secure against the highest possible A if we set N/D=W/N, ie. N is the geometric mean of D and W (eg. if D = 6 seconds, W = 1 hour, then N ~= 147 sec, allowing the mechanism to resist an attacker advantage up to sqrt(W/D) ~= 24.5.

You may ask: why not have the VDF difficulty adjustment target N to be close to W, and then have  a backstop where if the VDF is not calculated by time W, a committee can approve a backstop that allows an easier VDF solution to be used? However, this is problematic: if you are the fastest VDF producer, then you can check the fast and slow solutions, and then choose which one to use by going offline, manipulating the randomness for free. It’s an open problem to see if we can achieve full safety against attacker advantages higher than sqrt(W/D) as above.

## Replies

**djrtwo** (2018-06-27):

What if we use successive portions of the VDF to seed things over time. This can be a solution to (1) if the randomness is needed to seed a series of discreet events (like who is to be the block producer for a series of blocks).

Specifically in the case of the beacon chain, the VDF can be used throughout the epoch to seed things just in time. At its most granular, seed block-1 producer/attesters of the epoch with `VDF(seed, 1 * X / EPOCH_LENGTH)`. Seed block-2 producer/attesters with `VDF(seed, 2 * X / EPOCH_LENGTH)`, and block-N of the epoch with `VDF(seed, N * X / EPOCH_LENGTH)` where `X` is the difficulty of the VDF targeting taking approx an entire epoch to compute.

This extends the sponge metaphor given by [@JustinDrake](/u/justindrake). Instead of just squeezing out the one source of randomness for the epoch, validators must squeeze out randomness throughout the epoch. A validator with N=20 speed up would be able to see a bit into the future but would be limited in how far into the epoch they can see.

This *might* work for proposers/attesters but would not work for shard notary committees. Those committees have to be specified well ahead of time so they can divide up and do work on their specific shard.

---

**dlubarov** (2018-06-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The attacker can perform the first attack if A > N/D

I’m not sure `D` is important. As long as the entropy submissions are VRFs of some sort, like `hash(sk, height)` with a zero knowledge proof, the attacker can’t start grinding the VDF until he knows the submissions of all uncooperating validators, right?

We could make `D` 24 hours to give plenty of time for submissions, and suppose that an attacker near the end of an epoch is capable of DOSing the `k` validators before them, plus any after them. Then the attacker needs `A > W / (k * BlockTime)`.

Edit: I guess your premise was that entropy contributions can be made at any time in an epoch, and most validators would submit near the epoch start? I’m assuming submissions are interspersed throughout an epoch, e.g. by having each validator include a submission in their block header.

---

**vbuterin** (2018-06-28):

> the attacker can’t start grinding the VDF until he knows the submissions of all uncooperating validators, right?

Yes, but I’m assuming here that the attacker is the last one to submit a message that has the ability to influence the VDF result. So the attacker has the information needed to compute the result with or without their submission, and if they can do that quickly enough they would be able to choose the one of the two that is more favorable to them.

---

**NicLin** (2018-07-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The attacker can allow the difficulty adjustment process to adjust to their presence, then suddenly go offline, greatly slowing down the system.

Is the difficulty adjustment algorithm in VDF different than the one in PoW? I imagine it should not be since in VDF scheme everyone submits instead of only the fastest one as in PoW.

If we use PoW difficulty adjustment algorithm in VDF(i.e., to limit the fastest participant), participants would start to fail to reveal in time as attackers push up the difficulty and I suppose this is observable hence we could act on this in time to prevent the difficulty from climbing up?

---

**vbuterin** (2018-07-02):

The difficulty would be fairly simple: if the VDF solution is submitted earlier than expected, increase the difficulty, if it’s submitted later than expected, decrease the difficulty. The adjustment could be fairly rapid.

---

**NicLin** (2018-07-02):

So attackers should not be able to manipulate the difficulty unless the attacker owns the majority of the participants right? If so then I think the second attack will be difficult to be carried out under honest majority assumption?

---

**vbuterin** (2018-07-03):

It’s not about the majority of the participants, it’s about who is the fastest participant. If an attacker is the fastest participant, then they can manipulate the difficulty somewhat.

---

**raullenchai** (2018-09-21):

It may be possible to construct memory-hard VDFs to mitigate (to some degree) ASIC acceleration. A simple one off the top of my head is a memory-hard but “weak” password-hash function h() whose preimage (assume it is unique for the time being) can be computed with a reasonable amount of time; so the VDF is y=h^{-n}(x), and verification is x=h^n(y). Apparently, computing the hash chain reversely takes much more time.

---

**augustoteixeira** (2018-09-23):

A few comments:

1 - The second attack is not deniable. I mean, contrary to ASIC in mining nowadays, people will see that someone has a special hardware somewhere. So perhaps N should be closer to W.

2 - If various (non-cooperative) attackers develop an ASIC, I think the system stabilizes again. Does that make sense?

3 - If I understand well the threat model, there needs to be only one honest party with a fast hardware to secure the system. In this case, crazy superclocking a good CPU with well written code could make it very hard for an adversary to reach a 25 fold improvement with an ASIC. Actually, even developing an inhouse hardware is an option, like Siacoin did.

---

**DB** (2018-09-23):

Why use only a single VDF function? If we let multiple actors choose their function (from a set), as long as there is a single function the attacker cannot break by the reveal time, he cannot manipulate the randomness.

---

**JustinDrake** (2018-09-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/augustoteixeira/48/2208_2.png) augustoteixeira:

> The second attack is not deniable.

Right, the fact that an attacker would “reveal his hand” by making a DoS attack is the basis for the [DoS-hardened difficulty mechanism](https://ethresear.ch/t/vdf-based-rng-with-linear-lookahead/2573).

![](https://ethresear.ch/user_avatar/ethresear.ch/augustoteixeira/48/2208_2.png) augustoteixeira:

> there needs to be only one honest party with a fast hardware to secure the system

Right. There needs to be at least one honest party with fast *enough* hardware (specifically, no slower than A times what an attacker can do).

![](https://ethresear.ch/user_avatar/ethresear.ch/augustoteixeira/48/2208_2.png) augustoteixeira:

> developing an inhouse hardware is an option, like Siacoin did

This is the current plan. We want to build a state-of-the-art commodity VDF ASIC—in collaboration with Filecoin and others—to get a reasonable maximum advantage A. The ASIC would be optimised for squaring modulo a fixed 2048-bit modulus (this is the RSA setup for the [Wesolowski VDF](https://eprint.iacr.org/2018/623.pdf)).

We are considering outsourcing the hardware design and manufacturing to Obelisk (see [their launchpad service](https://obelisk.tech/launchpad.html)), the same company that did the Sia hardware.

---

**zawy12** (2019-03-10):

I do not see how the primary complaint above is relevant if a few ASICs are publicly available (enough to be “decentralized”) for everyone with a low solvetime to send their parameters for solving. The circuit design should be very small, so a single VDF ASIC could handle many requests. It only has to accept maybe 5 requests per block, the 5 which who have the fastest solvetimes in the stake-weighted randomness.

VDFs can be used to remove the complexities of PoS by enabling stake-rate to replace hash-rate. But Nakamoto consensus has to be done backwards because mining equipment proves its value over time when it’s producing low-entropy solutions. The time comes before the proof of equipment value is finished, proving a miner has a certain hashes/second. The equipment is inherently occupied during time, but stake is only a value that partly solves the uniqueness problem in voting. By not being occupied in time, it can’t show that it did not vote twice during the vote. So we can use the VDF to show stake was occupied during the vote. But since the value is already known to the chain, and used to adjust the time instead of vice versa, we have to do consensus backwards.

I’m calling this “reverse Nakamoto consensus” and vPOW because other POS systems get complicated quickly from not doing doing consensus backwards.


      ![image](http://zawy1.blogspot.com/favicon.ico)
      [zawy1.blogspot.com](http://zawy1.blogspot.com/2019/03/reverse-nakamoto-consensus.html)


    ![image]()

###

Abstract    POW consensus is problematic due to 51% attacks. Even BTC is potentially vulnerable as it shifts from rewards to fees.[1][2] ...









      ![image](http://zawy1.blogspot.com/favicon.ico)
      [zawy1.blogspot.com](http://zawy1.blogspot.com/2019/03/a-virtual-pow-to-prevent-51-attacks.html)


    ![image]()

###

Introduction  This is a coin design that combines a lot of ideas to prevent common POW problems and enable it function as a stable value cu...

---

**mehranshakeri** (2019-10-01):

What if we break down the process to two deterministic and (semi) nondeterministic parts?

Let’s assume there is a cycle with deterministic calculation `(f(x) = g(..g(x)..))`. Attacker can be as fast as it can here.

But at the end/beginning of the cycle we use a seed to change the result of the cycle and make pre-calculation of other cycles difficult. Also reset or drop the difficulty each time a cycle starts/ends to prevent super fast attacker’s dominance.

For example considering implementation in a smart contract:

- In each cycle, difficulty alway increases starting from a very low value
- At the beginning of each cycle the last valid random number is hashed with the current value of the seed and set as lastRandomHash
- During each cycle, a valid random value is the smallest positive number/hex string which increases the difficulty where difficulty is the number of leading zeros of output of hash(lastRandomHash + validRandomNumber) and output will be set as the new value of lastRandomHash chaining the results.
- Always users can spontaneously tip the smart contract which will result in changing the seed mixed with the block number and sender address. A simple pay to contract transaction. Thus the attacker can’t start pre calculating the next cycle.
- Edge cases can be avoided e.g. if someone submits a random value which is not the smallest but fulfills the difficulty increase, the history can be kept and reverted if someone proves it’s been happened.
- The cycle should be long enough to generate few valid numbers and short enough to prevent high difficulties or simply cap the difficulty
- Maybe some incentives to attract more generators and first submitting the hash and reveal the number later to prevent other participants (miners, …) to steal the generated random value.
- Even there could be more than one smart contract generating random numbers and one can aggregate all the results. Thus attacker has less control over the whole process or has to distribute its processing power among all the contracts.

The last submitted random value in each cycle can be assumed as the returned random number of the smart contract.

