---
source: ethresearch
topic_id: 20426
title: "PANDAS: A Practical Approach for Next-Generation Data Availability Sampling"
author: oascigil
date: "2024-09-13"
category: Sharding
tags: [data-availability, p2p, scaling]
url: https://ethresear.ch/t/pandas-a-practical-approach-for-next-generation-data-availability-sampling/20426
views: 1617
likes: 7
posts_count: 11
---

# PANDAS: A Practical Approach for Next-Generation Data Availability Sampling

**PANDAS: A Practical Approach for Next-Generation Data Availability Sampling**

Authors: Onur Ascigil1, Michał Król2, Matthieu Pigaglio3, Sergi Reñé4, Etienne Rivière3, Ramin Sadre3

**TL;DR**

- PANDAS is a network layer protocol that supports Danksharding with 32 MB blobs and beyond.
- PANDAS aims to achieve a 4-second deadline for random sampling (under the tight fork choice model).
- Following the Proposer-Builder Separation (PBS), resourceful builders perform the initial distribution (i.e., seeding) of samples to the nodes.
- PANDAS proceeds in two phases during each slot: 1) Seeding Phase, where the chosen builder of a slot distributes subsets of rows and columns of a 2-D encoded blob to the validator nodes, and 2) Row/Column Consolidation and Sampling phase, where nodes sample random cells and at the same time retrieve and reconstruct assigned rows/columns to boost the data availability of cells.
- PANDAS uses a direct communication approach, which means 1-hop, i.e., point-to-point communications, for both seeding and sampling phases rather than a gossip-based, multi-hop approach or a DHT.

We make the following assumptions when designing PANDAS:

**Assumption 1) Resourceful Builders:** Following the [Proposer-Builder Separation (PBS)](https://www.google.com/url?q=https://ethereum.org/en/roadmap/pbs/&sa=D&source=editors&ust=1726244230016209&usg=AOvVaw2u6aLVhX_45QF4JizRPRrL) scheme, in PANDAS, a set of resourceful builders — e.g., cloud instances with sufficiently high upload bandwidth such as 500 Mbps or more — undertake the distribution of seed samples to the network.

**Assumption 2) Builder Incentives:** The builders have an incentive for the blob data to be available since the block will be accepted only if DAS succeeds. However, different builders can have different amounts of resources. The interest of rational builders is to guarantee that data will be considered available while spending a minimal amount of resources.

**Assumption 3) Validator Nodes (VNs) are the primary entities of DAS protocol:** A single Validator Node (VN) performs only a single sampling operation (as one entity), independent of the number of validators it hosts.

**Assumption 4) Dishonest Majority:** A majority (or even supermajority) of VNs and builders can be malicious and, therefore, may not follow the protocol correctly.

**Assumption 5) Sybil-resistance** **VNs**: An honest VN can use a [Proof-of-Validator](https://www.google.com/url?q=https://ethresear.ch/t/proof-of-validator-a-simple-anonymous-credential-scheme-for-ethereums-dht/16454&sa=D&source=editors&ust=1726244230018106&usg=AOvVaw2S4QQ8d0c8zadKQKbVBQ6W) scheme to prove that it hosts at least one validator. If multiple nodes attempt to re-use the same proof, they can be blocklisted by other honest nodes and builders.

Below are the objectives of PANDAS:

**Objective 1)** **Tight fork choice:** *Honest validator nodes (VNs) complete* *random sampling* *before voting for a block, even when the* *majority of VNs are malicious**.* Therefore, we target the [tight fork choice model](https://www.google.com/url?q=https://ethresear.ch/t/das-fork-choice/19578&sa=D&source=editors&ust=1726244230019035&usg=AOvVaw0jtQl6ICcsg9iqBiQh4Mst), which means that honest VNs in a slot’s committee must complete random sampling before voting *within four seconds* into that slot.

**Objective 2)** **Flexible builder seeding strategies:** Given that different builders can have different resources, our design allows the block builder the flexibility to implement different blob distribution strategies, each with a different trade-off between security and resource usage. For higher security, the builder can send more copies of the blob’s cells to validator nodes, ensuring higher availability. Conversely, to minimise resource usage, the builder can distribute a single copy of each cell at most, reducing bandwidth usage at the expense of lower security. This flexible approach allows the builder to navigate the trade-off between ensuring data availability and optimising bandwidth while under the incentive for the block to be deemed available by validator nodes to be accepted.

