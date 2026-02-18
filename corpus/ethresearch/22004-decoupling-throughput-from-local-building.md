---
source: ethresearch
topic_id: 22004
title: Decoupling throughput from local building
author: barnabe
date: "2025-03-25"
category: Proof-of-Stake > Economics
tags: [protocol-research-call]
url: https://ethresear.ch/t/decoupling-throughput-from-local-building/22004
views: 2384
likes: 49
posts_count: 14
---

# Decoupling throughput from local building

*Many thanks to Alex Stokes, Ansgar Dietrichs, Carl Beekhuizen, Caspar Schwarz-Schilling, Dankrad Feist, Data Always, Drew van der Werff, Eric Siu, Francesco d’Amato, Jihoon Song, Julian Ma, Justin Drake, Ladislaus von Daniels, Mike Neuder, Nixo, Oisín Kyne, Parithosh Jayanthi, Potuz, Sacha Saint-Leger, Terence Tsao, Thomas Thiery, Tim Beiko, Toni Wahrstätter for their comments and reviews (these are not endorsements). I bothered a lot of people lol.*

---

There are important conversations the Ethereum community should have in the next months: What to make of *local building*? What is the future of the *validator set*? How to *scale the L1*? How to *scale the blobs* so the L2s can scale?

To make these decisions, we need to clarify what the goals of Ethereum are, and what are means for us to achieve goals such as censorship-resistance, security (e.g., safety + liveness), scale or verifiability. Given recent advances in protocol R&D, we want to engage in efforts to explore how these features further the goals of our users and builders.

This note discusses **local building** and asks:

*To scale the L1 and provide more blobs for rollups, should we decouple network throughput from what local builders with minimal hardware achieve, and if so, can we still preserve the good properties that local builders guarantee?*

