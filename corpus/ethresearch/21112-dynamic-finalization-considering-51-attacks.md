---
source: ethresearch
topic_id: 21112
title: Dynamic Finalization Considering 51% Attacks
author: banr1
date: "2024-11-29"
category: Proof-of-Stake
tags: [security]
url: https://ethresear.ch/t/dynamic-finalization-considering-51-attacks/21112
views: 621
likes: 7
posts_count: 3
---

# Dynamic Finalization Considering 51% Attacks

from [Titania Research](https://x.com/titaniaresearch)

*Thank you [Ambition](https://x.com/ChenXuan_C), [terence](https://x.com/terencechain), [Artem](https://x.com/artofkot), Titania Research Protocol Team for discussion and feedback*

---

## TL;DR

This document classifies attack methods against PoS Ethereum and proposes countermeasures, particularly against the notably dangerous 51% attack. The main points are as follows:

1. Classification of Attack Methods: Two indicators, attack stealthability and attack sustainability, are introduced to analyze known attack methods.
2. Risks of a 51% Attack: It highlights the particular danger posed by attacks where the attacker controls more than 51% of the staking ratio and explains why this is the case.
3. Proposals for New Defenses: Two new mechanisms are suggested to counter the high likelihood of a 51% attack: Close Vote Detection, which detects the potential for such an attack, and Emergent Dynamic Finalization, which delays finalization when the risk is elevated.
4. Concerns and Future Challenges: It addresses potential issues with the proposed mechanisms and discusses future research directions.

The aim of this proposal is to enhance the security of PoS Ethereum, specifically by strengthening defenses against the perilous 51% attack.

## 1. Classification of Existing Attack Methods

Several attack methods against PoS Ethereum are known, with potential outcomes that attackers might realistically target, including reorg, double finality, and finality delay. A crucial factor in this analysis is the staking ratio required for an attack, indicating the minimum stake necessary, which serves as a barrier to entry. However, nearly as critical is attack sustainability, which measures how continuously an attacker can maintain the attack. If an attack is sustainable, it could cause significant damage. Additionally, attack stealthability is also important, as it indicates how covertly an attacker can execute an attack. If a protocol cannot detect an attack, it becomes difficult to determine whether defensive measures are necessary. Higher values for both metrics indicate a more negative outlook from the protocol’s perspective. The representative attack methods analyzed include:

1. Finality delay 33% attack
2. Double finality 34% attack
3. Short-reorg & censoring 51% attack (control over future)
4. Short-reorg & censoring 66% attack (control over past and future)

### A: Finality delay 33% attack

The finality delay is an attack that can be executed with a staking ratio of 33%. The attacker prevents finalization by failing to provide 33% of attestations. A defensive measure during this attack is the inactivity leak mechanism. This mechanism identifies validators who either fail to attest or attest against the majority, reducing the staked ETH of such inactive validators. During a 33% attack, the inactivity leak activates, causing the attacker’s ETH to decrease and fall below the amount needed to sustain the finality delay. Consequently, the attack’s sustainability is relatively low and temporary, making it easier to detect due to the inactivity leak.

### B: Double finality 34% attack

Double finality refers to an attack wherein the attacker submits attestations to finalize two branches simultaneously. To achieve double finality, the attacker requires a staking ratio of 34%. The attacker engages in double voting for the 34% of attestations, working to finalize both forks. Defensive measures during this attack include the slashing mechanism. Since double voting is prohibited, the attacker would lose their staked ETH, making the attack easily detectable (low undetectability). Furthermore, the substantial slashing penalty means that attacking will likely only happen once; if the attacker had the budget to attack multiple times, they would likely choose a 66% attack instead. Thus, attack sustainability for this method is also very low.

### C: Short-reorg & censoring 51% attack (control over future)

When an attacker possesses a staking ratio of 51%, they can manipulate the fork choice algorithm. Attacks A and B were directed at the Casper FFG (finality gadget), whereas this attack targets the LMD GHOST (fork choice algorithm). In this scenario, the attacker can freely create the heaviest branch in LMD GHOST, causing honest validators to follow the attacker’s branch, resulting in finalization. This enables the attacker to censor specific transactions and perform short-term reorganization (reorg) to maximize their miner extractable value (MEV) without incurring slashing penalties.

In attacks A and B, mechanisms existed to reduce the attacker’s potential upon occurrence. In attack A, the inactivity leak decreases the attacker’s staking ratio below the 33% threshold, rendering the attack impossible. In attack B, one-third of their staking ratio is slashed during that epoch, making repeated attacks effectively unfeasible.

However, there are currently no algorithmic defensive measures against attack C. Even if there is a slot with a 51% voting ratio, there is no way to distinguish whether that attestation is malicious or a legitimate disagreement among honest validators. This means that attack undetectability is significantly high. Once an attack succeeds, the attacker can persistently continue the attack until a hard fork decision is made through the social layer, resulting in very high attack sustainability.

### D: Short-reorg & censoring 66% attack (control over past and future)

In the short-reorg & censoring 66% attack, the attacker can freely manipulate finalization, rewriting past chains and finalizing new branches. The characteristics of attack D are similar to attack C, with both exhibiting high undetectability and high sustainability.

A critical point to highlight is that after executing a 51% attack, the attacker can utilize the profits to aim for a 66% attack. The potential gains from a 51% attack are significantly higher compared to the 33% and 34% attacks, and because they incur no penalties such as inactivity leak or slashing, a successful attempt could exponentially increase their dominance.

### Summary of attack methods

The following table summarizes the characteristics of the representative attack methods analyzed:

| Attack Method | Staking Ratio | Attack Stealthability | Attack Sustainability |
| --- | --- | --- | --- |
| A. Finality delay attack | 33% | Low | Low |
| B. Double finality attack | 34% | Low | Low |
| C. Short-reorg & censoring attack (control over future) | 51% | High | High |
| D. Short-reorg & censoring attack (control over past and future) | 66% | High | High |

From this table, an interesting trend can be observed: attacks at the 33% and 34% levels (A and B) are easy to detect and exhibit low sustainability, while attacks of 51% and higher (C and D) are difficult to detect and show high sustainability, illustrating a clear dichotomy.

## 2. The Potential Impact of a 51% Attack

I would like to emphasize the importance of considering worst-case scenarios regarding the security of PoS Ethereum. Simply put, there is a real possibility that Ethereum could face a situation described as ‘game over.’ If such a scenario were to occur, all past activities and data within countless ecosystems would be rendered null and void.

Referring to the earlier table, attacks A and B have low levels of both attack undetectability and attack sustainability. From the perspective of an attacker, there is a high likelihood that their actions will be exposed, and these attacks tend to be short-lived.

In contrast, attacks C and D exhibit high levels of both attack stealthiness and sustainability. For attackers, these actions are less likely to be detected, allowing them to sustain the attack over a longer period and potentially reap immense profits. When considering which of the two attacks, C or D, to focus on, we must first pay attention to the staking ratio as a barrier to attack. While both attacks could cause significant damage, attack C, which requires a smaller absolute amount to execute, is more realistically targeted (especially considering its potential to lead to attack D). In light of these considerations, this discussion will explore defensive measures against short-reorganization and censoring 51% attacks.

The key issue with short-reorganization and censoring 51% attacks, as mentioned above, is their high levels of attack undetectability and sustainability, which imply that the potential damage could be extensive.

Let’s delve deeper into attack sustainability. The reason these attacks are sustainable is that the only defensive measure available is a hard fork through social consensus, which takes considerable time (as demonstrated by the DAO incident, which took a month from the discovery of the hack to the hard fork). During this interval, blocks and epochs finalized by the attacker will accumulate on the legitimate chain. Honest validators risk being penalized for attesting to blocks on an illegitimate chain that has become the minority despite being the canonical one. The crux of the matter lies in the fact that the number of epochs required for finalization is fixed; hence, even in emergencies, the finalization occurs over the same two epochs (approximately 13 minutes) as it does under normal circumstances.

## 3. Proposals for Detecting and Defending Against 51% Attacks

In the event of a 51% attack, we anticipate that attestations will exhibit a tight margin, such as 50.5% vs. 49.5%, and such close contests are relatively rare during normal operations. We introduce a metric to indicate the likelihood of the current epoch being attacked based on the number of slots where the head votes are ‘close.’ Furthermore, as this metric increases, the number of epochs necessary for finalization will rise exponentially. This mechanism allows for the algorithmic postponement of finalization during emergencies, enabling the community to respond to attackers through social means without requiring a hard fork. Because normal finalization periods will remain unchanged, this implementation can be seamlessly integrated without compromising user experience. We propose the close vote detection mechanism for the former and emergent dynamic finalization for the latter as defenses against 51% attacks.

### Close Vote Detection

When a 51% attack occurs, attackers will deliberately choose a head that appears canonical by being the heaviest. Honest validators can still propose blocks, but attackers can easily manipulate the canonical head through short-term reorganizations whenever they find the proposed blocks undesirable. The closer the attacker’s staking ratio is to 50%, the closer the amount of attestations will be to 50%. Such attestations that are very near to 50% of the head will be referred to as ‘close votes.’ Currently, the determination of whether to finalize an epoch is made at the last slot of that epoch, where we will add the counting of close votes.

### Emergent Dynamic Finalization

If the occurrence of close votes exceeds a certain threshold, the system will recognize a state of emergency and significantly increase the number of epochs required for finalization. As a result, the attacker will need to maintain a substantial majority of votes over a longer period to achieve finalization. During this time, the community will have the opportunity to implement countermeasures. Specifically, if the number of slots classified as close votes in the current epoch exceeds a certain threshold, the required number of epochs for finalization will be raised dramatically from the standard two. We refer to this as emergency mode. While there is plenty of room for debate on what this value should be, aiming for a significant improvement over the DAO incident’s month-long delay might suggest trying a value like 2^{15}. This would require the attacker to continue their assault for about nine days (32,768 * 12 seconds ≈ 4,551,168 seconds ≈ 9 days), providing the community ample time to implement countermeasures quickly. This defensive mechanism ensures that normal network operations are unaffected and activates only during emergencies, thereby allowing for smooth implementation without degrading user experience. Moreover, since it functions algorithmically, it can be executed immediately without waiting for human judgment, allowing for rapid responses.

### Formalization

Let’s define the following symbols, where W, E, F are parameters:

- i: Slot index of the current epoch, ranging from 1 to 32
- C_i: Indicates whether the voting at slot index i is close (1) or not (0)
- V_i: The percentage of attestations at slot index i, expressed in %
- F: The number of epochs required for finalization

In its simplest initial form, we propose the following:

C_i =  \begin{cases}
1 \ ,& \text{if} \ |V_i-0.5| < W \\
0 \ ,& \text{otherwise}
\end{cases}

F = \begin{cases}
D \ ,& \text{if} \ \sum_{1\le i \le32} C_i \ge E
\\
2 \ ,& \text{otherwise}
\end{cases}

Here are the parameters defined:

- W: The percentage point deviation from 50% that qualifies as a close vote
- E: The threshold number of close vote slots to trigger the emergency mode
- D: The number of epochs required for finalization when in emergency mode

The formulas provided define two indicators indicating the possibility of a 51% attack. First, C_i indicates whether a specific slot is considered a close vote, yielding 1 when |V_i - 0.5| falls within the threshold W. Second, F indicates the number of epochs required for finalization. Hence, if the number of close vote slots reaches the threshold E, the required number of epochs increases to D, thereby planning for sustained attacks and mitigating their potential impacts.

Let’s consider specific values:

W = 1\% \\
E = 4 \\
D = 2^{15}

Thus, we have:

C_i =  \begin{cases}
1 \ ,& \text{if} \ |V_i-0.5| < 0.01 \\
0 \ ,& \text{otherwise}
\end{cases}

F = \begin{cases}
2^{15} \ , & \text{if} \ \sum_{1\le i \le32} C_i \ge 4
\\
2 \ ,& \text{otherwise}
\end{cases}

With these settings, if the attestation percentage V_i for any slot is within ±1% of 50%, that slot will be counted as a close vote. If, for instance, 4 out of the 32 slots are close votes, the total of C_i will be 4, requiring F to be set to 2^{15}. Consequently, the attacker will not be able to finalize the chain for approximately nine days, allowing the community enough time to implement a quick hard fork to restore the legitimate Ethereum blockchain.

### Reducing the estimated maximum damage

The goal of this proposal is to reduce the estimated maximum damage during a 51% attack. It aims to mitigate the likelihood of a ‘game over’ scenario. While it’s challenging to discuss specific quantitative changes, it is feasible to set the parameter D to ensure that the duration does not extend to a month like in the DAO incident. It is essential to consider that the anticipated response time from the social layer should also be factored into this aspect.

Moreover, various services that interact with Ethereum, such as other chains and centralized exchanges, can operate based on this D. By introducing algorithmic mechanisms, the surrounding ecosystems will also be able to respond algorithmically.

## 4. Concerns and Future Work

### Concerns about new finality delay mechanisms

There is a concern that this proposal may inadvertently create a new finality delay mechanism. For example, it is possible to randomly control 51% dominance over L occurrences among 32 slots, which can be easily calculated using a binomial distribution. While the economic incentive to delay finality is generally low, we cannot rule out potential incentives that may not have been considered. If such incentives arise, they could potentially be addressed by introducing a reputation system. Since attestations involve signatures, attempts to impersonate other validators would require significant time to execute.

### Scrutinizing the procedure for implementing a hard fork via social layer

To determine optimal parameters, we need to carefully examine the specific procedures required to execute a hard fork through the social layer.

### Determining parameters W, E, D and formula F through empirical evidence

It is necessary to empirically determine suitable values for parameters W (defining the range for close votes), E (defining the threshold for emergency mode activation), and D (defining how much to delay finalization). Additionally, D is a component of the formula F, but we could also consider a more dynamic design where the increase in the number of close votes \sum_i C_i would result in a greater value for F.

F = \begin{cases}
2^{\sum_i C_i - E+\text{const}} \ ,& \text{if} \ \sum_i C_i \ge E
\\
2 \ ,& \text{otherwise}
\end{cases}

### Determining the specifications of attestation

We need to determine the specifications for attestations.

- How to handle justifications during emergency mode
- The behavior of inactivity leaks during emergency mode
- How to specifically update the data types submitted through attestations.

## 5. Conclusion

In this proposal, we focused on the particularly dangerous 51% attack as one of the attack methods against PoS Ethereum, discussing its risks and implications while proposing new defense strategies. Specifically, we aimed to enhance resistance to 51% attacks by introducing mechanisms like Close Vote Detection and Emergent Dynamic Finalization.

Future research should further explore the effectiveness of the proposed defense strategies and their applicability to other attack methods. There is also a need to continue investigating parameter optimization and specific implementation methods.

Additionally, analyzing attack methods against different consensus algorithms and formulating defense strategies based on social incentives are valuable directions for further discussion. I look forward to engaging with the Ethereum community about the value of these ideas and addressing any concerns.

## Reference

- Ethereum proof-of-stake attack and defense | ethereum.org
- History and Forks of Ethereum | ethereum.org
- Understanding The DAO Attack
- Hard Fork Completed | Ethereum Foundation Blog

## Replies

**AmbitionCX** (2024-11-30):

1. This is a good strategy for dealing with 51% attacks - keeping the damage to a limited range. While, the biggest concern with this proposal is how to determine that a 51% attack has occurred, and whether this proposal will give attackers a very easy method to finality delay.
2. The core idea of Dynamic Finalization is a trade-off between gain and loss, by lossing the finality of the whole chain, to gain the consistance of user assests. Thus, a small probability of loss should correspond to a small range of delays, rather than a 9-day delay once there is a possibility of a 51% attack. Therefore, I recommend using a dynamic delay strategy. For example, D = 2^(∑C)
3. Finally there is a philosophical question, there’s a certain amount of  fault can be tolerated for any consensus algorithm. And of course, Ethereum is vulnerable to 51% attacks, but it is also vulnerable to 66%, 99% attacks, when a 99% attack occurs, and you try to delay the finality, who is the attacker?

---

**banr1** (2024-12-01):

Thank you very much, Amibition, for your extremely valuable feedback.

1. You’re right, this might introduce a new method for finality delay. What I’m still not fully clear on is the economic incentive for carrying out a finality delay. If this incentive is low, I believe it’s crucial to limit the potential damage in the worst-case scenario.
2. I agree with you that a dynamic delay strategy would be better, for the same reasons. I presented that formulation in my initial proposal primarily for the sake of simplicity. I believe the optimal parameters should be determined by analyzing past attestations.
3. I completely agree. Ultimately, there’s always a threshold somewhere, and when that threshold is exceeded, the worst-case scenario occurs. What I want to emphasize is the critical importance of continuously developing defensive measures while assuming the worst-case scenario. Even strategies that seemed optimal at one point may need to be reconsidered depending on how the world evolves (revolutionary ideas in cryptography might be discovered, for instance). As mentioned in the article, the reason for this is that if it happens even once, it’s “game over.” I argue that one of the current “worst-case scenarios with the highest probability of occurrence” is a 51% attack, and I’ve proposed countermeasures against it. I’d like to discuss with the community whether these should be implemented. I believe it’s extremely dangerous that with the current security measures, an attack at the level of a national budget could easily lead to “game over.”

