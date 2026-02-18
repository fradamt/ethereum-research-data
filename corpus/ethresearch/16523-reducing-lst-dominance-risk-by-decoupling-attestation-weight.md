---
source: ethresearch
topic_id: 16523
title: Reducing LST dominance risk by decoupling attestation weight from attestation rewards
author: minimalgravitas
date: "2023-08-31"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/reducing-lst-dominance-risk-by-decoupling-attestation-weight-from-attestation-rewards/16523
views: 2452
likes: 17
posts_count: 9
---

# Reducing LST dominance risk by decoupling attestation weight from attestation rewards

**Abstract:**

If we end up increasing the maximum effective balance, the larger validators could have a  reduced attestation power relative to the same amount of stake in multiple smaller validators. Offering increased attester incentives (i.e. extra rewards) for these larger validators would encourage uptake of the option in return for the reduced relative power over the network.

**Background:**

Large staking-as-a-service providers control a large portion of Ethereum validators. In particular Lido has either passed or is about to pass 33% of all staked ether. As many in the community have [explained already](https://twitter.com/dannyryan/status/1524044527828303872), this represents a threat to the perceived credible neutrality of the network and as such threatens future adoption and the fulfillment of Ethereum’s potential. Efforts to elicit voluntary caps on their growth have been futile, with their DAO [voting almost unanimously not to self limit](https://snapshot.org/#/lido-snapshot.eth/proposal/0x10abedcc563b66b1adee60825e78c387105110fa4a1e7354ab57bc9cc1e675c2).

There are now frequent discussions amongst the EthFinance Community (e.g. [A](https://old.reddit.com/r/ethfinance/comments/160phdq/daily_general_discussion_august_25_2023/jxo14ll/), [B](https://old.reddit.com/r/ethfinance/comments/160phdq/daily_general_discussion_august_25_2023/jxooqnv/), [C](https://old.reddit.com/r/ethfinance/comments/161lowk/daily_general_discussion_august_26_2023/jxt6ypg/) just in the last few days) and presumably elsewhere regarding this issue, and people are starting to [raise the question](https://twitter.com/hanni_abu/status/1694833660292219039) of when social slashing should be considered as a way to protect the ecosystem, despite how drastic this option seems.

**Proposal:**

I believe that the Ethereum ecosystem’s real superpower, it’s potential to slay Moloch, comes from the ability to design and adapt incentive structures, and so that is the tool I think we should use here. We set up a system to make use of their profit maximalist position by forcing a choice between increased rewards vs increased control.

This idea builds from [@mikeneuder](/u/mikeneuder)’s proposal to [increase the max_effective_balance of validators](https://ethresear.ch/t/increase-the-max-effective-balance-a-modest-proposal/15801) and relies upon that being implemented. Then we give extra attestation rewards to validators with larger balances, but at the same time reduce their attestation weight relative to the same number of ether in smaller balances.

So for example… Alice has 4x validators with 32 ether, earning issuance at around 3.5% (ignore transaction tips and MEV) so say 4.48 ether per year and with attestation power of 4 * 32 = 128 ether.

Bob has 1 validator with 128 ether, earning issuance at 3.5% * 1.04 = 4.66 ether (for example) but with an attestation power of only √4 * 32 = 64 ether (for example).

In this way, if all Lido (and centralized exchanges) care about is getting as much profit as possible they are incentivized to go for big validators with to take advantage of the Rich-get-richer™ mechanism. In doing so they reduce the influence they have over the network and put relatively more power into the hands of smaller validators.

Obviously the parameters for increased rewards and reduced power could be adjusted to whatever seems appropriate, but as a back-of-the-envelope approximation though, using a Max_Effective_Balance of 1024 and only the big 4 centralized staking pools (Lido, Coinbase, Binance and Kraken) taking up the option, this could reduce Lido’s control over Ethereum to about 11.5%.

**However:**

I’ve been slow thinking this idea for a while, and it has a lot of obvious disadvantages:

- Massively fundamental change to how the Beacon Chain works, which I don’t even know is possible (if anyone can help me understand this I would really appreciate it);
- Reduced overall attestation weight would reduce Ethereum’s security in terms of vulnerability to 33%/51%/66% attacks (though I don’t think this would be to particularly risky levels);
- Increased overall rewards would slightly impact Ethereum’s economic policy of minimum viable issuance;
- Perception of rewarding the bigger validators more would probably be terrible in the wider crypto community (this might be the most serious issue);
- In the (very) long term would this just delay the problem, postponing discovery and implementation of a better solution.

**Conclusion:**

The idea has many flaws, and it may be that it would have a larger negative impact than the problem it attempts to solve, but as yet I haven’t encountered a solution proposed to Lido’s growing dominance that seems more reasonable. While this doesn’t seem quite right yet, it seems to me to be the right ‘shape’ of solution, using incentive gradients rather than brutal forks would presumably be less messy if nothing else! I am very open to learning and criticism, so please do point me towards any resources that might help me with this topic, whether that’s links to help understand how possible (or not) this idea may be in practice, or to better solutions that other people are working on.

**Disclaimer:**

My educational background is in astrophysics rather than computer science/cryptography/ or anything more relevant - therefore please assume that my maths uses liberal [approximations](https://xkcd.com/2205/) and should be taken as indicative only.

## Replies

**mikeneuder** (2023-09-01):

hey [@minimalgravitas](/u/minimalgravitas) ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

very interesting idea. i don’t see any technical reason why this wouldn’t be possible. however, i share a lot of your concerns.

![](https://ethresear.ch/user_avatar/ethresear.ch/minimalgravitas/48/12494_2.png) minimalgravitas:

> Perception of rewarding the bigger validators more would probably be terrible in the wider crypto community (this might be the most serious issue);

i think this is the core of the issue. and beyond just “perception” of rewarding bigger validators with larger rewards, by making the APR higher for bigger stakers we just further push everyone into joining a pool. in the long run, if 100% of staked ETH is in a pool, and all the validators are 2048 ETH validators to max out their rewards, then they still have the exact same proportional power over the fork-choice rule that they had before (which i think you hint at in your last bullet point).

i love the ideation still and would be super happy to receive pushback. personally, i am thinking a ton about this lately too. for example [@dankrad](/u/dankrad)’s [post](https://notes.ethereum.org/bW2PeHdwRWmeYjCgCJJdVA) on liquid staking maximalism is a fascinating thought experiment too.

---

**arbora** (2023-09-01):

Thanks for posting this idea!

To me, the core observation is that staking entities actually running nodes might be divided up into three categories:

A. Solo/decentralized pool stakers

B. Centralized pool operators who only care about profit from staking rewards

C. Centralized pool operators who actually would consider attacking the network if they got big enough

Entities in A are not a threat to Ethereum, because they individually control relatively small portions of the stake, and therefore contribute to decentralization, rather than harming it.

Entities in B and C control enough of the stake that they have the power to harm Ethereum, either by colluding or in the case of Lido, even by operating unilaterally. Currently we have no way to distinguish between entities in B and in C, and they have no way to behave differently onchain to signal their intents.

If, as you suggest, we decoupled attestation weighting from staking rewards, at the same time that we bump up the Max_Effective_Balance, that gives B and C a way to distinguish themselves.

Entities in B are purely profit-motivated, and if provided a means of coalescing their enormous validator counts into e.g. 1/32nd that number (for 1024 Max_Effective_Balance) or 1/64th (for 2048), would very likely do so, even, IMO, without the added (and problematic) incentive of higher rewards for doing so. There are various operational and latency overheads created by running many validators, versus fewer, and I believe that would provide sufficient incentive for them to consolidate. Some might consolidate their entire validator sets, while others might consolidate only new validators going forward, but both would be helpful. And perhaps more importantly, it would provide a way for those pools to signal that they are benign entities with no intention of attacking the chain. Profit-motivated, neutral staking pools do not want to risk their cash cow (and some might even go so far as to care about their customers’ financial wellbeing!) and willingly reducing their voting weight on the chain (while retaining the same rewards) would go a long way towards demonstrating alignment with Ethereum, and ensuring the safeguarding of their income.

On the other hand, entities in C explicitly would not desire to consolidate their validators, either existing or new ones, because it would reduce their voting weight and ability to attack the chain. Pools that declined to do so would therefore immediately draw extra attention, scrutiny, and pressure from the Ethereum community. Clearly that alone cannot check the growth of large staking pools (look no farther than Lido), but knowing which pools were benign and which were suspicious would be quite helpful.

One large issue with purely voluntary (i.e. not incentivized) consolidation, though, is the following: if benign staking pools reduce their voting weight, it leaves the malicious ones that decline to do so with proportionally higher voting weights, reducing the barrier to attack for them, and decreasing the security of the chain.

Resolving that issue does seem to lead back to your proposal to increase profits in exchange for consolidation. That effectively puts a price on remaining in camp C: keeping open the option of being malicious incurs a potentially significant cost over consolidating and taking the rewards. An attacker that truly does not care about profit, and is solely planning to attack the chain, would not be deterred by this, but they would need to make up the difference to their customers, if they wanted to continue gaining enough stake to attack the network, and so it would not be merely lost profit, but an actual expense.

Overall I agree that this is definitely an avenue worth exploring, but as you say, it would have deep structural and game theory implications for the economic security of Ethereum, and therefore would require extensive research as a next step.

---

**minimalgravitas** (2023-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> by making the APR higher for bigger stakers we just further push everyone into joining a pool. in the long run, if 100% of staked ETH is in a pool, and all the validators are 2048 ETH validators to max out their rewards, then they still have the exact same proportional power over the fork-choice rule that they had before (which i think you hint at in your last bullet point).

Thanks for the feedback, and yes you’re right, if we incentivized bigger pools then the big operators would end up growing faster, but the rate at which that growth occurs I was assuming would be slow - though it obviously depends on the amount of extra rewards.

If the concept is not technically impossible then maybe my next step should be to start playing with different values for increased rewards and see how the effect the balance (pun intended…) over various timescales, with various assumptions on adoption etc etc.

![](https://ethresear.ch/user_avatar/ethresear.ch/arbora/48/13075_2.png) arbora:

> Currently we have no way to distinguish between entities in B and in C, and they have no way to behave differently onchain to signal their intents.

I wasn’t ever really thinking about type C entities, actual hostile attackers, but I can definitely see your point about why it would be useful to be able to see who was signaling that they were not one.

One difficulty that I’m struggling with is that if a malevolent staking pool is really just out to disrupt Ethereum, how do you start to think about what effect financial costs would have on their decisions?

There certainly seems to me to be some interesting possibilities that open up with the ability to have different ‘sizes’ of validator, but yea, not a space that will be easy to optimize a best answer for.

---

**ryanberckmans** (2023-09-02):

Fascinating idea.

> Then we give extra attestation rewards to validators with larger balances

> Bob has 1 validator with 128 ether, earning issuance at 3.5% * 1.04 = 4.66 ether (for example) but with an attestation power of only √4 * 32 = 64 ether (for example).

If LSTs have a structural requirement to distribute stake across dozen(s) of validators, does that mitigate the need to give extra rewards to larger validators to produce the desired incentives?

For example, if this proposal was implemented as-is but with no extra rewards for larger validators, then Lido’s staked ETH would still be spread across a minimum of O(independent node operators) number of validators, since it seems unworkable for ~two dozen independent node operators to share a single validator. Lido’s node operators may collude to create a mega-validator using eg. DVT, but there’s no additional rewards in it for them because they’d only get more power and not more money. In fact, removing the `1.04` large validator reward bonus may remove any incentive Lido validators have to form a mega validator using DVT (if such a thing were possible, to put all Lido staked ETH in a single validator).

---

**minimalgravitas** (2023-09-04):

Thanks for the response! If the extra reward wasn’t there then what would be the motivation for them to form a single mega-validator in the first place? Just reduced infrastructure requirements?

I’d also understood the ‘Increase Max_Effective_Balance’ proposal to still have some upper limit, significantly higher than current 32 ether, but not completely uncapped - I might well have misunderstood that though.

---

**aimxhaisse** (2023-09-06):

> If the extra reward wasn’t there then what would be the motivation for them to form a single mega-validator in the first place? Just reduced infrastructure requirements?

One drawback from the perspective of large node runners in the current proposal is the increase in slashing risk. i.e: if you get slashed on a mega-validator, the entire stake is slashed at once and you can’t react, while experience shows that correlated slashes is not a single event and tend to be spread over time, where you can have time to react to stop the bleeding.

So the incentive of having the extra-reward for the extra-risk could be a motivation.

---

**mikeneuder** (2023-09-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/aimxhaisse/48/12694_2.png) aimxhaisse:

> One drawback from the perspective of large node runners in the current proposal is the increase in slashing risk

Check out [Slashing penalty analysis; EIP-7251](https://ethresear.ch/t/slashing-penalty-analysis-eip-7251/16509)! We examine the slashing penalties and propose a few changes to reduce the risk for large validators ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**kertapati** (2023-09-28):

Intriguing discussion on Ethereum’s staking mechanics. One dimension that’s not fully fleshed out is the potential for a graded rewards system. In the same way that staking more could bring about higher rewards, could we consider other metrics that factor into these rewards? This could offer an elegant way to balance the financial incentives against the network’s security needs.

