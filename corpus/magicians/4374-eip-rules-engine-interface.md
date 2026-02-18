---
source: magicians
topic_id: 4374
title: "EIP-?: Rules Engine Interface"
author: jaerith
date: "2020-06-21"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-rules-engine-interface/4374
views: 693
likes: 3
posts_count: 3
---

# EIP-?: Rules Engine Interface

https://github.com/jaerith/EIPs/edit/master/EIPS/eip-draft_rules_engine.md

**Simple Summary**

An interface for using a smart contract as a rules engine.  A deployed instance of the contract can register a data domain, create sets of rules that perform actions on that domain, and then invoke a set as an atomic transaction.

## Replies

**jpitts** (2020-06-23):

[@jaerith](/u/jaerith), is there a framework which served as inspiration for this proposal?

---

Implementations mentioned in the EIP:

Wonka Rules Engine: https://github.com/Nethereum/Wonka/

Wonka Rules Editor: https://github.com/jaerith/WonkaRulesBlazorEditor

---

**jaerith** (2020-06-23):

Hi [@jpitts](/u/jpitts)!  That’s a good question, since there are probably a few sources of inspiration for it.  Mainly, the Wonka project/framework served as the main reference point, especially in terms of its technical design, due to Ethereum being paramount in its architectural goals.  (I mainly created Wonka to see if the idea was simply insane.  As it turns out, it’s only half insane.)  However, reflecting now on my career, the culmination of Wonka was influenced to some degree by the various rules engines encountered over time (such as BizTalk, Tibco, Pega, etc.).  In fact, I think that it would be incredibly beneficial to the entire Ethereum ecosystem if bridges could be built between these existing enterprise systems (like BizTalk) and the blockchain.  That is, of course, a somewhat lofty goal, but I’m enticed by such ideas.

