---
source: ethresearch
topic_id: 6512
title: "[ETH1.X call 2 - Tuesday Dec 17th] Next Steps and Collecting Research Topics"
author: MadeofTin
date: "2019-11-27"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/eth1-x-call-2-tuesday-dec-17th-next-steps-and-collecting-research-topics/6512
views: 3593
likes: 5
posts_count: 6
---

# [ETH1.X call 2 - Tuesday Dec 17th] Next Steps and Collecting Research Topics

# Eth1.x Meeting 2

Thank you all who joined the [previous](https://ethresear.ch/t/scheduling-our-first-call/6443) call. The next Eth1.X meeting will be in about 3 weeks, just before the holidays:

Date: **Tuesday December 17th @ [16:00 UTC](https://www.worldtimebuddy.com/mst-to-utc-converter?qm=1&lid=7,100,2759794&h=7&date=2019-11-12&sln=9-10.5)**

Estimated duration: **1.5 Hours**

The meeting is open to all who wish to attend. If you would like to be added to the call detail email list, please dm me or [@pipermerriam](/u/pipermerriam). We are also planning on using the Ethereum/PM repository for managing the call agenda repo similar to the AllCoreDevs agenda. Please dm me your thoughts/suggestions on how best to share the call link, coordinate the agenda among the group, and publish meeting results for the community.

For this next meeting, The overall agenda is as follows:

- Establishing a high level very loose 6-month roadmap
- Digging deeper into specific topics

We will publish a link to the agenda in the coming week.

## Collecting Eth1.x Research Topics

If you haven’t introduced yourself through the introductions thread, please do so.



    ![](https://ethresear.ch/user_avatar/ethresear.ch/sponnet/48/4256_2.png)
    [Introductions for the Eth1.x research group](https://ethresear.ch/t/introductions-for-the-eth1-x-research-group/6430/19) [Execution Layer Research](/c/execution-layer-research/37)



> Stefaan Ponnet ( @sponnet on twitter / github / telegram / … )
> Product development at AVADO (ava.do) - pre-installed blockchain node hardware
> areas of interest:
> 3.1 point-and-click solution (a.k.a. a wizard) to set up and maintain a residential ETH1.x node
> 3.2 create incentives for running hardware at home - making running a node easier

In the previous call, we discussed a few research topics of interest primarily around the development of stateless clients. There are also a few circulating Eth1.X suggested research opportunities and Priorities.

- @AlexeyAkhunov - Ethereum 1 Research topics - HackMD
- @pipermerriam -  Roadmap for Eth 1.x into 2.0 execution environment - HackMD

If you haven’t reviewed these, I would highly recommend reading them. I also invite anyone else who has a research topic lists to please share them below.

Specifically, I’d like to hear from [@cdetrio](/u/cdetrio), [@axic](/u/axic), [@karalabe](/u/karalabe), [@holiman](/u/holiman) as you all have deep experience with Eth1, and I want to make sure we get a good overview of topics from many vantage points. Also, [@tjayrush](/u/tjayrush), who is a strong voice from the community, committed to open data availability. And, [@shemnon](/u/shemnon) and a representative from the parity client.

Please tag others I missed. I will collect these and write a report for the group.

## Replies

**Mikerah** (2019-11-27):

Is privacy a priority for ETH1.x research?

I have been working on both network layer and on-chain privacy for ETH1.0 and ETH2.0 and was wondering whether these calls would be a good place to discuss some of this research.

---

**pipermerriam** (2019-12-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/mikerah/48/1616_2.png) Mikerah:

> Is privacy a priority for ETH1.x research?

Yes, but probably not for this call.  This forum category is open to all eth1.x research topics, but the call that is being scheduled is focused on stateless clients.

---

**pipermerriam** (2019-12-03):

A brief list of short term (next 6 months) items that I think we can look at doing.

- Reduce network bandwidth usage by gossiping transaction hashes rather than full transactions.  This would be an upgrade for the ETH devp2p protocol.  Clients would no longer send the full transactions, but rather only their hashes.  The recipient of the transaction hashes could then request the transactions by their hash, typically only requesting the ones they don’t already have.
- Ancient chain data pruning.  The Status message would need to be updated to have the ability for clients to broadcast what data they keep.

How do we deal with data availability problems for ancient data?  Is this actually a problem…
- One of the highly used features of ethereum clients is logs.  Can we remove this functionality and replace it with a layer-2 solution.

Other less concrete topics.

- Merklizing contract codes to reduce proof sizes.  What sort of EVM changes would be needed to support this.
- “Meta” witnesses: Non-proovable witnesses in the form of a list of addresses and storage slots which were read.  Client would still need to acquire the witness data via other means (like already having it locally or requesting it over the network).  How does this effect proof sizes.  What are the security implications of this.

---

**chfast** (2019-12-12):

Another less concrete topic which is floating around for some time:

### Lowering Ethereum client implementations requirements for black-box testing



    ![](https://ethresear.ch/user_avatar/ethresear.ch/chfast/48/8027_2.png)
    [Lowering Ethereum client implementations requirements for black-box testing](https://ethresear.ch/t/lowering-ethereum-client-implementations-requirements-for-black-box-testing/6626) [Execution Layer Research](/c/execution-layer-research/37)



> Lowering Ethereum client implementations requirements for black-box testing
> (The title is my interpretation)
> @AlexeyAkhunov proposed some time ago to drive black-box testing by p2p network interface instead of RPC methods. This eliminates the need of having RPC module in an Ethereum client implementation.
> I also know this was recently discussed with @Andrei and he proposed (my interpretation) something in functionality similar to RPC but without inter-process communication — i.e. API / FFI all…

---

**pipermerriam** (2019-12-16):

Looking for a volunteer to take notes on tomorrows call.  Anyone interested?

