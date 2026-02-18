---
source: ethresearch
topic_id: 5095
title: Looking for blockchain and ethereum related open math problems
author: martintassy
date: "2019-03-05"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/looking-for-blockchain-and-ethereum-related-open-math-problems/5095
views: 4508
likes: 7
posts_count: 10
---

# Looking for blockchain and ethereum related open math problems

Hi everyone,

I am a math researcher and an ethereum enthusiast but until now more as a hobby than as a professional activity. This could change since my university received a grant to do some Blockchain related research and I would like to use the opportunity and come up with a good proposal for the grant. Unfortunately I don’t have the necessary overview on Blockchain research to decide on suitable math problems to include. In the past there use to be https://github.com/ethereum/research/wiki/Problems to look at interesting ethereum related problems but it seems that it has not been updated in a while. My field of research are combinatorics/probability/graph theory but problems arising from number theory or geometry would work too. Could anyone advise me or direct me to more recent ressources on open blockchain math problems which could help with the proposal?

Thanks in advance!

## Replies

**Mikerah** (2019-03-06):

There’s is also this list of potential problems by the Ethereum Foundation: https://notes.ethereum.org/s/rkxpeG0ff#

Protocol Labs also has a list of research problems and has ongoing bounties for computer scientists and mathematicians. You can read more here: https://github.com/protocol/research-RFPs.

The Interchain Foundation also gives out grants for research as well. You can find more info here: https://interchain.io/research

---

**martintassy** (2019-03-06):

Thanks a lot for the ressources, I sincerely appreciate it. Hopefully I can help with one of those problems.

---

**ldct** (2019-03-07):

I am not the best person for a comprehensive answer but here are some blockchain-related combinatorics/graph theory problems I’ve seen in the past little while:

- light-client friendly shuffle: https://github.com/ethereum/eth2.0-specs/issues/563
- the plasma cash exit game is related to graph theory via Plasma Cash with smaller exit procedure, and a general approach to safety proofs
- Various designs for using RSA accumulators (https://ethresear.ch/t/rsa-accumulators-for-plasma-cash-history-reduction, Log(coins)-sized proofs of inclusion and exclusion for RSA accumulators)
- Alternative accumulator designs similar to ^
- Graph-theoretical algorithms needed for CBC e.g.: Beacon-chain friendly CBC Casper, Bitwise LMD GHOST

There are also math problems closer to cryptography e.g. I’m sure people are still on the lookout for more designs for VDFs or for SNARK/STARK-friendly hash functions, but I have less familiarity here.

---

**martintassy** (2019-03-07):

thanks a lot it’s exactly the kind of resources I am looking for.

---

**tromp** (2019-04-17):

I recently posted an interesting graph theory conjecture related to the Cuckoo Cycle Proof-of-Work at



      [mathoverflow.net](https://mathoverflow.net/questions/327172/seeking-proof-of-the-cuckoo-cycle-conjecture)



      [![John Tromp](https://ethresear.ch/uploads/default/original/3X/2/3/233b2610b6396d848c4ebb0e8043ce7418a7df03.jpeg)](https://mathoverflow.net/users/110733/john-tromp)

####

  **graph-theory, conjectures**

  asked by

  [John Tromp](https://mathoverflow.net/users/110733/john-tromp)
  on [10:42PM - 04 Apr 19 UTC](https://mathoverflow.net/questions/327172/seeking-proof-of-the-cuckoo-cycle-conjecture)

---

**MadeofTin** (2019-04-18):

Not sure if this is a direction you are looking, but this could certainly use some Maths help.



    ![](https://ethresear.ch/user_avatar/ethresear.ch/marckr/48/1636_2.png)
    [Deep dive into Current PoW Difficulty Adjustment Algorithm and a Possible Alternative](https://ethresear.ch/t/deep-dive-into-current-pow-difficulty-adjustment-algorithm-and-a-possible-alternative/5267/4) [Mining](/c/all-about-miners-and-their-behaviors/21)



> Worked with Hawkes Processes and Poisson Point Processes in the past, have been thinking along a Beta distribution however to capture second order statistics so as to have an estimator on conditional variance. From what I’ve read the difficulty adjustment is modeled after simple hysteresis and does its job well.
> I’ve found it useful to see the demand and supply side of a given resource as distributions of utility rather than a single point estimator. Not only does this make more sense, but it a…

---

**marckr** (2019-04-18):

With respect to this, I would concur with [@vbuterin](/u/vbuterin) as in the thread referenced that what works presently is quite fine, so this may not be an avenue for impactful research as pertains to changes to the core protocol.

Would love to see any experimentation, but researcher time is always valuable. I believe there are other issues that are far more pressing to apply combinatorics and graph theory to.

Let me give a think over it [@martintassy](/u/martintassy). I’ve likewise spent quite a bit of time up this alley. What areas are you specifically focused in or geared toward? Have quite a list, personally. Glad to see others intrigued by questions to apply in this space.

---

**marckr** (2019-04-18):

It is difficult as about a year ago I systematically found problems with many issues in decentralization, at least from the direction I saw it needed to go. This pertained to decentralized control, a long unsolved problem: [Witsenhausen’s counterexample](https://en.wikipedia.org/wiki/Witsenhausen%27s_counterexample).

Further, the complexity classes are often unwieldy and preclude many a voting situation, through the difference between Search vs Decision in theoretical computer science. Even many of the more interesting issues with zk-SNARKs come down to NP-intermediate in graph isomorphism.

I have written quite a bit on this privately with just a desire to bring the space forward. Even if results have seemed discouraging, it is certainly not without hope. Combinatorial auctions are very useful but have specific constraints. Blockchain complicates the matter, but I believe not too terribly much. Working on this presently.

Regardless, thanks [@Mikerah](/u/mikerah)! That’s a great list. Not sure about the bounty aspect, or if that is even a feasible way to approach compensating and/or incentivizing research units, but it’s a resource I hadn’t been aware of. I’d similarly taken the ethereum/research/wiki/Problems document as a starting ground, and then sought to apply perhaps even too much research to it. This is ultimately a very practical space, it seems. Top-down, bottom-up, two different approaches, but they’re converging.

---

**dankrad** (2019-04-22):

I might have a few interesting problems in number theory/complexity/cryptography for interested math researchers. Ping me for details ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

