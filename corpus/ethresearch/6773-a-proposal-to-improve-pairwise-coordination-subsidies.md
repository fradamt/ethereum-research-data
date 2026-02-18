---
source: ethresearch
topic_id: 6773
title: A Proposal to Improve Pairwise Coordination Subsidies
author: zoudavid
date: "2020-01-13"
category: Economics
tags: []
url: https://ethresear.ch/t/a-proposal-to-improve-pairwise-coordination-subsidies/6773
views: 2084
likes: 1
posts_count: 4
---

# A Proposal to Improve Pairwise Coordination Subsidies

*(This proposal benefits greatly from discussion with Vitalik)*

## Background Introduction

Since 2018, Vitalik has advocated for quadratic financing (QF) as a method to generate optimal provision of public goods in a decentralized, self-organizing ecosystem (Buterin, Hitzig, and Weyl, 2018). One of the most challenging problems faced by QF is collusion. For example, one actor or a group of coordinated actors may control multiple addresses or collude to “game the system” and extract unjustifiable subsidies in QF.

Since 2019, Gitcoin Grants has run 4 rounds of QF. Gitcoin Grants uses an innovative method: **pairwise-bounded coordination subsidies** (Buterin, 2019). However, I find the specification of the discoordination coefficient in Buterin (2019) not very intuitive and convincing. Besides, the tweakable parameter in Buterin (2019) mainly serves to bound extractable value for any pair of investors, but not doing enough to adjust for the collusion between them.  In this post, I propose a new method to improve pairwise coordination subsidies with rich economic meaning.

## A New Specification of the Discoordination Coefficient

Adopting the notation of Buterin (2019), I propose a new specification of the discoordination coefficient:

k_{i,j} = 1 - \frac{\sum_p \sqrt{c_{i \rightarrow p} } \sqrt{c_{j \rightarrow p} }}{(\sum_p c_{i\rightarrow p})^{1/2}(\sum_p{c_{j\rightarrow p}})^{1/2}} \tag{1}

Where k_{i,j} is the discoordination coefficient between investor i and j, c_{i\rightarrow p} and c_{j\rightarrow p} stand for investor i  and j's investment to project p, and \sum_p means the sum over all projects. The discoordination coefficient measures how independent a pair of investors are in making investment decisions.  There are two ways to understand the economic meaning of (1).

First, consider two vectors I = [\sqrt{c_{i\rightarrow 1}}, \sqrt{c_{i\rightarrow 2}}, ... , \sqrt{c_{i\rightarrow P}}] and J = [\sqrt{c_{j\rightarrow 1}}, \sqrt{c_{j\rightarrow 2}}, ... , \sqrt{c_{j\rightarrow P}}], where P stands for the total number of projects.

Let  ||\quad || be the magnitude of a vector:

||I|| = (\sum_\nolimits{p} c_{i\rightarrow p})^{1/2},  ||J||=  (\sum_\nolimits p{c_{j\rightarrow p}})^{1/2} \tag{2}

Let I\cdot J be the inner product of the two vectors:

I\cdot J = \sum_\nolimits p \sqrt{c_{i\rightarrow p}} \sqrt{c_{j\rightarrow p}}   \tag{3}

Let \theta be the angle between two vectors. Therefore,

I\cdot J = ||I|| \cdot ||J|| \cdot cos(\theta) \tag{4}

If the two vectors are orthogonal (i.e. \theta=\pi/2), then \cos(\theta)=0 and I\cdot J=0. If they are codirectional (i.e. \theta=0), then \cos(\theta)=1 and I \cdot j = ||I||\cdot||J||.

From (1)-(4), it is easy to see that

k_{i,j} = 1-\cos(\theta) \tag{5}

For (5), Let’s first consider two extreme cases.

**Case #1**: If for every p, \sqrt{c_{i\rightarrow p}}\sqrt{c_{j\rightarrow p}}=0, which means i and j have no investment in common, this corresponds to the case of \theta = \pi/2 and \cos(\theta)=0  (i.e. orthogonal vectors). In this case, k_{i,j}=1, means  i and j have maximum discoordination.

**Case #2**: If there exists a number \lambda such that for every p, \sqrt{c_{i\rightarrow p}}=\lambda\sqrt{c_{j\rightarrow p}}, which means  i and j make the same investment decision. Although they may have different amounts of money to invest, they share the same asset allocation decision in term of percentage. This corresponds to the case of  \theta = 0 and \cos(\theta)=1. (i.e. codirectional vectors). In this case, k_{i,j}=0, which means  i and j have maximum coordination.

The other cases lie between Case #1 and #2: \theta is between 0 and \pi/2, and \cos(\theta) is between 0 and 1. Therefore, **k_{i,j} is between 0 and 1. The larger k_{i,j} is, the higher discoordination is.**

