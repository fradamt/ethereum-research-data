---
source: magicians
topic_id: 3793
title: "EIP-2384: Difficulty Bomb Delay"
author: econoar
date: "2019-11-22"
category: EIPs > EIPs core
tags: [difficulty-bomb, eip-2384]
url: https://ethereum-magicians.org/t/eip-2384-difficulty-bomb-delay/3793
views: 33305
likes: 7
posts_count: 18
---

# EIP-2384: Difficulty Bomb Delay

Um, we’re about to ice the chain.

So let’s discuss it [EIP-2384 - Difficulty Bomb Delay by econoar · Pull Request #2384 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/2384)

## Replies

**axic** (2019-11-22):

A lengthy discussion started on the [ACD gitter channel here](https://gitter.im/ethereum/AllCoreDevs?at=5dd4ce8050010612b2eeb9d6).

---

**tjayrush** (2019-12-02):

Why not choose a number that sets the `fake_block` number to a known quantity like `50,000` or `100,000`? If we did that, the `period` would get set back to `0` or `1` and the amount of time between bomb diffusions would be maximized. Choosing `9,000,000` setback is arbitrary and depends on `fork block` which adds a bit of uncertainty that seems unnecessary. (It will set the `period` back to `1` most likely, though.)

The arbitrary choice of `5,000,000` for the previous bomb diffusion is, I think, why the bomb is appearing so early this time.

---

**fulldecent** (2019-12-03):

Here is my review of EIP-2384 (DRAFT) now in Last Call.

# 4 mil is too much

The 4,000,000 block delay is 1.7 years. This gives Ethereum core devs too much leeway to stall on Ethereum 2 development without seeking further community input.

Why is a 3,000,00 block delay as was done previously not sufficient?

Are you that scared of us?

# Block reward should go down

There should be a commensurate decrease in the block reward with this change.

Reading the references which are already presented in EIP-2385 (DRAFT) show the thinking that developed in the past when considering this same issue.

See: https://www.youtube.com/watch?v=wLaI7680I4w&t=4888s

You can hear Vitalik argue that reducing the block reward from 5 to 3 is appropriate if the price of Ether is above $10 or so. Well, we’re well above $10 now. Reducing it again is appropriate.

So far this has been a discussion point. But I will argue that the EIP draft is currently defective because the EIP-649 is cited as “The implementation in it’s logic does not differ from [EIP-649](https://eips.ethereum.org/EIPS/eip-649)” but the reward reduction is not even mentioned. This is missing a required point in the Rationale section.

---

**karalabe** (2019-12-06):

> This gives Ethereum core devs too much leeway to stall on Ethereum 2 development without seeking further community input.

I honestly don’t think anyone wants to stall Eth 2 development. Actually, I don’t even see how we could stall it, since Eth 2 is currently it own, completely separate network. A real live Eth 2 will also probably take 2+ years still, so it’s not like we’re being unreasonable here.

> Why is a 3,000,00 block delay as was done previously not sufficient?

Please see [It’s Not That Difficult. All about the Ethereum Difficulty… | by Thomas Jay Rush | Medium](https://medium.com/@tjayrush/its-not-that-difficult-33a428c3c2c3), where it argues why the previous Ice Age delay was wrongly calculated in the first place, causing the current “emergency”.

> Are you that scared of us?

Dafuq does this even mean?!

---

**tjayrush** (2019-12-06):

This EIP (https://eips.ethereum.org/EIPS/eip-2384) says that the difficulty calc will be set back a hard coded distance from the head of 9,000,000 blocks from `FORK_BLOCK`.  This one (https://eips.ethereum.org/EIPS/eip-2387) says it will activate at block `9,200,000`. This means that the `fake_block` will be `200,000`.

There’s an issue with this in that `fake_block` is dependent on when the fork happens (forks have been delayed in the past).

If, instead of being hard coded, the setback was (`FORK_BLOCK - 200,000`), then the delay would have no effect on how far back the bomb gets reset.

This would make the statement in the Muir Glacier EIP that the bomb is difficult to model much less true. In the future, if we always reset the bomb to `FORK_BLOCK - 200,000`, it would predictably start to make itself known NO EARLIER than X months/years later.

(Hash rate has no effect on how the bomb grows–the fist part of the difficulty calc is designed specifically to eliminate fluctuations in hash rate–and the bomb, once it appears dominates being exponential. All you need to predict the earliest time the bomb will appear is knowledge of where it started. A lowering of hash rate can’t make it come earlier, and a rise in hash rate can only make it come later.)

I suggest the bomb be delayed `FORK_NUMBER - 200,000` (or earlier).

---

**jmorris** (2019-12-06):

# 4 mil is too much

+1

2 years delay is way too much.

**Context:**

The difficulty bomb has the purpose to add pressure in order to upgrade to Proof of Stake. This EIP is not aligned with that fundamental that ethereum subscribed for.

**Current situation:**

the difficulty bomb is being delayed for free*. For free* means that ethereum delays its promised improvements without any compensation or commitment.

On the demand/supply analysis we can’t see that there’s not enough demand for Ether to play its scarcity game. A higher demand has to be created and this is done through improvements. If improvements have to be delayed, the difficulty bomb was programmed to tick and start reducing the supply of ether, the bomb works as expected, the development is not as expected, these are the facts.

**Problem:**

However, nothing is for free. A delay of the difficulty bomb without any compensation or commitment to the Ethereum network has its costs. Costs might not be visible at first sight, but sure they exist and ethereum has suffered this impact for the last 1,5 years.

**Proposal:**

To link the difficulty bomb delay to the development of Ethereum (eth 2.0 and/or eth 1.x).

Instead of 2 years bomb delay for free, have bombs delays only after ethereum hits a development milestone.

**Example:**

Today, there’s no need to delay the bomb by installing a client that applies EIP-2384.

Instead, deliver Ethereum 2.0 Phase 0 as expected within 2020 Q1. Or deliver Ethereum 1.x.

Once delivered, then ethereum nodes cast their votes to delay the bomb in the network by installing a client that applies EIP-2384.

Putting off everything breaks the entire game theory of these networks.

---

**econoar** (2019-12-06):

I really don’t know why people keep associating this with eth2 development. Yes the ORIGINAL idea was to not allow stagnation but that’s an ancient thought at this point.

As Peter has already pointed out, eth2 is now mostly entirely independent of eth1. In fact, besides the potential of the finality gadget, eth1 isn’t even aware of eth2 and doesn’t need to fork for it.

We should really stop combining these two ideas. A delay in the difficulty bomb in no way delays eth2 development.

---

**levarato** (2019-12-07):

Why it’s an ancient thought? Eth 1.0 still needs improvements and can be improved. Eth 2.0 is 2+ years away. Etehreum is a software platform not a simple SOV if ethreum 1 go in stagnation of development, when eth 2.0 will be ready there is the risk that Etehreum will be not more relevant. So in my opinion set the difficulty bomb 1 year from now would be a far better choice. Another point is: why not compensate the inflation of the coming eth 2.0 beacon chain reducing the emission of eth in eth1?

---

**TXien** (2019-12-09):

I suggest that we can replace the difficulty bomb with a dynamic reduction of blockchain rewards to achieve the expected ETH2.0 issuance.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/f/f571f90d0bbede71c3ae79fe826b01764664cab7_2_690x396.jpeg)image1376×790 211 KB](https://ethereum-magicians.org/uploads/default/f571f90d0bbede71c3ae79fe826b01764664cab7)

this picture show that the insurance is unpredictable.

we should make inflation predictable and write it in code in advance, instead of repeatedly delaying the difficulty bomb and change rewards.

---

**fulldecent** (2019-12-09):

When the community decides to update its clients this is showing a vote of confidence in the Ethereum Foundation and the mainnet Ethereum network.

Since the Etherum Foundation has promised, and promotes, Eth 2.0 development, this makes Ether (currently $16B USD), mainnet and the community’s trust in Ethereum Foundation all connected.

Part of this promise includes, basically:

> The core devs commit to include you in future decision making. And if we fail to make progress with the community as a whole then we have mutually assured destruction (ice age). This guarantees to the community as a whole that core dev interests are aligned with the community.

By delaying or removing ice age, the voids the core dev promises above.

And basically that means core devs are afraid of the community.

---

**BFire** (2019-12-10):

This 1.7 year delay gives away all leverage to change the fee model in 2020 via EIP 1559 or enabling the beacon chain to finalize ETH 1.x  blocks (which would reduce issuance dramatically).

---

**timbeiko** (2019-12-10):

To be clear, the difficulty bomb delay will *not* be the last upgrade to Eth 1.0 before Eth 2.0 goes live.

If it had been known in advance that it would kick in so soon, it would have been delayed as part of Istanbul.

There is already a list of EIPs that are Eligible for Inclusion for the next upgrade after Muir Glacier (likely called Berlin, which also had a [Meta EIP](https://eips.ethereum.org/EIPS/eip-2070)): https://github.com/ethereum/EIPs/pull/2378

EIP 1559 is supposed to be discussed on this week’s [AllCoreDevs call](https://github.com/ethereum/pm/issues/142). If it’s ready to be implemented by clients, it will and will be scheduled for an upgrade, independent of when the difficulty bomb is meant to kick off.

---

**BFire** (2019-12-10):

But what will provide an incentive for miners to adopt any upgrade that reduces issuance (and/or fees) if the bomb is far off into the future?  1559 might get pushed through but I don’t see any non-altruistic miners wanting to allow the beacon chain to finalize (which will require a hard fork)

---

**timbeiko** (2019-12-11):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/b/e36b37/48.png) BFire:

> But what will provide an incentive for miners to adopt any upgrade that reduces issuance (and/or fees) if the bomb is far off into the future?

That’s a good point. With regards to the Finality Gadget, I doubt we’ll see it live on mainnet in <1 year (given that light clients for Eth2 need to be built and that work hasn’t started as far as I’m aware). This would come fairly close to the ~1.5 years in which the bomb would go off again.

Aside from the bomb, though, miners will have an incentive to upgrade to what is considered the “proper” Ethereum by the community.

If a large majority of Ethereum users & infrastructure providers consider the finality-gadget chain to be the correct one, then miners have an incentive to follow that chain given that it will be “ETH” and have most/all activity/economic value tied to it.

---

**fulldecent** (2019-12-30):

Just here to note that this EIP was accepted as final AFTER the Ethereum Foundation endorsed the Muir Glacier hard fork on its blog.

EF announcement: https://blog.ethereum.org/2019/12/23/ethereum-muir-glacier-upgrade-announcement/

EIP promotion to final:  https://github.com/ethereum/EIPs/commit/0104c3a3d914a2766331ce208d1519b6e6e99f6b

The ordering of these two events indicates that EF does not recognize the community input process when it unilaterally implements major breaking changes.

---

**timbeiko** (2019-12-31):

I’m not sure that’s accurate. As per the AllCoreDevs call [notes](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2077.md#decisions) (decision 77.5), it was agreed to move it to Final pending a small change (`Push it to final once a line "that the block rewards are unchanged" is added in the EIP.`) that made more explicit the fact that this EIP didn’t change the block reward.

The call was on Dec 13th, so 10 days before the EF’s blog post. Agreed that that PR should have been done sooner, though.

---

**fulldecent** (2020-01-14):

The decision-making occurs in the pull request using the process established by EIP.

To say that “it was agreed to move it to Final” on the AllCoreDevs call is incorrect. Such would be an illegitimate action (i.e. usurpation).

The correct statement is “it was agreed to move it to Final” when the PR was merged to move it to Final.

