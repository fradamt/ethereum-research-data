---
source: magicians
topic_id: 807
title: "EIP-1234 vs EIP-1227: Constantinople Difficulty Bomb & Block reward"
author: dontpanic
date: "2018-07-19"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-1234-vs-eip-1227-constantinople-difficulty-bomb-block-reward/807
views: 4453
likes: 14
posts_count: 28
---

# EIP-1234 vs EIP-1227: Constantinople Difficulty Bomb & Block reward

The difficulty bomb currently is being discussed in two opposing proposals. Rather than having to follow two comment threads, this thread should merge the debate.

EIP-649 established a delay in the difficulty bomb and reduced the block reward as part of the Byzantium fork. The bomb was originally included in the metropolis HF with the intent to provide leverage in the transition to PoS as there was not a clear governance process in place to enforce the project roadmap and was to be used to make mining increasingly unprofitable. In the interim 2 years the community has grown considerably and the transition to PoS is now a universally understood matter of ‘when’ not ‘if’.

As it is currently implemented, under EIP-649, the difficulty bomb will soon begin to become a determent to network difficulty and block time again. As such, the Constantinople fork is the logical junction to implement a change in the bomb. Two opposed EIPs have been suggested, EIP-1234 and EIP-1227.

EIP-1234

**Abstract:** Starting with CNSTNTNPL_FORK_BLKNUM the client will calculate the difficulty based on a fake block number suggesting the client that the difficulty bomb is adjusting around 6 million blocks later than previously specified with the Homestead fork. Furthermore, block rewards will be adjusted to a base of 2 ETH, uncle and nephew rewards will be adjusted accordingly.

EIP-1227

**Abstract:** Starting with FORK_BLKNUM the client will calculate the difficulty without the additional exponential component. Furthermore, block rewards will be adjusted to a base of 5 ETH, uncle and nephew rewards will be adjusted accordingly.

REF: https://github.com/ethereum/EIPs/issues/649

REF: https://github.com/ethereum/EIPs/pull/1234

REF: https://github.com/ethereum/EIPs/issues/1227

## Replies

**MicahZoltu** (2018-07-19):

As has been said in both threads (once by me), both should be split into separate EIPs.  Bundling the difficulty bomb and the block reward into the same EIP is likely to confuse the issue more than help it.

---

**SmeargleUsedFly** (2018-07-19):

I completely agree. I’ve added a line “Note: the issuance reduction is not the focus of this proposal, and is optional; the defusing of the difficulty bomb is of primary concern.” to my proposal, since the block reward reset is 1) of lesser importance, by far and 2) as you just said, they should not be bundled together. Indeed, they should never have been bundled in #649, but that’s story for another day.

---

**dontpanic** (2018-07-19):

Yes, I completely agree.  Having the two linked needlessly made the 649 thread muddy and distracting. The bomb is a technical issue, block reward is economic.

---

**SmeargleUsedFly** (2018-07-19):

Thanks [@dontpanic](/u/dontpanic) for starting a discussion thread. I’ve since made a formal PR at https://github.com/ethereum/EIPs/pull/1235/files.

---

**dontpanic** (2018-07-19):

If I remember correctly, block reward was tied to the bomb in 649 because it would have been incredibly unlikely that miners would have agreed to reduce their reward as it isn’t in their best interest. Removing/delaying the bomb is beneficial to miners so it became the carrot that allowed the reduced block reward to be implemented. This seems to be the spirit of 1234. 1227 are both beneficial to miners so they could be implemented separately with out worry that miners wouldn’t act in their best interest on both.

---

**AtLeastSignificant** (2018-07-19):

It’s not *not* worth adding information pertaining to the motives of [@SmeargleUsedFly](/u/smeargleusedfly): https://www.reddit.com/r/ethereum/comments/8zv38m/in_light_of_continuing_changes_to_the_eip_process/

From my discussion with them, I’ve concluded that they want a permanent disable of the difficulty bomb for the sole purpose of not having to “deal with it themselves” when some hypothetical group decide to not support some hypothetical contentious hardfork that is brought about by unilateral core dev decisions.

Getting rid of the difficulty bomb so that deprecated chains can more easily exist seems to be counter to the purpose of the bomb in the first place.

---

**AtLeastSignificant** (2018-07-19):

Regarding the proposal to *delay* the difficulty bomb, I have no objection with that piece.  Miners should have no issue with accepting this as it is in their interest - however, if we would also like to reduce issuance to 1-2 ETH then it would make sense to bundle this with a bomb delay.  As [@dontpanic](/u/dontpanic) says, this is similar to 649 in that it is a give-and-take proposal.

I have never seen any objection to the argument that issuance should be as low as possible while still maintaining blockchain security.  Reducing the block reward from 3 to 2 could cause security concerns if the price of ETH remains the same or falls.  If price of ETH increases to compensate the reduced block reward, we will not have achieved anything in terms of the fiat inflation rate of the chain (but this is clearly in the interest of investors).

I do no think decisions about protocol changes should consider what is in the best interest of investors/money.  Thus, I can only see an issuance reduction as a potential security risk OR financially motivated with no real impact on inflation.  For this reason, I think the block reward should be a separate proposal form the difficulty bomb *delay*, so that I may support the bomb delay and not support the issuance change.

---

**MicahZoltu** (2018-07-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dontpanic/48/98_2.png) dontpanic:

> it would have been incredibly unlikely that miners would have agreed to reduce their reward as it isn’t in their best interest

It doesn’t matter what miners what, it matters what economic participants want.  99% of miners can go and mine on the chain that has a block reward of 50,000,000 ETH per block if they want, if economic participants don’t use that chain then they’ll have 50,000,000 worthless ETH.

