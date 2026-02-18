---
source: ethresearch
topic_id: 14588
title: Execution & Consensus Client Bootnodes
author: pcaversaccio
date: "2023-01-10"
category: Architecture
tags: []
url: https://ethresear.ch/t/execution-consensus-client-bootnodes/14588
views: 10801
likes: 62
posts_count: 48
---

# Execution & Consensus Client Bootnodes

Having looked in depth at the dependency of bootnodes, I would like to express my concerns about the centralisation and reliance on third-party cloud services that current bootnodes exhibit.

### Overview Execution Clients

#### Go-Ethereum

- Mainnet Bootnodes: go-ethereum/bootnodes.go at 2c6dda5ad7a720cccd957230f7978de0082ec8c7 · ethereum/go-ethereum · GitHub
- 8 bootnodes running on AWS, Azure, and Hetzner.

#### Nethermind

- Mainnet Bootnodes: nethermind/foundation.json at 9e74cff36443bc72c75eb4efcbe6dfcd57ac8ab6 · NethermindEth/nethermind · GitHub
- 32 bootnodes running. 8 of the 32 bootnodes are the Geth bootnodes running on AWS, Azure, and Hetzner.
- For the remaining 24 bootnodes, I couldn’t find the hosting locations. However, they use the same bootnodes as in the original Parity client: trinity/constants.py at master · ethereum/trinity (github.com). However, all without information on where hosted.

#### Erigon

- Mainnet Bootnodes: erigon/bootnodes.go at 19af2009dc4f9b20c3a647527f9495f95eb35f49 · ledgerwatch/erigon · GitHub
- The 8 Geth bootnodes running on AWS, Azure, and Hetzner.

#### Besu

- Mainnet Bootnodes: besu/mainnet.json at e129c9f0b9e3979259a96f5c8a8f101429834d65 · hyperledger/besu · GitHub
- 14 Bootnodes running. 8 of the 14 bootnodes are the Geth bootnodes running on AWS, Azure, and Hetzner. Additionally, 5 legacy Geth & 1 C++ bootnode is listed. However, all without information on where hosted.

On the CL side (i.e. Beacon node), I couldn’t figure out any information on the hosting location.

I was wondering what other people think about this, especially since Hetzner, for example, doesn’t really seem to be crypto-friendly. Personally, I would strongly advocate for more bare metal in Ethereum! In summary, I would like to see more transparency from the EL and CL side on hosting information.

> Please see my replies below about the source links of the different client bootnodes.
> Update: I was now able to put all relevant links into this description. I deleted the further replies accordingly.

## Replies

**randomishwalk** (2023-01-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/pcaversaccio/48/10260_2.png) pcaversaccio:

> Personally, I would strongly advocate for more bare metal in Ethereum! In summary, I would like to see more transparency from the EL and CL side on hosting information.

Will second and echo the sentiment shared here. The problem I think is that it seems like operating bare metal reasonably well requires some degree of sysadmin expertise and I don’t think these types of people are easy to come by? Could be wrong.

To that end, if there’s any docs or community resources, esp from client teams, would be good to curate and consolidate in one place to make everyone’s life easier. I am not aware of what’s out there given I haven’t had a chance to look but happy to pitch in and help on this if there’s some degree of consensus that this is somewhat of an issue. Even something as simple as a vendor sheet with basics around pricing, jurisdiction, geographic diversity of DCs, etc would be helpful. Ideally we don’t need to rely on DCs but I don’t see why bare metal can’t be a compelling option (alongside independently operated infra / self-hosting).

---

**MicahZoltu** (2023-01-11):

This is concerning, certainly, but the failure mode is a liveness failure for new participants which isn’t the worst situation, especially since you can change your bootnodes via configuration.

It would be great to see more boot nodes that are hosted independently (e.g., in someone’s basement), or at least spread across many different datacenters in many different jurisdictions.  This *doesn’t* mean just different AWS regions, because all of AWS (except China, sort of) are under the jurisdiction of the US.  Ideally we would find some smaller locally owned/operated DCs in various jurisdictions including places that have a bit of a history with censorship resistance and privacy like Iceland, Sweden, Switzerland, as well as some jurisdictions that are just non-functional like many “developing nations”.

---

