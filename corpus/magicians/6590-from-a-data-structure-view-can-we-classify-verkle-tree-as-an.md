---
source: magicians
topic_id: 6590
title: From a data structure view, can we classify Verkle Tree as an augmented finger tree with Kate Commitments as the augmented fn?
author: Shymaa-Arafat
date: "2021-07-03"
category: Uncategorized
tags: [kate-commitments, verkle-trees]
url: https://ethereum-magicians.org/t/from-a-data-structure-view-can-we-classify-verkle-tree-as-an-augmented-finger-tree-with-kate-commitments-as-the-augmented-fn/6590
views: 480
likes: 0
posts_count: 1
---

# From a data structure view, can we classify Verkle Tree as an augmented finger tree with Kate Commitments as the augmented fn?

I’m trying to write something about Verkle Trees from a different point of view, so pls tell me if this direction of thinking is wrong as a start …

Can Verkle Trees be viewed from the data structure community as an augmented finger tree

“A finger tree gives amortized constant time access to the “fingers” (leaves) of the tree, which is where data is stored”



      [en.wikipedia.org](https://en.wikipedia.org/wiki/Finger_tree)





###

In computer science, a finger tree is a purely functional data structure that can be used to efficiently implement other functional data structures.  A finger tree gives amortized constant time access to the "fingers" (leaves) of the tree, which is where data is stored, and concatenation and splitting logarithmic time in the size of the smaller piece. It also stores in each internal node the result of applying some associative operation to its descendants.  This "summary" data stored in the inter...










  [![image](https://ethereum-magicians.org/uploads/default/original/2X/c/c4c6a2b34db6ae88ede0173eb98904cab4984023.jpeg)](https://www.youtube.com/watch?v=xVka6z1hu-I)

with Kate Commitments as the associative operation?

“It also stores in each internal node the result of applying some associative operation to its descendants.”

Or this is not quite accurate???

.

I mean approaching the problem from the idea that luckily we can define what we call “+” operation on Elliptic Curves that happens to be linear& associative, and ECC is something we trust anyway.

Oh then, this brings to mind another question:

Does this mean Blake2b/Keccak256/… are not going to be used anymore???
