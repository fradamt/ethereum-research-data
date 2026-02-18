---
source: ethresearch
topic_id: 21790
title: Toward a General Model for Proposer Selection Mechanism Design
author: cyberhang
date: "2025-02-19"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/toward-a-general-model-for-proposer-selection-mechanism-design/21790
views: 543
likes: 8
posts_count: 10
---

# Toward a General Model for Proposer Selection Mechanism Design

APS, or Attester-Proposer Separation, introduces an in-protocol modification that decouples the execution proposer’s responsibilities from the other tasks performed by validators. Its motivation, along with some execution proposer leader election mechanisms (e.g., Execution Tickets) and their corresponding implications, has been [extensively discussed within the Ethereum community](https://efdn.notion.site/Attester-Proposer-Separation-Tracker-15bd9895554180c2ac75cb40878ecd33).

However, as highlighted in [Julian’s recent article](https://ethresear.ch/t/exploring-sophisticated-execution-proposers-for-ethereum/21386), ecosystem participants have not reached consensus on the most desirable mechanism. This lack of consensus stems primarily from the fact that the “mechanism design problem” itself is not [well-defined](https://en.wikipedia.org/wiki/Well-defined_expression). To meaningfully compare different mechanisms and determine the optimal solution, we have to first formulate the problem mathematically and establish a unified general framework for systematic analysis.

We begin by introducing a basic model for our analysis. While the model remains incomplete due to certain constraints and specifications that require further discussion, one general conclusion holds regardless of the specific constraint set: collusion-proof mechanisms may not exist. In the final section, we provide a brief review of the existing literature.

### Base Model

The mechanism design problem for APS can be formulated as a principal-agent problem. The principal (the protocol) seeks to allocate the proposing right (PR) to a group of agents 1,2,…,n (potential proposers). Since the value of PR is unknown ex-ante (may have some prior knowledge, e.g., follow some prob. distributions; but if fully known, the problem would be trivial), the principal must design a mechanism \mathcal{M} that elicits signals \vec{a} = (a_1, a_2, …a_n) from agents (heterogeneous with valuation v_i) to allocate PR efficiently. The mechanism \mathcal{M} transforms these signals \vec{a} into two key outputs: agent payoffs (winning probabilities) T^\mathcal{M}(\vec{a}) = (t_1,t_2,…, t_n), and agent costs (transfer to the principal) C^\mathcal{M}(\vec{a}) = (c_1,c_2,…, c_n). The principal solves:

\begin{aligned}
\text{Choose} \ \mathcal{M} \ \text{to} \ \text{maximize} \quad & g(T^\mathcal{M}(\vec{a}), C^\mathcal{M}(\vec{a})) \\
\text{subject to} \quad & t_1 + t_2 + ...+t_n = 1,\\
& t_i \cdot v_i - c_i \geq 0, \ \text{for any} \ i=1,2,...n,
\\& a_i \ \text{is a best repsonse of agent} \ i ,
\\& \text{Constraint 4, e.g.,} \ \mathcal{M} \ \text{is Sybil-proof,}
\\& \text{Constraint 5, e.g.,} \ \mathcal{M} \ \text{ensures competition,}
\\& \dots
\\& \text{Constraint j, ...}
\end{aligned}

Here g is a goal function that measures the principal’s payoff by mapping T \times C to a real value. When the principal prioritizes monetary gain, g could be the sum \sum c_i. When focusing on outcome fairness, g could be a fairness measure such as \sqrt{t_1\cdot t_2 \cdots t_n}. The function g can also combine both objectives and may take any general form (depends on the exact desiderata).

The mechanism \mathcal{M} is a function that maps \mathcal{M}: \vec{a} \to T \times C. It can take any form as long as it satisfies all program constraints. Naturally, all [proposed mechanisms](https://www.notion.so/15bd9895554180c2ac75cb40878ecd33?pvs=21) (e.g., ETs, EAs) fit within this general framework. Also, it is easy to identify that some proposed mechanisms are conceptually identical despite having different names —for example, a winner-take-all ET is equivalent to an EA. Conversely, some mechanisms share the same name but are conceptually quite different, such as [ET with capped supply versus elastic supply](https://collective.flashbots.net/t/inelastic-vs-elastic-supply-why-proof-of-stake-could-be-less-centralizing-than-execution-tickets/3816). We only need to compare mechanisms that are conceptually different.

The critical next step is to clearly define our constraints and the goal function g. This raises a fundamental question: what are our expectations for APS, and how should we measure and formalize them? These expectations could stem from design goals (e.g., see [Mechan-stein](https://ethresear.ch/t/mechan-stein-alt-franken-ism/20321)) or engineering considerations (as highlighted by [Neuder, Garimidi, and Roughgarden (2024)](https://ethresear.ch/t/on-block-space-distribution-mechanisms/19764)). **I seek the community’s input and guidance on this matter.**

After finalizing the model setup, the next challenge is solving it. The program is particularly difficult since the decision variable, \mathcal{M}, is a general function—a complexity commonly seen in [traditional principal-agent problems](https://en.wikipedia.org/wiki/Principal%E2%80%93agent_problem). However, we now have a unified framework to initiate our analysis. At the very least, this allows us to theoretically compare common solutions and evaluate their performance. Additionally, we aim to identify certain conditions under which specific mechanisms are optimal. Our findings may take the following form: a mechanism is optimal or robust if and only if it satisfies Property A, or a mechanism will lead to Outcome Y if it meets Condition X. For example, an insight can be drawn, even without a complete constraint set.

### Non-existance of Collusion-proof Mechanisms

**Definition 1.** A mechanism \mathcal{M} is said to ensure competition if under \mathcal{M}, for any n>1, the total cost of agents \sum_{1}^{n} c_i > \underline{c}({\mathcal{M}}), where \underline{c}({\mathcal{M}}) is the minimal cost of the agent to gain PR when n=1.

**Definition 2.** A mechanism \mathcal{M} is said to be collusion-proof if no off-chain agreement (OCA) among agents Pareto improves the (equibrium) outcome, i.e., T^\mathcal{M}(\vec{a})  \times C^\mathcal{M}(\vec{a}) ,  under \mathcal{M}.

The second definition follows [Roughgarden (2023)](https://arxiv.org/abs/2106.01340).

**Theorem.**  There doesn’t exists a collusion-proof mechanism \mathcal{M} that ensures competition.

***Proof***. For any \mathcal{M} that ensures competition, we have \sum_{1}^{n} c_i > \underline{c}({\mathcal{M}}). There exists an OCA that Pareto improves the (equibrium) outcome: Only the most sophasticated agent i particpates, while all others forgo the opportunity. Agent i pays  \underline{c}({\mathcal{M}})  to obtain PR. Agent i gains a realized block net reward R. Agent i then shares t_j \cdot R + \frac{\sum_{1}^{n} c_i -\underline{c}({\mathcal{M}})}{n} with each agent j\neq i. Q.E.D.

To better illustrate, consider a first-price auction. Agents can form a single cartel through an OCA. The agent with the highest valuation v submits a  super small bid in the auction (others bid 0 by OCA), effectively securing PR at almost zero cost. The winning agent then redistributes v among the other agents, ensuring mutual benefit within the cartel. We can also consider a Proportional-all-pay Execution Tickets (a Tullock Contest) provided by [Neuder, Garimidi, and Roughgarden (2024)](https://ethresear.ch/t/on-block-space-distribution-mechanisms/19764). Agents can form a single cartel through an OCA to obtain PR with almost 0 cost. They then proportionally share the realized block reward according to the equilirum outcome under the ET mechanism.

For a more realistic example, I encourage readers to refer to this reply:  [OCA in the long run](https://ethresear.ch/t/toward-a-general-model-for-proposer-selection-mechanism-design/21790/6).

The intuition is straightforward. In such a principal-agent problem, the principal aims to increase costs for agents and extract profits through their competition. However, agents can always minimize these costs by forming a single entity, pooling their resources to achieve the highest possible MEV reward, and redistributing the gains among themselves through OCA to ensure each agent receives a higher payoff than they would under competition.

One might wonder why such an OCA does not occur in existing blockchain consensus. The key difference lies in that the token value of the blockchain relies on its decentralization. If such an OCA were to take place, the exceptionally low costs for miners would become evident to all market participants, signaling weak competition and potential collusion within the network. This, in turn, would undermine confidence in the blockchain’s decentralization, leading to a decline in the token value. Since miners’ earnings are directly tied to the token value, they have no incentive to form an extreme cartel that would reduce costs at the expense of the network’s perceived integrity.

Therefore, while the theorem suggests that agents in this principal-agent problem can benefit from collusion, such behavior can be mitigated in several ways:

1. Validator Oversight: Validators can observe both the outcome and costs incurred by each agent. If the outcome strongly indicates collusion, they can reject the block.
2. Fee Mechanisms: The principal can design a contract (included in a Fee Mechanism) where a fixed proportion ((\alpha < 1)) of the block reward is allocated to the protocol, regardless of the realized value. This ensures that a portion of the principal’s payoff remains independent of agent cooperation.

### Discussions

Current research on this topic typically focuses on the bigger picture [(Stichler, 2024)](https://ethresear.ch/t/agent-based-simulation-of-execution-tickets/21254), but presents analyses and implications within relatively narrow frameworks, with conclusions in each article constrained by the specific assumptions underlying the respective mechanisms. For instance, [Burian, Crapis, and Saleh (2024)](https://arxiv.org/abs/2408.11255) demonstrate that Execution Tickets (ETs) could lead to a proposer monopoly, as candidates with a significant capital cost advantage may dominate the ET market. As [Christoph (2024)](https://collective.flashbots.net/t/inelastic-vs-elastic-supply-why-proof-of-stake-could-be-less-centralizing-than-execution-tickets/3816) points out, this conclusion is primarily driven by the assumption of a fixed ticket supply. Consequently, under the framework proposed by [Neuder, Garimidi, and Roughgarden (2024)](https://ethresear.ch/t/on-block-space-distribution-mechanisms/19764), where the ticket supply is uncapped, this conclusion no longer holds. Such framework isolation results in implications that lack generality and limits meaningful comparisons between different mechanisms.

A more recent study by [pascalst](https://ethresear.ch/u/pascalst), i.e., [Stichler (2024)](https://ethresear.ch/t/agent-based-simulation-of-execution-tickets/21254), simulated comparative results between mechanisms. However, establishing generality remains challenging due to the exponential increase in computational complexity as more variables and mechanisms are introduced. Therefore, a unified theoretical framework is crucial, enabling high-level analysis of different mechanisms and potentially identifying a conceptually optimal one.

This article serves as an initial step toward establishing a theoretical model. Its completion requires further discussion and examination of APS’s objectives, potential constraints, and the corresponding measures needed to accurately model real-world conditions. Additionally, new environments, such as those involving incomplete information, may also need to be considered.

## Replies

**Julian** (2025-02-19):

Thanks for the insightful post!

First, the constraints that I think any APS implementation must satisfy are the following:

1. Remove Execution Rewards from Beacon Proposers.
2. Prevent Multi-Slot MEV.
3. Ensure Competition in Execution Proposer Market.
4. Next Execution Proposer Always Known.

The first constraint captures removing timing games incentives and reward variance from beacon proposers which is the main goal of APS. The second constraint means that pay-offs for a single execution proposer controlling two slots in a row should not exceed two different execution proposer’s pay-offs for both of those slots independently, keeping all else equal. We want to prevent multi-slot MEV because it would lead to a bad user experience. The third constraint/desideratum is the same as what you have. Finally, the fourth constraint is there because providing preconfirmations requires that the next execution proposer is always known.

Another constraint is that Ethereum does not have an unpredictable source of randomness. This means preventing multi-slot MEV using a just-in-time allocation using randomness is impossible.

I am curious about how these constraints/desiderata fit into your model.

---

**trevelyan** (2025-02-19):

Just FYI – the Roughgarden collusion proof is incorrect. There is a paper that shows the underlying problem but links do not seem to be permitted – feel welcome to contact me if you’d like to read it.

The TL;DR version is that if I am a block producer and promise you a hamburger to collude with me, how much you value hamburgers affects your decision to collude. The efficiency with which I can produce hamburgers is also relevant. If I give you a cash discount, your valuation of anything you might purchase with the savings is suddenly a relevant preference that has to be disclosed to the mechanism.

The error in the Roughgarden paper is to assume the fees constitute “truthful preference revelation” in a TFM because in a Vickrey auction with a trusted auctioneer it is the only relevant preference and thus the only preference that needs to be revealed to the mechanism. Essentially, Roughgarden changed the strategy space without realizing it affects the preference maps that both users and producers must disclose (see Hurwicz), the type of mechanism in play (direct vs. indirect) and what kinds of generalizations can be made about the possibility or impossibility of building incentive compatible mechanisms.

The impossibility result are tautological – the complicated proof isn’t needed because the Revelation Principle already does the heavy lifting – you can’t achieve incentive compatibility in direct mechanisms if participants aren’t sharing all relevant preferences truthfully with the mechanism.

---

**aelowsson** (2025-02-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/cyberhang/48/19158_2.png) cyberhang:

> Agents can form a single cartel through an OCA. The agent with the highest valuation v submits a super small bid in the auction (others bid 0 by OCA), effectively securing PR at almost zero cost. The winning agent then redistributes v among the other agents, ensuring mutual benefit within the cartel.

I assume that agents are not monopolizing private tx orderflow, since the text does not discuss this scenario. Then, starting from a [base model of collusion](https://en.wikipedia.org/wiki/Collusion#Base_model_of_(price)_collusion), I am interested in your comments on the following:

1. Monitor – Cartel members will have no way of knowing if a member has violated the agreement when someone places a bid just above v at the last moment of the auction.
2. Control – There is no fixed supply of seats at the bidding table, and entering is profitable when a cartel fixes the price at v.

I also add the following points to consider:

1. If the auction is APS burn, the beacon proposer will at least ensure that the price corresponds to available priority fees, or otherwise self-build. We can assume that v must correspond to easily attainable MEV.
2. There is a wide variety of burn incentives under APS burn. Particularly, staking service providers will wish to ensure that competitors do not attain more rewards than them, so that they can win the overarching staking metagame. This can be achieved by integrating with builders to bid away competing beacon proposers’ profit margins at the attester observation deadline.

---

**cyberhang** (2025-02-20):

Thanks for the valuable guidance!

I think the first constraint is assumed to be always hold, as the model restricts MEV exclusively to the selected execution proposer. Both the second and final constraints need further careful examination. We might incorporate them into a [repeated-game](https://en.wikipedia.org/wiki/Repeated_game) framework, and their corresponding mathematical formulation also presents an intriguing challenge.

---

**cyberhang** (2025-02-20):

Thank you for your reply—very good point! The **“monitoring” and “control”** issue may not be a concern, as justified in the **“Regarding the Monitor and Control”** section.

First, here are some underlying assumptions in the discussion of OCA. OCA is essentially framed within a [repeated-game](https://en.wikipedia.org/wiki/Repeated_game) context, meaning that the game unfolds over multiple periods—closely mirroring reality. Additionally, it is assumed that agents know each other’s valuations, which reflects their sophistication or ability to extract value from MEV. In practice, participants might be aware of which actors are best positioned to exploit MEV.

In a one-shot scenario, OCA would be unsustainable because a member could simply breach the agreement by placing a marginally higher bid without worrying about future repercussions or damaging their reputation within the cartel. However, in a repeated game, any breach would eventually be detected (since the outcome changes). **In a complete information scenario**, the offending member would be caught and thus suffer reputational damage, potentially face expulsion from the game, or be forced to compete against the cartel—outcomes far less desirable than adhering to the agreement in the long run.

### Regarding the Monitor and Control:

If I’m not mistaken, your point is that the cartel cannot verify whether the individual responsible for a different outcome is a member of the cartel or an outsider. Even if they know the person is an insider, they cannot determine their exact identity. Furthermore, since the market is open to everyone, outsiders can easily join the bidding process and thus can place a marginally higher bid.

That’s a fair point. **However, assuming that agents’ sophistication (i.e., their valuation or ability) in the market is common knowledge, the OCA can still work effectively even if the cartel cannot directly monitor which individual is responsible for a deviation from the agreed outcome.**

Let’s consider a simple example below: Consider only three agents in the market at the very beginning—Alice, Bob, and Carol—with sophistication levels satisfying 30 > 20 > 10. It means that if Alice secures the proposing right, she can extract a monetary payoff of  30 dollars. We assume the game is played over infinitely many periods, with each period operating as a first-price auction.

In a single-period non-cooperative equilibrium, Alice will win by bidding 20+\epsilon, \epsilon \to 0.  In this case, Alice’s payoff is 30-20=10. If the game is repeated over infinitely many periods and the agents remain non-cooperative throughout, then Alice’s total payoff will be 10 + 10 r + 10r^2+ \dots  = \frac{10}{1-r}, where r is the discount factor. Bob and Carol gain 0 all the time.

**Alice now announces an OCA**: In each period, she submits a bid of a small value—say, 1 (it could be even lower, approaching 0, but for simplicity, we assume 1)—while Bob and Carol bid 0. Then, at the end of each period (after Alice has extracted MEV), she pays Bob and Carol 1 dollar each (also could be even lower). If there is any deviation from the agreed outcome—for instance, if in any period Alice fails to win by bidding 1—the parties revert to the non-cooperative regime.

**We assume that agents cannot directly observe the number of bids, meaning they cannot determine whether an outsider has joined. Additionally, if Alice fails to win in a given period, she cannot verify whether the agent responsible for the alternative outcome is Bob, Carol, or an outsider.**

Under this OCA, if nobody breaches the agreement, Alice’s payoff is any single period is 30-1-5-4 =20. Alice’s total payoff will be 20 + 20 r + 20r^2+ \dots  = \frac{20}{1-r}. Also, since Bob gains 5 dollars in each period, Bob’s total payoff will be \frac{1}{1-r}, and similarly Carol’s total payoff will be \frac{1}{1-r}. Note that all parties receive a higher payoff than they would under the non-cooperative regime.

Will Bob or Carol breach the agreement at any point? They will not, because a breach would reduce their future payoff to 0 from that moment onward, whereas under the agreement they receive \frac{1}{1-r} and \frac{1}{1-r}, respectively. **This demonstrates that the OCA can operate effectively even without Monitor**.

Now we dive into the **Control** issue. Based on the above argument, Alice can infer that if she fails to win the bid at any point, it must have been placed by an outsider. **How does the Cartel address the outsider problem?**

**Alice can simply announce a new OCA**: For any other agent in the market, as long as that agent, denoted by Dan, with sophistication d, can choose to join the cartel (initially composed of Alice, Bob, and Carol) under the following rule: If Dan can prove that his sophistication exceeds Alice’s, i.e., d>30, then Dan takes the lead. This means that in subsequent rounds, Dan bids 1 while all others bid 0. At the end of each period, Dan distributes payments to Alice, Bob, and Carol—for instance, 1, 1, and 1 dollars, respectively (without loss of generality). If Dan cannot prove that his sophistication exceeds Alice’s, then Alice is still the leader. But Alice has to pay 1 dollar to Dan at the end of each period. Any breach of the agreement results in a reversion to the non-cooperative regime.

**Why does the cartel have an incentive to establish this new OCA?** It is because the cartel recognizes that, in the long run, they will continually lose if an outsider possesses a higher valuation (sophistication).

**Will Dan join the cartel? He will, even if he remains in the dark (i.e., without revealing his sophistication or valuation)**, because refusing to join would force him to compete against the cartel.

Hence, if Dan’s sophistication exceeds Alice’s—say, 40—he is better off joining the cartel in the long run. This is because, over time, the cartel can gradually raise the bidding price until it approaches 30, meaning Dan would have to bid 30 to win. However, by joining the cartel, he only needs to bid 1 to secure the win and pay 3 dollars (or even less, without loss of generality) to the other cartel members. If Dan’s sophistication is lower than Alice’s—say, 20—he is also better off joining the cartel in the long run. This is because, eventually, he would lose the competition, as he cannot afford to bid more than 20, while the cartel can.

**Note that this type of adaptive OCA forms a recursive process. This means that each time the cartel admits a new member, a similar announcement can be made. In the long run, the cartel remains intact, with the most sophisticated agent consistently taking the lead.**

Of course, this type of OCA can be applied to other mechanisms as well. For example, similar OCAs can be easily constructed within a Tullock contest. Additionally, forming an entity and cooperating can sometimes enhance their collective sophistication beyond that of any individual (a **1+1>2** effect). Fundamentally, in a long-run setting, lower-sophistication agents naturally delegate their power to the most sophisticated one—just as the saying goes: *Leave professional tasks to professionals.*

I’ll stop here for now and will revisit your third and fourth points later.

---

**cyberhang** (2025-02-20):

Thanks for your reply! I’m glad to read the paper you referred to. I also encourage you to take a look at my concrete example regarding the OCA issue.

![](https://ethresear.ch/user_avatar/ethresear.ch/cyberhang/48/19158_2.png) cyberhang:

> Let’s consider a simple example below: Consider only three agents in the market at the very beginning—Alice, Bob, and Carol—with sophistication levels satisfying 30 > 20 > 1030>20>1030 > 20 > 10. It means that if Alice secures the proposing right, she can extract a monetary payoff of 303030 dollars. We assume the game is played over infinitely many periods, with each period operating as a first-price auction.



    ![](https://ethresear.ch/user_avatar/ethresear.ch/cyberhang/48/19158_2.png)
    [Toward a General Model for Proposer Selection Mechanism Design](https://ethresear.ch/t/toward-a-general-model-for-proposer-selection-mechanism-design/21790/8) [Economics](/c/economics/16)



> Thank you for your reply—very good point! The “monitoring” and “control” issue may not be a concern, as justified in the “Regarding the Monitor and Control” section.
> First, here are some underlying assumptions in the discussion of OCA. OCA is essentially framed within a repeated-game context, meaning that the game unfolds over multiple periods—closely mirroring reality. Additionally, it is assumed that agents know each other’s valuations, which reflects their sophistication or ability to extrac…

---

**cyberhang** (2025-02-20):

Thank you for your reply—very good point! The **“monitoring” and “control”** issue may not be a concern, as justified in the **“Regarding the Monitor and Control”** section.

First, here are some underlying assumptions in the discussion of OCA. OCA is essentially framed within a [repeated-game](https://en.wikipedia.org/wiki/Repeated_game) context, meaning that the game unfolds over multiple periods—closely mirroring reality. Additionally, it is assumed that agents know each other’s valuations, which reflects their sophistication or ability to extract value from MEV. In practice, participants might be aware of which actors are best positioned to exploit MEV.

In a one-shot scenario, OCA would be unsustainable because a member could simply breach the agreement by placing a marginally higher bid without worrying about future repercussions or damaging their reputation within the cartel. However, in a repeated game, any breach would eventually be detected (since the outcome changes). **In a complete information scenario**, the offending member would be caught and thus suffer reputational damage, potentially face expulsion from the game, or be forced to compete against the cartel—outcomes far less desirable than adhering to the agreement in the long run.

### Regarding the Monitor and Control:

If I’m not mistaken, your point is that the cartel cannot verify whether the individual responsible for a different outcome is a member of the cartel or an outsider. Even if they know the person is an insider, they cannot determine their exact identity. Furthermore, since the market is open to everyone, outsiders can easily join the bidding process and thus can place a marginally higher bid.

That’s a fair point. **However, assuming that agents’ sophistication (i.e., their valuation or ability) in the market is common knowledge, the OCA can still work effectively even if the cartel cannot directly monitor which individual is responsible for a deviation from the agreed outcome.**

Let’s consider a simple example below: Consider only three agents in the market at the very beginning—Alice, Bob, and Carol—with sophistication levels satisfying 30 > 20 > 10. It means that if Alice secures the proposing right, she can extract a monetary payoff of  30 dollars. We assume the game is played over infinitely many periods, with each period operating as a first-price auction.

In a single-period non-cooperative equilibrium, Alice will win by bidding 20+\epsilon, \epsilon \to 0.  In this case, Alice’s payoff is 30-20=10. If the game is repeated over infinitely many periods and the agents remain non-cooperative throughout, then Alice’s total payoff will be 10 + 10 r + 10r^2+ \dots  = \frac{10}{1-r}, where r is the discount factor. Bob and Carol gain 0 all the time.

**Alice now announces an OCA**: In each period, she submits a bid of a small value—say, 1 (it could be even lower, approaching 0, but for simplicity, we assume 1)—while Bob and Carol bid 0. Then, at the end of each period (after Alice has extracted MEV), she pays Bob and Carol 1 dollar each (also could be even lower). If there is any deviation from the agreed outcome—for instance, if in any period Alice fails to win by bidding 1—the parties revert to the non-cooperative regime.

**We assume that agents cannot directly observe the number of bids, meaning they cannot determine whether an outsider has joined. Additionally, if Alice fails to win in a given period, she cannot verify whether the agent responsible for the alternative outcome is Bob, Carol, or an outsider.**

Under this OCA, if nobody breaches the agreement, Alice’s payoff is any single period is 30-1-5-4 =20. Alice’s total payoff will be 20 + 20 r + 20r^2+ \dots  = \frac{20}{1-r}. Also, since Bob gains 5 dollars in each period, Bob’s total payoff will be \frac{1}{1-r}, and similarly Carol’s total payoff will be \frac{1}{1-r}. Note that all parties receive a higher payoff than they would under the non-cooperative regime.

Will Bob or Carol breach the agreement at any point? They will not, because a breach would reduce their future payoff to 0 from that moment onward, whereas under the agreement they receive \frac{1}{1-r} and \frac{1}{1-r}, respectively. **This demonstrates that the OCA can operate effectively even without Monitor**.

Now we dive into the **Control** issue. Based on the above argument, Alice can infer that if she fails to win the bid at any point, it must have been placed by an outsider. **How does the Cartel address the outsider problem?**

**Alice can simply announce a new OCA**: For any other agent in the market, as long as that agent, denoted by Dan, with sophistication d, can choose to join the cartel (initially composed of Alice, Bob, and Carol) under the following rule: If Dan can prove that his sophistication exceeds Alice’s, i.e., d>30, then Dan takes the lead. This means that in subsequent rounds, Dan bids 1 while all others bid 0. At the end of each period, Dan distributes payments to Alice, Bob, and Carol—for instance, 1, 1, and 1 dollars, respectively (without loss of generality). If Dan cannot prove that his sophistication exceeds Alice’s, then Alice is still the leader. But Alice has to pay 1 dollar to Dan at the end of each period. Any breach of the agreement results in a reversion to the non-cooperative regime.

**Why does the cartel have an incentive to establish this new OCA?** It is because the cartel recognizes that, in the long run, they will continually lose if an outsider possesses a higher valuation (sophistication).

**Will Dan join the cartel? He will, even if he remains in the dark (i.e., without revealing his sophistication or valuation)**, because refusing to join would force him to compete against the cartel.

Hence, if Dan’s sophistication exceeds Alice’s—say, 40—he is better off joining the cartel in the long run. This is because, over time, the cartel can gradually raise the bidding price until it approaches 30, meaning Dan would have to bid 30 to win. However, by joining the cartel, he only needs to bid 1 to secure the win and pay 3 dollars (or even less, without loss of generality) to the other cartel members. If Dan’s sophistication is lower than Alice’s—say, 20—he is also better off joining the cartel in the long run. This is because, eventually, he would lose the competition, as he cannot afford to bid more than 20, while the cartel can.

**Note that this type of adaptive OCA forms a recursive process. This means that each time the cartel admits a new member, a similar announcement can be made. In the long run, the cartel remains intact, with the most sophisticated agent consistently taking the lead.**

Of course, this type of OCA can be applied to other mechanisms as well. For example, similar OCAs can be easily constructed within a Tullock contest. Additionally, forming an entity and cooperating can sometimes enhance their collective sophistication beyond that of any individual (a **1+1>2** effect). Fundamentally, in a long-run setting, lower-sophistication agents naturally delegate their power to the most sophisticated one—just as the saying goes: *Leave professional tasks to professionals.*

I’ll stop here for now and will revisit your third and fourth points later.

---

**aelowsson** (2025-02-20):

Thanks for taking the time to answer!

![](https://ethresear.ch/user_avatar/ethresear.ch/cyberhang/48/19158_2.png) cyberhang:

> …if Alice fails to win in a given period, she cannot verify whether the agent responsible for the alternative outcome is Bob, Carol, or an outsider…
>
>
> …Will Bob or Carol breach the agreement at any point? They will not, because a breach would reduce their future payoff to 0 from that moment onward…
>
>
> …Based on the above argument, Alice can infer that if she fails to win the bid at any point, it must have been placed by an outsider.

At the moment Bob realizes that Alice will always blame winning bids on an outsider, he begins rubbing his hands. Now the only remaining task is to invent a new agent “Dan” to extract more value.

![](https://ethresear.ch/user_avatar/ethresear.ch/cyberhang/48/19158_2.png) cyberhang:

> How does the Cartel address the outsider problem? Alice can simply announce a new OCA: … any other agent … denoted by Dan, with sophistication d, can choose to join the cartel … under the following rule: … If Dan cannot prove that his sophistication exceeds Alice’s … Alice has to pay 1 dollar to Dan at the end of each period.

Bob launches “Dan”, wins the auction, and is then invited to join the cartel for a steady stream of additional income. In fact, since the cartel lacks the capacity to both *monitor* members and *control* the entry of new agents, it does not really matter who “Dan” is. He could be an outsider or an insider. Soon enough, new agents “Emma”, “Frank”, and “Gabriella” will show up. Nobody knows where they came from or who they are, but they demand entry to the cartel. After a while, the cartel is saturated, such that Alice is better off by simply bidding 20+\epsilon and taking home the 10-\epsilon profit.

---

**cyberhang** (2025-02-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) Anders Elowsson:

> Bob launches “Dan”, wins the auction, and is then invited to join the cartel for a steady stream of additional income. In fact, since the cartel lacks the capacity to both monitor members and control the entry of new agents, it does not really matter who “Dan” is. He could be an outsider or an insider. Soon enough, new agents “Emma”, “Frank”, and “Gabriella” will show up. Nobody knows where they came from or who they are, but they demand entry to the cartel. After a while, the cartel is saturated, such that Alice is better off by simply bidding 20+\epsilon20+ϵ20+\epsilon and taking home the 10-\epsilon10−ϵ10-\epsilon profit.

Thanks for your follow-up. That’s a really good point.

To justify this, another assumption can be made: the players have some prior knowledge of the market. Specifically, the upper bound N(t) on the total number of players in the market is common knowledge. If N(t) cannot grow rapidly over time—meaning its growth rate is far lower than the block production rate—then the logic remains valid. (Certain “KYC” technologies may be used to justify this, to mitigate Bob’s Sybil attacks.)

Under this assumption, Alice can better counter the potential “fake Dan” issue by slightly tweaking the OCA—specifically, by ensuring that the total profit shared among members (except for the leader) decreases but still be positive whenever a new member joins. For example, under the initial OCA, Bob and Carol each receive 1 dollar per period. However, after Dan joins, all agents’ share except the leader drops to 1/3. If Emma joins, then all agents’ share except the leader drops to 1/12… Also, at time t if the total # of members in the cartel exceeds N(t), they revert to the non-cooperative regime. Everything other remains unchanged.

In this case, Bob has no incentive to invent “Dan” since he cannot prove that the invented Dan possesses a higher level of sophistication than Alice. Consequently, Bob can win MEV for at most (N−3)/2 periods by inventing new members (assuming Carol follows the same strategy as Bob). Beyond that, Bob’s gains per period become far less than 1. However, if Bob chooses not to invent Dan, he can secure a consistent gain of $1 per period.

