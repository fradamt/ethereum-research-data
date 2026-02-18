---
source: ethresearch
topic_id: 3705
title: Limiting Last-Revealer Attacks in Beacon Chain Randomness
author: poemm
date: "2018-10-05"
category: Sharding
tags: [random-number-generator]
url: https://ethresear.ch/t/limiting-last-revealer-attacks-in-beacon-chain-randomness/3705
views: 3300
likes: 4
posts_count: 9
---

# Limiting Last-Revealer Attacks in Beacon Chain Randomness

It is an honor to post on this respected forum. Posting here was suggested by lrettig, [@cdetrio](/u/cdetrio), and [@chfast](/u/chfast), but any errors were introduced after their review.

The procedure below can be used to limit last-revealer attacks in randomness generation on the Ethereum 2.0 Beacon Chain. The full text below is copied from [paul.oemm.org/commit_reveal_subcommittees.pdf](http://paul.oemm.org/commit_reveal_subcommittees.pdf).

**Abstract.** The goal is for a committee to output a number with little or no bias. We consider the commit-reveal procedure (during the commit-period, each committee member publicly commits to a secret contribution to the final output, and during the reveal-period, reveals their secret) in which the last-revealer can create bias by choosing whether to reveal. We generalize commit-reveal by allowing each secret to be committed and revealed by a subcommittee of members, significantly reducing the probability of a last-revealer attack. Unfortunately, the proof is for existence – a lot of work remains in finding optimal parameters for this generalized procedure.

**1. Introduction**

Definition. A *committee number generation procedure* is an effective procedure for members of a committee to agree upon and output a number.

Definition. A *biased* committee number generation procedure is one in which committee member(s) can manipulate the output to take a specific form.

Remark. For the purposes of this document, we will not define a measure for bias, but just an axiom that more manipulation corresponds to higher bias.

Definition. A *honest* committee member never creates bias.

**2. Commit-Reveal**

Remark. Our focus is on commit-reveal procedures, which are designed to limit bias. Alternative procedures are not considered.

Definition. A *commit-reveal procedure* is a committee number generation procedure with steps

1. during a commit period, each party may commit to a secret by publishing its hash,
2. during a reveal period, each party may reveal their secret corresponding to the hash, and
3. revealed secrets are combined into an output value.

All secrets, hashing, revealing, and combining have predefined formats which all members agree are not vulnerable to bias.

Remark. If all parties are honest, i.e. commit independently of other secrets and reveal at the appropriate time, then we consider there to be zero bias.

**2.1 Non-Obligatory Commit-Reveal**

Definition. A *non-obligatory commit-reveal procedure* allows members who fail to commit or reveal to be ignored when combining reveals to form the final output.

Remark. An obligatory procedure may be attacked by members who refuse to reveal unless doing so creates bias. In the worst-case, they may refuse to ever reveal. We avoid these attacks by focusing on non-obligatory procedures.

**2.2 Ordered Commit-reveal**

Definition. An *ordered commit-reveal procedure* puts an order on when each member reveals its secret.

Definition. A *last-revealer attack* occurs when the last member to reveal decides whether to reveal based on the effect on the final output, creating bias.

Remark. Both ordered and non-ordered procedures are vulnerable to last-revealer attacks. Non-ordered procedures are especially vulnerable if a non-honest member can delay their decision to reveal until the end of the reveal-period, once most or all others have revealed. If one party controls the last several revealers, then they can reveal only certain ones, giving more bias. These attacks can even be forced by hindering communication channels. To limit these attacks, our focus is on the ordered procedure.

Remark. In an ordered procedure, influencing the ordering can influence who reveals last, which leads to a last-revealer attack. We assume a random ordering (perhaps the randomness comes inductively from earlier committee-generated numbers). We consider a model in which the probability of a last-revealer attack is equal to the ratio of dishonest members – i.e. each member has equal probability of being the last revealer.

**2.3. Subcommittee Commit-Reveal**

Definition. A *subcommittee commit-reveal procedure* partitions the committee into subcommittees, and each secret is committed and revealed by a subcommittee. For notation, we use ``n-subcommittee’’ to denote a n-member subcommittee.

Remark. This is a generalization of the special case with all 1-subcommittees.

Claim. Consider a large committee with ratio p of non-honest committee members, with 0<p<1. The ordered subcommittee non-obligatory commit-reveal procedure can have lower probability of a last-revealer attack if it is not limited to all 1-subcommittees.

Proof.

For all 1-subcommittees, the probability of a last-revealer attack is p, since p is the probability of a dishonest member as the last revealer. To prove the claim, we show a case in which having subcommittee(s) of size greater than one will result in smaller probability of a last-revealer attack. Consider a committee of all 1-subcommittees except the last subcommittee is a 2-subcommittee. Then the probability of a last-revealer attack is (for large committee approximately) p^2, since p^2 is the probability that both members of the last subcommittee are dishonest, since if at least one of the two is honest then they will reveal. Since p^2<p for 0<p<1, we have a lower probability of last-revealer attack, as desired.

Remark. Subcommittee procedures bring forth an *omniscience attack* – if an attacker knows all secrets during commit-time, then they may have complete bias on output by choosing appropriate secret(s). Fortunately, this attack can be reduced to arbitrarily small probability by adding enough early-revealing 1-subcommittees, with probability of omniscience attack decreasing exponentially(!) with each additional 1-subcommittee. The last subcommittee(s) can still have many members, with probability of last-revealer attack decreasing exponentially(!) with each additional member. So there is a trade-off between probability of last-revealer attack and omniscience attack, but each can be made arbitrarily small by choosing subcommittees of appropriate size with appropriate ordering.

**3. Conclusion**

Remark. We have reduced the problem of a public commit-reveal procedure to a composition of procedures by subcommittees. Current work follows.

1. How to generate a number among each subcommittee. Perhaps recursively perform a subsubcommittee procedure. But the subcommittee problem is different because the secret should be kept private by the subcommittee until reveal-time, and there is less vulnerability to last-revealer attack. Depending on parameters and requirements, a reasonable choice may be Diffie-Hellman generalized to many parties. At least one member would have to reveal the subcommittee’s true shared secret along with everything required to verify it.
2. Model new attacks where a single party controls many committee members, can buy secrets early, or even competes with other dishonest members.
3. Find the optimal sizes of subcommittees as a function of full committee size and ratio of honest members. We have already derived formulas for some of the counting problems, and are working on numerically plotting probabilities for small committee sizes, and also hope to analytically solve for optimal subcommittee sizes. Heuristically, half of the committee members could be 1-subcommittees which reveal earlier, and the rest on subcommittees of size one greater than the subcommittee which reveals just before them.

If there is existing work in any of these directions, this author would be grateful for a hint.

## Replies

**dlubarov** (2018-10-06):

Hey Paul – interesting idea, thanks for sharing this work!

Would subcommittee members use public key encryption to communicate the secret within the subcommittee without revealing it to outsiders?

![](https://ethresear.ch/user_avatar/ethresear.ch/poemm/48/2402_2.png) poemm:

> Then the probability of a last-revealer attack is (for large committee approximately) p^2, since p^2 is the probability that both members of the last subcommittee are dishonest

If the attacker controls one member of the final 2-subcommittee, then they can’t prevent the last value from being revealed – that makes sense. But since they would know the value in advance, they could perform manipulation from the previous subcommittee if they fully control it, right?

So I think we should focus on the probability that the attacker fully controls some subcommittee, and has “infiltrated” each subsequent subcommittee. Let’s call that attack probability P(a), and let m be the number of members the attacker controls in a given subcommittee. If all subcommittees have two members, then

\begin{align}
P(a) &= P(m=0) P(a | m=0) + P(m=1) P(a | m=1) + P(m=2) P(a | m=2) \\
&= (1-p)^2 \cdot 0 + 2p(1-p) \cdot P(m) + p^2 \cdot 1 \\
(1 - 2p(1-p)) P(a) &= p^2 \\
P(a) &= \frac{p^2}{1 - 2p(1-p)}
\end{align}

which, happily, is still below p as long as p < 0.5. So looks like we still benefit from subcommittees, at least if our security model already assumes p < 0.5.

![](https://ethresear.ch/user_avatar/ethresear.ch/poemm/48/2402_2.png) poemm:

> if an attacker knows all secrets during commit-time, then they may have complete bias on output by choosing appropriate secret(s)

It would also help to use some deterministic scheme, rather than letting members commit to arbitrary values. That way if an attacker controls the last n subcommittees, they can manipulate a maximum of n bits, by presenting or withholding values from subcommittees they control.

---

**poemm** (2018-10-06):

Daniel, thank you for your thoughtful and useful response.

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> Would subcommittee members use public key encryption to communicate the secret within the subcommittee without revealing it to outsiders?

Great idea, public key encryption seems perfect for this.

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> So looks like we still benefit from subcommittees, at least if our security model already assumes p  It would also help to use some deterministic scheme, rather than letting members commit to arbitrary values. That way if an attacker controls the last n subcommittees, they can manipulate a maximum of n bits, by presenting or withholding values from subcommittees they control.

Great idea.

---

**dlubarov** (2018-10-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/poemm/48/2402_2.png) poemm:

> Your calculation assumes that the subcommittee before the last one is fully controlled by an attacker

Sorry if my notation was sloppy, but I think the formula works in both cases. If the final subcommittee has m=1 (the attacker controls one member), I figure we can ignore it and recurse to the previous subcommittee. So I substituted P(a | m=1) = P(a). I should have given them indices and explained the argument.

I did assume that

- All subcommittees are 2-committees.
- The recursion continues ad infinitum. In reality, when we get to the very first subcommittee, P(a | m=1) = 0.

---

**poemm** (2018-10-07):

Daniel, thank you for the interesting discussion!

I did not recognize the recursion since there was no stated base case, and I’m not sure that you can recurse like this for the finite committees using approximations like p^2. Nevertheless, I agree with your conclusion about p<0.5 [edit: modulo some special cases addressed below]. Let me define your attack, and generalize your conclusion to arbitrary subcommittee sizes.

Definition. An *extended last-revealer attack* occurs when a single party controls a secret while knowing all later secrets (this includes the possibility that they control the final secret). The bias is from choosing whether to reveal this secret they control.

Claim. Consider an ordered subcommittee non-obligatory commit-reveal procedure with ratio r of dishonest members all controlled by a single attacker. Consider the probability p of an extended last-revealer attack. [edit: Ignore the cases where the attacker knows all secrets but controls none, because this technically is not an extended last-revealer attack but a different attack whose probability can be made arbitrarily small as discussed in other comments.] If the last revealer is a 1-subcommittee, then p=r. Otherwise,

p  \left\{
\begin{array}{ll}
        < r &\text{if } r<0.5\\
       = 0.5 &\text{if } r=0.5\\
        > r &\text{if } r>0.5.
\end{array}
\right.

Proof. If the last-revealer is a 1-subcommittee, then p=r, the probability that the last revealer is dishonest. Otherwise, consider the following cases. The case of r=0.5 has p=0.5 since attack and non-attack are complements of each other, i.e. swapping all honest and dishonest members will also swap whether there is an attack or not. The case of r<0.5 (r>0.5) has p< r (p> r) since some cases of non-attack (attack) do not have enough of the opposite type of members to swap with to create the corresponding attack (non-attack).

This is a strong claim because it covers all possible subcommittee sizes, and the proof provides insights into finding optimal subcommittee sizes.

We have successfully generalized the original attack to better capture the behavior of Ethereum stakers. But we have not considered competing attackers, selling secrets to possibly multiple parties, selling control of a member on an important subcommittee, economic incentives like rewards or slashing, and perhaps other things. Does anybody know whether these have been studied for the current beacon chain procedure (which is a special case of the subcommittee procedure)?

I still believe that subcommittees or other generalized procedures have potential to reduce bias on the Ethereum Beacon Chain, but more work is needed to prove things in more general attack and incentive situations.

---

**dlubarov** (2018-10-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/poemm/48/2402_2.png) poemm:

> swapping all honest and dishonest members will also swap whether there is an attack or not

Strictly speaking, this doesn’t hold in the case where all subcommittees are partially (but not fully) controlled by the attacker; in that case there’s no manipulation opportunity regardless of swapping. But I think it’s reasonable to ignore that case (as I did earlier), since its probability decreases exponentially with the number of subcommittees (assuming a constant subcommittee size).

![](https://ethresear.ch/user_avatar/ethresear.ch/poemm/48/2402_2.png) poemm:

> But we have not considered competing attackers, selling secrets to possibly multiple parties, selling control of a member on an important subcommittee, economic incentives like rewards or slashing, and perhaps other things.

This is just my take, but I like to bucket users into honest (rule followers) and dishonest (profit maximizers), and assume that all dishonest users will be perfectly coordinated, so we can model them as a single agent. In the future, “dark” protocols will probably exist for coordinating things like entropy manipulation, which could give near-perfect coordination. Or if not, at least we planned for the worst case!

---

**poemm** (2018-10-07):

Yes, I started working through some small examples, and noticed what you are talking about – I think my argument only works in the limit as committee size goes to infinity. I will re-evaluate what I want to prove, which may take some time.

I would like to share the following design of subcommittee sizes which may work well for the beacon chain. Many 1-subcommittees, followed by several 2-subcommittees, followed by several 4-subcommittees, followed by several 8-subcommittees. Some benefits of this design are (i) there is arbitrarily high probability that an early 1-subcommittee is honest, removing the omniscience (all-knowing) attack, (ii) the larger subcommittees at the end make it difficult for someone who wants to use their current bias to give themselves even more bias next time.

---

**dlubarov** (2018-10-07):

> removing the omniscience (all-knowing) attack

This could work, but we also have other options to prevent that attack. We could have each user commit before any secrets are shared with subcommittees, or we could use verifiable random functions, in which case we don’t need commitments. Another deterministic approach would be having each user prove `hash(pk, block_index)` in zero knowledge, and taking that hash output as their value.

Here’s a generalization of my previous argument to k-subcommittees. Consider an attacker with stake r, and let m_i denote the number of members they control in subcommittee i. Let P(a_i) be the probability that they can perform an extended last-revealer attack, given that they have partial control of all subcommittees following i (i.e. \forall j > i, \; 0 < m_j < k).

I’ll again make the simplifying assumption that the number of subcommittees is infinite, which implies that P(a_i) is identical for all i. Hence the “partial control” condition, 0 < m_i < k, has no bearing on P(a_i), since P(a_i | 0 < m_i < k) = P(a_{i-1}) = P(a_i).

\begin{align}
P(a_i) =& \sum_{j=0}^k P(m_i=j) P(a_i | m_i=j) \\
={} & P(m_i=0) P(a_i | m_i=0) \\
&+ P(0 < m_i < k) P(a_i | 0 < m_i < k)\\
&+ P(m_i=k) P(a_i | m_i = k) \\
={} & (1 - r)^k \cdot 0 + (1 - (1-r)^k - r^k) \cdot P(a_i) + r^k \cdot 1 \\
((1-r)^k + r^k)) P(a_i) ={} & r^k \\
P(a_i) ={} & \frac{r^k}{(1-r)^k + r^k}
\end{align}

P(a_i) decreases with k as long as r < .5, so it seems the larger the subcommittees, the better.

> use their current bias to give themselves even more bias next time

I think it’s good that you’re considering the extent of the bias, rather than just the probability of nonzero bias. I did a bit of analysis of a deterministic ordered reveal scheme – see [here](https://github.com/sigma-network/white-paper/blob/master/sigma-network.pdf), section 4.1. There I compared the expected block rewards of manipulative versus honest validators.

Depending on the parameters, the results were pretty close. E.g. with an epoch size of 10,000 blocks, a user (or coalition) with 40% stake could increase their expected rewards by ~0.41% by manipulating entropy. Looking at it another way, if the normal validator interest rate was 5%, they could increase their interest rate to ~5.02% with manipulation.

---

**poemm** (2018-10-08):

From your calculation, it seems that for any ratio of dishonest members under 0.5, we can make the probability of extended last-revealer attack arbitrarily small(!) by choosing large enough subcommittees. This is the best we can hope for! I would like to prove it for finite committees.

We need a procedure for each subcommittee to output a number, which they commit to and hopefully keep secret until it is their turn to reveal. What is a good way to do this? I was thinking about commiting/revealing the group secret created using Diffie-Hellman generalized to many parties, but I have never implemented anything like this. Also, I only know basics of verifiable random functions and zero-knowledge methods which you mentioned. Anyway, it would be good to study methods for subcommittees to see whether they introduce new attacks.

I skimmed your section 4.1. You are correct that we should consider economics instead of just probabilities. This way we can set appropriate economic incentive/punishments.

