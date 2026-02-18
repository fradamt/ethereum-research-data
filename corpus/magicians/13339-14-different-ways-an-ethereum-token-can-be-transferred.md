---
source: magicians
topic_id: 13339
title: 14 different ways an Ethereum token can be transferred
author: agostbiro
date: "2023-03-16"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/14-different-ways-an-ethereum-token-can-be-transferred/13339
views: 806
likes: 5
posts_count: 5
---

# 14 different ways an Ethereum token can be transferred

Hi folks,

I’ve collected 14 different ways (e.g. [ERC-2612,](https://eips.ethereum.org/EIPS/eip-2612) [ERC-2771](https://eips.ethereum.org/EIPS/eip-2771)) an Ethereum token can be transferred from an EOA with flow charts:


      ![](https://ethereum-magicians.org/uploads/default/original/2X/8/8f0a562a90992dd656ced3f9b9b37c942cfbde54.png)

      [HackMD](https://hackmd.io/@agostbiro/SksOybaJh)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###



# Token Transfer Traces  **Update: the canonical version of this document now lives at https://sealv










I wanted to ask your feedback: what’s missing?

## Replies

**bawtman** (2023-03-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agostbiro/48/8393_2.png) agostbiro:

> I’ve collected 14 different ways (e.g. ERC-2612, ERC-2771) an Ethereum token can be transferred from an EOA with flow charts:

Great write up agostbiro, Is there any type of cross chain methods that could be included in this? I am not even sure that is possible but is something I am working towards. Thank you for the info!

---

**bawtman** (2023-03-16):

Ironicly just after I posted this another post came up https://ethereum-magicians.org/t/the-erc-21-standard-for-cross-chain-compatibility/13327 ![:grin:](https://ethereum-magicians.org/images/emoji/twitter/grin.png?v=12)

---

**agostbiro** (2023-03-17):

Thanks, that’s great input!

As far as I can tell, bridges work like exchanges from the perspective of the source change.

I’ve seen the following patterns used by bridges:

- Native token transfer
- Custom token approval with contract spender

But it’s possible that I’m missing something.

---

**agostbiro** (2023-04-15):

So I initially found 1 way a native token can be transferred and 13 ways a custom token can be transferred. After specifying custom token transfers from a wallet perspective with TLA+, it turns out there are 42 ways a custom token can be transferred from an EOA. Wrote it up here: [Exploring Ethereum Token Transfers with TLA+ for Wallet Security - SealVault](https://sealvault.org/blog/2023/04/token-transfer-tla/)

