---
source: ethresearch
topic_id: 8328
title: Price of forgery digital identity. Measuring human uniqueness score in dollars
author: porobov
date: "2020-12-07"
category: Applications
tags: [identity, sybil-attack]
url: https://ethresear.ch/t/price-of-forgery-digital-identity-measuring-human-uniqueness-score-in-dollars/8328
views: 1717
likes: 1
posts_count: 1
---

# Price of forgery digital identity. Measuring human uniqueness score in dollars

Imagine someone is building bot armies and then sells them to whoever is interested. What is the sell price?

## Harnessing the shadow market

In order to agree on the bot price the buyer and the seller probably rely on some parameter to measure the bot quality with. Probably it is the total number of social connections, or how well the bots are connected with a “target” account, or it is the lack of bot clusters. Probably the quality depends solely on some specific purpose of the buyer, on how they are going to use the bots. **The fact is we don’t know the parameters. And we cannot predict the price.**

How much do users value their accounts? How easy it is to create a fake account? Can this platform’s accounts be used as a verification method? The price of an account is a very reliable metric to asses the quality of the platform’s audience. It would be really helpful to know it. But there is no simple way to get it. There is a market but it is in a shadow.

Upala uses the same shadow market forces to get an account price precisely, easily and immediately. Upala provides digital identity uniqueness score which is measured with this price. In other words Upala’s account score corresponds to the efforts needed to forge the account (price of forgery). Let’s see how Upala makes it possible.

## Upala main concepts

First lets have a briefest dive into two major concepts behind Upala.

**1. Groups.** Users join a group. They put their deposits in the group’s pool in dollars (DAI). The group assigns scores to all of its users.

[![](https://ethresear.ch/uploads/default/optimized/2X/9/9b267bbed8324ae0a4e5953326b35017036c5f40_2_690x431.png)1280×800 144 KB](https://ethresear.ch/uploads/default/9b267bbed8324ae0a4e5953326b35017036c5f40)

**2. Explosive bots protocol.** The score is also valued in dollars. And the score is higher than the deposit. It represents the explosion price - an amount of money that an identity holder can get at any time for deleting their ID.

When exploding, an attacker betrays other members of the group (steals their money). This group will not let the attacker in again. So if that person wants to create a new Upala ID and get some score they’d have to build trust within some other group of people.

This is what incentivizes groups members to let only trusted people in.

[![](https://ethresear.ch/uploads/default/optimized/2X/c/c9f711622e6325a8400c9b4463f567d07f9dbe36_2_690x431.png)1280×800 171 KB](https://ethresear.ch/uploads/default/c9f711622e6325a8400c9b4463f567d07f9dbe36)

Deposits are not necessarily money. It could be any other value or efforts “put on stake” - like solving captchas, sms-verification or real-world reputation. The group can decide on any verification method. And the pool is not necessarily consists of user deposits - it may have outside sources (works a lot like insurance). Groups may earn by charging DApps for providing scores to them or earn interest on their pools (or other - Upala allows arbitrary incentive and governance models). Have a look at this [video](https://www.youtube.com/watch?v=u_jAXgcvjyg&t=1s) or check out the [Upala docs](https://upala-docs.readthedocs.io/en/latest/index.html) to have a deeper dive.

## The score is the sell price limit

Back to our bot sellers. Explosive bots protocol gives a bot owner a choice to sell the army or to explode every bot in it. It makes no sense then to set the sell price lower than the explosion price. It would be easier just to explode and get an amount of money corresponding to the combined scores of the bots, effortlessly and deterministically.

At the same time one cannot set the sell price too high, as there are other bot owners around willing to sell. Someone else will create an army of the same quality and lower the prices.

The ultimate limit of the sale price is the explosion price. The competition in this bot shadow market will constantly push the sell price down to it (and explosion price equals the score, as described above).

`sell_price → score`

`bot_owner_income = score - efforts`

## What a group can do

Let’s examine the situation from the viewpoint of group owners and managers.

A group starts to see explosions among its members. Managers now have a choice either to lower the scores, or to strengthen the entry tests. So that next time a malicious user wants to create a bot it would be harder to do or cheaper to sell (or both). Both changes will make the group less attractive for malicious users.

But the same changes will make it less attractive for ordinary users as well. Existing users don’t want their score to be lowered. And new applicants will have to put more efforts (e.g. more time on CAPTCHA, prove another social network profile, deposit more money) in order to get a score.  Users have their choice too. They will just chose a group with better **score/efforts ratio**.

## What a group should do

A better option for group managers is to **make it harder for malicious users only**.

Malicious users want to earn. So they are looking for groups where the score could compensate for the efforts spent on creating a bot army and provide some income. Malicious users are looking for groups with the best **score/forgery_efforts ratio**:

`bot_owner_income = score - forgery_efforts`

Forgery efforts are not the same as non-malicious efforts. These efforts include research, coding, bribery, etc - paying machines to act like humans and paying humans to act like other humans  (recognizing images containing traffic lights maybe?).

It makes sense for the group managers to focus on entry tests that make only these efforts harder. The perfect entry test then is the one that allows **any human to pass without any efforts but only once.** This is what groups will focus on.

## Market

By increasing forgery efforts groups may **push the scores up** and attracts more users. This is the only way to outperform competitors. The wider the gap between the efforts of a malicious user and a good one, the better. The most effective human tests win and get the most profits.

At the same time bot owners will focus on inventing new methods of exploiting entry tests and try to lower their forgery efforts. The perfect forgery method is the one that passes an entry test with no efforts (for free) and for as many times as needed. This is what bot owners will try to achieve.

So bot owners is the opposite market force. They don’t let the groups set scores higher then their forgery efforts as they will explode. And they will also drive the sell price close to explosion price to outperform their evil competitors in turn. **Bot owners push scores down.**

[![](https://ethresear.ch/uploads/default/optimized/2X/1/1be99f1de401aefe0862c5ecb10e3f0dc27d55da_2_690x431.png)1280×800 48.9 KB](https://ethresear.ch/uploads/default/1be99f1de401aefe0862c5ecb10e3f0dc27d55da)

As the minimum score that bots can afford equals to the forgery efforts and the maximum score that groups can afford is the forgery efforts too - the score is attracted to this equilibrium. The score  represents the forgery efforts! Or as we call it the price of forgery.

`bot_owner_income → 0`

`score - forgery_price → 0`

`score → forgery_price`

## Example

Let’s say we created a group that uses SMS verification to assign scores to users. Every approved user gets a $5 score. If someone can get an sms verified for $1 they can generate 1000 accounts and earn $4000 after explosion (or even more if they would manage to sell the army for a higher price). Here the group owners will have to lower the score provided by sms-verification to $1 - as it is the real forgery price of this method (actually, they first have to lower even further and then increase the score gradually to “find” the $1 value). And they’d better think about moving to another method of verification, that could provide their users with the same $5 score again or more.

## Conclusion

Knowing forgery price is priceless. With a metric like this DApps know exactly how much trust they can put in a user. It is like quality control for identities.

Bringing decentralized identities to blockchain may unlock many unforeseen and wonderful use-cases.

The new market forces provided by the price of forgery identities will create an incentive to constantly enhance human verification methods and increase price of forgery (scores) accordingly. One day we may see identities that are harder to forge than the existing state IDs.

Upala links:

- Github
- Docs
- Gitcoin grant
- Upala Dashboard
- Telegram
- Twitter

You are part of the resistance now😉. Thank you for reading!
