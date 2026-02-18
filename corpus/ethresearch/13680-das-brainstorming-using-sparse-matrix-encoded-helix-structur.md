---
source: ethresearch
topic_id: 13680
title: DAS Brainstorming Using Sparse Matrix Encoded Helix Structure
author: ctrl-alt-lulz
date: "2022-09-14"
category: Sharding
tags: [data-availability, data-structure]
url: https://ethresear.ch/t/das-brainstorming-using-sparse-matrix-encoded-helix-structure/13680
views: 2576
likes: 0
posts_count: 4
---

# DAS Brainstorming Using Sparse Matrix Encoded Helix Structure

Just a highly experimental thought concept idea for brainstorming on data availability checking and compression.

Place binary data into encoded 4D Bit Arrays to create a double helix data structure

Double Helix Encoding in DNA

cytosine [C], guanine [G], adenine [A] or thymine [T]

Encoding for Binary Data

C - 00

G - 01

A - 10

T - 11

Arbitrary Strands in a Helix Group to Create a Matrix for Parity Checking

CGAT

AGCT

etc

That creates a sparse matrix of 0, 1s inside a helix grouping

The below illustrations are just; assume the 0s pad to create a true matrix.

Diagonal → Generate X

[CGAT, 0, 0, 0]

[0, AGCT, 0, 0]

[0, 0, GGCA,0]

[0, 0, 0, CCAT]

RLRL → Do this transformation

[0, 0, 0, CGAT]

[0, AGCT, 0, 0]

[0, 0, GGCA,0]

[0, CCAT, 0, 0]

Maybe using the rotation direction, spirals, and angles to encode the error correction logic can generate an “RNA” structure to reconstruct the full “DNA” structure more efficiently than reed-solomon.

Sparse data is by nature more easily compressed and thus requires significantly less storage. Some very large sparse matrices are infeasible to manipulate using standard dense-matrix algorithms.

Maybe that can allow additional more efficient error checking algorithms to be implemented without the additional overhead

