---
source: magicians
topic_id: 22566
title: "ERC-7824: State Channels Framework"
author: modtail
date: "2025-01-17"
category: ERCs
tags: [erc, token, erc-721, eip-4337]
url: https://ethereum-magicians.org/t/erc-7824-state-channels-framework/22566
views: 528
likes: 5
posts_count: 4
---

# ERC-7824: State Channels Framework

**Proposal for Standardizing State Channel Interfaces**

Hello Magicians!

After several years of work in the domain of state channels, we believe the time has come to take a significant step towards standardizing their interface. These interfaces have been rigorously tested across various real-world use cases and have demonstrated their capability to express state channel mechanisms in a unified and simplified manner. With this proposal, we seek feedback from the community.

**Abstract**

State channels are a layer-2 scaling solution that enables participants to execute transactions off-chain while retaining the security guarantees of the Ethereum network. By allowing parties to interact directly through signed messages and committing only the final result on-chain, state channels significantly reduce gas costs and improve transaction throughput.

Our work consolidates the intricate mechanics of state channels into a clear, modular framework, which we now propose for standardization.

**Motivation**

Standardizing a common domain language and interface for state channels can have profound benefits. It will enable a small but growing community of developers and researchers to communicate more effectively. A standardized SDK will reduce redundancy we have seen.

The modular design of our proposed interface ensures flexibility, allowing developers to implement diverse protocol rule sets without being constrained by the core framework. This approach supports a wide range of use cases while establishing a solid foundation.

**Call to Action**

We humbly invite your feedback, suggestions, and constructive criticism on this proposal.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/728)














####


      `ethereum:master` ← `layer-3:master`




          opened 12:05PM - 22 Nov 24 UTC



          [![mod](https://avatars.githubusercontent.com/u/80003?v=4)
            mod](https://github.com/mod)



          [+354
            -0](https://github.com/ethereum/ERCs/pull/728/files)







### Pull Request Description

#### EIP Title
ERC-7824: State Channels Protoco[…](https://github.com/ethereum/ERCs/pull/728)l Framework

#### Description
This ERC introduces a standard for implementing state channels on Ethereum. The proposal defines the essential structs and interfaces for state channels, enabling scalable off-chain execution, efficient on-chain dispute resolution with interoperability.

#### Author
Louis Bellet (<[mod@yellow.org](mailto:mod@yellow.org)>)

#### Status
Draft

#### Type
Standards Track (ERC)

#### Category
ERC

#### Build Status
All required builds have passed successfully. The proposal adheres to the provided guidelines and submission criteria.

#### Notes
This pull request creates a new draft EIP for ERC-7250 and follows the template provided in [[EIP-1](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1.md)](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1.md). The proposal aims to facilitate scalable state channel implementations on Ethereum while aligning with existing standards for account abstraction.












Reference implementation :


      ![image](https://github.githubassets.com/favicons/favicon.svg)

      [github.com](https://github.com/statechannels/go-nitro/tree/main/packages/nitro-protocol/contracts)





###



Implementation of nitro-protocol in Go. Contribute to statechannels/go-nitro development by creating an account on GitHub.










Looking forward to the discussion,

Louis

## Replies

**modtail** (2025-02-21):

Heya,

I created a mini site: https://erc7824.org/

Proof reading would be welcome.

I will be present at Denver 2025 to explain ERC-7824, feel free to reach me for debate or learn more!

---

**DKScrypto** (2025-03-18):

Exciting to see this proposal coming together! After years of development and real world testing, standardizing state channel interfaces feels like the right move to push adoption forward for this great tech that not many have really understood .

---

**modtail** (2025-05-20):

Quick heads up, We are release a new version of the SDK

accessible on [GitHub - erc7824/nitrolite: Nitrolite is a simplified version of Nitro, which facilitate prototyping of state-channels apps](https://github.com/erc7824/nitrolite)

and the documentations have been updated with a tutorial: https://erc7824.org/

Tomorrow we will have a presentation workshop we are looking for contributors:


      ![image](https://lu.ma/favicon.ico)

      [lu.ma](https://lu.ma/vtrg2gqr)



    ![image](https://social-images.lu.ma/cdn-cgi/image/format=auto,fit=cover,dpr=1,anim=false,background=white,quality=75,width=800,height=419/api/event-one?calendar_avatar=https%3A%2F%2Fimages.lumacdn.com%2Fcalendars%2F2g%2F51552989-7fdc-432d-ad96-6572947ac34d&calendar_name=Yellow%20Network&color0=%23f0ece9&color1=%23060505&color2=%2385807f&color3=%23fcd916&host_avatar=https%3A%2F%2Fimages.lumacdn.com%2Favatars%2Fze%2Fc1fdb2e5-129b-49b5-8b1e-25f7b13f3b5f.jpg&host_name=Yellow&img=https%3A%2F%2Fimages.lumacdn.com%2Fevent-covers%2F80%2F6124338d-0c2b-4ce9-895f-d40a0dfbd55a.png&name=Build%20to%20Win%20with%20Yellow%20at%20ETHGlobal%20Prague%20Hackathon)

###



Build to Win with Yellow Network at ETHGlobal Prague Hackathon
📅  Date: May 21, 2025
⏰Time: 16:00-17:30 GMT+3
📍Location: Online Google meeting
Get ready to…

