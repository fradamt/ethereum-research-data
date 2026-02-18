---
source: ethresearch
topic_id: 1052
title: DAICO and Iterative Investment
author: dogezer
date: "2018-02-11"
category: Better ICOs
tags: []
url: https://ethresear.ch/t/daico-and-iterative-investment/1052
views: 9066
likes: 12
posts_count: 32
---

# DAICO and Iterative Investment

In attempt to overcome some of the problems current ICO market has, Vitalik Buterin and his team came out with the concept of DAICO. The idea is based on the merging concepts of DAO with the ICO concept, where investors can control the way how funds are withdrawn from the smartcontract. While this concept really solves some of the questions and is a step forward towards a more reasonable ICO market, we feel that there are still some challenges to be handled. Most of these questions are related to the way how disciplined should be investors to really make reasonable decisions, and what will happen if short term motivation of investors prevails long term product development goals. We would like to propose a different approach to solve the same set of problems:

- Project team generates their token and defines the basic price for their token (e.g. 0.001 ETH per token).
- The ETH/$ value of all tokens generated is enough for the project to complete the development, or more realistically, to make the project reach the break-even point. (With some reserve in mind).
- The tokens are not for SALE by project owners. The smartcontract, which holds the tokens, doesn’t really have the “payable” function. Note the variations described later.
- But tokens inside the smartcontract can be used to pay for the job being done by developers, designers, managers, salespersons and others working on the product.
- These payments are available for review by a third party (potential investors) which could validate that the amount paid is reasonable and the project really moves in the right direction. For example, every issue in the project issue tracker is recorded into a public ledger with information on what that issue is and associated transaction.
- Such payment for the job done can happen exclusively in the project tokens, but, if required, can happen as a combination of project tokens and traditionally established fiat or cryptocurrencies (may be outside of the publicly accessible ledger)
- People who have earned the coins are free to sell these coins on an open market to multiple investors (for example, through EtherDelta or a separate smartcontract as described below).
- Investors are buying the tokens from people who actually put effort to move the product further, rather than buying them from the project owner.

Optionally, to ensure that there is a demand from investors to buy tokens from developers, investors can send funds to another smartcontract — a smartcontract used to demonstrate the interest of the crowd towards the project:

- Developers can send “sell” their tokens to this smartcontract for ETH stored in it.
- Investors can withdraw funds from that contract after some period of time (for example 1 month) if they feel they don’t want to be a part of this project anymore.

As a result, there is no actual “ICO” event — but there is something which we call an “Iterative Investment”. Investors are buying only when the project progresses forward. Chances that the funds are misused are minimized. On the early stages, project owners overpay developers paying them more in “project tokens” than they would normally pay in dollars. Developers sell that to investors with discounts to account for the risk taken. On further stages, when it is clear that the project is moving in the right direction — these premiums/discounts become smaller and smaller.

In case if project nature requires some real funds for some asset (not lambos) — then a smartcontract may be adjusted to release a fixed amount of tokens for sale proportionally to the funds spent to pay development team.

The biggest problem in this concept is the need to be able to review transactions to really confirm that the token payments done are matching the real job done. At https://dogezer.com we solve that by providing our own set of tools and a special role of a “Watcher” in a team to be able to track the progress. Other solutions may require manual logging of a task completed into each token transaction or publicly accessible report being periodically published by the project owner.

Would appreciate comments and critique!

## Replies

**vbuterin** (2018-02-12):

This is actually quite similar to how MakerDAO launched. I fully support this kind of mechanism.

---

**jamesray1** (2018-02-12):