Second, we can also understand the meaning of k_{i,j} from the theory of probability. *Ex ante,* every investor’s investment decision is a random variable. Therefore, [\sqrt{c_{i\rightarrow 1}}, \sqrt{c_{i\rightarrow 2}}, ... , \sqrt{c_{i\rightarrow P}}] and [\sqrt{c_{j\rightarrow 1}}, \sqrt{c_{j\rightarrow 2}}, ... , \sqrt{c_{j\rightarrow P}}] are *ex post* realization of inverstment decisions of i and j, respectively. In (1), \frac{\sum_p \sqrt{c_{i \rightarrow p} } \sqrt{c_{j \rightarrow p} }}{(\sum_p c_{i\rightarrow p})^{1/2}(\sum_p{c_{j\rightarrow p}})^{1/2}}  is simply  a sample estimation of the correlation coefficient between their investment decisions. **The higher the correlation coefficient is, the smaller the discoordination coefficient is.**

### Discoordination Adjusted Subsidies

For project p, i and j's subsidy after adjusting for coordination is

2k_{i,j}\sqrt{c_{i\rightarrow p}}\sqrt{c_{j\rightarrow p}} \tag{6}

The subsidy is 0 whenever \sqrt{c_{i\rightarrow p}}\sqrt{c_{j\rightarrow p}}=0 or i and j are perfect correlated.

From (6), I define the discoordination adjusted subsidy (DAS) extracted by i and j  from all projects as

DAS_{i,j} = \sum_\nolimits p{2k_{i,j}\sqrt{c_{i\rightarrow p}}\sqrt{c_{j\rightarrow p}}}\tag{7}

It is worthy pointed out that to estimate k_{i,j} by (1), we can use sample data from past rounds of quadratic financing, not just the current round. In this way, we can make the estimation of the discoordination coefficient more robust and less constrained by current sample size.

### Adjustment for Pairwise Bound

Suppose for any pair of investors, we introduce an upper bound on the total subsidies they extract from all projects. Let B be the universally applied upper bound. B is similar to the tweakable parameter in Buterin (2019)  .

We need to accommodate DAS_{i,j} with the upper bound B. Similar to Buterin (2019b) , I use the following formula :

\frac{B\cdot DAS_{i,j}}{B+ DAS_{i,j}}\tag{8}

Obviously, \frac{B\cdot DAS_{i,j}}{B+ DAS_{i,j}}\leq B **and it is an increasing function of** DAS_{i,j}.

Also similar to Buterin (2019), if there exists a particular level of total subsidies T, we need to solve for B that satisfies the following constrains (N is the total number of investors):

\sum_\nolimits{1\leq i \ne j \leq N}{\frac{B\cdot DAS_{i,j}}{B+ DAS_{i,j}}}=T \tag{9}

It is not difficult to solve (9) with numeric methods.

### Comparison with Current Method

