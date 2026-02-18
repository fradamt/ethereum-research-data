---
source: ethresearch
topic_id: 18399
title: Testing path for a gas limit increase
author: parithosh
date: "2024-01-18"
category: Consensus
tags: []
url: https://ethresear.ch/t/testing-path-for-a-gas-limit-increase/18399
views: 2856
likes: 30
posts_count: 7
---

# Testing path for a gas limit increase

# Testing path for a potential gas limit increase

Thanks to [Barnabé](https://twitter.com/barnabemonnot), [Andrew](https://twitter.com/Savid), [Sam](https://twitter.com/samcmAU) and [Marius](https://twitter.com/vdWijden) for the review and discussions

## Introduction

As the topic of Gas limit increase has surfaced recently, I thought I’d spend some time compiling thoughts from various places and try to enumerate a path forward to increase the limit safely.

In its current form, Ethereum consists of 2 layers, the Execution Layer (EL) that is responsible for handling transactions, state, history, building blocks and the Consensus Layer (CL) that is responsible for consensus. The CL consensus engine is currently a combination of Casper the Friendly Finality Gadget (Casper FFG) and the LMD-GHOST fork choice algorithm. This consensus engine is strictly time dependent and introduces a concept of Slots and Epochs, there are tasks that need to be completed at certain periodic intervals by the validators. Two such tasks that we will consider are called Block proposals and Attestations. A block proposal specifies what the assigned validator thinks the canonical slot needs to be and the attestation specifies the vote of each validator for said proposed slot. Each interval (slot) is 12 seconds long and the [specification](https://github.com/ethereum/consensus-specs/blob/b2f2102dad0cd8b28a657244e645e0df1c0d246a/specs/phase0/validator.md#attesting) says that the validator must attest as soon as they see a valid block or at the 4s mark into the slot. This introduces the concept of a deadline for the attestation task, i.e, under ideal conditions we’d want every validator on the network to attest to the canonical slot with a valid block before the 4s mark.

On receiving information about the proposed block, the CL triggers a engineAPI call called `forkchoiceUpdated`(fcu). If the EL has all the data it requires, then it verifies the block and responds with `VALID`. Until this verification is complete, the CL cannot proceed with its duties, implying that the verification needs to ideally be complete within the 4s mark. There are a couple of variables at play with regards to this verification time: It depends on when the CL sends it the `fcu`, how big the block being verified is and if the EL already has all the data required for verification. A higher gas limit would be one factor that affects this verification time.

The presence of Blobs also adds some complexity to this systems as a slot isn’t valid until all the blobs proposed in it are fetched from the network and verified. The CLs do this in parallel, i.e once the block is received the `fcu` is issued, the block is then imported into forkchoice once the blobs have been deemed valid and available. The trigger for both tasks are handled by the CL, since they are done in parallel we would need to analyze which aspect takes the longest. If the blob fetch and verification takes longer, then the assumption is that on this one metric we can potentially afford to increase the EL gas limit. If the block verification takes longer, then on this one metric alone we can potentially increase the blob count. However, we do need to ensure that in any case the tasks are complete (ideally) in under 4s across the network.

While we mainly spoke about CL considerations till this point, the EL also has some independent considerations. These mainly have to do with the size of the state, the access duration and the growth for the foreseeable future. [Péter](https://twitter.com/peter_szilagyi) from the Geth team articulates these arguments in depth in his talk [here](https://youtu.be/Cmuz_Xn_YJw?si=cgUxijQ147gAv3xZ). The arguments largely boil down to increasing difficulty in managing access to data as time passes. We would need to collect metrics as to the rate of growth per month of the state at the current gas limit and attempt to predict the rate of growth with an increased gas limit.

Generalizing the constraints, we can classify them under two categories:

- Bust constraints: For a given slot we want the processing time to always be lower than the worst case the network can handle
- Long term constraints: We want to be sure that with certain network parameters the clients are viable for the forseeable future

So we need to ensure that we collect metrics for both types of constraints before we make any decision on changing the gas limits.

TLDR: There’s a time budget we have, gas limit factors into this time budget. Consider the CL, EL and combined node perspectives.

## Testing

We currently have 5 supported CLs and 5 supported ELs. Since there is no limitation on what combination users can run, we need to ensure that any gas limit decisions would perform well in any of these 25 combinations.

We’d ideally like to start testing by figuring out interesting metrics. Since the gas change would affect various layers of the stack, we’d likely need to monitor:

- Client performance related to attestation and committee duties
- Missed slots/reorg rates
- iops per node
- rate of account growth
- rate of trie size growth per client
- disk usage growth per node
- RAM/CPU increase per node

… at a bare minimum. There are probably a lot more metrics that EL client devs would be interested in surfacing as well.

It would be prudent to start with local testing and then graduate to shadowforks (Which would represent more real network loads).

### Initial Local testing

My suggestion would be to use [kurtosis](https://github.com/kurtosis-tech/ethereum-package) as a local testing tool to orchestrate test networks with arbitrary ELs and CLs as participants. Kurtosis supports both a Docker and Kubernetes backend, Kubernetes would be the preferred approach here as we can isolate a EL/CL pair from the effects of others on the same host. One has to be careful to use local volumes, as network volumes introduce their own latency complications.

Kurtosis supports the ability to pass a participant arbitrary flags, this is useful as the ELs allow you to override the gas limit with a runtime flag (Flags similar to `--miner.gaslimit`). Some CLs contain flags similar to `--suggested-gas-limit` on the validator, others might need a value change and recompilation. (Hint, if you have a branch with changes and need a Dockerfile, the ethpandaops github action can build it for you [here](https://github.com/ethpandaops/eth-client-docker-image-builder/)).

Once you have the flags/images and kurtosis config ready, you can spin up a new network with `kurtosis` and specify the tooling it should spin up as well (Such as `tx_spammer` and `goomy_blob`). This tooling will ensure that your blocks are being filled up for the test.

Running the kurtosis run with `mev_mode: full` would also spin up the entire mev workflow, allowing us to analyse the delays it adds to our expectations. Note that the default mev workflow that is spun up is purely greedy, this may not be the strategy run in mainnet by relays.

This would also be a good time to figure out the data collection and metrics aspects. While some/most metrics are available via the clients themselves, they might not be standard or visible in a single dashboard. It might be easier to fetch the data via an [exporter](https://github.com/ethpandaops/ethereum-metrics-exporter) or from the host directly via [node exporter](https://github.com/prometheus/node_exporter) or similar tools. Ideally whatever metric collection approach is chosen, is independent of kubernetes - as we currently don’t support shadowforking with kurtosis on kubernetes. The shadowforks are usually instrumented with ansible on various hosts.

### Shadowforks

Once the gas limit change has been vetted on local tests and we have a better idea of what kind of metrics are needed, we can graduate to shadowforks. These networks fork away from the canonical chain, so they inherit the entire chain and for a limited duration continue to import the transaction load. This would mean that we could genuinely see how the network would perform with a higher gas limit.

Shadowforks currently aren’t automated in kurtosis, the work for that is still underway. The best approach would be to follow [this guide](https://notes.ethereum.org/@parithosh/shadowfork-tutorial). The base testnet functionality can be found [here](https://github.com/ethpandaops/template-devnets), This will allow you to spin up nodes on a cloud provider and deploy a network onto them. Most of the shadowfork functionality is performed with various ansible playbooks found [here](https://github.com/ethpandaops/dencun-devnets/blob/907a885b12bf6ac09d76f50a5f959607913ecbaa/ansible/shadowfork.yaml).

We also support running the entire mev workflow with ansible, this can be found [here](https://github.com/ethpandaops/ansible-collection-general/tree/master/roles/mev_relay). MEV adds a lot of changes to the default pathways, so it would be prudent to test this on the shadowfork as well.

## Conclusion

This two step approach would allow us to collect data in an agile manner and to vet our proposed changes on a production-like network. This however would still not include some externalities like MEV-relay strategies and DVT clusters. It also wouldn’t include the edge case of an attacker finding a transaction that can trigger extremely slow evm execution. But this systematic approach would lead to a reproducible system we can use for future discussion of gas limit increases as well.

## Replies

**MicahZoltu** (2024-01-18):

I’m generally a fan of the approach you are proposing here of setting constraints, gathering data, and adjusting gas limit such that we remain within those constraints.  I think this is a very wise and pragmatic approach to the problem.

![](https://ethresear.ch/user_avatar/ethresear.ch/parithosh/48/11805_2.png) parithosh:

> Long term constraints: We want to be sure that with certain network parameters the clients are viable for the forseeable future

My primary concern is that it is going to be impossible to get everyone to agree on what “viable” means here.  I have come to appreciate that the gas limit debate boils down to a disagreement in who should be able to run a node.  Which of these people should be able to run an Ethereum node trustlessly?

1. Somenoe with a 10 year old flip phone?
2. Someone with a high end cell phone and great network connectivity?
3. Someone with a consumer daily driver laptop?
4. Someone with a gaming rig?
5. Someone with a low cost dedicated server in their home?
6. Someone with a dedicated server in a datacenter?
7. Someone with a datacenter?

Solana fills the market need for (7), so we probably want to fill the market need for one of the others.  (1) and (2) are probably too far out of reach for Ethereum at this point and should be left to new startup chains with clever solutions to problems (like a fully ZK blockchain).  The fighting is all around those middle ones (3-6), with a huge range of opinions and beliefs that are often in direct opposition to each other.

It may be valuable to create the framework you have described, and then try to fill in the “viable” definition after as it will hopefully make it more clear what this debate is really about.  I do worry that it may be impossible to actually fill that definition in.

---

**parithosh** (2024-01-18):

Yeah agreed, seems like an answer to that definition would also be required for the Verkle transition discussions. We can only do the transition at the speed supported by the slowest validator we wish to support.

The current working assumption has been a rock5b with an SSD big enough in it, but that’s just an opinionated decision and not one that has gone through any sort of real discussion.

---

**Polynya** (2024-01-18):

As a data point, it’s now possible to buy a laptop with 32 GB RAM and 2 TB NVMe SSD for [$500 or less](https://ethresear.ch/t/testing-path-for-a-gas-limit-increase/18399). [2 TB PCIe 4.0 NVMe SSDs are available for under $100](https://www.newegg.com/p/pl?d=2+TB+SSD+NVMe) for those looking to upgrade. I believe this is a reasonable spec to target, and price-equivalent to slower 500 GB SSDs in 2021. The main limiting factor will probably be bandwidth, which varies a lot globally, but anecdotally 100 Mbps+ fiber is widely available throughout most of Asia.

PS: As a possibly more controversial side note, I believe gas limits should be forward-looking. E.g. if there’s a high probability of verkle trees leading to an X% increase in gas limits, some fraction of X% can start being “priced in” before it ships. (Emphasis high probability, obviously)

---

**benaadams** (2024-01-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> My primary concern is that it is going to be impossible to get everyone to agree on what “viable” means here.

1. Pre-merge a “validator” that wanted to remain competitive would need to upgrade their GPU annually or bi-annually depending if they bought a top of the line or not.
2. At EIP-1559 a $500 2TB NVMe SSD was recommended.
3. At Merge the cost from requirement to have and on going costs to upgrade the GPU went away.
4. Now that same SSD drive is $139

So the hardware outlay to run a “validator” have decreased radically; dropping 72% just on the drive without even factoring in the GPU savings or how much it is in real-terms as inflation has been high during this time.

- You can now buy a 4TB SAMSUNG 990 PRO SSD for $319; which is double the space for 25% less than the price of a recommended drive at the time of EIP-1559
- For the low end of the market are already proposed changes for this segement (eip-4444, Verkle => Light Clients)
- Doubling the recommended storage from 2TB → 4TB is still a lower outlay than the costs at EIP-1559

The advance of technology is driving down the costs significantly; and every client has been improving performance with each release. As well as the low-end being catered for by verkles and eip-4444.

So question is how are we taking advantage of this technological boon; considering the low-end market is already covered by changes already in the pipeline (e.g. Verkle) and the most significant diskspace contributor is also already covered (e.g. eip-4444)?

Factoring in inflation the EIP-1559 drive outlay is now $600; which at a push can get you an 8TB NVMe SSD (though is probably a bad one); with more quailty coming in around $800.

What should we do for full-nodes? (currently recommened at 2TB)

1. 2TB: Follow hardware costs to $0; people bought some hardware 3 years ago why should they ever need to upgrade?
2. 4TB: Maintain base hardware pricing, or even reduce a little.
3. 8TB: Increase the base hardware; as light-clients should be supported in medium term (not significantly more, will take a while to get there driving costs down)

---

**MicahZoltu** (2024-01-19):

I don’t think this thread is the right place to debate what “viable” means, but I did want to drop a couple of responses early on in case it turns into that:

![](https://ethresear.ch/user_avatar/ethresear.ch/benaadams/48/14892_2.png) benaadams:

> So the hardware outlay to run a “validator” have decreased radically; dropping 72% just on the drive without even factoring in the GPU savings or how much it is in real-terms as inflation has been high during this time.

Not everyone agrees that validators are who we should care about.  Many people believe that *users* are who we should care about, and whether or not they can trustlessly interact with Ethereum in a censorship resistant way.  Step one in figuring out what “viable” means is, as I mentioned, figuring out what demographic we are targeting and that includes what class of users.

![](https://ethresear.ch/user_avatar/ethresear.ch/benaadams/48/14892_2.png) benaadams:

> considering the low-end market is already covered by changes already in the pipeline (e.g. Verkle)

We should not count our chickens before they hatch.  Until verkle trees, 4444, state expiry, light clients, portal network, etc. actually exist and are usable we should operate as though they don’t exist and may never exist.  We must be resilient to state level censorship, and that means we should design things such that if development suddenly halts, the chain still works as well as it has been for as long as possible.  So we can’t be taking on debt in hopes we’ll pay it off in the future.

---

**Spore-Druid-Bray** (2024-01-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/benaadams/48/14892_2.png) benaadams:

> Pre-merge a “validator” that wanted to remain competitive would need to upgrade their GPU annually or bi-annually depending if they bought a top of the line or not.

The most important level of participation to target is a non-consensus full node (this was the main consideration pre-merge), since trustless participation is in some sense foundational to meaningful censorship resistance. A non-consensus full node is verifying all consensus layer and execution layer activity it has access to, but it doesn’t participate in consensus or block construction.

Realistically we also need to cover other node duties like block propagation and make allowances for consensus participation (even including aggregating signatures and generating proofs) but these are downstream of running a non-consensus full node. The same goes for economic implications, for example the community feels comfortable to exclude (flashbots) Searcher hardware (for finding MEV and computing efficient block contents) from the relevant barrier to participate.

[I don’t have relevant feedback for the proposed testing path]

I like Parithosh’s discussion of response times for consensus participants.

I’d like to mention a few other cases where “time” could show up:

1. Running a non-conensus full node with the full might of a high end laptop, but only for 6 hours a day (every day).
2. Your cheap desktop PC’s non-consensus full (or even validator) node falling behind after being turned off for several weeks each year while you’re away.
3. Syncing a full node (with only the blocks) from the last special point in time (genesis, a fork, a weak subjectivity period).
4. Quickly catching back up after a network-wide catastrophe (eg mass syncing of Parity clients in the Shanghai attacks, or Ethereum Classic miners facing (ETC’s) Geth’s 256ish block reorg depth limit during a 51% double spend attack).

In each of these cases we have different urgencies and different distances to cover. To me the two worth really paying attention to are [1] and [4]. Similar to [4], under PoW if there were consensus instability (such as during a 51% attack) you could reasonably expect to need to track two fairly long chain segments simultaneously which would increase hardware demands. I don’t know if that’s a realistic issue under PoS, but it’d affect both safe RAM requirements and block processing times.

I agree with Micah that we should let someone else should worry about 10 year old flip phones (or even IOT devices) and high end end cell phones as “viable” hardware targets, however personally I think until the crypto ecosystem changes substantially Ethereum should err on the smaller side (as in closer to 2.5 or 3.0 on Micah’s scale than 5.5 or 6). The rationale being that we don’t *yet* have any real alternatives to Ethereum in terms of its position within the crypto ecosystem and within civilisation as a whole.

