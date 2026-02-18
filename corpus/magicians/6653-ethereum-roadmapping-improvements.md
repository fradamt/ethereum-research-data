---
source: magicians
topic_id: 6653
title: Ethereum Roadmapping Improvements
author: timbeiko
date: "2021-07-14"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/ethereum-roadmapping-improvements/6653
views: 34613
likes: 36
posts_count: 23
---

# Ethereum Roadmapping Improvements

*Apologies in advance for the long post!*

## TL;DR

- I propose we have fixed deadlines for when we stop considering EIPs for specific upgrades.
- I think we should try and agree on the “large items” for each of the coming network upgrades, even if subject to change, so that we can have better visibility over the general roadmap.
- I share some thoughts about the “best practices” we’ve seen groups pushing larger initiatives for Ethereum take.

---

On [ACD117](https://youtu.be/OLCumSVoc0o?t=3834), we had a discussion about how to improve network upgrade planning and longer-term roadmapping for Ethereum. A few core issues were highlighted:

- A lot of things need to be done on Ethereum in the next 18-36 months;
- Our current process tends to bias towards smaller changes, but a lot of the most important work we need to do is larger (e.g. The Merge, State Expiry, etc.);
- For client teams, working on network upgrades means putting maintenance of the client aside for a while;
- For EIP champions, not knowing when upgrades will happen causes a lot of uncertainty and pressure to get an EIP included in the next upgrade.

There were also a few things that most people seemed in agreement about:

- Client teams can likely handle 2 upgrades per year, but not more;
- There is value in having things scheduled farther out in the future and when things try to get added in the current upgrade, it causes a lot of stress and delays;
- In many cases, testing is the biggest bottleneck, rather than client implementations.

Finally, there was some conversation about how upgrade coordination would work post-Merge. For simplicity, this is out of scope for this document.

## Process Proposal

If we target ~2 upgrades per year, it means each will happen at a roughly 6 month interval. It is also worth noting that towards the end of an upgrade (e.g. after the testnet releases are set), there is typically some bandwidth to start considering things for the next upgrade. Let’s use **T** for the time at which an upgrade gets activated on mainnet.

### T-6 months: “Considered For Inclusion” Closed

Roughly six months before an upgrade is scheduled to go onto mainnet, nothing can be [“Considered for Inclusion”](https://github.com/ethereum/eth1.0-specs/tree/master/network-upgrades#definitions) for it anymore. Any “new idea” since then automatically gets CFI’d for at least the next upgrade.

### T-5 months: Client Integration Testnets start

Roughly five months before the upgrade goes live on mainnet, devnets should be started with all CFI’d EIPs for this upgrade.

At this point, EIP champions should be actively contributing to test coverage for their EIP. **Insufficient testing can be used as a blocker for an EIP to go from Client Integration Testnets to being formally included in the network upgrade.**

### T-3 months: Testnet Activation Blocks Chosen + Client Released

Roughly three months before the upgrade goes live on mainnet, a final list of EIPs for the upgrade has been agreed upon and implemented in all clients, along with a testnet activation block, with the goal of choosing a mainnet block after successful testnet upgrades.

### T-2 months: Testnet Activation

The upgrade goes live across the major public testnets.

### T-1 months: Mainnet Activation Block Chosen + Client Released

Roughly one month before the upgrade goes live on mainnet, a block is chosen and clients are released with activation scheduled for this block.

## Tentative Upgrade Schedule

One comment raised on ACD117 was that we should “open” upgrades earlier in order to provide better visibility to EIP champions. Here is an initial proposal:

### November/December 2021: Shanghai

- Needed because of difficulty bomb pushback in EIP-3554
- “CFI open”: ???
- T-6 “CFI closed” mark: June 1

Special case because this process is new. Worth talking with client teams about EIPs already proposed to gauge interest and impact on Merge work.

### 2021Q4/2022Q1: The Merge

- List of changes available here. Unlikely to include anything else given the large scope.

### 2022Q2/Q3: Cancun

- “CFI open”: now - T-6.
- T-6 “CFI closed” mark: shortly after mainnet-compatible Merge releases by clients are out.
- Large initiatives to consider: Beacon Chain ETH Withdrawals, State Expirty “Stepping Stones” (Verkle Tries, Address Space Extension)
- EIPs to consider: EIPs excluded from Shanghai

Note: first post-Merge upgrade, will need to be coordinated with the Consensus layer because of withdrawals.

### 2022Q4/Q1: Prague

- CFI open: shortly after mainnet-compatible Merge releases by clients are out.
- T-6 “CFI closed” mark: when Cancun mainnet-compatible client releases are out.
- Large initatives to consider: State Expiry

## Getting “Large Initatives” to Mainnet

Changes which affect multiple components of the Ethereum network tend to require a larger, more structured effort to make progress, gain community acceptance, and eventually get deployed to mainnet. These can be thought of as working groups.

Typically, these working groups end up doing/producing the following, usually over 6-18 months:

- A specification of the change (EIP, or a set of EIPs);
- Prototypes of the change across >1 client implementation;
- Hosting calls between implementers and/or the community to discuss the change and progress made;
- Reaching out to relevant parts of the community to gather feedback, address objections, document support for the proposal;
- “Audit” the change, either with a formal audit or at least a thorough analysis of the impacts of the change on clients, users, infrastructure, etc.;

There currently is no official “playbook” for how to sucessfully project-manage these initiatives, but two that can be used as reference are the recent [Fee Market Changes](https://github.com/ethereum/pm/tree/master/Fee-Market) and the work around [The Merge](https://github.com/ethereum/pm/tree/master/Merge).

There is likely little value in overly formalizing how working groups should operate, but having examples (and potentially retrospectives on their success/failure) can be useful for future contributors.

## Replies

**timbeiko** (2021-07-14):

Note: one thing I haven’t made explicit in the above post is how we agree around which “large initiatives” go in each fork. I think, weirdly enough, this can happen somewhat naturally if we simply try and make sure most forks *have* one such initiative.

Because they tend to involve a lot of R&D, their readiness is hard to predict far in advance, but we can know, of the current initiatives, which one is the closest to ready, and plan the upgrade around that (i.e. we accept delaying the upgrade if that change isn’t done, but don’t hold deploying that change if other EIPs aren’t ready).

---

**MicahZoltu** (2021-07-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> ### T-1 months: Mainnet Activation Block Chosen + Client Released
>
>
>
> Roughly one month before the upgrade goes live on mainnet, a block is chosen and clients are released with activation scheduled for this block.

I think we should set the block at the same time as the testnet blocks and then drop changes that would cause us to slip that date rather than slipping the date.  I think at this stage of Ethereum’s lifecycle, it is better to have clear scheduling than it is to get features included ASAP.  This means that if EIP-12345 is in the list but bugs show up during testnets that would cause us to miss the mainnet fork then we should drop EIP-12345 and move it to the next fork (6 months later) rather than pushing the fork back.

---

**axic** (2021-07-15):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> This means that if EIP-12345 is in the list but bugs show up during testnets that would cause us to miss the mainnet fork then we should drop EIP-12356 and move it to the next fork (6 months later) rather than pushing the fork back.

Poor 12356 is penalised for 12345 ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

---

**timbeiko** (2021-07-15):

I somewhat agree… !

One reason to not pick the mainnet block at the same time as testnets is to not set expectations in the community too early. IMO what we did for London, to wait and make sure the testnet deployment went smoothly, was the right approach.

The reason for this is that the things which have the highest likelihood of breaking are the “large initiatives”, and they are also the ones we would be most likely to delay the fork for. For example, if we had found an issue with EIP-1559 on the testnets, it probably would have been worth delaying London by 1 month to fix it.

OTOH, if we find an issue in a “small EIP”, then maybe it’s not worth delaying the fork. It’s also worth pointing out that in some cases, removing an EIP can be more work than fixing a bug, because we need to test for non-inclusion, to not end up with consensus issues like we saw on OE in Berlin.

---

**MicahZoltu** (2021-07-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> For example, if we had found an issue with EIP-1559 on the testnets, it probably would have been worth delaying London by 1 month to fix it.

I think this is where we disagree.  If we had very regular hardforks, I would rather delay EIP-1559 for 6 months to the next hardfork and keep on the reliable schedule than slip the schedule by a month to get EIP-1559 included 5 months earlier.  For a smaller venture (e.g., brand new blockchain, startup company, etc.) I would argue the opposite, but for something the size and scope of Ethereum with the number of involved stakeholders I think that reliable schedule is more important than timeliness of specific features.

---

**timbeiko** (2021-07-15):

Fair enough! I think delaying makes sense for the larger initiatives, and it’s kind of what we’ve done historically. Also, I don’t think we’ll get “perfect” 6 month schedules, so I’m fine with a rough “2 forks per year” commitment, but if I’m the minority here, I’m happy to try a very strict schedule.

Also, FWIW, this can be thought of as a gradual process to make things more predictable: our current process → “loose 2 forks per year, with some margin of error for big things” → “strict forks every 6 months”.

---

**fvictorio** (2021-07-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> ### T-2 months: Testnet Activation
>
>
>
> The upgrade goes live across the major public testnets.

This doesn’t seem like a good idea. This would mean that for *two months* there is no testnet that can be used as a sort of “staging environment” for a mainnet deployment.

There’s probably a deeper underlying problem here: that right now, there doesn’t seem to be a clear difference of purpose for each testnet. (Maybe there is! But if it is, it seems to me that it’s not clearly communicated)

Maybe this schedule could be a first step towards better differentiating each testnet. For example, one of them could have the fork scheduled for (T - 1 week). This would be the most stable of the testnets. This would also mean that there’d be two weeks per year where a reliable testnet doesn’t exist, but that seems like a decent compromise.

(This is just a first idea. This surely needs more thought.)

---

**timbeiko** (2021-07-22):

[@fvictorio](/u/fvictorio) to be sure I understand your point: you are saying it is bad that testnets for “so early” before a fork because then they are not the same as mainnet and it makes it hard to test an application in “mainnet conditions” on a testnet?

If so, I think this is a hard dillema. There are three things we are usually working for when forking testnets:

1. “Testing all code paths”, i.e. making sure the changes are entirely tested. For this, we typically use Ropsten because it is PoW, like mainnet.
2. Cross-client consensus issues, i.e. making sure all clients agree to each other. Here, again, Ropsten or Goerli can work (but not Rinkeby/Kovan, given that only Geth/OE are validators).
3. Replicating mainnet activity. This is probably the most important part, but also the one we want to do last because we may be able to catch issues with (1) + (2) before. Historically, we’ve used Goerli for this.

So, on one hand, the more time we have on testnets, especially those with lots of applications deployed, the higher the chance we catch bugs (i.e. like the [Ropsten one](https://notes.ethereum.org/@timbeiko/ropsten-postmortem) from yesterday, which came a few weeks after the fork). OTOH, this means the testnets aren’t “staging environments” for application developers.

Another thing that’s worth noting is that we need ~1 month to properly choose a mainnet block, get it implemented in client, and sharing those client versions with the community, and there is a desire from core devs to pick a mainnet block after seeing testnets fork successfully.

I’m not sure what the “least worst” option is here, open to ideas!

---

**fvictorio** (2021-07-23):

Based on that, I’d say that a good start would be to consider Ropsten and Goerli the “less stable” (in the sense that they’ll fork earlier) and Rinkeby/Kovan the “most stable” (whose forks are closer to the mainnet fork). Since Rinkeby/Kovan aren’t that good as a testing ground for the protocol-level stuff, they would be better used as an app-level staging ground.

I understand though that there’s an inherent conflict here: the core devs would get better data if more contracts are deployed and used, but app devs will prefer more stability. I still think is worth it to fork them at different blocks based on that “intended usage”.

As a data point for this: when the testnets were forked, some features of Hardhat stopped working until we released the version with support for London. In the meantime, users moved to other testnets instead (I don’t remember right now which one was the last one to be forked). If all of them would’ve been forked at the same time, or at a very close point in time but two months before mainnet, where it’s probable that tooling isn’t ready yet, there would’ve not been a workaround.

If this makes sense, the next step would be to clearly communicate it. At the very least, the [testnets section of ethereum.org](https://ethereum.org/en/developers/docs/networks/#testnets) and this [very upvoted SE question](https://ethereum.stackexchange.com/questions/27048/comparison-of-the-different-testnets) should be updated. (That’s probably out of the scope of this discussion, I’m mentioning it here just for completeness)

---

**timbeiko** (2021-07-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fvictorio/48/3828_2.png) fvictorio:

> Based on that, I’d say that a good start would be to consider Ropsten and Goerli the “less stable” (in the sense that they’ll fork earlier) and Rinkeby/Kovan the “most stable” (whose forks are closer to the mainnet fork). Since Rinkeby/Kovan aren’t that good as a testing ground for the protocol-level stuff, they would be better used as an app-level staging ground.

Yeah, I think that’s fair. For Berlin + London, Kovan has actually forked *after* mainnet. It is being deprecated, but it may be worth considering doing so for Rinkeby. I can definitely bring this up on AllCoreDevs (although with the merge coming, it may not be directly applicable…! Still TBD.).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fvictorio/48/3828_2.png) fvictorio:

> If this makes sense, the next step would be to clearly communicate it. At the very least, the testnets section of ethereum.org and this very upvoted SE question should be updated. (That’s probably out of the scope of this discussion, I’m mentioning it here just for completeness)

Agreed, once we reach some sort of consensus we should update them. Thanks for highlighting!

---

**timbeiko** (2021-07-23):

## On Naming Upgrades

On ACD118, the [topic of the next upgrades came up](https://github.com/ethereum/pm/issues/356), along with their naming. There are a few different things to decide on this front:

### City Name vs. Two-Words for Ice Age

The first point was whether we should stick to our city name terminology or use a two-word name for the December upgrade, which will have to update the Ice Age (assuming The Merge is not ready), and *may* contain additional EIPs. [@axic](/u/axic) shared some thoughts [on Github](https://github.com/ethereum/pm/issues/356#issuecomment-885649852) about this:

> On the topic of naming: there was a time we used two-word names, and then somehow we ended up on the city-name track (starting with Byzantium). In this city-name era, the only two-word update is Muir Glacier, which is both a non-feature update and somewhat a “unplanned update”.

> I am slightly leaning towards keeping the city names for every feature update (including the merge), as long as there is a single feature apart from the difficulty bomb. And keeping everything else with a different name.

> In case there will be only a difficulty bomb change, I suggest we look for another retreating glacier perhaps in so far unrepresented regions, such as Africa or Oceania: Arrow Glacier or Tasman Glacier sounds like an interesting one.

The counter argument is that following the [devcon names](https://ethereum-magicians.org/t/more-frequent-smaller-hardforks-vs-less-frequent-larger-ones/2929/33) provides more predictability for people looking at the “Ethereum roadmap” (e.g. we know Shanghai is in December, and it is followed by Cancun, etc.).

If you have a preference, please share it here.

- City names (Shanghai = December, Cancun = X, etc.)
- Two word name for Ice Age  ( Arrow Glacier = Difficulty Bomb, Shanghai = EIP X, Y, Z)

0
voters

### “The Merge” as a special name

Should we use a city name for “The Merge”, or should we use a city name (e.g. Cancun)?

- The Merge
- City Name (Cancun, Prague, etc.)

0
voters

### Time-based vs. Content-based Updates

Another question that was discussed on the call is whether we should try and adhere to strict schedules in our network upgrades (as argued by [@MicahZoltu](/u/micahzoltu) [here](https://ethereum-magicians.org/t/ethereum-roadmapping-improvements/6653/6)), or whether we should aim to define what the “big initiative” in a upgrade is, roughly schedule it, but be flexible to ensure that this large feature is delivered (as argued by me [here](https://ethereum-magicians.org/t/ethereum-roadmapping-improvements/6653/5)).

- Strict Time-Based Upgrades
- “Large Initiative”-Based Upgrades

0
voters

---

**schone** (2021-07-23):

I generally like the thinking, but I don’t know that it’s going to be net positive for where Ethereum is right now.

These kind of rigid structures is what makes big entrenched companies unable to change, and what ultimately leads to their demise albeit slowly.  The key word here is entrenched.

I think Ethereum’s agility is a feature for now, not a hinderance.  Hence I too kinda lean towards the semi flexible “attempting to do two hard forks per year”.

Is this always ideal for all stakeholders? no.  But agility being the magic power that it is comes with a cost, and I don’t think we are at a stage yet where we’ve become the entrenched mammoth nobody can touch.  We need some flexibility for the time being while the product is not feature complete.

---

**hwwang** (2021-07-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> ## On Naming Upgrades

I’d like to propose another option for the post-merge releases. ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=12)

In Eth2 R&D, we’ve chosen [star names theme as the release naming convention](https://github.com/ethereum/eth2.0-pm/issues/202#issuecomment-775789449).

Quoting the proposer Edson Ayllon:

> Ethereum 1 upgrades are named after cities. I’d like to continue the theme of physical locations, but do so with a different kind of physical locations. I’m thinking star names. Then, we can move onto galaxies for Eth3.

IMHO it was a wise and poetic proposal. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

I suppose that after the merge, we may have protocol upgrades that:

1. Only change the execution layer.
2. Only change the consensus layer.
3. Change both execution and consensus layer software.

We can start to think about how to merge the two organisms for these cases in community communication.

> The Merge

IMHO since this release is likely to only include the merge-related features, “The Merge” seems okay to be a special case as it has been recognized broadly. *Or*, we can consider naming it to a star name starting with the alphabet “B”.

---

**timbeiko** (2021-07-24):

Thanks for sharing!

Happy to stick to star names for post-merge updates. I suspect it will be more likely that both sides (consensus + execution) get updated at the same time (for simplicity, amount of changes we can do in a year, etc.) so the star names can just represent these updates.

If people are happy with this, then we can probably have either Shanghai/Arrow Glacier, then The Merge, and then “B-Star”, which would be the first post-merge upgrade (e.g. with cleanups/enabling withdrawals/activating some EIPs if Shanghai doesn’t happen, etc.).

---

**matt** (2021-07-24):

My 2 wei:

I would prefer we stick to devcon names *only* until the “The Merge” hard fork at which point we switch to star names *only*. If a fork has no features and is executed just to delay the bomb, I’m fine to go with a 2-word name since we did set the precedence with Muir Glacier.

I feel rather strongly that the official name of “The Merge” should not be “*The Merge*”. I don’t care how people refer to it, but I think the *official* name should be a “B-star” star name and we follow that new convention for all future forks.

It wasn’t called “*Launch Fork*” when Ethereum initially launched!

---

**Michaelcodeleone** (2021-07-26):

My 3 wei:

Alternatively, if we stick with a city, I propose Budapest which started as the twin cities Buda and Pest merged together.

---

**poojaranjan** (2021-07-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hwwang/48/4167_2.png) hwwang:

> I suppose that after the merge, we may have protocol upgrades that:
>
>
> Only change the execution layer.
> Only change the consensus layer.
> Change both execution and consensus layer software.

I would vote for

- Merge - “The Merge”

- Difficulty bomb only - 2 word name (eg. Arctic Glacier)

Other proposals for different upgrades are

1. Only change the execution layer - next Devcon city name (Shanghai)
2. Only change the consensus layer - next Star name (eg Baham)
3. Change both execution and consensus layer software - (Baham Shanghai or Shanghai Baham).

I think following an agreed-upon convention will help the rest of the community to follow what to expect with the upcoming upgrade.

---

**schone** (2021-07-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> Only change the execution layer - next Devcon city name (Shanghai)
> Only change the consensus layer - next Star name (eg Baham)
> Change both execution and consensus layer software - (Baham Shanghai or Shanghai Baham).

I like the combination a lot (option 3).  I think devcon city names will run out especially if Coronavirus continues to be a thing.  But what I do like in the overall theme here, is a notion of execution layer having names that are down here on earth and consensus layer being a higher up abstraction having names up high in space.  I think it’s important that one can almost deduct immediately by the name of the hard fork which layer it is intended for. A self branding mechanism.

---

**poojaranjan** (2021-07-28):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/258eb7/48.png) schone:

> I think devcon city names will run out especially if Coronavirus continues to be a thing.

Can’t deny the possibility but we have got at least 4 names (at least next four execution layer upgrades are covered, approx. next 2 years) - Shanghai, Cancun, Prague, Osaka.

We never know after that we move to Eth3 with Galaxies name ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/258eb7/48.png) schone:

> I think it’s important that one can almost deduct immediately by the name of the hard fork which layer it is intended for. A self branding mechanism.

100%

---

**Chris2** (2021-07-29):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/90db22/48.png) Michaelcodeleone:

> Alternatively, if we stick with a city, I propose Budapest which started as the twin cities Buda and Pest merged together.

I’m suggesting Toronto, partly out of Canadian pride. It makes sense as the city where the ETH whitepaper was written. I think its a shame that ETH’s Canadian roots aren’t mentioned. It makes sense that the city at the start marks the largest milestone.

In the alternative I’d suggest Ottawa. It was the city chosen as the capital when the two colonies merged into the Province of Canada and is located in the same province as where ETH was proposed.

PS: Also everyone likes Canada so Canadian cities cause the least controversy.


*(2 more replies not shown)*
