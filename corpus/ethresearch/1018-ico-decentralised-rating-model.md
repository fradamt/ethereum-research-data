---
source: ethresearch
topic_id: 1018
title: ICO decentralised rating model
author: rumkin
date: "2018-02-07"
category: Better ICOs
tags: []
url: https://ethresear.ch/t/ico-decentralised-rating-model/1018
views: 2059
likes: 4
posts_count: 6
---

# ICO decentralised rating model

What does community think about decentralised rating working on principles of independent rate. Algorithm is pretty simple:

1. There is rating Contract which holds rates from Agencies to ICO Tokens.
2. Users can collect rates of any Token from all Agencies and select such agencies they trust to calculate average rate value.
3. Agency can put report into Swarn using same rating Contract to explain its’ rate.

This algorithm allow to calculate average Agency rate accuracy. To calculate average Token rate. And to publish Token report.

## Replies

**kladkogex** (2018-02-08):

Great idea!

Some additional thoughts:

1. there should be a way for rating agencies to stay totally unanimous forever - otherwise people will not be able to express their thoughts. For example, I may think that IOTA is totally insecure snake oil (which it is BTW), but I may not be able to express this view because me getting scared these guys may sue me.  You want to enable people to do write nasty reports and give really low ratings.

A huge problem for the industry now is that great projects and total scams are loved by investors in the same way. Wall Street has a similar same problem where analysts/investors/IPO underwriters are frequently the same people.

1. In real life users may have little abilities to understand whom to trust, because the subject is very technical.  As an analogy, for biotech common investors have little ability to decide which biotech analyst is good or bad in analyzing cancer drugs. Most biotech analysts unfortunately have little to do with science,  for the most part are photogenic people in expensive suits with expensive smiles )
2. A way to fix this would be a mathematical algorithm that automatically adjusts the weights of a particular analyst based on the past long term token performance (such as 5 year performance).  The smart contract could pull token prices from EtherDelta or other decentralized exchanges.  A problem is that to start the system you could not specify the 5 year requirement right away, you could probably start with 6 months, and then increase it gradually to 5 years
3. Each anonymous analyst would need to be paid somehow, the payments would need to be made in proportion to weights.  What is not clear to me at the moment, is where the money would come from, you do not want the analysts to be paid by ICO companies, analysts need to be paid by investors.
This means that there could be some kind of a paid encryption scheme that allows investors to pay for analyst reports …

---

**rumkin** (2018-02-08):

1. The Rating Contract itself has no any identification except of sender address which is secure enough. So I think this is the most thing that can be done.
2. Yep. There is a lot of such companies which work could not be analysed well in any reasonable term. So this is became some kind of lottery. And this is high risk investments for those who doesn’t afraid to loose. But with DAICO investors will have tools to control money.
3. The current plan is to rate initial offerings and collect it rates to inform early investors. So long term rating is a second generation of such rating. There is too much variables currently.
4. There is different kinds of rewards. I know several groups of people who rates ICO for free and earn money on consulting. But this is open question.

---

**metabol** (2018-02-12):

Token report still means Centralization , infact it will lead to typical scenerios where prospective ICOers pay some «backshish» to get a rating of AAA+ when all they care about are holidays in the carrebean!

The most practical way to deal with ICO scams is tying ICO to some utility product or service.

---

**rumkin** (2018-02-12):

> infact it will lead to typical scenerios where prospective ICOers pay some «backshish» to get a rating of AAA+

Yes. But in decentralised model such ICOers could not buy good rating from every agency. So everyone can see incorrect behaviour and higher rating from bought agencies. Decentralised rating make rating transparent and inspectable.

> The most practical way to deal with ICO scams is tying ICO to some utility product or service.

I don’t understand how it lead us to honest ICOs. Could you explain?

---

**metabol** (2018-02-15):

It takes a mixture of time, pain and strongwill to put ideas into code …moreso daring projects we see in blockchain space…if a requirement for deploying ICO contracts was some form of POC /demo or alpha release most scammers would definitely not get to ICO stage as they would not be able to meet the cutoff mark of POC.

Even if the project eventually fails atleast it would be comforting to know that the good intention was there from the start.

