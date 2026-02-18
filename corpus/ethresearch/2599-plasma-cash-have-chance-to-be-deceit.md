---
source: ethresearch
topic_id: 2599
title: Plasma Cash have chance to be deceit
author: IntegralTeam
date: "2018-07-18"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-cash-have-chance-to-be-deceit/2599
views: 1491
likes: 0
posts_count: 4
---

# Plasma Cash have chance to be deceit

The problem described here is not directly related to the Plasma Cash protocol.

But because of the desynchronization of data between users and the operator, the exchange transfer speed of coins as a minimum may decrease.

To prevent the problems described in this presentation, you need to pay special attention to the security of the software that processes data in Child Chain.

More details we’ve described in our Flow presentation.

[Presentation](https://drive.google.com/file/d/1zLPvtAZi8CeH24SD6jeluBf0BbuNE9tp/view?usp=sharing)

## Replies

**rectinajh** (2018-07-19):

Good post, very detail thinking about security of the plasma cash that processes data in Child Chain. so are u have any solutions~~

---

**gakonst** (2018-07-23):

So the attack you describe is as follows (Alice colludes with Operator and Bob to steal a good from Charlie):

1. Alice deposits a coin to Plasma and gets a coin.
2. Alice sends coin to Bob by submitting the transaction to the operator.
3. Operator withholds transaction, and does not include it in the block, but still has it in hand. (At this stage Alice notices that her transaction was not included, or that information about it is withheld, and decides not to exit her coin)
4. Since the coin was not spent yet, Alice proceeds to send her coin to Charlie.
5. Charlie validates the coin history, and decides to accept the coin since its history is valid.
6. The operator creates a block which now includes the previously withheld transaction to Bob, and directly creates another block which includes the transaction to Charlie (The operator withholds the contents of the block which includes the transaction to Bob but not the block which includes the transaction to Charlie)
7. As a result, from Charlie’s point of view everything looks good, his transaction has been included and decides to

I believe the attack you describe is flawed since Alice needs to give Charlie the full coin history, with proofs of inclusion AND proofs of non-inclusion. When the Operator decides to publish the root of a withheld block, Alice needs to also provide a merkle proof of non-inclusion for that block. This does not happen in the attack you mentioned since the coin history she provided did not take the withheld block into account.

Also, you could slightly alter your transaction format by adding a `target_block` for a transaction to be included, otherwise it should be considered invalid. This disables the kind of attack where the operator saves the tx and publishes it later.

---

**KY-SmartMesh** (2018-07-26):

User cannot receive a token without verifying the entire history of the token.

The solution is a requirement.

That is, a token’s history cannot be private.

Aside of operators and users, there are validators.

The problem is resolved in the exit game process. All subsequent transactions that are initiated after an invalid state transition become invalid by default. Double triple spend is impossible. The operator does not get any benefits if it misuses the system.

This is so, since they need to have a bonded stake in the system.

The benefits of a system’s proper operation should outweigh the returns of its misuse by bad actors.

Compact proof problem can be resolved with zero knowledge or bloom filters as Vitalik said in the first video … https://www.youtube.com/watch?v=uyuA11PDDHE

Seems an inprovement of the workflow within the child chain is what you tried to address ?

