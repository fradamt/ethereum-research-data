---
source: magicians
topic_id: 12152
title: EIP-6145 Proposal #Hashtag NFT Collective Royalty Treasury
author: Livetree
date: "2022-12-14"
category: EIPs
tags: [nft, royalty, treasury]
url: https://ethereum-magicians.org/t/eip-6145-proposal-hashtag-nft-collective-royalty-treasury/12152
views: 924
likes: 6
posts_count: 7
---

# EIP-6145 Proposal #Hashtag NFT Collective Royalty Treasury

# EIP - #Hashtag NFT Collective Royalty Treasury



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/6145)














####


      `master` ← `AshleyTuring:master`




          opened 06:05PM - 15 Dec 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/2/221bb9152d5d02d888ebdcf7cf7968e37ffd2003.jpeg)
            AshleyTuring](https://github.com/AshleyTuring)



          [+84
            -0](https://github.com/ethereum/EIPs/pull/6145/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/EIPs/pull/6145)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.












A standardized way to deposit, withdraw and retrieve creator fee (“royalty”) information associated with a human readable name - this standard enables universal support for royalty payments across social networks, NFT marketplaces and ecosystem participants, its generic design can be implemented on any EVM compatible blockchain and its specific implementation is intended to associate royalties with a hashtag (#) name, however, it is highly versatile and can be used to attribute royalties for any Ethereum address, for example, an NFT.

## Implementation Addresses

We have implemented this proposed standard on the following blockchains.

| # | Contract Name | Blockchain | Address |
| --- | --- | --- | --- |
| 1 | HashtagNFTCollectiveTreasury | Ethereum | 0xe4E9ae2D65008d171A07C12F20D5a5d62Fb31776 |
|  |  | Moonbeam | 0xA50e98f9cb301c04B9BB34d1BD95c2Dc8F3e8Ff3 |
|  |  | Moonriver | 0xA50e98f9cb301c04B9BB34d1BD95c2Dc8F3e8Ff3 |
|  |  | Celo | 0x72824902d75F9832002c7907DF61a60A4AB801C9 |
|  |  | Unique | 0xA50e98f9cb301c04B9BB34d1BD95c2Dc8F3e8Ff3 |
|  |  | Quartz | 0xA50e98f9cb301c04B9BB34d1BD95c2Dc8F3e8Ff3 |
| 2 | HashtagNFTCollectiveResolver | Ethereum | 0xA50e98f9cb301c04B9BB34d1BD95c2Dc8F3e8Ff3 |
|  |  | Moonbeam | 0x9a6Cba29cc0cA4f18990F32De15aae08819F4cD0 |
|  |  | Moonriver | 0x9a6Cba29cc0cA4f18990F32De15aae08819F4cD0 |
|  |  | Celo | 0xdEc0F21665065e0c67b8eD107b1767c95cC4A763 |
|  |  | Unique | 0x9a6Cba29cc0cA4f18990F32De15aae08819F4cD0 |
|  |  | Quartz | 0x9a6Cba29cc0cA4f18990F32De15aae08819F4cD0 |

Further implementation details may be found in the Livetree repository [here](https://github.com/livetreetech/LivetreeCollective).

## Replies

**anett** (2022-12-14):

Hi, did you share your EIP to [GitHub - ethereum/EIPs: The Ethereum Improvement Proposal repository](https://github.com/ethereum/EIPs) ?

Would be better if you shared just link to your EIP instead of pasting whole EIP here

---

**Livetree** (2022-12-14):

Thank you [@anett](/u/anett) !

I did attempted to do so but the process took me here. Do you have some instructions on how I can generate the appropriate EIP < NUMBER > and how I can add it to the repo?

---

**anett** (2022-12-14):

EIP number will get assigned by the EIP Editors when you submit your EIP to ethereum/EIPs repo

**EIP Tutorial:**

Write your EIP using [EIP template](https://github.com/ethereum/EIPs/blob/master/eip-template.md)

Then create to [ethereum/EIPs](https://github.com/ethereum/EIPs/pulls)

Afterwards share the link to [Eth Magicians forum](https://ethereum-magicians.org/) to gather community feedback

EIP editors will assign the EIP number to it

Do not copy paste the EIP itself to FEM forum, post just overview and link to the EIP itself

#### You can find more information on EIP process in the , it includes EIP Guidelines and EIP specific group chats

---

**Livetree** (2022-12-15):

Hey [@anett](/u/anett)

Thanks very much for the info.

Created the PR but it seems the Bot has thrown it out

- Do we now just await for the PR to be reviewed?

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/a/a34d1928d5d77b7f3fdb065ef4ebdda1e6223e87_2_690x432.png)image2401×1506 281 KB](https://ethereum-magicians.org/uploads/default/a34d1928d5d77b7f3fdb065ef4ebdda1e6223e87)

---

**5cent-AI** (2022-12-16):

I just submitted an eip draft and have the same question

---

**Livetree** (2022-12-24):

It does get picked up [@5cent-AI](/u/5cent-ai) by reviewers and they assign the PR number as the EIP number. Be sure to make sure you pass the auto check bots it is a bit finicky. Hope this of of some help.

[@anett](/u/anett) it appears as if my PR and EIP are now good [Add EIP-6145: Hashtag NFT Collective Royalty Treasury by livetreetech · Pull Request #6145 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6145) it is linked to this discussion thread. What are next steps? Thanks.

