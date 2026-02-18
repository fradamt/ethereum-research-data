---
source: ethresearch
topic_id: 3859
title: "[Question for game theory experts] Coalitions with and without a concentrated beneficiary"
author: vbuterin
date: "2018-10-19"
category: Economics
tags: [coalition, cooperative-game]
url: https://ethresear.ch/t/question-for-game-theory-experts-coalitions-with-and-without-a-concentrated-beneficiary/3859
views: 2429
likes: 11
posts_count: 15
---

# [Question for game theory experts] Coalitions with and without a concentrated beneficiary

Consider the following two scenarios:

- Aaron, Abraham … Zwingli (1000 people total) all have free time which they could use to help build a building for a local megacorp, CoordiCorp, which needs to be finished within one month. They value their free time at $1000 per month, the building takes 500 man-months to build, and provides CoordiCorp with $1 million of value.
- Aaron, Abraham … Zwingli (1000 people total) all have free time which they could use to help renovate a park. They value their free time at $1000 per month, the park takes 500 man-months to renovate, and provides each of the 1000 people with $1000 of value.

In both cases, a coalition of at least 500 people is required to achieve a positive result. However, in the first case, there is an easy solution to align incentives: CoordiCorp pays each of 500 people $1500 to work for a month, so each worker gets a net utility gain of $500, the company gains $1m value from the building at $750k cost, and everyone is happy. When such a solution is undesirable, we call it bribery, but here the possibility of “bribing” workers to work leads to a very good result. In the second case, however, there is not an easy solution, and the best argument I can think of for why is that in the second case **there is no concentrated beneficiary** that can make the side payments.

An “ideal dictator god” can clearly force everyone to work for 0.5 months (or, if months are indivisible, force 500 people to work for a full month and force the other 500 to pay them $500 each) and achieve an outcome better for everyone than the uncoordinated market, and a hypothetical charity CoordiOrg can pay 500 people $1500 to work for a month, but there’s no direct market incentive for such an organization to exist. Hence, there’s no easy way otherwise for the coalition to naturally emerge.

On the one hand, this is simply private goods vs public goods, and we all know that public goods are harder to incentivize. On the other hand, this thought experiment shows that **required coalition size by itself is not a sufficient measurement of difficulty of coordination**. A mechanism that is secure unless the 500 people coordinate in case A is not very secure, a mechanism that is secure unless the 500 people coordinate in case B is much more secure. There are rather two levels of “ability to coordinate”, the first level being the ability of a group of agents to coordinate by accepting side payments from a given agent, and the second level being the ability of a group of agents to coordinate by actually acting as one agent with a shared set of interests.

The scary thing about public goods incentivization techniques involving subsidies is that they sit on a knife edge of coordination assumptions: they are only needed if agents cannot cooperate in the second (more difficult) sense, but they can fall victim to manipulation if agents can cooperate even in the first (easier) sense, as if the first sense of coordination is possible a fake public goods provider could extract subsidies by bribing many people to pretend that they are a legitimate public goods provider.

Question for game theory experts: does this distinction between types of coordination have a formal name in the literature? Has it been studied? Are there existing results that are relevant to making mechanisms robust against adversaries that have stronger coordination abilities?

## Replies

**Planck** (2018-10-19):

Not sure if this is what you’re looking for, but here’s my take from IO game theory side of things:

