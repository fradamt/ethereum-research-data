---
source: ethresearch
topic_id: 4448
title: "Re-posting an old post: Metcalfe's law, externalities and ecosystem splits"
author: vbuterin
date: "2018-12-02"
category: Economics
tags: [externalities, metcalfes-law]
url: https://ethresear.ch/t/re-posting-an-old-post-metcalfes-law-externalities-and-ecosystem-splits/4448
views: 4616
likes: 13
posts_count: 21
---

# Re-posting an old post: Metcalfe's law, externalities and ecosystem splits

My post from 1.5 years ago: https://vitalik.ca/general/2017/07/27/metcalfe.html

General conclusion: if network effects are O(N^2) then many suboptimal forks exist and so forking should be to some extent actively discouraged; if network effects are O(N * log(N)) then externalities from moving from one fork to another fork are either zero or positive for moving to smaller forks and negative for moving to bigger forks, meaning that groups attempting to fork should either be left alone, or forking should be actively encouraged.

See also more recent work on a similar topic by Stephanie Hurder:

https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3192208

## Replies

**oliverbeige** (2018-12-04):

What makes a fork suboptimal?

---

**vbuterin** (2018-12-04):

If it happens despite being collectively welfare-reducing. On a micro level, if an individual jumps from a bigger chain to a smaller chain because he values the smaller chain enough, but discounts the negative externalities he is imposing on the other users of the bigger chain by reducing its network effect.

---

**oliverbeige** (2018-12-04):

But how do you measure “collective welfare”?

---

**vbuterin** (2018-12-05):

Essentially, the model here is that each uses makes a binary choice of whether they’re part of chain A or chain B, and derives utility from their use of what chain they’re on, which depends on some combination of their personal preferences and network effect. Collective welfare = sum of everyone’s utility.

---

**sachayves** (2018-12-05):

You might be interested in this recent paper by Nick Gogerty

https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3281845

Relevant insight:

“Metcalf’s law doesn’t hold for most currency. The network effect is linear at scale and not exponential per node. This is assumed to be a function of the limited need for transaction nodes vs. the actual field of potential transactional nodes using a protocol.”

---

**vbuterin** (2018-12-06):

That’s definitely one more piece of evidence for O(n * log(n)) being a better approximation of network effects than O(n^2).

---

**oliverbeige** (2018-12-06):

> which depends on some combination of their personal preferences and network effect. Collective welfare = sum of everyone’s utility.

I remember discussing the article with you when you first posted it (indeed iirc, it was the impetus for me to create the ecoinomia cryptotwitter account, so I should thank you belatedly for kicking it off), and back then we discussed local vs global effects, so let me focus on this aspect of the model.

Back when I wrote my dissertation, I briefly used the term “endogenous preferences” to describe this “some combination of personal preferences and network effect”, defining endogenous preferences informally as “If you go to a movie theater, your ultimate choice of which movie to see depends in part on whether you go by yourself, with your buddies, your spouse, or your parents.”

This terminology was voted down very quickly (for spurious reasons), so I stopped using it. But it has another,  very serious flaw: It doesn’t reflect endogenous *preference*, it reflects endogenous *choice*.

And the big problem economics has with network effects that I had to contend with is that under non-trivial demand-side interaction effects the all-encompassing *Axiom of Revealed Preference* breaks down. You can no longer impute from an observed choice (a fraction of) the underlying preference ordering: How can an outsider tell from watching you go to a movie with your parents whether you picked your preferred movie, or whether you just tagged along with your parents to make them happy? There is an underlying, typically unobservable and often tacit, negotiation process between involved parties to come to a (pooling or separating) equilibrium choice.

It’s an understandable modeling simplification to treat preference and (what I ended up calling) influence factors as similar, to be able to simply add them up into a personal utility function. I did exactly that. But its problematic to extract welfare implication from just aggregating those individual utility functions. (And yes, it’s still widely done in economics). Because doing so means you reinstate the Axiom of Revealed Preference in a situation where it doesn’t work.

