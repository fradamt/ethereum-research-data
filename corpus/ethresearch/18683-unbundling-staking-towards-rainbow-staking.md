---
source: ethresearch
topic_id: 18683
title: "Unbundling staking: Towards rainbow staking"
author: barnabe
date: "2024-02-15"
category: Proof-of-Stake > Economics
tags: [censorship-resistance, single-slot-finality]
url: https://ethresear.ch/t/unbundling-staking-towards-rainbow-staking/18683
views: 13147
likes: 57
posts_count: 13
---

# Unbundling staking: Towards rainbow staking

*Many thanks to [@fradamt](/u/fradamt), [@casparschwa](/u/casparschwa), [@vbuterin](/u/vbuterin), [@hxrts](/u/hxrts), [@Julian](/u/julian), [@aelowsson](/u/aelowsson), [@sachayves](/u/sachayves), [@mikeneuder](/u/mikeneuder), [@DrewVanderWerff](/u/drewvanderwerff), [@diego](/u/diego), [@Pintail](/u/pintail), [@soispoke](/u/soispoke), [@0xkydo](/u/0xkydo), [@uri-bloXroute](/u/uri-bloxroute), [@cwgoes](/u/cwgoes), [@quintuskilbourn](/u/quintuskilbourn) for their comments on the text (comments ≠ endorsements, and reviewers may or may not share equal conviction in the ideas presented here).*

---

We present **rainbow staking**, a conceptual framework allowing protocol service providers, whether “solo” or “professional”, to maximally participate in a differentiated menu of protocol services, adapted to their own strengths and value propositions.

---

