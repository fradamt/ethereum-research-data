---
source: magicians
topic_id: 2169
title: "Call for Participation: Developing an incentivisation for NonOrgs"
author: Ethernian
date: "2018-12-08"
category: Magicians > Primordial Soup
tags: [nonorg]
url: https://ethereum-magicians.org/t/call-for-participation-developing-an-incentivisation-for-nonorgs/2169
views: 1075
likes: 4
posts_count: 6
---

# Call for Participation: Developing an incentivisation for NonOrgs

[As already introduced earlier](https://ethereum-magicians.org/t/donations-to-the-un-organisation-of-ethereum-magicians/1746), I would like to develop an incentivisation for Non-Orgs.

In contrast to DAO, a NonOrg (non-organization) tries to operate without any executive body at all. Ethereum Magicians try to be such NonOrg. The main reason is to avoid the centralization of power in hands of executives.

The lack of executives makes usual operations like invoicing or paying for the work quite challenging for NonOrgs. There are good discussions [here](https://ethereum-magicians.org/t/otherhoods-some-thoughts-after-the-meta-ring/1820/9) and [here](https://ethereum-magicians.org/t/community-call-with-open-collective/2085), but it is about to how get invoices paid and expenses covered. I would target another aspect of NonOrg: Incentivisation of participation beyond of direct expenses coverage.

### Problem:

1. NonOrgs are creating public value and there are sponsors who would like to support it.
Who should receive the donation if there is no executives in Non-Orgs? Who should receive how much reward if the rewarded work was created by whole community over the long time? What is the fair distribution rule?
2. Even NonOrgs is just a group of independent people, they have resources “for sale”. For example, a Non-Org has a community. Attention and appreciation of the community may be valuable. It could be also advertising on NonOrg’s site.
What is the fair price and fair distribution of the income from that “sales”?

### Solution:

I would propose to create an incentivisation platform as follows:

1. We need a token that get minted and distributed upon work done to the member of Non-Org.
2. May be the token should be non-transferable in order to avoid speculations and corresponded legal problems.
3. Any token holder may put his token into public order book for sale for any price he like.
4. A sponsor “buys and burns” so much token as possible with his donated money.
5. A sponsor provides “proof of burn” to the Non-Org community and get community appreciation or access to particular resources.

### Advantages:

1. Legally donation goes directly from sponsor to the members whos token get bought (and burned). They are solely responsible for legal and taxation aspects of the donation. NonOrg as whole is not a part of the financial transaction, because it neither takes the money nor provides services.
2. Anyone is free to set any price and order time in the orderbook. No one can be accused of unfair distribution of sponsored money.
3. If NonOrg makes meaningless work, token gets diluted. If the work is great more sponsors will come and token can be bought at higher price.

### Challenges:

1. How many token should be minted for the work done?
2. It is unclear who can accept the work done and mint the token?

I believe the challenges should not be “hard coded”. It can a “wet code” provided by roughly consensus.

But it should be discussed anyway.

### Roadmap:

I am going to implement it because I need it for [Ethereum Architects](https://github.com/Ring-of-Ethereum-Architects) community. But I don’t like to develop alone. Would anyone join the implementation team?

## Replies

**AmarRSingh** (2018-12-10):

This seems like an interesting idea! I am wondering whether the token is essential to what you’re trying to achieve, which, from what I gather, is **a convenient way to incentivize contributions to a non-hierarchical organization through sponsorships**. We could just use a leadership board for a github repo (monitored using Sourcegraph or some other repo monitoring service) to determine the distribution of donations. If this distribution process is made entirely transparent, then there’s no need to use a token (or accordingly a smart contract on a blockchain).

Even so, experimenting with non-hierarchical DAOs is something I’m interested in so I am happy to join the implementation team. I’m sure we could add checks and balances to your proposed scheme by supplementing it with a voting system in which the Non-org’s members can vote on the distribution of donations (with their tokens which are awarded based on contributions to the project). There are still a lot of open questions that would need to be addressed once we start building.

---

**Ethernian** (2018-12-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amarrsingh/48/1273_2.png) AmarRSingh:

> a convenient way to incentivize contributions to a non-hierarchical organization through sponsorships .

yes, this is the goal.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amarrsingh/48/1273_2.png) AmarRSingh:

> We could just use a leadership board for a github repo … to determine the distribution of donations. If this distribution process is made entirely transparent, then there’s no need to use a token.

I am not quite happy with the leaderboard approach.

- Awards should be assigned just after work is done, but it can be paid out only when sponsor money is here. Inbetween members should trust leader board maintainers and custodians quite long term. Not good.
- Someone must take sponsors money to distribute it. This is the centralization we try to avoid and it may create extra legal obligations.
- It is not only about coding. It can be any work done. Github repo is too technical.

Token gives an opportunity to decide on time of pay out. Later pay out may bring more money because the value of the NonOrg may be cumulative.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amarrsingh/48/1273_2.png) AmarRSingh:

> I am happy to join the implementation team… I’m sure we could add checks and balances to your proposed scheme by supplementing it with a voting system.

great! I am very happy to have someone to implement it together.

Would you explain what challenges do you see and how would you solve it?

You have mentioned voting, but what problem would you like to solve by that?

---

**AmarRSingh** (2018-12-11):

Well, there are a lot of unanswered questions. For example, how is work measured? This will probably differ for each project, but if we consider different categories of work (pushing code, reviewing code, documentation, blog posts, etc), then how do we determine the correct distribution of sponsorship funds between these types of work. The *fairest* distribution will vary depending on the nature of the project, but who determines this?

Are sponsors donating to specific contributors to the Non-org because it seems like that’s what you’re proposing. I don’t think that’s practical – it significantly increases the inconvenience to sponsors if they have to find which employee of the Non-org they want to sponsor. Why include a token? Some sponsors might get confused by the fact that they have to navigate an order book, buy a token, and burn said token in order to donate to a project. Moreover, you said these tokens were NFTs (unique to each worker) so how would the sponsor know which one they should buy and burn.

I think it might be best to just experiment with a DAO that uses some sort of rotating council to distribute funds among workers. It just seems more practical to establish a trusted subset of members who have developed a reputation within the non-org through consistent commitments (still this begs the question of how these commitments would be measured and how do we start the org’s governance). I realize that this sort of idea has already been discussed extensively, but there’s still room to experiment.

SideNote:

- Sponsored burning seems like a relevant idea to your proposal (not a direct solution to your scheme, but some token bonding curve paradigm could probably be adapted for what has been proposed).
- I’m a big fan of Polkadot’s governance mechanisms (such as Adaptive Quorum Biasing (to solve for low turnout by requiring a higher ‘yes’ threshold accordingly) as well as the use of a council in addition to coin-voting). These are geared towards on-chain governance rather than organizational governance, but these mechanisms can also be used to manage organizations.

---

**Ethernian** (2018-12-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amarrsingh/48/1273_2.png) AmarRSingh:

> Well, there are a lot of unanswered questions. For example, how is work measured?

yes, this is undefined currently. I believe it is possible to define some “price list” that satisfy the “rough consensus” and if not - just change it accordingly. It means, essentially, only the award distribution will be decentralized and trustless. Setting up the rules (what price list is a part of) remains old-school wet coded. Nevertheless if rules are changing rarely, making award distribution processes trustless is meaningful, IMHO.

Anyway I agree: here is a need for further improvements.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amarrsingh/48/1273_2.png) AmarRSingh:

> The fairest distribution will vary depending on the nature of the project, but who determines this?

“Abstract fairness” is not my goal (I don’t know how to define and achieve this). I would happy to see “subjective roughly fairness”, which means most people accepting it “as is”.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amarrsingh/48/1273_2.png) AmarRSingh:

> Are sponsors donating to specific contributors to the Non-org because it seems like that’s what you’re proposing. I don’t think that’s practical – it significantly increases the inconvenience to sponsors if they have to find which employee of the Non-org they want to sponsor.

No. It is not my proposal. The system should support contribution to NonOrg as whole.

In some edge cases it can be part of the NonOrg, but definitely not some specific contributor.

Sponsors are free to support particular contributors just by making targeted money transfer, they do not need any system for that.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amarrsingh/48/1273_2.png) AmarRSingh:

> I think it might be best to just experiment with a DAO that uses some sort of rotating council to distribute funds among workers.

It is not what I proposed. The proposal tries to avoid any DAO distributing the wealth.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amarrsingh/48/1273_2.png) AmarRSingh:

> It just seems more practical to establish a trusted subset of members who have developed a reputation within the non-org through consistent commitments

Trusted subset of members is exact, that NonOrg tries to avoid, otherwise you have an usual Org like DAO.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amarrsingh/48/1273_2.png) AmarRSingh:

> SideNote:
>
>
> Sponsored burning

hmm… May be it is really a TCR, that I have proposed. I have to think about it a little bit.

Thanks for the hint.

---

**AmarRSingh** (2018-12-14):

Not sure if you’ve come across [sourcegrain](https://github.com/sourcegrain/mission/); seems relevant to your idea. Building on 0x seems like a good idea as well (what sourcegrain is doing) – it’s a great project with solid output thus far and a seemingly bright future.

