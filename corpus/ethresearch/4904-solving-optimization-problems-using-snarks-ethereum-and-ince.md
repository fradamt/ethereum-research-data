---
source: ethresearch
topic_id: 4904
title: Solving optimization problems using snarks , ethereum and incentives
author: barryWhiteHat
date: "2019-01-28"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/solving-optimization-problems-using-snarks-ethereum-and-incentives/4904
views: 5674
likes: 12
posts_count: 7
---

# Solving optimization problems using snarks , ethereum and incentives

## Abstract

So far we have used snarks for privacy and for scalability. We can also use snarks to solve optimization problems.

We provide economic rewards based upon the results of optimization. This allows competition between different optimization methods.

We take computational drug discovery as an example optimization problem and explain how we can use snarks to solve this.

We sketch a basic drug discovery DAO and discuss its limitations.

## Introduction

There are a bunch of optimization problems that take a long time to find solutions but whos solutions can be easily verified.

So what we can do is reward people for finding the best solution to a problem. This will allow us to use market dynamics

to find the best solution to complex optimization problems.

We only care about the result of the optimization we allow the market to find what is the best way to optimize this

particular problem and reward only based upon results.

Now we introduce a case study of computational drug discovery to explore further how this can be used for a specific system.

This technique can be repurposed to be used for other optimization problem.

## Computational drug discovery

The search for drug candidates can be done computationally. We have a target protein which is associated with

some disease. We want to find a drug that changes its behavior. So that we can slow/prevent the disease.

The steps of computational drug discovery are

1. Finding a small molecule which binds to our
target protein with high affinity. Such a molecule is refereed to here as a lead compound.
2. Optimizing the lead compound so that they bind more strongly to the target or has other useful properties.
3. Clinical trials.
4. Approval.

We can use computers to find the small molecules. We cannot use the EVM because the gas costs are above the gas block limit.

We can use snarks to prove that such a molecule exists and snarks have the added benefit of letting us prove a candidate has been found

that has a given affinity without revealing what the molecule is.

So naturally the next question is how do we reward people to do this?

## Possible approaches

1. Allow anyone to auction their drug candidates without revealing them. But they must reveal them in order to get the funds.
Tho there is an attack here where someone auctions a molecule that has previously been patented by someone else.
So we need to actually auction the patent.
2. If we can tokanize a drug patent we can allow people to share the work in creating new drugs.
Building upon each others work and sharing the profits. All in a trustless way.
3. We can allow drug companies to compare their drug candidates binding affinities without revealing them to
each other or anyone else.

## Drug Search Decentralized Autonomous Organization.

### Assumption / Disclaimer

Here we assume we can make an organization that holds patents and can only send all the profit

from these patents to a smart contract.

I am not a lawyer and don’t really know if this is possible but it seems that it should be.

### Phase 0: Setup

Someone finds a protein that looks like a good drug target.

They create an atomistic model of this protein. And provide a scoring rule.

Which is usually the summation of the forces between the target and the candidate.

They make a snark that optimizer use the prove they have found a candidate that

has a certain score.

Define a list of potential drug candidates (this list will have billions of entries)

each of which can be optimized a a few million other ways.

They define the `number_of_rounds` in the clinical trials and they define `clinical_trial_cost_round_i`

and `harberger_tax_rate_round_i` for each round of clinical trials.

They need to nominate

1. The patent holding organization, who will negotiate royalties for successful drugs and distribute the profits
according to a token.
2. The Clinical trial organization who will receive the money to pay for clinical trials and release the results.

We could try and do 2 trustlessly but that is work for another post. So for simplicity we just use a centralized organization.

Everyone needs to trust organization 1 and 2.

### Phase 1: Target Search

Miner use what any method they want to try and find candidate molecules.

When they find one that is above the target binding affinity they create a snark that

proves that this binding affinity is correct and publish it on chain. The snark does not

reveal the compound used.

This is so people can compare each others results and possibly save from patenting

things that are not competitive.

### Phase 2: Target Commitment

The miner who have found a compound that is below the the threshold are invited to apply for a patent for

that compound and pass that patent to the patent organization.

Once the patent organization receives the patent the miner receive `reward_finder`% of tokens as a reward for this.

The rest are reserved for people who optimize this molecule.

### Phase 3: Candidate optimization

Anyone is able to come forward and improve the binding affinity of a candidate.

They find can change `max_change` atoms in the candidate molecule and recalculate its binding affinity.

They can publish it on chain and they can get `reward_optimizer` tokens as reward.

When an optimization for the previous molecule is found there is a hard fork where each holder of the parent molecule

gets the same number of tokens in the new molecule and `reward_optimizer` are awarded to the party that found this optimization.

### Phase 4: Market selection

We want the market to select the drug candidates that have the highest probability or working.

We want this system to be resistant to market manipulation.

We only want people to own a share of the drug candidate if they are actively working to improve them.

