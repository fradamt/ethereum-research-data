---
source: ethresearch
topic_id: 5580
title: Minimal fully generalized S*ARK-based plasma
author: vbuterin
date: "2019-06-07"
category: zk-s[nt]arks
tags: [plasma]
url: https://ethresear.ch/t/minimal-fully-generalized-s-ark-based-plasma/5580
views: 4838
likes: 15
posts_count: 13
---

# Minimal fully generalized S*ARK-based plasma

Suppose that you have a Plasma chain that works by committing state roots to the main chain, along with a S*ARK (verified by the contract on the main chain that accepts the state roots) that proves that the state root is a valid state transition from the previous state root. That is, we have a state transition function STF which processes a block and a state and outputs a new state and a list of exits, and the contract on the main chain maintains a state root R, and if it receives a tuple (R', \Pi) where \Pi is a proof that there exists some block B, old state S, new state S' and list of exits E such that (i) STF(S, B) = (S', E), (ii) root(S) = R, (iii) root(S') = R'. If the proof passes, then the root is replaced by R' and for each exit in E the contract sends out the required amount of funds to the required recipient. This is essentially the architecture used by https://www.starkdex.io in its current form.

The problem with this architecture is that while an operator cannot steal funds, as only valid user exit operations can create an exit and those operations decrease the user’s balance in the state, the operator can still cause all funds in the system to be locked up forever by shutting down.

We solve this problem as follows. First of all, users chain publish requests to exit to the contract on the main chain. For a new state root to be accepted, the proof must in addition to the three claims above prove a fourth claim: the exit list E must include all exits published by users to the contract since the last root was published. Now, the child chain cannot progress at all without honoring users’ exits.

Second, we add a mechanism where if the child chain has not made progress within some period (eg. 1 week), another 1-week period begins during which any user can vouch that they know the full state represented by some historical state root of the child chain, along with a deposit. After this second period ends, we make a list of all historical state roots that have been vouched for, in most-recent-to-oldest order. We add another 1-week period during which **anyone can publish the full state corresponding to the most recent root to the chain that was vouched for**. If this full state is published, the chain processes exits from any user directly. If this state is not published for a week, the user that vouched for that state loses their deposit, and another 1-week period starts during which anyone can publish the full state corresponding to the *next most recent* state root, and so forth.

### Security argument

Suppose that you know a full state S for which the root has been successfully published to chain. If you want to exit the child chain at any point in the future, you can publish an exit request.

**Case 1**: the operator publishes a new root, which includes and successfully processes your exit (success).

**Case 2**: the operator never publishes any more roots. After a week, you vouch for S. After two weeks, either you can publish S or someone else publishes a state more recent than S (if someone else wins on vouching priority but fails to publish, eventually the queue will reach you), and at that point you can process your exit on chain (success).

## Replies

**Econymous** (2019-06-07):

[redacted]Is it necessary to push the state to mainchain? Can we just push assets up and down a child and parent chain (if the asset originates from at least /lowest parent chain)

Is this question too noob to be asking here?

I have a “token” based scaling solution and when I went into researching sidechains, they seem to have a lot more complexities than I originally thought.

When I read a week. I’m just thinking “holy ****”…[/redacted]

Ok. In the last few minutes I just got all the answers I need. I don’t need plasma. I need to fork a sidechain. I blurred the two

---

**josojo** (2019-06-07):

This kind of construction has been discussed here:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png)
    [Plasma snapp - fully verified plasma chain](https://ethresear.ch/t/plasma-snapp-fully-verified-plasma-chain/3391) [Plasma](/c/layer-2/plasma/7)



> Special thanks to the roll_up team for their hard work on building a first PoC for verifiable snapps (snark-dapps) and special thanks to Felix and Ben for their invaluable contribution to this idea.
> Plasma snapp:
> TL;DR
> The following specification outlines a new plasma version which utilizes snarks to prove its integrity and validity. Via an interlinking between exit requests and deposits with the correctness proof of a block - the snark -, we are able to specify an implementation without any ne…

The main issue with this construction is that clients need to come online and check the data availability. If they do not have data availability, the operator could withdraw funds from a state S_n and then roll back the chain to a state S_(n-k), where the operator has the withdrawn funds again in the side-chain. If the operator then also withdraws funds from S_(n-k), we get a “fractional reserve”.

Only if customers have data availability, they can stop the rollback. If they do not have data availability, they quickly need to request/enforce their deposit, in order to not be vulnerable for such an operator attack.

Still, even with this requirement of checking data availability regularly, it’s a great scaling solution.

---

**vbuterin** (2019-06-07):

Ah, I didn’t see that post; great to see that this has been thought about!

For checking data availability, I agree that this is an issue. There are two solutions:

1. 1-of-N trusted watchtowers
2. Data availability proofs as in https://arxiv.org/abs/1809.09044

I think either one could work.

---

**ldct** (2019-06-08):

Does this capture the design of something like “plasma cash + verified state transactions”, where the commitments are not state roots but transaction roots? It seems to me that this would make computing the proof independent of the list E (except when a user tries to spend and exit at the same time)

---

**vbuterin** (2019-06-09):

If you do it that way, how would you publish the full state to chain and authenticate it if the operator disappears?

---

**sina** (2019-06-09):

> “plasma cash + verified state transactions”

I’m very curious about this type of construction and have a post about it @[[0]](https://ethresear.ch/t/validity-proofs-plasma-cash-simpler-exit-game-coin-history/5333). Namely, taking the property of Plasma where people are responsible for their own data availability and using validity proofs to limit the amount of data (history) a user would need to keep around to secure their coins to `O(#coinslots)`.

From where I was at there’s some more thought needed in the direction of the worst-case exit procedure and ensuring a spend+exit of the same coin can’t happen in weird edge-case scenarios, but I like the idea in the OP of including on-chain exit proposals in the validity proof as a potential solution.

> If you do it that way, how would you publish the full state to chain and authenticate it if the operator disappears?

If the construction is like what I’m referencing, then users themselves are responsible for the data availability that proves ownership of their own funds. It ends up looking like the familiar Plasma Cash setup, where, users can attempt to exit coins and other users can challenge the exits within the challenge period. You can exit at your leisure, unless you need to challenge someone invalidly attempting to exit your coins.

Similar synchrony assumption to Plasma Cash variants-- that is, a user needs to sync once per challenge period to challenge any potentially invalid exits on their coins.

[0] [Validity Proofs + Plasma Cash = Simpler Exit Game/Coin History?](https://ethresear.ch/t/validity-proofs-plasma-cash-simpler-exit-game-coin-history/5333)

---

**ldct** (2019-06-10):

[@sina](/u/sina) is correct - my design would be that there is no operation to publish the full state to chain, and the response to “operator disappears” is inherited from plasma cash - withdraw from the most up-to-date transaction root.

---

**ldct** (2019-06-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/sina/48/11475_2.png) sina:

> I’m very curious about this type of construction and have a post about it @[0] . Namely, taking the property of Plasma where people are responsible for their own data availability and using validity proofs to limit the amount of data (history) a user would need to keep around to secure their coins to O(#coinslots) .

thanks! I definitely remeber reading about this design here but didn’t succeed in finding it ![:blush:](https://ethresear.ch/images/emoji/facebook_messenger/blush.png?v=12)

---

**ldct** (2019-06-11):

On further thought, the property that the prover is not interrupted by new exits can be achieved with state roots instead of transaction roots. The balance tree can simply contain coin ranges instead of balances (like in plasma cashflow), and the smart contract keeps track of which coin ranges are funded; the snark is not aware of that at all.

---

**sina** (2019-06-11):

> the smart contract keeps track of which coin ranges are funded; the snark is not aware of that at all

I think this makes sense. To receive a coin from Alice, Bob already has to ensure the signed inclusion proof from Alice is legitimate, so Bob has to sync with the main chain anyway. This is just an extra sync step before accepting the transaction as legitimate of checking that it’s still backed by something according to the contract.

So to make sure I’m understanding what you’re saying correctly: upon receiving a coin at index i via transaction t, Bob makes sure there are no pending or completed exits for coin i with timestamp occurring before t’s. Any exits after t’s timestamp can be challenged validly, and any before will validly exit due to not counting t as valid (since the exit was earlier).

Where the “timestamp” of a transaction is the timestamp of the block containing it.

---

**avihu28** (2019-07-04):

Nice construction! [@bbrandtom](/u/bbrandtom) and myself are also working on a plasma design for data availability along the same lines, but with more relaxed assumptions.

There is a problem with the OP solution even under the assumption that users regularly check and react instantly when data is not available. The problem is that a state transition with no data available can include withdrawals. So even if users track constantly for data availability, the operator can withdraw into an unpublished state, causing it to roll back and then withdraw the same funds again.

Let’s look at an example:

Suppose the state is now S1, with root R1, and data is available for it. The operator publishes a new root R2 for some state S2 without its data and includes some withdrawals W in the state transition as well as some trades T. Users immediately notice that data is unavailable and ask to withdraw. The operator does not respond and after some time those users roll back the state to S1. But in S1 the operator still has the funds he withdrew previously with W! So he can withdraw again from S1, causing the contract to be insolvent (with only fractional reserve) per the state S1.

S1      → (T+W)	S2		->rollback	S1

data-![:grinning_face:](https://ethresear.ch/images/emoji/facebook_messenger/grinning_face.png?v=14)		       data-![:cry:](https://ethresear.ch/images/emoji/facebook_messenger/cry.png?v=14)			data-![:grinning_face:](https://ethresear.ch/images/emoji/facebook_messenger/grinning_face.png?v=14) but contract missing W funds​:cry:

So even if users watch the chain constantly to ensure data availability, they won’t be able to prevent this from happening.

A possible solution:

Separate trades T and withdrawals W, such that every state transition can be either W-only or T-only. Now, because W’s data is always on chain, any state transition with W that follows a state for which data is available, is also guaranteed to have the data available. If a state transition is of type T-only, it can lead to a state without data but then no withdrawals will be included. This is why this kind of state can be rolled back safely, as no money has left the system since the latest state for which data was available.

Rerun the same example:

Option 1:

S1  → (T)		S2  		->rollback	S1

data-![:grinning_face:](https://ethresear.ch/images/emoji/facebook_messenger/grinning_face.png?v=14)		| data-![:cry:](https://ethresear.ch/images/emoji/facebook_messenger/cry.png?v=14)			| data-![:grinning_face:](https://ethresear.ch/images/emoji/facebook_messenger/grinning_face.png?v=14)

Option 2:

S1	 → (W)		S2

data-![:grinning_face:](https://ethresear.ch/images/emoji/facebook_messenger/grinning_face.png?v=14)		| data-![:grinning_face:](https://ethresear.ch/images/emoji/facebook_messenger/grinning_face.png?v=14)

---

**vbuterin** (2019-07-05):

Nice catch!

I don’t think that solution works. Because you can always do an unavailable T-only state transition followed by some withdrawals (from fresh accounts), and then the system would have to revert the unavailable state transition, it would not know the source of funds for the withdrawals, so the funds could be withdrawn again.

The simplest solution I can come up with would be bringing back a delay for withdrawals: if a block proposer makes a withdrawal for you at time T, you don’t get your funds until the block producer publishes a withdrawal message for *all withdrawal requests up until T + 1 week*. So if you see a withdrawal you don’t have data for, you would publish your own request, and either both would get satisfied or the system stops before then, in which case the mechanism chooses a state to publish and finalizes all withdrawals processed before that state but not any of the withdrawals after that state.

