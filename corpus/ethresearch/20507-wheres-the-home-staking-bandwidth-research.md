---
source: ethresearch
topic_id: 20507
title: Where's the home staking bandwidth research?
author: ryanberckmans
date: "2024-09-27"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/wheres-the-home-staking-bandwidth-research/20507
views: 1012
likes: 41
posts_count: 9
---

# Where's the home staking bandwidth research?

As a non-researcher but committed long-term observer, I’ve been surprised to see a lack of research focused on home staking bandwidth requirements. Please let me know if these studies exist and I haven’t seen them.

Here are some starter questions for home staking bandwidth research that seem interesting to me:

- Where can’t you run a home validator today?
- What happens if your bandwidth is slightly below where it needs to be? How sensitive are rewards/participation to bandwidth requirements? Is this symmetric in upload/download or is one more important?
- Many consumer internet packages have significantly worse upload. But how much worse? imo we need a rigorous target for bandwidth requirements. Do we target, say, 10th decile of global upload speeds in towns with population over 10,000, excluding countries in bottom 5% of GDP? or maybe excluding, say, Africa? We use the phrase “home staking” but for which homes do we intend support?
- How sensitive are these analyses to running N validators at home instead of 1? Do we want our target to aim for a particular number of home validators on the same internet connection, like 5 or 10?
- Can we agree to omit Starlink from our analyses and target bandwidth requirements due to its extraordinary position as the monopolistic apex outlier? Starlink is so good, and will likely remain so far ahead of other options for so many years, that if we allow Starlink to satisfy our chosen target, then Ethereum could come to rely on Starlink.

I would like to see us scientifically develop a rigorous definition of staking minimum bandwidth requirements to help maximize credible neutrality, especially so we have an solid idea of **where the entire validator set can and can’t migrate should a disaster warrant such a migration.**

## Replies

**hanniabu** (2024-09-27):

This is relevant not just for home stakers, but also for nodes

---

**0x00101010** (2024-09-27):

Strongly agree with this proposal. We urgently need a well-defined minimum network specification for Ethereum.

While addressing our current requirements is crucial, we should also look ahead. It would be great that this specification not only reflect our present needs but also guide our future development. Specifically, we need to consider the network demands of full danksharding:

1. How much bandwidth will we need to support full danksharding effectively?
2. What other network parameters might need adjustment as we progress towards this goal?

By answering these questions, we can create a roadmap that ensures our network infrastructure evolves in parallel with Ethereum’s protocol advancements.

---

**mratsim** (2024-10-08):

Ping [@AgeManning](/u/agemanning) for the followup of

  [![image](https://ethresear.ch/uploads/default/original/3X/a/4/a49a5e74ab5f6cc8240488c40f10cf657dff8708.jpeg)](https://www.youtube.com/watch?v=u8JJh-E-VMg)

---

**AgeManning** (2024-10-08):

Hey all.

There is actually quite a lot of research into this and how we can minimize bandwidth for home

stakers, especially in the context of the upgrades.

Let me link you some old, current and future research you might want to take a look at.

- We investigated and implemented changes to gossipsub via IDONTWANT. See PR and related research links: [GossipSub 1.2] IDONTWANT control message by Nashatyrev · Pull Request #548 · libp2p/specs · GitHub
- FullDAS from a networking perspective: FullDAS: towards massive scalability with 32MB blocks and beyond
- Network bandwidth and hardware requirement analysis: MigaLabs - Blockchain Data Analytics Transforming Insights in Real Time
- Expected number of peers for PeerDAS - Number of peers you need for peer sampling in PeerDAS (EIP-7594)
- An EPF member is currently researching bandwidth requirements for PeerDAS using simulations: EPF5: Week 16 - HackMD

There is quite a few people working on this, and our aim to maintain or even reduce network load for home stakers.

---

**ryanberckmans** (2024-10-10):

Thanks, these links are great.

I would also be interested in seeing answers to some of the high level questions I asked above, such as

> What happens if your bandwidth is slightly below where it needs to be? How sensitive are rewards/participation to bandwidth requirements? Is this symmetric in upload/download or is one more important?
> How sensitive are these analyses to running N validators at home instead of 1? Do we want our target to aim for a particular number of home validators on the same internet connection, like 5 or 10?

As well as - orthogonal to protocol and client research - I’d love to see studies on where exactly in the world you can run a validator (rural vs urban, 1st world vs developing countries, etc), and how we expect this location set to change over time.

---

**taxmeifyoucan** (2024-10-10):

I agree these are important questions and we need much more analysis and data on this. There is a data collection effort lead by EthPandaops happening right now. Anyone running a node can contribute by using their xatu tool [Contribute to Xatu: Join the Community Data Collection Effort · ethPandaOps](https://ethpandaops.io/posts/contribute-to-xatu-data/)

---

**yiannisbot** (2024-10-11):

Not directly related to “home staking bandwidth requirements”, but at [ProbeLab](https://probelab.io) we have done some research on bandwidth requirements recently - see:

- Ethereum Node Message Propagation Bandwidth Consumption
- Number Duplicate Messages in Ethereum’s Gossipsub Network

As for some of our future plans:

- we’ve adapted our tool, Hermes (GitHub - probe-lab/hermes: A Gossipsub listener and tracer.) to support IDONTWANT messages and we’ll repeat the studies to see how much bandwidth is actually saved,
- we also plan to do some active measurements on the available upload bandwidth of nodes and come up with a distribution. No concrete plans or details yet, but if we succeed, we’ll be able to have a good picture of what bandwidth availability looks like today and hopefully project to the future.

cc: [@cortze](/u/cortze)

---

**HawkBand** (2024-10-22):

Ethereum needs a holistic research not only of bandwith, but also of hardware requirements and minimum viable geographical decentralization. Specifically the interaction of all 3 aspects.

The first step needs to define the minimum viable geographical decentralization Ethereum needs, as in what % of the world population do we want to be able to run solo staking? how many continents do we need? what kind of countries and political spectrum are we targeting? what kind of cities, tier 1 and 2? countryside?

Step two - what kind of hardware is widely available in the countries we are targeting. In terms of storage, ram, CPU you can easily find, and at what price? How long does it take to order and receive it? what kind of monetary spend do we want to set?

if some of the countries or areas have widely inferior hardware available, can we drop them or are we losing valuable decentralization in terms of location and political spectrum and organizations?

Step three - same thing as step two but for bandwith.

