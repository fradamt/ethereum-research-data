---
source: ethresearch
topic_id: 1355
title: An (impractical) idea for unmanipulable entropy
author: dlubarov
date: "2018-03-10"
category: Cryptography
tags: [random-number-generator]
url: https://ethresear.ch/t/an-impractical-idea-for-unmanipulable-entropy/1355
views: 2902
likes: 1
posts_count: 7
---

# An (impractical) idea for unmanipulable entropy

RANDAO is not ideal in that minor manipulation (controlling a few bits) is easy, albeit costly. Even if it’s rarely profitable to manipulate randomness for the block rewards, it could be helpful in setting up a single-shard attack. If nothing else, the potential for manipulation makes it harder to analyze the feasibility of attacks.

Threshold signatures make manipulation harder, but not quite infeasible. If the threshold is 51%, an attacker could conceivably DOS 50% of the network, get the others’ signature shares, privately compute the group signature, and decide whether to broadcast their own shares based on the result.

How about the following scheme? We devise some time-hard function f with an adjustable difficulty d. Maybe an iterated hash function f(x) = \text{hash}^d(x), preferably with a memory-hard hash function so that ASICs won’t have a major advantage. In any case, the computation should take everybody \mathcal{O}(d) time since it’s not parallelizable; any advantages would be limited to a constant factor.

We have each validator include a random number r in their block header. After each epoch, let’s say 100 blocks, we start computing f(r_1, ..., r_{100}). The result becomes the random seed for some future epoch, far enough out that everybody can complete the computation before then.

Admittedly this would probably introduce more problems than it solves. It would waste some computational resources, and it would become more difficult for new nodes to catch up to the network. I just think it’s academically interesting that a single honest validator per epoch can prevent manipulation.

## Replies

**vbuterin** (2018-03-12):

Yep, I suggested this exact idea in a different context [a year ago](https://www.reddit.com/r/ethereum/comments/4mdkku/could_ethereum_do_this_better_tor_project_is/). Definitely think it’s worth trying.

---

**clesaege** (2018-03-12):

Some people are working on that. The hard part is how to get the right result on chain.

[@vbuterin](/u/vbuterin) proposal is a really good idea but had some flows, it required computing the sequential hashes for each submitter, therefore requiring each participant to have one cpu per participant which would not scale well.

We can solve this by having the seed=hash(x1,x2,…,xn) in whatever order. Parties can change the seed, but cannot set it to a particular value due to preimage resistance.

An article about sequential hashing (and also modular squaring) has been published http://stevengoldfeder.com/papers/BGB17-IEEESB-proof_of_delay_ethereum.pdf , only using the blockhash as a seed (which is sufficient in PoW, as miners can withhold blocks with blockhash they don’t like, but can’t set it to a particular value) but we still need a full implementation and this proposal is vulnerable to the delay attack.

You can look at [Multiparty Interactive Verification](https://ethresear.ch/t/multiparty-interactive-verification/1221) for discussions about how to verify it while mitigation the delay attack.

RNG is really important both for protocols and apps. The RNG proposal of the yellow paper (using a low influence function) is IMO quite week as parties can collude to control it (by inputting non random values always biased in the same direction, I mean if a minority collude inputting  the same number, if the other parties don’t collude and give random values, the bit to bit vote will what colluders decided with high probability). What RNG does the fondation plan to use for POS?

---

**dlubarov** (2018-03-13):

Thanks for the links; I tried to search for prior work but didn’t know what terms to use.

Getting the result on the chain isn’t strictly necessary, right? Everyone could do the computation independently. Seems like the computational waste could be kept reasonably low since we can extract as much entropy as we want from each RANDAO++ round. For PoS with a minimum account age of 1 day, we could do RANDAO++ just once per day to prevent grinding attacks.

I think the main challenge is catching up to the network after starting a new node or discovering a fork that goes far back. We could mitigate that by pushing say 100 checkpoints on-chain, so nodes could parallelize and catch up at up to 100x real-time speed, depending on how much computational power they have.

The referee ideas could also work and your analysis looks good, but it’s like relying on SPV with fraud proofs – if you don’t validate yourself, you can’t be 100% certain that you’re on a valid branch. There’s the possibility that no referees are active; maybe they were DOS victims. It might be a stretch, but I expect most node operators would happily spend a bit of computational power to eliminate any doubt that their branch is valid.

---

**drstone** (2018-03-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> I think the main challenge is catching up to the network after starting a new node or discovering a fork that goes far back

What exactly would cause the slowdown? Would all new nodes need to recompute this function/simulate the randomness procedure? Couldn’t some opt out?

---

**clesaege** (2018-03-13):

Without a referee system, catching back is way harder, using 100 checkpoints won’t speed up the process by 100, as nodes would  need 100 CPUs to parallelize everything.

Using modular squaring could lead to a better verification speed up.

In this case, the referee system could also work to slash validators publishing incorrect randomness results.

---

**dlubarov** (2018-03-13):

[@drstone](/u/drstone) yeah, performing the calculations yourself could be optional, I just think trusting a third party’s calculation is a little risky.

If I’m the target of an eclipse attack, the attacker could feed me seeds of his choosing while cutting me off from all referees. It would become harder for me to tell that I’m being eclipsed from the honest network, since the attacker could select seeds which result in his accounts being overrepresented, making it look like the validator participation rate was normal.

The extent of overrepresentation would depend on the attacker’s computational power. We can use the binomial CDF to calculate the expected number of candidate seeds that the attacker would need to try before finding one which gives him a certain level of representation. I plugged some sample values into a [binomial calculator](http://www.wolframalpha.com/widgets/view.jsp?id=78baf4f3a070cc5b9b226664d2ce80ec), and it looks like it could be computationally feasible for an attacker with 25% stake to achieve 50-60% representation in an epoch, depending on the epoch size.

If everybody calculates the seed, the same attack could potentially still work, but we get a couple extra defensive options. E.g., I could insist on contributing my own entropy in each epoch. If the network doesn’t accept my entropy contribution, then I won’t trust any subsequent transactions until I have a chance to inject entropy again and observe the validator participation rate with the new seed.

