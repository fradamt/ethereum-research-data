---
source: ethresearch
topic_id: 1974
title: Plasma Cash without any blockchain at all
author: kladkogex
date: "2018-05-11"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-cash-without-any-blockchain-at-all/1974
views: 5364
likes: 4
posts_count: 27
---

# Plasma Cash without any blockchain at all

It seems that if coins are indivisible/immutable, then one can have Plasma Cash as a simple Merkle tree without having any blockchain.  The reason for this is that since the coins are immutable,  there is no need for global transaction ordering/consensus.  For a particular coin you only need its history and other coins are irrelevant. Therefore,  a blockchain  may be an overkill

Here is a quick sketch of how this could work - comments are welcome

1. Each coin-chain is a linked list of ECDSA signatures one on top of another.
2. If I want to pass my coin-chain to someone else, I simply append the address of the receiver to the SHA-3 hash of the current tip of the list and sign it creating a new tip.  The coin-chain then becomes one entry longer.
3. The Plasma operator maintains a Merkle tree of all coin-chains.
4. When I transfer a coin-chain to someone else, I submit the new tip of the coin-chain to the Plasma operator.  The Plasma operator then waits to receive say 1000 submissions, keeping them in the pending queue. Once the Plasma operator receives 1000 submissions, it recalculates Merkle root and posts the Merkle root to the Plasma smartcontract, which just becomes a sequence of Merkle roots. Plasma operator then provides me a Merkle proof of inclusion of the updated coin-chain in the Merkle tree.
5. A transaction is confirmed once the Merkle root is updated in the Plasma smart contract.
6. Exiting becomes really easy - to exit I simply sign a transfer of my coin-chain to address 0.
7. Double-spend is impossible because coin-chains in the Merkle tree are ordered by coin-ID, and there is only one coin-chain for a particular coin ID.
8. The current coin-chain owner always has the longest coin-chain, so if someone tries to revert transactions by shortening a coin-chain, the owner can always provide a fraud proof
9. If a coin-chain grows too long,  one can checkpoint it (cut old history),  checkpoint security can be achieved by maintaining a separate Merkle tree of checkpoints and storing the Merkle root of checkpoints in Plasma smart contract.

## Replies

**vbuterin** (2018-05-11):

The blockchain is still useful to prevent the operator from maintaining multiple conflicting Merkle trees.

---

**kladkogex** (2018-05-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> If the Merkle tree committed to the parent chain is just a state root, what happens if the chain operator commits a new Merkle tree that conflicts with an old one?

If the chain operator commits a new Merkle root that conflicts with an old one, then I think everyone is supposed  to exit since the operator is a bad guy

In this case I think everyone exits according to coin ownership as per

Merkle root preceding  the bad root …

I

---

**danrobinson** (2018-05-11):

If the Merkle tree committed to the parent chain is just a state root, what happens if the chain operator commits a new Merkle tree that conflicts with an old one?

I think your proof of valid coin history will also need to provide all the past Merkle paths from the state roots (to prove that there was never a reversion of one of those states), at which point I think the only difference is that you’re using state roots rather than transaction roots (which ends up with roughly similar overhead but a little more difficult validation).

---

**kladkogex** (2018-05-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> If the Merkle tree committed to the parent chain is just a state root, what happens if the chain operator commits a new Merkle tree that conflicts with an old one?

If the chain operator commits a new Merkle root that conflicts with an old one, then I think everyone is supposed to exit since the operator is a bad guy.

In this case I think everyone exits according to coin ownership as per

Merkle root preceding the bad root …

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> I think your proof of valid coin history will also need to provide all the past Merkle paths from the state roots (to prove that there was never a reversion of one of those states),

I think it can be the duty of the chain operator to make sure reversions do not happen (reversions would mean going from a longer coin-chain to a shorter coin-chain.

If the chain operator allows any of bad things to happen (such as reversion) then everyone exits.  During the exit longer coin-chains win over shorter coin-chains

So it seems one does not need past Merkle paths …

---

**danrobinson** (2018-05-11):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> If the chain operator allows any of bad things to happen (such as reversion) then everyone exits. During the exit longer coin-chains win over shorter coin-chains

When you receive a coin, how do you know there isn’t a longer coin-chain already in its history?

(Also, I don’t think you could mean that longer chains always win over shorter chains. That would give you a bigger problem—it would mean anyone could double-spend a past coin, and just just spend it more times than you to gain priority. Do you mean that earlier spends of a coin have priority over later spends?)

---

**kladkogex** (2018-05-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> When you receive a coin, how do you know there isn’t a longer coin-chain already in its history?
>
>
> (Also, I don’t think you could mean that longer chains always win over shorter chains. That would give you a bigger problem—it would mean anyone could double-spend a past coin, and just just spend it more times than you to gain priority. Do you mean that earlier spends of a coin have priority over later spends?)

Thank you for the insights )

All coins are ordered by their coin IDs at the lower level of the Merkle tree (I guess one could also use a Patricia tree)

If I am getting paid with an older coin chain,  then what must have happened is that

1. Eve had coinchain OldCoinChain in Merkle Tree
2. Eve paid to Alice so the OldCoinChain got replaced by NewCoinChain where  Alice is the owner
3. Eve in cooperation with a malicious Plasma operator replaced NewCoinChain with the OldCoinChain in the Merkle Tree (the operator should have rejected this operation)

4,  Eve is trying now to pay with OldUsingChain to Bob

It looks like at 3, Alice should have noted that somebody has stolen her coin, so Alice can provide a fraud proof to the Plasma smartcontract showing her chain included in on of previous Merkle roots.

I think you are totally right, it is earlier spends vs newer spends, not short chains vs long chains …

---

**danrobinson** (2018-05-14):

If the chain operator hides the block where step 3 happened from Alice (refusing to make it available), what can Alice do?

And how is Bob supposed to know that the fraud happened if he doesn’t check the previous Merkle state roots? Particularly since there’s no guarantee that there was an “Alice” defrauded in the past—this could just be a fraud on Bob, where Eve and the operator will reveal the prior fraud *after* Bob has been tricked into accepting the coin.

Also, does your mechanism depend on Alice noticing this unavailability and exiting within a fixed time period? If so, it loses one of the main advantages of Plasma Cash (avoiding mass forced exit).

---

**kladkogex** (2018-05-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> If the chain operator hides the block where step 3 happened from Alice (refusing to make it available), what can Alice do?

If the chain operator starts witholding blocks from Alice, Alice will simply exit the system then. This is not much different from Plasma MVP

“A user should continually validate (or validate at least once per 7 days) that the Plasma chain is fully available and valid; if it is not, they should exit immediately.”

Note that the probability of the chain operator becoming malicious is way lower than any user becoming malicious.  If a chain operator becomes malicious, it loses  all of its business.

In real life,  the most attacks will come from users

---

**danrobinson** (2018-05-15):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> If the chain operator starts witholding blocks from Alice, Alice will simply exit the system then. This is not much different from Plasma MVP

Yes, but it is different from Plasma Cash (at least if there is a time within which the user must withdraw).

I still don’t understand how a user receiving a coin would know that there are no double spends in the coin’s history (which could invalidate the transaction in which the user received it).

---

**kladkogex** (2018-05-15):

Similar to Plasma cash you could provide non-spend proofs for the previous Merkle trees :–))

The reason why the entire thing is interesting to me is because for Plasma cash you only need history for each particular coin,  the relative histories are irrelevant. Therefore,  having a global ledger and a global consensus seems an overkill  at the conceptual level ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**danrobinson** (2018-05-15):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Similar to Plasma cash you could provide non-spend proofs for the previous Merkle trees :–))

