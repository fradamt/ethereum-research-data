---
source: magicians
topic_id: 4912
title: Will ETH 2.0 fix these 2 ETH 1.x flaws?
author: Hikari
date: "2020-11-04"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/will-eth-2-0-fix-these-2-eth-1-x-flaws/4912
views: 544
likes: 0
posts_count: 1
---

# Will ETH 2.0 fix these 2 ETH 1.x flaws?

Hello. I haven’t found any article talking about these issues, so I decided to make a post asking about them.

First one is ETH not being compliant to ERC20. ERC20 standard provides an interface so that smartcontracts are able to interact with any ERC20-compliant token. As we all know, ETH is prior to ERC20 and isn’t compliant to it, so sc must either have double functions to handle ERC20 and ETH, or rely on swapping for WETH which makes them spend more gas, and WETH isn’t ETH at all. Anybody knows if on ETH 2.0 we’ll have ETH compatible with fungible tokens standard?

The other one is needing to authorize smartcontracts to mess with a token on our address so that we can interact with it using that token. I don’t understand how that design could have been created, as it’s a huge security flaw. We must trust sc won’t steal our tokens from our address and will do only what it announces and we accept, which includes it being hacked or “used in innovative ways”.

For Trezor T users it’s even worse, as we never see on our device screen what token is being sent neither its amount.

Will ETH 2.0 remove this authorization stuff and just let we clearly see on transaction the token amount we’re sending when interacting with the sc?
