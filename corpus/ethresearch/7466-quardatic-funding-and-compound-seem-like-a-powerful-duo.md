---
source: ethresearch
topic_id: 7466
title: Quardatic funding and Compound seem like a powerful duo
author: Bam
date: "2020-05-25"
category: Economics
tags: []
url: https://ethresear.ch/t/quardatic-funding-and-compound-seem-like-a-powerful-duo/7466
views: 1360
likes: 1
posts_count: 5
---

# Quardatic funding and Compound seem like a powerful duo

Hey guys, I’m an ambassador from the Ivan on Tech blockchain academy ![:yum:](https://ethresear.ch/images/emoji/facebook_messenger/yum.png?v=14) We’ve been developing an app on top of Compound that grants students with scholarships at our academy (using the interest generated to fund their tuition fees).

We ran through the problem of “how do you make sure that these students are worthy of the fund?” but we want to try something other than simply hiring an HR manager that would assess and choose the best talents. We want to experiment with Quadratic Funding.

You could imagine a public good being the Tezos cryptocurrency ecosystem  (I’m going for Tezos because I think it’s a great platform but there aren’t a lot of developers building on it). And the projects in our case are represented by students who want to study Tezos programming and hope that in the future, and after graduating, they can contribute to this ecosystem.

The way we set up the rewards is by asking individual donors, governments, philanthropists, etc. to lock an amount of money in a central pool of funds. In this case, it will probably be the Tezos Foundation. And finally, you let the Tezos community vote over who gets what from that funding pool. In other words, they will divide this pie into slices (rewards) by voting with their money to the students who they think will have the most positive impact on the ecosystem. Students who have previous experience in functional programming are likely to receive bigger slices than those who don’t. A student, Alice, might have that skill and also have developed Ethereum dapps and open-source projects before so she will probably get the biggest slice.

So, I want to know:

**1- Is my understanding of this method is correct?**

**2- Do you think QF can be applied and work well in our case, and with Compound?**

## Replies

**owocki** (2020-05-25):

How big is the fund that generates interest via compound, and where does the money come from? Seems it would have to be rather large to generate enough funding to cover tuitition whenrates are currently around 1pct on DAI

Quadratic funding is a great way of measuring if someone is respected by their peers, but that is an indirect method of measuring worthiness at best. you’d need to educate your community about what to look for and trust their judgment. And you’ll need anti Sybil and anti collusion infrastructure

I work at gitcoin and we’ve done several QF rounds worth about 2mm USD . PM if I can help.

---

**Bam** (2020-05-26):

Well we started the project when it was at 6% so we didn’t anticipate this sharp decrease. A 6-month scholarship will cost $96 so the principle according to the old rates is $1600 but now it’s $9600 ![:grimacing:](https://ethresear.ch/images/emoji/facebook_messenger/grimacing.png?v=14)

It’s still just a fun project to do (similar to rTrees). We do have a large educated community (+15k students and 200k subs on YT) but you’re right at these rates its very difficult to establish something sustainable. I’ll PM you once we finish with our MVP and grants a couple of scholarships ![:nerd_face:](https://ethresear.ch/images/emoji/facebook_messenger/nerd_face.png?v=14)

---

**mpmp67** (2021-02-15):

I am interested in this subject. Have you made any progress on this?

---

**Bam** (2021-02-15):

Unfortunately not. We didn’t receive any kind of funding so we started slacking then we just stopped lol. Check out https://spendless.io/ they’re doing something similar but without quadratic funding and the whole scholarship part. Just random charities I guess.

