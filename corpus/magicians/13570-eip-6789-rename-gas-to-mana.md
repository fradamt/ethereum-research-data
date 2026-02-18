---
source: magicians
topic_id: 13570
title: "EIP-6789: Rename `gas` to `mana`"
author: pcaversaccio
date: "2023-03-27"
category: EIPs
tags: [gas]
url: https://ethereum-magicians.org/t/eip-6789-rename-gas-to-mana/13570
views: 4598
likes: 72
posts_count: 23
---

# EIP-6789: Rename `gas` to `mana`

I would like to reconsider renaming `gas` to `mana` as initially proposed by [@vbuterin](/u/vbuterin) in [EIP-102](https://github.com/ethereum/EIPs/issues/29). This thread should serve as the point of discussion ~~and I plan to write up an EIP on it soon~~ [EDIT: DONE]. The EIP-6789 proposal can be found [here](https://github.com/ethereum/EIPs/pull/6789) (PR) and [here](https://eips.ethereum.org/EIPS/eip-6789) (EIP website).

## Motivation

The underlying motivation for reviving Vitalik’s original proposal from 2015 is that we have finally arrived at the age of PoS, and given the roadmap ahead (i.e. “The Surge”, “The Scourge”, “The Verge”, “The Purge”, and “The Splurge”), I consider this moment as the last opportunity to make such a far-reaching semantic change.

## Rationale

- mana reflects the increased environmental friendliness of Proof-of-Stake;
- mana is generally understood to be ephemeral and non-transferable, which better represents the concept of gas; and
- mana is generally portrayed as renewable, while (natural) gas is non-renewable.

## Replies

**trell** (2023-03-27):

Mana doesn’t make sense for a blockchain with fees. Gas does. Gas gets spurted out, wasted, never to be seen again by the user. Gas is a resource that you have to go out and collect to gain more of (buy more ETH). Mana is generally a property that recharges. The user who spends mana, regains that mana with time.

---

**Vectorized** (2023-03-27):

Technically, gas is renewable with stuff like biofuels.

And I think everyone has already put comments like “this saves 32 gas”.

And all the tooling use “gas”.

Renaming now will lead to more confusion.

This might protect some jobs from AI. But I think we’ll have enough protection with the upcoming EIPs.

---

**fewwwww** (2023-03-28):

I agree with the idea that renaming leads to more confusion.

This was less of a problem when Vitalik proposed it, but it’s hard to change the terminology now. This means that all teaching materials, official documentation, or blog posts would need to be corrected.

Some recent examples I’ve seen of misuse of the terminology include ETH2.0 (which makes it look like an “upgrade”) and ZK Rollup (Validity Rollup). I feel that these examples are similar to the gas example in that they are harmless misuses that don’t have to be fixed since they are widely spread. Besides, gas is a very common word in everyday use, which makes it even more resistant to correction.

---

**relyt29** (2023-03-28):

I like gas as a term, because it allows me to describe to novices using the following analogy:

In Ethereum, how much computation the transaction can do is like how far the car can drive: how many gallons of gas you put in the gas tank is like how many units of gas you put in the `gas limit`, and the price per gallon you pay at the gas station to fill your car is the `gasPrice` or nowadays the `maxPriorityFee + maxBaseFee`

Mana has no equivalent. People will not just instantly understand mana, as nobody uses mana in their day to day life, in the same way that many people use gas and cars in their day to day life.

---

**Amxx** (2023-03-28):

Among the many things in the Ethereum glossary, gas might be one thing that people actually understand (or think they understand).

Do we really want to change the nomenclature and create confusion on the one thing that people actually understand. Do we really want to make all tutorials and vulgarization material outdated ?

IMO, that is not how we go toward adoption.

---

**pcaversaccio** (2023-03-28):

ChatGPT argument (for the sake of completeness):

> “Mana” is a term that has been proposed as an alternative to “gas” in the Ethereum network, and it has several advantages over “gas.”
>
>
> Firstly, “mana” is a more intuitive term for users. In Ethereum, gas is used to pay for computational resources required to execute a transaction, but for many people, the term “gas” does not immediately evoke this meaning. In contrast, “mana” is a more direct reference to the idea of resources or energy required for an action, which makes it easier for users to understand.
>
>
> Secondly, “mana” has a more positive connotation than “gas.” The term “gas” is often associated with something negative, such as the high cost of fuel or the harmful emissions of a gas-powered vehicle. In contrast, “mana” has a more positive connotation, as it is associated with the idea of spiritual or mystical energy. This makes it a more appealing term for users.
>
>
> Finally, “mana” has the potential to create a more consistent and standardized user experience across different Ethereum-based applications. Currently, each application may use different terms and units to describe gas costs, which can be confusing for users. By adopting a standardized term like “mana,” it can make it easier for users to understand the costs associated with different actions on the network.
>
>
> Overall, while “gas” is a widely-used term in Ethereum, “mana” offers a more intuitive, positive, and standardized alternative that could improve the user experience on the network.

---

**greg** (2023-03-29):

Irrespective of what makes sense/doesn’t make sense, I have a major concern (personal objection).

This would cause utter case all over the various ecosystem. Devtools, nodes, explorers, etc… For what it offers (a minor naming change) it has a serious amount of negative outcomes on use-ability, and would probably break so many applications.

The `gasLimit -> gas` transition took years to fully implement, and AFAIK some code bases have ugly comparators still to ensure there is no code duplicate. Which for new people entering the ecosystem would be quite an ugly mess.

AFAIK web3js/ethersjs had `if (gasLimit || gas)` riddled throughout the codebase.

---

**qizheng09** (2023-03-29):

This is not a technical issue, it’s an ecological compatibility issue. Many protocols and naming schemes were designed early on and may not be perfect, but that’s not a reason to change them directly. The networking field is similar in this regard - modifying a lower-level protocol requires support from all devices in the network. It’s not just about the protocol itself, but the entire ecosystem, so multiple factors need to be weighed and considered.

---

**fussl** (2023-03-29):

why isnt that done already?

---

**alijasin** (2023-04-01):

I feel like confusion would outweigh any potential benefit this EIP would introduce.

Fully agree with [@greg](/u/greg)’s points here.

---

**gdevdeiv** (2023-04-03):

We don’t need any more magic around here.

[EIP 102 (Serenity): Rename “gas” to “mana”](https://github.com/ethereum/EIPs/issues/29#top) was closed for a reason: no agreement was reached, because it was not needed.

“Gas” is perfectly fine. Let’s keep on walking.

---

**CrystallineButterfly** (2023-04-03):

I love this, definitely flows off the tongue better and is just much more fucking cool ![:joy:](https://ethereum-magicians.org/images/emoji/twitter/joy.png?v=12) Paying that sweet mana to enable the magic of transactions, I fully approve this change ![:owl:](https://ethereum-magicians.org/images/emoji/twitter/owl.png?v=12)![:butterfly:](https://ethereum-magicians.org/images/emoji/twitter/butterfly.png?v=12)![:owl:](https://ethereum-magicians.org/images/emoji/twitter/owl.png?v=12)

---

**zihaoccc** (2023-04-11):

what if we change ‘gas’ to ‘force’ instead of ‘mana’?

Additional rationale: ‘gas’ to ‘force’ we only need to adjust one syllable, instead of ‘mana’ has two syllables difference. Also ‘force’ can inherit all rationale from ‘mana’ above

---

**Krubot** (2023-05-27):

I think this is a potentially very confusing renaming, I not sure why others see gas as transferable while mana isn’t but the reasons for keeping things as is would be the following:

1. Changing this name causes more confusion and missunderstanding.
2. Mana has magic connotations which I don’t think fits with the rigorous culture of ethereum.

I enjoy these debates and don’t think they shouldn’t happen but this is my opinion on it.

---

**backdoor** (2023-10-21):

I think “gas” is a more commonly used word than “mana”.

Renaming gas → mana will bring a lot confusion to existing blogs/answers and reeducation.

---

**z0r0z** (2023-10-21):

I like the rename because it basically confirms network can have fun online.

---

**1m1-github** (2023-10-21):

i suggest ‘energy’

‘energy’ is the Scientific term for what ‘gas’ refers to

---

**sullof** (2023-10-21):

The term “gas” is deeply embedded throughout the Ethereum ecosystem. Even if “mana” might be a more fitting name — which is debatable — the effort required to make such a change is substantial and could lead to issues at various levels.

---

**charles-cooper** (2024-07-28):

Make ethereum fun again! Vyper has merged [feat[lang]: introduce `mana` as an alias for `gas` by pcaversaccio · Pull Request #3713 · vyperlang/vyper · GitHub](https://github.com/vyperlang/vyper/pull/3713), which adds `msg.mana` as an alias for `msg.gas`.

---

**wjmelements** (2024-07-30):

> Make ethereum fun again!

Alternative names for `gas`:

- steam (“out of steam!”)
- ammo (“out of ammo!”)
- time (“out of time!”)
- breath (“out of breath!”)
- jurisdiction (“out of my jurisdiction!”)
- focus (“out of focus!”)
- control (“out of control!”)
- hand (“out of hand!”)
- depth (“out of my depth!”)
- order (“out of order!”)
- reach (“out of reach!”)
- way (“out of my way!”)


*(2 more replies not shown)*
