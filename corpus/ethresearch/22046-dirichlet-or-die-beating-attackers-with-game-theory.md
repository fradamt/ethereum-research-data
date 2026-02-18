---
source: ethresearch
topic_id: 22046
title: "Dirichlet or Die: Beating Attackers with Game Theory"
author: VaibhavVasdev
date: "2025-03-30"
category: Economics
tags: []
url: https://ethresear.ch/t/dirichlet-or-die-beating-attackers-with-game-theory/22046
views: 340
likes: 2
posts_count: 1
---

# Dirichlet or Die: Beating Attackers with Game Theory

**Tl;Dr**: This research establishes game-theoretic foundations for blockchain security through an adaptation of the Colonel Blotto game, proving: (a) In decentralized systems with heterogeneous subsystems, no pure-strategy equilibrium exists, necessitating probabilistic defenses; (b) A mixed-strategy Nash equilibrium emerges where players follow Dirichlet distributions with security thresholds \tau = B_D/\sum_{i=1}^k v_i and \alpha = B_A/\sum_{i=1}^k v_i, yielding adversarial success probabilities bounded by P(x_i > y_i) = \frac{\alpha}{\alpha+\tau} + \mathcal{O}(v_i^{-1/2}).

**Note**: This article is the first part to a two part series research. It aims at constructing the mathematical groundwork and the next part will focus on the practical implications, which have been briefly discussed in the tail end of the conclusion of this article. Please feel free to comment on this article, message me on this platform or mail me at [vaibhavvasdev63@gmail.com](mailto:vaibhavvasdev63@gmail.com)

---

## Introduction

Traditional security models inadequately capture the strategic dynamics between resource-constrained defenders and adaptive attackers. I bridge this gap through a Blockchain Blotto Game model, demonstrating that decentralized security fundamentally requires probabilistic strategies and proportional resource allocation. This research provides actionable insights for blockchain architects and security engineers seeking to fortify decentralized systems against rational adversaries.

The Colonel Blotto game was chosen as the foundational framework for this analysis due to its unique capacity to model *resource allocation conflicts across multiple heterogeneous fronts*—a structure that directly mirrors the security dynamics of decentralized blockchain systems. In traditional Blotto games, players strategically distribute limited resources to compete over geographically dispersed battlefields, with outcomes determined by relative investments. This mirrors the adversarial interaction in blockchain ecosystems, where defenders and attackers vie for control over subsystems (shards, consensus layers) of varying criticality.

---

## Model Formulation

### Blockchain Blotto Game

