---
source: ethresearch
topic_id: 7654
title: Validating transactions with ZK methods
author: Joncarre
date: "2020-07-07"
category: Consensus
tags: []
url: https://ethresear.ch/t/validating-transactions-with-zk-methods/7654
views: 3339
likes: 3
posts_count: 14
---

# Validating transactions with ZK methods

After reading some topics on the implementation of ZK methods in the Ethereum, how would this affect the PoW?

Please have someone correct me if I am wrong (I started recently), but if the nodes need to validate transactions, how can they do it without having access to the information?

For example: a smart contract fulfills a condition when person A makes a payment of 1 Ether to person B. With ZK methods this information is not known. Therefore, if it is not known, how can the nodes validate that the contract has been correctly fulfilled if it is not possible to access this information?

## Replies

**vbuterin** (2020-07-07):

The idea is generally that whoever generates the transaction (and the ZK proof) would have the information needed to correctly process that transaction, and would use that information as part of the process of generating the proof.

---

**Joncarre** (2020-07-07):

Hum… could you explain more about that? I don’t quite understand

---

**vbuterin** (2020-07-08):

So for example here is how a ZK rollup works:

- Alice, Bob, Charlie… Zachary all sign transactions that send money from some account to some account (inside the rollup). They send their transactions to an operator, Ozzie.
- Ozzie verifies all the transactions, and computes the Merkle root of the new state (ie. everyone’s new balances) after the transactions are processed. Let R be the previous Merkle root (ie. the Merkle root of everyone’s balances before these transactions are processed), and R' be the new Merkle root. Ozzie also generates D, a compressed record of the balance changes made by the transactions.
- Ozzie generates a cryptographic proof, that proves the statement “I know a bunch of transactions such that if you start with a state whose Merkle root is R, then apply the transactions, it leads to the balance changes in D, and leaves the new Merkle root R'.” Ozzie publishes D, R, R' and the proof to the chain. The smart contract checks that the current Merkle root is R, verifies the proof, and if all checks out, changes the Merkle root from R to R'. Notice that the transactions themselves never need to go on chain, just D (~15 bytes per transaction).

ZK-SNARKs generally have the property that you can make proofs of claims like “I know a piece of data, such that if you perform a calculation with this data and some other data, then the result is 1846124125”. These proofs can be verified very quickly no matter how complex the claim is that they are proving.

Does that make some sense to you?

---

**Joncarre** (2020-07-08):

I think I get it… May I ask another question? The Ethereum blockchain has the data visible in its transactions, but is it possible to encrypt some of the information? Must ALL information be made public? If some of the information can be encrypted, then the nodes cannot read it or execute the PoW, am I wrong?

Therefore I deduce that the information must be obligatorily public, but sometimes I can’t understand this concept (I read some research articles in which researchers develop frameworks to encrypt information… does it make sense?)

Thank you very much for answering!

---

**qbzzt** (2020-07-13):

The information on the blockchain has to be public for it to be properly used for a PoW. Smart contracts don’t have secrets.

However, the information that is provided to the smart contract doesn’t have to be cleartext. For example, if I have a smart contract that publishes messages, I might send it

`Uryyb, jbeyq`

Everybody will know the message, but only people who know how to decrypt it (https://rot13.com/) will know that the message is actually

`Hello, world`

---

**Joncarre** (2020-07-14):

Thanks a lot for your answer! Then, my last question is: the PoW does not need to see the information to validate a transaction, right?

What confuses me is: how can the nodes validate the transactions if they can’t see the plain text? (because as far as I know, at this moment Ethereum doesn’t have Zero-knowledge methods)

---

**qbzzt** (2020-07-15):

Whether it is PoW or PoS, the blockchain has to have the information to validate the way smart contracts run. If a smart contract needs to be able to read the cleartext, anybody on the blockchain will be able to read the cleartext.

AFAIK, the only way to use secrecy on the blockchain is to handle the encryption and decryption in the UI code, and only have the ciphertext on the blockchain.

---

**Joncarre** (2020-07-15):

I think I understand… May I give you a little example?

Let’s say a contract that runs an auction. The auction is private, so I send what I’m willing to pay (just like anyone else who calls the contract). Then, the auction is executed.

If the blockchain nodes have to validate the transactions and decide if the result is correct, all those nodes must also know the bids that were placed, right? Then there would be no privacy in the data.

Is this correct?

btw, what’s UI? ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=14)

---

**qbzzt** (2020-07-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/joncarre/48/5014_2.png) Joncarre:

> If the blockchain nodes have to validate the transactions and decide if the result is correct, all those nodes must also know the bids that were placed, right? Then there would be no privacy in the data.

Exactly. You could have your bid come from a throw away address you’ve never used and will never use again, but the amount of the bid cannot be a secret.

UI is short for user interface. It would typically be code that runs in your browser and communicates with the blockchain.

---

**Joncarre** (2020-07-15):

Thank you very much for the answer. So, that said, do at least 51% of the nodes execute (and validate) all the contracts of all the transactions that are made every 17 seconds?

Sometimes the blockchain seems like magic to me.

---

**qbzzt** (2020-07-15):

I haven’t read the white paper so I’m not sure, but I think all nodes execute and validate all the transactions. Otherwise they wouldn’t be able to verify that a proposed next block is valid.

![](https://ethresear.ch/user_avatar/ethresear.ch/joncarre/48/5014_2.png) Joncarre:

> Sometimes the blockchain seems like magic to me.

Maybe this will help. [etherdocs/what_can_Ethereum_do.md at be4e7792897158fa843dd5b7b08d01b351bcf138 · qbzzt/etherdocs · GitHub](https://github.com/qbzzt/etherdocs/blob/be4e7792897158fa843dd5b7b08d01b351bcf138/what_can_Ethereum_do.md)

---

**barryWhiteHat** (2020-07-17):

All nodes execute and validate all the transactions. If they didn’t do this I could create  a block creating a lot of eth and giving it to myself. If people don’t check everything they could be vulnerable to this attack.

---

**Joncarre** (2020-07-17):

yeah good point… Thanks so much guys. That helped a lot.

