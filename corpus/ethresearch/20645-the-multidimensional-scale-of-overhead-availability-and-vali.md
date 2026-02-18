---
source: ethresearch
topic_id: 20645
title: The Multidimensional Scale of Overhead, Availability, and Validation Requirements
author: maxkoeg
date: "2024-10-14"
category: Architecture
tags: []
url: https://ethresear.ch/t/the-multidimensional-scale-of-overhead-availability-and-validation-requirements/20645
views: 130
likes: 2
posts_count: 1
---

# The Multidimensional Scale of Overhead, Availability, and Validation Requirements

If you’ve ever wondered why the cost of Ethereum validation is so high; or why nodes can be so computationally demanding, this paper is for you. From SSF to Validation requirements, this paper aims to uncover the lost world of tradeoffs enshrined within the Ethereum protocol.

Special thanks to [ethereum.org](https://ethereum.org/en/) and [Hacken.io](http://hacken.io) for their insight into [SSF dynamics](https://ethereum.org/en/roadmap/single-slot-finality/) and [Proto-Danksharding research](https://hacken.io/discover/eip-4844-explained/). Additional thanks to [Chainspace.co](http://chainspace.co) for their invaluable mission of bringing semi-premises storage to the masses.

[chainspace.co](http://chainspace.co)

# Overview:

Ethereum is a complicated system. Nearly every protocol choice has downstream cascading effects, from the scale of Validation Requirements (VR) and Security to TTF tradeoffs, every EIP or network alteration, no matter the size, will impact nearly every corner of the network. This paper features a few sections covering the hidden impacts of certain well-known network goals.

Every mechanic implemented in the Ethereum protocol has some downstream effect, for example, following the EIP-4844 Proto-Danksharding implementation, the Base rollup experienced a ~200% tx volume increase. Enjoy this simplicity while you can, as it’s the simplest example throughout this paper. Moving away from predictable effects, it’s clear that even core protocol mechanics have radiating effects on other protocol functionality; An example of this being validation cost.

This section merely introduces these concepts so you’ll have to read further to get more details, but in short, increasing validation cost concentrates validation responsibility, discourages malicious activity, decreases computational overhead, and affects countless other Ethereum components. Some of these effects are objectively good, some bad, and some in the grey. In addition to numerous other examples, this paper outlines these dynamics between a few critical Ethereum components. Interested? Good.

# Computational Overhead & TTF

SSF, or Single Slot Finality, has recently been a rather dismissed area of research. Overshadowed by ePBS, Verkle implementations, and countless other protocol research projects. SSF has missed the impact research phase and, nearly blindly has been accepted as a future protocol goal. While SSF should, in itself be a network improvement, many of the paths to get there could pose a detrimental impact to network health. Although an unlikely approach to solving the TTF problem, the permitted time to finality could be altered to achieve either a faster or slower finality time. You may be asking, “Why increase the Permitted TTF?” well, let’s start with the impact of decreasing it.

To clear things up, TTF is the time it takes for the Ethereum network to back a transaction with at least 33% of the total network ETH. This process requires validators to give a supermajority justification to a checkpoint that must be followed by another justified checkpoint. This practically gives an irreversible guarantee that transactions within that block are agreed upon and legitimate. This finality is required for many Dapps such as L2 - Mainnet bridges that need a guarantee that deposits were made. Permitted TTF simplifies the checkpoint bundling, block creation, and attestation process, and it represents the total time needed for this finality if the protocol enforced some time limit.

Assuming that all protocol, networking, computational inefficiencies, and bottlenecks are minimal, it can be roughly assumed that changing permitted TTF would have a linear impact on the average validator computational overhead. These are *incredibly* crude and idealistic circumstances but they do provide a baseline for expected network impacts when changing the permitted TTF. By increasing the pTTF, or by slowing down the entire finality process it can be expected that computational requirements will decrease, and under the previously stated circumstances, in a linear manner. On the other hand, by decreasing pTTF or forcibly speeding up the finality process, it can be expected that computational overhead will increase. Here are some basic and idealistic equations that represent this relationship:

**Change in computational overhead:**

CO_{new​}=CO_{old}​×\frac{TTF_{new}}{​TTF_{old}​​}

(the percent change in TTF proportionally affects the change in Computational Overhead)

**Impact on computational overhead:**

\textbf{Percent Impact On CO}=\frac{CO_{old}}{CO_{new}​−CO_{old}​​}×100

(Basic percent change formula)

&&

\textbf{Percent Impact on CO}=\frac{TTF_{new}}{​TTF_{old}​​−1}×100

(the percent impact on Computational Overhead derived by the proportional change in TTF)

Once again, these equations do not represent the actual network impact if the pTTF was changed/enforced but it does provide a minimum expected impact on computational requirements.

Through these relationships, a scale can be derived that reveals how, although reducing pTTF and speeding up the finality process may provide countless benefits, its impact on computational requirements would reduce validator numbers and make it increasingly difficult for individuals to validate. By increasing validation requirements, smaller home validators would be deterred and provide more space for larger computational centers, this then reduces networking requirements and decreases CO, potentially attracting Validators again. Considering these interactions, Validator Count impact will still be noticeable but not crippling.

pTTF

pTTF

Reduced TTF

Reduced TTF

pTTF->Reduced TTF

TTF enforcement

CO

CO

Reduced TTF->CO

Computational Compression

Validator Count

Validator Count

CO->Validator Count

1: Increased Validation Cost

CO->Validator Count

3: Reduced Validation Cost

Validator Count->CO

2: Network Relief

Concluding this segment, it’s clear that as we demand a faster TTF, our computational overhead increases and we (potentially) begin to lose the major benefit of PoS. According to the Ethereum Foundation, PoS reduces energy requirements by over 99% compared to PoW, which is great, but we must notice that this is variable, and demanding some TTF convenience via “brute force” may negate this major benefit of PoS. There are a few patterns that will arise as I continue this paper but one I’ll reveal now is how PoS and PoW are on more of a spectrum than you might think. Both Sybil Resistance mechanisms provide benefits but both are distorted with each convenience. In this case, as TTF decreases (presumably through an enforced pTTF) and we move towards convenience we lose some of our consensus identity leading to either severe Validation concentration or a larger environmental impact.

# Validation Cost & Security

Looking into the world of validation costs, (either computationally or financially) you can find another tradeoff between the cost of validation and security. Validation costs, in the traditional sense, are large deposits required of users to participate in block assembly. This deposit incentivizes good behavior through the threat of penalties and reduces validator turbulence. The difference in validation requirements between BTC and ETH is found in the discouragement method, while the cost of entry for BTC is in computation only (leading to probability discouragement) ETH validation requirements are financial (leading to price discouragement). Both of these discouragement methods, make it too costly for a malicious actor to launch a chain-destabilizing attack. By increasing validation requirements, malicious actors can be better deterred and chain integrity can be further guaranteed. Increasing this validation requirement, however, doesn’t always benefit the chain. Take, for example, validation rights and concentration.

## Validation Rights & and Concentration

As validation cost increases, fewer and fewer people are able to participate in the validation process, and remaining validators are allowed more responsibility over network activities. As validation requirements increase, validation is concentrated and network manipulation is possible. The saying, ‘Too much of a good thing’ applies here, as without high validation requirements, bad actors have more opportunity to strike, but with VR being too high, validation responsibilities are concentrated and network sovereignty is compromised. The major punchline of these distributed ledgers is their ability to incorporate the community in network-wide decisions and block assembly. Currently, Bitcoin is able to provide a lower barrier to entry for community validation contributions, while Ethereum is able to provide more equitable validation selection. In short, validation cost influences network security on both ends, one end enables community validation but reduces the cost of malicious activity, on the other end validation is concentrated, and network sovereignty is compromised. One last thing to mention is that if VRs are lowered, more will participate in network validation leading to a higher computational overhead. This mechanism alongside the aforementioned ones plays into each other creating a web of interactions all based upon each other:

pTTF

pTTF

Reduced TTF

Reduced TTF

pTTF->Reduced TTF

TTF enforcement

CO

CO

Reduced TTF->CO

Computational Compression

User Base

User Base

Reduced TTF->User Base

Convenience

Validation Cost

Validation Cost

CO->Validation Cost

1: Increased CR

CO->Validation Cost

4: Decreased CR

Validator Count

Validator Count

Validation Cost->Validator Count

2: VR

Validation Cost->Validator Count

5: VR

Security

Security

Validation Cost->Security

Malicious Activity Deterrence

Validator Concentration

Validator Concentration

Validation Cost->Validator Concentration

Validation Concentration

Validator Count->CO

3: Network Relief

Validator Concentration->Security

Centralization

*CR=computational requirement, VR=validation requirement, CO=computational overhead*

# Wrapping it all up:

Overall this article aimed not just to list out singular interactions, but to remind developers and users alike that any development made to the core Ethereum protocol will have countless lasting impacts. From computational overhead to validation concentration, this web of interactions is a testimony to the complexity of the core Ethereum protocol, and a reminder that protocol decisions should not be taken lightly.
