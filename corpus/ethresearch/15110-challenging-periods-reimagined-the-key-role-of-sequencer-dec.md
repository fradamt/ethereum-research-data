---
source: ethresearch
topic_id: 15110
title: "Challenging Periods Reimagined: The Key Role of Sequencer Decentralization"
author: daniFi
date: "2023-03-21"
category: Layer 2
tags: []
url: https://ethresear.ch/t/challenging-periods-reimagined-the-key-role-of-sequencer-decentralization/15110
views: 2214
likes: 3
posts_count: 2
---

# Challenging Periods Reimagined: The Key Role of Sequencer Decentralization

**Check out the complete second part of the Challenging Periods Reimagined Series by clicking [here](https://threesigma.xyz/blog/optimistic-rollups-challenging-periods-reimagined-part-two). This part focuses on sequencer decentralization and its integration into our proposed dynamic challenging period model. If you have not read the first part, we highly recommend that you do so. It is available [here](https://threesigma.xyz/blog/optimistic-rollups-challenging-periods-reimagined-part-one).**

Below, AndreP3Sigma and I provide a brief introduction to this article.

# Preface

Challenging periods are a hallmark of batches submitted to L1, as well as the sequencers behind them. Therefore, they must be trimmed, considering the sequencers who submit them to L1. A sequencer with a history of honest behavior and a clear commitment to the protocol should enjoy an advantage over new sequencers, malicious sequencers with unfamiliar addresses, or those showing no interest in protocol growth. Moreover, this advantage should benefit not only the sequencers themselves but also the users of the L2 protocol.

Furthermore, there is a growing movement towards decentralizing sequencers to increase security and protocol participation through yield mechanisms.

This second part of the series covers all these topics and completes the implementation of the Dynamic Challenging Period. It explains how the governance-adjusted time factor (introduced in Part I) is computed, including a novel mechanism for sequencer selection, economic incentives for sequencers, and penalty guidelines.

The article’s sections are now introduced.

# Governance-adjusted time factor

The governance-adjusted time factor takes into account the reputation of sequencers. This is linked to the goal of transitioning to a decentralized network of sequencers. Therefore, this topic must be addressed first.

To achieve sequencer decentralization, the model enforces a multi-slot sequencer selection process that differentiates sequencers based on their honesty. The selection process is random and includes four reputation slots. Each slot represents the number of batches ever submitted by a sequencer.

At each batch epoch, a certain number of batches is attributed to each slot. This aspect is essential so that the process is not “Guilty until proven innocent” and allows all sequencers to advance in the reputation slots.

At the end of each epoch, sequencers that submitted batches are reallocated to new slots accordingly.

## Multi-chain multi-slot sequencer selection process

The single-chain multi-slot sequencer process is the basis for sequencer selection, but it has a drawback: all sequencers must be available at all times, which can be resource-intensive. To address this, a multi-chain multi-slot sequencer selection process is used. A new chain is created when the number of sequencers exceeds a specific threshold.

The maximum number of sequencers per chain is determined by balancing network latency and network centralization. By establishing a parallelism between studies made on this topic and the Ethereum network, a maximum number of 1180 sequencers was defined.

When this number is exceeded, a new chain is created, and sequencers are randomly and equally distributed among the new number of chains. At each epoch, a sequencer in a given chain knows whether it has any chance of being selected or not. It can then choose to stay online or offline, making the whole process more resource-efficient. Moreover, if they decide to be offline, then the network’s latency may also decrease as there are fewer nodes communicating.

The shuffling mechanism that occurs at the beginning of each batch epoch ensures that every time the chains are composed of different sequencers and different slot fillings, contributing to a more decentralized and democratized selection process.

For a better understanding of the selection process, please refer to the corresponding sections of the article.

## Governance-adjusted time factor function

As introduced, to ensure a fairer sequencing environment, a governance-adjusted time factor function has been created. The metric used in this model is the locking process of DAO tokens \Psi of the protocol under consideration.

The governance-adjusted time factor function is defined as follows:

\text{G}_\text{T}(\Psi) = \begin{cases}\left(\frac{\frac{23\cdot n}{{24}\cdot 7}-1}{\psi}\right)\cdot \Psi+1\,, & \Psi<\psi\\
\frac{23 \cdot n}{{24}\cdot 7}\, , & \Psi\geq \psi
\end{cases}

where ***n*** is the number of 23h periods to which reduce the batch time to, and \psi is the minimum amount of DAO tokens locked to achieve the maximum time discount.

The sequencer is incentivized to participate in the system because it benefits the ecosystem as a whole. Additionally, each sequencer gains an indirect economic benefit from the DAO token appreciation.

Any protocol seeking to adopt this model should determine a value for \psi that aligns with the value of their governance token and hardware costs involved in being a sequencer, based on their own tech implementation.

Check the article’s “Applying the governance-adjusted time factor function” section for a clear understanding of the function’s derivation.

## Economic incentive for sequencers

Locking benefits the ecosystem by reducing the challenging period. However, it’s necessary for sequencers to benefit from locking to encourage their participation. A new fixed percentage fee is introduced, where L2 users support the cost. A portion goes to the protocol treasury and the rest to the sequencer. The more DAO tokens locked, the higher the percentage they receive.

This fee may be seen as a price to pay for a better user experience. By paying it, one is incentivizing sequencers to act honestly and reduce the challenging periods. Analogously with the proof-of-stake mechanism in Ethereum’s mainnet, this new fixed percentage fee may be implemented at 30% of the one already applied in L2.

The portion that goes directly to the sequencer depends on the number of DAO tokens locked, ranging from 10% to 90%, as follows:

\text{I}_\%(\Psi) = \begin{cases}\frac{0.8}{\psi}\cdot \Psi+0.1\,,& \Psi<\psi\\
0.9\,,& \Psi\geq \psi
\end{cases}

This fee distribution mechanism applies to every sequencer that submits a batch, regardless of the slot they are in, which makes the implementation attractive to newcomers.

Check the article’s “Economic Incentive for Sequencers” subsection for a more detailed explanation.

# Penalizing a malicious sequencer

To discourage dishonest behavior, penalties are in place for malicious sequencers in optimistic rollups. If a sequencer is found to be malicious, their address is added to a blacklist and they cannot participate in sequencing using that address again. However, they can change their address and be added to the Newcomers slot. If the sequencer has locked DAO tokens at the time of the malicious behavior, a slashing mechanism will be in place. The percentage of slashing depends on the severity of the malicious behavior.

These penalties incentivize honest behavior among sequencers, ensuring a secure and trustworthy environment in optimistic rollups.

# Conclusion

Optimistic rollups offer a promising solution to Ethereum’s scalability challenge, but come with challenges such as long challenge periods and a centralized sequencer. This two-part series proposes a dynamic challenge period model, which considers the value of the transaction batch and the cost of spamming the L1 network (Part I), and stimulates decentralization, increases security, and enhances user experience by providing a multi-chain multi-slot sequencer selection process with a set of incentives.

The proposed model establishes an incentive virtuous circle, which improves security and attracts more sequencers to participate in the network. As a result, challenge periods tend to be shorter (never less than 23 hours), improving the user experience and promoting the protocol.

It is essential to consider that the proposed model is still theoretical and requires further research and testing. Nonetheless, the model provides an innovative approach to address challenges faced by current optimistic rollup implementations. Furthermore, the proposed model can help optimistic rollups compete with ZK rollups in the medium-long term period, introducing new content to the novel of decentralized sequencers.

[![Incentive Virtuous Circle.drawio](https://ethresear.ch/uploads/default/optimized/2X/b/b435be0a8dbc16bddd65acc924c066c0235e8291_2_690x389.jpeg)Incentive Virtuous Circle.drawio1920×1085 107 KB](https://ethresear.ch/uploads/default/b435be0a8dbc16bddd65acc924c066c0235e8291)

## Replies

**AndreP3Sigma** (2023-03-21):

We have completed the model for Dynamic Challenging periods by selecting a sequencer and establishing a complete incentive virtuous circle. This model benefits the entire ecosystem, which is why we believe it can be successfully implemented to further accelerate the adoption of Optimistic Rollups.

PS: A little reminder that in our model, the sequencer is the entity which orders transactions, bundles them and submits them in L1.

