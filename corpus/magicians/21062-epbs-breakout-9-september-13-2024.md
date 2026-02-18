---
source: magicians
topic_id: 21062
title: ePBS breakout #9, September 13 2024
author: abcoathup
date: "2024-09-12"
category: Protocol Calls & happenings
tags: [breakout, epbs]
url: https://ethereum-magicians.org/t/epbs-breakout-9-september-13-2024/21062
views: 87
likes: 0
posts_count: 1
---

# ePBS breakout #9, September 13 2024

#### Agenda

[EIP-7732 breakout room #9 · Issue #1150 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1150)

#### Notes

Notes by [@terence](/u/terence) *[copied from [X](https://x.com/terencechain/status/1834613607818244174)]*

- Julian presented an argument that slot auction gives an out-of-protocol trusted advantage by running an MEV-Boost auction at the execution stage
- Mark presented new engine API methods for retrieving payloads
- We talked about whether withdrawals could be on executions and what the blocker for this is


      ![](https://ethereum-magicians.org/uploads/default/original/2X/c/c2b74ef14ba10e3cb1468e5e7a306e4d85700ce9.png)

      [HackMD](https://hackmd.io/@ttsao/epbs-breakout-9)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###



Julian presented a new argument against slot auctions, stating that slot auctions give off-protocol a clear advantage over on-protocol. The new argument can be summarized as follows. A proposer is better off doing the following:










Recap by [@potuz](/u/potuz) *[copied from Eth R&D [Discord](https://discord.com/channels/595666850260713488/874767108809031740/1284169691723595858)]*

- @JulianMa presented an analysis pretty much showing that on slot auctions there’s a “trusted advantage” that does not seem to be possible to avoid. This seems like a serious problem on slot auctions and it’d be nice to weigh against the known problems of block auctions. We decided to keep building on block auctions for the time being cause it’s an easy switch to slot auctions if they are decided later.
- @ethDreamer proposed a new method in the Engine API to requests payloads by range. We agreed that it was sensible to have this method. I raised that we shouldn’t even need to have the payload to sync. Would like to talk to @m.kalinin about this, Perhaps we can schedule an informal call Misha? I think once the requests are sent outside of the payload and the block is hashed as SSZ, we should not need to get the payloads ever on the CL, and would only need to have the payload HTR.
- @terence proposed that we moved the processing of withdrawals to the execution phase. Mark seemed to strongly prefer it, I don’t oppose it and even like it, but acknowledge that it’s different on the beacon chain and would want someone else besides me vouching for it. We decided to requests here for signals from teams if they rather want to move this to the EL payload processing.

#### Recording

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/0/0b8f210e32b4657cd1a9cf672d8a34ccbd8c1119.jpeg)](https://www.youtube.com/watch?v=2BUsiUnUZYc&t=12s)

#### Additional Info



      [docs.google.com](https://docs.google.com/presentation/d/1-MnAqDzR7JapIPpUEbScALEtY5axyRcPgJDpgaJ_qVI/edit)



    https://docs.google.com/presentation/d/1-MnAqDzR7JapIPpUEbScALEtY5axyRcPgJDpgaJ_qVI/edit

###

Trusted Advantage in Slot Auctions Julian Ma Robust Incentives Group @ EF
