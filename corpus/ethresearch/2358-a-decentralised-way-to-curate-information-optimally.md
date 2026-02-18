---
source: ethresearch
topic_id: 2358
title: A decentralised way to curate information optimally
author: cryptowanderer
date: "2018-06-26"
category: Economics
tags: []
url: https://ethresear.ch/t/a-decentralised-way-to-curate-information-optimally/2358
views: 1931
likes: 2
posts_count: 17
---

# A decentralised way to curate information optimally

Hello all,

I would dearly love to get feedback from anyone in this forum on the ideas outline here: https://github.com/andytudhope/theStateOfUs

Any flaws in my premises, any attacks I can’t see, any problems with the maths - please help me find them and make this the best it can be for all of us.

Let me know if you have any problems accessing the spreadsheet [here](https://docs.google.com/spreadsheets/d/1V1EMpDtAa7pP9F968VBb3dc2GUOT_BmS7-dK_0kwSDw/edit?usp=sharing) for the “really good” stuff.

Also, there is a Meta bounty in that repo of 34 704 SNT for anyone who can disprove it all. And also rewards for help with further optimisations and better, more formal proofs.

## Replies

**vbuterin** (2018-06-27):

I’m not sure I understand. The FAQ goes straight into “does it work in this complicated way? No, it works in this other complicated way”. Can you give a maximally simple description of (i) who the participants are, (ii) what actions the different categories of participants can take and (iii) what the incentives are?

---

**cryptowanderer** (2018-06-28):

Sure, sorry about that [@vbuterin](/u/vbuterin) ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=9)

DApps are ranked by whoever has staked the most, it is as simple as that. With one, small twist: the more you stake to get ranked highly, the easier it is to influence that position, should people so want to.

(i) Participants are developers who want to see their DApp get ranked highly so people use it.

(ii)

a) Developers can stake SNT (really, this is a general solution that only requires some fixed, fungible limit against which to optimise, so it could be ANY fixed, fungible asset or thing that people value).

b) Users can upvote or downvote their DApps, though I don’t see this happening too much, because it costs them and there is NO INCENTIVE for users, unless they’re feeling super motivated to make sure some DApp gets ranked less/more highly and are willing to pay to make that happen.

c) Users simply benefit as a side-effect of the optimal curation of information, much like they do now.

The big difference here is that, instead of having limited insight into PageRank and what you are being shown on your search and why, you KNOW that the DApps that appear first are those who have paid the most.

People ask, “But, but, but shouldn’t the DApps that appear the first be, like, the **most useful** or provide the most value to the community or something?” Yes, they absolutely should be.

As we all know here, the problem is with defining “value to the community”. Is that downloads, stars, usage metrics, customer feedback? All of these things are suboptimal and easy to manipulate.

The system I propose quite literally ranks the DApps that appear first by whichever ones provides most actual, **literal** value to the community, because a % of what is staked (defined by the curve I found, not by any human), stays staked forever, meaning there is less SNT in circulation, meaning that the value of each individual SNT goes up, meaning that the developers who do pay to get their DApp ranked highly are - again, quite literally - providing value to the community of users and getting ranked appropriately on it. I believe it’s similar to what you wrote about [here](https://vitalik.ca/general/2017/10/17/moe.html).

(iii)

a) The user of the app - NO INCENTIVES, this is the sociological factor that makes it all work. People are always saying “We need to get the community more involved! Let’s incentivise them to curate information FOR us, so we don’t have to do it”. No! That’s not the point of mechanism design as applied to cryptoeconomics. The point is to create systems that use mathematics and/or cryptography so that NO-ONE has undue influence over the system. It costs users to vote, so they would only do so to complain (if they feel really strongly), or donate to/protect an app that is being trolled. #EffectiveDirectCharity.

b) The developer is incentivised by appearing higher in the Dapp store, and by being able to receive back at least 52% (in this curve) of the SNT they staked if they get trolled, do something the community doesn’t like resulting in downvotes, OR do something awesome that the community likes, and wants to donate to. Complaining and donating are the same economic signal with signs reversed, so we can treat them the same mathematically if we set things up correctly.

---

**cryptowanderer** (2018-06-28):

It’s worth re-iterating that I think this is a general system that could be used by any community/individual to curate information they are interested in (with the only requirement being that they have some fixed and fungible constant like TOTAL SNT to optimise against).

i.e. Though I have described it this way above, it does not have to be for developers/DApps only, though that’s a use case of particular interest to Status right now.

---

**cryptowanderer** (2018-06-28):

One last note: yes, the maths is a little complicated (certainly nothing you can’t handle though), but so is the maths behind Bitcoin or Ethereum right? The users and developers never see that at all - that’s the whole point of doing it, to abstract the complexity away from the contractual and user levels and down into the abstract mathematical one.

Developers just know that they can get ranked highly by staking some value to the community in which they want to rank highly.

That community just knows that what they’re seeing first, at the top of the page, is purely a function of the people who have put the most skin in the game in terms of their, specific community.

The moon maths is only for forums like this. Once verified formally, it can go and live in the background, only ever again to be consulted by geeks with nothing better to do ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9)

---

**cpfiffer** (2018-06-28):

It seems like the weakness here is not the math, but that the fact that the participants have no reasonable incentives. If developers have to stake and they don’t really get the bulk of those resouces back and the users don’t ever need to use it, what’s the point? The developers won’t stake if there’s no users, and no users will use it because there’s no incentive for them to vote on Dapps.

It seems like a pay-to-play system that has no economic incentives to bind anyone into using it. In my view, Dapps are better shared and prioritized through regular communication channels like social media or word of mouth. That’s where I see the failure here.

---

**cryptowanderer** (2018-06-28):

