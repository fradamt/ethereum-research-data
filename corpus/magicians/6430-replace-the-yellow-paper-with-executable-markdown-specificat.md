---
source: magicians
topic_id: 6430
title: Replace the yellow paper with executable markdown specification
author: pipermerriam
date: "2021-06-07"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/replace-the-yellow-paper-with-executable-markdown-specification/6430
views: 2173
likes: 35
posts_count: 17
---

# Replace the yellow paper with executable markdown specification

## Eth2 specs

The Beacon chain is currently specified using a custom format which I’ll refer to as “executable markdown”.



      [github.com](https://github.com/ethereum/consensus-specs)




  ![image](https://opengraph.githubassets.com/77b03e9e1b7dae88398023bb3cce9afc/ethereum/consensus-specs)



###



Ethereum Proof-of-Stake Consensus Specifications










The specification is a combination of high level descriptions written in markdown, and python functions embedded in markdown code blocks.  The executable nature comes from custom scripts that are used to extract the function definitions from the markdown, which are then run against the test fixtures to verify the specification is inline with the expected behavior.  The python has been written with a focus on readability and simplicity.

This format has some significant benefits:

- the python definition of the functionality is tested to be compliant with the official test fixtures.
- the executable nature means the spec can be used to generate test fixtures.
- the use of markdown and python result in a low barrier to entry to contribute to the spec.

## The Yellow Paper

In contrast, the official specification for Eth1.x is the yellow paper.



      [github.com](https://github.com/ethereum/yellowpaper)




  ![image](https://opengraph.githubassets.com/bc6d0e3e56c46bab711c83132dc0cc23/ethereum/yellowpaper)



###



The "Yellow Paper": Ethereum's formal specification










The yellow paper is written using mathematical notation and uses LaTex.  These two technology choices (LaTex and Mathematical notation) result in both a high barrier to entry for contributing to the document.  The mathematical notation also makes the document less accessible to those without an academic background.

## Replacing the Yellow Paper

I would like to formally propose we attempt to replace the yellow paper with a new specification written in the same style as the Eth2.0 Beacon chain specification.  A collection of markdown documents with embedded python functions, and the necessary scripting scaffolding to make the specification executable.

The benefits from this effort being successful could be significant.  Having a specification that is significantly more accessible for both contributing would lessen the burden currently carried by a small few.  This should result in the specification staying more up to date, as well as seeing more contributions that make small improvements to make things better defined and easier to understand.  In addition, by moving away from the less accessible mathematical notation, and towards a more accessible descriptive and code based format, we should see reduced barriers to entry for understanding how Ethereum works.  This should make core protocol development more accessible.

## How we get there

Here is my rough sketch of how this could be executed.

### Stage 0: Validate the idea

I would propose that we first validate the idea.  This would be done by taking a small and self contained chunk of functionality from the yellow paper and implementing it in this format.  Candidates for this might be:

- RLP
- the hexary patricia trie
- the POW function
- the bloom filter

For whatever is chosen, the markdown specification would need to be written and then the additional scripting scaffolding would need to be created so that the spec can be executed against whatever official test fixtures exist for that functionality.  A pragmatic approach would likely be to lift much of the descriptive text directly from the yellow paper with minimal modification, and then to make use of the existing python implementation for that functionality as a starting point for the inlined python functions.

### Stage 1: Latest hard fork

Instead of trying to backfill all historical hard forks, I would propose that we only focus on the latest hard fork.  The [Py-EVM](https://github.com/ethereum/py-evm) codebase will likely be a valuable resource, though care will need to be taken to adjust the code to prioritize readability and simplicity over the current focus on clean library architecture.

The specification would not be expected to execute any of the fixture tests that deal with fork transitions, only things fully constrained to the chosen fork.  At this stage, it should be possible to parallelize work on the spec since things like individual opcodes could be worked on concurrently by different contributors.

### Stage 2: Backfill and/or Fork Transitions

Once the spec has been expanded to cover the full fork rules for the latest hard fork, we would then need to decide whether to backfill old fork rules as well as determining how to handle transitions between different forks.

## Replies

**vbuterin** (2021-06-07):

Another option for stage 0 is to validate the idea by applying it to *future* changes. A good example for this would be the Verkle trie and/or state expiry design.

---

**schattian** (2021-06-07):

I agree that would be more friendly for non-academics to replace math notation with embedded scripts. But being the yellow paper the starting point to deeply understand the EVM I think going exactly like the beacon chain isn’t the best way to achieve a high-level architectural overview, which I think is expected. Maybe the best way to do that could be continue maintaining (or adding more) plain-english explanations.

As another advantage I think the scripts usage could provide much better consistency across notation and improve context for the reader (who can just look to the scaffold).

---

**poemm** (2021-06-07):

Here are [RLP](https://github.com/poemm/PythonYellowpaperExperiment/blob/43d6406b107033bfe2bdf8ad5b075697d0e3c8cd/ethereum_001_frontier.py#L1401) and [TRIE](https://github.com/poemm/PythonYellowpaperExperiment/blob/43d6406b107033bfe2bdf8ad5b075697d0e3c8cd/ethereum_001_frontier.py#L1592) implementations closely following the yellowpaper. This code passes VM tests and RLP tests, and executes the first ~50,000 blocks in ~8 hours. (Could go much faster if TRIE was memoized, as suggested in yellowpaper appendix D.)

[@timbeiko](/u/timbeiko) [@djrtwo](/u/djrtwo) [@matt](/u/matt), please let me know which license is best for Eth1 specs. I will change my repo to that license.

---

**matt** (2021-06-07):

I believe CC0 is the preferred license!

---

**hmijail** (2021-06-08):

Knuth proposed something called “literate programming” in the 80s, in which text for humans in markup is interspersed with source code, and both parts can be automatically extracted and processed, generating at once both publishable documents AND executables. Maybe it’d be worth it taking a look at existing tools/practices to do that kind of thing?



      [en.wikipedia.org](https://en.wikipedia.org/wiki/Literate_programming)





###

 Literate programming is a programming paradigm introduced in 1984 by Donald Knuth in which a computer program is given as an explanation of how it works in a natural language, such as English, interspersed (embedded) with snippets of macros and traditional source code, from which compilable source code can be generated. The approach is used in scientific computing and in data science routinely for reproducible research and open access purposes. Literate programming tools are used by million Th...

---

**hmijail** (2021-06-08):

More concretely, if the goal is having Markdown + Python, this tool covers it: [Literate](https://zyedidia.github.io/literate/)

(it’s just the one mentioned for those languages in the Wikipedia page - no idea if there’s anything better)

---

**chaals** (2021-06-16):

The drawbacks of python code in blocks with a few links are similar to those of the yellow paper’s primarily mathematical notation, except a different group get to feel the pain.

When I looked at the doc it said what to do, but largely missed out why, what not to do, and what the intention is. It says almost nothing about how the thing actually works, and is instead like very sparsely commented code that is really only accessible to people who have already implemented it.

That is good for testing, but not for enabling an open interoperable ecosystem of new thoughtful implementations that might lead to significant proposed improvements (as opposed to e.g. optimising for a fast square root procedure). I also think that it simplifies testing stuff already known, but doesn’t necessarily help much in testing the things that are actually hard, or subject to different interpretation

It makes for a fairly opinionated version of how it ought to be implemented - you might choose a different language, and vary small details about the code, but overall there is little in to support taking a notably different (or innovative) approach, and you need to collect a lot of code and work out what it does in your head. In many ways I think that is a disadvantage compared to the Yellow Paper’s formalisms.

---

**pipermerriam** (2021-06-16):

You make some statements here like:

> The drawbacks of python code in blocks with a few links are similar to those of the yellow paper’s primarily mathematical notation, except a different group get to feel the pain.

I will assert that these two different groups are very different in size.

- Group A: People who know formal mathematical notation and who can write LateX
- Group B: People who know markdown and python

I would postulate that Group B is significantly larger than Group A, and that the barriers to entry in joining Group B are lower than that of joining Group A.  I believe things like stackoverflow’s developer survey provide both direct and indirect support that these two things are true (Group B is larger and easier to join).  The rest of your concerns seems to be things that could be addressed or improved simply in how we write the spec.

---

**chaals** (2021-06-16):

TL;DR: I think your overall reading of my comment is accurate.

Painful details:

I think you only need a passing familiarity with mathematical notation to understand what is in the Yellow Paper. I’m a tricky test case - a human language nerd with passing familiarity for mathematical notation but not a mathematician. I don’t think you need to know anything about LateX unless you want to edit the Yellow Paper yourself.

I believe for group B you need a *good* knowledge of Python, and sufficient experience of reading it to debug large systems written in it.

I suspect that reduces the difference in group size somewhat, but don’t claim it invalidates your argument. And as you note, improvements in the way the spec gets written can have a big impact overall.

---

**pipermerriam** (2021-06-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chaals/48/1515_2.png) chaals:

> I don’t think you need to know anything about LateX unless you want to edit the Yellow Paper yourself.

I think this is one of the very significant parts that I’m at least excited to see addressed.  One of the  issues we’ve had with the yellow paper is that it is difficult to update or otherwise contribute to because only a small group feel comfortable doing so.  This new proposed format should improve that, allowing for a much broader set of contributors as well as allowing the spec to stay more up to date (historically it has had some reasonable amount of delay in being updated as we introduce new fork rules).

---

**jpitts** (2021-06-16):

Fantastic proposal, and I think that other projects will adopt it!

With this “replacement” I would propose that we also recognize that there are classes of specifications for the same tech, i.e. let’s position the YP as “formal”, and the [eth2.0-specs](https://github.com/ethereum/eth2.0-specs) and Eth1.0-specs as “practical”.

The YP has a very specialized use which is not relevant to most of the development work done in clients. However, for cases like formal verification and research its mathematical elaborations are crucial (correct me if I am wrong those who know this subject better).

I would hope that formal types of specs of the YP grade would continue to be worked on (especially for Eth2), but that it not be confused or seen as competing with the more practical, more accessible specs.

---

**pipermerriam** (2021-06-16):

Linking to recently started work on this project by the Quilt team: [GitHub - quilt/eth1.0-specs: Specifications for the Ethereum 1.0. Tracking network upgrades.](https://github.com/quilt/eth1.0-specs)

I won’t go into details on the exact design decisions they are choosing to take or what the end result will be, but in general, this project is along the same ideological/philosophical lines of what I’ve initially proposed here.

---

**CryptoBlockchainTech** (2021-06-25):

I like the idea, my only question is how this translates into Python?

![image](https://ethereum-magicians.org/uploads/default/original/2X/8/88f3d7ac619b917b87e8d2821d5dc9299e3e3915.png)

---

**pipermerriam** (2021-06-25):

There are ideological stances that the yellow paper takes which don’t necessarily have to be carried over to this new format.  We are focused on creating a technical specification and anything extraneous to that goal should be given consideration as to whether it is valuable to retain.  An objective definition of the protocol should be our goal here.

---

**Arachnid** (2021-07-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chaals/48/1515_2.png) chaals:

> I think you only need a passing familiarity with mathematical notation to understand what is in the Yellow Paper. I’m a tricky test case - a human language nerd with passing familiarity for mathematical notation but not a mathematician. I don’t think you need to know anything about LateX unless you want to edit the Yellow Paper yourself.
>
>
> I believe for group B you need a good knowledge of Python, and sufficient experience of reading it to debug large systems written in it.

Speaking for myself - I know the EVM intimately and have a passing understanding of mathematical notation; I still find the details in the yellow paper - those parts described in mathematical notation - nigh-impenetrable.

I know Python well, so I’m not the best to assess its readability by someone unfamiliar with it, but I think that it can be written clearly to easily be understood by that group - much more easily than the YP’s notation.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pipermerriam/48/65_2.png) pipermerriam:

> There are ideological stances that the yellow paper takes which don’t necessarily have to be carried over to this new format. We are focused on creating a technical specification and anything extraneous to that goal should be given consideration as to whether it is valuable to retain.

These could just be copied over verbatim in the English text, couldn’t they?

Either way, I am wildly enthusiastic about this idea. Please let’s make it happen.

There have been other attempts along this line such as the Jello paper; is it worth adopting them rather than starting from scratch?

---

**SamWilsn** (2021-07-06):

In case anyone comes here looking for it, you can find the rendered output of our specification effort here (for now):

https://quilt.github.io/eth1.0-specs/autoapi/ethereum/index.html#ethereum-specification

I ~~think~~ hope it’s quite similar to Knuth’s literate programming style.

