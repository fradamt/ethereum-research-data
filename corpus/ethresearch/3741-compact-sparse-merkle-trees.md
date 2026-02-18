---
source: ethresearch
topic_id: 3741
title: Compact Sparse Merkle Trees
author: farazhaider
date: "2018-10-08"
category: Layer 2 > Plasma
tags: [sparse-merkle-tree]
url: https://ethresear.ch/t/compact-sparse-merkle-trees/3741
views: 8616
likes: 8
posts_count: 18
---

# Compact Sparse Merkle Trees

A novel approach to SMTs which provides efficient non-membership proofs, allowing for the creation of new and faster blockchains similar to Plasma Cash.

You can find the full paper here https://osf.io/8mcnh/.

To achieve this C-SMT, we need to augment the tree nodes to contain a parameter called

max-key.

So for every non-leaf node, it’s two children will have max-key values representing the maximum key in their respective subtree. An incoming key to be inserted in this SMT would get put in the subtree for which it’s binary distance is closest. And it will recursively go down the tree following this approach until it reaches a leaf node.

The key gets inserted at this level and the hashes and max-key values are adjusted as we recurse back.

The path which the key follows down the tree is called minimum distance path and we call this approach for inserting a key as Minimum distance path algorithm.

You can read more about the approach in the paper link provided above.

## Replies

**vbuterin** (2018-10-08):

I’m not sure I fully understand the construction. In a normal sparse Merkle tree, if you’re deciding whether to include a value in the left or right subtree, you simply check the first bit of the key, and if it’s 0 go left and if it’s 1 go right. Here, it seems like you’re doing something different.

In this code:

```python
left = root.left
right = root.right
l_dist = distance(k, left.key)
r_dist = distance(k, right.key)
```

It seems like each subtree has a parameter called a “key”. Is this the same as the maxkey? What happens if the right subtree is empty; what’s the maxkey then?

Also, what is the argument that it’s nearly balanced? What happens if I introduce, in order, 0xfeeee…ee, 0xffeee…ee, 0xfffee…ee, 0xffffe…ee … 0xfffff…e, 0xfffff…ff? Wouldn’t that create a tree of depth ~256 with ~256 elements?

---

**farazhaider** (2018-10-09):

Hi [@vbuterin](/u/vbuterin), thanks for going through the paper.

The construction here indeed is different from a normal sparse Merkle tree.

The idea is to place every key in it’s correct subtree. To achieve that I calculate a parameter called **distance** which is defined as the binary separation between two keys.  This parameter will tell us whether incoming key will lie in either of the subtrees or will lie in it’s own subtree. For e.g, we have values **1** and **3** in the left and right node so our tree looks some thing like this.

```auto
        h(h(1)+h(3))
          /        \
         /          \
     h(1)          h(3)

```

Now consider an incoming key 2,  for left subtree distance(1,2) is 2 while for right subtree distance(3,2) is 1. So the key 2 lies in right subtree.

An incoming key 4 will have distance(1,4)  and distance(3,4) equal to 3. So in this case the key 4 does not lie in either of the subtree. And as 4 is greater than max-key 3, the root will become the left child and 4 will become the right child. For a key 0, the reverse will happen.

The parameter key for leaf node is the actual key. For inner nodes, the key parameter is max of it’s children’s keys. I have used the same parameter to make it more succinct.

No case occurs where one of the subtrees is empty, it’s either a leaf node, or a completer inner node so either 2 children or 0.

The tree gets nearly balanced as the hash function SHA256 behaves as an ideal hash function. The hash function SHA256 will take an input and output a value in the range of 0 to

2^256. This assumption is called random oracle model in cryptography.

