---
source: magicians
topic_id: 12404
title: Regarding the development of the wallet program, can a safe deposit box feature be added?
author: qiuyuning
date: "2023-01-03"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/regarding-the-development-of-the-wallet-program-can-a-safe-deposit-box-feature-be-added/12404
views: 374
likes: 2
posts_count: 2
---

# Regarding the development of the wallet program, can a safe deposit box feature be added?

I don’t know programming, every authorization of the wallet, I can’t understand, what am I authorizing to the program? Every authorization of the wallet, I have to take my chances, I have to go trust the programmer, don’t steal my money, don’t steal my NFT. because of an inexplicable authorization, money is stolen, NFT is transferred, it has happened many times. Can you add a safe deposit box feature or firewall feature to the wallet where money and NFT in the safe or firewall cannot be authorized to be transferred. This would give me more peace of mind and I would not have to apply for multiple wallets.

## Replies

**Pandapip1** (2023-01-03):

The point is that you *are* trusting the program when you authorize it. But instead of this authorization being implicit and done without your consent, you have to manually let the program access your funds (hence, the authorization transactions!). The feature you desire exists by default. It is only possible to have funds stolen through user error (which is unfortunately very easy to do at the moment). As such, this is more of a UI problem than it is a feature that wallets lack.

If you want what is equivalent to a safe deposit box, I would recommend creating a multisig with a time delay and code that only allows `transfer` calls or regular ether transfers. You could do this with a Gnosis safe and a custom-made guard.

