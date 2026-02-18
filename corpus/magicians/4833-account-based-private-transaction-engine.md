---
source: magicians
topic_id: 4833
title: Account-based private transaction engine
author: snjax
date: "2020-10-15"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/account-based-private-transaction-engine/4833
views: 828
likes: 1
posts_count: 1
---

# Account-based private transaction engine

# Account-based private transaction engine

## Prior work

Sapling is a well-known privacy engine, supporting N-to-M join-split transactions. For each spent note we should publish a separate nullifier. There could be the following issues:

1. Nullifiers take space onchain and require onchain computations.
2. Number of nullifiers of the transaction is known and it is a potential data leak.

## This work

Let’s represent new object `Account = (dk, pos, amount, salt)`, where `dk` is the decryption key or another private identity of the account, `pos` is the biggest position of the spent leaf inside the Merkle tree, `amount` is current currency balance of the account, and `salt` is a random blinding parameter.

The `UTXO=(d, pk_d, amount, salt)` will be the same as in Sapling. To reduce the number of circuit inputs we will store both UTXOs and accounts inside one Merkle tree. For example, for the N-to-2 case, even leaves will be accounts and odd leaves will be UTXOs.

To initialize accounts, let’s suppose, that there are any accounts with form `(dk, 0, 0, 0)` inside our privacy set. So, when we make the first transaction, we should publish the nullifier for the initial state of our account and we will never initialize any account with the same `dk` in the future.

To transfer, we put Merkle root, old account nullifier `and output_note = hash(new_account_hash, new_utxo_hash)` to zkSNARK’s public inputs, and data and Merkle proofs to private inputs.

The SNARK checks, that sum of output equals to the sum of input, the nullifier is valid, the user is the owner of the notes, the new account’s `pos` is greater or equals the previous one, and all nonzero UTXOs spent has a position between old and new accounts.

### Advantages

We can spend any big number of UTXOs in one transaction without onchain overhead (and in-circuit overhead will not be so huge due to snark-friendly functions and novel proving systems) and data leaks.

So, it’s enough to publish 10 bytes per nullifier, 20 bytes per output note, and 4 bytes to link the Merkle root. 34 bytes total.

### Disadvantages

The user should spend the UTXOs only one by one. So, the user cannot skip any number of dust UTXOs without burning them.

## Author

Igor Gulamov, [zeropool.network](https://github.com/zeropoolnetwork/).
