---
source: magicians
topic_id: 2602
title: Solving the cordination problems in ethereum with a crypographic orginizational primative
author: pvienhage
date: "2019-02-06"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/solving-the-cordination-problems-in-ethereum-with-a-crypographic-orginizational-primative/2602
views: 1194
likes: 2
posts_count: 4
---

# Solving the cordination problems in ethereum with a crypographic orginizational primative

TLDR: We could use category theory to model and plan the full ethereum stack to allow distributed coordination and mathematical proofs that structural changes will improve the ethereum.

A set of problems in Ethereum Governance Right Now:

1. Many teams and researchers who are deeply focused on their own part of the system without a vision of the whole.
2. Many stakeholders create backwards compatible inertia making pushing large changes super hard. [Or even the a false inertia where things don’t change because of perceived effects on existing stakeholders]
3. The lack of communication between teams about central goals and the how what they are building will fit together. This is a transparency point as well, as new developers enter the space they have trouble seeing what needs to be built.
4. We have reached a level of scale where no person can be expected to understand everything and everyone in ethereum and thus no one can quite put their work into the whole perspective.

If not resolved these problems will become an existential threat to the ethereum project because the development will be slow and uncoordinated and we risk being so bound up by a fear of change that we will no longer innovate [a criticism many in Ethereum have of Bitcoin]. Centralized companies solve these problems by having people plan and tell other people what to do, but ethereum cannot do that and so has reached a semi choke point of a decentralized system.

What I propose is that we adopt a new mathematical/cryptographic primitive: category theoretic collaborative design. What I mean by mathematical primitive is a new piece of mathematics that we as a community both put trust in and follow. An example of this is ECDSA to guarantee that a message came from a person. In this case I think we should use the mathematical system of category theoretic codesign as a system from which we can derive planing, iteration, and “governance”.

When designing a complex system the implementation of components intrinsically depend on the implementation of other components, so how can you plan a system which has recursive feedback between its parts? This is called the co-design problem, and Andrea Censi proposed a mathematical formulation to its solution in 2016. https://arxiv.org/pdf/1512.08055.pdf In this paper he did not use the language of category theory, however he built a system which if you change the names a bit is a categorical [and highly general].

This raises another question: what is category theory? Category theory has a reputation as one of the most abstract branches of mathematics, mostly because it does math using fields of mathematics as the object of the mathematics. But at its core Category theory is the study of organization via the relationships between things, the reason it has its reputation for navel gazing is that the things that mathematicians like to organize is mathematics itself. However if presented right you will not need a math degree to understand what the category is doing [infact you may find it more intuitive than ECDSA]

The organization of a project via category theory is done by representing the project as components and relationships between components, then deciding on a way of translating that system into outcomes [Censi uses cost and functionality, but we could use more complex outcomes like ‘decentralization’, ‘functionality as sound money’, ‘minimum and average client size’ by defining the correct profunctors]. Each of the ethereum stakeholders can be grouped and given inputs and outputs in this representation and then can model their internal construction using their own category.

You might be saying: “That’s great but how is learning a bunch of math going to heard this group of cats”. This system will do a number of things, first if we agree on the category as a community then any team can orient themselves from the category and the pending changes to the category. In this way the team can make optimal choices for the ecosystem as a whole while only focusing on their own project by just plugging the results of changes to their components into the category and seeing what happens and how the feedback they introduce affects the system. This “plugging in” process would take place through a website which allows communication between stakeholders and a very visual representation of the category.

Imagine you want to introduce a new opcode eccheck which does a generic elliptic curve signature verification. In order to decide if we want to do that, what we do is estimate the extra computational cost to miners and the feedback it will have on decentralization [more miner cost means smaller pool can do it], mining code refactoring costs, and other expense factors. Then we estimate the reduction in cost for layer two snarks solutions, ring bases signature algorithms, and other cryptographic heavy applications. If we see that the added privacy and reduction in transaction costs give us an outcome point which has a better ratio [or other measure] of benefits to costs then we implement the change [or the teams which are in charge of implementing the change implement it].

The category plays an important role in this system, it gives us two things (1) a canonical product map which is a way of knowing who the changes will affect and (2) a mathematically verifiable rigorous test to see if a change will help or hurt the product [being ethereum as a whole]. We currently do all of this manually as we suggest ethereum level changes and projects, but that manual process is super squishy, non rigorous, and political. If we as a community agree to be partially governed by mathematics then we can add rigor and settle discussions quickly.

This system will not eliminate all of the human influence from governance, we will need to have human input to make changes to the canonical category and to decide between outcomes which are incomparable under our mathematics [the Pareto optimal antichain]. What it is solve the problem of orienting the whole space without centralized command structures.

Here’s a MIT lectures on applied category theory solving the co design problem https://www.youtube.com/watch?v=4Uqgsy3zrjs for a more rigorous technical definition of the problem and solution.

## Replies

**Ethernian** (2019-02-07):

Could you apply the Category Theory to this [EIP Workflow problem](https://ethereum-magicians.org/t/decentralizing-eip-workflow/1525)? Could you propose more structured solution?

---

**pvienhage** (2019-02-07):

Hi [@Ethernian](/u/ethernian) I just read your EIP workflow problem post and I think we are seeing some of the same problems and the need for optimization in the process of making changes. Which is super cool, and I do think that category theory could add a structural/ mathematical backbone to the EIP Workflow changes.

A rough proposal would be: when someone enters an EIP they identify the changes to inputs and outputs of the component they would change [or a category structural change with a transitional functor], and then if  the category shows a net increase in output it get’s a preliminary “approval”. At that point the community who is affected/ knowledgeable about those components assesses for realism and mathematical validity, these would be like the tagged groups in the EIP workflow problem. If the math is found to be right by the affected groups the change gets approved, and implemented by affected groups.

---

**Ethernian** (2019-02-07):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/p/ea5d25/48.png) pvienhage:

> A rough proposal would be: when someone enters an EIP they identify the changes to inputs and outputs of the component they would change [or a category structural change with a transitional functor], and then if the category shows a net increase in output it get’s a preliminary “approval”.

Let’s eat our own dog food.

I would like to propose the [EIP Workflow](https://ethereum-magicians.org/t/decentralizing-eip-workflow/1525) and then push it through the implementation process according the rules of the category theory.

Could you guide me through the process? I am not familiar with formalism of the category theory (like anyone else here). I do not know what are the inputs and outputs and have only qualitative understanding of the net increase.

How could I apply the theory on my problem? What should be my next steps?

Thanks in advance.

