---
source: ethresearch
topic_id: 19067
title: Addressing systemic risks – discouragement attacks against centralized validator sets
author: themandalore
date: "2024-03-21"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/addressing-systemic-risks-discouragement-attacks-against-centralized-validator-sets/19067
views: 1790
likes: 6
posts_count: 9
---

# Addressing systemic risks – discouragement attacks against centralized validator sets

This post describes a new discouragement attack which can reduce attestation and sync committee rewards of a targeted actor. This attack can theoretically be used to reduce a concentrated actor’s attestation and sync committee participation and reduces their rewards almost directly proportional to the number of validators participating in the attack.

Of the options looked at, this attack was the one with the highest likelihood to achieve a finalized chain state with the following properties:

- reduced concentrated actor(CA) validator share
- reduced CA rewards
- minimal/nonexistent penalty to participating validators
- still Ethereum (aka not a minority fork)

*back to the start - identifying validators*

The first step to targeting a validator(s) is figuring out how to identify them. Ethereum PoS validators are not identified by address but by validator index. So rather than target validators set by public key, we must map their address to a valid Index. Since every validator is assigned a validator index upon depositing, we can create a map of validator indices by looking at deposit events in the beacon contract. [1]

Note that for some CA’s, finding their addresses may be difficult (e.g. a list of validators run by a CEX). Fortunately though, LST’s and restaking protocols are much more transparent in their inner workings, so the indices are relatively easy to gather. Also note that LST’s could simply upgrade to obfuscate this or hide; but this isn’t actually too bad. An LST or CEX that has the ability to hide from the social layer is also hiding from would-be regulators or attackers looking to bribe/influence the party.

