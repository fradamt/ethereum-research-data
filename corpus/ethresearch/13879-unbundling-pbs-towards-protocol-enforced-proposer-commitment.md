---
source: ethresearch
topic_id: 13879
title: "Unbundling PBS: Towards protocol-enforced proposer commitments (PEPC)"
author: barnabe
date: "2022-10-08"
category: Economics
tags: [proposer-builder-separation]
url: https://ethresear.ch/t/unbundling-pbs-towards-protocol-enforced-proposer-commitments-pepc/13879
views: 19143
likes: 53
posts_count: 9
---

# Unbundling PBS: Towards protocol-enforced proposer commitments (PEPC)

*Many thanks to [@fradamt](/u/fradamt) [@casparschwa](/u/casparschwa) [@vbuterin](/u/vbuterin) [@ralexstokes](/u/ralexstokes) [@nikete](/u/nikete) for discussions and comments related to the following post. Personal opinions are expressed in the first-person-singular.*

Protecting the proposer and ensuring liveness of the chain are a big part of why PBS is considered to be moved into the Ethereum protocol. Ideally, when the proposer utilises the services of a builder, there is a contract between parties for the delivery of some goods (valuable blockspace), and the contract is honoured atomically:

- Either the contract fails to be made and the goods are not delivered/block content is not published, or
- The contract is successfully made and payment always succeeds, no matter what the party committed to supply the goods does.

