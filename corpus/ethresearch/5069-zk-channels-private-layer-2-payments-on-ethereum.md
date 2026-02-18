---
source: ethresearch
topic_id: 5069
title: "Zk-channels: Private layer 2 payments on Ethereum"
author: chris.whinfrey
date: "2019-02-27"
category: Layer 2 > State channels
tags: []
url: https://ethresear.ch/t/zk-channels-private-layer-2-payments-on-ethereum/5069
views: 5546
likes: 17
posts_count: 9
---

# Zk-channels: Private layer 2 payments on Ethereum

# zk-channels

Private layer 2 payments on Ethereum

*Inspired by the ETHSignapore hackathon project [zkDAI](https://github.com/atvanguard/ethsingapore-zk-dai) which was inspired by the [Zerocash paper](http://zerocash-project.org/paper).*

## Abstract

Private payments on Ethereum have struggled to gain traction due to their relatively high transaction cost. Combining the scalability of payment channels with the privacy provided by zk-snarks can enable a cost-effective and private payment network on Ethereum.

## Description

zk-channels function by using “notes” tracked in an Ethereum smart contract. Each note has a private owner and value and is represented by a hash. There are two types of notes: `Note`, and `ChannelNote`. A `Note` is represented by the hash of the owner, the value, and a salt. A `ChannelNote` is represented by the hash of the owner, the value, the channel recipient, and a salt.

`Note`s function much like UTXOs. A new `Note` can be created by depositing the collateral token into the contract. `Note`s can then be privately transferred by proving ownership. When a `Note` is transferred, two new `Note`s are created, one owned by the receiver, one owned by the sender with the remaining value. At any time, a `Note` can also be redeemed for the underlying collateral token.

`Note`s can also be used to open a payment channel by converting it into a `ChannelNote`. `ChannelNote`s can be spent using a signed message from the owner. `ChannelNote` owners can also force the receiver to withdraw within a given period in order to unlock the `ChannelNote`'s remaining value.

A payment channel is created by the spender by first creating a `ChannelNote` and then sending signed messages of increasing value to the receiver. Only the receiver can close the channel allowing them to use the last and highest value signed message. If the sender wishes to withdraw the remaining value in a `ChannelNote`, they can force a withdrawal by kicking off a withdrawal period during which the receiver must withdraw or forfeit their payment.

## Note - (owner, value, salt)

Represented by the hash of `(owner, value, salt)`

### Actions

- createNote() - Collects deposit and creates a Note of equal value.
- transferNote() - Validates proof, marks the Note as spent and creates two new Notes
- depositNote() - Validates proof (snark not described), marks the Note as spent and creates a ChannelNote
- redeemNote() - Marks Note as spent and transfers the deposit to owner

### transferNote() zk-snark description

- Public inputs:  originalNote, noteA, noteB
- Private inputs: sender, value, salt, receiver, valueA, saltA, valueB, saltB, senderPrivateKey
- Verifies:

originalNote is the hash of (sender, value, salt)
- noteA is the hash of (sender, valueA, saltA)
- noteB is the hash of (receiver, valueB, saltB)
- valueA + valueB = value
- senderPrivateKey is the private key of sender

## ChannelNote - (owner, value, receiver, salt)

Represented by the hash of `(owner, value, receiver, salt)`

### Actions

- closeChannel() - Validates proof, marks the ChannelNote as spent, and creates two new Notes
- forceWithdrawal() - Validates proof (snark not described), kicks off a withdrawal period during which the receiver must withdraw. If no withdrawal is made, sender can spend the ChannelNote for a single Note with equal value.

### closeChannel() zk-snark description

- Public inputs:  originalNote, noteA, noteB
- Private inputs: sender, value, salt, receiver, valueA, saltA, valueB, saltB, signature, receiverPrivateKey
- Verifies:

sender is the signer recovered from signature with the message (sender, value, receiver, salt, valueB)
- originalNote is the hash of (sender, value, receiver, salt)
- noteA is the hash of (sender, valueA, saltA)
- noteB is the hash of (receiver, valueB, saltB)
- valueA + valueB = value
- receiverPrivateKey is the private key of receiver

## Replies

**lebed2045** (2019-02-27):

the concept sounds cool. What’s the total gas fee for this 4 operations:

- createNote()
- transferNote()
- depositNote()
- redeemNote()
?

---

**chris.whinfrey** (2019-02-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/lebed2045/48/2342_2.png) lebed2045:

> What’s the total gas fee for this 4 operations:

I haven’t started an implementation yet so I’m not sure. I believe the signature recovery could be implemented relatively efficiently using [@barryWhiteHat](/u/barrywhitehat)’s [baby jubjub](https://github.com/barryWhiteHat/baby_jubjub_ecc) curve.

Would be curious to hear what other people’s experiences have been with gas costs when dealing with zk-snarks on Ethereum. I will report back if I can get a proof of concept together too.

---

**barryWhiteHat** (2019-02-28):

One thing I would encorage you to do is to store the notes in a merkle tree. And use nullifiers to invalidate leafs. This helps us with privacy because we don’t need to reveal `noteA` `noteB` in `transferNote` and a bunch of others. This will mean you cannot link the input note to the output which really helps. See https://www.youtube.com/watch?v=84Vbj7-i9CI for a better description of this technique.

The gas costs will be ~ 500k gas per snark validation.

---

**technocrypto** (2019-02-28):

I love zero knowledge stuff for channels!  I would actually go one step further than Barry mentions and think about just using a general zero knowledge method *within* a channel, instead of this very specific one to *create* the channel.  We have discussed zero knowledge stuff for channels extensively at L4, and a good place to start seems to be to first identify which properties you want to make zero knowledge, and then to find as general a way as possible to provide that functionality, because zero knowledge schemes benefit from having as many people using the same mechanism as possible, rather than just users of your application, or just users of channels, etc. (because it increases the total anonymity set, improving the actual privacy you get out of the scheme).  Here are some properties one might want to make private in a simple channel:

1. To have identities of the channel members be private from the public (already effectively provided by using new keys to create channels)
2. To have identities of the channel members be private from each other (partially provided by using new keys to create channels, but not possible to keep the association between multiple payments private from the counterparty of a simple two party channel not part of a network. With more than two parties key cycling in between payments can again provide this property without any zero knowledge construction, though with an anonymity set limited to the number of total channel participants, like a small mixer.)
3. To have amounts transacted in channels be private from the public (already effectively provided by the normal architecture of two-party channels not part of a network)
4. To have deposits and withdrawals to a channel not associated with any later or previous on-chain transaction activity (can be easily provided by simply redirecting state channel deposits and withdrawals through an onchain, zero knowledge transfers contract).
5. To have channel disputes not identify which party in the channel owns which funds, or which party plays which role in the dispute (can be easily provided by key cycling between operations).
6. To not have channel disputes associated with a specific channel (can be provided in a very generic way by a zero knowledge “cross reference” table, where a public key-value store is accessible by any contract or user, each the only one with permission to set their own values, and a parallel key-value store uses private commitments which reference the public store as keys, and shows public values for a key only if a zero knowlege proof is submitted showing that a supplied value is correct. With careful design the anonymity set for each entry can be the total number of entries in the parallel, public key-value store. With such a scheme only one bit is required per channel withdrawal, to check if the state referenced was later revoked. An optional second bit can mark state as final for instant withdrawals).

There are more things one could aim for, of course, but I think the above list captures most of the goals for your own design, correct?  Of course, when one considers channel *networks* like Raiden or the Lightning Network there are many additional properties one might consider making private:

1. Keeping the full channel path private from any intermediaries along the path (possible via the onion routing technique)
2. Keeping private which of multiple channels (including multi-party paths) one is using to connect to another node or intermediary in the network (possible via a system of updated hashes and direct p2p off-chain zero knowledge proofs to guarantee that the intermediary’s total balance is conserved and fees are being paid, no on-chain zero knowledge required)
3. Keeping individual transaction details private from intermediaries along the path (provided automatically by rent-a-path channel models such as Counterfactual or Perun)
4. Keeping net transaction details private from intermediaries along the path (requires complicated techniques too large for a parenthetical note)

and so on!  Number 4 is something a lot of people have put a lot of thought into, and the degree of success there varies wildly depending on your real-world assumptions about the specific network in question.

My main point is that, yes, privacy in channels is an awesome and important thing to think about.  But it’s also important to identify *what you’re trying to make private*, and ask if there is a cheaper (performance or gas) or more private (higher total anonymity set) method for accomplishing the desired result.  In general I feel very strongly that channels should be either doing zero knowledge proofs offchain entirely, or else utilizing common on-chain resources so that all the use cases can share an anonymity set.  Privacy applications need to be very careful about fracturing their anonymity sets into very small pieces.

This, of course, does not touch much on the use of the *succinctness* properties of these techniques to reduce gas costs.  That is also very valuable, but my post was getting long enough as is ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**chris.whinfrey** (2019-03-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> The gas costs will be ~ 500k gas per snark validation.

Thanks for this! ~ 500k gas seems very reasonable. I believe that’s ~$0.35 at current ETH prices and a gas price of 5 Gwei.

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> One thing I would encorage you to do is to store the notes in a merkle tree. And use nullifiers to invalidate leafs. This helps us with privacy because we don’t need to reveal  noteA   noteB  in  transferNote  and a bunch of others.

I’m having a hard time understanding how the merkle tree will allow `noteA` and `noteB` to not be revealed. I get how you could prove inclusion of `originalNote` in the tree with a merkle proof. But I don’t understand how you could modify the root for the insertion of `noteA` and `noteB` into the tree without at least revealing which branches were modified. Also, could this technique be used for this proposal as well? [zkERC20: Confidential Token Standard · Issue #1724 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/1724)

---

**chris.whinfrey** (2019-03-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> We have discussed zero knowledge stuff for channels extensively at L4, and a good place to start seems to be to first identify which properties you want to make zero knowledge, and then to find as general a way as possible to provide that functionality, because zero knowledge schemes benefit from having as many people using the same mechanism as possible, rather than just users of your application, or just users of channels, etc.

Love this approach! And really appreciate this detailed response.

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> There are more things one could aim for, of course, but I think the above list captures most of the goals for your own design, correct?

Yes, this is a great list. ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> To have deposits and withdrawals to a channel not associated with any later or previous on-chain transaction activity (can be easily provided by simply redirecting state channel deposits and withdrawals through an onchain, zero knowledge transfers contract).

This is one area where I could possibly see the creation of channels with on-chain zero knowledge proofs helping. If a deposit is routed through a zero knowledge transfers contract and then immediately out and into the channel contract wouldn’t it be easy to figure out where that deposit originated because the value in and out of the contract is the same? Also, even if the anonymity set of the zero knowledge transfers contract is large, if a counterparty in a channel knows that deposit from the zero knowledge transfers contract was likely recently submitted, they could significantly narrow down that anonymity set to addresses that have recently made deposits to the zero knowledge transfers contract with a high probability.

By allowing participants to open and close channels and make transfers without ever exiting the contract, it may be more difficult to deanonymize participants when they do exit than if a common behavior is to enter and immediately exit the contract. I do think it’s a good point though that having many different privacy contracts leads to fractured anonymity sets and this is a very specific application.

I know you and the rest of the folks at L4 have given this a lot of thought and would love to hear what you think about this and where this logic may be flawed. Also, I’m very curious how different privacy applications could share a common set of resources in order to achieve a unified anonymity set if you all have started to think about how that could take form.

---

**technocrypto** (2019-03-02):

Regarding this last point, yes the ideal situation is to have as many spend conditions as possible supported within the single “zero knowledge zone”, including the multisig conditions.  In particular, to maintain the maximum benefit there should be no difference between a multisig/channel transfer and any other.  Someone should do some serious analysis as to which is the most general way to do this, so that the proof submitted for a send or batch of sends from the “zero knowledge zone” could in theory be a proof of arbitrary conditions having been met.  As some very preliminary thoughts of where to start, either a direct zero knowledge proof of a value in the state trie might work, or if that is too gas intensive the more specific “cross reference” table approach, with suitably proof-friendly hash function utilised, might be a good way to support an open standard for arbitrary capabilities.  The initial naive approach of using a regular contract to set a bit and then the zk proof to retrieve it would leak quite a bit of timing information at first, but anyone could still share in the total anonymity set by just waiting longer between the step for each side, and as increasingly general zk proof techniques were added on the “transparent” side the anonymity set on that side would eventually eat more and more use cases into fewer and fewer contracts, reducing the value of the timing information until it meant little at all.  Might be a nice place to start, unless someone can think of a better approach when they put their thinking cap on ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**barryWhiteHat** (2019-03-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/chris.whinfrey/48/10236_2.png) chris.whinfrey:

> I’m having a hard time understanding how the merkle tree will allow noteA and noteB to not be revealed. I get how you could prove inclusion of originalNote in the tree with a merkle proof. But I don’t understand how you could modify the root for the insertion of noteA and noteB into the tree without at least revealing which branches were modified. Also, could this technique be used for this proposal as well? zkERC20: Confidential Token Standard · Issue #1724 · ethereum/EIPs · GitHub

The addition is completely transparent but when you “spend” that you can do it in a way that noone knows. You need to add some complexity with nullifiers which prevents double spending. And if you want your leaf to create a new leaf you can do that too and just add that leaf to the MT afterwards. No information about what the new leaf does or what the last leaf was is leaked. Except the nullifier which is hidden. Check https://www.youtube.com/watch?v=84Vbj7-i9CI

> Also, could this technique be used for this proposal as well? zkERC20: Confidential Token Standard · Issue #1724 · ethereum/EIPs · GitHub

I have not studied that proposal but i think so.

