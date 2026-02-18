---
source: ethresearch
topic_id: 2011
title: Staking pool using Casper (Casper-pool)
author: fubuloubu
date: "2018-05-16"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/staking-pool-using-casper-casper-pool/2011
views: 2090
likes: 4
posts_count: 8
---

# Staking pool using Casper (Casper-pool)

Could you create a staking pool using the Casper contract where the decisions made by the pool get tied to the decisions made on behalf of the pool on the main contract?

Could probably build a parameterization that would work for that pool with much smaller amounts and guarantee suitable liveness of that pool in a similar way. Might also stagger the decision making through the modulo so it’s `x mod 50 == 49` instead of 0 to ensure decisions are made one block ahead of the period so the last validation on the pool triggers the vote on the main Contract.

#randomthoughts

## Replies

**liangcc** (2018-05-16):

Hi [@fubuloubu](/u/fubuloubu),

Not quite understand the idea. Do you mean something like this?

```python
# Add this function in this pool: https://github.com/ChihChengLiang/mvp-pool/blob/master/contracts/pool.v.py
def vote_to_casper():
    assert not self.vote_history[source_epoch]
    validator_index: int128 = self.validator_index
    target_hash: bytes32 = Casper(self.CASPER_ADDR).recommended_target_hash()
    target_epoch: int128 = Casper(self.CASPER_ADDR).current_epoch()
    source_epoch: int128 = Casper(self.CASPER_ADDR).recommended_source_epoch()
    msg = RLP_encode([validator_index, target_hash, target_epoch, source_epoch])
    sig: bytes <= 1024 = somehow_sign(hash(msg))
    vote_msg = RLP_encode([validator_index, target_hash, target_epoch, source_epoch, sig])
    Casper(self.CASPER_ADDR).vote(vote_msg)
    self.vote_history[source_epoch] = True

```

---

**fubuloubu** (2018-05-16):

Yeah, that looks like the correct mechanism to vote with. So, that gets triggered when more than 2/3’s of votes are cast in a Casper-like pool?

---

**kladkogex** (2018-05-16):

It is discussed [in this thread](https://ethresear.ch/t/decentralized-casper-validator-proposal/1430)

---

**fubuloubu** (2018-05-16):

Nice!

Was trying to see if it would be possible to directly leverage the Casper Contract, reducing parameters like minimum stake and logout time, but largely the same codebase so we could leverage the audits and testing that Casper has, and also increase usage of it to discover issues sooner through multiple sub-pools.

---

**vbuterin** (2018-05-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/liangcc/48/39_2.png) liangcc:

> somehow_sign(hash(msg))

This is not actually possible. Whatever the mechanism is that’s used to make the signature, that could be simulated offline, and the result directly sent into Casper’s vote function. It’s not possible to have a voting procedure that’s stateful; this is by design.

---

**fubuloubu** (2018-05-16):

This means that any validation pool would have to be handled externally? (which could be facilitated by a contract) There’s no way to allow a validators to be a smart contract controlled by a group of accounts?

---

**kladkogex** (2018-05-16):

The validators would be using some type of an online protocol (p

robably using some type of a consensus to agree on a vote, and then using a threshold signature scheme to sign it

