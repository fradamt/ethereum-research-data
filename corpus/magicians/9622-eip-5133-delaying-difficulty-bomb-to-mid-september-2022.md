---
source: magicians
topic_id: 9622
title: "EIP-5133: Delaying Difficulty Bomb to mid-September 2022"
author: ericmartihaynes
date: "2022-06-14"
category: EIPs > EIPs core
tags: [difficulty-bomb]
url: https://ethereum-magicians.org/t/eip-5133-delaying-difficulty-bomb-to-mid-september-2022/9622
views: 24877
likes: 10
posts_count: 11
---

# EIP-5133: Delaying Difficulty Bomb to mid-September 2022

Discussion for: [EIP-5133](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-5133.md)

(Previous discussion [here](https://ethresear.ch/t/delaying-difficulty-bomb-to-mid-august-2022/12762/))

## Replies

**Chris2** (2022-06-16):

My only comment is that in the future if there is a delay in the merge the policy should be that the bomb should be pushed back quickly instead of  the decision being delayed.

Harming the network should be avoided at all costs. Raising block times has led to decreased overall network activity (total # of transactions decrease) while loyal customers are forced to pay higher gas costs. L2’s and others who are required to use the network should be encouraged to not punished. Its actions like these that push users to competing networks.

The #1 goal of all Ethereum developers should be to benefit all Ethereum users and stakeholders. This whole difficulty bomb thing where some developers try to use harming the network as a threat to blackmail other developers to work faster is childish. It was meant as a thing to keep people talking/involved not to beat them over the head with a stick.

Bad publicity due to delaying the bomb should be a tiny factor compared to harming Ethereum’s users. The bomb does nothing to make the merge come faster developers are not children. They are working as fast as they can and understand the importance of Ethereum development. The threat itself is also stupid as companies rushing their developers has generally led to tragedy in history. Cyberpunk 2077 being a prime example along with the DAO and Fallout New Vegas. I have heard people claim that developers are not being “rushed” but if thats so then why are we trying to time a bomb that will greatly harm Ethereum users and the merge to be weeks apart?

The Merge will happen when its ready and has been fully tested. The bomb will not influence it.

The linked article is a great reference

[Why rushed code and projects doesn’t save time](https://thehosk.medium.com/why-rushed-code-and-projects-doesnt-save-time-ce00410004e5)

---

**cipherix** (2022-06-23):

Hi all,

I manage multiple Geth nodes used by large ecosystem companies and need to clear out my calendar to monitor the Grey Glacier hard fork next week.

I’m trying to write a script to predict when (in human time) the Ethereum hard fork will take place. It’s getting a bit off-hand because of the difficulty time bomb’s impact on inter block time. If anyone here could point me to an already-existing formula to do this, that’d be much appreciated. [@timbeiko](/u/timbeiko) mentioned Wednesday in the blog post which makes me think a script for this already exists.

I think it’d be something other node-runners would really appreciate in order to figure out if they’ll have to pull an all-nighter and plan accondingly with their teams  ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)

---

**ericmartihaynes** (2022-06-24):

The problem to estimating this is exactly what you said, calculating the exact date is complicated because of the changes in block time caused by the bomb. You can use https://etherscan.io/block/countdown/15050000 to see a rough estimate, but it will change according to the current block time. If all else was equal, block times would not change so quickly, as the difficulty added by the bomb only increases every 100k blocks. The issue seems to be that if hashrate decreases, the effect of the bomb is more pronounced, and increases block times even if the 100k blocks have not gone by yet.

---

**cipherix** (2022-06-24):

Thank you [@ericmartihaynes](/u/ericmartihaynes)!

I was not aware of the 100k increments – very interesting, is there a formula I could rely upon for the difficulty increase?

Perhaps another approach would be to ignore difficulty altogether. I have data on inter-block times from Arrow Glacier and Muir Glacier. Do you think if I get the exponential function of both of these curves and extrapolate them onto Grey Glacier it would reflect the time bomb’s impact on block time? In other words, I would just model out the exponential increase in block times using inter-block times from previous hard forks.

This approach might be more accurate as it accounts for hashrate volatility, which also impacts inter-block time ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12)

---

**ericmartihaynes** (2022-06-27):

You’re welcome ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

For the formula and the exact calculation used in order to calculate the difficulty increase, you can check out the formulas in described in the [Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf). I think page 7 is what you are looking for.

Your suggested approach of using historical data from previous times the bomb has detonated could work, we are actually working on a similar prediction model, I will post it here when it is ready

---

**cipherix** (2022-06-27):

That would be great, would love to take a look.

With regards to the difficulty formula, it appears it has changed a couple of times since the yellow paper. [This excellent post](https://tjayrush.medium.com/its-not-that-difficult-33a428c3c2c3) by [@tjayrush](/u/tjayrush) provides a formula that, from my understanding, is current. He was able to pull some really interesting data from showcasing the delay ahead of hardforks:

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/8/8846de95dbaf0efa9dc75fcafaf3aaa928434a71_2_381x375.png)image1226×1202 76.1 KB](https://ethereum-magicians.org/uploads/default/8846de95dbaf0efa9dc75fcafaf3aaa928434a71)

I’ll keep sharing my progress here as I still think this will be an important tool for Grey Glacier and The Merge.

---

**fulldecent** (2022-06-27):

I believe the wording in the EIP “To avoid network degradation due to a premature activation of the difficulty bomb.” is overly generous.

Customers have been waiting for this bomb / and the associated upgrade for years. In fact the majority of the value of ETH (maximum USD 0.5T) is probably based on the assumption that “the bomb will go off in the next three month and Eth2 will ship before then”.

There is no reason to use such misleading and self-serving language in an EIP.

Perhaps “To avoid network degradation due to us not shipping major upgrades to Ethereum on time, now currently 5 years overdue” is a more accurate and realistic wording.

---

**timbeiko** (2022-06-27):

[@cipherix](/u/cipherix)  here’s what I used to guesstimate the block number for the fork happening around June 29th: [Gray Glacier Block Height - Google Sheets](https://docs.google.com/spreadsheets/d/1fTSbD712YEU0MQKOuF-bgBH9LuO1X8G9vf-znwEVjVs/edit?usp=sharing)

All the block time data is from [Etherscan](https://etherscan.io/chart/blocktime), so you can probably refine it by using data from the current bomb period rather than historical looks at the same period in different conditions.

---

**ericmartihaynes** (2022-06-30):

Deep dive into the difficulty bomb delay: https://www.notion.so/nethermind/EIP-5133-Difficulty-Bomb-Delay-02bba2398b8b4e95a221338b259b2574

---

**sbacha** (2022-07-01):

Great article!

Got anymore:))))))

