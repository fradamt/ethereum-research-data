---
source: ethresearch
topic_id: 2462
title: Mathematical Building blocks for convergence and stability of equilibria
author: mzargham
date: "2018-07-06"
category: Economics
tags: []
url: https://ethresear.ch/t/mathematical-building-blocks-for-convergence-and-stability-of-equilibria/2462
views: 1899
likes: 6
posts_count: 13
---

# Mathematical Building blocks for convergence and stability of equilibria

I produced an academic paper with researcher at the Warren Center for Network and Data Science at the University of Pennsylvania, for presentation at the International Conference on Complex Systems. This work constructs a formal model of the evolution of the economic network composed of addresses in a blockchain network as a dynamical system. Dynamical systems formulations in turn provide equipment for the treatment of global system properties despite the characterization of all action spaces as local to individual agents.

The work presented is the beginning of an effort to cross apply 15 years of work on decentralized optimization and coordination to a blockchain economics context. Key topics that are opened up from this framework include the relationship between iterative behaviors and/or repeated games characterized as dynamical systems, formal theories of economic invariants, and provability of convergence, uniqueness and stability of equilibria in potential games.


      ![image](https://static.arxiv.org/static/browse/0.2.7/images/icons/favicon.ico)
      [arXiv.org](https://arxiv.org/abs/1807.00955)


    ![image]()

###

Decentralized Ledger Technology, popularized by the Bitcoin network, aims to
keep track of a ledger of valid transactions between agents of a virtual
economy without a central institution for coordination. In order to keep track
of a faithful and...








Thanks.

-mZ

## Replies

**phillip** (2018-07-08):

[UCC § 9-102](https://www.law.cornell.edu/ucc/9/9-102#depositaccount) (see “account” v. “deposit account”)

[Hohfeld (1913)](https://digitalcommons.law.yale.edu/ylj/vol23/iss1/4/)

[Jensen (2000)](https://books.google.com/books?id=aA8vLoVW45UC&pg=PA169)

[Schlag (2015)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2465148)

---

**mzargham** (2018-07-08):

[@phillip](/u/phillip):  One cannot write proofs of things with Legal definitions. If need be you can change the names in the paper as you see fit in order to interpret it properly in your preferred english language space, but all the mathematical definitions are explicit and formal.

We chose the verbiage the engineers we worked with were most comfortable and would not be opposed to changing terms for the purpose of clarity with other communities. We simply used address to refer to the unique identifier and account to refer to the object identified which contains other data. In the context of our work, we felt this was a more important distinction than resolving to details of financial and legal terms. Ambiguity is not an issue because the technical definition is explicitly stated.

It seems an odd critique, as this choice of terms has no bearing the mathematical equipment presented nor its suitability in proving existence, uniqueness, convergence and stability of equilibrium. If you are not interested in these topics that is fine but if you are, please see a textbook on [non-linear systems](https://www.amazon.com/Nonlinear-Systems-3rd-Hassan-Khalil/dp/0130673897) as a starting point, then one can move on to academic papers addressing harder problems. This material is somewhat esoteric but it is practical; it serves as the underpinning of all complex physical world systems that perform under high degrees uncertainty or explicitly missing information. Solving problems formally with lots of missing information requires higher degrees of mathematical abstraction, but the results provide equipment for designing practical algorithms with provable fixed point properties.

If you would like to get the gist of it here are some wiki articles:


      [en.wikipedia.org](https://en.wikipedia.org/wiki/Fixed-point_theorem)




###

In mathematics, a fixed-point theorem is a result saying that a function F will have at least one fixed point (a point x for which F(x) = x), under some conditions on F that can be stated in general terms. Results of this kind are amongst the most generally useful in mathematics.
 The Banach fixed-point theorem gives a general criterion guaranteeing that, if it is satisfied, the procedure of iterating a function yields a fixed point.
 By contrast, the Brouwer fixed-point theorem is a non-construc...









      [en.wikipedia.org](https://en.wikipedia.org/wiki/Banach_fixed-point_theorem)




###

In mathematics, the Banach–Caccioppoli fixed-point theorem (also known as the contraction mapping theorem or contractive mapping theorem) is an important tool in the theory of metric spaces; it guarantees the existence and uniqueness of fixed points of certain self-maps of metric spaces, and provides a constructive method to find those fixed points. It can be understood as an abstract formulation of Picard's method of successive approximations. The theorem is named after Stefan Banach (1892–19 De...








Our paper formally maps the state variables maintained by a blockchain network to discrete dynamical systems so these concepts can begin to be applied. The fundamental building blocks (fixed point theorems) engineering systems of high orders of complexity and are woefully lacking in the current “crypto-economic” literature. It is frustratingly common to see existence results from Nash game theory invoked and mistakenly claim uniqueness, convergence and/or stability. You need more mathematical equipment to get into that and we simply aim to help equip this new field with proper constructs to address equilibrium in a blockchain-enabled economy properly.

---

**phillip** (2018-07-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/mzargham/48/1622_2.png) mzargham:

> It seems an odd critique, as this choice of terms has no bearing the mathematical equipment presented nor its suitability in proving existence, uniqueness, convergence and stability of equilibrium. If you are not interested in these topics that is fine but if you are, please see a textbook on non-linear systems as a starting point, then one can move on to academic papers addressing harder problems.

I am, actually, interested in nonlinear dynamics, but leaving aside the matter of “suitability” and normative discussions on what ideally constitutes a foundations text in an institutional agent-based computational economics taking for granted the effectiveness of the cryptographic protocol: I read your paper. I should like to read many more like it. The matter of resolution in, well, something like legal namespace, is not a critique of the formal portion of the work, but I hope you find the papers responsive to the thrust of the motivation.

I think the scab I am picking at is inverse to the frustration you express: inasmuch as you describe “accounts,” what does that mean for “rights” in terms of “methods,” and similar heuristics. What you are describing is in many parts chain-[of-title-]agnostic; I have posted material on property that may or may not reflect a development cognate with the institutional transition you describe between your sections III and IV.

---

**mzargham** (2018-07-08):

> taking for granted the effectiveness of the cryptographic protocol

I agree that taking as an assumption the proper functioning of the underlying cryptographic protocol is an important thing to call out. I would argue that it is strictly necessary in order to properly decouple two hard problems, one which is fundamentally combinatorial in nature (the consensus protocol) and one which is best modeled as continuous, the flow of funds and/or the evolution of other dynamic variables such prices, interest rates, bonding curves, revenue sharing allocations, etc.

> I think the scab I am picking at is inverse to the frustration you express: inasmuch as you describe “accounts,” what does that mean for “rights” in terms of “methods,” and similar heuristics.

The methods that I construct are in fact totally chain agnostic (as you note) as they only represent the notion of an operation on the state for which the resulting change in state caused by the operation is explicitly (or implicitly) dependent on both an input provided by the actor and the current state of the system. This is actually so completely generic structurally that there will be examples from any field where there is an  pre-specification of a future right to act*, including legal financial where terms and conditions of an agreement include observations or estimation of facts at the time some right is exercised.

The particular definitions in IV are actually just overview of the kind of mathematical constructs one can use to show invariance or convergence (or divergence) in the space of possible states of the system rather than to make arguments about any particular realization. By staying in the realm of possible as implied the structure of a state depend outcome, we get more general tools for informing the design and verification of “contracts” which are primarily defined by the right to take an action which has a predefined outcome as function of the action itself and the state of the system at the moment that action is actually computed on chain. In generally, imagine applying these tools to the set of methods exposed publicly but there is not reason that access control of these methods wouldn’t play a part in applying them to a specific use case.

I see a lot of cases where actions or states in one system would modify the right to access other functions, but for the purpose of proofs in the manner I hope to see, one would not worry about who has access so much as how any use of the methods at anytime but any actor would impact the set of all possible states the system may take thereafter.

I view this work as far from complete both in language choice (because this is a normative process) as well is in the mathematics (which i don’t consider normative). I think the most direct response to concerns about terminology choice would be step up from any terms with use case specific baggage and stay in the realm of formal operators and then only to adapt domain specific language when applying the tools to a particular application. I could happily do without the word account – from perspective we’re talking about spaces, partitions of those spaces, measures of those spaces and functions that may have implications on those measures.

I admittedly struggle to make this to of work accessible to the broader community responsible for implementing programatic contracts for which this concepts serve as important building blocks for rationality agnostic guarantees. Even for engineers trained in fields that rely on such arguments the derivations and fundamentally topological arguments are often out of reach. I’ve studied mathematical models (and design and deployed algorithms) of estimation, decision making and coordination for well over a decade (since ~2003) so I may have had unreasonable expectations of this community regarding the formal study emergent and/or convergence properties of systems.

In fact my aim forward is to see more algorithms with state dependent structures implemented which respect invariants and then to collect actual data from the ethereum network to validate those claims. My R&D firm has its own custom ethereum data collection infrastructure and we’re working on some prototype state-feedback algorithm designs on private test nets.

[@phillip](/u/phillip),  Thanks for the feedback. I hope this helped answer some of your questions.

-mZ

*I would argue that the physical world it self has this property. We have naturally the right or ability to take physical actions (like exert forces on things to move them) that don’t violate the law’s of Newtonian physics. To tie it back to your comment about the assumption that the consensus protocol does its job. I view this as being akin to focusing on Newtonian physics for engineering purposes when we know well that these a just scale and context appropriate mathematical models.

---

**phillip** (2018-07-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/mzargham/48/1622_2.png) mzargham:

> I view this work as far from complete both in language choice (because this is a normative process) as well is in the mathematics (which i don’t consider normative). I think the most direct response to concerns about terminology choice would be step up from any terms with use case specific baggage and stay in the realm of formal operators and then only to adapt domain specific language when applying the tools to a particular application. I could happily do without the word account – from perspective we’re talking about spaces, partitions of those spaces, measures of those spaces and functions that may have implications on those measures.

I actually just meant to make salient a complementary abstraction and referred to §9-102 as an index of customary definitions bound to a history of implementations of a surprisingly formally describable set of operations, not to imply, necessarily, a competition for scarce terminological lexicon…account space, or assert some kind of priority contest for terminological dominance.

That said, maybe that incentive-compatibility inquiries tend to stop at existence proofs, and your IV.C observation that the construction of Lyapunov functions are non-trivial - well, in the interest of prudence, best to leave it at the empty truism that there appear to be a handful of expensive public choice questions that turn on semantic virality in the wild, and to coordinate semiotic building blocks between expert communities is something I’m more than happy to leave to smarter people like yourself, as to handle optimal control formalizations of [this kind of thing](https://coincenter.org/entry/what-could-decentralization-mean-in-the-context-of-the-law) in terms of propositional content and feedback between global and local values is a pretty serious undertaking.

![](https://ethresear.ch/user_avatar/ethresear.ch/mzargham/48/1622_2.png) mzargham:

> By staying in the realm of possible as implied the structure of a state depend outcome, we get more general tools for informing the design and verification of “contracts” which are primarily defined by the right to take an action which has a predefined outcome as function of the action itself and the state of the system at the moment that action is actually computed on chain. In generally, imagine applying these tools to the set of methods exposed publicly but there is not reason that access control of these methods wouldn’t play a part in applying them to a specific use case.
>
>
> I see a lot of cases where actions or states in one system would modify the right to access other functions, but for the purpose of proofs in the manner I hope to see, one would not worry about who has access so much as how any use of the methods at anytime but any actor would impact the set of all possible states the system may take thereafter.

I’d love to know a chain-agnostic notion of “error” in complex systems that manages to credibly isolate the formal procedures in federated decision state-space as mathematical problems when I saw it, but it’s beyond my pay grade, so to speak. Maybe [McCarty (2001) at 29-31](https://www.researchgate.net/publication/220539475_OWNERSHIP_A_case_study_in_the_representation_of_legal_concepts) comes closer to where I’m…drifting? Section 3 of [Shaheed, Yip, Cunningham (2005)](https://pdfs.semanticscholar.org/547b/43c4ace615a640eb9b7cb89d7a1df58abf16.pdf) might also mirror the is-ought divergence in the possible-optimal for access control generally, as distinct from security ownership rules or similarly particular, domain-specific schemes.

tl;dr if I have a point, much less a critique, it is maybe just that an account as a [frame 𝕱=(sk,pk)](https://ncatlab.org/nlab/show/Kripke+frame) is a cool idea?

---

**mzargham** (2018-07-08):

> That said, maybe that incentive-compatibility inquiries tend to stop at existence proofs, and your IV.C observation that the construction of Lyapunov functions are non-trivial - well, in the interest of prudence, best to leave it at the empty truism that there appear to be a handful of expensive public choice questions that turn on semantic virality in the wild, and to coordinate semiotic building blocks between expert communities - well, I’ll leave it to smarter people like yourself to handle optimal control formalizations of this kind of thing in terms of propositional content and feedback between global and local values.

This block represents the prevailing sentiment that I object to for the following reasons:

a) incentives do not come into play at all in the Lyapunov-like value functions i constructed – in fact I propose these functions precisely because they are sufficiently general to handle conditions where we wish to make no assumptions about the actions taken, merely all actions that might be taken

b) incentives do matter and should be considered careful AFTER one has established or at least reasoned about the actual achievable states of a system. No one writing an Ethereum smart contract for example worries about disincentivizing an ERC20 token from being double spent because the correct execution of the code already ensure that and its resulting global conservation property.) Any considerations for such an “attack” live at the level of the consensus protocol for ethereum where they can and should continue to be studied.

c) There is a huge difference between a hard proof and a complex algorithm. More often than not the work of an engineer responsible for designing a decentralized algorithms challenge is discover and prove that a dirt simple local algorithm has desirable global properties. This is very hard and the workproduct is complex because it is not the algorithm itself but rather the algorithm, its formal goal, and the conditions and extent to which it achieves or approximates that goal. Case in point one of the first systems I worked on was “robotic flocking.” These algorithms can be reduced to each agent locally applying collision avoidance and velocity matching with other nearby observable agents. One needs to impose potential functions and use Lyapunov arguments to prove when and the extent to which the groups are cohesive and achieve navigation goals but the algorithms themselves are very simple.

d) lastly, assuming that we cannot similarly understand the cohesive behaviors of economic actors as group even when we cannot understand them individual is just the story people tell themselves to avoid doing the hard work necessary to defend claims. One can character multi-agent repeated potential games which are mathematically very similar to the flocking problem AND you should not even need to assume rationality beyond depending the potential gradient in expectation even if you move against it often. For that type of reasoning one also needs to under stand convergence properties of stochastic process.

My argument really hinges on the community assuming they cannot prove anything practical and then using that as an excuse to never explore properly what one can and cannot realistically prove. I am not an advocate of math for maths own sake. I would not have left my cushy academic career trajectory if I was like that. Now I am spending a lot of effort to bring academics who actually know how to do this stuff to help solve crypto problems, which is actually the purpose of this paper.

Still appreciating the discussion.

-mZ

---

**phillip** (2018-07-08):

Oh, I well appreciate the effort. I don’t mean deference to your expertise as, like, implying a black eye for tractability of stochastic models. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**mzargham** (2018-07-08):

No worries. I appreciate the discourse. You don’t get coordination if you don’t have flows of information. I will try to be more aware of the specific financial and legal formalisms you linked as I continue to extend my own work and engage with my former colleagues from this academic discipline.

I do advocate that anyone who is serious a blockchain as platform for coordination look more into more Electrical Engineering, Systems Engineering, control engineering, robotics, estimation, optimization and decision system with a specific eye to problems with embedded unknown network topologies and/or agents who are characterize not by a pattern of behavior but rather by some local utility which may or may not be known at all.

I’ve also been trying to figure out how best to approach curating a library of resources and its been difficult to assess where to start when so much builds on 4-6 years of baseline engineering education (multivariate calculus, physics, applied differential equations and signal processing, statics, dynamics, circuits, etc) that we cannot assume most people have or remember.

In any case, the discussion helps me better understand how to approach the normative aspect of my problem solving space just by virtue of the exchange.

Thanks,

mZ

---

**phillip** (2018-07-08):

Pleased to have been no more noxiously dense than as to only register as a typical innumerate. Below is a draft with copy from before reading your response, incomplete, presented as notes, ranging in quality from redundant/inapposite to possibly/probably downright incorrect and/or counterproductive.

---

> mzargham:
>
>
> More often than not the work of an engineer responsible for designing a decentralized algorithms challenge is discover and prove that a dirt simple local algorithm has desirable global properties. This is very hard and the workproduct is complex because it is not the algorithm itself but rather the algorithm, its formal goal, and the conditions and extent to which it achieves or approximates that goal.

I was actually commenting earlier that the assumption is that the cryptography qua cryptography is working, not reflecting on the matter of the integrity of the consensus protocol in terms  of the validity of the mapping of concepts in such a manner as to rehash [Quine (1951)](http://www.ditext.com/quine/quine.html).

The point is not as to the objective appropriateness of “account” any more than, for example, the degree of intrinsic vulgarity of the idea of an asset-backed “curation market.” But then, I am not sure the point is even as to whether the desirability of using ordinary language for descriptive purposes is a function of the endogeneity of regulation, however abstracted, to commercially-coded communications. It is certainly not an ex ante proposition as to “how” the specification of preferences within a community of heterogeneously distributed sophistications across a number of dimensions and contexts would be best reached.

![](https://ethresear.ch/user_avatar/ethresear.ch/mzargham/48/1622_2.png) mzargham:

> I propose these functions precisely because they are sufficiently general to handle conditions where we wish to make no assumptions about the actions taken, merely all actions that might be taken…incentives do matter and should be considered careful AFTER one has established or at least reasoned about the actual achievable states of a system.

Wrestling with formalizing [“building blocks”](https://plato.stanford.edu/entries/wittgenstein/#LangGameFamiRese) of a language-game vis-à-vis a gradient in expectation in distributed state histories is, as McCarty *supra* notes, not reaching this particular interpretive community as a brand new challenge:

![](https://ethresear.ch/user_avatar/ethresear.ch/mzargham/48/1622_2.png) mzargham:

> My argument really hinges on the community assuming they cannot prove anything practical and then using that as an excuse to never explore properly what one can and cannot realistically prove. I am not an advocate of math for maths own sake. I would not have left my cushy academic career trajectory if I was like that. Now I am spending a lot of effort to bring academics who actually know how to do this stuff to help solve crypto problems, which is actually the purpose of this paper.

Whether the constraints of the namespace in an allocation scheme in “crypto problems,” in matters where the crypto is not cryptography, matter or should matter, is not my place to say. If they do, the cause of such unwillingness to make positive statements may well have a [family resemblance](https://www.casebriefs.com/blog/law/securities-regulation/securities-regulation-keyed-to-coffee/definitions-of-security-and-exempted-securities/reves-v-ernst-young-2/) to the fact that I am not the reader’s lawyer and this is not legal advice. I enjoyed reading the paper and hope to read clear material of the sort you describe from qualified parties.

---

**mzargham** (2018-07-08):

Definitely going to need time to digest your notes but I will say on first pass the thing stuck out at me is that I would agree that none of what we are doing should really be called “crypto problems” – we’re not really doing cryptography AT ALL in the layer I am talking about, its run of the mill coordination, estimation and decision problems that have the awesome extra property that they are equipped with a trustworthy source of computation.

Admittedly, I’ve been slowly picking up that language as I’ve slowly gotten more acquainted with the community. I am admittedly also, lukewarm with the title “token engineering” for the community I am helping curate with others who share aspects of my background but I differed from contention over naming, but i prefer economic systems engineering. If anything at all, I would argue its systems engineering and in particular Information and Decision Systems if one were to be precise in the manner of (https://lids.mit.edu/).

Let’s continue this discussion a slight longer period. Basic research is my grind of choice but I have practical and operational work to attend to.

Thanks,

-Z

---

**mzargham** (2018-07-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/phillip/48/766_2.png) phillip:

> I was actually commenting earlier that the assumption is that the cryptography qua cryptography is working, not reflecting on the matter of the integrity of the consensus protocol in terms of the validity of the mapping of concepts in such a manner as to rehash [Quine (1951) ]

I am struggling to peel myself away – my philosophy of models (and language as a subset of models) is an important motivator for the kind of work i do.

So on to the point –  I really liked reading the Quine link above, but i still disagree the point I think you are referring to – that said, based on the totality of that article, I may share a lot philosophically with Quine. He just uses too rigid a framework, that doesn’t allow him to expand his language model to the point that it is sufficiently rich to handle the ideas in question. If you feel that there is a place where the ‘model’ in my work needs to be enriched or modified to be sufficient, I am open to it.

If we had white board we could map out a logical structure (actually many different ones as they are not unique) that would pretty clearly provide valid analytical reasoning that would not conclude that morning star = evening star.  The breakdown comes because his logical model doesn’t retain the context that it needs to properly handle the idea presented.

Simplest extension of the first example might be to say that evening star is a reference to (venus, context = c1) and morning star = (venus, context = c2) so that clearly not equal accounting for the different context. I am not even saying c1 = ‘evening’ and c2 = ‘morning’ because I would argue that is still missing the cultural context of the term – in this case the terms ‘morning star’ or ‘evening star’ are actually serving to encode and transmit ideas that are way too rich for such a simple compression.

Even that is only a slightly richer model - if one were committed to characterizing a particular set of ideas analytically it falls on the communicator or person doing the reason to chose the simplest model that has enough detail to capture the information they wish to transmit or evaluate. It’s a VERY common fallacy to pick a model that is bad fit for a particular idea and then show it failing and say models are bad. Regardless of whether we are talking about formal or natural languages. I believe this comes from people not being aware of the fact that they are applying models and furthermore have the burden of properly fitting the model to the task at hand.

My take is this:

Ideas and concepts are inherently too complex for us to perfectly represent them with any model (all models are wrong but some are useful is a famous quote ([All models are wrong - Wikipedia](https://en.wikipedia.org/wiki/All_models_are_wrong))

I purport that all of the following are just models of ideas:

-spoken word

-written word

-logical constructs

-mathematical constructs

-arbitrary combinations of the above are all just models of ideas

the models are useful insofar as they help us accomplish a goal

BUT goals are themselves ideas so we need to model them as above

so the logic is recursive.

To close the loop with our earlier discussions this is actually only useful if the above recursion ends up having a fixed point – that is to say the models of all the ideas in question are logically consistent:

we say “problems are solved” when:

models of ideas about solutions meet the needs of the models of ideas about goals

Personally I find that much easier when both of those two things are expressed predominantly in formal language, which bring us to another relatively famous idea: [The Unreasonable Effectiveness of Mathematics in the Natural Sciences - Wikipedia](https://en.wikipedia.org/wiki/The_Unreasonable_Effectiveness_of_Mathematics_in_the_Natural_Sciences)

that is to say, philosophically speaking our models are way too coarse to truly capture the physical world and yet engineering marvels demonstrate that sufficiently formal models, analytical reasoning plus empirical data, allows us to not only “solve problems” with our models but actually to use those modeled goals+solutions to make real things work in our full fidelity physical world.

I simply believe that we can also do that in our social/tech/economic domain.

---

**phillip** (2018-07-18):

Yes, I would love to see more formal managerial economics & decision science approaches in mutually digestible New Institutional / “world computer” pragmatics. But *Naming and Necessity* aside,

![](https://ethresear.ch/user_avatar/ethresear.ch/phillip/48/766_2.png) phillip:

> tl;dr if I have a point, much less a critique, it is maybe just that an account as a frame 𝕱=(sk,pk) is a cool idea?

[![01%20AM](https://ethresear.ch/uploads/default/optimized/2X/f/f7576632fdcf8c3f176c062efb76eb8938cc416d_2_690x421.png)01%20AM1204×736 332 KB](https://ethresear.ch/uploads/default/f7576632fdcf8c3f176c062efb76eb8938cc416d)

