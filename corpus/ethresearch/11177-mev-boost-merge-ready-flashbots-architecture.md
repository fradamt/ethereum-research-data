---
source: ethresearch
topic_id: 11177
title: "MEV-Boost: Merge ready Flashbots Architecture"
author: thegostep
date: "2021-11-04"
category: The Merge
tags: [mev]
url: https://ethresear.ch/t/mev-boost-merge-ready-flashbots-architecture/11177
views: 33690
likes: 53
posts_count: 25
---

# MEV-Boost: Merge ready Flashbots Architecture

# MEV-Boost: Merge ready Flashbots Architecture

*This architecture is a work in progress - the final design will reflect the feedback collected and lessons learned through implementation and can be found on the [mev-boost github repository](https://github.com/flashbots/mev-boost)*

This document outlines the design for a marketplace for block construction (often referred to as block proposer / block builder separation or PBS) compatible with the upcoming Ethereum merge fork. This trust based solution closely resembles the [current Flashbots auction design](https://docs.flashbots.net/flashbots-auction/overview) with modifications to enable solo staker participation without introducing changes to Ethereum consensus. This solution aims to bridge the gap to a [permissionless PBS design](https://ethresear.ch/t/proposer-block-builder-separation-friendly-fee-market-designs/9725) which should be strongly considered for the cleanup fork in order to improve decentralization.

*Thank you to the Flashbots team, EF research team, client implementation teams, and staking service providers for the feedback and countless hours of discussion which went into this document.*

## terminology

- consensus client: the client in charge of ethereum proof of stake consensus
- execution client: the client in charge of ethereum virtual machine execution
- execution payload: a message containing the complete content of an unsigned execution payload to be added into a beacon block
- mev-boost middleware: a new piece of software that sits between the consensus client and the execution client to outsource block construction
- proposer: party which signs and submits a beacon block to the network, often referred to as the validator
- user: a normal ethereum user who sends transactions
- searcher: advanced ethereum user specialized in finding MEV opportunities and sending advanced transaction types like bundles
- builder: party specialized in the construction of ethereum execution payloads using transactions received from users and searchers (trusted by searchers and users for fair inclusion)
- relay: party specialized in DoS protection and networking who validates and routes execution payloads to proposers (trusted by builders for fair routing and by proposers for block validity, accuracy, and data availability)
- escrow: party tasked with providing redundant data availability for proposed execution payloads (trusted by relay for data privacy)

## architecture

This proposed architecture allows validators to outsource the task of block construction to a network of third party block builders. While the validators have the ability to include any payload into the chain, we believe network neutrality and validator revenues are maximized when the validator’s job is limited to selecting the payload which pays them the most ETH.

[![image](https://ethresear.ch/uploads/default/optimized/2X/c/c9fa06a58cabde886291b28dedb643abd968623c_2_690x216.png)image2002×628 33.2 KB](https://ethresear.ch/uploads/default/c9fa06a58cabde886291b28dedb643abd968623c)

The block construction process involves the following steps:

1. Users and searchers send transactions to block builders through the public p2p txpool or through direct channels.
2. Builders construct execution payloads using these transactions as well as header parameters provided by validators. Builders may directly set the validator’s feeRecipient address as the coinbase address of the payload, or the builders may set their own address and include a transaction which transfers to the feeRecipient in the payload.
3. Relays receive execution payloads from builders and verify the validity of the payloads as well as calculate the payload value (amount of ETH paid to the feeRecipient).
4. Escrows receive the full execution payloads from relays to provide data availability.
5. Validators receive execution payload headers from relays (execution payloads stripped of the transaction content). The relay must attach an indication of the payload value to each header. The validator selects the most valuable header, signs the payload, and returns it to the relay and escrow to be propagated to the network.

Note that a single entity may play multiple roles in this system. The roles are labeled separately as they each lend themselves to some level of specialization. For redundancy and decentralization, there should be multiple independent parties competing in each role. In the future, a permissionless PBS design at the consensus level will remove the need for relays and escrows.

On the validator side, this architecture makes use of an independent middleware called MEV-Boost which sits between the consensus client and the execution client. This middleware handles communication with the relays, the profit switching logic for selecting the most valuable payload, and a fallback mechanism to a local execution client if relays get disconnected. Using a middleware instead of direct modification of the consensus clients allows for maintaining each component independently and provide cross client compatibility with minimal changes to the [engine api](https://github.com/ethereum/execution-apis/blob/5966998897f9526e050fd1438026ce8c94c93fb7/src/engine/specification.md).

[![image](https://ethresear.ch/uploads/default/optimized/2X/f/f0ef8cdd3c5b3f28bc7267aa920aac486338c273_2_690x420.png)image1368×834 32.9 KB](https://ethresear.ch/uploads/default/f0ef8cdd3c5b3f28bc7267aa920aac486338c273)

It’s important to note that relays should only be used for payloads during block construction - relays are not meant to be used for other roles performed by the execution clients like verifying blocks for attestations. Validators should always fall back to local payload construction if relays are unavailable.

Since the [execution payload header](https://github.com/ethereum/consensus-specs/blob/a45ee9bf5b1fde766d69e551a6b1a21fe2531734/specs/merge/beacon-chain.md#executionpayloadheader) does not include the transaction content, the risk of validators frontrunning is eliminated. This design allows solo stakers to participate in MEV thus reducing the incentive for economic centralization. However, this design also requires validators to trust the relay to filter invalid payloads, accurately report payload value, and reveal the transaction content once the header is signed. Escrows are introduced to improve data availability by duplicating the transaction content across multiple providers.

Summary:

- Validator trust relay for data availability, payload validity, and payload value accuracy
- Users and searchers trust builders, relays, and escrow for frontrunning protection
- Minimal changes to consensus clients due to middleware architecture
- Adds additional round trip communication between relay and validator to block proposal latency

## discussion points

### client modifications

Flashbots will provide a formal specification similar to the [current MEV-Geth specification](https://docs.flashbots.net/flashbots-auction/miners/mev-geth-spec/v04) and will support client implementation teams to add MEV compatibility for the merge.

The current design requires the following modifications to the consensus client interface:

- enabling the validator to include and sign execution payload header in beacon blocks instead of full execution payloads
- enabling the validator to sign prefixed messages using the staking keys for authentication purposes
- enabling the consensus client to route a signed beacon block back to the middleware instead of attempting to send to the network
- enabling the consensus clients to fall back to a local or remote execution client if there is a fault in the middleware

There are no execution client changes currently required.

### malicious relay

The most important security mechanism of this design is the ability for all validators to identify if a relay has turned malicious.

Lets assume the worse case scenario: there is a single relay which is connected to 100% of the validators. The relay begins proposing invalid blocks and lies about the value of the payloads such that the validators always selects them.

Under this scenario, a naive MEV-Boost implementation could cause the chain to halt as validators are no longer proposing valid blocks.

There are three ways for the relay to propose a bad payload:

1. invalid payload: the payload breaks some consensus rules
2. inacurate value: the payload proposed has a different value than claimed once executed
3. missing data: the payload body was never revealed by the relay

To mitigate this, it must be possible to either 1) pre validate payload between multiple parties ahead of sending to validators or 2) for all validators in the network to identify when a relay has proposed a bad payload and automatically fallback to a safe alternative. Critically, this security mechanism must be robust in the face of relays who are adversarial towards each other.

### communication between MEV-Boost and relays

There are multiple alternatives for communication between MEV-Boost and the relays: push vs pull, direct vs p2p.

Care must be taken to ensure the following requirements are met in order to select the best implementation:

1. it must protect validator privacy by not associating validator key and IP address
2. it must have lowest possible latency
3. it must be robust against adversarial relays / validators

### risk of missed slots

Missed slots can occur if the block proposer fails to propagate a block in time for sufficient attestations to be collected. In this case, the block proposer does not receive the base reward for the block (approx 0.025 eth at 10m eth staked) nor the transaction and MEV rewards. Since this architecture requires sending signed headers back to the relays / escrows before propagation to the attestors, it will be important to understanding what is an acceptable rate of missed slots and how to minimize it under normal network operating conditions.

### header parameters

In order to produce valid blocks, builders and relayers must know all of the attributes of the [execution payload header](https://github.com/ethereum/execution-apis/blob/5966998897f9526e050fd1438026ce8c94c93fb7/src/engine/specification.md#executionpayloadv1). It’s in the interest of validators to provide all the inputs required for block construction as early as possible. This allows builders to maximize the accuracy and compute time available for finding an optimal block construction.

All header attributes except from `coinbase` can be derived by the builder based on their observed state of the network. It is up to the middleware to filter payloads built on incorrect states.

### validator authentication and feeRecipient address

The validators needs to communicate to builders and relays the address they wish to use as the `feeRecipient`. This address is necessary to accurately measure the value of the proposed payload. Since `feeRecipient` can be any address, the validator must authenticate themselves when publishing it.

There does not currently exist a way for validators to authenticate and publish their `feeRecipient`. The best way to do this would likely be to add a signing domain which allows validators to safely sign arbitrary messages with their staking key.

### partial blocks vs full blocks

This specification deprecates the use of “Flashbots Bundles” in the communication between builders and block proposers in favor of execution payloads which represent the full ordering and content of a block. While bundles have provided an efficient auction mechanism for inclusion of transaction at the top of blocks, they are not expressive enough for all order preference. In particular, bundle auctions are not well suited for large transactions or frontrunning protection use cases. Moving to full block proposals means the full range of preference on ordering can be expressed.

### out of band bribes for priority and MEV smoothing / burning

It is possible some validators will accept out of band bribes to prioritize certain payloads or attempt to perform time bandit attacks through attestation bribery. It is not possible to protect against this behavior without consensus modifications. In theory, consensus could enforce that the block builder which pays the most to the block proposer in ETH must be included and that the payment is spread or burned, though the mechanism is out of scope of this proposal requires further research.

### decentralization

As mentioned in the architecture section above, relays are trusted providers of frontrunning and DoS protection. While the system enables having multiple relays competing with eachother permissionlessly, it is possible there will only be a handful of successful relays. We suggest a [permissionless design](https://ethresear.ch/t/proposer-block-builder-separation-friendly-fee-market-designs/9725) be strongly considered by core devs for the cleanup fork in order to eliminate the need for relays which should improve network decentralization.

### client optimizations

Although not recommended, a validator who is relying exclusively on third party block builders for block construction may run a stripped down version of an execution client which removes the transaction pool and the block construction logic thus reducing the hardware and bandwidth requirement of their client.

## Replies

**pmcgoohan** (2021-11-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/thegostep/48/7751_2.png) thegostep:

> This design allows solo stakers to participate in MEV thus reducing the incentive for economic centralization

MEV is *fundamentally* a centralizing force. MEVA only serves to accelerate this centralization. It is time to stop misrepresenting MEVA as democratizing or decentralizing the network in any meaningful way.

See here for a discussion on why any proposal furthering the integration of MEV auctions into Ethereum [will be disasterous](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980/2).

In summary, MEVA/PBS (especially full-block) incentivizes:

1. centralization around a dominant private relayer with gatekeeping powers over the entire network
2. that centralized relayer must be the most exploitative in order to achieve and maintain dominance, using predatory mechanisms such as censorship markets (allowing one user to censor the transactions of another user for a bribe)
3. there is no requirement for the dominant relayer to have any stake in the network as the Eth needed to buy blocks can be converted just-in-time. Their intention may actually be to profit from trying to harm the network long term (think competing chain, central or private bank, hostile hedge fund or VC). In fact the dominant relayer must care little about the long term success of Ethereum in order to be willing to use the most profitable/exploitative methods possible to win blocks short term.

It’ll end in the antithesis of what Ethereum set out to be, with Tony Soprano running the network.

---

**CodeForcer** (2021-11-04):

Great writeup! I love the simplicity and elegance of the architecture you have outlined.

A few questions/thoughts.

1. How does relay discovery work on the network? Is it a manual process where you input the relay address into the client, or can relays be gossiped between clients like regular peers?
2. If relay discovery is decentralised how do we protect against Sybil relays? Could we make relays stake ETH, give them a reward, and potentially slash them?
3. In a design with a lot of relays, do we need separation between block builders and relays - could these just be the same entity? Would we want to encourage that?

In general it seems a lot of the concerns about centralisation or lack of transparency could be addressed by encouraging a lot of relays to exist, making sure they have skin in the game (need to stake, can be slashed, etc, or some other mechanism), and then consequently trusting them as little as possible, assuming by default that they might be malicious.

Alternatively, if you are imagining this system launching with a single relay or small number of relays, perhaps transparency could be achieved with a historical record of block proposals.

Looking forward to seeing the reference implementation of mev-boost!

---

**pmcgoohan** (2021-11-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/codeforcer/48/6351_2.png) CodeForcer:

> Looking forward to seeing the reference implementation of mev-boost!

As a searcher and Flashbots member I’m sure you *think* this is a good idea.

But my message to searchers is that you’d better not be squeamish, because unless you are prepared to run your own dark pool with a censorship-as-a-service feature, force multi block pump and dumps, grief L2s trying to rollup, steal high value NFTs in auction and any other of the myriad mafia style attacks that full block MEVA permits, then it won’t be you winning the blocks.

---

**Svante** (2021-11-04):

MEV is a fact of reality, whether we like it or not. For discussion to be constructive, I think we should focus on how we can handle MEV and not pretend that the alternative is that MEV goes away.

If we don’t handle MEV collectively, it will grow by itself and only be more centralized.

In this light I think the above proposal is very positive.

---

**pmcgoohan** (2021-11-04):

Mev *is* centralizing. No amount of trying to ‘manage’ it will change that. Any proposal (like this  one) that makes it easier for a single actor to dominate block content worsens the situation. Read the links I gave to see why.

Mev is a reality because the protocol permits it.

If you actually want to decentralize you must include transaction order in the consensus.

---

**Svante** (2021-11-04):

Allright, I gave your linked thread a good 20min read. This will be my last comment on this, as I feel it starts to derail the discussion of [@thegostep](/u/thegostep)’s proposal.

1. Nowhere do I see you propose a better solution to MEV
2. Arguing that MEV is bad is a straw man. We all agree on that. We are discussing what to do about it

If you think the best course of action is to ignore MEV, do nothing about it and let the chips fall where they may, don’t beat around the bush and come with an actual proposal on that, including why it’s better to do that than this alternative.

And if you think there’s a third option, by all means articulate it.

But all your criticism of [@thegostep](/u/thegostep)’s proposal is also true for letting MEV grow unregulated. With this proposal we will at least know if we are suffering the consequences, as it will not happen in the dark.

In any regard, I do appreciate you thinking deeply about MEV, as it has large potential consequences for us all. So thank you for that!

---

**pmcgoohan** (2021-11-04):

Thank you for taking the time to read it. I am deliberately avoiding mitigations because I am attempting to do the prerequisite work of defining the true extent of the problem.

The risks of full block MEVA have not only been underestimated, they have barely been explored at all. The result will be catastrophic.

Here’s a fix. If centralized relayers are now acceptable in the eth2 base layer, then why aren’t they fair ordering transactions and solving MEV?

---

**terence** (2021-11-05):

Had a fruitful conversation with [@thegostep](/u/thegostep) where we explored another scheme where consensus(validator) is the final actor that submits block to the network.

[![image](https://ethresear.ch/uploads/default/original/2X/9/98097c541b8b43671b972d22a1dc500df00baa87.png)image564×610 13 KB](https://ethresear.ch/uploads/default/98097c541b8b43671b972d22a1dc500df00baa87)

**In this design:**

1.) **consensus** requests `ExecutionPayloadHeader` from **mev_boost**

2.) **mev_boost** returns the most profitable to **consensus**

3.) **consensus** signs `SignedBeaconBlock` which contains `ExecutionPayloadHeader` and submits it to **mev_boost**

4.) **mev_boost** validates block signature and saves the block to escrow to enforce slashing in the event of frontrunning

5.) **mev_boost** returns `SignedBeaconBlock` with `ExecutionPayload` to **consensus**

6.) **consensus** validates `SignedBeaconBlock` again, saves it in the DB, and submits it to the network

**Pros**

1.) mev_boost and relay network no longer have to touch the consensus layer’s network stack. Easier to reason and simpler to implement

2.) beacon node / validator guaranteed to have full version of `SignedBeaconBlock` (ie `Payload` not `PayloadHeader`) to be saved in storage and not depend on network to gossip back previous signed block.

**Note**: same could be achieved in current scheme by just having mev_boost return the full block as it submits to the network

3.) consensus get to submits backup block in the event mev_boost fails to respond back signed block with full payload.

**Note**: this is dangerous and requires more consideration in the event mev_boost fails to respond back but still kept the good `SignedBeaconBlock` with `ExecutionPayloadHeader`, validator could be subjected to slashing with two versions of valid blocks

**Cons**

1.) consensus validator identity will become known to the mev_boost, the more validators connects to the same mev_boost software, the risk amplifies

This captures most of the notes. I will do more thinking around this scheme and evaluate further trade offs

---

**jgm** (2021-11-05):

This solves many of the issues with the initial design.  Ensuring the validator receives the block is, in my opinion, critical to keeping the network decentralized from an operational point of view.

Regarding the con of the relay being able to map the validator index to a given IP address (which I assume is what you mean by “identity”), the ideal solution would be to put the request and response on the p2p network.  However, given that this would require additions to the protocol and would be a relatively large amount of traffic for what is in reality a client-server interaction that seems unlikely.

One option could be for many participants in the ecosystem to provide open mev-boost services that connect to the same relay.  At the point the consensus client needs to fetch a payload it can pick one of the mev-boost providers at random and ask them to forward the request for a block.  This is, ultimately, just an obfuscation layer (and brings with it potential additional overheads) but with the low incidence of individual proposer selection it may be enough to ensure that no single mev-boost instance obtains details of the index-to-IP address mapping of a significant portion of the network.

---

**jgm** (2021-11-05):

Sorry, a couple more things. A note on point 3) in the pros: once the consensus node sends its signed header it absolutely cannot do anything but broadcast the block containing the payload for which it has signed, or it can be slashed.  This does mean that the relay can carry out blocking attacks (where the consensus node submits a signature but never receives the related payload) but that’s about as bad as it gets.

