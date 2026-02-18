---
source: ethresearch
topic_id: 17540
title: Edinburgh Decentralization Index - Invitation to Contribute
author: mtefagh
date: "2023-11-27"
category: Data Science
tags: []
url: https://ethresear.ch/t/edinburgh-decentralization-index-invitation-to-contribute/17540
views: 2029
likes: 7
posts_count: 6
---

# Edinburgh Decentralization Index - Invitation to Contribute

Dear Ethereum Community,

The [Edinburgh Decentralisation Index (EDI)](https://www.ed.ac.uk/informatics/blockchain/edi) is a project of the [Blockchain Technology Laboratory (BTL)](https://www.ed.ac.uk/informatics/blockchain) at the University of Edinburgh which will measure the decentralization of blockchain systems. The EDI will be used by regulators, developers, and blockchain users alike for different purposes. For instance, regulators can use it to help decide whether a cryptocurrency constitutes a security. Developers and users can use it to decide which chain is safer to build and use applications.

We are currently looking to extend the EDI by adding support for more blockchains. We would like to request your assistance in providing access to a full node as a data source, or to point us to someone in the community who might be interested in contributing. Other forms of contribution are also possible, see our [GitHub repository](https://github.com/Blockchain-Technology-Lab/pooling-analysis).

Thank you for your time and consideration.

Best regards,

Mojtaba Tefagh

Blockchain Programme Manager

School of Informatics, University of Edinburgh

## Replies

**isidorosp** (2023-11-30):

This is a really interesting initiative! It may also be worth reaching out to ETH Zuri who recently published this paper https://arxiv.org/pdf/2306.10777v2.pdf. I would be happy to discuss different measures relating to decentralization (what can be measured, how, what are the different facets (e.g. entity concentration/correlation, geographic and jurisdictional dispersion, infrastructure diversity) and you can also check out work done by rated.network (some work on network penetration and HHI) as well as [@simbro](/u/simbro)’s initiative on geographic decentralization [here](https://ethresear.ch/t/geographical-decentralisation/13350/52).

I contribute to Lido DAO and would be happy to help get you guys some more details about the node operators and validators that run validators as a part of the Lido protocol. In the meantime you can check out the metrics that are aggregated and published on a quarterly basis here: [Lido Validator and Node Operator Metrics (VaNOM)](https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest) and more info on the relevant [forum thread](https://research.lido.fi/t/lido-node-operator-validator-metrics/1431/23).

---

**LadyChristina** (2023-12-04):

Hi [@isidorosp](/u/isidorosp), thanks so much for your response, the resources you linked seem very useful!

I am also a member of the EDI team and I would be happy to arrange a discussion with you to talk about Lido and decentralization in general

---

**MicahZoltu** (2023-12-04):

I think “decentralization” is not the right word here for what actually matters (at least for users).  Decentralization is a means to an end, but what actually matters is:

1. Censorship resistance.
2. Trustless.
3. Permissionless.

In other words:

1. Can someone (or some group with a reasonable ability to coordinate) censor you?
2. Do you need to trust someone (or some group with a reasonable ability to coordinate)?
3. Can you gain the ability to take any particular action in the system upon meeting well defined technical/financial requirements, or are some actions limited to certain people with special privileges?

If one can build a system that meets those requirements but is *not* decentralized, that is totally fine and great.  For example, maybe someone sends a satellite into space with some code deployed on it and anyone with a satellite dish can interact with it in a particular way and no one has control over the satellite (and it has the ability to avoid being taken over).  This hypothetical system could meet these requirements while *not* being decentralized.

---

**mtefagh** (2023-12-06):

Hi [@MicahZoltu](/u/micahzoltu) - Even though the EDI focuses more on the tools and the methodology, and the points you raised are more about the philosophy of decentralisation, I think decentralisation can be broader. Historically, people in politics and economics have considered the decentralisation of power and the risk of special interest groups, just like what people in blockchain worry about single points of failure. The main point is that the three items that you have listed are certainly important, but how can we be sure that this is the complete list and that there are no other security risks, such as the risk of censorship that you mentioned. One approach could be to try to come up with a comprehensive list, but decentralisation is a holistic measure of resilience.

---

**MicahZoltu** (2023-12-07):

Even if one disagrees with the list of endpoints I provided, I still argue that “decentralization” is not a goal in and of itself.  Decentralization is a means to an end, but it is not something people actually care about other than when it helps them achieve their *real* goals.

For example, “minimizing risk of some person or group doing Y bad thing” is a concrete endpoint that matters, and decentralization may be a means to achieve that end, but just saying “we have achieved decentralization” doesn’t matter if some person/group is still doing Y bad thing.

