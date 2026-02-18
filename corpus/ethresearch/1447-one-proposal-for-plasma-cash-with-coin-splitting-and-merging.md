---
source: ethresearch
topic_id: 1447
title: One proposal for plasma cash with coin splitting and merging
author: ldct
date: "2018-03-21"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/one-proposal-for-plasma-cash-with-coin-splitting-and-merging/1447
views: 3759
likes: 0
posts_count: 5
---

# One proposal for plasma cash with coin splitting and merging

Expanding on a post I made in the Plasma Cash thread, and after reading the discussion there.

Coin IDs are variable-length bitstrings, which are encoded into a fix-length bitstring by prepending the unique string that matches the regex 0*1; for example, assuming encoding to uint8, “0” is encoded as “00000010”, “1” is encoded as “00000011”, “110” is encoded as “00001110”. there is a global constant K and the denomination of a coin with coinid of length k is 2^(K-k).

There are three types of transactions:

1. a single coin (with coin id X) changes owner
2. two coins with coin ids X0 and X1 merge into a coin with id X
3. a coin with id X splits into coins with id X0 and X1

Block headers commit to a (binary, not-necessarily-complete) merkle tree of transactions. each transaction is labelled by X and transactions must be stored in the merkle tree at position X. we say that two coins “intersect” if one of their coin ids is a prefix of the other (intuition: we can view a coin as a set of the smallest coins into which it can be split (e.g.: maximum coin id length is 7, then consider “11111” as the union of coins {“1111100”, “1111101”, “1111110”, “1111111”}), and coin intersection reduces to set intersection, equivalently set containment). note that by the consturction of the transaction tree, a commitment that no transactions includes coinid P implies that no transaction include coinid PB for all bitstrings B.

The root plasma contract stores the subset of minimal coins that have been deposited, and no valid transaction can change this subset. if an invalid transaction with id X begins exit, every honest coinholder that holds a coin Y that intersects X knows and can stop the exit.

An assumption here is that users will find it mutually beneficial to swap coins of the same denomination with each other in such a way that they end up with coins that can be merged.

## Replies

**danrobinson** (2018-03-21):

Why is it necessary that only adjacent coins merge? What do you think of [Plasma Cash: Plasma with much less per-user data checking - #53 by danrobinson](https://ethresear.ch/t/plasma-cash-plasma-with-much-less-per-user-data-checking/1298/53)?

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> The root plasma contract stores the subset of minimal coins that have been deposited, and no valid transaction can change this subset. if an invalid transaction with id X is committed, every honest coinholder that holds a coin Y that intersects X knows and immediately exits Y.

Quibble: in Plasma Cash, you don’t have to watch for invalid transactions and exit if you see one. You can just lazily wait for any exit attempt for any coin that intersects with yours, and challenge it then.

---

**ldct** (2018-03-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> Quibble: in Plasma Cash, you don’t have to watch for invalid transactions and exit if you see one. You can just lazily wait for any exit attempt for any coin that intersects with yours, and challenge it then.

right, you have to monitor the chain for intersecting invalid transactions, but when you see one you don’t have to exit. in my mind the immediate-exit and lazily-exit protocols are basically equivalent.

> Why is it necessary that only adjacent coins merge?

mainly because the informal safety proof I used to reason that my design is correct doesn’t work if non-adjacent coins can merge; of course, a different proof might be used for some other design (such as yours) which allows any coins to merge, but I’d have to think about it, and I’ll comment on that thread.

---

**danrobinson** (2018-03-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> right, you have to monitor the chain for intersecting invalid transactions, but when you see one you don’t have to exit. in my mind the immediate-exit and lazily-exit protocols are basically equivalent.

Continuing to quibble—you don’t have to monitor the chain at all. You only need to hold on to your coin, and respond to any attempt to withdraw your token ID by revealing your latest transaction. (If you want to send the coin on the Plasma chain, you do need to get that subsequent data from someone, so you can provide a proof to the recipient. In my opinion, it actually makes the most sense for the chain operator to just keep all this data and provide it to the recipient, since they are trusted for on-chain liveness anyway).

---

**ldct** (2018-03-21):

you are correct about that, I’ve edited my post ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

