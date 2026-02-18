---
source: ethresearch
topic_id: 9769
title: KVaC (Key-Value Commitments) for Stateless Validation
author: srini131293
date: "2021-06-07"
category: Cryptography
tags: []
url: https://ethresear.ch/t/kvac-key-value-commitments-for-stateless-validation/9769
views: 1971
likes: 0
posts_count: 3
---

# KVaC (Key-Value Commitments) for Stateless Validation

Hello everyone!

Shashank Agrawal and myself (Srini Raghuraman) would like to would like to share a new result on key-value commitments that we published in Asiacrypt recently (ia.cr/2020/1161). The talk given at the conference describing the construction can be found here: https://bit.ly/3w2GFCf.

The details of the construction can be found in the paper linked above, with the concrete description, appearing on page 22, also reproduced here for ease.

[![Screen Shot 2021-06-07 at 1.50.08 PM](https://ethresear.ch/uploads/default/optimized/2X/3/3ad1d82b80b9c690581302a341b5a9a214995b8b_2_351x500.png)Screen Shot 2021-06-07 at 1.50.08 PM986×1402 171 KB](https://ethresear.ch/uploads/default/3ad1d82b80b9c690581302a341b5a9a214995b8b)

Our commitment scheme KVaC (pronounced ‘quack’) allows one to commit to any number of key-value pairs and prove efficiently that a certain pair(s) is contained in the commitment. In particular, the commitment and the proofs consist of just two and three group elements respectively (in groups of unknown order like RSA/class groups). Verifying and updating proofs involves just a few group exponentiations, and so does additive updates to values.

We believe that KVaC could be a very good commitment scheme for building stateless clients. We found out that Verkle tries with Kate commitments are being considered for this purpose, so here we compare the two.

**KVaC vs KZG (Kate) commitments**

*Similarities*

- Both have very short commitments and proofs.
- Both support short multiproofs too: one can prove that the commitment contains several values with a proof whose size is the same as the one for a single value.

*Pros of KVaC*

- Kate relies on a trusted setup while KVaC doesn’t (if class groups are used). In Kate, the size of trusted parameters limits the number of values that could be committed.
- KVaC is a key-value commitment, a more general primitive than vector commitments. So KVaC could enable more use-cases than Kate.
- In KVaC, inserting new key-value pairs or updating the value of an existing pair is very efficient (just a few group operations in either case). The cost of these operations in Kate is not clear.

*Cons of KVaC*

- KVaC operates in groups of unknown order while Kate is defined in elliptic-curve groups. So group operations will be faster in Kate and the elements will be shorter. (However, verification in Kate involves pairings which tend to be expensive.)
- Commitment and proofs in Kate consist of just one group element whereas they consist of two and three group elements, respectively, in KVaC.

**Merkle Trees and Commitments**

KVaC could be used in a Merkle Tree like fashion just as Kate commitments. In other words, KVaC could be a replacement for Kate in Verkle Tries. In particular, just as proofs for different commitments could be combined in a clever way for Kate, one could also combine proofs from different KVaC commitments to produce a short proof for all the values.

We would be happy to discuss more! Looking forward to many conversations on this ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

## Replies

**Pratyush** (2021-06-08):

Cool paper [@srini131293](/u/srini131293) !

![](https://ethresear.ch/user_avatar/ethresear.ch/srini131293/48/5811_2.png) srini131293:

> Kate relies on a trusted setup while KVaC doesn’t (if class groups are used). In Kate, the size of trusted parameters limits the number of values that could be committed.

When deployed in Verkle tries I think this matters less, as you only need a setup of size corresponding to the arity of the tree, which for practical purposes is probably less than 2^15, and setups of this size have already been performed multiple times.

> KVaC is a key-value commitment, a more general primitive than vector commitments. So KVaC could enable more use-cases than Kate.

Is it not  possible to generalize the trie to support key-based lookups, as opposed to index-based lookups? (It might make updates a bit trickier, I guess).

---

**srini131293** (2021-06-18):

Thank you so much [@Pratyush](/u/pratyush), and apologies for the delayed response.

Yes, your observation regarding the setup size is absolutely true.

And yes, I believe that generalizing the trie would make updates harder, at least in a straight-forward way. However, one solution to that could be to use KVaC as the base commitment in a structure much like the trie. I believe a structure of this sort would be possible and also have the properties one would look for. Overall, it seems to be the case that a “Merklized” commitment would be the way to go in terms of getting the best of both world.

