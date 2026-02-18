---
source: magicians
topic_id: 20058
title: "EIP-7704: Soul Resonance Token"
author: Mike_0x1024
date: "2024-05-20"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/eip-7704-soul-resonance-token/20058
views: 743
likes: 4
posts_count: 2
---

# EIP-7704: Soul Resonance Token

**Introduction:**

SRT(Soul Resonance Token), introduces a novel token protocol. Much like SBT, SRT lacks support for transfer methods, prohibiting users from moving SRT assets between different accounts. What sets SRT apart is its utilization of the mint() and burn() methods via the Bonding Curve mechanism, facilitating pricing and trading functionalities for SRT. Consequently, SRT represents an asset type that is non-transferable yet tradable. By merging the features of SBT’s soul binding and the tradability of traditional ERC20 assets, SRT effectively closes the gap between SBT and conventional ERC20 tokens.

**Characteristics:**

1. Non-transferable:

The inability to transfer SRT tokens ensures that they remain securely bound to the account where they were originally minted or acquired.

1. Tradable:

Despite being non-transferable, SRT tokens are still tradable. This means that they can be bought and sold on decentralized exchanges (DEXs) or other platforms that support trading of SRT tokens. The trading functionality allows users to exchange SRT tokens for other assets or currencies within the ecosystem in a unique way.

1. Customizable Market Curve:

SRT implements a customizable market curve through the Bonding Curve mechanism. This curve determines the pricing and supply dynamics of SRT tokens based on the amount of tokens in circulation. By customizing the market curve, developers can tailor the token economics of SRT to suit specific use cases or objectives.

https://github.com/ethereum/ERCs/pull/414

## Replies

**jhfnetboy** (2024-05-26):

If you want to buy or sell SRT, you must transfer into or out of your account.

or transfer SRT with a holding account?

