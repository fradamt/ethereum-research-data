---
source: ethresearch
topic_id: 2257
title: "Highlighting a problem: stability of the equilibrium of minimum timestamp enforcement"
author: vbuterin
date: "2018-06-15"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/highlighting-a-problem-stability-of-the-equilibrium-of-minimum-timestamp-enforcement/2257
views: 5120
likes: 9
posts_count: 10
---

# Highlighting a problem: stability of the equilibrium of minimum timestamp enforcement

Many algorithms, especially PoS but ultimately PoW as well due to difficulty adjustment, rely on messages to be broadcasted at particular times, and so the protocols tend to enforce a rule that if a message, implicitly or explicitly, specifies some timestamp T, then another node will not process that message until the node’s local clock reaches T, or possibly T+k for some k (~2 hours in the case of bitcoin). Question: is the rule that, if a node receives a message with intended time T, at local clock time T’ < T, it should ignore the message until its own local clock time reaches T, a game-theoretic equilibrium?

Clearly, at the extreme where clock time disparity and network disparity are zero, it is, because the time a message was sent is common knowledge and so it can be thought of as a tag attached to the message itself. But what if there are perturbations in both cases? Clearly, if one node perceives that its clock is earlier than that of *every* other node, it will likely have the incentive to adjust its clock forward to match everyone else’s, and if a node perceives that its click is later than that of everyone else, it will similarly want to adjust backward. Such a clock homogenizing force seems by itself benign.

But are there possibly less benign incentive effects that could show themselves? For example, what if it’s the case that, in some particular chain-based PoS algo, a node has an incentive to accept and process blocks ~100 milliseconds before it’s supposed to accept and process them, because of some asymmetry in waiting too early versus waiting too late, and *every* node has this incentive? Then, every node will start accepting blocks 100 milliseconds earlier, and at that point a node will start having the incentive to accept and process blocks 200 milliseconds before the intended time, and so on and so forth. And once everyone’s used to adjusting 100 milliseconds per day, some nodes will start anticipating everyone else’s *changes* and will start adjusting 200 milliseconds per day. Could small perturbations like this over time cause the equilibrium to eventually unravel and lead to no timestamp enforcement whatsoever?

This seems like the sort of thing that there has not yet been sufficiently formally modeled or researched, and could benefit from more such research.

## Replies

**zack-bitcoin** (2018-07-19):

Currently in Ethereum the difficulty of the new block depends on the timestamp.

It is a step function every 10 seconds.

The step function is too steep at the disconnect, it is causing this problem you describe.

If we use a connected function instead, it would fix it.

There is a maximum slope which we cannot exceed, this is easy, the max is very steep.

There is a negative side effect.

If the difficulty depends on the timestamp continuously, then mining pools earn more profit by updating their timestamp more frequently. So this would over-reward the biggest pools.

A possible solution is to keep a stair-like shape where 9 seconds is flat, and 1 second slopes upwards.

This way mining pools that only update their work once per 10 second period will have a smaller disadvantage.

---

**nootropicat** (2018-07-23):

> Question: is the rule that, if a node receives a message with intended time T, at local clock time T’ < T, it should ignore the message until its own local clock time reaches T, a game-theoretic equilibrium?

Yes, as enforcement by nodes (esp. exchanges’) clearly works for bitcoin. Without the 2 hour rule bitcoin would now be in the year 2060+

---

**rcconyngham** (2018-07-29):

For PoS, clearly, we do not need to add the timestamp, rather the implicit timestamp given by number of blocks and number of skips should be the measure of choice. What does a node gain or lose when it changes the rule of when to accept a block by \Delta t, where \Delta t can be positive or negative?

As far as I can think, there are two effects of this on the rule-changing node, one positive with \Delta t positive in \Delta t and one negative:

- On the positive side, a node may be able to see into the future if other nodes start broadcasting their blocks early. Of course this is only relevant if other nodes actually do this.
- On the negative side, the node risks following a chain that later turns out not to be the main chain, because someone made a “long skip extension” of the main chain. However, this could easily be remedied by the node implementing a new rule: Only follow extensions of the chain up to \Delta t that would have been the main chain at the real time t, where the extension has a small number of skips.
- Finally, a second negative in the case where a node also broadcasts blocks early would be that it would miss out on transaction fees for not collecting the maximum number of transactions it could have collected.

From these effects, it seems that for a single node, there is very little to gain for changing the rule, but losses can also be kept at a minimum by also implementing stricter fork choice rules for chains between t and t+\Delta t.

However, what happens if a fraction f of nodes decided to break away from the rule (this could happen through an particular client implementation changing the rule, intentionally or unintentionally)? They would clearly only get any advantage among them if they also publish blocks early.

- In the pure RANDAO case (RNG exploitability analysis assuming pure RANDAO-based main chain), they would get the advantage of seeing the entropy slightly earlier than everyone else, if one or more of the next blocks are produced by the fraction f. This by itself probably does not translate into a direct monetary advantage, unless there are lotteries going on using this entropy. In fact, if level 2 contracts make use of beacon chain entropy, then this might encourage nodes to this behaviour. Maybe we need a rule to not use beacon chain entropy to decide anything in contracts? That would probably require making the beacon chain entropy itself inaccessible from inside the EVM, not sure if that’s possible, but feels like it could be.

