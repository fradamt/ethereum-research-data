---
source: ethresearch
topic_id: 920
title: Using ICOs to fund science
author: kladkogex
date: "2018-01-26"
category: Better ICOs
tags: []
url: https://ethresear.ch/t/using-icos-to-fund-science/920
views: 7887
likes: 47
posts_count: 26
---

# Using ICOs to fund science

Currently, most whitepapers cite scientific papers, but academia people get little from the ICOs.

Here is a proposal how science could be funded by ICOs:

1. An ICO would voluntary commit, say 1% of proceeds to the science used by the technology.
2. The LATEX citations section of the whitepaper would include allocations of the proceeds in percentages.  Basically, the whitepaper author would decide to allocate, say, 7% to one citation, 5% to another citation etc., the total being 100%.
3. Then in a pass-through fashion, each scientific paper would voluntarily allocate the percentages to the papers it cites. So if my paper cites papers X,Y, Z I could allocate 40% to myself, 15% X, 20% to Y and  25% to Z.
4. As a result, you could have every paper to include smart-contract readable allocations, and then a smart contract would essentially create a network flow of money from ICOs to papers cited in the whitepaper,  then to second level citations, third level citations etc.
5. When a professor moves to one university to another, she could “take”  her papers with her, so the university would receive funding from the sum of contributions of its faculty.

## Replies

**vbuterin** (2018-01-26):

Interesting! Basically an airdrop into a reputation system for academia. I’d support this.

Another idea is that at the time that they write their papers, scientists could issue tokens for the paper and if desired sell them; then the airdrop would go to the token holders. This could allow scientists to pre-fund work, as well as creating a prediction market for how influential work would be in the future, which may be useful to society for informational purposes.

---

**dillchen** (2018-01-27):

[@kladkogex](/u/kladkogex) I’m glad someone posted about this. I had some thoughts along these lines as well -> [here](https://www.evernote.com/l/AQ1f_LfjrMBNobyU0zMDJyK7hHj5c8p63JU). They’re a bit messy, so I’ll just summarize below.

1. Research coin distribution event (ICO? or just give it researchers and other stake holders)
2. Each paper, when hits preprint server starts a game.

perhaps authors of papers have to stake money as well???
3. Owners stake research coin so they can peer review this paper
4. We gather a set pool of staked money for the paper

They decide on the validity of the paper
5. And how to initially distribute the distribution of said paper’s individual token in proportion to owners and citations to other papers.
6. This is some type of schelling point game.
7. Accurate schelling point people are rewarded with some new research coin (in some proportion to how much was staked)

Slashing the stake of bad reporters
8. Once paper schelling point is set, then distribute locked research token recursively to owners of said paper’s token with pro rata of schelling point.

Intuition is that peer reviews want to review important papers and therefore will stake tokens to do this.
9. More important papers get more staked token
10. More token flows recursively to the owners of the paper’s token.
11. I guess this is technically securitizing basic research IP, lol
12. Markets develop for individual paper’s token. These may later on yield great research results and therefore generate recursive payments of research token. As more papers get published, flow of money goes recursively to the paper parent papers/owners. The price of the token’s paper, denominated in research coin may

Recursive ownership is important because it incentivizes research with the greatest NPV in terms of research coin.
13. Researchers who publish should get steady payouts as more papers cite them, so they can continue to fund more research.

Nicola at Protocol Labs has written about this as well. https://nicola.io/research-coin/2017

---

**nicola** (2018-01-28):

Awesome to read this here! (thank for the mention! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) )

I once did a braindump of possible ideas to make this happen (although they are good intuition, I don’t believe they work in practice). The general idea is to combine prediction markets with peer review:

- Research Coin: first attempt
- Research Coin: second attempt

Have fun, hope to see good ideas out of this!

---

**mattiasbergstrom** (2018-01-29):

I believe that the right idea is to get rewarded by the papers use as in quoted or referenced, so for a researcher a kind of reputation system, then  I also like the idea of [@vbuterin](/u/vbuterin) to be able to pre-sell access to a specific research area, the only question there is if it could skew the research in a specific way, but I believe that finding new ways to found research should really be a core topic for ICO/crypto investors.

http://ieeexplore.ieee.org/document/7933951/  with 244 downloads I could have gotten some coins out of that paper ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**FBrinkkemper** (2018-01-29):

While I really like the general use case, I really hope this technology does not result in a popularization of science, in the sense that only really popular research gets proper funding, while newer and fundamental research gets less funding.

I do really like this idea though for the development of open source code and funneling the ICO capital through the dependencies. So proper general cryptography libraries for example get funded by multiple ICO’s.

So for example:

ICO for new Blockchain protocol where 60% of the received funds are used for the development. Then they can spend that by allocating 50% to their own code, and 10% to 5 big dependencies for example. Those dependencies can do the same again.

Is the above use-case worked on already by anyone’s knowledge?

---

**kladkogex** (2018-01-29):

Yes - I think this is a very good point !  We all need things like good crypto libraries, or and there should be a way to fund this …

---

**bpolania** (2018-01-31):

I have always thought that the white paper itself is not required to be a smart-contract, not on it’s entirety but a reflection of the paper document, so in a similar fashion to how gas in managed, the ICO company can set a price for the citation and the author of the paper can decide to accept it or not.

Having the white paper in the blockchain will come with additional benefits in terms of accountability but they are outside the scope of this thread, I’ve designed a contract for a white paper, let me know if anyone’s interested.