Why do people pay for AdWords, SEO, etc. then? Or as users, do we use PageRank, even though there is no incentive to vote on which links appear first and why? This is exactly the same incentive structure when you really think about it, except the users have no influence at all over what they see, it’s not transparent about who is at the top and why, and we all just have to trust blindly uncles Larry and Sergey not to be evil…

---

**cryptowanderer** (2018-06-28):

Also, incentives can be deeply effected by sociological stuff, right? So, we set up a program called `Optimised for Status` and give the first (say) 100 DApps that work really, really well on mobile 10 000 SNT to stake initially so that they can be displayed on the 1st page. Just doing that, imo, is enough to kickstart the system and I think Status is just about popular enough that other DApp developers would really like their product to show up in our store.

This, however, can’t be proven, and so is just my opinion. Would prefer help with formal verification etc., though I really appreciate the feedback above ![:heart:](https://ethresear.ch/images/emoji/facebook_messenger/heart.png?v=9)

---

**vbuterin** (2018-06-28):

Ok, so what I understand so far is, if a developer publishes a dapp, they can stake some quantity of SNT, and everyone’s dapps appear in the dapp store in decreasing order of how much SNT they submitted. So basically it’s an ad auction on the blockchain, paid with capital lockup instead of raw coin payments.

That said, I am still not clear on how this interacts with upvotes and downvotes. If dapp A has 2500 SNT staked with 10 upvotes and 0 downvotes, and dapp B has 2600 SNT staked with 2 upvotes and 4 downvotes, who gets ranked higher? Also, what are the votes denominated in? Do the votes also involve staking SNT, or is it something else?

Also, can the staked SNT be withdrawn at any time, or are there delays or restrictions on withdrawing?

![](https://ethresear.ch/user_avatar/ethresear.ch/cryptowanderer/48/1558_2.png) cryptowanderer:

> The developer is incentivised by appearing higher in the Dapp store, and by being able to receive back at least 52% (in this curve) of the SNT they staked if they get trolled, do something the community doesn’t like resulting in downvotes, OR do something awesome that the community likes, and wants to donate to. Complaining and donating are the same economic signal with signs reversed, so we can treat them the same mathematically if we set things up correctly.

I still don’t understand this. What curve? What does a developer receive back?

---

**cryptowanderer** (2018-06-28):

> If dapp A has 2500 SNT staked with 10 upvotes and 0 downvotes, and dapp B has 2600 SNT staked with 2 upvotes and 4 downvotes, who gets ranked higher?

If you look at the contract, there is an idea named `_effectiveBalance`, which is what the DApp actually gets ranked on. As it turns out, because of the boundary value problem solved on the `curve_algo` sheet in the spreadsheet above, we can subtract the same absolute value X from `_effectiveBalance` in SNT as the % effect on `staked_available` (cell H2 in the sheet) downvoting X times would have.

So, dapp A would have `_effectiveBalance` 2500 SNT, dapp B 2596 SNT, therefore DApp B ranks higher.

I think the SNT staked can be withdrawn at any time yes, also defined in the contract (though I worry about key management and developers getting compromised there). Open to suggestions on delays/restrictions that might make this more secure.

---

**cryptowanderer** (2018-06-28):

The curve is in this spreadsheet: https://docs.google.com/spreadsheets/d/1V1EMpDtAa7pP9F968VBb3dc2GUOT_BmS7-dK_0kwSDw/edit#gid=1723492827

Change the value in B2 to 0.001 % and verify for yourself that it is an exponential relationship that has been linearized, and that linearizing it by setting the interval used to some arithmetic sequence based on a % of the Total SNT in circulation is the thing itself that makes all of this work.

---

**vbuterin** (2018-06-28):

Wait, why 2590? Shouldn’t it be 2510?

Still waiting for an answer on:

> Also, what are the votes denominated in? Do the votes also involve staking SNT, or is it something else?

And incentives.

---

**cryptowanderer** (2018-06-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Wait, why 2590? Shouldn’t it be 2510?

Sorry, I have misspoken very badly.

**Very NB:** upvoting has NO EFFECT on the `_effectiveBalance` on the Dapp (it just makes it more expensive to mint future votes). This is important because there are already perverse incentives for developers to stake their app to the top of the rankings and then just buy all the votes available and use them to upvote, getting 52% of their money back and ensuring that no-one can move their DApp down (other than another developer staking more, obvs).

So, we implement a social contract that says Status does not have to honour the the **contractual reality** in 2 very specific, narrow and **falsifiable** conditions:

1. Malicious code: requires a link to the code and a proof of why it is malicious.
2. Vote manipulation: requires blockchain proof of suspicious transactions.

---

**cryptowanderer** (2018-06-28):

Votes are not “denominated” in anything, there are just more and more of them “minted” as more SNT is staked, so that they have a bigger effect on `_effectiveBalance`, and therefore satisfy the condition that, the more someone stakes the get to the top of the store, the easier it is the influence that position.

Minting votes does cost SNT though, yes. A cost that is also calculated in the sheet above, based on the params explained.

---

**cryptowanderer** (2018-06-28):

Interesting question: https://github.com/andytudhope/Recollections/commit/5990c2b5b5e10f2803370b48456b6884c95c3d0b

---

**cryptowanderer** (2018-06-29):

Updated README: https://github.com/andytudhope/Recollections/blob/master/README.md

---

**Futurizt** (2018-09-02):

In this model, as with all advertising models the useful application with big pocket on the start will always win against another useful application that does not have same resources. PageRank comparison is not valid IMO since PR is not driven solely by paid results (paid results are separate). Same reason why Google actually trying to fight black SEO practices. I think the question here is not regarding the economics and incentive structure but rather inequality of an opportunity to begin with.

