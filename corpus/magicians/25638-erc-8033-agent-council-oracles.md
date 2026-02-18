---
source: magicians
topic_id: 25638
title: "ERC-8033: Agent Council Oracles"
author: phiraml
date: "2025-09-30"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-8033-agent-council-oracles/25638
views: 125
likes: 5
posts_count: 3
---

# ERC-8033: Agent Council Oracles

This standard outlines an interface for oracle contracts leveraging multi-agent councils to enable decentralized resolution of information queries. It supports trust-minimized data aggregation and validation, with agents handling off-chain processing and on-chain coordination for enhanced scalability.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1226)














####


      `master` ← `phiraml:master`




          opened 11:47PM - 28 Sep 25 UTC



          [![](https://avatars.githubusercontent.com/u/4934391?v=4)
            phiraml](https://github.com/phiraml)



          [+163
            -0](https://github.com/ethereum/ERCs/pull/1226/files)







This standard outlines an interface for **oracle contracts leveraging multi-agen[…](https://github.com/ethereum/ERCs/pull/1226)t councils** to enable decentralized resolution of information queries. It supports **trust-minimized data aggregation** and **validation**, with agents handling off-chain processing and on-chain coordination for enhanced scalability.

It defines a core flow with lightweight methods for **request creation, commitments, reveals, judging, and rewards,** while providing optional hooks for **disputes and reputation systems**.












It defines a core flow with lightweight methods for request creation, commitments, reveals, judging, and rewards, while providing optional hooks for disputes and reputation systems.

We hope that the discussion around this proposal brings new insight into strengths and weaknesses of the core flow, as well as opening it up to questions from the community.

We also hope to work closely with individuals in the data oracle and prediction market spaces to bring further improvements.

*We acknowledge Davide Crapis (Ethereum Foundation) for his time and feedback.*

## Replies

**davidecrapis.eth** (2025-10-16):

Agent councils is a very important direction that we should make progress on. Important for validation tasks in relation with ERC-8004. Looking forward for this to go live and start the community discussion.

---

**phiraml** (2025-10-16):

Thanks Davide! Excited to discuss and improve this topic with the rest of the community as well ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

