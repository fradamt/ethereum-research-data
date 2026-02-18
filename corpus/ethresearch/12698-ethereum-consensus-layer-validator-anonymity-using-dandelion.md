---
source: ethresearch
topic_id: 12698
title: Ethereum consensus layer validator anonymity using Dandelion++ and RLN conclusion
author: blagoj
date: "2022-05-22"
category: Privacy
tags: []
url: https://ethresear.ch/t/ethereum-consensus-layer-validator-anonymity-using-dandelion-and-rln-conclusion/12698
views: 5332
likes: 14
posts_count: 9
---

# Ethereum consensus layer validator anonymity using Dandelion++ and RLN conclusion

[Link to the analysis](https://www.notion.so/Ethereum-consensus-layer-validator-privacy-and-feasibility-analysis-using-Dandelion-and-RLN-4674432febdc43979a67f043961442e6)

At PSE team we’ve (me, [@AtHeartEngineer](/u/atheartengineer) and [@barryWhiteHat](/u/barrywhitehat) ) researched the problem of Ethereum consensus layer validator anonymity in detail as an important problem in general but also as an application for [RLN](https://medium.com/privacy-scaling-explorations/rate-limiting-nullifier-a-spam-protection-mechanism-for-anonymous-environments-bbe4006a57d).

The problem itself is sound, as currently ethereum validators are not anonymous and [it is easy](https://ethresear.ch/t/packetology-validator-privacy/7547) to map validator IDs to physical IP addresses of beacon nodes (validator nodes and beacon nodes are usually run on the same machine for home stakers) and do DDoS attacks on these nodes in order to destabilise the network. Especially problematic is the current consensus layer design where the block proposers for an epoch are revealed in advance.

Few solutions for providing stronger validator anonymity and avoiding DDoS attacks are being worked on, usually each solving the problem from different angle. One such proposal for a solution is [WHISK](https://ethresear.ch/t/whisk-a-practical-shuffle-based-ssle-protocol-for-ethereum/11763), which tries to solve the problem at the consensus layer itself.

We’ve researched a solution that do not do any changes at the consensus layer, but deals with changes at the network layer. The initial reasoning is that network layer changes are easier to accomplish and are less tightly related to the application logic (consensus layer). Additionally the network level changes could be opt-in.

The general idea about the solution is to obfuscate the beacon node through which the message is propagated to the p2p network. This could be done by using various different tools, but we’ve chosen to experiment with [Dandelion++](https://arxiv.org/pdf/1805.11060.pdf) because of simplicity and low latency purposes (in comparison with other solutions).

The idea is to create a private pre-network which serves for obfuscation, to which only validators could send messages. At a random point (according to the Dandelion++ protocol), the message would get published as a normal consensus layer gossipsub p2p message. Additionally we would add RLN as a spam prevention mechanism for this private pre-network (stronger spam prevention than gossipsub peer scoring and extended validators + rate limiting at protocol level).

However because of latency constraints we’ve come to a conclusion that this proposal is infeasible for the Ethereum consensus layer (at least not for any strong anonymity guarantees).

Our main conclusion is that network changes are hard, the benefits added are only marginal and the complexity for these benefits is huge. Solutions such as WHISK, which approach the problem at it’s root (consensus layer changes) although complicated are most likely the right way of solving this problem long term (except other changes are made at the consensus layer which relax the latency constraint). Additionally there are some other applicable solutions for in the short term, such as leveraging multiple beacon nodes instead of one, etc.

The reasons for this conclusion are the following:

- Ethereum consensus layer latency constraints are very tight and validator reward and penalties are dependent on the latencies (anonymity solutions that add one more second of latency are likely irrelevant, probably even less than that, depending on the network state)
- In order to provide anonymity on network layer, additional steps are needed. This could be extra hops, encryption or some thing else. These extra steps add additional latency and complexity. Dandelion++ + RLN in order to provide sufficient anonymity guarantees add multiple seconds of delay.
- The gossipsub protocol is designed with peer scoring and extended validators in mind. Those can’t be completely replaced by RLN for spam prevention, as those are not only used for spam prevention. This would likely require an additional effort to make sure the gossipsub p2p protocol works correctly, and that the implemented changes do not open other vulnerabilities.

The idea in general might not be applicable to the Ethereum consensus layer, but it can be applied to p2p applications that require anonymity and are not latency constrained (the latency added from this solution is acceptable.

Additionally RLN can be used as a spam prevention and rate limiting mechanism for applications that require anonymity. In anonymous environments where rate limiting and frequency-based objective spam prevention is desired, the regular spam prevention rules do not apply and RLN can help a lot in these scenarios.

## Replies

**asn** (2022-05-23):

Hello [@blagoj](/u/blagoj) and thanks for the update on the integration of Dandelion in Ethereum.

> In order to provide anonymity on network layer, additional steps are needed. This could be extra hops, encryption or some thing else. These extra steps add additional latency and complexity. Dandelion++ + RLN in order to provide sufficient anonymity guarantees add multiple seconds of delay.

Can you please expand further on the latency overhead that Dandelion++ adds when compared to the privacy that it offers?

On a similar note, do you have any thoughts on the networking-centric [approach that Polkadot is taking with SASSAFRAS](https://ethresear.ch/t/whisk-a-practical-shuffle-based-ssle-protocol-for-ethereum/11763#sassafras-25) where it builds ephemeral one-hop proxies for the purposes of submitting VRF tickets for SSLE? While the idea is simple on the high-level, I’d be interested in insights on low-level complexities that can appear in such schemes.

Thanks!

---

**blagoj** (2022-05-29):

Hey [@asn](/u/asn), about Dandelion latency latency issues vs benefits:

Latency issues:

- 300ms added per stem hop on average (highly dependent on the network)
- 2.5 seconds for the fluff phase initiation
- more than few stem hops necessary to ensure “acceptable enough” privacy (by the paper) - this is clearly infeasible
- we need to consider 1-2 hops max

Privacy benefits:

- considering 1-2 hops max, privacy benefits are marginal, and does not improve the metadata analysis attacks by a lot
- additionally by design the privacy is limited (or more accurately the metadata analysis attack vulnerabilities) by the number of sybil nodes the attacker has - dandelion is not resilient to global network view adversaries or ISP level adversaries (and this is for the setup in the paper, this holds true even less with 1-2 max stem hops)

So realistically speaking, considering the current latency constraints of the Ethereum consensus layer, the costs vs benefits ratio seems to be not sufficient for this solution.

Regarding SASSAFRAS:

I haven’t researched this topic enough to have a strong opinion, but hopefully will do and let you know.

---

**seresistvanandras** (2022-09-14):

Congrats on this research. The anonymity on the p2p level will become increasingly more important in the near future “thanks” to the blatantly senseless laws on privacy-enhancing technologies, e.g., Tornado Cash. Really informative and super helpful. I really liked the report on the notions site you linked above [@blagoj](/u/blagoj) .

[![image](https://ethresear.ch/uploads/default/optimized/2X/c/cc3d03253e14447f17e23d3170375ecf2e5f9471_2_690x292.png)image1600×679 17 KB](https://ethresear.ch/uploads/default/cc3d03253e14447f17e23d3170375ecf2e5f9471)

This is an image taken from the linked analysis. I really like this figure because it drives home the point how latency is crucial in the context of validators and block producers. Can you elaborate more, please, how you obtained this figure? Were you running a beacon chain validator and were publishing attestations with a given delay (x-axis), and you then measured what percentage of those attestations made it in the canonical chain (y-axis)? Or how exactly was this measurement conducted?

I feel that the current latency requirements are so strict that they make it impossible to design new anonymity schemes or integrate existing ones such as Dandelion. I would not say that 2-hop Dandelion is useless and privacy benefits are marginal. See a more detailed anonymity analysis on Dandelion by Sharma, Gosain and Díaz [here](https://arxiv.org/pdf/2201.11860.pdf).

---

**Mikerah** (2022-09-14):

I wrote about using Dandelion++ for validator privacy a few years ago [here](https://github.com/ethresearch/p2p/issues/11). My approach was to be more deeply integrated with gossipsub though. However, at the time, gossipsub was significantly underspecified so it was hard to determine a path forward from that. Might be a good time to pick this up again.

---

**kaiserd** (2022-10-06):

[@blagoj](/u/blagoj) thank you for this analysis.

I have some questions/remarks regarding the latency numbers:

> 2.5 seconds for the fluff phase initiation

The paper mentions this is specific to Bitcoin Core.

Couldn’t we skip this delay for Ethereum transactions.

Also, applications outside of validator anonymity could skip this delay.

(We are working on a new [Waku spec](https://rfc.vac.dev/spec/10/) using Dandelion as deanonymization mitigation.)

> 300ms added per stem hop on average (highly dependent on the network)

The 300ms, too, were specific to Bitcoin because each hop consists of a three-way exchange: (INV, GETDATA, TX).

For Eth, we would have a similar situation with (NewPooledTransactionHashes, GetPooledTransactions, Transactions).

A possible way of reducing delay would be relaying new *transactions* unsolicitedly in the stem phase.

This should not overload the network, because the transactions are only relayed to a single Dandelion relay.

In standard operation, beacon nodes transmit *transactions* unsolicitedly to a few select peers anyway.

The fluff phase could proceed with the typical three-way exchange of NewPooledTransactionHashes, GetPooledTransactions, Transactions.

For an average of 5 stem hops, we would reduce the expected delay from 4000ms to 500ms.

This is also interesting for applications outside of validator privacy.

An average stem length of 5 seems to provide decent anonymity according to the paper, as the authors use 5 as minimal average stem length in their analysis.

(We will work on further analysing anonymity properties with respect to various average stem lengths, as well as fixed stem length.)

---

**pdsilva2000** (2022-10-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/blagoj/48/5900_2.png) blagoj:

> validator nodes and beacon nodes are usually run on the same machine for home stakers

Hi I am doing a separate research to map the validators to assess the regulatory risk of the network in the new POS model. in your note, its states that It is easy to map validators ?have you performed a validator mapping as part of your research ? I so, can you please share any results (DM) ?

---

**blagoj** (2022-10-10):

My conclusion was based on the results in this paper: [Packetology: Validator Privacy](https://ethresear.ch/t/packetology-validator-privacy/7547), as well as discussions I had with multiple people in the past previous year or so. Unfortunately I don’t have any hard data to share, or done validator mapping myself.

---

**pdsilva2000** (2022-10-10):

Thanks for your reply. Splitting the Beacon Nodes from Beacon Validators is a security measure that protects validators in the network. whilst the validator duties are public in each slot, are are yet to map them to a low granularity (e.g. resolving to country).

