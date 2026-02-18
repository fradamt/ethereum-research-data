---
source: ethresearch
topic_id: 5438
title: Possible to re-org without slashing?
author: adlerjohn
date: "2019-05-11"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/possible-to-re-org-without-slashing/5438
views: 1821
likes: 1
posts_count: 3
---

# Possible to re-org without slashing?

This may be a stupid question, please forgive me in advance. A common adage is that if someone tries to re-org under Casper, a minimum of 1/3 of staked ETH get slashed.

My understanding is that slashing for equivocation only occurs when a validator signs two votes at the same height ([e.g., what I read here](https://ethresear.ch/t/what-will-happen-in-casper-ffg-if-two-branches-both-get-significant-amount-of-votes/5335)) *not* if they vote for conflicting histories. What if someone executes a re-org (or a long-range attack) and carefully staggers her votes such that she only gets hit by inactivity leak, and never actually votes for two blocks at the same height, therefore never getting hit by slashing? Will the inactivity leak in this case be equal in magnitude to slashing (I don’t think it is, even remotely)? In this situation my concern is less that the 2/3 honest validator assumption is violated and more that “economic finality” doesn’t seem to hold. What did I miss?

I know that weak subjectivity can technically be used to hand-wave away this issue, but again this doesn’t help us with “economic finality.”

## Replies

**villanuevawill** (2019-05-12):

From the spec, there is slashing for surround votes:

```auto
def is_slashable_attestation_data(data_1: AttestationData, data_2: AttestationData) -> bool:
    """
    Check if ``data_1`` and ``data_2`` are slashable according to Casper FFG rules.
    """
    return (
        # Double vote
        (data_1 != data_2 and data_1.target_epoch == data_2.target_epoch) or
        # Surround vote
        (data_1.source_epoch < data_2.source_epoch and data_2.target_epoch < data_1.target_epoch)
    )
```

---

**adlerjohn** (2019-05-25):

Okay I think I may have figured it out. My mental model:

From the definition of “weak subjectivity” ([source](https://blog.ethereum.org/2014/11/25/proof-stake-learned-love-weak-subjectivity/)):

> Weakly subjective : a new node coming onto the network with no knowledge except (i) the protocol definition, (ii) the set of all blocks and other “important” messages that have been published and (iii) a state from less than N blocks ago that is known to be valid can independently come to the exact same conclusion as the rest of the network on the current state, unless there is an attacker that permanently has more than X percent control over the consensus set.

Under the weak subjectivity assumption, long re-orgs of >N blocks are forbidden. Short re-orgs are allowed, but will result in slashing as doing so would require voting for conflicting histories (surround votes).

Implementing this checking for voting for conflicting histories is bounded by N. I’m unsure how expensive this will be in practice, as the deposit length (N) is quite long and all those blocks needs to be checks against every attestation.

