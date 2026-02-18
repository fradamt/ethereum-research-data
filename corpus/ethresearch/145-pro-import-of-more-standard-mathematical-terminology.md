---
source: ethresearch
topic_id: 145
title: Pro import of more standard mathematical terminology
author: virgil
date: "2017-10-15"
category: Proof-of-Stake > Casper Basics
tags: []
url: https://ethresear.ch/t/pro-import-of-more-standard-mathematical-terminology/145
views: 1803
likes: 7
posts_count: 4
---

# Pro import of more standard mathematical terminology

Disclaimer: None of this deeply matters.  This is simply something that I think is a good idea, but I feel that others don’t currently appreciate its value, and I want to argue for it.

In the Casper Basics paper, there’s been disagreement about the use of two terms.

1. epoch number vs height or depth of a checkpoint
2. genesis vs root

Of these, the only one I personally care about is (1), but I think the same argument could be made for (2)—it just matters much less.

For (1), I recognize that the term “epoch number” more precisely characterizes our specific use of this object within Casper basics.  *And if someone knew no graph theory, or was not engaging with the existing mathematical literature, “epoch number” would be the superior term.*  However, we see these terms and concepts have existed in graph theory for >200 years.  For example:

- Depth: https://en.wikipedia.org/wiki/Glossary_of_graph_theory_terms#D
- Height: https://en.wikipedia.org/wiki/Glossary_of_graph_theory_terms#H

I would argue two things:

- Importing existing mathematical terms will make it easier for the academics currently outside of the blockchain space to understand and build upon our work.
- We, the Ethereum research team, gain value from using older, established terms because it embeds our research within the large number of archived results already in mathematics.  And presumably some of these existing results will be relevant to our ongoing research.  Using their same terminology will make it easier for us to pillage from the treasure trove of prior mathematical results.  Nothing would make me happier than to see some old theorem applied to our block/checkpoint to prove some counter-intuitive result.  This is a weak example, but to start I discovered this old term, Arborescence, that perfectly captures the properties of our block tree as well as our checkpoint tree.  Given the two centuries these ideas have been in mathematics, I am confident we will find more connections—perhaps even theorems about arborescent trees.  And I argue that reducing the barriers between our world and graph-theory is worth our tolerating less… obviously applicable/natural, terminology.

For (2), I recognize that the term “genesis block” comes from Satoshi and is used routinely throughout the blockchain literature.  I suppose I would say the number of citations for canonical graph theory textbooks exceeds the number of the citations of the Satoshi paper.

And we see that “genesis” is synonymous with the “root” of a rooted tree.

- https://en.wikipedia.org/wiki/Glossary_of_graph_theory_terms#R
- https://en.wikipedia.org/wiki/Tree_(graph_theory)#Rooted_tree

## Replies

**daniel** (2017-11-05):

I totally agree!

Currently I am in the position of trying to understand the current state of research in solving the scalability challenge and while there are lots of super-interesting and fascinating resources from super-smart people in the ethereum community, this trend of using new terminology for things that already have a known name in literature makes it confusing at times.

Additionally, I have the feeling that terms and variable definitions are used inconsistently, sometimes even during the same article / paper. Some general guidelines that everyone agrees with could be very helpful, I think.

---

**jamesray1** (2017-11-16):

Looks good to me, your proposals seem reasonable. I think height and depth are pretty intuitive compared to epoch number, and if there is a formal mathematical definition for such terms that are applicable, even better. The terms that you linked to all seem pretty straightforward to understand.

---

**krzhang** (2018-03-03):

I agree that this would look better to academics (like myself!). Two nuances:

- I like “root” over “genesis.”
- (at least speaking for my own experience with mathematicians, especially graph theorists and combinatorialists, and TCS people) I very seldomly hear academics say “arborescence” (despite having seen it defined this way in a few sources) I’ve almost always heard it referred to as “rooted graph (directed away from root)” or some variant. I have a feeling that sticking to words like “rooted graph” or “directed graph” maximizes intersection with the culture (which is the real goal here?), even though arborescence is correct. The latter may give some impression of “trying too hard” with the community. (probable cause: the word has too many syllables and never “stuck,” and “directed rooted graph” is easy enough to say, even if you have to specify direction)