The adversarial interaction is modeled as a two-player zero-sum Blotto game [[1]](#footnote-53608-1) [[2]](#footnote-53608-2) between an Attacker (A) and Defender (D). The Attacker seeks to compromise k \geq 2 subsystems (shards, consensus layers) with heterogeneous values \{v_1,\ldots,v_k\}, while the Defender aims to protect them. Players allocate budgets B_A and B_D respectively across battlefields through strategies \mathbf{x},\mathbf{y} \in \mathbb{R}^k_+ satisfying \sum_{i=1}^k x_i = B_A, \sum_{i=1}^k y_i = B_D.

The payoff function reflects blockchain’s adversarial nature:

\pi_A(\mathbf{x},\mathbf{y}) = \sum_{i=1}^k v_i \mathbb{I}(x_i > y_i) \tag{1}

where \mathbb{I} denotes the indicator function. Ties (x_i = y_i) favor the Defender.

#### Assumption 1 (Incomplete Coverage) :

Total security resources are insufficient for the perfect protection:

B_D < \sum_{i=1}^k v_i \tag{2}

B_A < \sum_{i=1}^k v_i\tag{3}

Players possess complete information about budgets and battlefield values.

---

### Nonexistence of Pure-Strategy Equilibria

***Lemma 1*** (Marginal Advantage Exploitation) : For any pure strategies (\mathbf{x},\mathbf{y}) where \exists i,j with \frac{v_i}{y_i} > \frac{v_j}{y_j}, there exists \epsilon > 0 such that reallocating \epsilon from x_j to x_i yields:

\Delta\pi_A \geq \epsilon\left(\frac{v_i}{y_i} - \frac{v_j}{y_j}\right) > 0 \tag{4}

***Proof*** : Consider the smooth approximation \mathbb{I}_\sigma(x > y) = \frac{1}{1 + e^{-(x-y)/\sigma}}. The directional derivative when reallocating \epsilon from j to i is:

\begin{aligned}

\partial_\epsilon \pi_A\big|_{\epsilon=0}

&= \lim_{\sigma \to 0} \left[ \frac{v_i}{\sigma}\mathbb{I}_\sigma'(x_i - y_i) - \frac{v_j}{\sigma}\mathbb{I}_\sigma'(x_j - y_j) \right] \\

&= v_i\delta(x_i - y_i) - v_j\delta(x_j - y_j)

\end{aligned}

For x_i \neq y_i or x_j \neq y_j, the dominant term comes from the ratio comparison. By assumption \frac{v_i}{y_i} > \frac{v_j}{y_j}, therefore \exists \epsilon > 0 making \Delta\pi_A > 0.

***Theorem 1*** : Under Assumption 1, no pure-strategy Nash equilibrium exists in the Blockchain Blotto Game with k \geq 2 and non-uniform v_i.

***Proof*** : Assume a pure-strategy Nash equilibrium (\mathbf{x}^*,\mathbf{y}^*) exists. Defender’s optimality requires equal marginal losses:

\partial_{y_i} \pi_A = -v_i H(x_i^* - y_i^*) = \lambda \quad \text{for all } i \tag{5}

where H is the Heaviside function. This implies x_i^* - y_i^* = c constant \forall i. From budget constraints:

\sum_{i=1}^k x_i^* = B_A,\ \sum_{i=1}^k y_i^* = B_D \implies kc = B_A - B_D  \tag{6}

Let v_m = \max_i v_i. Defender can profitably deviate to:

y_i' =  \tag{7}

\begin{cases}

B_D & \text{if } i = m \\

0 & \text{otherwise}

\end{cases}

The attacker’s payoff becomes:

\begin{aligned}

\pi_A(\mathbf{x}^*,\mathbf{y}')

&= v_m\mathbb{I}(x_m^* > B_D) + \sum_{i\neq m} v_i\mathbb{I}(x_i^* > 0) \\

&\leq v_m\mathbb{I}(c > 0) + \sum_{i\neq m} v_i \\

&< \sum_{i=1}^k v_i \quad \text{(since } B_A < \sum v_i \text{ by Assumption 1)}

\end{aligned}

This contradicts (\mathbf{x}^*,\mathbf{y}^*) being an equilibrium, as the Defender can unilaterally reduce \pi_A.

---

### Probabilistic Defense Equilibrium

***Lemma 2*** (Dirichlet Marginal Distributions) : Let \mathbf{w} \sim \text{Dirichlet}(\alpha_1, \ldots, \alpha_k) with [[3]](#footnote-53608-3) \alpha_i > 0 \forall i, then:

1. Marginally : w_i \sim \text{Beta}(\alpha_i, \alpha_0 - \alpha_i) where \alpha_0 = \sum_{j=1}^k \alpha_j
2. \mathbb{E}[w_i] = \frac{\alpha_i}{\alpha_0}, \operatorname{Var}(w_i) = \frac{\alpha_i(\alpha_0 - \alpha_i)}{\alpha_0^2(\alpha_0 + 1)}

***Proof*** : Let X_j \sim \text{Gamma}(\alpha_j, 1) for j=1,\ldots,k be independent random variables, then:

w_i = \frac{X_i}{\sum_{j=1}^k X_j} \sim \text{Beta}(\alpha_i, \alpha_0 - \alpha_i)

since the ratio of a Gamma variable to the sum of independent Gamma variables follows a Beta distribution. The moments follow directly from the properties of the Beta distribution.

**Theorem 2** : Under Assumption 1, the Blockchain Blotto Game admits a mixed-strategy Nash equilibrium where:

1. Defender’s Strategy :  \mathbf{y} = B_D\mathbf{w}, \mathbf{w} \sim \text{Dirichlet}(\tau v_1, \ldots, \tau v_k)
2. Attacker’s Strategy :  \mathbf{x} = B_A\mathbf{z},  \mathbf{z} \sim \text{Dirichlet}(\alpha v_1, \ldots, \alpha v_k)
3. Security Parameters : \tau = \frac{B_D}{\sum_{i=1}^k v_i}, \alpha = \frac{B_A}{\sum_{i=1}^k v_i}

The success probability for any battlefield i satisfies:

P(x_i > y_i) = \frac{\alpha}{\alpha + \tau} + \mathcal{O}\left(v_i^{-1/2}\right) \tag{8}

***Proof : Defender’s Optimal Response*** : Given attacker strategy \mathbf{z} \sim \text{Dirichlet}(\alpha v_i), the defender minimizes:

\mathbb{E}[\pi_A] = \sum_{i=1}^k v_i P(B_A z_i > B_D w_i) \tag{9}

Using the transformation:

w_i = \frac{\tau v_i}{\sum_{i=1}^k v_i} \tilde{w}_i \quad \text{where} \quad \tilde{w}_i \sim \text{Beta}(\tau v_i, \tau(\sum_{i=1}^k v_i - v_i))

First-order optimality requires (derivation provided in Appendix A.3):

\frac{\partial \mathbb{E}[\pi_A]}{\partial y_i} = -v_i f_{x_i}(y_i) = \lambda \quad \forall i \tag{10}

where f_{x_i} is the Beta density. The solution f_{x_i}(y) \propto y^{\alpha v_i-1}(B_D-y)^{\alpha(\sum_{i=1}^k v_i-v_i)-1} satisfies:

\frac{\alpha v_i}{y_i} = \frac{\alpha(\sum_{i=1}^k v_i - v_i)}{B_D - y_i} \implies y_i = \tau v_i \tag{11}

***Attacker’s Optimal Response***

The Attacker’s optimal response follows from a symmetric analysis of the Defender’s problem. This is verified in Appendix A.1, where mutual best responses are shown to satisfy the Nash equilibrium conditions.

The Attacker’s optimization mirrors the Defender’s problem, differing only in the parameterization and the Attacker’s strategy follows analogously, showing the attacker’s best response to \mathbf{w} \sim \text{Dirichlet}(\tau v_i) is \mathbf{z} \sim \text{Dirichlet}(\alpha v_i) \quad \text{with} \quad \alpha = B_A/\sum_{i=1}^k v_i

***Equilibrium Verification***

Mutual best responses constitute a Nash equilibrium. The success probability decomposes as:

\begin{aligned}

P(x_i > y_i) &= \int_0^1 f_{z_i}(t)P\left(w_i < \tfrac{B_A}{B_D}t\right)dt \\

&= \frac{\alpha}{\alpha + \tau} + \int_0^1 f_{z_i}(t)\left[\Phi\left(\tfrac{t-\mu_i}{\sigma_i}\right) - \Phi_{\text{BE}}\right]dt

\end{aligned}

where \Phi_{\text{BE}} is the Berry-Esseen approximation. Applying the Berry-Esseen inequality [[4]](#footnote-53608-4) to z_i/w_i:

\left|P(z_i/w_i \leq t) - \Phi\left(\tfrac{t-\mu_i}{\sigma_i}\right)\right| \leq \frac{C(\mathbb{E}|z_i|^3 + \mathbb{E}|w_i|^3)}{\sigma_i^3} \tag{12}

with, \mu_i = \alpha/\tau,  \sigma_i^2 = \alpha(\alpha+\tau)/(\tau^3 v_i) and the third moment term yields \mathcal{O}(v_i^{-1/2})

The Berry-Esseen inequality establishes the convergence rate of P(x_i > y_i), with the third-moment term justifying the \mathcal{O}(v_i^{-1/2}) error bound. The complete derivations for the concentration of measures are provided in Appendix A.2.

---

## Conclusion

By quantifying security thresholds and deriving optimal Dirichlet-based resource allocation strategies, the framework enables practical trade-offs between subsystem criticality, budget constraints, and risk tolerance. For instance, cross-chain networks can apply the adversarial success probability bound P(x_i > y_i) \approx \frac{\alpha}{\alpha + \tau} to audit interchain security guarantees or allocate staking capital across heterogeneous zones.

First, I prove that pure-strategy equilibria cannot exist in decentralized systems with heterogeneous subsystems, formally justifying the industry-wide shift away from static defense mechanisms like fixed validator assignments.

Second, I derive optimal probabilistic strategies where defenders and attackers allocate resources according to Dirichlet distributions parameterized by subsystem values v_i and security thresholds \tau = B_D/\sum_{i=1}^k v_i, \alpha = B_A/\sum_{i=1}^k v_i.

Third, I demonstrate that adversarial success probabilities are bounded by P(x_i > y_i) = \frac{\alpha}{\alpha+\tau} + \mathcal{O}(v_i^{-1/2}) offering designers explicit trade-offs between subsystem criticality and resource allocation. By quantifying the security threshold \tau, I further enable principled budgeting for sharded ledgers [[5]](#footnote-53608-5) and cross-chain networks.

These principles extend to designing incentive-compatible consensus protocols, stress-testing decentralized applications, and optimizing monitoring resource distribution in real-time.

---

## Appendix: Technical Derivations for Equilibrium Verification

### A.1 Indifference Condition Verification

For Defender indifference across battlefields, the first-order condition requires:

\frac{\partial \mathbb{E}[\pi_A]}{\partial y_i} = v_i f_{x_i}(y_i) = \lambda \quad \forall i \tag{13}

Given x_i \sim B_A \cdot \text{Beta}(\alpha v_i, \alpha(\sum_{i=1}^k v_i - v_i)), the density is:

f_{x_i}(y) = \frac{y^{\alpha v_i-1}(B_D-y)^{\alpha(\sum_{i=1}^k v_i - v_i)-1}}{B_D^{\alpha\sum_{i=1}^k v_i-1}B(\alpha v_i, \alpha(\sum_{i=1}^k v_i - v_i))} \tag{14}

Taking the logarithmic derivative:

\begin{aligned}

\frac{d}{dy}\ln f_{x_i}(y)

&= \frac{\alpha v_i - 1}{y} - \frac{\alpha(\sum_{i=1}^k v_i - v_i) - 1}{B_D - y} \\

&= \frac{\alpha v_i}{y}\left(1 - \frac{1}{\alpha v_i}\right) - \frac{\alpha(\sum_{i=1}^k v_i - v_i)}{B_D - y}\left(1 - \frac{1}{\alpha(\sum_{i=1}^k v_i - v_i)}\right)

\end{aligned}

Under security parameter scaling \alpha v_i \gg 1:

\frac{d}{dy}\ln f_{x_i}(y) \approx \frac{\alpha v_i}{y} - \frac{\alpha(\sum_{i=1}^k v_i - v_i)}{B_D - y} \tag{15}

Equating across i yields the proportional allocation:

\frac{v_i}{y_i} = \frac{\sum_{i=1}^k v_i - v_i}{B_D - y_i} \Rightarrow y_i = \frac{B_D}{\sum_{i=1}^k v_i}v_i \tag{16}

#### Attacker’s Problem

The Attacker faces symmetric optimality conditions. Given Defender strategy \mathbf{w} \sim \text{Dirichlet}(\tau v_i), the Attacker maximizes:

\mathbb{E}[\pi_A] = \sum_{i=1}^k v_i P(B_A z_i > B_D w_i)

First-order conditions require:

\frac{\partial \mathbb{E}[\pi_A]}{\partial z_i} = v_i f_{w_i}(z_i) = \lambda \quad \forall i \tag{17}

Substituting the Defender’s Beta density:

f_{w_i}(z) = \frac{z^{\tau v_i-1}(1-z)^{\tau(\sum_{j=1}^k v_j - v_j)-1}}{B(\tau v_i, \tau(\sum_{j=1}^k v_j - v_j))}

Equating marginal gains across all i:

\frac{v_i z_i^{\tau v_i - 1}(1 - z_i)^{\tau(\sum_{j=1}^k v_j - v_j) - 1}}{B(\tau v_i, \tau(\sum_{j=1}^k v_j - v_j))} = \text{constant} \quad \forall i \tag{18}

This is satisfied iff \mathbf{z} \sim \text{Dirichlet}(\alpha v_i) with \alpha = B_A/\sum v_i, confirming mutual best responses.

---

### A.2 Concentration of Measures

For R_i = z_i/w_i with z_i \sim \text{Beta}(\alpha v_i, \alpha V_{-i}) and w_i \sim \text{Beta}(\tau v_i, \tau V_{-i}) where V_{-i} = \sum_{j=1}^k v_j - v_i:

**Assumption 2** (Large Subsystem Value):

The analysis assumes subsystem values satisfy v_i \gg 1, enabling asymptotic normality of Beta distributions through the Central Limit Theorem.

**Berry-Esseen Application**:

From Eq. (12), the Berry-Esseen constant C depends on the normalized third moments:

C = \frac{1}{2} \sup_{t \in \mathbb{R}} \left|\mathbb{E}\left[\left(\frac{z_i - \mu_i}{\sigma_i}\right)^3\right] - \mathbb{E}\left[\left(\frac{w_i - \mu_i}{\sigma_i}\right)^3\right]\right| \tag{19}

**Third Moment Calculation**:

For z_i \sim \text{Beta}(\alpha v_i, \alpha V_{-i}):

\mathbb{E}[|z_i - \mu_i|^3] = \mathcal{O}\left(\frac{\alpha v_i (\alpha V_{-i})}{(\alpha v_i + \alpha V_{-i})^4}\right) = \mathcal{O}\left(\frac{1}{(\alpha \sum_{j=1}^k v_j)^3 v_i}\right) \tag{20}

Symmetrically for w_i \sim \text{Beta}(\tau v_i, \tau V_{-i}). Substituting into Eq. 19:

C = \mathcal{O}\left(\frac{1}{\min(\alpha,\tau)^3}\right) \tag{21}

**Uniformity Across Subsystems**:

The Berry-Esseen constant C depends only on the security parameters \alpha = B_A/\sum v_j and \tau = B_D/\sum v_j, not individual v_i. Thus, the error bound:

\left|P(z_i/w_i \leq t) - \Phi\left(\tfrac{t-\mu_i}{\sigma_i}\right)\right| \leq \frac{C}{\sqrt{v_i}} \tag{22}

holds uniformly across all subsystems under fixed \alpha,\tau, with C independent of v_i.

---

### A.3 Measure-Theoretic Justification

**Theorem (Differentiation Under Integral Sign)**:

Let f(x,y) be measurable in y and differentiable in x, with |\partial_x f(x,y)| \leq g(y) where g(y) is integrable. Then:

\frac{d}{dx} \int f(x,y)dy = \int \partial_x f(x,y) dy

**Application to Defender’s Problem**:

For f_{x_i}(y_i) = \frac{d}{dy_i} P(x_i > y_i), we have:

1. Dominance: |f_{x_i}(y_i)| \leq \sup_y f_{x_i}(y)

1. Kovenock, D., Roberson, B. (2015) Generalizations of the General Lotto and Colonel Blotto Games Springer Economic Theory ↩︎
2. Hart, S. (2008) Discrete Colonel Blotto and General Lotto games | International Journal of Game Theory International Journal of Game Theory 36(3):441-460 ↩︎
3. Balakrishnan, N., Nevzorov, V. (2000) A Primer on Statistical Distributions Wiley ↩︎
4. Berry, A. (1941) The Accuracy of the Gaussian Approximation to the Sum of Independent Variates Transactions of the AMS 49(1):122-136 ↩︎
5. Kokoris-Kogias, E. et al. (2018) OmniLedger: A Secure, Scale-Out, Decentralized Ledger IEEE S&P: 19-34 ↩︎