We propose to curate a wider discussion through writings and open discussions in a new “Protocol research call”. See the [announcement](https://ethereum-magicians.org/t/protocol-research-call/23261?u=barnabe) over at ethereum-magicians! See also “[Paths to SSF revisited](https://ethresear.ch/t/paths-to-ssf-revisited/22052)”, a second post discussing the role of home operators in the consensus layer, also discussed during the Protocol research call #1.

## Protocol roles and service providers

In this note and following, we will be concerned with *protocol roles*, such as *attester* or *builder*, which are functions expected by the protocol to be fulfilled. The party responsible for fulfilling a role is a *service provider*, ultimately represented by a **node** on the Ethereum network. Assigning the right node to the right role is derived from understanding what the system needs to optimise for, and how much various nodes contribute to these objectives given their resources.

[![Validator services map](https://ethresear.ch/uploads/default/optimized/3X/2/a/2a6b33c6260ea443495fabb1667e7674d61307b0_2_690x383.png)Validator services map2830×1572 384 KB](https://ethresear.ch/uploads/default/2a6b33c6260ea443495fabb1667e7674d61307b0)

*A staking node is expected to fulfil the roles above, or may be expected to (the FOCIL role does not currently exist, and is discussed below).*

We want every node on the network meeting certain [hardware requirements](https://github.com/ethereum/EIPs/pull/9270) to always be able to *verify* the availability and validity of Ethereum. [This is a non-negotiable constraint.](https://dankradfeist.de/ethereum/2021/05/20/what-everyone-gets-wrong-about-51percent-attacks.html) A node with *the most basic* resources meeting the hardware requirements may be called a **minimal node**. A node controlling a *validator*—a protocol role bundling the functions of *attester*, *proposer*, *sync committee* and others—is called a **staking node**.

In this note, we discuss how to tap into the [asymmetry](https://vitalik.eth.limo/general/2021/12/06/endgame.html) between verifying and building. *Building* is the act of appending data to the ledger, whether transactions or blobs. *Verifying* is the act of receiving this data and convincing oneself that the data is available (“I know that all of the data published by the builder can be recovered somewhere on the network”) and valid (“The data follows protocol rules, e.g., transactions included in blocks must be valid”). *Building* supplies **throughput** to the network, i.e., supplies the gas and blobs delivered per unit of time. *Verifying* limits this throughput, to the quantity that can be verified by nodes before they must perform other tasks such as attesting.

[![External building](https://ethresear.ch/uploads/default/optimized/3X/e/f/efd0d2e57f56cbbab599ae0a5741f15312b1eb0e_2_690x382.jpeg)External building1920×1063 76.4 KB](https://ethresear.ch/uploads/default/efd0d2e57f56cbbab599ae0a5741f15312b1eb0e)

*The builder role was mostly externalised by staking nodes to* **external building nodes**.

## The asymmetry of verifying and building

Today, the hardware requirements are set such that minimal nodes are always able to verify the chain fully, and perform validating duties including producing FFG attestations for finalizing the chain, and LMD-GHOST attestations for updating the fork-choice rule. The target throughput of the chain is set such that minimal nodes are able to supply this throughput entirely, i.e., make blocks delivering up to the target throughput (and its corresponding limit).

[![Coupled throughput](https://ethresear.ch/uploads/default/optimized/3X/2/9/294fd3e7df32c2c95bbe8bf12c316f9f089f5db1_2_690x449.jpeg)Coupled throughput2080×1356 138 KB](https://ethresear.ch/uploads/default/294fd3e7df32c2c95bbe8bf12c316f9f089f5db1)

*Minimal nodes satisfying precisely the minimum validating requirements are able to run a validator.*

Yet in more and more places, we have a strict asymmetry between *verifying* and *building*. There is a potential future, where a node that has the most basic resources and still meets hardware requirements stops focusing on anything related to building and just verifies. The builder in this model would handle requirements around significant throughput potentially required to scale blocks and blobs.

With PeerDAS for instance, a builder with 8x resources could create an [8x larger block](https://hackmd.io/@manunalepa/peerDAS/https%3A%2F%2Fhackmd.io%2Fe3UGeZ7cS92uk8b1SeVSyw#WithPeerDAS) that a 1x attesting node fully verifies with a fraction of the builder’s resources. While the builder must upload the blobs themselves, 8x more data in the worst case, (if minimal attesting nodes have not received the blobs in their own mempools previously), a minimal attesting node must only download 1x the amount to verify availability and perform its duties properly. We could then allow building nodes with strictly higher upload bandwidth to disseminate this data, while attesting nodes require only a fraction of this bandwidth to verify that the data is available and gossip it to their peers.

Another example of where we expect a large asymmetry will occur when the L1 EVM is snarkified. Then, the major cost of building a block will consist in generating a proof of its validity, while every other node on the network needs only ensure that the block data is available (you can think of dumping the block in a blob, with availability checks becoming even lighter as we move [towards full DAS](https://ethresear.ch/t/fulldas-towards-massive-scalability-with-32mb-blocks-and-beyond/19529)) and making a constant-time computation to verify the proof of validity. This future [may be much closer than we think](https://ethproofs.org/), and as a thought experiment, should we make nothing of the massive resource asymmetry between building a zkEVM-proven block and verifying it? This should clue us in to the fact that asymmetries are scaling opportunities, and lead us to ask whether they are to be acted upon in more immediate places, such as scaling blob throughput.

[![Decoupled throughput](https://ethresear.ch/uploads/default/optimized/3X/3/e/3e3bcf73391c87ef56cfcfa51b79055dde56b151_2_690x448.jpeg)Decoupled throughput1920×1249 75.9 KB](https://ethresear.ch/uploads/default/3e3bcf73391c87ef56cfcfa51b79055dde56b151)

*While we have a broad base of many staking nodes performing the attestation service, there are fewer, better-resourced (in compute, bandwidth, or order flow) building nodes in the network. Could the target throughput be increased given the existence of these building nodes?*

## Three network properties to achieve

So far, we have kept network throughput to a level that *all* staking nodes could achieve while performing the building role. We spell out three network properties that we wish to satisfy, guiding our hand in designing network architecture:

1. Censorship-resistance of the network: We want any fee-paying transaction to be included given that throughput is available for this transaction to be included.
2. Target throughput achievement: Suppose the Ethereum network sets some target throughput, by setting the EIP-1559 gas and EIP-4844 blob targets. We may ignore the reasons why this amount of throughput was set, we just take as given that there is some target that is now given to us. Can we be satisfied with high probability that the network will achieve this throughput, without leading to bad outcomes such as an implicit increase in minimal hardware requirements?
3. Block production liveness: No single party or colluding group of parties should be able to halt the progression of the chain, e.g., by being the only parties able to deliver a valid block to the network.

When a staking node does not delegate its building function to a separate external builder, we call the node a *local builder*. The presence of local builders buys us a lot in terms of the three network properties:

1. Censorship-resistance of the network: Local builders are part of the validator set, which is assumed to be decentralised enough to provide good censorship-resistance. When external builders censor, assuming that some local builders keep producing blocks, the chain preserves some (possibly lower) censorship-resistance.
2. Target throughput achievement: Today, throughput is set such that local builders are always able to achieve it, so we have a pretty good guarantee that it will be achieved, given that every external builder has at least equal capabilities.
3. Block production liveness: A local builder can always make a valid block, so we are also confident that there will always be a builder (either local or external) who is able to progress the chain.

## Effects of decoupling throughput from local builders

What would happen if network throughput was now set to a level higher than minimal local builders could achieve? The first property may be the most hurt, as local builders could not be able to provide throughput at the target quantity. Yet this throughput may be recovered by external builders, as EIP-1559 targets and achieves some fixed amount. It is notable that already today, local builders are on average unable to provide throughput at the current target, given the depletion of the public mempool in favour of private pools (see [analysis by Data_Always](https://x.com/Data_Always/status/1882873599637467562)). The two remaining properties would not be more hurt under this hypothetical scenario than today, as local builders under a higher network throughput could still propose blocks at today’s throughput, guaranteeing minimal liveness, and include potentially censored transactions at a lower throughput.

We may still find this situation uncomfortable: If we wish for local builders to remain economically competitive with externally-building nodes, we should ask them to delegate their building function. But if we ask them to do so, we may not feel comfortable with the quality of any of the three properties above. So if we want to decouple network throughput from what can be provided by local builders, we must ensure that we still achieve these three properties. We discuss each of them in the following sections.

### Censorship-resistance of the network

With [EIP-7805: Fork-choice enforced Inclusion Lists (FOCIL)](https://eips.ethereum.org/EIPS/eip-7805), we believe that the censorship-resistance property is essentially guaranteed at network level, in the sense that formerly-locally-building validators can achieve the provision of at least as much (but in practice much more) censorship-resistance through FOCIL than with local building.

The FOCIL mechanism selects 16 new *includers* from the validator set every slot, and each includer is able to propose a list of transactions which must conditionally be included in the block proposed for this slot. These inclusion lists constrain the proposer of the current slot, or their chosen builder, preventing them from arbitrarily excluding transactions from the network.

[![FOCIL](https://ethresear.ch/uploads/default/optimized/3X/9/6/9656835b8364da222fdd3e79d4b6dea7089c9110_2_328x250.png)FOCIL1000×760 196 KB](https://ethresear.ch/uploads/default/9656835b8364da222fdd3e79d4b6dea7089c9110)

*FOCIL chooses 16 includers every slot to impose constraints on the block-building process.*

FOCIL allows staking nodes who decide not to be local builders anymore, delegating their building function to the external builder market, to still participate in the provision of censorship-resistance. Local builders do not need to pick between locally building to provide censorship-resistance or using external builders to maximise their rewards, they can do both.

FOCIL is not currently deployed, and we are still required to choose a design that extends FOCIL to blobs.

### Target throughput achievement

The target network throughput must still be carefully chosen by the network in order to prevent builders from delivering blocks that become increasingly hard to verify by minimal nodes. As a thought experiment, could we simply remove the gas limit and let the builder (either local or external) decide the size of the block they want to produce? We would have two issues:

1. The builder may output blocks that can barely be verified by minimal nodes. As long as the block receives sufficient attestations, it may be enough for it to be part of the canonical chain. But it could lead to an arms race where the requirements made on minimal nodes become no longer enough to attest properly, increasing the expectations on minimal nodes to beef up their hardware beyond the minimal specs. Note that zkEVMs for instance could alleviate this, in that any gas supplied by the builder, as long as it also comes with a proof, incurs a constant verification cost on the verifying nodes. This may not hold for blobs and data availability, for which throughput increases must always be matched with increasing verification resources in the aggregate.
2. There is a tragedy of the commons where some externalities of a large block are only felt over time, e.g., state growth or node syncing time.

I may be able to deliver a very large block now, that gets enough attestations, but my doing so increases the state size for everyone in the future, and makes it harder to achieve a consistent throughput over time. Note that stateless architectures may partially alleviate this issue.
3. By delivering bigger blocks, I would also increase the sync time necessary for new nodes to catch up to the head of the chain. Again, a combination of validity proofs and statelessness can alleviate this issue.

### Block production liveness

Relying on an external network means that its failures become the system’s failures. Inherent to the nature of delegation, we can never entirely control the actions of the building “agents” chosen by our staking node “[principals](https://en.wikipedia.org/wiki/Principal%E2%80%93agent_problem)”, or prevent them from failing. But ultimately, [staking nodes themselves are agents to the protocol](https://barnabe.substack.com/p/seeing-like-a-protocol), and could fail themselves, or miss the mark in providing what the protocol seeks to supply. So the question we should ask is how far can we go and how far are we willing to go to mitigate these risks?

There are two broad approaches to obtain these mitigations: *Improving out-of-protocol infrastructure* or *adding new features in-protocol*. [Proposer-Builder Separation](https://barnabe.substack.com/p/pbs) (PBS) is instantiated today by out-of-protocol [MEV-Boost](https://boost.flashbots.net/) and [Commit-Boost](https://github.com/Commit-Boost), with relays taking on the role of trust anchors to access the market. PBS would be strengthened with in-protocol [EIP-7732: Enshrined Proposer-Builder Separation](https://eips.ethereum.org/EIPS/eip-7732) (ePBS). Using ePBS, we can provide better guarantees for the market participants, i.e., the staking nodes on one side and the external builders on the other side, as the protocol guarantees the fair exchange between the two.

To understand what is needed, we must understand the risks and failures of delegating the building role. We can never completely rule out the bad case of a “timeout” liveness failure, where the builder does not deliver the block even after a contract is struck between a staking node and the builder. We may have more systemic risks, where the interface to the external market fails. And we may have a cartel of builders refusing to build any block for anyone, unless the staking nodes paid them some sort of extortion rent.

We now give some arguments to guide our hand in choosing the required arsenal of defences:

- Staking nodes can adapt their behaviour to repeated failures of the external market, e.g., by a falling back on local building via a circuit breaker.
- We can ensure that if a deal is struck and the builder fails to deliver, the payment still proceeds. There are multiple ways to guarantee this with in-protocol solutions. If the relay itself doesn’t fail, some optimistic relays also require an escrow payment from the builder, to compensate for failures of the builder to deliver as promised.
- We could take the view that liveness of the block construction process assumes a particular realisation of the user demand, and strictly ask whether given a particular set of transactions available to be built, some building party will take up the job. In other words, we may care about the existence of any one single builder who can do at least as well as the staking node itself, and if the staking node does not receive most user transactions (who may prefer to transit via private pools), decide that it is not an issue with the block production liveness. Still, order flow remains a determinant factor in the success of builders. A market dominated by few entrenched entities could potentially discourage the entry of more participants, even as temporary fallbacks when liveness of the few dominant entities is in doubt. The presence of neutral relays increases the entry points into the market, favouring such fallbacks. Additionally, with the emergence of new protocols such as BuilderNet, we observe more innovation in the builder market towards neutral infrastructure, at least in its idealised form.
- There are ways to harden the current out-of-protocol infrastructure, e.g., ensuring sufficient diversity with both MEV-Boost and Commit-Boost, which are both neutral pieces of software, or improving our circuit-breaker and fallback routines to minimise liveness risk should failures occur somewhere along the chain.
- There is a true worst case where only a few nodes in the world can build the block required by the network. This is somewhat theoretical, as there are not many cases where a staking node could be forced into a position where only a few parties could satisfy the building requirements imposed on the node. A strawman is imagining FOCIL outputting a very large set of transactions and blobs to include, perhaps under a zkEVM regime where the block must additionally receive a validity proof. If the staking node itself cannot build this block themselves (and this is entirely possible if network throughput is decoupled from local builder capabilities), the staking node will be required to rely on an external builder. We should ensure that this reliance is as wide as possible, i.e., that there always exists a builder ready to deliver this block. This is not the case if we can find ourselves in a situation where only super computer-sized nodes are able to deliver, for some reason, but this can be easily mitigated by setting a network throughput limit to a level that guarantees a wide enough market, even if this limit exceeds the capabilities of local builders.
- Going in-protocol is costly, in added complexity to the protocol mainly, especially on the path to reducing slot times and changing the consensus mechanism towards SSF. There are also questions regarding the future-proofness of any single mechanism given alternative proposals such as Attester-Proposer Separation. We typically want to have in protocol the features that require honest majority, e.g., the consensus mechanism, getting the full force of a large set of participants to bear on the safekeeping of this property. Meanwhile, obtaining a valid block from a builder requires a 1-out-of-N honesty assumption, as a single builder needs to be live to perform the service at the moment it is required. Given the 1-of-N honesty assumption, relying only on out-of-protocol solutions for delegating block building could be reasonable.

There is no easy answer on which combination of solutions to deploy here, especially as the argument for ePBS is not solely about hardening the exchange between staking nodes and builders, but also about scaling by providing better pipelining (note that for the scaling argument, it should be [considered in the context](https://ethresear.ch/t/delayed-execution-design-tradeoffs/21877) of alternative and/or complementary approaches such as [delayed execution](https://ethresear.ch/t/delayed-execution-and-skipped-transactions/21677), a topic for a future note/call).

### What we should talk about

Overall, there are two independent discussions to have:

1. Deciding whether to decouple network throughput from what local builders can achieve. Arguments were made above, discussing how the three properties fare in this context, and how they could be improved with new mechanisms such as FOCIL.
2. Deciding how to ensure block production liveness. While this is a wide spectrum, we see broadly two ways to move forward, which are not mutually exclusive:

Doing more in-protocol: By deploying protocol infrastructure such as ePBS, we strengthen access to the external builder market.
3. Improving out-of-protocol options: Perhaps we are happy enough with keeping this builder interface out of the protocol, and letting staking nodes decide on their approach.

Local building is a means of obtaining liveness of the block production service, as well as censorship-resistance. Local building is also a constraint on throughput, if we decide to couple our throughput to the highest level that can be provided by the worst nodes on the network. This is a reasonable choice if local building is our *only* tool to get liveness of blocks as well as censorship-resistance. But if it is not the only tool, or the best one, we should ask ourselves: Could we move the network throughput beyond what local builders are able to provide, *as long as all nodes remain able to sustainably verify the chain at this throughput*? What changes or improvements would we need to make in order to feel comfortable with that demand?

---

*See also [a recent talk](https://youtu.be/595CmPyzFJ0?si=1eaG-6fO7A9_pW9L&t=3958) on this topic.*

## Replies

**come-maiz** (2025-03-25):

I want to gesture towards one more layer. To explore and design to make this layer appear.

A solo node building locally is very limited. I know it’s important to keep it as one of the possible configurations, and these solo nodes can be responsible for important properties of the network. Now having that as a base, we can do so much more.

I imagine a clan with 10 small nodes, each of the nodes is somewhat cheap and somewhat unreliable. In this clan they trust each other, they are in geographic proximity, and they have ways to make decisions. They connect to 1 medium node, stewarded by all of them together. The relation of these 10 small nodes connected to this 1 medium node in a grounded geography can be very powerful, resilient, and interesting. Together they can serve 1000 light nodes that are within range. They can relate with other medium nodes while keeping their own ways and their sovereignty, providing censorship-resistance.

Then the throughput can be anchored to what this medium node can achieve. There will be smaller independent nodes in basements and bigger cloud corporate nodes, that will explore trade-offs and figure out their own paths, letting us to focus on the medium node.

This medium node can be open hardware, open software, reproducible, verifiable, solar powered, connected by satellite, forming a mesh local network, with crypto ASICs for speed, FPGAs for experimentation, TEEs for what cannot be achieved with crypto, with a fair and transparent supply chain, and affordable. We just have to paint the stories about rainbow/delegation/DVT/endgame/attesters/provers/builders/tiers/orderflow/DAS/stateless/bioregion/layer2/liquidstaking/inclusionlists/communitycurrencies/identity/circlesoftrust to spread responsibilities around the medium node.

We can call it ch’ixi.

---

**benaadams** (2025-03-26):

I know what bothers me; if the “local” node is high bandwidth, high resource, it should be able to participate somewhat competitively

Rather than being locked out of building from other externalities and barriers to entry (pure private orderflow being one of these issues)

---

**barnabe** (2025-03-26):

Yes, I think there is a lot of value in recognising the diversity of nodes that we could have and thinking hard about architecting these possibilities. In particular our more binary models of “solo staker” vs “commercial operators” are flawed, and should be revisited. This is the topic of a next post ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**barnabe** (2025-03-26):

I see this as orthogonal to the question above. It is still desirable to have minimal nodes (in fact as minimal as possible) to perform certain roles such as attesting, and possibly desirable to set throughput beyond what these minimal nodes can accomplish. But if you have at home a non-minimal node, you are free to operate as an external builder serving other nodes or as a local builder for yourself.

Whether you are competitive or not depends on your performance as a builder, and the services you provide. Being able to offer better, credible guarantees of service (eg, using cryptography) makes you a better builder. Ensuring that order flow can be obtained without upfront payments or b2b deals seems a net positive for anyone in this scenario.

---

**benaadams** (2025-03-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> Ensuring that order flow can be obtained without upfront payments or b2b deals seems a net positive for anyone in this scenario.

Agreed; though with the difficulty of avoiding the type of mev that reinforces the private orderflow, whether that’s BuilderNet TEE, or encrypted mempools. or something else etc

---

**VaibhavVasdev** (2025-03-28):

In a system where network throughput is decoupled from the capabilities of local builders, how can we architect adaptive fallback mechanisms to ensure that both censorship-resistance and block production liveness are preserved when external builders experience failures or market disruptions?

Specifically, is there scope for designing dynamic incentive structures or adaptive FOCIL configurations that not only encourage local builders to step in when needed but also maintain a competitive and decentralized external builder market?

---

**keyneom** (2025-04-02):

I’m not positive it is actually really feasible. At least I’m not convinced yet. [BuilderNet](https://buildernet.org/docs/flashbots-infra) is probably the closest.

I’ve written here about why I think maintaining local block building is a viable path forward: [Enshrined Native L2s and Stateless Block Building](https://ethresear.ch/t/enshrined-native-l2s-and-stateless-block-building/22079)

---

**CPerezz** (2025-04-03):

Thanks for the post! I liked it.

I have a couple questions wrt the overall directions.

- If we assume that - as you suggest - local builders shouldn’t limit the throughput of the network (and even I don’t like it, it’s true and we should face it).
And if we give block building to an oligopoly effectively (MEV builders). Then, we need to lower the hardware requirements such that we can build the most protocols that help validators to fight/retain a power equilibrium right??.
That being said, would that mean that the focus for PR&D should be working on exactly that? (ie. lowering hardware/bandwidth requirements for validators/IL builders/IL attesters and also creating protocols like FOCIL, Rainbow, Distributed Validators etc… that allow having more validators that have more tools to fight for power equilibrium within the network?).
- Would we double down on externalizing heavy parts of the protocol to these parties? Meaning, now we put block building onto them which will entail holding state, generating proofs(at some point), managing A LOT of compute and bandwidth etc…
Is the plan to keep designing and basing some of the “scaling L1” on the fact that these parties with this much compute power exist? Ie. ZKEVM-based proof of chain validity for instant sync. Hold both cold and hot state in case state-expiry happens to reduce the burden on users and dApps/wallets? etc…
- Final question, is more related to the section

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> What we should talk about

How can we ensure we hear the community and at the same time the decision doesn’t drag for years so that we can figure out what the priorities are and work towards them??.

For instance, this recalls me the different stateless flavours ([see this post from Julian](https://ethresear.ch/t/a-protocol-design-view-on-statelessness/22060)). If we decide we are scaling by having these super-heavy builders. This makes it easier to decide to go towards `weak statelessness` rather than other options.

And also helps scoping how much of a priority things like `state expiry` are.

Thanks, and nice to see discussions like this being triggered. Feels we should decide. As the only clear thing we have now is that we need more blobs. But there’s a lot more to do ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) ![:grin:](https://ethresear.ch/images/emoji/facebook_messenger/grin.png?v=12)

---

**barnabe** (2025-04-03):

Maybe a vague answer, but incentivising FOCIL seems pretty hard in general (ongoing work on this though!), if you want to keep it ~MEV-free. As for local builders, I think the incentive to work as a fallback is there via user transactions paying fees. A user wants service and mediates economic value via their transaction, this should be incentive enough for someone to bother picking it up. If that doesn’t happen, the user can increase their fees, for instance. In my view, this provides quite a bit of robustness already, and moves the system back towards being operational and heal.

---

**barnabe** (2025-04-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> Then, we need to lower the hardware requirements such that we can build the most protocols that help validators to fight/retain a power equilibrium right??.

I’d say this is a tool among many others, and as I argue more in the [other post on SSF](https://ethresear.ch/t/paths-to-ssf-revisited/22052#p-53618-improvements-of-home-operator-economics-9), this is happening anyways: history expiry, zkEVM/statelessness, DAS all converge to making it extremely light to run a validating node. Designing mechanisms such as Light FOCIL is another way to tilt the power more towards the many than the few, and create groups with possibly competing enough incentives to obtain checks and balances, essentially.

That’s the defensive part, but I also think our focus can and should be on the attack. Scale matters to provide as much welfare as possible to our users, so spending time on trying to get as much juice out of our system is also a very worthy use of our time. Fortunately, the two are not in conflict in many places, e.g., zkEVMs make it extremely easy to verify (so high robustness) as well as providing huge scaling benefits. There is still a trade-off between maxing out gas and proving time, relying on fewer parties able to prove this, but at least the efficiency frontier is pushed way forward thanks to this new tech.

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> Would we double down on externalizing heavy parts of the protocol to these parties?

Where sensible and where we have more of these 1-of-N quality of service guarantees (i.e., we only need one party out there to be live and honest to give us good service), there is the opportunity. But it’s not a blank cheque, as detailed in the post above, and it still requires careful calibration. And yeah, [this post](https://ethresear.ch/t/a-protocol-design-view-on-statelessness/22060) by [@Julian](/u/julian) also discusses the question for state management.

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> How can we ensure we hear the community and at the same time the decision doesn’t drag for years so that we can figure out what the priorities are and work towards them??

My view is additive, we should first communicate as clearly as possible the opportunities and risks, gather more understanding and allies and critiques of these ideas, and I don’t imagine that a discrete one-off decision is made saying “ok now we pump it”, but I expect when the topic at hand is “how far can we go with blobs” (for instance), hopefully some of the discussion we had on higher-level principles filters through and is actionable enough to guide the current decision.

I’ll also link to [this slide](https://docs.google.com/presentation/d/1Wny8LwcaZ4Yj5GFWgmalJ9p_jPBDuH_hSJ5W-hcUB3o/edit#slide=id.g34741fac2e3_0_78) of the protocol research call #1, hoping to use these channels to keep the conversation going.

---

**MicahZoltu** (2025-04-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> explore how these features further the goals of our users and builders.

Why do we care about the goals of builders?  Shouldn’t the goals of users be the only thing that matters?

Even within users/builders, not all are created equal.  Should we care about the goals of a Venezualan selling anti CCP propaganda to an Iranian woman, or should we care about the goals of a Silicon Valley chad trading meme coins with his Manhattan doppelganger?

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> We want every node on the network meeting certain hardware requirements to always be able to verify the availability and validity of Ethereum.

The linked EIP was originally meant to outline what pragmatic node requirements are today, not to be a guideline for what node requirements *should* be.  During the authoring of that EIP I provided feedback on this exact subject and it was made clear that this is just a first step of outlining the reality of today and was not intended to be used as some sort of agreed on target of what we *should* be building towards.  I believe I expressed concerns at the time that such a document would likely be viewed as a target, and I am saddened to see that come to pass so quickly.

If that EIP is, in fact, going to be used as a target, then that should be made clear to those who gave feedback so they can appropriately voice concerns, and there should be some process for deciding what the target is beyond a handful of researchers asserting whatever they want.

---

Any discussion about RPC nodes (nodes that users actually interact with in order to interact with the blockchain), seem to be missing here.  DAS doesn’t really help them at all without sharding or some solution for privacy preserving data acquisition from third parties.  I would argue that these nodes are far more important than any other node type in the network.  There are theoretical ways to make these be very small/light, but that needs to be designed into builders/validators and cannot be ignored in any discussion around hardware requirements and throughput.

---

**barnabe** (2025-05-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Why do we care about the goals of builders?

I meant builder in the sense of someone who builds something useful onchain, but I realise now that it’s used for a different meaning in the rest of the text. Philosophically yes, if builders/devs are only mediating user wishes, then we only care about user goals. And if there is a plurality of user goals and we have to choose between which to serve, we need to have different conversations. I’d argue that the points made here are agnostic to which user goals are served.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> The linked EIP was originally meant to outline what pragmatic node requirements are today, not to be a guideline for what node requirements should be.

I see the distinction, I also think here it’s enough to assume that there exists a way to list a pragmatic list of requirements that one calls “a minimal node”. I referred to the hardware EIP because it was the closest to an agreed upon description of what a minimal node looks like today. I don’t assume that the discussion on what the requirements should be today or in the future has happened or terminated conclusively. If it did conclude, then the “minimal node” concept in the post could be prescriptive rather than descriptive.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Any discussion about RPC nodes (nodes that users actually interact with in order to interact with the blockchain), seem to be missing here.

This is right, and it surfaced in other places, e.g., [@parithosh](/u/parithosh) among others recently started looking into making RPCs more robust as throughput increases. This is not something I had in mind when writing, as I was more focused on the consensus-specific functions like attesting. That being said, it’s possible to add in the “model” an extra constraint that “RPC throughput” (sth like the throughput of successful requests served by the network as a whole) should increase in commensurate amounts with “gas/blob throughput”. I feel like some answers are to be found in the larger context of state management/statelessness, which also intersects network topology of builder/validator/light nodes, alluded to in [@CPerezz](/u/cperezz)’s reply too

---

**MicahZoltu** (2025-05-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> This is not something I had in mind when writing, as I was more focused on the consensus-specific functions like attesting.

I strongly suspect that RPC nodes (“light nodes” in Vitalik’s new post) are going to be the bottleneck on almost any changes until such time as we have a fully functional, trustless, distributed state network/marketplace.  Past precedence makes me concerned that if we continue to ignore those nodes in research like what you are doing here then we will again, as we have in the past, push RPC node requirements up and drive home operators even further out, causing even more centralization than we already have.

IMO, any discussion of “how far can we push Ethereum” should focus on the things that are most likely to be bottlenecks, and I just don’t see block building or staking being a bottleneck anytime soon, even if we include home stakers.

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> I don’t assume that the discussion on what the requirements should be today or in the future has happened or terminated conclusively.

I think it is important to get agreement on the target hardware we are building towards prior to trying to optimize for some specific hardware.  While some of the high level abstract concepts may be applicable regardless of the outcome of that discussion (e.g., “heavy nodes” vs “light nodes”), any meaningful R&D is likely to get blocked on that.  Something I worry about, because we have gone down this path in the past, is that people will do a bunch of research as a “mental exercise” or “just to explore what our options would be if we solved the hardware target problem” and then we’ll find ourselves implementing and releasing that research without ever having had the conversation that should have happened before any of that research ever started.

---

By far my biggest concern with this post is the lack of discussion of RPC nodes because I think they are the primary bottleneck, and because they have been historically completely ignored.  My other comments are somewhat less important and I would prefer to focus on that rather than get bogged down debating other points until that is resolved.

