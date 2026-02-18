---
source: magicians
topic_id: 908
title: "EIP-1276: Eliminate Difficulty Bomb and Adjust Block Reward on Constantinople Shift"
author: eosclassic
date: "2018-07-31"
category: EIPs
tags: [block-reward]
url: https://ethereum-magicians.org/t/eip-1276-eliminate-difficulty-bomb-and-adjust-block-reward-on-constantinople-shift/908
views: 3597
likes: 3
posts_count: 8
---

# EIP-1276: Eliminate Difficulty Bomb and Adjust Block Reward on Constantinople Shift

[![FOREIGN201501300805000257079516292](https://ethereum-magicians.org/uploads/default/optimized/1X/9bc6fceec9cf40d6d5c1d9d81ff386227d811f6d_2_690x458.jpg)FOREIGN201501300805000257079516292850×565 135 KB](https://ethereum-magicians.org/uploads/default/9bc6fceec9cf40d6d5c1d9d81ff386227d811f6d)

(Eliminating the bomb, that’s what we do!)

Hello Ethereum Community and developers!

I am EOS Classic from alternative EOS mainnet development team, and today I would like to suggest new improvement proposal for Ethereum!

We all know that difficulty bomb is a cancer for ethereum since it meant to work for casper upgrade however it is now ending up with significant transaction delay & mining centralization that comes from high difficulty.

Therefore it will likely end up harming user experience if we don’t change the difficulty adjustment algorithm on this Constantinople hardfork.

And we should change the issuance of ethereum block reward that goes to miners in order to respond for casper upgrade and supply plan. Ethereum is now dominating more than 90% of mining hashrate share on ethash algorithm coins, it should be changed.

For detailed information please refer my EIP here [EIP-1276: Eliminate Difficulty Bomb and Adjust Block Reward on Constantinople Shift](https://eips.ethereum.org/EIPS/eip-1276) and please feel free to discuss about this EIP ![:grinning:](https://ethereum-magicians.org/images/emoji/twitter/grinning.png?v=15)

## Replies

**ligi** (2018-07-31):

I do like this bomb. It is a nice forcing function for updates and can prevent stagnation.

So:

> “Stop worrying and love the bomb”

![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=15)

[![4050083521_b771915fcc_o](https://ethereum-magicians.org/uploads/default/optimized/1X/6a9fc780d67b3bb7a535bed7f1eb7ade0e8382ab_2_690x460.jpg)4050083521_b771915fcc_o720×480 180 KB](https://ethereum-magicians.org/uploads/default/6a9fc780d67b3bb7a535bed7f1eb7ade0e8382ab)

Regarding the block reward - fully support decreasing the block reward - but [@MicahZoltu](/u/micahzoltu) is correct here - that should not be in the same EIP

---

**boris** (2018-07-31):

Hello! From reading your website https://eos-classic.io/ you seem to be running an EIS / Ethereum Alternative chain. I understand that the difficulty bomb means more work for alternate chains as you have to coordinate hard forks on your own, but that shouldn’t concern the main chain.

Are you developing your own client node software? Are you basing it on Geth or Parity? Have you contributed any open source code or pull requests to improve Ethereum so far?

The All Core Devs call that I sat in on last Friday had a good discussion on this. Getting the community to HAVE to take an action (specifically a hard fork) every 12 - 18 months is a good forcing function. This seems like a good thing.

---

**eosclassic** (2018-08-01):

Hello, thank you for pointing out!

My idea for bomb removal is simple

1. If ethereum is immutable, why do we need to delay the bomb every time by hardforking it??
2. We can hardfork ethereum for the proper upgrade & bug fix if we want, and we shouldn’t rely on diff bomb for forking it, forcing miners to upgrade their node.

Last year difficulty bomb caused so many problem on relaying the transactions, dropping 1/2 performance of tps.

If the difficulty bomb is intended to force the upgrade, it should not affect the whole performance and gasprice like last year, therefore I am suggesting to remove completely before we fork again otherwise unpredictable transaction delay will harm the whole ecosystem of ethereum

And yes more work is great for chains however think of uncountable sidechains of ethereum that is working on the standard protocol that ethereum is using now, for sidechain development removal is needed also.

---

**eosclassic** (2018-08-01):

For my account this is my first contribution for ethereum ecosystem since we are a new coin ![:grinning:](https://ethereum-magicians.org/images/emoji/twitter/grinning.png?v=9) I hope we can keep contribute for the good stuff! ( And I am using both geth and parity for our node management )

---

**MariusVanDerWijden** (2018-08-30):

For Ethereum, the difficulty bomb is a good way to enforce frequent updates from the core developers. Otherwise miners would delay developments like Casper for ever, since there would be no incentive to create a fork. The difficulty bomb is a genius idea that allows the community to force the miners to accept forks that go against their economic believe. I however support the issuance reduction proposed by this EIP

---

**dontpanic** (2018-08-30):

the difficulty bomb is the opposite of a genius idea. It is a poor design both economically and technically. A much better solution would be to just have old version of the code base become nonfunctional after 6 weeks. Zcash uses this method.

---

**MicahZoltu** (2018-08-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mariusvanderwijden/48/1374_2.png) MariusVanDerWijden:

> miners would delay developments like Casper for ever,

Miners have no influence over whether economic participants switcth to Casper or any other client update.