Then I don’t think this is significantly distinguishable from Plasma Cash, except that the things being committed are state commitments rather than transactions, right?

---

**kladkogex** (2018-05-15):

Yes !

But it is interesting to understand what the optimal data structure to commit (transactions vs state as you said or soemthing mixed). For state there are things like Merkle Mountain ranges that people discussed here.  It may be that you can to update non-spend proofs less frequently if you use Merkle Mountain ranges plus state roots - it is interesting to understand  how this would work. Also it is interesting which data structure is more efficient for concurrent execution by the operator ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**ldct** (2018-05-16):

It is worth noting that checkpoints in [Plasma XT: Plasma Cash with much less per-user data checking](https://ethresear.ch/t/plasma-xt-plasma-cash-with-much-less-per-user-data-checking/1926) can be thought of as state roots, which are tied to the transaction roots cryptoeconomically.

~~One problem with using only state roots is that you no longer have an O(1) exit game. The plasma operator could commit N state roots, 1 of which is an invalid state transition (with respect to the previous state root) but withhold all the data, and then exit with the last state root. The proper coin owner cannot construct a fraud proof because the necessary data is unavailable; hence the exit game must take O(\log N) steps. I believe this is necessarily true in your design, but it seems like a description of the exit game has been omitted.~~

Also, small nitpick: I think you mean “sparse merkle tree” since “merkle tree” as the term is commonly used doesn’t support succint non-inclusion proofs.

---

**danrobinson** (2018-05-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> One problem with using only state roots is that you no longer have an O(1)O(1) exit game. The plasma operator could commit NN state roots, 1 of which is an invalid state transition (with respect to the previous state root) but withhold all the data, and then exit with the last state root. The proper coin owner cannot construct a fraud proof because the necessary data is unavailable; hence the exit game must take O(logN)O(\log N) steps. I believe this is necessarily true in your design, but it seems like a description of the exit game has been omitted.

I don’t think this is right? The proper coin owner can just reveal their older coin and challenge the exiter to provide a spend of that coin, just as in normal Plasma Cash.

---

**ldct** (2018-05-16):

Ah yes, you’re right. The state roots here are not authoritative in the sense that they are still subject to the exit game.

---

**kladkogex** (2018-05-16):

I think potentially a good point of using state roots is it can allow one to run generic EVM  contracts on Plasma.

One could use the state root of the internal smart contract state as Plasma root. Then you would need to have some type of a bounty for independent validation of smart contract state root transitions.

Truebit does not fit well because it is vulnerable to front  running,  one probably needs a more advanced online crypto protocol that allows validators to claim fraud with a provable protection against front running.

---

**jdkanani** (2018-05-17):

> EVM contracts on Plasma

For EVM (with the limited state) to work, challenge period is required and it will end up increasing block time.

> Truebit does not fit well because it is vulnerable to frontrunning, one probably needs a more advanced online crypto protocol that allows validators to claim fraud with a provable protection against frontrunning.

Yes. but for now, Truebit (game) like challenge will work.

---

**MaxC** (2018-05-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> Also, small nitpick: I think you mean “sparse merkle tree” since “merkle tree” as the term is commonly used doesn’t support succint non-inclusion proofs.

Merkle trees support O(log(n)) non-inclusion proofs.

---

**MaxC** (2018-05-17):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Truebit does not fit well because it is vulnerable to front running, one probably needs a more advanced online crypto protocol that allows validators to claim fraud with a provable protection against front running.

Wonder if one could use either a commit-reveal scheme (or zero knowledge proof) to prevent front-running.

---

**ldct** (2018-05-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> Merkle trees support O(log(n)) non-inclusion proofs.

What’s the mechanism for this?


*(6 more replies not shown)*
