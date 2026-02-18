---
source: magicians
topic_id: 1130
title: "Core Devs agenda item: Three competing EIPs to delay the difficulty bomb and/or reduce the block reward"
author: jpitts
date: "2018-08-22"
category: Protocol Calls & happenings > Announcements
tags: [core-devs, block-reward, difficulty-bomb, issuance-rate]
url: https://ethereum-magicians.org/t/core-devs-agenda-item-three-competing-eips-to-delay-the-difficulty-bomb-and-or-reduce-the-block-reward/1130
views: 1521
likes: 3
posts_count: 5
---

# Core Devs agenda item: Three competing EIPs to delay the difficulty bomb and/or reduce the block reward

[Core Devs Meeting 45](https://github.com/ethereum/pm/issues/54)

on Friday 24 August 2018 at 14:00 UTC

A key agenda item at this Friday’s meeting is “Three competing EIPs to delay the difficulty bomb and/or reduce the block reward”:

a. [EIP-858](https://github.com/ethereum/EIPs/pull/858) - Reduce block reward to 1 ETH per block.

b. [EIP-1227](https://github.com/ethereum/EIPs/pull/1235) - Delay bomb and change rewards to 5 ETH.

c. [EIP-1234](https://github.com/ethereum/EIPs/pull/1234) - Delay bomb and change rewards to 2 ETH.

Perhaps some discussion about these proposals can occur here and the results presented and discussed further on the call.

## Replies

**atlanticcrypto** (2018-08-22):

Please include: https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1295.md

Which I’ve framed for discussion here:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/atlanticcrypto/48/688_2.png)
    [Proof of Work Incentives and Opportunistic Adjustments](https://ethereum-magicians.org/t/proof-of-work-incentives-and-opportunistic-adjustments/1105) [EIPs](/c/eips/5)



> Hello everyone,
> It’s been suggested by several folks that this is the best launchpad for a discussion on Proof of Work incentives.
> By way of background, my name is Brian Venturo, I am the CTO of Atlantic Crypto (ACC). We are a large GPU computing firm based in the US with a sizeable hardware allocation to the ETH network. Currently we represent approximately 0.2% of the global ETH network hashrate. Prior to ACC I operated a systematic fundamental US energy commodity hedge fund, specializing in…

---

**AtLeastSignificant** (2018-08-22):

I want to chime in on the issuance/difficulty bomb/ASIC resistance discussion just so that these perspectives are out there and can hopefully be discussed in the call.

---

The way I see it, issuance is not the same as miner incentive.  That means that tweaking issuance only has a limited ability to impact security because price is an independent variable in the mining profitability equation.

We should assume all miners are immediately cashing out at spot price. If they are not, then they are now investors/traders in addition to being a miner, and we should not make protocol design choices to cater to investor profitability.  This means that “miner profitability” is with respect to current prices right now, not in the future or an average over time.

There is no guarantee that increasing / decreasing issuance will have a meaningful impact on price, especially over longer periods of time.  We could make the reward 5ETH, and miners may still struggle to be profitable if prices drop.  We could decrease it to 1 ETH and they may be *more* profitable than ever in just a few months. This number simply does not determine how profitable a miner is.

The long-term issuance rate will be determined by the long-term issuance model, which as I understand is not going to be under PoW.  The PoS issuance rate can be much lower due to a reduction in cost to actually run the network, and it will have to be readdressed in the future when the change to PoS happens.

Ultimately, the only reason I have against changing the issuance rate is simply because I don’t think the current one is broken.  Don’t fix what ain’t broke.  Every “changing it to X will do Y” argument I’ve seen is entirely speculation that usually has historical evidence against it.

---

With respect to the difficulty bomb - I don’t see how it’s a viable option to *not* delay/eliminate it.  I’m in favor of simply delaying it because there is precedent for that change.  Eliminating it does nothing but benefit old-chain supporters, which I don’t think is something we want to encourage even if having the difficulty bomb doesn’t do us much else.

---

ASIC resistance needs to be a part of this discussion because the majority of people are only interested in this topic because of miner profitability / network security.  I do not believe we have sufficient data on how many “above optimized GPU miner” systems are on the network, and there appear to be newer, more ASIC-like systems coming out like the Innosilicon A10.

When I think about security risks, an attacker has a huge advantage in terms of knowledge.  They know when they have 51% of the hashpower, and I don’t think it’s impossible for the rest of the network to be largely unaware.

Ultimately though, I’m less concerned about a network attack and more concerned about a decision to not pro-actively *try* to address this problem.  ASIC-resistance is a fundamental property of the Ethereum network, I don’t think that can be denied.  I’m more in favor of making a change that has little impact than not making one at all, because that at least shows that we are willing and capable of combating future ASICs.

---

**atlanticcrypto** (2018-08-22):

I agree with [@AtLeastSignificant](/u/atleastsignificant)’s assessment of everything.

The only thing we know for certain is that the payment for securing the network will ALWAYS be incorrect. When you pair the current issuance profile with hashrate growth, it is still in an effective deflationary environment - during deflationary growth periods I do not believe the issuance profile needs to be adjusted greatly.

I warn against using the 6 month price response following the last block reward reduction from 5 to 3 as a supporting argument - this was a coincident path - not a correlated or caused path.

---

**atlanticcrypto** (2018-08-23):

Presentation supporting EIP-1295 (UNCH block reward, reduced Uncle rewards) can be downloaded here:

https://drive.google.com/file/d/15n7Vur8wwlfDK6ZXwohUc95rXOUIXo7j/view?usp=sharing

