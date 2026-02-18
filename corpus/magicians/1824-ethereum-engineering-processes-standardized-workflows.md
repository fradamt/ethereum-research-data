---
source: magicians
topic_id: 1824
title: Ethereum Engineering Processes (standardized workflows)
author: jpitts
date: "2018-11-06"
category: Magicians > Primordial Soup
tags: [forks, devops, workflows]
url: https://ethereum-magicians.org/t/ethereum-engineering-processes-standardized-workflows/1824
views: 1094
likes: 1
posts_count: 1
---

# Ethereum Engineering Processes (standardized workflows)

> Everyone hates checklists, but Ethereum will only reach its potential if we can regulate it with the gravity of flight engineering.

“Ethereum Engineering Processes” is an excellent resource proposed / created by [@karalabe](/u/karalabe).

He starts by proposing EEP-1, a workflow for network participants on how to roll out consensus upgrades onto the Ethereum mainnet reliably and reproducibly.



      [github.com/karalabe/eee](https://github.com/karalabe/eee/blob/master/eeps/eep-1.md)





####

  [master](https://github.com/karalabe/eee/blob/master/eeps/eep-1.md)



```md
---
EEP:     1
Title:   Consensus update rollout
Authors: Péter Szilágyi

Status:  Draft
Version: 2018-11-06
Discuss:
---

*Ethereum is a mission critical system, the long-term sustainability of which requires strict engineering practices over rock-star development. Part of that effort is ensuring we have well defined processes that all ecosystem participants understand, agree with and adhere to. Everyone hates checklists, but Ethereum will only reach its potential if we can regulate it with the gravity of flight engineering.*

*All amendments to this standardized workflow must be rationalized via real world failures, which must be included for future reference to avoid regressions. When adding a new item, please also include an inline explanation to help newcomers.*

## Abstract

The goal of this document is to act as a step-by-step guide for network participants on how to roll out consensus upgrades onto the Ethereum network in a reliable and reproducible fashion. It defines the timelines and deliverables different teams must follow, as well as the emergency procedures in case something foreseeable goes wrong.

The scope of this document is *not* the specification, implementation and preparation of forks. Rather, the scope of this document is to outline their safe rollout once the ecosystem gives the green light on deploying them.

## Preconditions
```

  This file has been truncated. [show original](https://github.com/karalabe/eee/blob/master/eeps/eep-1.md)










Related to this topic are recent posts about the disorderly Constantinople-related fork on Ropsten:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png)
    [Issues we discovered in the Ropsten Constantinople hard fork](https://ethereum-magicians.org/t/issues-we-discovered-in-the-ropsten-constantinople-hard-fork/1598) [Process Improvement](/c/magicians/process-improvement/6)



> Here’s my initial post-mortem and concern/task list following the Constantinople Ropsten hard fork, in no particular order.
>
>
> A consensus bug in Parity was discovered (https://github.com/paritytech/parity-ethereum/pull/9746). We need to understand why this consensus bug occurred in the first place, and particularly why it wasn’t caught by the tests. @ethchris suggests that we may need clearer EIP specs including pseudo code (https://twitter.com/ethchris/status/1052503731072315392). Apparently i…



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png)
    [Disorderly Constantinople fork on Ropsten testnet](https://ethereum-magicians.org/t/disorderly-constantinople-fork-on-ropsten-testnet/1582) [Signaling Ring](/c/working-groups/signaling-ring/19)



> This case brings up interesting developer coordination issues and illustrates the importance of a well-defined testing process as client developers prepare to implement changes affecting mainnet.
> In this planned activation of changes on Ropsten testnet, when the forking block was reached, there was not enough mining power from Ropsten clients implementing Constantinpole changes. This led to a disorderly forking in which the intended upgraded network failed to quickly materialize / become domina…



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png)
    [A case to study: proposed Constantinople-related fork on Ropsten](https://ethereum-magicians.org/t/a-case-to-study-proposed-constantinople-related-fork-on-ropsten/1529) [Signaling Ring](/c/working-groups/signaling-ring/19)



> Context: AllCoreDevs meetings notes #47 on Fri, September 28, 2018
>
> “Geth, Parity, aleth, ethereumj, mana, nethermind - completed implementation of all EIPs”
> “we should probably pick a block number today for testnet fork”
> “Let’s go with Ropsten block 4.2M, that puts us at this time in 11 days, on Oct. 9”
>
> Certain client development stakeholders wanted to activate forking changes / Constantinople in order to identify possible consensus bugs and reduce risks for when these changes are activate…