And although direct front-running is not possible in this model, it would still be possible for the consensus node to not broadcast the block for the given slot, and broadcast a new bundle to the relays to be included in the subsequent block.  This relies on the consensus node sacrificing its rewards for the current block in the expectation of higher rewards in the next, but should be preventable if the relay also broadcasts the block after it has returned it to the consensus node (so between steps 5 and 6 in your process).

---

**terence** (2021-11-06):

> This does mean that the relay can carry out blocking attacks (where the consensus node submits a signature but never receives the related payload) but that’s about as bad as it gets.

I agree. There’s certainly trust assumption between `mev_boost` and `validator`. Similar to `beacon_node` and `validator` as standalone software in some client implementations today

> This relies on the consensus node sacrificing its rewards for the current block in the expectation of higher rewards in the next

I think having proposer score boosting does mitigate some the concern, but certainly worth further exploration

---

**jgm** (2021-11-06):

There is little detail in here on how the escrow works.  It seems to have been dropped in to the design in an attempt to hand-wave away the issue of relays being dishonest (most obviously about the value of the execution payload they want the validator to sign) but it’s another trusted component.

Given the complexity and potential holes here, I believe that relays trusting validators is a far simpler approach.  Yes the validator can cheat, but then the relay can block the validator from receiving further blocks.  Detecting a cheating validator should be no harder than detecting a cheating escrow or relay in the existing proposal.  This would also turn the relay in to a simple block builder, which fits more cleanly with the proposed builder/proposer separation and so would require less work to move to the fully decentralized model.

