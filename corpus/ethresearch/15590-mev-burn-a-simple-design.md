---
source: ethresearch
topic_id: 15590
title: MEV burn—a simple design
author: JustinDrake
date: "2023-05-15"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/mev-burn-a-simple-design/15590
views: 19947
likes: 69
posts_count: 28
---

# MEV burn—a simple design

**TLDR**: We describe a simple enshrined PBS add-on to smooth and redistribute MEV spikes. Spike smoothing yields security benefits. Redistribution yields economic benefits like EIP-1559.

*Special thanks to [@dankrad](/u/dankrad), [@domothy](/u/domothy), [@fradamt](/u/fradamt), [@joncharbonneau](/u/joncharbonneau), [@mikeneuder](/u/mikeneuder), [@vbuterin](/u/vbuterin) for feedback.*

## part 1: enshrined PBS recap

We recap enshrined PBS before describing the MEV burn add-on.

- builder balances: Builders have an onchain ETH balance.
- builder addresses: Builder balances are held in EOA addresses.
- builder bids: Builders gossip bids which contain:

payload commitment: a commitment to an execution payload
- payload tip: an amount no larger than the builder balance
- builder pubkey: the ECDSA pubkey for the builder address
- builder signature: the signature of the builder bid

**winning bid**: The proposer has a time window to select a bid to include in their proposal.
**payload reveal**: The winning builder has a subsequent time window to reveal the payload.
**attester enforcement**: Attesters enforce timeliness:

- bid selection: an honest proposer must propose a timely winning bid
- payload reveal: an honest winning builder must reveal a timely payload

**payload tip payment**: The payload tip amount is transferred to the proposer, even if the payload is invalid or revealed late.
**payload tip maximisation**: Honest proposers select tip-maximising winning bids.

