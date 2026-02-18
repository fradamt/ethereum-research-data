---
source: ethresearch
topic_id: 3379
title: Censorship based on stake taint
author: govebela
date: "2018-09-14"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/censorship-based-on-stake-taint/3379
views: 1649
likes: 2
posts_count: 2
---

# Censorship based on stake taint

With proof of work there is a clear separation between the hardware investment and the proof of work nonce. There is no way to trace back the nonce to the hardware and thus the miner (note: not the reward address) can’t be held accountable because of plausible deniability.

However with proof of stake, the block producer is selected based on identity tied to a stake on chain. This stake can be traced and thus made to be tainted if the block producer doesn’t comply with regulations from a powerfully entity.

How is Casper going to resolve this?

## Replies

**MihailoBjelic** (2018-09-14):

IMHO there’s absolutely no need to resolve this. Actually, that’s one of the advantages of PoS over PoW. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)  To make things better, the stake of a dishonest validator is “slashed”, i.e. burned (even worse than tainting buahaha ![:smiling_imp:](https://ethresear.ch/images/emoji/facebook_messenger/smiling_imp.png?v=9)). Slashing conditions are baked into the protocol, so there’s no “powerfully entity” that can influence this process. This all is impossible to do in PoW (you cannot slash ASICs of a dishonest Bitcoin miner ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)).

On the other hand, speaking of censorship of miners/validators by outside entities (e.g. governments), both the PoW miners and the PoS validators can be anonymous, and can even protect their IP addresses if needed. But, PoS has a big advantage here, too - there is no expensive hardware that is hard (sometimes even impossible)  to hide and/or relocate. If you have a big ASIC farm in a certain country, the local government can easily locate/confiscate it and even put you in jail (we’ve seen that happening in Venezuela recently). ![:disappointed_relieved:](https://ethresear.ch/images/emoji/facebook_messenger/disappointed_relieved.png?v=9) If you are a PoS validator, it’s extremely hard for a government to locate/confiscate your wallet. ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9)

Hope this helped! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

