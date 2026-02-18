---
source: ethresearch
topic_id: 7184
title: No-loss ponzi- how to allocate interest?
author: astanger
date: "2020-03-24"
category: Applications
tags: []
url: https://ethresear.ch/t/no-loss-ponzi-how-to-allocate-interest/7184
views: 1980
likes: 0
posts_count: 10
---

# No-loss ponzi- how to allocate interest?

I’m building a ‘no loss ponzi’ and struggling to come up with an appropriate formula for allocating interest.

The idea is simple: deposit Dai. Dai earns interest. Interest is given proportional to when you added your Dai to the pool. So if you are a later investor, some of the interest on your Dai is given to those that got in before you. You can always withdraw your original Dai- hence, no loss.

Assume the following two simplifications, which make the maths easier:

- users can only deposit 100 Dai at a time. Let’s conceptualise this using NFTs. Instead of ‘depositing’ dai, you mint an NFT at the cost of 100 Dai.
- users can never withdraw only their interest, they must withdraw their principle at the same time (by destroying the NFT). They will then lose their spot in the ponzi pyramid.

I’m struggling to come up with a formula that will work out how much interest each NFT is owed when they try and sell/destroy their NFT that does does not have some fatal flaw.

### Idea 1: rank all NFTs, payout according to rank.

The first NFT created has rank 1, the third rank 3, etc. We can then use a formula like this to allocate interest to each NFT:

Interest allocated to each NFT = Total interest  * ( n + (n - 1)/2 - (r - 1) ) / n^2

Where n = the total number of NFTs and r = the NFT’s rank. If we have three NFTs, this formula gives 44% of the interest to the first, 33% to the second, 22% to the third.

**Problem 1:** I do not believe it is possible to implement this without using unbounded loops. Because, if someone ‘sells’ their NFT, then the rank needs to change for all NFTs of a higher rank. If someome sells an NFT with rank 5, then NFT with rank 6 will now have rank 5, all the way up to rank N. Is there a way to do this without unbounded loops?

**Problem 2:** it ignores the fact that earlier investors need more interest anyway, before it is ‘ponzid’, simply because their Dai has been accruing interest longer. More specifically- someone could mint a fresh NFT and even though they would have the worst (highest) rank, they would still have some interest allocated to their NFT even though the Dai contributed has yet to accrue a single wei-Dai in interest, so the incentive would always be to just mint then instantly destroy the NFT.

### Idea 2: payout according to timestamp.

If we were to payout with zero ponzi rules, simply on how long they have invested we can use this formula:

Interest allocated to each NFT = Total interest * ( Tc - Tp  ) / ( ( Tc - Ta ) * N )

Where Tc = current timestamp, Tp = timestamp NFT purchased, Ta = average (mean) purchase timestamp of all NFTs, N = total number of NFTs.

This is great, and solves both problem 1 and 2 above. It solves problem 1 because when an NFT is destroyed, you only need to update one variable- Ta. No loops needed. And of course it solves problem 2 because it is directly allocating interest based on time.

The problem, of course, is that there is no ‘ponzi’ element. There is zero incentive to get in early.

I thought I had a genius solution to this: when allocating interest- don’t use the actual purchase time of each NFT, adjust it. For example:

adjusted purchase time = Tp - (Ta - Tp) * W

Where Tp = timestamp NFT minted, Ta = mean purchase timestamp of all NFTs, W = ponzi weighting factor (the higher, the more ponzi’d it is)

This will have the effect of decreasing the timestamp for NFTs that were minted before the mean purchase time, and increasing the timestamp for NFTs that were minted after the mean purchase time. We can then throw this adjusted Tp into the previous formula, and those who got in before the average time will see an interest boost, those that got in after will see a drop. There is now an incentive to mint your NFT early- it is ponzi’d! I thought I was real clever here. But no:

**Problem 3:** newly minted NFTs will end up with an adjusted purchase time that is in the future. Therefore, new NFTs will have a negative interest allocation, and the whole project will no longer be a ‘no loss ponzi’.

---

