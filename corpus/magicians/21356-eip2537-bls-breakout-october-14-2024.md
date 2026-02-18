---
source: magicians
topic_id: 21356
title: EIP2537 BLS breakout, October 14 2024
author: abcoathup
date: "2024-10-12"
category: Protocol Calls & happenings
tags: [breakout, bls]
url: https://ethereum-magicians.org/t/eip2537-bls-breakout-october-14-2024/21356
views: 71
likes: 1
posts_count: 1
---

# EIP2537 BLS breakout, October 14 2024

##### Agenda

[EIP-2537 Breakout Call · Issue #1176 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1176)

#### Summary

TLDR from Kev *(Copied from Eth R&D [Discord](https://discord.com/channels/595666850260713488/1293956979848380529/1295417430058864642))*

- @ralexstokes will try to reach out to users to see what they think about not having subgroup checks
- One possibility was to add a flag, but it was noted by @mratsim that this becomes a pain for zkEVMs to implement this branching logic
- Removing G1MUL and placing it inside of MSM did not seem to have a lot of backing, though there were folks advocating for it as an equalizer, if we decide to add more opcodes like the subgroupCheck
- There seems to have been consensus that the precompiles were underpriced

I think most decisions will be downstream from figuring out whether users want to have subgroup checks

#### Recording

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/0/0b8f210e32b4657cd1a9cf672d8a34ccbd8c1119.jpeg)](https://www.youtube.com/watch?v=zUIogzxkTpc)
