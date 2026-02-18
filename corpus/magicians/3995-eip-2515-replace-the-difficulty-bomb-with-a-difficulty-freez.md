---
source: magicians
topic_id: 3995
title: "EIP 2515: Replace the Difficulty Bomb with a Difficulty Freeze"
author: MadeofTin
date: "2020-02-11"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-2515-replace-the-difficulty-bomb-with-a-difficulty-freeze/3995
views: 5272
likes: 6
posts_count: 6
---

# EIP 2515: Replace the Difficulty Bomb with a Difficulty Freeze

At the time of the Muir Glacier hardfork, I committed to proposing an update to the Ice age that is easier to predict and clarifies the intended function of the Ice age. More is written here https://eips.ethereum.org/EIPS/eip-2387

The following is the first step to fulfill that commitment. The PR is here https://github.com/ethereum/EIPs/pull/2515 and the draft is as follows.

## Simple Summary

The difficulty Freeze is an alternative to the Difficulty Bomb that is implemented within the protocols difficulty adjustment algorithm. The Difficulty Freeze begins at a certain block height, determined in advance, and freezes the difficulty. This does not stop the chain, but it incentivizes devs to upgrade at a regular cadence and requires any chain split to address the difficulty freeze.

## Abstract

The difficulty Freeze is a mechanism that is easy to predict and model, and the pressures of missing it are more readily felt by the core developers and client maintainers. The client maintainers are also positioned as the group that is most able to respond to an incoming Difficulty Freeze.

## Motivation

The current difficulty bombs’ effect on the Block Time Targeting mechanism is rather complex to model, and it has both appeared when it was not expected (Muir Glacier) and negatively affected miners when they are not the target (in the case of delaying forks due to techincal difficulties). Miners are affected by a reduction in block rewards due to the increase in block time. Users are affected as a function of the usability of the chain is affected by increased block times. Both of these groups are unable on their own to address the difficulty bomb. In the case of the Difficulty Freeze, the consequences of missing it are more directly felt by the client maintainers.

## Specification

Add variable `DIFFICULTY_FREEZE_HEIGHT`

The logic of the Difficulty Freeze is defined as follows:

```auto
if (BLOCK_HEIGHT <= DIFFICULTY_FREEZE_HEIGHT):
   block_diff = parent_diff + parent_diff // 2048 * max(
                1 - (block_timestamp - parent_timestamp) // 10, -99)

else:
 block_diff = parent_diff
```

**Optional Implementation**

Add the variable `DIFFICULTY_FREEZE_DIFFERENCE` and use the `LAST_FORK_HEIGHT` to calculate when the Difficulty Freeze would occur.

For example we can set the `DFD = 1,800,000 blocks` or approximately 9 months. The Difficulty Calculation would then be.

```auto
if (BLOCK_HEIGHT  <= LAST_FORK_HEIGHT + DIFFICUTLY_FREEZE_DIFFERENCE) :
   block_diff = parent_diff + parent_diff // 2048 * max(
                1 - (block_timestamp - parent_timestamp) // 10, -99)

else:
 block_diff = parent_diff
```

This approach would have the added benefit that updating the Difficulty Freeze is easier as it happens automatically at the time of every upgrade. The trade-off is that the logic for checking is more complex and would require further analysis and test cases to ensure no consensus bugs arise.

## Rationale

Block height is very easy to predict and evaluate within the system. This removes the effect of the Difficulty Bomb on block time, simplifying the block time targeting mechanism.

## Backwards Compatibility

No backward incompatibilities

## Security Considerations

The effect of missing the Difficulty Freeze has a different impact than missing the Difficulty Bomb. At the point of a Difficulty freeze, the protocol is no longer able to adapt to changes in hash power on the network. This can lead to one of three scenarios.

- The Hash rate Increases:
Block Times would decrease on the network. At the same time uncles would increase. At some point the blocktime would be short enough that clients would not be able to sync fully.
- The Hash rate decreases:
Block times would increase.
- The Hash rate stays the same:
No change to Block Time

Clients are motivated to have their client sync fully to the network and so are very motivated to keep this situation from occurring. Simultaneously delaying the Difficulty Freeze is most easily implemented by client teams. Therefore the group that is most negatively affected is also the group that can most efficiently address it.

## Economic Considerations

Under the current Difficult, Bomb issuance of ETH is reduced as the Ice Age takes affect. Under the Difficulty Freeze, it is more likely that issuance would increase; however, clients are motivated to prevent this and keep clients syncing effectively. This means it is much less likely to occur.

It is also easy to predict when this change would happen, and stakeholders who are affected (Eth Holders) can keep client developers accountable by observing when the Difficulty Freeze is approaching and yell at them on twitter.

## Replies

**MicahZoltu** (2020-02-11):

Consider using `block_timestamp + block_count` as the trigger, rather than block height.  This will let us predict with a very high degree of accuracy when the fork will occur.

The reason for `block_timestamp + block_count` instead of just `block_timestamp` is just because right at the crossover, there are some perverse incentives to manipulate the timestamp.  By saying "`n` blocks after `time`" we can be pretty confident that timestamp manipulation effects have faded by the time the freeze kicks in.  `block_count` just needs to be a number big enough such that any timestamp manipulation by miners around `block_timestamp` will have faded.

---

**tjayrush** (2020-02-11):