You might be interested in the work on Team Production (the ritual citations are [Jensen & Meckling](https://www.sfu.ca/~wainwrig/Econ400/jensen-meckling.pdf) and [Alchian & Demsetz](https://www.nuff.ox.ac.uk/users/klemperer/IO_Files/production,%20information%20costs%20Alchian%20and%20Demsetz.pdf)). One of the foundational papers is [Holmstrom 82](https://www.kellogg.northwestern.edu/research/math/papers/471.pdf) which is a similar-ish setup. I think this perspective would tend to view the question in B as “why can’t there exist an organization that does a similar thing as in A”. As for mechanisms, there’s Holmstrom’s Budget Breaker…

Another entry point would be the Relational Contracts literature, beginning with [Fama](http://lib.cufe.edu.cn/upload_files/other/4_20140516100637_8%20Fama%20E.F.%EF%BC%881980%EF%BC%89Agency%20Problems%20and%20the%20Theory%20of%20the%20Firm.pdf) and more commonly associated with [Baker, Gibbons, and Murphy](http://web.mit.edu/rgibbons/www/RelConWP.pdf), which would highlight CoordiOrg’s limited existence as being a problem because it can’t access relational contracts.

Finally, while this seems not to be your view, imo it’s very useful to think of successful organizations as *transforming* PD games into coordination games (rather than being equilibrium selection mechanisms in existing coordination games.) Or, short of that, thinking of coordination costs in terms of “Risk Dominance” and off-equilibrium payoffs. It isn’t in the letter of Ostrom but I think it’s in her spirit.

One reason for this approach is that the pareto optimum is extremely salient in experiments on coordination games, so it’s hard to explain enormously profitable firms as just directing people toward something they naturally pick (even in enormous groups, even without communication, etc.) More specific to your example: absent some pretty unrealistic assumptions about utility and production functions, you’re almost certainly describing a PD game in example B’s park.

---

**georgios** (2018-10-20):

These two settings from a game theoretic perspective seem to be quite distinct.

The first one (in the presence of a coordinating center) seems more like a cooperative game. Indeed here the socially optimal outcome seems easy to enforce and there is a multiplicity of payoff vectors that can achieve that. Notions such as core would be of use here.

The second case, the one without the coordinating center is much more interesting and non-standard. To model this, you also need to add/introduce a dynamic/evolutionary model of coalition formation (along with a mechanism for splitting profits within the emerging coalitions). There is some work in this area. E.g.

http://people.sutd.edu.sg/~georgios/papers/wine2010full.pdf

However, as far as I know there are no “standard” models of dynamic coalition formation.

Given such a model of dynamic coalition one can try to analyze the properties of the stable coalition structures that can emerge and what are the social properties of the resulting game states. This is the goal of the paper linked above.

I am not familiar with any papers about making mechanisms robust against adversaries that have stronger coordination abilities. As you point out whether the resulting outcome is beneficial or not is observer dependent. So, most likely any game theoretic mechanism that aims to stop such bad outcomes will probably have to work at another higher level (e.g. a reputation mechanism).

---

**sleonardos** (2018-10-21):

Just to add a different perspective: external payments can (indeed) promote/enforce the stability of coalitions, thus confirming your intuition. AFAIK, such payments have been only studied as a stabilizing factor in the context in which the contributor is benevolent, see [The Cost of Stability for Coalitional Games](https://arxiv.org/abs/0907.4385) and the literature that it initiated. A paper that is similar in spirit, but which focuses on non-cooperative setting is [K-Implementation](https://arxiv.org/abs/1107.0022).

It seems that in your context, the contributor is malevolent (he wants to motivate the coalition to obtain long term profits for himself). This gives an interesting twist to the story, and AFAIK, this has not been explicitly studied (yet).

---

**phillip** (2018-10-24):

Not an expert, obviously enough I hope. For whatever it’s worth:

1. “Fundamental divergence” (Shavell 1997) is first in priority if not in time to mind.
2. Hart & Grossman (1986)'s “residual claimant” is salient when the issue of a “concentrated beneficiary” in the form of a public trust is involved. See also HSV (1997) at 1129, maybe; haven’t finished Halonen-Akatwijuka & Hart (2017) and can’t speak to applications to lemon partisanship & commitments in the market for endgame context / style.
3. I suppose there’s also the scholarship on “collusion;” see, e.g., IJRST (2003), citing which only gets me that much further from a helpful path into optimal supervision literatures.

edit: & yes, per [@Planck](/u/planck) supra, “common pool resources” *as a class of* managerial problems

---

**v-for-vasya** (2018-10-26):

Both of your examples can be looked through the prism of **cooperative games with transferable utility** (TU), in particular the concept of Shapley values.

**Q1**: While I don’t think there’s a formal name for your types of coordinations, there is actually **a quantitative way to express them with characteristic functions of coalitions in coordinated games with transferable utility** (*I’ll show below how using a simplified version of your example in Python*).

You can then calculate Shapley values for such games and compare them! If the Shapley value is inside the core, then you have a very stable coalition. If it’s not, then people will not be interested in forming such a coalition.

**Q2**: Robustness against adversaries with stronger coordination abilities would involve shrinking the core of a cooperative game to zero. There’s this conjecture called “Edgeworth’s conjecture” which basically states that as you increase the amount of agents in a game to infinity, you wind up shrinking the core of an economy to zero, meaning coordination becomes pointless.

As long as a core exists, there can exist a stable grand coalition which can be formed within it and the Shapley value can be in it. Here’s a quick intuitive read on Shapley values and cores ( page 9 and page 14 http://www.math.ucla.edu/~tom/Game_Theory/coal.pdf ).

After thinking for a couple of hours on this I don’t think there exists a core in both case A and case B, but there *does* exist a core within case A if there’s a subgame with 500 players + Coordicorp player.

If we look at case A, **there’s actually 1001 players with 1001st being your concentrated beneficiary, Coordicorp.**

**Case A:**

Player Coordicorp’s characteristic function `v(Corp)=0`, but is `v(Corp, any 500 players)=1,000,000`.

A - Z’s characteristic function is just `v(a-z)=1,000`

See github link for implementation below for Shapley values in case A game.

**Case B:**

Coordicorp is absent in case B which changes everything, especially when looking at it with Shapley values.

The Shapley values are equal to the characteristic function values `v(a-z)=1,000` so there’s no sense in forming any coalitions in case B.

Your example reminds me of the glove game, actually (https://en.wikipedia.org/wiki/Shapley_value#Glove_game). I’ve included an example of it in the code below which you can

play around with in Python.It also includes examples of your cases A & B where you can play around with the payoffs. I’ve simplified your game by grouping the 1000 players into bigger groups to make it easier to understand:


      [github.com](https://github.com/v-for-vasya/Gamepy/blob/7dcbfcfc9259719913896eda376e0ad65fc3d975/Shappy/Coordicorp.py)




####

```py
import math
import shap

"""
Shapley value calculation basic example from wikipedia with glove game - https://en.wikipedia.org/wiki/Shapley_value#Glove_game
"""

player_list = ['L1','L2','R'] #L1-left glove, L2-second left glove, R-right glove from wikipedia example
coalition_dictionary = {'L1' : 0, 'L2': 0, 'R': 0, 'L1,R': 1, 'L2,R': 1, 'L1,L2': 0, 'L1,L2,R': 1} #characteristic functions of each coalition's payoff
g = shap.Coop_Game(player_list, coalition_dictionary) #shapley calculation
print g.shapley() #one can interpret Shapley values quantitatively either as the power of each player, or as the amount of money each player fairly deserves
#in this case, if we are splitting a $1, then R is entitled to $0.66 and L1,L2 are entitled to $0.16 if they want to be a part of a grand coalition

"""
Shapley value calculations for case A, case B, subgame of case A with 500 people, subgame of case A with 500 people split up into 2, case A with 4 groups of 250 people
"""

print 'Case A - Big game - no core exists - grouped 1000 people into 500 people as players v1,v2 - non stable since Shapley values are below v1,2s characteristic functions'
```

  This file has been truncated. [show original](https://github.com/v-for-vasya/Gamepy/blob/7dcbfcfc9259719913896eda376e0ad65fc3d975/Shappy/Coordicorp.py)








I winded up simplifying your game to at max 5 players (250 groups of 4 + Coordicorp for case A) because analyzing a cooperative game of 1001 players is just a bit nuts. (calculation of Shapley values is factorial in nature math.fact(1001)!!!)

The great thing about Shapley values is that they will always give you a result which can be compared to other games with the same players whether a core exists or not!

For example, if player Aaron’s gain by himself is `v(a)=$1000`, but a Shapley value of `v'(a)=$1,001` is found for him in some other game with a Coordicorp or someone like that, then such a person may be subject to joining a coalition probably with Coordicorp as the instigator for this $1 gain.

---

**vbuterin** (2018-10-26):

Thanks a lot for this!

I’m not sure the coalitional game theory framework quite captures the problem though. For example, suppose that the rules of were changed: *any* number of people could work on improving the park, and each additional person’s month of work adds $2 of value to each person. We could even make it superlinear, and say that with N people working, the value-per-person of the park v = N * (1 + \frac{N}{500}). Now, the grand coalition (and any coalition, really) is stable, but in such a setting the public goods problem clearly still exists.

The problem is that in the coalition game theory setting, only the participants in the coalition get a payout, whereas here, each person’s work gives a payout to everyone regardless of whether or not they participate.

I suppose in the linear payoff setting (each worker contributes $2 of value to each of the 1000 people) you could decompose the game into 1000 games, where in game i player i is the dictator and decides whether or not the $2000 total payoff happens, in which case Shapley values suggest that all other players get a payout of zero; since the players’ “natural” payout is $2, that would mean *every* other player would have to agree to give $2 to the worker. Summing over these games, you get the result that it’s a stable coalition if every player agrees that if they do not work they must sacrifice $1998 to the other players, which then motivates every player to work.

This technically works, but it is *incredibly* fragile. If even one player actually doesn’t care about the park, or just wants to “watch the world burn” (cf. [the Lizardman constant](http://slatestarcodex.com/2013/04/12/noisy-poll-results-and-reptilian-muslim-climatologists-from-mars/)), then the entire mechanism breaks down and nobody works and the park does not get renovated at all.

---

**v-for-vasya** (2018-10-27):

Yes, it doesn’t 100% capture the dynamic, but it can still be expressed. I thought a bit more and realized that there should actually be 1000 subgames first (kind of what you’re alluding to in third paragraph). I’ll show in a link below of how this can be expressed in cooperative game theory. In short, with the presence of a dictator, some of the payoffs are reduced which “encourages” people to coordinate in the big game.

Your $1998 example is a good idea and you’re right that it’s fragile (*rationality of human beings is a big assumption in the first place*). The Lizardman read is very interesting (and funny). I actually have two economic solutions to this to prevent such kamikaze behavior.

On one end you have the disposition effect with prospect theory ([1](https://en.wikipedia.org/wiki/Disposition_effect)). If I have $100, taking away  $10 hurts me more than gaining $10. So punishing people is the right thing to do, **but** if you punish too hard ($1998) you encourage kamikaze behavior. The corollary there is the Ultimatum game ([2](https://web.stanford.edu/~jdlevin/Econ%20286/Experimental.pdf)) which deals with splitting $100 with player A determining how to split and the other player B choosing to accept or not. Rationally, any split ($99, $1) is fair to B, but if it’s too skewed away from $50/$50, the $50 becomes an anchor so people consider a deviation from $50 as a loss. If this loss is $20 or more, player B will, on average, reject even though it’s perfectly rational to accept $30.

Basically, punishing people relative to what their payoff is or what they *think* the are entitled to as a payoff ($50) should be a percentage, but that percentage should not be too high, which encourages irrational behavior.


      [github.com](https://github.com/v-for-vasya/Gamepy/blob/cbd75ef3eb919098205db51e2cdb4bebb9228901/Shappy/case_b)




####

```
1,000 different subgames with v(1)=Aaron ... v(1000)=Zwigli

Subgame with Aaron (v(1)) being the charitable park contributor:
  v(1)=1002 // Aaron contributes by himself
  v(2...n)=1000 // other players not interested in helping on park
  v(1,2 ... n-1) = 1000*n // all subcoalitions except for grand coalition
  v(1,2,...n) = 1002*1000  // grand coalition of all getting $2 from Aaron's work while everyone else was leeching off.

Subgame with Abraham (v(1)) being the charitable park contributor:
  v(2)=1002 // Abraham contributes by himself
  v(1,3...n)=1000 // other players not interested in helping on park
  v(1,3 ... n-1) = 1000*n // all subcoalitions except for grand coalition
  v(1,3,...n) = 1002*1000  // grand coalition of all getting $2 from Abraham's work while everyone else was leeching off.

Same thing for all 998 subgames. In each one of these games it appears to be a good idea for each individual person to contribute,
but once we put it all together:

Big game case B where all would like to contribute:
  v(1...n)=1002
  v(1,...,500)=v(1,...,501)=v(1,...,1000) // You only need 500 people to improve the park.
```

  This file has been truncated. [show original](https://github.com/v-for-vasya/Gamepy/blob/cbd75ef3eb919098205db51e2cdb4bebb9228901/Shappy/case_b)

---

**vbuterin** (2018-10-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/v-for-vasya/48/13320_2.png) v-for-vasya:

> Subgame with Aaron (v(1)) being the charitable park contributor:
>
>
>
> ```auto
> v(1)=1002 // Aaron contributes by himself
> v(2...n)=1000 // other players not interested in helping on park
> v(1,2 ... n-1) = 1000*n // all subcoalitions except for grand coalition
> v(1,2,...n) = 1002*1000 // grand coalition of all getting $2 from Aaron's work while everyone else was leeching off.
> ```

Not sure I understand this. Why 1002 * 1000? As I see it (in the linear version as that seems easiest to analyze):

- Aaron contributes: $0 to Aaron, $2 to each of other 999 participants, so $1998 total
- Aaron does not contribute: $1000 to Aaron, so $1000 total

We can turn this into a coalition game in a bunch of ways, all of which involve Aaron making his work in the park conditional on some property about how much money the other participants give him (eg. if all other 999 participants give him $1.5); then we have a game with a grand coalition with value 1998 and imputation (1498.5, 0.5, 0.5 … 0.5), a single-participant coalition with Aaron getting 1000, and every other coalition getting zero. Another example would be Aaron working if at least 750 people provide $1.5 each; then there are many 750-person coalitions that are stable in the game-theoretic sense, but extremely fragile in practice.

---

**oliverbeige** (2018-10-27):

Very interesting. IIRTC, this would be some modified stag hunt with freeriding: the hunting party would be successful if a given fraction of the population participates in the hunt, but the spoils would be shared among the whole population. I’m inclined to send you down the strategic interaction/stag hunt literature rabbit hole (Peyton Young, Larry Blume, Glen Ellison come to mind), but tbh I can’t think of a published paper that modifies a stag hunt that way. But then again, I’m not really up to date on that literature.

Is your intuition that this “concentrated beneficiary” could be automated (e.g. by assigning members to hunting parties so that everyone gets to take their turn) and then collectively governed? I guess this would come close to what I called a “rent-dispersing Aumann machine” before.

---

**v-for-vasya** (2018-10-27):

Sorry, let me clarify with Aaron. I should’ve subtracted 1000 from the payoffs for all of those values.

Wouldn’t Aaron’s actions result in him also getting $2 of value since he is also one of the players? This was the logic for 1002 x 1000 (supposed to be 2 x 1000). Aaron’s charitable desire to contribute to the park is expressed as the grand coalition in this subgame results in everybody getting $2 (including himself as well? If not, it’s $1998).

With your 750 player example, fragile in practice, yes. Another tool to tackle this is to make Aaron’s work conditional on certain goals being met, if not met, then Aaron is punished and some of the money is returned to the other players.

This is similar to the concept of options for founders in the VC startup world. A bunch of VCs giving their $1.5 to Aaron could result in Aaron behaving wildly so what VCs started to do was, instead of buying shares, they buy preferred shares (downside protection if park goals not met), and have the founder (Aaron) receive shares that vest over time (options).

---

**vbuterin** (2018-10-28):

By fragility, what I mean is that if the minimum is 750 people, and at some point in time exactly 750 people are expected to participate, then any one of the 750 could cause the coalition to fail. Now you could argue that if one person drops out, then another will join in, but then there’s no longer such a large incentive against dropping out…

---

**phillip** (2018-10-28):

[Hart & Holmström (1986)](https://dspace.mit.edu/bitstream/handle/1721.1/64265/theoryofcontract00hart.pdf%3Bjs) at around 26 may be adequately corelike; social dynamics at 15.

I don’t know if the Prize Lecture on “Pay for Performance” or whatever from 30 years later is back online. The PDF wasn’t.

**
tl;dr: rat race + 1980s Laffont & Tirole**

1. More and more inclined to think that, apart from expositions of optimality of linear contracting for agent-principal problems (Holmström, Milgrom, Hart, Mirrlees, etc.) & team production lit cited by @Planck supra,  this is basically where Laffont & Tirole’s mid/late 1980s shine, if it’s as much about behavior-oriented regulation of information “quality” as a constraint on pooling as the momentum of incentives assumed by characterizations of holders of residual “ownership” entitlements as rational / institutionally competent.
2. @oliverbeige, on “rent-dispersing Aumann machines”: curious about Carroll (2014) at 19-20 and why “sunspots” are “oracles” in your Medium post, particularly as this seems like a mixed question of firm boundaries and returns to contracting technology: essentially, the rat race (Akerlof) more than the stag hunt. But:
3. If the building needs to be done in a month (giving fixed δ₁ with CoordiCorp’s “patience” reflecting if not constituting labor market power), and the maintenance of the park is a game against nature (giving floating-rate δ₂ [, … δᵢ] “pegged to” the animal spirits of dynamically weighted regret [scheme / machine / tournament] ρ) then it’s “just” sticking dollarized utility values into a whiteboard folk theorem / Rubinstein model (Levin 2002 at 9) to make a qualitative Williamsonian description look like a mathy “core” problem.³ But not to fight the hypo; BGP (1994) at 235 characterize the participation consolidation game as the realization of "new value exit options."
–
On the flip side of Rubinstein’s “patience,” the term of art in Kandel & Lazear (1992) is “pain;” categorizing “effort” also sounds in the exploration / exploitation dichotomy in bandit problems, it sounds like, if this is a norm-discovering economic learning problem? This is getting into @mzargham herding territory, maybe. In any event the question seems begged as to the capability of a trust in the form of a foundation to sustain a public good (see Hansmann 1980; Verstein 2017), particularly if it’s just a transfer of limited liability risk premium from a community to a private firm.
4. A little off the path, but maybe tying things together in an oblique way for a certain kind of reader: I wonder if the Steps 1-3 in H,LPD,LdS,M (1997) correspond to Fudenberg & Maskin (1986)'s Phases I-III of determining “crazy” types (in which case this presents as an “internal capital markets” problem). In any event, if it’s about incomplete information and spreading risk (in this case, of which the only flavor is counterparty risk and the systemic effects of bundled transferability are assumed), that’s what derivatives markets are for, right?

---

e: what a way to arrive at Selten’s **“chain store paradox”** https://link.springer.com/article/10.1007%2FBF00131770

e2: there’s also [Romer (1990)](http://pages.stern.nyu.edu/~promer/Endogenous.pdf) at S94 rephrasing whether a planner’s licensing is working optimally and [Kaplow & Shavell (1994)](https://www.jstor.org/stable/724462).

³ / e3: This might be the *dumbest* comment but I anticipate spending plenty more time banging my head against footnote 20 in [Bebchuk & Guzman (1999)](https://scholarship.law.berkeley.edu/cgi/viewcontent.cgi?article=1980&context=facpubs) at 779, so spillover from the denoising and renoising process is possible. Romer *supra* has intuitive enough applications to R&D in recontextualizing local/global rate spreads to wheel-reinvention.

To close on an affectionately trollish note, however taken, in the form of a run-on: I gather that as my experience with posting here on “meta-innovation” of all topics was NIH ad absurdum, pressing the issue (or, if not about establishments vs. parks vs. special purpose vehicles in boundaries of **[semicommons](https://digitalcommons.law.yale.edu/cgi/viewcontent.cgi?article=4052&context=fss_papers)**, then about whether the question as to {ex ante | ex post | in medias res | continuous} updating might be usefully reframed here as part of an economic learning problem) is useless in settings where people are keen to say “mechanism design” for the sake of saying “mechanism design” and I’m clueless in the first instance.

---

**v-for-vasya** (2018-11-02):

I would say that if your 751 coalition (750 + Aaron because he is also a player) has a core and the Shapley value is in that core, it’s not as fragile as you may think. The reason for it is that the Shapley value also takes into account the ability of players to do damage to other players as well as to add value to other players.

Let me give you an interesting experiment in which I participated in class once with 3 players (let’s call them alice,bob,eve) dividing gains given the following values:

```
a=0
b=0
e=0
a,b=380
a,e=300
b,e=440
a,b,e=480
```

There exists a core with a Shapley value inside it. Observe how a appears to be the weakest player.

Shapley values (rounded off):

```
a=127
b=197
e=157
```

Nobody in class was introduced to Shapley values. (60 graduate students forming teams of 3(a,b,e) to play this game). At the end of this experiment  everybody formed the grand coalition and the amount of money they managed to negotiate for a was at max 100! **Nobody** went towards Shapley’s 127 for a because everybody was conditioned in thinking in terms of the question “**how does a add value**?”

b & e could just stay with each other at 440 and allow a to join for 40 in a,b,e for example because a can add 40 of value. b & e would be indifferent.

**Nobody was thinking of the question "how can a ruin things for us?"**

Here’s the kicker, a can utterly ruin the grand coalition and subcoalitions if it doesn’t get close to its Shapley value.

a can engage in a suicidal tactic by saying to either b or e “**I am going to get nothing, but before I do that I will give up all of my gains to either b or e, but not both**”

- if a gives everything to b, b gets 380 from a, but e gets 0!
- if a gives everything to e, e gets 300 from a, but b gets 0!
- b,e can only get 440 together if they ignore a, but a’s offers to both are very lucrative!
- a is not interested in giving all of his gains to both of them.
- This causes a quarrel between b and e where they now have to bribe a to stay as part of the grand coalition and they would keep bribing a until it approaches the Shapley value for a!

If your game has many players like a who think nefariously/want to watch the world burn, you have to bribe them all.

So in your 750+Aaron game, the Shapley value would be such that since any of the 750s can ruin it for everybody, Aaron would have to bribe all of the 750s. The 750’s Shapley values would be much

higher to ensure the grand coalition from breaking up.

I can’t tell what the Shapley value of a 751 player game is because computing it would take days and days. I just tried computing the Shapley value with 10 players and my old laptop still hasn’t given me an answer after 3 hours. Kind of why it’s nice to work with examples with much fewer players.

Hope this helps,

Vasily

---

**phillip** (2018-11-02):

[Jehiel & Lamy (2018)](https://philippe-jehiel.enpc.fr/wp-content/uploads/sites/2/2018/03/Tiebout.pdf) apply a **pivot mechanism** frame to the Tiebout sorting problem. If nothing else, it seems like a reasonably extensive bibliography of efficient competitive entry/search, as for on which information asymmetry and deception moral hazard, I have not read [LVW (2015)](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.649.3335&rep=rep1&type=pdf) in notes 25-26 (or “centralization” at note 18).¹

If reading through J&L as a list of modeling caveats doesn’t work (I just came across it browsing recent issues of the Journal of Political Economy), maybe going forward through Google Scholar on the citations to [McAfee (1993)](https://econpapers.repec.org/article/ecmemetrp/v_3a61_3ay_3a1993_3ai_3a6_3ap_3a1281-1312.htm) or [Athey & Segal (2004)](https://cowles.yale.edu/sites/default/files/files/conf/2008/sum_athey.pdf) would be a more satisfying exercise. YMMV.

As usual, discount me deeply.

---

**
¹**

I haven’t read the paper cited at 18 n. 42 in [Posner & Weyl (2013)](https://chicagounbound.uchicago.edu/law_and_economics/643/) either, if that’s a more germane point of entry.) I’d imagine, however, the context of voting implies assumptions of established process in a consensus n-period world (or “distributed state machine,” whatever) and treats as given at least rudimentary discretized reputation mechanisms (the sun rises in the morning, the clocks keep comparable time, and the infrastructure gets people to work for the deep-pocketed firm). So that’s chasing the tail back to the initial presentation as a fundamental divergence setup when agency costs are introduced.