My broken record reminder: Miners are a service provider.  They do not have any power of the direction of the blockchain.  They are easily replaced and if some leave to mine another chain, others will pop up to fill the void.

---

**AtLeastSignificant** (2018-07-19):

Probably not the place to hash out this governance/power argument, but I do think your argument is a valid *perspective* of things.  You can certainly frame things in which miners are the ultimate power though, in that economic participants literally cannot participate unless miners allow the blockchain to exist.  This is probably not realistic nowadays since mining is too profitable an activity to expect altruistic or irrational financial decisions form them.

To expand on your point though, if economic participants are the primary driver for what exists and is worth anything, why do they have no impact on the actual development decisions?  Nick Johnson just said the other day quote:

> Ultimately the only way the community can accept or reject a change is by running, or refusing to run, the code. There’s no way to reliably measure the popularity of a proposed change (to the degree where you can be sure it’s not worth implementing), and trying to do so would simply bog the EIP process down with a political process - most likely resulting in people switching to a new way to agree on changes that doesn’t impose massive overhead.

https://old.reddit.com/r/ethereum/comments/8zk7l0/changes_are_being_made_to_the_eip_process_which/e2jl29o/

Where is the disconnect here?  Is it economic participants, miners, or core devs who call the shots?  Again, not the time or place to hash this out, but this is my broken record reminder that miners absolutely do have a say in what they mine, especially when the economic participants have decided that there are other profitable (and not that far off) blockchains to go mine with the same hardware.

---

**5chdn** (2018-07-19):

That’s wrong Micah. Reducing block times increases issuance. Reducing block rewards reduces issuance. If you split this, you end up modifying issuance. The goal of bundling it in one EIP aims at maintaining a stable issuance.

---

**dontpanic** (2018-07-19):

is there a target for issuance or just ideally matching the present?

---

**tjayrush** (2018-07-20):

This article may or may not be relevant, but the same sort of discussion (should have) occurred pre-Byzantium: https://medium.com/@tjayrush/byzantiums-difficulty-calculation-2cdef46f79d3.

Conflating a change in the block reward and a fix to the difficulty bomb in the same hard fork accomplishes exactly the reason for the difficulty bomb in the first place – it allows the devs to control issuance.

Afri is right, the issuance remains relatively the same over the particular block at the hard fork, but over the previous month the issuance had decreased due to the difficulty bomb. The net effect at the Byzantium fork was a lowering of issuance from five eth every 15 seconds to three eth every 15 seconds. The miners, obviously, didn’t like it, but they went along with it because they needed the fix to the difficulty bomb – thus the need to keep the two combined.

---

**dontpanic** (2018-07-20):

If the idea is to mimic the issuance as if the bomb were still in place, the current target issuance would be zero. If their is no total coin issuance target, there is little difference technical difference in setting 1, 5, 50 or 100 ether per block. Unless something has changed, there isnt an opcode for the evm to even query what the block reward is.

Is there a target?

---

**AtLeastSignificant** (2018-07-20):

To expand on this, you can have a target total supply, target issuance rate, and target issuance in terms of fiat.

Miners operating cost is in fiat currency, so framing the target issuance in terms of fiat make sense to me. I believe this would mean creating an adaptable issuance rate based on oracles.

---

**dontpanic** (2018-07-20):

fiat isnt real and would create a needlessly complex consensus model. in order to use an Oracle, the system would need op codes to get block rewards. since there is never real finality l, reorgs would be insanely complex

edit: fiat isnt real == there is no global standard fiat rate that is fixed. pegging to usd may create inefficiencies compared to gbp, euro, yuan, gold etc on any given day

---

**AtLeastSignificant** (2018-07-20):

It would definitely be a technical nightmare, but let’s say for the sake of discussion that it is doable (to have a flexible block reward that pays miners a fixed amount of fiat).

This would free miners from speculation because they would be able to calculate exactly how profitable mining would be.  This makes difficulty (and security) completely controllable based on the fixed fiat payment amount.

However, this would mean only the most efficient miners would exist - since they are the only ones who stand to make any money in a scenario where the mining “market” is saturated.  This probably leads to centralization around ASICs and ASIC producers.

Doesn’t sound like a good plan, even if it was technically feasible.

---

So, are we talking about a target supply cap or a target issuance rate with no supply cap?

---

**dontpanic** (2018-07-20):

the only supply cap proposal I’m aware of is https://github.com/ethereum/EIPs/issues/960 , but as I understand it this was a joke.

The technical restraint would still be the lack of the system to grep its total supply and could only approximate based on block number

---

**flygoing** (2018-07-20):

The latest [Casper/Sharding](https://notes.ethereum.org/SCIg8AH5SA-O4C1G1LYZHQ) spec has a supply cap in it as well.

---

**dontpanic** (2018-07-21):

> ETH_SUPPLY_CAP - self-explanatory. Currently set to 227 ~= 134 million.

is this gospel or a strong assumption?

---

**MicahZoltu** (2018-07-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5chdn/48/1242_2.png) 5chdn:

> That’s wrong Micah. Reducing block times increases issuance. Reducing block rewards reduces issuance. If you split this, you end up modifying issuance. The goal of bundling it in one EIP aims at maintaining a stable issuance.

If the block reward is intended to be stable by time (not blocks) then the algorithm should be changed to not have difficulty as an independent variable and instead use time as the independent variable.  That could be an EIP just as easily as this one.  By conflating these two issues, you are conflating discussion about them.  As an economic participant, I am an advocate of removing the difficulty bombs entirely and also of reducing the block reward.  Rather than having 4 EIPs with all 4 combinations of such, we can have two EIPs that are isolated from each other and can be evaluated and discussed separately.

We have seen discussions around block reward/difficulty bomb EIPs degrade in the past and this is partly because they keep getting proposed as two-in-ones like this.


*(7 more replies not shown)*
