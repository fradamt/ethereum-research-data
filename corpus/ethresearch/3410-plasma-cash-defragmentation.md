---
source: ethresearch
topic_id: 3410
title: Plasma Cash Defragmentation
author: vbuterin
date: "2018-09-17"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-cash-defragmentation/3410
views: 7307
likes: 11
posts_count: 18
---

# Plasma Cash Defragmentation

The main weakness of Plasma Cash is the indivisible nature of the tokens. To make the system worthwhile to use, the transaction fee needed to exit should be much smaller than the value exited; because in Plasma Cash each unit of value needs to be exited separately, this effectively means that the minimum denomination size in Plasma Cash would need to be several hundred times a blockchain transaction fee (ie. in the dollars).

We can solve this problem by making the denomination very small, and allowing users to “multi-exit” a subtree of coins that all have the same owner with a single Merkle branch. Given a 2^k sized subtree where every element is identical, a single branch of that tree is enough to provide the information needed to verify the entire subtree and sign off on behalf of it. However, using this in practice leads to a fragmentation issue, as users send each other partial payments and keep breaking their coins up into more and more pieces; after enough payments, a user would have to submit a separate Merkle branch and pay a full transaction fee for each coin that they exit, nullifying the benefit of exiting subtrees.

One solution to this is ongoing defragmentation, and the scheme I will propose is as follows: as a condition of accepting a transaction from A sending coins to B, A and B would have to send each other coins in such a way that at the end, every coin held by A has a lower index than every coin held by B. For example, suppose the starting allocation is `B A C D A; B B E B F; G A A H I`, and A is sending B two coins. The starting balances are A: 4, B: 4, so the final balances would be A: 2, B: 6, so the final allocation would be `A A C D B; B B E B F; G B B H I`, so the transfer would be an atomic swap: A gives B coins 4, 11, 12, and B gives A coin 0.

A simulation shows that this scheme can keep fragmentation very low indefinitely:

```python
import random, math

def mk_initial_balances(accts, coins):
    o = []
    for i in range(accts):
        o.extend([i] * random.randrange((coins - len(o)) * 2 // (accts - i)))
    o.extend([accts-1] * (coins - len(o)))
    return o

def fragments(coins):
    o = 0
    for i in range(1, len(coins)):
        if coins[i] != coins[i-1]:
            o += 1
    return o

def xfer(coins, frm, to, value):
    coins = coins[::]
    pos = 0
    while pos  0:
        if coins[pos] == frm:
            coins[pos] = to
            value -= 1
        pos += 1
    return coins

def unscramble(coins, c1, c2):
    coins = coins[::]
    k1 = coins.count(c1)
    pos = 0
    while pos  0 else c2
            if coins[pos] == c1:
                k1 -= 1
        pos += 1
    return coins

def run_with_unscrambling(coins, rounds):
    for i in range(1000):
        c1, c2 = sorted([random.randrange(max(coins)+1) for _ in range(2)])
        value = int(coins.count(c1) ** random.random())
        coins = xfer(coins, c1, c2, value)
        coins = unscramble(coins, c1, c2)
    return coins

c = mk_initial_balances(25, 1000)
c = run_with_unscrambling(c, 10000)
print(fragments(c))
```

