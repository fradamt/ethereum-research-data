---
source: ethresearch
topic_id: 3515
title: Plasma Cash defragmentation, take 2
author: vbuterin
date: "2018-09-24"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-cash-defragmentation-take-2/3515
views: 3640
likes: 1
posts_count: 4
---

# Plasma Cash defragmentation, take 2

See also: [Plasma Cash Defragmentation](https://ethresear.ch/t/plasma-cash-defragmentation/3410)

Another way to do Plasma Cash defragmentation is to have the *operator* publish a permutation that contributes toward defragmenting coins. Consider a design as follows. The operator can, at any point, make a special transaction to commit the Merkle root of a permutation which has the property that consists of a set of swaps between pairs (eg. 1 2 3 4 5 6 → 4 2 5 1 3 6 is ok, as it swaps (1,4) and (3,5), but 1 2 3 4 5 6 → 2 5 6 4 1 3 is not ok). The operator commits the Merkle root of a tree where the value at each position is the difference between the position and the value in the permutation (eg. for 1 2 3 4 5 6 → 4 2 5 1 3 6 this would be +3 0 +2 -3 -2 0).

Any exits, challenges or other on-chain operations involving data published before the permutation transaction is placed related to coin x must now use branches at position p(x) in the transaction trees (where p is the permutation), along with branches of the permutation tree at x and p(x); this de-facto reassigns ownership of coin x to the owner of p(x).

For two weeks after the permutation transaction is placed, a special type of exit can be made which exits a coin using purely pre-permutation data; if some coin x exits in this way, then the owner of x that used to be the owner of p(x) can publish the permutation branches, claiming p(x) for themselves. This should be used by honest users if the Plasma operator fails to publish permutation branches for their coins. This data can later be pointed to in an adjudication battle to essentially claim that in this permutation round, it’s “really” the case that (if q = p(x)), that x does not exist and p(q) = q.

![image](https://ethresear.ch/uploads/default/original/3X/c/1/c1aeb227987331648f23111cdf3003e6e4a164e2.svg)

*If yellow pre-exits, then B is left without a coin, so B can use the permutation data to take ownership of green*.

Note that this is why the permutation must be a self-inverse: if there were cycles with arbitrary lengths, there could be arbitrarily long cascades of x pre-exiting, leading to the new owner of x claiming p(x), but wait p(x) also pre-exited, so they need to claim p(p(x)), and so on, potentially requiring one party to publish O(N) data to chain.

You can show that it’s possible to use log(N) such permutations to shuffle N coins in an arbitrary way; the simplest algorithm is a greedy algorithm which looks for places where c[i] \ne i and swaps i and c[i] as much as possible; this will reduce the distance between the current permutation and your desired permutation by at least half in each iteration.

This approach does lead to old data needing more and more auxiliary branches over time to exit with; however, an ordinary user would only need to look up old data in one of two cases: (i) they did not make a transaction in a very long time and are exiting, or (ii) they are responding to a challenge made by another malicious user. A user can avoid (i) by sending to themselves every few months, and (ii) is at most 1:1 griefing factor, and can be avoided by making the procedure of sending to oneself every few months mandatory and disallowing challenges using very old data, or alternatively [Plasma XT](https://ethresear.ch/t/plasma-xt-plasma-cash-with-much-less-per-user-data-checking/1926/8)-style state commitments.

Edit: here’s some python code to play with defragmentations: [research/defrag/permutation2.py at master · ethereum/research · GitHub](https://github.com/ethereum/research/blob/master/defrag/permutation2.py)

## Replies

**danrobinson** (2018-09-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> For two weeks after the permutation transaction is placed, a special type of exit can be made which exits a coin using purely pre-permutation data;

Wouldn’t this mean that the operator can force a mass exit?

What about a design where the permutation is fully specified on the main chain, so there’s no data availability problem?

---

**MaxC** (2018-09-24):

What about having a zk snark proof that a permutation is correct, if that’s possible. Then Bob or ALice or whoever else just need to know start and end indices within the tree to exit, and a proof that those start and end indices are correct.

So, as long as the operator is over-collateralised - data availability is never a problem. This is because you could require an operator to post information about the start and end indices for a user when exiting, and if he doesn’t respond those funds are sent to the user.

What’s even more interesting - you could have the participants or other participants claim that data is available and stake their coins if it is.

---

**vbuterin** (2018-09-24):

> What about a design where the permutation is fully specified on the main chain, so there’s no data availability problem?

You can do that, and if you do that you don’t even need to restrict permutations to being self-inverses. But that does require something like k * log(n) bits on chain for n coins with k fragments. I suppose if you’re okay with that then that is the best solution.

> Wouldn’t this mean that the operator can force a mass exit?

We can try to remove the need for proactive exiting as follows. There is no time limit on pre-exiting. However, if you hold x and p(x) gets pre-exited, then you must either post a transaction challenging the pre-exit as above, or pre-exit yourself. This can be done through multiple permutations; if x gets pre-exited by a previous owner, the current holder of x can take ownership of p_n(p_{n-1}(...(p_1(x))...)), providing proofs for each permutation. If the current owner of that coin complains, they would need to themselves challenge by providing proof that x was spent by the same party that pre-exited, thereby canceling the pre-exit.

