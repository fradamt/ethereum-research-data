---
source: magicians
topic_id: 833
title: "EIP-1234: Constantinople Difficulty Bomb Delay and Block Reward Adjustment"
author: 5chdn
date: "2018-07-21"
category: EIPs
tags: [block-reward, difficulty-bomb]
url: https://ethereum-magicians.org/t/eip-1234-constantinople-difficulty-bomb-delay-and-block-reward-adjustment/833
views: 6464
likes: 0
posts_count: 5
---

# EIP-1234: Constantinople Difficulty Bomb Delay and Block Reward Adjustment

```auto
eip: 1234
title: Constantinople Difficulty Bomb Delay and Block Reward Adjustment
author: Afri Schoedon (@5chdn)
discussions-to: https://github.com/ethereum/EIPs/pull/1234
type: Standards Track
category: Core
status: Draft
created: 2018-07-19
```

**Abstract**: Starting with `CNSTNTNPL_FORK_BLKNUM` the client will calculate the difficulty based on a fake block number suggesting the client that the difficulty bomb is adjusting around 6 million blocks later than previously specified with the Homestead fork. Furthermore, block rewards will be adjusted to a base of 2 ETH, uncle and nephew rewards will be adjusted accordingly.

Read the draft here: [eip-1234.md](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1234.md)

Previous and related discussions:

- EIP-1240: Difficulty Bomb Removal (EIP-1240)
- EIP-1234 vs EIP-1227: Constantinople Difficulty Bomb & Block reward
- https://twitter.com/5chdn/status/1020631670398038016

## Replies

**MicahZoltu** (2018-07-21):

Moving discussion to here from PR.

Recommend splitting this into two separate EIPs.  One for the Ice Age and one for the block reward.  At the moment, the block reward is per block, rather than per time.  From previous discussions it sounds like there is a desire for block reward to be a function of time instead of a function of block.

I have already created EIP 1240 which proposes removing the difficulty bomb all together.  If there is a desire to keep the difficulty bomb, then I recommend creating an EIP that *just* delays it.

Separately, if there is in fact a desire to make the block reward a function of time (which it sounds like there is) then create an EIP that does that.

The current system of letting an ice age come (which reduces block reward per time) and then rollback/delay the ice age but *don’t* rollback the block reward reduction is *feels* like it is trying to sneak in a block reward reduction.  I don’t necessarily think that is the intent, but I do believe there is value in more clearly defining that the block reward schedule is intended to decrease with time.

Personally, I support a block reward reduction with time and a delay (or better yet removal) of the ice age all together.  My only real complaint with this EIP is that it is bundling two concepts that shouldn’t be bundled.  I recognize that perhaps they were bundled in the past and it is easiest to just “bundle them again” but in the past this class of EIP has resulted in a large amount of discussion and that discussion would be easier to have if the two changes were separated from each other and more clearly isolated.

---

**jmiehau** (2018-08-31):

[@5chdn](/u/5chdn) thanks for doing this commit: [Move EIP-1234 to accepted; change delay to 12 months by 5chdn · Pull Request #1365 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/1365/commits/e9db95978db66d118292c8d8edd62e89c9b56225)

> This will delay the ice age by 29 million seconds (approximately 12 months), so the chain would be back at 30 second block times in winter 2019.

Which calculations do you use to it? (Just want to learn about this process and double check). Maybe a google datasheet or similar with the data would be great!

---

**5chdn** (2018-09-01):

The delay of the bomb is another 2 million blocks (~ 60 seconds * 60 minutes * 24 hours * 365.2424 days / 14.58 seconds per block)

Rounded to millions for simplicity. 2 million blocks times 14.58 seconds are around 29 million seconds ~ 12 months.

---

**jmiehau** (2018-09-02):

Thank you [@5chdn](/u/5chdn) for the clarification.

=======

Edit Sept 8:

@Bigomby has done calculations and confirms that EIP-1234 with 2MM blocks delay the diff bomb and we would be back at 30 second block times in winter 2019.

He is planning to publish an interactive data to show the results and the code.

=======

Charts from Etherscan:

https://etherscan.io/chart/difficulty

https://etherscan.io/chart/blocktime

