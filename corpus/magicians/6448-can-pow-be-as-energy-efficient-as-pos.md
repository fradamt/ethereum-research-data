---
source: magicians
topic_id: 6448
title: Can PoW be as energy efficient as PoS?
author: kladkogex
date: "2021-06-09"
category: Uncategorized
tags: [pow, pos]
url: https://ethereum-magicians.org/t/can-pow-be-as-energy-efficient-as-pos/6448
views: 1197
likes: 5
posts_count: 15
---

# Can PoW be as energy efficient as PoS?

Lots of discussion on Twitter recently regarding PoW vs PoS.  People like Jack Dorsey from Twitter arguing that PoW vs PoS is not black vs white, for instance considering solar or places in the world where the price of energy is zero (like deserts or wind tunnels)

Here is one proposal on how PoW can be made as energy efficient as PoS.

1. Energy consumption of chips comes mostly from transistor switches (a transistor is a capacitor, and energy per switch is $ C V^2/2$ where $V$ is voltage and $C$ is capacitance.
2. Transistors essentially switch on each clock cycle, so if you need to have crypto algorithms that require fewer clock cycles and larger chip area.  In this case, energy use will be small and costs of chip design and production will be large, so energy will be a small percentage of mining costs. In the extreme case, you have a huge chip with a very slow clock and a crypto algorithm requires such a chip to run efficiently.
3. The question is, are there hardware people on this board that could help to design a chip/algorithm like that?

## Replies

**schattian** (2021-06-09):

I think specialized hardware isn’t the go-to if you don’t have any other incentive more than reaching consensus, thus you can’t depend on it to be efficient.

---

**kladkogex** (2021-06-09):

Why?

Dont people use specialized hardware for GPUs?

---

**schattian** (2021-06-09):

Yes, but GPUs aren’t result of looking for consensus.

---

**schattian** (2021-06-09):

Supposing specialized hardware is the way to reach energy-efficient consensus, then it should be distributed for all users. Otherwise, this tends to become centralized like ASICs do.

To achieve that, I think it should be motivated for more reasons than reaching consensus, that’s philanthropic, but isn’t achievable.

For example, the AES instruction set IMHO is implemented not because Intel wants users to be secure, but to improve performance of a national standard implementation (therefore, their revenue).

So I think this approach leads to a energy-efficient ASICs, which is an improve to Bitcoin if it’s possible, but certainly isn’t that aligned with Ethereum’s goal.

From the yellow paper:

> One plague of the Bitcoin world is ASICs […] Because of this, a proof-of-work func-
> tion that is ASIC-resistant has been identified as the proverbial silver bullet.

---

**kladkogex** (2021-06-09):

Well Sebastian -

I think many people will agree with you and many disagree.

ETH is becoming a way larger ecosystem than ETH yellow paper.

It just make sense to create things in compatible way even if they are different.

Many people experiment in whatever way they want and their goals are determined by their imagination.

I imagine what what Linux would turn into if Linus Torvalds would write a yellow paper for it and tell people to follow it.

Linux is just a collection of fun things that people designed.  No one really policed them.

People will do the same to blockchain. It is unavoidable.

---

**camillecorti** (2021-06-12):

I think PoW fueled by volcanoes is a pretty strong move in the ethereal sci-fi film that is our reality rn

also, Dorsey looked pretty cool on stage at the btc con in a flame colored tie dyed shirt. Bitcoin might be winning.

---

**kladkogex** (2021-06-14):

Well ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

I think blockchain community needs to adopt moderate mentality instead of separating in camps and fighting.

It is amazing how few people are willing to accept the fact that both PoW and PoS both have strong and weak sides.

---

**tyevlag** (2021-07-04):

I think whether energy consumption is an indicator that needs to be referred to. The meaning of “wasting energy” is that the cost is less than the return, which depends on the return brought by energy consumption. PoW is still young, it will have a more efficient way and a broader prospect. At the same time, I think PoS is also an abstract PoW, and energy is consumed in an non intuitive form

---

**Arachnid** (2021-07-04):

If you make a PoW ASIC that’s twice as efficient, people will simply buy twice as many of them, doubling the difficulty, until the equilibrium - where the marginal benefit of another mining farm is zero - is re-established.

---

**mass59** (2021-07-04):

That’s right for more than one

---

**ileuthwehfoi** (2021-07-04):

Isn’t this myopic focus on the efficiency of the utilization portion of the product lifecycle? This solution can reduce energy usage, but it comes at the expense of producing a product that consumes extra resources (including energy during the manufacturing stage), cannot be reused for other applications, and must be disposed of in our incredibly inefficient electronics recycling pipelines.

---

**camillecorti** (2021-07-11):

I am accepting of all blockchains. But, in the spirit of gamification: volcano v My Validator is more fun for dreamscaping. AlSo y’all put “magicians” in the forum title so I thought there was room for Fun : P I will attempt to get serious, I realize what’s at Stake.

---

**kladkogex** (2021-07-11):

It is a good question how much resources ASIC production will take, as well as its subsequent utilization. My suspicion still way less than the constant burning of energy by today’s ASICS.

I think the next step is to find someone from the ASIC design field to look at the problem (or dig into it yourself).  May be we look at it at SKALE in our free time.

---

**gcolvin** (2022-05-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/schattian/48/4081_2.png) schattian:

> So I think this approach leads to a energy-efficient ASICs, which is an improve to Bitcoin if it’s possible, but certainly isn’t that aligned with Ethereum’s goal.
>
>
> From the yellow paper:
>
>
>
> One plague of the Bitcoin world is ASICs […] Because of this, a proof-of-work func-
> tion that is ASIC-resistant has been identified as the proverbial silver bullet.

That goal was abandoned in the course of the ProgPoW fiasco, and will be irrelevant post-PoS.

