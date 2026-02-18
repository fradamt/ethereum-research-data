---
source: ethresearch
topic_id: 2242
title: Fast exits for Plasma MVP using Optimistic Burn Proofs
author: kladkogex
date: "2018-06-14"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/fast-exits-for-plasma-mvp-using-optimistic-burn-proofs/2242
views: 1891
likes: 3
posts_count: 11
---

# Fast exits for Plasma MVP using Optimistic Burn Proofs

There was a discussion of burn proofs on Plasma MVP thread.

Essentially a burn proof means that the user burns an UTXO on the Plasma chain and submit a proof to the Plasma smart contract (PSC). Some people do not like burn proofs because of data availability concerns (the Plasma operator may withhold the proof).

How about making burn proofs optimistic? This means, that if a user burns an UTXO on the Plasma chain and provides a burn proof to the PSC the main chain, the user can exit immediately without having to wait.

If the user does not have a  burn proof the user can fall back on Plasma default mechanism for exits.

This seems to address the availability issue people raised regarding burn proofs.

## Replies

**danrobinson** (2018-06-14):

That would allow the operator to immediately steal all the assets on the Plasma chain, since they could create burn proofs with invalid history.

---

**kladkogex** (2018-06-14):

I am assuming that the burn proof is signed by the private key of the user (UTXO) that did the burn …

What you are saying is that Plasma operator could create an UTXO out of the thing air and burn it …

It should work for Plasma Cash though.

How is this addressed by Plasma MVP ? If Plasma operator creates an UTXO (or chain of UTXOs) out of thin air and exits it, how do other users even know something is bad ?  Other users are not supposed to monitor or store UTXOs that do not belong to them

---

**ldct** (2018-06-14):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> How is this addressed by Plasma MVP ? If Plasma operator creates an UTXO (or chain of UTXOs) out of thin air and exits it, how do other users even know something is bad ? Other users are not supposed to monitor or store UTXOs that do not belong to them

In Plasma MVP users are supposed to validate the entire chain, which includes UTXOs that don’t belong to them

> It should work for Plasma Cash though.

An attack for plasma cash would be for Alice to send coins to Bob, then a while later Alice double-spends her coin to Eve, and Eve burns and exits the double-spend

---

**sg** (2018-06-15):

I like this idea. Zilliqa and Thunder(Thunderrela) also has `slow-mode` construction when the chain is byzantine. I think security gradation is necessary for better usability.

When Plasma validator withholds a burning Tx, we may be able to know Tx withholding by timeout or something (*I need clarification). Then Plasma chain is regarded as byzantine state AND the process switches to exit scenario as fall back.

Because of this is byzantine fault, just in case we may need to deal with sudden burn proof incoming. Double withdrawal is big no-no.

---