The following explaination is taken from [here](http://www.ccs.neu.edu/home/wichs/class/crypto-fall15/lecture11.pdf).

The random oracle model is a model where all parties (e.g. algorithms, adversaries) have oracle access to a (uniformly) random function

RO :   \{0, 1\}^∗ → \{0, 1\}^n

(we can be flexible about the output length, but for now let’s just insist on n bits.)

We can think of this as whenever a fresh value x is queried, the oracle chooses a random

output y. The next time that x is queried, the oracle gives back the same y as previously.

Hope this answers your questions. Please let me know if you have any other comments, I’ll appreciate that.

---

**tawarien** (2018-10-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/farazhaider/48/2695_2.png) farazhaider:

> The idea is to place every key in it’s correct subtree

What does correct subtree mean in that regards is it just the condition that the Leaves are Ordered by key (in respect to a in-order Traversal), or is their more that defines the correct subtree?

Will this construction return the Same root hash when the tree contains the same elements or is the root hash dependent on the insertion order of the elements?

If seen that the construction supports Membership and Non-Membership Proofs is it possible to Proof a correct insertion or correct deletion to someone only having the root hash?

---

**farazhaider** (2018-10-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/tawarien/48/302_2.png) tawarien:

> What does correct subtree mean in that regards is it just the condition that the Leaves are Ordered by key (in respect to a in-order Traversal), or is their more that defines the correct subtree?

The correct subtree for a key to be inserted is the closest subtree in which the key lies.

Yes if you do an in-order traversal and exclude all non-leaf nodes, you’ll get an ordered list of keys.

Consider this tree, inner-nodes specify the max-key values and the leaf nodes contain the actual key.

```auto
           7
       /       \
     3           7
    / \         / \
  1     3     5     7
             / \   / \
            4   5 6   7

```

So if we want to insert  2, the correct subtree lies with 3

```auto
      x
    /  \
   2    3
```

So the algorithm will recursively reach till 3, and pair up 2 with 3, so the tree will look like this now

```auto
           7
       /       \
     3           7
    / \         /  \
   1    3      5    7
       / \    / \   / \
      2   3  4   5 6   7

```

![](https://ethresear.ch/user_avatar/ethresear.ch/tawarien/48/302_2.png) tawarien:

> Will this construction return the Same root hash when the tree contains the same elements or is the root hash dependent on the insertion order of the elements?

It will return the same root hash regardless of the order of insertion of elements. Because all element in both the case will end up at the same places.

![](https://ethresear.ch/user_avatar/ethresear.ch/tawarien/48/302_2.png) tawarien:

> If seen that the construction supports Membership and Non-Membership Proofs is it possible to Proof a correct insertion or correct deletion to someone only having the root hash?

Yes it is possible to prove an element is in the tree, the membership does exactly that. To prove an element does not exist in the tree, the non-membership proof gives you proofs of two closest key which bound the key for which it is being queried.

---

**farazhaider** (2018-10-09):

[@vbuterin](/u/vbuterin) [@tawarien](/u/tawarien)

I have released a framework which includes a module for Compact Sparse Merkle trees.

https://github.com/ZanjeerPlatform/bargad

---

**bharathrao** (2018-10-29):

Do you have a version in solidity and/or javascript?

---

**farazhaider** (2018-10-30):

Solidity is an Ethereum VM implementation so it wouldn’t make sense to implement this in it.

It could be implemented as Javascript library though, maybe someone can take up that implementation, the data structure is described extensively in the paper.

---

**bharathrao** (2018-10-30):

Regarding Solidity, wouldn’t you need the ethereum contract to verify the proof?

---

**eezcjkr** (2018-11-08):

[@farazhaider](/u/farazhaider) Thank you for this contribution. I have a few questions:

1.) Why do you need to take the log of the distance? Is it for performance reasons, i.e. making the bit-size of the values to compare smaller?

2.) Why did you choose xor as the distance measure, why not something like abs(key1-key2)?

![](https://ethresear.ch/user_avatar/ethresear.ch/tawarien/48/302_2.png) tawarien:

> If seen that the construction supports Membership and Non-Membership Proofs is it possible to Proof a correct insertion or correct deletion to someone only having the root hash?

I believe this is possible, but the max-key value needs to be hashed together with the children hashes. The way I see it:

Each node in the tree is of type TreeNode. TreeNode can be either of type Leaf or Parent.

Every Leaf has 2 properties: hash and key, and they are always the same: the key the leaf represents (and we can consider the associated value to be the preimage of the key).

Every Parent has 4 properties: key, hash, left and right. Left and right point to the respective children of the parent. The key property is the biggest key in the subtree that the Parent is the root of. The hash property is: sha3(left.hash ++ left.key ++ right.hash ++ right.key).

Hashing the max-key values was omitted in the paper, but I think this is problematic if we want to verify insertions in a smart contract, since the contract would need these values to perform an insertion, and we could fool it by lying about these values.

If we want to verify an insertion in a smart contract which only holds the root of the tree, we would pass the audit path to it. The contract would then verify the audit path like for any Merkle tree (the difference being that now the hashes include both the hash and the key property). After that it would perform the insert algorithm, for which it only needs the audit path, and store the new hash. And assuming the tree is approximately balanced, the audit path will always be logarithmic in the size of the tree.

EDIT: The above description implements a verifiable set, but not a map.

---

**farazhaider** (2018-11-13):

[@eezcjkr](/u/eezcjkr) Thanks for going through the paper.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/e/6a8cbe/48.png) eezcjkr:

> @farazhaider Thank you for this contribution. I have a few questions:
> 1.) Why do you need to take the log of the distance? Is it for performance reasons, i.e. making the bit-size of the values to compare smaller?
> 2.) Why did you choose xor as the distance measure, why not something like abs(key1-key2)?

