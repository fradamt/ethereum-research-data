---
source: ethresearch
topic_id: 14782
title: Anomaly detection through Temporal Graph Neural Networks (thoughts?)
author: ChristopherLey
date: "2023-02-09"
category: Data Science
tags: []
url: https://ethresear.ch/t/anomaly-detection-through-temporal-graph-neural-networks-thoughts/14782
views: 1225
likes: 1
posts_count: 1
---

# Anomaly detection through Temporal Graph Neural Networks (thoughts?)

Hi there research community,

I was directed by the Ethereum Support Program to convey our research direction to the community to gauge interest and applicability so any thoughts would be appreciated (please check out the [github](https://github.com/ChristopherLey/EthereumGraph)). Here’s what we intend to do:

To build a temporal (dynamic) graph representation of all block transactions. Which will allow us to then leverage (and extend) the deep learning frameworks based on dynamic graph neural networks / temporal graph neural networks to extract valuable insight from the transaction network at scale.

For an overview of dynamic graphs please see [“Representation Learning for Dynamic Graphs: A Survey” by Kazemi, S. et.al. (2020)](https://www.jmlr.org/papers/volume21/19-447/19-447.pdf)

The aim is to classify either a single transactions (or wallet) or a series of transactions based on the relative relations from both past and present interactions represented as a transaction graph that evolves over time from the Ethereum blockchain network and develop new TGN (temporal graph neural networks) methodologies in the process.

Typically, we divide the application cases in 3 parts:

- edge classification/prediction (e.g. classify transactions), see “Temporal Graph Networks for Deep Learning on Dynamic Graphs” by Rossi, E. et.al. (2020)
- node classification/prediction (e.g. classifying wallet types/holders), “Influencer Detection with Dynamic Graph Neural Networks” Tiukhova, E. et.al.(2022)
- graph/subgraph classification/prediction (e.g. transaction load, anomalies) “Graph Neural Network-Based Anomaly Detection in Multivariate Time Series” by Deng, A. et.al. (2021)

We have quite extensive experience applying these techniques to social networks (predicting future connections via Twitter), road networks (predicting traffic load in a sector of the network and detecting road blockages through network dynamics) and detecting anomalies in multi-input industrial processes and believe there is significant value and insight to be added to the Ethereum network.

Such use cases:

- Peer Discovery
- Network Anomaly detection
- P2P Network Health

These two objectives closely align with two of the *academic-grants-wishlist-2023* items:

- Networking & P2P: “Tools & techniques for analysis of p2p network health, early detection of attacks, identification of p2p bugs, overall data analysis, etc.”
- Security: “Machine Learning on a network level to find anomalies and enable early warning systems for issues that start occurring”

### Additional background

- “Graph-Augmented Normalizing Flows for Anomaly Detection of Multiple Time Series” Dai, E. et.al. (2022)
- “Anomaly Detection in Multiplex Dynamic Networks: from Blockchain Security to Brain Disease Prediction” Behrouz, A. et.al. (2022)
- “Imperceptible Adversarial Attacks on Discrete-Time Dynamic Graph Models” Sharma, K. et.al. (2022)
- “Provably expressive temporal graph networks” Souza, A. et.al. (2022)

# Application example

We also rested it on a small semi-supervised (mostly unlabeled) bitcoin transaction graph and got promising results

[![Bitcoin_fraud_detection](https://ethresear.ch/uploads/default/optimized/2X/c/ce874368f85a4371c14531c72f682bc07ba98f6a_2_499x499.jpeg)Bitcoin_fraud_detection1130×1132 429 KB](https://ethresear.ch/uploads/default/ce874368f85a4371c14531c72f682bc07ba98f6a)

Heres a temporal snapshot of blocks 16577361->16577370

[![Ethereum_graph_temporal_snapshot](https://ethresear.ch/uploads/default/optimized/2X/e/e45bddeaf7061b3e3fe0f02d3af409491a86709c_2_503x499.png)Ethereum_graph_temporal_snapshot1249×1240 286 KB](https://ethresear.ch/uploads/default/e45bddeaf7061b3e3fe0f02d3af409491a86709c)

# Contact me or reply here

Feel free to contact me or reply here if your a researcher in this area and wish to collaborate

p.s. Also if you have any input regarding labelling and/or data (apart from whats available via etherscan) we would be very grateful
