---
source: magicians
topic_id: 1529
title: "A case to study: proposed Constantinople-related fork on Ropsten"
author: jpitts
date: "2018-10-04"
category: Working Groups > Signaling Ring
tags: [forks, signaling]
url: https://ethereum-magicians.org/t/a-case-to-study-proposed-constantinople-related-fork-on-ropsten/1529
views: 1021
likes: 4
posts_count: 3
---

# A case to study: proposed Constantinople-related fork on Ropsten

Context: [AllCoreDevs meetings notes #47 on Fri, September 28, 2018](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2047.md#constantinople)

> “Geth, Parity, aleth, ethereumj, mana, nethermind - completed implementation of all EIPs”
>
>
> “we should probably pick a block number today for testnet fork”
>
>
> “Let’s go with Ropsten block 4.2M, that puts us at this time in 11 days, on Oct. 9”

Certain client development stakeholders wanted to activate forking changes / Constantinople in order to identify possible consensus bugs and reduce risks for when these changes are activated in clients for mainnet. This group includes the geth team.

On the other hand, dapp stakeholders who depend on Ropsten stability did not the burden of dealing with a fork, and wanted a stable, enduring testnet for their users/testers. In this case it was the Raiden team.

The key discussion between these groups happened here: https://gitter.im/ethereum/AllCoreDevs?at=5bb5c0b0ef4afc4f281795f2

## Replies

**MadeofTin** (2018-10-04):

It would be good to get a sense how many projects this would affect. I assume it is not just Raiden. I know giveth is using Ropsten for some things. An opportunity for Project Decision Makers to signal they are ready to support such forks would be helpful here.

---

**xinbenlv** (2023-08-02):

Hi from 2023,

[ERC-5982: Role-based Access Control](https://eips.ethereum.org/EIPS/eip-5982) provides a Role-based Access, and ERC-7303 is proposed to implement it in NFT [Add EIP: Token-Controlled Token Circulation by kofujimura · Pull Request #7303 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7303)

