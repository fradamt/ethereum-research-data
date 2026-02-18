---
source: magicians
topic_id: 6000
title: ⚡️🤖, Client Diversity and Tx Censorship
author: Quentinc137
date: "2021-04-15"
category: Magicians > Primordial Soup
tags: [eth1x, mev, flashbots]
url: https://ethereum-magicians.org/t/client-diversity-and-tx-censorship/6000
views: 1238
likes: 1
posts_count: 1
---

# ⚡️🤖, Client Diversity and Tx Censorship

A short argument for why we should both condemn and include the Flashbots specification in all ethereum clients, and why the merge doesn’t make this go away.

At the core we need to ask: what happens when mining/ PoS pools have a monopoly on arbitrage, and can this lead to a 1/3 majority client split?

TLDR: >50% of hashrate is controlled by a single client that never shows up to ACD calls. Up 25% from last week. A canonical MEV client controlling that much hashrate is a weapon.

# What does the Flashbots Specification actually do?

Flashbots  implements a transaction censorship specification (so we can speak more concretely) that gives them a monopoly* on, on-chain arbitrage.

# How?

(1) adds a networking layer that functions as a private/privileged transaction pool for miners to whisper MEV bundles (arb opportunities): [mev-geth/internal/ethapi/api.go at c3303c3db5a60b12d8a324194e0337fa16e98368 · flashbots/mev-geth · GitHub](https://github.com/flashbots/mev-geth/blob/c3303c3db5a60b12d8a324194e0337fa16e98368/internal/ethapi/api.go#L2104)

(2) ignores canonical txpool unless there is zero profit margin: [mev-geth/miner/worker.go at c3303c3db5a60b12d8a324194e0337fa16e98368 · flashbots/mev-geth · GitHub](https://github.com/flashbots/mev-geth/blob/c3303c3db5a60b12d8a324194e0337fa16e98368/miner/worker.go#L1150)

There is separate software to calculate bundles, The actual client implementation footprint is very small

# What’s the problem? This doesn’t break the spec right?

```
If a block is found where the w.current.profit is more than the previous profit, it switches mining to that block.
```

![:roll_eyes:](https://ethereum-magicians.org/images/emoji/twitter/roll_eyes.png?v=15) technically, but that’s not the main problem. >1/3 miners running altered, unaudited clients built to preserve profit by exploiting unintended attack surface in the eth client spec. IS DANGEROUS, standardized MEV clients is what a stage 0 Byzantine fault looks like.

When I was asked to move the thread from CT to this forum, this client (mev-geth) controlled >58% hash power **which is antithetical to maintaining multiple clients.** I can only assume the problem is quickly worsening.

![:police_car_light:](https://ethereum-magicians.org/images/emoji/twitter/police_car_light.png?v=15)![:police_car_light:](https://ethereum-magicians.org/images/emoji/twitter/police_car_light.png?v=15)![:police_car_light:](https://ethereum-magicians.org/images/emoji/twitter/police_car_light.png?v=15)

### Are all the miners running their own implementations across multiple clients?

No, I’ve been looking for them but it shouldn’t matter because:

This means that either

(A) mev-geth client right now effectively decided if Berlin (or any other update) actually makes it on time. In which case we should fork in the changes and regain hashrate client diversity.

OR

(B) If you believe the narrative: 50% of the mining pool hired developers to upgrade and fork in the Flashbots MEV spec back into the other clients. In which case we might as well include it in the clients who do attend ACD calls (*or at least, don’t actively brand themselves as pirates and hypocrite anarchists that build authoritarian power structures to streamline exploitation*) to regain consensus share.

## Tell me how you really feel though

Ok. Forget the glaringly obvious problem that is  mev-geth controlling more client share than every other client combined or that they don’t audit their code (to my knowledge) or really write tests, w.e.

On the other hand: Most of MEV is arbitrage (which will happen anyway in any imperfect market) Flashbots is arguably better than transaction ordering auctions or PGA bots which make the network unusable in different ways.

The Merge does not fix this. This specification (private tx chan for miners + profit driven tx censorship) can still exploit PoS versions of the chain as miners colluding to censor transactions is not prevented by anything in the ETH2 specification (that I’m aware of anyway).

Does net-neutrality matter in decentralized systems? Does it matter that miners can cut in line? Does it matter that stakers could cut inline? Is it more fair when- how often you get to cut in line is based on how wealthy you already are (PoS)?
