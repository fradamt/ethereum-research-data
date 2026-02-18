---
source: magicians
topic_id: 11771
title: EIP-5987 - Permissionless Transfer With Authorization
author: mgrant
date: "2022-11-17"
category: EIPs
tags: [gas]
url: https://ethereum-magicians.org/t/eip-5987-permissionless-transfer-with-authorization/11771
views: 1134
likes: 1
posts_count: 10
---

# EIP-5987 - Permissionless Transfer With Authorization

Thread to discuss [EIP-5987](https://github.com/ethereum/EIPs/pull/5987)

## Replies

**MicahZoltu** (2022-11-20):

I would like to see support for contract wallets added.  Perhaps something like a registry where a wallet can register a “signature validator” contract, and then an opaque set of bytes can be provided (instead of v,r,s) which is given to the signature validator contract to verify whether the provided data is sufficient to allow the proposed transfer.

Generally speaking, we are *trying* to move away from EOA wallets, and this feels like it enshrines them a bit more (similar to `permit`) as it makes it so EOAs can do signed transfers while contract wallets have to follow the approve-send flow.

---

**mgrant** (2022-11-20):

[@MicahZoltu](/u/micahzoltu) thanks for the feedback. Contract support would be a separate, parallel EIP. It is not in scope of this EIP.

---

**mgrant** (2022-11-20):

[@MicahZoltu](/u/micahzoltu) also I don’t know if I agree that we are trying to move away from EOAs. Both can and will live in parallel for different use-cases. I don’t want to sidetrack this thread…but I would love to have a side chat on the merits of EOA vs contracts.

---

**Pandapip1** (2022-11-20):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/cc9497/48.png) mgrant:

> I don’t know if I agree that we are trying to move away from EOAs

You may not agree with it, but the entire Ethereum ecosystem is trying to move away from them. EOAs have a strict subset of the functionality of contract accounts, which is why the vast majority of Ethereum developers support some form of AA.

---

**mgrant** (2022-11-20):

[@Pandapip1](/u/pandapip1) no one person can speak for “the entire ecosystem”. Account abstraction is not mutually exclusive with better EOAs. AA is to add functionality for contracts to behave similar to EOAs. Are we going to avoid any improvement to EOA UX in the *years* in-between now and when full AA is realized?

Also, who is going to pay deployment cost for these AA contracts? If a new user wants to onboard into the system and they do not have ETH how do they get an AA contract…they need to trust a third party? That does not align with the self custody model we must strive for.

---

**mgrant** (2022-11-20):

Side note: EIP-3009 *already* contains receiveWithAuthorization so contracts do not need to do approve/send flow. The limitation is that receiveWithAuthorization requires to address to be msg.sender to prevent frontrunning, which does not work with a permissionless relayer.

EDIT: hmmm apparently receiveWithAuthorization never made it into the EIP-3009 PR (despite it being implemented in the USDC contract). The original discussion [here](https://github.com/ethereum/EIPs/issues/3010) does have more info.

---

**Pandapip1** (2022-11-21):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/cc9497/48.png) mgrant:

> no one person can speak for “the entire ecosystem”.

You’re right, but I challenge you to find a single core dev that doesn’t support some form of account abstraction. Why not support [EIP-1271](https://eips.ethereum.org/EIPS/eip-1271)?

---

**MicahZoltu** (2022-11-21):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/cc9497/48.png) mgrant:

> also I don’t know if I agree that we are trying to move away from EOAs. Both can and will live in parallel for different use-cases. I don’t want to sidetrack this thread…but I would love to have a side chat on the merits of EOA vs contracts.

The general form of the problem is that the more we improve EOAs (e.g., UX improvements) the harder it is to get people to switch to contract wallets, which provide significant security benefits.  A big part of the issue here is information asymmetry between users and developers, where the users often don’t realize the risks they are taking when they use an EOA with a written down seed phrase (compared to say a social or time based recovery wallet).

Note: I recognize that this is just another form of the argument that “we know better than the users, so we should build things that protect them even when they don’t realize they need it… for their own good”.

Note 2: I would not block an EIP like this from being included, but I would like to see another EIP released at the same time and lobbied for integration in tandem with this EIP.  What I would really like to see avoided is tokens like USDC integrating this and *not* integrating a similar EIP that provides the same UX but for contract wallets.

Already on Uniswap it is *easier* for users to securely swap USDC with an EOA than with a contract wallet, so this isn’t some hypothetical problem, it is a real problem that exists today.

---

**mgrant** (2022-11-21):

[@MicahZoltu](/u/micahzoltu) [@Pandapip1](/u/pandapip1) to be clear, I totally recognize that better account abstraction is going to be a huge value add. Certainly excited on that front!

I think we can agree that there are two distinct bodies of work:

1. Add permissionless meta tx relay for externally owned accounts.
2. Add permissionless meta tx relay for contract accounts.

This EIP is only addressing #1.

However, I do understand that improvements to EOAs without similar improvements to contract accounts decrease the likelihood of contract account adoption, and I agree that #2 is important. But I do have a few concerns:

- Difficulty. What I like about this EIP as it stands is that it is incredibly simple (just 13 additional lines when compared to original EIP-3009). I worry that building support for contract account permissionless relay will require a lot of new code and as you know established tokens such as USDC are quite risk averse, especially when thinking about potential on-chain changes.
- Standardization. There are a lot of ways to solve this, but what one is the best? What standard will be adopted? In the meantime, while consensus is being reached, a wrapper contract can handle all of this logic with some massaging from custodian / contract account deployers.
- Adoption. Are users even interested in permissionless relay of EOAs? Is it worth trudging through the above 2 challenges to get everything working for contract accounts or should we iterate and re-evaluate later if EOAs prove to be successful?

(Thank you both for all of the feedback and discussion, this is really helpful context!)

