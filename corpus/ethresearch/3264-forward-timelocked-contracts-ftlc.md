---
source: ethresearch
topic_id: 3264
title: Forward Timelocked Contracts (FTLC)
author: nginnever
date: "2018-09-07"
category: Layer 2 > State channels
tags: []
url: https://ethresear.ch/t/forward-timelocked-contracts-ftlc/3264
views: 3214
likes: 6
posts_count: 7
---

# Forward Timelocked Contracts (FTLC)

*Conditional off-chain Ether and Token payments for offline participants without on-chain checkpointing.*

FTLC is an alteration of the Hashed-Timelocked-Contracts (HTLC) deployed to the Lightning and Raiden network. FTLCs potentially enhance the user experience of “layer2” scalable cryptocurrency payments by allowing an online party to initiate and complete a payment to an offline party. In HTLC networks like Lightning, both the sender and recipient of a payment must be online to coordinate the off-chain payment. This is due to the way that the receiver of a HTLC payment must share the pre-image between intermediaries. FTLCs are inspired by Plasma-Debit where an operator is allowed to checkpoint the state of their “channels or merkle leaves” on the parent chain, however this construct attempts to achieve this with no need to checkpoint plasma blocks or data to the main chain.

FTLCs are called “forward-time locked” rather than “hashed-time locked” as with Lightning or Raiden. This implies that the payment initiator contract does not rely on a pre-image of a hash to move funds from initiator to hub, rather it relies on some proof that the hub updated their channel to reflect the payment before the initiators FTLC timeout.

**Ledger Channel:**

Assume a simple payment network with one intimidiary (Ingrid) containing { Alice (sender), Ingrid, Bob (receiver) }.

Between {Alice/Ingrid} and {Bob/Ingrid} we deploy a ledger channel that tracks normal bidirectional payment state updates and special single signed additive payment updates. The rules for re-entering this channel’s state to the main chain will vary from normal channels. There will be one type of transaction that will be allowed to build on the normal double signed ledger channels that increase the receivers balance. Since the consensus mechanism of normal channels is now broken for these types of state updates, the main chain contract must also verify that the deposit bond or receiving capacity is valid. This is similar to “Force-Move-Games” from Magmo. The contract may also attempt to punish incorrectly signed updates. Alice needs verify that the forwarded payment is valid off-chain and if it is not she must challenge to undo her payment to Ingrid.

**Forward Proof:**

The proof of forwarding that Ingrid creates comes in the form of the single signed state update on the receiving channel. In order to prevent double spending on Ingrid’s behalf, we require that an identifier be supplied by Alice and attach this to the state update from Ingrid. Ingrid_Sig({ID, Bob_Balance}). If an identifier is not supplied then Ingrid may use old payments as proof in challenges initiated by Alice to Bob. If an identifier is supplied then Alice’s challenge will need to be supplied the specific update for that FTLC that proves transfer and that the transaction was constructed properly (Ingrid had enough collateral).

**Basic Protocol:**

1 Alice signs channel update to Ingrid with a conditional FTLC. This state transition moves the conditional funds to Ingrid’s balance with a timestamp and TX_ID.

