---
source: magicians
topic_id: 22160
title: FOCIL breakout #1, December 13, 2024
author: abcoathup
date: "2024-12-11"
category: Protocol Calls & happenings
tags: [breakout, focil]
url: https://ethereum-magicians.org/t/focil-breakout-1-december-13-2024/22160
views: 105
likes: 1
posts_count: 1
---

# FOCIL breakout #1, December 13, 2024

#### Agenda

[FOCIL Break-Out Room · Issue #1210 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1210)

#### Summary

TLDR by [@soispoke](/u/soispoke) *(Copied from [Twitter](https://x.com/soispoke/status/1867618797622112583))*

We discussed some of FOCIL’s features but mostly focused on coordinating efforts on the implementation side.

Core devs are obviously quite busy shipping Pectra and peerDAS, but we settled on the end of January as a realistic timeline to get to a working devnet

#### Notes

Notes by [@matthewkeil](/u/matthewkeil) *(Copied from [ethereum/pm](https://github.com/ethereum/pm/issues/1210#issuecomment-2541647674))*

##### Spec Stability

- CL spec is relatively stable
- EL spec will be formalized with a PR to EELS

##### Spec Questions

- Fork-Choice slot/block enforcement via proposer-boost reorging. This might/should need to be a separate EIP

##### Inclusions/Exclusions for First Round

- Blobs will not be included
- Maybe not verify IL’s for first round of integration testing

##### Rough Timeline

- Shoot for first week of January for next meeting
- Hope that by that meeting we can have at least 1 CL and 1 EL ready to test with
- Shoot for attempting to set up a basic Kurtosis/Hive network between the first clients on the next call

##### Spec Test Goals

- Engage with Testing group to figure out timeline for work on spec tests

##### Active Branches

- Geth: GitHub - jihoonsong/go-ethereum at focil
- Lodestar: GitHub - ChainSafe/lodestar at focil

##### References Posted During Call

- https://meetfocil.eth.limo/
- FOCIL prototype - HackMD
- FOCIL with geth - HackMD

##### Implementation Notes

Goal should be to keep discussion strictly in Discord and on the website [https://meetfocil.eth.limo](https://meetfocil.eth.limo/). Telegram and Twitter should be avoided to help corral the discussion to a single (or two) places.

There are two cases in the execution case. When sync’d and before sync. Should the CL be notifying the EL to check the IL’s? This will be different cases for when syncing and after sync is complete. A PR will be opened to the spec to dial this in.

EL will look at specifying that if an IL is passed in then the IL should be checked, if not then the IL’s will not need to be verified to check the block. Terrence requested for [@Jihoon](https://github.com/Jihoon) to open a pr here? [Pull requests · ethereum/execution-apis · GitHub](https://github.com/ethereum/execution-apis/pulls)

#### Recording

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/d/da41667d37d4f36b00e36ae9487c315c6ed05cef.jpeg)](https://www.youtube.com/watch?v=SOt-rNDlsRU)