**Objective 3) Allowing Inconsistent Node Views:** Our objective is to ensure that the VNs and the builders are not required to reach a consensus on the list of VNs. While we aim for the VNs and builders to generally agree on the set of VNs in the system, it is not necessary for the VNs to maintain strictly consistent views or for the builders’ and VNs’ views to be fully synchronised.

**PANDAS Design**

**Continuous Peer Discovery:** To achieve Objective 3, the nodes in the system perform continuous peer discovery in parallel to the protocol phases below to maintain an up-to-date “view” containing other peers. *The builder* and the VNs aim to discover all the VNs with a valid [Proof-of-Validator](https://www.google.com/url?q=https://ethresear.ch/t/proof-of-validator-a-simple-anonymous-credential-scheme-for-ethereums-dht/16454&sa=D&source=editors&ust=1726244230020521&usg=AOvVaw1-IdEEIXKyEqrBkmFcpdG1). We expect both the builder and VNs to have a close but not perfect view of all the VNs in the system.

A membership service running the peer discovery protocol inserts new (verified) VNs to the view and eventually converges to a complete set of VNs. Peer discovery messages are piggybacked to sample request messages to reduce discovery overhead.

PANDAS protocol has two (uncoordinated) phases, which repeat during each slot:

**Phase 1**) Seeding,

**Phase 2)** Row/Column Consolidation and Sampling

In the seeding phase, the builder pushes subsets of row/columns directly to the VNs where row/column assignment is based on a deterministic function. Once a VN receives its samples from the builder, it consolidates the entire row/column it is assigned to (by requesting missing cells from other VNs assigned to the corresponding row/column) and simultaneously performs random sampling.

VNs do not coordinate to start consolidating and sampling. Therefore, a node finishing phase 1 can begin phase 2 immediately without coordinating with other nodes. The VNs who are the committee members of a slot must complete seeding and random sampling within 4 seconds into the slot.

Below, we explain the two phases of our protocol in detail.

**Phase 1- Seeding**: The builder assigns VNs to individual rows/columns using a deterministic function that uses a hashspace as we explain below. This mapping of VNs to individual rows/columns is dynamic and changes in each slot. The mapping allows nodes to locally and deterministically map nodes to rows/columns without requiring the number or full list of nodes to be known.

The Builder prepares and distributes seed samples to the VNs as follows:

**1.a) *Mapping Rows/Columns to static regions in the hashspace:*** The individual rows and columns are assigned static regions in the hashspace as shown in the upper portion of Figure 1.

**1.b)** ***Mapping VNs to a hashspace*** *:* The builder uses a sortition function FNODE(NodeID, epoch, slot, R) to assign each VN to a key in the hashspace. The function takes parameters such as NodeID, which is the identifier of the node (i.e., peer ID), epoch and slot numbers, and a random value R derived from the header of the block header from the previous slot.