Another way this fraction could use this lookahead feature is to exclude other validators not participating in the scheme. In this way they could probably execute an uncoordinated 51%-attack on the chain, similar to [RANDAO beacon exploitability analysis, round 2]. However they would be able to get lucky “runs” before reaching the critical 36%, forcing other nodes to adopt the new rule. I think this would be the scenario to be worried about. [Interesting follow-up: Analyse at which level this pressure would become a relevant factor]

In a vdf based RANDAO, the advantages would be different:

- If there is a small fraction with a “small” lookahead, they would mainly get the advantage of being able to start the vdf computation before everyone else, and so would get the vdf rewards if one of the rule-breaking nodes is the last entropy contributors.
- If there is a larger fraction, they may be able to get vdf results before the rule-following main chain has arrived at the vdf input. As long as the fraction f does not coordinate, this probably will still not allow manipulation of the entropy, so in the vdf case, the rule-breaking is overall more harmless. But this situation might also warrant more investigation on whether it lowers the overall security of the beacon chain.

---

**rcconyngham** (2018-07-29):

> Only follow extensions of the chain up to Δt that would have been the main chain at the real time t, where the extension has a small number of skips.

In order to be safe that their chain will very likely be the main chain when the general network catches up, the number of skips allowed here can actually be 50%. So nodes implementing the new rule would follow chains if 1. They are extensions of the main chain, where the main chain is defined as the chain that would be the main chain if only blocks up to time t are considered and 2. The extension has less than 50% skips. [This fraction changes if skips get a longer time constant than blocks]