1(a) Igrid approves the conditions (checks that Bob has enough receiving capacity and that she is able to sign an update to complete the FTLC. Move on to step 2.

1(b) Ingrid rejects the FTLC and nothing happens. Either party may exit per normal state channels rules.

2 Alice waits as Ingrid is now responsible for completing the payment to Bob.

2(a) Ingrid generates a single signed state update with Bob with the same amount moving from Ingrid’s balance to Bob’s balance as was moved from Alice to Ingrid with the FTLC ID and incremented channel sequence. Moves to step 3.

2(b) Ingrid does not sign a state update to Bob within FTLC timeout, Alice must then go to chain and settle the latest state of their channel that reflects the active FTLC, then she may exit with state that nullifies the transaction after a second timeout to prove that nobody has evidence that Ingrid produced a valid forward proof for the FTLC.

3 Alice and Ingrid may settle the FTLC offchain.

3(a) Once Alice witnesses this state update, she may sign an update with Ingrid that nullifies the FTLC and leaves the balance transfer permanently on the channel.

3(b) Alice does not sign a channel update, then Ingrid may bring the state channel on-chain and prove the latest double signed state reflecting the FTLC, after which she may then prove her payment was forwarded by supplying to the contract the proof that Bob’s balance has irrevocably incremented in a single signed state channel. This needs to be done before the timeout or Ingrid will lose the transaction.

## Replies

**eolszewski** (2018-09-07):

This is reasonable, but I’m curious wrt the checking of the valid transaction between Ingrid and Bob that Alice’s is predicated on and if that is more efficient than the existing hashlock system where transactions are valid if submitted with a valid pre-image.

Also, in the case where Bob is offline, wouldn’t it make sense for Alice to just make an on-chain transaction to Bob instead of going through Ingrid? Sure, if all of Alice’s money is in the payment channel and she has nothing else to draw on in a regular wallet, then this is a no-go. I am curious if what you propose is more cost effective and if there are any numbers to go along with this.

---

**yahgwai** (2018-09-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/nginnever/48/1936_2.png) nginnever:

> 1(a) Igrid approves the conditions (checks that Bob has enough receiving capacity and that she is able to sign an update to complete the FTLC.

What happens if Ingrid does not have enough capacity, but approves the conditions anyway. Perhaps by signing an old state of her channel with Bob. In a two way channel Bob would not accept this, but without him online Alice can’t know this.

Could you make a settlement in the onchain contract between Alice/Ingrid dependent on a settlement (with the FTLC ID) in the onchain contract between Ingrid/Bob? This would mean that Ingrid wouldn’t be able to use her funds - either to send back to Alice, or to retrieve them on chain - before either a settlement with the correct FTLC ID in the Ingrid/Bob channel had been committed onchain, or the FTLC ID is signed by bob and distributed to Alice.

---

**nginnever** (2018-09-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/yahgwai/48/759_2.png) yahgwai:

> What happens if Ingrid does not have enough capacity, but approves the conditions anyway.

Good question. I have been thinking about this for a few days now. In plasma, the intermediary of payments would commit on-chain to the tx. This way the hub/intermediary could be directly challenged if it is found to be miss-behaving. If, for example, Ingrid signed an update to her channel with Bob that lied about the receiving capacity she had with Bob in an attempt to steal the FTLC from Alice, it could be caught and challenged by Alice by exiting with the last known good state before the provably incorrect update happened.

Recently the plasma cash/debit research has proposed

> “the most flexible thing to do is to have signatures list their dependencies, rather than transactions. so a particular signature on a transaction can say it is only valid if proof of inclusion/validity of these additional transactions is also provided.”

I think what we are proposing here is, rather than forcing the hub to commit roots of every atomic swap, we could structure the parent ledger channel to exit in a way that checks to be sure the on-chain forward happens (as you suggest) only when the receiver does not come back online before the initiator wants to exit. This could add some flexibility to the plasma cash/debit design and offer some cost reduction in the amount of data that needs to be checkpointed on the parent chain.

Off-chain FTLC settlement is possible when the receivers of FTLCs come back online to check that Ingrid actually has the correct signatures committing the receiving capacity of Bob’s FTLC txs. Once verified, the receivers of FTLC may sign LC updates with the online hub to settle the tx. Alice may be notified of this signature from Bob the next time she is online, and then she can confidently sign an LC update that nullifies the proven open FTLC.

Exiting LC state to parent chain:

Type 1. There are no open FTLC on the LC, the exit is immediate as the LC contains a latest state with unanimous consent on the channel balances.

Type 2. There are open FTLC transactions on the LC. The exit is not immediate as Alice isn’t yet sure that the recipients of the open FTLC have actually received valid channel updates (Alice isn’t sure if Bob’s offline channel has the receiving capacity claimed by the hub, or that the hub won’t pull their on-chain liquidity before the receiver tries to exit).

Exiting 1 happens per normal state channel exits. Exiting 2 is where the conditional FTLC payment comes in. 2 exits will only complete FTLC txs if on-chain proof of the forward is supplied by the hub. We would consider an on-chain LC settlement with open FTLC txs inside of it a sort of challenge initiated by Alice that the hub could later invalidate by proving on-chain completion of the FTLC.

However it can’t be exactly considered a challenge since there is the possibility the Bob never comes back online to confirm the FTLC. In the case the receiver of FTLC txs does not come online before the senders of the tx wants to exit to the parent chain, it becomes non-ideal to have to create an on-chain tx to complete the transactions. We could perhaps fall back on plasma cash/debit and allow the hub to commit to a merkle root of batch commitments that would allow for multiple FTLC txs to be completed globally across channels. The hub could wait X amount of time for on-chain LC exits that contain FTLC txs to aggregate to reduce costs.

Still putting thought into this.

EDIT:

I think an important thing to clarify in my post here and what [@yahgwai](/u/yahgwai) is mentioning is that the incentive is on the hub to sign updates with recipients of FTLC txs where they don’t actually have a signed commitment with the receiver to cover the transaction. This is problematic since Alice may not have the data of the Ingrid/Bob channel since Bob is offline and Ingrid may lie to Alice and present an old state update that appears to have the required locked capital. It may just be simpler to require all LC exits that have “incomplete” FTLC txs in them require an on-chain commitment from the hub. Where “incomplete” means the receiver of an FTLC hasn’t come online to confirm the tx.

---

**yahgwai** (2018-09-22):

Cool. I have a couple more questions/thoughts to cast your way: what happens in the case of multiple intermediaries Alice|Ingrid|Ignatius|Bob, and what if the same id is, perhaps unintentionally, chosen for two FTLC transactions?

For multiple intermediaries I assume the process is pretty much the same, except that what is required is to unlock funds is not proof that the transfer has been forwarded, but rather that Bob has received it. Achieved by Bob’s signature over a hash of the id, which would unlock all intermediary transfers.

The same id/recipient pair should never be chosen - just as in the hashlock case - as an intermediary would be able to replay a signature.

None of this appears be payment specific, it seem that this could also be used in a state channel networks?

![](https://ethresear.ch/user_avatar/ethresear.ch/nginnever/48/1936_2.png) nginnever:

> allowing an online party to initiate and complete a payment to an offline party

And should “complete” be removed here, since completion can only occur once the recipient has come back online?

---

**nginnever** (2018-09-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/yahgwai/48/759_2.png) yahgwai:

> For multiple intermediaries I assume the process is pretty much the same, except that what is required is to unlock funds is not proof that the transfer has been forwarded, but rather that Bob has received it. Achieved by Bob’s signature over a hash of the id, which would unlock all intermediary transfers.

Ideally proof of transfer forwarded = Bob may receive it eventually. If Bob or the final recipient is required to sign to create the unlocking proof, then we could just a virtual channel system closer to the Perun construct. I think if we can get the unlock proof to verifiably contain evidence that there is capacity then we can get this to work with some sort of on-chain commitment. In a network this should only be necessary on the last hop to receiver as all other hops are online and can negotiate to be sure they have channel capacity to cover the forwards in real time. The forward proof supplied by the last hop could be the global unlock for all of the forwards, similar to how Sprites works for HTLC.

![](https://ethresear.ch/user_avatar/ethresear.ch/yahgwai/48/759_2.png) yahgwai:

> The same id/recipient pair should never be chosen - just as in the hashlock case - as an intermediary would be able to replay a signature.

Yup! As you mention this is a pretty standard requirement in state channels.

![](https://ethresear.ch/user_avatar/ethresear.ch/yahgwai/48/759_2.png) yahgwai:

> And should “complete” be removed here, since completion can only occur once the recipient has come back online?

I don’t think so. “incomplete” just means the hub had to make an attestation to their capacity on-chain that can be challenged. I want to say that we can develop a compact proof that the forwarder has a valid channel with the recipient and they are building a single direction payment state on top of that. But in reality this may always require a verification game that can disprove claims of latest state. Either way the receiver could potentially stay offline for all of this I believe.

---

**Hither1** (2019-01-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/nginnever/48/1936_2.png) nginnever:

> “forward-time locked”

Hi. Could you pls explain a bit what is “forward-time locked”?

