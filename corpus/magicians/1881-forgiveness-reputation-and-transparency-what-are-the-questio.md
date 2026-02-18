---
source: magicians
topic_id: 1881
title: Forgiveness, reputation, and transparency. What are the questions?
author: chaals
date: "2018-11-12"
category: Magicians > Primordial Soup
tags: [reputation-systems, reputation-types]
url: https://ethereum-magicians.org/t/forgiveness-reputation-and-transparency-what-are-the-questions/1881
views: 1189
likes: 12
posts_count: 10
---

# Forgiveness, reputation, and transparency. What are the questions?

This is a starting point for a discussion that began as oral history in the council of prague.

There are a lot of places where reputation systems are valuable - but on the blockchain they live forever. That’s problematic in reality:

- One reason for reputation systems is to avoid permitting bad actors to continue acting badly. Allowing people to create new identities at will completely defeats this use case. Less seriously, in many numeric systems anyone who has an average below e.g. 4 stars just creates a new identity and starts again, so values below 4 are only theoretically meaningful.
- Many real social systems provide for some form of forgiveness, potentially predicated on elapsed time or specific actions or circumstances.
- In some jurisdictions, there are now legal requirements that you do not drag up various bits of people’s alleged past. Failing to solve the problem excludes a whole class of people from participation in a reputation system on fairly dubious grounds.

There is an inverse case, where someone recommended somebody because their interaction was wonderful, but it later turns out that the recommended person did something terrible in the same situation to someone else, and so the recommender wants their recommendation to be “forgiven” - i.e. no longer taken into account.

