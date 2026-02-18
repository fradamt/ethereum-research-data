---
source: ethresearch
topic_id: 21844
title: The Dave Fraud-Proof Algorithm
author: GCdePaula
date: "2025-02-27"
category: Layer 2 > Optimisitic Rollup
tags: [fraud-proofs, sybil-attack]
url: https://ethresear.ch/t/the-dave-fraud-proof-algorithm/21844
views: 1466
likes: 11
posts_count: 9
---

# The Dave Fraud-Proof Algorithm

# The Dave Fraud-Proof Algorithm — Triumphing over Sybils with a Laptop and a Small Collateral

*(a.k.a. Fraud Proofs Are **Not** Broken)*

The security of fraud proof systems hinges on two key properties: *you* should be able to become a validator (even if you’re broke), and *you* should be able to prevail over any number of dishonest validators (even if they’re a nation state). Together, these two properties allow an optimistic rollup to inherit the security of Ethereum. In addition, we require a third property: that disputes settle in a timely manner.

As it turns out, it is quite hard to design algorithms that adequately fulfills these three properties — **allowing just anyone to participate opens the floodgates for an attacker to create as many Sybils as its resources allow.**

Last year, in an [ethresearch post](https://ethresear.ch/t/fraud-proofs-are-broken/19234), we showed that no algorithm at the time adequately satisfied all three properties. They were vulnerable either to resource exhaustion attacks or delay attacks, and mitigation strategies inevitably restricted participation. As a result, all implementations were destined to be suboptimal. This is particularly worrisome, given that over 90% of all value secured by rollups is poised to be protected by fraud proofs.

In November 2024, we [published](https://arxiv.org/abs/2411.05463) our novel research on this topic, introducing the Dave algorithm — a new fraud-proof algorithm that is resilient to Sybil attacks. We later [presented](https://youtu.be/dI_3neyXVl0) our findings at Devcon SEA.

In this post, we provide a concise overview of the algorithm and its results. While Dave builds on established concepts in fraud proof protocols, it also introduces several novel techniques that address longstanding challenges, such as resource exhaustion attacks and delay attacks. We believe these advancements may represent a significant step forward in the field. At the same time, we are eager to engage with the community — especially those working on similar challenges — to refine these ideas further. Your insights and feedback will be invaluable as we continue to develop and enhance Dave.

Note that this post focuses on the theoretical properties of the Dave algorithm rather than its current development stages. We assume the reader is generally familiar with fraud proofs, and we have left the more technical details to the full paper. Interested readers are encouraged to read the paper for an in-depth analysis.

## Resources

- Permissionless Refereed Tournaments (PRT) — our first algorithm, which introduces the computation hash (a.k.a history commitments), tournament brackets, and recursive disputes.
- Fraud Proofs Are Broken (but we can fix them) — our ethresearch post that started it all.
- Fraud Proof Wars by Luca Donno from L2Beat — an in-depth analysis of fraud proof approaches, algorithms, and trade-offs. There’s also his Devcon SEA 2024 talk of the same title.
- Dave: a decentralized, secure, and lively fraud-proof algorithm — our paper detailing the Dave algorithm.
- The Dave Fraud-Proof Algorithm: triumphing over Sybils with a laptop and a small collateral — our Devcon SEA 2024 talk on the Dave algorithm (here are the slides).

## TL;DR

There are three properties we need from permissionless fraud proof protocols:

- security — an attacker must spend an impractical quantity of resources to defeat any single honest validator;
- decentralization — participation is unrestricted, either by imposing a permission list or demanding the deposit of expensive bonds;
- liveness — disputes settle in a timely manner.

Dave allows (**but does not require**) honest validators to cooperate trustlessly, playing collectively as one. We refer to this collective of honest players as the *hero*, and we call the attacker and its mob of perfectly coordinated Sybils the *adversary*. We’ll use the terms validator and player interchangeably.

Launching a Sybil attack in Dave is exponentially expensive for the adversary, relative to the resources the hero must allocate to prevail. In practice, this enables a singleton hero to triumph against nation-states — even with cheap bonds and no permission lists. The hero requires only a constant amount of hardware to participate in Dave, regardless of the number of Sybils, and the costs incurred are reimbursed after the dispute is resolved.

Crucially, settlement delay grows logarithmically on the number of Sybils, but with a key advantage over [Permissionless Refereed Tournaments (PRT)](https://arxiv.org/abs/2212.12439): the constant multiplying the logarithm is one order of magnitude smaller. As a result, Dave settles disputes within 2–5 challenge periods for any realistic number of Sybils.

[![have you tried logarithms?](https://ethresear.ch/uploads/default/optimized/2X/1/1afc14e3db541a2c67ed0bf8b0221edcf44c96ba_2_296x303.jpeg)have you tried logarithms?872×894 88.3 KB](https://ethresear.ch/uploads/default/1afc14e3db541a2c67ed0bf8b0221edcf44c96ba)

---

Below, we compare Dave with three other fraud proof algorithms: [OPFP](https://github.com/ethereum-optimism/specs) from Optimism, [BoLD](https://arxiv.org/abs/2404.10491) from Arbitrum, [PRT](https://arxiv.org/abs/2212.1243) from Cartesi, and Dave (also from Cartesi). We consider a scenario where an attacker burns *1 million ether* to launch a Sybil attack.

This comparison focuses on three key properties:

- Bonds: setting bonds too high undermines decentralization by excluding potential validators;
- Hero’s Expenses: excessive expenses compromise security — if the hero lacks sufficient funds to cover costs, the adversary will win and steal the total value secured (TVS);
- Delay: high delays harm liveness by slowing dispute resolution.

Note how Dave strikes a favorable balance between bonds, expenses, and delay relative to competing methods.

|  | Bond | Expenses* | Delay |
| --- | --- | --- | --- |
| OPFP | 0.08 ETH | 1,000,000 ETH | 1 weeks |
| BoLD | 3,600 ETH | 150,000 ETH | 1 weeks |
| PRT-1L | 1 ETH | 1 ETH | 20 weeks |
| Dave | 3 ETH | 7 ETH | 3 weeks |

* Expenses are reimbursed to honest parties after the dispute is over.

Although burning 1 million ether a very expensive attack, BoLD currently protects more than three times this amount ([see L2BEAT](https://l2beat.com/scaling/projects/arbitrum#tvs)) — it is conceivable, provided that it has an appreciable chance of succeeding.

## Threat and resource model

The security of optimistic rollups depends on certain assumptions concerning the way blockchains operate. We assume that all transactions are processed correctly, eventually. However, we also assume that the adversary can subvert this process, to a limited extent, by:

- Censoring transactions: The adversary has the power to delay any set of transactions. The only limitation to this power is that the total amount of time during which it is exerted cannot exceed one week. This means the adversary may choose to use up all its budget in one go and delay any set of transactions for a week, or partition its budget in multiple spans of censorship.
- Reordering transactions: The adversary has the power to reorder incoming transactions on the blockchain, for example by front-running honest validators.

Interactive fraud-proof protocols require players to take turns when interacting with the blockchain. If no deadlines are set, the adversary could stall a dispute indefinitely. Conversely, the adversary could use its censorship budget to force the hero to miss a deadline. Fraud-proof algorithms must therefore take the censorship budget into account when setting the penalties incurred for missing any deadline.

It is quite a challenge to design lively protocols around a one-week censorship assumption. Pessimistically setting the deadline of every interaction to at least 1 week would ruin the liveness of any protocol. Protocols commonly use strategies like chess clocks to amortize this 1 week over many interactions. Dave introduces a novel technique that amortizes it over the entire dispute.

Players interact by making *moves*, which require spending resources (gas, compute, and/or bonds). The only hope an adversary has to defeat the hero is to exhaust its resources, preventing it from taking part in the dispute and compromising the security of the algorithm. Because of this, it is not sufficient to consider the hero as the total number of honest agents. The analysis must include the resources held by the hero as well. We need a more nuanced understanding of what “one honest validator” means.

For that, we take inspiration from [Vitalik’s post](https://vitalik.eth.limo/general/2020/08/20/trust.html). He describes trust as the use of any assumptions about the behavior of other people, classifying trust models as “the ability of the application to continue operating in an expected way without needing to rely on a specific actor to behave in a specific way”. When an algorithm allows N players to participate but requires M of them to be honest, he argues, M should be as small as possible (ideally 1) and N as large as possible.

[![Trust Models](https://ethresear.ch/uploads/default/optimized/3X/e/4/e4535b1f8532714fdca47187096bf2895da2aec5_2_480x425.png)Trust Models640×567 26.8 KB](https://ethresear.ch/uploads/default/e4535b1f8532714fdca47187096bf2895da2aec5)

(*From Vitalik’s [Trust Models](https://vitalik.eth.limo/general/2020/08/20/trust.html)*)

This maps naturally to what we have described as security and decentralization. In the context of fraud proofs, decentralization demands an arbitrarily large value for N, and security demands — *in addition* — that M be 1. Algorithms that have these two properties (i.e., a single honest validator can enforce the correct result, and that validator can be anybody) inherit the security of the base layer. Through this lens, we define “one honest player” not as an individual agent, but rather as a unit of a total of N resources, M of which are spent to defend the correct behavior.

We assume the existence of at least one honest player.

## The Computation Hash

Claims in Dave, like in PRT, are a computation hash: rather than committing only to the final state of a computation, validators now commit to the entire path of a computation. A computation hash is a Merkle tree where each leaf corresponds to an intermediary state in the execution history.

Now every bisection during the dispute must be accompanied by a valid proof that the segment is consistent with the original computation hash. This requirement prevents validators from lying during bisection; once committed, players can no longer lie during bisection. In particular, an adversary that posts the honest computation hash cannot single-handedly lose the game on purpose.

Unfortunately, building computation hashes that contain all state transitions is extraordinarily expensive if the state transition is a small VM step. In PRT, we proposed recursive disputes to mitigate this cost, but it introduces other problems. In Dave, we instead change the state transition from one VM step to several VM steps, and use a validity proof (i.e. a ZK proof) for the final one-step proof.

## Dave

Dave, like PRT, employs a divide-and-conquer strategy that forces Sybils to eliminate one another, so that the hero never has to personally fight and defeat every single Sybil. To this end, we use a tournament-like matchmaking mechanism to pit competing claims against each other.

Our first attempt, PRT, used a simple bracket tournament that gives the hero an exponential advantage both in resource costs and incurred delays. Dave builds on this by introducing a *repechage* mechanic, not unlike a Swiss tournament. This mechanic, in addition to the exponential advantage, amortizes the one-week censorship assumption over the entire dispute.

Here is an informal overview of a dispute resolution under Dave:

1. The hero submits the honest claim (a computation hash), and each Sybil submits a dishonest one. Claims are unique. All competing claims must be posted within 1 week. Rounds start as soon as there is more than one competing claim;
2. At the start of a round, Dave partitions all surviving claims into small groups of size G, following a specific matchmaking rule that we’ll describe later. One can think that G = 2 for most cases. Each group spawns one match for every pair of claims within. All matches of all groups in a round are concurrent, starting together and ending together. The round duration is fixed and is significantly shorter than 1 week;
3. A match concludes with one claim defeating the other, either by timeout or through a step action. The claim that wins all its G - 1 matches wins its group, and all the other claims lose;
4. Dave doesn’t eliminate claims outright. Instead, it keeps a tally of the number of times each claim has failed to win its group. When a claim has failed enough times to ensure censorship cannot be blamed, it is eliminated;
5. If at least 1 week has elapsed, and if there is a single surviving claim, then this claim wins the dispute. Otherwise, repeat from item 2.

In the following sections, we’ll go into more details of each piece.

### Match

A match progresses as follows: the blockchain guides the two competing claims through a binary search that progressively *bisects* the computation to pinpoint the earliest disputed state transition. Then, by verifying this single state transition (i.e., executing a *step*), the blockchain identifies the dishonest claim.

At each turn in a match, a validator defending a claim is expected to act with the goal of refuting its opponent. Ultimately, these actions — bisect and step — require submitting a transaction to the blockchain. There are different reasons for which a player might fail to submit bisect or step actions — Sybils may refuse to take actions, or honest participants may be censored. In these situations, we introduce a timeout mechanism that causes the unresponsive claim to forfeit the match.

Recall, however, that there’s a one-week censorship assumption. PRT uses a clock like the ones used in chess matches, which allows for amortizing the cost of censorship over all actions taken throughout a match. The idea is simple: give both claims an initial time budget of 1 week plus the needed time to take all moves (2 hour), and whenever one side is expected to act, keep its clock ticking. Once one of the claims exhausts their time budget, it forfeits the match by timeout. In this setup, it would be safe to eliminate losing claims, since everyone had enough time to have their say. However, considering the optimal delay strategy for the adversary, this makes disputes take `(1 week + 2 hours) * log2 Sybils`, which can still be too long.

Dave uses a similar idea. However, instead of a time budget of `1 week + 2 hours`, it sets a much lower value of 8 hours (a *grace period*) plus the 2 hours to take all moves. (In the paper, we detail why 8 hours minimizes delays.)

Under this shorter budget, eliminating a claim immediately after a timeout would be unsafe, as it might be due to censorship. However, there’s an upper bound on how many matches a claim can lose due to censorship: `1 week / 8 hours`, totalling a maximum of 21 lost matches. After 21 losses, it is safe to eliminate a claim, since the only possible explanation is a Sybil repeatedly running down its clock on purpose.

This mechanism is known as the *hitpoint* (HP) mechanic: every claim starts with 21 HP and loses one HP per timeout. The hero can never lose due to hitpoint loss, because the adversary can, through censorship, force at most 20 timeouts. After the adversary has fired all its shots and left the hero with 1 HP, the adversary will continue to lose its Sybils — mostly due to friendly fire, and ultimately at hands of the hero.

### Matchmaking

The final piece of the algorithm is Dave’s matchmaking rule, which is at its heart. After each round, all surviving claims are repartitioned into new groups. Dave’s goal during matchmaking is to ensure that claims are pitted against opponents with similar HP, to the best extent possible.

The process is straightforward. Dave first sorts all claims by decreasing HP, and then consumes them in order, forming groups of `G` claims each. (Naturally, the last group may have fewer than `G` claims — and should a claim find itself alone in this last group, it is assumed to have won the group.) Without this matchmaking rule, Dave’s liveness would be worse than PRT’s.

Putting everything together, we show an example with four Sybils, and group size `G = 2`, showing how Sybils are grouped, demoted (i.e. lose hitpoints), and eventually eliminated.

[![Dispute example](https://ethresear.ch/uploads/default/optimized/3X/8/f/8f726a73c80d57a39e52a9c2a520ea489aa3cda7_2_690x126.png)Dispute example1643×302 38.7 KB](https://ethresear.ch/uploads/default/8f726a73c80d57a39e52a9c2a520ea489aa3cda7)

## Results

In the paper, we prove that the number of rounds grows logarithmically with the number of Sybils, plus a linear factor on the number of HP (i.e., `O(HP + log Sybils)`). To validate this theoretical result, we further created a program that exhaustively explores the adversary’s decision tree and identifies all maximum delay strategies.

Next, we analyze Dave with respect to liveness, security, and decentralization under a one-week censorship assumption and an eight-hour grace period (meaning 21 HP). While increasing the group size `G` can further improve liveness, it also raises the hero’s resource expenditures, which weakens security. Fortunately, a small group size of `G = 4` adequately fulfills liveness. Therefore, the following discussion uses `G = 4`.

We show the settlement times in the table below, which indicates the total delay in days. We also propose a variant of our algorithm (described in Subsection 7.1 of the paper) that replaces the discrete HP mechanic with a *continuous* tally, to be studied in a future work. This variant could reduce the round duration by about half, thereby significantly improving liveness.

| N | Delay (standard) | Delay (continuous) |
| --- | --- | --- |
| 2^{4} | 21.75 days | 12.08 days |
| 2^{8} | 27.00 days | 15.00 days |
| 2^{12} | 30.00 days | 16.67 days |
| 2^{16} | 33.00 days | 18.33 days |
| 2^{20} | 35.25 days | 19.58 days |
| 2^{24} | 38.25 days | 21.25 days |
| 2^{28} | 40.50 days | 22.50 days |
| 2^{32} | 42.75 days | 23.75 days |

This represents a significant improvement over PRT in terms of liveness. Next, we discuss why Dave’s security and decentralization are as strong as those of PRT.

Remember that decentralization demands that anyone is free (and can afford) to be the hero, and security requires that even a singleton hero can defeat an adversary backed by a nation-state.

The first threat to both security and decentralization comes from hardware requirements. In Dave, the peak transient computational power is independent of the number of Sybils — it remains constant. This means that, from a hardware perspective, Dave is secure (a Sybil attack cannot overwhelm the hero’s compute capacity) and decentralized (the minimum hardware remains affordable).

The next threat comes from gas expenditure and bond requirements. We proved that the number of rounds in Dave grows only logarithmically with the number of Sybils. This gives the hero an exponential resource advantage over the adversary, ensuring that even a lone validator can afford to engage in a dispute against a nation-state. As we showed in the TL;DR, a *1 million ether* attack requires the hero to spend only 7 ETH. Dave is, as such, secure.

In practice, no realistic investment can drain a singleton hero’s funds — at worst, an adversary can only cause delays. This is in contrast with fully parallel algorithms like BoLD, where a well-funded or well-equipped adversary can win. We believe that a modest cost to liveness is preferable to a security vulnerability. This is perhaps the main reason we expect there will be no large-scale Sybil attacks in Dave: the adversary will never win, and delays grow logarithmically with the size of the investment that is ultimately lost.

This exponential advantage effectively decouples bond price from security, enabling bonds to be safely set low so anyone can act as the hero. Even a system with no bonds is secure. Ultimately, bonds in Dave serve as a mechanism to refund the winner for resources it spent in the defense of the honest claim, and perhaps as an added incentive for acting as the hero. Either way, a mispriced bond does not compromise security. By our best estimations, we suggest a bond of 3 ether. Thus, Dave maintains a high degree of decentralization.

## Conclusion

We’ve shown a new fraud-proof algorithm that effectively balances decentralization, security, and liveness.

The barriers to entry, both in terms of bonds and in terms of hardware requirements, are constant and very low. This allows anyone to participate (decentralization). The quantity of resources necessary to mount an attack is exponential both on the delay it manages to cause and on the resources needed to overcome it. This makes it impractical to defeat the honest claim (security). Finally, a new strategy for amortizing censorship over the entire dispute enables punishing unresponsiveness without risking security or introducing large delays. In practice, no dispute will take longer than 2–5 weeks to complete (liveness).

> Thus Dave triumphed over the Sybils with a laptop and a small collateral. Dave had no supercomputer on his hands.
> (1 Samuel 17:50)

## Afterword

The Dave algorithm has had the support of a remarkable group of people. I extend my deepest gratitude to:

- Augusto Teixeira and Diego Nehab, co-authors of the Dave paper.
- Pedro Argento, Stephen Chen and Guilherme Dantas, my co-conspirators in implementing the fraud proof system.
- Felipe Argento, Eduardo Barthel, João Garcia, and Milton Jonathan, for their insightful feedback and thorough review.
- Donnoh for his gracious involvement in reviewing our work.

I also extend my gratitude to [Cartesi](https://cartesi.io) for funding the research and for providing the environment where the development could take place. We invite the reader to join us on [our Discord](https://discord.gg/pfXMwXDDfW), where we continuously engage in public research and debate these topics constantly.

## Replies

**victorshoup** (2025-03-10):

Hi! I am studying the Dave paper on arxiv, and have a few questions.

Hi guys,

I’ve been studying your Dave paper on arxiv and have some questions about a few details.

The first question I have is about the optimization in section 7.1.

In the second to last paragraph on that section, you say:

> The only difference is the lower round duration of the continuous varia. Hence the numbers shown in table 4.

So my question is, if that is the case, why are the round number counts different in tables 2 and 4. For example, in table 2, for N=2^4, you have R=49, while in table 4, for the same N (and G=4) you have R=29?

Based on my own calculations, it seems that R=29 is the correct value, and this is also consistent with the DeltaT values.

Is that correct?

The second question is about the description about the “heuristically optimal delay strategy” in the left column on page 7. There, you say:

> Preserve the claim with fewer demotions in every mixed group, except if doing so would terminate the dispute when doing otherwise wouldn’t.

I don’t quite understand  the “except if doing so…” clause.

Indeed, by my understanding, the dispute will end when the hero wins.

Moreover, the hero wins precisely when there is a single group and all sybils in that group have demotion count K-1 – indeed, if there is more than one group, some sybils will certainly be alive to play in the next round.

So I’m not sure what is being said here – I don’t understand how this case could arise, nor do I understand precisely what the intended “heuristically optimal delay strategy” would be in this case.

Maybe you could describe what this means by example?

Preferably an example with G=2, if that is possible.

Third question. In making certain estimates about the Dave gas expenses (C_m)  and the nominal delay (T_m) for a match, there seem to be some built-in assumptions, such as:

1. The number of bisections per match (i.e., the value B),
2. The nominal delay per bisection,
3. The gas cost per bisection,
4. The nominal delay of computing a snark proof and the gas cost for verifiying it.

I wonder if you could spell out these assumptions – I can’t find them in the paper.

Thanks (in advance) for any help you can give me understanding your paper better!

---

**GCdePaula** (2025-03-11):

Hello Victor! Thank you very much for your interests and thoughtful comments. I’ll try to address your three questions.

---

![](https://ethresear.ch/user_avatar/ethresear.ch/victorshoup/48/19382_2.png) victorshoup:

> Is that correct?

The values are correct, but on closer inspection we inadvertently changed the interpretation of the value R between Tables 2 and 4. Specifically, the values differ by an offset of 20 (i.e., `k-1`). In Table 2, R represents the number of rounds under a scenario where the adversary exercises full censorship power—thus, it relates to `ΔT'`. Conversely, in Table 4, R corresponds to a scenario with no censorship, making it directly related to `ΔT`.

Thank you for catching this inconsistency. We apologize for the confusion and will clarify this distinction in an update to the paper.

---

![](https://ethresear.ch/user_avatar/ethresear.ch/victorshoup/48/19382_2.png) victorshoup:

> I don’t quite understand the “except if doing so…” clause.

To simplify the process of finding an upper bound on the delay the adversary can cause, and make the simulation faster to run and easier to code, we give the adversary two advantages that can only help it. The first is that proofs of the final step do not cause any elimination, but only demotions. The second is that the adversary controls the actions of every claim, even the honest one. It is under this light that the strategy “preserve the claim with fewer demotions in every mixed group, except if doing so would terminate the dispute when doing otherwise wouldn’t”. By the time there are only two claims left, one is at the top and one is at the bottom, and the adversary needs to make sure it doesn’t kill the weakest Sybil, or the dispute would end unnecessarily early.

If you take into account that one of the last two claims is controlled by the hero, and not by the adversary, then the adversary policy for maximizing delay can be simplified to: “Always preserve the Sybil with least demotions”. But then you need to look at the two possible situations when there are two claims left and one of the claims is about to be eliminated. Either the hero is at the top, or the hero is at the bottom. If the hero is at the bottom, then the adversary cannot use censorship anymore. If the hero is at the top, the adversary might still be able to apply some censorship. I feel like this is harder to explain and to code.

---

![](https://ethresear.ch/user_avatar/ethresear.ch/victorshoup/48/19382_2.png) victorshoup:

> I wonder if you could spell out these assumptions

Indeed, our estimates rely on a few assumptions—since we don’t yet have a complete implementation, these estimates are approximate.

We estimate that each match involves a total of 10 rounds of 16-ary dissections, meaning 5 rounds per player. This allows us to handle up to 2^40 state transitions per rollup settlement, a number we consider sufficient, especially when using a “fat” state transition function.

Regarding gas costs, we based our estimates on our work with PRT and extrapolated this data for Dave: each dissection round is estimated to cost around 90,000 gas. Thus, each player would spend approximately 450,000 gas per match (90,000 gas × 5 dissections). While step actions could be taken, it is a poor choice for the adversary since each step action eliminates a Sybil. Therefore, our gas estimates assume step actions do not occur. For reference, however, the on-chain verifier from risc0 consumes about 300,000 gas per verification if such an action is taken.

Our choice of a benchmark gas price P is guided by a robustness analysis of the system against mispricing risks, specifically concerning the possibility of a sustained increase in the average gas price over an entire week. For large values of N, the hero’s expenses are easily covered due to exponentially larger amounts of confiscated funds, reducing the financial risk of mispricing. Moreover, the hero’s actual expenses grow only logarithmically with N, giving them an exponential advantage over the adversary. Conversely, for small N, the reduced number of rounds limits expenses significantly, ensuring that even if reimbursement is compromised due to mispriced P, the actual financial damage remains small. This combination of factors places the system in a favorable position, allowing us to be less pessimistic in estimating P.

Given this robustness, we chose 100 GWei as our worst-case gas price benchmark—during the entire year preceding publication, the weekly moving average gas price never exceeded 100 GWei. Under these assumptions, the estimated gas cost per match C_m (450,000 gas at 100 GWei) totals approximately 0.05 ether.

Regarding the nominal delay (T_m), we’ve set it to 2 hours. This estimate includes about 1 hour allocated for transaction inclusion across the total of 10 dissections and 1 step action, averaging roughly 5.5 minutes per transaction. Such timing is achievable even under scenarios with up to 70% block builder censorship.

This leaves us with approximately 1 hour to generate a validity proof for a computation stride between state hashes. Based on our benchmarks with risc0, we estimate the overhead of ZK proofs compared to bare-metal computations to be roughly 5000x. Given this, each computation stride in the bare-metal implementation should take at most 0.72 seconds (3600 seconds / 5000), ensuring that producing a corresponding validity proof within an hour is achievable. While there is considerable room for optimization, these preliminary estimates are already quite reasonable.

---

Thanks again for your thoughtful questions—feel free to reach out if you have any more! We’re happy to help clarify further.

---

**blacktemplar** (2025-03-15):

Hi [@GCdePaula](/u/gcdepaula) thank you for the interesting research. I am not very familiar with the topic as a whole but I have read your very interesting post + partially read your paper.

Your post inspired me to think about alternative modifications to the original tournament-based PRT approach and I want to bounce my idea here to see if I understand the concepts and if my idea makes any sense.

# 1. Idea description

I want to introduce 2 new things to PRT. First having groups of size `G` in each round of the tournament. At most one claim (the one that won all matches) of a group proceeds to the next round (similar to the paper).

Next I want to tackle the long fixed-round time of 2 weeks + 2h. To reduce this we need to do two things:

1. We don’t wait for all groups to be finished to start new matches for the next round. So the rule would be like this: As soon as one claim has won all matches of a group they proceed to the next round and join there a potentially “unfinished” group (or finish a group). They start immediately matches with all other claims in this (potentially unfinished) group. When the unfinished group in the next round reaches G claims then the last matches just got started and for the next claims coming in a new unfinished group gets created.
2. We introduce a global time budget similar to the idea in Dave. But this time we really consider it as a global time budget b for each claim. At the start of the tournament each claims budget is 1w. The max time a claim can use in round k is 2h plus the global time budget they have left at the beginning of the round. When moving from round k to k+1 we look at the match the claim consumed the most time, lets say this is d, then if d > 2h we subtract d - 2h from the global time budget of the the claim.

# 2. Property comparison with Dave

I think I can prove that with those rules we always get a tournament finish time of at most `K * (1w + 2h) + censoring_time` where `K` is the number of rounds and `censoring_time` is the total time the hero needed to consume from their budget (i.e. the total time they got censored). See the full proof in the next section.

Now the idea is to use a much larger `G` than for `Dave`. For example `G = 50`.

For our comparison we will assume `2^20` sybils (which is similar but a bit more than the `1,000,000` ETH).

## 2.1 Comparing the computational (and transactional) effort for hero

Note that the two systems are similar enough that it is enough to compare the the number of matches the hero must play, since a match is exactly the same for the two systems.

In Dave with `G = 4` and `T_g = 8h` we can look in the table in the paper and see that with `2^20` sybils the hero needs to play `67` rounds, `3` games per round which totals in `201` games.

To compute the number of rounds in our system we can simply compute `ceil(log_50(2^20))` which equals `4`. So our hero has to play `4 * 49 = 196` games (almost the same, I chose the `G = 50` exactly to match the effort in this sense for the hero).

## 2.2 Comparing the total duration

If we look in the table of the paper (or the table in the original post) standard Dave needs `35.25` days to deal with `2^20` sybils assuming no censorship happened. In the continuous variant it is `19.58` days.

Lets compare this to our situation. Our max duration without censorship is `K * (1w + 2h) = 4 * (1w + 2h)` (see previous section why it is `K = 4` rounds). So we get `4w + 2h` which is less than the `35.25` but more than in the continuous variant.

# 3. Proving tournament finish time

This is the crucial step to this approach. We want to prove that the total tournament runtime is bounded by `K * (1w + 2h) + censoring_time` where `K` is the number of rounds and `censoring_time` is the total time the hero needed to consume from their budget (i.e. the total time they got censored).

To do this we want to prove this more general statement:

For any match between claims `c1` and `c2` in round `k` (with `1 <= k <= K`) that starts at time `t`. Let `b1` and `b2` be the global time budgets of `c1` and `c2` at the beginning of round `k`, then the following must hold:

```auto
b1 + b2 <= (k - 1)(1w + 2h) + 2w - t
```

Note that this statement also implies that `t <= (k - 1)(1w + 2h) + 2w` because budgets cannot become negative.

To prove this statement we introduce a new notation. We say a claim consumes `x` amount of budget in a match `m` if its total time spent on the match equals `1h + x`.

First we want to show what follows if the statement would be true. Let `x1` and `x2` the amount of budget consumed in match `m` by claims `c1` and `c2` respectively. Then we get for the finish time `f` of `m`:

```auto
f = t + 2h + x1 + x2 <= (k - 1)(1w + 2h) + 2w - b1 - b2 + 2h + x1 + x2 = k(1w + 2h) + 1w - (b1 - x1) - (b2 - x2)
```

We have written the last expression in this form because `b1 - x1` is a upper bound for the budget left for the claim `c1` in the next round and the same for `c2` (note that it is only an upper bound since there could be other matches that consumed more budget in round `k`).

The inequality for the finish time also tells us why proving all of this helps us with the original statement we wanted to prove. Let us consider `k = K` and note that in the last round only the match finish times of the hero are relevant since if the hero wins all of them the tournament is finished and no need to wait for other matches to finish (since they are irrelevant). Lets say the her consumes `censoring_time` of its global time budget during the whole tournament while all sibyls clearly will consume the full global time budget in the worst case.

In our formula we can say `c1` is the claim of the hero and `b1 - x1 >= 1w - censoring_time` and `b2 - x2 >= 0`. That gives us:

```auto
f <= k(1w + 2h) + 1w - (b1 - x1) - (b2 - x2) <= k(1w + 2h) + 1w - (1w - censoring_time) - 0 = k(1w + 2h) + censoring_time
```

This means all of heroes matches in the last round finish no later than `k(1w + 2h) + censoring_time` and therefore this is an upper bound for the tournament duration.

So the only thing that remains is proving

```auto
b1 + b2 <= (k - 1)(1w + 2h) + 2w - t.
```

We do this by induction on `k`.

For `k = 1` it is trivial since all matches of the first round start at time `t = 0` and all budgets are `1w`, therefore we get: `b1 + b2 = 2w <= 0*(1w + 2h) + 2w - 0`.

Now for the step `k -> k + 1`: We look at the finish time of any match of any of the two claims `c1` or `c2` in round `k`. Lets call this match `m` and its participating claims `c_i` and `c_x` where `i` stands for 1 or 2 and `x` stands for a totally different claim. Lets also denote the time budgets of those two claims at the beginning of round `k` by `b_ik` and `b_xk`. We denote the match start time of `m` by `t_m`. Then we get by the induction hypothesis:

```auto
b_ik + b_xk <= (k - 1) (1w + 2h) + 2w - t_m
```

Now lets denote the budget time claim `c_i` consumes in match `m` by `x_i`. Then we get the following inequality for the finishing time `f_m` of match `m`:

```auto
f_m <= k(1w + 2h) + 1w - (b_ik - x_i)
```

Now we know that `min(b1, b2) <= (b_ik - x_i)` since either `i` stands for 1 or 2 and then the new budget in round `k + 1` is smaller or equal the old budget minus the consumed budget of a game in round `k`.

This means:

```auto
f_m <= k(1w + 2h) + 1w - min(b1,b2)
```

Now we are independent of `i` and `x` and this means any match claim `c1` or `c2` played in round `k` finishes no later than `k(1w + 2h) + 1w - min(b1,b2)` and therefore `t <= k(1w + 2h) + 1w - min(b1,b2)` (remember that a match starts as soon as all matches of the two claims have finished in the previous round).

So we get in total:

```auto
min(b1, b2) <= k(1w + 2h) + 1w - t
max(b1, b2) <= 1w
```

Summing this up gives us `b1 + b2 <= k(1w + 2h) + 2w - t`.

We are finally done :).

# Summary

I have described a simple modification of the PRT approach that seems to have properties that can compete with Dave. I am wondering if I have a mistake somewhere in my reasoning, if my approach has some other wholes I don’t see or if it is a viable alternative. Furthermore, if it is a viable alternative, what are the benefits of Dave vs this approach and vice versa.

---

**GCdePaula** (2025-03-16):

That is very clever—your reasoning is sound ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

Indeed, the current PRT implementation already uses this matchmaking strategy (with G = 2), along with some small modifications to simplify implementation.

Informally, we think about settlement time such that at any moment, at least half the timers are ticking. As a result, every (1w + 2h) interval, half of the total remaining clock time is expended.

A caution on increasing G: the resource function scales linearly with G, while liveness improves only logarithmically (log G). For example, setting G = 50 would require 50 reference units of hardware, which might include 50 GPUs to generate the final validity proof, but would improve liveness only by ~5.6x.

Thanks again for your impressive analysis, it is much appreciated.

---

**blacktemplar** (2025-03-17):

Hi [@GCdePaula](/u/gcdepaula), thanks for your quick response ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12). You are right I have not considered the hardware burden introduced by `G = 50` due to the fact that the hero must be able to play all 49 matches in parallel.

That said I think one way to still make it “fair” and comparable is to increase the time claims have to finish a game. So in Dave and in my analysis above it was 1 hour (ignoring the additional time for censorship resistance that sums up to 1 week in both approaches). So with Dave’s parameters the assumption is that the hero must be able to play 3 complete matches in parallel within 1 hour.

If we say now we don’t want to force the hero to buy more hardware we want to keep up the rough estimate of 3 matches need 1 hour of computation (plus transaction times but lets not consider that for now). Then to play 49 matches the hero would need 49 / 3 = 16 + 1/3 hours to finish the matches without more hardware. So if we replace in our calculation the 1h with 16 + 1/3 or equivalently the 2 hours (summing for both claims in a match) by 32 + 2/3 hours we get:

max duration without censorship is `K * (1w + 32 + 2/3 hours)`. This means with our example that has `K = 4` this would lead to `4 * (1w + 32 + 2/3 hours) = 33.44...` hours which is still lower than Dave’s `35.25h` (although to be fair not by much).

So to summarize if we change my proposal to give the claims 16h20min for every match we would in theory get the same hardware requirements than for the parameters for Dave and the worst case runtime would end up being still a bit lower. The difference is now tiny, but given that the system I proposed seems like a bit simpler than Dave’s (maybe this is just my subjective impression because it feels natural to do it this way for me) I still think it could be a viable alternative. Of course I am very curious how the continuous version will work since the numbers you posted there seem to outperform my proposal by quite a bit.

All that said I think I have a small extension to my approach that could bring down worst case runtimes by yet another week compared to Dave. The idea is that in Dave I assume there must be a period of at least a week in which claims can get posted before the tournament can even start. With my approach we could include this period in the global time budget of 1 week since without censorship the hero should always be able to post their claim at the beginning of the week. So this means that we start matches again immediately as soon as claims come in and don’t wait for other claims and the one week window to pass by. Other claims can still be posted within this one week window but if they get posted to the end of this one week window their global time budget will be low (the global time budget starts with 1w - the time passed to post the initial claim). This still upholds that the hero can successfully win the tournament if they don’t get censored for more than a week.

---

**GCdePaula** (2025-03-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/blacktemplar/48/4640_2.png) blacktemplar:

> That said I think one way to still make it “fair” and comparable is to increase the time claims have to finish a game.

Good idea! Here’s a possible improvement, building on the observation that step actions are both rare and time-consuming (since they would eliminate Sybils): time backloading.

Instead of allocating a fixed censorship budget of 1 week and frontloading 1 hour per match, each claim would start the tournament with a total budget of 1 week plus 1 hour. Then, each time a step action occurs, an additional hour is added (backloaded) to that claim’s timer.

This approach would save you from needing to repeatedly pay the 16 + 1/3 hours upfront for every match.

![](https://ethresear.ch/user_avatar/ethresear.ch/blacktemplar/48/4640_2.png) blacktemplar:

> in Dave I assume there must be a period of at least a week in which claims can get posted before the tournament can even start

In both algorithms, there are techniques to make disputes begin instantly, by penalizing claims that delay entering the tournament. In PRT, this is achieved through the mechanism you described, and in Dave, by proportionally demoting claims based on their delay.

---

**victorshoup** (2025-04-02):

Thanks for your help filling in some details of Dave and your underlying assumptions.  I have one more small question.  I don’t see anywhere a careful description of the structure of a match, but based on what you say about each player making 5 moves for a total of 10 16-ary dissections (or 2^40 state transitions per assertion), I surmise the following move structure:

1. Player 1 makes a 16-ary dissection of its commitment to get nodes at level 1
2. Player 2 makes a 16-ary dissection of its commitment to get nodes at level 1, and then makes a 16-ary dissection of the first level-1 node that matches a corresponding level-1 node of Player 1 to get nodes at level 2
3. Player 1 makes a 16-ary dissection of its commitment to get nodes at level 2, and then makes a 16-ary dissection of the first level-2 node that matches a corresponding level-2 node of Player 2 to get nodes at level 3
4. …
This continues with each player making 2 dissections per move…in round 10 Player 2 makes two such dissection to get nodes at level 10, and then in round 11 Player 1 makes a single dissection to also get nodes at level 10.
So in fact, Player 2 makes 5 moves, each of which is a double dissection, while Player 1 makes 6 moves, 4 of which are double disections and 2 of which are single dissections.

If that is correct, then I surmise that 90K gas is the cost of doing a double dissection move, while the two single dissections moves performed by Player 1

add up to a cost that is not much larger than 90K gas (it must be a bit higher as there are significant fixed costs per transaction).

To be honest, I can’t be 100% sure my interpretation is correct, which is why I’m asking here.

Can you clarify?

Thanks.

---

**GCdePaula** (2025-04-03):

Hey Victor! Thank you very much for your thoughtful question and for engaging so closely with our paper.

Our primary focus in the paper was on theoretical analysis, especially regarding the novel tournament structure. As we move toward implementation, many practical details will naturally become clearer. Indeed, there are multiple valid approaches to these specific implementation choices, as well as numerous potential optimizations.

Regarding the match structure, your understanding is correct, and the design you’ve outlined is certainly viable. Your description of the moves in points 2 and 3 (the double dissections) aligns precisely with our intended design. However, there is greater flexibility in designing the first and last moves.

The first move could be integrated into a previous action. For example, a step action could naturally include the immediate sub-trees, effectively “wrapping around” into the next match. Similarly, when entering the tournament, the initial claim could implicitly include this initial dissection.

Likewise, the final single dissection could be combined with a step action, in which case only Player 1 would be permitted to take step actions. Under this scenario, Player 2’s only path for victory would be via timeout. This arrangement preserves all the essential properties of the algorithm. In such a setup, Player 2 would typically perform five “double dissect” actions, while Player 1 would typically perform 4 “double dissect” actions and occasionally an additional single dissect + step action. Our gas expenditure estimates were based on this loose design.

Ultimately, as shown in our earlier PRT work, multiple implementation options are viable, and we have yet to finalize these details fully.

Feel free to reach out if you have any further questions! ![:blush:](https://ethresear.ch/images/emoji/facebook_messenger/blush.png?v=12)

Cheers!

