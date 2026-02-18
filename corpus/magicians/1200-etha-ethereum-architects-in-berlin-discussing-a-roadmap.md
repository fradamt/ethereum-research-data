---
source: magicians
topic_id: 1200
title: "[EthA]: Ethereum Architects in Berlin. Discussing a Roadmap"
author: Ethernian
date: "2018-08-30"
category: Working Groups > Ethereum Architects
tags: [roadmap, berlin]
url: https://ethereum-magicians.org/t/etha-ethereum-architects-in-berlin-discussing-a-roadmap/1200
views: 1033
likes: 3
posts_count: 5
---

# [EthA]: Ethereum Architects in Berlin. Discussing a Roadmap

Hello guys!

I have spent some more days to realize how we could go forward, here are my ideas.

Any feedback is welcome. If you are in Berlin on 05-11.09.2018 let me know - it would be great to brainstorm in person.

I see two huge topics we can start with:

1. Book of Ethereum Reference Architectures and Design Patterns
2. Organize a EIPs in a meaningful way.

Both topics are much needed for community and for ethereum adoption. Although final goal is very unclear at the moment, I could imagine a way forward:

**(1) Starting with List of Architecture:**

I would propose to start first with simple list of links to possible architectures or reference solutions.

For somebody, who looks for suitable architecture it will be useful even in this simplest form. An author of the architecture description or an author of the reference implementation will have an incentive to include a reference to his work into the list. Looks like we have a good case for TCR (token curated registry) here.

Once we have collected dozen of entries in our list, we will see an internal structure of the list and organize it in better way, compare entries, introduce metrics and so on.

**(2) Organizing EIPs:**

Here I would start to create a labeling (tagging) structure for categorizing EIPs with. It should help to group and categorize them quickly. I have already few tags in mind (here is verbose naming):

*[DESIGN_PATTERN vs. ETHEREUM_CHANGE]:*

there are a lot of EIPs, that are not “Ethereum Improvement Proposals” (EIP) actually, but “Design Patterns” (DP).

DPs do not need a community consensus and do not change a protocol. DPs do not need much attention of entire community.

EIPs do require community consensus and need to be reviewed almost by anyone.

This label helps to filter out “must-read” proposals from “nice-to-have read”.

*[IMMUTABLE STANDARD]*:

this label should mark a standard, which can be adopted without consensus, but once adopted, can’t be changed any more easily. Example: ERC20. It is an interoperability standard. Trying to change it will create a mess between old and new tokens on exchanges.

This label marks a proposal requiring broad and comprehensive discussion, but does not change protocol.

*[HARD_FORK]*: proposal can lead to hard fork.

marks dangerous EIPs that requiring community consensus.

Incentivization of the labeling work is not quite clear to me yet.

======

Any feedback is welcome. If you are in Berlin on 05-11.09.2018 please drop me a message.

## Replies

**apitkevich** (2018-08-31):

Speaking about architecture I would start from the list or map of the services like:

1. Infrastructure services
2. Core services
3. Integration services
4. Data services
5. Presentation services
6. Administration/Operation services
7. Development services

It’s kind of self explanatory but very high level. Thank I will try to detail it further on a basis of available input:  projects, initiatives etc. It’s not necessarily that a project will fit into one item or make a complete item, but by placing it into the structure we should be able to define each item and its pieces and move to the lower levels of definition.

Having a starting list of projects we should be able to start the discussion.

---

**apitkevich** (2018-08-31):

I support the idea to create the EIP taxonomy (IMHO it’s the good word for your “organisation” term). I definitely didn’t read all EIPs  but those I saw can be placed in the structure inherited from the standard software testing methodology:

1. Requirements, Features, and Functionality Bugs
1.1 Design Pattern - seems it can be here or shape the separate top level item
1.2 Change request (ETHEREUM_CHANGE)
2. Structural Bugs
2.1 Control and Sequence bugs
2.2 Logic bugs
2.3 Processing bugs
2.4 Initialization bugs
2.5 Data-Flow bugs
3. Data Bugs
4. Coding Bugs
5. Interface, Integration, and System Bugs
5.1 External Interface Bugs (UI)
5.2 Internal Interface Bugs (API)

Those I would park for a moment as I never seen EIPs on these topics

6. Test and Test Design Bugs

7. Testing and Design Style

In parallel with this EIP “content” based structure I’d create the multiple dimensions of other classifications like

Importance: must_read vs nice_to_read

Realization: where your HARD_FORK belong

So for me it’s multiple dimensions classification where each dimension can have either list or tree-like structure. IMHO tagging doesn’t really support this as it has no limitations and not forcing a structural thinking… being not centrally controlled it can easy create a mess: you will have tags but won’t be able to structure the EIPs well:  simplest example - it’s technically possible to tag EIP with two tags must_read & nice_to_read simultaneously. Also tagging is not mandatory and I guess it would be beneficial for some parts of our taxonomy to force the value provisioning/correct structure right at the beginning, while EIP is created.

Hope it make sense…

---

**Ethernian** (2018-08-31):

thank you for your detailed posts, [@apitkevich](/u/apitkevich)!

> I support the idea to create the EIP taxonomy

Some of your thoughts are still unclear to me:

- What do you mean by “bugs”? EIP deals with protocol, not with implementation. There are issues lists for particular clients like geth or parity for bugs in the software, aren’t there?
- Who is the beneficiary of your taxonomy? Why it is important to create separate groups for “logic” and “initialization” bugs? Do you see any EIP reader, who would like to read and understand all “logic” bugs, but not “processing” bugs?

---

**Ethernian** (2018-08-31):

I think it is important to keep in mind why we need a taxonomy of EIPs. Who is the beneficiary?

The goal behind my taxonomy was:

1. I don’t want to read all that “Design Patterns”. They are not EIPs at all an do not need to get my attention and attention of whole community.
2. I want to see an explicit tag IMMUTABILITY on particular EIP because can be easily overlooked.
3. I want to see a tag HARD_FORK for “dangerous” changes.

The goal of my taxonomy is to find all “must-read” EIPs and hide all “nice-to-have” ones.

