---
source: ethresearch
topic_id: 1423
title: ICO Control Tokens
author: akomba
date: "2018-03-18"
category: Better ICOs
tags: []
url: https://ethresear.ch/t/ico-control-tokens/1423
views: 2311
likes: 1
posts_count: 5
---

# ICO Control Tokens

It became clear that running a pre-ICO makes the rest of the ICO (even DAICO) easily attackable. I am proposing using Control Tokens that are only issued during the public sale. This mitigates most of the problems that I highlighted in the [previous post](https://ethresear.ch/t/daico-praise-and-critique).

During a presale, a dishonest founding team could acquire enough tokens to disable or manipulate the controlling mechanisms of a DAICO.

Removing the presale is often not an option. It often has legitimate use.

## Two Tokens

However, it is possible that only the public sale buyers get controlling tokens. During the public sale, contributors would get *two different* tokens.

The first one is the actual **ICO token** — both private and public contributors get this. This is the utility token that will fuel the project’s use case.

The second token is the **control token** — the owners of these can exercise the control functions of the DAICO — opening the tap, pulling the plug, etc.

This structure makes most of the DAICO attacks financially non feasible. It also empowers the enthusiast crowd — the people who are less likely to be speculators, and more likely to be interested and care about the project.

## Control Token Implementations

There are three ways how control tokens can be implemented:

### 1. Tradable Control Tokens

By default, the control tokens would be transferrable and tradable. They might be sent, received and bought, independently of the ICO tokens.

It does open up a host of interesting economic questions. For example that in this scenario it is possible for someone to acquire a large amount of control tokens, without owning any ICO tokens. That person would be able to influence the project without being financially involved in it.

Whether it’s a problem or not, yet to be seen — but I sense some interesting economic scenarios emerge from this setup.

### 2. Non-tradable Control Tokens

In this scenario, control tokens are awarded together with the ICO tokens, but unlike the latter, control tokens would not be tradable or sendable. In other words, the public sale contributors would get a unique, non-transferrable right to control the project.

One could argue that these are the people who helped the project to become a reality. They should be recognized for this forever, and their right should not be sellable.

This is a defendable, but rather draconian solution — one variant of this could allow the trading of these tokens after a certain time period. Or we can go with hybrid tokens:

### 3. Hybrid Tokens

This method was suggested by [Clément Lesaege](https://ethresear.ch/u/clesaege). Hybrid tokens work like Tradable Control Tokens, but the control would only manifest if the same amount of ICO tokens would coexist on the same address.

In other words, in order to vote with my 10 control tokens, I would have to have 10 ICO tokens on the same address. This fixes the issue highlighted under the first scenario, and keeps the system more flexible than the second scenario.

## Legal Implications

The legal implications of control tokens is unclear. I am checking with lawyers who are familiar with the area.

## Summary

The DAICO attack vectors enabled by a presale can be mitigated by using a dual token structure. There are multiple, non mutually exclusive ways to implement these. Further research, and probably several live sales are needed to find out the pros and cons of each.

Original post on Medium: https://medium.com/@akomba/ico-control-tokens-e328da170514

## Replies

**hochbergg** (2018-03-18):

Thank you - this is very interesting, and is somewhat similar to how in corporations having a ‘controlling stake’ requires special disclosure and limits you from making certain decisions without notification and approval.

Question regarding control tokens - how would these change attack dynamics? Couldn’t the team treat a pair of (token, control token) as a single entity for the purposes of attack? (Give themselves many in presale, buy many pairs in public offering, buy many and close down)

Assuming control tokens initial offering pay into the DAICO, could you explain how that changes attack dynamics?

---

**akomba** (2018-03-20):

Hi, thank you for the good questions.

![](https://ethresear.ch/user_avatar/ethresear.ch/hochbergg/48/892_2.png) hochbergg:

> how would these change attack dynamics?

It would make it financially very expensive to gain majority. Because control tokens would be only handed out during the public phase, when one actually has to send in ether to get the ICO (and the control) tokens.

![](https://ethresear.ch/user_avatar/ethresear.ch/hochbergg/48/892_2.png) hochbergg:

> (Give themselves many in presale, buy many pairs in public offering, buy many and close down)

In the presale, only ICO tokens would be given out. So they can give themselves as much as they want, it won’t directly help them to gain the majority of the control tokens.

Please let me know if the above makes sense or I should elaborate more.

---

**hochbergg** (2018-03-21):

Got it - I didn’t fully grasp that from the article. The structure is:

1. Audit contract to make sure control tokens are distributed only on ICO
2. Control Tokens are distributed as part of ICO (eg. 1-1 with ICO tokens)
3. These may be tradable/not tradable/hybrid

This effectively protects against presale attacks, as control requires a provable deposit of ether.

This does not protect against public sale attacks (tap or closing down), as attackers may still lend ether to buy control tokens covertly.

This may also (Depending on the economics) create another sort of attack where control tokens are cheaper than real tokens, given that individually they give very limited value - and so small holders may choose to sell them in a tragedy-of-the-commons style situation (each small holder would rather have money than control tokens, and so all small holders are incentivized to sell their control tokens).

In a ‘hybrid’ or ‘non-tradable’ situation this attacked is prevented as you either you can’t get tokens (or must pay at least as much in real tokens to get them).

One note on the ‘hybrid’ scenario - if you decide to sell ICO tokens (in a pre-sale, or additional offerings) without selling control tokens, you also reduce the % market cap required to mount attacks. Thats better than not being able to do them at all though.

---

**akomba** (2018-05-23):

I agree with your concerns – but as you seem to conclude as well, this is better than not having it.

Ultimately we don’t have to make it perfect – we just have to make it good enough.