1. It makes the computation less complicated and the log value directly maps to the levels in the trees so it makes the algorithm intuitive.
2. When we do the XOR of the two keys, we are trying to find the first bit which mismatches.
Subratcting the keys won’t give that information. For example, I want to insert a key 8.
And my tree has a key 7 and 9 present. 7 in the subtree 0–7 and 9 in the subtree 8–15.
abs(7-8) and abs(8-9) is the same and you won’t be able to decide which subtree to put 8 in.
While xor(7,8) and xor(8,9) is different and the key gets inserted into subtree 8–15

---

**tawarien** (2019-03-17):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/e/6a8cbe/48.png) eezcjkr:

> tawarien:
>
>
> If seen that the construction supports Membership and Non-Membership Proofs is it possible to Proof a correct insertion or correct deletion to someone only having the root hash?

I believe this is possible, but the max-key value needs to be hashed together with the children hashes.

After some time I have returned to this topic as and looked at the paper again and agree with eezcjkr, that wen have to hash the max-keys as well if insertion & deletion proofs should be supported in addition to membership & non-membership.

As in many applications the keys are hashes including them in the node hash will double the space required for a proofs ( 1x Key + 1x Node Hash per Proof Node).

So I tried to understood the intuition of the algorithm a bit better with the goal of reducing the space requirements for insert & deletion proofs. Here a a description from another perspective:

If we have a classical Sparse Merkle Tree and want to convert it into a Compact Sparse Merkle Tree. We can do this by replacing every subtree (non-leaf node) where its left or right child but not both is a non-default node (non-empty node/leaf) by its non-default child, and repeat this until no more replacements are possible. This eliminates all default nodes (unless the whole tree is empty) and each leaf ends up in its corresponding subtree. The remaining tree nodes are augmented by setting on each a key (or max-key) property to max(left.key, right.key).  If I’m not mistaken this would result in the same tree as if all the nodes would have been inserted over the proposed algorithm (or did i describe something different?).

The alternative construction I came up works as following. When starting with the classical Sparse Merkle Tree we augment all non-leaf nodes with a property called height which is the height of the subtree it is the root of (height(leaf) = 0, height(node) = height(node.left)+1 = height(node.right)+1). Now we do the same compaction as before but we do no longer need to add the max-key property.

Note that we only need n bits to encode the height of a tree containing keys with 2^n bits (The extra information is much smaller: 1 Byte for 32 Byte keys).

To traverse this tree at each node we look at the bit at position n in the key we are looking for (counting from the lsb) where n is the height-1 of the current node. If that bit is 0 we go left and if that bit is 1 we go right (similar to a classical Sparse Merkle Tree but we can skip sparse parts, but have to record heights as trade-off) if we reach a leaf we check if lookup key == leaf.key.

I claim that these two are equivalent because the decision to go left or right depends on a single bit in the lookup key which is the height and is derivable from the left & right max key.

(Bittpatterns of keys, || = concatenation, x = shared prefix l & r)

l = node.left = x||0||z   (x & z sequences of bits)

r = node.right = x||1||y  (x & y sequences of bits)

k = lookup key = a||b||c  (a & c sequences of bits, b single bit)

distance(l,k) = bxor(x,a)||b||bxor(z,c)

distance(r,k) = bxor(x,a)||not(b)||bxor(y,c)

Note: both start with bxor(x,a) and thus this part has no influence on which is the bigger number.  the log was ommited as it has no influence on which is the bigger numbe. It follows that:

if b > not(b) then bxor(x,a)||b||bxor(z,c) > bxor(x,a)||not(b)||bxor(y,c)

if b < not(b) then bxor(x,a)||b||bxor(z,c) < bxor(x,a)||not(b)||bxor(y,c)

Meaning the decision to go left or right is only dependent on the bit b and the position of bit b can be derived from l & r to be more specific it is rounded down distance(l,r), which is the first non-shared bit, which is the height -1 of the node ( as in a Sparse Merkle Tree each bit of a key corresponds to one level in the tree)