---

**fradamt** (2021-11-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> I believe that relays trusting validators is a far simpler approach. Yes the validator can cheat, but then the relay can block the validator from receiving further blocks. Detecting a cheating validator should be no harder than detecting a cheating escrow or relay in the existing proposal.

The main objective of this proposal (as I see it) is precisely that it avoids any trust assumption about validators. As soon as the design allows validators to steal MEV (i.e. we take away the blind signing), small stakers are imho unlikely to be able to receive the very best MEV opportunities, because they can’t be trusted with them. The fact that cheating is detectable (and still, this is not easy at all, so you’d rather trust and police few reputable entities like the escrows) helps very little, because for a small staker stealing once can be worth more than a year of expected rewards (or even several years). Also, small stakers can hardly build a reputation worth anything, because they propose so few blocks (20-40 a year I think?), most of which might not have very high MEV.

For example, would a searcher who has found a 100 ETH extraction opportunity (assuming it’s not very time-sensitive) trust an unknown proposer with it, or just wait one block and give it to a staking pool?

Even if it’s just a small percentage of MEV opportunities, it matters because the distribution of MEV is very much long-tailed, so this small percentage amounts to a disproportionate fraction of the total MEV. Making the long-tail much less accessible for small stakers can result in them earning significantly less, and is therefore a centralizing force

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> There is little detail in here on how the escrow works. It seems to have been dropped in to the design in an attempt to hand-wave away the issue of relays being dishonest (most obviously about the value of the execution payload they want the validator to sign) but it’s another trusted component.

Validators trusting relays is a completely different game than the opposite, because the relay “plays” all the time, so it has a much higher incentive not to do anything bad. Moreover, from the perspective of a validator, I don’t think the relay can do any bad thing which isn’t easily detectable (from the perspective of a searcher it can, i.e. stealing MEV, but that’s irrelevant to validators):

- It can lie about how much the proposer will be rewarded for signing the block, but that’s obvious once the full block is published
- It can withhold the full block or publish something invalid
- It can publish the full block too late for it to be considered. There can be disagreement here about whether the block was actually sent too late, but not about whether it becomes canonical, and that’s something measurable about a relay’s performance

Not only all these faults are detectable and contribute to a relay’s performance/reputation score, they are also greatly mitigated by the presence of multiple reputable escrows. Before signing a payload header, a proposer can simply ask a variety of escrows which it trusts to certify the availability and validity of the full payload, and only sign if it gets at least one positive response (or however many the proposer wants). The trust model for validators becomes then 1/N, and think most small validators would be quite ok with this tradeoff (no trust required versus this trust model) considering it gives them full access to MEV.

---

**BoogerWooger** (2021-11-08):

MEV is already a fact. You cannot deny it, by naming it “centralized”. Ethereum and Bitcoin are also “centralized” by mining pools. In crypto, everything, allowing free market is good. MEV is not “bad”, you cannot dictate network how to order transactions and how to propagate them in p2p network. It’s allowed by protocol, and that’s enough to make it “legitimate” for traders - there is no need to do somethng with it with words, only with algorithms.

MEV, flashbots and other projects, moving in the same direction is only a develoment of “ordering market”, it’s normal. We need to build things like flashbots, better auctions, more concurrency on this market, it will stimulate new strategies of mitigating it. MEV make markets more effective, allowing almost instant reactions on asset prices changes - so, it’s not so bad for whole market, only for part of it. Also, there are strategies to attack MEV searchers, it’s also makes this topic not so simple as “MEV is bad”.

It’s a serious problem, but there are many ways to work with MEV, flashbots are not the only solution. DeFi protocols will mitigate MEV problem with offchain swaps, commit-reveal orderbooks, deterministic randomization of orders. These solutions, born in fight, will make crypto market stronger - so, it’s not so bad as you suggest, IMHO

---

**jgm** (2021-11-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/fradamt/48/6474_2.png) fradamt:

> The main objective of this proposal (as I see it) is precisely that it avoids any trust assumption about validators.

At the expense of creating a trust assumption about relays, and there will objectively be far fewer relays than validators.  The most likely outcome is one major relay, with a handful of minor and/or special-case relays.  Network effects will cause one relay to become dominant, because MEV is all about maximizing rewards and any relay with an advantage over the others will pick up the lion’s share of MEV (and hence the lion’s share of validators chasing said MEV).

![](https://ethresear.ch/user_avatar/ethresear.ch/fradamt/48/6474_2.png) fradamt:

> would a searcher who has found a 100 ETH extraction opportunity (assuming it’s not very time-sensitive) trust an unknown proposer with it, or just wait one block and give it to a staking pool?

That is up to the searcher to decide.  They can put their bundle through sooner with higher risk (but less chance of losing their MEV to a competing bundle), or later with a validator they prefer.  If a validator has little history, however, then it seems a fair assumption that the validator is unlikely to have built their own internal infrastructure to take the proposed block, decompose it, find the MEV, extract it, build a new block, and validate and broadcast said block on the off-chance that a long tail MEV opportunity comes along just at the right time.

Alternatively, given that a relay will be in play all of the time it would be easy for that relay to be 99% trustworthy and subvert the occasional bundle: it has both the financial incentives and the power structure to be able to do so, and it is easy for parties to believe that a small amount of MEV going missing doesn’t point to a corrupt system.

A general point I would like to make, though: the trusted relays design helps to maximize MEV returns at the expense of decentralization (in operational terms), stability and diversity of the network.  Trusted relay creates a chokepoint through which all (or many) block proposals will flow, both for selection of the payload and broadcast of the block.  Consider: in the trusted relay model a corrupt relay can stop block creation (for one slot at least, and highly likely for many more) acting against the validator’s interests, whereas in the trusted validator model the worst a corrupt validator can do is steal MEV.  As far as the chain is concerned, the former is far more problematic than the latter.  The chain is also able to punish the validator (both within the protocol and socially), but has no similar capability over the relay.  Fundamentally, relays are external entities and so should not have any significant level of control over what happens in the network.

Decentralization is not simple when there are conflicting views of which bit of it matters, and the course seems to be heading for a builder/proposer split enshrined in the protocol.  Until then, though, I would prefer to see an architecture that favors putting the burden on in-protocol entities and utilizes the built-in rewards and punishments system to encourage the right behavior for the good of the network.

---

**poma** (2021-11-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/fradamt/48/6474_2.png) fradamt:

> For example, would a searcher who has found a 100 ETH extraction opportunity (assuming it’s not very time-sensitive) trust an unknown proposer with it, or just wait one block and give it to a staking pool?

But the majority of MEV opportunities currently are arbs, sandwiches, and liquidations. All of them are extremely time sensitive. And in cases when multiple searchers compete for an arb opportunity the large chunk of profit goes to miner anyway as a result of bets race. Searchers also have highly optimized smart contracts so an average validator is unlikely to have good enough infrastructure to steal the opportunity and get significantly more than he got via bribe.

Overall I think trying to build infrastructure that likely ends up in a single relay controlling the majority of blocks produced on the network is dangerous.

---

**tkstanczak** (2021-11-15):

As for the relay lying about the value of the block, it can be solved by attaching a Merkle proof of the fee_recipient account balance.

---

**tkstanczak** (2021-11-15):

Any misbehaviour of the relay is detectable within a single slot or immediately.

1. lying about the block value - detectable with a Merkle proof or after the block is signed and published
2. lying about the block validity - detectable upon the block being signed and published
3. not publishing the block after the header is signed - this is a little bit more tricky since it requires the validator to inform other relays and (directly, or indirectly) informing other validators about it too. The tricky part hides in the fact that it is imaginable to have a staking pool A collude with relays to claim that some competing relay is not publishing blocks while never delivering the signed header to that relay in the first place (and only using it in the proof of bad reputation later). If we assume that all the relays are highly competetive then they would always be willing to participate in such behaviour (although it should be hurting them in the long game when they become targets of such attacks themselves).
So - each relay should ask validators to give them information about the latest signed header in each slot - so they can participate in verification whether the block was published by the proposing relay. This leads to a 1 slot delay in verifying whether the best relay has in fact published the block. And collusion to spread misinformation is bad in the long term (but remains unsolved unless we assume p2p gossiping).

---

**pmcgoohan** (2021-11-15):

I uncovered another howler concerning Flashbots auctions over the weekend…

#### Extractors Owning Validators

*Myth: Flashbots auctions mitigate the centralization risk of extractors investing profits into owning validators because they no longer need to own validators to extract.*

This is not the case. If a searcher makes 5% running a strategy on someone else’s validator and 100% running it on their own validator, they are still incentivized to put their profits into buying validators.

Auctions ensure that the majority of extracted profits go to validators, therefore extractors will make more from running strategies on their own validators and centralization risk has not been mitigated.

This is in addition to the existing risks I highlighted of [block builder centralization](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980/10), [censorship-as-a-service](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980/5) and [unstaked hijack attacks](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980/23).

MEV is fundamentally centralizing. You can’t build stuff ontop of a centralized component (lone miners choosing block content) and expect it to decentralize. It’s magical thinking. The only workable option is to decentralize content. I would not expect this idea to be controversial in this community.

From what I’ve heard, just two actors now dominate MEV extraction (Wintermute and Alameda) so it seems like the centralizing effects of unchecked MEV are already building. They will be busy buying up validators with their profits. Whichever of them is the first to establish a censorship market will dominate the other when full-block MEVA arrives.

All this proposal would achieve is to build a collusion network acting against the interests of the network into the network itself.

---

**thegostep** (2021-11-15):

A few thoughts based on the discussion so far:

1. MEV-Boost is a short term solution that bridges the gap to the permissionless block proposer / builder separation + mev smoothing solution which is preferred by everyone as it eliminates relays and therefore relay centralization. That being said, I expect multiple entities with existing reputations + large validators to offer relay services in the short term as it can be monetized + allows for reducing counter-party risk.
2. Pursuing a solution which enables solo staker participation is critical to MEV democratization as it protects the ability for individuals to participate in receiving MEV rewards without the need to join a pool. I don’t see it being possible to scale up monitoring and enforcement of solo validators in a way that makes it reasonable to send payloads to validators in cleartext - if there was an automated way to evaluate solo validator behavior I could see this path being more plausible.
3. Any MEV minimization / fair ordering system needs to be incentive compatible in order to succeed in the long run - I don’t see a path for these fair ordering experiments to gain adoption without either a) providing move revenue to validators, or b) introducing a consensus level change to the protocol. Solutions involving a) are already compatible with this proposal whereas solutions involving b) are outside the scope of the discussion in this post.


*(4 more replies not shown)*
