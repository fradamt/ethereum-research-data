---
source: ethresearch
topic_id: 7061
title: Casper FFG paper - "Accountability Safety" proof (Theorem 1) and "finalized" term confusion
author: sea212
date: "2020-03-02"
category: Proof-of-Stake > Casper Basics
tags: []
url: https://ethresear.ch/t/casper-ffg-paper-accountability-safety-proof-theorem-1-and-finalized-term-confusion/7061
views: 1850
likes: 2
posts_count: 2
---

# Casper FFG paper - "Accountability Safety" proof (Theorem 1) and "finalized" term confusion

Hello ethresearch community,

this is my first (real) post, so please be lenient toward me.

Paper: [research/papers/casper-basics/casper_basics.pdf at 2a94a123efab844662da3be9a086c9b944fbab9c · ethereum/research · GitHub](https://github.com/ethereum/research/blob/2a94a123efab844662da3be9a086c9b944fbab9c/papers/casper-basics/casper_basics.pdf) (as of 2nd march 2020)

> Theorem 1 (Accountable Safety). Two conflicting checkpoints a_m and b_n cannot both be finalized.
> Let a_m (with justified direct child a_{m+1}) and b_n (with justified direct child b_{n+1}) be distinct finalized checkpoints as in Figure 3. Now suppose a_m and b_n conflict, and without loss of generality h(a_m)  h(a_{m+1}); then h(b_{j-1})  \textbf{I.} h(t_1) = h(t_2)

> \textbf{II.} h(s_1)  A checkpoint c is called \textit{finalized} if it is justified and there is a supermajority link c \to c^\prime where c^\prime is a \textit{direct child} of c.  Equivalently, checkpoint c is finalized if and only if: checkpoint c is justified, there exists a supermajority link c \to c^\prime, checkpoints c and c^\prime are not conflicting, and h(c^\prime) = h(c) + 1.

And the definition of the height function h:

> the height h(c) of a checkpoint c is the number of elements in the checkpoint chain stretching from c all the way back to root along the parent links

Using this definitions, b_n can not be a finalized checkpoint, even without Commandment II, since h(b_{n+1}) = h(b_n) + 3.

If the proof can stay in that form (I see that it’s valid if I am not strict with the terminology), I suggest to add “(Commandment II)” after the last word in the proof. Also I suggest to rename “condition I” to “Commandment I” in that proof.

Besides that, a general question:

If we take Figure 3 and remove the supermajority links on the blue path (left), the checkpoint chain on the pink path (right) would be valid. Nevertheless b_2 and b_3 would not be considered finalized. Is that volitional?

Edit: One more question, doesn’t a_3 already violate Commandment I, since h(a_3) = h(b_2)?

## Replies

**blacktemplar** (2020-03-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/sea212/48/4620_2.png) sea212:

> Using this definitions, b_n can not be a finalized checkpoint, even without Commandment II, since h(b_{n+1}) = h(b_n) + 3 .

If you follow the proof we consider n = 3 for this concrete example of Figure 3 and therefore

h(b_{n+1}) = h(b_4) = 7 = h(b_n) + 1 = 6 + 1. Therefore this shows that b_3 is finalized.

![](https://ethresear.ch/user_avatar/ethresear.ch/sea212/48/4620_2.png) sea212:

> Besides that, a general question:
> If we take Figure 3 and remove the supermajority links on the blue path (left), the checkpoint chain on the pink path (right) would be valid. Nevertheless b_2 and b_3 would not be considered finalized. Is that volitional?

Note that there may be many finalized checkpoints on one branch, the important thing is, that there will never be two conflicting checkpoints (checkpoints lying on one branch of the tree are not conflicting by defintion).

Despite that in this concrete example by definition b_2 is not finalized since h(b_3) \neq h(b_2) + 1.

![](https://ethresear.ch/user_avatar/ethresear.ch/sea212/48/4620_2.png) sea212:

> Edit: One more question, doesn’t a_3 already violate Commandment I, since h(a_3)=h(b_2) ?

No h(a_3) = 5 \neq h(b_2) = 3.

