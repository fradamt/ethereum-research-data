---
source: ethresearch
topic_id: 4960
title: Canonical TheDAO business logic question
author: unboxedtype
date: "2019-02-07"
category: Economics
tags: []
url: https://ethresear.ch/t/canonical-thedao-business-logic-question/4960
views: 1214
likes: 0
posts_count: 5
---

# Canonical TheDAO business logic question

Hi!

In the original TheDAO contract, it is assumed that TheDAO token holders

can vote for or against some proposal. The motivation for voting against

some proposal (as opposed to not voting at all), **as I understand it,** is to prevent spending TheDAO budget on some project you do not believe in and not willing to risk by your piece of the pie.

My question is in the following: Why not to divide TheDAO investors tokens

into separate “baskets”: separate basket for each proposal (as opposed to having

one big basket with all the tokens). If an investor wants to vote for a proposal, his tokens are put into the corresponding basket. The proposal under consideration can get only as much funds as the corresponding

basket contains. This step puts away the necessity to vote against some project,

because, by default, you are not risking by your tokens anyway?

Isn’t this solution also mitigates the so called “Majority robs minority” attack?

I’m pretty sure that there is a misunderstanding on my part regarding TheDAO business logic, I will appreciate any clarification.

TheDAO white paper:

https://download.slock.it/public/DAO/WhitePaper.pdf

## Replies

**oliverbeige** (2019-02-08):

I never understood that myself. An ideal DAO as venture capital pool enables pooling money from multiple investors and funneling it to the ventures the investors believe in.

---

**vbuterin** (2019-02-08):

If you do as the poster suggests, then the DAO essentially just becomes an interface for investing in stuff; economically it becomes a no-op. With investing being mandatory unless you pull out entirely, it’s not quite a no-op because there’s no way to invest in one proposal without investing in all of them.

---

**oliverbeige** (2019-02-08):

I follow this, but whats the advantage of not being a no-op? (Assuming that means you think it’s a do-nothing operation, which I don’t quite see that way. It’s still a marketplace that matches and bundles supply and demand for early stage venture capital.) Does forced participation force a more thorough due diligence process?

---

**haokaiwu** (2019-02-08):

[@vbuterin](/u/vbuterin) I think that’s only true if you take the post at face value. Instead of creating baskets by investments, you could theoretically create baskets based on theme. For example: protocol projects, DApp games, DeFi projects, etc. Bigger VC’s organize their money this way, as do traditional investment funds with sleeves of asset classes. There’s lots of wiggle room between zero bucketing and allowing investors to choose individual investments.

