---
source: ethresearch
topic_id: 5075
title: Evidence-Based Subjective Logic and Sybil-resistance
author: liamzebedee
date: "2019-03-01"
category: Applications
tags: []
url: https://ethresear.ch/t/evidence-based-subjective-logic-and-sybil-resistance/5075
views: 3202
likes: 5
posts_count: 9
---

# Evidence-Based Subjective Logic and Sybil-resistance

A couple months ago I was reading a paper called [Flow-based reputation with uncertainty: evidence-based subjective logic](https://link.springer.com/article/10.1007/s10207-015-0298-5). I think it’s a pretty unexamined piece of research for what it presents, which is a reputation algorithm that can compute across **arbitrary trust networks**. I’d love to get others opinion of this in the light of Sybil-resistant design - for which PoW-style control mechanisms look to be the only currently effective approach.

To give a brief overview of EBSL:

- Subjective Logic is an algebra for computing “subjective” qualities. It deals with opinions, which are tuples of the form (belief + disbelief + uncertainty) = 1, and has a couple operators such as discounting (used for transitive trust) and fusion/consensus (for combining opinions).
- SL can be used to model trust networks, where relations are defined as opinions of trustworthiness. Given a set of opinions, a fixed-point convergence algorithm (similar to PageRank) can be used to arrive at a reputation matrix. However the algorithm for computing the flow of trust is flawed (see more in the EBSL paper).
- Evidence-Based SL (EBSL) solves this issue and also introduces a more natural primitive of evidence. I’m not sure of the terminology of domains, but opinion components range 0-1 and evidence is just an integer (so it’s an absolute rather than relative metric, if that makes sense). They define a mapping between the two, and also introduce discounting/consensus operators that can converge trust flow over arbitrary network structures.
- You can give evidence or an opinion to the convergence algorithm, although the former I’d argue is more organic. The original simulation used evidence amounts between nodes to compute the reputation, which in modelling P2P downloads for example (as in the original EigenTrust) scales better than adjusting a reputation opinion for every node.

I’ve reimplemented the algorithm [here](https://github.com/liamzebedee/retrust) (logic in `ebsl/lib.py`), based off of the code that the authors kindly forwarded me (also in the repo). In `simulations/main.py`, I’ve done some work simulating Sybil networks and how they can inflate their rep in the eyes of other users. In a highly-connected network of honest nodes and a Sybil network of relations, the honest network’s perception of Sybil’s reputation scales only *linearly* with every honest node you convince.

I’d like to share and encourage others to experiment - I’m not a trained mathematician by any means, more of a hacker - but it’s the first model I’ve seen which seems to be Sybil-resistant and be able to handle **reconfigurations of trust networks** in a versatile manner.

What’s possible is modularising reputation providers, such as Uber/Lyft. Let’s model Uber as a reputation network, wherein we trust them to administer/bootstrap the initial reputation of riders/drivers. Riders get their initial reputation by tying their identity to a phone/credit card no., and drivers also undergo initial license checks etc. Thereafter the usual mutual rating system occurs, and the system can filter out bad actors.

In a decentralized version, we would still have a reputation provider ‘dUber’, but their role would be reduced to simple attestations of identity, license checks, etc. Riders/drivers could require a proof-of-location for their rating of an exchange to be counted (since it’s a physical exchange). Modelling interaction, all drivers/riders in the trust graph are connected by their edge to the dUber org, trust flows and we can get the trust of users we haven’t interacted with.

Because dUber is just another edge in the graph, we can replace/augment our worldview with information from other providers/networks (ie. Lyft). If they behave maliciously, we can adapt the network without the usual inertia of large reconfigurations of social relationships.

I think this could be an interesting orthogonal to proof-of-stake/work and general consensus algorithms, and just want to get some discussion going in any case.

## Replies

**miles2045** (2019-03-02):

Similar to e-voting mechanisms, subjective trust networks need bribery-resistance mechanisms to work well in my opinion. If reputation can be easily bought, for instance, then that isn’t a super effective reputation system in many cases as it’s functionally a plutocratic social consensus algorithm. Fortunately, progress is being made in this area of research. Phil Daian et al. recently proposed a [scheme for bribery-resistant voting](https://ethresear.ch/t/bribery-resistant-voting-schemes-for-smart-contracts/3354) using secure enclaves, for example.

---

**liamzebedee** (2019-03-03):

Haha thanks, Miles ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=9) ! I’m well aware of the possible bribery attack. Discussion you linked was great, I’ve also been researching zk DAO’s so it’s a good parallel.

I’d ask - is vote bribing moreso a domain problem? In the scenario of a marketplace, assuming some proof that distinguishes authentic interactions from fake ones (ie proof of location during a ride), bribing users for better ratings still requires some cost of proving rides were authentic.

---

**yondonfu** (2019-03-05):

Flow based reputation systems that result in local views of the network seem like a promising alternative to reputation systems that try to converge on a global leaderboard.

- Is the investigation of EBSL over insurance based distributed trust systems such as TrustDavis motivated by a desire to minimize the economic costs of bootstrapping trust? If so, it seems that in systems where users “stake trust” (I saw this terminology in your GH repo), users will always be able to sell the stakable trust whether it be by selling a transferrable token or by selling access to a private key which has acquired some amount of trust (assuming users are identified by addresses). As a result, there would end up being an economic cost (i.e. the opportunity cost of not selling your stakeable trust) in bootstrapping trust i.e. it is actually costly for me to stake trust to you
- In certain domains such as computational marketplaces, the protocol could define clear slashing conditions triggered by a cryptographic proof. If these marketplaces were powered by a trust system in order for users to determine which providers to use, perhaps a single triggered slashing condition can lead to a chain of reputation decreases for all nodes that staked trust to the faulty provider as well as any nodes that staked trust to those nodes.
- I wonder if there is utility in overlaying EBSL (or any other flow based reputation system) on top of an existing PoS system (using PoS in the general staking sense and not in the context of a blockchain consensus protocol). The underlying PoS system would bootstrap an initial set of providers for a marketplace that fulfill some base level of economic security (perhaps due to a minimum stake requirement + slashing conditions). The overlay EBSL system would then serve as the basis for provider selection mechanisms executed by users

---

**miles2045** (2019-03-05):

For certain applications, I think that requiring proofs of authentic interactions can definitely make bribery attacks less scalable. To use the ride-sharing example you shared, however, a passenger who has been permitted to rate a driver by providing the location proof (which I think is a neat idea) can still prove to others how they rated the driver and therefore they can sell their ratings via trust-minimized escrow smart contracts.

On that note, I’m super interested in subjective trust network and DAOs (…subjective DAOs) so I would love to learn more about what you’re working on. My twitter is [@miles2045](/u/miles2045) if you want to connect.

---

**liamzebedee** (2019-03-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/yondonfu/48/3265_2.png) yondonfu:

> Is the investigation of EBSL over insurance based distributed trust systems such as TrustDavis motivated by a desire to minimize the economic costs of bootstrapping trust? If so, it seems that in systems where users “stake trust” (I saw this terminology in your GH repo), users will always be able to sell the stakable trust whether it be by selling a transferrable token or by selling access to a private key

Yes, it’s about eliminating the economic cost. TrustDavis is pretty cool, in that they model reputation with inherent stake attached - which can be used to directly approximate the risk in transactions. I like how they strap-on the incentive system of payments for reviews.

However, where is their explanation of how they process claims in a distributed manner? Otherwise, I don’t see how this can scale effectively (as a counterparty will always claim the good was not faulty, etc).

---

**yondonfu** (2019-03-06):

IIUC the claims could just be processed as local social agreements i.e. Alice has published a $100 reference for Bob and sells that reference to Charlie.  Alice agrees to pay Charlie $100 if Bob sells Charlie a faulty good. Charlie has no guarantee that Alice will actually pay him $100 if Bob sends a faulty good. Ideally, Charlie would buy a reference from someone that he has established trust with already (i.e. direct neighbor in the graph) and for whom Charlie has also published a reference either due to the established trust or because the person left a security deposit with Charlie (the paper mentions this mechanism in order for new entrants to get their first references). In the scenario where Alice doesn’t pay Charlie for a reference when Charlie declares a faulty good then: if Alice left a security deposit with Charlie then Charlie claims Alice’s security deposit and if Alice did not leave a security deposit with Charlie then Charlie misplaced his trust in Alice.

---

**liamzebedee** (2019-03-11):

On the note of vote buying, and interesting train of thought I’ve been developing from yesterday’s talk at EthCC from [Iden3](https://iden3.io) - **non-transferable** zk-proofs. A non-transferable proof means that a user can prove to another user their reputation, without risking that information being leaked. Apparently Vitalik discussed this idea and they’ve built it out - you generate a ZK proof of your reputation, which is OR’d with your private key. You can thus only verify the proof only if you know the private key.

Vote buying as a problem is generally just a subversion of the reputation score. To approach it, you can attempt to penalise or attach a cost to nodes giving ratings that aren’t consistent in intention with their other ratings.

Probably something with ZKProofs will be the solution. You want the votes to be private, but your reputation to be public.

- proof that you rated an interaction
- proof of reputation and proof that it’s linked to all interactions people have had with you

To mitigate vote buying, you basically invert your model of reputation from being public-by-default to private-by-default. To build reputation, you rely on proving your previous interactions to other users.

---

**Steake** (2025-10-11):

# “Shadowgraph” - EBSL via ZKML for DPKI-WoT

## Reputation Gated Airdrop

I’ve followed this line of work for years and have been building a concrete variant I call **Shadowgraph**—a ZKML-backed, reputation-aware identity & airdrop stack. I’d love eyes on the cryptography, circuit design, and mechanism incentives. (Note: the ref repo is an **PoC and incomplete WIP Frontend**: github/Steake/Reputation-Gated-Airdrop

## TL;DR

**Shadowgraph = ZKML + blockchain = hyper-dimensional social graph with verifiable reputation.**

Off-chain we compute **EBSL** (Evidence-Based Subjective Logic) over a time-decayed trust graph; on-chain we verify succinct proofs of **set membership**, **one-per-epoch nullifier**, and **“score ≥ τ / allocation = f(score)”**—no raw graph data leaks.

## Sketch

- Identity & attestations. Users hold a DID-style bundle (liveness, work/contrib proofs, social attestations) merklised into C_id. Membership is proven via Merkle/accumulator; Semaphore-style nullifier enforces one claim per epoch.
- Reputation (EBSL). Map evidence (r,s) → opinion (b,d,u) with Dirichlet prior; fuse via SL/EBSL ops (consensus/recommendation), apply time decay, edge reliability, and anti-sybil regularisers (e.g., low-conductance penalties). Export a scalar R∈[0,1].
- ZK proofs.

 π_id: set membership
- π_null: correct epoch nullifier
- π_rep: correct inference over a curator-committed snapshot (snapshotHash) and a published model/circuit (modelHash), asserting R≥τ or allocation = f(R).
Circuit path: (a) pure algebraic EBSL; or (b) a small quantised NN that approximates EBSL for scale.

**Mechanism.**

- Gate: threshold + flat mint; or smooth curve with caps, e.g. min(A_max, A·log(1+αR)).
- Collusion/Sybil: one-per-epoch, non-transferable attestations, ZK non-verifiability of private features to depress bribery value.

**On-chain interface (sketch).**

```auto
function claim(bytes calldata proofId, bytes calldata proofNull, bytes calldata proofRep,
               bytes32 modelHash, bytes32 snapshotHash, uint256 epoch) external;

```

## What I’m asking

1. Circuit-friendly EBSL operator pitfalls you’ve hit (discounting/consensus composition, range bounds, overflow discipline).
2. Privacy-preserving sybil regularisers you like for penalising low-conductance clusters without exposing graph cuts.
3. Best practice for binding large, partially redacted feature matrices to a single snapshotHash (avoid selective disclosure / model-shopping).
4. Cleaner allocation curves that are collusion-discouraging under mild assumptions.

Happy to share drafts of circuits and interfaces; again the codebase here is **WIP/incomplete** and feedback will shape the next cut.

—Shadowgraph