Consider the case that  i and j make the same investment decision (i.e. there exists a number \lambda such that for every for p, \sqrt{c_{i\rightarrow p}}=\lambda\sqrt{c_{j\rightarrow p}}. With my method, they will receive no subsidy. But with current method, they could extract a large amount of subsidy, being only scaled downed by the tweakable parameter.

For example, the scenario in Buterin (2019). Suppose k  coordinated agents all contribute a very large amount of money W toward a project. Since they are perfect correlated, the subsidies that they can extract are 0 with my method. However, with current method, the subsidies they can extract are \frac{2MW}{M+W}< 2M, where M is the tweakable parameter.

Vitalik suggests the following case. Suppose we have two donors A and B and three projects A, B and C, and  the pairs of donor and project that have the same letter are colluding with each other. Now suppose A donates X 0 X, and B donates 0 X X.

In this example, k_{A,B}=0.5. If we use data from past rounds of quadratic financing, k_{A,B} may have a different estimation and could be more accurate.

The discoordination adjusted subsidy is DAS_{A,B} = 2\cdot 0.5 \cdot (\sqrt{X}\cdot 0 + 0 \cdot \sqrt{X} + \sqrt{X} \cdot \sqrt{X}) = X, which exactly half the level with current method. After taking the upper bound into consideration, the total subsidy is \frac{B\cdot X}{B+X}. With current method, the total subsidy is \frac{2MW}{M+W}.

**From the above examples, it is clear to see with current method, there is no adjustment for discoordination, only adjustment for pairwise bound.**

## Reference

[1] Buterin, Vitalik, Zoë Hitzig, and E. Glen Weyl, 2018, “Liberal Radicalism: A Flexible Design for Philanthropic Matching Funds”. URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3243656

[2] Buterin, Vitalik, 2019b, “Pairwise Coordination Subsidies: A New Quadratic Funding Design”. URL: [Pairwise coordination subsidies: a new quadratic funding design](https://ethresear.ch/t/pairwise-coordination-subsidies-a-new-quadratic-funding-design/5553)

## Replies

**vbuterin** (2020-01-13):

Very interesting insight, to use the dot product to estimate discorrelation between multiple actors directly!

After thinking about it, I think I understand the flaw behind this approach more deeply. Basically, any agent A can always increase their discoordination coefficient with any other agent B by simply making a project and donating a very large amount to themselves. If every A makes a project p_a and sets c_{A \rightarrow p_a} \rightarrow \infty then this will not affect their dot product with anyone else because no one else donates to p_a, but it will increase their |I| = (\sum_p c_{i \rightarrow p})^{\frac{1}{2}} value to infinity, reducing the fraction to zero and setting k_{A,j} = 1 for all j.

The property that the bound-based correlation coefficient in my original post gives is that two participants donating to the same project will increase their correlation score, but two participants donating to different projects will not decrease their correlation score. If you want to have a system where two participants donating to different projects *will* decrease their correlation score, then you need to defeat the send-to-self attack somehow.

One approach would be to make the focus one step further removed: instead of focusing on projects, focus on participant pairs that donated to the same project. That is:

1. If agents i and j both donate to project p they are more correlated
2. If agents i and j donate to projects p and q where some third agent k donated to both p and q, they are more correlated
3. If agents i and j donate to projects p and q where some third agent k donated to p but did not donate to q, or vice versa, they are less correlated

Rule (3) would be summed over all agents, so donating to your own project gives much less discorrelation than donating to a project that 100 other people also donated to (but some other agent has no connection to).

It feels like there’s some way to describe this using a more complicated use of matrix multiplications. If M is a (non-square) matrix mapping sqrt-contributions from individuals to projects, then M^T M would give you the raw correlations between individuals, and then you can do something else to figure out the higher-order measures… would need to think about this more.

---

**zoudavid** (2020-01-13):

Thanks for your reply!

However, I don’t think the send-to-self attack could cause serious problems.

First, the send-to-self attack is costly since the attacker needs to lock lots of capital in his “fake” project. Meanwhile, his return will be marginal. Suppose the attacker makes a project that only he invests and no other investors invest. It is true that by rising his investment in this project, he can increase the estimation of correlation between him and other investors. However, the subsidy that he can extract from his “fake” project is still 0. For other projects, increase in subsidies caused by the attack should be very limited and such increase can’t be enjoyed solely by the attacker.

Second, in calculating the discoordination coefficient, we can simply exclude any project with only one investor. For example, we can consider those projects to be failed in fundraising and not qualified for QF subsidies. In fiat denominated crowdfunding, there is often a threshold mechanism: Any project that is unable to win enough supporters or capital commitment within a certain time frame will be considered as failed, and any capital commitment will be returned thereafter. I think QF can incorporate similar mechanism.

Third, we can use data from past rounds of QF to estimate the discoordination coefficient and make its estimation less impacted by a single data point.

For the “higher-order measures of correlation”, I have done some preliminary research. Basically, besides correlation among different investors, we should also consider correlation among different projects. Just like coordinated investors tending to make similar investment decisions, related projects tend to attract similar groups of investors. When using investment data to estimate correlation among investors, we should be aware of the interdependence among projects.

I believe Singular Value Decomposition (SVD) is the right tool to study this problem. However, I think the solution may be too complicated to communicate to the community of investors. Besides, the solution may be susceptible to over-fitting.

---

**ptrwtts** (2020-01-14):

Coordination penalties appear to rely on an assumption that honest users will spread their funding across multiple projects, perfectly reflecting their preferences (ie funding every project they will receive value from, in proportion). In reality, I suspect that many users will fund just a handful, due to convenience or strong preferences. As a result, genuine public goods will have a lot of highly correlated funders, and be under-subsidized. It’s important that we don’t lose the core tenants of CLR when trying to reduce fraud.

Before settling in a local maxima based purely on coordination penalties, there is probably many more mechanisms to explore, that either compliment coordination penalties or supersede them. The measure of success should not just be how well fraud is reduced, but how well funds are allocated to genuine public goods.

A couple of additional ideas come to mind:

**1. Negative preferences**

For each user, projects effectively belong to three categories:

A) Projects I am willing to fund (high value perceived)

B) Projects I am not funding, but don’t mind if they are subsidized (small value perceived)

C) Projects that I don’t want subsidized (no / negative value perceived)

Currently, there is no way to differentiate between B and C. Perhaps the UI could allow users to “downvote” certain projects, with this information impacting the subsidies. Your downvotes only impact how subsidies are allocated between projects you didn’t fund. So downvoting for all other projects is the equivalent of downvoting none.

This comes out of the reality that users aren’t going to fund every single project that benefits them. The nature of public goods is that many of them are like to give small, indirect benefits. It’s easier to identity projects that are clearly fraudulent or unlikely to benefit you in any way.

**2. Stronger weight to number of unique contributors**

Most attacks leverage the ability to execute outsized influence by contributing large amounts. This is because in a sybil-resistant system (which is already required), it’s easier to accumulate funds than contributors. So one simple way to reduce the effectiveness of “fake” projects is to give even higher subsidies to projects with more contributors. This limits the impact of strong preferences, but may be a worthwhile trade-off.

At one extreme, you have CLR, which allows for strong preferences, but is vulnerable to collusion. At the other extreme, you could divide subsidies based on how many unique contributors a project received. The idea is to use a coefficient to pick the optimal point on this spectrum.

