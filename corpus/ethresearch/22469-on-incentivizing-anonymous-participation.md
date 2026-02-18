---
source: ethresearch
topic_id: 22469
title: On incentivizing anonymous participation
author: mikeneuder
date: "2025-05-26"
category: Economics
tags: []
url: https://ethresear.ch/t/on-incentivizing-anonymous-participation/22469
views: 931
likes: 7
posts_count: 1
---

# On incentivizing anonymous participation

## On incentivizing anonymous participation

\cdot

[![upload_0bca3fb7f6b0d2fc3fe0596f28531112](https://ethresear.ch/uploads/default/optimized/3X/a/7/a7631547fb904abc2dcdc72095a57e542c701cea_2_552x368.jpeg)upload_0bca3fb7f6b0d2fc3fe0596f285311121300×867 189 KB](https://ethresear.ch/uploads/default/a7631547fb904abc2dcdc72095a57e542c701cea)

\cdot

**tl;dr;** Blockchain activity is facilitated through independent actors participating in shared protocols. Incentivizing this participation is a critical design consideration, especially in permissionless, adversarial, and pseudonymous environments. We present a model and motivate the participation game in [Section 1](#p-54693-h-1-motivation-model-3). In [Section 2](#p-54693-h-2-symmetric-equilibrium-of-the-lottery-payment-rule-7), we analyze this game’s symmetric, anonymous equilibria. We then apply this framework in two settings. [Section 3](#p-54693-h-3-prover-market-cost-minimization-9) details prover markets, which aim to incentivize the generation of *at least one proof*. [Section 4](#p-54693-h-4-a-proof-of-work-objective-function-13) turns to Proof-of-Work protocols, which aim to incentivize *at least 50% participation* (motivated by the goal of avoiding a 51% attack). In both cases, we derive the optimal incentive structure for the protocol to minimize its cost. We conclude in [Section 5](#p-54693-h-5-conclusion-and-future-work-15) by discussing how the model can be extended and other blockchain-specific techniques used for bootstrapping participation.

\cdot

by [maryam](https://x.com/bahrani_maryam) & [mike](https://x.com/mikeneuder) – *may 26, 2025.*

\cdot

*Thanks to [Akilesh](https://x.com/akileshpotti), [Noam](https://x.com/noamnisan), [Matt](https://www.cs.princeton.edu/~smattw/), and [Barnabé](https://x.com/barnabemonnot) for review and discussion on this post!*

---

### Contents

[(1). Motivation & Model](#p-54693-h-1-motivation-model-3)

  [(1.1). Participation game model](#p-54693-h-11-participation-game-model-4)

  [(1.2). A trivial, non-anonymous solution](#p-54693-h-12-a-trivial-non-anonymous-solution-5)

  [(1.3). A non-symmetric equilibrium](#p-54693-h-13-a-non-symmetric-equilibrium-6)

[(2). Symmetric equilibrium of the lottery payment rule](#p-54693-h-2-symmetric-equilibrium-of-the-lottery-payment-rule-7)

  [(2.1). Considering large n](#p-54693-h-21-considering-large-n-8)

[(3). Prover market cost minimization](#p-54693-h-3-prover-market-cost-minimization-9)

  [(3.1). Optimizing for at least one participant](#p-54693-h-31-optimizing-for-at-least-one-participant-10)

  [(3.2). Asymptotics](#p-54693-h-32-asymptotics-11)

  [(3.3). The 1 + \ln c bound is tight](#p-54693-h-33-the-1ln-c-bound-is-tight-12)

[(4). A Proof-of-Work objective function](#p-54693-h-4-a-proof-of-work-objective-function-13)

  [(4.1). Asymptotics](#p-54693-h-41-asymptotics-14)

[(5). Conclusion and future work](#p-54693-h-5-conclusion-and-future-work-15)

  [(5.1). Alternative cost functions](#p-54693-h-51-alternative-cost-functions-16)

  [(5.2). Heterogeneous agents and information asymmetry](#p-54693-h-52-heterogeneous-agents-and-information-asymmetry-17)

  [(5.3). Tokens, airdrops, and blockchain applications](#p-54693-h-53-tokens-airdrops-and-blockchain-applications-18)

---

### 1. Motivation & Model

> Opening vignette – You are at your local sports bar and have a table to watch an NBA playoff game. You don’t want to watch alone, so you plan on letting the group chat know you are there. To make people more likely to come, you offer to buy the first round of wings, but you first need to decide how many to order. If you order too few, there is a chance no one shows up, thinking that someone else will go and there won’t be enough to go around. If you order too many, there won’t be room at the table if everyone comes. What is the optimal amount of wings to buy so that some, but not all, of your friends come?^1

This story often comes up in blockchain protocol design. Protocols want to attract participation in some form and use incentives to elicit it:

- Proof-of-Work offers block rewards to incentivize miners to solve cryptographic puzzles.
- Proof-of-Stake offers consensus rewards for staking and voting correctly on blocks.
- Prover markets coordinate the production of computationally intensive ZK proofs.

Crucially, blockchains also want to allow **permissionless participation**. This makes the coordination problem much more difficult. This post presents a model for incentivizing participation and analyzes the symmetric equilibria of anonymous, common-value payment rules. In particular, we study the equilibrium where each player plays the mixed strategy of purchasing a lottery ticket with probability p.

#### 1.1. Participation game model

We model the participation game as follows:

- player – A player is a strategic agent who, based on the mechanism, can choose to purchase an entry ticket.
- participant – A participant is a player who purchases an entry ticket.
- protocol – The protocol is an agent with a cost function (or, equivalently, a positive valuation function) for inducing participation.
- payment rule – A function implemented by the protocol that maps the set of participants to their respective payments.

Let there be n players in the participation game. Each faces the same entry fee, q and for simplicity, we use q=1 for the remainder of this post. Each participant can deterministically decide to join or not; they can also choose to play a randomized strategy where they join with some probability p. Before deciding whether to join, the participants observe a protocol-specified payment rule. The payment rule can depend on the realized set of participants and may be randomized. Each participant chooses an action to maximize their *expected utility*, meaning the expected payment they receive minus the entry fee (if they choose to participate).

The following two sections introduce the notions of anonymity and symmetry.

#### 1.2. A trivial, non-anonymous solution

Suppose the protocol aims to attract at least one participant and assume players tie-break in favor of participation. A straightforward mechanism follows: “Choose a specific player, denoted `WINNER`, and tell them you will pay them $1 if they participate.” This trivial solution has many desirable properties:

1. individual rationality for everyone (because each player can get utility zero by not participating), and
2. satisfactory participation in equilibrium (WINNER will participate, and no one else will), and
3. payment minimization for the protocol (because $1 is the ticket fee, and thus the smallest possible cost for getting a participant).

If the protocol designer is OK with choosing a winner, then this solution is sufficient.[^2](#fn2) Instead of stopping here, we focus on a set of solutions that are *anonymous.*

> Definition (informal): An anonymous payment rule cannot depend on the identity of the player.

We formalize this property in [Section 3.3](#p-54693-h-33-the-1ln-c-bound-is-tight-12), but hopefully, it should be intuitive. These payment rules *must* treat every player equally. The rules can depend on the players’ actions (e.g., by dividing the prize evenly among all participants that enter) and can be randomized (e.g., by giving the prize to a single participant randomly). However, the mechanism above relies on the player’s identity and is not anonymous.

#### 1.3. A non-symmetric equilibrium

Separately, consider the following scenario: “A single player, denoted `COMMITTER`, makes a public commitment to purchasing a ticket and becoming a participant.” Depending on the payment rule, this commitment may disincentivize other players from participating. For example, suppose the payment rule evenly divides a prize of $1 between all participants. In that case, a second player considering joining is guaranteed negative utility because they pay $1 and earn $1/2. This leads to no one else joining the protocol and `COMMITTER` earning the full prize. This equilibrium is **payment minimizing** for the protocol but requires participants to pick `COMMITTER`, pushing the coordination complexity to the players. We use this example as motivation to restrict our attention to [symmetric equilibria](https://en.wikipedia.org/wiki/Symmetric_equilibrium).

> Definition: In a symmetric equlibirium each player use the same strategy.

This strategy can be deterministic (e.g., always buy a ticket and participate) or mixed (e.g., buy a ticket with probability p). Since these deterministic strategies can be thought of as p=0 or p=1 respectively, any symmetric equilibrium is fully specified by a single value p\in[0,1]. In such an equilibrium, the number of participants is drawn from \text{Binomial}(n,p), where n is the number of players.

### 2. Symmetric equilibrium of the lottery payment rule

With our attention restricted to symmetric equilibria, there are only three outcomes for the players’ strategies:

1. no one joins (p=0),
2. everyone joins (p=1),
3. everyone joins with probability p\in (0,1).

Depending on the payment rule, any of these outcomes is possible. This section studies the lottery payment rule.

> Definition: A lottery payment rule pays a single player a prize of magnitude x by uniformly randomly selecting a winner from the set of participants.

The lottery payment rule is anonymous and induces a symmetric equilibrium p depending on the size of x. The protocol sets the value of x, the players decide whether or not to join, and the prize is given in full to one of the participants. If x<1, we are in case (1); no one will join because the prize is less than the entry fee. If x\geq n, then we are in case (2); everyone will participate because they are guaranteed (in expectation) to be paid more than their entry fee. For other values of x, the number of participants will be a random variable drawn from \text{Binomial}(n,p) with p\in (0,1). The protocol can shift the mean, np, by tweaking x.

We can characterize the symmetric equilibrium under case (3) above, where each player mixes their strategy and joins with probability p. (There are many approaches to it; we show the explicit one here using differentiation; see Aside #1 for an alternative.) We consider player  i‘s decision by fixing the other players’ strategies at p. i chooses its joining probability p' to maximize its expected utility,

\begin{align}
U_i(p') &= \bigg[ \underbrace{\mathbb{E}\left[\frac{x}{1+Y}\right]}_{\text{expected winnings}} - \underbrace{1}_{\text{ticket price}}\bigg] p', \; \text{where } Y \sim \text{Binomial}(n-1,p) \\
&= \left[x\cdot \frac{1-(1-p)^n}{np} -1\right]p'
\end{align}

In other words, player i receives a payment of x if she joins and wins the lottery among participants. In particular, since each of the other n-1 players joins independently with probability p, the number of participants beside i is drawn from \text{Binomial}(n-1,p). i's utility from joining is that payout minus the ticket price. i's utility from joining *with probability p'* is her utility from joining times p', since i gets 0 utility from not joining.

For the symmetric strategy p to be an equilibrium, p'=p must maximize this expression among all p'\in[0,1]. The first order condition is

\begin{align}
\frac{\partial U_i}{\partial p'} = x\cdot \frac{1-(1-p)^n}{np} -1.
\end{align}

Setting this to zero, we get an analytical solution for the relationship between x and p,

x\cdot \frac{1-(1-p)^n}{np} -1 = 0\implies  \boxed{x = \frac{np}{1-(1-p)^n}}

This tells us: “given a prize of size x, what probability p creates a symmetric equilibrium” or equivalently, “if the protocol designer desires the participant count to come from \text{Binomial}(n,p), they set a prize of size x.” The plot below shows the relationship between these variables for n=2.

[![upload_d625b6de301ed0283341dc168f71222a](https://ethresear.ch/uploads/default/optimized/3X/9/1/915cbf0411ded23ff22c1d3f2465694a3586edfc_2_364x349.png)upload_d625b6de301ed0283341dc168f71222a931×895 37.7 KB](https://ethresear.ch/uploads/default/915cbf0411ded23ff22c1d3f2465694a3586edfc)

The dashed lines are interpreted as, “if the protocol sets the prize x=1.5, then the strategy p=2/3 is a symmetric equilibrium.” Also, notice that if the prize is <1 or >2, the players join with probability 0 or 1, respectively. These are the “no one joins” and “everyone joins” outcomes described at the beginning of this section. For the interior region, x \in (1,2), a unique p is induced by each x.

> Aside #1 A different way of deriving the same equation is by considering the aggregate cash flow for the set of all players. For a given p, the set of players pays np in expected entry fees. Thus, the protocol will need to pay np in expectation as reimbursement (because this is a competitive equilibrium, any excess value will be competed away). When the protocol chooses a prize x, the set of players receives this prize as long as at least one player participates. This occurs with probability 1-(1-p)^n, meaning the set of players earn x \cdot (1-(1-p)^n) in rewards.

> Aside #2: One interesting property of mixed-strategy equilibria is that the player is indifferent to either action (which is why they randomize their behavior in the first place). In the above example, if everyone else joins with probability p, player i receives zero utility from any action. You can see this by plugging in x to her utility function,
>
>
> \begin{align}
>  U_i(p') &= \bigg[ x \cdot \frac{1-(1-p)^n}{np} -1\bigg] \cdot p' \\
>  &= \bigg[\frac{np}{1-(1-p)^n}\cdot \frac{1-(1-p)^n}{np} -1\bigg] p' \\
>  &= (1-1)p'\\
>  &= 0.
>  \end{align}
>
>
> Another way of interpreting this is that the equilibrium is fully competitive. This induces the indifference between outcomes and the resulting mixed strategy.

#### 2.1 Considering large n

Recall the relationship

x = \frac{np}{1-(1-p)^n}.

An interesting observation about this equation is that, for large n, we can rewrite x as a function of \mu=np (expected number of participants), using (1-x) \rightarrow e^{-x} for small x as

x(\mu) \approx \frac{\mu}{1-e^{-\mu}}.

The protocol can target a desired mean participation count \mu using this simple formula, *without knowing n*. For example, if the protocol wants a single participant in expectation, it should set a prize of 1/(1-1/e)\approx 1.582. That is, the protocol pays a 58\% premium over the entry fee of 1 to attract one participant in expectation. This approximation improves as n grows. The plot below shows the necessary protocol prize to attract one participant on average. It also shows the limit as n \to \infty approaches x(1)=1/(1-1/e).

[![upload_9cde4a87098e4108fb332832c204d531](https://ethresear.ch/uploads/default/optimized/3X/7/d/7da8da20f5383ab5ac6e3411b4e95a4112f7c9ae_2_371x349.png)upload_9cde4a87098e4108fb332832c204d531949×895 33.3 KB](https://ethresear.ch/uploads/default/7da8da20f5383ab5ac6e3411b4e95a4112f7c9ae)

The dashed lines can be interpreted as: “if n=10, then the protocol designer needs to set a prize of at least x=1.535 to attract one participant in expectation.” Of course, the protocol designer may choose a higher prize to reduce the risk of no participants. The following section describes this tradeoff formally.

### 3. Prover market cost minimization

So far, we have shown how the protocol can target a specific expected participation count, \mu, by varying x. We now consider protocols that are particularly averse to low participation. We formalize this by introducing a “low-participation penalty.” In this section, we start by examining prover markets. In [Section 4](#p-54693-h-4-a-proof-of-work-objective-function-13), we will look at a different low participation penalty motivated by Proof-of-Work consensus.

We consider a ZK rollup that wants to incentivize the costly production of proofs. The market designer may only care that *at least 1* prover participates (and pays the entry fee, which is the cost of generating the proof).[^3](#fn3) Further, say that if there is no participation at all, the protocol can generate the proof itself for a cost of c (you can think of c as the “outside option”). This allows us to write the low-participation penalty as a function of the number of participants, k, as

\begin{align}
\text{low-participation penalty}(k) =
\begin{cases}
c & \text{if } k = 0 \\
0 &\text{otherwise}.
\end{cases}
\end{align}

Naturally, a protocol designer wants to choose the payment rule that minimizes its total cost (the prize size plus any penalty).

#### 3.1. Optimizing for at least one participant

The analysis above allows the protocol designer to choose the magnitude of the prize to target a certain amount of participation under the symmetric equilibrium induced by the relationship between x and p. With the low-participation penalty, the protocol’s cost function, which we denote by C_p, is

C_p = c \cdot \Pr[\text{no participation}] + x \cdot \Pr[\text{participation}].

This cost is what the protocol seeks to minimize, and the protocol faces a tradeoff when choosing x when given c. Too low of a value of x results in the protocol incurring the penalty c with high probability; higher values of x are directly costly because the protocol has to pay a larger prize. Using the fact that in the symmetric equilibrium, each player participates with probability p, we can write,

C_p = c \cdot (1-p)^n + x \cdot (1-(1-p)^n).

With x = \frac{np}{1-(1-p)^n} (the relationship we derived above), this simplifies to

C_p = c \cdot (1-p)^n + np.

This is the protocol cost, which it seeks to minimize over p \in [0,1]. With the optimal probability p^*, the protocol can directly calculate the prize size needed to induce the symmetric equilibrium at p^*. We minimize the protocol’s cost using the first-order condition,

\begin{align}
    \frac{\partial C_p}{\partial p} &= -cn(1-p)^{n-1} + n =0 \\
    &\implies p^* = 1-c^{-\frac{1}{n-1}}
\end{align}

The second derivative is always negative over p \in [0,1], so p^* is indeed a unique local minimizer of the protocol cost. The following plot shows the protocol cost as a function of x (which has a bijection with p\in(0,1)) for n=2 and c=1.5,2,2.5, respectively.

[![upload_68cf7e34e09faa5dfee6d7ce96b8e0fb](https://ethresear.ch/uploads/default/optimized/3X/e/d/ed995c7e7e9f6938b090ded0156d1cae00c52b6b_2_621x445.png)upload_68cf7e34e09faa5dfee6d7ce96b8e0fb1246×895 62.3 KB](https://ethresear.ch/uploads/default/ed995c7e7e9f6938b090ded0156d1cae00c52b6b)

The x^* values (denoted as dots in the plot) are increasing in c because as the protocol faces a higher penalty for no participation, it chooses higher x^* (which results in a higher p^*) to be very confident that at least one player will participate. From p^*, we calculate the optimal prize size in closed form as

\begin{align}
x^* &= \frac{np^*}{1-(1-p^*)^n} \\
&= \frac{n(1-c^{-1/(n-1)})}{1-c^{-n/(n-1)}}
\end{align}

We also calculate the optimal protocol cost of

\begin{align}
C_p^* &= c \cdot (1-p^*)^n + np^* \\
&= n-(n-1) c^{-1/(n-1)}
\end{align}

The plot below helps visualize this cost as a function of n,c.

[![upload_32974a3ccb2b0fc03b6c63af46b5baa4](https://ethresear.ch/uploads/default/optimized/3X/b/6/b60bb98de3f97139342a7da487dea72d2d74657c_2_395x374.png)upload_32974a3ccb2b0fc03b6c63af46b5baa4945×895 66.1 KB](https://ethresear.ch/uploads/default/b60bb98de3f97139342a7da487dea72d2d74657c)

We see that as the low-participation penalty increases, the protocol cost seems to scale logarithmically. The next section formalizes this relationship by looking at the asymptotic behavior of the protocol cost.

#### 3.2 Asymptotics

A natural question arises about how the values of p^*, x^*, C_p^* scale as a function of c. In particular, a protocol designer may want to know how their utility scales as a function of c assuming a large number of players in the game, n. Expanding (see footnote[^4](#fn4) for derivation), we get

\begin{align}
p^* &= \frac{\ln c}{n-1} + O\left(\frac{(\ln c)^2}{n^2}\right).
\end{align}

Similarly, we can examine the asymptotic behavior of x^* (see footnote[^5](#fn5) for derivation), which is the optimal prize for the cost-minimizing protocol:

\begin{align}
x^* = \frac{\ln c}{1 - 1/c} + O\left(\frac{(\ln c)^2}{n}\right).
\end{align}

Finally, we examine the asymptotic behavior of the optimal cost paid by the protocol, C_p^* (see footnote[^6](#fn6) for derivation):

\begin{align}
C_p^* &=1 + \ln c + O\left(\frac{(\ln c)^2}{n}\right).
\end{align}

Critically, we see that as n\to\infty, the total cost of the protocol scales as 1+ \ln c. This is great for the protocol because it provides a logarithmic bound on the cost as a function of the outside option. Further, *the optimal cost doesn’t depend on n.* This is nifty in a permissionless setting because the protocol can set an optimal prize just based on the quality of the outside option (i.e., the low-participation penalty) without knowing how many players there are! It also means the protocol can be sure their costs are bounded even if the number of players in the game is very large.[^7](#fn7)

The next section answers the question, “can we beat this logarithmic bound?” More formally, *does an anonymous payment rule exist such that the resulting symmetric equilibrium has a protocol cost C_p < 1+\ln c?* We show in the following section that the answer is *no!* The protocol cost is tightly bounded by 1+\ln c.

#### 3.3 The 1+\ln c bound is tight

`Note for the math/formalism-averse crowd: this section can be safely skipped!`

We know that each player joins with probability p in the symmetric equilibrium. We need to formalize the anonymity property we sketched in [Section 1.2](#p-54693-h-12-a-trivial-non-anonymous-solution-5) to compare our mechanism with other anonymous payment rules. A payment rule \pi(S,r) takes as input the set S\subseteq [n] of participants that joined and a random seed r, and outputs a payment to each participant. The mechanism in the previous section pays a random participant the lottery prize x with probability 1/|S| if S is non-empty and pays no one otherwise. We say a mechanism  \pi(S,r) is *(ex-post) anonymous* if it’s pointwise symmetric with respect to the agent’s actions. Formally, \pi is *ex-post anonymous* if for all r and S and all permutations \sigma, \pi(S,r)=\pi(\sigma(S),r). When a mechanism is anonymous, we can rewrite its payment rule as \pi(S,r)=\pi(k,r) where k=|S| and is drawn from \text{Binom}(n,p). We now only care about the number of participants rather than the specific set.

Let \pi(k,r) be an anonymous mechanism with a symmetric equilibrium p. Then, the expected cost to the auctioneer is

C_p = \underbrace{c \cdot (1-p)^n}_{\text{no participation}} + \underbrace{\mathbb{E}_{k,r}[\pi(k,r)]}_{\text{participation}}.

This expectation is taken over the randomness realization, r, and each possible number of participants, k. In expectation, we know that each of the k participants must be individually rational to join the lottery. In aggregate, any protocol must pay *at least* each participant’s entry fee in expectation. Formally, \mathbb{E}_{k,r}[\pi(k,r)] \geq np. Plugging this in, we again arrive at the form

C_p \geq c \cdot (1-p)^n + np.

At equality, this is exactly the protocol cost for the lottery mechanism. So it has the same optimal protocol cost of C_p^* = n-(n-1) c^{-1/(n-1)} and asymptotic behavior of 1+\ln c as n \to \infty apply. **The lottery mechanism is optimal among anonymous and individually rational mechanisms in minimizing the “at least one player” objective!**

### 4. A Proof-of-Work objective function

In the previous section, the protocol incurred the cost c only if there was *no participation*, corresponding to the following step function in the number of participants, k,

\begin{align}
\text{low-participation penalty}(k) =
\begin{cases}
c & \text{if } k = 0 \\
0 &\text{otherwise}.
\end{cases}
\end{align}

This cost function makes sense for the prover market example, where a single participant is necessary because only a single proof will suffice to satisfy the protocol. In other blockchain contexts, different low-participation penalties (or general participation valuation functions) may make sense; for example, Proof-of-Work requires participation from many miners. Our participation framework can be applied to these more general contexts as well. Intuitively, we split the protocol cost in the following way

C_p : \text{low-participation penalty} + \text{prize used to induce participation}.

Different participation requirements in various settings will correspond to different first terms. The second term is always np in a lottery prize mechanism (i.e., the payment rule we use here, which is optimal by a similar argument to the one in [Section 3.3](#p-54693-h-33-the-1ln-c-bound-is-tight-12)).

To demonstrate generality, we chose another penalty function that captures the spirit of Proof-of-Work mining: the protocol incurs a penalty if less than 50% of the players participate. Again, this can be written as a step function, where the threshold for incurring a penalty is raised from 0 participants to fewer than n/2 participants,

\begin{align}
\text{PoW low-participation penalty}(k) =
\begin{cases}
c & \text{if } k < n/2 \\
0 &\text{otherwise}.
\end{cases}
\end{align}

If at least 50% of the players choose to participate, then the protocol can be sure that no malicious actor could acquire enough hash power to 51% attack the network. This is one way to represent the type of participation that Proof-of-Work protocols may seek to induce.[^8](#fn8) As before, to attract participation, the protocol specifies a lottery prize that results in the symmetric equilibrium where every player mixes with probability p, and we have the familiar relationship, x = \frac{np}{1-(1-p)^n}. Thus, the total protocol cost can be written as,

\begin{align}
C_p = c \cdot \Pr[k < n/2] + np, \quad k \sim \text{Binom}(n,p).
\end{align}

We can expand this to

\begin{align}
C_p = c \cdot \sum_{k=0}^{n/2} \binom{n}{k}p^{k}(1-p)^{n-k} + np.
\end{align}

For n=100 players, the figure below shows the probability that the number of participants k<50 (and thus the protocol incurs the PoW low-participation penalty) for various prize sizes, x.

[![upload_54c70df9f2113debd9038344ddb43a1d](https://ethresear.ch/uploads/default/optimized/3X/f/2/f20b2beb857d6204051eeaa2925cdec5d8ed6d9a_2_414x281.png)upload_54c70df9f2113debd9038344ddb43a1d1392×947 43.6 KB](https://ethresear.ch/uploads/default/f20b2beb857d6204051eeaa2925cdec5d8ed6d9a)

There are three regimes:

1. Small prize: When the prize is x\in[0,40], the resulting equilibrium value of p will be low and thus k 50.
3. Large prize: When the prize is x\in[60,100], the resulting equilibrium value of p will be high and thus k^1 See the [El Farol Bar problem](https://en.wikipedia.org/wiki/El_Farol_Bar_problem) for one variant of this problem. [![:right_arrow_curving_left:](https://ethresear.ch/images/emoji/facebook_messenger/right_arrow_curving_left.png?v=14)︎](#fnref1)

^2 Note that above, the protocol just wanted a single participant. Similarly, if the protocol wanted *k* participants, it could specify an appropriately sized subset of the total player pool and pay their entry fee. More generally, the protocol can optimize any objective function by finding the subset of players whose participation would minimize the protocol’s cost and promise to reimburse the entry fees of those players (and only those players) if they all join. [![:right_arrow_curving_left:](https://ethresear.ch/images/emoji/facebook_messenger/right_arrow_curving_left.png?v=14)︎](#fnref2)

^3 We assume players have homogenous proving costs; the protocol designer knows this cost exactly. Generalizing this to heterogeneous provers with unknown costs will be the subject of a future post. [![:right_arrow_curving_left:](https://ethresear.ch/images/emoji/facebook_messenger/right_arrow_curving_left.png?v=14)︎](#fnref3)

^4 Starting with p^* we rewrite,

p^* = 1-c^{-1/(n-1)} = 1-e^{-\ln c / (n-1)}.

Using the Taylor expansion of e^{-y} at 0 with y=\ln c / (n-1), we have,

\begin{align}
    p^* &= 1 - \Big[\underbrace{1- y + \frac{y^2}{2} - \frac{y^3}{6} + \frac{y^4}{24} - \ldots}_{\text{expansion of $e^{-y}$}}\Big] \\
    &= \frac{\ln c}{n-1} - \frac{(\ln c)^2}{2(n-1)^2} + \frac{(\ln c)^3}{6(n-1)^3} - \frac{(\ln c)^4}{24(n-1)^4} - \ldots \\
    &= \frac{\ln c}{n-1} + O\left(\frac{(\ln c)^2}{n^2}\right).
    \end{align}

[![:right_arrow_curving_left:](https://ethresear.ch/images/emoji/facebook_messenger/right_arrow_curving_left.png?v=14)︎](#fnref4)

^5 We first rewrite

\begin{align}
x^* &= \frac{n(1-c^{-1/(n-1)})}{1-c^{-n/(n-1)}} =\frac{n\bigl(1 - e^{-\ln c/(n-1)}\bigr)}{1 - e^{-n\ln c/(n-1)}}.
\end{align}

Using the Taylor expansion of e^{-y} at 0 with y=\ln c / (n-1), we have

\begin{align}
x^* = \frac{n\bigl(1 - e^{-y}\bigr)}{1 - e^{-n y}} &= \frac{n(1-e^{-y})}{1-c^{-1}e^{-y}}\\
&= \frac{n\displaystyle{y - \tfrac{y^2}{2} + \tfrac{y^3}{6} - \tfrac{y^4}{24} + \cdots}}
{\displaystyle{1-\tfrac1c (1-y+\tfrac{y^2}{2} - \tfrac{y^3}{6} + \tfrac{y^4}{24}+ \cdots)}} \\
&= \frac{\displaystyle{ny + O\left(ny^2/2\right)}}
{\displaystyle{1-\tfrac1c +O(y/c)}}\\[6pt]
&= \frac{\displaystyle \ln c + O\left(\frac{(\ln c)^2}{n}\right)}
{\displaystyle 1 -\frac1c+O\left(\frac{\ln c}{cn}\right)} = \frac{\ln c}{1 - 1/c} + O\left(\frac{(\ln c)^2}{n}\right).
\end{align}

[![:right_arrow_curving_left:](https://ethresear.ch/images/emoji/facebook_messenger/right_arrow_curving_left.png?v=14)︎](#fnref5)

^6

\begin{align}
C_p^* &= n-(n-1) c^{-1/(n-1)} \\
&= n- (n-1) e^{-\ln c / (n-1)}
\end{align}

Letting y=\ln c / (n-1) and again using the e^{-y} expansion, we have

\begin{align}
C_p^*
&= n - (n-1)\Big[1 - \frac{\ln c}{n-1} + \frac{(\ln c)^2}{2(n-1)^2} - \frac{(\ln c)^3}{6(n-1)^3} + \frac{(\ln c)^4}{24(n-1)^4} - \ldots\Big] \\
&= n - (n-1) + \ln c +O \left(\frac{(\ln c)^2}{n}\right) \\
&=1 + \ln c + O\left(\frac{(\ln c)^2}{n}\right).
\end{align}

[![:right_arrow_curving_left:](https://ethresear.ch/images/emoji/facebook_messenger/right_arrow_curving_left.png?v=14)︎](#fnref6)

^7 This analysis extends to the case where the protocol wishes to attract not just one but up to \log c participants. See [Section 4](#p-54693-h-4-a-proof-of-work-objective-function-13) for larger participation requirements. [![:right_arrow_curving_left:](https://ethresear.ch/images/emoji/facebook_messenger/right_arrow_curving_left.png?v=14)︎](#fnref7)

^8 Depending on how we define the set of players in the participation game, this description may not make as much intuitive sense. For example, if we consider the player set as the total available global compute that could be used to solve PoW puzzles, inducing 50 % participation is probably a bit overkill. We use this example because it is tidy, but more modeling of the specifics of the players would be necessary to make these results practical. [![:right_arrow_curving_left:](https://ethresear.ch/images/emoji/facebook_messenger/right_arrow_curving_left.png?v=14)︎](#fnref8)