[![image3](https://ethresear.ch/uploads/default/optimized/3X/4/8/48bcaeee1eef51ab1128caf78e0d29d6d54dbe7e_2_690x352.png)image3904×462 68.9 KB](https://ethresear.ch/uploads/default/48bcaeee1eef51ab1128caf78e0d29d6d54dbe7e)

**Figure 1:** Assignment of Row samples to VNs. The Column samples are mapped similarly.

A VN assigned to a row’s region will receive a subset of the cells belonging to that row from the builder. As the VNs are re-mapped to the hashspace during each slot using FNODE, their row/column assignments can also change.

**NOTE:** A dynamic, per-slot assignment of rows and columns to VNs is impossible in a gossip-based seeding approach where per-row and per-column gossip channels must remain relatively stable over time.

**1.c)** **Row/Column *Sample Distribution:*** For each row and column, the builder applies a best-effort distribution strategy to push subsets of each row/column to the VNs mapped to the corresponding row/column’s region. The builder uses a direct communication approach, particularly a UDP-based protocol, to distribute the cells for each row/column directly to the VNs.

*Rationale for direct communication**:* We aim to complete the seeding phase as quickly as possible to give time for committee members to complete random sampling before voting (Objective 1).

Row/Column Distribution Strategies: We allow the builders to choose distribution strategies based on resource availability in line with Objective 2. A trade-off between resource usage and data availability exists for different distribution strategies. Consider the example in Figure 2 for distributing two rows. In one extreme case (on the left), the builder distributes the entire row 1 to each VN in the row’s region for improved data availability at the expense of higher resource usage. In another extreme case, the builder sends non-overlapping row pieces of row 6 to each VN in that row’s region, which requires fewer resources but results in less availability of individual cells.

We are currently evaluating different distribution strategies, including ones that can deterministically map individual cells of rows/columns to individual VNs in the row/column’s region.

**NOTE**: The builder is only involved in the Seeding phase.

[![image1](https://ethresear.ch/uploads/default/optimized/3X/2/d/2d447780eca05e1064f2f780b7a1dcaad92a386e_2_690x374.png)image1904×490 103 KB](https://ethresear.ch/uploads/default/2d447780eca05e1064f2f780b7a1dcaad92a386e)

**Figure 2:** Two (extreme) strategies to distribute row samples to the VNs in the corresponding row’s region.

**Phase 2- Row/Column Consolidation and Sampling**: VNs that are part of the current slot’s committee aim to complete random sampling within the slot’s first four seconds (i.e., voting deadline). To boost the availability of cells, particularly for the committee members of the slot who must perform (random) sampling within four seconds, the VNs also consolidate, i.e., retrieve the full row and column they are assigned to based on the FNODE mapping as part of row/column sampling.

**2.a) VN Random Sampling:** The VNs in the current slot’s committee attempt to retrieve [73 randomly chosen cells](https://www.google.com/url?q=https://ethresear.ch/t/peerdas-a-simpler-das-approach-using-battle-tested-p2p-components/16541/5?u%3Doascigil&sa=D&source=editors&ust=1726244230027394&usg=AOvVaw3dcjIB9khL3JRIj_je8GsM) as soon as they receive their seed samples from the builder.

Using the deterministic assignment FNODE, VNs can locally determine the nodes expected to eventually custody a given row or column.

*Sampling Algorithm:* Some of these nodes may be offline or otherwise unresponsive. Sequentially sending requests for cells risks missing the 4-second deadline for the committee members.

[![image2](https://ethresear.ch/uploads/default/optimized/3X/b/3/b315051e7742d17e0aabd822c6d282c69402eead_2_690x276.png)image21048×420 45.2 KB](https://ethresear.ch/uploads/default/b315051e7742d17e0aabd822c6d282c69402eead)

**Figure 3:** Sample Fetching Example: The rows and columns assigned to each VN are shown on the top of the corresponding VN. VN14 knows to send a request to VN78 to retrieve cell one based on the knowledge of the mapping FNODE.

At the same time, sending requests to all peers holding copies will lead to an explosion of messages in the network and bear the risk of congestion. Fetching must, therefore, seek a tradeoff between the use of parallel and redundant requests on the one hand and latency constraints on the other hand. Our approach employs an adaptive cell-fetching strategy using direct communication between nodes through a UDP-based (connectionless) protocol. The fetching algorithm can tolerate losses and offline nodes.

**2.b) VN Row/Column Consolidation:** If a VN receives less than half of the cells of its assigned row or column from the builder (as a consequence of the builder’s chosen distribution strategy), it requests the missing cells from other VNs. A VN requests cells from only the VNs assigned to the same row/column’s region during row/column consolidation. When a VN has half of the cells of a row or column, it can locally reconstruct the entire row or column.

*The Rationale for Consolidating Row/Column:*

- Reconstructing missing cells: while performing row/column sampling, VNs reconstruct missing cells.
- To boost the availability of cells: Given the deterministic mapping (FNODE), the builder can choose any distribution strategy to send subsets of rows and columns to the VNs. Row/Column consolidation aims to improve the availability of samples so that random sampling can be completed on time.

Ideally, the builder should select a seed sample distribution strategy that enables VNs to consolidate rows and columns efficiently. To facilitate this, the builder can push each VN a map (together with the seed samples) that details how individual cells of a row/column are assigned to VNs within that row/column’s region as part of the builder’s distribution strategy. With this map, VNs can quickly identify and retrieve missing cells to reconstruct a complete row, thereby improving the availability of the data.

**NOTE:** In some DAS approaches, the term ‘row/column sampling’ refers to nodes retrieving multiple rows and columns before voting on the availability of the blob. In our approach, nodes retrieve rows and columns to enhance data availability, supporting validators who must perform random sampling before they vote.

We refer to this as ‘row/column consolidation’ instead of ‘row/column sampling’ because in PANDAS, committee members vote based on random sampling, and they do not directly sample entire rows or columns.

**What about Regular Nodes (RNs)?**

Unlike VNs, RNs do not obtain seed row/column samples from the builder. The builder sends initial seed samples to a Sybil-resistant group of VNs that use the [Proof-of-Validator](https://www.google.com/url?q=https://ethresear.ch/t/proof-of-validator-a-simple-anonymous-credential-scheme-for-ethereums-dht/16454&sa=D&source=editors&ust=1726244230030492&usg=AOvVaw3FE6AN3DjFuibklaNwyDPO) scheme. There is currently no mechanism for RNs to prove that they are not Sybils; therefore, the initial distribution of samples from the builder only uses VNs.

Using the public deterministic function FNODE, RNs can be similarly mapped to individual row/column regions. Once mapped to a region, RNs can (optionally) perform row/column consolidation to retrieve entire rows and columns and respond to queries for cells within their assigned region.

Like other nodes, RNs must perform peer discovery. In general, RNs aim to discover all the VNs and can also seek to discover other RNs. Given the knowledge of other peers through peer discovery, RNs can perform random sampling through direct communication. Unlike VNs, RNs are not under strict time constraints to complete sampling — they can start sampling after the VNs, for instance, after receiving the block header for the current slot.

**Discussion & On-going Work**

We assume rational builders to have an incentive to cut costs (and under provision) but, at the same time, aim to make blocks available (to be rewarded). This implies that the builders will aim for the row/column consolidation to be as efficient as possible, i.e., with efficient consolidation, which boosts the availability of cells, the builder can send less copies of each cell during the seeding phase to cut costs.

We are currently experimenting with different distribution strategies with malicious VNs withholding samples and attempting to disrupt peer discovery. Our DAS simulation code is available on [DataHop GitHub repository](https://www.google.com/url?q=https://github.com/datahop/kademlia-simulator/&sa=D&source=editors&ust=1726244230032037&usg=AOvVaw1UC1uGBj8kO1dTX4Q01QRY).

1 Lancaster University, UK

2 City, University London, UK

3 Université Catholique de Louvain (UCLouvain)

4 DataHop Labs

## Replies

**fradamt** (2024-09-16):

Nice work! A couple of quick questions after a first read:

![](https://ethresear.ch/user_avatar/ethresear.ch/oascigil/48/15349_2.png) oascigil:

> NOTE: A dynamic, per-slot assignment of rows and columns to VNs is impossible in a gossip-based seeding approach where per-row and per-column gossip channels must remain relatively stable over time.

In your view, what is the goal of quickly rotating the assignments?

![](https://ethresear.ch/user_avatar/ethresear.ch/oascigil/48/15349_2.png) oascigil:

> 2.a) VN Random Sampling: The VNs in the current slot’s committee attempt to retrieve 73 randomly chosen cells as soon as they receive their seed samples from the builder.

Why do they not also get the 73 cells directly from the builder? For the purpose of having *all but up to a very small minority* of the validators voting correctly, it makes little difference whether the samples all come from the same party

---

**harnen** (2024-09-19):

> Blockquote
> In your view, what is the goal of quickly rotating the assignments?

There are two main reasons:

1. Load balance - the pseudorandom assignment might create regions with more or less validator nodes. The validator nodes assigned to less dense regions must work more to handle all the sampling requests. By rotating the assignments, we ensure it’ll even out in the long run.
2. Security - an attacker who knows the assignment well in advance can try to attack a specific region to disturb the sampling. This could be done by placing its validators in this region or corrupting/attacking specific validator nodes. The rotating assignment gives the attacker much less time to prepare for such attacks and ensures that any group of colluding validators will be scattered around the regions.

> Blockquote
> Why do they not also get the 73 cells directly from the builder? For the purpose of having all but up to a very small minority of the validators voting correctly, it makes little difference whether the samples all come from the same party

Again, two reasons here:

1. Fixed builder load - providing sampled cells directly by the builder means that the builder load increases with the number of the validator nodes (e.g., 73*). With our approach, the builder can always give fewer cells* to each validator node keeping its load fixed and independent of the number of validator nodes.
*as long as the validator nodes in a region can jointly reconstruct a row/column
2. Preventing network split attacks - if validator nodes take the sampled cells directly from the builder, the builder can make the sampling fail for some specific validators. This is potentially dangerous. Preventing that would require some solid anonymity layer. This is very difficult to deploy in practice. Having a 2-step approach fixes this problem. Once the builder gives the custody cells to validator nodes it cannot control whether sampling will fail for some specific validator nodes.

---

**pop** (2024-09-26):

I have a concern on the direct communication.

Even though we assumes that the builder is resourceful, it turns out that we cannot assume that it’s infinitely resourceful. With direct communications, I think the builder is required to have too much bandwidth for this.

Since every byte that a VN receives during the seeding phase has to be sent by the builder, let’s say the average download bandwidth consumption of a VN is `b` and there are `n` nodes in the network the average upload bandwidth consumption of a builder is `B = b*n`. No matter what trade-off you do (like the one in Figure 2), the equation is always true.

This poses a scalability problem. Let’s say `b = 10Mbps` and `n = 20,000`. Now `B = 200Gbps`. We can assume that the bandwidth of the builder is high, but not this high. 200Gbps is even more than the whole bandwidth consumption of some medium-sized city. In fact, you cannot even buy an Amazon EC2 instance with 200Gbps. Even if you can buy one, it doesn’t mean that you can reach 200Gbps. Your EC2 instance can probably handle that but the middle Internet Exchanges probably cannot. The physical locations of the machines affect the network throughput as well.

Some may argue that a home Internet connection can have a high bandwidth of 1Gbps, so 200Gbps should be equivalent to just 200 homes. This is not true. When you buy the Internet package, the ISP assumes that you won’t use all the 1Gbps all the time. Even if you use it all the time, they assume that not many people will do it.

You will probably say that in order to reduce `B` we can reduce `b`. No, we can’t. The whole point of DAS is to reduce the bandwidth consumption of the nodes, so we should set `b` to a reasonable number.

So I think getting rid of the direct communication is mandatory. Otherwise, the protocol is not really practical.

---

**oascigil** (2024-09-26):

Thanks for the comment, Pop.

The objective of PANDAS is for the builder to supply only a tiny portion of the blob to each VN. Then, the VNs perform P2P random sampling to probabilistically ensure that the complete blob data is available (alongside P2P row/column consolidation, which does not involve the builder). The builder is not expected to supply most/all blob data to each VN.

The scalability problem exists only if the builder’s bandwidth consumption is proportional to the number of VNs. Our direct communication approach allows builders to choose a distribution strategy that trades off their resource utilisation (i.e., costs) and the will to receive rewards linked to successful data availability sampling (i.e., security).

A reasonable strategy is to keep the builder’s upload bandwidth consumption fixed while diminishing the download bandwidth requirement for individual VNs as the number of VNs increases. This can be achieved by dividing the fixed-sized blob data of B bytes into #VNs pieces and delivering each piece to an individual VN.

For increased security, the blob data B sent by the builder can include redundancy to deliver K copies of each cell; however, redundancy selection is about the target level of security and not related to the number of VNs.

To give you some numbers, let's assume #VNs = 10,000, and the blob data size, encoded as 512*512 cells, is 128 MB. If the builder targets a deadline of 1 second to seed the network with one copy of each cell (K=1), its upload bandwidth is 128MB/1sec ~= 1Gbps. Each VN needs, on average, 100 kbps of download bandwidth. Using K=1 means relying on erasure coding to recover lost cells (e.g., due to faulty or malicious VNs). Using a higher cell redundancy factor (e.g., K=5), the builder’s upload requirement increases fivefold, i.e., goes up to 5*128MB/1sec ~= 5 Gbps, well within the capacity of standard cloud instances.

---

**pop** (2024-10-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/oascigil/48/15349_2.png) oascigil:

> A reasonable strategy is to keep the builder’s upload bandwidth consumption fixed while diminishing the download bandwidth requirement for individual VNs as the number of VNs increases. This can be achieved by dividing the fixed-sized blob data of B bytes into #VNs pieces and delivering each piece to an individual VN.

This doesn’t address my issue yet.

I think we are not on the same page yet. Many of your points don’t make sense.

1. What I want to fix is the VN bandwidth requirement not the builder bandwidth because the problem that I want to point is on the builder bandwidth. Let’s make it variable to discuss my issue.
2. Fix the number of VNs as well since we currently have ~10k nodes and it’s unlikely to go significantly lower or higher.

I feel like your comment didn’t try to address my issue at all and you just repeated what you have said.

---

**srene** (2024-10-07):

Hi Pop,

We believe that we already addressed your concerns and provided specific details regarding the bandwidth requirements for both validator nodes (VNs) and the builder.

Your claim that “if each VN’s download bandwidth is b, then the builder’s upload consumption will be b x n” simply does not apply to the strategy we explained in our previous comment.  If the total blob data (counting all the cells that will be sent individually to different VNs)  to be sent in one slot is 128MB, it will require 1Gbps (approximately) link to be sent in 1 second (and not 200Gbps)

To clarify: in the proposed distribution strategy, the download bandwidth (used for seeding) for individual VNs decreases as the number of VNs increases. At the same time, the builder’s upload bandwidth remains constant, regardless of the number of VNs.

You also mentioned that “many of our points don’t make sense.” Which points exactly? Please specify what you find unclear so we can move the conversation forward productively.

---

**pop** (2024-10-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/srene/48/17803_2.png) srene:

> Your claim that “if each VN’s download bandwidth is b, then the builder’s upload consumption will be b x n” simply does not apply to the strategy we explained in our previous comment. If the total blob data (counting all the cells that will be sent individually to different VNs) to be sent in one slot is 128MB, it will require 1Gbps (approximately) link to be sent in 1 second (and not 200Gbps)

Let’s talk about the `b x n` thing.

> it will require 1Gbps (approximately) link to be sent in 1 second (and not 200Gbps)

It’s 1Gbps only if you assume that the builder sends only one copy of each cell. I didn’t assume that in my 200Gbps number, so your contradiction is not valid.

> To clarify: in the proposed distribution strategy, the download bandwidth (used for seeding) for individual VNs decreases as the number of VNs increases.

Of course, the VN bandwidth decreases as the number of VNs increases because of `B = b*n`. If you fix `B`, `b` will decreases as `n` increases.

> At the same time, the builder’s upload bandwidth remains constant, regardless of the number of VNs.

How can it be constant? If you increase the number of copies, you increase the builder bandwidth already. The size of the whole matrix is 128MB, right? Assuming that you need to send it in 1 second, the builder needs to have `1Gbps` **if it sends only one copy for each cell**. If we let `c` be the number of copies for each cell, the builder bandwidth will be `c * 1Gbps`, right? So the final equation will be `B = b*n = c*1Gbps`.

You claimed that `B = b*n` is not true for some strategy. Can you explain more? I think you haven’t made a valid reason yet.

Let me explain the `B = b*n` once more. When a VN (let’s call it v_i) downloads a byte, it has to be sent by the builder, right? and every byte that the builder sends goes to some VN. Let d_i be the number of bytes the VN v_i downloads and D be the number of bytes the builder sends. So \sum{d_i} = D. Divide it by a unit of time, it will become \sum{b_i} = B, where b_i is the bandwidth of v_i. Let b = \sum{b_i}/n, so B=b*n.

Now let’s talk about my numbers. Because I put 200Gbps for B, it means that my `c` is 200. You may argue that 200 is too high. I think the lowest that we can go is 100. That even means 100Gbps for the builder, which is still too high. Setting `c` to something like 5-10 doesn’t work because it’s possible that the network will not be fault-tolerant and the VNs holding those copies are probably all malicious.

Does that make sense? What do you think?

Another point (which you can ignore): From the `B = b*n = c*1Gbps` equation. If you feel that `c=200` is too high, we tend to increase the size of the matrix rather reducing `B` in order to increase the data throughput, (i.e. `B=200Gbps=100*2Gbps` rather than `B=100GBps=100*1Gbps`). The point is we need to keep `b` as high as possible while keeping it attainable to fully utilize the bandwidth of the network (I chose 10Mbps in this case) and `n` doesn’t change much so it’s preferable to keep `B` 200Gbps.

---

**oascigil** (2024-10-16):

Hi Pop,

![](https://ethresear.ch/user_avatar/ethresear.ch/pop/48/9805_2.png) pop:

> You claimed that B = b*n is not true for some strategy. Can you explain more? I think you haven’t made a valid reason yet.

Here is a simple random seeding strategy: for each cell of a row (or column) r, the builder selects c Validator Nodes (VNs) uniformly at random from the VNs in the row r’s region to distribute c copies of the cell. Upon receiving its seed cells for the assigned row/column, a VN communicates with other VNs in its region to consolidate the entire row/column.

The graph below illustrates the probability of successful consolidation, which is the probability that all honest Validator Nodes (VNs) retrieve and reconstruct the entire row/column they are assigned to. This probability is calculated given that c copies of each cell are distributed using the above random seeding strategy in the presence of a fraction F of malicious peers within each row/column’s region. The malicious VNs withhold the samples they retrieve from the builder.

Consolidation succeeds if at least one copy of half the cells of each row/column is seeded to the honest VNs, assuming honest VNs have discovered each other. The graph below shows the probability of successful consolidation under different ratios of malicious VNs using the random seeding strategy.

![](https://ethresear.ch/user_avatar/ethresear.ch/pop/48/9805_2.png) pop:

> Now let’s talk about my numbers. Because I put 200Gbps for
> B, it means that my c is 200. You may argue that 200 is too high. I think the lowest that we can go is 100. That even means 100Gbps for the builder, which is still too high. Setting c to something like 5-10 doesn’t work because it’s possible that the network will not be fault-tolerant and the VNs holding those copies are probably all malicious.

As shown in the graph below, even with a supermajority (i.e., F= 0.9) of malicious VNs, consolidation succeeds with a probability of 1.0 when c is only 9 (red line). So, even in the supermajority of dishonest VNs, distributing c = 9 copies of each cell is sufficient. This requires only 9 Gbps of upload bandwidth by the builder.

We are unsure why you think c = 200 or even c = 100 is necessary. Could you please clarify your reasoning? You mentioned that network faults, such as packet drops, could occur when a single cloud instance handles the seeding. However, it is unclear to what extent such faults might impact the system (when sending data at a few Gbps rate), and we would like to run experiments using a cloud instance to assess this.

That said, our approach is also compatible with a distributed builder, where the builder’s task is spread across multiple nodes. This setup could help mitigate the risk of packet loss by distributing the workload.

**[![](https://ethresear.ch/uploads/default/optimized/3X/2/2/22331600283ff59c57e8a64a9e7f2f2cf19c9807_2_545x451.png)846×701 40.1 KB](https://ethresear.ch/uploads/default/22331600283ff59c57e8a64a9e7f2f2cf19c9807)**

Below is how we compute the probability of successful consolidation in the above graph:

P(all copies to malicious peers)= Fc

P(at least one copy to honest peer)=1− P(all copies to malicious peers)

P(at least N/2 out of N of cells are stored by honest peers) = 1- Sum(Binom (1 .. N/2, N, P(at least one copy to honest peer))

P(all 512 row/column regions succeed with consolidating) = P(at least N/2 out of N of cells are stored by honest peers)512

---

**pop** (2024-11-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/oascigil/48/15349_2.png) oascigil:

> Sum(Binom (1 … N/2, N, P(at least one copy to honest peer))

What is that? You know? you can use Latex here. The parentheses don’t even match.

![](https://ethresear.ch/user_avatar/ethresear.ch/oascigil/48/15349_2.png) oascigil:

> P(all 512 row/column regions succeed with consolidating) = P(at least N/2 out of N of cells are stored by honest peers)512

Why do you take it to the power of 512? I don’t understand.

---

![](https://ethresear.ch/user_avatar/ethresear.ch/oascigil/48/15349_2.png) oascigil:

> Upon receiving its seed cells for the assigned row/column, a VN communicates with other VNs in its region to consolidate the entire row/column.

This post has very little detail about consolidations, while I think it’s a big thing since I think there would be a lot of bandwidth consumption there. Could you explain exactly how it works? I think the current explanation is very vague. The reasons why it’s vague are as follows:

1. “communicates” - like what is communicated exactly? you mean forwarding the received cells to other peers?. I think it should be more specific.
2. “other peers” - which peers exactly? you mean every other peer? or every other peers that are supposed to receive some cells in the same row/column? or not every other peer but only some peers that are supposed to receives some cells in the same row/column and expect them to forward further?

If those peers already received the cells from some other peer, do you still need to foward it to those peers? If not, how do you know they already receive?

There are many things that need to be explained and defined for consolidations.

I would say **we need to calculate the bandwidth usage by each VN (including from consolidations)** because the whole point of DAS is to reduce the bandwidth consumption. When we get the number, we can tell how useful the construction is.

If we aren’t able to calculate it yet, it means it’s still vague and the detail is needed.

Please ignore the bandwidth usage calculation that I made previously since I didn’t take the consolidations into account.

![](https://ethresear.ch/user_avatar/ethresear.ch/oascigil/48/15349_2.png) oascigil:

> We are unsure why you think c = 200 or even c = 100 is necessary

I didn’t take consolidations into account. So yes, if we take the consolidation into account, c = 100 is unnecessary.

I will wait for your detailed explanation of consolidations and how much is the bandwidth consumption and we can discuss further from that.

---

**oascigil** (2025-02-12):

Sorry for the very late response. Here is a latex version of the above post.

The total number of cells is given by N=512. The malicious ratios considered are:  F \in \{0.6, 0.7, 0.8, 0.9\}

For a given number of copies per cell, c, the probability that at least one copy of a cell is assigned to an honest peer is:

P_{\text{honest}} = 1 - F^c

The probability that at least ( \frac{N}{2} ) out of N cells are stored by honest peers is given by:

P_{\text{half}} = 1 - \sum_{k=0}^{N/2 - 1} \binom{N}{k} (P_{\text{honest}})^k (1 - P_{\text{honest}})^{N-k}

where  P_{\text{honest}} = 1 - F^c .

Finally, the probability that all N=512 row/column regions successfully consolidate is:

P_{\text{total}} = \left( P_{\text{half}} \right)^{512}