This stands in contrast to [MEV-boost](https://github.com/flashbots/mev-boost), where a proposer could enter into a commitment with a relay, by signing a block header, after which the relay could fail to publish the block in time, and the proposer is not trustlessly compensated while missing the opportunity to make a block.

But with our version of in-protocol PBS (IP-PBS), we bind ourselves to a very specific mechanism for making these contracts, where there is trustless infrastructure for the proposer to sell off *entirely* their right of making the block. Amendments exist, such as [inclusion lists](https://notes.ethereum.org/@fradamt/H1ZqdtrBF), or [increasing proposer agency by letting them build part of the block](https://ethresear.ch/t/how-much-can-we-constrain-builders-without-bringing-back-heavy-burdens-to-proposers/13808). Still, few results exist showing that a proposer can be fairly unsophisticated and achieve most of the value their position confers upon them.

As an example, what if there is [economic value for the proposer in selling the rights to make their block in advance](https://gateway.pinata.cloud/ipfs/QmWXkzM74FCiERdZ1WrU33cqdStUK9dz1A8oEvYcnBAHeo), say 10 slots before? Under IP-PBS, a cartel of builders must honour an out-of-protocol market, where the winner of the blockspace future (perhaps auctioned at slot n-10) trusts the winner of the slot n IP-PBS auction to let them make the block. Yet the notion of an IP-PBS “winner” is semantically violated, and the value cannot be achieved by an untrusted proposer. Builder colocation with trusted proposers could also increase the delta between what IP-PBS returns to an unsophisticated proposer and what trusted proposers can achieve, beyond simple latency improvements.

In such cases, the incentive to use IP-PBS is cosmetic, as builders can make arrangements out-of-band with proposers, who then ignore bids received via the IP-PBS facility. The incentive to “go around” IP-PBS is reduced with mechanisms such as [MEV-smoothing](https://ethresear.ch/t/committee-driven-mev-smoothing/10408) (much in the same way [EIP-1559 makes off-chain agreements moot](https://timroughgarden.org/papers/eip1559.pdf)), but they entrench further a specific allocation mechanism of blockspace, which if suboptimal, doesn’t allow the Ethereum protocol to realise the highest possible social welfare.

It is hard to foresee what the future will ask of the protocol, or how economic value will be realised by agents interacting with the protocol. The current version of IP-PBS feels strongly opinionated with respect to the organisation of a market around blockspace, while what we seem to be trying to solve for is trustless infrastructure for commitments to be honoured, e.g., the commitment to provide (possibly partial) block contents or be penalised up to the promise that was made. Meanwhile IP-PBS attempts to set a “good default” for unsophisticated proposers, yet appears to require proposer intervention to ensure censorship-resistance.

In other words, **we may need a mechanism for credible signalling *in general*, not a mechanism for credibly realising one specific signal** (”I can make the whole block for you and return you *x* amount of ETH for it”). With such a mechanism, we can look towards future protocol duties which proposers may wish to outsource, as outlined in [Vitalik’s recent ethresear.ch post](https://ethresear.ch/t/how-much-can-we-constrain-builders-without-bringing-back-heavy-burdens-to-proposers/13808), ideally without requiring changes to the protocol and without needing to design and enshrine a specific mechanism for the contracting of proposers and third-parties.

This post explores this alternative and attempts to draw its consequences, in the spirit of exhaustive search of the design space. Many open questions remain to be answered to consider this direction a feasible alternative to existing designs.

**TL;DR**

- In the following we build towards a trustless, permissionless scheme for validators to enter into commitments with third parties. We start by protocolizing Eigenlayer, to ensure that out-of-protocol commitments entered into by validators are reflected into the protocol, e.g., tracking their effective balance if they are slashed by Eigenlayer middleware.
- We recognise that this is not enough, since it allows for attacks up to some “maliciousness upper bound”: the protocol cannot enforce the validator won’t deviate when the profit is greater than the slashed amount. So we need to go further, and not simply move to the protocol the outcome of commitments (if the validator is slashed or not) but also whether the commitment was satisfied or not, and base our protocol validity on it.
- As a stepping stone, I propose an optimistic block validity notion, where a validator could do something slashable with respect to the commitments they entered into, and such a slashable behaviour could be made canonical by attesters, but everyone involved eventually gets slashed.
- To return to pessimistic block validity (validator behaviour must be proven correct (no slashing) for block validity), we allow proposers to submit commitments expressed as EVM execution in their block. Attesters can then simply check validity of the block they receive with respect to the commitments that were made.
- We then need to deal with data availability, to ensure that neither proposer nor committed third-party is able to grief one another. Here we observe a fundamental difference between “selling auctions”, where the proposer auctions something valuable to a third-party, e.g., the right to make a block, and “procurement auctions”, where the proposer attempts to obtain something valuable from the third-party, e.g., a validity proof of the execution payload.
- Finally, assuming the existence of such a generalised market for commitments, we revisit the idea of “proposer dumbness”, as expressed by the addition of protocol features aimed at levelling the playing field between dumb and smart proposers.

## In-protocol Eigenlayer (IP-Eigenlayer)

[Eigenlayer](https://youtu.be/01xDSwMO5U4) is a good starting point to build towards our mechanism, as it allows, in its own words “permissionless feature addition to the consensus layer”. However, relying only on Eigenlayer-provided guarantees is weaker than what the protocol may enforce, even if it comes as a handy tool to [augment current out-of-protocol mechanisms](https://www.youtube.com/watch?v=ywJNXIUSqOw) such as builder markets.

One issue with Eigenlayer, seen from the PoS protocol’s perspective, is the principal agent problem (PAP). The protocol outsources its security to a set of validators, which are staked. When validators are slashed out-of-band by Eigenlayer middleware, the protocol does not realise that the agents to which it has delegated security may have weaker incentives to participate in the protocol than the protocol is led to believe via its own state. One way to make the protocol aware of such discrepancies is to allow Eigenlayer or any other system to update a validator’s in-protocol balance, a protocol we call *IP-Eigenlayer*.

We let validators allow external addresses to slash them, and the protocol is able to see the amount slashed. For instance, a validator is allowed to sign a message saying “Address `0xabc` is allowed to slash me”, and this message is included on-(beacon-)chain, after which `0xabc` can submit a slashing message to the protocol, for some amount of stake.

[![eigslash](https://ethresear.ch/uploads/default/optimized/2X/0/06ee025547d2f7530c5116960a5776056a3e5c5c_2_345x209.jpeg)eigslash976×592 38.7 KB](https://ethresear.ch/uploads/default/06ee025547d2f7530c5116960a5776056a3e5c5c)

Allowing external constructs to influence the state of the protocol may sound unwise. But with the existence of Eigenlayer, validators *will* enter into such schemes, so protocolizing it doesn’t reduce the potential for protocol misalignment coming from validator restaking and getting slashed out-of-protocol, either due to operational errors, not performing their duties correctly, middleware smart contract risk, bribing or anything else. Yet protocolizing removes part of the principal agent problem coming from restaking.

With IP-Eigenlayer, the protocol at least has a correct view of the amount currently guaranteeing safety of the system. There are multiple issues to think through, e.g., does an Eigenlayer slashing exit the validator from the active PoS set or simply diminishes their balance, should there be a fee market for restaking/slashing beacon chain messages etc, but we only offer here this construction as a thought experiment to build towards a more general mechanism.

Indeed, while the PAP problem is removed, this does not solve the commitment-based problem of *maliciousness upper bound*: a restaked validator could decide to get slashed if they expect their malicious action to net them a greater payoff than the slashed amount.

## Protocol-enforced proposer commitments (PEPC, “pepsi”)

If we want to generalise beyond the whole block auction proposed by IP-PBS, we need the validator to be able to enter into any commitment, while being secured by the protocol. We should first recognise that there are many protocol-related commitments which are verifiable on-chain, via the `BEACONROOT` opcode, for instance, “the exec-block made at slot *x* was signed by builder *y*, as committed by proposer *z*”. There is a space of such “verifiable protocol-related commitments”, indeed smaller than the larger space of “all possible commitments”, which could include exotic things such as “I will slash proposer *z* unless they show up at my doorstep dressed as a clown” (word to the wise: don’t enter into such commitments!)

To determine whether a commitment was entered into and whether it was appropriately fulfilled, the protocol needs to distinguish between three potential outcomes:

1. The validator entered into a commitment with a third-party and either:
i. The third-party delivered their part of the commitment, the commitment payout is processed.
ii. The third-party did not deliver their part of the commitment, the commitment payout is processed.
2. The validator never entered into a commitment.
3. The validator entered into a commitment with a third-party, then did something violating that commitment, e.g., stole the goods from the third-party for their own benefit.

We want the protocol to make safe *only* one of the first two alternatives, **(1)** or **(2)**. Importantly, it should not be possible for the validator to enter into a commitment with a third-party *and then* finalize a version of history where they did not enter into a commitment with a third-party. The current two-slot IP-PBS design satisfies this property, if we replace “finalize” with “make safe up to the builder’s risk tolerance”, since we do not (yet ![:grinning_face:](https://ethresear.ch/images/emoji/facebook_messenger/grinning_face.png?v=14)) have single-slot finality (SSF).

In the following, we have the [two-slot IP-PBS pattern](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980) in mind, where the proposer first enters into and records commitments, to be made safe/finalized in a first round, after which committed third-parties are expected to deliver on the commitments in a second round. Even though we use this pattern as a template, there could be important deviations to consider and possibilities to generalise beyond it, e.g., schemes where the proposer is able to enter into commitments well before their own slot. We believe this does not undermine the core idea expressed in the following.

Besides ensuring that commitments cannot be reverted, the other ingredient needed is for the protocol to determine whether the commitment was fulfilled, i.e., discriminate between outcomes **(1.i.)** and **(1.ii.)** We build towards this using the IP-Eigenlayer mechanism described above, *adding attesters as validity checkers*.

### Committee-based optimistic block validity

In the IP-Eigenlayer construction, external commitments are entered into by the validator via a smart contract deployed on the execution layer. An instance of such a commitment is “I promise to let builder `y` build my exec-block”.

To see why attesters need to check validity of the commitment fulfillment, consider the following attack from the proposer:

- Suppose the proposer commitment is finalized or made safe enough for the committed third-party to be willing to release their goods.
- The committed third-party releases their contribution.
- The proposer “steals” the goods (think bundle theft in a blockspace market), by e.g., releasing a block violating the commitments they set, in time for attesters to vote on it.
- The proposer is slashed by the protocolized Eigenlayer, as the violation of their commitment can be proven on the execution layer.
- Still, the proposer makes off with the goods’ value because attesters make canonical the proposer’s theft. This value may be far greater than the stake they committed.

In other words, we run into this issue with non-protocol-enforced commitment-based schemes, because it is possible for the proposer to make canonical a history which violates their commitments.

[![youshouldleave](https://ethresear.ch/uploads/default/optimized/2X/0/05f7869c2005f7fd654fa068f7976b4fc95afc7a_2_345x192.jpeg)youshouldleave1654×924 79.8 KB](https://ethresear.ch/uploads/default/05f7869c2005f7fd654fa068f7976b4fc95afc7a)

The trick is to realise **attesters are also able to determine whether the proposer fulfilled their end of the bargain**, or whether they deviated. With IP-PBS, attesters won’t vote on a builder block made by the proposer, since it would violate the validity of the beacon chain state transition function (BC-STF) where the proposer gave rights to the builder to make the block. In this PEPC design, the BC-STF doesn’t have a specific validity condition for each commitment entered into by the proposer.

But attesters are still able to determine out-of-band whether the content they are voting on satisfies the validator commitments that were made. Again, this is a thought experiment, where we assume the presence of IP-Eigenlayer and commitments are enforced via the on-(exec-)chain restaking smart contracts. The protocol could further enforce that an attester voting on content violating the commitments stands to be slashed by the protocolized Eigenlayer mechanism. This *optimistic block validity* condition allows the protocol to differentiate *ex post* between outcomes **(1)** and **(3)**.

(For data availability/fulfilment of commitments, attesters do as they normally do, for instance, they vote “empty” with a `(block, slot)` [fork choice rule](https://github.com/ethereum/consensus-specs/pull/2197), allowing the protocol to differentiate between outcomes **(1.i.)** and **(1.ii.)**. We give more explicit details later in the post.)

We may be uncomfortable with slashing attesters based on a validity condition that is not executed “pessimistically in-protocol”, for at least two reasons:

- Since we have this Turing-complete space of commitments, someone could grief the system by entering into a very complex commitment, making a lot of attesters somehow vote on a block that did not satisfy the commitment, and force the chain to process a lot of expensive slashings for the attesters. This could be remedied by not including one proof per attester, but one proof per invalid block, and slashing all attesters who voted on such a block. Broadly, we have to think carefully about the computational metering of such operations, as mixing consensus-critical messages (slashings) with regular execution could lead to bad outcomes.
- We might also be concerned that all this business of slashing attesters mitigates the commitment-based failure but does not eliminate it. Whenever cost of corruption

Does the nature of the trade mean that there is no trustless market where such griefing is impossible? Perhaps not. Maybe suppliers are required to supply along with their bid something like a zero-knowledge proof (”I can’t tell you what the proof is, but I can prove to you that I have a validity proof for your block”). But even then, after having convinced the proposer that they do know such a proof, the supplier could refuse to supply the proof itself. The supplier could otherwise encrypt the validity proof to some public key, to be decrypted by a committee of attesters via threshold decryption.

## Revisiting “proposer dumbness”

In the scheme above, a proposer is considered “dumb” when they do not enter into any commitment: they make their own beacon block and execution-payload and whatever else is expected of them.

In IP-PBS, the “dumb” proposer is different. There, a “dumb” proposer would enroll themselves into listening to bids received for the right to make an execution payload, and select the highest bid by default—unless they are actually forced to, as in [MEV-smoothing](https://ethresear.ch/t/committee-driven-mev-smoothing/10408). “Dumbness” is subsidised by saying implicitly “the best possible outcome for you as a proposer is to passively listen to bids selling off your whole right to make a block and choose the highest one”.

My argument here is that restricting or narrowing the possibilities for proposers to organise their blockspace’s allocation does not make non-dumb proposers worse (since they can go around any mechanism deployed in protocol), but they *could* make dumb proposers worse, e.g., by making it unable for them to organise in a way that is preferable to them. In this case, I would rather proposers be given template commitments they can decide to use or forego, than imposing on them a specific form of commitment in the shape of IP-PBS. I note as well that inclusion lists are a form of commitment that we now feel like proposers should be able to ape into.

In other words, we have a philosophy of promoting proposer dumbness, yet in many places problems are solved by giving proposers more agency. Good defaults certainly help set a baseline revenue to ensure validators remain decentralised. Still, by kneecapping proposers, we may also lose the hard-earned strengths of a massively decentralised set.

We may now revisit the conclusions drawn from the [Endgame post](https://vitalik.ca/general/2021/12/06/endgame.html). It was right to recognise that as the protocol gets more complex, it will become impossible for all proposers to “do it all” without increasing centralisation towards sophisticated proposers, unless certain protocol-required functions are outsourced to agents outside the boundaries of the protocol. But from this observation, three approaches may be considered:

- Do nothing, and let proposers figure out the best way to outsource their core functions, away from the protocol’s eyes. This is essentially what MEV-boost embodies today.
- Custom-build a market for every possible function that the proposer is expected to satisfy, and hope that the resulting market maximises proposer welfare as a default, while instantiating specific mechanisms to backstop the mechanism (e.g., censorship resistance schemes). This is essentially embodied by IP-PBS and its variants.
- Recognise that as the protocol ossifies, and given the huge complexity of figuring out each market structure independently (if it is at all possible to figure them out in a timeless manner, markets do change after all!), it may be better to provide a trustless infrastructure for proposers to enter into commitments with third-parties, even though there is no “near-optimal” default strategy encoded via the protocol and markets are structured via proposer commitments instead. Should there truly be a bullet-proof, “near-optimal” strategy for the proposer, it may be suggested as part of a client software default package. Meanwhile, the community figures out which commitments work best in various situations, and proposers are free to choose which commitments they are willing to enter into. At most, the protocol may provide more commitment-legos for proposers to choose from, such as whitelisting particular block templates. This feels like an appropriate scope for the protocol in general, which does not overdetermine the economic organisation of its actors.

In this post, we attempt to sketch this third way, while recognising that more work is necessary to gauge the costs, benefits and implementability of such an approach.

## Replies

**randomishwalk** (2022-10-14):

Really great and thorough post Barnabe! A lot to react to here, so I’ll try to do this in chunks and start first maybe with higher-level comments & questions for you (along with everyone else following this topic).

**Goals of PBS**

This is more so for me but I find it helpful to start with an explicit outlining of what outcomes we’re trying to achieve with PBS. In my mind, a successful PBS design should consider the broader goals below. And I haven’t thought through enough as to whether or not there’s some “impossibility theorem” or yet another form of a “trilemma” in here:

1. Maximizing value accrual for proposers
2. Minimizing the difference in returns on capital between sophisticated & unsophisticated proposers
3. Censorship resistance
4. Minimizing external, “off-chain” dependencies
5. Minimizing incremental protocol complexity

**Summary of PEPC as you envision it**

And here’s my attempt at a tl;dr of your tl;dr ![:blush:](https://ethresear.ch/images/emoji/facebook_messenger/blush.png?v=12)

1. Use an EigenLayer-like system for enforcing certain rules and behaviors in the builder market
2. Open question of whether to use optimistic or validity proofs
3. The data availability problem rears its ugly head yet again

**Some questions that popped into my mind**

- Until we have a strong consensus on what outcomes we’re trying to optimize for, it’s difficult I think to react to specific proposals or ideas around mechanism design?
- What EIPs would this type of system depend on?
- What EIPs would be nice to have and make the implementation of PEPC far easier / more elegant? [Initial thought is that 4337 (AA) might be somewhat helpful here]
- Should something like EigenLayer be enshrined or not? Essentially the same question people have asked around other fairly dominant “side-car” pieces of software or middleware whether it be scaling solutions, liquid staking, and/or MEV relays
- What are some low effort / low cost ways we can simulate different types of mechanism designs here? Or “do it live” but in far lower stakes environments (testnets, sidechains, etc)?

---

**barnabe** (2022-10-16):

Thank you for your thoughts [@randomishwalk](/u/randomishwalk) ! After a few conversations at Devcon about this proposal, here are a few answers.

![](https://ethresear.ch/user_avatar/ethresear.ch/randomishwalk/48/9610_2.png) randomishwalk:

> Maximizing value accrual for proposers
> Minimizing the difference in returns on capital between sophisticated & unsophisticated proposers
> Censorship resistance
> Minimizing external, “off-chain” dependencies
> Minimizing incremental protocol complexity

On the goals, I am not sure whether there is an impossibility theorem, but there are definitely dependencies between points 1 to 5. If you assume that the dominant builder is censoring, and if you assume that a proposer shuts themselves out of receiving a block made by a dominant builder whenever they mandate the inclusion of some transaction (either via inclusion-list, partial block building or PEPC pre-commitment), then there is absolutely a trade-off between value accrual and censorship resistance. It may be mitigated by the fact that over time, censoring builders are shut out of making blocks for non-censoring proposers, and hopefully their edge diminishes as a result (e.g., the private order flow they may control decides that the greater latency is not worth it, and connects with different builders). It would be great to formalise these points better, I hope to publish something on the cost of censorship soon but the models are tricky!

Protocol complexity is an interesting one too. h/t to conversations with sxysun on expressivity, though I might do a poor job at relating his ideas, so take the following as my own interpretation which is possibly not in line with what he has in mind. But anyways, there is a space of mechanisms that attempts to maximize social welfare by satisfying user preferences. The space of user preferences over state is hugely complex, not only because state is derived from a general state machine, but also because preferences may be in conflict with one another. Given this assessment, how might we attempt to maximize social welfare? We need mechanisms to mediate user preferences, and the more expressive mechanisms are, the better hope we have to make an allocation that maximizes welfare. Then there is perhaps a trade-off to make: the less expressive the mechanism on the protocol-side (e.g., the whole block auction), the more expressive the mechanisms need to be on the user/searcher/builder-side, to aggregate preferences up to making a single PBS bid (see also [my talk at Devcon](https://archive.devcon.org/archive/watch/6/updates-on-proposer-builder-separation/?tab=YouTube)). PEPC is an attempt to increase expressivity on the protocol-side, under the assumption that there may be some value that cannot be realised otherwise. This assumption needs to be analysed further to understand whether that is indeed the case.

![](https://ethresear.ch/user_avatar/ethresear.ch/randomishwalk/48/9610_2.png) randomishwalk:

> Summary of PEPC as you envision it

I believe there are two independent constructions of interest in the post. The first is the protocol infrastructure for Eigenlayer-type restaking. We might decide not to do PEPC or something akin to it, but we might still think it’s a good idea to have protocol facilities for the principal-agent problem (PAP) of Eigenlayer, e.g., ability of an outside smart contract to update the validator’s state on the CL. Of course, even with such protocol features it would be always possible for an Eigenlayer-type system to let a validator restake and not bother surfacing updates to the CL, then it would probably be more of a social consensus scenario where we frown upon restaking services that don’t surface the signal clearly enough (I believe Eigenlayer addresses this by providing exhaustive monitoring).

The second result is PEPC. In-protocol PBS in general is an attempt to resolve the PAP coming from dependencies between the validator (the principal) and third-parties (the agents). PEPC is an attempt to generalise a solution to the PAP. h/t to a chat with [@adompeldorius](/u/adompeldorius) who described it as “using the coordination mechanism feature of Ethereum to coordinate proposers themselves” (again, my own words, hopefully not a misinterpretation ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=12))

Imo the optimistic approach won’t cut it for a protocol-side feature, we want much more guarantees than this, so the pessimistic approach would be the way to go. Note however that it doesn’t rely on validity proofs (SNARKs), I was only making the point that validity proofs *could* be used to simplify verification of the commitments. It’s a big open question what the space of these commitments are, how flexible we want them to be etc. But note also that it doesn’t purport to fully replace out-of-protocol restaking services, which could offer validators to enter into much more general commitments, which cannot be verified in-protocol (e.g., EigenDA?)

Then the data availability problem has more to do with the delivery of the specific commitment by the third-party, at which point the protocol needs to decide what has been delivered and what has not been delivered. It’s not as bad as data availability as understood e.g., with rollups publishing data to L1 etc.

![](https://ethresear.ch/user_avatar/ethresear.ch/randomishwalk/48/9610_2.png) randomishwalk:

> Some questions that popped into my mind
>
>
> Until we have a strong consensus on what outcomes we’re trying to optimize for, it’s difficult I think to react to specific proposals or ideas around mechanism design?

Agreed! I definitely want to see more research on this. Maybe the whole block auction with inclusion lists satisfies it. Maybe it’s good enough for the exec-block PAP, but we want something more generic for other things (witnesses, validity proofs, etc.)

![](https://ethresear.ch/user_avatar/ethresear.ch/randomishwalk/48/9610_2.png) randomishwalk:

> What EIPs would this type of system depend on?

I am not sure. What I would like to work on is a proof-of-concept of e.g., the PBS whole block auction end-to-end under the PEPC framework, then adding inclusion-lists, then maybe even “mev-geth” (parallel bundle commitments) and building up a richer library of commitments. I think it will become clearer what’s needed and at what stage which EIPs become relevant.

![](https://ethresear.ch/user_avatar/ethresear.ch/randomishwalk/48/9610_2.png) randomishwalk:

> What EIPs would be nice to have and make the implementation of PEPC far easier / more elegant? [Initial thought is that 4337 (AA) might be somewhat helpful here]

I strongly feel AA is an important part of flexible user-side commitments, I don’t think it’s particularly controversial, I am also probably late to recognise it since I didn’t look too deeply into AA yet ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) But I am wondering if PEPC could be helpful to mediate the relayer entity in 4337, again as another instantiation of the PAP.

![](https://ethresear.ch/user_avatar/ethresear.ch/randomishwalk/48/9610_2.png) randomishwalk:

> Should something like EigenLayer be enshrined or not? Essentially the same question people have asked around other fairly dominant “side-car” pieces of software or middleware whether it be scaling solutions, liquid staking, and/or MEV relays

Replied to this one above, I can see a few different ways to go about it, I don’t have a strong opinion until I understand better what each mechanism can provide.

![](https://ethresear.ch/user_avatar/ethresear.ch/randomishwalk/48/9610_2.png) randomishwalk:

> What are some low effort / low cost ways we can simulate different types of mechanism designs here? Or “do it live” but in far lower stakes environments (testnets, sidechains, etc)?

I would be happy first with pen-and-paper proof-of-concepts, then possibly looking at implementation/prototypes.

---

**mingweiw** (2022-12-20):

I like the idea of focusing on providing trustless commitment infrastructure. Here is a high-level pen and paper strawman of one way to approach implementing the pessimistic block validity approach.

The plan is to first define a representation of a commitment in protocol. Then have attesters evaluate the representation to enforce it.

**In protocol representation**

Let’s start with the whole block auction example. In this case, we have between the proposer and the winning bidder Bob a series of promises to do things by certain time.

1. Bob promises to produce a signed block B by time \delta
2. Proposer promises to propose B as the next block
3. Bob promises to pay proposer X ETH when B becomes the next block

**And** what happens if promises are not kept.

1. If Bob failed a promise, he needs to pay
2. If Proposer failed a promise, he needs to pay

Generalizing this a bit. We have between proposer and Bob

1. a finite series of action to be performed
2. state changes from successful actions
3. time limit to perform an action or dependencies between actions
4. penalty for failure to perform an action successfully

I think 1-4 covers a sufficiently large space of commitments, at least all the ones I can think of. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) If we assume the coverage is sufficient, then the next step would be to turn 1-4 into something computable within protocol. This is mostly straightforward with 1 subtle point. There are 2 types of actions.

1. For some actions, all we care about is the end state. For example, for the action of producing a block, all we care about is whether we got a block signed by Bob or not. We don’t care if Bob actually built the block or subcontracted the building to someone else. For these actions, a check on the end state is sufficient to determine if the action has been successfully performed.
2. For the rest, the end state alone is not sufficient to determine if an action has been successfully performed. For example, for the action Bob pays proposer X ETH, it’s not sufficient to check the end balance of Bob and proposer because there could be multiple ways to reach that end balance and not all ways are desirable.

Due to this difference, we need different ways to handle the 2 types of actions. With that in mind, here is one way represent 1-4 in protocol. We define a representation V of a commitment as follows.

1. Path dependent actions: pre-agreed upon transactions between parties to the commitment. An example would be a payment transaction from a builder to the proposer. This captures the parts of a commitment where the action end state alone is insufficient to determine if an action has been performed successfully. Each transaction carries a signature that’ll identify it within a block.
2. Validity assertions: pre-agreed upon validity assertions represented as code that takes blockchain states (ex. block / messages / slot number) and signatures of transactions in 1 as input and returns True / False / NA. True iff assertion is true. False iff assertion is false. NA iff assertion can’t be evaluated from the input. For example, an assertion might be missing a dependency or can’t be evaluated at the current time. This captures the parts of a commitment where the action end state alone is sufficient to determine if an action has been performed successfully. I think we can further constraint the code to be pure in the functional programming sense. So it should have no visible side effects and always return the same value for the same input.
3. Dependencies: A DAG representing pre-agreed upon dependencies between validity assertions. Nodes are assertions. Edges are dependencies. Note that because signature of transactions in 1 can be inputs to code in 2. Some dependencies involving transactions in 1 can be modeled in the DAG if we choose.
4. Penalties: pre-agreed upon code that executes if one or more validity assertions return False. For example, if a builder fails to deliver, he still pays.

We say V is satisfied iff all validity assertions evaluate to True before the commitment expires.

With this representation in mind, we can modify Vitalik’s [Two-slot PBS](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980) proposal to implement commitment enforcement of a single block commitment between proposer and 1 other party as follow. Let me know if I’m on or close to the right path. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

**Sequence of events in a slot pair**

> slot 0
>
>
> Proposer enters into a commitment with Bob and publishes a beacon block containing V and another block P containing the penalties.
> Attesters evaluate the DAG in V starting at the “root” nodes and in breath-first order, stop when either getting a False or blocked by NA on all further evaluations, vote for the beacon block unless an assertion returned False. If an assertion retuned False, vote for P.
>
>
> slot 1
>
>
> If enough attesters in slot 0 voted for P, then P becomes the next block.
> Otherwise, Bob sees enough attesters voted for V and publishes an intermediate block containing promised content and as many attestations on V as he can find.
>
> Attesters evaluate the DAG in V and vote for the intermediate block iff all assertions return True. Otherwise vote for P.
> Aggregation of intermediate block attestations
>
>
> Bidding starts for the next slot pair

I think this is generalizable to enforcing multiple parallel commitments between proposer and multiple parties. The main issue there appears to be we need a generic way to combine the outputs of the commitments into a single block. This is similar as the new “template” block feature mentioned in the main post. It’s a separate problem that I’m not addressing here.

Another open issue is around penalty execution failures. Do we leave it up to the parties entering into a commitment or provide some guarantee in protocol? More thinking is needed there.

Now let’s do a couple of examples to make this more concrete.

**Example 1**

Basic whole block auction: assume Bob is the winning bidder. Then V consists of

1. Path dependent actions: payment transaction from Bob to the proposer. I assume Bob ensures that this transaction only executes successfully in his block.
2. Validity assertions:
a. View of attester at time \delta in slot 1 contains block B signed by Bob (Bob publishes in time)
b. Fork choice output for attester at time \delta in slot 1 is B (only allows Bob to build the block)
c. B contains the payment transaction from Bob to the proposer and the transaction succeeded
3. Dependencies: a → b → c
4. Penalties:

```auto
if 2a or 2c returns False (Bob fails his part of the commitment)
  Bob pays the proposer
else if 2b returns False (Proposer fails its commitment)
  proposer is slashed
```

**Example 2**

Block SNARK proof auction: assume Bob is the winning bidder. Then V consists of

1. Path dependent actions:
a. payment transaction from proposer to Bob
b. penalty payment transaction from Bob to proposer
2. Validity assertions:
a. if view of attester at time \delta in slot 1 contains verified SNARK signed by Bob (Bob publishes in time) and
b. Fork choice output for attester at time \delta in slot 1 contains the payment transaction 1a and the transaction succeeded
3. Dependencies: a → b
4. Penalties:

```auto
if 2b returns False (proposer doesn't pay)
  execute transaction 1a (enforce proposer payment)
// note that if we reach here, Bob is guaranteed to be paid
if 2a returns False (no SNARK)
  execute transaction 1b (penalizes Bob)
```

There are some high-level points that needs more thinking and clarification and many important details that need to be worked out. But this is already getting long. I’d to get some feedback as I think more about it.

Thanks for reading!

---

**llllvvuu** (2023-01-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> With IP-Eigenlayer, the protocol at least has a correct view of the amount currently guaranteeing safety of the system. There are multiple issues to think through, e.g., does an Eigenlayer slashing exit the validator from the active PoS set or simply diminishes their balance, should there be a fee market for restaking/slashing beacon chain messages etc, but we only offer here this construction as a thought experiment to build towards a more general mechanism.

As a separate item (regardless of the rest of the post) this seems spot on.

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> The validator entered into a commitment with a third-party and either:
> i. The third-party delivered their part of the commitment, the commitment payout is processed.
> ii. The third-party did not deliver their part of the commitment, the commitment payout is processed.
> The validator never entered into a commitment.
> The validator entered into a commitment with a third-party, then did something violating that commitment, e.g., stole the goods from the third-party for their own benefit.
>
>
> […] the other ingredient needed is for the protocol to determine whether the commitment was fulfilled, i.e., discriminate between outcomes (1.i.) and (1.ii.)

I’m not too familiar with this subject, but intuitively I feel like the key ingredient is actually **(1.ii.)** vs **(3)**. To rephrase your points here, you have two dimensions,

- whether or not the proposer included the thing
- whether or not the proposer received the thing to include

The first dimension seems like it should be quite easy to do purely in an EL escrow contract, especially if we add an EVM variable like `block.prefix_accumulator`.

The second dimension, we know it’s necessary because missing out on the escrowed payment is not sufficient punishment for lying about it. But it’s a lot more tricky because it amounts to Byzantine atomic broadcast: in order for the nodes to correctly call out a lie, they must have common knowledge about whether all honest nodes received the goods. Probably that requires some synchrony assumption, otherwise as a slasher I cannot tell if the proposer/attester being offline when I gossip the goods to them but online to gossip the block to me, is a benign behavior.

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> Seeing Bob’s message containing the (partial) exec-block, attesters of the “reveal” slot attest that they have seen Bob’s message.

This seems a lot weaker than Byzantine atomic broadcast, so I’m not sure that it solves **(1.ii.)** vs **(3)**.

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> Here we need a feature to allow proposers to build “template” blocks, where parts of the block can be retroactively applied once they are accepted by the attesters, e.g., the block made by Alice has partial content provided by Bob.

I see that this circumvents the issue of the proposer needing to personally process the goods (and therefore the Byzantine atomic broadcast issue), but in that case who does?

Is the template block just a gossip construct (for pipelining) or is it actually part of the execution layer? If so, would it not requirement enshrinement? If not (and it sounds like it’d still require a p2p/gossip enshrinement), how would that work? Also, how “retroactively” are we talking about? Would it be so retroactive that we might have to build on top of a template block? Does that mean template blocks must be valid in and of themselves, and does that require an EL enshrinement?

---

**barnabe** (2023-01-25):

Thanks for your reply! My claim in the post is that given Properties 1 and 2, outcome (3) cannot happen, because proposing an execution payload against their commitments would be ignored by attesters and couldn’t become finalised.

![](https://ethresear.ch/user_avatar/ethresear.ch/llllvvuu/48/9687_2.png) llllvvuu:

> in order for the nodes to correctly call out a lie, they must have common knowledge about whether all honest nodes received the goods

I am not sure I see where this part is coming from, so I will state the mental model I have for something like whole block PBS in PEPC:

1. Builders send offers to Proposer, offers are EVM transactions tx_1, tx_2, …
2. Proposer makes commit-block, committing to a Builder offer re: the block being made
3. Attester group 1 votes on the commit-block
4. Builder releases execution payload, made on-spec based on Proposer commitment
5. Attester group 2 votes on the execution payload

The payment part is trickier, and indeed needs something like a template block. The template here could be `[builder payload?, tx_B]`, where `tx_B` is the Builder offer, and that transaction can only be executed if the Proposer makes a commitment (somehow the transaction can check if the commitment has been made).

- If Builder releases the payload in time, attester group 2 votes on block [builder_payload, tx_B]. The builder_payload part is retroactively applied to the template [builder payload?, tx_B]
- If Builder doesn’t, attester group 2 votes on block [None, tx_B], which executes as [tx_B].

Note that it is a very rough structure, it’s not clear to me how to operationalise this. Yes, the notion of block templating would somehow need to be a protocol feature, I am not sure if it can be done at p2p level or execution layer.

---

**barnabe** (2023-01-25):

Thank you also [@mingweiw](/u/mingweiw) for your reply! Though I have not replied I have come back to your text a few times and I think you have a correct intuition in several parts. There is likely a pretty big design space to

a. write commitments

b. verify commitments

c. process conditional payments.

For a), a DAG of dependencies may be the correct data structure/language. For b), SNARKs would be a good option if available, but you can also have attesters validate the commitment with e.g., commitment-gas or something. For c), the hope is that EVM transactions combined with a clever use of templating/evaluation of commitments allows for such things. Once you have all three I believe it is generic enough to think about any kind of reward/penalty scheme.

---

**llllvvuu** (2023-01-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> I am not sure I see where this part is coming from, so I will state the mental model I have for something like whole block PBS in PEPC:

That part was just referring to a world in which the proposer would be responsible for completing the full block (e.g. proposer suffixes; proposers->attesters->builder->proposer->attesters vs proposers->attesters->builder->attesters) and not just a template. I agree that templates don’t have this issue, although they introduce their own complexity.

To me it sounds like the cadence here is somewhat between crLists and proposer suffixes. In crLists the crList is known well in advance to the builder, and in proposer suffixes the built block is known in advance to the proposer; if the template looks like `[builder payload?, tx_B]` i.e. the template hole and winning bid are released simultaneously, then neither the builder or the proposer know what each other are doing. The challenge I see here is duplicating transactions. Even in pre-committed proposer suffixes, the proposer gets the last look, to be able to deduplicate / prune transactions from the pre-committed tree.

That being said, templating does sound like a fun design space. Can it be as expressive as the proposer constructing the block *after* looking at the goods? One would have to think carefully about the shape of the holes:

- Do we only allow tx-shaped holes?
- Do we allow value-shaped holes (e.g. an optional function parameter that can be injected by third-party)
- What happens if the hole is malformed? Is that something the EL needs to understand? The CL? Or just the IP-Eigenlayer?
- If builders are only releasing builder_payloads and attesters must vote on [builder_payload, tx_B], when/how does [builder_payload, tx_B] get propagated and validated? Is every intermediate data part of the chain? Is there a DoS if the proposer enters many commitments/payloads in a single block (e.g. suppose every end user tries to get MEV-resistant inclusion via a PEPC; this would call for throttling via some new fee market design and/or a cap on PEPCs per block)?
- What happens if builders no longer get proposer boost?

---

**pmcgoohan** (2023-03-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> Protecting the proposer and ensuring liveness of the chain are a big part of why PBS is considered to be moved into the Ethereum protocol

It sounds as if reducing the load on validators to ensure liveness (and presumably scalability) is now the primary reason for PBS, but I can see a problem with this logic.

While we have a mempool, builders aren’t needed for this. Validators need the bandwidth to handle txs anyway and it’s more censorship resistant with less toxic mev to self build.

If we do away with the mempool and only have builders to reduce the load on validators, Ethereum becomes centralized and censorable.

For example, I don’t see how do crLists work if validators don’t see txs, and if they do, how is this more censorship resistant than self building?

