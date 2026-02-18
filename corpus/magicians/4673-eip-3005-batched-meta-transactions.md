---
source: magicians
topic_id: 4673
title: "EIP-3005: Batched Meta Transactions"
author: cmango
date: "2020-09-25"
category: EIPs
tags: [erc-3005, eip-3005]
url: https://ethereum-magicians.org/t/eip-3005-batched-meta-transactions/4673
views: 2780
likes: 0
posts_count: 6
---

# EIP-3005: Batched Meta Transactions

Here’s the place to discuss EIP-3005: [EIP-3005: Batched meta transactions](https://eips.ethereum.org/EIPS/eip-3005)

Link to the PR: https://github.com/ethereum/EIPs/pull/3005

tl;dr:

- The EIP defines a function called processMetaBatch() that extends any fungible token standard (like ERC-20).
- The function can process a batch of meta transactions sent as data in a single on-chain transaction.
- Other meta tx relaying implementations can only process 1 meta tx per 1 on-chain tx. Some allow batching, but only a batch of meta txs from a single sender (not multiple senders).
- EIP-3005 allows sending multiple meta txs from multiple senders (in 1 on-chain tx) which reduces the gas cost per meta transaction (compared to other relaying solutions).

I have also conducted **gas usage tests** and compared the results to other relaying services and also to just doing a normal on-chain token transaction. You can [see the results and conclusions here](https://github.com/defifuture/erc20-batched-meta-transactions#types-of-batched-meta-transactions).

Looking forward to your feedback ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=9)

## Replies

**MicahZoltu** (2020-09-28):

I question whether the gas savings (32 bytes of calldata per transaction) are worth the cognitive complexity introduced by having the nonces not included in the transaction.  While this solution will work, it makes it harder to understand the code since the data being signed is not all included in the calldata.

---

**MicahZoltu** (2020-09-28):

I believe that an array of tuples would be easier to work with rather than a bunch of arrays.

If you did an array of “tuples”, you *could* bitpack which would let you give you some gas savings and would let you add the nonce to the payload at lower gas cost.  For example, first 20 bytes is the sender, next 20 bytes is the recipient, next 32 bytes is the amount, next 32 bytes is the relayer fees, next 5 bytes is the timestamp, next 2 bytes is the nonce, next byte is `v`, followed by 32 bytes for `r` and 32 bytes for `s`.  This would reduce your calldata size by quite a bit and make adding in the nonce pretty inexpensive (which makes the specification easier to describe and grok).

---

**MicahZoltu** (2020-09-28):

Layer 1 sponsored transactions are something being [worked on](https://eips.ethereum.org/EIPS/eip-2711).  Is this still useful in the face of such transactions?

---

**cmango** (2020-09-28):

Hi Micah, thanks again for your feedback! ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=9)

About the nonce and bitpacking data: makes sense, I’ll try it out and see how it works out. The main reason why I left out nonce from parameters was actually not gas savings, but avoiding the “Stack too deep” error. Not sure if the same error would happen when unpacking a payload, but it’s worth trying.

EIP-2711: This is a very interesting proposal! I must have missed it in my research because it uses a term “sponsored transactions”, not meta transactions (but I understand why). If this goes through, it will probably make meta txs obsolete (including my proposal), but I wouldn’t mind it ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=9)

EDIT: I see the EIP-2711 talks about batched txs from the same user. Do you think batched transactions from different users would be possible to implement? This is what EIP-3005 focuses on.

---

**MicahZoltu** (2020-09-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cmango/48/2864_2.png) cmango:

> The main reason why I left out nonce from parameters was actually not gas savings, but avoiding the “Stack too deep” error.

This issue can be solved in other ways, usually just by re-ordering variables or creating local scopes and helper methods.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cmango/48/2864_2.png) cmango:

> I see the EIP-2711 talks about batched txs from the same user. Do you think batched transactions from different users would be possible to implement? This is what EIP-3005 focuses on.

There are no immediate plans for a layer 1 solution to transaction batches from multiple users.  I personally believe the use case for that is pretty narrow so I haven’t pushed for it in layer 1 since it increases complexity for *all* transactions if present.

