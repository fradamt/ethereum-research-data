---
source: ethresearch
topic_id: 3737
title: Plasma Cash defragmentation, take 3
author: vbuterin
date: "2018-10-08"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-cash-defragmentation-take-3/3737
views: 4533
likes: 6
posts_count: 5
---

# Plasma Cash defragmentation, take 3

*Special thanks to Ben Jones for the more pre-signed defragmentation idea*

See also [Plasma Cash Defragmentation](https://ethresear.ch/t/plasma-cash-defragmentation/3410) and [Plasma Cash defragmentation, take 2](https://ethresear.ch/t/plasma-cash-defragmentation-take-2/3515)

This time, we go back to “voluntary defragmentation”, where in order for the index of any user’s coins to change that user must actively participate, but we propose and implement a specific algorithm. Suppose that A wants to send x coins to B, and for simplicity A has a single fragment containing these coins. Simply transferring that fragment to B may increase total fragmentation by 1, as A's fragment of y \ge x may split up into two fragments of x (owned by B) and y-x (still owned by A) if y > x.

But we can instead try to look for a **non-fragmenting path**. We define a non-fragmenting path for a transfer of x coins as follows. We consider G a *forward-neighbor* of F if there exists a fragment controlled by G which is adjacent to a fragment controlled by F of size \ge x:

![Fragments](https://ethresear.ch/uploads/default/original/2X/6/65dc076a5367a11a421208c78907056825988057.png)

Because G has a 2-coin slice adjacent to F at the end, G is a forward-neighbor of F for \le 2 coins, but *not* \ge 3 coins. F is a forward-neighbor for G for \le 3 coins.

A non-fragmenting path from A to B for x coins is a sequence A = S_0, S_1, … ,S_{n-1}, S_n = B, where S_{i+1} is a forward-neighbor for S_i for x coins. If such a path exists, then we know that every S_i can make a non-fragmenting transfer to S_{i+1} by transferring ownership of their slice adjacent to S_{i+1}, and so we can make a transfer from A to B as an atomic swap: A sends coins to S_1, S_1 to S_2 … S_{n-1} to B.

[![Fragments(1)](https://ethresear.ch/uploads/default/original/2X/5/5a8b2912a64a69ce280e21a900b1abc2a7dade26.png)Fragments(1)601×104 1.73 KB](https://ethresear.ch/uploads/default/5a8b2912a64a69ce280e21a900b1abc2a7dade26)

If Q wanted to transfer a coin to G, and the slice on the left was not controlled by G, then this is also possible (notice that the slice F uses to receive and the slice F uses to send are different):

[![Fragments(2)](https://ethresear.ch/uploads/default/original/2X/8/8cbb0568762981b2bc894b21f96c29d3e906682c.png)Fragments(2)601×104 2.37 KB](https://ethresear.ch/uploads/default/8cbb0568762981b2bc894b21f96c29d3e906682c)

The entire path can be completed as a single atomic swap transaction. Large transfers can be split up into multiple paths if the fragments are not large enough to complete them as a single path. Large transfers can actually be good for defragmentation, as all paths except the last involve the sender sacrificing ownership of a complete fragment, thereby decreasing fragmentation by 1.

Paths should be easy to find. When a user has N fragments, for small transfers they have \approx 2 * N forward-neighbors, and so if portion p of them are online, they have 2 * p * N neighbors they can count on in the pathfinding graph.

Here is simulation code for using this as a way of sending transactions in Plasma Cash: [research/defrag/send_bfs.py at master · ethereum/research · GitHub](https://github.com/ethereum/research/blob/master/defrag/send_bfs.py) . One key result is that the number of fragments stabilizes (at least given the assumptions in the simulation about ownership and transfer sizes) when p * N \approx 10, and even there the code is likely suboptimal; in any case, it is clear that under any reasonable assumptions, keeping fragmentation permanently below a fixed number of fragments per user with this algorithm is feasible.

But we can go further. First of all, the above fragmentation-limiting mechanism does not need to happen at the same time as transfers. Instead, we can use it to find a path between a user and a slice beside themselves.

[![Fragments(4)](https://ethresear.ch/uploads/default/original/2X/1/172b6f99f539aa8bffb681b3072fdafc545655c2.png)Fragments(4)602×104 1.93 KB](https://ethresear.ch/uploads/default/172b6f99f539aa8bffb681b3072fdafc545655c2)

![Fragments(5)](https://ethresear.ch/uploads/default/original/2X/e/ea0cacb3cea2195fc150c8f1a48c943a40886c23.png)

Note that defragmentation makes pathfinding harder, eg. after this defragmentation round, the only path from G to R depends on Q, which was not the case before. This is why there will inevitably arise an equilibrium of fragment sizes, though simulations show that a small number of fragments per user is sufficient.

Now, here’s the next optimization: we can ask users to pre-sign defragmentation swaps that are scheduled at some block in the future, and execute them only if everyone else listed in the swap also comes online before that time (and no parties involved make any other transfers). This allows us to keep fragmentation low even if a very small portion of users are online at the same exact time.

An atomic swap only requires two users with coins A and B to both sign a transaction that specifies that the transaction’s use in the Plasma exit game for either coin A or B requires providing the Merkle branches proving inclusion in both coins at a given exact height (see [discussion here](https://ethresear.ch/t/plasma-cash-minimal-atomic-swap/3409/2)), so atomic swaps are easy to execute, and can be safely pre-signed.

This allows us to use Plasma Cash in a way that keeps fragmentation very low, keeping its on-chain resource consumption limited even if the minimal denomination is very small.

## Replies

**danrobinson** (2018-10-08):

I think this is the right approach. It starts to look more and more like a bilateral payment channel network like Lightning, but built on a better substrate (where rebalancing between your channels happens naturally, rather than requiring a full on-chain transaction).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> An atomic swap only requires two users with coins A and B to both sign a transaction that specifies that the transaction’s use in the Plasma exit game for either coin A or B requires providing the Merkle branches proving inclusion in both coins at a given exact height (see discussion here), so atomic swaps are easy to execute, and can be safely pre-signed.

Unfortunately I believe it’s a little more complicated than I had thought—the exit game needs to account for a lot of edge cases, including the following difficult case:

- Alice has signed an atomic transaction trading her coin 1 for Bob’s coin 2 but doesn’t have a signature from Bob
- the operator begins withholding blocks
- Bob attempts a withdrawal from coin 1 (from some possibly invalid new transaction, which could be after the atomic trade) and coin 2 (from the coin Alice was trying to trade with him) simultaneously.

Alice would need to challenge coin 2 to find out the information she needs to challenge coin 1’s withdrawal.

We think there’s probably a way to do it if you augment the exit game, and possibly have two rounds of signatures on each atomic transaction. But requiring the ability to safely have multiple atomic transactions in flight seems like it’s courting unmanageable complexity, so I’m not sure if that part of the defragmenting protocol will be worth it.

---

**vbuterin** (2018-10-08):

> Alice would need to challenge coin 2 to find out the information she needs to challenge coin 1’s withdrawal.

Yes, this is correct. The modification to the exit game needed to make the exit game secure is that when a withdrawal attempt of coin 1 using an atomic swap transaction between coin 1 and coin 2 is started, any active withdrawals of coin 2 have their challenge periods extended by a week. So when Alice sees Bob’s withdrawal she can immediately use the same data to start a withdrawal on coin 2.

---

**danrobinson** (2018-10-08):

But what if Bob doesn’t withdraw coin 1 from the atomic swap tx, but rather from a later spend of coin 1 (which may or may not have invalid history)? Alice doesn’t find out any new useful information from that. Additionally, the protocol doesn’t see any atomic tx (just Bob’s attempted withdrawal from a simple spend), so it has no way of knowing that it should toll any withdrawal periods.

---

**vbuterin** (2018-10-08):

> But what if Bob doesn’t withdraw coin 1 from the atomic swap tx, but rather from a later spend of coin 1 (which may or may not have invalid history)?

Alice already did not see the atomic swap get included, so as soon as Bob starts that withdrawal, Alice will challenge, and to answer the challenge Bob will have to reveal the fully double-signed atomic swap tx, allowing Alice to win the exit game on the other side.

