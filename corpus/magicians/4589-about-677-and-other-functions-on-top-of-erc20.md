---
source: magicians
topic_id: 4589
title: About #677 and other functions on top of ERC20
author: Amxx
date: "2020-09-09"
category: EIPs
tags: [token, erc20]
url: https://ethereum-magicians.org/t/about-677-and-other-functions-on-top-of-erc20/4589
views: 1941
likes: 2
posts_count: 6
---

# About #677 and other functions on top of ERC20

It seems that the as been a recent regain of interest issue for #677 (that is NOT an ERC has it doesn’t have the proper documentation) both on the EIP repo and on youtube, with [ChicoCrypto making a video about it](https://www.youtube.com/watch?v=e8m2vrUBixE).

While I love the underlying idea, I have to emphasize that there are many ways to achieve the same results. I know at least 2:

- Chainlink’s (and Dai’s ?) transferAndCall:

the function `transferAndCall(address receiver, uint amount, bytes data)` transfers some tokens and calls the function `onTokenTransfer(address from, uint256 amount, bytes data)` on the receiving side to notified the tranfered happened.

- iExec’s approveAndCall

the function `approveAndCall(address _spender, uint256 _value, bytes _extraData)` only approves the transfer, and call the function `receiveApproval(address _from, uint256 _value, address _token, bytes _extraData)` on the receiving side to notifity it can transferFrom

I personnaly prefer the second pattern, because despite it using a little bit more gas, it doesn’t break the approve-transferFrom workflow dapps are used to. Also receiver are less likelly to have bugs due to poor implementation of the onTokenTransfer function.

I’m sure people will have other views: lets discuss that, and eventually make up a standard for futur tokens (even though ERC20 are not that hyped anymore)

## Replies

**Amxx** (2020-09-09):

[@MicahZoltu](/u/micahzoltu) & [@se3000](/u/se3000),   you might have many things to say

---

**MicahZoltu** (2020-09-09):

The long term solution to this problem is Rich Transactions, which I have been trying to work on.  It would allow a single signed transaction to do multiple operations in a row such as approve and then call.

---

**wighawag** (2020-09-09):

[@amxx](/u/amxx) thanks for bringing that up here.

I also prefers the approveAndCall approach. it is also the approach we choose at Sandbox except that as notification, we simply ensure the first param of the call data being forwarded is equal to the msg.sender. This is unconventional and I would instead now use something like EIP-2771 to pass the notification data (the address should be sufficient though)

The nice thing about is that it retain the freedom of the receiver to choose the function signatures it wish.

---

**wighawag** (2020-09-09):

I have another proposition : https://github.com/wighawag/transfer-gateway

There are quire few variant of these “transfer gateway”

The simplest is the “Trusted gateway” shown in the repo, where we only need one deployed per network.

One benefit for it is that it works with existing ERC20 contract.

The gateway need to be user approved once per erc20 and then it work with every gateway recipient.

For new ERC20 contract they can make the gateway a pre-approved operator for all owner to not require further approval

The gateway could also support [EIP-2612](https://eips.ethereum.org/EIPS/eip-2612) permit message so it handle all approval automatically as part of the tx.

For recipient, the logic is quite simple with a trusted gateway, they simply extract [msg.data](http://msg.data/) (a la [EIP-2771](https://eips.ethereum.org/EIPS/eip-2771) metatx _msgSender trick) : https://github.com/wighawag/transfer-gateway/blob/c09d33ca6e116b9e65ca1d6ce46fe90e39b0f14f/src/ERC20Consumer.sol#L27-L41

This way there is no need for specific receive function, simplifying the receiver code

---

**Amxx** (2021-03-06):

Since I openned this topic, I learned about [ERC1363](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1363.md) which is actually marked as final.

- transferAndCall → onTransferReceived
- transferFromAndCall → onTransferReceived
- approveAndCall → onApprovalReceived

