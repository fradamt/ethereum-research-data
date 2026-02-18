---
source: ethresearch
topic_id: 14545
title: Collusion Resistance and Plurality in Quadratic Mechanisms (Paper Summary)
author: Jmiller4
date: "2023-01-04"
category: Economics
tags: []
url: https://ethresear.ch/t/collusion-resistance-and-plurality-in-quadratic-mechanisms-paper-summary/14545
views: 1235
likes: 1
posts_count: 2
---

# Collusion Resistance and Plurality in Quadratic Mechanisms (Paper Summary)

Hi all. Gen Weyl, Leon Erichsen and I recently published a paper on [collusion-resistance and plurality in quadratic mechanisms](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4311507). In this paper we tried to examine some of the proposed mechanisms from the appendix of the DeSoc paper more deeply and suggest new ones. In this post, I’m going to give a TLDR for the most important technical parts of the paper. (Also: all the mechanisms I’ll discuss are coded up in this [GitHub repository.](https://github.com/Jmiller4/plural-qf))

**Defining Collusion Resistance for QF**

In order to formally define collusion resistance, we used “vanilla” QF as a guidepost. In regular QF, there are diminishing returns from contributing more and more: when an agent contributes x, the system adds in O(\sqrt{x}) in external matching funds. If an agent could contribute x and eke out O(x) in matching funds, that might be an issue. But that’s exactly what can happen in vanilla QF if we imagine that agents can coordinate in groups: a group can contribute x collectively and get matching funds that grow linearly in x or faster. (To be clear: in our model, “groups” are simply sets of members who have the ability to coordinate.)

So it seemed natural to define collusion resistance as essentially an extension of this diminishing returns property to groups. Specifically, we define collusion resistance via three sub-properties:

1. Diminishing returns for agents: if an agent contributes x, the amount of external matching funds is O(\sqrt{x}) (normal QF already has this property, as mentioned above – we want to make sure we don’t lose it).
2. Diminishing returns for groups: if a group of coordinating agents contributes x collectively, the amount of external matching funds is O(\sqrt{x}).
3. Diminishing returns from adding new members: If x agents join a group, each contributing some constant amount y, then the amount of external matching funds is both O(\sqrt{x}) and O(\sqrt{y}). These agents can be completely new to the system, or they can have already been in other groups.

It’s important to note that from here on out, we’ll be assuming that our mechanisms have accurate information about group memberships. Despite this assumption, the problem is still non-trivial since, as we’ll see, the mechanisms from the DeSoc paper have issues even with complete information about group memberships.

**Examining the Mechanisms from the DeSoc Paper and Moving Forward**

The three mechanisms from the DeSoc paper (*Pairwise Discounting*, *Cluster Match* and *Offset Match*) each have strengths, but also fall short of the technical criteria I laid out above.

- Pairwise Discounting doesn’t have diminishing returns from adding new members, but leverages a very powerful and intuitive idea about attenuating specific parts of the funding amount which we use later.
- Cluster Match uses another nice idea: creating synthetic “group donations” using group information, and then doing QF on those. However, it doesn’t have diminishing returns for agents or diminishing returns for groups.
- Offset Match brought a somewhat orthogonal set of technical questions to the table. Offset Match uses the solution to a system of linear equations to calibrate funding, but it turns out that this system doesn’t always have a solution. We were able to characterize the set of circumstances that correspond to solvable systems of equations, and leverage that characterization to add in a pre-processing step to guarantee solvability. But we were also able to show that offset match can sometimes completely eat an agent’s donation and not increase funding at all, therefore making it somewhat irrational for agents to participate in the first place (i.e. Offset Match doesn’t have individual rationality).

Fortunately, we were able to design a new mechanism, *Connection Oriented Cluster Match*, that essentially combines ideas from both Pairwise Discounting and Cluster Match to achieve all three of the sub-properties in our definition of collusion resistance. We also suggest two other promising mechanisms for further exploration. The one we’re most excited about, *Eigen Match*, uses the eigenvectors of a social graph’s adjacency matrix to calibrate funding levels.

**Limitations and Future Work**

The most important caveat is that we’re not trying to prove which mechanism is “the best” here – instead, we’re just taking a look at the space from one particular technical viewpoint. There are surely other ways to define collusion resistance and other desirable properties in general (for example, one might want a mechanism that incentivizes people to be honest about their social connections). On a related note, it’ll be quite important to explore how these mechanisms behave in the absence of complete information about groups, or under more nuanced representations of groups (in our paper they’re just sets). There are other deeper questions as well, but you can find those in the paper.

Thanks for reading – let me know if you have any questions.

## Replies

**Jmiller4** (2023-01-04):

New users can only put two links in a post, [so here’s a link to the DeSoc paper I mentioned.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4105763)

