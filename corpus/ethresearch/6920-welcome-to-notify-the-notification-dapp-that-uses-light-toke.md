---
source: ethresearch
topic_id: 6920
title: Welcome to Notify. The notification dapp that uses light tokens to notify users right from a smart contract. 75k gas for a notification
author: pr0toshi
date: "2020-02-11"
category: Applications
tags: []
url: https://ethresear.ch/t/welcome-to-notify-the-notification-dapp-that-uses-light-tokens-to-notify-users-right-from-a-smart-contract-75k-gas-for-a-notification/6920
views: 1970
likes: 1
posts_count: 9
---

# Welcome to Notify. The notification dapp that uses light tokens to notify users right from a smart contract. 75k gas for a notification

The Notify dapp lets you send a notification over Ethereum using “pseudo-tokens”; any wallet that supports ERC20 tokens is capable of receiving Notify messages!

We use a very small smart contract that implements just enough of the ERC20 interface to allow wallets to interpret them as ERC20 token contracts.

When you send a message, one of these contracts gets created with your message and a transfer event is emitted that the recipient’s wallet will interpret as receiving a token. When their wallet looks up the name of the token they just received (part of the ERC20 interface), the contract returns your message!

To use the Dapp, just paste the address of the person you want to notify, type in a message and hit Notify! The next time they look at their wallet, they’ll see your message; it’s that easy!

Once a message is received, the recipient can use their wallet to “transfer” the token to any address. When they do, the contract simply deletes itself, as it has served its purpose. This keeps the recipient’s wallet free of old messages and saves the Ethereum network a few bytes of storage.

A single notification only costs about 75k gas, as much as 3 eth transfers or about $0.02.

Try it out at [Nowdapp.com](http://nowdapp.com/) or contact us on [Twitter](https://twitter.com/0xNow) to learn more!

Source


      ![image](https://etherscan.io/images/favicon2.ico)
      [Ethereum (ETH) Blockchain Explorer](https://etherscan.io/address/0x9212aae431d079adadf1041be4cf2db4a929fe63)




###

The Contract Address 0x9212aae431d079adadf1041be4cf2db4a929fe63 page allows users to view the source code, transactions, balances, and analytics for the contract address. Users can also interact and make transactions to the contract directly on...








Btw the dapp has a fee for the front end but the contract and use by other ABI will not pay the fee.

## Replies

**Europe** (2020-02-12):

You should write on the form that there is 0.001 ETH fee and that some chars are not allowed. Other than that - it’s a great idea - I might try how it works with Argent or Metamask later.

---

**pr0toshi** (2020-02-12):

Most should be ok if they’re utf8 or the wallet supports them. The fee for nows just there to stop flooding. If dapps or services want this we got one with no fee and custom symbol and amount too for free. Just trying to not let people be dumbasses

---

**Europe** (2020-02-12):

It is misleading not to display the fee on http://nowdapp.com/. I could’ve easily confirmed the transaction based on your description without checking the amount (assuming I’m paying only the tx fee).

I suggest you modify the form to allow users to set the (donation) fee (i.e. default=0.001 but it can also be 0).

---

**pr0toshi** (2020-02-12):

Again it’s there for flooding and proof of concept. Still under what ud pay if u made a token. There’s a free implementation that offering to projects to use just don’t want people that flood transactions using this before it’s big

---

**pr0toshi** (2020-02-12):

Also if people want the source was verified but ull need to know huff. This was going to be 0 fee but thought that offering the 0 one to the public would probably not be great for adoption with people using for flooding. Would cost u only 2000 usd for 100k tokens.

---

**Europe** (2020-02-12):

OK, but could you please just display the fee?

---

**pr0toshi** (2020-02-17):

Removed it. It’s probably useless when we open source anyway.

---

**pr0toshi** (2020-03-02):

And by when we that’s a when we are already open source. Not a when we are going to. It’s always been open source.

