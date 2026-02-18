---
source: ethresearch
topic_id: 1596
title: Copying plasma chain output sets from one chain into another plasma chain
author: josojo
date: "2018-04-02"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/copying-plasma-chain-output-sets-from-one-chain-into-another-plasma-chain/1596
views: 2249
likes: 2
posts_count: 6
---

# Copying plasma chain output sets from one chain into another plasma chain

Hi,

in this thread, I would like to discuss the possibility to copy utx-outputs from one plasma chain into another plasma chain.

In order to describe the technique I have in mind, I would like to talk about 3 processes:

1. How a user could withdraw all his utx-outputs from a plasma chain with one request to the root-chain.
2. How several users could copy all their utxos from one plasma chain into another one.
3. How we could allow ‘trusted Exiters’ to copy our outputs from one plasma chain to another very conveniently.

**How a user could withdraw all his utx-outputs from a plasma chain with one request to the root-chain.**

If a user detects a data unavailability or some false behavior from the chain operator, the plasma contract on the root-chain could allow him to formulate him a trueBit challenge game like this:

" If I review all my unspent, valid utxos from the plasma chain and add them up, then I get X ether and if I sort them alphabetically, put them into a Merkle tree, then I get the hash H1 and the lowest priority from all outputs is P". The plasma contract on the root chain would require the person putting up this trueBit-game to send a bond along, which could be used to reward a successful challenger. Once this withdraws request is put into the root chain anyone can inspect the plasma chain for all unspent utxos of this particular user [UTXO_1, UTXO_2, … UTXO_N], sort them alphabetically, hash them together, calculate their sum and check their lowest priority. If their hash is not H1, P is no correct or the sum is not X, everyone can challenge them:

- If the hash is not H1, one would ask for the hashes of the Merkle trees made of: [UTXO_1, UTXO_2, … UTXO_N/2] and [UTXO_N/2+1, UTXO_N/2+2, … UTXO_N]. One of them would not be correct and one could challenge them again. This proceeds until the disagreement between the challenger and the withdraw requesters is about one particular [UTXO_K]. Now the challenger would have to prove that this particular [UTXO_K] either, has already been spent, does not exist in the root chain or that there is actually another output, which should be the Kth output. All these things could be proven on the root chain.
- If the sum is not X, one would ask for the sums of the outputs of: [UTXO_1, UTXO_2, … UTXO_N/2] and [UTXO_N/2+1, UTXO_N/2+2, … UTXO_N]. One of them would not be correct and one could challenge them again. This proceeds until the disagreement between the challenger and the withdraw requesters is about one particular [UTXO_K]. Now, this output can be processed on the root chain and it could be checked whether it really has the claimed size or not.
-If P is not correct, one could just hand in an unspent output with a worse priority.

The trueBit-withdraw request would be processed with the priority P if it is not challenged. Users should not include any outputs, which they have signed once and are included in the plasma chain, but are not signed twice into the withdraw request, in order to keep things simpler.

**How several users could copy all their utxos from one plasma chain into another one.**

Method 1 would allow one user to withdraw all their funds into another contract by putting up this trueBit-withdraw request. Now several users could come together and put up the following trueBit-withdraw request:

" If we -the accounts [A1, A2, … A_M] - review all unspent, valid utxos from the plasma chain and add them up, then we get X ether and if we order these alphabetically, put them into a Merkle tree, then we get the hash H1 and the lowest priority from all outputs is P; this message is signed by A1, A2, …, A_M".  If the request is not challenged, the plasma contract PC1 on the root chain could deposit the X Ether to another plasma chain PC2 contract. Now if an account A_i wants to withdraw one of his utxo’s [UTXO_A_ui] on the 2nd plasma chain, he would post the withdraw request to the PC2 contract with a proof that [UTXO_A_ui] is legit output in the other plasma chain PC1. PC2 would now validate this claim by validating this request exactly as a withdraw request would have been validated by PC1. Also the withdraw request can be challenged by proving that this output was already spent either in plasma chain 1 or plasma chain 2.

But of course, the utxos from the first plasma chain could also be spent on the plasma chain 2 first and then only be withdrawn later.

Using this technique, we can copy many utxo’s from one plasma chain into another one, without losing any information. This would be of tremendous help in case of a mass exit, as only many outputs can be processed without actually touching the root chain.

**How we could allow ‘trusted Exiters’ to copy our outputs from one plasma chain to another very conveniently.**

The technique described in 2 can be used to make mass exits from one plasma chain into another one quite convenient. A user U1 on the plasma chain could approve a “trusted Exiter” TE on the plasma chain to exit their funds in case of a data-unavailability into another predefined plasma chain. Once a trusted Exiter is approved, all funds transferred on the plasma chain from U1 are only valid, if TE signs them 2 times as well. This is needed so that a user hiding a transaction from the TE, cannot destroy the exit-request from the TE. The TE will sign all transactions of his clients immediately, once he sees them. If he does not sign them, then the TE can be unapproved by the plasma chain user.

In case of a data-availability the trusted Exiter would put up trueBit-withdraw request:

" If we review all unspent, valid utxos from the plasma chain of accounts that approved me to withdraw their funds and add them up, then we get X ether and if we sort these alphabetically, put them into a Merkle tree, then we get the hash H1 and the priority P for withdraw should be: max(priority of unspent output, priority of last spent output, which was signed two times). If this request cannot be challenged, the X ether will be sent to the predefined plasma contract PC2".

If the withdraw request is made correctly, all outputs of all accounts which approved the trusted Exiter will be sent to the new plasma chain with plasma root contract PC2. The trusted Exiter can not steal there any coins, he just transferred them into the predefined contract P2. The only trust he is getting is that he does not cause inconvenience by transferring funds into other chains although there is no data-unavailability.

Note1: the trusted Exiter would actually need to put a 2 step withdraw request:

1. First, we would put up a note that he wants to withdraw all outputs associated with his address.
2. Secondly, after 1 week when everyone revealed their withdraws request in the priority queue, he or other people can actually put the sum of outputs, hash of outputs and withdraws priorities up for a trueBit-challenge. This updating of the withdraw request needs to happen since people might wanna withdraw their outputs individually and thereby impacting the outputs of the withdraw.

Also, this would allow one user to have several trusted Exiter and then only the trusted Exiter with the highest priority would actually do the withdraws. I think the concept of a trusted exiter is very powerful since it allows copying whole output sets into another plasma chain. If there are several Plasma chains each operator could also run a trusted Exiter in the other chains and if data availability occurs in another chain, he would be able to withdraw user funds from the one plasma chain into their own plasma chain and thereby winning new customers.

Something similar could be also constructed for plasma cash.

## Replies

**MaxC** (2018-04-03):

Very interesting idea.

I think that the truebit style checking requires data available for verifiers to check. So truebit is more what you can do when data is available rather than a solution to availability.

Suppose the plasma chain is unavailable to all users except the malicious operator and then one of the users attempts to exit with a double spend. No one else will check the user because they don’t know whether the exit is valid or not, as data is unavailable.

If you could apply data availaibility proofs to blocks it could work.

---

**josojo** (2018-04-03):

Yes, you are right, we need data availability. But still it works:

If the data is available all false trueBit withdraw requests can easily be challenged.

If data is unavailable from some block n, then trueBits withdraw requests that reference only data before the block n will be challengable. And they would have a higher withdraw priority as any trueBit withdraw requests that references to data after the block n, which might not be challengable. Hence invalid request would only be processed if everyone else would have already withdrawn their funds. In this aspect, it has the same defense mechanisms as the usual Plasma chain.

Very cool to see you being interested in this solution concept.

---

**MaxC** (2018-04-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> " If I review all my unspent, valid utxos from the plasma chain and add them up, then I get X ether and if I sort them alphabetically, put them into a Merkle tree, then I get the hash H1 and the lowest priority from all outputs is P". The plasma contract on the root chain would require the person putting up this trueBit-game to send a bond along, which could be used to reward a successful challenger. Once this withdraws request is put into the root chain anyone can inspect the plasma chain for all unspent utxos of this particular user [UTXO_1, UTXO_2, … UTXO_N], sort them alphabetically, hash them together, calculate their sum and check their lowest priority. If their hash is not H1, P is no correct or the sum is not X, everyone can challenge them:

Beautiful solution. Have you given thought to state based  rather than utxo based models?

---

**danrobinson** (2018-04-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> Something similar could be also constructed for plasma cash.

To the extent any of these solutions involve any challenger being able to “inspect the Plasma chain”, I think they won’t, because Plasma Cash is designed so that users don’t have to (and probably won’t be allowed to) see the entire Plasma chain; they’re only shown their own outputs and the data necessary to prove the validity of those outputs.

But yes, I do think there is a way to do transfers from one Plasma Cash chain to another without touching the parent chain: [PoS Plasma Cash with Sharded Validation - #6 by danrobinson](https://ethresear.ch/t/pos-plasma-cash-with-sharded-validation/1486/6).

---

**josojo** (2018-04-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> Beautiful solution. Have you given thought to state based  rather than utxo based models?

No. I think state-based solutions are even much more complex. First, we need to master utxo models. Also storing states might not always be so powerful because many meaningful states are not suited for a plasma chain. People should be able to leave the plasma chain at any time, but states are usually not “leaveable” at any time. But for sure it would be very interesting.

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> But yes, I do think there is a way to do transfers from one Plasma Cash chain to another without touching the parent chain: PoS Plasma Cash with Sharded Validation.

Your post is very interesting. It highlights how powerful plasma cash might be. Pretty cool.

But it seems like there is a small hook. Because users want these inter plasma transactions especially once one plasma chain operator is no longer working correctly(i.e. produces unavailable blocks.) But then these inter plasma chain transactions can no longer be included and one would have to leave the plasma chain via a root chain transactions.

But how about this:

We could approve a coinId to be transferred by plasma chain1, plasma chain2, … plasma chain n. Once these n plasma chains are approved, the token transfer could happen on any of these chains. Hence all chains would be required to have kind of the same protocol. For accepting a plasma cash payment, one would need proofs that the coin was not spent in any of the approved chains, etc. But once one operator is offline, malicious or whatever, we can just keep on spending the coin in the other plasma chains. We only would have to specify on another chain via a transaction that the unavailable chain is no longer allowed to accept payments with this coinId.

