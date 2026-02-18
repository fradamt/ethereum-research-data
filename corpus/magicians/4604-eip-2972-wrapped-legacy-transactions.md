---
source: magicians
topic_id: 4604
title: "EIP-2972: Wrapped Legacy Transactions"
author: MicahZoltu
date: "2020-09-12"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-2972-wrapped-legacy-transactions/4604
views: 2838
likes: 1
posts_count: 7
---

# EIP-2972: Wrapped Legacy Transactions

**Simple Summary**

Two new transaction types for wrapping legacy transactions with and without a chain ID.

**Abstract**

Introduces two new [EIP-2718](https://eips.ethereum.org/EIPS/eip-2718) transactions that are signature compatible with legacy transactions and can be automatically upgraded by any client.

```auto
0x00 || yParity || r || s || 0x65000000 || rlp(nonce, gasPrice, gasLimit, to, value, data)
0x01 || yParity || r || s || 0x65000000 || rlp(nonce, gasPrice, gasLimit, to, value, data, chainId, 0, 0)
```

## Replies

**matt** (2020-09-14):

A few questions:

1. What is the goal of wrapping legacy transactions today? The legacy transaction will continue to be valid for a period of time. I think this idea should be pursued once it is deemed necessary, rather than just preemptive.
2. Is supporting unprotected (no chain id) transactions necessary? It would be great to determine if this functionality is still used.
3. @pipermerriam has convinced me that some smart transitions to SSZ can provide a lot of benefits to eth1, particularly in the area of witnesses. It would be useful to understand how the choice of SSZ here is useful, as well as what areas of eth1 would be most beneficial to convert to SSZ. Hopefully doing so can help us avoid to using SSZ just to use it.

---

**MicahZoltu** (2020-09-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> What is the goal of wrapping legacy transactions today ? The legacy transaction will continue to be valid for a period of time. I think this idea should be pursued once it is deemed necessary, rather than just preemptive.

That would be a discussion to have regarding mainnet inclusion, which I believe is now handled over at the eth1.0 specs repository now.  ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)  That being said, step 1 for deprecation is to provide a new option.  The sooner we do that, the sooner we can start the next steps of the deprecation process (such as defining an end of life date and a mechanism for slowly killing off stragglers).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> Is supporting unprotected (no chain id) transactions necessary? It would be great to determine if this functionality is still used.

Yes, it is commonly used to create deployment transactions that can be executed on all chains at the same address via a vanity signature (create signature by hand, recover address, send ETH to address, submit transaction).  There are EIPs out there that provide a bettere way to achieve that, but they aren’t available yet.

Even if we didn’t want that, in order to ensure that someone with a signature from before EIP-155 can still submit that transaction to the blockchain we have to continue supporting both formats.  There is a strong desire to ensure that someone who has an old hardware wallet or something doesn’t lose the ability to sign transactions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> It would be useful to understand how the choice of SSZ here is useful, as well as what areas of eth1 would be most beneficial to convert to SSZ. Hopefully doing so can help us avoid to using SSZ just to use it.

Agreed! Unfortunately, I’m not the right person to do this.  Would love to get some help fleshing out the Rationale by someone more knowledgeable than I on *why* SSZ!

---

**matt** (2020-09-14):

I also see that `yParity` is expected to be either `0` or `1`. What is the rationale for departing from the standard `27` or `28` used by Ethereum today (tbh, not sure where those numbers came from – best I’ve only found this [explanation](https://github.com/ethereum/go-ethereum/issues/19751#issuecomment-504900739) by Peter)?

Edit: from the yellow paper:

> It is assumed that v is the ‘recovery identifier’. The recovery identifier is a 1 byte value specifying the parity and finiteness of the coordinates of the curve point for which r is the x-value; this value is in the range of [27, 30], however we declare the upper two possibilities, representing infinite values, invalid. The value 27 represents an even y value and 28 represents an odd y value.

Unless there is a strong motivation to deviate, I think it is best to `v` to continue being either `27` or `28`.

---

**MicahZoltu** (2020-09-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> What is the rationale for departing from the standard 27 or 28 used by Ethereum today (tbh, not sure where those numbers came from – best I’ve only found this explanation by Peter)?

The rationale is that it is a point of confusion and a source of bugs in integration software and there was no good reason for 27/28 in the first place.  It was an artifact of copying Bitcoin that just kind of meandered its way into Ethereum and has confused developers ever since.  One nice property of 0/1 is that you can treat it as a boolean in code, which results in code like `yParity ? x : y` rather than `v == 27 ? x : y` which is not only marginally simpler, but also more intuitive since the variable name now actually makes sense to anyone familiar with the concept of parity in mathematics.

---

**tkstanczak** (2020-09-22):

I think everywhere else we save signatures in the order of r, s, v (yParity) so maybe better to do the same here?

---

**MicahZoltu** (2020-09-24):

This EIP no longer specifies a new transaction type.  However, the feedback still applies to new EIPs that do.  In the transaction signatures previously, it was `v,r,s` I believe?  Also I think byte array encoded signatures also lead with the parity byte?  Where does parity byte come last?

