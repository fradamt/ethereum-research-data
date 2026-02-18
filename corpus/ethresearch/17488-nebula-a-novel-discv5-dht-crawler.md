---
source: ethresearch
topic_id: 17488
title: Nebula - A novel discv5 DHT crawler
author: dennis-tra
date: "2023-11-23"
category: Networking
tags: []
url: https://ethresear.ch/t/nebula-a-novel-discv5-dht-crawler/17488
views: 1664
likes: 9
posts_count: 3
---

# Nebula - A novel discv5 DHT crawler

Hi everyone,

I’m Dennis from the network measurement and protocol benchmarking team ProbeLab that spun out of Protocol Labs. So far, the team has focused on developing metrics for IPFS (see probelab dot io) but recently started looking into other libp2p-based networks. We extended our DHT crawler that powers IPFS metrics for over a year to also support Ethereum’s DiscV5 DHT. In this post, I want to share some findings and gather feedback. You can find the source code here:



      [github.com](https://github.com/dennis-tra/nebula)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/5/2/5229bd5ea7bb342bbceffba8221714feaa20e99e_2_690x344.png)



###



🌌  A network agnostic DHT crawler, monitor, and measurement tool that exposes timely information about DHT networks.










This Discourse instance only allows one media item and a maximum of two links in a post for new users. So please follow the following link to this Notion page. I originally intended to post its contents here:


      ![](https://ethresear.ch/uploads/default/original/2X/8/8af67b2b7f4a78f0ef3c6668522cae1bad69148e.png)

      [Notion](https://pl-strflt.notion.site/Nebula-A-novel-discv5-DHT-crawler-1cd78fa120a14dfe82ad8dc9dde5dd76)



    ![](https://ethresear.ch/uploads/default/optimized/2X/f/f4f10b180cdc7e8f3334adcc2c52939e0398ef4b_2_690x362.png)

###



A tool that connects everyday work into one space. It gives you and your teams AI tools—search, writing, note-taking—inside an all-in-one, flexible workspace.

## Replies

**leobago** (2023-11-28):

Hi Dennis,

very interesting analysis, as usual.

I understand the CL client distribution that you see is before filtering with any particular fork digest, correct? This means the distribution you are showing is for all networks combined, mainnet and testnets (See figure below for Ethereum testnets). The distribution shown in monitorEth is only for mainnet, so the two should not be compared directly (Apple vs Oranges).

[![image](https://ethresear.ch/uploads/default/optimized/2X/4/439f28046df08d67435066ee7ef8413138db3473_2_690x139.png)image1050×213 35.7 KB](https://ethresear.ch/uploads/default/439f28046df08d67435066ee7ef8413138db3473)

Regarding the fork digests that you see in the network, you can find most of them in our source code: [armiarma/pkg/networks/ethereum/network_info.go at 1f69e0663a8be349b16f412174ef3d43872a28c4 · migalabs/armiarma · GitHub](https://github.com/migalabs/armiarma/blob/1f69e0663a8be349b16f412174ef3d43872a28c4/pkg/networks/ethereum/network_info.go)

I am curious how the CL client distribution looks like after filtering out all the testnets and leaving only the last fork of mainnet. You seem to see about 9.5K nodes on mainnet (**0xbba4da96**), which is very close to the number of nodes that we managed to connect in the last week with Armiarma, see the first bar in the figure below (9680 nodes). The other bars are nodes that we managed to connect some weeks before but haven’t managed to connect since then. They will get deprecated later if a connection is not successful in the coming weeks.

[![image](https://ethresear.ch/uploads/default/optimized/2X/0/03801829f9d02480a119fd1125f0e6e2616371b2_2_690x333.png)image1454×702 43.8 KB](https://ethresear.ch/uploads/default/03801829f9d02480a119fd1125f0e6e2616371b2)

One of the trade-offs between having a very general libp2p crawler vs a specialized one is that with the general one is much harder to be a “good citizen” in the network, as you admit in your post. The first version of Armiarma was very general and we used it for other networks. However, for Armiarma v2, we changed it for a specialized one so that nodes could connect to us and keep us as a good peer of their peer list. This, together with running 24/7, are some key elements that are particularly useful for discovering peers behind NATs, as well as clients that are more strict on following the Ethereum specification. For instance, we have noticed that this is the case of Prysm nodes. If you don’t fully follow the specs (e.g., BeaconStatus exchange, etc) it is normal to see several connections dropped because of it, which might explain why Nebula sees so few of them.

Overall, this first preliminary results look very promising and I am looking forward to see more coming out of this.

Cheers! ![:grinning_face:](https://ethresear.ch/images/emoji/facebook_messenger/grinning_face.png?v=14)

---

**dennis-tra** (2023-11-29):

Hi [@leobago](/u/leobago)

thanks for your insights!

![](https://ethresear.ch/user_avatar/ethresear.ch/leobago/48/18496_2.png) leobago:

> I understand the CL client distribution that you see is before filtering with any particular fork digest, correct? This means the distribution you are showing is for all networks combined, mainnet and testnets (See figure below for Ethereum testnets).

You are totally right! I revised my analysis in two ways:

1. Filtered by the fork digest of 0xbba4da96
2. Looked at multiple crawls to derive the agent version. If I’m not able in a crawl to connect to a peer I won’t find out its agent version. However, when in the next crawl I’m able to connect to it I’m able to extract the agent version. The numbers in that Notion page refer to a single crawl. The below numbers take into account any crawl I’ve done so far.

These numbers come **much** closer to the ones you report:

| Client | Peers | Share |
| --- | --- | --- |
| Lighthouse | 3600 | 38.66 % |
| Prysm | 2645 | 28.40 % |
| teku | 1349 | 14.49 % |
| nimbus | 643 | 6.90 % |
| null | 629 | 6.75 % |
| rust-libp2p | 216 | 2.32 % |
| lodestar | 192 | 2.06 % |
| erigon | 37 | 0.40 % |
| Grandine | 2 | 0.02 % |
| — | — | — |
| Total | 9313 | 100.00 % |

For comparison from https://monitoreth.io/validators:

[![image](https://ethresear.ch/uploads/default/optimized/2X/8/828120bee756fea9c98c575a8041c1cd64a1f7cc_2_690x39.png)image2258×128 14.5 KB](https://ethresear.ch/uploads/default/828120bee756fea9c98c575a8041c1cd64a1f7cc)

Not perfect but we’re getting there!

That’s my brief update! I’ll circle back here regarding your other remarks and when I have updates!

Cheers ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

