---
source: magicians
topic_id: 23942
title: Formalizing decentralization goals in the context of larger L1 gaslimits and 2020s-era tech
author: vbuterin
date: "2025-04-30"
category: EIPs > EIPs Meta
tags: []
url: https://ethereum-magicians.org/t/formalizing-decentralization-goals-in-the-context-of-larger-l1-gaslimits-and-2020s-era-tech/23942
views: 3081
likes: 119
posts_count: 33
---

# Formalizing decentralization goals in the context of larger L1 gaslimits and 2020s-era tech

*See also: this earlier post from Barnabe [Decoupling throughput from local building - Economics - Ethereum Research](https://ethresear.ch/t/decoupling-throughput-from-local-building/22004)*

One of the unavoidable consequences of raising the L1 gaslimit, especially larger increases that have been proposed, is that the hardware and bandwidth requirements of running a full node will increase.

In my view, these changes in tradeoffs are likely net good. This is true for a few reasons:

1. Today, we are paying the costs of low node requirements (low gaslimit) but we are not actually getting the benefits (wide-scale personal full node operation)
2. 2010s-era thinking assumed symmetry between block production and verification: you can only verify by re-executing - which implies one class of node. Newer 2020s era technologies - access lists, statelessness, zk proving - all break that symmetry, and all have the format of one powerful actor doing more work to make verification much easier for everyone else.
3. Newer block building designs also introduce new forms of decoupling, eg. breaking up transaction inclusion authority (sufficient to ensure non-censorship) from optimal block building.

All of these factors hint in the direction of a more heterogeneous architecture, where some nodes become larger, but in exchange the ability to ensure core guarantees becomes accessible to many more people. **Even as full-node requirements increase, an Ethereum where most users’ wallets are running light clients that ZK-verify the chain is slowly coming within reach**.

However, if we start going in this direction, we need to be very clear about what our underlying goals in terms of decentralization are: what properties are we trying to give to users, and what red lines are we not willing to cross?

This post will sketch out one framework for thinking about this.

I will define three types of nodes:

- Light node: sufficient to (i) verify the chain, including correctness and availability, and (ii) access any needed data privately, assuming the existence of at least 1 honest heavy node (for liveness; safety is unconditional)
- Medium node: any type of node that Ethereum has a n/2-of-n trust assumption in (eg. attesters in staking, FOCIL)
- Heavy node: any type of node that Ethereum has a 1-of-n assumption in (eg. optimal block building, proving)

FOCIL goes in the medium category because even though the trust assumption is not quite n/2-of-n, it’s definitely bigger than 1-of-n: we want lots of people to participate in FOCIL honestly to ensure rapid inclusion guarantees.

A possible rubric for these might be:

- We want running a light node to be so trivial that it is included in browser and mobile wallets by default (as well as newer categories of clients like eg. AI agent frameworks that specialize in blockchains)
- Running a medium node should cost roughly what it costs now, maybe a little more but not too much more
- Running a heavy node can be more resource-intensive (because we only need one of them to be honest for Ethereum to work), but we still need to put some limits to ensure a competitive market

The latter category will likely be the most controversial, and I expect heavy requirements on block building will be more controversial than equally heavy requirements on proving (because proving is a “dumb pipe” task, there is no way to “abuse the authority”, whereas even with FOCIL a malicious dominant block builder can do some damage).

If we want to set limits, we can start asking the question: what is the goal of those limits? Some possible answers are:

- Fixed costs should be low enough to ensure a highly competitive market
- Energy requirements should be low enough to run from a home (ie. max ~15 kW), so that Ethereum is strongly protected from dependency on data centers, which are easy censorship choke points

One tricky one to think about is internet (both bandwidth and latency). Having reasonable bandwidth and latency requirements is critical to geo-decentralization and censorship resistance, but what requirements are reasonable is more difficult to measure - there isn’t a clean equivalent of “for $30,000 you can buy an H200”. For many people in many locations, internet bandwidth above a certain speed is not available at all. Internet is also challenging to rely on because, unlike hardware, it can be easily and suddenly taken away. Finally, we do not want to become wholly dependent on one type of internet (eg. Starlink). **In general, we should probably be more conservative on bandwidth than on hardware specs**.

This is a sketch with numbers still to be filled in, and even some of its underlying assumptions are perhaps disputable (to give one example of many: FOCIL has strong consensus within some circles, but other circles have barely even started thinking about it - and if we don’t do FOCIL, that has implications for optimal block building)

We need to get to a much clearer collective view on our answers to these questions ASAP. The answers will define both what L1 gaslimits are safe, and what EIPs are most important to prioritize to maximize the gaslimit/decentralization tradeoff curve.

## Replies

**LefterisJP** (2025-04-30):

Hey V, thanks for writing those out a bit.

This seem to focus on only one type of node. The type of node that follows the chain and is used for either staking or normal usage. And then try to split is into the subcategories of light/medium/heavy.

I would split nodes further into these categories that come in mind:

- follower node. Just for normal usage and keeping up with the chain.
- staking node. Used for staking.
- historical noded. Used to access historical data

### Follower node

The follower node can be either light or heavy, matching what you mentioned above. But I would assume in the absence of staking, the incentives are not there to have anything but a light node.

### Staking node

The staking node is divided into two so far from our experience. Local block building staking node and one that uses mev-boost and pushes the block building to 3rd parties.

Having increasing hardware requirements, for either of these is not bad imo. Anyone that puts up the capital of 32 > ETH should be able to afford it. Having a bit more beefed up machines is not a problem, so long as it stays within sensible size limits that can run in a residential location.

The biggest difference between the local staker and mevboost staker is bandwidth. There was some measurements (I don’t have links in handy) but the difference is quite big (when we cross 50 mbps upload bandwidth required, limitations hit). And bandwidth requirements is the one thing we can’t easily pay for if you want to have stakers run from home **and** have geographical diversity. As there is many areas around the world with insufficient infrastructure.

So power and bandwidth requirements are what can hurt us here and we need to find a good balance.

The problem I see is that there is no incentive to run a local builder vs a mevboost proposer. You can still run mevboost at home, even in places with VDSL (and not fiber) so 250mbp down/50 mbps up and you make more money than running a local builder. Win/win.

So the incentives here keep pushing the local builders towards big actors, or data centers and centralization. That’s something I fear about.

### Historical node

The ability to be able to query the history of the chain, and now with all the L2 of all these chain is essential. You need to be able to see what was the stated on 30/04/2021 on a given contract. It’s essential for accounting, for taxes, historical processing and generally book-keeping.

But right now it’s very hard. Running an archive node per chain is super expensive and non-trivial for end-users. On top of that it’s not enough. Even if you run an archive node you can’t get the answer to some really basic questions:

1. Give me a list of all the transaction hashes that an address appeared in. Essentially tell me my history.
2. Give me a list of all the withdrawals to an address
3. Give me a list of all the blocks proposed by an address (as a fee recipient)
4. Turn a block number to timestamp and vice versa
etc.

At the moment lll these require extra expensive indexing on top of an archive node. Per chain. Even for devoted individuals this becomes too expensive and too much work to maintain.

Which is why we all end up centralizing the fetching of these data around indexers such as etherscan, blockcha.in and other centralized APIs.

I don’t have a solution here. But I see this as a big problem, I have been talking about for years now as someone writing local applications analyzing the chain.

The continuous centralization of historical queries to external centralized indexers, even if you run your own archive nodes is scary for me and I am afraid that a few years down the line we won’t even be able to double check stuff and what the 1, or 2 remaining centralized sources of data say will become the truth of what happened.

And that is too much power to put on any one or two entities.

---

**vbuterin** (2025-04-30):

Regarding historical nodes, what would you say is wrong about a world where:

- Maintaining a historical node takes more resources than before (eg. $5k)
- For people who don’t, they can query a specialized RPC node, and do so trustlessly (both in terms of guaranteeing correct answers and in terms of privacy). The RPC protocol is expanded to support more types of queries. There is an open protocol by which RPC nodes can charge ETH per 1000 queries
- History is stored on a distributed p2p network, which provides a highly distributed backup for history, guaranteeing that anyone with the resources can spin up a new archive node

This would make “truly local ethereum blockchain accounting” accessible to fewer people than today, but on the other hand it would make “trustless and privacy-preserving ethereum blockchain accounting” accessible to more people than today.

---

**vbuterin** (2025-04-30):

Would it be ok for you if 1 ETH nodes can participate in every task *except* block building?

So with a 1 ETH node you can attest (meaning, you are part of the set that can help block 51% attacks), you can participate in FOCIL (meaning, you frequently get assigned to a slot within which you can pick transactions from the mempool and guarantee inclusion of them within that slot), but you would have to outsource block proposal responsibility to someone else of your choosing.

---

**daniellehrner** (2025-04-30):

I would be very helpful to be much more concrete what is expected from the nodes.

**Light node**

I guess this mean very low hardware requirements, maybe a smart watch even and being stateless. I think that is not very controversial.

**Medium node**

What exactly is needed here? At least FOCIL currently requires the node to have the full state. Which means state growth is an issue. Also today in order to have the state the node needs to be able to execute the blocks themself to follow the chain.

Should the node not be able to execute the transaction it cannot be sure that it is successfully executable. At least I don’t know how to determine otherwise if the gas limit of a transaction is sufficient or not. The node can of course select txs without executing them, but what real value does FOCIL provide if many of the txs in the IL are garbage, meaning not successfully executable?

**Heavy node**

Again what is exactly needed here? Can a home staker be expected to run one? If no home staker can run one, what is the fallback mechanism in case the centralised block builders get taken down? On-chain estimates suggest that today we have around 10.000 home stakers with roughly the same number of nodes.  Should centralised players get shut down, we can fallback on those home stakers. The throughput will drop a lot, but having low throughput in times of distress is acceptable IMO.

Should only heavy nodes in data centers have the full state how would we even sync a new heavy node in case governments take down all the existing ones. We have 2 or 3 main block builders currently, Bitcoin has a similar number. What makes us think that this will change in the future? It seems extremely risky to rely on such low numbers of block builders.

I know WW3 resistance is a meme, but I think any future changes in node types needs a fallback mechanism. Today we can fall back to local block building in times of distress without missing a single slot. I just don’t see how this will be possible in the future.

---

**vbuterin** (2025-04-30):

> At least FOCIL currently requires the node to have the full state.

FOCIL can actually be designed to be stateless.

> Again what is exactly needed here? Can a home staker be expected to run one? If no home staker can run one, what is the fallback mechanism in case the centralised block builders get taken down? On-chain estimates suggest that today we have around 10.000 home stakers with roughly the same number of nodes

Suppose that we have 100 block builders, and other home stakers subscribe to those block builders via an open market (in addition to contributing directly to censorship resistance with FOCIL). Then, even if 99 of them get taken down, the network still works fine.

A new node would be able to sync by downloading history from a distributed history storage network (this does need to be built; it’s a critical part of the EIP-4444 effort).

> We have 2 or 3 main block builders currently, Bitcoin has a similar number. What makes us think that this will change in the future? It seems extremely risky to rely on such low numbers of block builders.

In the current market design, I don’t expect that it will change. The best that we can do short term is things like FOCIL to make sure censorship resistance is preserved even if no builders cooperate, and good backup block building options to make sure blocks still get built even if all builders go offline (I think this part is easy today). But long term, I think we do need to change the market design, and make sure that we consider all of the available options.

---

**pcaversaccio** (2025-04-30):

Dropping some first, potentially incomplete thoughts here:

- Given my current understanding of the landscape is that relying on specialised “Heavy” nodes wouldn’t just concentrate block building; it also potentially centralises ZK proving infra (i.e. requiring specific hardware/expertise), data availability mechanisms crucial for light clients & increases dependency on high-spec bandwidth which is inherently unequal and controllable. Maybe I’m a bit too paranoid here (but hey, only the paranoid survive long term :D), but each specialised, high-requirement role becomes now a potential point of failure/coercion; I’m thinking of a nice target for state-level adversaries or other concentrated economic actors. We’re not just managing one potential bottleneck (builders), but potentially creating several.
- While defining trust assumptions like 1-of-N (“Heavy”) or N/2-of-N (“Medium”) is necessary for analysis, we shouldn’t become too comfortable IMHO with them tbh. The core Cypherpunk goal remains trust minimisation. How robust do you think are these assumptions against sophisticated, coordinated attacks, or even just correlated failures (e.g., regional outages (hello Spain/Portugal), regulatory pressure on specific node types)? We should be scrutinising these assumptions continually, not just accepting them as parameters to be “managed” IMO.
- (caveat: that’s how I currently understand light clients): While pivotal for accessibility ofc, the security & privacy guarantees of light clients are fundamentally dependent on the integrity & availability of the heavier tiers and the infra serving them data/proofs. This dependency needs to be factored into the risk model; they don’t offer the same resilience as a network where more participants can independently verify.
- Remember the “Why”; the original promise of Ethereum was credible neutrality and censorship resistance (that’s my personal view and can differ probably from others :D). As we argue about gas limits and node structures, we need to constantly ask: Does this change make the system harder to capture or censor, or does it create new vulnerabilities? Are the scaling gains worth potentially compromising the fundamental reason many users trust and value Ethereum over permissioned systems? - I don’t have an answer for this yet.
- Instead of just finding acceptable limits for resource requirements, the discussion should perhaps focus more on minimising single points of failure and dependence on trusted entities. This might imply being more conservative on L1 gas limit increases than pure technical capacity allows, or prioritising EIPs that reduce node requirements across the board (like statelessness) over those that enable further specialisation, even if the latter offer seemingly easier scaling paths.
- To summarise a bit my view on this topic: The goal shouldn’t just be to manage decentralisation within a scaling roadmap, but to ensure the scaling roadmap doesn’t fundamentally undermine the properties that make Ethereum a platform worth scaling for a free and open internet.

---

**g11in** (2025-04-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> he scaling roadmap doesn’t fundamentally undermine the properties that make Ethereum a platform worth scaling for a free and open internet.

what are those properties?

so if you can ensure builder’s can’t censor (FOCIL) while ensuring a distributed set (credible neutrality) of validators can verify (ZK proof) while still have  a recourse to builder monopoly (some sort of viable local blockbuilding even if degraded) what else is left that you desire in ethereum as the underlying property

---

**daniellehrner** (2025-04-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Suppose that we have 100 block builders, and other home stakers subscribe to those block builders via an open market (in addition to contributing directly to censorship resistance with FOCIL). Then, even if 99 of them get taken down, the network still works fine.

I just don’t see a future were we even have 100 block builders. Even if we do, compared to the thousands of nodes today that’s 1 - 2 orders of magnitude less. Is increasing throughput really worth such a high price? I honestly don’t think so.

I honestly thought this kind of hardware requirements were meant for rollups only, they need it, Ethereum IMO does not. We already plan to 10x throughput within a year. Nethermind is testing a Gigagas network at the moment. I think we can still go do much faster with the hardware and bandwidth requirements that we have right now.

I know that research needs to see many years ahead, but it just seems to me that making local block building viable for home stakers is just not a goal anymore and AFAIK nobody is even looking into it.

From the outside it seems that centralised block building is the only way forward and nothing else is even considered anymore.

---

**LefterisJP** (2025-04-30):

Something like this would not be bad, and costing more to run is not a problem. The main problem is that it costs way too much to run and there is no “perfect indexing” mechanism yet.

I think that these should move into the node, and we should very accurately define those historical nodes and their specs too.

So if someone wants to and can should be able to run a node with specific parameters and get all that data.

At the moment this is not possible. The ability to charge via the RPC in a standardized way would be quite cool, as this could potentially add incentives to running such nodes!

---

**pcaversaccio** (2025-04-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/g11in/48/3906_2.png) g11in:

> what are those properties?
>
>
> so if you can ensure builder’s can’t censor (FOCIL) while ensuring a distributed set (credible neutrality) of validators can verify (ZK proof) while still have a recourse to builder monopoly (some sort of viable local blockbuilding even if degraded) what else is left that you desire in ethereum as the underlying property

Good question - I believe if we can guarantee CR (yes, FOCIL is good), scalable trustless verification (ZK, but those proofs can become still a bottleneck), and avoid structural centralisation in key roles (via market competition & fallback paths), we’re close. But IMHO the missing part is ensuring those guarantees are *globally accessible* and *permissionless to participate in* at every tier of the stack. That’s why even *invisible* things like bandwidth or client diversity matter. Not because they change the rules, but because they determine who gets to play.

---

**soispoke** (2025-04-30):

Some thoughts about [FOCIL](https://eips.ethereum.org/EIPS/eip-7805):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> One of the unavoidable consequences of raising the L1 gaslimit, especially larger increases that have been proposed, is that the hardware and bandwidth requirements of running a full node will increase.

I don’t want people to get the impression that FOCIL is somehow designed to push forward a scaling roadmap, it is not. The core proposal of FOCIL is to rely on multiple parties amongst the more decentralized validator set ***to preserve Ethereum’s censorship resistance properties*** by constraining sophisticated builders and force them to include transactions so they can’t arbitrarily censor.

Yes, the increased CR given by FOCIL can then be considered as a first step towards decoupling local block building from CR responsibilities, but we would also crucially need a good CR mechanism for blobs, and a way to be resilient against liveness failures if we were going towards this direction anyways. Whether FOCIL belongs in the light or medium node category (if that’s how we want to frame things in the first place, there are [many](https://ethresear.ch/t/unbundling-staking-towards-rainbow-staking/18683) [possible](https://ethresear.ch/t/three-tier-staking-3ts-unbundling-attesters-includers-and-execution-proposers/21648) [variations](https://ethresear.ch/t/rainbow-roles-incentives-abps-focilr-as/21826)) doesn’t matter much right now imo (as in, for the current proposal), because we would need to answer

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> FOCIL goes in the medium category because even though the trust assumption is not quite n/2-of-n, it’s definitely bigger than 1-of-n

h/t [@Julian](/u/julian): Where exactly FOCIL is in the spectrum of 1-of-n or n/2-of-n doesn’t matter so much, we can adjust the mechanism either way (we can increase the number of includers per slot, or the size of ILs, etc)

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/db5fbb/48.png) daniellehrner:

> Medium node
> What exactly is needed here? At least FOCIL currently requires the node to have the full state. Which means state growth is an issue. Also today in order to have the state the node needs to be able to execute the blocks themself to follow the chain.

A FOCIL node doesn’t need to execute transactions and also doesn’t need to hold all the state so it could potentially fit in the light node category as well. Ideally, we go towards a future in which home operators can participate in preserving Ethereum’s CR with very low hardware and bandwidth requirements, I personally think we can get there. Here’s a recent proposal in which nodes only have to store the minimal data required to preserve CR and maintain the public mempool called [VOPS](https://ethresear.ch/t/a-pragmatic-path-towards-validity-only-partial-statelessness-vops/22236).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> to give one example of many: FOCIL has strong consensus within some circles, but other circles have barely even started thinking about it

Genuinely curious to know more about what circles that have barely even started thinking about it? FOCIL isn’t really user facing, and we have talked a lot with core devs, researchers, builders, searchers, and MEV people. But if anyone reading this wants to learn more or has questions feel free to reach out anytime.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> transaction inclusion authority (sufficient to ensure non-censorship) from optimal block building.

More generally, I want to make sure people realize that yes, FOCIL introduces a new role and a new primitive, specifically by imposing constraints on builders, and allowing multiple validators to have a say in what goes in Ethereum blocks to preserve CR.

People can then build on FOCIL and extend it to serve other purposes, but it’s confusing to tie FOCIL to scaling or even privacy considerations as it’s all a bit speculative for now.

The question should be:

- Do we think Ethereum’s current CR is good enough? I think there is broad consensus, and the answer is clearly not.
- And then, do we have many proposal  that address this specific issue? I don’t think so. I think we have one, FOCIL, that’s been researched for years and now implemented by 4 clients. I would really like to know if there are specific concerns about the proposal itself though.

I also want to strongly make the point that there are no viable alternatives to FOCIL out there today, people can bring up ideas like MCP ([one post](https://ethresear.ch/t/concurrent-block-proposers-in-ethereum/18777), nothing on the actual way to merge different blocks together) or BRAID (promises of a revolutionary paper by Devcon Bangkok but really just some [abstract slides](https://www.youtube.com/watch?v=mJLERWmQ2uw) from Max Resnick). In reality it’s unlikely MCP will “solve MEV”, and if they want to do so they introduce latency by using slow cryptography, or additional rounds of consensus, and in any case can’t prevent the last look problem and colocation with centralized exchanges.

So the only alternative there is right now is just letting 2 block builders completely control block contents and censor transactions without any safeguards.

---

**potuz** (2025-04-30):

Just two brief comments.

- I think the list separation in three subsets (light=stateless, medium=statefull but can’t execute/prove full blocks, heavy=can execute and prove blocks) is lacking a crucial player, those that want to execute at the tip of the chain but can’t prove. The difference between executing and proving is quite large and it is going to continue to be large for the foreseeable future. Allowing users of the chain to run a node at home that can follow and execute the chain, even though they won’ t be able to prove and therefore produce blocks, is still a feature that I think it is crucial to maintain in Ethereum, unless a bullet proof solution for trustless, privacy preserving and always available RPC providers is found. Since this last problem is definitely not solved even in research, I would suggest that we clarify what are the current plans towards what can be actually done at home. I’d say that having a stateful FOCIL includer that can only execute a few txs from mempool and can verify the ZK proof but cannot execute the tip is not what we should aim for. Trustless execution at the tip of the chain is something that we should not give up on.
- The other topic which is relevant to this discussion but not directly and that is usually not addressed at least to my satisfaction without handwaving about non-existent cryptographic primitives in the Beam-Type upgrades is that of aggregators. If we want to move to a world in which we have fast slot times and fast finality, with a large attester set, we still need to handle aggregation, which still needs to be decentralized as it’s an integral part of the attestation security model. However, aggregating requires proving (albeit not the same as full block proving) and I haven’t seen any actual quantification of these two contending forces: we want a highly decentralized set of aggregators chosen from light attester sets, and at the same time they need to run hardware that is fast enough to prove and broadcast these aggregates.

---

**MicahZoltu** (2025-04-30):

Minor note while I read: I feel like this should have been posted on ethresear.ch rather than ethereum-magicians.  I (and I suspect others) are subscribed there because it is *relatively* low volume, but I’m not (and I suspect others are not) subscribed to this forum because it is high volume due to being the place that every EIP discussion thread goes.

For primary Ethereum Research, it feels like we should keep discussions consolidated there in the future, or officially abandon it for this one and make it easy for people to selectively subscribe to certain subjects.

---

**MicahZoltu** (2025-04-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> assuming the existence of at least 1 honest heavy node

I think a critical addition here would be “assuming the existence of at least 1 honest non-censored heavy node”.  If I am running a light client in Iran and I am unable to access the one heavy node located in the US because the US government has mandated that US service providers must block all Iranian connections, then having 1 heavy node doesn’t do me any good and I’m unable to use Ethereum.

Another scenario where censorship can come into play is people blocking entire countries at the IP level because DoS attacks are coming from those networks and banning swaths of IPs is easier than other filtering solutions.  As someone who exclusively uses a VPN, I am frequently victim of this sort of behavior and if the only heavy nodes around are engaging in this sort of censorship there may be users who are cut off from Ethereum due to no fault of their own.

Also, specific pieces of data may be censored by the heavy node like access to the Tornado contracts.  Assuming we don’t have privacy at the data access layer, then you can run into problems where censorship isn’t of the light node itself, but rather the data they are trying to access.

When we have 1/n assumptions, I think we need to make it very clear/explicit how available/accessible that 1 needs to be, because I don’t think it is necessarily a given that we will get even 1 that meets all of the necessary requirements once they are spelled out (see below for more discussion on this).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> low enough to run from a home (ie. max ~15 kW)

This seems incredibly high to me, on the scale of low-end datacenter.  I have a home solar setup that is *way* overbuilt and it is still only 12kW max, that includes energy to charge batteries for overnight, and I don’t get anywhere near maxing it out.  On top of that, in 230V countries 60A breakers are probably the most common for *your entire residence* with individual circuits with outlets being maybe 20A, 30A at the high end.  30A @ 230V is only ~7kW.  The situation is worse in 110V countries where you are running essentially ~half watts over the same size wire (since amps are a function of wire size essentially).

I don’t think it is reasonable to consider someone having to rewire their entire house to run a node to be “home operator”, that crosses the line into datacenter pretty strongly for me.  Note: Upgrading this requires changing out wires, usually embedded in walls, not just swapping a breaker in a panel.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Fixed costs should be low enough to ensure a highly competitive market

I think that before we can have a meaningful conversation about this or the ongoing costs (energy, bandwidth) we need to agree on what demographic we want to be able to operate each type of node.  Some example demographics/personas:

- Web: Has a mobile device or low power netbook.  They won’t install anything, but they’ll open web pages.
- Home Desktop: Has a machine you can buy at a big box store recommended by a salesman.  They won’t buy any extra hardware or engage in any operational work, but they will double click an installer.
- Gamer: Has a top end machine but probably fully utilizes it regularly.  They can contribute a lot of power but are unwilling to use their whole machine for Ethereum only.  They may have a big drive or two, but they are probably half full already.  Will install software and may engage in some light operational work, probably has above average internet but needs to be able to limit Ethereum client usage at times.
- Minnow Enthusiast: Not rich, but willing to buy hardware dedicated to Ethereum if costs are “low”.  Will actively engage in operational work and is willing to have hardware that only runs Ethereum stuff.  Still has shared home connection though, limiting bandwidth availability.
- Whale Enthusiast: Wealthy and willing to buy hardware dedicated to Ethereum, costs don’t really matter.  Likely doesn’t engage in operational work like the minnow and may have extended outages, but can buy a dedicated internet connection and maybe hire someone to one-time rewire their house to run high watt lines to power a powerful host.
- Company: Has financial incentives to see Ethereum be successful, but is averse to legal risks.  Their operations are known and if a government announces that doing X is illegal they will immediately stop doing X even if the government’s position is likely to be found to be unconstitutional (or similar) in the future.  Likely runs in a datacenter or has their own datacenter.  Has staff to deal with any operational issue and can maintain high uptime.  Unlikely to be widely distributed around the globe, but willing and able to buy whatever hardware and bandwidth is needed to complete a given task.  Legal risk aversion makes them unwilling to provide uncensored access.

It is worth noting that in this list, there isn’t a persona that would be able to run an uncensored heavy node as I understand it from this thread.  The last two can run heavy nodes, but the company will censor if asked and the whale doesn’t have the free time to ensure high uptime or carefully construct anti-DoS filters (they likely will just blanket ban IPs by country).  The minnow is the ideal candidate for running uncensored software, but they don’t have the money to run the beefy infrastructure implied here.

One can imagine some hypothetical enthusiast who wants to spend all of their time fine tuning their Ethereum node and also has absurd amounts of money to throw at hobby problems, but in my experience such people generally don’t exist, at least not in the volume necessary to have the network rely on for 1/n assumptions.  Your average linux kernel hacker is generally not a retired billionaire, it is young people before their career or family takes over their lives, or people who want a simple life not chasing wealth, or ideologues who have decided making the world a better place is more important than getting rich.

---

**green** (2025-04-30):

> Note in this post: I had skimmed over the thread and started typing but I missed the topic. I think the writeup is still related to the thread title “Decentralization goals” as it reframes the idea of “just pump gaslimit” into “price resources properly”. But now after reading again I realized you were focusing on hardware to figure out how much leeway is there to increase the gaslimit. I don’t think the issues will be solved by insisting on the idea of hardcoded costs on a bigger volume, but since my post is a bit out of scope you can ignore.

If you want to scale Ethereum, you need to think about the worst case. Multiplying gas x100 is a bad idea. The fundamental problem in Ethereum scaling is resource pricing: the cost of resources is not related to its price.

There are various resources:

- Storage creation (if clients need to store N + 1 elements)
- Storage upkeep (how long will clients need to remember something?)
- Storage diff
- Storage access (applies for reading storage, account balances and bytecode)
- Memory (creating and reading temporal memory)
- Max memory (how much are clients expected to track in the same tx context?)
- Bandwidth (how much needs to be transferred around the internet? Txs and their calldata, blockhashes, PoS consensus stuff…)
- Compute (either in the EVM, ECDSA or other precompiles)

These resources are priced according to hardcoded rules, and that means that a series of ugly patches have been applied to prevent everything from collapsing. For example, loading account bytecode (as in, loading a contract) is artificially cheap. If it was priced the same way as cold   SLOAD are, it would be very expensive. So there were attacks loading contract bytecode, and this ugly patch was made: [EIP-170: Contract code size limit](https://eips.ethereum.org/EIPS/eip-170)

There is no flexibility on how these resources are priced. A way to fix the problem is pricing each resource with its own token, and controlling the issuance rate and maximum usage per block of those resources.

Another is to have different measures of gas per resource (the resources outlined above), and have the clients vote dynamically the price of those tokens. This is what I’m going to propose below.

Example:

We have this price chart

- Storage creation: 50_000 gwei per word (note that e.g. when you SSTORE a slot 0 → !0, that’s two words, key and value!)
- Storage diff: 5_000 gwei
- Storage cold access: 500 gwei
- Memory: 5 gwei per create/read
- Bandwidth: 100 gwei per 32-byte word
- Compute unit: 0.05 gwei (like, ADD spends 1 compute unit. but you could have ECDSA spend x20000 compute units)

Let’s leave storage upkeep pricing out because I don’t know how I would tackle the problem without needing a time tracker per word, although this could be a convenient solution.

In this model, Creating or reading smart contract bytecode would be priced the same way as storage! Mind this if you storage is too cheap.

And we have these limits:

- Max Storage creation per block: 10000 slots worth (note this would effectively mean max contract size is 320 KB)
- etc etc I think you get the point.

The idea here is our block proposer chooses the TXs, and as part of the PoS the clients get to vote to raise, maintain or lower a threshold per every resource. If the network believes storage is underpriced because the state growth is getting out of control (like it is right now), then they can raise the price. Or they can charge more per year of word storage.

The other grand problem with Ethereum is there’s no sort of garbage collection. All ideas to remove state got broken because they could cause issues, such as gas refunds being an attack vector, SELFDESTRUCT, etc. The garbage needs to be removed. There’s way too much state in Ethereum and there seems to be no way to get rid of it. Here’s a fictitious example of rubbish all clients need to remember:

> address(0x14b0…2904) has 12.135 FROG, a forgotten 2017 shitcoin.

If someone wants this trash to be in the protocol, and wants all clients to remember it, they must pay for it, because having the “biggest computer of the planet” remember 64 bytes of garbage does not come for free. This is even worse in the case of smart contracts.

- If Selfdestruct is changing way too much storage in many clients, don’t remove the option, just price it accordingly.
- If SSTORE !0 → 0 is allowing people to do a massive attack thanks to the refunded gas, just don’t refund the gas until the end of the transaction. And only refund a portion of it.

If Storage was properly priced, we would immediately see the effect of application developers being more responsible with their gas usage, designing contracts that can remove unneeded information. The storage required to hold the bytecode of smart contracts would have to be paid for, as with all storage it needs an upkeep to keep clients from removing it.

---

**CelticWarrior** (2025-05-01):

Rather than arbitrarily deciding that operating a medium node should cost roughly what it costs today, it might be better to understand what kind of economics home stakers are experiencing by not just focusing on the cost side (i.e. hardware + bandwidth) but also focusing on the revenue side (i.e. how many validators are they running) and overall profitability.  It may be that the vast majority of home stakers could tolerate a 2-3x increase in their internet costs with minimal impact on their profitability by requiring them to have the fastest connection available in their region.  We should be explicit in stating that staking on a toaster in the desert is not supported and that the expectation of stakers is that they have good hardare and a better than average internet connection.

---

**MicahZoltu** (2025-05-01):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/b2d939/48.png) magicians:

> with moore’s law these can increase

They cannot.  The system was designed under the assumption that Moore’s Law will hold and that is why unbounded state growth was allowed.  Just to *maintain* hardware requirements denominated in human labor we need Moore’s Law to continue.  If we want to go beyond that then either tech advancement needs to outpace Moore’s Law or we need to address the unbounded state growth problem.

---

**vbuterin** (2025-05-02):

We do have an open option for solving state growth if we want to:

Strong statelessness (aka. tx-level mandatory access lists). Transactions have to specify the state objects they access and provide proofs for them.

This would allow even block builders to be stateless (or alternatively, hybrid architectures where eg. state that is less than a year old is assumed to be held by a larger number of nodes, but for any older state you’re personally responsible for it, though we could have a distributed p2p network for it)

I don’t think it’s needed short term, because history is a bigger issue and we should focus on distributed history storage first (state only grows by ~30 GB per year, history ~5x as much), and history is easier to solve distributed storage for. Even with 100x higher gas limits, state would grow by ~3 TB per year, which $1k of hard drives can hold for a decade (eg. https://www.amazon.com/Seagate-Exos-Enterprise-Internal-Drive/dp/B0CM293XCL/). But in the long term, strong statelessness is an available option.

---

**Pmatt328** (2025-05-02):

As home staker I agree, storage is a false problem at least in my opinion

---

**kladkogex** (2025-05-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> I don’t think it’s needed in the short term, because history is a bigger issue and we should focus on distributed history storage first (state only grows by ~30 GB per year, history ~5x as much).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> I don’t think it’s needed in the short term, because history is a bigger issue and we should focus on distributed history storage first (state only grows by ~30 GB per year, history ~5x as much).

One important thing to understand is that the challenge is less about storage capacity and more about database architecture. Most clients use LevelDB as the key-value database for storing state. LevelDB is quite efficient, and there are few viable alternatives.

LevelDB stores key-value pairs in read-only “level” files, organized by generation.


      ![](https://blog.senx.io/wp-content/uploads/2018/11/cropped-android-icon-192x192-32x32.png)

      [SenX – 17 Sep 19](https://blog.senx.io/demystifying-leveldb/)



    ![](https://blog.senx.io/wp-content/uploads/2019/09/LevelDB.png)

###



LevelDB is the storage library used in the standalone Warp 10 version. Learn how it works and how to read its LOG in the Most Advanced Time Series Platform.



    Est. reading time: 7 minutes











I won’t go too deep into the architecture of LevelDB, but the key point is that these level files are periodically compacted (i.e., merged). As the database grows, large files occasionally get compacted at random times. This can cause the database to stall intermittently. As a result, historical nodes with larger states and databases will fall behind regular nodes with smaller databases.

To solve this problem, clients will need to adopt a more advanced architecture, where LevelDB is split into multiple shards (e.g., by the first bytes of the key). If you use, say, 32 shards, then you can utilize 32 CPU cores in parallel, and each shard’s database will be 32 times smaller. Additionally, you can spread the data across multiple SSDs, improving read/write bandwidth by a factor of 32.

If LevelDB remains monolithic, then only a single core is utilized during database updates, and moving to a more powerful machine won’t help the historical node keep up.

So, the key point is that the challenge is not so much about storage requirements, but about re-architecting clients into a parallel, sharded database architecture — which is significantly more complex to engineer and QA.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/b/ba31df179f2727793423087e7c8b4700adf880a3_2_690x385.png)image953×533 74.8 KB](https://ethereum-magicians.org/uploads/default/ba31df179f2727793423087e7c8b4700adf880a3)


*(12 more replies not shown)*
