---
source: magicians
topic_id: 1642
title: Toolkit for planned changes/forks on testnet
author: jpitts
date: "2018-10-21"
category: Magicians > Primordial Soup
tags: [testnets, devops, toolkits]
url: https://ethereum-magicians.org/t/toolkit-for-planned-changes-forks-on-testnet/1642
views: 844
likes: 4
posts_count: 2
---

# Toolkit for planned changes/forks on testnet

I’ve seen various comments on Twitter and direct, as well as discussion at EF DevOps about having better planning and documentation with testnet deployments. Some that stand out in particular are: 1. creating institutional knowledge and 2. ways we can enlist more help in the process.

I’ll start the thread here and collect some of those discussing this.

For background, start with this thread: [Lane Rettig’s Retrospective & comments](https://ethereum-magicians.org/t/issues-we-discovered-in-the-ropsten-constantinople-hard-fork/1598).

Initial work is on a [DevOps Retrospective](https://docs.google.com/document/d/1-zWUV491YLK9RxmyFAaY34yvhfEP6umOweXP1EKBhdI/edit#), in order to discuss what happened and what can be done / put into the toolkit.

## Replies

**fubuloubu** (2018-10-22):

This is great!

I think regarding “enlisting more help” for mining (eventually validating) on testnets, there will never be incentive to mine unless we make incentive to mine. One way would be to set aside some money to award mining for a specific length of blocks for the final test period. This is after a period of initial integration testing between client developers.

Awards could be given manually to the addresses that mine during the period (if it was considered stable enough to award) at a rate of 0.001 mainnet ETH to 1 testnet ETH. You would ideally get 1/1000 of the total difficulty/stake (if properly advertised), which would correspond with what should be expected for the mainnet release. For PoS, I think staking tokens could be freely given so inadvertent slashing isn’t a concern, we would just award fees and block rewards manually to the stakes addresses to conduct our final, incentivized test.

I also think we should give up on advertising the non-incentivized PoW/PoS test network for anyone other than client devs and people testing mining upgrades or whatever. Smart contract testing needs a way more stable environment for conducting tests (like Rinkeby), and that should be the best practice/common wisdom everyone should have.

