---
source: ethresearch
topic_id: 7265
title: Attestation aggregation heuristics
author: farazdagi
date: "2020-04-12"
category: Sharding
tags: [signature-aggregation]
url: https://ethresear.ch/t/attestation-aggregation-heuristics/7265
views: 5958
likes: 15
posts_count: 12
---

# Attestation aggregation heuristics

###### tags: eth2 algorithms

H!

**Context:**

I work at Prysmatic Labs, and at the moment looking for ways to improve how attestations are aggregated in [Prysm](https://github.com/prysmaticlabs/prysm) client. The problem is notoriously hard (as in NP-Complete hard), so I wanted to ask whether anyone has any suggestions on top of what I’ve already found.

Below is the self-contained abridged version of what I am working on, [full version](https://hackmd.io/@farazdagi/rJHy8gGD8) is also available. Please, let me know if there’re some approaches I’ve missed or if some of the explored approaches have more to them than I’ve noticed.

Any help in this exploratory analysis is highly appreciated!

## Background

In order to increase profitability, attestations must be aggregated in a way to cover as many individual

attestors as possible. There is an important invariant: overlapping attestations can not be merged/aggregated.

```auto
// Sample attestations:
A0 = [
    [0 0 0 1 0], // A
    [0 0 1 0 0], // B
    [0 1 0 1 0]  // C
]

// List can be transformed into:
A1 = [
    [0 0 1 1 0], // A + B, most profitable - will be used for BLS aggregation
    [0 1 0 1 0]  // C
]

// Or, even better:
A2 = [
    [0 0 0 1 0], // A
    [0 1 1 1 0]  // B + C, most profitable - will be used for BLS aggregation
]
```

The main objective is to **find an approximation algorithm that will result in a solution which is as close to the optimal one as possible**.

> Algorithms are analyzed using \alpha-approximation method, where 0 \le \alpha \le 1 is the approximation ratio, and an algorithm with a given value of \alpha produces solution which is at least \alpha times the optimal
> value.
>
>
> In our problem, solutions are scored by their cardinality: the more participants we have within a single aggregated item the better, with the maximum possible size equal to all the validators in a given committee.

## Formal Problem Statement

### Definition

**Def (Attestation Aggregation):**

AA(U, S, k) \to S'

Let U be a finite set of objects, where |U| = n. Furthermore, let S = \{S_1, ..., S_m | S_i \subseteq 2^U\} be a collection of its subsets, where \bigcup_{i = 1}^m S_i = U i.e. all u \in U are present in one of the elements of S. Then, **Attestation Aggregation** (AA) is the problem of finding S' \subseteq S that covers at least k \in [1..n] elements from U, and sets in S' are disjoint:

|\bigcup\limits_{T \in S'}T| \ge k

and

S'_i \cap S'_j = \emptyset, \forall i, j \in [1..m], i \ne j

Ideally, we want \bigcup\limits_{T \in S'}T to have maximum cardinality, that’s k = |U| i.e. all u \in U are covered by S':

|\bigcup_{T \in S'}T| = |U|

Since BLS doesn’t allow merging overlapping signatures, there’s that additional constraint of making sure

that all elements of S' are pairwise disjoint.

To summarize: given a family of sets S, we need to find a subfamily of disjoint sets S', which have the same (or close to same) union as the original family.

The problem is NP-Complete and only allows for logarithmic-factor polynomial-time approximation.

### Comparison to Known Problems

#### Attestation Aggregation (AA) vs Minimum Set Cover (SC)

In the MSC we have the very same input set system (U, S), but our target S' is a bit different: we want to find a full cover of U with minimal |S'|.

With AA, partial (if still maximal) coverage is enough, there’s no constrains on cardinality of S', and all elements of S' are pairwise disjoint.

#### Attestation Aggregation (AA) vs Exact Cover (EC)

Again, we start from the same set system (U, S), and the EC matches the ideal case of our problem when there exists an optimal solution within a given input S. So, if input list of attestations form (by itself or as any combination of its subsets) a full partition of U, the resultant S' for both EC and AA coincide.

There is on important difference in AA: it allows for partial covers.

#### Attestation Aggregation (AA) vs Maximum Coverage (MC)

In the [MC](https://en.wikipedia.org/wiki/Maximum_coverage_problem) problem, we want to find up to k subsets that cover U maximally:

|S'| \le k \land \mathop{argmax}\limits_{S'} |\bigcup\limits_{T \in S'}T|

Important thing to note is that in its conventional form MC doesn’t require elements of S' to be disjoint, which is a problem for our case – as overlapping attestations cannot be aggregated.

So, the important differences of AA include: no constraints on cardinality of S', requirement of pairwise disjoint elements in S'.

MC can still be utilized for our purposes: since there exists an approximation algorithm  with \alpha \approx 0.6 (pretty impressive) we can rely on it to build partial solution by gradually increasing k (see the Possible Solutions section below).

## Possible Solutions

So, our problem is closely related to set cover kind of problems to which there exist several possible approaches, none of which enjoys having a deterministically optimal solution.

Several closely related NP/NP-hard problems (and their variants) have been considered:

- Set Cover Problem
- Exact Cover
- Maximum Coverage Problem
- Set Packing
- Max Disjoint Set

### Set Cover

The [Set Cover problem](https://en.wikipedia.org/wiki/Set_cover_problem) is one of [Karp’s 21 NP-Complete problems](https://en.wikipedia.org/wiki/Karp%27s_21_NP-complete_problems).

It seems natural to start from the base covering problem because it serves as a foundation for other

problems, it has a greedy algorithm solver with ln(n) approximation to optimal, and with some effort

we can even make that greedy solver run in a linear time!

**Def (Minimum Set Cover):**

MSC(U, S) \to S'

Let U be a finite set of objects, where |U| = n. Furthermore, let S = \{S_1, ..., S_m | S_i \subseteq 2^U\} be a collection of its subsets, where \bigcup_{i = 1}^m S_i = U. Then, **Minimum Set Cover** (MSC) is the problem of covering U with a subset S' \subseteq S s.t |S'| is minimal.

Framed like that, this problem doesn’t abstract attestation aggregation completely. While MCS produces

a cover of U, S' may contain subsets with overlapping elements from U, and as such can’t be used as input to aggregation function. So, we need to add an extra constraint – making sure that all elements in S' are pairwise disjoint.

**Def (Minimum Membership Set Cover):**

MMSC(U, S, k) \to S'

The same set system as in MSC, with additional requirement on how many times each u \in U can occur in elements of S' i.e. \mathop{max}\limits_{u \in U} |\{T \in S'|  u \in T\}| \le k, for a nonnegative k \in [1..m].

![:star:](https://ethresear.ch/images/emoji/facebook_messenger/star.png?v=12) Applicability of MMSC:

- Decision version of the problem (whether S' exists) can be used to check for cover.
- When used as MMSC(U, S, 1) i.e. limit number of occurrences of u \in U to a single occurrence, we effectively transform problem to Exact Cover variant (which matches our ideal case exactly).

Another variant worth mentioning is Partial Set Cover, where we again are looking for S' of minimal cardinality (just as we do in MSC) which covers at least k elements from universe U.

**Def (Partial Set Cover):**

PSC(U, S, k) \to S'

Consider the same set system as in MSC, with additional parameter k \in [1..m]. Then, **Partial Set Cover** (PSC) is the problem of finding S' \subseteq S of minimal cardinality, that covers at least k elements of U.

**Partial Set Cover (PSC) vs Maximum Coverage (MC)**: PCS differs from Maximum Coverage problem in a subtle way: in the MC we limit number of subsets |S'| \le k, for maximum covered elements in U; in PSC we limit upper bound on how many items are covered |\bigcup\limits_{T \in S'}T| \le k with S' of minimal cardinality.

![:star:](https://ethresear.ch/images/emoji/facebook_messenger/star.png?v=12) Applicability of PSC:

- Again, decision version can be useful, to check the boundaries (gradually increasing k) of
S' existence. With k = |U| we effectively have MSC problem. In order for PSC be really useful,
we also need to constrain number of occurrences of u \in U within S' elements i.e. so that all subsets in S' are pairwise disjoint.

### Exact Cover

The [Exact Cover problem](https://en.wikipedia.org/wiki/Exact_cover) is one of [Karp’s 21 NP-Complete problems](https://en.wikipedia.org/wiki/Karp%27s_21_NP-complete_problems).

When exact cover exists within a given set system, the Exact Cover abstracts attestation aggregation perfectly. The problem is that perfectly non-overlapping partitions of U are not naturally happening in our system (so making them happen can be an attack vector when solving the problem ![:question:](https://ethresear.ch/images/emoji/facebook_messenger/question.png?v=12)).

**Def (Exact Cover):**

EC(U, S) \to S'

Let U be a finite set of objects, where |U| = n. Furthermore, let S = \{S_1, ..., S_m | S_i \subseteq 2^U\} be a collection of its subsets, where \bigcup_{i = 1}^m S_i = U. Then, **Exact Cover** (EC) is the problem of covering U with a subset S' \subseteq S s.t S'_i \cap S'_j = \emptyset, \forall i, j \in [1..m], i \ne j.

This NP-Hard problem has a nondeterministic backtrack solver algorithm ([Algorithm X](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X) by D.Knuth). The Algorithm X is capable of  finding *all* the optimal solutions to the problem.

However, having such an S that there exists a subcollection of pariwise disjoint subsets that cover U completely is a rare luck in our system. More than often S will not contain the solution to EC. In such cases, we still want some partial solution, even if only part of attesters can be collected within a single aggregation.

So, adding constraint similar to MMSC (where we limited number of times u \in U can occur in S'),  we need to transform the problem into accepting another parameter k \in [1..n], with the purpose of finding the S', where |\bigcup\limits_{T \in S'}T| \ge k i.e. union of elements of found subsets covers at least k elements of U. Then by gradually increasing k we want it to be as close to |U| as possible (max k-cover? ![:question:](https://ethresear.ch/images/emoji/facebook_messenger/question.png?v=12)).

![:star:](https://ethresear.ch/images/emoji/facebook_messenger/star.png?v=12) Applicability of EC:

- If solution exists, then Algorithm X (effectively implemented using DLX) can find it. If full solution is impossible, we need to explore possibility of finding partial cover.

### Maximum Coverage

**Def (Maximum Coverage):**

MC(U, S, k) \to S'

Let U be a finite set of objects, where |U| = n. Furthermore, let S = \{S_1, ..., S_m | S_i \subseteq 2^U\} be a collection of its subsets, where \bigcup_{i = 1}^m S_i = U. Then, **Maximum Coverage** (MC) is the problem of finding S' \subseteq S, |S'| \le k covering U with maximum cardinality, that’s

|S'| \le k \land \mathop{argmax}_{S'}|\bigcup_{T \in S'}T|

![:star:](https://ethresear.ch/images/emoji/facebook_messenger/star.png?v=12) Applicability of MC:

- With additional requirement of S_i \cap S_j, \forall i, j \in [1..m], i \ne j (pairwise disjoint sets in S') we can have a very useful mechanism to build approximate solutions using greedy approach.

## Summary and Further Work

So, possible solutions can be enumerated as following:

- Exact Cover (EC)

Can be used to check for solutions if situations when perfect solution exist are not rare.
- If combined with Partial Set Cover (PSC) for partial cover solutions, can match Attestation Aggregation perfectly.

**Maximum Coverage (MC)**

- Greedy algorithm + additional constraint of disjoint sets in S'
- Gradual increase of k (1 \to |S|) to obtain maximal cover for a maximum number of available attestations.

> The scope of this work is to find good enough heuristic to solve the Aggregation Attestation problem as defined in problem statement. There can be a highly effective ways to aggregate attestations that rely on how data is transmitted i.e. instead of concentrating on covering arbitrary set systems, we try to come up with heuristic that will result in a preferable attestations propagating the network (see Heuristically Partitioned Attestation Aggregation for a very interesting approach). Such or similar optimization will eventually be applied, but those are beyond the scope of this effort.

## Replies

**jcaldas84** (2020-04-13):

(first post in this forum, hi!)

Quick question: Can we make any reasonable assumption about the structure of the attestation matrix A0 (e.g. size, sparsity)?

---

**farazdagi** (2020-04-14):

Well, the matrix should start as sparse (rows - number of attestations from each validator, cols - number of validators), as attestations are gradually aggregated (with rows from merged ones discarded) and with possible duplicate messages, we start getting more dense matrix (it will have significantly less rows as well).

---

**lsankar4033** (2020-04-20):

Thanks for sharing these thoughts; this was very helpful for getting up to speed.

Out of curiosity, why limit solutions to those where a node sees the set of all attestations (and must pick  a minimum covering subset from that)? As you mentioned to in your endnote, there could be solutions that scope the problem each node has to solve by considering network propagation in the solution as well.

---

**kladkogex** (2020-04-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/farazdagi/48/4771_2.png) farazdagi:

> In order to increase profitability, attestations must be aggregated in a way to cover as many individual
> attestors as possible

Can you explain please what do you mean by increasing profitability, please.

You mean that the network is used more effectively if attestations are effectively aggregated?

---

**farazdagi** (2020-04-23):

Yep, basically that. Attesters are rewarded for the work done, and their work must be properly logged. So, we better not lose any information when aggregating.

---

**farazdagi** (2020-04-23):

I am limiting the scope of my current endeavour only - it is not the only optimization that Prysmatic plans to apply, in the long run. So, my immediate aim was to understand what are theoretical and practical limitations of the most straightforward solution (w/o involving changes to how overlay network is operated etc).

---

**aliatiia** (2020-04-28):

I think there is an efficient way to solve the Aggregation Attestation problem (AAP) **optimally**, not just find a good approximation. The **maximum-weight independent set** ([MWIS](https://en.m.wikipedia.org/wiki/Independent_set_(graph_theory))) problem  (not to be confused with the [maximal](https://mathworld.wolfram.com/MaximalIndependentVertexSet.html) independent set):

(1) captures the disjoint requirement of AAP

(2) captures the fact that not all attestations are equal by virtue of the weight attribute which maps to the total number of signatures are there in an attestation

(3) is NP-hard **but** admits a polynomial-time dynamic programming algorithm (DPA) assuming reasonable bounds on the total number of attestations (indeed bounded in ETH2)

(4) its DPA is well suited for the way attestations find their way in the subnet, in that clients can keep updating the DPA table(s) and memoizing partial solutions while still listening for more attestations on the wire.

### Reduction from AAP to MWIS:

- Construct a graph by creating a vertex v_n for each attestation X_n =(x_1x_2...x_c), where c is the number of validators per committee (= MAX_VALIDATORS_PER_COMMITTEE in ETH2 specs) and x_i\in \{0,1\} =1 if X contains a signature from validator i and 0 otherwise (i.e. x_i=1 \Rightarrow the i\text{-th} bit in aggregation_bits is 1). The “n” is a counter local to each aggregating validator client, so e.g. X_{n+1} is the attestation a client received on the wire after X_n (note: there will be 16 designated aggregators per slot per committee).
- Label each vertex v_n with weight w_n where w_n=H(X_n) is the Hamming weight of attestation X_n, i.e. it’s the total number of signatures in the attestation.
- Create an edge (v_n, v_m) \forall m > n   iff   H(X_n \wedge X_m) >0 for attestaions X_n and X_m, i.e. there’s an edge between any two attestations that have at least one BLS signature in common.

The graph is constructed incrementally, everytime an attestation arrives on the wire it is added as a vertex and then edges from older **overlapping** attestations are connected to it.

### Example:

The following graph corresponds to the sample attestations  A, B, and C  in the OP above:

%0

A

A

C

C

A->C

B

B

There is an edge from A \rightarrow C because they overlap on the 4th bit.

Suppose a new attestation D=(01100) arrives on the wire, then the graph becomes:

%0

A

A

C

C

A->C

D

D

C->D

B

B

B->D

Thus far the DP algo has memoized these potential aggregations:

| Aggregation candidate(s) | Total weight |
| --- | --- |
| {A} | 1 |
| {B} | 1 |
| {C} | 2 |
| {D} | 2 |
| {A, D} | 3 |

If now is the time to BLS-aggregate (reaching the end of `slot`) the client would aggregates A and D as the optimal choice. If two solutions are equally optimal clearly pick the one with less total attestations (less crypto).

The efficiency gain provided by the DPA is by virtue of the fact that when a new vertex v_j is appended to a path (v_i, v_k, ...,v_p, v_s), then we know that either we get more weight by including v_j and excluding v_s or vice versa (can’t be both), and in doing so **we need not re-compute the best trajectory up until v_p … the DPA memoized that and we’re now just reusing it.**

### Proof AAP is NP-hard:

The reduction above from AAP to MWIS  does **not** prove the NP-hardness of the AAP. For that we need to do the reverse: reduce a known NP-hard problem *into* AAP in polynomial time and logarithmic space.

Here is a reduction from [Exat Cover](https://en.m.wikipedia.org/wiki/Exact_cover) (EC) to AAP. Given the universe set X=\{x_1, x_2, .., x_n\} and the set of subsets S=\{S_1, S_2, ..., S_k\}  of an EC instance, create a corresponding AAP instance as follows:

- initialize |S| attestations A_1, A_2, ... A_k each as a sequence of n 0’s
- set the i\text{-th} bit in attestation A_j to 1 if x_i\in S_j
- solve this AAP, if the solution is empty return “no”, otherwise return the indices of attestations in the optimal solution as indices to the susbets in S in the optimal solution to the EC instance \blacksquare.

### Expected performance:

In ETH2 the number of attestations floating around in a subnet during a given `slot` is bounded and so **the** optimal solution can be found and no attestation should go to waste.

Rough back of the envelop calculations: if there are 128 validators in the committee each broadcasting 10 **unique** attestations to every other validator, then 10*128^2*480 bytes/[attestation](https://github.com/ethereum/eth2.0-specs/blob/9d39c292e020ee9243bd33de99208d884fb92517/specs/phase0/beacon-chain.md#attestation) \rightarrow a DPA table of size ~75mb in RAM. That’s a conservative upper bound though, because most of the time there are lots of duplicate attestations and (I think) clients aren’t simply flooding the subnet [[1](https://github.com/ethereum/eth2.0-specs/pull/1694/files), [2](https://github.com/ethereum/eth2.0-specs/pull/1706/files), [3](https://github.com/ethereum/eth2.0-specs/pull/1710/files)]  with attestations (b/c pubsub in the gossip protocol), so 128^2 is an exaggeration.

---

**farazdagi** (2020-06-13):

Sorry for a late reply - the last several weeks was working mostly on sync optimizations, only now getting back to AAP. The idea to turn `AAP` to `MWIS` is definitely something to consider, thank you for such an amazing writeup. This week I am working on implementing various heuristics and algos for the AAP, and I will definitely look into implementing MWIS DPA solver – we’ll see how that fares.

Thanks again, your suggestion is the exact kind of thing I was hoping to get, when shared the original post.

---

**michaelsproul** (2021-08-30):

Sorry to bump such an old thread, but doesn’t the dynamic programming algorithm you’re referring to for MWIS only work for trees? It’s the same as the one described here: https://courses.engr.illinois.edu/cs473/sp2011/Lectures/09_lec.pdf

I also think that the attestation aggregation problem as phrased is a bit strange. Attestation aggregation as it happens *live* on the network is mostly concerned with single-bit unaggregated attestations: validators need to group these and broadcast them ASAP when it’s their turn to aggregate. They shouldn’t wait until other aggregators have sent them aggregates, and as such shouldn’t be solving difficult optimisation problems at aggregation time.

IMO the tricky optimisation problem that does need solving arises when packing aggregates into blocks. You need to select up to k attestations from *all* subnets, and sometimes multiple aggregates from the same subnet if they overlap and this is the most profitable thing to do. This is where the maximum coverage problem is a much closer fit, but doesn’t take into account the fact that non-overlapping attestations could be aggregated for lower cost. The budget k is the `MAX_ATTESTATIONS_PER_BLOCK` constant, currently 128.

I’ve been thinking about how to solve the attestation packing problem (APP) and so far the best I can come up with is a two-stage process:

Construct a graph G with attestations as nodes, and edges between nodes when those attestations *can* be aggregated (the reverse of the edges used in the independent set formulation).

1. Solve the maximum clique enumeration problem for each sub-graph of G, i.e. enumerate all of the viable aggregates for each sub-graph.
2. Solve the maximum coverage problem on the set of all maximal cliques output from step (1). This allows us to select the best aggregates overall, including ones that might contain some overlapping signatures from the same validators.

The small number of aggregators expected on each subnet limits the size of the sub-graphs in (1) to around ~16 nodes, which *should* make them amenable to enumeration with an algorithm like [Bron-Kerbosch](https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm). Each sub-graph could also be enumerated in parallel. Solving max coverage can either be done with the approximation algorithm that most clients use today, or possibly integer linear programming.

---

**michaelsproul** (2022-11-30):

We (SigP) have a new blog post + technical report on the maximum clique approach:



      [Sigma Prime – 29 Nov 22](https://lighthouse-blog.sigmaprime.io/optimising-attestation-packing.html)



    ![](https://ethresear.ch/uploads/default/optimized/3X/b/7/b7c813ae274257808de12c5c447f88bbd80fd2c1_2_690x459.jpeg)

###



Optimality analysis of Lighthouse's attestation packing algorithm










We’re planning to push ahead with the maximum clique enumeration first, and then revisit the optimal solving of the max-coverage part of the problem further down the line.

---

**nibnalin** (2022-12-02):

Necroposting here but since there’s already some recent activity, it’s worth noting this problem was posed at an [SBC workshop](https://tselab.stanford.edu/workshop-sbc22/) and a group (including myself) realised we can in fact solve the underlying problem instead by creating a signature aggregation scheme which can handle unions of joint sets (not just disjoint set unions, as is assumed by the BLS aggregation scheme in this post). In particular, to create such a scheme we show a simple modification of the original BLS scheme by attaching a SNARK (bulletproof or other succinct proof in practice) that keeps track of the multiplicity of each aggregated signature. The use of this modified BLS scheme is described in the new [Horn proposal](https://ethresear.ch/t/horn-collecting-signatures-for-faster-finality/14219) and in much more detail in this [HackMD note](https://hackmd.io/@nibnalin/bls-multiplicity).