http://web.mit.edu/julia_v0.6.0/julia/share/doc/julia/html/en/manual/arrays.html#Sparse-Matrices-1



      [en.wikipedia.org](https://en.wikipedia.org/wiki/Sparse_matrix)





###

In numerical analysis and scientific computing, a sparse matrix or sparse array is a matrix in which most of the elements are zero. There is no strict definition regarding the proportion of zero-value elements for a matrix to qualify as sparse but a common criterion is that the number of non-zero elements is roughly equal to the number of rows or columns. By contrast, if most of the elements are non-zero, the matrix is considered dense. The number of zero-valued elements divided by the tota Conce...











      ![](https://ethresear.ch/uploads/default/original/3X/1/f/1fcd562d26d31873d508f71af754d4884ca4d652.png)

      [errorcorrectionzoo.org](https://errorcorrectionzoo.org/kingdom/bits_into_bits)



    ![](https://ethresear.ch/uploads/default/optimized/3X/0/d/0dbe1b84873d4b63118d71aded2e06226a938b9e_2_690x362.png)

###



The Error Correction Zoo collects and organizes error-correcting codes.










[![Screen Shot 2022-09-14 at 1.56.38 PM](https://ethresear.ch/uploads/default/optimized/2X/8/8123302488a64424852633617754e49295252ad4_2_631x500.png)Screen Shot 2022-09-14 at 1.56.38 PM1044×826 244 KB](https://ethresear.ch/uploads/default/8123302488a64424852633617754e49295252ad4)

Reed solomon reference:

A very common R-S configuration is what is generally described as “(255,223)”. This means that the block size N is 255, which implies that the symbol size is 8 bits. The second number means that 223 (K) of these symbols are payload, and that 255-223 = 32 (t) bytes are parity symbols.

[![Screen Shot 2022-09-14 at 1.56.48 PM](https://ethresear.ch/uploads/default/optimized/2X/3/31eebecf6b01f162010a6bc8e7d23dde23e2a0e9_2_690x305.png)Screen Shot 2022-09-14 at 1.56.48 PM1024×453 94.4 KB](https://ethresear.ch/uploads/default/31eebecf6b01f162010a6bc8e7d23dde23e2a0e9)

## Replies

**ctrl-alt-lulz** (2022-10-20):

[![Screen Shot 2022-10-20 at 10.27.34 AM](https://ethresear.ch/uploads/default/optimized/2X/2/25e591d3fe88ba25a889f487d71b673622743818_2_690x304.jpeg)Screen Shot 2022-10-20 at 10.27.34 AM1920×847 112 KB](https://ethresear.ch/uploads/default/25e591d3fe88ba25a889f487d71b673622743818)

[![Screen Shot 2022-10-20 at 10.32.09 AM](https://ethresear.ch/uploads/default/optimized/2X/d/d2ff518abee19e1b15a6f3817db2d3a381cb101b_2_690x447.jpeg)Screen Shot 2022-10-20 at 10.32.09 AM1345×873 99 KB](https://ethresear.ch/uploads/default/d2ff518abee19e1b15a6f3817db2d3a381cb101b)

Some diagrams on how this could work

Now each bitfield segment can be checked against many different properties. The envelope must increase by a constant periodic amount, the area of the envelope - the area in the error correction curve, and applying the left and right rotations per period should cancel each other out. You could split the helix over frequency envelope crossing points, and randomly assign others to compare them against such rules without needing to have the whole helix structure. You only need to store half of the helix to generate a full error correction encoding, because the other half is just an inverse, so it can be calculated and then partitioned. Each bitfield encoding has a unique integral solvable area generated by the internally wrapped frequency within the envelope and its periodic step which wraps the bitfield row data.

matrix bitfield row = max length of envelope diameter = d or M

num of envelopes in data block = number of rows = L or N

total data size = matrix[M][N]

If the envelope is always constant over an interval period, eg 12s. Then it can just be represented using a trig func instead of having to be stored in full.

trig(x,y,z,t) → governs where data space is

The internal frequency  t_range = (t_start, t_end) as a subset of the full envelope t_env_range.

error_encoding_freq = dataFn(trig(x,y,z,t), trigPhaseShiftFn(x,y,z,t_range))

Store 010101… by default or whatever is the most likely data pattern that can be represented periodically. eg 011011…, or 110011… would do the same. If you have all the data for the total N rows, you can optimize a constant starting row that results in the least amount of phase shifts needed, and thus adds data compression. Each partition will then be given this row value for the N rows over M. One data integrity check can be the number of phase shifts applied in a t_range or what the total phase shift space size should be. And also each point can be compared to the next for relative phase difference and since each bit in the bitfield has a wrapped max, min governed by the envelope divided by the length of bitfield, there should be a predictable binary answer for the next bit, eg where your internal frequency crosses the double helix boundary.

Use a phase shift to flip a bit, or combine with frequency + phase for two bit flips. This lets you generate a frequency that can in worst case require ~N data, and in best case where it’s the default 0101, requires only one row value N to store if all the others over the time period M are identical (since it’s implied by design). So you only need to find the phase shifted data spaces to have the full data represented. Every matrix row now should equal the same starting value independent of row position in the helix when you apply the data and polar inverse phase frequencies together in that t_range.

You can compare any envelope’s phase shifts to others and combine that with other mathematical checks and statistical properties of how you distribute envelope partitions to validator groups to create a system with high data integrity checking & data compression properties.

You can also now take advantages of properties per envelope total phase shift size

encode_count_per_envelope is bound by

MaxP max phase shifts needed by any envelope over the t_range

MinP min phase shifts needed by any envelope over the t_range

EC encode_count_per_envelope

MaxP <= EC <= MinP

MaxP * EnvelopeCount <= Total EC Sum <= MinP * EnvelopeCount

Sum the encode_count_per_envelope over t_range, and that’s the total data space needed to encode your data. Any violation in any of the properties is how you can check data integrity. The more periodic element dimension & space properties you can add reference points the more efficient you can make it.

---

**ctrl-alt-lulz** (2022-10-20):

The center local envelope center frequency pole can be a reference point to all the over envelope side bands since it doesn’t have a polar peak representation and since it’s much easier to verify just one element is correct per envelope, this gives you confidence in your compass reference point that you can use to inspect it for data integrity locally and against other reference points.

---

**ctrl-alt-lulz** (2022-10-20):

You can then represent where these phase shifts are on a very sparsely populated matrix, adding a 1 where the envelope crossing exists in space to encode the phase shift space.

