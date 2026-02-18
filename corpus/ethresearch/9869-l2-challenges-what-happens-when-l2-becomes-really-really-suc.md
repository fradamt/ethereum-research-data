---
source: ethresearch
topic_id: 9869
title: "L2 Challenges: What happens when L2 becomes really, really successful?"
author: Therecanbeonlyone
date: "2021-06-17"
category: Layer 2
tags: []
url: https://ethresear.ch/t/l2-challenges-what-happens-when-l2-becomes-really-really-successful/9869
views: 2531
likes: 9
posts_count: 5
---

# L2 Challenges: What happens when L2 becomes really, really successful?

Hi Everyone,

Tas Dienes, Dan Shaw, and I have been looking at ways to help L2 adoption, particularly in the Enterprise world.

Over the course of the last couple of months, and in various conversations with people in the L2 ecosystem, enterprises and our own research have surfaced a set of key challenges that we believe may arise when Layer 2 becomes widely adopted. We would like to understand from the community if they share those concerns and what the community think could be done to address the challenges below:

1. L2 transactions could crowd out transactions from non-L2 projects because L2 projects are able to pay higher fees and require a lot more storage than non-L2 transactions. Crowding out of projects that are doing good things, but do not have sufficient capital is saying “you need to use L2”. This is basically the platform argument Facebook, Google and other Big Tech players were and are using; neither very democratic nor equitable.
2. A few handfuls of L2 transactions could quickly hit the hard gas limit in the upcoming Berlin fork (EIP1559) which would allow miners to “play favorites” and drive up fees further because with a hard gas limit, and continued high demand, fees will remain high until enough block space is either available to fulfill demand such as through Eth2 or volume will migrate to alternative networks that are still somehow anchored on Mainnet as is currently happening with Polygon experiencing explosive growth.
3. L2 projects by their very nature further concentrate TVL, increasing MEV and reducing the networks economic security guarantees; as large projects grow larger in TVL as they can pay higher network fees from higher transaction volume and value-added fees to guarantee inclusion of their blocks on Mainnet compared to other, smaller projects, leading users to abandon smaller projects for larger ones that can give higher assurances that blocks are included on Mainnet. As TVL concentrated in a small number of projects starts to significantly exceed the economic security assurances of L1, successful network attacks become more and more likely. This is like building higher and bigger skyscrapers in Manhattan until the weight is such that the ground beneath them starts to give way and they start to sink and tilt, leading to collapse unless they are stabilized by strengthening the ground beneath them – an expensive fix after the fact.
4. Often the cryptography, especially in zk-rollups, is still very new and needs more robust research before it can be safely used at a scale of potentially hundreds of billions or trillions of USD.

We believe these four challenges represent significant medium and long-term risks to the Ethereum ecosystem if not addressed, and that it would be worthwhile to have some discussion on the topic. We are very much looking forward to hearing your thoughts about those challenges and ideas how they might be successfully addressed.

All the best,

Andreas

cc [@tasd](/u/tasd)

## Replies

**pmcgoohan** (2021-06-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/therecanbeonlyone/48/6527_2.png) Therecanbeonlyone:

> L2 projects by their very nature further concentrate TVL, increasing MEV and reducing the networks economic security guarantees; as large projects grow larger in TVL…leading to collapse unless they are stabilized by strengthening the ground beneath them – an expensive fix after the fact.

Have you considered the impact that the current adoption of MEV auctions on L1 will have on L1/L2 in this scenario?

The L2 TVL doesn’t have to be greater than the security assurances of L1, it potentially only has to be greater than the highest MEV auction bid for as long as an attacker wants to delay inclusion, ie: cheap.

Competing chains (the Google and Facebooks in your example) may enter MEV auction wars where they bid not only to get their rollups included on L1 but their competitors rollups censored. If including the rollup on L1 also updates the state of contracts on L1 or other L2s (trading against some other master DEX that combines L2 DEXs for example) the incentive to do this is higher again.

Perhaps L2 may be what ends up finally demanding that Ethereum’s greatest flaw is fixed: that the right to corrupt transactional data integrity is for sale (whether GPA, MEVA or any other auction system).

In my view the solution is a distributed content layer [(an early example)](https://pmcgoohan.medium.com/how-to-fix-mev-in-one-sentence-6e4a47ef4085) that gives block content (fair tx inclusion and order) the same security guarantees as block structure: that any attacker must have the ability to perform a 51% attack and in doing so potentially has the most to lose from their attack.

Then you ‘only’ have the problem you identify of the L1 security assurance needing to be high enough.

From what I can see, for as long as transaction inclusion/ordering is for sale, the bar is way lower than that.

---

**lookfirst** (2021-06-19):

This is a great post and something that should get some attention. I really like how you point out how L2 could mess with 1559, it was a vector I hadn’t considered before.

During the recent IRON meltdown, I looked in the mempool and noticed that people were submitting transactions with whatever high gas mwei fees. The default is 1 mwei and people were at 10k+. I just looked right now and the top one is only 700 with the next being 340.

It made me realize that because gas is so inexpensive in L2 networks, it costs much less to get ahead of the queue. It is also possible to just drive the gas price up by simply outbidding everyone else, kind of regardless of what the transaction queue is looking like. An attacker would only need to saturate the network with relatively inexpensive transactions…

A long time ago people theorized that spammers wouldn’t send spam if emails cost something small like $0.01 to send. The realization being that if the spam emails still generate more than a penny in revenues… it doesn’t matter…

---

**Therecanbeonlyone** (2021-06-30):

[@pmcgoohan](/u/pmcgoohan) … this is a great insight. MEV auctions actually increase the economic attack surface than mitigate it.

Besides your suggestion, there are two other options for mitigation:

1. A trusted transaction ordering service based on for example time received and fee submitted at time of submission – wrote something about that 3 years ago … https://media.consensys.net/the-promise-of-trusted-compute-resources-a9ea72309412
2. Obfuscating the fee through partially homomorphic cryptographic predicates e.g. a Pedersen Commitment. This would allow a miner to approximate the total earned for a proposed block through a range proof without knowing the individual transaction fees. You would still have to figure out how to subtract the fee from the account the block has been formed. Might have to be that fee allocation happens in the next block using a hashed time lock contract where people need deposit an escrow for their transaction fees.

In any event, you are point out a very significant concern. Thank you for that!

---

**Therecanbeonlyone** (2021-06-30):

[@lookfirst](/u/lookfirst) … thank you for the insight. Very helpful. I think that auctions for scarce resources with asymmetrically distributed purchasing power are not the right way to go. It seems as if people made that implicit assumption that Eth is roughly worth the same for everyone. That is, of course, not the case. The cost of capital varies greatly.

We need a different mechanism to enable equitable access that avoids spamming at the same time.

