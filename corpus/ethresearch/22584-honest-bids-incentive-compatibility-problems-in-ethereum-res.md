---
source: ethresearch
topic_id: 22584
title: "Honest Bids ≠ Incentive Compatibility: Problems in Ethereum Research"
author: trevelyan
date: "2025-06-11"
category: Economics
tags: [consensus-incentives]
url: https://ethresear.ch/t/honest-bids-incentive-compatibility-problems-in-ethereum-research/22584
views: 304
likes: 5
posts_count: 3
---

# Honest Bids ≠ Incentive Compatibility: Problems in Ethereum Research

As someone actively working on mechanism design, I wanted to write a short post about a recurring issue in how implementation theory is being applied in research connected to the Ethereum Foundation, its Incentives Research Group, and several other ETH-adjacent institutions.

The problem is, at heart, very simple: instead of specifying the outcome (the “social choice rule”) with which protocols are supposed to be incentive compatible, many papers instead assume that “honest bidding” constitutes “truthful preference revelation,” and that this is sufficient for incentive compatibility.



      [scholar.harvard.edu](https://scholar.harvard.edu/files/maskin/files/implementation_theory_published_version.pdf)



    https://scholar.harvard.edu/files/maskin/files/implementation_theory_published_version.pdf

###



3.10 MB










Correcting this impression is one of the goals Maskin set himself in his chapter on implementation theory (above). If our goal is to elicit a certain kind of information from users (e.g., a truthful bid), then what must be revealed for a mechanism to have truthful preference revelation is any private information that affects whether users share that information. The bid itself is not the private preference.

Part of the confusion seems caused by the Vickrey auction, which uses honest bidding to implement a particular social choice rule: “efficient allocation.” But even here, this correspondence holds only under limited conditions. We cannot assume that any mechanism – even a similar auction – with disclosure of the same preferences will be incentive compatible with the same social choice rule.

To provide two simple examples of why this is the case, note that moving from a one-sided to a two-sided auction changes the entire landscape. Implementing “efficient allocation” now also requires implementing the “efficient production” of utility. And that means eliciting private information from producers as well as users.

A second more subtle issue is that even the standard Vickrey auction is not incentive compatible with “efficient allocation” once user valuations become interdependent — that is, once the fee anyone is willing to pay depends on total fees or other system-wide effects. So even if we ignore block producers completely it is not even true that honest bidding achieves incentive compatibility in the way people assume it does.

There are many other issues. A two-sided market introduces many additional complexities: heterogeneous utilities, multi-dimensional preference revelation, strategic behavior involving public and private transaction flow, and new forms of collusion and time-sensitive bidding. None of these fits comfortably into the models lacking proper preference revelation.

I don’t know whether the continued use of simplified frameworks results from systemic publish-or-perish pressures – favouring fast iteration on existing models over other work – or reflects the types of research that the EF sees as critical for analysing ETH-specific economic problems.

Regardless, my experience is that it is hard to make progress in this area when papers don’t clearly define their social choice rules or properly use the incentive compatibility framework – and where peer review, including from core institutions like the EF, fails to catch this.

I hope that articulating this issue publicly can encourage more rigorous use of the incentive compatibility framework. This would open the door to easier discussions, stronger peer review, and ultimately, protocols that are simpler and more reliable in decentralized environments.

## Replies

**MicahZoltu** (2025-06-12):

I would love to see more people (such as yourself) calling out these things on various proposals.  I try to call them out when I see them, but many proposals are very long so I narrowly constrain the set of proposals I read to topics of great interest to me.  We need more people giving constructive criticism like this to proposals overall.

---

**trevelyan** (2025-06-13):

Thank you for the goodwill shown in the reply, Micah. And for reading.

