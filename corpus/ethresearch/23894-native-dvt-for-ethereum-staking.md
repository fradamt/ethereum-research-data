---
source: ethresearch
topic_id: 23894
title: Native DVT for Ethereum staking
author: vbuterin
date: "2026-01-20"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/native-dvt-for-ethereum-staking/23894
views: 1969
likes: 32
posts_count: 20
---

# Native DVT for Ethereum staking

Distributed validator technology (DVT) is a way for Ethereum stakers to stake without fully relying on one single node. Instead, the key is secret-shared across a few nodes, and all signatures are threshold signed. The node is guaranteed to work correctly (and not get slashed or inactivity-leaked) as long as > 2/3 of nodes are honest.

DVT includes solutions like [ssv.network](https://ssv.network/) and [Obol](https://obol.org/), as well as what I call “DVT-lite”: either the [Dirk + Vouch combination](https://docs.gateway.fm/validators/nodes/validator-clients/3rdparty/) or [Vero](https://github.com/serenita-org/vero). These solutions do not do full-on consensus inside each validator, so they offer slightly worse guarantees, but they are quite a bit simpler. Many organizations today are exploring using DVT to stake their coins.

However, these solutions are quite complex. They have a complicated setup procedure, require networking channels between the nodes, etc. Additionally, they depend on the linearity property of BLS, which is exactly the property that makes it not quantum-secure.

In this post, I propose a surprisingly simple alternative: we enshrine DVT into the protocol.

## The design

If a validator has `>= n` times the minimum balance, they are allowed to specify up to `n` keys and a threshold `m`, with a maximum of `m <= n <= 16`. This creates `n` “virtual identities” that all follow the protocol fully independently, but are always assigned to roles (proposer, committee, p2p subnet) together.

That is, if there are a total of 100000 validators and you have a size-n validator with multiple virtual entitities, and there is a role with `t` participants (eg. `t=1` for proposal, `t=16` for FOCIL, `t=n/64` for some p2p subsystem that shards nodes into 64 subnets, there is a t/100000 chance that *all* of your virtual identities will be assigned to that role.

From the perspective of protocol accounting, these virtual identities are grouped into a single “group identity”. That single object is treated as taking some action (eg. making a block, signing) if and only if at least `m` or the `n` virtual identities signed off on the action. Based on this, rewards and penalties are assigned.

Hence, if you have an identity with eg. `m = 5`, `n = 7`, then if five signatures all attest to a block, you get 100% of the attester reward and your participation is counted, but if four signatures do, you get 0% of the reward and your participation is not counted. Similarly, to slash such a validator, you need to show proof that >= 5 of the nodes votes for A, and >= 5 of the nodes voted for B.

Note that this means that if `m <= n/2`, slashing is possible without any malfeasance, so such a setting is strongly anti-recommended, and should only be considered in situations where some nodes are normally-offline backups.

## Properties

This design is extremely simple from the perspective of a user. DVT staking becomes simply running `n` copies of a standard client node. The only implementation complexity is block production (or FOCIL production): realistically, a random node would need to be promoted as a primary, and the other nodes sign off on it.

This only adds one round of latency on block and FOCIL production, and no latency on attestation.

This design is easy to adapt to any signature scheme, it does not depend on any arithmetic properties.

This design is intended to have two desirable effects:

1. Help security-conscious stakers with medium to high amounts of ETH (both individual whales and institutions) stake in a more secure M-of-N setup, instead of relying on a single node (this also makes it trivial to get more gains in client diversity)
2. Help such stakers stake on their own instead of parking their coins with staking providers, significantly increasing the measurable decentralization (eg. Herfindahl index, Nakamoto coefficient) of the Ethereum staking distribution.

It also simplifies participation in existing decentralized staking protocols, reducing the client load and devops experience to something equivalent to the most basic form of solo staking, allowing such protocols to become more decentralized and more diverse in their participation.

## Replies

**alonmuroch** (2026-01-20):

[@vbuterin](/u/vbuterin) thank you for the post

I get a few questions:

1. Coordination vs. Passive Broadcasting

For attestations, nodes can stay passive; if they see the same head, the threshold is met naturally. However, for block production, how do you prevent nodes from signing different payloads and failing to reach the m threshold? Would you favor a simple leader rotation or a local gossip sub-net?

2. Async BFT & Multiple Proposers

We could allow a “race” where multiple virtual identities broadcast proposals simultaneously. The first to collect m signatures wins. This eliminates round-change latency, though it slightly increases p2p overhead.

3. Key Rotation

I’d suggest adding a protocol-level key rotation. An m-of-n signed message could swap a compromised key without a full exit/restake, making this much more viable for institutions.

---

**serenita_luca** (2026-01-20):

An interesting proposal, though it seems to go against the ongoing efforts of:

- reducing consensus overhead (e.g. via validator consolidations) - enshrined virtual DVT identities would cause additional network overhead which is currently contained “in-cluster”. With 2048 staked ETH, n  Help security-conscious stakers with medium to high amounts of ETH (both individual whales and institutions) stake in a more secure M-of-N setup, instead of relying on a single node (this also makes it trivial to get more gains in client diversity)

This is mostly my skepticism speaking but gains in client diversity have historically been extremely hard to achieve. Even with DVT options available today, we are frequently seeing operators run DVT clusters powered by only 2 different client pairs, protecting validators from downtime while completely failing to protect from the much more dangerous threat – consensus bugs.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Help such stakers stake on their own instead of parking their coins with staking providers, significantly increasing the measurable decentralization (eg. Herfindahl index, Nakamoto coefficient) of the Ethereum staking distribution.

I don’t believe requiring such stakers to run multiple machines with different client pairs will make this option very attractive compared to what is available today. Such entities are probably quite capable of running out-of-protocol DVT options, Vouch+Dirk or a couple of Vero instances.

I agree something needs to be done about Ethereum’s stake distribution and its centralizing trend. But I don’t think enshrining DVT will help much at all. I’m currently working on an idea that could help a little on this front but I’m 100% sure we will need more ideas to revert the existing trend.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> It also simplifies participation in existing decentralized staking protocols, reducing the client load and devops experience to something equivalent to the most basic form of solo staking, allowing such protocols to become more decentralized and more diverse in their participation.

This I can see happening, and it would be good for decentralized staking protocols, and by extension Ethereum.

---

**alonmuroch** (2026-01-20):

Another point is, should the security considerations of a staking actor increase overhead on the CL? Isn’t it much better to offset it to an optimized layer?

---

**alonmuroch** (2026-01-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/serenita_luca/48/17802_2.png) serenita_luca:

> This is mostly my skepticism speaking but gains in client diversity have historically been extremely hard to achieve. Even with DVT options available today, we are frequently seeing operators run DVT clusters powered by only 2 different client pairs, protecting validators from downtime while completely failing to protect from the much more dangerous threat – consensus bugs.

It is true that SSV only has 2 clients at the moment (others have 1) but that an evolution/ iteration thing. Also, it might be better to have the EF “split the bill” so we could have more clients

---

**serenita_luca** (2026-01-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/alonmuroch/48/4817_2.png) alonmuroch:

> It is true that SSV only has 2 clients at the moment (others have 1) but that an evolution/ iteration thing. Also, it might be better to have the EF “split the bill” so we could have more clients

I wasn’t referring to SSV having 2 clients.

What I meant is that there are node operators that run Vero/Vouch/DVT but then only connect their validator clients to Prysm+Geth and Lighthouse+Nethermind nodes (clients used by large parts of the network), resulting in them losing the (imo) most important benefit of multi-node setups – protecting from consensus bugs.

---

**OisinKyne** (2026-01-20):

A few considerations from our end, mostly in-line with whats flagged before.

My primary concern is how this contends against other ongoing research trying to lower the amount of signatures on the chain to facilitate the move to ZK and 3SF, e.g. [your proposals](https://ethresear.ch/t/sticking-to-8192-signatures-per-slot-post-ssf-how-and-why/17989) to get to 8192 signatures per slot, and efforts like [EIP7251](https://eips.ethereum.org/EIPS/eip-7251) (Max EB), as well as flagging that taking DVs in protocol doesn’t mean we no longer have extra communication to make them viable.

I also think the problem to be solved here could be more clearly specified. If the goal is to come up with a solution for distributed validators in post quantum (lean) ethereum, I outline Obol’s research on the topic to date below.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This design is extremely simple from the perspective of a user. DVT staking becomes simply running n copies of a standard client node

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> and no latency on attestation

I don’t think it is that simple. Take an attestation’s head vote component (or a sync message); If you have e.g. 7 honest operators taking part in a DV, three might not see a proposers block in time, and attest to a missed slot, while 4 (or 3 or 2) might see the block, and propose it instead. This will result in no majority for the attestation (or at least an incorrect head vote if the protocol can introspect the constituent parts of an attestation and sees quorum votes for correct source and targets) and lost rewards. For a sync message, it would be an outright penalty. These distributed validators have to coordinate to reach a super majority, and now we’d either be doing it on the main p2p network (a bad idea), or doing it in a dedicated p2p channel between the nodes like the status quo.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If a validator has >= n times the minimum balance, they are allowed to specify up to n keys and a threshold m, with a maximum of m  Additionally, they depend on the linearity property of BLS, which is exactly the property that makes it not quantum-secure.

This I think is the most important problem to solve as it pertains to post-quantum distributed validators. (Whereas I think the chain’s declining nakamoto co-efficient is the most important problem to solve for Ethereum’s validator set. DV enshrinement is not likely to be a big fix for that). All of the aforementioned DV(-adjacent) designs rely on BLS signature aggregation.

At Obol, we have been working on Distributed Validators for Lean Ethereum for over a year now, I’ll briefly describe some avenues that we don’t think will work, then will focus on our most promising avenue to date, which is more or less in line with the design in this post anyways in my opinion.

- Firstly, we looked at using pure MPC protocols to complete the hash based signature schemes being considered for Lean Ethereum. In short, these involve too many round trips to be viable at the slot times Lean aspires to. Towards Practical Multi-Party Hash Chains using Arithmetization-Oriented Primitives [1]
- Next we worked on a combinatorics based approach to calculate a threshold HBS, inspired by your 2018 post here:  thbs_combinatorics/doc/main.pdf at 653155fc62265646850bf173576c1a89130d06e5 · ObolNetwork/thbs_combinatorics · GitHub Unfortunately, the security reduction was too large such that the scheme was not viable on the preferred lean hash chain parameters.
- Most recently, we have extended the LeanMultisig repo to support threshold XMSS signatures. leanMultisig/docs/threshold_xmss_design.md at feature/threshold_xmss · ObolNetwork/leanMultisig · GitHub  This is the most promising work to date, and in my eyes, not dissimilar to the plans in this post (enshrinement), just in a ZKP paradigm where threshold signatures are supported within the proof system rather than handled transparently in the STF. These threshold signatures do have a negative impact on the resulting proof size, and aggregation of the threshold signatures as well as aggregation of a mix of threshold signatures and standard XMSS signatures are still an open item for implementation before we can consider this viable for the finalised Lean Ethereum protocol. Nonetheless I think its worth doing and our best avenue yet.

To conclude; I don’t think enshrinement pre-lean Ethereum has a strong enough need. Post-lean I would support an approach that keeps DVs viable yet out of the core protocol complexity if we could, but we don’t yet have such a design. So including them in-protocol is our best option. I certainly think distributed validators are critical for Ethereum to [survive its struggles](https://blog.obol.org/tackling-the-staking-problem/) with (mostly unavoidable) centralisation forces, and can’t be dropped from the staking model outright without all but assuring that the chain will be co-opted by a small number of parties in the not so distant future. Small groups are more credibly neutral than individual parties, and are more likely to make the best decision for the wider community beyond their group.

1. Alexandre Adomnicăi, Towards Practical Multi-Party Hash Chains using Arithmetization-Oriented Primitives: With Applications to Threshold Hash-Based Signatures. IACR Communications in Cryptology, vol. 2, no. 4, Jan 08, 2026, doi: 10.62056/ahp2tx4e-. ↩︎

---

**vbuterin** (2026-01-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/alonmuroch/48/4817_2.png) alonmuroch:

> I’d suggest adding a protocol-level key rotation. An m-of-n signed message could swap a compromised key without a full exit/restake, making this much more viable for institutions.

Yeah I agree with this, I think it’s a good idea independent of this one. It should not be hard to allow instant key changes, and keep the old key around for a while for slashability.

> go against the ongoing efforts of: reducing consensus overhead (e.g. via validator consolidations)

This is fair, though it’s designed to not make the worst case worse. That is the reason behind the “you must have >= 32 * n" rule.

> Such entities are probably quite capable of running out-of-protocol DVT options, Vouch+Dirk or a couple of Vero instances.

I think this is the crux of the matter. I’ve personally seen the inside of organizations and ETH whales (incl myself) trying to figure out Vouch/Dirk/Vero, and it’s a big headache to wrap our heads around and understand. If running DVT were as simple as “run 7 independent nodes, the only change is a one-line difference in config file” (maybe even the line of change in the config is not required, as it could autodetect your key’s membership in a DVT set), then I’m pretty sure both others and myself would have been DVT-staking for a while now.

So I feel confident that this style of in-protocol DVT would be pretty decisive in terms of enabling people (esp. whales and smaller institutions) to stake on their own

> I don’t think it is that simple. Take an attestation’s head vote component (or a sync message); If you have e.g. 7 honest operators taking part in a DV, three might not see a proposers block in time, and attest to a missed slot, while 4 (or 3 or 2) might see the block, and propose it instead.

yeah I agree this is a weakness. Though I guess (i) I expect it to be rare and not a large penalty to revenue, because most attestations do come on time [and we can further penalize edge case attestations by adding penalties in proportion to how much people behave differently wrt an attestation], and (ii) we can treat each action separately from a rewards perspective, eg. if you break it down to (i) “voted for X” vs “voted for nothing”, (ii) voted for parent Y, then you can give such a voter a reward for voting for parent Y without a reward for voting for X or nothing.

> Most recently, we have extended the LeanMultisig repo to support threshold XMSS signatures. leanMultisig/docs/threshold_xmss_design.md at feature/threshold_xmss · ObolNetwork/leanMultisig · GitHub

I appreciate the research, thank you!

I do agree that it has fewer edge cases to go through a single leader and have a single action; though the thing to trade it off against is devops ccomplexity.

It’s possible that the right thing to do is to figure out a way to do it natively but in a way that still avoids tracking partial participation onchain (eg. leader sends their signature, the other nodes see it in the p2p net and follow the leader). In that case, the tradeoff would become just latency (though maybe it’s not that bad)

---

**fluidity-dev** (2026-01-21):

I really appreciate the pragmatic approach here, it looks extremely simple and on-point. My question is about technical debt of enshrining a transitional solution. Adding consensus or specific penalty logic for a temporary mechanism may risk bloating the protocol with rules that might become gradually obsolete once ZK matures.

Given the rapid progress in folding schemes and hardware acceleration, a client-side ZK solution (where a threshold of partial signatures are aggregated into a single validity proof locally, precluding split votes) might become viable sooner than expected.

Would it be desirable in your view to design the proposal as a lightweight, opt-in standard rather than an enshrined protocol rule? This would solve the immediate pain for institutions without forcing the protocol to carry legacy logic, keeping the path open for a cleaner ZK migration later.

Please kindly let me know if I am misunderstanding anything here.

---

**vbuterin** (2026-01-22):

> I really appreciate the pragmatic approach here, it looks extremely simple and on-point. My question is about technical debt of enshrining a transitional solution. Adding consensus or specific penalty logic for a temporary mechanism may risk bloating the protocol with rules that might become gradually obsolete once ZK matures.

Fully agree with this concern.

I think if it becomes obsolete once ZK matures, we should not even bother.

But why would it be obsolete when ZK matures?

The problem is not cryptography, the problem is latency, and fundamental difficulty of getting nodes to talk to each other.

---

**OisinKyne** (2026-01-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> So I feel confident that this style of in-protocol DVT would be pretty decisive in terms of enabling people (esp. whales and smaller institutions) to stake on their own

I think you misjudge why whales and smaller institutions are not staking on their own. The two primary reasons are the operational costs versus delegation, and the illiquidity costs versus delegation. Setup costs round to zero.

Running one node by yourself costs at least $300 per year, assuming you value your time at $0/hr and you share the cost of an internet plan with your personal/professional use. That’s just power + hardware depreciation + a contribution to internet. A fairer model of cost is to consider what it would cost to run a validator on a bare metal provider. A $150/mo machine gives you $1800 per year, and if that machine dies you’re in trouble because you can’t run a backup without getting slashed, so you then start looking at 3 machines, and running something DV-like. Lets pretend there are savings along the way and call it $3k per year in just hardware, still no labour.  (And if we assume whales and small institutions run >4k eth, we should really add another $500 per node minimum in egress, but I’ll underestimate to prove a point).

If we compare that to the fees for delegating, we see:

- At a retail 10% fee: 3k equates to $30k in staking rewards at 10%, or about $1.2m in staked ether to begin to break even with delegation. (Realistically more because of my rounding down).
- At a whale/small institution 2.5% fee: You need to be staking $5m+ to come close to break even on DIY with free specialist labour. And likely again higher due to the risk premium associated with doing this yourself as an entity who’s primary focus is probably not staking their own money.

And cost isn’t even the biggest blocker for most large institutions on staking, **illiquidity is**. The biggest headwind for native staking is the interminable exit queue. If Ethereum had a [price based means](https://ethereum-magicians.org/t/eip-7002-execution-layer-triggerable-exits/14195/6?u=oisinkyne) to exit stake, more entities would consider native staking. Without it, the potential for a multi-month lock in is intolerable for most entities, forcing them into LSTs or CEX staking. An EIP1559 style ‘burn X eth to be out deterministically in Y time’ would be a massive fix to Ethereum’s centralisation problems, far above lowering the cost to run a validator node or a marginal improvement in the devops overhead of setting up a DV.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I expect it to be rare and not a large penalty to revenue, because most attestations do come on time

I’m talking about late blocks, not late attestations. Late blocks are prevalent and growing due to timing games. Our data indicates 2.5% of slots are processed late. Also the penalty for incorrect head votes is very significant, 22% of a validators reward by [this data](https://pintail.xyz/posts/modelling-the-impact-of-altair/#modelling-perfect-participation). Near double a proposal, and 7x a sync committee. In an extremely squeezed industry, head vote accuracy is a significant issue. I’m open to lowering their rewards, but that comes at the cost of latency sensitive apps that want the head of the chain to be accurate/have large stake weight as fast as possible. (e.g. the [soft-confirmation](https://arxiv.org/html/2405.00549v3) rule)

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I do agree that it has fewer edge cases to go through a single leader and have a single action; though the thing to trade it off against is devops ccomplexity

I’d love to help you out trying out DV tech like Obol, I think we’ve done a good job of simplifying the deployment of distributed validators, but of course there is still much to do on that front that we’re working on. Few people these days are wiring together these clients themselves by hand, the vast majority are using existing tooling, such as [eth-docker](https://github.com/ethstaker/eth-docker), our [docker-compose setups](https://github.com/ObolNetwork/charon-distributed-validator-node), [stereum](https://github.com/stereum-dev), sedge, community maintained ansible scripts, [helm charts](https://github.com/ObolNetwork/helm-charts/tree/main/charts/dv-pod), etc. I think you’re an outlier given that you have a solo setup you’re looking to modify.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> leader sends their signature, the other nodes see it in the p2p net and follow the leader

The main p2p layer is one of the chain’s biggest bottlenecks, its not something we should overload lightly. Also, establishing direct communication between nodes in a DV (as Obol does) is faster, and less wasteful on bandwidth than using a shared gossip network.

---

**GalRogozinski** (2026-01-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I think this is the crux of the matter. I’ve personally seen the inside of organizations and ETH whales (incl myself) trying to figure out Vouch/Dirk/Vero, and it’s a big headache to wrap our heads around and understand. If running DVT were as simple as “run 7 independent nodes, the only change is a one-line difference in config file” (maybe even the line of change in the config is not required, as it could autodetect your key’s membership in a DVT set), then I’m pretty sure both others and myself would have been DVT-staking for a while now.

If the crux of the matter is a UX issue, it sounds easily solvable with some good documentation, a docker-compose.yaml template, and maybe some AI templates that can spin everything up (besides touching private secrets of course).

I personally don’t understand why add overhead and complexity to the core protocol ![:person_shrugging:](https://ethresear.ch/images/emoji/facebook_messenger/person_shrugging.png?v=14)

---

**ladidan** (2026-01-22):

It is worth noting that the cost of running a staking node are set to dwindle with the advent of zkAttester clients (potentially as early as Glamsterdam).

Furthermore, ongoing work will allow ‘DVT-lite’ solutions—as described above—to be baked into client software, making them a default feature on single-node instances. This is possible because the cost of cross-client validation will become marginal (i.e., k-of-n zkEVM [or eventually zkCL] proof verification can happen locally on even the most minimal hardware).

This alone represents a massive boost in protection against consensus bugs without the overhead of additional hardware, specialized software, or distributed keys.

While ‘Full-DVT’ may still make sense for some multi-operator scenarios, giving all attesters the option of simple, minimal, in-protocol, out-of-the-box threshold signing —paired with incentive layer adjustments e.g. to disincentivize correlated attesting (EIP-7716), among other proposals — appears reasonable.

---

**OisinKyne** (2026-01-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/ladidan/48/18796_2.png) ladidan:

> giving all attesters the option of simple, minimal, in-protocol, out-of-the-box threshold signing —paired with incentive layer adjustments e.g. to disincentivize correlated attesting (EIP-7716), among other proposals — appears reasonable.

Reasonable, sure. Will it solve all our problems? I don’t think so. Protecting smaller stakers from consensus bugs is good, and we should do it. Penalising correlated downtime is good, and we should do it. Lowering the operational cost of staking is good, and we should do it (except at the cost of hindering our ability to scale). These changes however will not overcome the illiquidity penalty of native staking, nor do i expect them to overcome the economies of scale of centralised staking as service (though help on the margins doesn’t hurt). I also doubt the benefit of bringing particularly threshold signing in protocol outweighs the opportunity cost of other EIPs core devs could choose (like EIP-7716). (Though i do support keeping threshold signing in Lean)

If we don’t want Ethereum to be captured, we need to stop the degradation of its fork choice nakamoto coefficient and withdrawal credential gini index. We need to protect two things, 1) the diversity and sovereignty of the validator sets withdrawal credentials, and 2) the diversity and sovereignty of its signing keys.

Validators overwhelmingly point at a handful of custodial (or third-party upgradeable) withdrawal credentials, the validator set has a gini index of [0.94](https://x.com/robplust/status/1975872756647649325?s=20) and climbing before we look at factory contracts like upgradeable eigenpods, so in practice its even higher. This risks the theft of a large part of the validator set. Something that wouldn’t harm Ethereum directly, but could be extremely socially destructive as well as bad for the price of ether (and thus its ‘economic security’ by second order effect). A protocolised path to exit liquidity would help mitigate this ongoing centralisation.

The hot keys are more difficult to discern, due to the specialty of StaaS providers ensuring their nodes aren’t easily doxxed and clustered (speaking from personal experience running a double digit % of the network and landing in the ‘unknown’ tab on explorers, one should assume most keys in the unidentified section of staking breakdowns to be centralised without other data). With the marginal rate for delegated staking close to and regularly 0% or negative, it is very difficult to see how the delegated staking market will improve without a black swan massive correlated slashing, which we cannot just cause. Hoping that a large % of stake will begin to solo stake is admirable, but not credible in my eyes. A more attainable hope is that delegated parties are not single points of control nor failure in fork choice. Having groups of entities running stake together on behalf of delegators is more trust minimised than having single parties run the stake. A group of 4/7 operators are less likely to collude to do something untoward with that stake. Imagine putting a plan in writing and sending it to the other operators to get their buy in to defect. Multi-operator distributed validators shifts the burden of coordination onto defectors, which makes defection more difficult.

Compare the staking set to the execution layer by analogy. Would we think the EL, L2s, and DeFi are healthy, if the vast majority of eth are in upgradeable smart contracts or opaque EOAs? no. If you are a retail CEX user, are you safer if your eth sits in a metamask that the CEO can access? or a multisig controlled by the team, or better yet, multiple teams? To date we haven’t held the staking set up to a standard near those of DeFi, L2s, nor wallets, and Ethereum’s security and decentralisation is worse for it. Improving the UX of high availabilty staking can help on the margin, but will it change the set radically? I don’t think so. A price to exit, correlated downtime penalties, and a ValidatorBeat are more worthwhile initiatives than taking DVs in protocol for the supposed DevOps benefit imo.

---

**fluidity-dev** (2026-01-22):

Thanks for the clarification. Yes, ZK doesn’t fix the latency itself. It still may remove the need to handle the consequences of that latency. If coordination fails or lags, the ZK proof is simply not generated or allows us to verify accountability and valid failovers without burdening L1, whereas a stateful approach requires additional rules to manage slashing risks. I thought such contingency logic might become obsolete. I appreciate you taking the time to engage with these questions. It really helps me clarify the trade-offs involved.

---

**bbjubjub2494** (2026-01-22):

Are you sure this system works out when it comes to block proposals? (and by the same token inclusion lists)

![](https://ethresear.ch/user_avatar/ethresear.ch/alonmuroch/48/4817_2.png) alonmuroch:

> We could allow a “race” where multiple virtual identities broadcast proposals simultaneously. The first to collect m signatures wins. This eliminates round-change latency, though it slightly increases p2p overhead.

Isn’t it a likely outcome that the virtual identities split over multiple proposals and nothing gets included? You would have to race N-M+1 proposals to ensure optimal liveness, (up to N-M can be offline) and non-proposing nodes can only safely sign one proposal, so unless they all independently decide the same way everyone will miss the proposal rewards. We can play with the tradeoff a bit, but I’m skeptical something practical would come out.

Of course on the other hand you could run some kind of consensus algorithm between the identities, even a fast n≥5f+1 if we want, but we would be re-introducing some of the downsides of current DVT since nodes will have to set up maintain reliable connections with each other. The kicker is that they will be seldom used, so you might not notice if they have an issue. (Still at least we are getting rid of private one-to-one channels for the DKG)

As a result I think this could work well for “pure” consensus signatures under synchrony: FFG and Casper votes, and sync committee — the same signatures that can be heavily aggregated, but it breaks for roles where nodes have millions of bits of discretion such as inclusion and proposal. Maybe what we should do instead is allow validators to group for the purposes of voting, but retain independent proposal slots. That way you still socialize 87.5%¹ of your revenue with let’s say your validator *coalition*, the design stays nice and simple, and the chain still gets the benefits of diversity. (since a few bugged proposers aren’t what causes harm)

Of course unbundling validator roles is not a new idea and has been explored in [3TS](https://ethresear.ch/t/three-tier-staking-3ts-unbundling-attesters-includers-and-execution-proposers/21648) most recently. These could go well together.

1: [Upgrading Ethereum | 2.8.4 Rewards](https://eth2book.info/capella/part2/incentives/rewards/)

---

**Bez625** (2026-01-23):

Thanks for the post and mentioning Vouch + Dirk. I’ve given a lot of thought to the comments here.

Firstly, I think it’s a bit inaccurate to conflate tools like Vouch/Dirk/Vero with Obol / SSV. To my mind the purpose of Obol / SSV is to distribute validator duties to separate, independent operators that have some additional form of guarantees around honest behaviour. The intent at a conceptual level is for a validator to distribute duties to other entities.

Conversely, Vouch+Dirk aims to perform the duties of multiple validators at once with one minimal set of trusted Ethereum nodes. Dirk can be configured to be a threshold signer and keys distributed to multiple instances. The entire setup is designed to be operated by one entity and so trust is implicit. This setup guards against consensus bugs, client bugs and allows for high availability with 0 down time. The intent at a conceptual level is for a single entity to perform multiple validator duties with a resilient and secure infrastructure. Without minimising the benefits this adds, we can think of the distributed part of this setup as an implementation detail rather than design.

From my perspective, I’m not convinced the reason institutions are staking with professional operators is solely that it’s too technically complex to operate themselves. Oisin did a great job of articulating some reasons, but I think there are additional reasons such as a support model, slashing insurance and so on. Ultimately, I don’t think enshrining DVT at a protocol level will sway institutional stakers away from professional staking providers.

Regarding Vouch + Dirk being too complicated; this is something we hear a lot. Part of the reason behind the complexity is that to get Vouch+Dirk to an institutional grade setup requires an understanding of the entire orchestration, and abstracting away details is potentially dangerous. Maybe we need to do more in the way of making this easier for people that don’t require an institutional grade setup. Any feedback on specific pain points with Vouch+Dirk would be welcome.

A simple setup with one Dirk instance (i.e. slashing protection, but no threshold signing) and Vouch with a configurable set of beacon clients should be easy to orchestrate in something like Kubernetes via a Helm chart and a minimal configuration. This would guard against client and consensus bugs and would be more than possible to run even on a single host (assuming the resources are enough to run the desired client pairs).

---

**Oba-One** (2026-01-23):

Thanks [@vbuterin](/u/vbuterin) for sharing this post, really great to see DVT tech and squad staking get highlighted and potentially enshrined in Ethereum. I would like to speak to the potential effects of this change from a more regenerative and public goods lens.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This design is intended to have two desirable effects:
>
>
> Help security-conscious stakers with medium to high amounts of ETH (both individual whales and institutions) stake in a more secure M-of-N setup, instead of relying on a single node (this also makes it trivial to get more gains in client diversity)
> Help such stakers stake on their own instead of parking their coins with staking providers, significantly increasing the measurable decentralization (eg. Herfindahl index, Nakamoto coefficient) of the Ethereum staking distribution.

For the past couple of years, I have been working in Greenpill under the Dev Guild banner to grow staking for public goods. We took a ton of inspiration from Impact Stake and Launchnodes, which create protocols to funnel staking rewards to public goods. I love this model for public goods because it introduces a low-risk path for people to support by staking, not donating.

The core aspects of the protocol are:

- Dappnode: Provides the hardware to stake and now even more with self-hosted AI and other privacy-preserving aspects it enables, like having your own RPC and IPFS node.
- Obol: Enables running a squad and fits the ethos of Greenpill, which is a distributed community across the globe, and enables potential futures where you have a concentrated cluster of squads. What I love about squads is the team, trust, and relationship building it enables between node operators.
- Lido CSM: Drastically lowers the barrier for node operators to participate and has been huge for us in Greenpill, being able to provide this as a viable path for members with limited funds who deeply care about Ethereum and decentralization.
- Octant Vaults: Serve as the funnel point for yield generated from squads to then go into low-risk DeFi protocols to compound and grow. They, with different allocation strategies like streaming and conviction voting, disburse funds.

As we have been building this protocol, we have had some issues on the operator side getting people fully set up, and the current process, while feasible, could greatly improve. One of the effects I see is once again **lowering the barrier for people to stake in Ethereum and enabling more people to get skin in the game** and utilize the ultimate public good, Ethereum.

To close, I want to highlight that I believe a core aspect of Ethereum scaling is enabling as many people to become validators as possible and start to build a physical relationship with Ethereum where you can see your node running and know that’s building my savings, that gives me privacy, etc. I strongly feel if we can get Ethereum infrastructure embedded at a community level so not just even home stakers but communities staking at the public library or town hall, these are the things I feel will make Ethereum truly stick.

[@vbuterin](/u/vbuterin), I appreciate you so much for being a clear and coherent voice in our space; it’s done so much to keep people like me alive and aligned with the Ethereum vision.

You’re the unicorn in dark times that shines a light and keeps things bright ![:unicorn:](https://ethresear.ch/images/emoji/facebook_messenger/unicorn.png?v=14)

---

**alonmuroch** (2026-01-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/bbjubjub2494/48/19148_2.png) bbjubjub2494:

> Isn’t it a likely outcome that the virtual identities split over multiple proposals and nothing gets included? You would have to race N-M+1 proposals to ensure optimal liveness, (up to N-M can be offline) and non-proposing nodes can only safely sign one proposal, so unless they all independently decide the same way everyone will miss the proposal rewards. We can play with the tradeoff a bit, but I’m skeptical something practical would come out.

If we want reliable duty execution between those parties we need some coordination layer, either you take the trust assumptions Vouch has or less assumptions that DVT has. Either way some coordination is required, otherwise we will see a lot of missed duties.

I’ve written the above paragraph as a reference to asyn-bft which allows “multi” proposers to co-exist.

---

**rodrod** (2026-01-28):

This is a very interesting proposal and could represent a significant shift for Ethereum.

I’d like to complement the current discussion with another important direction that I think we should actively pursue. So far, the discussion has focused on the (important) issues of increasing security through an M-of-N setup, decentralization, or simplifying participation. However, this overlooks another significant benefit of DVT: it mitigates the concentration of power held by a single proposer in a given slot, which today enables MEV extraction (e.g., sandwiching), censorship, reorgs, and related behaviors.

DVT opens the possibility of addressing these issues through the power of consensus, but its protocols must be carefully extended to incorporate defenses against these various undesired behaviors. Our group at Técnico-ULisboa started working on these extensions and will post a longer article on the subject in a separate thread. We are also reaching out to colleagues at the EF for input and potential collaboration.

Once again, this is a very exciting research direction, thanks for the great discussion!

Rodrigo, Christof, and Miguel