---

**ChosunOne** (2019-03-18):

Not trying to toot my own horn, but I believe I have something extremely similar to what is described in this topic at my Github, which I call a [Binary Indexed Merkle Tree](https://github.com/ChosunOne/merkle_bit) (Merkle-BIT).  It stores the min key from each branch as opposed to the max key, but essentially works the same.

---

**gcolvin** (2019-05-05):

A like your alternative construction, but how can it be built up by a series of insertions and deletions?

---

**tawarien** (2019-05-05):

To build a tree from updates and deletions we would have to treat the empty tree special as it can not be encoded in this scheme.

The first leaf inserted would simply become the root of the tree

If the last leaf is deleted the tree would become the special empty tree

Otherwise it would always work the same

Insertion is sadly a bit more complex then deletion or update.

**Insertion of key *ki* with value *vi*:**

1. Traverse the tree (as described in previous post) until we end at a leaf with key ke. (as it is an insertion ki != ke else it would be an update)
ki = a||b||c
ke = a||not(b)||d
where a is the shared prefix of the two keys and b is the first bit that is different
2. Calculate height =  n - bitLength(a)  //for n bit keys
3. Find the highest node nOld in the traversal path to ke where nOld.height < height
Note: a leaf counts as a node with height = 0
Hint: any leaf key under nOld would suffice as ke for example the maxKey from the original algorithm
4. Replace the node nOld with a node nNew
nNew.heigth = height
nNew.leftChild = if(b == 0) leaf(ki,vi) else nOld
nNew.rightChild = if(b == 0) nOld else leaf(ki,vi)

**Update of *ki* with value *vi***

1. Traverse the tree (as described in previous post) until we end at a leaf with key ki.
2. Replace the found leaf with leaf(ki, vi)

**Deletion of *ki***

1. Traverse the tree (as described in previous post) until we end at a leaf with key ki.
2. Replace the parent of the found leaf with the sibling of the found leaf

---

**gcolvin** (2019-05-13):

Thank you, [@tawarien](/u/tawarien)!

---

**tawarien** (2019-06-03):

It bugged me that the Insertion algorithm is complicated in my construction. The original construction did not have this problem as it is possible to find the insertion place while traversing because the current key could at each node be compared to the max-key and thus detect if a subtree does not contain the inserted key. My construction threw away the max-key and replaced it with the information necessary to navigate the tree but lost the information needed for early detection of non-membership.  Thus here is argumentation that re-enables that property without increasing the proof size

We replace the *heigth* property with a *common-prefix* property on each node (this is included in the node Hash): the *common-prefix* is the shared initial bits of all keys stored in the subtree of a node. The *common-prefix* of a leaf is just its key.

It has to be noted, that from the *common-prefix* the height can be restored:

*height* = *n* - bitLength(*common-prefix*) where *n* is the number of bits in a key.

The additional information allows to check at each node during traversal if *common-prefix* is a prefix of the lookup key and if not we know the key is not part of the tree and we can abort (in case of an insert we have found *nOld*)

In case we use this for proofs we do not have to include *common-prefix* of each node in the proof, it suffices to include *height*. The *common-prefix* value can then be restored from the lookup key & *height* as it is the key without the last *height* bits. If the wrong key is provided then the prefixes will be wrong and a different root hash is calculated (as *common-prefix* is included in the node hash).

With that in place Insert becomes:

**Insertion of key *ki* with value *vi* :**

1. Traverse the tree until we end at a node/leaf where common-prefix is not a prefix of ki. (if we do not find such a node, it is an update not an insert)
2. Replace the found node (called nOld) with a node nNew
common-prefix = sharedPrefix(nOld.common-prefix,ki)
b = nthBitOf(nOld.common-prefix, bitLength(common-prefix)) //index starts at 0
nNew.common-prefix = common-prefix
nNew.leftChild = if(b == 0) leaf( ki , vi ) else nOld
nNew.rightChild = if(b == 0) nOld else leaf( ki , vi )

---

**MarKus1** (2020-07-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Also, what is the argument that it’s nearly balanced? What happens if I introduce, in order, 0xfeeee…ee, 0xffeee…ee, 0xfffee…ee, 0xffffe…ee … 0xfffff…e, 0xfffff…ff? Wouldn’t that create a tree of depth ~256 with ~256 elements?

I think that this concern is right.

Correct me if I’m wrong, but following the algorithm steps I ended up with such tree.

