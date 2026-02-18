---
source: ethresearch
topic_id: 5553
title: "Pairwise coordination subsidies: a new quadratic funding design"
author: vbuterin
date: "2019-06-04"
category: Economics
tags: [quadratic-funding]
url: https://ethresear.ch/t/pairwise-coordination-subsidies-a-new-quadratic-funding-design/5553
views: 28201
likes: 44
posts_count: 29
---

# Pairwise coordination subsidies: a new quadratic funding design

One of the challenges of the CLR subsidy formula (if a set of agents i \in [1..n] each make contributions c_{i \rightarrow p} to a project p then the project p gets a subsidy of k * [(\sum_{i=1}^n \sqrt{c_{i \rightarrow p}})^2 - \sum_{i=1}^n c_{i \rightarrow p}] where k is the CLR subsidy coefficient) is that it assumes that agents are fully uncoordinated, and there are no bounds on how much money can be illicitly extracted from a CLR if even two agents are capable of coordinating: for any subsidy coefficient k, if two agents each put in a large amount of money M into a fake “project” that splits the funds between them, then they get a subsidy of k * [(2\sqrt{M})^2 - 2M] = 2cM. If k is set to target a fixed subsidy amount, then as M \rightarrow \infty the two agents would extract almost the entire subsidy and leave all other contributors with near-zero.

We can make the CLR design more robust to the possibility of coordination between agents as follows. First, let’s philosophically reinterpret the existing CLR formula somewhat.

