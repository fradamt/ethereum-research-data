---
source: magicians
topic_id: 4345
title: Using tx.origin to create an onlyNonContract modifier
author: ilanDoron
date: "2020-06-08"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/using-tx-origin-to-create-an-onlynoncontract-modifier/4345
views: 1212
likes: 7
posts_count: 7
---

# Using tx.origin to create an onlyNonContract modifier

tx.origin usage is discouraged in many places. But as of now, it seems like the best way to avoid receiving a transaction from a contract.

This article proposes tx.origin usage as best approach for certain scenarios such as non contract check:

https://consensys.github.io/smart-contract-best-practices/recommendations/#avoid-using-extcodesize-to-check-for-externally-owned-accounts

On the other hand it has been mentioned that tx.origin might be deprecated in the future: https://ethereum.stackexchange.com/questions/196/how-do-i-make-my-dapp-serenity-proof

So I have two questions:

1. Are there any plans to remove tx.origin?
And if anyone could point out a better way to create an onlyNonContract modifier.

Thanks in advance.

## Replies

**matt** (2020-06-08):

Out of curiosity, what scenarios would you want to determine if a call is coming from a contract?

To your question, I’m not aware of any concrete plans to modify the behavior of `tx.origin`. There was a brief conversation recently that if we add support for sponsored transactions, `tx.origin` could refer to the gas payer. But we would need to better understand how `tx.origin` is currently being used on the network first.

---

**Amxx** (2020-06-09):

Why in hell would you want to reject contracts interacting with you? IMO, EOA are just good for paying gas and signing messages. Identities/wallets are moving for EOA to SC and this is a good thing!

---

**3esmit** (2020-06-12):

You don’t have to use `tx.origin` to determine if the action is being done from a EOA, you can use `ecrecover` and ask a signature from `msg.sender`, because only EOA can be sign messages.

However, removing access from other smart contracts is not future proof, as there are many uses to account contracts that might want to interact. Also, if your contract is unsafe because of the use of smart contracts, it’s not safe at all, as creating a new EOA is really cheap.

Probably you are looking for a KYC or some sort of proof-of-individuality, you can research for this terms to better understand how you can handle the weakness of an open API.

---

**ilanDoron** (2020-06-15):

I am writing a function that is callable by any address.

The function will trade Eth to KNC and burn the KNC, this is part of Kyber’s new Katalyst version.

A number of safety measures were added to block manipulation options. For example the trade rate is compared to a third party price oracle. Also due to Kyber’s architecture, if a few reserves support ETH-KNC pair, price manipulation can’t be done by one reserve. Since best price for taker is always chosen.

But still, in order to try and block any attack we didn’t think of (like the ones shown in last flash loan show off) we find it safer if the function can’t be triggered from a contract.

I am aware that if it’s called from any non contract address it can still be attacked but an attack would be far less feasible and have fewer profit options for the attacker.

Adding to that, even if the use case isn’t clear, or anyone disagrees with the motivation, I still believe it might be a valuable feature to be able  to block calls from contracts.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/3esmit/48/2255_2.png) 3esmit:

> You don’t have to use tx.origin to determine if the action is being done from a EOA, you can use ecrecover and ask a signature from msg.sender , because only EOA can be sign messages.

Thanks. will look at this one.

---

**ilanDoron** (2020-06-15):

Yes

Its a great thing its moving to contracts. No argument there.

IMO keeping it flexible is always desired. No one can imagine the various use cases that will be found for smart contracts.

From my side, EOA isn’t the main point.

Main point is how to avoid attacks that are made very easy with automatic execution

like the flash loan attack we saw this year.

---

**Amxx** (2020-06-16):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/i/51bf81/48.png) ilanDoron:

> Main point is how to avoid attacks that are made very easy with automatic execution
> like the flash loan attack we saw this year.

If you can be attacked by a flash loan you can be attacked by a whale. Rather then forbidding the use of smart contracts, and turning down many users, you should just fix you contract logic to not be vulnerable.

I’ll give you a hint: don’t do arbitrary external calls (this includes sending ETH) unless your internal state is clean and the invariant are valid.