See also the [essay on reputation types by @kronosapiens](https://hackernoon.com/reputation-systems-promise-and-peril-ae0af60595ea) that pulls at some of the questions, as referred to from the [thread starting a sub-ring on reputation types](https://ethereum-magicians.org/t/cop-trust-reputation-sub-ring-types-of-reputation/1818)

(as far as I can tell, this topic is related to some rings but is really at the level of primordial soup. Feel free to suggest it should be marked otherwise).

## Replies

**billygrande** (2018-11-13):

Reputation systems are a real problem in the medical community where doctors, dentists etc. have to deal with all sectors of society often on their own with no available security. Everybody gets sick including people with very serious social problems. Being married to a medical professional I see that most of the reviews people leave on our friend’s Google reputation thing are negative because quite frankly WHO BOTHERS TO LEAVE POSITIVE REVIEWS ABOUT THEIR DOCTOR ANYWAY. You gotta be one sad self-important person if you think you should be contributing to a doctor’s “reputation”. All the negative reviews are about the “attitude” of the doctor too as though a doctor should be trying to sell you an Iphone with a cheesy ass smile or something. People forget that the attitude of the doctor (especially female) might be because they are scaring the crap out of her with their Whiskey breath and crude chat up lines. These crazy patients then run to the Internet and vent their frustration after experiencing a cold shoulder. This is really a very negative aspect of geek culture and contributes to geek hate among the educated sectors of society. Medical reputations and complaints are handled by competent governing bodies and if a health professional is practicing it means they are recognized by their state. I know for a fact that there is a major push back coming down the pipeline in Europe regarding these “star review” things. It will lead to restrictions on all of us eventually if we are not careful. I recommend non-pursuit of reputation systems for blockchain devs.

---

**ravachol70** (2018-11-14):

There would be a working standardisation here, amenable to implementation via ERC-1410.

---

**kronosapiens** (2018-11-15):

One distinction I think it would be helpful to make is between reputation systems in which there is a “starting  score” that someone can fall below, and one where you start at 0 and can only go up.

Take for example the Uber rating: you begin with a perfect 5-star rating, and then you work to maintain that rating over time. More ratings both makes your rating robust, but inevitably brings it down. You work to **maintain** a high rating.

In contrast, consider a “video game” type of leveling system, in which you begin at 0 and can only become stronger. In some games, if your character dies, you reset to 0; that is the most severe punishment, since all of your work is lost.

Note how in the Uber case, work is done to prevent a rating from decreasing, while in the games case, work is done to strictly increase a rating (denominated in levels).

In regards to forgiveness, I would say these systems behave differently. In the Uber case, we cannot simply allow someone to “start over”, since the rating incorporates past misdeeds; a fresh start would allow people to escape from the consequences of bad actions. In the games case, on the other hand, anyone can choose to start over at any time; starting over necessarily means *foregoing gains*, rather than *escaping sanctions*.

I would like to suggest that a level-like system allows for handling forgiveness more easily, as “forgiveness” can be invoked by the individual at any time, if they feel like the benefit of a fresh start outweighs the burden of starting over. There is less of a need for a system of rules determining how and when sanctions are forgotten by the system.

---

**chaals** (2018-11-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kronosapiens/48/699_2.png) kronosapiens:

> I would like to suggest that a level-like system allows for handling forgiveness more easily, as “forgiveness” can be invoked by the individual at any time, if they feel like the benefit of a fresh start outweighs the burden of starting over. There is less of a need for a system of rules determining how and when sanctions are forgotten by the system.

True. But often the purpose of a reputation system means you can’t just institute a level system. Reality is less linear than either a permanent record or a level system. Your credit score goes up and down according to how well you make repayments. Your bankruptcy is discharged one day, but until then you are not allowed to do certain things - the option of resetting is not there.

Likewise some places regard having committed a misdeed as a permanent reason to exclude you from full participation, while others have strong rules about forgiveness and make it a misdeed to recall things deemed to have been expunged.

---

**kronosapiens** (2018-11-21):

That’s fair, but I would suggest a second look at a level-like system. StackOverflow is a classic example of this mechanism working well. There are a lot of dynamics at play in reputation, and a lot of reasons why we might want to grant or withhold specific privileges; no fixed set of rules will be able to encompass them all. I like levels because they give us a simple knob to play with (number of points), make it easy to define punishment (loss of points), and give us flexibility to assign different privileges to different levels. Is discharging a bankruptcy after X years **really** so different from docking someone some number of levels which will take X years (on average) to regain? I would even say docking levels is a better punishment, since a motivated person could work harder to rebuild faster; a punishment of a fixed number of years removes that incentive.

---

**Ethernian** (2018-11-21):

It is already some years ago, but I remember it was a good presentation by Andres Junge in DevCon1 in London about challenges in reputation systems.

Please find [youtube video here](https://www.youtube.com/watch?v=W63oB4fbnEg).

.

---

**billygrande** (2018-11-28):

Maybe rating systems shouldn’t be defined by the likes of us who can hide behind a screen but by police, teachers, doctors, military, social workers etc. who are on the front lines of society  and understand the human cost of such systems.

We should concentrate on building a system that doesn’t crash when a few people want

to buy a digital image for LOLs (cryptokitties).

---

**chaals** (2018-12-02):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/b/9d8465/48.png) billygrande:

> Maybe rating systems shouldn’t be defined by the likes of us who can hide behind a screen but by police, teachers, doctors, military, social workers etc. who are on the front lines of society and understand the human cost of such systems.

That would be great. But in the meantime those people are often busy in their jobs, and people **are** defining rating systems. So we should at least consider the implications as best we can.

It is also the case that if you ask a set of doctors, soldiers, police and social workers you are likely to get a pretty varied set of answers about what we need. Especially depending on which individuals you ask.

---

**wschwab** (2018-12-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chaals/48/1515_2.png) chaals:

> we should at least consider the implications as best we can

Maybe instead of looking globally at the implications of reputation systems, we need a framework of relevant questions to help cater reputation systems to the specific circumstances that they’re being implemented in.

What I mean is that it would seem that there is no one reputation algorithm to rule them all. Different situations call for different systems. I don’t think that it’s possible to enumerate every possible permutation of reputation system, but maybe there is a way to identify basic themes, and develop categories of reputation systems?

Just as an idea: Earlier in the thread Uber and level-based video games were mentioned. In the second, the ability to increase the rank of the character is critical to the user’s interaction with the game. While such a principle could be introduced at Uber, in the current scheme, they are not looking for character/driver development. This would categorize the two ranking schemes differently.

(As mentioned above, they could also be differentiated on a technical level: Uber is using an averaging system, in which the participant will always average out between 0 and 5, whereas games use an additive system. StackOverflow, mentioned above, uses a bi-directional additive and subtractive system. Different types of categorization are good.)

