---
source: magicians
topic_id: 7726
title: Has there ever been considerations for a dynamic effective validator balance for staking?
author: domothy
date: "2021-12-08"
category: Uncategorized
tags: [questions]
url: https://ethereum-magicians.org/t/has-there-ever-been-considerations-for-a-dynamic-effective-validator-balance-for-staking/7726
views: 846
likes: 0
posts_count: 1
---

# Has there ever been considerations for a dynamic effective validator balance for staking?

My understanding currently can be summarized in these bullet points (feel free to correct/nitpick anything I get wrong)

- A validator has a total balance that increases with staking rewards, and an effective balance which is always 32 ETH.
- Any excess balance above 32 ETH does not get any extra staking rewards, the staking APR is always calculated on 32 ETH.
- Any total balance below 32 ETH is an inactive validator, meaning they have to deposit more to get to at least 32 ETH to receive staking rewards.
- The reason for 32 ETH was picked was a compromise between the following:

 It’s enough capital to disincentivize people/attackers from getting slashed. Bigger stake = bigger incentive to play by the rules
- Accessible to enough people to promote decentralization of staking
- Not accessible enough that too many people stake and bloat the beacon chain overhead
- It’s equal for all validators so no need to do complex randomness weighted by balance, every validator has an equal chance of being selected for proposals/attestations/committees
- It’s a clean power of two because of dev preferences (or is there a more technical reason?)

Which is all good on the surface, but something about a static effective balance of 32 ETH kind of feels wrong to me. I see Ethereum-the-network as some kind of a self-stabilizing organism with many feedback loops that self-correct when external variables change. These variables are out of Ethereum’s control, but the network reacts automatically to adjust for them and ideally everything should keep working as-is under the most extreme shifts in those variables.

External variables such as demand for blockspace, where EIP-1559 automatically and predictibly adjusts the base fee to compensate. If demand for blockspace suddenly falls or rises 99% in minutes, the whole network would automatically self-adjust to keep everything running smoothly. Ethereum has no control on external demand for its blockspace, all it can do is adjust the pricing accordingly.

Another example is the staking reward APR that goes up and down predictibly depending on how many people are staking. If the external market as a whole decides that the risk/reward of staking Ether is worth 5% APR, then capital will flow into Ether staking when it’s higher than 5% and flow out when it’s lower. Like with blockspace demand, Ethereum has no control over what APR is deemed appropriate by the external market, but it can react appropriately to swings via the underlying incentive structure.

Combining issance and fee burning also reaches an eventual equilibrium where the total supply of Ether will stabilize at a specific value (or a range within say ±2% of that value) and this value self-adjusts to account for changes in those external variables, but whether this equilibrium point is at a total supply of extreme values like 500M or 1M, it should have no effect on Ethereum operating normally as a network

Which gets me to the 32 ETH balance. I believe this effective balance should also be a dynamically self-adjusted figure that can vary up and down predictibly/mathematically according to objective metrics to which Ethereum has access:

It could target a specific number of active validators (2^20 or 2^21?) where anything below the target lowers the minimum effective balance to make staking more accessible (and allow current validators to release the excess balance back into circulation or compound into more validators), and anything above increases it to reduce beacon chain overhead by having validators with a low balance be inactive, making them either deposit more or withdraw.

Forcibly ejecting validators could still happen, just at min_effective_balance / 2 instead of a static 16 ETH.

Under the 5 points listed above, I would only get rid of point 5 and keep 1 through 4 operational even under extreme scenarios where 1 ETH is suddenly worth $1 (current static 32 ETH model would fail point 1 and 3) or 1 ETH is eventually worth $1M (current model fails point 2). Since the effective minimum balance would be the same for all validators, point 4 would remain as well

Similarly, the burn-issuance equilibrium could be free to become arbitrarily low or high and the entire network could keep running normally even in an absolute extreme scenario where all but 1M ETH have been burned – we’d still have 10^24 units to work with. With the current model, if we want a desired 2^20 active validators of 32 ETH each, then total supply cannot go below 33.5M. With 2^21 validators: 67M. The current model also fails to account for the burn-issuance equilibrium going the other way, a supply too high may invite more stakers than we want, at which point a solution would be needed anyway (e.g. rotating active validators randomly)

The main thing that could kill this early-proto-proposal-probing in its track would be that the added complexity of such a mechanism is simply not worth it for reasons I have failed to consider. Reasons that may be obvious or have been considered extensively in the past (wasn’t able to find a thread on it before if it exists, sorry). Point is, feel free to roast me!

But I believe if Ethereum as a network wants a target number of active validators and preserve points 1-4, some complexity would be required anyway. It also seems elegant to throw in more self-adjusting feedback loops in the mix rather than potentially have to manually increase or lower minimum effective balance through hard forks or deal with extreme cases one by one. Would be cool if Ethereum could just self-adjust in those extremes like it can with issuance, burning and total supply.

What do you all think?
