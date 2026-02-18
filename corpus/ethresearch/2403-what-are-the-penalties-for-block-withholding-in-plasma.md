---
source: ethresearch
topic_id: 2403
title: What are the penalties for block withholding in Plasma?
author: dh1234
date: "2018-07-02"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/what-are-the-penalties-for-block-withholding-in-plasma/2403
views: 1305
likes: 0
posts_count: 3
---

# What are the penalties for block withholding in Plasma?

The whitepaper says:

> In the event a chain is attacked via block withholding or other
> Byzantine behavior, the non-Byzantine participants conduct a mass compact withdrawal
> on the parent/root blockchain. If bonds for the highest parent Plasma chain are in the form
> of tokens, it is likely the value of the token will significantly devalue as a result of the mass
> exit.

It seems to imply that a token will devalue, but which tokens? Let’s say you have a dapp with a token that uses a Plasma sidechain and  you use those tokens for POS bonds, it seems pretty bad that all those tokens would devalue. It seems like everyone using the dapp gets punished, not just the validators withholding blocks.

## Replies

**josojo** (2018-07-02):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/d/35a633/48.png) dh1234:

> It seems like everyone using the dapp gets punished, not just the validators withholding blocks.

Well, there are many token models out there. I guess that Vitalik and Joseph had the pure staking token model in mind: Tokens are primarily used to for staking in the plasma chain. And the fees in the plasma chain are also distributed only to the people, who are staking - maybe by a block reward.

Then the usual people using the plasma-dapp would just pay some fee in eth and they would not lose anything if the data-unavailability occurs.

Be aware that there are also solutions which motivate operators to ensure data-availability, even when they are bonded by Ether only. With snarks/starks one is able to do decide on data-unavailability more objectively, for more info see [here](https://ethresear.ch/t/interlinking-plasma-exit-request-with-plasma-correctness-proofs-using-snark-stark/2331/4).

---

**kfichter** (2018-07-12):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/d/35a633/48.png) dh1234:

> It seems to imply that a token will devalue, but which tokens?

Generally the idea here is that stake is held in one token, but that fees are paid in some other token(s). You definitely don’t want to punish users for an action taken by the operator.

