---
source: magicians
topic_id: 2496
title: EIP-1717 - permanently diffusing the difficulty bomb
author: ligi
date: "2019-01-21"
category: EIPs
tags: [difficulty-bomb, eip-1717]
url: https://ethereum-magicians.org/t/eip-1717-permanently-diffusing-the-difficulty-bomb/2496
views: 1583
likes: 22
posts_count: 10
---

# EIP-1717 - permanently diffusing the difficulty bomb

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/1717)














####


      `master` ← `5chdn:a5-diffbomb`




          opened 09:18PM - 21 Jan 19 UTC



          [![](https://avatars.githubusercontent.com/u/15729797?v=4)
            5chdn](https://github.com/5chdn)



          [+59
            -0](https://github.com/ethereum/EIPs/pull/1717/files)







```
eip: 1717
title: Final Difficulty Bomb Delay and Block Reward Adjustment
[…](https://github.com/ethereum/EIPs/pull/1717)author: Afri Schoedon (@5chdn)
type: Standards Track
category: Core
status: Draft
created: 2019-01-21
```

## Simple Summary
The average block times are increasing due to the difficulty bomb (also known as the "_ice age_") slowly accelerating. This EIP proposes to delay the difficulty bomb for approximately 640 times the age of the universe and to reduce the block rewards with the Istanbul fork, the third part of the Metropolis phase.












My first feeling is no. I kind of like this bomb somehow and think it is a good forcing function. Wonder what others think about this EIP.

## Replies

**ajsutton** (2019-01-21):

Agreed. The difficulty bomb is extremely useful at forcing people to make an active choice about the direction of the network regularly.  You don’t have to accept the Constantinople fork for example, but rejecting it involves proposing an alternate fork to at least delay the difficulty block.

There’s a lot of momentum behind “do nothing” which makes it very difficult to continue to improve and evolve unless there’s some balancing function and the difficulty bomb is that forcing function.

We may however want to be more generous in how long we extend it as part of each hard fork so the time pressure is reduced.

---

**jochem-brouwer** (2019-01-22):

Without a difficulty bomb miners have no incentive to upgrade their nodes, besides of course if the general public does not accept the non-forked coin to have any value. Miners can now easily take the network “hostage” by deciding not to switch.

If miners see that the block reward goes down and there is no difficulty bomb, they can simply decide not to switch. There is no way to force the miners to switch. If the general public sees that the upgraded coin is not being mined most of them will simply use the “outdated” fork - because let’s be real, the majority of people who hold Ethereum right now hold it as an investment and only care about the value, not about the technology.

---

**AlexeyAkhunov** (2019-01-22):

To all the people who are saying that the difficulty bomb makes sure miners have incentive to upgrade their node. If you think about this one for a bit more, you might conclude that the reason miners do upgrade their code ahead of the release is not to avoid the bomb (which might only start having effect in a few weeks), but to avoid mining the fork that has no value (which will start hitting the bottom line the moment miner wants to sell some mined ETH).

I said it before and I will say again - miners will not “rebel” against developers unless there is someone funding alternative group of developers who will continue maintaining their fork. And if there is an alternative group of developers, they will love to defuse the bomb as the first “job”. The fact that the upgraded side of the fork has a backing of entities like EF and ConsenSys gives that side more value than the non-upgraded one, because these entities can help fund maintenance and further development of the protocol for the years to come.

The utility of the bomb in forcing the miners to upgrade is IMO a big red herring. Now to another proposition - that the bomb forces ***developers*** to do something. This is closer to the truth. Although, it would say, when it comes to protocol development, many times it is better to do nothing that to do “something”. It might sound harsh, but many changes made in the protocol over the last two years are non-essential and low impact. Some more difficult but higher impact changes (like account abstraction) were dropped from the release plan because there would not be enough time to get them ready before the bomb.

So it is not so very black and white to me that the bomb is still useful, but I am happy for it to stay if others feel really strongly about it and it makes them more comfortable ![:hugs:](https://ethereum-magicians.org/images/emoji/twitter/hugs.png?v=9)

---

**fubuloubu** (2019-01-23):

I never understood why this makes sense either, it always seemed to just be a stand-in for better project management and keeping to appropriate deadlines/release schedules. What you’re saying makes total sense, and I don’t know why I thought there was a good reason for it.

I think adopting an explicit release schedule would accomplish the same thing in regards to developers, and create a more stable experience for those who run clients (miners, validators, full/archive node providers, exchanges, businesses, etc.)

6 month release schedule:

1. (prior to cycle start) Agree on what major EIPs make it in
2. 3 months prior to release, have alphas prepared for testnet release
3. 2 months prior to release, beta on testnet for wider infrastructure testing
4. 1 month prior to release, NO/GO on release, decide block height
5. 1 week prior to release, all hands GO, exchange contact, social media blast, etc.

or something like that!

---

**boris** (2019-01-25):

Well, this is essentially what [@5chdn](/u/5chdn) proposed for Istanbul, except 9 months rather than 6. See https://en.ethereum.wiki/roadmap/istanbul (which will now be stale because Constantinople do-over).

---

**fubuloubu** (2019-01-25):

Duh, I almost forgot that.

Why do we all think alike??

---

**virgil** (2019-01-27):

Strong support keeping the difficulty bomb.  It’s what keeps us moving and our deadlines honest.  The difficulty bomb helps protect against the sclerosis we see in BTC.

---

**xazax310** (2019-02-06):

I believe the problem with the ice-age was the insane sharp increase in difficulty, now with reduced rewards that was not within the original spec of Ice-age/Difficulty Bomb.

*Allegorically speaking, Two men are in a dry desert. One has access to a well, the other doesn’t. The men with the well helps the other man in by giving small amounts of water. Well gradually he want to move on and stop having him so dependent on him. So first he’ll give him less and less water till One day he decides he no longer want to help the man. But rather than no longer giving him sips of water he decides to splash the water in his face. Well if he does this enough that the man then leaves in search of water, or better yet a nicer person.*

The problem comes down to time-line. I would vote for a slow-gradual increase in difficulty over the course of 2 years or the time-line for PoS. That’s currently up in the air, as far as I know, so there should not be a built in time until the Eth Dev’s agree to a strict time-frame release for PoS.

---

**tjayrush** (2019-02-08):

The difficulty bomb functions as a forcing function. That’s clear. Whether that’s a forcing function on the miners or the developers or some combination of both or neither doesn’t really matter. It keeps the code moving forward.

My concern is that diffusing the bomb has been conflated with lowering the block reward. Think about it. For the Byzantium fork, people used the fact that the increased difficulty (which effectively lowered the block reward over a given time frame) necessitated lowering the per-block reward from five to three. The same argument was made for Constantinople to lower the reward from three to two. Unless they’re arguing that the difficulty bomb was part of the original monetary policy, this makes no sense (particularly because the actual hard fork date is totally at the whim of the core devs).

The bomb is great because it forces forward movement. It’s bad when people use it to justify completely arbitrary decisions to lower the block reward.

Don’t get me wrong. I actually support the lowering of the reward, just not when it’s justified arbitrarily by the difficulty bomb. I don’t think the bomb was ever intended to be part of the monetary policy of the chain. But, let’s don’t start a whole conversation about that.

bomb good – using it to justify arbitrary monetary policy bad.