This puts a heavy burden on the security of atomic swap protocols: each transaction is now an atomic swap. Here is one way to do this reasonably efficiently in Plasma Cash: [Plasma Cash Minimal Atomic Swap](https://ethresear.ch/t/plasma-cash-minimal-atomic-swap/3409).

## Replies

**kladkogex** (2018-09-17):

If the denomination is very small it will make the potential use of SNARKs for non-inclusion proofs  even harder since the number of SNARK inputs will rise

---

**vbuterin** (2018-09-18):

What claim are you looking to STARK prove? In general it should be possible to just make a STARK proof for an entire subtree in O(log(n)) time.

---

**danrobinson** (2018-09-18):

This is a really, really exciting approach.

I’m worried that the simulation might be unrealistic. I’m not sure why you can sort `c1` and `c2`, which should tend to lead to all the money being clustered in the highest accounts; or why the recipient `c2` is picked from accounts that currently hold some coins, rather than from the set of all accounts. (It also hardcodes 1000 for the number of rounds instead of using the argument).

```auto
def run_with_unscrambling(accts, coins, rounds):
    for i in range(rounds):
        c1 = random.randrange(max(coins)+1)
        c2 = random.randrange(accts)
        value = int(coins.count(c1) ** random.random())
        coins = xfer(coins, c1, c2, value)
        coins = unscramble(coins, c1, c2)
    return coins
```

(I also think `xfer` might be unnecessary, since you could do the same thing by changing `unscramble` to define `k1` as `coins.count(c1) + value`.)

I expect that combining this kind of bilateral defragmentation with an operator balance that can move around freely in every transaction would provide a useful additional degree of freedom, although that will probably be a more complicated algorithm.

---

**vbuterin** (2018-09-18):

You’re right, there are two bugs in my code. Here’s the fixed version:

```auto
def run_with_unscrambling(coins, rounds):
    M = max(coins) + 1
    for i in range(rounds):
        c1, c2 = [random.randrange(M) for _ in range(2)]
        value = int(coins.count(c1) ** random.random())
        coins = xfer(coins, c1, c2, value)
        coins = unscramble(coins, min(c1, c2), max(c1, c2))
    return coins
```

This still leads to a low and stable level of fragmentation even after a large number of rounds, eg. with 25 accounts, 5000 coins and 10000 rounds I got 271, 267 and 290 fragments in my three trials, and going up to 50000 rounds I got 300, 260 and 296 fragments.

---

**vbuterin** (2018-09-18):

Edit: going up to 100 accounts, the fragment count goes up to ~2200. So it seems like in the limit \approx \frac{N^2}{4} fragments get created, which is high. I imagine it’s improvable with more intelligent defragmenting.

---

**ldct** (2018-09-18):

Might be worth noting that any compression scheme (where we make it cheaper to exit sets of coins with a certain structure) like this suffers from a 1:1 capital-lockup attack; for this scheme the attacker can buy a block of low-index coins (say {1, 2, … N}) and then send all the odd coins to other people; none of these coins can be exited anymore and they cannot be defragmented.

---

**vbuterin** (2018-09-18):

How is that a capital lockup attack? That’s just sending other people money that they cannot exit.

---

**ldct** (2018-09-18):

For example if in return for the money you send them, they send you some money that you can exit (eg in a payment channel)

---

**kladkogex** (2018-09-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> What claim are you looking to STARK prove? In general it should be possible to just make a STARK proof for an entire subtree in O(log(n))O(log(n)) time.

May be it is not relevant anymore, but people were thinking about doing non-inclusion proofs using SN(T)ARKS - may be it is not relevant



    ![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png)

      [Plasma Cash verification cost](https://ethresear.ch/t/plasma-cash-verification-cost/2727) [Plasma](/c/layer-2/plasma/7)




> If there is a Plasma block every minute, then if one holds a coin for a year the size of the non-spend proof for a payment is
> 60 * 24 * 365 * 100 * 10 * 256 = 17 Gbyte
> This assumes that an  average payment transfers 10 coins and that the depth of the Merkle tree is 100
> This needs to be multiplied by 2 because the receiver needs to send the change back. So it is 34 GByte total traffic
> How feasible is the entire payment then?  How long will it take for sender to upload and for receiver to down…

If there are lots of small coins there will be lots non-inclusions proofs - correct me I am wrong …

---

**gakonst** (2018-09-18):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> If there are lots of small coins there will be lots non-inclusions proofs - correct me I am wrong …

You can make the exclusion proof be for the subtree itself. If coins you have received have a different `parentBlock` because of different histories, you can make a transaction for all of them to yourself, and now they all have identical fields, which allows to do an exclusion proof for the whole subtree (credits [@ldct](/u/ldct))

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> as a condition of accepting a transaction from A sending coins to B, A and B would have to send each other coins in such a way that at the end, every coin held by A has a lower index than every coin held by B.

This means that it works only if all coins of small denomination have the same denomination right? Otherwise it’s not always possible (credits [@ldct](/u/ldct) again)

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This puts a heavy burden on the security of atomic swap protocols: each transaction is now an atomic swap. Here is one way to do this reasonably efficiently in Plasma Cash: Plasma Cash Minimal Atomic Swap.

For this to become practical, I believe we need a way of doing swaps between coins in 1 round, have you done any thinking on that?

---

**kfichter** (2018-09-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> For this to become practical, I believe we need a way for non-interactive swaps between coins, have you done any thinking on that?

Can you clarify what you mean by “non-interactive” here?

---

**kfichter** (2018-09-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> We can solve this problem by making the denomination very small, and allowing users to “multi-exit” a subtree of coins that all have the same owner with a single Merkle branch.

Does this require that each coin have the same denomination?

---

**gakonst** (2018-09-18):

I meant in 1 round, edited the original post. The good thing here is that the 2nd round of commitments is not necessarily done by the operator - i think! - (although it makes most sense to be done by them), and can be done by the interested parties (similar to Plasma XT).

This is regarding the Atomic Swap post so let’s take the discussion there

---

**vbuterin** (2018-09-19):

The goal of this specific design is that all bottom-level coins have the same denomination, but pretty much everyone deals with various 2^k-sized subtrees, not individual coins.

---

**augustoteixeira** (2018-09-20):

If such defragmentation is possible, there is another advantage to this design. Not only the exit proofs get batched, but the same reduction will be felt on the amount of data that needs to be provided to some recipient in order to convince her that a transfer is sound.

This is the case because if a whole collection of coins (power of two, contiguous and aligned) get no transaction inside a block or get all transfered to the same address, these coins need a single proof for that block. This reduces the proof storage burden, but makes some other designs more complicated, like Plasma XT, since such large amount of coins wouldn’t fit a bitmap on the main chain.

But I think this is just a matter of finding a good compression algorithm for these checkpoint masks which is efficient for defragmented data. So, instead of submitting to the main chain a bitmap indicating all coins that signed in for a checkpoint, the operator would submit a compact representation of the bitmask that everyone (including the Plasma contract) can use to check if a sub-branch got checkpointed or not.

One trivial design would be to only allow checkpoints of contiguous data at a certain fixed depth. In this case a bitmap for all the branches in that depth can be submitted. But I think that more heterogeneous designs should be investigated.

---

**ldct** (2018-09-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Given a 2k2^k sized subtree where every element is identical, a single branch of that tree is enough to provide the information needed to verify the entire subtree and sign off on behalf of it.

To elaborate on what [@gakonst](/u/gakonst) brought up: suppose you receive coin id 0 in block k and coin id 1 in block k+1, there are no other transactions, and you wish to exit the set of coins \{0, 1\}. In the design as written it seems like to exit you need a merkle proof from the transactions root of block k as well as another merkle proof from the transactions root of block k+1, correct?

---

**augustoteixeira** (2018-09-20):

I think in this case you could (without transacting on the main chain) transfer the two coins to yourself on the same block and then exit them with a single proof.

