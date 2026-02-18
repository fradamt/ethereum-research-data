---
source: ethresearch
topic_id: 3916
title: Casper CBC lite via committees
author: vbuterin
date: "2018-10-24"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/casper-cbc-lite-via-committees/3916
views: 3504
likes: 5
posts_count: 5
---

# Casper CBC lite via committees

Casper CBC roughly works as follows:

- Validators make messages.
- Each message specifies a block that the validator is voting on, and also specifies the most recent message that the validator received from each other validator.
- The block that the validator is voting on must be equal to or descended from the block that is the head under the GHOST fork choice rule using as inputs the other validators’ latest messages.
- The only slashing conditions are (i) the above rule, (ii) a validator cannot make two messages with the same sequence number, (iii) a validator cannot in a later message refer to messages with an earlier sequence number than the messages that the validator referred to in an earlier message.
- Finality is endogenous: at some point, when there are multiple rounds of validators voting on descendants of X, it’s mathematically impossible for the head to switch to being not-X without a large portion of validators making invalid messages. A lower bound on this amount can be detected and measured using various heuristics.

Here’s an example of the GHOST fork choice rule in action. The letters A,B,C,D,E represent the five most recent votes.

![image](https://ethresear.ch/uploads/default/original/3X/b/3/b317c2a8d25bea2ac53052a62284a1170a6aba93.svg)

The first choice is between green and yellow. Green wins because there are three votes that descend from green, and only two that descend from its competitor yellow. The second choice is between red and blue. Blue wins by 2 vs 1. Blue has only one child, orange, so orange wins.

The major efficiency issue with doing this naively is obvious: every message needs to refer to every other recent message that it has seen, potentially leading to O(N^2) data complexity.

---

This post explores one particular strategy for alleviating the data complexity. Instead of every validator’s vote being the evaluation of the GHOST fork choice rule on *every* other validator’s message, validators are explicitly assigned private committees of m other validators (likely 32 \le m \le 256), and in their messages must include a reference to the signatures of these m validators. This reference could be by sequence number, or by position in which those signatures were already included into the chain. The slashing condition can simply check that these messages actually do represent the GHOST fork choice evaluation of these m other messages, and that the counters always increment.

Stated more concretely:

- For a chain to accept a message, either (i) the message must be voting for a block in the chain or (ii) the off-chain block that the message is voting for must have been included as an uncle
- For a chain to accept an uncle, the uncle’s parent must either (i) be part of the chain or (ii) have already been included in the chain as an uncle
- For a chain to accept a message, all messages that the message refers to in its most-recent set must have been accepted.
- Every message has a sequence number. For a chain to accept a message with sequence number n, it must have already accepted a message from that validator with sequence numbers 0....n-1,.
- A validator can be slashed for two messages with the same sequence number, or for a message voting x where the evidence included in the message does not justify voting x.

If the committees are large enough, they will approximate the entire validator set, and you can heuristically determine the number of validators that will need to make attributable failures in order to illegally shift the fork choice from A to B. Here is some code that can calculate this:



      [github.com/ethereum/research](https://github.com/ethereum/research/blob/659f0b31f9337b3e7ee4bde45cdb93c0ed4fd390/graph_cbc/graph_cbc.py)





####

  [659f0b31f](https://github.com/ethereum/research/blob/659f0b31f9337b3e7ee4bde45cdb93c0ed4fd390/graph_cbc/graph_cbc.py)



```py
import random

VALIDATORS = 5000
EDGES = 255
FINALITY = 4000

assert EDGES % 2 == 1

neighbors = list(range(VALIDATORS))
edgelist = neighbors * EDGES
random.shuffle(edgelist)
edges = [edgelist[i*EDGES:i*EDGES+EDGES] for i in range(VALIDATORS)]

last_votes = '1' * FINALITY + '0' * (VALIDATORS - FINALITY)

while 1:
    new_zeroes = []
    for i in range(VALIDATORS):
        votes_for_0 = len([e for e in edges[i] if last_votes[e] == '0'])
        if votes_for_0 * 2 > EDGES:
```

  This file has been truncated. [show original](https://github.com/ethereum/research/blob/659f0b31f9337b3e7ee4bde45cdb93c0ed4fd390/graph_cbc/graph_cbc.py)










The result is that with m \approx 256, the fault tolerance seems to be close to ~20%, very close to the maximum 25% possible within two rounds with Casper CBC. Though we lose a few percentage points of safety, we gain a surprisingly simple and parsimonious representation of a protocol that may otherwise require some fairly complex data structures.

Also, note that this style of Casper CBC is fundamentally very similar to how Avalanche works, where each node gets consensus by polling a committee of other nodes. The main difference here is that the committee is selected by the protocol, slashing conditions enforce compliance, and GHOST is used as a fork choice rule to extend N-ary consensus to chains, achieving economic security efficiently. This suggests that there may be a more general framework that can include both Casper CBC and Avalanche effectively.

Further work:

- Casper CBC’s fault tolerance can be improved up to \frac{1}{3} - \epsilon by increasing the number of rounds that you wait. Can we use a similar technique to increase fault tolerance above 20%?
- Is there some way to make sharding happen naturally in this setup? In general, the goal would be to replace the chain with some kind of DAG, where each block is aware of the parent in its own shard and, say, the tenth most recent and older blocks in other shards, and expect validators to only full-validate blocks that have not yet been validated by a sufficiently large validator sample.

## Replies

**naterush** (2018-10-30):

> validators are explicitly assigned private committees of m other validators

In what sense is the committee private?

> in their messages must include a reference to the signatures of these m validators.

So, in practice, we need to insist theres some overlap between these committees of validators if we ever want any safety. It would probably be fine to randomly assign these committees per validator - but it wouldn’t work to split the validator set in half, for example.

> A validator can be slashed for … a message voting x where the evidence included in the message does not justify voting x.

Is the evidence included in x just the m messages that the validator commits to? Or is it the “closure” of these messages under justification? If it’s the second, then I think the current safety oracle works to detect safety.

That is - I think we can just allow validators to commit to only m other validators messages, keep the slashing conditions exactly as they are (where a messages justification is understood as the closure of the justifications that a validator commits to), and have the safety oracle detect safety without any changes (e.g. a clique of validators see each other agreeing and can’t see each other disagreeing). So “Can we use a similar technique to increase fault tolerance above 20%?” seems to be yes.

---

**vbuterin** (2018-10-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/naterush/48/4241_2.png) naterush:

> In what sense is the committee private?

Ah, I just mean that it’s a different randomly sampled committee per validator.

> So, in practice, we need to insist theres some overlap between these committees of validators if we ever want any safety. It would probably be fine to randomly assign these committees per validator - but it wouldn’t work to split the validator set in half, for example.

Agree! And with randomly assigned committees that does happen in practice.

> Is the evidence included in x just the m messages that the validator commits to?

In the model that has 20% fault tolerance, the protocol only cares about just those m messages.

> and have the safety oracle detect safety without any changes (e.g. a clique of validators see each other agreeing and can’t see each other disagreeing). So “Can we use a similar technique to increase fault tolerance above 20%?” seems to be yes.

Interesting! Immediate questions:

- What if m were lower (eg. 8), so high enough that it’s still a strongly connected graph, but not much higher?
- I take it that would imply that safety requires \approx 2 * log(N) actual rounds of communication, correct?

---

**naterush** (2018-10-31):

> What if m were lower (eg. 8), so high enough that it’s still a strongly connected graph, but not much higher?

Hmm. Making m small seems like it might have problems w.r.t. fault tolerance. Let’s say m = 8. Consider a case where there are two validators v_1 and v_2 who each have 1/3 + \epsilon of the total weight. For safety, it’s both necessary and sufficient for these two validators to see each others messages. However, consider the case where the rest of the validators in the network have a weight of, say, \frac{1}{1000000}, and v_1 and v_2 are not watching each other. If the 16 validators that v_1 and v_2 are watching go offline, then these two large validators will be unable to see each other’s messages (as they will not see any messages), although only \frac{16}{1000000} validators are offline. So: no liveness even with a very minimal number of faults.

There are two obvious potential fixes - although I’m sure both of them have second order effects I’m missing.

1. Larger valdiators watch (and are watched by) a larger number of validators. Thus, it’s harder for validators with a larger weight to be disconnected from the rest of the validators. As a side note, not having this property in the original schemes described above seems like it might be a minor centralization pressure (commit to less validators with with less addresses).
2. Allowing validators to choose some portion of which m validators they commit to. For example, imagine if validators were required to commit to m' < m validators, and the remaining m - m' validators they could chose (with some restrictions). For example, they are expected to choose the m other heaviest chains tips.

Both of these schemes might perform better in the specific example given above, but it’s unclear if they do better generally (and moreover how they perform when there are faulty nodes).

---

**vbuterin** (2018-11-11):

Ah sorry I was assuming all validator sizes are homogeneous. So large validators would be just split into many validator slots that get assigned different neighbors.

