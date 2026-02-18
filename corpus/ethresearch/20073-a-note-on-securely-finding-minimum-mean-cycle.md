---
source: ethresearch
topic_id: 20073
title: A Note On Securely Finding Minimum Mean Cycle
author: 0xvon
date: "2024-07-15"
category: Privacy
tags: []
url: https://ethresear.ch/t/a-note-on-securely-finding-minimum-mean-cycle/20073
views: 2216
likes: 7
posts_count: 1
---

# A Note On Securely Finding Minimum Mean Cycle

This study is supported by an Ethereum Foundation R&D grant and is a collaborative work with Enrico ( [@enricobottazzi](/u/enricobottazzi) ), Masato ( [@0xvon](/u/0xvon) ) and Nam ( [namnc (Nam Ngo) · GitHub](https://github.com/namnc) ) from Ethereum Foundation.

**Abstract**

Executing graph optimization algorithms such as the Minimum Mean Cycle (MMC) while preserving privacy has significant potential for handling sensitive information between users and companies. For example, it enables multilateral netting to solve the Minimum Cost Flow (MCF) problem [4] without disclosing mutual debts, making it highly relevant for processes like netting among multinational corporations. Aly et. al. [2] proposed an algorithm using Multi-Party Computation (MPC) to execute the MMC problem. However, this approach is based on Karp’s algorithm [1], which was found by Chaturvedi et al. [3] to occasionally fail to detect cycles. In this study, we propose a revised protocol that corrects this issue and enhances its efficiency. We implemented our protocol using MP-SPDZ and confirmed that it correctly identifies the MMC, similar to traditional protocols. Our findings indicate that our proposed protocol operates correctly and more efficiently than Aly’s protocol, which reduces the time/round complexity from O(|V|^5) to O(|V|^3) and the space complexity from O(|V|^4) to O(|V|^2). Furthermore, we discuss potential improvements for even more efficient algorithms.

# 1. Introduction

### 1-1. Importance of Graph Theory Optimization

Graph theory optimization problems play a crucial role in various domains, from computer science and engineering to economics and finance. These problems involve finding the most efficient way to navigate, connect, or utilize network structures, and solutions to these problems have far-reaching implications for improving systems and processes.

One of the representative problems in graph theory optimization is the Minimum Cost Flow (MCF) problem, which aims to find the least costly way to send a certain amount of flow through a network. The MCF problem is foundational in numerous applications, providing critical insights and optimizations.

In the financial sector, particularly in Netting, the Minimum Cost Flow (MCF) problem is often addressed to optimize the settlement of transactions and reduce systemic risk [4]. Netting involves aggregating multiple financial obligations to streamline transactions, minimize risk, and enhance efficiency. However, one of the critical challenges in this context is maintaining the privacy and confidentiality of sensitive financial data. Traditional methods for solving the MCF problem may require exposing transaction details, leading to significant privacy concerns and potential security risks.

Beyond netting, the MMC problem and its solutions have a wide array of applications across various fields:

- Network Security: Enhancing security measures by optimizing the flow of information and resources while minimizing potential points of vulnerability.
- Supply Chain Management: Streamlining logistics and distribution networks to reduce costs and improve delivery times.
- Urban Planning: Developing efficient transportation systems by optimizing traffic flow and reducing congestion.

The Minimum Mean Cycle (MMC) problem is a crucial component in solving the MCF problem. The MMC problem focuses on identifying cycles in directed graphs with the minimum average weight, which is essential for detecting inefficient paths and optimizing network performance. By incorporating the MMC problem into the solution of the MCF problem, we can achieve more accurate and efficient outcomes.

To address the privacy concerns inherent in solving the MCF problem, we explore the use of Multi-Party Computation (MPC) to securely solve the MMC problem. MPC is a cryptographic approach that allows multiple parties to collaboratively compute a function over their inputs while keeping those inputs private. By applying MPC techniques, we can solve the MMC problem without exposing sensitive data, thus preserving the privacy of financial transactions and other confidential information.

### 1-2. Previous Work

Aly et al. [2] proposed a method to solve Karp’s MMC algorithm [1] using Multi-Party Computation. However, this approach has some problems and suffers from significant computational complexity and time consumption. Additionally, the Karp’s algorithm [1] was found by Chaturvedi et al . [3] to occasionally fail to detect cycles.

### 1-3. Our Contribution

in this study, we propose a novel approach that not only addresses these shortcomings but also offers a more efficient and practical solution for securely solving the MMC problem using MPC. Our proposed protocol aims to reduce computational and time complexities, enhance cycle detection accuracy, and ensure robust privacy protection. Our experimental results demonstrate a significant improvement in efficiency, with a reduction in time complexity from O(|V|^5) to O(|V|^3) and space complexity from O(|V|^4) to O(|V|^2).

# 2. Minimum Mean Cycle Problem

Minimum Mean Cycle Problem and its solution is defined by Karp in 1978 [1].

### 2-1. Problem Definition

Given a connected graph G(V,E) where V is a set of nodes and E is a set of edges, with defining these parameters:

- c_{i,j} \in C denotes the cost on the edge (i,j).
- d^k(i) denotes the minimum cost from node s to i that contains exactly k edges.

First of all, for any cycle X, the mean cycle is defined by:

\begin{equation}
\mu (X) = \frac{\sum_{uv \in X} c_{uv}}{|X|}
\end{equation}

Thus, the minimum mean cycle is:

\begin{equation}
\mu ^* = \min_{cycle X} \mu (X)
\end{equation}

Minimum Mean Cycle (MMC) Problem is the problem to find this \mu ^*.

### 2-2. Efficient MMC

The MMC problem is known as NP-hard, and Karp introduces an efficient algorithm for solving it. The solution is followed by 2 steps.

The first step, we call it as **Walk**, is to calculates d^k(i), which denotes minimum cost from node s to i that contains exactly k edges. Walk can be computed via the recurrence:

\begin{equation}
d^k(j) = \min_{(i,j) \in E} d^{k-1}(i)+c_{ij}
\end{equation}

Initially, d^0(j)=\infty, except for the source node d^0(s)=0

The second step is to calculate the minimum mean cycle by:

\begin{equation}
\mu^* = \min_{j \in V} \max_{0 \leq k \leq |V|-1} \left[ \frac{d^V(j) - d^k(j)}{|V| - k} \right]
\end{equation}

See Karp’s paper [1] for a proof of equation (4). Overall algorithmic complexity is O(|V| \cdot |E|), and the first step has a significant impact on the entire algorithm.

# 3. Aly’s Secure MMC Protocol

**Notation**

- [a] denotes secret shared or encrypted values of a
- [z] = _{[c]} [x]:[y] denotes the assignment that if [c] is one, [x] is assigned to [z] or [y] otherwise.

### 3-1. Protocol

Aly et. al. [2] provide algorithmic solutions to MMC problem in a secure multi-party and distributed setting. This protocol is constructed by 2 sub-protocols:

1. walk([C],[b]) \rightarrow [A],[walks]
2. mmc([A],[walks]) \rightarrow [\text{min-cost}], [\text{min-cycle}]

This corresponds to Steps 1 and 2 of Karp’s Algorithm in section 2.

In first sub-protocol, we have two inputs. The cost matrix [C]_{ij} denotes the cost of edge (i,j). It represents [\infty] for non-existing edges. The viable matrix [b]_{ij} denotes 1 if edge (i,j) doesn’t exist, and 0 otherwise.

From these inputs, we outputs two values. One is the 2-dimensional walk cost matrix [A] which [A]_{jk} records d^k(j). The other is 4-dimensional walk path matrix [walks] which [walks]_{ijkl} records the number of times the edge (i,j) is traversed by the shortest walk of length k from s to l. The algorithm is detailed as Protocol 3-1.

---

**Protocol 3-1. Aly’s Walk Protocol**

---

**Input**: A matrix of shared costs [C]_{ij} for i,j \in \{1,2,...,|V|\}, a binary matrix on viable adges [b]_{ij} for i,j \in \{1,2,...,|V|\}.

**Output**: A matrix of walk costs [A]_{ik} for i \in \{1,2,...,|V|\} and k \in \{0,1,...,|V|\}, a wak matrix [walks]_{ijkl} for i,j,k,l \in \{1,2,...,|V|\} encoding these walks.

1. [A] \leftarrow [\infty], [A]_{00} \leftarrow [0], [C] \leftarrow [C] + [\infty](1-[b])
2. for k \leftarrow 1 to |V|+1 do

for j \leftarrow 1 to |V| do

for i \leftarrow 1 to |V| do

[c] \leftarrow [A]_{ik-1} + [C]_{ij}
**end**

**end**

**end**

---

In second sub-protocol, we have two outputs. [\text{min-cost}] is the minimum mean cost. [\text{min-cycle}] denotes the 2-dimensional cycle matrix which [\text{min-cycle}]_{jk} is 1 if edge (j,k) is included in the cycle achieving \mu ^* and 0 otherwise. Here, \text{min-cycle} is s-j path with |V| edges whose cost is d^{|V|}(j), minus the s-j path with k edges whose cost is d^{k}(j). The details are provided as protocol 3-2. We note that we use the theorem that \frac{a}{b}>\frac{c}{d} \iff ad>bc to make a comparison of \frac{d^V(j) - d^k(j)}{|V| - k} without calculating the inverse.

---

**Protocol 3-2. Aly’s MMC Protocol**

---

**Input:** A matrix of walk costs [A]_{ik} for i \in \{1,2,...,|V|\} and k \in \{0,2,...,|V|\}, a walk matrix [walks]_{ijkl} for i,j,k,l \in \{1,2,...,|V|\} encoding these walks.

**Output**: The cost of the minimum mean cycle [\text{min-cost}], a matrix with the minimum mean cycle [\text{min-cycle}]_{ij} for i,j \in \{1,2,...,|V|\}

1. for j \leftarrow 1 to |V| do

[\text{max-cycle}],[\text{max-cost}] \leftarrow \phi
2. for k \leftarrow |V| to 1 do

[\text{a-num}] \leftarrow [A]_{j(|V|+1)} - [A]_{jk}
3. [\text{a-den}] \leftarrow |V|-k
4. [c] \leftarrow [\text{k-num}] \cdot [\text{a-den}]
**end**
[c] \leftarrow [\text{j-num}] \cdot [\text{k-den}] < [\text{k-num}] \cdot [\text{j-den}]
[\text{j-num}] \leftarrow _{[c]} [\text{k-num}]  : [\text{j-num}]
[\text{j-den}] \leftarrow _{[c]} [\text{k-den}]  : [\text{j-den}]
[\text{min-cycle}] \leftarrow _{[c]} [\text{max-cycle}] : [\text{min-cycle}]
[\text{min-cost}] \leftarrow _{[c]} [\text{max-cost}] : [\text{min-cost}]

**end**

---

**Complexity**

This method requires O(|V|^5) time/round complexity, from the conditional assignments to |V| \times |V| elements in [walks] matrix for |V|^3 loops (line i-3~4 of Protocol 1). And this method requires O(|V|^4) space complexity, due to 4-dimensional [walks] matrix.

### 3-2. Problem in Aly’s Protocol

Aly’s protocol implements Karp algorithm [1] in the secure manner. In karp’s alrogithm, we determine \text{min-cycle} like s-j path with |V| edges whose cost is d^{|V|}(j), minus the s-j path with k edges whose cost is d^{k}(j). However, Chaturvedi and McConnell [3] provides an counterexample which the cycle couldn’t detected with this method. Furthermore, they prove the following lemma.

**Lemma 1**

Let j be a vertex such that there exists k, where j and k are a minimizing pair. Every cycle on the length |V| edge progression from s to j of cost d^{|V|}(j) is a cycle of minimum mean cost. (See the proof on their paper [3].)

This lemma means that the cycle can be detected by traversing the edge progression from the last edge and marking the vertices visited by the walk until a previous marked vertex is encountered, from s-j path with |V| edges whose cost is d^{|V|}(j).

# 4. CM-based Secure MMC Protocol

**Notation**

- [a] denotes secret shared or encrypted values of a
- [z] = _{[c]} [x]:[y] denotes the assignment that if [c] is one, [x] is assigned to [z] or [y] otherwise.

### 4-1. Protocol

We propose a protocol that converts the minimum mean cycle detection from Aly’s protocol to one with Lemma1. In addition, a few changes have been made to the data structure. We name it “**CM-based Securely MMC Protocol**”, taking the initials of Chaturvedi and McConnell, who proposed Lemma 1.

CM-based protocol is constructed by 3 sub-protocols:

1. walk([C],[b]) \rightarrow [A],[ep]
2. mmc

mmcn([A],[ep]) \rightarrow [\text{min-cost}],[\text{minimizing-node}]
3. extract\text{-}cycle([\text{minimizing-node}],[ep]) \rightarrow [\text{min-cycle}]

Here, Aly’s second sub-protocol is divided into CM-based second and third sub-protocols.

In fist sub-protocol, For the most part, it is the same as Protocol 3-1, with one difference: Instead of [walks], we record the edge progression in a 2-dimensional matrix called [ep], which [ep]_{jk} means the edge that passes before one of j in the shortest s-j path with k edges. This change eliminates the need for extra |V|^2 loops to update [walks]_{..kj}. The algorithm is detailed as Protocol 4-1.

---

**Protocol 4-1. CM-based Walk Protocol**

---

**Input**: A matrix of shared costs [C]_{ij} for i,j \in \{1,2,...,|V|\}, a binary matrix on viable adges [b]_{ij} for i,j \in \{1,2,...,|V|\}.

**Output**: A matrix of walk costs [A]_{ik} for i \in \{1,2,...,|V|\} and k \in \{0,1,...,|V|\}, a matrix of walk edge progressions [ep]_{ij} for i,j \in \{1,2,...,|V|\}.

1. [A] \leftarrow [\infty], [A]_{00} \leftarrow [0], [C] \leftarrow [C] + [\infty](1-[b])
2. for k \leftarrow 1 to |V|+1 do

for j \leftarrow 1 to |V| do

for i \leftarrow 1 to |V| do

[c] \leftarrow [A]_{ik-1} + [C]_{ij}
**end**

**end**

**end**

---

In (a) of the 2nd sub-protocol, instead of computing [\text{min-cycle}], we detect the node j that achieves mmc. We call it minimizing node.

The algorithm is detailed as Protocol 4-2-a.

---

**Protocol 4-2-a. CM-based MMCN Protocol**

---

**Input:** A matrix of walk costs [A]_{ik} for i \in \{1,2,...,|V|\} and k \in \{0,2,...,|V|\}, a matrix of walk progressions [ep]_{ij} for i,j \in \{1,2,...,|V|\}.

**Output**: The cost of the minimum mean cycle [\text{min-cost}], the node achieving the minimum mean cycle [\text{minimizing-node}].

1. for j \leftarrow 1 to |V| do

 [\text{max-cost}] \leftarrow \phi
2. for k \leftarrow |V| to 1 do

[\text{a-num}] \leftarrow [A]_{j(|V|+1)} - [A]_{jk}
3. [\text{a-den}] \leftarrow |V|-k
4. [c] \leftarrow [\text{k-num}] \cdot [\text{a-den}]

**end**

[c] \leftarrow [\text{j-num}] \cdot [\text{k-den}] < [\text{k-num}] \cdot [\text{j-den}]

[\text{j-num}] \leftarrow _{[c]} [\text{k-num}]  : [\text{j-num}]

[\text{j-den}] \leftarrow _{[c]} [\text{k-den}]  : [\text{j-den}]

[\text{minimizing-node}] \leftarrow _{[c]} j : [\text{minimizing-node}]

[\text{min-cost}] \leftarrow _{[c]} [\text{max-cost}] : [\text{min-cost}]

**end**

---

In (b) of the 2nd sub-protocol, from [\text{minimizing-node}], we construct a back pointer which indicates s-j path with |V| edges whose cost is d^{|V|}(j) and extract a cycle from the back pointer. Compared to Protocol 3-2, instead of expanding [\text{min-cycle}] directly from [walks], the additional protocol is required. We follow Lemma 1 and consider any cycle included in the back pointer as a minimum mean cycle. The algorithm is detailed as Protocol 4-2-b.

---

**Protocol 4-2-b. CM-based Extract-Cycle Protocol**

---

**Input:** A minmizing node [\text{minimizing-node}], a matrix of walk progressions [ep]_{ij} for i,j \in \{1,2,...,|V|\}.

**Output**: A matrix with the minimum mean cycle [\text{min-cycle}]_{ij} for i,j \in \{1,2,...,|V|\}

1. [\text{backpointers}]_{0} \leftarrow [\text{minimizing-node}], [\text{next-index}] \leftarrow [\text{minimizing-node}]
2. for k \leftarrow |V| to 1 do

[\text{val}] \leftarrow [0]
3. for j \leftarrow 0 to |V|-1 do

[match] = j == [\text{next-index}]
4. [\text{val}] = _{[\text{match}]} [ep]_{jk}:[\text{val}]
5. [\text{match-index-matrix}]_{jk} = [match]

**end**
[\text{next-index}] = [\text{val}]
[\text{backpointers}].append([\text{val}])

**end**
**for** i \leftarrow 0 to |V|-1 do

1. [\text{counter}] \leftarrow [0]
2. for k \leftarrow 0 to |V| do

[\text{counter}] = [\text{counter}] + [\text{match-index-matrix}]_{ik}

[c] = [\text{counter}] >= 2
[\text{cycle-node}] = _{[c]} i : [\text{cycle-node}]

**end**
[\text{min-cycle}] \leftarrow [0],[\text{counter}] \leftarrow [0]
**for** k \leftarrow |V| to 1 do

1. [\text{edge-from}] \leftarrow [\text{backpointers}]_k
2. [c] = [\text{edge-from}] [\text{cycle-node}]
3. [\text{counter}] = [\text{counter}] + [c]
4. [c_0] = [\text{counter}] + 1
5. for j \leftarrow 0 to |V|-1 do

[c_1] = [\text{match-index-matrix}]_{jn-k}
6. [c_2] = [c_0]*[c_1]
7. for i \leftarrow 0 to |V|-1 do

[c_3] = [\text{match-index-matrix}]_{jn-k+1}
8. [\text{min-cycle}]_{ji} = [\text{min-cycle}]_{ji} + ([c_2] * [c_3])

**end**

**end**

**end**

---

**Complexity**

This ****method requires O(|V|^3) multiplications or communication rounds, from the conditional assignments of [A],[ep],[\text{min-cycle}] for |V|^3 loops (line i-2~3 of Protocol 4-1 and like iii-3 of Protocol 4-2-b). And this method requires O(|V|^2) space complexity, largely due to 2-dimensional matrixes. A table comparing the Complexity of each protocol is shown in Table 4-1 below.

**Table 4-1. Complexity Analysis of Secure MMC Protocols**

|  | multiplications/communication rounds complexity | space complexity |
| --- | --- | --- |
| Aly’s | O(|V|^5) | O(|V|^4) |
| CM-based | O(|V|^3) | O(|V|^2) |

### 4-2. Implementation

We have implemented CM-based Securely MMC protocol in naive secret sharing scheme using Python MP-SPDZ. And we confirmed that the minimum mean cycle was found reliably in a number of random edges, including the counterexamples shown by Chaturvedi et al [3].

# 5. Conclusion

In this study, we have proposed a more efficient protocol for solving the Minimum Mean Cycle (MMC) problem using Multi-Party Computation (MPC). Our CM-based approach not only addresses but also significantly improves upon the issues identified in Aly’s protocol. Specifically, our protocol reduces the time/round complexity from O(|V|^5) to O(|V|^3) and the space complexity from O(|V|^4) to O(|V|^2) compared to Aly’s protocol.

Despite these advancements, the complexity remains super-quadratic in terms of the number of nodes, which can pose practical challenges for very large graphs. To mitigate this limitation, we propose the following strategies:

- By exposing the graph’s topography, we can optimize the edge search to include only the minimum necessary edges, thereby reducing the time/round complexity to O(|V|^2 \cdot |E|). This approach, however, requires a trade-off with some degree of privacy.
- Implementing simpler algorithms that provide approximate or sub-optimal solutions, such as Greedy Algorithms and Distributed Algorithms, can further enhance practicality. These algorithms can significantly reduce computational overhead while delivering sufficiently accurate results for many applications.

In summary, our protocol offers a substantial improvement over existing methods, paving the way for more efficient and practical solutions to the MMC problem in secure computation settings. Future work will focus on refining these strategies to further balance the trade-offs between efficiency, accuracy, and privacy.

# Reference

1. Richard M. Karp, “A characterization of the minimum cycle mean in a digraph”, Discrete Mathematics, Volume 23, Issue 3, 1978, Pages 309-311, ISSN 0012-365X, https://doi.org/10.1016/0012-365X(78)90011-0.
2. Aly, A., Van Vyve, M. (2015). Securely Solving Classical Network Flow Problems. In: Lee, J., Kim, J. (eds) Information Security and Cryptology - ICISC 2014. ICISC 2014. Lecture Notes in Computer Science(), vol 8949. Springer, Cham. Securely Solving Classical Network Flow Problems | SpringerLink
3. Mmanu Chaturvedi, Ross M. McConnell, “A note on finding minimum mean cycle”, Information Processing Letters, Volume 127, 2017, Pages 21-22, ISSN 0020-0190, Redirecting.
4. Fleischman, T.; Dini, P. “Mathematical Foundations for Balancing the Payment System in the Trade Credit Market”, J. Risk Financial Manag. 2021, 14, 452. JRFM | Free Full-Text | Mathematical Foundations for Balancing the Payment System in the Trade Credit Market
