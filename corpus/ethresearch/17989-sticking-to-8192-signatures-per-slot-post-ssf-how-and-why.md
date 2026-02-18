---
source: ethresearch
topic_id: 17989
title: "Sticking to 8192 signatures per slot post-SSF: how and why"
author: vbuterin
date: "2023-12-27"
category: Proof-of-Stake
tags: [single-slot-finality]
url: https://ethresear.ch/t/sticking-to-8192-signatures-per-slot-post-ssf-how-and-why/17989
views: 33027
likes: 241
posts_count: 43
---

# Sticking to 8192 signatures per slot post-SSF: how and why

A major difference between Ethereum and most other (finality-bearing) proof of stake systems is that Ethereum tries to support a very high number of validators: we currently have 895,000 validator objects and a naive Zipf’s law analysis implies that this corresponds to tens of thousands of unique invididuals/entities. The purpose of this is to support decentralization, allowing even regular individuals to participate in staking, without requiring everyone to give up their agency and cede control to one of a small number of staking pools.

However, this approach requires the Ethereum chain to process a huge number of signatures (~28,000 today; 1,790,000 post-SSF) per slot, which is a very high load. Supporting this load entails a lot of technical sacrifices:

- It requires a complicated attestation propagation mechanism involving attestations being split between multiple subnets, needing to hyper-optimize BLS signature operations to verify these signatures, etc.
- We don’t have a clear drop-in quantum-resistant alternative that is anywhere near efficient enough.
- Fork choice fixes like view merge become much more complicated because of the inability to extract individual signatures.
- SNARKing the signatures is hard, because there’s so many of them. Helios needs to operate over a specialized extra signature, called the sync committee signature
- It increases safe minimum slot times by requiring three sub-slots in a slot instead of two.

