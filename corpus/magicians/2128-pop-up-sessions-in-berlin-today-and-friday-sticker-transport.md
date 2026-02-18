---
source: magicians
topic_id: 2128
title: Pop up sessions in Berlin today and Friday & sticker transport to ETHDenver
author: ligi
date: "2018-12-05"
category: Protocol Calls & happenings > Regional Sessions
tags: []
url: https://ethereum-magicians.org/t/pop-up-sessions-in-berlin-today-and-friday-sticker-transport-to-ethdenver/2128
views: 977
likes: 4
posts_count: 2
---

# Pop up sessions in Berlin today and Friday & sticker transport to ETHDenver

Will meet with [@rmeissner](/u/rmeissner) today discussing: [Add `wallet_` methods to improve dapp to wallet interaction](https://ethereum-magicians.org/t/add-wallet-methods-to-improve-dapp-to-wallet-interaction/1848) and [EIP-695: Create `eth_chainId` method for JSON-RPC - #3 by pedrouid](https://ethereum-magicians.org/t/eip-695-create-eth-chainid-method-for-json-rpc/1845/3) - if someone wants to join this discussion please let us know.

Friday will be the Ethereum Meetup Berlin so we could also do some small pop up sessions in this context.

To both occasions I will bring these stickers:

[![ethmagicians](https://ethereum-magicians.org/uploads/default/optimized/2X/e/e1f93bb782aebced15e44ac8493f2a84b7fd3b9e_2_690x388.jpeg)ethmagicians4000×2250 3.14 MB](https://ethereum-magicians.org/uploads/default/e1f93bb782aebced15e44ac8493f2a84b7fd3b9e)

If you want some just ask. And if you are going to ETHDenver it would be great if you could take a batch of them to pass them on to [@c-o-l-o-r](/u/c-o-l-o-r)

## Replies

**ligi** (2018-12-05):

Outcomes of this session:

regardng the wallet_ rpc methods:

- there needs to be a wallet_version RPC call which returns the version of the wallet_ rpc methods that it supports - should be “1.0.0” after for the first EIP
- the EIP should not contain javascript code as examples but the rpc-calls/responses
- wallet_sendTransactions vs wallet_signTransaction gets complicated when it comes to contract wallets - the solution that looked best to us in the end is wallet_handleTransaction(transaction,chainId,listOf(allowedMethods)) where allowedMethods in the simplest case is [“sign”] → would return the signed Transaction , also quite simple [“send”] → would send the transaction and return the transaction hash - it get’s a bit messy when it comes to contract wallets - we both did not yet have a clear vision here - input on this is very welcome!

other outcomes:

https://github.com/gnosis/svalinn-kotlin/issues/29

[@rmeissner](/u/rmeissner) let me know if i forgot something or got anything wrong - I also forgot one thing that I had on the agenda in my mind - I think " Possible Future Methods" should be removed from the EIP - let’s discuss these outside the EIP scope and create an EIP with them when the time is ripe. With the wallet_version call we should have a clear upgrade path for this in the future.

