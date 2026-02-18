---
source: ethresearch
topic_id: 1014
title: "\"Holographic consensus\" — decentralized governance at scale"
author: fmatan
date: "2018-02-07"
category: Uncategorized
tags: [governance]
url: https://ethresear.ch/t/holographic-consensus-decentralized-governance-at-scale/1014
views: 6131
likes: 13
posts_count: 16
---

# "Holographic consensus" — decentralized governance at scale

A critical but still missing element for successful implementation of DAOs and collaborative DApps is a **decentralized governance system**: an efficient and resilient engine for collective decision-making, at scale.

The greatest challenge of distributed consensus is to enable an efficient navigation of the collective attention: too much of collective attention on certain things conflicts scalability, but insufficient collective attention on other things conflicts with resilience.

This is the fundamental “scalability problem” appearing in any decentralized governance/consensus system.

Any resolution of this tension will allow minority decisions that are guaranteed to be in strong correlation with the majority “truth”. That can be taken to be the definition of *coherence*.

“Holographic consensus” is a solution of this sort (analogue to off-chain computation), which is detailed over a series of blog posts, the first of which is this:


      ![image](https://cdn-static-1.medium.com/_/fp/icons/favicon-rebrand-medium.3Y6xpZ-0FSdWDnPM3hSBIA.ico)
      [Medium – 13 Feb 18](https://medium.com/daostack/decentralized-governance-first-principles-1fc6eaa492ed)


    ![image]()

###

Blockchain hype is at an all-time high and many people anticipate the first decentralized application to reach the market and gain mass…



Reading time: 6 min read









I would love any feedback, questions and other discussion on these matters.

## Replies

**jamesray1** (2018-02-07):

Sounds good, I’ll read the blog posts tomorrow.

---

**kladkogex** (2018-02-07):

You could have a system where initially a small number of users are picked, and in case of unanimous  or near unanimous decision, the veridict is reached,  otherwise of a tighter split a large group is formed.

In this case, easy decisions will be reached faster, and tighter decisions will require attention from more users.

As an example, you first pick 8 random users and let them vote for a binary decision. If you get  8 or 7 votes yes (or no) the verdict is reached.   Otherwise mark the verdict as undecidedd and  pick 8 more users.  If out of 16 total users, say 16, 15,14, or 13 vote yes (or no) then the verdict is reached, otherwise, you randomly pick 16 more users, and so on.

What the description above informally describes is you replace global voting by small sample voting,  but then require supermajority to account for statistical fluctuations on small samples. The supermajority requirement weakens as you move to large samples, so you are guaranteed to reach a verdict at some point.

This all can be defined mathematically I believe, based on probability theory. Basically, one needs to define a supermajority cutoff function

Sm = F(N, r), where N is the total size of the sample, and r is the majority vote (the minority vote is then N - r).  You start with a small sample, and then double if the required level of supermajority is not reached, and stop and issue a verdict if you achieve the supermajority as defined at the current sample size.

---

**tawarien** (2018-02-07):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> As an example, you first pick 8 random users and let them vote for a binary decision. If you get  8 or 7 votes yes (or no) the verdict is reached.   Otherwise mark the verdict as undecidedd and  pick 8 more users.  If out of 16 total users, say 16, 15,14, or 13 vote yes (or no) then the verdict is reached, otherwise, you randomly pick 16 more users, and so on.

In that case, it would be important to use a selection algorithm where nobody knows who was selected but only the selected should be able to proove that they are allowed to vote .

if this is not guaranteed bribing attacks are very easy.

---

**kladkogex** (2018-02-07):

There are cryptographic algorithms such as *mental poker* and others which allow exactly this - selecting sets of users in such a way, that only selectees know they have been selected …

---

**miles2045** (2018-02-07):

There is an under-the-radar project in development I’ve been following over the years called Tau, a collaboratively self-amending program designed to scale human collaboration and knowledge building. IMO it’s the best approach I’ve seen to scalable governance, and it introduces some very interesting concepts: http://www.idni.org/blog/the-new-tau

---

**jamesray1** (2018-02-08):

Sorry I need to focus on building a sharding implementation.

---

**jamesray1** (2018-02-09):

Has anyone read the Democracy.Earth [white paper](https://github.com/DemocracyEarth/paper/blob/master/README.mediawiki)?

---

**fmatan** (2018-02-10):

You’re very right [@kladkogex](/u/kladkogex).

Generally any effective large-scale governance needs to have **certain** mechanism to allow for small-group decisions on behalf of the greater majority, that are **guaranteed** to be in good correlation with it.

The first mechanism that I’m aware of is analogous to off-chain computations (where agents can stake tokens against the outcome of a certain proposal), on which I will expand in the 2nd coming blog post.

The second way that I’m aware of is indeed the one you mention, which is analogous to dynamic sharding, where random sets are chosen and supermajority is required accordingly, just as you describe.

However, let me point to two weaknesses of the second approach (and thus my current focus on the first, although I believe eventually we might have both in conjunction):

1. As mentioned above, randomness is subtle, and, while I’m not claiming it’s unsolvable, I would at least say that randomness here is critical, and is not a trivial issue (although perhaps solvable, as argued).
2. More importantly, note that this second approach relies on proposal-agnostic statistics, which is problematic. Let me try to explain:

If there’s a certain fixed probability to “attack the system” (= succeed in passing a proposal that is not in correlation with the greater-majority will), and there’s a certain fixed price for submitting a proposal, then I can easily submit enough proposals that are benefitting enough (i.e. enough money sent to me) to make it profitable / attackable.

The point is that in a fully decentralized governance system you cannot allow for a “small probability” to make “very large mistakes”. You may be ok with a “small probability” for “small mistakes”. The problem/subtlety is to programmatically weigh the “size of a mistake”. In terms of transactions of tokens it’s perhaps easier, but what if the contracts can do other things, such as assigning reputation (what is “small”? depending on some factors), or changing the protocol (this is potentially definitely not small), etc.

Not unsolvable, but just pointing out the subtlety.

The advantage of the first method (to be expanded over next time) is that you use cryptoeconomics to bound mistakes. In other words, **whenever there exists a potential for a mistake / attack to take place**, there is a **clear and well defined** potential to make profit for whoever identifies the mistake. That guarantees a market-like, dynamic resistance to attacks (so that people weigh the criticality of mistakes rather than programs).

But really good point made above, and great discussion.

Thanks

---

**fmatan** (2018-02-10):

Thanks [@miles2045](/u/miles2045).  I know Ohad (the founder and scientist of Tau) for years.

I wasn’t aware about a solid achievement on general, decentralized and scalable governance systems, but I will definitely check in again with him and hope to learn new things.

To my best knowledge, a scalable governance system has not been implemented yet, not even on paper. I think we’ve finally got all ingredients in place (on paper and in code: https://github.com/daostack/arc ).

I’ll release the 2nd post describing the protocol in the coming weeks and would hope to get the feedbacks of the community. Working DApps/DAO using this protocol will follow soon.

Would be grateful for any specific materials on these matters.

---

**fmatan** (2018-02-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> white paper

Thanks [@jamesray1](/u/jamesray1). No, I haven’t; does it solve same problems? have you read it?

Did you have time to go over my [post](https://medium.com/daostack/decentralized-governance-first-principles-1fc6eaa492ed)? would love to hear your feedback.

---

**jamesray1** (2018-02-10):

[@fmatan](/u/fmatan) I am about halfway through the Democracy Earth white paper. They are offering a solution for governance on the blockchain with organisations of any size. The governance is set accordingly by the organisation, but there are a range of voting and other methods. I haven’t had time to read your post yet.

---

**fmatan** (2018-02-10):

From a very (very) quick look at the Deomcracy Earth white paper it seems to me that we have a slightly different focus then them.

Firstly, if I grasp it correctly (by a few sec look) they’re focusing on vote-per-identity paradigm => and then the need to verify identities. This is a very legitimate use case, though I’m more interested in general DAOs whereby an agent can be a group of people, and vice versa, a person can have 10 identities. What matters for an agent is only its “voting/impact power”, or reputation (though DE use this word for something else).

Secondly, it seems that their main method for scaling governance is Delegation. While it is very legitimate and useful, again, I’m focused on a much more flexible method. Delegation would generally lead to semi-centralization (although voluntarily) and degradation of the collective intelligence. Holographic Consensus actually allows decision making take place at the edges (which is quite different from classic delegation), and I would argue it induces the collective intelligence significantly.

Nevertheless, let me just note that I’ve met before the people of Democracy Earth and that they’re very talented and impressive. They’re just working on a slightly different direction, designed more towards “classical systems” on the blockchain (more efficient and scalable) rather than DAOs in sense of completely new form of organizations.

---

**jamesray1** (2018-02-11):

[@fmatan](/u/fmatan), thanks for your comments. I need to prioritise looking for work, but if I get a chance to read your posts I’ll let you know my thoughts on them, but it might be a while until I find some time to set aside.

---

**jamesray1** (2018-02-12):

[@fmatan](/u/fmatan), I left comments on your post, and here are links to them:


      ![image](https://cdn-static-1.medium.com/_/fp/icons/favicon-rebrand-medium.3Y6xpZ-0FSdWDnPM3hSBIA.ico)
      [Medium – 12 Feb 18](https://medium.com/@james.ray/https-ethresear-ch-t-holographic-consensus-decentralized-governance-at-scale-1014-13-u-jamesray1-db483201ad8e?source=quoteResponses---------0)


    ![image]()

###

The organization sets the rules: which could be no delegation allowed.



Reading time: 1 min read










      ![image](https://cdn-static-1.medium.com/_/fp/icons/favicon-rebrand-medium.3Y6xpZ-0FSdWDnPM3hSBIA.ico)
      [Medium – 12 Feb 18](https://medium.com/@james.ray/de-are-also-looking-to-do-off-chain-computation-although-albeit-it-is-less-secure-as-i-have-raised-afb2e1772801?source=quoteResponses---------0)


    ![image]()

###

DE are also looking to do off-chain computation, although albeit it is less secure as I have raised in an issue. In the event of an attack, funds could be recovered if they are on-chain, but not…



Reading time: 1 min read

---

**fmatan** (2018-11-18):

An introduction to Holographic Consensus: https://medium.com/daostack/holographic-consensus-part-1-116a73ba1e1c

