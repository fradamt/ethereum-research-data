---
source: ethresearch
topic_id: 21963
title: Transpiling a Halo2 circuit into CCS
author: pnyda2
date: "2025-03-16"
category: Cryptography
tags: []
url: https://ethresear.ch/t/transpiling-a-halo2-circuit-into-ccs/21963
views: 332
likes: 5
posts_count: 1
---

# Transpiling a Halo2 circuit into CCS

## TL;DR

Happy to release [halo2 ccs+](https://github.com/pnyda/halo2-ccs-plus/), a transpiler that converts [zcash/halo2](https://github.com/zcash/halo2) circuits (with or without lookups) into [CCS](https://eprint.iacr.org/2023/552) circuits. At the end of this post, we also go over Poseidon hash benchmarks for our transpiler and discuss our results.

## Preliminaries

[Plonkish](https://zcash.github.io/halo2/concepts/arithmetization.html) is a popular arithmetization used by various projects in the ecosystem, such as [ZCash](https://z.cash/), as well as [Scroll](https://scroll.io/). [Halo2](https://zcash.github.io/halo2/) is a popular proof system implementation that supports Plonkish arithmetization. It consists in 3 types of constraints: custom gates, copy constraints and lookup constraints. We point the reader to the [Halo2 book](https://zcash.github.io/halo2/) as an helpful resource to obtain more details.

The paper [Customizable Constraint System for Succinct Arguments](https://eprint.iacr.org/2023/552) introduced CCS, an arithmetization well-suited for folding schemes like [HyperNova](https://eprint.iacr.org/2023/573). CCS aims to generalize R1CS, Plonkish, and AIR simultaneously. While the paper defines an algorithm to convert a Plonkish circuit into a CCS circuit, there is to my knowledge no existing implementation capable of transpiling production-ready Plonkish circuits into CCS. To address this, I developed a transpiler that converts Plonkish circuits written in [Halo2](https://github.com/zcash/halo2) into CCS - using the [Sonobe](https://github.com/privacy-scaling-explorations/sonobe) implementation.

In CCS, we can define constraints equivalent to custom gates and copy constraints. However, lookup constraints do not have an equivalent representation in CCS. To address this, CCS authors introduced an arithmetization called CCS+, which combines CCS with lookup constraints. However, we found that CCS+ is not expressive enough to fully represent the lookup constraints used in the Halo2 ecosystem. We will discuss this further later.

## Challenges I faced

### Supporting multiple lookup tables

CCS+, as defined in the original paper, supports only one lookup table. However, Halo2 allows us to define multiple lookup tables. We managed to generalize CCS+ to support multiple lookup tables.

### Handling of dynamic lookups

CCS+, as defined in the paper, requires the lookup table to be a public fixed vector T. This means that (1) the lookup table cannot be private, and (2) witnesses cannot be part of a lookup table, as the PSE fork of Halo2 allows them to be.

That is why we chose to use zcash/halo2 instead of the PSE fork of Halo2. zcash/halo2 only supports public fixed lookup tables, which simplified our work. It might be in the interest of the community to formally define a revised version of CCS+ that supports dynamic private lookup tables, enabling the transpilation of circuits developed for the PSE fork of Halo2 into CCS.

### Handling of lookup inputs

Halo2 lets us constrain an [Expression](https://docs.rs/halo2_proofs/latest/halo2_proofs/plonk/enum.Expression.html) evaluated at each row to be in a lookup table. However, CCS+, as defined in the paper, does not allow us to constrain an arbitrary expression evaluated at each row to be in a lookup table. Thus, we needed to:

1. Evaluate the expression at each row in the original Plonkish table.
2. Append the evaluation results into the witness vector Z.
3. Constrain those new witnesses according to the expression, using CCS.
4. Constrain the new witnesses to be in a lookup table, using CCS+.

### Removing unconstrained witnesses

In Halo2, the height of a Plonkish table must be a power of 2. This means that when the number of rows required for the circuit does not exactly fit a power of 2, a lot of unconstrained padding cells must be introduced. For example, if you need only 129 rows, you must create a Plonkish table with a height of 256, leaving 127 cells unconstrained.

To achieve this, a custom gate is introduced that looks like `selector * constraint = 0`, where `selector` is a fixed column. The `selector` is assigned to be 1 for the rows where you want to enable the constraint (the first 129 rows in the example) and 0 for the rows where you want to disable the constraint (the last 127 rows in the example).

CCS doesn’t require these padding cells, so it’s desirable to remove them from the witness vector Z[[1]](#footnote-53404-1).

To effectively reduce the size of the witness vector Z, it was necessary to detect and remove cells that are either:

- Literally unconstrained, meaning there is no custom gate constraining the cell.
- Virtually unconstrained, meaning there are custom gates constraining the cell, but all of them will evaluate to 0 regardless of the assignments to advice/instance cells, due to assignments on fixed cells.

First, recall the CCS formula:

\sum_{i=0}^{q-1} c_i \cdot \bigcirc_{j\in{S_i}} M_j \cdot z = 0

Now, we show how to reduce the sized of Z, in three steps:

1. For some a, b, k, when we detect a situation where the k-th row of M_a \cdot Z is destined to be multiplied by 0 regardless of the assignments on Z, due to the existence of some M_b where the k-th row is a zero vector, we update the k-th row of M_a to be a zero vector. This has no effect on the overall constraint, as the k-th row of M_a had no impact on \bigcirc_{j \in S} M_j \cdot Z anyway.
2. For some i, after updating all M matrices, if the i-th column of all M matrices happens to be a zero vector, we can conclude that the i-th row of Z is either literally or virtually unconstrained, as it was referenced by none of the M matrices.
3. Remove Z[i] from Z.

## Benchmarks

CCS has an advantage over R1CS because it supports high-degree gates, resulting in fewer witnesses. This, in turn, leads to a smaller degree of the polynomials we need to commit to, which may contribute to faster proving times. In addition to this, CCS has an advantage over Plonkish as it supports witness deduplication. Unlike Plonkish, where we need to commit to the same witness multiple times, CCS eliminates the copy-constraint redundancy. This results in smaller witnesses, leading to smaller polynomial degrees to commit to, and potentially faster proving times[[2]](#footnote-53404-2)

With this in mind, we benchmarked effective witness size reduction when transpiling a production ready halo2 circuits to CCS.

### Poseidon hash

We transpiled [a Poseidon hash function implemented in Plonkish by Electric Coin Company](https://github.com/zcash/halo2/tree/main/halo2_poseidon) into CCS. Additionally, we compared the number of witnesses in the transpiled CCS circuit with [a Poseidon hash function implemented in R1CS by the circomlib team](https://zkrepl.dev/?gist=5cef0dde9ea4603810c9154394371289). Our benchmark code can be found [here](https://github.com/pnyda/halo2-ccs-plus/blob/e293a8109d5a3ab2863f8de769f3b3abdff63ff3/tests/poseidon.rs).

|  | CCS | Plonkish | R1CS |
| --- | --- | --- | --- |
| Witnesses | 142 | 320 (~2.25x) | 243 (~1.71x) |
| Constraints | 139 | 652[3] (~4.69x) | 240[4] (~1.72x) |

### Witness size reduction vs Plonkish

- Plonkish advice/instance cells: 320
- CCS witness length: 142
- Reduction ratio: ~0.44x

This reduction is largely due to the removal of unconstrained witnesses, as described above. The Poseidon hash implementation by Electric Coin Company only uses 12 copy constraints, so only 12 witnesses were removed due to these constraints.

### Witness size reduction vs R1CS

- R1CS witness length: 243
- CCS witness length: 142
- Reduction ratio: ~0.58x

This reduction is largely due to high-degree gates. The transpiled circuit has a degree of 5, compared to the circomlib implementation, which has a degree of 2.

### Constraints reduction vs Plonkish

- The number of custom gates: 10
- The number of rows in the Plonkish table: 2^6 = 64
- The number of copy constraints: 12
- The number of Plonkish constraints: 10 * 64 + 12 = 652[3:1]
- M matrices height in CCS: 139
- Reduction ratio: ~0.21x

This reduction is largely due to removal of disabled custom gates. In Plonkish arithmetization, there is no way for us to selectively apply a custom gate only on some rows. Rather, all custom gates are applied on all rows. We often workaround this by introducing selector columns, as described in previous section. This contrasts with CCS where we can selectively apply a constraint only on specific witnesses. Our transpiler exploits this fact, and generates minimal M matrices, in a sense that they don’t include the constraints generated from a custom gate applied at a row if the gate’s selector was turned off at the row. This leads to shorter height of M matrices, and smaller number of constraints.

### Constraints reduction vs R1CS

- A, B, C matrices height in R1CS: 240
- M matrices height in CCS: 139
- Reduction ratio: ~0.58x

This reduction is largely due to high-degree gates. The transpiled circuit has a degree of 5, whereas the circomlib implementation has degree 2.

## Conclusion

Although we believe there is plenty of room for optimization in the codebase, transpiling today runs in 4 seconds on an Intel Core i7 1260P… Contributions are welcome!

Thanks to [@Pierre](/u/pierre) for reviewing this post as well as the codebase and to [@CPerezz](/u/cperezz) for advising on Halo2 internals.  This work was done in the context of a grant with [PSE](https://pse.dev/).

1. While CCS itself doesn’t need padding cells, proof systems that use CCS might still require the witness vector Z to be a power of 2. Since this transpiler is agnostic to proof systems, this concern is not addressed in this implementation. ↩︎
2. See remark 5 in the CCS paper. ↩︎
3. Since Plonkish arithmetization has multiple types of constraints, we can’t compare this number directly to the height of A, B, C in R1CS. ↩︎ ↩︎
4. The parameters used in circomlib’s Poseidon implementation and the parameters used in halo2_gadgets’ Poseidon implementation slightly differ. ↩︎
