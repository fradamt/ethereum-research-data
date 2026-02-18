---
source: ethresearch
topic_id: 8112
title: Incentive design for surviving periods of non-finality in Ethereum 2.0
author: technocrypto
date: "2020-10-14"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/incentive-design-for-surviving-periods-of-non-finality-in-ethereum-2-0/8112
views: 1060
likes: 3
posts_count: 1
---

# Incentive design for surviving periods of non-finality in Ethereum 2.0

I posed this [in the Eth R&D discord](https://discord.com/channels/595666850260713488/598292067260825641/765962506379853864), thought I’d copy it here too.

> So, the recent medalla finality issues have pointed out something interesting. If there’s a period of finality problems, and you keep producing blocks/attestations during it, as does >50% of the network, and then eventually some of the offline nodes come back online, and finality catches back up to the head, it’s my understanding under the current spec that the combined effect of so many slots being missed with 33%
>
> Alternatively, if we want a purely technical adjustment, it seems like it might be safe to just further reduce the losses of “online heroes” who eventually get finalised again after the period of interruption. Since they would still lose a little money it doesn’t incentivise majority censorship attacks, but it also doesn’t completely throw away the signal of eventual finalisation
>
>
> Another alternative for the social norm of a full on hard fork is simply to have deployed a standard, thoroughly audited contract to which people can donate during periods of non-finality which directly rewards “online heroes” proportionate to the blocks they produced and attestations they made during the finality outage. Since this is already present as a bribery vulnerability in the majority censorship attack it would serve purely as a measure of economic endorsement of the honesty of the “online heroes”. And of course this technique could be combined with the “further reduction of losses” alternative as well.
>
>
> Note that the presence of such a contract makes a hard fork technically trivial since the only value which must be updated during such a fork is the balance of the “online heroes” contract.