So we use a [herbgerger tax](https://medium.com/@simondlr/what-is-harberger-tax-where-does-the-blockchain-fit-in-1329046922c6).

`herbgerger_tax_rate` is the % tax per year for the value of each token.

This tax is contributed to a fund that will be used for the clinical trials of this particular drug candidate.

After a candidate has raised enough via herbgerger tax for phase i of the clinical trials`clinical_trial_cost_i`

the clinical trials organization receives the money and begins the trials.

Most candidates should fail during the first steps here. But it is left up to the market weather to continue the trials.

### Limitations

1. We would want to use more complicated computational measurements other than just binding affinity. Such as dwell time

We can possibly do this with recursive snarks, tho the size of these proofs will be very high. But since we are already spending

orders of magnitude more computational power trying to find and optimize these molecules it should be acceptable.

1. It is possible during phase 0 to say that each the target molecule must be X Angstroms from the proteins active site.

This can be considered during phase 0.

1. We optimize only for binding affinity. We should optimize for effecting the proteins function.

The market dynamics in phase 4 should take this into account. This system incentivizes people to run experiments.

To find out information and reveal it.

1. The patent holding organization is a point of centralization

Agree, but unless we can find a jurisdiction which is happy to tokenize patents I cannot think of another approach.

1. This will lead us to only optimize a single thing the drug binding between the protein. Where as we want to optimize a bunch of other things
such as probability of absorption in the digestive system.

The patent organization can define an absorption score for each drug like molecule.

1. How do we prevent another user from defining a new drug based upon an old target compound the patenting that.

The current patent system should prevent this.

1. What about proofs under adversarial conditions. Say I find a spherical protein and we can dock it very securely inside the sphere in a place
that in neither the candidate molecule would never be able to reach.

The target proposer should be careful about this when they have a new candidate drug. They should define the active site they want to target as in no 2.

1. Patents are evil and you shouldn’t use them.

Please don’t interperate this as an endorsement of the current patent system. We are just using the incentives that we have available.

1. There seems to be no way to force people to build upon other peoples optimizations. For example for candidate A I find B that is a child of A.
But someone else finds C which is a child of B but they report it as being a child of A and cut me out of the reward.

So in order to prevent this we can require users follow the smallest number of atoms changed path. So that they will need to build upon others changes.

## Conclusion

We have introduced a method of computational drug discovery that uses ethereum, snarks and incentives.

This will allow global participation in computational drug discovery and spur the creation of

infrastructure (asic miners) similar to bitcoin, ethereum.

Further work can explore how we can use such systems to provide insurance for optimization problems that have a high probability of failing.

The current method with herbgerger tax is designed to reduce effect of market manipulation. But other mechanisms can be explored.

The area of optimization using incentives is very interesting and we hope to do some experiments.

## Apendix

### Variables

These variables need to be set

`reward_finder`

`reward_optimizer` This should be proportional to the amount optimized

`max_change` The max number of atom that an optimizer can change and still be a child of the original patent.

for i in 0:`number_of_rounds`

`clinical_trial_cost_round_i`

`harger_tax_rate_round_i`

## Replies

**vbuterin** (2019-01-29):

This could also be useful to solve optimization problems within the crypto space; one particular one is calculating matchings for combinatorial order books between N assets. Could be an interesting short-term use case to prove the concept.

---

**barryWhiteHat** (2019-01-29):

So gnosis are working on this at the [moment](https://github.com/gnosis/dex-research/blob/f2694d96838f21469d5082b1d5e1a7755bd675e8/dFusion/dFusion.rst).

tl;dr They basically let a bunch of people “bid” for how to execute orders. The select the bid with the “best price” for everyone and then anyone can deposit a bond and force them to prove their matching via snark.

[@josojo](/u/josojo) please correct me if my tldr is not correct ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**josojo** (2019-01-29):

[@barryWhiteHat](/u/barrywhitehat)

Yeah that sounds right. We are working on this, since we believe in the benefits of having a fully decentralized trading protocol.

I really like the idea of dao’s owning patents ![:heart_eyes:](https://ethresear.ch/images/emoji/facebook_messenger/heart_eyes.png?v=9) . Cool post.

Though there are a lot of challenges. To my knowledge, the computer search can only take care of some key-features, but there still needs to be a lot of optimization later in the labs afterward. Probably, the DAO would only be able to take care of a small fraction of the whole process.

---

**oliverbeige** (2019-01-29):

This sounds like a pretty neat setup to run a decentralized Netflix prize.

---

**tvanepps** (2019-01-29):

what do you mean by Netflix prize?

---

**oliverbeige** (2019-01-30):

It was the competition that spurred the renaissance of machine learning, in large part bc it brought computer scientists and statisticians/econometricians, which had previously been at cross-purposes, together to solve a problem.


      ![](https://ethresear.ch/uploads/default/original/3X/4/d/4d675e5a67e39a8224c80ad13679c1ac73d41f10.png)

      [Thrillist – 7 Jul 17](https://www.thrillist.com/entertainment/nation/the-netflix-prize)



    ![](https://ethresear.ch/uploads/default/optimized/3X/6/6/66b3ada83c72b9f6af816dae220bd7bb376c03df_2_690x460.jpeg)

###



Inside the race for the prize.

