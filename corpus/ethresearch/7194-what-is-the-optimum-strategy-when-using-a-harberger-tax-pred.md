---
source: ethresearch
topic_id: 7194
title: What is the optimum strategy when using a Harberger Tax prediction market?
author: astanger
date: "2020-03-25"
category: Applications
tags: []
url: https://ethresear.ch/t/what-is-the-optimum-strategy-when-using-a-harberger-tax-prediction-market/7194
views: 1612
likes: 1
posts_count: 7
---

# What is the optimum strategy when using a Harberger Tax prediction market?

I’m currently building one of these, and [@monteluna](/u/monteluna) asked me what the optimum strategy is- for example, if I think that X outcome has a 20% chance of winning, under what conditions should I be adding money to the system? And I realised that I had no idea what the answer is.

Here is how it works. There is one NFT for each outcome of an event. Let’s say, the event is the US Presidential Election, and there are two outcomes- Trump or Biden [let’s assume Biden gets the nomination]. So there’s a Trump NFT and a Biden NFT.

Anyone is free to ‘rent’ each token at any time, by stating a daily rental price and submitting Dai to fund the rent. Anyone else is free to take the token off them at any time, if they quote a higher price. If the current owner’s deposit runs out, it returns to the previous owner, at the previous price. If there are no previous owners, the token price drops to zero and is unowned.

So this is effectively a Harberger Tax where the ‘tax’ is 100% a day. The concept of ‘daily rent’ is just a way of abstracting this. There is one fundamental difference to normal Harberger rules- when you wish to purchase a token, you do NOT pay anything to the current owner. Arguably, this means that the tax rate is infinite, depending on how you define such things.

Anyway. The total rent paid among both tokens is held by the contract, at the end of the competition, it is paid out to all the owners of the winning token, in proportion to how long they owned it. If 1000 Dai is paid in rent among both tokens, and I own the Trump token for 25% of the total time, and Trump wins, I would win 250 Dai.

This is the question: assume I think trump has a 50% chance of winning. Under what conditions should I rent the Trump token? Perhaps, the Trump token is currently being rented for 25 Dai a day, with the Biden token being rented for 75 Dai a day. These translate to implied odds of a 25% chance of a Trump victory- so it would seem that, if I think that Trump has a 50% chance of winning, I should rent the Trump token at the lowest possible price until the implied odds rise to 50%.

But it is not as simple as that, because it ignores a) the total rent already held by the contract and b) how long I am likely to own the Trump token for.

Anyone have any ideas what a slightly better, if not optimum strategy would be?

## Replies

**denett** (2020-03-25):

On the last day before the election when the chances are still 50-50. You would pay up to 50% of the average rent paid per day for each side, because then you get a 50-50 bet. So you can expect that on the last day the pot will accrue the same amount as it has accrued on average. Recursively this means that you can expect that in all future days the amount accrued will be the same as the average over the previous days. So you can use the average paid per day to calculate the rent based on you odds.

This off course assumes rationality. When you expect people to overbid in the future, it might be rational to overbid now.

---

**astanger** (2020-03-26):

I’m a little confused- could you clarify your answer with a numerical example?

---

**denett** (2020-03-26):

If over the time of the competition the average rate paid for the two tokens is 100 DAI per day, then on the last day everybody is willing to hold both tokens for a combined rate just under 100 DAI. When the sum of the rates are below 100 DAI, you can make a profit by holding both tokens. So we can expect that on the last day 100 DAI will be paid as well. Recursively this means that the average rate paid for the two bets will remain stable over time.

So when the average rate paid up till now is 100 DAI you can bid up to 60 DAI if you think the chances of your candiate are higher than 60%.

---

**astanger** (2020-03-27):

That makes complete sense! I do believe this is the answer to the post. I have rephrased what you said for my own understanding:

If you have no idea what the real odds are, it is always in your interest to rent both tokens if the combined price is less than the average of the combined prices to date- you are effectively buying a ‘complete set’ aka all the outcomes, for less than what others paid.

If you think the odds of token X winning are Y%, then it is always in your interest to rent token X if the price is less than Y * (average price of both tokens combined).

Thanks for your input!

---

**monteluna** (2020-04-02):

So it seems like a user should consider prices on a per day basis? This somewhat seems weird because of scaling issues. For example, if a user sets up a rental for $0.10 per day on a 10% likelihood bet, someone could come in to rent the token for $100 per day. Now this forces someone on the other side to bet up to $900 per day. Maybe someone could dig into this further because I think you’re on the right track with taking an inductive approach, but I don’t see how this doesn’t create an environment that escalates prices to insane levels. The only thing stopping this is the user has a finite amount of money.

[@astanger](/u/astanger) this is a terrible idea. When will this go live so I can play in this degenerate game?

---

**denett** (2020-04-02):

As I have shown, the average total rate paid is unlikely to decrease much, so I don’t think you need to adjust your rate downward when the likelihood does not change. The average total rate paid could off course rise when people are outbidding each other, but it will only increase slowly since it is an average over a longer period.

When in your example the average total rate paid has been $1 for 10 days, paying $100 for a day will only increase the average total rate paid to around $10. So the other side will only pay $9 for the 90% likelihood. When the average total rate paid remains $10 until the end, the winner will get $10 for holding the token for a day. The person that paid $100 will lose at least $90, so I don’t he/she will pay the $100 in the first place.

