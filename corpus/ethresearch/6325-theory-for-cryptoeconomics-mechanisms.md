---
source: ethresearch
topic_id: 6325
title: Theory for Cryptoeconomics Mechanisms
author: szhygulin
date: "2019-10-14"
category: Economics
tags: [security]
url: https://ethresear.ch/t/theory-for-cryptoeconomics-mechanisms/6325
views: 1806
likes: 2
posts_count: 2
---

# Theory for Cryptoeconomics Mechanisms

Hey,

Have anyone seen this paper?


      ![image](https://static.arxiv.org/static/browse/0.2.7/images/icons/favicon.ico)
      [arXiv.org](https://arxiv.org/abs/1905.08595)


    ![image]()

###

Cryptocurrencies have garnered much attention in recent years, both from the
academic community and industry. One interesting aspect of cryptocurrencies is
their explicit consideration of incentives at the protocol level. Understanding
how to...








It seems to be a very good advancement in formalizing theory in cryptoeconomic mechanisms and distributed computation.

## Replies

**witgaw** (2020-05-05):

Hi,

Read it before CES’20 at MIT and went to their talk there. Some of the notes I took at the time in case anyone finds them useful:

- The paper surveys literature on game theoretic models applied to fields of mechanism design, cryptography, distributed systems.
- It provides fairly rigorous definitions of game theoretic notions useful for study of incentives in protocols.
- It stresses importance of analysing robustness of a protocol not just by considering its’ internal rules, but also the external environment and types of agents likely to interact with it.
- A large part of it is devoted to the study of incentive schemes - something that might be useful in the fine-tuning phase of protocol development.
- It contains references to well-established papers from the fields mentioned above - so it might be worth checking them out if anyone considers applying any of the tools outlined by the authors.
- It includes a section on analysis of Bitcoin and a few other protocols with the methods outlined in the preceding sections - though the analysis is quite superficial and doesn’t contain any detailed modelling.

Review summary from conference organisers: https://cryptoeconomicsystems.pubpub.org/pub/ml84muxq/