If the difficulty freezes and the hash rate increases, block times go down and transactions complete more quickly. Thus, the incentive for ‘the users’ (which includes the core devs who also users) to fix the problem is upside-down. Regular users will argue that faster blocks times are better (because the system is more responsive). Miners will argue that faster blocks times are better because there’s more issuance. Everyone will be hesitant to fix a problem that proposes to make block times longer.

Also, for ‘the world at large’ (outsiders/maximalist), who tend to ‘demagogue’ every change, you will literally be giving them ammunition on a silver platter. They will represent this as a change to the monetary policy (which it clearly can be interpreted as being).

Furthermore, the claim that it’s hard to model the effect of the current calculation ignores the fact that modeling the *entire* effect of the calc is unnecessary. You only need to predict the bomb’s earliest re-appearance and reset it again prior to that (or soon after). The January 2019 diffusion didn’t set the FAKE_BLOCK back far enough (period 21). If, instead, it had set it back to period zero (or near there, as the previous diffusions did), we would have way more time. Because it was only set back to FAKE_BLOCK around 2,000,000, we only had 20, 100,000 block periods which is why it snuck up on us. Further explained [here](https://medium.com/@tjayrush/a-method-to-diffuse-the-ethereum-difficulty-bomb-c32cb9ac267e) and [here](https://medium.com/@tjayrush/its-not-that-difficult-33a428c3c2c3).

The most important reason, however, for why I’m not in support of this is that it’s an example of an overstep driven only by the convenience of the core devs. The current bomb *explodes*. There is a reason for that. The explosion keeps the whole system from getting complacent or lazy.

There are three constituencies in the community (users, miners, core devs), the current calculation aligns all three each time the bomb explodes. Everyone *needs* the bomb to be diffused. This current suggestion, while it makes life easier for the core devs, incentivizes users and miners to want to keep the difficulty frozen as pointed out above, misaligning incentives.

---

**tjayrush** (2020-02-18):

After a long conversation with [@MadeofTin](/u/madeoftin) this weekend at EthDenver, I’ve had a change of heart about the difficulty bomb. I now believe that it is more difficult to predict than I originally thought (although still not impossible—my argument was to that we should predict earliest possible appearance by making very conservative assumptions about hash rate).

The point of the EIP, I have come to understand, is that we should purposefully make the timing of the bomb perfectly predictable — and this is what the EIP does. So—because of that—I now support the idea of ‘fixing’ the difficulty bomb.

I do not think we should remove it, nor do I think we should make it ‘freeze’ as the current EIP suggests, but James mentioned discussion about alternatives to a frozen bomb which I look forward to seeing.

Thanks so much to James for being patient and explaining to me his concerns.

---

**MadeofTin** (2020-03-06):

yes, the new design is where at the time of triggering the bomb would increase the difficulty linearly.

For comparison this is what the original proposal would look like

[![Updated Difficulty bomb - Flat Version](https://ethereum-magicians.org/uploads/default/original/2X/2/2ce565b5d53a61385aee67207a756308f857ec7d.png)Updated Difficulty bomb - Flat Version600×371 17.2 KB](https://ethereum-magicians.org/uploads/default/2ce565b5d53a61385aee67207a756308f857ec7d)

New version

[![Updated Difficulty bomb - Linear increase V2](https://ethereum-magicians.org/uploads/default/original/2X/7/7febd788c84ee3b6dac61935f2e10e26874e14d1.png)Updated Difficulty bomb - Linear increase V2600×371 16.5 KB](https://ethereum-magicians.org/uploads/default/7febd788c84ee3b6dac61935f2e10e26874e14d1)

Here eventually in all cases the difficulty even though it would no longer adjust based on block time would increase to a point of block times becoming unusable on the network.

Thank you to Q (quentinc137) on twitter who helped me walk through the game theory on this.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/a/a21fbc7d0f406f85cd647214b91813cdcc7df4c3_2_244x250.jpeg)image1999×2048 225 KB](https://ethereum-magicians.org/uploads/default/a21fbc7d0f406f85cd647214b91813cdcc7df4c3)

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/f/fe26d35f6e6dd5bd2bec6fb2be0834651e7fc37b_2_259x250.png)image680×655 28.1 KB](https://ethereum-magicians.org/uploads/default/fe26d35f6e6dd5bd2bec6fb2be0834651e7fc37b)

The last option to explore is if changing the adjustment window is preferable.

e.g Currently the adjustment factor is up if less then 10 seconds, and down if greater than 20. You could increase both of those over a period of blocks, such that the target block time increases after a certain point. I am not sure if this has other complications, but it is worth exploring.

---

**tjayrush** (2020-04-28):

I listened to the discussion about this EIP on the ACD call. I think people are missing part of the point of James’ proposal. James’ proposal changes only the ‘bomb’ part of the calculation. The ACD discussion had a lot to do with what happens if the hash rate increases. Since the proposal only alters the ‘bomb’ part of the calculation, it leaves the ‘non-bomb’ part. The ‘non-bomb’ part works exactly as designed to ‘squelch’ any increase in hash rate. I know you’all think there’s some sort of feedback loop, and you’re right there is, but it has no effect on the effectiveness of the ‘non-bomb’ part.

Thought experiment: remove the ‘bomb’ part of the calculation entirely. Bomb === 0 for every block.  Does the non-bomb part keep block times stable? The answer is clearly yes. So – related to James’ change – increased hash rate is not a problem.