---

**kladkogex** (2018-02-01):

Boris nice - may be you can share a GitHub link then ?

---

**bpolania** (2018-02-01):

I just created a repo for this: https://github.com/bpolania/WhitePaperContract/tree/master

Please note that this is a work in progress, it means that it’s untested and is lacking functionality, the main intention is to define how a white paper could be represented in the blockchain, so at this point it’s better if you think of it as pseudo-code.

Also, I haven’t though about the citation part up until I read this post, so that functionality is not there but I’ll be adding it gradually.

---

**jamesray1** (2018-02-02):

Note that the concept of

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> an airdrop into a reputation system for academia

can be generalized to airdrops into other reputation systems.

---

**bpolania** (2018-02-02):

The github repo now has citation related functionality

---

**rumkin** (2018-02-08):

I was thinking about such system but from another angle. What if to create kickstarter for scientists. Scientist or developer may to make a proposal to community to solve some problem and provide proofs of experience to realise it. Community may support his work in safe manner paying for milestones. It’s some kind of (DA)ICO but in model when results became a public property after some time. It’s a kind of open source but in science.

---

**akomba** (2018-03-18):

Yes, I think generalization would be a good idea – to include support for critical projects in the ecosystem as well (etherscan, etc).

---

**musalbas** (2018-03-28):

This is also of interest: [MathCoin: A Blockchain Proposal that Helps Verify Mathematical Theorems In Public](https://eprint.iacr.org/2018/271)

> MathCoin: A Blockchain Proposal that Helps Verify Mathematical Theorems In Public
>
>
> Abstract: A public blockchain is proposed in an attempt to enable the coin holders to participate in verifying mathematical theorems for public access. Incentives are designed to encourage any party to contribute their knowledge by buying tokens of mathematical propositions that they believe are true. The proposed blockchain is a platform for people to exchange their belief in mathematical propositions. An implementation of this blockchain proposal, once established, will provide the general public an easy and instant access to reliable knowledge without having to read difficult proofs or having to blindly trust a small number of experts. Conversely, experts from various fields may find it be much easier for making their work appreciated by more people, leading to a better impact. According to the incentive inherently provided by the blockchain, they can even earn significantly if they do prove some theorems that were not previously known by the blockchain. Foundations who are interested in the validity of a particular proposition not yet explicitly recorded on the blockchain can donate a fund, which will distribute to experts who contribute positive efforts toward solving the specified problems. Only the people who erroneously create or buy tokens of a proposition that is eventually proven false will lose money. A reference design of the proposed blockchain that attempts to achieve the above-mentioned goal is described and reasoned.

---

**MariusVanDerWijden** (2018-04-01):

Is your repository private?

I tried to write my own implementation, it’s not finished and I’m new to this, so any comments are appreciated

https://github.com/MariusVanDerWijden/smartcontracts/blob/master/FundScience.sol

---

**7hKBg82PX** (2018-04-03):

I’m not sure how point two would work in practice; as an academic I do not see the incentive for allocating a certain percentage of my paper to each used citation; this mostly sounds like  a lot of extra work and I think people will not fully commit to this.

Furthermore, another problem which should be taken into account is how academics tend to uplift their h-index by conducting large research and then publishing the results not as one big paper but as multiple smaller ones, whereby their h-index gets increased and they can receive more citations (by both themselves as other scholars). This is a big problem in academia as it is, but it is hard to check for, and this would be a continuous problem if you allocate a percentage based on citations.

I do not have the answers, but I do think that these are some important issues to take into consideration.

Notwithstanding this, I think your general idea is good and at the very least a very important problem that the blockchain could help solve.

---

**kladkogex** (2018-04-03):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/7/e8c25b/48.png) 7hKBg82PX:

> I’m not sure how point two would work in practice; as an academic I do not see the incentive for allocating a certain percentage of my paper to each used citation;

In reality it will not be so easy to do: as an academic if you do not allocate to your peers than the community may not like it. As an academic you know that the academic community is very tightly  bound (reviewers,  funding etc.)

---

**7hKBg82PX** (2018-04-03):

Of course, I think I may have explained myself unclearly. I wonder about allocating an exact percentage (and determining that exact percentage, you draw on many sources, often also to support the same claim), not about acknowledging your sources in the first place ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**david.hite** (2018-04-04):

What do you think about this: scientist or developer may make a proposal to community to solve some problem and provide proofs of experience to realise it. Community may support his work in safe manner paying for milestones. It’s some kind of (DA)ICO but in model when results became a public property after some time. It’s a kind of open source but in science. Anyway, it’s better to use [ICO rating](https://icobuffer.com/), if you want to invest your money the best way.

---

**Perun** (2018-04-14):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/d/13edae/48.png) david.hite:

> What do you think about this: scientist or developer may make a proposal to community to solve some problem and provide proofs of experience to realise it. Community may support his work in safe manner paying for milestones. It’s some kind of (DA)ICO but in model when results became a public property after some time. It’s a kind of open source but in science. Anyway, it’s better to use ICO rating, if you want to invest your money the best way.

The main problem with this approach is that in academia contracts for, e.g., PhD researchers or postdocs are usually for at least 3 years, and hence tying funding to achieving short term milestones is not that easy to realize in practice. That’s why most funding agencies that offer support for basic research typically offer contracts that run for 3+ years. Of course these agencies ask for detailed work package description etc., but they will not stop funding if certain milestones after 1 year are not achieved.


*(5 more replies not shown)*
