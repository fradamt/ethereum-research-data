---
source: ethresearch
topic_id: 3583
title: Rabbit-or-Child Dilemma in Plasma implementations
author: MihailoBjelic
date: "2018-09-27"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/rabbit-or-child-dilemma-in-plasma-implementations/3583
views: 1564
likes: 3
posts_count: 8
---

# Rabbit-or-Child Dilemma in Plasma implementations

Plasma implementations generally rely on exits and challenges as mechanisms to protect users, i.e. their funds, from operators’ malicious actions.

We can notice and unavoidable dilemma that precedes any such exit and/or challenge. Let’s say a potentially malicious action is noticed (e.g. block root/header is submitted to the main chain but the block is not available). At this moment, every Plasma user (or their client software) has to choose one of the following options/strategies:

1. “Rabbit” strategy - The user doesn’t want to take any chances and immediately submits an exit (named like this because rabbits run away at the slightest sign of danger).
2. “Child” strategy - The user believes that the action is not necessarily malicious (e.g. it could be just a temporarily crash of the operator’s server), and decides to wait for some time (named like this because children are innocent and trustful).

There are tradeoffs for both. By choosing the “rabbit” strategy, the user can easily waste their time and money “running away” from (and then “coming back” to) an honest operator who really just had a temporarily technical issue. Also, if the majority of users in the Plasma ecosystem prefer this strategy, that can be cause issues for the main chain (too many exits → clogged main chain). On the other hand, by choosing the “child” strategy, the user can completely lose the chance to submit an exit (or challenge malicious operator’s exit) at a later point in time (e.g. the main chain can get clogged in the meantime), and consequently lose all of their funds (this especially relates to Plasma MVP).

Also, it’s not clear who should be making the decision - the user themselves or the client software?

To make this decision somehow easier, it might be good to have some sort of scoring for Plasma chains/operators in the future. Having that, we can even try to design a simple hybrid model for such situations:

1. A potentially malicious action is detected by the client software
2. UI notifies the user about the issue, provides the scoring to support the decision, and waits for the user’s input (e.g. “We were unable to download block #345678 from the OmiseGO chain. Their score is Great (9.8/10). Do you want to submit an exit (0.2ETH available)? [Yes]/[No, update me in 1 hour]”
3. The users provides an input and the software acts accordingly.

Thought and comments are welcome.

## Replies

**bharathrao** (2018-10-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> UI notifies the user about the issue,

This would require them to keep the app always on. What if the user has closed his browser/UI? I don’t see how any user won’t opt for automation if the option is available

---

**MihailoBjelic** (2018-10-31):

Thanks for the comment! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Probably the only thing that’s sure about users is that you can never know what will they do/how will they behave. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Also, I thought the client/app has to be online anyways (to watch both the Plasma chain and the main chain)?

That said, I believe that most of the users would indeed choose the automatic mode (the software makes the decision). This would put all the burden on system designers (they need to decide between the two strategies and take responsibility for the decision).

---

**Dapploper** (2018-10-31):

I think it’s really important issue in terms of UX. When we designed any plasma model, we just assumed that every user will run the full node on plasma chain. But this is not that good for ordinary users like what you said because they should stay awake all days for looking into what’s going on in the plasma chain that they use.

I think we can divide this problem(staying awake all days) into two, one thing is for staying for the challenge and the other is staying for the exits.

Actually, it’s not that a big problem in the challenge. Since there is always some incentives for validators(they could be users or not), we don’t need to worry about in terms of UX here. For example, we could force exiter or the operator to deposit some bonds in the contract and give it to any challengers who did successful challenge. Then there will be always some challengers who are running full nodes to detect if the operator do bad things or not. In this case, if only one validator is honest and online, then all users can be protected by this challenge system even if one does not running full node.

But in the case of exits, which are specifically invoked because of the data withholding (and this is hard to be resolved by the challenge mechanism), it becomes quite complicated. Except for the plasma cash-like models, every other models like based on the plasma-mvp have kind of similar time-attack-like exit mechanism. (ex. Priority) Because the time matters, every user has to see if the operator withholds the data or not.

Eventually, the problem what you stated here is actually about how we can build robust solution for data unavailability. And this is why I think that the data unavailability is way much more important than the challenge system(a.k.a fraud proof) in Plasma.

---

**bharathrao** (2018-10-31):

The requirement for every user to be responsible for the safety of their coins is a problematic UX issue. The plasma paper had the concept of mass exit for this reason. Effectively, it states: “Exit if most people think its a good idea to exit”.

You could have a threshold exit to deal with it:

`function thresholdExit(myutxo) { if (10% of chain value wants to exit) then exit(myutxo); } `

Regardless, there is going to be a stampede effect that will overwhelm the chain. There is no clean way to address this in an UTXO system.

---

**Dapploper** (2018-10-31):

Maybe we can build mass exit system like stop-loss option in trading stocks or something. I think it would be better to set various thresholds for mass exit. (ex. 10% of chain value wants to exit => just warn me / 20% => ask me whether exit or not / 30% => definitely do exit right now)

---

**nourharidy** (2018-11-08):

As far as I am concerned, the main usability of Plasma chains from a user perspective is to “enter” them for short periods of time to transact at high throughput for an intended purpose whether it is simple transfers, DEX, gaming, etc. The main chain would act as bridge that moves value between multiple “plapps” as well as an expensive but safe long-term store of value. Therefore, it is acceptable to assume that each user can check the Plasma chain at least once a week in order to exit if required. A user who intends to store/hold their assets securely for longer periods of time without frequent usage should just keep them on the main chain. A good metaphor can be the utility of a personal wallet vs a that of a personal safe. Money is most secure when it is locked up in an expensive big heavy safe for as long as you need, but you do not carry your safe outside to pay for your coffee, instead you take your wallet out everyday with little sums of money. If you keep large sums of money in your wallet when you leave your house, you always have to be extra careful and make sure it doesn’t get picked up by strangers. Except that you have more chances of stopping a stranger from exiting a Plasma chain with your money in 7 days than you have chances catching someone trying to steal your purse in just a moment.

Following the above rationale, I suggest an automated Rabbit strategy. Due to the fact that it is fair to believe that users of a specific Plasma chain will most likely have a relatively small percentage of their assets placed inside which they use for day-to-day transactions (e.g. buying coffee). In this case, a temporary freeze of their Plasma chain assets for a challenge period of 7 days can be deemed acceptable from a usability perspective because, until the challenge period is finished, they can go get some more money from their big heavy mainnet “safe” or just use their money already available on alternative Plasma chains.

Another reason to support an automated Rabbit strategy, is the potential security reduction assuming there is a possibility of the Child strategy being followed by some users. If a dishonest operator can assume that a number of participants who carry assets larger than the security bond will follow the Child strategy, the operator can be incentivized to carry an attack because it may be likely to be profitable even when their bond is slashed. It could be thousands of participants each with negligible assets but the collective value of their assets can be larger than the operator’s bond. Therefore, an automated Rabbit strategy without any user interference must be mandatory across most clients in order to act as a deterrent to the operator.

---

**MihailoBjelic** (2018-11-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/nourharidy/48/2143_2.png) nourharidy:

> As far as I am concerned, the main usability of Plasma chains from a user perspective is to “enter” them for short periods of time to transact at high throughput for an intended purpose whether it is simple transfers, DEX, gaming, etc. The main chain would act as bridge that moves value between multiple “plapps” as well as an expensive but safe long-term store of value. Therefore, it is acceptable to assume that each user can check the Plasma chain at least once a week in order to exit if required. A user who intends to store/hold their assets securely for longer periods of time without frequent usage should just keep them on the main chain. A good metaphor can be the utility of a personal wallet vs a that of a personal safe.

I disagree. This is an analogy primarily used for Bitcoin and the LN; I argue that Ethereum is a way more potent platform/tech with way more use cases, so IMHO we shouldn’t be limiting ourselves to these “buy coffee” Plasma chains.

![](https://ethresear.ch/user_avatar/ethresear.ch/nourharidy/48/2143_2.png) nourharidy:

> Therefore, an automated Rabbit strategy without any user interference must be mandatory across most clients in order to act as a deterrent to the operator.

Automated Rabbit strategy in a situation where we have hundreds or thousands of Plasma chains will almost certainly clog the main chain on a regular.

