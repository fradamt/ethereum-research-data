---
source: ethresearch
topic_id: 14508
title: Delay Attacks on Rollups
author: augustoteixeira
date: "2022-12-29"
category: Layer 2
tags: [rollup]
url: https://ethresear.ch/t/delay-attacks-on-rollups/14508
views: 2242
likes: 4
posts_count: 3
---

# Delay Attacks on Rollups

Arbitrum has recently brought up a discussion on Medium about [Delay Attacks on Rollups](https://offchain.medium.com/solutions-to-delay-attacks-on-rollups-434f9d05a07a). In short, their post raises an important issue that affects all optimistic rollups that are based on interactive verifications, such as Optimism, Arbitrum, Cartesi, Truebit, etc.

In short, although the attack does not compromise the security of the rollups chain, it allows a well funded party to delay its finality by continuously burning collaterals for the duration of the attack.

This news could have been worrisome, since it affects several different protocols. However Delay Attacks are far from an unsurmountable problem.

First of all, Arbitrum itself has announced in their article that they know a solution to the problem. They have announced a new protocol to be published soon, which is already being implemented.

On another front, Cartesi’s contributors have also worked to tackle this Delay Attack and they have just published a solution to the issue in this [article](https://arxiv.org/abs/2212.12439).

In summary, under Cartesi’s proposal, a team of dishonest parties with `x` funds can be defeated in a single dispute by an honest player who is willing to deposit `log(x)` funds. This makes Delay Attacks impossible and sibling attacks impractical.

**References**

[Delay Attacks on Rollups](https://offchain.medium.com/solutions-to-delay-attacks-on-rollups-434f9d05a07a) - Offchain Labs, Medium.

> This article digs into the delay attack problem, and discusses how it was handled in various versions of the Arbitrum rollup protocol.
> (…)
> This is based on a technical breakthrough from the Arbitrum research team that makes all-against-all challenges feasible and efficient. This allows a single honest staker to efficiently defeat an army of attackers who have posted a forest of malicious branching assertions.

[NT](https://arxiv.org/abs/2212.12439) - Nehab and Teixeira, ArXiv.

> In this paper, we propose a practical dispute resolution algorithm by which a single honest competitor can win disputes while spending effort linear on the cost of the computation, but only logarithmic on the number of dishonest competitors. This algorithm is a novel, stronger primitive for building permissionless fraud-proof protocols, which doesn’t rely on complex economic incentives to be enforced.

## Replies

**Hyp** (2023-01-20):

Truebit already solved this problem, back in 2018 when Cartesi was first released!


      ![](https://ethresear.ch/uploads/default/original/2X/1/16e9178b5ca3ebbf39cff88e0f259591da880e0a.png)

      [Lightshot](https://prnt.sc/wTjcjK5cjSH2)



    ![](https://ethresear.ch/uploads/default/optimized/2X/5/59d23393ec8de6fe3fd60586e0280b7397151996_2_690x266.png)

###



Captured with Lightshot










https://arxiv.org/pdf/1806.11476

---

**GCdePaula** (2023-01-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/hyp/48/11161_2.png) Hyp:

> Truebit already solved this problem, back in 2018 when Cartesi was first released!

Yeah, the collaterals and slashing solution is well known! It’s currently being employed by other optimistic solutions like Arbitrum, and it addresses many issues with making the algorithms of Canetti et al. and Feige at al. permissionless, related to Sybil attacks. However, described by Ed Felten [here](https://research.arbitrum.io/t/solutions-to-delay-attacks-on-rollups/692), it has issues of its own.

The collaterals and slashing solution is orthogonal to Cartesi’s solution. In fact, a protocol using Cartesi’s proposed algorithm should also include collaterals and slashing. Rather, Cartesi’s algorithm is a new fraud-proof primitive.

First, the paper starts with the “Refereed Games” primitive of Canetti et al., where two players can prove to a computationally limited referee that theirs is the correct result of a computation. Then, using this primitive, one can extend the protocol to allow a set of `N` players to fight over the result of a computation. This way, a single honest player in the set of `N` players can enforce the correct result of a computation.

However, this does not scale well over `N`; both the number of referee interactions and the computational effort spent by honest players grows linearly, and so does the overall dispute times. Adding collaterals and slashing is a way to disincentivize attackers. (And winning parties must at least recoup the resources they spent, otherwise a well-funded attacker may exhaust an honest player’s resources.) However, this introduces attacks that can delay liveness of roughly `N` challenge periods at a cost to the attacker of `N` collaterals.

Moreover, this has centralization concerns. The choice of collateral has to balance between restricting the number of people that can participate in disputes and how feasible delay attacks are. If it’s set to zero, then anyone can participate, but one could delay finality forever. If it’s set very high, very few would be able to participate, but delay attacks would be very expensive.

The preliminary Cartesi paper introduces the “Permissionless Refereed Tournaments” primitive, which addresses the limitations mentioned above. The main contributions are the concept of a computation commitment — a Merkle tree where the leaves are the intermediary Merkle hashes of the state of a computation — and sorting validators into tournament brackets.

With this primitive, rather than dispute effort growing linearly with the number of players, it grows logarithmically. An attacker that wants to delay finality by `X`, would have to spend `exp(X)` collaterals.

And this is just on delay attacks. There are other interesting features of Cartesi’s algorithm besides that.

