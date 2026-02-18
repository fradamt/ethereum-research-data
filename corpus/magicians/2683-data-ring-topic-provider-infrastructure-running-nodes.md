---
source: magicians
topic_id: 2683
title: "Data Ring Topic: Provider Infrastructure / Running Nodes"
author: tjayrush
date: "2019-02-19"
category: Working Groups > Data Ring
tags: []
url: https://ethereum-magicians.org/t/data-ring-topic-provider-infrastructure-running-nodes/2683
views: 887
likes: 6
posts_count: 7
---

# Data Ring Topic: Provider Infrastructure / Running Nodes

The ecosystem should begin moving away from relying on centralized node/data providers. Potential areas for discussion:

1. Forking client code to add indexing / digesting services
2. EIPs specific to improving usability from the nodes
3. Better documenting existing RPC interfaces
4. Improving cross-client consistency (i.e. Parity traces vs. Geth traces)
5. Modular / plugable clients.
6. dAppNode

**Action item:** [@Patrick](/u/patrick) will start a thread about what is required for devs to run nodes.

**Action Item:** [@tjayrush](/u/tjayrush)  will write a Medium post and start an EIP related to building indices.

Please provide links or comments to any of the above.

## Replies

**jpitts** (2019-02-21):

Super-excited about this one, as you know!

I would add business models / incentives /  “sustainability”.

---

**ankitchiplunkar** (2019-02-21):

This is a great topic.

We have earlier written about cross client consistency

1. https://medium.com/tokenanalyst/weird-quirks-we-found-in-ethereum-nodes-d5dcbad0c86
2. https://medium.com/tokenanalyst/towards-production-grade-open-source-ethereum-nodes-6ef2e9458fb4

Would be willing to contribute in any way possible.

---

**ferranbt** (2019-02-25):

Hi!

Some of the work Im working on might be useful for this topic.

For the past months I have been working on a modular Ethereum client in Go (https://github.com/umbracle/minimal). The main goal is to increase the use cases for the client by building it with plug and play components. For example, a discovery protocol to build clusters of nodes or an bandwidth-limited syncer protocol for contrained devices.

Besides, I am also working on another project that might be of interest for the data ring. Heura (https://github.com/umbracle/heura) is a Domain-Specific Language (DSL) to interact with Ethereum smart contracts. With a couple of lines is possible to call smart contract functions or listen for

events on specific topics. It is intended to make it extensible with plugins (e.g. send email alert messages for specific events or dump an ETL operation into a JSON file). Heura could be used to build indexes and digesting services for Dapps on top of Minimal.

I hope I can be of any help.

---

**tjayrush** (2019-02-26):

I’ve been thinking that some of the ideas in this post might benefit from short presentations at the Magician’s council in Paris. I think [@ankitchiplunkar](/u/ankitchiplunkar) will be there. I’ll be there. [@ferranbt](/u/ferranbt)  will you be in Paris next week?

[@ankitchiplunkar](/u/ankitchiplunkar) Perhaps we can each do a short demo of the work we’re doing related to the above as part of the data ring discussion. Your thoughts?

---

**ankitchiplunkar** (2019-02-26):

Sounds, great. We can do a 10-15 minute presentation to onboard people into these discussions

---

**ferranbt** (2019-02-28):

[@tjayrush](/u/tjayrush) Yes, I’ll be in Paris for the magicians council.