Can anyone think of a way to solve either Problems 1&2 (so that Idea 1 can be implemented), or Problem 3 (so that Idea 2 can be implemented)? Or perhaps some entirely alternative approach that I am failing to see? It is not unlikely there is some very obvious solution that I can’t see…

From a UX perspective, I think Idea 1 is the better approach, if it can be made to work, because I like the idea of the ‘order’ being important- just like a real ponzi, it SHOULD make a big difference if you get in a second before someone else. With Idea 2, it makes effectively no difference if you get in a second before someone else. Yet I fear Idea 1 is a non-starter.

## Replies

**monteluna** (2020-03-24):

Just trying to think about this in a sort of algorithmic way using rough ideas. Why not think of the problem like this…

tK          := Chai | cDai | any other interest representing token.

Pool      := Pool of tK.

Chain n := { User, n, (Chain n-1) } | { User, 0, (Empty) } | Empty

User      := { Address }

Now the problem really boils down to how to allocate tK to a User who wishes to break the chain, and how to add a new user. I think this entire problem then becomes managing the tK widthdrawals from the tK Pool. Imagine if the chain is empty. User 0 comes in and adds to the Pool of tK with their Dai deposit, but can only widthdraw their own interest. User 1 comes in and adds to the Pool of tK, but now instead of receiving their tK that they first started with, they need to widthdraw only the amount of tK equal to 100 Dai. Since that tK price is always lowering, this is pretty much “widthdraw from the pot exactly 100 Dai”. The general case is pretty hard. You have to allocate a time dependent widthdraw for everyone else that also depends on the total amount left in the pot.

The cases break down pretty easily in terms of the parameters k and n for both the Add and Remove functions. Note here, the 0 user is the bottom of the ponzi chain getting the most interest.

Some rough ideas of all these cases are below:

Add (User a) Empty := Chain { (User a), 0, (Empty) }

Add (User a) (Chain n) := Chain { (User a), n +1, (Chain n) }

Defining these functions are pretty easy above and I’m sure these are mostly about managing the chain. The hard parts are the Remove functions on the chain. Again, some rough ideas of the cases are below.

Case: For any k, Remove k (Empty).

- Removing from an empty Chain is pretty much null.

Case: For any k, For any n, if k > n, Remove k (Chain n)

- Removing position k from a chain of length n where k is greater than n is also pretty much null.

Case: For any k, For any n, if k == n, Remove k (Chain n)

- Removing position k from a chain of length n where k equals n is the best case. This is the top case where this user didn’t earn any interest because there’s no one above them. In this case, the number of tK they started with should probably be reduced over time. They want 0% interest, so as the value of tK they can pull out should be reduced according to the interest rates.

Hard Case: For any k, For any n, if k = 0, Remove k (Chain n)

- I think in this case it’s time dependent. Think of the case for Chain 1 (two users). The top person’s tK output is reducing to keep a fixed Dai amount, so obviously the bottom person’s tK allocation must be increasing. I’ll chat more about this below.

General Case: For any k, For any n, Remove k (Chain n)

- This is the worst case when someone is in the “middle” of the chain. Piggybacking off the last case, it’s likely some users will have increasing tK, while others will have decreasing tK. The point here is to obviously allocate your in-chain interest in terms of the tK interest via a Dai price feed, essentially giving people higher up the chain lower interest than the people below. Maybe someone else could come up with some algorithm for this? If you can convert a user’s position directly to the interest they should receive dependent on the chain length, then the conversion from that to equivalent tK via the Dai price feed should be easy.

Kind of coming up with my own, let’s just do for every new user, the interest is evenly split between the existing users. In units of INT where 1 INT is the going rate for interest., oing with a chain of length 2 is a good start. Obviously the user 0 earns 2 INT, since that’s an even split between the existing user of 1. As more users come on, there’s more interest to allocate. For 3 users, user 0 earns 2.5 INT, user 1 earns 0.5 INT, user 2 earns 0. For 4 users, User 0: 2.5 + 0.3333 INT, User 1: 0.5 + 0.3333 INT, User 2: 0.3333 INT, User 4: 0.