**kladkogex** (2018-06-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> In Plasma MVP users are supposed to validate the entire chain, which includes UTXOs that don’t belong to them

[@ldct](/u/ldct), [@danrobinson](/u/danrobinson)  - this is imho the least documented part of Plasma MVP

In the example that [@danrobinson](/u/danrobinson) brought up,  a malicious Plasma operator creates an UTXO chain out of thin air and then exits it.

Note that the malicious UTXOs may be far far in the past.  Therefore, the only way for users to protect against malicious Plasma operators (as in the attack that [@danrobinson](/u/danrobinson) mentioned)  seem to be check all transactions in every block.

How realistic is that having the tragedy of commons - a particular user has little interest to do work that benefits community.

So it seems that every user has to have a copy of the entire chain. How is this going to work at all? ![:smiling_imp:](https://ethresear.ch/images/emoji/facebook_messenger/smiling_imp.png?v=12)

In other words, imho the sentence “users are supposed to validate the entire chain” needs to be expanded and mechanisms explained,  otherwise how can one prove security of this ? ![:smiling_imp:](https://ethresear.ch/images/emoji/facebook_messenger/smiling_imp.png?v=12)

May be one should state that Plasma MVP is incomplete and mechanisms are still being researched ?

---

**ldct** (2018-06-15):

The mechanism for validating the entire chain seems pretty straightforward - the user should run a client that does this (much like how Parity or geth validate the ethereum chain) and the client initiates exits when necessary. The security model is “if you sync your client once every 7 days and you pay for exits if necessary and you pay for cancelling fraudulent exits if necessary and if the main chain is not censored, then your money is safe”.

From an incentives point of view, however, I think you are right that there’s a validator’s-dilemma-like situation where the protocol-specified behaviour (operator doesn’t commit fraud, users validate once every 7 days) is not an equilibrium, since an individual user can save electricity and disk space by not validating and relying on others to “sound the alarm” in case of fraudulent operator or fraudulent exits.

Although, if we keep hardware requirements low enough, I don’t think this will end up being a problem, especially since the ethereum chain is also vulnerable to this. The hardware requirements for various TPS targets should be worked out. I think storage might become the most onerous, since users need to keep the entire TXO set around to cancel exits of spent TXOs, although XT-style checkpoints would mitigate this. Another thing that might help is a sharded validation architecture, i.e., block producer is still a single entity, but the TXO set and transactions are sharded so that a successful “money out of thin air” attack on one shard doesn’t affect other shards, and users just need to validate the shards that contain their money.

---

**danrobinson** (2018-06-15):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> How realistic is that having the tragedy of commons - a particular user has little interest to do work that benefits community.

As we’ve discussed before, you have to make a deposit for every attempted exit, and a challenger can receive that deposit by challenging your withdrawal. So there is an individual reward for challenging invalid withdrawals.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> So it seems that every user has to have a copy of the entire chain. How is this going to work at all?

*Any* user. As long as *someone* challenges invalid outputs, you are safe. And you don’t need the entire chain to do this, just the current state.

But yes, you as a user do need to constantly watch the chain (in particular I think you need to watch for unavailability, since nobody can challenge faults resulting from data unavailability). This is why I like Plasma Cash!

---

**kladkogex** (2018-06-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> The mechanism for validating the entire chain seems pretty straightforward - the user should run a client that does this

I am a bit pessimistic about this … a Plasma chain can potentially have thousands and millions times more transactions per second than the Ethereum main chain.  In addition to that,  Plasma users may have much smaller average transaction sizes.

If I have $10 stored on a Plasma chain which I am using for micropayments, why should I care to validate Plasma transactions of unrelated users.  Doesn’t this look like as a textbook example of “the tragedy of commons”.  I will probably not care at all, since Plasma operator is a good guy and since I only have $10 to lose.

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> Any user. As long as someone challenges invalid outputs, you are safe. And you don’t need the entire chain to do this, just the current state.

What about the spurious UTXO chain example that you brought up in the past?

Or about an example where Alice deposits $10, makes thousands of self-transfers over a year and then exits all of these UTXOs. It seems that in these examples one needs to keep long long history to catch the fraud.

If you say that essentially “someone will challenge but a typical user will not challenge”, wouldn’t you call the someone who challenges a de-factor validator.  But if you gonna have de-factor validators anyway, and the security will depend on this small number of pro-active users. why would not you explicitly call them validators and economically incentivize them? ))

If a Plasma chain will be 1000 times faster than a normal chain, why should one validate this thing for free out of altruistic reasons, if even in the existing main chain there is a problem where the guys who validate things are not paid anything? ![:smiling_imp:](https://ethresear.ch/images/emoji/facebook_messenger/smiling_imp.png?v=12)

So it seems to me that a statement like “Plasma without validators is not Plasma” is a bit naive. Who cares after all, if introducing validators can make things more secure ?))

---

**danrobinson** (2018-06-16):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> What about the spurious UTXO chain example that you brought up in the past?
> Or about an example where Alice deposits $10, makes thousands of self-transfers over a year and then exits all of these UTXOs. It seems that in these examples one needs to keep long long history to catch the fraud.

My bad, I think you’re probably right about this part. You can detect fraudulent exits using just the current state, but you need to have the history of the chain in order to construct the challenge.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> If you say that essentially “someone will challenge but a typical user will not challenge”, wouldn’t you call the someone who challenges a de-factor validator. But if you gonna have de-factor validators anyway, and the security will depend on this small number of pro-active users. why would not you explicitly call them validators and economically incentivize them? ))

Because an open set of validators, where anyone can join the validator set anonymously and with zero overhead, and security only depends on any one validator being online and active around the time of a fraud, and each of the validators is individually economically motivated to act, is better than a finite set of validators where some proportion of them needs to be honest.

But this is sort of moot because in MVP the operator can misbehave catastrophically by withholding data, and MVP does not provide a way to challenge or remedy that, other than mass exit.

---

**kladkogex** (2018-06-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> Because an open set of validators, where anyone can join the validator set anonymously and with zero overhead, and security only depends on any one validator being online and active around the time of a fraud, and each of the validators is individually economically motivated to act, is better than a finite set of validators where some proportion of them needs to be honest.

“and each of the validators is individually economically motivated to act”

I think economic incentives to validate Plasma operators is the part of Plasma which at the moment is undefined.

The problem is that a Plasma operator under normal conditions will be faithful, in fact any single fraud event on behalf of a Plasma operator will be catastrophic to its business.

How do you design economic incentives to catch one-in-a-hundred-years fraud event?)  This is a big question I think, one possibility would be to require the Plasma operator to include mock-up fraud transactions from time to time. But then you essentially get into designing a True-bit like protocol, which opens up a Pandora box …