**pcaversaccio** (2023-01-11):

> especially since you can change your bootnodes via configuration

yes, but many don’t even know this! So the issue here is also about creating awareness & create a game plan for the extreme case that the bootnodes get censored. One very important feature that needs to be implemented by client teams is a warning when bootnodes are becoming unavailable. This would be an early warning for the community and we could react by opening PRs, publishing Tweets etc. about alternative enodes or Ethereum Node Records as defined in [EIP-778](https://eips.ethereum.org/EIPS/eip-778).

> It would be great to see more boot nodes that are hosted independently

Exactly, this is pivotal to mitigate any liveness failure. The liveness failure is not only for new participants but can also happen to existing ones that need to restart.

---

**MicahZoltu** (2023-01-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/pcaversaccio/48/10260_2.png) pcaversaccio:

> Exactly, this is pivotal to mitigate any liveness failure. The liveness failure is not only for new participants but can also happen to existing ones that need to restart.

I thought clients kept track of peers they discovered across restarts?

---

**randomishwalk** (2023-01-11):

Better yet, have the DCs located in your geographically diversified basements ![:blush:](https://ethresear.ch/images/emoji/facebook_messenger/blush.png?v=12)

---

**pcaversaccio** (2023-01-11):

> I thought clients kept track of peers they discovered across restarts?

Yes, but in an extreme censoring event they might lose the peers during restart and need the bootnodes.

---

**randomishwalk** (2023-01-11):

I think to [@MicahZoltu](/u/micahzoltu)’s overall point though (while I do appreciate your caution here), realistically speaking, seems like it would be quite difficult to fully censor the peering process at least for any significant period of time, no? And it doesn’t seem tremendously difficult to respond to this type of censorship attack, though it is good that you are calling attention to something that not many people pay attention to (and the vast majority are simply unaware).

Counterpoint to the point I made above on *“this being too hard to censor for long”*:

- I guess a state actor could go through the local ISPs (and in any given country, there are typically only a few given they are basically always oligopolies and occasionally state-owned/operated and/or somehow state-sponsored public-private actors in some regions such as Asia) and do the damage that way…hm

---

**pcaversaccio** (2023-01-11):

At the core of Ethereum should be a censorship-resistant design. I think we all agree on this. Thus, it’s also important to think about the unimaginable (even though we’ve globally seen already such censoring events in certain countries or similar ones like GitHub with Tornado Cash). It will be very difficult to execute such an extreme event, **but it remains a possibility** (coordination across a couple of countries is not unusual…). That’s why I think it’s important to think about a game plan and document it properly in case such extreme (or even less severe) events take place so operators/participants know how to act accordingly. Where could you potentially find new uncensored bootnodes? How can I configure it? etc.

That’s why I’m convinced that it’s so important to have globally diversified DCs for the bootnodes to circumvent supranational but still local censoring attacks. Peers can always be censored via ISPs so it’s important to have globally distributed bootnodes available to preserve the censorship-resistance core value and resilience of Ethereum as a whole.

---

**randomishwalk** (2023-01-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/pcaversaccio/48/10260_2.png) pcaversaccio:

> That’s why I’m convinced that it’s so important to have globally diversified DCs for the bootnodes to circumvent supranational but still local censoring attacks. Peers can always be censored via ISPs so it’s important to have globally distributed bootnodes available to preserve the censorship-resistance core value and resilience of Ethereum as a whole.

Sounds like we need better docs and better visibility on the hosting options available. What else do you think we need to do here?

Ideally we don’t need a DC but for boot nodes I understand why putting these on someone’s laptop in a basement is probably not the most robust long-term solution (well unless a lot of people do that but that’s not reasonable to assume as likely)

---

**pcaversaccio** (2023-01-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/randomishwalk/48/9610_2.png) randomishwalk:

> What else do you think we need to do here?

The most important part IMHO is to create *awareness* about the issue. We can’t fully resolve this challenge but we have to make the network participants conscious of this.

The problem with cloud solutions is the following: most of them a running under US law, so in case we even diversify on the cloud providers for the bootnodes, a single point of failure exists: the US enforcement possibility. One option is that the EF is setting up in at least 20 countries around the globe independent bootnodes running each on country-specific (i.e. local) DCs. Another additional option could be that the EF maintains an official bootnode list (including the hosting details) from which each of the clients pulls the information and you can be also added as an individual there after being carefully vetted - i.e. trying to include the broader community. We would need to think about an incentive scheme (& slashing possibility) there of course. Maybe others have other ideas…

---

**randomishwalk** (2023-01-12):

Obviously it would be nice to have support, but in the absence of that I don’t see why we can’t do some of the stuff ourselves? “Ourselves” being community members, sysadmin-types, devops people, Core devs who have time to comment, and enlist folks from the various home staker & solo staker communities — would involve some degree of cat herding yes

---

**pcaversaccio** (2023-01-12):

fully agreed: how can we best create more awareness about this important discussion [@timbeiko](/u/timbeiko), [@MicahZoltu](/u/micahzoltu)? Cc: [@vbuterin](/u/vbuterin)

---

**gsalberto** (2023-01-20):

Hey Guys,

[@randomishwalk](/u/randomishwalk) sent this thread to me over twitter and I am jumping here as I can potentially help with distributed global infrastructure

latitude.sh, bare metal company I operate, run in 15 locations (9 of them being our of the US) - [Global regions to deploy dedicated servers and custom projects - Latitude.sh](https://www.latitude.sh/locations)

Happy to chat more

---

**holiman** (2023-01-30):

Bootnodes are nice, they are something of a UX helper, making it easier for a brand new node to find peers.

If they are beefy enough, they can also help serve `eth` data; state and blocks. Because of the amount of traffic (both egress and ingress), they are also pretty costly.

Are they terribly important to the network? In my opinion, no. Geth works fine without them, since more stable peers can be found via the dns discovery . The dns discovery is also centralized as in “it’s collected and published by EF”, but the information that is published is self-signed by the nodes themselves (in the form of ENR records).

Also, nodes (at least geth) remembers information about peers from previous runs.

In general though: If EF-controlled bootnodes are seens as ‘critical infrastructure’ then we should remove them, because the network needs to get by without central points of failure.

---

**pcaversaccio** (2023-01-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/holiman/48/4014_2.png) holiman:

> Are they terribly important to the network?

If everything works as intended, I would agree. But they can become pivotal in an extreme censoring event. And my threat model tells me that in the current state of the world we should think about this possibility.

![](https://ethresear.ch/user_avatar/ethresear.ch/holiman/48/4014_2.png) holiman:

> because the network needs to get by without central points of failure

that’s exactly the point - the overall preferred solution should be to have a situation where we could completely remove the current kind of centralised initial trusted setup. However, since DNS discovery is also centralised (for anyone interested, see [here](https://github.com/ethereum/discv4-dns-lists) for the list) and can be affected by an extreme censoring event, I think having globally distributed, EF-independent bootnodes serving as last resort rescue is the best solution.

---

**pcaversaccio** (2023-04-14):

## UPDATE (14 April 2023)

**TL;DR**: 4 EF Azure bootnodes got removed since my original post. Now mostly dependent on AWS and Hetzner (silently screaming inside!).

### Overview Execution Clients

#### Go-Ethereum

- Mainnet Bootnodes: go-ethereum/bootnodes.go at e14043db71c5d2d91520fab217302fcecf7aa939 · ethereum/go-ethereum · GitHub
- 4 bootnodes running on AWS (2 out 4) and Hetzner (2 out 4).
- In this commit params: remove EF azure bootnodes (#26828) · ethereum/go-ethereum@e14043d (github.com) the 4 Azure bootnodes got removed.

#### Nethermind

- Mainnet Bootnodes: nethermind/foundation.json at 64608b94bfd08793e84eb9d90028aafef7efe684 · NethermindEth/nethermind · GitHub
- 34 bootnodes running. 4 of the 32 bootnodes are the Geth bootnodes running on AWS (2 out 4) and Hetzner (2 out 4).
- For the remaining 28 bootnodes, I still couldn’t find the hosting locations. However, they use the same bootnodes as in the original Parity client: trinity/constants.py at master · ethereum/trinity (github.com). However, all without information on where hosted.
- In this commit Remove deprecated EF bootnodes (#5408) · NethermindEth/nethermind@7d6215d (github.com) the 4 Azure bootnodes got removed.

#### Erigon

- Mainnet Bootnodes: erigon/bootnodes.go at 7258a2b872710d6fee9b8e9f4ba617917e8f0e74 · ledgerwatch/erigon · GitHub
- The 4 Geth bootnodes running on AWS (2 out 4) and Hetzner (2 out 4).
- In this commit params: remove EF azure bootnodes (#7061) · ledgerwatch/erigon@43960fe (github.com) the 4 Azure bootnodes got removed.

#### Besu

- Mainnet Bootnodes: besu/mainnet.json at e6395c3af3012b4c4eeee6b2241486a7863b47c7 · hyperledger/besu · GitHub
- 14 Bootnodes running. 4 of the 10 bootnodes are the Geth bootnodes running on AWS (2 out 4) and Hetzner (2 out 4). Additionally, 5 legacy Geth & 1 C++ bootnode is listed. However, all without information on where hosted.
- In this commit Remove deprecated EF bootnodes (#5194) · hyperledger/besu@7afc035 (github.com) the 4 Azure bootnodes got removed.

---

**Souptacular** (2023-04-14):

I love that this discussion is coming back around. I am not convinced that it is as much of an issue as it used to be (because devp2p improvements happened like better DNS discovery so bootnodes aren’t even necessarily needed). At the same time, I’d love to see a solution for a decentralized way to have bootnodes that don’t also increase the risk of bad actors compromising the alternative bootnodes.

I co-lead the DevOps team at the EF from 2016-2021 (and had a 3 year stint in the middle of that as orgsec lead after Martin Swende). I won’t explain the entire security and set up for the bootnodes for security reasons, but I would find it super unlikely that the bootnodes could be compromised via a hack (so a hacker changes the geth bootnode to a bad geth node that makes a split chain) or that a sustained dos attack could happen to the nodes (because the EF would be able to respond and mitigate any attacks or at worst rebuild the whole thing in under half an hour not counting sync time).

I’m definitely open to hearing solutions, but I’m not convinced adding more entities besides the EF is the right way considering the low risk and the potential to open more possibilities for exploit of the bootnodes.

---

**pcaversaccio** (2023-04-14):

My issue here is that I don’t have transparency about why, for example, the EF is able to act as you claim. Security through opacity doesn’t work well, and I understand that you can’t disclose all information for security reasons either. The current situation is like: please trust the EF that we’re doing our job properly. I’m not saying this is not the case, but the required information is (at least publicly) not available. Also, peers can always be censored via ISPs so it’s important to have globally distributed bootnodes available to preserve the censorship-resistance core value and resilience of Ethereum as a whole.

---

**Souptacular** (2023-04-14):

I agree with everything you are saying, but I don’t think the risk is high enough for the ones responsible for the boot nodes to act compared to other pressing issues that would affect Ethereum at the protocol/safety level more. Note: I’m not really involved in that deeply anymore so it’s up to them, I’m just relaying what I suspect they will react.

At the same time that shouldn’t mean we ditch your ideas because they do help.

One idea: start asking individual client teams to set up bootnodes that are geographically diverse and with a common set of standards that include what you propose (geographically diverse, bare metal, etc.). It shouldn’t be the responsibility of the EF to do this entirely and adding bootnodes once the other client teams create them is as simple as a PR on each client. I think other EL client teams would be very open to this and may already have testing infra that can be converted to supporting their own bootnodes as well.

---

**randomishwalk** (2023-04-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/souptacular/48/11800_2.png) Souptacular:

> One idea: start asking individual client teams to set up bootnodes that are geographically diverse and with a common set of standards that include what you propose (geographically diverse, bare metal, etc.). It shouldn’t be the responsibility of the EF to do this entirely and adding bootnodes once the other client teams create them is as simple as a PR on each client. I think other EL client teams would be very open to this and may already have testing infra that can be converted to supporting their own bootnodes as well.

I think that’s a great idea and somewhat of a natural choice given existing devops expertise.

Yet another option, which seems to be more the case in the MEV-Boost relay space, are independent, non-client team affiliated infrastructure operators (Agnostic and USM being two examples on the MEV-boost relay side). Experienced folks from the ethstaker community, for example, might be one natural fit for something like this.


*(27 more replies not shown)*
