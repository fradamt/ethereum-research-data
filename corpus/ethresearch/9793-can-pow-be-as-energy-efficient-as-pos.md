---
source: ethresearch
topic_id: 9793
title: Can PoW be as energy efficient as PoS?
author: kladkogex
date: "2021-06-09"
category: Economics
tags: []
url: https://ethresear.ch/t/can-pow-be-as-energy-efficient-as-pos/9793
views: 5756
likes: 15
posts_count: 25
---

# Can PoW be as energy efficient as PoS?

Lots of discussion on Twitter recently regarding PoW vs PoS.  People like Jack Dorsey from Twitter arguing that PoW vs PoS is not black vs white, for instance considering solar or places in the world where the price of energy is zero (like deserts or wind tunnels)

Here is one proposal on how PoW can be made as energy efficient as PoS.

1. Energy consumption of chips comes mostly from transistor switches (a transistor is a capacitor, and energy per switch is  C V^2/2 where V is voltage and C is capacitance.
2. Transistors essentially switch on each clock cycle, so if you need to have crypto algorithms that require fewer clock cycles and larger chip area.  In this case, energy use will be small and costs of chip design and production will be large, so energy will be a small percentage of mining costs. In the extreme case, you have a huge chip with a very slow clock and a crypto algorithm requires such a chip to run efficiently.
3. The question is, are there hardware people on this board that could help to design a chip/algorithm like that?

## Replies

**elbeem** (2021-06-09):

Energy is consumed not only when computing POW, but also in the hardware manufacturing process. If this proposal trades one kind of energy consumption for another, how does the total energy use decrease?

---

**kladkogex** (2021-06-09):

Hey Elbeem - I think energy consumed during manufacturing process is amortized over the life time of the chip.

So in the perfect world the chip should be produced once and then work for long long time …

---

**elbeem** (2021-06-09):

Hmm, if the total energy consumption, and thereby the total cost of a chip during its lifetime is smaller than for existing POW chips, wouldn’t that just lead to mining being more lucurative, attracting more miners until the total energy consumption is the same as today? The only difference is that there will be more chips.

---

**kladkogex** (2021-06-09):

Hey Elbeem

The equation is

MiningCost + ProfitMargin = BlockBounty

OR

EnergyCost + OperationsCost + ProratedDesignCost + ProratedChipCost

= BlockBounty

OR

EnergyCost = BlockBounty - ProratedDesignCost - OperationsCost

- ProratedChipCost

Therefore, you can bring energy cost to almost zero for a fixed block bounty by tuning the rest.

Agree?

---

**nherceg** (2021-06-10):

I’m not quite sure what is the proposal here. There’s no point in designing chip that runs slower because the algorithm can always be emulated on more efficient processor.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> energy use will be small and costs of chip design and production will be large

This is in principle the same as acquiring ETH (large initial cost) and running a validator in PoS (low energy use).

---

**kladkogex** (2021-06-10):

Hey,

It is not about the chip running slowly.

Computing power of the chip is essentially clock cycles per sec multiplied by the amount of computation you do per cycle.

The point is about using algorithms that use less CPU cycles, but do more computing per cycle and use a larger computational module area on chip. These chips will be expensive to produce but cheap to run in terms of energy. So you shift the costs from energy to chip production.

---

**nherceg** (2021-06-10):

In that case, what would prevent someone from raising the clock rate of the CPU?

If I had such processor, the first thing I would do to maximize profit is increase the clock rate to the point where cooling starts to be the problem. But this means it dissipates a lot of energy and we’re back at the beginning.

I don’t think this problem can be avoided as long as computational power correlates with profit.

---

**kladkogex** (2021-06-10):

Hey

If the processing area is large, the electric signal needs time to propagate.

So clock time needs to be larger than propagation time. The larger is the area, the more time it needs to propagate.

---

**junosz** (2021-06-17):

OP may be interested in the research around Optical Proof of Work, using a hash algorithm designed to be implemented in energy efficient photonic chips that use optical switching. See: [oPoW Resources — PoWx](https://www.powx.org/opow)

As identified above, this changes the energy inputs in the PoW from CAPEX + OPEX for the ASICs + electricity to primarily CAPEX for the photonic chips up front. Other than that, as far as I can tell, it retains many of the features of current generation PoW: dependence on specialized hardware (and supply chains) plus obsolescence over time requiring continuing re-capitalization to sustain security.

---

**Mister-Meeseeks** (2021-06-17):

Are there any tasks that can only be done efficiently by humans, but can be verified efficiently by machines? If so, you could imagine a chain where PoW is done by existing humans, providing employment, rather than electricity guzzling chips.

---

**SebastianElvis** (2021-06-23):

A potential approach of making PoW energy-efficient is to make mining non-parallelisable, where each node can only use a single processor to mine and cannot accelerate mining by using parallel processors. Recent attempts include [[2010.08154] PoSAT: Proof-of-Work Availability and Unpredictability, without the Work](https://arxiv.org/abs/2010.08154) and https://eprint.iacr.org/2020/1033.pdf.

However, non-parallelisable mining protocols are vulnerable to the grinding attack, where the adversary can mine on different block templates in parallel. This is still an open challenge and further research in this area would be interesting.

---

**kladkogex** (2021-06-23):

I have been thinking about optical processing too. Switching to light totally changes energy consumption.

One question I have is how real is this optical thing - how much of an investment would one need to build a real-life network?

The authors of the paper start from an existing PoW algorithm  - it does not seem necessary to me.  It seems that the best is to design algorithm from the scratch that maximizes optical vs traditional computational efficiency.

---

**kladkogex** (2021-06-23):

No. Humans are bad at everything. There is not a single computational task at the moment that humans do better than machines.

Thats why the governments need to keep printing money do feed humans …

---

**mikeborghi** (2021-06-25):

I would argue traditional PoW fulfills that very criteria.  Human’s are the only one that are capable of implementing the technology to mine cryptocurrency and the resulting hash power is a very direct measure of how much value one brings to the market.  There is currently no better means of burning ‘real world’ resources in a way measurable to the ‘digital world’ than traditional PoW.  I doubt any human-only PoW method would stay ‘human only’ for very long as there is an extraordinary financial incentive to automate what others are not automating.

On topic, I share [@junosz](/u/junosz) interest in Optical Proof of Work systems.  I still have a bit to comprehend regarding oPoW but assuming the assertions made by the [oPoW page from powx.org](https://www.powx.org/opow) (that junosz also provided) are accurate, then it is absolutely an area of research worth investigating.  If one wishes to minimize the energy consumption for PoW they must decouple mining power with energy costs ( [Towards Optical Proof of Work - Michael Dubrovsky](https://youtu.be/-URzxEjeBu4?list=PLKCUhIiFc_PfT_9IlARL2LZmXaAIthE_n&t=75) ) which has the additional benefit of reducing the reliance on geographical differences in energy prices.

---

**kladkogex** (2021-07-11):

Any of people working on Optical PoW coming to ETHCC?

Would be fun to chat

---

**MaverickChow** (2021-07-14):

Technically, I don’t think PoW will ever be as energy efficient as PoS.

But assuming it will, someday, be equivalent in energy efficiency, PoW’s price and security are detached from each other, i.e. you can have varying price level independent from the security level.

Price is affected by market manipulation, while security is affected by hardware tech.

PoS’ price and security, however, are attached, i.e. as more and more assets are digitized/tokenized on Ethereum, higher price leads to higher security level.

---

**kladkogex** (2021-07-16):

I am not really sure it is completely true.

If you can hack lots of nodes, it does not really matter what the value of the stake is.

---

**MaverickChow** (2021-07-16):

Anything that can be accessed (by anyone), can be hacked (by others).

Bitcoin was once hacked too, with many millions of new BTC minted out of thin air, before “Satoshi Nakamoto” did a hard fork to save the day.

Everyone only talk about the Ethereum DAO hack, and argue about why Ethereum Classic is the original chain, yet nobody talk about the Bitcoin chain that is dominant today that is also not the original chain (as the original chain was hacked with multi millions more BTC minted out of thin air).

This truly reflects the bias and prejudice of human nature.

Ultimately, nothing in this world will ever last.

Even then, as long as this world is still ongoing, PoS will remain superior to PoW.

---

**cloveranon** (2021-07-21):

An example of a large chip that uses little power is an SSD or a RAM stick. You just need a PoW algorithm that scales best by adding more storage, and not faster computation. I believe this has been done by Chia coin (XCH). They call it “proof of space”. I remember not liking their particular algorithm as it requires time oracles.

---

**Mister-Meeseeks** (2021-08-06):

Has anyone has been following the crypto amendment debacle in the US Congress? One of the potential counter-proposals would drastically advantage PoW chains over PoS.

The original bill puts essentially impossible compliance requirements on any node in a cryptocurrency blockchain. There’s a good proposal (Wyden-Lummis) that would exempt that, and a bad counter-proposal (Portman-Warner) that exempt *only* proof-of-work chains. Assuming the latter passes, it might be strategically advantaged to think about how existing PoS schemes can be re-conceptualized so they include a nominal PoW component. A simple example might be a hybrid chain, where 99% of the blocks are validated by shakers and 1% are mined.

Obviously there’s some intersection of law and technology here. But assuming the worse happens and Ethereum post-merge is effectively banned in the US, it’d be good to develop a technically legal L2 or side chain solution.


*(4 more replies not shown)*
