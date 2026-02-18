---
source: ethresearch
topic_id: 2198
title: "Plasma Debit: Arbitrary-denomination payments in Plasma Cash"
author: danrobinson
date: "2018-06-10"
category: Layer 2 > Plasma
tags: [new-extension]
url: https://ethresear.ch/t/plasma-debit-arbitrary-denomination-payments-in-plasma-cash/2198
views: 22731
likes: 36
posts_count: 45
---

# Plasma Debit: Arbitrary-denomination payments in Plasma Cash

This is a proposed extension to Plasma Cash, partially inspired by an [on-going](https://twitter.com/danrobinson/status/1000842275633729536) [Twitter](https://twitter.com/VitalikButerin/status/1000856690982510592) [discussion](https://twitter.com/VladZamfir/status/1004983493133250561) about the taxonomy of layer  2 scaling solutions and how they relate to each other, as well as discussions with [@kfichter](/u/kfichter), [@vbuterin](/u/vbuterin), [@jcp](/u/jcp), [@karl](/u/karl), and others.

## Mechanics

In Plasma Cash, the transaction Merkle tree is divided into slots, each of which stores a fixed denomination of ETH (the amount that was deposited) and tracks a public key. Each transaction in that slot updates the public key currently associated with that coin.

In Plasma Debit, each slot would track not only a public key, but a number *a* between 0 and *v*, where *v* is the total amount of ETH that was deposited into that account on the main chain. *v* does not change, but *a* can vary in each transaction, and represents the portion of the current coin that is owned by the owner. The remainder of the money deposited in that slot is owned by the operator. A transaction in which *a* is changed, like any other transaction, requires a signature from the current coinholder. (The operator does not need to sign the update, since their consent is implied by their inclusion of the transaction.)

When a coin is withdrawn, the coinholder receives *a*, and the operator receives *v* – *a*. (The exit rules need to be altered slightly to allow either the owner *or* the operator to exit a coin.)

When a coin is initially created, *a* is equal to *v*. The operator can increase *v* (and thus increase their balance held in the coin) by depositing additional ETH into that coin, using a separate `operatorTopUp` function on the parent chain’s contract.

This would allow users to pay arbitrarily small fees to the operator. (Vitalik proposed almost this exact solution to the fees problem [here](https://ethresear.ch/t/plasma-cash-plasma-with-much-less-per-user-data-checking/1298/31)).

Even more usefully, however, this allows any user on the Plasma Cash chain to pay any amount to any other user on the chain (as long as the recipient’s coin is undercapitalized by a sufficient amount). They can do this by creating an atomic transaction (i.e. a transaction that updates multiple coins and is only valid if it is included in both slots in the same block), where the sender’s account is debited by that amount, and the recipient’s account is credited by that amount.

For example, suppose Alice has an 8 ETH coin with a 4 ETH current balance, and Bob has a 5 ETH coin with a 3 ETH current balance. Alice would be able to send 1.3 ETH to Bob, by creating a transaction where the balance of her coin is reduced to 2.7, and the balance of Bob’s coin is increased to 4.3. The operator will accept and include the transaction (in both Alice’s and Bob’s slots) because it does not change the operator’s total balance (which remains, with respect to those two coins, at 6 ETH).

## Theory

The above explanation defined Plasma Debit as Plasma Cash with partial balances.

However, there’s an equivalent way of approaching this construction. Each Plasma Debit coin is essentially equivalent to a bidirectional payment channel (similar to the multisig-based payment channels used in the Lightning Network) between the current coin owner and the operator. The only difference is that the state of the payment channel is regularly notarized on the main chain (in a Merkle root with the operator’s other channels).

This notarization gives Plasma Debit coins two significant capabilities that payment channels do not have:

1. Assignability. A Plasma Debit coin can be transferred from one owner to another (the same way a Plasma Cash coin can). This is equivalent to allowing one of the participants in a payment channel to permanently assign their interest in that payment channel to some new party, which is not possible with previous payment channel constructions. Most significantly, this allows new parties to join the payment network without doing an on-chain transaction (which is a disadvantage of the Lightning Network).
2. Atomicity. Plasma Debit coins can be updated atomically with other coins on the same Plasma chain, without the need for HTLCs. (There are limbo-exit-like edge cases around data availability that make this slightly less of a win than it seems at first, but it is still potentially powerful.)

## Limitations

- To receive one of these kinds of transfers, the recipient must have (or receive) a coin that is undercapitalized by at least the amount of the transfer. This is similar to the constraints on Lightning Network channels, where the net balance between yourself and your counterparty is constrained by the balance that was initially deposited into your channel, and may require significant capital lockup (particularly on the part of the operator). However, the assignability of channels should make it easier to work around these limitations.
- This simple design only works for Plasma Cash chains with single operators. However, you could implement a more general form of this idea using merged and split coins, as described below, which would not be subject to this limitation.

## Extensions

- Updates to the balance would not actually need to be included in the Plasma blocks, since they require only the mutual consent of the coinholder and operator. The exit game could be altered relatively easily to allow the operator and current coinholder to instantly update their balance by exchanging signatures on a state update (which would then be almost exactly equivalent to a payment channel). The only transactions that need to be notarized (i.e. included in Plasma blocks) are those that either change the owner of the channel, or involve multiple coins.
- If coins can be split into arbitrary denominations and remerged with their siblings (as has been proposed, i.e., here), you could implement a more general version of this, where the “residual” amount of the coin could be owned by any party, not just the operator, and where any party could act as a liquidity provider for routing payments (by agreeing to remerge and resplit separate coins atomically). This is more complex may be more powerful, and might be necessary if the Plasma Cash chain has more than one operator.
- By increasing the expressiveness of the “scripting language” beyond just single public keys, we could adapt Plasma Debit to permit coins to act as more sophisticated state channels. Indeed, if we add support for hash locks and timeouts, Plasma Debit accounts could implement HTLCs, and thus have feature parity with Lightning Network channels. This would essentially allow a Plasma Cash chain operator to act as a Lightning hub, and interoperate with Lightning network participants (including participants on other cryptocurrencies), but with the added benefits of Plasma Cash (such as the ability to transfer ownership of a state channel from one user to another).
- It may be possible to implement transactions that are atomic across multiple Plasma chains (though this will need to be a subject for another post). If these are possible, then it would be possible to use Plasma Debit to make cross-Plasma-chain payments without HTLCs (as long as someone has an account on both chains and is willing to route the payment).

## Replies

**kfichter** (2018-06-10):

As a side note, I think this works particularly well for customer-merchant payments. The customer can deposit money into a single coin-account (or whatever), and the merchant can pay the operator some fee to lock funds into the operator-merchant channel. If the customer wants to quickly withdraw from the Plasma chain, they can lock funds up in the exact same way described in [Simple Fast Withdrawals](https://ethresear.ch/t/simple-fast-withdrawals/2128/29).

---

**sourabhniyogi** (2018-06-10):

Awesome innovations with the single operator assumption – it will make the plasma blocks, bloom filters, coin proofs a lot smaller with the new fungibility of Debit coins!

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> Updates to the balance would not actually need to be included in the Plasma blocks, since they require only the mutual consent of the coinholder and operator.

As usual, since the Plasma operator could be malicious, shouldn’t it *always* be necessary to include all balance changes to the Plasma Debit coin in the Plasma blocks?

For example, suppose Alice has an 8 ETH coin with a 8 ETH current balance, and Alice consumes 1 ETH worth of services of the Plasma operator but the Plasma operator maliciously claims 8 ETH of services were delivered.  We want Alice to be able to know that the outstanding balance is 7 ETH.

Exits would seem to require not “I want to withdraw my 8 ETH token, here is my Merkle proof of ownership with the last 2 txs” but “I want to withdraw my 8 ETH token, and my balance is 7 ETH, here is my proof of ownership with the last 2 txs *with the balance included*”  No?

---

**ameensol** (2018-06-10):

Doesn’t this increase finality time to the root chain blocktime?

---

**danrobinson** (2018-06-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/sourabhniyogi/48/808_2.png) sourabhniyogi:

> As usual, since the Plasma operator could be malicious, shouldn’t it always be necessary to include all balance changes to the Plasma Debit coin in the Plasma blocks?

No, because you could instead just have the operator and user both sign the new balance, along with an incrementing nonce representing which intermediate balance it was. When withdrawing, the most recent committed Plasma Debit coin would take priority, but after that, the most recent (i.e. highest-nonce) set of balances that was signed by both the operator and user would take priority. This is the same basic mechanism as state channels.

---

**danrobinson** (2018-06-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/ameensol/48/1455_2.png) ameensol:

> Doesn’t this increase finality time to the root chain blocktime?

I don’t think so… at least not relative to Plasma Cash. Why do you say that?

---

**ameensol** (2018-06-10):

Not relative to plasma cash, but relative to normal payment channels.

---

**sourabhniyogi** (2018-06-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> No, because you could instead just have the operator and user both sign the new balance, along with an incrementing nonce representing which intermediate balance it was. When withdrawing, the most recent committed Plasma Debit coin would take priority, but after that, the most recent (i.e. highest-nonce) set of balances that was signed by both the operator and user would take priority. This is the same basic mechanism as state channels.

Ok, with proofs extended with these joint signatures, how can some other entity that is receiving a partially spent Plasma Debit coin know that it is receiving the *highest nonce* joint signature between the coinholder and the Plasma operator?

Example:

1. Alice deposits 8ETH and gets a “v=8pETH, a=8pETH”  Plasma debit coin C with nonce 0.
2. Alice spends 1 pETH with Plasma operator.  Alice and Plasma operator jointly sign off on the balance “v=8pETH, a=7pETH” of C with nonce 1.   Unfortunately, no one knows about this.
3. Alice spends 6 additional pETH with Plasma operator.  Alice and Plasma operator jointly sign off on the balance “v=8pETH, a=1pETH” of C with nonce 2.
4. Alice and Plasma operator now collude against Bob in the following way:  Alice sends C in a token transfer to Bob, with the full history of C now containing just the joint signature of (1) at nonce 1 (malicious) rather than nonce 2.   Bob thinks he has 7pETH, but because he has zero visibility into the highest nonce of C, Bob is screwed.  When he withdraws his 7pETH, he finds out he can’t because Alice double spent!

It seems that to avoid Alice and Plasma operator colluding against Bob, you will still need these highest nonce+joint signatures included in the Plasma block’s Merkle Root hash (recorded on MainNet) for Bob to prove to himself that Alice and Plasma operator are being honest?

---

**danrobinson** (2018-06-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/ameensol/48/1455_2.png) ameensol:

> Not relative to plasma cash, but relative to normal payment channels.

Ah—nope, you don’t lose any latency relative to normal payment channels, because you can still update the balances instantaneously by mutual consent:

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> Updates to the balance would not actually need to be included in the Plasma blocks, since they require only the mutual consent of the coinholder and operator. The exit game could be altered relatively easily to allow the operator and current coinholder to instantly update their balance by exchanging signatures on a state update (which would then be almost exactly equivalent to a payment channel). The only transactions that need to be notarized (i.e. included in Plasma blocks) are those that either change the owner of the channel, or involve multiple coins.

---

**danrobinson** (2018-06-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/sourabhniyogi/48/808_2.png) sourabhniyogi:

> Ok, with proofs extended with these joint signatures, how can some other entity that is receiving a partially spent Plasma Debit coin know that it is receiving the highest nonce joint signature between the coinholder and the Plasma operator?

Nope, because notarized transactions (those included in the Plasma Cash chain) take strict precedence over the intermediate payment-channel-like transactions.

The transaction that transfers to Bob doesn’t have to mention or acknowledge any of the intermediate states between Alice and the operator, because those are all obsoleted as soon as the transfer to Bob is included on the Plasma Cash chain. The transfer to Bob *does* have to state what the balance of the coin is that Bob receives, though.

---

**sourabhniyogi** (2018-06-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> The transfer to Bob does have to state what the balance of the coin is that Bob receives, though.

Got it, cool – You are making the Plasma transaction from Alice to Bob require the last joint signature of the balance between Alice and Plasma operator.  So because *that* “close the Plasma debit coin” transaction is signed and included on MainNet, Bob can be satisfied that it knows the last balance.  If Alice sent Bob the balance of nonce 1 (7 pETH), then Plasma operator would not include that closing transaction in its Plasma block if it knows that it jointly signed on nonce 2 (1 pETH) – Makes sense, we’ll try it out further!

---

**MaxC** (2018-06-11):

Nice work, a lot more to think about.

---

**ldct** (2018-06-11):

It seems to me like building payment channels on top of plasma cash (which I think is you described in extensions) is strictly more powerful than plasma debit (without extensions). Do you see any downsides of payment channels compared to plasma debit?

One downside I see is that the plasma operator can censor transactions, forcing a routed payment to complete on ethereum, but that is a problem all L2 solutions will have. In sprites-style routed payments, this can be mitigated by placing the preimage manager on the root chain, allowing the timeouts (and hence the worst-case capital lockup costs) to be as short as non-plasmafied sprites channels.

> by agreeing to remerge and resplit separate coins atomically

There might be some ambiguity in language here, but for payment channels built on plasma cash, for routed transactions, in the optimistic case there should be no plasma transactions required; in terms of features that the plasma cash chain needs to support, it does not need any special atomicity support (beyond the already existing atomicity of individual transactions)

---

**danrobinson** (2018-06-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> It seems to me like building payment channels on top of plasma cash (which I think is you described in extensions) is strictly more powerful than plasma debit (without extensions). Do you see any downsides of payment channels compared to plasma debit?

I don’t think payment channels on top of Plasma Cash could give you the cross-coin atomic transactions (without HTLCs). So you’d basically be limited to making payments to (and receiving payments from) the operator.

Anyway, you’d have to adapt Plasma Cash to allow building payment channels on top of it. How would you do that?

---

**ldct** (2018-06-11):

Hmm I’m definitely thinking of something different then; let me try to write it down

---

**ldct** (2018-07-07):

So the way I was thinking of composing them doesn’t quite work, but the construction in [State Channels and Plasma Cash](https://ethresear.ch/t/state-channels-and-plasma-cash/1515) should be enough. It achieves the assignability and atomicity criterion with the same collateralization requirements, as well as all 4 extensions.

---

**eolszewski** (2018-08-07):

So, wouldn’t this mean that coin holders would need to keep track of more and more of the merkle tree to be able to prove their balance? Whereas previously they would need to account for just their slot(s), they now need to account for all the transactions that have affected that slot. If this continued for a long enough period of time without people closing out, I can see a world in which people would need to submit roughly the entire merkle tree in order to prove their balance and ownership.

---

**danrobinson** (2018-08-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/eolszewski/48/1902_2.png) eolszewski:

> So, wouldn’t this mean that coin holders would need to keep track of more and more of the merkle tree to be able to prove their balance? Whereas previously they would need to account for just their slot(s), they now need to account for all the transactions that have affected that slot. If this continued for a long enough period of time without people closing out, I can see a world in which people would need to submit roughly the entire merkle tree in order to prove their balance and ownership.

Nope. Counterintuitively, in Plasma Debit, when there’s an atomic transaction incrementing slot A and decrementing slot B, you need to validate almost nothing about one slot in order to validate the history of the other slot. (The exception is that if you are trying to validate slot A, then you need to check that the transaction was included in slot B in the same block. But that’s a negligible increase in overhead. (EDITED to correct and rephrase.)) The reasoning behind this is pretty involved, and I’m afraid I haven’t written it up yet, but I think it’s right. (EDITED: written up below.)

---

**eolszewski** (2018-08-08):

Re:

> So the way I was thinking of composing them doesn’t quite work, but the construction in State Channels and Plasma Cash should be enough. It achieves the assignability and atomicity criterion with the same collateralization requirements, as well as all 4 extensions.

You’re going to have to use hashlocks if you want to cover microtransactions or smaller transactions - I think ecrecover costs ~$10 to use on the main chain right now?

Sure, you could say that the cost could be greatly diminished on plasma, but i would prefer we stick to a standard across all chains ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**eolszewski** (2018-08-08):

Can you provide more detail, I’m failing to see how this works given that plasma cash won its scalability from the fact that it was non-fungible. How can this achieve the same property while being fungible?

---

**ldct** (2018-08-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/eolszewski/48/1902_2.png) eolszewski:

> You’re going to have to use hashlocks if you want to cover microtransactions or smaller transactions - I think ecrecover costs ~$10 to use on the main chain right now?

Paying through payment channels should always not incur ethereum gas fees “in the optimistic case”, since the payment involves just exchanging some messages. In that sense the cost of an ecrecover doesn’t affect the cost of paying through a payment channel. It does affect the kinds of griefing attack one can do through channels, so we would want to optimize it for that situation.

Unless you’re talking about hash locks in some other context?


*(24 more replies not shown)*