![:rainbow:](https://ethresear.ch/images/emoji/facebook_messenger/rainbow.png?v=14) **Why rainbow?**

We intend to convey that the architecture below is appropriate to offer services provided by a wide spectrum of participants, such as professional operators, solo home stakers, or passive capital providers.

Additionally, the [spectrum](https://en.wikipedia.org/wiki/Spectrum_of_a_matrix) may remind the reader of **eigen**values, while we intend for this proposal to partially enshrine a structure similar to re-staking.

---

### TLDR

- We take a first principles approach to identifying the services that the Ethereum protocol intends to provide, as well as the economic attributes of various classes of service providers (e.g., professional operators vs solo stakers).
- Heavy and light categories of services: We re-establish the separation between heavy (slashable) and light (non- or partially slashable) services. Accordingly, we essentially unbundle the roles that service providers may play with regard to the protocol. This allows for differentiated classes of service providers to be maximally effective in each service category, instead of lumping all under a single umbrella of expectations, asking everything of everyone.
- Delegators and operators: For each category of services, we further distinguish capital delegators from service operators. We obtain a more accurate picture of the principal–agent relationships at play for each service category, and the ensuing market structure which resolves conflicting incentives.
- Heavy services: The requirements of heavy services such as FFG, Ethereum’s finality gadget, are strengthened to achieve Single-Slot Finality (SSF). We suggest options to provide more protocol-level enshrined gadgets, helping foster a safe staking environment and a diversity of heavy liquid staking tokens. These gadgets include flavours such as liquid staking module (LSM)-style primitives to build liquid staking protocols on top of, as well as enshrined partial pools or DVT networks, all allowing for fast re-delegation among other features.
- Light services: Meanwhile, the protocol offers an ecosystem of light services such as censorship gadgets, which are provided using weak hardware and economic requirements. These light services are compensated by re-allocating aggregate issuance towards their provision, a pattern already in use today for sync committees. Additionally, “light”, trustless LSTs may be minted from the delegated (non-slashable) shares who contribute weight to light service operators, by capping operator penalties or making all light stake non-slashable.
- Intended goals: We believe the framework of rainbow staking helps to achieve several goals:

The correct interface to integrate further “protocol services” in a plug-and-play manner.
- Targeting Minimum Viable Issuance (MVI) and countering the emergence of a dominant LST replacing ETH as money of the Ethereum network.
- Bolstering the economic value and agency of solo stakers by offering competitive participation in differentiated categories of services.
- Clearing a path to move towards SSF with good trade-offs.

---

## Operator–Delegator separation

Discussions around staking have pointed out the natural separation between node operators and capital delegators, inherited from the perennial distinction between labor and capital. The separation is natural. Many parties wish to obtain yield, and yield is generated from the issuance rewarding participants who place their assets at stake to secure FFG, Ethereum’s finality gadget, and more largely to operate Gasper, Ethereum’s consensus mechanism. Along with placing assets at stake, the work of validation must be properly done to obtain rewards (more yield) and avoid penalties (less yield). This validation work is however costly, and may be performed by operators on behalf of delegators. The operator set is decomposed in two classes:

- Professional operators, whose higher sophistication, trustworthiness or reputation affords them capital efficiency. Delegators receive a credible signal attesting to the honesty of professional operators, and these operators may receive multiples of delegated stake against low or no collateral. For instance, Lido operators are vetted by the Lido DAO, creating a credible signal and allowing these operators to participate with no stake of their own, and thus maximal capital efficiency.
- Solo stakers, the set of permissionless operators participating in the provision of staking services. The permissionless nature means that solo stakers are fundamentally untrusted, and a delegator does not have access a priori to a credible signal of the reliability of a solo staker. Solo stakers may stake entirely with their own stake, or participate in protocols which create credibility by construction, e.g., requiring the operator to put up stake of their own (Rocket Pool), or joining a Distributed Validator Technologies (DVT) network (Diva).

Operators as part of a Liquid Staking Protocol (LSP) may offer to issue a liquid claim for the delegators, known as Liquid Staking Tokens (LSTs). These LSTs represent the principal which delegators have provided, along with the socialised rewards and losses collected by operators, net of fees.

We review recent proposals to enshrine the separation of operators and delegators further into the protocol. Such attempts naturally target the formation of “two tiers”, an operator tier and a delegator tier (see [Dankrad](https://notes.ethereum.org/bW2PeHdwRWmeYjCgCJJdVA), [Arixon](https://mirror.xyz/arixon.eth/pE2nU_tSWeiTae2vSJ7a-tNK17kIkE_tqlpDf-neMPo), [Mike](https://notes.ethereum.org/@mikeneuder/goldilocks) on the topic). A recent idea suggests that by capping slashing penalties to only the operator’s stake, assets of delegators are no longer at risk.

[![rainbow-staking-0](https://ethresear.ch/uploads/default/optimized/2X/f/fc8ef60bb44452ff9b021fcc0c5dee8ce4ae6b08_2_690x283.png)rainbow-staking-02802×1152 212 KB](https://ethresear.ch/uploads/default/fc8ef60bb44452ff9b021fcc0c5dee8ce4ae6b08)

If this sounds too good to be true, then why should delegators earn any yield? Vitalik lists two possibilities in his post, “[Protocol and staking pool changes that could improve decentralization and reduce consensus overhead](https://notes.ethereum.org/@vbuterin/staking_2023_10#Protocol-and-staking-pool-changes-that-could-improve-decentralization-and-reduce-consensus-overhead)”:

1. The curation of an operator set: Opinionated delegators may decide to choose between different operators based on e.g., fees or reliability.
2. The provision of small node services: The delegators may be called upon to provide non-slashable, yet critical services, e.g., input their view into censorship-resistance gadgets such as inclusion lists, or sign off on their view of the current head of the chain, as alternative signal to that of the bonded Gasper operators. Should a mismatch be revealed, the community would be brought in to decide whether to manually restart the chain from the delegators’ view, or go along with a possibly malicious FFG checkpoint.

In other words, delegators *in this model* do not exactly contribute economic security to FFG, their stake being non-slashable, but they are able to surface discrepancies in the gadget’s functioning. Their denomination as “delegators” remains somewhat contrived. We see three issues with the model of two-tiered staking as presented above:

1. Delegators in the two-tiered staking model are unlike delegators of current LSPs, who bear the slashing risk.
2. Some agents would wish to delegate their assets to “two-tier operators” and subject themselves to the slashing conditions, in search for yield.
3. Some agents would wish to not operate small node services themselves, yet participate in their provision by delegating operations instead.

## Heavy and light services separation

To resolve these issues, we take the view here of *two* distinct types of *protocol services*, each type inducing within itself a market structure of delegators and operators. The fully unbundled picture becomes:

[![rainbow-staking-1](https://ethresear.ch/uploads/default/optimized/2X/b/b161b303703991be074a722dcf785a018cd86fb8_2_690x240.png)rainbow-staking-13302×1152 278 KB](https://ethresear.ch/uploads/default/b161b303703991be074a722dcf785a018cd86fb8)

*The two categories are functionally different, but both feature the Delegator–Operator Separation*

### Economics of heavy services

- Heavy services use stake as economic security, making a credible claim that should the service be somehow corrupted, all or part of the stake will be destroyed. Gasper makes such a claim when it binds Gasper participants to slashing conditions, in particular the condition that should their stake participate in an FFG safety fault (conflicting finalised checkpoints), all of their stake will be lost.
- The heaviness of the service induces specific market structures. The heightened risk of slashing, coupled with the high amount of revenue paid out in aggregate to Gasper service providers via issuance, results in long intermediated chains of principal-agent relationships, with delegators providing stake to operators who participate in Gasper on their behalf.
- An architecture akin to the Liquid Staking Module (LSM), originally proposed by Zaki Manian from Iqlusion, may be deployed to enshrine certain parts of the heavy service provision pipeline, and allow for the emergence of competitive LSPs. In the LSM, delegators provide stake to some chosen operator. An LSM share may be minted from the delegate stake, representing the delegation from a given delegator to a given operator. Shares are then aggregated by an LSP, which mints a heavy LST backed by the set of shares it owns.
- Fast re-delegation is allowed, with the re-delegated stake remaining slashable for some unbonding period, all the while accruing rewards from the new operator it was re-delegated to (similar to Cosmos).

### Economics of light services

- Light services use stake as Sybil-control mechanism and as weight functions, akin to Vitalik’s first point on light delegators curating a set of operators. The low capital requirements and low sophistication necessary to provide light services adequately, mean that the playing field is level for all players.
- Nonetheless, a holder may still decide to delegate their assets to a light service operator. The light service operator would offer to perform the service on behalf of the delegator against fees, which aligns the incentives of the operator to maximise the reward for the delegator. In a competitive marketplace of light operators, along with re-delegation allowing for instant withdrawal from a badly performing operator, light operators would be expected to provide the service for marginal profitability and with cost efficiency.
- Some light services may require sticks in addition to carrots, i.e., must allow for slashable or penalisable stake. We suggest here to enforce penalties capping, where only the stake put up by the operator is slashable. We call these partially slashable light services.

[![rainbow-staking-2](https://ethresear.ch/uploads/default/optimized/2X/0/0b0516b17f26b1a323fc9a70cacfc5c48d3f7822_2_690x240.png)rainbow-staking-23302×1152 350 KB](https://ethresear.ch/uploads/default/0b0516b17f26b1a323fc9a70cacfc5c48d3f7822)

*By bonding light operators, penalties may be doled out to service providers with bad quality of service.*

- A delegator receives a tokenised representation of the assets they delegate towards the provision of light validation services. We call this tokenised claim a light LST. When delegator Alice deposits her assets to operator Bob, she receives an equal amount of LightETH-Bob.

This LST is trustless in the sense that Alice may never lose the principal she delegates to Bob, as Bob’s penalties are capped to his own bond. Accordingly, even an untrusted operator such as solo staker is able to mint their own trustless light LSTs.
- However, the light LSTs are not fungible between different operators. If Alice deposits with Bob and Carol deposits with David, Alice obtains LightETH-Bob while Carol receives LightETH-David. The non-fungibility comes from the internalisation of light rewards. Bob may set his commission to 5% of the total rewards received on the delegated stake, while David may set his own commission to 10%. Even at equal commission rates, the two operators may not perform identically, with one returning a higher value to its delegators or holders of their associated light LST. The value returned may be internalised with e.g., making the light LSTs rebasing tokens.
- Contrary to heavy LSTs which are market products, the light LSTs are protocol objects. Light LSTs have properties resembling LSM shares, rather than LSTs as traditionally known.

Note that we already have light services in-protocol today! The sync committee duty is performed by a rotating cast of validators, and is responsible for [about 3.5%](https://eth2book.info/capella/part2/incentives/rewards/) of the aggregate issuance of the protocol (including the proposer’s reward for including aggregate sync committee votes). This level of this allocation is based on a reasonable guess with respect to the value and incentives of the service (e.g., cost of attacking by accumulating weight).

- Consequently, we are already in a world where the protocol remunerates (via issuance) the provision of some chosen light services. We can add more to these light services if we believe these to be valuable enough to warrant either additional issuance or a redistribution of our issuance budget away from the Gasper mechanism remuneration and towards more of these light services. A thesis of this framework is that we indeed have such services at hand, including censorship-resistance gadgets.
- Admittedly, sync committees are not a great archetype of light services. First, these committees will be obsolete after SSF, which rainbow staking aims to achieve. Second, these committees exhibit strong synergies with activities performed by heavy operators, so they do not confer an overwhelming advantage to solo stakers. Our point here is to recognise that issuance is already diverted away from only Gasper, but it is not to advocate for sync committees as being the archetype for light services. Censorship-resistance gadgets fit the bill much more, if they are able to reward participants for increasing CR by surfacing censored inputs to the protocol via some gadget such as inclusion lists.

|  | Heavy services | Light services |
| --- | --- | --- |
| Service archetype | Gasper | Censorship-resistance gadgets |
| Reward dynamics | Correlation yields rewards usually, anticorrelation is good during faults | Anticorrelation yields rewards (surface different signals) |
| Slashing risk | Operators and delegators | None or operators only |
| Role of operators | Run full node to provide Gasper validation services | Run small node to provide light services |
| Role of delegates | Contribute economic security to Gasper | Lend weight to light operators with good service quality |
| Operator capital requirements | High capital efficiency (high stake-per-operator) + high capital investments | Not really a constraint (operators receive weight) + small node fixed cost |
| Solo staker access | Primarily as part of LSPs (e.g., as DVT nodes) | High access for all light services |
| Liquid stake representation | Market-driven plurality of heavy LSTs | In-protocol light LSTs |

---

![:package:](https://ethresear.ch/images/emoji/facebook_messenger/package.png?v=14) **Link to re-staking**

"*Provision of validation services*” sounds eerily familiar. We now draw a direct link between the discussion above and re-staking.

When a party re-stakes, they commit to the provision of an “actively validated service” (AVS). In our model, we may identify different types of re-staking:

- Re-staking into heavy services burdens your ETH asset with slashing conditions.
- Re-staking into light services may not burden you with slashing conditions, yet would offer rewards for good service provision.

So we claim that the model above is a partial enshrinement of re-staking, in the sense that we determine a “special” class of *protocol AVS* for which rewards are issued from the creation of newly-minted ETH. We then allow holders of ETH to enter into the provision of these services, either directly as operators, or indirectly as delegators.

---

## Staking economics in the rainbow world

This section presents a general discussion of the framework and its implications on the Ethereum network’s economic organisation.

We regard Gasper (and in the future, a version with Single-Slot Finality, SSF) as the heaviest protocol AVS, one that is rigidly constrained by its network requirements (e.g., aggregation and bandwidth limitations), and which receives the highest share of aggregate issuance minted by the protocol. As such, its locus attracts a great many parties wishing to provide the stake which the service demands for its core functioning, while inducing market structures of [long intermediated chains of principal-agent relationships](https://mirror.xyz/barnabe.eth/v7W2CsSVYW6I_9bbHFDqvqShQ6gTX3weAtwkaVAzAL4).

Yet, it is unnecessary to offer unbounded amounts of stake to the Gasper mechanism in order to make its security claim credible. In addition, given the induced intermediation of stake, it is necessary to prevent the emergence of a single dominant liquid staking provider collateralised by the majority of the ETH supply. This means that measures such as MVI are critical to target sufficient security, by creating sufficient pressure to keep the economic weight of Gasper in the right proportion. However, MVI drives competitive pressures ill-suited to solo stakers, who are, besides, mostly unable to issue credible liquid staking tokens from their collateral and have thus low capital efficiency.

What is the role of solo stakers in our system? Their economic weight means their group is not pivotal to the Gasper mechanism. In particular, they cannot achieve liveness of finality by themselves, which requires 2/3 of the weight backing Gasper. Solo stakers find solace in two core value propositions which they embody ideally:

- Bolster network resilience: Solo stakers bolster the resilience of the network to failures of larger operators who operate without solo stakers’ input, for instance by progressing the (dynamically available) chain while large operators go offline. Constructions such as Rocket Pool or Diva provide access to low-powered participants in liquid staking protocols. These features are considered by large liquid staking protocols to improve the credibility of their liquid staking token, as measured by the degree of alignment between operators and delegators. In this sense, solo stakers function as hedges for the large liquid staking protocols: Not their main line of operators due to capital and cost-efficiency limitations, yet a strong fallback in the worst case. While the road to SSF may introduce additional pressures for solo stakers who are not part of pools (detailed in a section below), options also exist to preserve the presence of more yield-inelastic participants.
- Generators of preference entropy: Solo stakers may contribute by additive means, the most potent one being as censorship-resistance agents. Performing such a light service is at hand for a wide class of low-powered participants. Additionally, mechanisms exist to remunerate “divergent opinions”, rewarding the contributions of operators who increase preference entropy. Preference entropy denotes the breadth of information surfaced by protocol agents to the protocol, allowing the protocol to see more and serve a wider spectrum of users. For instance, solo stakers of one jurisdiction may not be able to surface certain censored transactions to a censorship-resistance gadget, while others in a different jurisdiction would, and could be rewarded based on the differential between their contribution and that of others. Over time, such mechanisms would tilt the economic field towards solo stakers who express the most highly differentiated preferences, in particular, towards non-censoring solo stakers rather than censoring ones.

[![rainbow-staking-3](https://ethresear.ch/uploads/default/optimized/2X/d/d7dbff8196573f5476c3b4ed54e59b20532b1cf2_2_690x320.jpeg)rainbow-staking-31920×892 155 KB](https://ethresear.ch/uploads/default/d7dbff8196573f5476c3b4ed54e59b20532b1cf2)

*“Preference entropy” denotes the amount of information surfaced by protocol agents to the protocol. Agents who censor have lower preference entropy, as they decide to restrict the expression of certain preferences, such as activities which may contravene their own jurisdictional’s preferences. Collectively, the set of solo stakers who operate nodes to provide services is highly decentralised, and is thus able to express high preference entropy. This economic value translates into revenue for members of the set.*

This economic organisation redraws the lines of the MVI discourse. Today’s *1-D MVI* optimises for competitive pressure to keep the weight of derivative assets such as LSTs in check (”minimum”), while under the constraint of safeguarding the presence of participants with lower agency over this specific mechanism, FFG (”viable”). With rainbow staking, we offer an alternative *2-D MVI* where solo stakers are maximally effective participants *on their own terms*, achieving the goals which many have signed up for: Competitive economic returns with the ability to realise their preferences into the execution the chain, e.g., as ultimate backstops of chain liveness or as censorship-resistance agents. 2-D MVI no longer questions the ideal conditions of aggregate issuance with all participants lumped in a single battlefield, warring over a single scarce flow of revenue. 2-D MVI questions instead the adequate amount to allocate towards the remuneration of heavy services on one side and light services on the other.

We offer a strawman proposal for 2-D MVI determination. The first step is to port the current MVI thinking to the remuneration of heavy services, i.e., [decide on an issuance curve compatible with a rough targeting of stake backing heavy services](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448). This curve determines a level of issuance I_H given some proportion of stake d behind heavy services. The second step, given this level of “heavy” issuance, is to decide the issuance dedicated to light services. This could be determined with a simple scaling factor, i.e., set I_L = \alpha I_H for some small \alpha (note that today, \alpha \approx 3.6\%). The level of aggregate issuance is given by I = I_H + I_L. The two questions 2-D MVI would be required to solve are then:

1. Which amount of stake behind heavy services should be targeted? (i.e., which I_H do we want?)
2. How much more do we wish to issue in order to incentivise a viable ecosystem of light services? (i.e., which \alpha do we want?)

To provide orders of magnitude, issuance over the last year amounted to I \approx 875,000 ETH, close to 2 billion USD at current prices. If even \alpha = 5\% of the yearly issuance was offered to the good performance of solo stakers for light censorship-resistance services, while 95% was offered to the heavy operator set, the set of light participants would collectively earn I_L = 100 million USD. Assuming an investment of about 1,000 USD over the lifetime of a solo staker node (say 5 years, including upfront and running costs), we find that 100 million USD is enough to bring to marginal profitability up to 500,000 solo stakers as light operators. While this provides a generous upper bound in a world where all light service providers are also solo stakers, with no light delegators, we believe this order of magnitude is helpful to frame the terms of the debate.

[![rainbow-staking-4](https://ethresear.ch/uploads/default/optimized/2X/1/1c1d9fa783c18b2631fcb139f3cdede5aa94086b_2_449x375.jpeg)rainbow-staking-41502×1252 220 KB](https://ethresear.ch/uploads/default/1c1d9fa783c18b2631fcb139f3cdede5aa94086b)

*Professional operators are well-suited to provide heavy services due to their sophistication along many dimensions (economies of scale, capital requirements, knowledge, reputation). Meanwhile, solo stakers are well-suited to provide light services due to their high preference entropy, surfacing idiosyncratic signals to the protocol. The two groups overlap where heavy services earn credibility from the participation of solo stakers, or where light services earn efficiency from the participation of heavy operators.*

## Rainbow road

The next sections tackle individual facets of the rainbow staking framework, providing more colour. They are not essential to the text, and may be skipped by the reader in a hurry.

[![rainbowroad](https://ethresear.ch/uploads/default/optimized/2X/0/071dcc962e09b2a2c00ffd4f921c9cc8bc362ded_2_345x191.jpeg)rainbowroad978×542 70.7 KB](https://ethresear.ch/uploads/default/071dcc962e09b2a2c00ffd4f921c9cc8bc362ded)

### Mapping the unbundled protocol

We offer the following map to represent the separation of services in our model:

[![rainbow-staking-5](https://ethresear.ch/uploads/default/optimized/2X/e/e13c3b5a3fa5e13e9d9c5f305b7136feb712c44e_2_690x456.png)rainbow-staking-52802×1852 479 KB](https://ethresear.ch/uploads/default/e13c3b5a3fa5e13e9d9c5f305b7136feb712c44e)

The map emphasises the resources provided by each type of operator. We also unbundled the “execution services” from the “consensus services”. To achieve MVI for the heavy operator layer, it is critical to limit reward variability, and “firewall” the heavy operators reward functions from rewards not accruing from their role as heavy service providers.

While [Execution Tickets](https://ethresear.ch/t/execution-tickets/17944) (ETs) may not ultimately be the favoured approach to separate consensus from execution, we believe their essence represents this separation well. In a world with ETs, where MEV (a.k.a., the value of the block production/payload service) is separated from consensus, heavy operators are less concerned with reward variability, [timing games](https://ethresear.ch/t/timing-games-implications-and-possible-mitigations/17612) or other incentive-warping games which may occur.  The map also shows that the payload service receives (at least) two inputs from the consensus services above: Heavy services finalise the outputs of the payload service, while light services constrain payload service operators by e.g., submitting them to inclusion lists (ILs), constructed along the lines of [EIP-7547](https://eips.ethereum.org/EIPS/eip-7547) or using different methods such as [Multiplicity gadgets](https://efdn.notion.site/ROP-9-Multiplicity-gadgets-for-censorship-resistance-7def9d354f8a4ed5a0722f4eb04ca73b?pvs=4).

But how exactly do outputs of light services such as ILs constrain execution payload producers? In today’s models of inclusion lists, validators are both the *producers* and the *enforcers* of the list. Separating services, the light operators become responsible for the production of the list, but we still require the heavy operators to be its enforcers. Indeed, validity of the execution payload with respect to Gasper is decided by heavy operators, who attest and finalise the valid history of the chain, ignoring invalid payloads. We see two options to connect production and enforcement:

- Strong coupling: We could make the inclusion of a light certificate mandatory for the validity of a beacon block produced by heavy operators, where a light certificate is a piece of data attested to by a large enough share from a light committee, randomly sampled from all the light stake. The liveness of the overall chain then depends both on heavy operators and light operators: When the latter fail to surface a certificate, the heavy operators are unable to progress the chain with a new beacon block. On the other hand, given the inclusion of a certificate attesting to the presence and availability of an inclusion list, the execution payload tied to the beacon block would be constrained by the list, according to some validity condition (e.g., include transactions from the list conditionally on the blockspace remaining, or unconditionally).
- Weak coupling: Tying liveness of the overall chain to the light layer means opening a new attack vector, where a party controlling a sufficient amount of light stake is able to block progress by refusing to provide light certificates. Loosening this constraint, we could expect heavy operators to include the certificate and apply the list’s validity conditions, should the certificate exist, without mandating it. This situation is closer to the status quo: Should the validator set (respectively, the set of heavy operators) be censoring, inclusion lists will neither be produced nor enforced (respectively, enforced). In the worst case, we are indeed back to the status quo, with the additional benefit of having a more accountable object lying around, the light certificate, attesting to the potential censorship of heavy operators who refuse to include it, in lieu of a more diffuse social process relying on e.g., nodes observing their own mempools or researchers staring at censorship.pics (no shade to censorship.pics, it’s amazing ) In the best case, we widen the base able to participate in the production of such lists, and distribute economic benefits of censorship-resistance more broadly, beyond the validator set and towards the ecosystem of small nodes/light operators, who may not participate in the status quo. To make the best case an even likelier outcome, we could grease the wheels further by offering a reward (paid from issuance) to heavy operators who include a light certificate in their beacon blocks.

Additional analysis is required to understand the architecture of out-of-protocol services such as [pre-confirmations](https://ethresear.ch/t/based-preconfirmations/17353) or fast(er) finality ([EigenLayer whitepaper](https://docs.eigenlayer.xyz/assets/files/EigenLayer_WhitePaper-88c47923ca0319870c611decd6e562ad.pdf), Section 4.1), in relation to the rainbow staking framework. Some of these services may still benefit from overloading heavy operators with additional duties, so while this is not a total elimination of all rewards outside of protocol rewards, it is a great mitigation participating towards making MVI more palatable.

![:exploding_head:](https://ethresear.ch/images/emoji/facebook_messenger/exploding_head.png?v=14) Would it be worth unbundling further? The payload service is itself a bundle of two distinct services: “Execution gas”, allocated via ETs, and “data-gas/blobs”, allocated via some DA market. The separation was discussed at a few points in the past. First, as a way to [achieve better censorship-resistance for blobs](https://notes.ethereum.org/nnqDJF2iSrC21Dvh0Ofy8g#Secondary-auctions), by creating a “secondary market” focused on blobs. Second, as a way to [prevent timing games impacting the delivery of blobs](https://ethresear.ch/t/timing-games-implications-and-possible-mitigations/17612#impact-on-blob-inclusion-ht-dankrad-for-mentioning-this-10). Practically, a mechanism akin to partial block delivery may be required for the consensus services to finalise the delivery of both parts of the full block, with blob transactions (carrying commitments to blobs and some execution to update rollup contracts) included in an End-of-Block section. While further analysis is required to understand the costs and benefits of this separation, we believe this direction will become increasingly relevant.

### Towards SSF

We start the discussion with the most special protocol AVS: Gasper, the consensus mechanism of Ethereum. Its [reward schedule is well-known](https://eth2book.info/capella/part2/incentives/issuance/), as well as [its limitations regarding the size of its validator set](https://eth2book.info/capella/part2/incentives/staking/#stake-size), measured in “individual message signers”, and not in “stake weight”. To achieve Single-Slot Finality (SSF), a drastic reduction of the validator set size is required, but how can we achieve this without booting out the least valuable participants, as measured in units of stake-weight-per-message?

Vitalik’s post “[Sticking to 8192 signatures per slot post-SSF: how and why](https://ethresear.ch/t/sticking-to-8192-signatures-per-slot-post-ssf-how-and-why/17989)” details various approaches, including the first model presented above (Approach 2). Some trade-offs are difficult, asking the question whether to go all in on decentralised staking pools (Approach 1), or rotating participation to allow for a larger set in aggregate, if not in constant participation (Approach 3).

We advocate for something mixing both Approaches 1 and 2 (Approach 1.5!)

- A heavy layer that is liquefied as it is today, all in on decentralised staking pools but with a little help from protocol gadgets (e.g., LSM or other enshrined gadgets);
- Combined with a solo-staker-friendly light layer constituting the second-tier, with its own light LSTs.

The question of allocating one of the 8192 SSF seats to operators remains (note that this 8192 number may not be the absolutely correct one). Incentives may need to be designed in order to discourage large operators or protocols disaggregating and occupying more seats in an attempt to push out their competition. These incentives may once again favour more capital efficient players, who can amortise the cost of a seat over a larger amount of stake they control and revenue they receive. The number of available seats is constrained by the efficiency of cryptographic constructions such as aggregating signatures, but as cryptographic methods or simply hardware progress, the number of seats may increase, loosening the economic pressure to perform as a seat owner. Yet, the pressure of MVI keeping overall rewards to heavy operators low remains.

### The heavy layer’s layers

Are we ruling out solo stakers from the heavy layer entirely? I do not believe we are. A re-phrasing frames well the terms of the debate, by calling solo stakers operating in the heavy layer *solo operators* instead. What we want here is for a low-powered participant to still perform a meaningful role in the heavy service.

Enshrining an LSM-like system, which looks a bit like Rocket Pool, already makes a significant dent into the requirements. We take the number of “seats” in SSF as given by Vitalik, i.e., up to 8192 participants. Assume that we intend for [1/4th of the total supply of ETH](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448) to be staked under SSF, which is roughly 30 million ETH today. We would then require a single participant at the SSF table to put up about 3662 ETH, or about 8 million USD. Gulp!

With an LSM-like enshrined mechanism, we favour the emergence of partially collateralised pools (*partial pools*). Rocket Pool requires a minimum bond of 8 ETH for 24 units of delegated stake (1:3), while the LSM defaults to 1:250. Even a (more) conservative choice of 1:100, in-between the two, brings us back to an operator needing to put up about 36 ETH, roughly 4 ETH more than the minimum validator balance required today. Regardless of the limit allowed by the LSM defaults, an LSP may require a higher collateralisation ratio from their operators, e.g., Rocket Pool could still force the use of 1:3 shares.

Could we go further? Running the gamut of existing LSPs, Diva coordinates solo operators with low capital via Distributed Validator Technologies (DVT). A sub-protocol of Gasper could allow for the creation of *DVT pools*, where a virtual operator would behave akin to a solo operator does under the enshrined partial pool model. The virtual operator meanwhile requires *DVT slots* to be collateralised by partial solo operators, and the Ethereum protocol could offer the ability to condition the validity of a Gasper message on the availability of a DVT’d signature performed by a sufficient quorum of partial solo operators.

Regardless of how the solo operator is synthesised (either directly under the enshrined partial pool model, or via quorum under the enshrined DVT model), the solo operator is then provided with the ability to accept deposits from heavy delegators. Heavy delegators then tokenise their deposits as shares of an LSM-like system. These shares are received as assets by an LSP, according to the LSP’s own internal rules on the composition of its basket of operators. In exchange, the LSP mints a fungible asset, better known as an LST. Voilà!

Dynamics here are interesting. An LSP wishes for their LST to be *credible*, i.e., an LST is not credible if holders do not believe that the [operators holding their principal are good agents](https://eprint.iacr.org/2023/605). In the worst case, malicious operators may seek to accumulate as much stake as possible in order to perform some FFG safety fault, at the cost of getting slashed and devaluing the LST. An LSP curating a basket of good operators mints a credible LST, which has value to its holders.

Gadgets such as DVT bolster this credibility, as long as entropy of the DVT set can be ascertained. Importantly, this is not something that the Ethereum protocol needs to concern itself with. The protocol may not be able to procure itself an inviolable on-chain proof that a DVT set’s entropy is high, for instance because it is composed with unaffiliated solo stakers. Yet the open market may recognise such attributes, and value the LST derived from an LSP with good curation more than an LST with poor composition. While participating in the heavy layer may not be the most effective vehicle for solo stakers to express their agency on the network, the optimist in us believes this is a potent avenue and one that just makes [good business sense](https://research.lido.fi/t/staking-router-module-proposal-simple-dvt/5625).

## Open questions

- We would like to understand the limits of “protocol re-staking”, i.e., the ability for the same stake to be burdened with the provision of both heavy and light services. We distinguish in this post only two categories of services, meaning that holders have an “opt-in” choice to make for each of the two services, but should the unbundling go further, allowing for “opt-in” choice of every heavy or light service? Is the addition of protocol services permissionless, or do they require network upgrades?
- We pose the question of service-completeness, i.e., do we now have mechanisms addressing all services which protocol agents may wish to provision? To answer this question, we go back to a distinction already discussed in the PEPC FAQ, originally made by Sreeram Kannan about EigenLayer:

> According to Sreeram [in this Bell Curve podcast episode], there exists three types of use cases for Eigenlayer (timestamp 26:25):
>
>
> Economic use cases (timestamp 27:44): The users of the Actively Validated Service (AVS, a service provided by validators via Eigenlayer) care that there is some amount at stake, which can be slashed if the commitments are reneged upon.
> Decentralisation use cases (timestamp 30:05): The users of the AVS care that many independent parties are engaged in the provision of the service. A typical example is any multiparty computation scheme, where collusion between parties defeats the guarantees of correct execution (e.g., yielding them the power to decrypt inputs in the case of threshold encryption).
> Block production use cases (timestamp 40:10): Validators acting as block producers can make credible commitments to the contents of their blocks.
> In the PEPC FAQ, we have argued that as an execution-layer-driven gadget, PEPC resolved primarily the third use case, i.e., block proposers making commitments about some properties which their blocks must satisfy. We ask whether the distinction of heavy and light services directly map to the other two use cases, economic security and decentralisation services, respectively. To provide more details:

Are there other valuable heavy services? Economic security services seek to make a claim backed by the largest amount of slashable stake. Recent discussions on pre-confirmations have hinted at this property being relevant, beyond the commitment made by a single block proposer.
- Which other valuable light services exist, for which the value proposition of solo stakers is well-suited? Censorship-resistance services are an ideal category, by rewarding participants who are uncorrelated with each other. Do other categories of protocol services exhibit the same dynamics?

What are the general economics of light services? What do the light capital requirements (hardware, partially slashable stake) for service provision induce for the light services economy? What is the role of the light LST minted from delegated shares of light services? How to decide on issuance towards light services, and if multiple light services are offered, how should one allocate the issuance between different services?
… how do we implement all of this? ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=14)

## Replies

**alonmuroch** (2024-02-18):

I might be missing something here but how does this prevent “collapse” into the same topology of few operators controlling most stake?

Ultimately the big professional operators can still get most of the stake via delegation

---

**barnabe** (2024-02-18):

I’ll give a few notes, but bearing in mind that some arguments are speculative. Generally the post tries to *augment* the status quo, giving more optionality rather than less, so any configuration we have today may certainly be realised under rainbow staking too. I’ll then argue for why I believe outcomes where protocol rewards are generally better distributed, are likelier under this framework rather than the status quo.

I would expect the dynamics of the heavy layer to be somewhat similar to what the status quo of staking dynamics currently is. The post suggests making more staking gadgets available to the protocol, so that the playing field may be more level between different LSPs, and allowing features such as fast-redelegation. This is nothing particularly novel, borrowing from a few different places such as existing LSP constructions on Ethereum or gadgets deployed in different ecosystems such as Cosmos. Professional operators may still receive most of the stake via delegation, as they do today, but hopefully the environment can be as a whole more competitive and feature greater diversity and resilience.

The post then suggests to create a new type of service, light services, which have fundamentally different economics. Taking censorship-resistance gadgets as an example, and the construction of some inclusion list as mechanism archetype, the mechanism can be designed without “economic security” in mind, its goal really is to surface a signal to the protocol. Liveness of the mechanism matters (we want it to be useful after all) so we want to incentivise people to do a good job at it still, but we need not require them to have much or anything at stake. This means that we can create something akin to token-curated provider selection mechanisms, where the token (ETH) can be trustlessly re-issued as (provider-specific) “light LSTs” to still align incentives between delegators who share in the rewards, and their chosen operators.

Could professional operators still get most of the stake via delegation? Certainly, and we would expect them to be active on the light layer too. But note that without separating light and heavy layers, a.k.a., the status quo, whatever distribution of stake we currently have between professional and solo operators will mechanically also be the distribution of stake prevailing for censorship-resistance mechanisms such as inclusion lists, since staking signs you up to all services at once including FFG + LMD-GHOST (Gasper), sync committees, (execution) block production and potentially in the future inclusion lists too. By unbundling, my thesis is that the competitive advantage of solo operators as providers of light services (the preference entropy argument), as well as the social dynamics at play allowing anyone holding ETH to back risk-free any provider that they choose, will allow solo operators to command a more significant amount of (light) stake than the amount of stake they currently command (which is about 6.5% according to [rated.network](https://www.rated.network/overview?network=mainnet&timeWindow=1d&rewardsMetric=average&geoDistType=all&hostDistType=all&soloProDist=stake)). By directing a moderate amount of issuance to light services, we may help foster an ecosystem of small node operators who are a strong counterweight to the more professionalised heavy layer.

The outcome where solo operators on the light layer represent *less* than 6.5% of the delegated light stake is theoretically possible, but imo is unlikely given that the light layer has in some sense weaker restrictions than the heavier one. The next step will be to provide a more complete specification of each layer of services, making some of the claims and constructions more precise, to evaluate whether this is workable.

---

**alonmuroch** (2024-02-18):

Thank you for the detailed response!

Any example network that does that to test out the dynamics between those 2 groups?

I might be a pessimists but IMO whatever dynamics we have now will translate completely to this 2 tier system, we might even see a slight improvement in the light tier but is it worth the complexity?

What will be a good benchmark for improvement? solo stakers jumping 2x?5x? (in size)

---

**barnabe** (2024-02-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/alonmuroch/48/4817_2.png) alonmuroch:

> Any example network that does that to test out the dynamics between those 2 groups?

Not to my knowledge, though I wouldn’t be surprised if some network somewhere had an isomorphic construction, or already discussed these (I put some of my own references/inspiration in the links). I was referred to [Celestia light nodes](https://typefully.com/CelestiaOrg/cDK10hO) as possibly relevant, to my knowledge they are not incentivised, but the links between these (and many other constructions of “light clients” in various shapes and forms) and light services deserves to be explored further. I can think of many ways that the consensus/protocol will require more services in the future, e.g., obtaining proofs/sampling, and maybe there is a more general principle at play.

![](https://ethresear.ch/user_avatar/ethresear.ch/alonmuroch/48/4817_2.png) alonmuroch:

> I might be a pessimists but IMO whatever dynamics we have now will translate completely to this 2 tier system, we might even see a slight improvement in the light tier but is it worth the complexity?

It’s a fair question, I am not sure ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) The starting point of this post was “two-tiered” staking mechanisms as described by e.g., Dankrad or Vitalik (links in post), but I couldn’t square the dynamics of the two tiers without introducing the “four quadrants” separating between the heavy/light and operator/delegator mixtures. So I was calling all this “two-by-two-tiered staking” at first, which is not very catchy…

Anyways, it seems like these ideas of enshrining some separation between operator and delegator come back in the discourse frequently enough that we might be ok with some level of complexity. We could call a basic operator/delegator separation *Level 1*: Adding the gadgets discussed in the heavy layer section and otherwise business as usual, validators are responsible for Gasper, inclusion lists etc.

If we wanted to go further, we could go to *Level 2*: Create a class of light delegators which is bound to the heavy layer operators. This is closer to the two-tiered staking proposals, but recognising that the slashable tier will itself be unbundled between operators and (heavy) delegates, something that Mike was also getting at in his [Goldilocks piece](https://notes.ethereum.org/@mikeneuder/goldilocks). The light delegators can choose to attach their light stake to their favourite heavy operators, and you then attach the responsibility of performing the light services to the heavy operators they choose. I would picture it in the following way:

[![2x2-staking-2](https://ethresear.ch/uploads/default/optimized/2X/d/dc8054e95b36ef06bffc0dc57813091dc16d3fa3_2_690x240.png)2x2-staking-23302×1152 208 KB](https://ethresear.ch/uploads/default/dc8054e95b36ef06bffc0dc57813091dc16d3fa3)

And then *Level 3*, which is the full rainbow staking model with enshrined light operators, as discussed in [this section](https://ethresear.ch/t/unbundling-staking-towards-rainbow-staking/18683#mapping-the-unbundled-protocol-8).

![](https://ethresear.ch/user_avatar/ethresear.ch/alonmuroch/48/4817_2.png) alonmuroch:

> What will be a good benchmark for improvement? solo stakers jumping 2x?5x? (in size)

I think we should move away from a monolithic view of “solo stakers”, even today it is quite a diverse set between those that stake with their own capital and hardware and those that are part of LSPs (where here I mean solo staker == permissionless operator), and then there is also the question of who participates in re-staking etc. So it would be hard to quantify with just one number that we try to maximise. Perhaps a better benchmark is the revenue captured by the set of permissionless operators, as a fraction of the total operator revenue. We might have the “right” number of permissionless operators today, but what’s less clear is their economic sustainability over time. By creating a source of revenue for which we have strong(er) reasons to believe it will sustainably benefit this set of participants, we can target the correct amount more easily.

---

**alonmuroch** (2024-02-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> I think we should move away from a monolithic view of “solo stakers”, even today it is quite a diverse set between those that stake with their own capital and hardware and those that are part of LSPs (where here I mean solo staker == permissionless operator), and then there is also the question of who participates in re-staking etc. So it would be hard to quantify with just one number that we try to maximise. Perhaps a better benchmark is the revenue captured by the set of permissionless operators, as a fraction of the total operator revenue. We might have the “right” number of permissionless operators today, but what’s less clear is their economic sustainability over time. By creating a source of revenue for which we have strong(er) reasons to believe it will sustainably benefit this set of participants, we can target the correct amount more easily.

That’s an interesting goal to define, I too agree just solo staking isn’t the whole story.

If we can find a way to also encourage moving to distributed validators on the heavy category I think it will have an even bigger effect

---

**barnabe** (2024-02-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/alonmuroch/48/4817_2.png) alonmuroch:

> If we can find a way to also encourage moving to distributed validators on the heavy category I think it will have an even bigger effect

I agree here, and we are looking into models to understand whether it may be economically rational for an LSP to onboard permissionless operators into their operations. There are a few factors there like capital efficiency, risk, anti-correlation between the permissionless and more permissioned operators etc.

However, such operators, as part of LSPs, would typically be subject to the LSP’s choice of censorship or MEV policies. As part of a distributed validator, a permissionless operator may not have full agency over the construction of an inclusion list. There may also be value in having permissionless operators active in IL construction without being active in the heavy services. So I still believe the enshrinement of light services is valuable for offering impactful participation to solo stakers, and that the effect on the network may be greater than with permissionless operators subject to LSP policies.

---

**mattstam** (2024-02-24):

I appreciate that your starting point involves asking and answering the following questions:

- For what role are LSPs suitable? Economic security.
- For what role are solo-stakers suitable? Censorship resistance.

It might seem like a minor detail, but most proposals for adjusting staking mechanics fail to consider these questions from the outset, which leads to overlooking how solo-stakers can meaningfully participate in the network over the long term.

The biggest downside I see to your proposal is that it is:

- Complex
- Difficult to migrate to
- Challenging to predict second-order effects

The first two points might not have any alternative other than defining a clear specification. For the last point, I would urge more research into areas such as tokenized claims, restaking, etc.

---

**barnabe** (2024-02-24):

Hi [@mattstam](/u/mattstam), thank you for your thoughtful reply!

Indeed, this post was an attempt at laying out a somewhat coherent vision. If the post managed to convince you of the coherence, it performed its function adequately. For the complexity part, I can discuss a little bit about what are some of the challenges I foresee moving forward.

The starting point would be the “three levels” I was describing in [my answer to Alon](https://ethresear.ch/t/unbundling-staking-towards-rainbow-staking/18683/5). As proposals such as [EIP-7251: Increase the MAXIMUM_EFFECTIVE_BALANCE](https://eips.ethereum.org/EIPS/eip-7251) are discussed, I believe enshrining some measure of operator–delegator separation at the same time may leverage a lot of the work currently done towards specifying EIP-7251. The idea of increasing MaxEB is to allow a single message to carry more stake; enshrining the operator delegator separation would be providing in-protocol a way to functionally distinguish “operator stake” from “delegator stake” on such a message.

The next step would be to offer in-protocol the ability to tokenise such messages. This is essentially the purpose of the LSM, creating shares out of delegated stake. I currently consider this a more “nice-to-have”, and its second-order effects seem to exclude anything worse than the status quo (it provides more flexibility, without removing functionality). Specifying this in the context of Ethereum does seem like a valuable exercise either ways, as it would surface some relevant questions for sure.

Moving to the “next level” (Level 2), again quite a bit of complexity seems embedded into the design and specification of some censorship-resistance mechanism. An extra mechanism is necessary for light delegators (essentially, delegated-staked and un-staked ETH holders) to give weight to the heavy operator of their choosing for the construction of the inclusion set. How this weight feeds into the mechanism itself needs further thought. In the context of inclusion lists as specified in [EIP-7547](https://eips.ethereum.org/EIPS/eip-7547), an idea could be to sample the producer of the list according to the light distribution of stake. With more sophisticated, committee-based mechanisms such as [Multiplicity](https://efdn.notion.site/ROP-9-Multiplicity-gadgets-for-censorship-resistance-7def9d354f8a4ed5a0722f4eb04ca73b), the sampling of the committee could be again performed according to the light stake distribution.

The real step into the unknown for me is Level 3. Allowing a separate set of participants to become light operators would require something akin to a “second deposit contract”, or at the very least some way of tracking the registration and assignment of weight to light operators. This point may be technical, but thornier questions lie imo in the relationships between the heavy operator set, light operator set, and full nodes more generally. I describe some ideas in the section [Mapping the unbundled protocol](https://ethresear.ch/t/unbundling-staking-towards-rainbow-staking/18683#mapping-the-unbundled-protocol-8), essentially we would have to decide on what kind of coupling we wish to go along with, to endow heavy operators with the function of enforcing outputs from the light set such as light certificates. More generally, this also has unknown second-order effects on the political economy of the network, and I agree that much more careful thought is needed.

As you also mention, it would be important to do all this with liquid claims and re-staking in mind. This is something I’ve been thinking more about with [recent posts](https://mirror.xyz/barnabe.eth/v7W2CsSVYW6I_9bbHFDqvqShQ6gTX3weAtwkaVAzAL4), but still incomplete and more about definitions than properties anyways. If you have some specific questions in mind, I would be happy to discuss them further, feel free to send a DM or reply here ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**FDucommun** (2024-03-24):

Thanks Barnabé for the great input.

In my opinion, improving the number of validators on the network by natively integrating liquid staking and restaking mechanisms is absolutely coherent. How could we in you opinion best achieve Level 1 or Level 2 at the current state of the Gasper Protocol ? Are there modifications at the core of the protocol required or could we already start developing such a “light operator” approach based on the existing protocol?

---

**barnabe** (2024-03-25):

Hi [@FDucommun](/u/fducommun), thank you for your reply!

I hope to get started on a specification effort to iron out some of these details, but here are a few ideas. For Level 1, we need for the Ethereum protocol to “see” the presence of operators and delegators. Today it doesn’t know who deposits, only that 32 ETH chunks enter its deposit contract and that they are activated as validators on the other side, but who controls these validators is illegible. Taking the LSM as template, a staker Alice (who provides stake to the system) would be able to mint a share that records their choice of operator along with the data that Alice remains the owner of the share. Contrast this with the situation today, when Alice deposits ETH to the Lido contract, Lido supplies it to the Ethereum PoS deposit contract, and the information that Alice is the capital provider is lost to the Ethereum protocol.

Safekeeping this information allows for heavy delegators (such as Alice) to also “delegate” the heavy share to light services, i.e., “re-stake” their heavy stake for a light operator. I put the words in quotes because you’re not really staking in the sense of providing economic security to light operators (they don’t require it) but in the sense of “backing” the operator and tying their performance to your reward stream. So Alice could both deposit her ETH to Lido, encoded by minting a share that composes Lido’s basket of assets at heavy-stake, and assign her stake to some light operator by writing the address of the operator on the share. So minimally we’d want a protocol object that looks like:

```python
class Share:
   amount: Gwei
   owner: address
   heavy_operator: address
   light_operator: address
```

It’s also possible to just create the light services ecosystem ex nihilo, e.g., by allowing any account to set the address of a light operator they wish to back. In Level 2, there is no distinct class of light operators, the only operators recognised by the protocol are heavy ones, so there is a requirement to enshrine some sort of operator–delegator separation in-protocol for the `light_operator` pointer to be meaningful.

The greatest difficulty is to decide how to embed the light services into the consensus. This is where the discussion in [Mapping the unbundled protocol](https://ethresear.ch/t/unbundling-staking-towards-rainbow-staking/18683#mapping-the-unbundled-protocol-8) is important, assuming we have the infrastructure to recognise light operators and items they produce (i.e., light certificates), how do we then tie consensus execution to the data contained in these light certificates? This is thorny, and not simply a technical problem, there are political arguments to consider (e.g., should liveness of the chain depend on heavy operators respecting the outputs of light operators, as the strong coupling method argues?)

---

**gorondan** (2024-03-27):

Thank you Barnabé for this great material! something to look forward to!

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> Intended goals: We believe the framework of rainbow staking helps to achieve several goals:
>
>
> The correct interface to integrate further “protocol services” in a plug-and-play manner.
> Targeting Minimum Viable Issuance (MVI) and countering the emergence of a dominant LST replacing ETH as money of the Ethereum network.
> Bolstering the economic value and agency of solo stakers by offering competitive participation in differentiated categories of services.
> Clearing a path to move towards SSF with good trade-offs.

the envisioned goals seem to light the way ahead in staking, as there are risks in relying too much on the social layer and morality to protect the protocol against centralization in the staking scene and countering the emergence of a dominant LST with its associated perils.

Here’s a proposal of how a minimal viable enshrinement of Operator and Delegator roles Separation (meODS) could look like for Level 1:

## Level 1 (meODS) Feature set

| FEATURE | Title | Description | Expected results |
| --- | --- | --- | --- |
| Feature 1 | enshrine Quick Staking Key (Q key) | allow validators to provide two staking keys: the persistent key (P key) and the quick staking key (Q key) - a contract address, that when called, outputs a secondary staking key during each slot | Protocol can functionally distinguish operator stake message from delegator stake message |
| Feature 2 | minimally enshrine LSM | adds Principal - Agent relations at protocol level | Operator stake and Delegator stake can exchange Claim and Liability messages |

## Feature 1 specification

A good starting point could be amending the structure denoting new deposit operation under EIP-6110. This EIP is now [included in the next hard-fork](https://github.com/ethereum/EIPs/commit/810c347a48052ab36a53a6aa684737ce386f6093), so the proposed specification takes the following into account:

- validator deposit is appended to EL’s block structure
- deposit inclusion and validation responsibility is passed to the EL  - no need for deposit data voting from the Consensus Layer

```auto
class DepositReceipt(Container):
    pubkey: BLSPubkey
    qkey_generator: ExecutionAddress #added line
    withdrawal_credentials: Bytes32
    amount: Gwei
    signature: BLSSignature
    index: uint64
```

OPERATOR - `operator stake message`

`DepositReceipt` needs to be signed with the depositor’s private key ( for reasons related to rogue key attacks) and the pubkey is added to the deposit data, so the protocol “sees” who the Depositor is.

Considering permissionless staking pools will most likely use pool-specific withdrawal addresses, the pool Operator can be considered the Depositor, and because (even in single-slot finality scenario) validator deposits are a core component of PoS consensus, the protocol will be able to distinguish Operator stake message this way.

DELEGATOR - `delegator stake message`

The protocol could map Principal - Agent relation by the logic contained in the smart contract provided by the Operator during deposit process e.g. “Y delegated stake to X and X deposited that stake in protocol”. So Y is the capital provider (Delegator), while X is the Operator.

## Feature 2

In a semi-enshrining of LSM scenario, having Feature 1 implemented would allow the protocol to map relation or claim and liability messages between Operators and Delegator.

Light Validator clients can then provide light services to the Execution payload and delegator stake message could be used for *light certificate* issuance, restaking, etc. as per Level2 criteria. This would unlock much stronger forms of Consensus participation for Delegators, which is a huge improvement compared to current situation, where capital providers have no saying in protocol consensus.

## Level 2

Unlocking level 2 of the rainbow tier system will allow further separation of each tier (Operators & Delegators) in to heavy services provider and light services providers.

To my understanding, the separation between heavy services providers and light services providers could be done in-protocol, after increasing the MAX_EFFECTIVE_BALANCE ([EIP-7251](https://github.com/ethereum/EIPs/blob/35589d35c40576d932923542b31a4d8f7812c3e7/EIPS/eip-7251.md)), and later implementing a balance threshold (e.g. 2048 ETH) to determine which existing validators enter which complexity tier.

While a full enshrinement of the 2by2 tiered staking (rainbow staking) and Strong coupling mandating the *light certificate* for block validity is the course to be taken imo, there can be value in [enshrining some things outright and leaving some things to the users](https://vitalik.eth.limo/general/2023/09/30/enshrinement.html#enshrining-liquid-staking) (i.e. staking pools) approach + a weak coupling approach under the staus quo(staking pools get to op-in), otherwise, we risk not having any in-protocol Operator-Delegator separation for the ~ next two years.

---

**Evan-Kim2028** (2024-03-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> |Role of operators|Run full node to provide Gasper validation services|Run small node to provide light services

Is there any intuition on how this will improve the roadmap towards danksharding? Specifically, in a world where there are more blobs than txs in a block and blobs are only propagated via probabilistic samples.

Could the heavy services be leveraged to store blob data indefinitely on chain as well?