A simple example script for finding Lido validator indexes (as of Feb 2024) [can be found here](https://github.com/danflo27/LidoValidators).

*midwest discouragement attacks*

[![](https://ethresear.ch/uploads/default/optimized/2X/2/27b832436de0e0d44604db4d9d19c7a3feaf217d_2_225x449.jpeg)744×1480 76 KB](https://ethresear.ch/uploads/default/27b832436de0e0d44604db4d9d19c7a3feaf217d)

> “Every slot a new committee becomes active and is expected to provide attestations. 440k validators / 64 committees = ~17k validators/committee. 17k validators poses a problem; it’s both too much network chatter and too many signatures to aggregate all at once. Fortunately, we’ve already split committees into 64 subnets. Each subnet consists of ~250 validators, of which 16 are designated as aggregators. As validators review blocks, they broadcast their attestations to their subnet. All 16 aggregators are attempting to build the same aggregate signatures, but network conditions often make perfection possible.”[2]

Validators send attestations to committee subnet aggregators who then create an aggregated attestation that will be included in each block. To explain further, validators are partitioned into committees in each epoch, with one committee per slot. In each slot, one validator from the designated committee proposes a block. Then, all the members of that committee will attest to the newly proposed block and its position in the chain.[3] The goal of our modification is to make it so that when our validators are the subnet committee aggregators, they ignore CA attestations. Couple this with a selection rule that says when we are proposer, we only choose the aggregation that does not include CA validator attestations.

*more background*

There is a substantial overhead associated with passing attestation data around the network for every validator. Therefore, the attestations from individual validators are aggregated within subnets before being broadcast more widely.[4]

During epochs where we have participating validators as the proposer AND aggregator, we can exclude a portion of attestations from CA validators in our blacklist set. Participating proposer clients will be modified such that rather than selecting the aggregation with the most attestations, they will choose the one with the most attestations and no CA attestations (a list of validator indices created from our participating aggregator). The probability for a given committee of having at least one of the aggregators and the proposer is as follows:

[![](https://ethresear.ch/uploads/default/optimized/2X/8/87907f11b34acec350a6b0c980871d1736f682d3_2_568x351.png)Chart1600×989 55.3 KB](https://ethresear.ch/uploads/default/87907f11b34acec350a6b0c980871d1736f682d3)

A nice feature of this discouragement attack is that it scales almost identically with validator participation. What this means is that if you get 20% of the validators participating, you should be able to reduce CA attestation rewards by about 20%.[5]

The downside for proposers here is that they would lose out on some attestation rewards as ⅛ of an attestation reward goes to the proposer. There is an argument to be made that participating validators will be open to losing this small amount as the CA (competing validators) will lose 7x the amount they amount will, thus making themselves more competitive and protecting the chain from centralization.

The case where we have only the proposer (and no aggregator in a given committee) was also looked at. A participating validator could drop all aggregations with CA signatures (so have no attestations for a given committee), but then you would punish non-CA validators as well as CA validators if they were in the same subcommittee. Not to mention, the participating validator would lose more rewards, rewards which would not be offset necessarily by a decreased CA reward. For these reasons, this action is something that we will avoid, however we will need to look further into how to best include/exclude if target CA lists do match up perfectly (e.g. if you drop one honest validator is it ok if you’re still dropping 20 CA indices?).

*aftermath*

**consequences to the CA**: Missing an attestation means missing rewards, about 84.4% of base rewards to be specific (see [here](https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/attestations/#rewards) for the exact rewards structure). Depending on block space, they could try to get attached to subsequent blocks for partial rewards, but from my understanding, it rarely happens and they would likely lose out on most attestation rewards as laid out in the analysis.

[![](https://ethresear.ch/uploads/default/optimized/2X/2/24b123b146940a78f99d6b9428d93a92ce2b253b_2_565x481.png)1055×900 53.3 KB](https://ethresear.ch/uploads/default/24b123b146940a78f99d6b9428d93a92ce2b253b)

Overall, any significant percentage of validators participating could be devastating to the CA with regard to staking competitively.

**consequences to participating validators**: Committee aggregators and proposers are incentivized to include as many valid attestations as they can see in their Aggregated Attestation. For every attestation the aggregator excludes, the reward decreases (see [Rewards scale with participation](https://eth2book.info/capella/part2/incentives/rewards/#rewards-scale-with-participation)). In general, the rule for ETH2.0 is that “7/8 of rewards go to validators performing duties and 1/8 to the proposers including the evidence in blocks.” The aggregator and proposer both therefore would lose out like all ETH validators in the sense that total attestation rewards scale with participation as well, but there would be no direct punishment that would make the aggregator less competitive.[6,7]

**consequences to the protocol**: Of all discouragement attack options analyzed, excluding a limited number of attestations from certain parties seems to be the option with the lightest footprint. More research should be done on how this could affect fork-choice-rule, however theoretically it shouldn’t affect it (all else equal). One consideration to note is relative to the size of the CA. If the CA is >33% of the validator set, you cannot ignore all their attestations, as it would affect block finality. Therefore you would need to limit the number of attestations ignored to only those greater than some threshold for finality.

*dousing the beacon - ignore sync committee messages*

In addition to attestations, we can reduce up to another 3.1% of CA rewards by doing a similar aggregation censoring in the sync committee. To briefly explain, Validators are rewarded for correctly participating in sync committee signatures (each day, 512 are chosen, so very rare), which are of use to light clients. This option may even be a preferable first step versus the attestation censorship, as the sync committee is not part of internal fork choice or even required for the main protocol at all.

The same “rewards scale with participation” concept is present here, however the big difference is that we have no issues with finality, forks, or even chain issues at all, as the sync committee is for use in other protocols and not within Ethereum. That said, several light client bridge implementations take advantage of the sync committee to finalize transactions and would be affected if a large portion of the sync committee is owned by the blacklisted CA. Overall though, it seems a relatively light touch on the system, but the big downside is that the rewards here are relatively small and may not be enough to deter a CA. It might be useful to try out as a first step in testing support/ implementation issues.

*the journey is just beginning*

Other options should still be on table for addressing systemic risks, however this should be a great starting place for continuing discussions with stakeholders and developers in the Ethereum ecosystem as to the best path forward. I’m optimistic that just talking publicly about these options can be enough to deter a CA from growing any larger or maintaining threatening levels of control.

**references**

[1] [annotated-spec/phase0/beacon-chain.md at master · ethereum/annotated-spec · GitHub](https://github.com/ethereum/annotated-spec/blob/master/phase0/beacon-chain.md)

[2] https://inevitableeth.com/home/ethereum/network/consensus/pos

[3] https://arxiv.org/pdf/2003.03052.pdf

[4] [Attestations | ethereum.org](https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/attestations/)

[5] [Aggregator selection - Google Sheets](https://docs.google.com/spreadsheets/d/1H3Mux2noz2NfKC3A63VX3ZBH4q_KP0MMk3OQM4Ysxpc/edit#gid=1960537153)

[6][Upgrading Ethereum | 2.8.4 Rewards](https://eth2book.info/capella/part2/incentives/rewards/)

[7] [Upgrading Ethereum | 3.5.3 Block processing](https://eth2book.info/capella/part3/transition/block/#def_process_attestation)

**further reading**

I’ve done a few other articles on social values / systemic risks too. The first article[is here](https://medium.com/@nfett/why-values-matter-social-flexing-in-crypto-f971b23167e2), the second is [here](https://medium.com/@nfett/social-flex-2-dangers-d4701f525d28), and the third is [here](https://medium.com/@nfett/social-flex-3-options-3788c3dd4b7a).

- Vitalik’s Discouragement attacks: research/papers/discouragement/discouragement.pdf at master · ethereum/research · GitHub
- Aggregation process:

consensus-specs/specs/phase0/validator.md at dev · ethereum/consensus-specs · GitHub
- Attestations | ethereum.org
- A note on Ethereum 2.0 attestation aggregation strategies - HackMD

Sync protocol spec: [consensus-specs/specs/altair/light-client/sync-protocol.md at dev · ethereum/consensus-specs · GitHub](https://github.com/ethereum/consensus-specs/blob/dev/specs/altair/light-client/sync-protocol.md)
Rewards: [Upgrading Ethereum | 2.8.4 Rewards](https://eth2book.info/capella/part2/incentives/rewards/)
Gasper paper: https://arxiv.org/pdf/2003.03052.pdf
Understanding the [fork choice rule](https://notes.ethereum.org/@vbuterin/serenity_design_rationale?type=view#LMD-GHOST-fork-choice-rule)
Inactivity Leak: [Serenity Design Rationale - HackMD](https://notes.ethereum.org/@vbuterin/serenity_design_rationale?type=view#Inactivity-leak)
Ethereum PoS Attack and Defense: https://mirror.xyz/jmcook.eth/YqHargbVWVNRQqQpVpzrqEQ8IqwNUJDIpwRP7SS5FXs
Shout to Banteg for ideas: https://twitter.com/bantg/status/1561177300741283842
Proof-of-Stake overview: [Proof-of-stake (PoS) | ethereum.org](https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/)
Vitalik on Lex Friedman on the Social Layer: https://www.youtube.com/watch?v=3yrqBG-7EVE
Can nodes go against the protocol: [What Happens After Finality in ETH2? - HackMD](https://hackmd.io/@prysmaticlabs/finality#Can-nodes-go-against-the-protocol)
Consensus and Execution client connections: [Networking layer | ethereum.org](https://ethereum.org/en/developers/docs/networking-layer/#connecting-clients)
Mitigating attacks in PoS [Change fork choice rule to mitigate balancing and reorging attacks](https://ethresear.ch/t/change-fork-choice-rule-to-mitigate-balancing-and-reorging-attacks/11127)
Cool Epoch and Slot Visualization: https://beaconcha.in/charts/slotviz
Censorship in the PBS Stack: https://www.youtube.com/watch?v=WcJlseuhbX8

## Replies

**aelowsson** (2024-03-22):

This is a minority discouragement attack, the topic first described [here](https://ethresear.ch/t/burning-mev-through-block-proposer-auctions/14029/9) (note that the correlated reward reduction in Eq. 41 is only relevant if the attack is constant and ongoing across the epoch, otherwise it becomes smaller; h/t Francesco). I recently also discussed minority discouragement attacks [here](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448/11) and [here](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448#h-54-additional-properties-under-consideration-22), since it is a relevant topic in terms of issuance policy. In particular, note the recent specific discussion on censorship of the attestation containing the head, source and target vote [here](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448/11#head-source-and-target-vote-5). Unfortunately, I have not yet had time to publish the paper.

![](https://ethresear.ch/user_avatar/ethresear.ch/themandalore/48/1652_2.png) themandalore:

> Depending on block space, they could try to get attached to subsequent blocks for partial rewards, but from my understanding, it rarely happens and they would likely lose out on most attestation rewards as laid out in the analysis.

This would need to be analyzed in the context of a sizeable attack where missing attestations are just not spurious but systematic and significant. This gives incentives for later proposers to try to pick them up, and of course, the attacked party will be particularly incentivized to try to recoup them. I have not studied this dynamic, so if you can perform a more detailed study on how the specific process of recouping such attestation could play out (or not play out), it would be very welcome!

Note that focusing on missed rewards as in your post does not give the full picture. Penalties must also be accounted for, as in previous links. The attacked party will not only lose out on rewards, it will get penalized if the source and target votes are not included. The correct griefing factor if all votes indeed would be dropped (which I would suggest cannot be counted on), while ignoring the correlated reward reduction for simplicity, is then

G= \frac{14+26\times2+26\times2}{(14+26+26)/7}\approx12.5

It should be noted, as described [here](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448/11#minority-discouragement-attack-against-sync-committee-attestations-2), that targeting sync-committee attestations gives a griefing factor of G=14, and that these cannot be picked up later.

Finally, a minority discouragement attacker is still susciptible to social slashing, and would need to make some calculus as to the risks before proceeding. But it is indeed true that these attacks exist, and it is important to keep them in mind in the design of Ethereum’s micro incentives going forward.

---

**keyneom** (2024-03-24):

These seem like pretty concerning attacks in the long run, why do you think they aren’t too much of a concern right now? I would think we need to adjust rewards so that losses are equal for the excluded and the excluder. Is there a concern in doing so?

---

**themandalore** (2024-03-25):

thanks for the comment!

I think the answer here would be a) it’s not that bad of an attack since you need to coordinate so many validators to have a meaningful dent, b) would be painfully obvious and we could always social slash them and c) you don’t really want to make it even because then it pushes even more rewards to the proposer (vs attestors) which makes it harder for solo stakers (reward smoothing is tough)

---

**themandalore** (2024-03-25):

Awesome stuff!  Can’t believe I hadn’t seen this.  But thanks for the factor adjustment.  If anything it makes it way stronger of an attack which is cool.  I think we’re just in this weird competitive world where social pressures and seeming “aligned” sort of keeps these parties in check from doing attacks like this.  I think you’re right that they would probably at least pick up their own attestations, but from my understanding (talked to a few validators), you need space in a block to do that, and given the low amount given to proposers, they usually don’t even check for others. Would love to know if you understand it differently though

---

**keyneom** (2024-03-26):

Pretty concerning might have been an overstatement but I’d think this is an attack that has a reasonable fix without a lot of downsides.

Coordinating a lot of validators is pretty easy for someone like coinbase. Also, it would be exceptionally hard for them to be detected. They don’t have to have a real specific target–just any validator they don’t run. Choose one at random, it can change each time, Everytime they do so it helps increase their relative rewards compared to everyone and allows for further centralization. It is an attack that is actually much easier for a CA to execute and with random targets it’s much harder to detect than a bunch of independent actors targeting a CA where you can see the impact on their returns.

Granted it is a pretty slow attack and you would still perhaps see the community push back if you saw one CA get “dangerously” large. But if be more concerned about an oligarchy emerging where no single entity has 33% but over time it eliminates solo stakers, etc from making up a meaningful part of the network. This happens naturally as the larger CAs execute the attack to increase their relative margins just enough to not draw too much attention. They already outperform.

Regarding the issues with rewards going to the proposer, I’d argue that it would be preferable and that smoothing pools do a great job of handling this. What’s hard about reward smoothing nowadays? Perhaps I’m just ignorant to the complications.

---

**themandalore** (2024-03-26):

I think here you’d just rely on some statistics (would love to see these) on how many attestations each proposer includes.  If you’re far off the average consistently, I’d think we’d just have to rely on some social pressure (or the reverse attack) to limit it

---

**keyneom** (2024-03-27):

In retrospect, smoothing pools might not be a real fix anyways. They actually make things more difficult. An attacker can join a smoothing pool and the lost revenue from executing an attack is diluted across the smoothing pool (as proposer). So even with evenly split losses between the proposer and attestor you can end up with a profitable attack. Right?

---

**themandalore** (2024-03-27):

It would definitely still be profitable in the sense that they would lose more than the proposer.  The inactivity leak portion (as aelowsson pointed out) really makes it much more severe on the attester, especially as the coordination rises (if a 40% CA agrees to block out a 20% of the attestations, those 20% targeted would get hit hard if they don’t get in a subsequent block)