The signature aggregation system *feels* reasonable at first glance, but in reality it creates [systemic complexity](https://vitalik.eth.limo/general/2022/02/28/complexity.html) that bleeds out all over the place.

Furthermore, it does not even achieve its goal. The minimum requirement to stake is still 32 ETH, which is out of reach for many people. **And just from a logical analysis, it seems infeasible to make an everyone-signs-in-every-slot system *truly* enable staking for the average person in the long term**: if Ethereum has 500 million users, and 10% of them stake, then that implies 100 million signatures per slot. Information-theoretically, processing slashing in this design requires at least 12.5 MB per slot of data availability space, roughly as much as the target for full daksharding (!!!). Perhaps doable, but requiring staking itself to be dependent on data availability sampling is a large complexity gain - and even that is only ~0.6% of the world population staking, and does not begin to get into the *computational* issue of verifying that many signatures.

Therefore, instead of relying on cryptographers to create magic bullets (or [magic bulletproofs](https://hackmd.io/@nibnalin/bls-multiplicity)) to make an ever-increasing number of signatures per slot possible, **I propose that we make a philosophical pivot: move away from having such an expectation in the first place**. This will greatly expand the PoS design space, and will allow for a large amount of technical simplification, make Helios more secure by allowing it to SNARK over Ethereum consensus directly, and solve the quantum resistance issue by making even boring long-existing signature schemes like [Winternitz](https://asecuritysite.com/encryption/wint) viable.

## Why not “just do committees”

Many non-Ethereum blockchains, faced with this exact problem, use a committee-based approach to security. During each slot, they randomly choose N validators (eg. N ~= 1000), and those are the validators responsible for finalizing that slot. It is worth reminding why this approach is insufficient: **it does not provide accountability**.

To see why, suppose that a 51% attack does happen. This could be a finality-reversion attack or a censorship attack. For the attack to take place, you do still need economic actors controlling a large fraction of the stake to *agree to* in the attack, in the sense of running software that participates in the attack with all validators that end up being selected for the committee. The [math of random sampling](https://vitalik.eth.limo/general/2017/12/31/sharding_faq.html#how-is-the-randomness-for-random-sampling-generated) ensures this. However, **the penalty that they incur for such an attack is tiny**, because most of the validators that agreed to the attack end up not being seen because they are not chosen for the committee.

Ethereum, at present, takes the opposite extreme. If a 51% attack takes place, a large fraction of the *entire* attacking validator set has their deposits slashed. The cost of an attack is at present around 9 million ETH (~$20 billion), *and that assumes network synchrony breaks in a way that maximally favors the attacker*.

I argue that this is a high cost, but it is *too high* a cost, and we can afford to make some sacrifices in the matter. Even a cost of attack of 1-2 million ETH should be totally sufficient. Furthermore, the main centralization risks of Ethereum that are present today are in a totally different place: large-scale staking pools would not be *that* much less powerful if the minimum deposit size were reduced to near-zero.

**This is why I advocate a moderate solution: one that makes some sacrifices on validator accountability, but still keeps the amount of total slashable ETH quite high, but in exchange gets us most of the benefits of a smaller validator set**.

## What would 8192 signatures per slot under SSF look like?

Assuming a traditional two-round consensus protocol (like what Tendermint uses, and like what SSF would inevitably use), you need two signatures per slot per participating validator. We need to work around this reality. I see three major approaches for how we could do this.

### Approach 1: go all-in on decentralized staking pools

The [zen of Python](https://peps.python.org/pep-0020/) contains a really key line:

> There should be one-- and preferably only one --obvious way to do it.

For the problem of making staking egalitarian, Ethereum currently violates this rule, because we are simultaneously executing on *two* distinct strategies toward this goal: **(i) small-scale solo staking**, and **(ii) decentralized stake pools using [distributed validator technology (DVT)](https://ethereum.org/en/staking/dvt/)**. For the reasons described above, (i) is only able to support *some* individual stakers; there will always be very many people for whom the minimum deposit size is too large. However, Ethereum is paying the very high technical burden costs of supporting (i).

A possible solution is to give up on (i) and go all-in on (ii). We could raise the min deposit size to 4096 ETH and make a total cap of 4096 validators (~16.7 million ETH). Small-scale stakers would be expected to join a DVT pool: either by providing capital or by being a node operator. To prevent abuse by attackers, the node operator role would need to be reputation-gated somehow, and pools would compete by providing different options in this regard. Capital provision would be permissionless.

We can make pooled staking in this model more “forgiving” by capping penalties, eg. to 1/8 of total provided stake. This would allow reducing trust in node operators, though it’s worth approaching this carefully due to [the issues outlined here](https://notes.ethereum.org/@vbuterin/staking_2023_10#The-role-of-delegators).

### Approach 2: two-tiered staking

We create two layers of stakers: a “heavy” layer with a 4096 ETH requirement that participates in finalization, and a “light” layer with *no* minimum (also no deposit and withdrawal delay, and no slashing vulnerability) that adds a second layer of security. For a block to finalize, *both* the heavy layer needs to finalize it *and* the light layer needs to have >= 50% of online light validators attest to it.

This heterogeneity is good for censorship and attack resistance, because one would need to corrupt *both* the heavy layer and the light layer for an attack to succeed. If one layer is corrupted and not the other, the chain halts; if it’s the heavy layer that was corrupted, the heavy layer can be penalized.

Another benefit of this is that the light layer can include ETH that is simultaneously used as collateral inside applications. The main downside is that it makes staking less egalitarian by enshrining a divide between small-scale stakers and larger stakers.

### Approach 3: rotating participation (ie. committees but accountable)

We take an approach in a similar spirit to the [super-commtittee design proposed here](https://notes.ethereum.org/@vbuterin/single_slot_finality#Idea-1-super-committees): for each slot, we choose 4096 currently active validators, and we carefully adjust that set during each slot in such a way that we still have safety.

However, we make some different parameter choices to get the “maximum bang for our buck” within this framework. Particularly, we allow validators to participate with arbitrarily high balances, and if a validator has more than some quantity M of ETH (which would have to be floating) then they participate in the committee during every slot. If a validator has N < M ETH, then they have a \frac{N}{M} probability of being in the committee during any given slot.

**One interesting lever that we have here is decoupling “weight” for incentive purposes, vs “weight” for consensus purposes**: each validator’s reward within the committee should be the same (at least for validators with \le M ETH), to keep average rewards proportional to balance, but we can still make *consensus* count validators in the committee weighted by ETH. This ensures that breaking finality requires an amount of ETH equal to > \frac{1}{3} of the total ETH in the committee.

A back-of-the-nakpin Zipf’s law analysis would compute that amount of ETH as follows:

- At each power-of-two level of total balance, there would be a number of validators inversely proportional to that balance level, and the total balance of those validators would be the same.
- Hence, the committee would have an equal amount of ETH participating from each balance level, except the levels above the barrier M, where the validator is in the committee always.
- Hence we have k validators at each of log_2(M) levels, and k + \frac{k}{2} + ... = 2k validators at the levels above. So k = \frac{4096}{log_2(M) + 2}.
- The largest validator would have M * k ETH. We can work backwards: if the largest validator has 2^{18} = 262144 ETH, this would imply (roughly) M = 1024 and k = 256.
- The total ETH staked would be:

The full stake of the top 512 validators (2^{18} * 1 + 2^{17} * 2 + ... + 2^{10} * 2^{8} = 2359296)
- Plus the randomly sampled smaller stakes (2^8 * (2^9 + 2^8 + 2^ 7 ...) \approx 2^8 * 2^{10} = 2^{18})
- In total we get 2621440 ETH staked, or a cost of attack of ~900k ETH.

The main disadvantage of this approach is somewhat more in-protocol complexity to randomly choose validators in such a way that we get consensus safety even across committee changes.

The main advantages are that it preserves solo staking in a recognizable form, preserves a one-class system, and even allows for the minimum deposit size to be reduced to a very low level (eg. 1 ETH).

## Conclusions

If we establish that in a post-SSF protocol, we want to stick to 8192 signatures, this makes the job much easier for technical implementers, as well as builders of side infrastructure like light clients. It becomes much easier for anyone to run a consensus client, and users, staking enthusiasts and others would be able to immediately work off of that assumption. The future load of the Ethereum protocol becomes no longer an unknown: it can be raised in the future through hard forks, but only when developers are confident that technology has improved enough to be able to handle a larger number of signatures-per-slot with the same level of ease.

The remaining job would be to decide which of the above three approaches, or perhaps something else entirely, we want to go with. This would be a question of which tradeoffs we are comfortable with, and particularly how we navigate related issues such as liquid staking, which could be resolved separately from the now-much-easier technical questions.

## Replies

**MicahZoltu** (2023-12-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Even a cost of attack of 1-2 million ETH should be totally sufficient.

There are many governments around the world who spend that much on one missile, or one plane.  We should be designing systems resilient to state attackers who are willing to spend money to ruin your day.  While 1-2M ETH *may* be enough to deter them from attacking, we have evidence that they will spend far more than this to achieve their goals, and many governments do appear to be heading in the direction of “destroy crypto” as one of their goals.

Of course, I cannot say that 9M ETH is enough either, or maybe both are in fact more than enough!  However, I don’t think it is as obvious as you imply that we can safely reduce the security budget.  Lindy doesn’t apply to these things, because everything will be fine right up until it isn’t, then it is all very very bad all of a sudden.

---

**vbuterin** (2023-12-27):

> There are many governments around the world who spend that much on one missile, or one plane. We should be designing systems resilient to state attackers who are willing to spend money to ruin your day. While 1-2M ETH may be enough to deter them from attacking, we have evidence that they will spend far more than this to achieve their goals, and many governments do appear to be heading in the direction of “destroy crypto” as one of their goals.

A single 51% attack is not fatal to Ethereum; if Ethereum gets attacked once we can always adjust the params to push the security budget back up. But I think the better argument here is that there are *all kinds of strategies* to destroy Ethereum that would take much less than 1-2M ETH: social layer manipulation, supply chain attacks on software libraries, attacks on the p2p layer, etc.

And I would argue that the best way to defend against the latter two especially is to make the protocol as technically simple as possible, minimize or avoid the use of crazy constructions that have 64 subnets etc. And that the benefits from doing *that* are much greater than the downsides of a “front-door” 51% attack costing 1 million ETH instead of 9 million ETH.

Security through simplicity, rather than security through getting a big headline number inside a particular mathematical model of security that doesn’t even correspond to the easiest available attack vector.

---

**hanniabu** (2023-12-27):

Great post and lots to think about!

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A single 51% attack is not fatal to Ethereum;

I guess that depends on perspective. Although Ethereum would live on, I know many in the ecosystem that would consider this a failure and it would love *a lot* of credibility.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I think the better argument here is that there are all kinds of strategies to destroy Ethereum that would take much less than 1-2M ETH: social layer manipulation, supply chain attacks on software libraries, attacks on the p2p layer, etc.

I think this is a dangerous mindset. Yes, while there are other cheaper attack vectors that we should work on improving, we ***should not*** use the weakest link as the bar for security. We should set the threshold high and work towards raising the bar across all attack vectors.

---

**RichardKoh1** (2023-12-27):

> I think this is a dangerous mindset. Yes, while there are other cheaper attack vectors that we should work on improving, we should not use the weakest link as the bar for security. We should set the threshold high and work towards raising the bar across all attack vectors.

This is what Ethereum has already been doing for years already imo. How long do you expect the chain to stay in a limbo state susceptible to all kinds of attacks and unscalable until the 100% perfect solution is found? At a certain point before mass adoption occurs, decisions must be made using all the info and tech currently available.

---

**uri-bloXroute** (2023-12-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Approach 1: go all-in on decentralized staking pools

I’d like to emphasize that A LOT of Ethereum’s current censorship resistance today is coming from the 7% who do not participate in PBS, mostly solo-stakers

we should be mindful of their value of individual proposers when considering going all-out staking pools.

not to dis it, but emphasizing this point.

---

**vbuterin** (2023-12-27):

> I think this is a dangerous mindset. Yes, while there are other cheaper attack vectors that we should work on improving, we should not use the weakest link as the bar for security. We should set the threshold high and work towards raising the bar across all attack vectors.

This is a fair point. I think the better counterargument here is that simplifying the protocol *is* the way to raise a whole bunch of security weakpoints that we have including those that we don’t know about (the most dangerous!). And reducing the computational load of a node makes staking more accessible, increasing censorship resistance in a different way.

---

**sasicgroup** (2023-12-27):

What are the specific technical challenges of processing 1,790,000 signatures per slot after the SSF upgrade? and  How would reducing the number of validators from 8192 to a lower number impact the security of the Ethereum network?

---

**mattstam** (2023-12-27):

If Approach 1 is adopted, how much of the committee & subnet sharding could be simplified / removed from the current protocol?

My understand is that both the current protocol and full DVT approach are topologically very similar - the main difference being that DVT has the potential to reduce load by taking the validator sharding and signature aggregation schemes out of protocol.

Giving individual operators the responsibility to form there own committees naturally makes the network more performant. For example, the current protocol may assign two validators on opposing ends of the world to the same subnet. This problem is resolved when operators can manually join a DVT pool with peers they know they can perform well with.

---

**OisinKyne** (2023-12-28):

To start with with my (biased) thoughts on Approach 1. The problem with solo staking is not only the bond, but also the return on it. If you take it down to 1 eth, the ~3% you’re making on it is ~$70 a year. Which needs a lot of sunk cost accounting to justify. Imo to decentralise the validator set effectively we need to make it appealing to have people delegate to these home stakers (we can see there is and always will be people who will want to delegate away this task for a fee), and the best way I’ve been able to see that achieved is through squad staking lowering the barrier to staking with non-professional entities. My aspiration is to get ‘normal people’ from low cost of living countries participating in DVs and earning a percentage of the rewards as a commission that amounts to a meaningful supplement to their annual income. At current parameters that’s maybe a 1% cut on a 100 validator cluster making circa ~$2.5k p.a. About the return of a single validator  but without the capital.

I’m not so sure of approach 2. I don’t know how much gain there is from the non slashable tier, and I fear high capital requirements for the primary tier would lead to high hardware and particularly bandwidth requirements, and Ethereum would drift  away from its accessibility to consumer hardware. I’d maybe restrict the high performance machine requirements to proposers rather than all validators. (And take in ePBS with CR lists for that matter).

I have one maybe basic question about SSF that I may as well ask. Would Ethereum retain something like GHOST that would continue liveness on in the event of losing a supermajority’s participation in an SSF paradigm, or would Ethereum opt to halt? I imagine it like SSF pulling forward Casper FFG from two epochs to a single slot, but were it to fail, ghost protocol would still allow for blocks to be produced that will eventually get finalised? Ethereum has lost its existing 2 epoch finality guarantee maybe twice for short periods, but I assume that it would be much more disruptive to  the community were it to halt in those instances rather than just lose finality guarantees, but maybe strict SSF is what is needed by L2s for atomic composability, so idk.

My suggestions on the different paths to pursue include:

⁃ Proceed with a change like the max effective balance one, that allows validators to go up to a certain stake (I would prefer to keep the option of ‘small’/32e validators for posterity and permissionlessness) [EIP-7251: Increase the MAX_EFFECTIVE_BALANCE](https://eips.ethereum.org/EIPS/eip-7251)

⁃ Get rid of committees so we can aggregate larger. Make aggregations attributable and economically rewarded/punished in protocol such that they are more respected.  (Could be ignored if we fast track the SSF duty) [EIP-7549: Move committee index outside Attestation](https://eips.ethereum.org/EIPS/eip-7549)

⁃ I personally am a fan of the proposals relating to validator index reuse, though I may not be completely up to speed on the technical issues relating to adopting it. The indices being allocated are already 20% larger than the active set, and that will get worse with time. [EIP-6914: Reuse Withdrawn Validator Indices](https://eips.ethereum.org/EIPS/eip-6914)

⁃ Consider introducing something instead of the existing sync committee duty that looks like approach 3 in [@vbuterin](/u/vbuterin)’s above post, bring it in not as the ultimate source of finality at first, but as an economically secured light client proof, and once happy it’s stable, maybe make it the canonical finality for the chain, and deprecate Casper FFG?

They are my somewhat disjointed thoughts on the matter. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

tl;dr: community led squad staking clusters are something we should encourage for the decentralisation of the network. SSF with halting is scary and I would suggest we be hesitant to give up weak liveness guarantees for the L1 that aims to be the most decentralised and credibly neutral and ww3 resistant.

---

**vbuterin** (2023-12-28):

> SSF with halting is scary

To be clear I do not support SSF with halting. When I say “SSF” you should always understand that as “something Tendermint-like but also with an LMD-GHOST-like fork choice rule that runs whenever finality does not happen”.

The thoughts on low-value solo staking are interesting! I think one big issue here is the raw technical burden of solo staking “meaningfully”: right now it’s a brute fact that you need a powerful computer and hundreds of gigabytes to solo stake, while you *could* theoretically participate in DVT with a light client, that’s not really meaningful for network security because you would just be following along whatever the majority of other stakers says regardless of whether they’re right or wrong. If that is not solved, solo staking for the masses will have to continue to fight a major uphill battle, but if it is solved, then lots of things become possible.

Given the above, in the short term the version of “squad staking” that makes sense thus becomes a squad all trusting one person in their squad, and accepting the risk of being leaked or slashed if that one person screws up. This at least contains the presently-high load of staking to one participant.

One other benefit that DV *can* provide for people in developing countries, especially regions with internet connectivity problems, is increasing uptime through safety-in-numbers: if you have five people and they can each only guarantee a 90% uptime, then with a 3-of-5 you can increase your uptime to ~99%.

So given that, if DV provides enough benefits that it is “the” clear way to stake for lower-income people, that is an argument for option (1): it’s the best solution so might as well rally around it and get all the protocol simplifications we can from doing so. But if we’re only half-convinced, then it’s an argument for (2) or (3), as those options are just as friendly to DV as (1) are but they also leave room for true solo stakers.

---

**vbuterin** (2023-12-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/mattstam/48/11645_2.png) mattstam:

> If Approach 1 is adopted, how much of the committee & subnet sharding could be simplified / removed from the current protocol?
>
>
> My understand is that both the current protocol and full DVT approach are topologically very similar - the main difference being that DVT has the potential to reduce load by taking the validator sharding and signature aggregation schemes out of protocol.
>
>
> Giving individual operators the responsibility to form there own committees naturally makes the network more performant. For example, the current protocol may assign two validators on opposing ends of the world to the same subnet. This problem is resolved when operators can manually join a DVT pool with peers they know they can perform well with.

Yeah this is a fair point: that we basically still get a two-layer network topology, it’s just that the second layer is out-of-protocol. Some nuances there are:

- The second layer doesn’t need to be a “regular” p2p network: if the pool is small you can just have everyone directly connect to everyone, and use one of the participants as a (untrusted) routing intermediary
- As I wrote above, the staking structure today is not sufficient to truly enable everyone to solo stake, and so we see attraction to DVT on top of today’s structure. Hence, the status quo is moving toward a three-tiered p2p structure, which is even more complex/fragmented than two-tiered.

---

**Guest20444** (2023-12-28):

Regarding Approach 1: Small solostakers are the life blood of Ethereum. Those are the people that make Ethereum what it is. Removing this option and basically becoming like all the other POS chains is a mistake. Honestly this would fragment the community it would lead to a contentious fork. Allow people to run validators with more than 32 Eth it will consolidate a lot of big fish. And see how the situation looks after that. We wont be down to 4096 that shouldnt even be the goal. Ethereum should be proud of every single entity that validates. With this approach the entire consensus will become way more centralized.

---

**vbuterin** (2023-12-28):

> What are the specific technical challenges of processing 1,790,000 signatures per slot after the SSF upgrade? and How would reducing the number of validators from 8192 to a lower number impact the security of the Ethereum network?

There are two challenges:

- Cost of verifying the signatures, at block verification time and during aggregation time. This is dominated by BLS additions: to verify N signatures, you need N BLS additions plus one pairing (technically, you can do fancy pippenger-esque stuff and get a log(N) optimization factor, and on the other side you need O(log(N)) rounds of aggregation: 2 now, likely 3 with SSF with that many validators, and 1 with my cap-to-8192 proposal, but these two nuances conveniently cancel out  )
- The data needed to pass around bitfields. The information-theoretic minimum is 1 bit per signature, but unfortunately the aggregation mechanisms require an increase to ~2 bytes per signature (unless we make the tradeoff of accepting much heavier computation costs). In addition to this there is extra overhead at attestation time.

If you reduce to 8192 signatures per slot, all these problems become no longer very challenging; the beacon chain passed 8192 signatures per slot way back in Nov 2021 (see: [this statistic](https://beaconcha.in/charts/validators), divided by 32) so we know what such a load was like and it was very manageable.

---

**mattstam** (2023-12-28):

I think Approach 1 is the clear choice, but reframing it as opt-in validator subnets with:

- network isolation
- optimal peer groups
- persistence across epochs

may help it come across better to folks like [Guest20444](https://ethresear.ch/u/Guest20444) who are concerned about centralization. Because in reality, *the aggregation always has to occur somewhere* and Approach 1 allows the operator to have more control over that process.

---

**Zergity** (2023-12-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> vbuterin:
>
>
> Even a cost of attack of 1-2 million ETH should be totally sufficient.

While 1-2M ETH *may* be enough to deter them from attacking, we have evidence that they will spend far more than this to achieve their goals, and many governments do appear to be heading in the direction of “destroy crypto” as one of their goals.

I don’t think a 51% attack can “destroy crypto”, the most they can do is re-org a couple of blocks to win an auction.

---

**MicahZoltu** (2023-12-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/zergity/48/5716_2.png) Zergity:

> I don’t think a 51% attack can “destroy crypto”, the most they can do is re-org a couple of blocks to win an auction.

A 51% attack could reorg finality.  Reorging a couple of blocks can happen on accident, or can be done with something like 20-30% and it is “free” (you don’t get penalized for it).

---

**kladkogex** (2023-12-28):

I feel that 1. is a good choice because it addresses the problem of wasteful computation in the network.

As far a small stakers are concerned, they can simply participate in one of decentralized staking pools.

The question is how can this limit of exactly (or approximately?) 8192 validators be enforced? Is it going to be some type of economic incentive/dissentive ?

---

**aivarasko** (2023-12-28):

Also, if removing solo stakers from the network, why to target consumer hardware. And in the end it becomes like all other chains.

---

**tbrannt** (2023-12-28):

> I’d like to emphasize that A LOT of Ethereum’s current censorship resistance today is coming from the 7% who do not participate in PBS, mostly solo-stakers
>
>
> we should be mindful of their value of individual proposers when considering going all-out staking pools.

I want to emphasize how important I think this point is!

Imagine a situation where 90% of ETH is staked with 2 large staking pools and 10% of staked eth is distributed among tens of thousands of home stakers. Who would you think is more likely to include e.g. a tornado cash transaction?

We need to be careful to not miss important angles to look at this problem. How much a 51% attack costs is one. But another very important angle is how likely is it that **every** fee paying transaction will *eventually* be included? A long tail of small validators greatly hardens the property that Ethereum currently still has of *eventually* including every valid fee paying tx.

The problem I have with approach 1 in this regard is that relying on DVT so heavily greatly reduces the ability for single individuals to participate even anonymously and in secret without anyone knowing. Don’t underestimate the importance of these. Some of these stakers might participate in a way voluntarily sacrifying some returns by **not** extracting MEV and e.g. using VPNs that - because of how unreliable many of them are - cause lower rates of attestations. These stakers wouldn’t be able to offer competitive returns in a DVT scenrario. We should increase **and** decrease the min/max effeictive balance to e.g. 8 or 16 and 4096 eth to allow even more of them.

---

**Milli3E** (2023-12-28):

I’m seeing a lot of support for Approaches 1 and 2, but both of those options are pretty significant pivots in Ethereum philosophy. Approach 3 seems to preserve all of the values that we like around low barriers for solo stakers, while economically taking advantage of large staker participation.

There is also a sort of elegance to decoupling staking weight for incentives from staking weight for consensus. This approach will mean the chain is incentivized to grow to as many nodes as possible without creating consensus bottlenecks, but still allows for the simplifications that prompted this discussion.

I think for the most part Ethereum has made the right trade offs to get to where it is now and its philosophy regarding staking decentralization is well placed. Straying too far from that may result in unpalatable changes to consensus which the community might not be vocal about yet feel strongly towards.


*(22 more replies not shown)*