I also think this could be a completely wrong approach. I’m not taking into account fluctuating interest rates, mostly because I think tK takes care of this under the hood, but the nature of the time-dependent calculation makes this wonky. You have to allocate tK at some rate that matches the earned interest, but earned interest depends on the DSR or Compound rates. Again taking an edge case, if tK = Chai, no one on the chain earns any new Chai so they’re getting back exactly the same Chai they put in. These are just some thoughts but maybe someone can piggyback on a different approach.

---

**astanger** (2020-03-25):

Thanks for this. It is certainly helpful to see the problem phrased with a bit more mathematical formality. Hopefully it helps someone else think about this in a different way.

You are right in your final paragraph (if I understand you correctly) that you do not need to take into account fluctuating interest rates, as that is taken care of under the hood.

I had another idea, but I think it runs into the same problems as the previous solutions, but here we go: interest is not originally pooled, each NFT earns interest independently. This is easy to track, each NFT would have a specific number of cDai which never changes- equal to 100 Dai when the NFT is minted but gradually more than 100 Dai over time. Anyway, the new idea is that whenever an NFT is destroyed, only 50% (for example) of the accrued interest is returned to the user, with the remaining 50% put into a pot. And future sales of NFTs would get a fraction of this pot, in addition to the interest from their own cDai.

This would appear to have the same problems as the previous solutions (mainly: how do you prevent new NFTs getting a share of this existing pot straight away without loops) , but maybe it is a helpful jumping off point for other ideas. It seems that part of the problem is the existence of a central pot where all interest is accumulated, so any attempts to minimise the existence of such a pot may help…with this new idea, this pot only holds ‘surplus’ interest and not the interest already owed on specific NFTs.

---

**denett** (2020-03-25):

I think an easiest way to accomplish this is to add levels. When a level is full, new signups will go to the next level. Every level is bigger than the previous. The interest earned per level is shared among the participants of all the previous levels. When a participant leaves you can easily calculate his/her share of the interest.

---

**astanger** (2020-03-26):

[@denett](/u/denett) an interesting idea, however I think this may run into the problem of requiring unbounded loops when calculating how much interest a user receives upon withdrawing? Assuming there is no limit to how many levels there are- and there can’t really ever be a limit on this, because if it ever got to the last level there would be zero incentive for anyone to join.

However, this certainly massively reduces the number of loops required- instead of being bound by n, it is now bound by n/[users per level]. A step in the right direction no doubt!

---

**denett** (2020-03-26):

When the size of a level increases with a certain percentage with each level, the total deposited amount increases exponential. So at a certain point we will run out of money, before we will run out of levels. For example when we start with 1000 DAI on level 1 and increase each level with 10%, the total amount of DAI deposited when we reach level 100 is more than the current market cap of DAI.

---

**astanger** (2020-03-27):

[@denett](/u/denett) Yeah that makes sense! In related news, I have come across binary search trees which greatly reduce any problem with too many loops.

However, I find myself still left with Problem 2 from the OP- namely, if users get access to a % of interest and their % is determined by their position (either each with a unique position, or ‘levels’) there is still the problem of new users immediately having *some* interest allocated to them immediately, such that the incentive is always to deposit and immediately withdraw.

---

**denett** (2020-03-27):

As I described it, the interest earned is distributed among the participants of all previous levels. So you will not earn interest until your level is full and participants are added to the next level. Since all previous levels are allready full, the interest accrued by your deposit can be distributed equally. When someone of one of the previous levels leaves we can calulate its share and subtract it from the accrued interest. After that, the interest is divided among less participants.

---

**astanger** (2020-03-27):

Apologies, I had forgotten that aspect of your approach, that you only get interest from levels above, which does indeed solve the problem.

Denett I think you’ve cracked this problem as well ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) You have solved both my issues, thank you very much indeed!

If I implement this I will let you know so you can snag yourself some room on level zero ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

---

**Jungle88** (2020-12-29):

Sounds really interesting! Really curious how it plays out.

Would love if you could let me know when you’re launching… happy to help promoting ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

