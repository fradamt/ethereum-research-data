---
source: ethresearch
topic_id: 2621
title: Plasma vs. withholding & forgery combo attack
author: karalabe
date: "2018-07-20"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-vs-withholding-forgery-combo-attack/2621
views: 3239
likes: 8
posts_count: 12
---

# Plasma vs. withholding & forgery combo attack

Hey all,

First up, apologies if I’m missing something overly obvious about Plasma. I haven’t been following this line of research too closely, but based on spending a few days trying to design a plasma scheme that I myself cannot break (game theoretically from all participants’ perspective), I have yet to find a workable solution.

My personal grudge is against the mass exit mechanism. But a bit of a background info before I get into that. Plasma seems to be an elegant way to do arbitrary calculations off chain and just commit the root hash into mainnet. Specifically, I like the construction because in theory the plasma operator could be challenged if they construct an invalid state, and if they just drop dead, users can always exit the chain themselves.

But a much more interesting attack scenario from my perspective is if the plasma operator starts to withhold data, but nontheless keep pushing state updates onto mainnet. First up, without the witness data, the operator cannot be challenged that they produced an invalid state (the operator could grieve users with valid but hidden state). As such, by withholding data, the operator can forge arbitrary state roots, and we know noone will challenge it, so imho one valuable aspect of the plasma construction is lost.

At this point, your only option is the mass exit, where each participant tries to get out of the chain before the whole thing implodes. This is what i don’t think will realistically work. The first and most obvious issue is that **all** the participants need to bail out, otherwise the operator can run off with arbitrary funds (e.g. I can create a root hash with “says” I have N ether (or some UTXO) and submit a merkle proof stating so). I don’t think this is a realistic scenario in itself: there are people within Ethereum who still have not touched their presale wallets in 3 years. I don’t think it’s reasonable to think that all participants of a plasma chain will be able to exit within a time windows that’s small enough to remain actually usable. If not all participants manage to exit, the operator can just forge withdrawals at different amounts and cash out the amount that’s still covered by the inactive accounts.

A second issue imho is that if a plasma chain becomes popular enough (lets assume 10K tps), the operator can pile up a ton of transactions from various participants. Then when it starts withholding state and users start mass exiting, it can keep dripping these queued up transactions back into mainnet. The effect will be that the operator could block a withdrawal request at the last moment for any user who has pending transactions. Eventually the operator’s own fake/double-spent withdrawals could exit while it’s users are kept being griefed.

Am I perhaps missing something too obvious?

Thanks,

Peter

## Replies

**karl** (2018-07-20):

> your only option is the mass exit, where each participant tries to get out of the chain before the whole thing implodes

