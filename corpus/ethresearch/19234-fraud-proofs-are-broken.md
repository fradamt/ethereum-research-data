---
source: ethresearch
topic_id: 19234
title: Fraud Proofs Are Broken
author: GCdePaula
date: "2024-04-08"
category: Layer 2
tags: [rollup, fraud-proofs]
url: https://ethresear.ch/t/fraud-proofs-are-broken/19234
views: 11006
likes: 57
posts_count: 19
---

# Fraud Proofs Are Broken

# Fraud Proofs Are Broken

*… but we can fix them.*

Optimistic rollups aim to inherit Ethereum’s security through fraud proofs. The reasoning is straightforward: a single honest validator can prove all dishonest validators are liars, and thus enforce the truth. Since anyone can be a validator (including you), securing any optimistic rollup is just a matter of setting up a node to run on your laptop. No need to trust anyone.

The underlying assumption is that these fraud proof algorithms are permissionless. We know of three algorithms that aim for permissionless interactive fraud proofs. In no particular order: Cartesi’s *Permissionless Refereed Tournaments* (PRT), Arbitrum’s *Bounded Liquidity Delay* (BoLD), and *OP Stack’s Fault Proof System* (OPFP).

They all have issues. **They’re vulnerable, in different ways, to [Sybil attacks](https://doi.org/10.1007%2F3-540-45748-8_24) that undermine the safety, settlement speed and/or decentralization of the fraud proof system.**

Our discussion focuses on the theoretical properties of the proposed algorithms, rather than the current development stages of any specific protocol that may or may not have training wheels. If the underlying algorithm isn’t resistant to Sybil attacks, the training wheels can never be safely removed. Now, fraud proofs with a permissioned set of validators are certainly much better than no fraud proofs at all; it’s quite acceptable as an intermediary stage. However, we need to keep researching better algorithms.

I’m a contributor in the Cartesi ecosystem, which provides an optimistic rollups solution. I’m part of the team developing the next iteration of our fraud proof protocol, mentioned above.

This post has three purposes:

- Establish a set of criteria to analyze fraud proofs. Quoting Vitalik, the ecosystem’s standards need to become stricter.
- Articulate why none of the candidates put forth so far meet these criteria. Including ours.
- Call for open and public research collaboration between the optimistic rollups teams. This is a personal frustration of mine. Our attempts at public communication with these teams haven’t been successful at eliciting substantive academic discourse on the vulnerabilities and tradeoffs for existing fraud proof algorithms.

This post is *not* about providing a solution to Sybil attacks in fraud proofs, nor is it about proposing a new algorithm. Furthermore, this post is concerned only with *interactive* fraud proofs; non-interactive fraud proofs have different challenges and criteria.

# Criteria

Optimistic rollups generally operate under two key assumptions: the base layer works (but can be arbitrarily censored for up to a week) and the presence of at least one honest validator. Under these assumptions, we need to design a protocol that allows anyone to participate while being resistant to Sybil attacks. Sybil attacks are the antagonist of this story, an ever-present adversary any permissionless protocol must face.

We propose three properties for analyzing permissionless interactive fraud proofs: safety, promptness and decentralization. These properties should be viewed as spectra rather than binary. Loosely, a permissionless algorithm is:

- Safe if it can reject all false states under the original assumptions;
- Prompt if settlement cannot be delayed substantially (or indefinitely);
- Decentralized if validating doesn’t require a lot of resources like hardware and funds.

In an ideal world, we want the honest validator to win any dispute in a timely manner using nothing more than a toaster.

We’ll assume the reader is generally familiar with fraud proofs. We’ll call the set of honest validators the ***hero*** (worst case scenario is just one validator), and the set of dishonest validators working in tandem the ***adversary***. We’ll use the terms *validator* and *player* interchangeably.

## What’s at stake

A dispute puts the total value locked (TVL) of a rollup at stake. An incorrect states that gets accepted can be extraordinarily profitable for the adversary. However, the same is not true for the hero – the hero gets nothing of the TVL by winning.

This financial imbalance puts the hero at an incredible disadvantage. At the limit, the adversary should be willing to burn a TVL’s worth of resources. What’s worse, different attackers may trustlessly coordinate through smart contracts and pool their resources.

We cannot assume the hero can match a TVL’s worth of resources, not even when teaming up with others. We must assume the adversary has significantly more resources than the hero, given what’s at stake. It’s a lot harder to design good algorithms under these constraints.

# Canetti et al.

Traditional fraud proof protocols are based on the [work of Canetti](https://doi.org/10.1016/j.ic.2013.03.003). We’ll highlight a few important concepts. The basic idea is quite simple.

Consider a setup with only two players. First, these players agree upon an initial state and a state-transition function (STF). They’ll run the computation on their machine by successively applying the STF to the initial state, and propose a final state to the blockchain. These proposals are called *claims*; they’re a commitment to the final state of a computation. If the players agree, all is well. If not, the system starts a verification game. A verification game consists of two phases: the *bisection phase* and the *one-step proof phase*. The bisection phase is an interactive binary search over the whole computation, trying to find where the players first disagree. This disagreement is called the *divergence*. Once the divergence is found, the blockchain applies the STF once (a *step*), and eliminates the adversary.

Now consider a setup with many players. Naively extending the algorithm described above, there’s an attack where the adversary posts the honest claim but lose the game on purpose by playing dishonestly. This makes evident the fragility of Canetti with respect to Sybils: it doesn’t reveal lies, it reveals liars. We can’t group players with the same claim into teams. Each player must represent themselves and only themselves for all parts of the dispute, even when there are others with the same claim. Players’ signatures have to be part of the message.

Canetti proposes a few ways to make verification games with many players, taking this fragility into consideration. Unfortunately, none of those approaches scale well on the number of players. This makes the algorithm unsuited for permissionless fraud proofs since they’d be susceptible to Sybil attacks.

For example, the first fraud proof protocols of Cartesi and Arbitrum (based on Canetti) would fail the promptness property if made permissionless without further changes. Ed Felten wrote a [post](https://research.arbitrum.io/t/solutions-to-delay-attacks-on-rollups/692) describing delay attacks, which are a type of Sybil attacks that compromises the promptness of the protocol. In short, there’s an attack where settlement is delayed linearly on the number of Sybils, which can be a very long time indeed.

We need to design algorithms that can scale on the number of players, and thus be resistant to Sybil attacks. Otherwise, we won’t be able to make protocols permissionless.

# Permissionless Refereed Tournaments (PRT)

The PRT algorithm was developed by Cartesi. The paper can be found [here](https://arxiv.org/abs/2212.12439). The algorithm is focused on application-specific rollups, which have different requirements when compared to shared chains. This has influenced the design of PRT: it’s important that anyone can validate a rollup in a laptop with minimal stakes. (We’d argue this is also true for shared chains; ideally, the hero shouldn’t need a supercomputer or a gazillion dollars.)

The key contribution of PRT is *computation hashes*. It addresses the fragility of Canetti described above, allowing players to be grouped into teams. This enables a more efficient tournament structure.

## Computation hashes

Claims in PRT are a stronger kind of commitment. Instead of a commitment just to a final state, claims are a commitment to the entire path of the computation (*i.e.* a *computation hash*). A computation hash is Merkle tree where each leaf is a hash representing the state at every state transition along the computation.

Bisections in PRT require a valid Merkle proof that the intermediary state is consistent with the computation hash. This way, an adversary that posts the honest computation hash cannot lose the game on purpose (except by inaction). As such, PRT can allow anyone to bisect any claim, since the Merkle proofs guarantee the bisection is honest. There’s a fundamental shift: PRT can reveal lies, instead of just liars. Players’ signatures need no longer be part of the message.

Therefore players can be grouped into teams and fight together. With this property, PRT creates a bracket-style tournament between claims, matching them pairwise and eliminating half the Sybils at each bracket level. **This means the amount of work required of the hero is logarithmic in the number of Sybils**; PRT scales well on the number of players.

[![have you tried logarithms?](https://ethresear.ch/uploads/default/optimized/2X/1/1afc14e3db541a2c67ed0bf8b0221edcf44c96ba_2_296x303.jpeg)have you tried logarithms?872×894 88.3 KB](https://ethresear.ch/uploads/default/1afc14e3db541a2c67ed0bf8b0221edcf44c96ba)

---

To make a claim, players need to post a stake. After a claim is made, there’s no need to post further stakes. Bisections are free, except for gas costs. Since the adversary needs to deposit one stake to create one Sybil, and half the Sybils are eliminated at each iteration, launching a Sybil attack is exponentially expensive.

The hero needs only fight one match at a time, which means they’ll only ever need one computer. Furthermore, they need to deposit only a single stake. This means the decentralization property of PRT is great. Additionally, given the assumptions of optimistic rollups, the correct claim will always be enforced, which means PRT is safe.

On promptness, delay grows logarithmically on the number of Sybils, which is nice since logarithms grow very slowly. Unfortunately, this logarithmic delay has high constants: each single match still takes about a week to complete. The logarithm of Sybils multiplied by a week is quite slow. It’s not fatally slow, but it’s still quite slow.

At this point, PRT has reached a trilemma of safety, promptness and decentralization. A rollup can choose:

- promptness and safety by increasing stakes (harming decentralization);
- promptness and decentralization by reducing the maximum base layer censorship (harming safety);
- safety and decentralization by making stakes small and keeping the maximum base layer censorship at seven days (harming promptness).

Ideally, we’d want to have the three properties at the same time, but for PRT something will have to give. We believe the second option is acceptable for chains that don’t have a lot of TVL. But since the other algorithms were designed with high TVL in mind, for this comparison we’ll pick the third option.

|  | PRT |
| --- | --- |
| Safety |  |
| Promptness |  |
| Decentralization |  |

## Multi-stage disputes

The PRT paper describes two setups: single-stage and multi-stage. In practice, *if the state-transition function is a single virtual machine (VM) step*, the single-stage setup is prohibitive for large computations. Generating a computation hash with every state transition in a computation is extremely slow. We introduced the multi-stage setup to address this issue.

The idea is to make the initial computation hash sparse, where the number of state transitions between each Merkle leaf is greater than one. This means we can’t resolve the divergence between two sparse computation hashes. The blockchain would need to perform too many state-transition functions.

However, we can reduce the search space to the sparseness of that commitment. With a smaller search space, we have reduced the dispute to a smaller computation; we can recursively use the same method, but with a denser computation hash since the computation smaller. The base case is a fully dense computation hash that can be resolved normally. Players still need to post a stake at every nested tournament they wish to submit a claim, otherwise generating a Sybils would be cheap.

This technique is clever, but introduces delays. In a two-stage setup, there’s a strategy where the adversary can delay settlement for the logarithm *squared* of the number of Sybils, making it strictly worse than the single-stage setup.

The description and analysis of PRT above consider the faster single-stage setup. Although prohibitive if the state-transition function is a single virtual machine step, we can leverage ZK proofs and change the state-transition function from one VM step to several VM steps. This makes the single-stage setup possible in practice. Note that this is still an interactive fraud proof; it’s just a change to its state-transition function.

Check [Carsten Munk](https://twitter.com/stskeeps)’s presentation [here](https://youtu.be/leCd5kyDTR8) about proving the execution of our virtual machine in ZK, using RISC Zero. Our benchmarks with low-end hardware are promising. This increases the hardware requirements from one laptop to one laptop with one GPU. Our [ongoing implementation](https://github.com/cartesi/dave) (called Dave) currently uses the multi-stage setup. We’re moving to the single-stage setup because it has better promptness. We’re also engaging in more research to create an algorithm that achieves all three properties simultaneously.

# Bounded Liquidity Delay (BoLD)

In December 2022, Arbitrum [announced](https://research.arbitrum.io/t/solutions-to-delay-attacks-on-rollups/692) their protocol was vulnerable to delay attacks in a permissionless setting. In the same post, they announced they had a solution, and that they’d post it soon. In August 2023, they released a [preliminary paper](https://github.com/OffchainLabs/bold/blob/main/docs/research-specs/BOLDChallengeProtocol.pdf), along with an [implementation](https://github.com/OffchainLabs/bold), naming it BoLD. The full paper is yet to be released. (One of the motivations of this text is also a call for teams to prioritize these discussions.) We look forward to the full release; we believe it will benefit the ecosystem as a whole.

BoLD was developed independently from PRT (PRT was published first), but both algorithms reached similar techniques. In particular, BoLD also uses computation hashes and the recursive disputes technique with sparse computation hashes. We’ve described these two techniques in the PRT section above. We highlight that players need to post a stake to enter a challenge in BoLD.

Unlike PRT, instead of setting up a tournament with brackets, in BoLD all claims fight each other simultaneously. Because of this and a novel clock technique, the settlement time is constant, regardless of the number of Sybils. The current implementation has a [16 day settlement time](https://x.com/dzack23/status/1737864854059335905). As such, the promptness property of BoLD is great. But there are trade-offs.

The core issue of BoLD is safety, compromised by an attack we call ***proof of whale***. It’s a kind of Sybil attack where a better funded adversary can win the dispute against the hero by exhausting the hero’s resources until they have no more resources to keep playing the game.

Reiterating, winning a dispute is extraordinarily profitable for the adversary, but not for the hero. At the limit, the adversary should be willing to burn resources approaching the TVL of the rollup. It’s reasonable to assume the attacker is significantly better funded than the hero.

[![poor seal](https://ethresear.ch/uploads/default/optimized/2X/2/2e390d880e5a7c2b330739c88e01e3550641a3a8_2_368x368.jpeg)poor seal1024×1024 267 KB](https://ethresear.ch/uploads/default/2e390d880e5a7c2b330739c88e01e3550641a3a8)

The hero needs to spend three different kinds of resource throughout a dispute: compute, blockspace, and stakes. Since each of these can be acquired with money, *proof of whale* can be seen as exhausting the hero *financially*. However, these resources are on different dimensions, and will be analyzed separately.

We’ll describe three variants to *proof of whale*, each exhausting a different resource.

## Variant one: Zerg Rush the hero’s servers

The first variant is an attack on the computational resources of the hero. The worst-case work required of honest parties is linear in the number of Sybils. Since the time is constant (one week) but the work is linear on the number of Sybils, hardware requirements grow linearly with the number of stakes the adversary is willing to burn.

This attack is hard to defend against, because the hero must be able to scale his computational power dynamically, or always dimension it with the worst case scenario in mind. Furthermore, the adversary needs no extra computers to pull this off since they can completely fabricate the states without turning on a VM.

Nevertheless, the adversary still has to burn one stake to create one Sybil. If the cost of stakes is irrelevant, then this attack is trivial to pull off. Increasing the stake to just match the cost of renting one laptop makes this attack as costly for the adversary as it is for the hero. In this case, if the adversary has more stakes than the hero has computers, then a wrong claim will win. Further increasing the stake increases the hero’s advantage.

Increasing the stake as to dominate the cost of hardware does mitigate this attack. However, it’s harder for players to participate when stakes are higher, compromising the decentralization of the algorithm.

## Variant two: Zerg Rush the hero’s access to blockspace

The second variant is an attack on the hero’s access to blockspace. Blockspace can be acquired by expending funds (think paying ether for transaction costs), but it’s not the only way. If a player is a block producer in the base layer (or has a generous friend who is), they will have blockspace access without expending funds for transaction costs. In any case, blockspace is not free; players have a limited amount of it. As such, instead of modeling access to blockspace as funds, it’s better to think about blockspace as a total budget for transactions that each player consume along a dispute. This attack is *not* about denying the hero’s access to blockspace (*i.e.* censorship), but forcing the hero to use up their budget.

All Sybils created by the adversary must be fought simultaneously by the hero. Each Sybil that eagerly participates in the bisection phase forces the hero to respond in kind. Playing the bisection phase to its completion, each eager Sybil forces both the adversary and the hero to include a number of transactions equal to the logarithm of the size of the computation. These transactions consume the budget of both adversary and hero.

If the adversary has more blockspace access than the hero, then the adversary might be able to exhaust the hero’s blockspace access, depending on how many stakes the adversary is willing to burn. If the cost of stakes is irrelevant and the adversary has access to more blockspace than the hero, then a wrong claim will win.

Increasing the stake to just match the cost of blockspace access gives the hero a two-fold advantage; the adversary has to pay one additional stake plus blockspace (the equivalent of two stakes), whereas the hero has to pay only one additional blockspace (the equivalent of one stake). Further increasing the stake-to-blockspace ratio increases the hero’s advantage, to the point where the advantage about equals this ratio.

Increasing the stake as to dominate the cost of transaction fees does mitigate this attack. However, it’s harder for players to participate when stakes are higher, compromising the decentralization of the algorithm.

It’s difficult to defend against this attack for several reasons. The adversary can use smart contracts to submit many claims and bisections at the same time, making their use of blockspace more efficient than the hero’s. Furthermore, depending on the magnitude of the whale, fees may skyrocket as blockspace becomes scarce, reducing the hero’s access to blockspace. Finally, if the adversary has the support of a block producer in the base layer, they can include transactions without having to pay (possibly skyrocketing) fees.

## Variant three: Zerg Rush the hero’s funds

If the stake is large, dominating both the cost of hardware and the cost of transaction fees, the adversary should use the third variant of *proof of whale*. The third variant hinges on the multi-level challenge setup that we described on previous sections. BoLD is set to use three levels of nested challenges.

Reiterating, players need to post a stake at every challenge they wish to submit a claim, otherwise it would be cheap to generate Sybils. Every claim made at a non-leaf challenge may potentially spawn a sub-challenge. Take a two-stage setup: if the adversary launches a Sybil attack posting `N` claims at the first challenge, BoLD will have to spawn `N` second-level sub-challenges. This means the hero will have to submit `N` claims in the second level, one claim for each spawned sub-challenge. Posting `N` claims requires `N` stakes. Therefore, if the adversary has more stakes than the hero, then the adversary will win.

---

Note that using the strategy described in the third variant also triggers the first and second variants. That is, ***proof of whale* forces the hero to have simultaneously more hardware *and* more blockspace *and* more stakes than the adversary has stakes.** Otherwise, the hero will lose the dispute. This makes the system behave not unlike majority token voting, though possibly biased towards the hero depending on the setup. We’ll go into more details about the hero’s advantage in the next section.

*Proof of whale* is extremely hard to defend against because of the financial imbalance between hero and adversary. To make things worse, different attackers may trustlessly coordinate through smart contracts and pool their resources.

|  | BoLD |
| --- | --- |
| Safety |  |
| Promptness |  |
| Decentralization |  |

## The hero’s advantage

The *proof of whale* issue was touched on this [post](https://research.arbitrum.io/t/bold-question-about-number-of-defender-s-stake/9445) at Arbitrum’s research forum. In it, Arbitrum researchers mention a behavior of the protocol not described in the preliminary paper: BoLD has sub-challenges requiring a “mini-stake” instead of a full stake. We take their comment to mean the hero still needs stakes linear on the number of Sybils, but the constant significantly favors the hero. This constant is defined by the ratio between the stakes of each challenge level.

However, the protocol setup has three levels of challenge (according to the preliminary paper). If the mini-stakes of the two final levels are the same, then we’re back to the original attack, shifted down one level: the adversary joins the root challenge once – paying a single full stake – and then joins the second challenge in earnest – paying one mini-stake for each Sybil. The hero must match the number of mini-stakes on the third level.

It seems the optimal strategy for BoLD is to chose the same ratio between levels one and two, and levels two and three. This ratio should be as high as possible to foil *proof of whale* variant three. Furthermore, the smallest stake should to be high enough to foil *proof of whale* variants one and two.

Let’s try some numbers. Suppose we want the hero to have an ten-fold resource advantage over the adversary. As such, we should choose a ratio of `10` between the stakes of each level. Suppose `$1,000` is just enough to cover for hardware costs and block access fees for any challenge. To keep the ten-fold advantage, we should set the smaller stake to about `$1,000 * 10`, otherwise the *proof of whale* variants one and two give the adversary a better advantage than the target of ten. This means the stakes for the top challenge should be set to `($1,000 * 10) * 10 * 10`, which is `$1,000,000`. This makes the system quite centralized, since few would be able to participate.

Nevertheless, BoLD is still unsafe. Large shared chains have several billion dollars in TVL; that’s what at stake here. If the adversary is willing to burn one billion dollars to win several billion, then the hero needs to have resources in the hundred millions (one tenth of one billion), sitting in the bank just to protect against whales. Ten is way too small of an advantage considering what’s at stake.

However, if we increase the advantage, we significantly hurt decentralization. For example, if we set the advantage to one hundred (which may not even be safe enough), the first level stake becomes `($1,000 * 100) * 100 * 100`, which is `$1,000,000,000`. We believe there’s no choice of parameters that makes the system reasonable.

## An improvement on BoLD

We suggest an improvement on BoLD: leveraging ZK proofs at the state-transition function to eliminate the use of sub-challenges, in the same way PRT is moving towards. This eliminates *proof of whale* variant three. Nevertheless, ZK is a huge engineering effort that has trade-offs of its own that must be considered carefully. Let’s call this improvement BoLD++.

BoLD++ settles in constant time like BoLD, so it has great promptness. Furthermore, the hero only ever needs one stake, addressing the third variant of the *proof of whale* attack.

However, BoLD++ is still susceptible to variants one and two of the *proof of whale* attack. Setting the stake high makes this attack prohibitively expensive, but unfortunately it compromises decentralization. In this setup, BoLD++ is quite centralized but not fatally so.

|  | BoLD++ |
| --- | --- |
| Safety |  |
| Promptness |  |
| Decentralization |  |

# OP Stack’s Fault Proof System (OPFP)

The Optimism specs can be found [here](https://specs.optimism.io). In particular, the fault proof system is described [here](https://specs.optimism.io/experimental/fault-proof/stage-one/fault-dispute-game.html). The implementation is [here](https://github.com/ethereum-optimism/optimism). It has just been deployed to testnet.

In the traditional conception of fraud proofs, dishonest players can say the correct thing but lose on purpose. Both PRT and BoLD use computation hashes to address this. OPFP has a different approach. It allows claims to be bisected multiple times by anyone, introducing a directed acyclic graph (DAG) of claims in which anyone can add more vertices. Claims are added by bisecting an existing claim in the DAG.

Disputes in OPFP are comprised of many games that anyone can create and play. All games are played simultaneously, which makes the dispute finish in constant time. Each game has its own DAG, starting with a root claim that asserts the result of the rollup. There are two main ways honest validators will play these games:

- Protect the game with the correct root claim. There’s only one game with the correct root claim.
- Expose all other games as faulty.

A game is played by countering claims. But since claims are countered mainly by adding child claims to the DAG, we’re entering the territory of countering counters all the way down to the one-step proof. Countering a counter uncounters the original claim. In the end, in order for a claim to be considered uncountered, all of its children must be countered. To consider a claim countered, it’s enough that a single one of its children is uncountered. The hero protects the correct game by countering the faulty claims that have countered the correct claims. The hero exposes faulty games by countering its root claims, and countering all the counters to their counters.

[![I bet the Optimism developers play mono blue in MtG](https://ethresear.ch/uploads/default/optimized/2X/d/d57ff7c4e33092f6f1019e4ac46c6ff36e583570_2_500x350.jpeg)I bet the Optimism developers play mono blue in MtG1667×1167 785 KB](https://ethresear.ch/uploads/default/d57ff7c4e33092f6f1019e4ac46c6ff36e583570)

It’s clever, though a tad convoluted. We recommend reading OPFP’s specs, where this is explained in more details. A detail we should highlight is that posting a claim (through bisections or otherwise) requires posting a bond. This bond starts small, and grows exponentially as claims get closer to the leaf. The final value of this bond was set to cover the worst-case cost of a one-step proof.

## Proof of Whale 2: Electric Boogaloo

OPFP, however, suffers from a similar *proof of whale* attack as the original BoLD.

The attack is straightforward. The adversary creates a script that bisects the correct claim in earnest. This can be improved by creating a smart contract that bisects many times, amortizing the base cost of an Ethereum transaction. This can be further improved by choosing the bisections in a way that the hero has to always compute a new state (in the worst case, the adversary can force the hero to post the entire computation on-chain). From time to time, the adversary also creates a new game by posting a faulty root claim. The hero has to counter all moves of either kind if they want to win.

---

Since countering a claim requires compute, blockspace and bonds, ***proof of whale* forces the hero to have simultaneously more hardware *and* more blockspace *and* more bonds than the adversary has bonds.** Otherwise, the hero will lose the dispute. This makes the system behave not unlike majority token voting.

Unlike BoLD, we believe it’s not possible to tune the parameters to give an advantage to the hero. The hero has no relevant advantage over the adversary; if the adversary is somewhat better funded than the hero, the adversary will win. It’s reasonable to assume the attacker is significantly better funded than the hero given what’s at stake.

Furthermore, we believe a winning adversary can recover both their bonds and the hero’s bonds, since the adversary’s claim will resolve correctly and the hero’s incorrectly. This makes a *proof of whale* even more profitable for the adversary.

|  | OPFP |
| --- | --- |
| Safety |  |
| Promptness |  |
| Decentralization |  |

# Conclusion

Some algorithms perform better than others, but it’s clear we’re not in an ideal situation. Reiterating, the ecosystem’s standards need to become stricter. Here’s the tally:

| Algorithm | Safety | Promptness | Decentralization |
| --- | --- | --- | --- |
| PRT |  |  |  |
| BoLD |  |  |  |
| BoLD++ |  |  |  |
| OPFP |  |  |  |

This is a call for collaboration. As a community, we need to fix fraud proofs. Furthermore, our individual implementations will be beneficial to all of us in a multi-prover future.

We have a couple of promising ideas that attempt to improve fraud proofs. We’ll publish them soon as a public good to the ecosystem, and we hope it can start a conversation.

Let’s nurture the *Infinite Garden* together. It all starts with openness. The ecosystem can only benefit from collaboration.

# Afterword

I’ve been supported by a remarkable group of people in the creation of this article.

I extend my deepest gratitude to:

- Augusto Teixeira and Diego Nehab, for their crucial collaboration in writing the article.
- Pedro Argento and Stephen Chen, my co-conspirators in developing the fraud proof system.
- Brandon Isaacson, Carsten Munk, Felipe Argento, Guilherme Dantas and Milton Jonathan, for their insightful feedback and thorough review.
- Donnoh and Willem Olding, for their gracious involvement in reviewing our work.

I also extend my gratitude to [Cartesi](https://cartesi.io) for funding the research and for providing the environment where the development could take place. We invite the reader to join us on [our Discord](https://discord.gg/pfXMwXDDfW), where we continuously engage in public research and debate these topics constantly.

## Replies

**felipeargento** (2024-04-08):

“A dispute puts the total value locked (TVL) of a rollup at stake. An incorrect states that gets accepted can be extraordinarily profitable for the adversary. However, the same is not true for the hero – the hero gets nothing of the TVL by winning.”

In my opinion, this is one of the most most powerful and dangerous ideas here. The concept that the TVL in a rollup can be effectively weaponized against its own fraud proof mechanisms is quite alarming. Attackers are capable of utilizing the full extent of the TVL to trustlessly bribe more participants into complicity. It’s almost like if one could use all the money stuck on Uniswap to attack Ethereum’s PoS. It’s hard to develop an algorithm under these constraints.

I love the  initiative to develop a better framework that allows us to reason about fault proofs in a more structured way. Kudos for that.

Despite the title, this piece does a good job at reflecting on the tradeoffs. I just wanted to reiterate:

These systems are not inherently “broken”. They do provide substantial utility and could be beneficial, under certain limited conditions. The PRT, for example, seems particularly appropriate for application-specific rollups (especially with new ideas coming up to reduce the impact of settlement delays).

However, if we’re to shift a significant portion of execution to these rollups and have them manage insane amounts of TVL without “training wheels,” I definitely agree that we need to do better!

---

**edfelten** (2024-04-08):

There seem to be several flaws in the game theory analysis here. For one, if the claim is that the adversary stands to gain the full TVL of the chain, then it is also the case that the parties who have assets on the chain will have an equal incentive to preserve that same TVL. The would-be thief has something to gain; but the would-be victims have just as much to lose – by definition.

Also, the contest between adversary and honest parties is asymmetric, to the honest parties’ advantage. If the adversary and honest parties invest equally, the honest parties will win the challenge and get their stake refunded, whereas the adversary’s stakes will be slashed. So staking is inherently more expensive for the adversary than for honest parties–the adversary loses their money, but the honest parties only need to lock up their money until the protocol ends.

---

**GCdePaula** (2024-04-08):

Let’s try to reach a common understanding of the problems fraud proof systems are dealing with. Consider the hero has a two-fold advantage over the adversary; if the adversary has twice the resources they’ll steal the entire TVL.

> For one, if the claim is that the adversary stands to gain the full TVL of the chain, then it is also the case that the parties who have assets on the chain will have an equal incentive to preserve that same TVL. The would-be thief has something to gain; but the would-be victims have just as much to lose – by definition.

Relying on the would-be victims mean each would-be victim has to both:

- run a validator node;
- keep half the amount of funds in L1 as they have locked in L2.

The analogy would be a bank suffering an attack by hackers. Imagine you have $200k in an account. The bankers tell the account holders their money may be completely stolen. But the bankers have a plan. First you’ll have to deposit an extra $100k (besides the $200k already in the account) in some security company working for the bank. (Alternatively, you can follow some steps on GitHub.) If all account holders do the same, then the attack will be foiled. After all is done, you’ll get your $300k back.

This isn’t a good position to be in.

We’d also argue you can’t rely on the hero being just as coordinated and responsive as the group who has planned a multi-billion dollar heist.

> Also, the contest between adversary and honest parties is asymmetric, to the honest parties’ advantage.

This doesn’t contradict the OP.

Our claim is that it’s reasonable to assume the adversary is better funded than the hero.

---

**felipeargento** (2024-04-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/edfelten/48/11460_2.png) edfelten:

> Also, the contest between adversary and honest parties is asymmetric, to the honest parties’ advantage. If the adversary and honest parties invest equally, the honest parties will win the challenge and get their stake refunded, whereas the adversary’s stakes will be slashed.

[@edfelten](/u/edfelten) that’s true that a group of honest parties could theoretically coordinate. But fault proofs adopt the premise of a single honest defendant for a specific reason. To justify moving execution from L1 to any rollup—and alleviate the burden on Ethereum nodes to improve scaling—we must do much much better than the 33% (or whatever) honest stakers assumption of the base layer PoS.

The moment we start discussing the need for coordination among honest participants, it’s the moment we lost that battle imo.

---

**edfelten** (2024-04-09):

The honest parties don’t need complex coordination. The fact–which you haven’t rebutted–is that the honest parties will get their money back, so they only need to lock up that money for a short period, whereas the adversary will lose their stake money.

Combine that with the fact that a properly designed protocol requires that if an adverary is trying a stake exhaustion attack, the adversary must stake significantly more than the honest parties do.

So that’s two big advantages for the honest parties: (1) the honest parties have to stake significantly less than the attacker, and (2) the honest parties will get their stake returned but the adversary will lose theirs.

---

**GCdePaula** (2024-04-09):

1. Yes, this is not in contradiction with the original post, where we went in deep detail on this very point. The critical questions are: (a) how significant does this advantage need to be, and (b) how much are the stakes in BoLD to reach that target advantage?
The BoLD paper is scarce on the value of the stakes. This discussion will be more productive if you can supply them.
2. Yes, this is not in contradiction with the original post. The adversary has to burn stakes to steal the entire TVL. It’s reasonable to assume the adversary is willing to burn a couple billion to win many billions.

I urge you to reread the original post.

---

Reiterating the point of this endeavor: this is a call for collaboration. If I didn’t care about our collective success, I wouldn’t have shared my concerns.

I believe we can design better algorithms, and I believe we can better achieve that together. I know it’s wishful thinking, but I surely can hope for constructive conversations.

---

**augustoteixeira** (2024-04-10):

So, in summary:

1- Optimism’s - vulnerable to 51% stake attacks.

2- PRT - could induce several weeks of delay.

3- BoLD - vulnerable to 91% stake attacks.

Besides this, both Optimism and BoLD require the hero to have a cluster of computers to defend against the attack. Although, if they successfully do so, both algorithms return the funds to the hero and burn the funds of the attacker.

This is a very worrisome fine print that is missing on the typical statement:

“It is enough to have one honest node runner to defend the chain”.

---

**edfelten** (2024-04-10):

Definitely in favor of collaboration.

(That said, most calls for collaboration on a class of protocols are not titled “[this class of protocols] are broken”.)

---

**GCdePaula** (2024-04-10):

That’s good to hear `:)`

As for the title, we included our protocol in the analysis as well. I truly believe we can design better systems. The first step is making the issues known and reaching a common understanding of the challenges facing current fraud proof algorithms.

Now, other than your objection to the form, it’s still unclear whether you agree with the substance of our argument. Can we start a collaboration by figuring out where you stand?

---

**ajsutton** (2024-04-10):

Note: I work for OP Labs but this is entirely my own opinion.

Thanks for this, I agree that there are plenty of challenges still left in the fault proof space to solve. One of them as you note is the proof of whale issue. However, there are points in this analysis that rely on overly-simplified criteria and I wanted to elaborate and add context to several:

The biggest issue I’d point out begins in the “What’s at stake” portion, in particular:

> A dispute puts the total value locked (TVL) of a rollup at stake. An incorrect states that gets accepted can be extraordinarily profitable for the adversary. However, the same is not true for the hero – the hero gets nothing of the TVL by winning.

While an accepted incorrect state can allow an attacker to steal the TVL, that doesn’t mean they are more highly incentivised than honest actors.  As [@edfelten](/u/edfelten) points out, the honest actors stand to *lose* to the TVL which makes them at least as well incentivised. But beyond that, the chain operator also stands to lose all future sequencer revenue, the value of any chain-related tokens they hold (including any potential direct and indirect benefit from as yet undistributed tokens) and other ecosystem participants stand to lose their investments and future benefits. Beyond the economics, chain operators are also incentivised to be honest actors by not wanting to see everything they’ve built be ruined. I think there’s a pretty strong argument that the honest actors are actually more highly incentivised than dishonest ones.

Ultimately, the key constraint on participation for honest and dishonest actors isn’t incentivisation - it’s availability of resources. While attackers stand to gain the TVL they can’t use any of it in the attack and have to already be extraordinarily weathly and risk extraordinarily large amounts of funds in the hope that they can outspend all honest actors combined. Again, that doesn’t mean there isn’t a proof of whale issue at all or that we can’t do better, but it does make it unreasonable to boil it down to a single tick-box for “Safety”.  And importantly, the analysis of systems should be considering availability of funds which is currently entirely ignored, not what stands to be gained.

And I’d echo a lot of [@edfelten](/u/edfelten)’s comments too, particularly around the advantage honest actors have because they can expect to get the bonds back whereas dishonest actors have a huge risk of losing it all. That reduces the availability of funds because it’s hard enough to convince people to fund illicit activity, but even harder when it’s high risk.

To the proposed criteria:

> the base layer works (but can be arbitrarily censored for up to a week)

If the base layer can be arbitrarily censored for up to a week I believe all these systems fail as they typically have a total time of one week but require multiple transactions to be sent - even if the specific configurations allow more than a week, I suspect being censored for a week would at least put the honest actors at a very significant disadvantage. And it isn’t necessarily the right trade off to extend timelines such that a full week of censorship can be tolerated given that further delays user withdrawals.  Fortunately, I believe the time required for EIP1559 to burn all ETH in existence if someone is censoring the chain can be measured in hours given its exponential nature. There are other potential avenues like via block builders but they’re also surprisingly difficult to pull off (despite what a simplistic view might suggest based on number of blocks using MeV builders - that’s not the whole story). If we’re building criteria around it, we should aim to do better than pick an arbitrary number.

> the presence of at least one honest validator

What does it mean for the honest validator to be present? The proof of whale attacks are all focussed on exhausting the honest actor’s resources so they can no longer be present in the system. If the assumption is that an honest but entirely unfunded validator is present then all systems fail. The decentralised criteria already captures whether the requirements for honest validators are high or low so it shouldn’t be conflated here.

In particular, I think it’s overly simplistic to say that a system is unsafe if it assumes that honest attackers have at least the same availability of funds/resources as dishonest ones.  If an attacker has sufficient funds, they can perform double-spend attacks by re-orging the chain under both PoS and PoW. Does that make Ethereum and Bitcoin both unsafe? No, we consider the safety of the chain by estimating what the cost of an attack would be and then considering if it is viable for someone to acquire the required resources to execute the attack. Similarly, a simple safe/unsafe evaluation is inappropriate and misleading here.

My suggestion would be to have this focus on correctness. Given the presence of a sufficiently resourced honest actor, the system correctly determines the validity of all proposed outputs. I’d also call it Correctness, not Safety - far less provocative and more accurately focussed to what is actually being evaluated.

Note also that it is insufficient for a system to reject all invalid outputs as an attacker could cause a liveness failure by rejecting all valid states (which then prevents users withdrawing and breaks the safety requirements of the L2). Admittedly there is some nuance here in that allowing a single invalid output to be accepted is catastrophic but allowing some valid output roots to be invalidated isn’t necessarily an issue (as long as some outputs are accepted and allow users to complete withdrawals without too much grief).

> In an ideal world, we want the honest validator to win any dispute in a timely manner using nothing more than a toaster.

This isn’t necessarily true. While it is good to minimise resources required, if you want to ensure minimal requirements, use L1. Its limited throughput is in a large part due to wanting to keep the required resources for validating the chain reasonable. L2s exist to scale so it seems quite reasonable that the required resources for validating the chain would be higher to enable greater throughput. Notably this evaluation completely ignores the cost of running a node on the L2 chain which is a requirement for participating in any fault proof system and the cost of running an L1 node which is required to avoid censorship on L1 and there are many other details that affect the requirements for participation in a fault proof game beyond the bonds that the analysis currently considers.

Ultimately, there’s a wide range of trade offs that can be made in this space for good reasons so it seems unreasonable to make running on a toaster a requirement - especially when it’s summed up in a rather misleading “decentralized” title - there’s far, far more to achieving decentralisation than low resource requirements!

The criteria also fails to capture the requirement that the honest actor is sufficiently compensated to participate in the game. Viable systems must ensure that the honest actor is compensated for *all* actions it must perform to ensure correct outcomes. This compensation must be sufficient to at least cover the costs of performing the actions (including any off-chain computation/resources and gas costs).  Otherwise the system is susceptible to the tragedy of the commons where everyone assumes someone else will perform the honest action but no-one actually does (even if it’s crazy cheap!).

Given the analysis of each system is based on these criteria, I won’t go into them in any real detail, but it’s worth mentioning a couple of things that stood out to me:

> Call for open and public research collaboration between the optimistic rollups teams. This is a personal frustration of mine. Our attempts at public communication with these teams haven’t been successful at eliciting substantive academic discourse on the vulnerabilities and tradeoffs for existing fraud proof algorithms.

There’s always opportunity to better collaborate, but the OP fault proof system has been built entirely in the open with inputs from teams across the ecosystem.

> A game is played by countering claims. But since claims are countered mainly by adding child claims to the DAG, we’re entering the territory of countering counters all the way down to the one-step proof. Countering a counter uncounters the original claim. In the end, in order for a claim to be considered uncountered, all of its children must be countered. To consider a claim countered, it’s enough that a single one of its children is uncountered. The hero protects the correct game by countering the faulty claims that have countered the correct claims. The hero exposes faulty games by countering its root claims, and countering all the counters to their counters.

I think this is the worst attempt at explaining the OP dispute game I’ve ever come across. What you’re describing is a bisection over the state transition function by posting claims and counter claims.

> This can be further improved by choosing the bisections in a way that the hero has to always compute a new state (in the worst case, the adversary can force the hero to post the entire computation on-chain).

If the adversary forces the hero to post the entire computation on-chain they would be using so much gas that they would be censoring the entire L1 chain which our assumptions say is impossible. Also the game is configured such that the person proposing the output root is the one who will ultimately execute the on-chain step computation. There are a surprising number of situations in blockchains where a system has a theoretically unbounded variable that is actually bound to often surprisingly low values in practice because of things like the availability of block space or the total available supply of ETH. As such it’s important to consider these broader limits when evaluating a system.

One of the advantages of not using a computation hash is that the honest actor does *not* need to compute the hash of every step of the trace, but only does so in response to the actually posted claims. This reduces the upfront computation required by the honest actor and ensures the attacker must expend at least some funds (and post a bond) before the honest actor has to expend resources on the computation.  The bonds are tuned such that the honest actor will be compensated for the computation they would be required to perform.

That’s not to say that the requirements for honest actors are low, or that a dishonest actor can’t win by significantly outspending an honest attacker. However, it’s another example of how this isn’t a simplistic yes/no question and the proposed criteria are ineffective at capturing that.

> If a player is a block producer in the base layer (or has a generous friend who is), they will have blockspace access without expending funds for transaction costs.

This is a fundamental misunderstanding of the way EIP1559 works. It is not possible for *anyone* to access block space without expending funds on Ethereum. They must always pay the base fee. Block producers can include transactions with no inclusion fee but the inclusion fee is typically negligible on Ethreum because of the way the base fee scales to target 50% full blocks, thus avoiding fee based auctions for block space.

> we can leverage ZK proofs and change the state-transition function from one VM step to several VM steps. This makes the single-stage setup possible in practice. Note that this is still an interactive fraud proof; it’s just a change to its state-transition function.

I’d would suggest this is now a hybrid - it is as you say still an interactive fraud proof, but it’s *also* a ZK proof and inherits the challenges, limitations and complexities of ZK proofs which have been entirely omitted from this analysis. If ZK is the answer, I’d ask why not just ditch interactive proofs and use ZK.

Anyway, as I mentioned above, I agree there are threats and work should continue towards trying to address them in better ways. Hopefully this provides some additional perspective to help us move towards a more useful set of evaluation criteria that properly captures the complexities and trade offs involved.

---

**GCdePaula** (2024-04-11):

I really appreciate your reply. Thank you. I’m mostly aligned with what you said, although it shifts the 1-of-N goal to something strictly less safe. I’m still optimistic we can keep 1-of-N, settling fast, and the toaster.

I see the 1-of-N and permissionless-ness, together, as the most important properties of fraud proofs. One way to frame these properties is: a single honest validator can stand up to the world and win against any number of malicious claims, and that honest validator can be you.

I can make a great case for an Ethereum rollup with these two properties inheriting the security of Ethereum. It’s a lot harder to make this case if the single honest party needs 51% or 91% of stakes.

This is my core concern with BoLD and OPFP, and I think it’s the main misalignment I have with your reply; 1-of-N is quite different from “a ratio of honest stakers”. Maybe for the Optimism, Base and Arbitrum networks it’s easier to now bootstrap a 51% of stakes security; you’re more valuable than most L1s out there. New rollups (L2s, L3s, application-specific or shared) don’t have this benefit. I don’t see a future where scalability is solved by only a couple huge rollup instances.

I’ll highlight the following sentences:

> If the assumption is that an honest but entirely unfunded validator is present then all systems fail.
> (…)
> Given the presence of a sufficiently resourced honest actor, the system correctly determines the validity of all proposed outputs.

Not all kinds of “sufficiently resourced” are the same. There are worlds of difference between `O(1)` and `O(N)`.

Yes, the hero needs sufficient resources. Ideally, we’d like a toaster and one stake to be enough, as to make validation more accessible. Requiring several toasters and several stakes instead is not a threat to safety, it just makes validation less accessible.

It is a threat if “sufficiently resourced” actually means “as many resources as the attacker”. Here, the toasters and stakes grow linearly on the number of Sybils. It’s exactly by this mechanism the adversary can exhaust the hero.

We can’t group “as many resources as the attacker” and “a constant number of toasters+stakes” together under “sufficiently resourced”. Being `O(Sybils)` violates the 1-of-N assumption we all claim to have, significantly weakening the system, whereas `O(1)` doesn’t.

I think I’d be comfortable with `O(log(Sybils))`, depending on the constants. PRT is `O(1)` – we might be willing to sacrifice `O(1)` for `O(log(Sybils))` if we get faster settlements. I’m very concerned with `O(Sybils)`.

---

These are the main points. I’ll comment on a few more, but it’s mostly in agreement or minor. Here’s one toaster with one steak fighting a horde of Sybils:

[![WHAT IS YOUR PROFESSION!](https://ethresear.ch/uploads/default/optimized/2X/3/35be7167b15cdef74d6d0db43b2db75e5aa29936_2_440x440.jpeg)WHAT IS YOUR PROFESSION!1024×1024 250 KB](https://ethresear.ch/uploads/default/35be7167b15cdef74d6d0db43b2db75e5aa29936)

---

> The biggest issue I’d point out begins in the “What’s at stake” portion (…)
> (…) the honest actors stand to lose to the TVL (…)
> I think there’s a pretty strong argument that the honest actors are actually more highly incentivised than dishonest ones.

I’d highlight there’s a difference between validators defending a rollup and users who have funds locked in the rollup. Users are the ones who stand to lose their funds. Validators will only lose their bonds.

We can consider users are incentivised to run and fund validator nodes. But for them to coordinate and together be better funded than the adversary, it would require each to hold funds in L1 proportional to what they’ve already locked in L2. Let’s ignore the tragedy of the commons and assume perfect coordination. It isn’t ideal to require each user to match their locked L2 funds in L1.

If not the users, it’s not ideal to require a non-user to have these resources. The same resources that could be used to protect the rollup could be used to attack it; if someone has these resources while not having funds in the rollup, they might as well attack the rollup.

---

> If the base layer can be arbitrarily censored for up to a week I believe all these systems fail

I disagree, but perhaps I phrased the original ambiguously. We consider the adversary can arbitrarily switch between two regimes: standard regime and censorship regime. On the latter, the adversary can censor any set of transactions they wish. The time the adversary stays in the censorship regime has to total at most one week. In PRT, matches take a week (censorship tolerance) plus enough time to include transactions in the standard regime. I believe BoLD does something similar. I was under the impression OPFP did the same. I think they’re all safe in that regard.

I agree the folkloric wisdom of one week is perhaps too extreme. I kept it because it seemed all our systems used it. I agree we should do better than pick an arbitrary number. I have no model to reason about this. Can you weigh in?

---

> L2s exist to scale so it seems quite reasonable that the required resources for validating the chain would be higher to enable greater throughput.

Yes, but are these extra resources being put to increase the throughput? I don’t mind choosing a large reference computer for L2, as long as you’re ok with fewer validators. I mind the number of required toasters growing depending on how much money the attacker has. You’re not putting these toasters to process more transactions, you’re putting them to fight Sybils, growing linearly.

PRT requires one laptop always (or a larger computer if you want more scalability), doesn’t matter how well-funded the attacker is. You will need to keep the laptop on for longer if under attack though. Also, modern hardware that can handle a L1 node can simultaneously handle PRT on a separate core.

Because of this, I believe the one toaster requirement is a property we can try to keep. I believe it would make it easier to compensate the honest parties too. I think much of your analysis on the toaster isn’t considering how the amount of work of the honest parties grows linearly with the number of Sybils.

---

> If the adversary forces the hero to post the entire computation on-chain they would be using so much gas that they would be censoring the entire L1 chain which our assumptions say is impossible.

Yes, it’s not possible because of L1 constraints, but it’s conceptually allowed. Concretely, my point is that the adversary can always force the hero to process a new state, linearly on Sybils, invalidating any caching strategy.

---

> One of the advantages of not using a computation hash is that the honest actor does not need to compute the hash of every step of the trace, but only does so in response to the actually posted claims.

This is indeed the advantage. We should analyze the tradeoffs. Considering sparse computation hashes, the performance impact is negligible, at least on our VM. Considering dense computation hashes (or at least dense enough for ZK), it’s complicated. We’re still optimizing state hash on our end, and the zkVMs have improved a lot since we last measured.

One approach is a system that eagerly does the computation hash. We change the claim to really be a computation hash. This allows you to shave a week off of disputes, and it’s easier on the toaster, but it reduces throughput. Alternatively, you can only start doing the computation hash once there’s a dispute; claims are final states at first. This adds one week to disputes, and it’s harder for the toaster since it has to keep up to date with the ongoing rollup while it’s reprocessing previous transactions.

If the overhead of computation hashes is 2x, but we achieve all the goals we want, I’d be ok with that.

---

> This is a fundamental misunderstanding of the way EIP1559 works.

I stand corrected.

---

> I’d would suggest this is now a hybrid

I wouldn’t! The proof being created is over a constant number of VM instructions, and not proportional to the size of the computation. To me, it’s really an implementation detail of the state-transition function. It has the same properties as an interactive fraud proof. Maybe my concern is how others use the term “hybrid”, where the entire claim is ZK proved.

Furthermore, ditching fraud proofs in favor of doing the whole thing in ZK will kill the scalability and efficiency of our systems. Depending on the computation, we can run our VM close to 0.5GHz in a modern CPU. We have some ideas (that we’d happily discuss!) to ditch even the VM overhead and execute everything in bare metal (up to a few specific points in case of a dispute). I wonder whether ZK is able to match that, and I wonder how many supercomputers it would take to do it. ZK rollups are great, but so are ORU.

---

> Anyway, as I mentioned above, I agree there are threats and work should continue towards trying to address them in better ways. Hopefully this provides some additional perspective to help us move towards a more useful set of evaluation criteria that properly captures the complexities and trade offs involved.

It does add additional perspective, and I think it does help us move further!

On our side, we’re researching new algorithms. We haven’t been doing a good job of making this research public. We’re changing that: we’ll post everything we have soon and try to hold the process itself in public. Just your feedback will help a lot, like your detailed reply.

Do you have any suggestions moving forward?

---

**edfelten** (2024-04-15):

The Offchain Labs team just released a new paper on BoLD, which includes an updated algorithm, analysis, proofs, and comparison to Cartesi, including some improvements to Cartesi’s published algorithm.



      [github.com](https://github.com/OffchainLabs/bold/blob/59682703c344ae44bd545384c7e351b4ffbeb186/docs/research-specs/BOLDChallengeProtocol.pdf)





####

  This file is binary. [show original](https://github.com/OffchainLabs/bold/blob/59682703c344ae44bd545384c7e351b4ffbeb186/docs/research-specs/BOLDChallengeProtocol.pdf)

---

**vuittont60** (2024-04-16):

Collaboration and open research are essential for improving fraud proof algorithms and ensuring the security and decentralization of optimistic rollups.

---

**cryptskii** (2024-05-13):

what about?

To insure 1-of-N security in optimistic rollups by allowing any honest validator to generate fraud proofs we use the follow setup:

## Definitions

- \mathcal{S}: set of states
- \mathcal{T}: set of valid transitions
- f: \mathcal{S} \times \mathcal{T} \to \mathcal{S}: state transition function
- t^*: proposed transition
- s_0: initial state
- s_n: final state
- \Delta t: challenge period

## Fraud Proof Generation

Decompose t^* into subtransitions \{t_1, \ldots, t_k\}:

```python
subtransitions = []
remaining = t*
while remaining != ∅:
    t_i = ExtractSubtransition(remaining)
    append(subtransitions, t_i)
    remaining = remaining \ t_i
return subtransitions
```

Generate fraud proof by applying each t_i to s_0:

```python
s = s_0
for i = 1 to k:
    s = f(s, t_i)
    if s == s_n:
        return ⊥ # Valid, no fraud
return (s_0, {t_1, ..., t_k}, s) # Fraud proof
```

## 1-of-N Security Theorem

If decomposition satisfies properties and \Delta t \geq K \cdot C, a single honest validator can generate fraud proofs.

This ensures 1-of-N security and decentralization in optimistic rollups.

---

**PaulRBerg** (2024-05-24):

Thanks to everyone for sharing your thoughts in this thread. I learned a lot by reading your comments.

![](https://ethresear.ch/user_avatar/ethresear.ch/ajsutton/48/15963_2.png) ajsutton:

> I believe the time required for EIP1559 to burn all ETH in existence if someone is censoring the chain can be measured in hours given its exponential nature

Can you expound on this, [@ajsutton](/u/ajsutton)?

Wouldn’t the base fee and the amount of ETH burned *decrease* over time if Ethereum is censored? Blocks would be under-filled.

---

**pedroargento** (2024-07-12):

There was a really nice panel on ETHCC Brussels about fraud proofs, with a lot of the panelists being active in this thread. I dont have permission to  post links, but here is the end of the youtube url:

*/live/TVhyiGfYgVM*

---

**GCdePaula** (2024-11-12):

We have publishing a new fraud proof algorithm that is truly decentralized while being resistant to Sybil attacks.

We address the issues outlined in the original post: delay attacks, resource exhaustion attacks (proof of whale), and centralization due to high bonds.

We hope to get feedback from the wider community.


      ![](https://ethresear.ch/uploads/default/original/2X/c/c683569a48ce1952ba841c851ae3b1f282d4b00f.png)

      [arXiv.org](https://arxiv.org/abs/2411.05463)



    ![](https://ethresear.ch/uploads/default/optimized/2X/d/db11c4139de0d4f279af48f5a1ade7b5181d481b_2_500x500.png)

###



In this paper, we introduce a new fraud-proof algorithm that offers an unprecedented combination of decentralization, security, and liveness. The resources that must be mobilized by an honest participant to defeat an adversary grow only...

---

**GCdePaula** (2025-02-27):

We’ve published a [new post on this forum](https://ethresear.ch/t/the-dave-fraud-proof-algorithm/21844), about the new Dave algorithm. We believe Dave may represent a significant step forward in fraud proof protocols. At the same time, we are eager to engage with the community — especially those working on similar challenges — to refine these ideas further. Your insights and feedback will be invaluable as we continue to develop and enhance Dave.

Cheers!