[![](https://ethresear.ch/uploads/default/optimized/2X/3/33a90d5f2ec895dc03e095facaf2b2b1747051cf_2_690x333.png)2722×1314 199 KB](https://ethresear.ch/uploads/default/33a90d5f2ec895dc03e095facaf2b2b1747051cf)

## part 2: MEV burn add-on

MEV burn is a simple add-on to enshrined PBS.

- payload base fee: Bids specify a payload base fee no larger than the builder balance minus the payload tip.
- payload base fee burn: The payload base fee is burned, even if the payload is invalid or revealed late.
- payload base fee floor: During the bid selection attesters impose a subjective floor on the payload base fee.

subjective floor: Honest attesters set their payload base fee floor to the top builder base fee observed D seconds (e.g. D = 2) prior to the time honest proposers propose.
- synchrony assumption: D is a protocol parameter greater than the bid gossip delay.

**payload base fee maximisation**: Honest proposers select winning bids that maximise the payload base fee.

[![](https://ethresear.ch/uploads/default/optimized/2X/e/ecb0344d8c47c4607d310b1a479609563030a2b6_2_690x334.png)2718×1318 237 KB](https://ethresear.ch/uploads/default/ecb0344d8c47c4607d310b1a479609563030a2b6)

*builder race to infinity*

ePBS without MEV burn incentivises builders to compete for the largest builder balance. Indeed, for exceptionally large MEV spikes the most capitalised builder has the power to capture all MEV above the second-largest builder balance. This design flaw can be patched with a L1 zkEVM that provides post-execution proofs.

Alternatively, MEV burn can solve the issue by relaxing the requirements on the pre-execution builder balance to cover a maximum upfront payload base fee of M ETH (e.g. M = 32) plus the payload tip. The payload is deemed invalid (with transactions reverted) if the post-execution builder balance is not large enough to cover the payload base fee.

With this change a malicious builder can force an empty slot for M ETH. The ability to force empty slots cannot be weaponised to steal MEV spikes above M ETH as empty slots merely delay the eventual burn of MEV spikes.

## part 3: technical remarks

- prior art: The design is inspired by Francesco’s MEV smoothing. See also Domothy’s MEV burn, a significantly different design.
- unbounded burn: Besides providing a fair playing field and reducing builder capital requirements, the fix to the builder race to infinity (see above) allows for an unbounded MEV burn, beyond the largest builder balance.
- honest proposer liveness: Honest proposers enjoy provable liveness under the synchrony assumption that bids reach validators within D seconds.

proof: Under synchrony, whatever top payload base fee was observed by an honest attester D seconds prior to an honest proposer selecting their top bid (i.e. the attester’s payload base fee floor) will have also been observed by the proposer.

**efficient gossip**: Bid gossip is particularly efficient because:

- builder balances provide p2p Sybil resistance (a minimum builder balance, e.g. 1 ETH, is recommended)
- bids fit within a single Ethernet packet (1,500-byte MTU)
- gossip nodes can drop all but their current top bid

**optimisation game**: Rational proposers will want to maximise the payload tip by guessing the payload base fee floor and accepting bids with non-zero tips after the payload base fee floor has been established. This creates a second optimisation game for rational proposers, in addition to the existing optimisation game with proposal timeliness.
**splitting attack**: Dishonest proposers can use the payload base fee to split attesters into two groups: attesters that believe the payload base fee floor is satisfied, and attesters that do not. Dishonest proposers can already split attesters on the timeliness of their payload reveals.
**late bidding**: Builders can try to deactivate MEV burn by not bidding until after the D seconds tipping window has started, causing attesters to set their payload base fee floor to 0. We argue this is irrational for builders by considering two cases in the prisoner’s dilemma:

- colluding builders: If all the builders capable of extracting a given piece of MEV are colluding then the optimal strategy is to not bid at all for that piece of MEV, even within the D seconds tipping window. Instead, the cabal of builders is better off coordinating to distribute the MEV among themselves, a strategy possible with or without MEV burn.
- non-colluding builders: If one of the builders capable of extracting a given piece of MEV defects by bidding there is no benefit for any of the builders to bid late. If anything, late-bidding builders risk not having bids reach the proposer on time.

**inclusion lists**: Inclusion lists allow proposers to specify a set of transactions they want included in the winning payload. This is sufficient for proposers to fight censorship and provide soft pre-confirmations, by including censored and pre-confirmed transactions in the inclusion list.

*technical similarities with EIP-1559*

- honest majority: Both depend on an attester honest majority. (As argued in the “side note for validators” section, validators are not incentivised to defect.)

EIP-1559: A dishonest majority can control the fork choice rule to only include lower-than-target blocks till the base fee is zero, deactivating EIP-1559 and devolving to a first-price auction.
- MEV burn: A dishonest majority can set the payload base fee floor to zero, deactivating the smoothing and redistribution of MEV spikes.

**partial burn**: Both are partial burns.

- EIP-1559: Base fees partially capture congestion fees when blocks are full. (Ethereum blocks have limited elasticity with a gas limit set to 2x the gas target.)
- MEV burn: The payload base fee floor is merely an MEV lower bound, and rational proposers may collect some MEV above the payload base fee floor.

**onchain oracle**: Both provide an onchain oracle.

- EIP-1559: Base fees yield an onchain congestion oracle.
- MEV burn: payload base fees yield an onchain MEV oracle. (Payload base fees are augmented with the builder address metadata.)

## part 4: security benefits from smoothing

- micro consensus stability: Spike smoothing significantly reduces the incentives for individual proposers to steal MEV via short chain reorgs, proposer equivocations, and p2p attacks (e.g. DoSes, eclipses, and saturations).
- macro consensus stability: An extreme MEV spike can create systemic risk for Ethereum, possibly bubbling to the social layer. Consider a malicious proposer receiving millions of ETH from a rollup hack.
- lower reward variance: MEV spikes cause the average MEV reward to be significantly higher than the median MEV reward. Smoothing significantly reduces proposer reward variance, reducing the need for pool-based MEV smoothing.
- rugpool protection: Pools with collateralised external operators (e.g. Rocket Pool and Lido) are liable to a “rugpool” (portmanteau of “rugpull” and “staking pool”). That is, whenever the operator’s collateral (financial or reputational) is worth less than the MEV spike at a given slot, the operator is incentivised to collect the spike instead of having the smoothing pool receive it.
- censorship resistance: The payload base fee floor is a forcing function for proposers to consider bids from all builders. Proposers that only consider bids from censoring builders (e.g. proposers that today only connect to censoring relays) will not satisfy the payload base fee floor for some of their proposals.
- toxic MEV whitewashing: Stakers and staking pools suffer a dilemma when receiving toxic MEV spikes: should toxic MEV (e.g. proceeds from sandwiching, user error, smart contract bugs) be returned to affected users? This dilemma disappears when toxic MEV is burned, resolving several issues:

incentive misalignment: Rational stakers are incentivised to keep toxic MEV, incentivising “bad” behaviour.
- ethical, reputational, legal, tax liabilities: Stakers have to weigh the pros and cons of a complex tradeoff space. Beyond the ethical and reputational conundrum, the legal and accounting situation may be a grey zone.
- disputes: Staking pools may suffer disputes on how to deal with toxic MEV. Pools with governance (e.g. RocketPool and Lido) may disagree on how to deal with MEV, and centralised pools may suffer backlash from their users if the “wrong” decision was made.

## part 5: economic benefits from redistribution

EIP-1559 and MEV burn yield the same economic benefits.

- reduced validator count: EIP-1559 and MEV burn reduce aggregate ETH staking rewards, itself reducing the amount of ETH staked. This has several benefits:

lower issuance: Aggregate issuance shrinks with reduced ETH staking. Since the beacon chain is designed to be secure with issuance only, EIP-1559 and MEV burn reduce overpayment for economic security and improve economic efficiency.
- more economic bandwidth: Reducing the amount of staked ETH increases the amount of ETH available as pristine economic bandwidth (e.g. as collateral for decentralised stablecoins). EIP-1559 and MEV burn prevent staking from unnecessarily starving applications that consume pristine economic bandwidth.
- lower validator count: Reducing the validator count reduces pressure on beacon nodes and makes single slot finality (SSF) easier to deploy. EIP-1559 and MEV burn reduce the urgency of active validator capping.

**staking APR**: The primary cost of ETH staking is the opportunity cost of money so staking rewards in an efficient market should approximate the broader cost of money. As such, neither EIP-1559 nor MEV burn should significantly affect long-term staking APRs.

- side note for validators: EIP-1559 and MEV burn should increase per-validator USD-denominated rewards. The reason is that ETH-denominated rewards are dictated by the cost of money but the USD price of ETH is positively impacted by EIP-1559 and MEV burn. EIP-1559 and MEV burn increase returns for decentralised staking pools (see “rugpooling”), and raise median returns especially for solo stakers.

**economic sustainability**: EIP-1559 and MEV burn are independent revenue steams for ETH holders, both contributing to economic sustainability. This diversity hedges against one of the revenue streams drying up:

- EIP-1559 dry up risk: Exponential growth of computational resources may lead to blockspace supply outstripping demand and crushing congestion fees. (The bull case for EIP-1559 is induced demand.)
- MEV burn dry up risk: Most MEV may be captured by rollups and validiums at L2. (The bull case for MEV burn is based rollups and enshrined rollups.)

**tax efficiency**: EIP-1559 and MEV burn can significantly improve staking tax efficiency in some jurisdictions by converting income (taxed at, say, 50%) into capital gains (taxed at, say, 20%). EIP-1559 has already prevented ~1M ETH of tax sell pressure, and MEV burn would similarly prevent millions of ETH of sell pressure.
**economic scarcity**: EIP-1559 and MEV burn increase ETH scarcity. Not counting the reduced issuance (see “lower issuance” above), the ETH supply since the merge would have decreased ~2.5x faster with MEV burn. (The supply would have reduced by ~270K ETH instead of just ~110K ETH.)
**enshrined unit of account**: EIP-1559 and MEV burn enshrine ETH as unit of account for congestion and MEV respectively.
**memetics**: EIP-1559 and MEV burn have [memetic potential](https://ultrasound.money/) and strengthen ETH as a Schelling point for collateral money on the internet. The success of Ethereum as a settlement layer for the internet of value is tied with the success of ETH.

## part 6: mental model

Blockspace fundamentally provides both transaction inclusion and transaction ordering services. Competition for inclusion leads to congestion, and competition for ordering leads to contention. Congestion and contention are externalities that can be natively priced with EIP-1559 and MEV burn, and each mechanism yields an independent revenue stream.

|  | transaction inclusion | transaction ordering |
| --- | --- | --- |
| externality | congestion | contention |
| pricing mechanism | EIP-1559 | MEV burn |
| revenue stream | transaction base fees | payload base fees |

*EIP-1559 and MEV burn—two sides of the same coin*

## Replies

**CometShock** (2023-05-15):

Thank you Justin for the great write-up! I’ve got a few questions to hopefully help my understanding of the proposal. Please feel free to correct me if I’m missing something critical with these questions, it happens often enough. ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=12)

**What incentives and/or design constraints discourage an upcoming proposer from publicly broadcasting that they are open to receiving private bids during their slot, where all bidders can privately collude with the proposer to minimize the base fee floor in favor of maximizing their returns?**

In this case, any bidder that believes they have a chance of being selected for a slot is incentivized to privately collude and not make an honest public bid. They can submit timely private bids to the proposer and still trust that the proposer will select the bid which that minimizes base fee floor and maximizes the payload tip.

Yes, a party who is an honest minority bidder and doesn’t believe they are likely to be selected (call them the “unconfident honest bidder”) could still make a public bid — thus smoothing at least some of the spiked profits that private collusion would have captured. However, this assumes that the unconfident honest bidder has block building/MEV skills that are at all comparable to the confident private bidders. If a lucrative MEV opportunity requires high skill to identify and execute, it’s much less likely to be caught by the unconfident honest bidder and remain un-smoothed.

Additionally, the incentives of running, maintaining, and improving an unconfident honest bidder primarily for the purposes of smoothing (rather than successful selection of their block) are very low, as the reward is socialized redistribution through burn. This is far less than the incentives of running, maintaining, and improving a confident private bidder, who is capable of capturing a large portion of the extractable returns for themselves.

**During non-MEV-spike events, what incentives and/or design constraints enforce attesters to set an honest payload base fee floor?**

(Is this question too far out-of-scope from the desirable outcomes of the proposal? If redistribution is just the “means” to the “end” where smoothing is accomplished, then this question doesn’t seem too important.)

I’m left wondering how the incentives for honest payload base fee floor could change based upon the % of ETH staked in the network. Intuitively, ETH stakers are a smaller subset of all ETH holders. Therefore stakers are jointly interested in resisting the redistribution of their base MEV returns to the larger set of all ETH holders.

To illustrate with an example, consider an extreme case where the network has 10% of ETH staked. If payload base fees are relatively efficient and close to total extractable MEV on a “typical” block, then the staker subset is missing out on ~90% of their capturable returns that are getting redistributed to the ETH holders. In this case, each attester (being a part of the staker subset) is highly incentivized to establish a culture of low payload base fee floors on each slot. This way when it becomes their turn to propose, they can capture a much larger MEV return for themselves as well (vs what would’ve been redistributed to them during attestations). The culture change seems plausible given that this is an infinite game. Unless there is some punishment for doing so, attesters could continuously signal they are willing to attest to very low payload base fee floors (on typical blocks) and slowly erode away the higher standard. This does not apply to MEV spikes, as if they’re sufficiently large enough the incentives for attesters could still be to redistribute.

Clearly the above example is extreme and not representative of the magnitude of incentives as if this proposal were to be implemented tomorrow. However, I do wonder if this is a desirable or acceptable outcome and if it should be explored further.

---

**JustinDrake** (2023-05-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/cometshock/48/12127_2.png) CometShock:

> What incentives and/or design constraints discourage an upcoming proposer from publicly broadcasting that they are open to receiving private bids during their slot

We’re not trying to discourage proposers from receiving private bids! In the analysis of MEV burn I would assume that all proposers are willing to receive private bids ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/cometshock/48/12127_2.png) CometShock:

> all bidders can privately collude

If all bidders capable of extracting a specific piece of MEV collude then it’s game over, with or without collusion with the proposer, as well as with or without MEV burn. As argued in the “colluding builders” section under “late bidding”, a cabal of colluding builders can keep all the MEV for themselves (e.g. equally split the MEV among themselves instead of racing towards zero margins). The good news is that 100% collusion within a permissionless set of competing builders is hard—the equilibrium is a race to zero where individual builders defect.

![](https://ethresear.ch/user_avatar/ethresear.ch/cometshock/48/12127_2.png) CometShock:

> During non-MEV-spike events, what incentives and/or design constraints enforce attesters to set an honest payload base fee floor?

The design is secure under an honest majority of attesters, similar to EIP-1559. (See the section titled “honest majority” under “technical similarities with EIP-1559”.)

![](https://ethresear.ch/user_avatar/ethresear.ch/cometshock/48/12127_2.png) CometShock:

> stakers are jointly interested in resisting the redistribution of their base MEV returns to the larger set of all ETH holders

I disagree with this premise—IMO it’s likely net positive for validators to embrace the redistribution of MEV. See the section titled “side note for validators” under “staking APR”. The crux of the argument is that ETH-denominated returns are tied to the cost of money, and USD-denominated returns (as well as the USD-denominated principal) should actually grow.

---

**CometShock** (2023-05-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> If all bidders capable of extracting a specific piece of MEV collude then it’s game over, with or without collusion with the proposer, as well as with or without MEV burn. As argued in the “colluding builders” section under “late bidding”, a cabal of colluding builders can keep all the MEV for themselves (e.g. equally split the MEV among themselves instead of racing towards zero margins). The good news is that 100% collusion within a permissionless set of competing builders is hard—the equilibrium is a race to zero where individual builders defect.

Apologies, I should have made my statement clearer. The emphasis is not that builders collude *with each other builder*, but rather *each individual builder* is incentivized to *collude with the proposer* by running private bids. It’s game theoretically optimal for each individual builder to do so, as you maintain timeliness while obscuring your payload base fee floor to the outside attesters (this reduces the potential payload base fee floor). Additionally, as more individual builders elect to privately bid, they all share the same benefit of an *even lower* payload base fee floor. (*Edit, previously:* Additionally, once each individual builder elects to…)

If the payload base fee floor is lowered due to obscuring the skilled bids, naturally the builder can bid marginally more (ex: half of recovered base fee) payload tip to the proposer - making it game theoretically optimal for the proposer to accept private bids. From the outside, this looks like all builders are colluding amongst each other as well as with the proposer — but in reality it’s just optimal for all builder-proposer relationships to do this on an individual basis and it scales in effectiveness as more builders participate. And the end result is heavily suppressed payload base fee floors. The only party who would intentionally defect from this structure would be an unconfident builder who wants to redistribute as much as they can (but as mentioned before, if they’re unconfident, they’re likely not skilled enough to capture much of the MEV spike anyways. So still suppressed payload base fee floor).

All this to say that it if private bidding is possible, it seems this proposal is effective at burning easy, low-skill MEV, but is ineffective at burning anything outside of that set.

---

**terence** (2023-05-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> observed D seconds (e.g. D = 2) prior to the time honest proposers propose.

Wouldn’t `D` be the same time proposer receive those bids as well? If yes, then I think it can be close to the end of the slot as possible.

Correct me If I am wrong, there will be a new gossip network called  `builder_bids` and the builder will broadcast the `bids` there. Attesters and proposers will all be listening there.

Some followup questions

- How are the attesters chosen for duty? size? new reward/penalty?
- Is this an extension of the forkchoice rule where the second highest bid can’t be head? or an extension of block validity condition where the second highest bid block can’t be valid?

---

**JustinDrake** (2023-05-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/cometshock/48/12127_2.png) CometShock:

> as more individual builders elect to privately bid, they all share the same benefit of an even lower payload base fee floor

Builders do not directly benefit from a low payload base fee floor ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) Naively (i.e. assuming no kickback from the proposer) builder profit margins are invariant to the payload base fee.

![](https://ethresear.ch/user_avatar/ethresear.ch/cometshock/48/12127_2.png) CometShock:

> (ex: half of recovered base fee)

The builder does not “recover” anything from a lower payload base fee. They don’t get the payload base fee, with or without MEV burn.

![](https://ethresear.ch/user_avatar/ethresear.ch/cometshock/48/12127_2.png) CometShock:

> easy, low-skill MEV

I call this “commoditised MEV”.

![](https://ethresear.ch/user_avatar/ethresear.ch/cometshock/48/12127_2.png) CometShock:

> they’re likely not skilled enough to capture much of the MEV spike anyways

Notice that a public-good builder (e.g. a hypothetical “ultra sound builder” ![:stuck_out_tongue_winking_eye:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue_winking_eye.png?v=12)) that wants to set a baseline payload base fee floor wouldn’t necessarily need to be good at capturing MEV spikes. They only need to be good at predicting what the payload base fee floor could be, and then bidding just under that value.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> Wouldn’t D be the same time proposer receive those bids as well? If yes, then I think it can be close to the end of the slot as possible.

The proposer is guaranteed to receive by the start of the slot all the bids broadcast D seconds before the start of the slot.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> there will be a new gossip network called builder_bids and the builder will broadcast the bids there. Attesters and proposers will all be listening there

Exactly! There will be a “bid pool” which is a new p2p gossip channel for bids. Builders broadcast signed bids, and validators listen.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> How are the attesters chosen for duty? size? new reward/penalty?

I would simply reuse the attester committee for the given slot. With SSF the attester committee could be the whole validator set. The same attestation rewards and penalties can also be reused, without modification.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> Is this an extension of the forkchoice rule

Yes, the payload base fee floor attestation rule is a modification to the fork choice rule (not a change to the state transition function).

---

**terence** (2023-05-15):

What happens if multiple bids have the same value? either from same builder or different builders

---

**CometShock** (2023-05-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Builders do not directly benefit from a low payload base fee floor  Naively (i.e. assuming no kickback from the proposer) builder profit margins are invariant to the payload base fee.

My assumption is that kickbacks from proposer to selected builder are inevitable. The proposer *wants* all the builders to privately submit so that some of what *would’ve been* the payload base fee floor is *instead captured* as proposer revenue. It’s very natural that proposers would provide kickbacks to selected builders to incentivize this structure.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Notice that a public-good builder (e.g. a hypothetical “ultra sound builder” ) that wants to set a baseline payload base fee floor wouldn’t necessarily need to be good at capturing MEV spikes. They only need to be good at predicting what the payload base fee floor could be, and then bidding just under that value.

Establishing a word for following response.

**Base Fee Overbid**: `payload_base_fee - builders_extracted_value_from_block` when `payload_base_fee > builders_extracted_value_from_block `

My point is that an “ultrasound builder” who wants to set a baseline payload base fee floor through overbidding would be risking a lot of their balance should they instead be selected. In fact, they could be selected in either two scenarios:

- They predicted wrong and are the most valuable bid, now they lose their base fee overbid to a burn
- A proposer attempting to create a private bid structure selects the public ultrasound builder to call their bluff, now the ultrasound builder lost their base fee overbid to a burn. Rational move in an infinite game with enough relevant information.

My intuition is that the base fee overbidding phenomenon wouldn’t last very long given a few aggressive private-favoring proposers. If the ultrasound builders wanted to remain resilient in the long term, they’d have to become relatively good at capturing MEV spikes. But again, the financial incentive for them to improve their operation is just incomparable to a selfish builder, so the scales are tipped in the selfish favor.

---

**JustinDrake** (2023-05-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/cometshock/48/12127_2.png) CometShock:

> My assumption is that kickbacks from proposer to selected builder are inevitable.

Ok perfect, let’s try to analyse that scenario ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

- setup: There are precisely k builders (e.g. k = 2) that are capable of extracting a piece of non-commoditised MEV (e.g. 0.69 ETH from an exotic CEX-DEX arbitrage). The proposer has setup a coordination device (e.g. some fancy SGX, MPC, smart contract—you name it) to partially kickback some of the non-burned MEV to the builders.
- claim: The builders are better off bypassing the proposer altogether, with or without MEV burn.
- intuition: Indeed, one of the k builders can replicate the coordination device to fully kickback all of the non-burned MEV to the builders. For example, this coordination device could be an SGX enclave to which builders privately submit bids, and which only publicly outputs one bid which maximises value for the builders.

If you still believe the proposer can provide special coordination services with kickbacks for the builders, it would be helpful to describe such coordination services in more detail.

---

**ballsyalchemist** (2023-05-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Builders do not directly benefit from a low payload base fee floor  Naively (i.e. assuming no kickback from the proposer) builder profit margins are invariant to the payload base fee.

The proposer and builder will indirectly benefit from colluding privately to lower the base fee floor (base fee takes away the MEV that could have benefitted proposer & MAYBE builder with kickback). Even with a public-good builder who attempts to set the base fee, which imo wouldn’t be as reliable as an assumption, builders with more orderflow (possibly private orderflow) can circumvent the base fee. Furthermore, this could incentivize the creation of a private bidding marketplace on the side for builders attempting to bribe proposers. In that case, as [@CometShock](/u/cometshock) suggested,  floor can still be suppressed while proposers continue to capture the lion’s share of MEV as usual.

---

**CalabashSquash** (2023-05-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> If all the builders capable of extracting a given piece of MEV are colluding then the optimal strategy is to not bid at all for that piece of MEV, even within the D seconds tipping window. Instead, the cabal of builders is better off coordinating to distribute the MEV among themselves, a strategy possible with or without MEV burn.

Is somebody able to explain this a bit more? Mostly: How would they distribute the MEV among themselves without bidding at all?

Thank you.

---

**Pintail** (2023-05-25):

Is this proposal compatible with a proposer suffix scheme whereby censorship resistance is enhanced by permitting the proposer to include transactions after the builder releases the payload? In your view would this be desirable?

Given then number of steps involved in the builder auction, do you think this proposal would require an increase in block interval?

---

**JustinDrake** (2023-05-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/calabashsquash/48/12199_2.png) CalabashSquash:

> Is somebody able to explain this a bit more? Mostly: How would they distribute the MEV among themselves without bidding at all?

Colluding builders would need some sort of coordination technology—could be legal, smart contract, SGX, blind trust, etc. The way builders collude is an implementation detail.

![](https://ethresear.ch/user_avatar/ethresear.ch/pintail/48/5796_2.png) Pintail:

> Is this proposal compatible with a proposer suffix scheme whereby censorship resistance is enhanced by permitting the proposer to include transactions after the builder releases the payload?

Yes, this proposal is compatible with inclusion lists (see also section titled “inclusion lists” under “part 3: technical remarks”). My favourite design is called forward inclusion lists:

- list means it’s an unordered list of transactions
- forward inclusion means the next builder must include the transactions (up to the gas limit)

![](https://ethresear.ch/user_avatar/ethresear.ch/pintail/48/5796_2.png) Pintail:

> a proposer suffix scheme

An important detail with inclusion lists is whether the list is ordered or unordered. The word “suffix” suggests that the list is ordered and must be included as-is in the block. The problem with ordered lists is that they allow the proposer to extract MEV, which incentivises the proposer to be a builder and defeats the purpose of PBS. My favourite inclusion list design so far allows for both reordering and insertions by the builder (but no deletions!).

![](https://ethresear.ch/user_avatar/ethresear.ch/pintail/48/5796_2.png) Pintail:

> In your view would this be desirable?

Inclusion lists for censorship resistance is important to derisk the potential outcome where top block builders are censoring. (Thankfully the [top two builders](https://www.relayscan.io/)—builder0x69 and beaverbuilder—are not currently censoring.) Inclusion lists are even more important with MEV burn because of the reduced discretionary power of proposers to choose the winning bid.

![](https://ethresear.ch/user_avatar/ethresear.ch/pintail/48/5796_2.png) Pintail:

> Given then number of steps involved in the builder auction, do you think this proposal would require an increase in block interval?

MEV burn does not require any increase in the slot duration beyond what is required for ePBS. Having said that, ePBS itself will almost certainly require an increase in the slot duration. This is because, as you note, there are two rounds of attestations instead of just one.

In practice ePBS likely requires single slot finality (SSF) which would add yet another round of attestations (for a total of three rounds of attestations per slot). My best guess is that the slot duration will have to increase for SSF and ePBS, possibly to something like 32 seconds.

As a side note, the effectiveness of MEV burn increases with larger slot durations (see section “partial burn” under “technical similarities with EIP-1559”). The reason is that the ratio of the parameter D to the slot duration reduces. So if D = 2 seconds and the slot duration is 32 seconds, roughly 93.75% of the MEV would be burned.

---

**voidp** (2023-05-25):

Very interesting idea!

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Rational proposers will want to maximise the payload tip by guessing the payload base fee floor and accepting bids with non-zero tips after the payload base fee floor has been established.

I think I’m missing something basic: why do they need to guess since bids (including base fee) & tips are broadcast publicly?

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> claim: The builders are better off bypassing the proposer altogether, with or without MEV burn.

If by bypassing the proposer you mean the builders can wait to be elected as a proposer by themselves, that may be risky if the MEV opportunity is time sensitive.

---

**JustinDrake** (2023-05-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/voidp/48/5082_2.png) Fan Zhang:

> why do they need to guess since bids (including base fee) & tips are broadcast publicly?

Because rational proposers need to guess the minimal base fee that attesters will accept. Every attester, depending on their connectivity to the bid pool and their clock skew, may enforce a different payload base fee floor.

![](https://ethresear.ch/user_avatar/ethresear.ch/voidp/48/5082_2.png) Fan Zhang:

> If by bypassing the proposer you mean the builders can wait to be elected as a proposer

I mean the builders can collude among themselves so that the MEV does not go to proposer.

---

**wanify** (2023-05-27):

Thanks for the great write-up!

Will attesters only accept the highest payload base fee they watched as the payload base fee floor? Or do they have some flexibility? (For instance, could they consider accepting a fee that is 90% of the highest observed fee, or perhaps even the second highest base fee.)

---

**bertmiller** (2023-06-03):

Thanks for a very interesting design [@JustinDrake](/u/justindrake) ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

Right now MEV-Boost and MEV burn have a first price account with public bids. I’d like to see more analysis of the trade-offs of other auction designs - for example making the auction sealed bid could be desirable because it prevents strategic bidding (builders watching the p2p layer for bids and incrementally bidding higher) and incentivizes builders to bid their true bid value instead. Moreover, we should explore the second-price auctions as well as an alternative to first price. The tradeoff, of course, is that these introduce more implementation complexity.

---

**JustinDrake** (2023-06-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/bertmiller/48/10408_2.png) bertmiller:

> Right now MEV-Boost and MEV burn have a first price account with public bids

MEV burn is largely orthogonal to the auction design. With cryptography (e.g. FHE) one can do sealed bids as well as second-price auctions.

For sealed bidding, bidders encrypt their bids. Whenever nodes in the p2p network or attesters receive two encrypted bids, they locally apply (using FHE) the comparison function which returns an encryption of the largest of the two bids. This allows attesters to produce an encryption of their subjective base fee floor, which can then be force-decrypted (e.g. using threshold decryption or time-based decryption).

Second-price auctions only make sense with sealed bids, and those are also possible with FHE. This time, the comparison function takes three encrypted bids and returns an encryption of the largest two bids.

---

**bertmiller** (2023-06-04):

All of that makes sense to me ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) From my perspective the discourse around PBS has mostly assuming first price, public auctions (as exist at the moment) and my intention was to highlight that this is an assumption and one that we should explore alternatives to.

---

**PatrickAlphaC** (2023-07-27):

Loved reading this, big question though - sorry if it sounds brash, but would this essentially remove MEV-boost, flashbots, and the likes from the ecosystem?

It seems they would have no place if this was at the protocol level.

---

**jessiepark** (2023-08-04):

[![Untitled](https://ethresear.ch/uploads/default/optimized/2X/6/6510d594dbb85311be662186dfd7dd4e2ebe5f09_2_690x119.png)Untitled2000×346 308 KB](https://ethresear.ch/uploads/default/6510d594dbb85311be662186dfd7dd4e2ebe5f09)

> Loved reading this, big question though - sorry if it sounds brash, but would this essentially remove MEV-boost, flashbots, and the likes from the ecosystem?
>
>
> It seems they would have no place if this was at the protocol level.

Hello Patrick,

I am Jessie, a researcher at [A41](https://www.a41.io/), an APAC based organization specializing in blockchain infrastructure services with particular strengths in ecosystem growth and technical understanding of protocols.

I wanted to discuss the concept of ePBS and MEV-burn, which were addressed in the Scourge roadmap shared by Vitalik. Currently, the PBS scheme is not available within the Ethereum network, so Flashbots’ MEV-boost is filling the gap outside the protocol and accounts for up to 95% of the blocks created in the network (This is addressed as the external markets in the roadmap). Therefore, embedding these kinds of schemes will essentially remove outside players like MEV-boost, flashbots, and the likes from the ecosystem, like what you said.

However, there are concerns about centralization within Relays in this external market, and that relying on a single external market could be a single point of failure. To address this, Ethereum is working on adopting PBS within the protocol, known as ePBS in the Scourge roadmap. This integration aims to make the system more robust and decentralized. Nonetheless, implementing ePBS within the network is expected to take more than two years, during which MEV-boost will continue to play a crucial role.

It’s important to note that the implementation of MEV-burn is dependent on the successful integration of ePBS. So, MEV-burn will have enough time to be developed thoroughly and address various aspects before it becomes a reality.


*(7 more replies not shown)*