Sounds good. Small investments over time, e.g. with paychecks, are much more financially sound than a big one-off investment, and are less risky, and as you say the discount on investment or price of tokens can increase as the project moves forward, returns increase and risk reduces. I think the use of a governance protocol like [Democracy Earth](https://github.com/DemocracyEarth/paper/blob/master/README.mediawiki) or [Holographic Consensus](https://ethresear.ch/t/holographic-consensus-decentralized-governance-at-scale/1014) would also help with iterative investment. The organization could set in its code a quorum for investors to vote on a budget, as well as other rules.

---

**AnthonyAkentiev** (2018-02-12):

Sorry, guys. But the [Thetta.io](http://Thetta.io) was first with this approach (with Bancor) and we have proofs here that we published this approach 2 days before you - https://medium.com/thetta/thettas-liquid-token-generation-event-ltge-988e29425d34

Thx for testing our idea. We have no any problems with you doing same.

In the world of Open Source we all win.

---

**rkapurbh** (2018-02-12):

Interesting thoughts, I especially like the concept of making use of the token as internal payment as opposed to an external offering.

The issue that I see with a lot of these controlled/structured ICO mechanisms is there are too many ‘Perfect World Assumptions’. Here are a few of the ones that I think are concerning:

1. Cost of writing an ICO contract and making a prettified Landing Page ~$0. Which means an ICO issuer has little to no incentive to put checks and bounds on the capital they raise.
2. Who determines how the coins are to be issued to employees that are building the product? Centralized by the founder?  If it is determined by the investor pool - how does one reconcile with (1) the body of investors changing over time (esp. with liquidity offered by various exchanges) and (2) misalignment between short term incentives of investors (i.e. pushing price up) and long term incentives of the company/non-profit/issuer of token?
3. How do we begin to account for the general variability involved in building a startup (unaccounted for edgecases)? Should token holders be issued new tokens if the startup piviots? How about non-tokenized expenses - i.e. flying to attend meetups all around the world (lol) and spreading the word of your idea?

---

**dogezer** (2018-02-13):

Thank you, really appreciate the support!

We also do believe that in this approach it may happen that in some cases no fundraising will happen at all. Developers, after investing their time and effort and seeing the progress, may prefer to keep the coins for themselves with all of the future benefits ownership of these coins will bring in. This may be especially true in a world of basic income, or in a gig economy world, where person is working on multiple “gigs” in parallel (one to cover basic necessities, and others as a form of investment). So ICOs may go away as another sort of “intermediary” between creative party and income/value created by future product.

All this may open a door towards a next phase of decentralization where a person is a member of multiple organization (sometimes DAOs) at the same moment of time, and able to shift his focus between different organizations basing on how they progress. Products will need to convince their “developers” to “invest” their efforts in, rather trying to take an advantage of uneducated investors - which should increase the quality of projects proposed.

---

**StanBSmith** (2018-02-15):

The governance model is still skeletal.  Why not have the development team invite Ethereum Alliance members join as “watchers” or auditors of the development process and enable them to be rewarded with tokens for doing the audit function.  If the development team is not performing, the auditor is vested in getting things moving and will be motivated to audit honestly to maintain reputation in the community because their role is publicly known to participants in the DAICO.

---

**ToJen** (2018-02-18):

Does this mean the public would not hold any tokens?

---

**dogezer** (2018-02-18):

Thanks for the feedback and sorry for the delay.

Both consensus approaches look reasonable - and can really help with running a DAO.

But for “iterative investment style” ICOs, I feel investors vote should only matter for a very limited set of questions - like additional token emission or switching token model (i.e. token contract changes proposed by product team). Any operational or budget topics should be transparent, but investors shouldn’t have any impact on decisions taken. In other case - “Shorting” the token and disapproving the budget/etc may be a very reasonable behavior, especially when only some of the investors cast their votes.

I feel investor actually already accepted the risk for the sake of expected gains when he bought the coin. If he disagree with some latest decisions - he may sell it on market. These people shouldn’t be asked to run the company one way or another, they may just don’t have the right skills/understanding of the topic, or misuse that in their interest.

In our model we actually put just one thing to be decided by voting by anyone - conflicts resolution between “contributor” and project “owner” (“You delivery is bad”/“Its fully matches your requirements”). We try to prevent these technically (through accurate records), financially (limiting the payment size for one task to $10,000K equivalent so damages are not huge) and ideologically (fail fast, iterative development, etc) - but these conflicts will happen anyway. So idea is to escalate that conflict to the community- but not every member of the community, and definitely not investors. Only these who actually work with both of the persons in conflict and posses enough knowledge about the piece in question. The challenges arise if there are no such person yet, which happens when project is just starting. In this case conflict (and budget) have to remain frozen until more people will jump in.

---

**jamesray1** (2018-02-19):

> Any operational or budget topics should be transparent, but investors shouldn’t have any impact on decisions taken. In other case - “Shorting” the token and disapproving the budget/etc may be a very reasonable behavior, especially when only some of the investors cast their votes.

This is exactly what a vote token can provide—signalling for specific things. If they short the token after the budget, one may suspect it was because of the budget, but what if that wasn’t the reason? You could set up a vote to approve or disapprove of the budget, but you don’t necessarily have to make it so that the outcome of that vote must be held to—the organization can set up the rules, e.g. the board of directors gets 51% of the votes, etc.

---

**dogezer** (2018-02-19):

Thanks for the comment - and it may be one of the solutions, why not - need to see how market will react.

I’m a bit afraid that this will get commercialized very very quickly. A “respected person” would be invited to join each and every ICO as auditor, but wouldn’t have enough time/ability to audit everything. At the same time the fact of having such “cool” auditor pumps up the coin valuation up automatically. As a result these auditors will be offered crazy money to join, and sometimes they will agree. Take a look on that link: https://icobench.com/people?sort=iss-desc - see how many ICOs top advisers are running now. The same will happen with audit.

I personally don’t feel there is a huge need to actually govern this. Market will decide what is better. For example - Company says  “we need 10 millions USD development budget”. They generate the coin mapped to that budget and start spending it. Every spend is recorded and publicly accessible. If investor feel records are reasonable - he may try to purchase it from developers. If he feels it is not going into right direction - he skips.

The question which i feel needs to be solved in that approach - is how ICO will get the marketing budget to make investors to know about it, and how it will get listed on exchanges (which may be really a LOOOOT of money). On a current market solving that may be a bit hard, but probably easy than doing a traditional ICO right now, as scale of investment needed each month is not big.

---

**StanBSmith** (2018-02-19):

The auditors would be issued tokens, not cash, and would be in ethereum alliance businesses that can offer value to the emerging token issuer.   If a business is in the alliance and funds are being spent on a solid idea, I think they would lend their reputation and connections to inform the market of the offering and progress.  The goal is to productively incentives informed and vested folks in the ethereal ecosystem to help the “new kids” so we don’t  have the silly redundancies and ill conceived projects shooting the whole ecosystem.   I’m  never sure I’m right, but investors will need a better stream of quality information and assurance projects are supported by folks who can help assure delivery.

---

**dogezer** (2018-02-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> This is exactly what a vote token can provide—signalling for specific things. If they short the token after the budget, one may suspect it was because of the budget, but what if that wasn’t the reason? You could set up a vote to approve or disapprove of the budget, but you don’t necessarily have to make it so that the outcome of that vote must be held to—the organization can set up the rules, e.g. the board of directors gets 51% of the votes, etc.

Thanks, got it !

Fully agree that organization should be setting up which questions are for real voting, and which questions are just to collect feedback. My personal stance - anything modifying token nature, like unplanned emissions, smartcontract change, forks - have to be DAO controlled, as this is a change in rules. Anything else should go only as a “feedback” - because, in contrast to traditional early stages investment schemes, in ICOs in most of the cases investors have a possibility to liquidate the position if they feel it is not going right.

But this is just my personal position, mostly motivated by desire to keep things simple. Of course different organizations may setup different set of rules on what investors can really control. So we are actually on the same page with you.

---

**dogezer** (2018-02-19):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/7993a0/48.png) ToJen:

> Does this mean the public would not hold any tokens?

Thank you for the question, this is something really worth discussing. I believe you are asking because coin need adoption to establish valuation.

I feel there are three usecases (sometimes overlapping):

1. Usecase when coins can be mined
2. Usecase when coins only serve the purpose of raising the investment
3. Usecase when coin is an utility token to access some functionality of product being build. Most Interesting

**1. Usecase when coins can be mined**

In this scenario initial team/investors gets a significant part of the tokens while building the product through “iterative investments”, and then, after launch - other parties join in and start to “mine” the coin. When i say “mining” it may not necessary mean blockchain PoW or something like this - it may be something different, like executing some task and being paid for it in tokens (but see the second usecase). The general public receive these coins through “mining”, and that is the way how adoption starts to grow. Increase in adoption defines/increase the valuation of coins being hold by team/initial investors (which is large enough comparing to daily “mining” volume).

**2. Usecase when coins only serve the purpose of raising the investment.**

Unfortunately this is very common usecase right now. While many things and businesses can be tokenized, often such tokenization with the help of the blockchain only damage the product. Blockchain is good for what its good for, but using it for payments for every like on likes on a facebook or for each calorie burned - it is like eagle chasing the flies (even with gas question aside). As a result we have a great number of ICOs right now who introduce blockchain into their product just to get an investment raised.

Idea is to don’t tokenize the product - but tokenize product revenue/ownership, allowing non-blockchain products to raise money through ICO/Iterative Investments. And in that case there is just no need for wide adoption of the coin - it is a bit closer to traditional holding until project becomes profitable. Which is much more fair than current state where people are investing into the products which are just not feasible if they will use the blockchain for what they want to use it.

**3. Usecase when coin is an utility token to access some functionality.**

That is most probably the most interesting part. There are two things which company doing an ICO right now tries to achieve:

- Raise an investment by selling their coin
- Increase the adoption by ensuring that people own the coin as much as possible.

These goals are contradicting to each other. The best way to increase the adoption - is to airdrop the tokens to as many people as possible. But investors are buying coins for money - and making an airdrop is kind of damaging for them. We have heard investors saying that they are in love with our idea, but will buy when these “free” tokens (which we actually don’t have) will hit the market and cause price to fall. So here is an idea:

There is “Master” coin, which can be earned/bought through “Iterative Investment”. There is a second “Utility” token, which is a token to access product function. Utility token only generated when product is ready. Utility token is airdropped to each and every in that world to encourage them to jump in and try the product. When utility token is used - it leaves the user wallet and is proportionally distributed to owners of “Master” coins.

This should be more reasonable than airdropping the same tokens as people are buying during ICO, and gives a good reward for folks participating in “iterative investments” to actually follow this concept. They are sort of working for/buying money printing machine in case if project is successful.

Let me know if this makes sense.

---

**dogezer** (2018-02-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/rkapurbh/48/742_2.png) rkapurbh:

> Interesting thoughts, I especially like the concept of making use of the token as internal payment as opposed to an external offering.

Thanks, appreciate the support. I is just more reasonable for both parties as ICO owners can concentrate on the product and spend less effort on packaging it for external offering.

![](https://ethresear.ch/user_avatar/ethresear.ch/rkapurbh/48/742_2.png) rkapurbh:

> Cost of writing an ICO contract and making a prettified Landing Page ~$0. Which means an ICO issuer has little to no incentive to put checks and bounds on the capital they raise.

Agree with that 6 month ago, almost agree now, but feel it is evolving. If we check [icoalert.com](http://icoalert.com) as of today - we will find ~80% failures, ~18% raising a few millions, and a few rockstars. I believe if nothing will change (regulation), then this tendency will continue - and it would be just impossible to raise anything meaningful without the prototype/product (which is actually positive) or huge marketing budget (which is negative). So i feel many startup owners will have to look for other ways eventually, even if they want “no check and bounds ICO with just landing page and smartcontract”. It will just not work without product or without a million to waste on marketing.

![](https://ethresear.ch/user_avatar/ethresear.ch/rkapurbh/48/742_2.png) rkapurbh:

> Who determines how the coins are to be issued to employees that are building the product? Centralized by the founder?  If it is determined by the investor pool - how does one reconcile with (1) the body of investors changing over time (esp. with liquidity offered by various exchanges) and (2) misalignment between short term incentives of investors (i.e. pushing price up) and long term incentives of the company/non-profit/issuer of token?

- It should be centralized by founders to be able to keep the control on where it is going and make quick or “hard”  decisions. I agree with you on the problems on involving investors there - better to be avoided.
- It shouldn’t be time based, but rather than task/performance based. We (and for example colony.io) are trying to map these to issues in issue tracker. We also map/plan to map issues to code commits in repository/uploads into cloud storage. So investors can track this and see if this is at least somehow reasonable.

![](https://ethresear.ch/user_avatar/ethresear.ch/rkapurbh/48/742_2.png) rkapurbh:

> How do we begin to account for the general variability involved in building a startup (unaccounted for edgecases)? Should token holders be issued new tokens if the startup piviots? How about non-tokenized expenses - i.e. flying to attend meetups all around the world (lol) and spreading the word of your idea?

- For pivots (big ones) - if the pivot causes the increase of the future planned valuation for the sake of increasing the dev budget - then, basing on the agreement from token holders (that is where voting/DAO may took place) new tokens may be generated. If pivot is to chase another goal - then another organization may be started with its own tokens (partially distributed to original organization if it plans to reuse any intellectual property from it). The original organization may continue to exist - may be with having other people jumping in as founders.
- For non tokenized expenses - idea is that project owner can sell some tokens to investors to finance that (and probably finance his daily needs) - but amount of tokens which could be sold is proportional to amount of tokens spend on development.

---

**dogezer** (2018-02-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/stanbsmith/48/538_2.png) StanBSmith:

> The auditors would be issued tokens, not cash, and would be in ethereum alliance businesses that can offer value to the emerging token issuer.   If a business is in the alliance and funds are being spent on a solid idea, I think they would lend their reputation and connections to inform the market of the offering and progress.  The goal is to productively incentives informed and vested folks in the ethereal ecosystem to help the “new kids” so we don’t  have the silly redundancies and ill conceived projects shooting the whole ecosystem.   I’m  never sure I’m right, but investors will need a better stream of quality information and assurance projects are supported by folks who can help assure delivery.

I agree with you in general, but afraid that in real live things will be different. As soon as someone will have a right to say if project is good or not - it would become a business.

It is already happening with the current ICOs on this icobench website, they just call these “experts”. Token purchasers kind of believe this - but my inbox full of crazy offers (a few thousands dollars each) from “experts” offering to pump up the rating for us. Even more - our rating is lower than it should be due to one guy who actually gave us 1.333 out of 5, and this guy have just two types of ratings - either 1/5 or 5/5, which raises a number of interesting questions.

So audits would be possible - why not, but they better be not paid, and people shouldn’t rely just on third party audits - they have to be able to audit themselves.

---

**jamesray1** (2018-02-19):

You could also have non-voting tokens and voting tokens, the latter of which come at a very slight markup in price, similar to shares. For example, GOOGL class A voting shares have a markup over GOOG class C shares, although at the moment the difference is only <0.1%, while previously it had been about 1.5%. If you’re gonna limit voting to forks, unplanned token emissions, changing tokens, smart contract changes, and similar changes, then there would be less reason to do this.

---

**phillip** (2018-02-19):

[Stein 1989] Efficient capital markets, inefficient firms: a model of myopic corporate behavior

**ABSTRACT:** This paper develops a model of inefficient managerial behavior in the face of a rational stock market. In an effort to mislead the market about their firms’ worth, managers forsake good investments so as to boost current earnings. In equilibrium the market is efficient and is not fooled: it correctly conjectures that there will be earnings inflation, and adjusts for this in making inferences. Nonetheless, managers, who take the market’s conjectures as fixed, continue to behave myopically. The model is useful in assessing evidence that has been presented in the “myopia” debate. It also yields some novel implications regarding firm structure and the limits of integration.


      [faculty.fuqua.duke.edu](https://faculty.fuqua.duke.edu/~qc2/BA532/1989%20QJE%20Stein.pdf)


    https://faculty.fuqua.duke.edu/~qc2/BA532/1989%20QJE%20Stein.pdf

###

1451.01 KB

---

**dogezer** (2018-02-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> You could also have non-voting tokens and voting tokens, the latter of which come at a very slight markup in price, similar to shares. For example, GOOGL class A voting shares have a markup over GOOG class C shares, although at the moment the difference is only <0.1%, while previously it had been about 1.5%. If you’re gonna limit voting to forks, unplanned token emissions, changing tokens, smart contract changes, and similar changes, then there would be less reason to do this.

yes, all of these options should be possible. The only reason why i’m proposing it that way - is to keep things simple - but if the company will decide that they need more investor involvement - for sure there may be multiple options!

---

**rayzh2012** (2018-02-21):

sounds more like a plan for potential salary based system that have regular schedule, and deliverable reviews before the next commitment. Though I think this would be more of the next wave of paying the developers than an investment which based on huge profit.

---

**dogezer** (2018-02-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/rayzh2012/48/829_2.png) rayzh2012:

> sounds more like a plan for potential salary based system that have regular schedule, and deliverable reviews before the next commitment. Though I think this would be more of the next wave of paying the developers than an investment which based on huge profit.

If the project is really destined to make huge profit - then this huge profit goes to these of developers who HODL the coins. So it is not exactly like the salary, it is like an investment - the only difference is that investment comes in a form of skills and effort from dev.


*(11 more replies not shown)*