For me the intellectual breakthrough came when I read North & Thomas’s *Rise of the Western World*, especially the footnote on page 1 (I tweeted about it before). I was trying to figure out how to explain that in a setup of *personal choice function = personal preferences + (factor) * network effects*, with factor = 0 means welfare is purely driven by preference considerations, and factor = 1 means preference and influence hold equal weight, my interacting group would maximize a global function where this factor was ½ (leading to suboptimal convergence).

The answer came in North & Thomas’s footnote explaining the distinction between “private returns” and “social returns”. The difference is that social returns aggregate influence factors twice, “to me” and “from me”, while private returns aggregate them only once: “to me”. In the absence of active altruism, even a community bent on coordinating their actions might fail to do so, and some circumstances even fail suboptimally. In the case of symmetric influences, this leads to a factor ½ for the “relevance” of network effects in welfare economics.

---

**burrrata** (2019-01-23):

Seems cool, but I’m not sure if I “get it”. Could you illustrate this with a picture/chart?

---

**oliverbeige** (2019-01-31):

Is that a question for [@vbuterin](/u/vbuterin) or me?

---

**burrrata** (2019-01-31):

[@oliverbeige](/u/oliverbeige) you. Generally pictures/illustrations/charts really help so I thought I’d ask if it’s possible. Specifically I’d like to better understand this part:

![](https://ethresear.ch/user_avatar/ethresear.ch/oliverbeige/48/1116_2.png) oliverbeige:

> For me the intellectual breakthrough came when I read North & Thomas’s Rise of the Western World , especially the footnote on page 1 (I tweeted about it before). I was trying to figure out how to explain that in a setup of personal choice function = personal preferences + (factor) * network effects , with factor = 0 means welfare is purely driven by preference considerations, and factor = 1 means preference and influence hold equal weight, my interacting group would maximize a global function where this factor was ½ (leading to suboptimal convergence).
>
>
> The answer came in North & Thomas’s footnote explaining the distinction between “private returns” and “social returns”. The difference is that social returns aggregate influence factors twice, “to me” and “from me”, while private returns aggregate them only once: “to me”. In the absence of active altruism, even a community bent on coordinating their actions might fail to do so, and some circumstances even fail suboptimally. In the case of symmetric influences, this leads to a factor ½ for the “relevance” of network effects in welfare economics.

---

**oliverbeige** (2019-01-31):

Oh ok. The “North-Thomas footnote” is [here](https://twitter.com/oliverbeige/status/1042017609074585600).

[![image](https://ethresear.ch/uploads/default/optimized/2X/d/d9544d54e0982e82b55ef77a20b5d53a64313771_2_690x231.jpeg)image1200×403 232 KB](https://ethresear.ch/uploads/default/d9544d54e0982e82b55ef77a20b5d53a64313771)

In my paper, the “private rate of return” is the choice function if everyone takes into account the effect of everyone else’s action on them, but not the effect of their action on others. The “social rate of return” is the choice function where everyone takes both effects into account. The “isolated return” would be if everyone ignored each other completely. This is the standard model in textbook economics.

---

**oliverbeige** (2019-01-31):

Here is a simple scenario expressed as a “game graph” (which is simply a stochastic automaton).

[![image](https://ethresear.ch/uploads/default/optimized/2X/7/7644e1233790603f1085528a277b44a7167bd99d_2_690x482.png)image1145×800 55.3 KB](https://ethresear.ch/uploads/default/7644e1233790603f1085528a277b44a7167bd99d)

There are three players, each with choices si = {–1, +1}, or simply “–” and “+”. The game could start anywhere, and at each node one player gets chosen randomly to update their choice based on their current utility, say u1 = b1 s1 + w12 s1 s2 + w13 s1 s3 = 3 s1 + 4 s1 s2 + 2 s1 s3 in this example. This simply translates into u1 = ± 3 ± 4 ± 2 depending on whether player 1 picks “+” or “–”, and whether players 2 and 3 pick the same (+) or the opposite (–) choice as player 1.

Each chosen player either sticks with their current choice, or flips to the other choice, whichever maximizes current utility. Flipping means moving to a new node.

There are a couple of things that are important here. The game could converge to the (–, –, –) corner, which is suboptimal even in *H* (“private returns”). So in this setup the players could end up in a local maximum. This can be resolved by adding random mutation, aka “erratic behavior”.

The other thing is that the state which maximizes social returns W is not an equilibrium, so under the typical game theoretic assumptions the player can never stay in the (+, +, +) corner which would create the highest amount of welfare, because player 3 would prefer to switch from “+” to “–”.

The functions for social returns and private returns are here. They differ simply by the factor ½ which reflects the scenario of “I care about the effect of your actions on me, but not about the effect of my actions on you.”

[![image](https://ethresear.ch/uploads/default/optimized/2X/7/7568b57271cd72ed6ed343a843ef285c819e56f9_2_690x304.png)image1169×516 50.1 KB](https://ethresear.ch/uploads/default/7568b57271cd72ed6ed343a843ef285c819e56f9)

The solution to such a scenario, if detected, would be for 1 and 2 to offer 3 a side payment.

Does this help? I’ve written a primer about it [here](https://medium.com/@trialsanderrors/microstructure-and-macrocoordination-revisited-b848252bfd13).

---

**burrrata** (2019-02-01):

This does help. Thank you ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/oliverbeige/48/1116_2.png) oliverbeige:

> In my paper, the “private rate of return” is the choice function if everyone takes into account the effect of everyone else’s action on them, but not the effect of their action on others. The “social rate of return” is the choice function where everyone takes both effects into account. The “isolated return” would be if everyone ignored each other completely.

Does your model take into account the effects of [bounded rationality](https://en.wikipedia.org/wiki/Bounded_rationality)?

Also, cool chart. TBH I care much more now that it’s a game of figuring out what the chart means vs parsing through a bunch of text lol

Anyways, isn’t this all dependent on context? For example the tragedy of the commons is much more likely for very large networks and resources, but can be managed quite reasonably at a local scale. Also the game changes considerably if reputations are established and players value that more than any immediate payoff which leads to reciprocal altruism. From the blog post it sounded like you were exploring coordination with people, but then also automated distributed systems, and those are very different contexts… which leaves me confused still. I think that now I have a better understanding of what you’re trying to model, but I don’t understand the context in which it’s being explored?

---

**oliverbeige** (2019-02-01):

Bounded rationality is a tricky concept, but to a certain extent it applies. Standard resolution concept in game theory is backwards induction, which you could technically apply to this mutation-less model, but in most scenarios players would just block solution paths they don’t favor and the game would get stuck very quickly in a low-utility state.

The main model, where I introduce mutation/erratic behavior to help the players get out of local optima (if you know simulated annealing, this is a distributed implementation of it), I follow the strategic interaction literature started by [Kandori, Mailath and Rob](https://www.jstor.org/stable/2951777?seq=1#page_scan_tab_contents), which is anchored in evolutionary game theory and which applies both mutation and learning. There’s a good deal of evidence in nature that organisms resort to randomness in order to move out of critical situations.

---

**oliverbeige** (2019-02-01):

You could conceptualize it as follows. In every decision situation, a player asks herself three questions:

1. “What is the best thing I could do under the current choices of all my peers?”
2. “How likely is the current state to stick as the final state?”
3. “How important is it for me to take ‘erratic’ action in order to not get stuck in a suboptimal state?”

This is of course very far away from economic reasoning, but it’s actually quite close to how the brain really works through crisis situations. This is not a coincidence.

---

**oliverbeige** (2019-02-01):

Regarding context, modern game theory is of course about stripping away the context to look at the underlying mechanism, to see if the mechanism might reoccur (with variations) in very different contexts. I’d say the least common context where we see the prisoners dilemma is when it involves two prisoners and an interrogator. I just posted something about PD being the underlying mechanism in the works of Oliver Williamson and Oliver Hart. And they weren’t writing about prison reform, but about corporate governance and the theory of the firm.

---

**burrrata** (2019-02-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/oliverbeige/48/1116_2.png) oliverbeige:

> You could conceptualize it as follows. In every decision situation, a player asks herself three questions:
>
>
> “What is the best thing I could do under the current choices of all my peers?”
> “How likely is the current state to stick as the final state?”
> “How important is it for me to take ‘erratic’ action in order to not get stuck in a suboptimal state?”
>
>
> This is of course very far away from economic reasoning, but it’s actually quite close to how the brain really works through crisis situations. This is not a coincidence.

Having been a human for quite a few years now I’ve never asked myself “How important is it for me to take ‘erratic’ action in order to not get stuck in a suboptimal state?”. Furthermore, 95%-99% of the time I WISH I was thinking “What is the best thing I could do under the current choices of all my peers?”, but actually what I’m thinking is “Me want!”, “Shiny!”, or “Fear!”.

And while the prisoner’s dilemma isn’t a thing most people have to deal with, blockchain forks and decisions on what blockchain network to build on or contribute to is a huge thing for developers. In that case it becomes very important to understand incentives as well as how those might be influenced by signalling and group dynamics. Being able to align the “social returns” with the “isolated returns” creates a system where the individual taking the most selfish/rational action actually benefits the network as a whole, as we’ve seen with mechanisms like PoW, PoS, and other cryptoeconomic games. Is that kind of what you’re trying to explore and model with your research: better ways to model and reason about that?

---

**oliverbeige** (2019-02-03):

Indeed. I don’t think I mentioned this here yet but I posted it on Twitter before: the game theoretic model is an adaptation of Geoffrey Hinton’s and Terrence Sejnowski’s Boltzmann machine, an artificial neural network that is a remarkably close model of how the brain solves combinatorial optimization problems. So while we might not ask ourselves these questions consciously very often, our brain asks them all the time. And it also adds mutations in times of crisis.

Game theory and machine learning have a common ancestor in the paper by Ernst Zermelo from 1913 on chess as a decision problem, but that common ancestry has mostly been forgotten. I brought those two things back together.

There’s a few reasons why I built this particular model.

For one, the prisoners dilemma has been widely used to explain certain facets of collective action: Robert Axelrod’s work on cooperation is the best known. Coordination games like battle of the sexes,  matching pennies, and tragedy of the commons had not gotten the same amount of attention. Now, partly because of the emergence of blockchains and the need to model consensus convergence, they finally do.

By the time I started writing the paper (in 1996), and even today, the “network” in “network externalities” has no structure by definition. It is simply a synonym for “group size”. I looked at how the structure of the network influences outcomes. That was before and partially in parallel to the work by Duncan Watts on “social networks”.

As you indicated, the economic model of the “rational actor” is fundamentally flawed. We don’t typically “decide” to act erratically, but two very well known forms of “erratic” or “irrational” behavior are artistic expression and entrepreneurship. I tried to both find a way to formalize actual human behavior and collective action rather than depend and further a known flawed model, and to explain why we see these kinds of behaviors and why evolution deemed it necessary to preserve them. Creativity is inefficient, but creativity is necessary to human survival.

Finally, the “rational actor” model also assumes complete or perfect information about the decision options, which is also a very flawed assumption. There is a fundamental axiom in economic choice theory called the “axiom of revealed preference” which states that by observing the choices of human actors we can divine their preferences. I tried to show how easily this axiom breaks down if we inject even a tiny amount externalities or “influence”.

---

**oliverbeige** (2019-02-03):

The question if selfish actions create socially optimal outcomes is a very old one. The simplest answer is “in the absence of externalities, asynchronicities, lock-ins, and information asymmetries, they do.”

My point of creating these three collective objective functions was to show how selfish action under externalities actually relates to social outcomes. It turns out that under certain circumstances selfishness can create optimal outcomes, but we can also pinpoint the situations where it doesn’t.

(Keep in mind that coordination games are games where everyone is interested in finding the best outcome for all, which sets them apart from competitive games.)

---

**JoshEick** (2024-05-28):

In a recent paper, `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4839567`, we study the proposed standard models aligned with Metcalfe’s Law, identifying the most effective approach and further augmenting it for the Ethereum Network.

The results indicate the proposed model appears to capture demand and network effects more effectively for the Ethereum Network, as shown in equation (12),  dt = CeλN̅m.

Consequently, we adjusted for the circulating supply, considering network upgrades. In the discussion, we explore an extension with the objective of addressing the criticisms of Metcalfe’s Law by evaluating network quality.

Any feedback is more than welcome.