This is one of the reasons why I am a huge fan of Plasma Cash. In Plasma Cash we don’t have this huge mass exit vulnerability. If the Plasma operator wants to steal funds & submits an exit of a particular coin which has an invalid state transition in it’s history, through the challenge response process this invalid transition will be exposed and the exit canceled, forfeiting the exit bond. You can take a look at some pretty diagrams here: [Plasma Cash Simple Spec](https://karl.tech/plasma-cash-simple-spec/)

With Plasma Cash, as long as the valid history of a coin is known to someone watching the mainchain for invalid exits, there is no way to attempt to steal the coin without a bond being forfeited. Users can sleep safe and sound even if the operator goes completely off the rails! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**karalabe** (2018-07-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/karl/48/9_2.png) karl:

> With Plasma Cash, as long as the valid history of a coin is known to someone watching the mainchain for invalid exits, there is no way to attempt to steal the coin without a bond being forfeited.

Ah, but my point exactly. The plasma operator can forge an invalid state, and also withhold the witness data. Then nobody can actually prove there was an invalid transition.

---

**ldct** (2018-07-20):

In Plasma Cash, if the operator forges an invalid state and then tries to exit that, the way to cancel that is **not** to point to an invalid state transition; the way to cancel it is for the proper owner to challenge the exiter to prove that a valid state transition occurred from the point where the owner owned the coin. The fraudulent exiter cannot answer that challenge.

I think it is useful to point out that in my opinion at least, Plasma Cash does not really fit into the strict definition of plasma given in the original paper, hence some of the claims the paper makes do not apply to it, and this is one example of that.

---

**karl** (2018-07-20):

You can take a look [here](https://karl.tech/plasma-cash-simple-spec/) at the diagram under `Exit with an Invalid History Challenge` – notice the challenger never needs access to the invalid state transition.

---

**karalabe** (2018-07-20):

Ah, so you essentially assign a serial number to each “bill” and embed that in the UTXO, so the legitimate owner will be able to prove that they still have the money.

Ok, let me polish my attack vector: I withhold multiple blocks, but I keep the first one legitimate (i.e. it includes proper state transitions) and only forge the second. Then, I try to exit UTXOs that were legitimately spent in the first block, and I counterfeited them to myself in the second block. At this point two things happen:

- The original owner knows that they sent a transaction spending that. However they do know know if it was included or not. If they challenge me, I can reveal inclusion and they lost their challenge fees. This will prevent the original spender from challenging.
- The new owner does not yet know that they received the UTXO, because I withheld the legitimate witness data, so they themselves won’t challenge me either.

The only way to get caught in this case is for the original owner to challenge me, and if I prove a valid first transition, then for the subsequent owner to challenge me further. However, if I allow a single block to transfer the same bill multiple times, all but the last challenger will fail.

EDIT: Even better. The original sender won’t be able to challenge at all, because I may legitimately have received that bill through a number of valid transactions. The original recipient won’t know they “own” the UTXO yet.

---

**karl** (2018-07-20):

Good catch! This is the in flight transaction attack which is addressed with limbo exits that are outlined here: [Reliable Exits of Withheld In-flight Transactions ("Limbo Exits")](https://ethresear.ch/t/reliable-exits-of-withheld-in-flight-transactions-limbo-exits/1901) – and here’s another post worth taking a look at [Limbo Exits and Challenging Fraudulent Exits](https://ethresear.ch/t/limbo-exits-and-challenging-fraudulent-exits/2015)

---

**karalabe** (2018-07-20):

The limbo exit appears to require the sender and recipient to collaborate. What happens if the Plasma operator also controls the sender? They issue a spending transaction and also include it in a block, but withhold the witness. Then forge a block and try to exit in it. In this case, the sender won’t challenge and won’t collaborate either. The recipient has to solve it alone.

---

**ldct** (2018-07-20):

This is a tricky issue. I have some notes on how to deal with it that I’ll try to finish and post here. Some quick answers though:

1. You could do away with limbo exits as well as requiring exit bonds. The tradeoff is that past coin owners can grief current coin owners (but at a bounded griefing factor).
2. In the specific case where you are just sending one coin from a sender to the receiver, it is fine to require them to collaborate in case the chain is unavailable. Difficulties arise when considering multi-input transactions (e.g. a change provider).
3. The plasma cash variant described at Plasma Cash with smaller exit procedure, and a general approach to safety proofs might be able to support multi-input transactions with bonds as well as multi-input transactions, but I am not sure if the original plasma specification could do so.

---

**gakonst** (2018-07-22):

Scenario: Receiver has an item that will sell in exchange for some Plasma Cash coin. Receiver will not sell the item unless they see the transaction included in a block that is submitted to the Root Chain. Sender will send

1. Sender submits transaction to operator
2. Operator includes it, and submits the block root to the root chain.
3. Operator withholds the contents of the block, as a result Receiver never sees the transaction.
4. Sender exits (or waits until Operator stops withholding but I’ll ignore that here). 2 things can happen here:

Sender is colluding with Operator: Operator will not challenge, Sender exits the coin, but the block contents are still withheld, so Receiver never gave away the item, so nothing got stolen. (this is what you are referring to, when do you expect this to be a problem for Receiver?)
5. Sender is not colluding with Operator: Operator challenges with exitSpentCoin, which requires Operator to stop withholding and reveal the withheld transaction. Unfortunately, Sender loses the bond placed during the exit, but the transaction is revealed - this is where Limbo Exits come into play as @karl said, where we force settlement to Receiver onchain. As a result, Receiver knows the transaction was included and gives the good to Sender.

Does that make sense?

Doing more complex transactions which have more than 1-input 1-output may break the above scenario but I haven’t thought about that yet. I’m thinking that if we had a kind of atomic transaction for Plasma Cash which modifies N>1 coins in 1 step, griefing could be avoided as above.

---

**sourabhniyogi** (2018-07-22):

[@karl](/u/karl) Why did you make `(target_block?)` optional rather than required in the simple spec?  Making it required would limit the operator’s ability to withhold transactions and limit the amount of dripping, right?

---

**kladkogex** (2018-07-23):

imho the only realistic way to address security is require the exiter to submit a proof of burn .  Otherwise Plasma is insecure and unusable.  There is not a single Plasma spec yet that is free of security problems.  The entire thing seems to be an example of the new emperor cloth - everyone is enthusiastically implementing something that does not really exist.

I think Plasma is an example of a greater problem that Ethereum has. There has to be a formal process for developing specifications and there have to be independent commitees of experts deciding on things. This is the way Java and Linux are being developed.

One needs equal representation of negative and positive points of view, and not simply cheerleading all the time.  Ethereum needs to mature in order to it to survive long term.