![](https://ethresear.ch/user_avatar/ethresear.ch/rcconyngham/48/2570_2.png) rcconyngham:

> However they would be able to get lucky “runs” before reaching the critical 36%, forcing other nodes to adopt the new rule. I think this would be the scenario to be worried about. [Interesting follow-up: Analyse at which level this pressure would become a relevant factor]

Adding a bit of meat to this:

Since they are not coordinating, the 36% is incorrect and the actual 51%-“attack” (where the chain of those not obeying the rule and implementing the changed rule will outrun the other nodes forever, whilst the other nodes will still follow their chain) will only happen at >50%.

But significantly earlier, the nodes adhering to the original version of the rule will feel signtificant economic pressure to also follow the new rule.

We can analyse this by looking at all the skip chains the non-rule followers will likely build. For any given length L, this can happen for chains where

- Both the first and the last producer are in the fraction f (the first needs to be to “get ahead” of the chain, the last needs to be in order to build a chain of length L
- For all prefix segments of the chain, at least 50% of the producers are in the fraction f (because using this rule, they will not follow chains that have more than 50% of skips for fear of running the main chain. The “attack”  is not coordinated, so this has to apply to all prefix chains).

This does not turn out to be accessible to a direct analytic solution, but I wrote a little python program to simulate it (see below).

[![timing_skip_chains](https://ethresear.ch/uploads/default/original/2X/1/19157213976b44c9d63db25e82fac39ab8377eb2.png)timing_skip_chains388×252 9.91 KB](https://ethresear.ch/uploads/default/19157213976b44c9d63db25e82fac39ab8377eb2)

As we can see, up to a fraction of f<0.2, it seems to be enough to consider chains up to length 10. If we take 1% as the percentage at which a loss becomes economically relevant to the rule-following nodes, this would be reached when around f\approx 0.15 of the nodes implemented the new rule. Then we would probably see more nodes breaking away and following the new rule.

```
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

def iterate_all_chains(max_length):
    for l in range(1, max_length + 1):
        for i in range(0, 2 ** l):
            yield ("{0:0" + str(l) + "b}").format(i)

def greater_equal_half_ones(chain):
    number_of_ones = len(filter(lambda c: c == "1", chain))
    return 2 * number_of_ones >= len(chain)

def iterate_all_valid_skip_chains(max_length):
    for chain in iterate_all_chains(max_length):
        if chain[0] == "1" and chain[-1] == "1":
            if all(greater_equal_half_ones(chain[:i]) for i in range(len(chain))):
                yield chain

def skip_chain_probabilities(f, max_length):
    ret = defaultdict(float)
    for chain in iterate_all_valid_skip_chains(max_length):
        number_of_ones = len(filter(lambda c: c == "1", chain))
        number_of_zeros = len(chain) - number_of_ones
        p = f ** number_of_ones * (1 - f) ** number_of_zeros
        ret[(len(chain), number_of_zeros)] += p
    return ret

def skip_chain_expected_loss(f, max_length):
    probabilities = skip_chain_probabilities(f, max_length)
    ret = 0
    for k, p in probabilities.items():
        l, skips = k
        ret += p * skips / l
    return ret

x = np.arange(0,0.2,0.01)
y = [skip_chain_expected_loss(f, 10) for f in x]
y2 = [skip_chain_expected_loss(f, 15) for f in x]

plt.plot(x,y, label="Expected loss maxlen=10")
plt.plot(x,y2, label="Expected loss maxlen=15")
plt.legend()
plt.show()
```

---

**rcconyngham** (2018-07-29):

In summary, this probably means the timestamp rule as suggested a saddle point rather than a stable equilibrium for the pure RANDAO.

---

**vbuterin** (2018-07-29):

What about attestation-based Casper FFG, where the chain alternates between blocks and attestations approving them, using something like GHOST as a fork choice rule?

I have an intuition that because there are so many actors participating all at once, there’s no gain to making a block earlier unless you can get an entire committee to collude with you, suggesting ~33-50% robustness, but would be good to check this.

---

**rcconyngham** (2018-07-29):

Do you mean the scheme defined in [[Attestation committee based full PoS chains, version 2](https://ethresear.ch/t/attestation-committee-based-full-pos-chains-version-2/2427)]?

---

**vbuterin** (2018-07-29):

Yes. At least, that’s one of the possible schemes.

---

**rcconyngham** (2018-08-02):

For the attestation committee case, we can first look at the probability that a fraction f can produce a block, for which they need SSize/2 attestations of the parent block.

Assuming that SSize is large (\approx 100  - 1000), this probability is sigmoid-like in the number of attesters available in the fraction f:

- After 0 skips, the probability is \approx 0 for f1/2
- After 1 skips, the probability is \approx 0 for f1/4
- After 2 skips, the probability is \approx 0 for f1/6
- After 3 skips, the probability \approx 0 for f1/6

and so on. So to produce blocks after s skips, the fraction implementing the new rule must be greater than 1/(2s). If it is smaller than that, the probability of being able to produce a valid block will be very close to zero; however, producing a valid block is not enough, it will also have to be accepted as the main chain.

**1st case: Fork choice = longest chain**

In order to produce the longest chain, the nodes in f cannot allow to have skips of length >1, as the main chain would almost certainly outrun their chain. So the interesting chains that the rule-breakers can produce are XOX, XOXOX, XOXOXOX, etc. where X is a block produced by someone in the fraction f and O is a skipped block (supposed to be produced by the remaining nodes). This chain has a 50% chance of winning against the “slow” chain, which will be of the same length (XXO vs XOX, XXOXO or XOXXO vs. XOXOX, etc.), depending on which of these chains the next block producer will accept as their head.

- Nodes from the fast chain fraction f will lose 50% of their validator rewards (other than the ones voting for the first block), as their chain will lose 50% of the time
- The remaining nodes will lose 3/4 of their rewards when the fast chain wins, and 1/4 of their votes when the slow chain wins, so in expectation also 50% [this is because, after every second block, with probability 1/2, they will consider the fast chain their head, meaning that they will attest the fast chain 1/4 of the time].
Overall, this only creates more side chains and nodes implementing a rule change will lose just as much as other nodes.

**2nd case: GHOST**

In GHOST, the case is pretty hopeless for anyone skipping ahead. If we analyse the chain XOX above, once the “slow” chain has produced XX everyone on the slow chain will  attest to it, as it is the head and the skip block is not yet valid for the slow validators. Then there would be one skip as the third producer has already produced its block on the fast chain; but at XXO (if I understand the fork choice rule correctly, see my question under [[Attestation committee based full PoS chains, version 2](https://ethresear.ch/t/attestation-committee-based-full-pos-chains-version-2/2427)]), the slow chain attesters would still all consider XXO to be the valid chain (because more have already attested to XX compared to XOX, so the other attesters should consider this the valid head). So they would still vote for XXO and not XOX. So unless f are already in the majority, their chain will not become part of the main chain if it has skips.

**3rd case: Slow GHOST**

The extreme resistance against a fast minority suggests that maybe there is an advantage to be gained for being slower than everyone else.

So what happens if a fraction f instead delays their own attestations, ignoring blocks up to t-\delta t where t is the real time?

Assume that the main chain skips one of their blocks, producing the chain XOX. This chain would have S(1-f) voters attesting for its last block. The slow chain XX would get Sf votes. However, once the time for the third block arrives, as long as f<1/2, even the slow attesters should agree that the XOX-chain has more votes for it, thus changing their head to the fast (normal) chain. The slow chain would not get attested.

**Does recursive proximity to justification as fork choice rule change the game**

For the definition, see here: [Immediate message-driven GHOST as FFG fork choice rule](https://ethresear.ch/t/recursive-proximity-to-justification-as-ffg-fork-choice-rule/2561)

- f with faster time: XXO from above would get S(1-f) votes from the second slot, whereas XOX only Sf votes from the third block. [I assume that only attestations in the same slot and not from later slots would count toward justification]. The chain would therefore lose
- Same thing happens if f slow down their clocks

In conclusion, I currently think that the attestation committee approach makes changing the clock away from the majority,  even with special fork choice rules, a bad strategy.

What we haven’t looked at show this could change with a distribution of clock skews/network delays. It’s well possible that this will favour some deviation from the network mean time.

