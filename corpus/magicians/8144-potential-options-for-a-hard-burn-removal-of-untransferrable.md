---
source: magicians
topic_id: 8144
title: Potential options for a hard burn/removal of untransferrable ERC20 tokens
author: Spirit
date: "2022-01-29"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/potential-options-for-a-hard-burn-removal-of-untransferrable-erc20-tokens/8144
views: 894
likes: 0
posts_count: 2
---

# Potential options for a hard burn/removal of untransferrable ERC20 tokens

Hello!

I want to discuss potential options to remove untransferrable, scam (honeypot) ERC20 tokens from a wallet: tokens that have their contract locked or paused specifically to steal users funds through UniSwap etc.

https://info.etherscan.com/what-happens-when-erc-20-token-transfer-might-have-failed/

Is it possible, in theory, to remove or ‘hard burn’ untransferrable tokens from a wallet?

I know most think it’s probably not an important issue, and you could just start fresh with a new wallet – but with the growth of ENS, I would argue having sovereigny over the contents of our wallets is more important than ever.

Is it technically feasible to propose an update that could implement a way to ‘hard burn’ anything in your wallet, overriding the locked or paused ERC20 contract?

Could obvoious scam tokens ever be dropped with The Purge?

I’d love to hear your thoughts, and explore possibilities and hopefully learn some valuable info in the process. Thank you ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

## Replies

**davidc** (2022-01-31):

Do you mean to extend ERC20 with some sort of a user-initiated burn function, so that it is no longer  associated with your wallet?

Couldn’t a scam token just decide not to implement this functionality correctly?