[![Untitled%20Diagram](https://ethresear.ch/uploads/default/original/2X/f/f4c8832d958643c849de60b387634a2584db8b70.png)Untitled%20Diagram651×471 7.65 KB](https://ethresear.ch/uploads/default/f4c8832d958643c849de60b387634a2584db8b70)

The green squares are the c_{i \rightarrow p} values, the *sides* of the squares are \sqrt{c_{i \rightarrow p}} values, the total green area is the original total contribution, and the yellow area is the subsidy if k=1 (the total size of the square is (\sum_{i=1}^n \sqrt{c_{i \rightarrow p}})^2, and the green area is \sum_{i=1}^n c_{i \rightarrow p}, so the yellow area is (\sum_{i=1}^n \sqrt{c_{i \rightarrow p}})^2 - \sum_{i=1}^n c_{i \rightarrow p}). But notice that we can reinterpret the area as being the sum of the sizes of rectangles, where each rectangle is of size \sqrt{c_{i \rightarrow p}} * \sqrt{c_{j \rightarrow p}} for all ordered pairs i \ne j (note that the (i,j) and (j,i) cases are identical so we can think of it as a subsidy of 2\sqrt{c_{i \rightarrow p}}\sqrt{c_{j \rightarrow p}} per *unordered* pair).

We can think of this as a *pairwise coordination subsidy*: for each pair of agents (i, j), if agent i contributed to a project that agent j also contributed to, then that means that agent i contributed to something that benefits agent j, and so agent i should be rewarded for this good deed. In the CLR formula, the subsidy given to each pair is k_{i,j} * 2\sqrt{c_{i \rightarrow p}}\sqrt{c_{j \rightarrow p}}, where k_{i,j} can be viewed as a “discoordination coefficient” for that pair: if k_{i,j}=1 then the pair is fully uncoordinated, if k_{i,j}=0 then the pair is fully coordinated and so the optimal subsidy is zero as the pair is itself fully capable of internalizing gains from coordination, but we could also have some 0 < k_{i,j} < 1.

**The new idea here is that instead of a single global k value, we have a local k_{i,j} value for each pair of agents, and we make an assumption that the amount of funds a specific pair of agents put toward the same projects is itself evidence of how coordinated they are, and so the more total funds a pair of agents put toward the same projects, the lower we set the k_{i,j} value for that pair.**

Let us try a coefficient k_{i,j} = \frac{M}{M + \sum_p \sqrt{c_{i \rightarrow p}}\sqrt{c_{j \rightarrow p}}}, where M is a tweakable parameter. That is, k_{i,j} = \frac{M}{M + T} where T is a measure of the total extent to which participants i and j both contribute to the same projects (the sum \sum_p is summing over all projects). So the more that any two agents i and j are seen to coordinate *in general*, the lower a subsidy coefficient k_{i,j} we give to that particular pair.

Now, let’s suppose that k coordinated agents all contribute a very large amount of money W (think W \rightarrow \infty) toward a project. There are \frac{k * (k-1)}{2} pairs, and in each pair the coefficient k_{i,j} is \frac{M}{M + W}, so the subsidy that they can extract is k_{i,j} * 2\sqrt{W}\sqrt{W} = \frac{2MW}{M + W} < 2M.

**Hence, the new scheme offers a clear bound (k * (k-1) * M) on the amount that the system loses to unexpected coordination between k agents** (which could come completely illegitimately, eg. fake accounts, or more benignly, as in two people from the same family caring about each other). The emphasis of the CLR switches from assuming total non-coordination between individuals to being more robust against there being some level of existing coordination between individuals, and focusing on subsidizing coordination between individuals who would not normally coordinate.

If one wishes to set up subsidies to target a particular level of total expenditure (ie. target \sum_{p \in projects} \sum_{i=1}^N \sum_{j=1}^{i-1} f(c_{i \rightarrow p},c_{j \rightarrow p}) = T), one can adjust the value of M to do so. If M = 0 then T = 0, if M \rightarrow \infty then T will almost always be too high, so one can binary-search M to lead to the desired total T.

Another possible future direction is distinct M values for each agent pair, where M_{i,j} = M_i * M_j, where each M_i is set based on a measurement of how certain we are that some given agent actually is a unique individual (ie. accounts that pass lower levels of verification would see lower M_i values).

## Replies

**Hackdom** (2019-06-04):

Interesting, just saw the tweet and indulged myself. So I assume no anonymous contributions and all contributions have to be made from within a closed pool of identifiable agents.

---

**vbuterin** (2019-06-04):

Unfortunately all of these quadratic markets have to be identity-based in some form… see https://vitalik.ca/general/2019/04/03/collusion.html

---

**RhysLindmark** (2019-06-04):

This is likely out of scope (the rectangles are more interesting), but I want to add a “direct” coefficient for the (non-pairwise) green squares as well. As you state, the subsidy is a combination of *both* the pairwise matches (yellow rectangles) and a “direct” match (green squares).

Right now the non-pairwise subsidy is set at c_{i→p}. Add a coefficient! (A “bad money” coefficient? i.e. Don’t match *that* person’s money.)

Unrelated: +1 using the “diagonal” green square visualization instead of “stacking” the green squares. It makes the pairwise tweak much clearer.

---

**vbuterin** (2019-06-04):

The green squares are not a subsidy, the green squares are the original contributions. I don’t think there’s value in trying to take away a contributor’s green square; if you do that and take away more than you give via non-diagonal rectangle subsidies, then it’s a net *tax* on contributions, so the contributors would just make their contributions outside the system.

---

**Pepo** (2019-06-04):

Maybe this can be applied to vote weight. The more correlated are the votes of any two pair of individuals over a sequence of past polls, the less their influence is on the current poll.

If you frame voting as a problem of information extraction, information is maximized as the more unpredictable each vote is.

---

**Hackdom** (2019-06-04):

Seems to be a “there” there intuitively.

---

**Gerstep** (2019-06-04):

what happens if there’s a large group of uncorrelated individuals with similar goals? For example, they care very much about climate change and always vote for all proposals regarding this issue. Over time their coordination coefficient grows and their votes becomes meaningless. This solves coordination problem but discriminates against active like-minded groups of users.

---

**Pepo** (2019-06-04):

Having 1 single person or 1 million people saying that *something* should be done about climate change is indeferent when it comes to the problem of *what* should be done.

The key point is whether you are using voters as pain sensors or as decision makers.

---

**Gerstep** (2019-06-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/pepo/48/3448_2.png) Pepo:

> Having 1 single person or 1 million people saying that something should be done about climate change is indeferent when it comes to the problem of what should be done.

Let’s say mechanism described by Vitalik is used to allocate funds in charity DAO and there’s a group of people who vote for (contribute to) *all* proposals regarding environmental issues.  This clearly indicates interest but over time their coordination coefficient k make it so those proposal don’t get subsidized (k = 0). How can an application prevent this from happening?

---

**vbuterin** (2019-06-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/gerstep/48/3582_2.png) Gerstep:

> what happens if there’s a large group of uncorrelated individuals with similar goals? For example, they care very much about climate change and always vote for all proposals regarding this issue. Over time their coordination coefficient grows and their votes becomes meaningless. This solves coordination problem but discriminates against active like-minded groups of users.

First of all, there is no “over time”; in the proposal the formula is a evaluated separately for each time period, so there isn’t any problem for anyone that gets progressively worse in any way.

But in any case, I’d agree there are cases where there is a genuine disadvantage of the scheme; more precisely, it discriminates against genuinely strong preferences more than CLR does. Note that there is no extra loss from a set of people all contributing $1 to ten separate climate-related projects versus contributing $10 to the same one; in either case, the total subsidies work out to be the same size.

I would argue though that in many cases this property of penalizing correlation within groups can be a good thing: it penalizes tribalism (or rather, is doesn’t subsidize tribalism as much as it subsidizes cross-tribe bridge building). Close-knit groups often already have some mechanisms for coordination (social pressure, if we’re talking about local or national groups then taxes, etc), so they “need the CLR less”. Looking at things from this view, the climate-related projects would *benefit* from this scheme because they attract constituencies from very different backgrounds, even those that normally agree on little.

---

**Xrosp** (2019-06-05):

If I am correct this falls short of penalising an actor that can influence multiple groups for and/or against a cause, to leverage a desired outcome

For instance, a coordinated attack against any system happens at multiple layers and is phased, there is no consideration for wave differential intervals of forces acting for or against.

The system SHOULD include designs to identify individual or agent pair along with, force F by M or W contribution, to determine the weight function along as well as a wave equation for both propagation and disturbances to allow for a recalculation to spot and and adjust to coordinated discoordination coefficients and such branches.

No different than identifying, a manipulation of a climate agenda (good or bad) designed to harness a particular outcome and actions. Would make more sense to include a metric measuring the force, etal.

---

**vbuterin** (2019-06-05):

What do you mean by “influence” here? Putting out propaganda on social media to influence people’s level of support for certain projects? Trying to understand better what you’re trying to mitigate.

---

**Xrosp** (2019-06-05):

“Influence” i.e “effect”.

---

**Xrosp** (2019-06-06):

For example I want a solution to distribute, fair value, amongst users, (gamers & customers); retailer(s) and game (publisher, dev or company if indie).

If game reward is an item from the retailer and suitable for the user, how many retailers can thrive in an environment where more money can effect (influence) which game publishers and retailers can develop partnerships, this squeezes the little guys (publishers and retailers with less money) to earn less and receive less transactional value from a platform, I would like to build.

It’s also the problem across many markets where advertising dollars are the “force” that pulls or pushes a product the “distance” . This directly has an influence on work done.

How can it be made fair if the effect and force aren’t calculated? It requires either a differential or partial differential solution of force and effect on work done.

Also, consider the role of the system or platform here, it also needs to be fairly scrutinized.

---

**kdenhartog** (2019-06-07):

I don’t believe the “anonymous” part is a necessary requirement. The identity system that is  valuable to this design is one where a series of actions to any particular agent is traceable and the interactions between other agents within the system is also traceable. However, traceability outside the system is not necessary. More practically speaking what this means is that a contributor to a project can create a new pseudonymous identity for a new project that can remain mutually exclusive from their contributions to another project. The merits of the pseudonymous identity would then be directly proportional to contributions made to that single project only.

There’s some work being done on this idea for the [did:git method](https://github.com/dhuseby/did-git-spec/blob/c247ad0f0726859a43a3021e58cdd79e17d37f1e/did-git-spec.md#in-band-identity-management). The nice aspects of this thinking is that it allows a contributor to maintain an identity separate from other contexts or other projects, but doesn’t disallow a contributors from carrying an identity if they choose.

---

**kronosapiens** (2019-06-10):

To phrase this differently (as I understand it), the mechanism described here limits the ability for two (or more) agents to *trivially* coordinate to extract value from the system (at the cost of inadvertently penalizing tribes). It doesn’t make the system coordination-proof, however: if I and a co-conspirator wish to extract value from the system, then we should *separately* run influence campaigns to encourage innocent third-parties to support ~fake projects of our choosing. By ensuring that we never contribute to the same project, we avoid the pairwise penalty; instead, the bulk of the contributions come from third-parties with whom we are not normally associated, meaning those projects still receive large subsidies.

In essence though this is no different from existing “pump and dump” schemes and so maybe isn’t such a big criticism (IMO one shouldn’t critique a mechanism for perpetuating existing problems, assuming it solves at least some others). The mechanism proposed makes *trivial* extraction (modulo an identity system) more difficult, and that seems like A Reasonably Good Thing.

---

**vbuterin** (2019-06-10):

> (at the cost of inadvertently penalizing tribes)

I’d argue that penalizing tribes is a benefit, not a cost. The reason why is that it’s not penalizing tribes; tribes can still extract quite a lot of subsidies from the scheme for their projects, they just get subsidized *less* than if they were fully independent actors. This makes sense, because tribes already have internal mechanisms for cooperating, so they need the mechanism’s help less; there are fewer unsatisfied opportunities for very-high-value public goods within tribes than there are between tribes.

> if I and a co-conspirator wish to extract value from the system, then we should separately run influence campaigns to encourage innocent third-parties to support ~fake projects of our choosing

Agree that there is this risk. But is this risk solvable in *any* public goods producing mechanism? It seems fundamentally impossible to distinguish between a project which is a genuine public good that benefits N people that signal the fact that they would benefit, and a fake public good that has tricked N people into believing that it’s good for them.

The one technique I can think of for mitigating this further is adding a time-based component: when you contribute $x then in N years you get refunded a percentage based on what percentage of people at that time think that the project *was* a good idea. I think ideas like that involving mixing together quadratic funding/voting for preference aggregations and some form of prediction markets for eliciting predictive information and rewarding competence could be really interesting.

---

**kronosapiens** (2019-06-10):

Sure, I can grok how inter-tribe coordination is easier and so incentivization should be reserved for inter-tribe coordination which is harder but arguably more valuable. If you wanted to you could probably model this with some type of gaussian mixed-membership model where everyone is part of many tribes and the subsidy k is a function of the hidden tribal memberships, which you observe via voting patterns. Computationally it would be more efficient to calculate k as a product of the tribal membership vectors and some weight matrix than to iterate over all pair-project triples but that is a conversation for another day.

I also agree that the problem of extra-model coordination is profoundly hard (much like identity, which IMO can only be asymptotically solved, i.e. never perfectly but increasingly well), which is why I said that we shouldn’t fault mechanisms for perpetuating existing problems, provided they solve at least one existing problem without re-introducing problems we’ve previously solved.

Regarding the time component, I strongly agree. Inasmuch as the world is fundamentally a process and yet all of our models of the world are static (to even model time, we must fix it with a symbol like t), the inclusion of actual time IMO imbues models with an essential dynamism. Along these lines, I think concepts like conviction voting will lead to invaluable tools for (cheaply) incorporating valuable (and hard to manipulate) information into models. I riffed a bit on this theme a few years back: http://kronosapiens.github.io/blog/2017/09/14/time-and-authority.html

---

**theRealBitcoinClub** (2019-11-01):

**For all these which are scared by mathematical formulas, this article shows this theory in practice! Must read all to the conclusion!** https://vitalik.ca/general/2019/10/24/gitcoin.html

---

**Sky** (2020-06-26):

Enjoyed reading all this other than the formulas.

My friend would say “Urbit fixes this”, but I would say “Diversification fixes this”:

Could the holy grail be achieved with diversification?

Example… all in one round together:

20% traditional CLR matching (whales can’t run the show)

20% pairwise-bounded quadratic matching (teams can’t team up)

20% CLR matching with Negative votes (shorts allow a free market)

10% single matching (good ol’days)

10% 3x matching (encourages donations larger than 1 Dai)

10% Randomized matching (Introduces lottery element - play lotto for your cause!)

10% Sample-vote matching (David Chaum knows what he’s talking about)

**Benefits:**

- Hard to game; a gamer might go in circles
- With the right optimization may not need identity???
- Diversification often makes things better - the game-able characteristics of certain strategies would be highly reduced by the other strategies.

DeDivGiv = Decentralized Diversified Giving

Cheers


*(8 more replies not shown)*
