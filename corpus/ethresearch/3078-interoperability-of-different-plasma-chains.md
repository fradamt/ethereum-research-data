---
source: ethresearch
topic_id: 3078
title: Interoperability of different Plasma Chains
author: Sowmayjain
date: "2018-08-24"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/interoperability-of-different-plasma-chains/3078
views: 1957
likes: 0
posts_count: 3
---

# Interoperability of different Plasma Chains

We are seeing a wide adaptation of plasma chains and lots of different projects are building their own sidechains. Isn’t it bit inconvenient to deposit ether (or tokens) in every new plasma chains in order to use their services?

Is it possible to deposit once and use them on many different plasma side chains?

## Replies

**YunJungHwan** (2018-08-25):

Personally, I think it is almost impossible. Comparing IBC to plasma, IBC does not guarantee security in the side chain. Plasma, however, ensures security in the side chain. This part complicates the plasma. In order to ensure the security of the plasma chain, I think at least all the tokens in the plasma chain must pass through the plasma contract. How is it possible to guarantee the security of tokens that do not pass through themselves? If you want more interaction between the chains, it would be better to choose IBC.

---

**nginnever** (2018-08-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/sowmayjain/48/899_2.png) Sowmayjain:

> Is it possible to deposit once and use them on many different plasma side chains?

Yeah atomic swaps should do the trick for payment state (a liquidity provider can verify your plasma state and swap it for state they have on a different plasma chain). This is easy to reason about for monetary transactions (I’ll swap plasma chain A tokens for equivalent plasma chain B tokens), but harder to reason about for smart contracts (system probably has to mass exit and reboot on a new chain which isn’t ideal). This assumes that chain A and B are sophisticated enough to implement HTLCs.

Atomic Swaps - There is already a proposal to make fast withdrawals in a similar way, this should be extensible between two plasma chains as well.



    ![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png)
    [Simple Fast Withdrawals](https://ethresear.ch/t/simple-fast-withdrawals/2128) [Plasma](/c/layer-2/plasma/7)



> Design from conversation with vi, David Knott, Ben Jones, and Eva Beylin. Thanks to Eva Beylin & Kelsie Nabben for review/edits.
>
> TL;DR
> We can enable fast withdrawals without Plasma contracts by taking advantage of root chain smart contracts. Withdrawals can then be handled as tokenized debt, and we can build a marketplace from there.
> Background
> Fast withdrawals are a construction in Plasma that effectively boil down to an atomic swap between the Plasma chain and the root chain. They’re useful…

This could alternatively be done with perun style “virtual channels” where you could swap chain A tokens for chain B tokens with state-channels. If both chains can implement a multisig account that exits to a state-channel contract on the parent, then two parties could agree to swap plasma tokens. This should get you to the point where you can deposit on chain A and then hop to chain B → C → and then exit on chain D. (in theory ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) )

