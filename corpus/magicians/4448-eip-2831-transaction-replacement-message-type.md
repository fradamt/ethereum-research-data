---
source: magicians
topic_id: 4448
title: "EIP-2831: Transaction Replacement Message Type"
author: greg
date: "2020-07-26"
category: EIPs
tags: [eth1x, eip-2831]
url: https://ethereum-magicians.org/t/eip-2831-transaction-replacement-message-type/4448
views: 3423
likes: 1
posts_count: 14
---

# EIP-2831: Transaction Replacement Message Type

Discussion for [EIP-2831 Transaction Replacement Message Type](https://github.com/ethereum/EIPs/pull/2831).

## Replies

**jpitts** (2020-07-30):

Here is [@greg](/u/greg)’s overview thread and call for feedback from Twitter.

https://twitter.com/gregthegreek/status/1288500914081484811

---

**greg** (2020-07-31):

Thanks [@jpitts](/u/jpitts)! ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**jpitts** (2020-08-10):

Noting here (for others who may arrive) that there are a number of relevant comments posted in the PR starting with this one: https://github.com/ethereum/EIPs/pull/2831#issuecomment-665253875

[@MicahZoltu](/u/micahzoltu) and [@greg](/u/greg) helpfully keep pointing out that the comments should go to this thread on the Forum  ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**pedrouid** (2020-08-10):

This is a great proposal [@greg](/u/greg) ![:raised_hands:](https://ethereum-magicians.org/images/emoji/twitter/raised_hands.png?v=9)

IMO we should break it down into two standards however to enforce stricter rules

It will improve both developer and user experience. My feedback is that tx_replacement is just too flexible even if it enforces the same nonce

My suggestion would be to replace `tx_replacement` with `tx_cancel` and `tx_speedup`

`tx_cancel`

- same nonce
- equivalent from and to
- zero value
- no data

`tx_speedup`

- same nonce
- same to
- same value
- same data
- higher gasPrice

---

**miohtama** (2020-08-20):

Here are my 10 gweis - (also was the Github PR discussion)

I have built a dApp where the transaction tracking was a problem as well. While tracking transaction is a larger problem and probably will need a complete revisit in the future, I feel that this spec would address some shortcomings in dApp UX in the next 2-3 years.

Have a hook when a wallet uses to speed up or cancel transaction feature: The current spec look sufficient enough for this minor feature.

What can still break or is missing - loosely related to the functionality, but not to the spec itself

- The replacement transaction is a different smart contract call what dApp originally intended (possible, though not sure why anyone would do this, so maybe not even worthy of discussion)
- Tracking transactions with wallet specific ids instead of transaction hashes: e.g. the user interface can associate the transaction in the notification menu easily as the same transaction regardless of how many times speed up feature is used with ever changing transaction hash
- Requesting transaction speed up (gas top up) from the dApp user interface itself
- Having a developer friendly events transactioncomplete (for some specified statistical criteria) and transactionfailed (completed, but was rejected by revert) - this would especially boost productivity of newcomer developers of Ethereum world

---

**miohtama** (2020-08-20):

> My suggestion would be to replace tx_replacement with tx_cancel and tx_speedup

This is super simple and semantics are clear ![:100:](https://ethereum-magicians.org/images/emoji/twitter/100.png?v=12)

Would (address, nonce) tuple to be sufficient for dApps to track the transactions in this case? I know most of the apps now track by hash and then find hard way this is not immutable.

If we feel this is the case then web3.js tutorials such be rewritten using (address, nonce) as logical transaction identifiers and maybe even modify web3.js APIs to make supporting this easier.

---

**greg** (2020-08-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> My suggestion would be to replace  tx_replacement  with  tx_cancel  and  tx_speedup

Thanks for the feedback, I think this suggestion is huge. I also believe making them their own message type is probably the best way to move forward, instead of wrapping it into `.on('message', () => {})`

---

**greg** (2020-08-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/miohtama/48/2826_2.png) miohtama:

> The replacement transaction is a different smart contract call what dApp originally intended (possible, though not sure why anyone would do this, so maybe not even worthy of discussion)

I’m not sure if i follow, ultimately every on chain action requires an off-chain signing to occur. Thus if the speed/cancel occurs then all on-chain events would not take place. Perhaps I’m misunderstanding something?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/miohtama/48/2826_2.png) miohtama:

> Tracking transactions with wallet specific ids instead of transaction hashes: e.g. the user interface can associate the transaction in the notification menu easily as the same transaction regardless of how many times speed up feature is used with ever changing transaction hash

If I’m understanding this correctly, you’re describing a situation that arises when a user has “clicked” speedup or cancel a numerous amount of times, and now the dapp has no idea what has occured? If so, the nonce is your unique ID theres no need to bake extra logic into this. The dapp should be required to track the nonce and its not up to the provider to do much more.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/miohtama/48/2826_2.png) miohtama:

> Requesting transaction speed up (gas top up) from the dApp user interface itself

Hmm - this is novel, but I wonder if it adds bloat, a DAPP could self initialise this for the user without the provider needing to bake it in. Would love to hear feedback on this, I can see how this could make for better security though…

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/miohtama/48/2826_2.png) miohtama:

> Having a developer friendly events transactioncomplete (for some specified statistical criteria) and transactionfailed (completed, but was rejected by revert) - this would especially boost productivity of newcomer developers of Ethereum world

I think this is out of scope. I believe theres a few EIPs that exist for this, namely the STATUS_CODES EIP aimed to solve this. It should be up to the dapp or wallet to make user friendly error codes.

---

**greg** (2020-08-28):

I’ve made a [pr](https://github.com/ethereum/EIPs/pull/2916) to update the EIP - would love feedback ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**ldub** (2020-08-30):

[@pedrouid](/u/pedrouid) ‘s suggestion to isolate tx_speedup and tx_cancel is excellent and will help dapp devs a lot. However I believe a third tx_replacement message should still be implemented for transactions that are not speedups or cancellations. It’s true that MetaMask only lets users send speedups or cancellations but I think this EIP should cover other kinds of replacements that can be sent by other providers/wallets.

The list would look like:

`tx_cancel`

- same nonce
- equivalent from and to
- zero value
- no data

`tx_speedup`

- same nonce
- same to
- same value
- same data
- higher gasPrice

`tx_replacement`

- same nonce
- different to, value, data, or gasPrice

Also, [@greg](/u/greg), it appears that you’ve left some references to tx_replacement in the Rationale and Backwards Compatibility sections.

EDIT: To be clear, I propose that exactly one of tx_replacement, tx_speedup, and tx_cancellation should be fired for any replacement transaction. In the case of cancellation technically both tx_replacement and tx_cancellation apply but I don’t think it makes sense to fire both events.

---

**greg** (2020-08-31):

Hmmm, this is actually an interesting edge case. I think you’re right, replacement should exist since there is an option that the transaction itself was totally changed.

---

**greg** (2020-09-07):

I’ve update the EIP!

---

**wighawag** (2021-01-21):

Hey all, that’s a great idea!

I have some comment on the proposal but wanted to first mention about the current state of affairs.

I have read various discussions about this and noticed that there was no mention that it is actually relatively easy to detect that a tx was replaced, even today. I do it in my library : https://github.com/wighawag/web3w

You can even play with it on https://jolly-roger.eth.link/ (rinkeby)  where user can submit greetings:

Do as follow:

- Send a greeting message and get ready to cancel or speed up right away.
if the tx get replaced (once mined and final) a notification will come, mentioning it.

Then there are 3 cases :

1. if that was a “cancel” tx or a completely different tx, then nothing apart from the “replacement notification” will happen. (the spinning wheel for the pending new greeting will also disappear)
2. if it is a speedup tx, the notification will show up later, after the new greeting will show up, potentially confusing the user as it comes a bit later (as it wait for finality).
3. if the tx was a similar tx with different greeting, then the new greeting would have shown by then (as the UI is optimistic and do not wait for finality). In that case too, the resulting notification might confuse user as it comes a bit later (as it wait for finality)…

The way it detects is simply fetching the nonce at block height - finality ( ~12 on mainnet,)  and if that nonce is equal or higher than the tx being checked and that tx receipt is still null, then you know the tx was cancelled

This is I guess the best we can do right now and what is missing is being able to get the new tx once it is broadcasted so we can let the user know that a competing transaction is in progress too and what the new transaction will be performing (if it is cancelling or speeding up for example).

As such EIP-2831 proposal would be a great addition. I just though it was a good idea to mention what is possible today and what is missing.

**Few comment regarding the current proposal:**

While others have mentioned to break it up in separate message, I think to have a single “tx_replacement” is simpler and let apps deal with cancel, replacement or speedup themselves. Library can make it easier if they want. the data could simply be the rawTransaction or its params, like in `eth_sendTransaction`.

Also I would like to discuss the possibility of a different more generic proposal, that if I remember was advocated a while ago (can’t find reference): that of a `transaction` event for every transaction broadcasted triggered by the app (and so speedup and cancelation should be considered).

This would allow application to handle tx replacement themselves by simply looking a the nonce of new transaction and be more generic.

One question is whether the `oldTx` field is necessary in EIP-2831. I think it should not be as application can track transaction per nonce too. But we could definitely add an extra field when a transaction is actually replaced explicitly. This is not always the case as the tx could come from another wallet instance, not aware of the potentially multitude tx with same nonce.

Such event could also be used for transaction emitted through other app so your app can deal with replacement transaction with completely different data. Such event is also useful in general so apps can easily track transaction, even the one triggered by metamask itself.

