---
source: magicians
topic_id: 18405
title: EIP-7605 Homogeneous Validator Penalty
author: skoya
date: "2024-01-30"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7605-homogeneous-validator-penalty/18405
views: 615
likes: 1
posts_count: 4
---

# EIP-7605 Homogeneous Validator Penalty

New idea to promote validator diversity.

Promote diversity across validators in the following areas:

Client

Operating System

Geo Location (avoid concentration)

CPU / other hardware

Cloud Hosting provider / ISP

## Replies

**abcoathup** (2024-01-31):

> Unfortunately we can’t make rewards directly dependent on what client a validator runs. There is no objective way to measure this that can’t be spoofed.

From: [Ethereum Merge: Run the majority client at your own peril! | Dankrad Feist](https://dankradfeist.de/ethereum/2022/03/24/run-the-majority-client-at-your-own-peril.html)

---

**skoya** (2024-01-31):

Would that be true of all features?

Client - can we not use a crypto hash of post installation to validate that the client hasn’t been tampered with?

OS - most languages have the ability to check the OS version?

Geo Location - granted - not sure if there is a way to avoid spoofing if relying on IP

IP/ISP/cloud hosting check - could we use WireGuard baked into the validator bootstrap so that during handshake we can validate that the client is really at a specific IP? Post registration I guess its not needed?

CPU likewise with the OS - should be able to detect ARM vs AMD vs Intel architectures?

For privacy could ZKP be used so that the handshake info can be kept private?

---

**abcoathup** (2024-02-01):

Blockprint uses finger printing to estimate consensus layer clients:



      [Sigma Prime – 10 Oct 23](https://blog.sigmaprime.io/blockprint-ui.html)



    ![](https://blog.sigmaprime.io/imgs/cover/blockprint-ui.jpg)

###



Announcing a graphical interface for Blockprint










Check out research kickoff on voluntarily providing some data on the execution layer:


      ![](https://ethresear.ch/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_32x32.png)

      [Ethereum Research – 1 Feb 24](https://ethresear.ch/t/allowing-validators-to-provide-client-information-privately-a-project-by-nethermind-research-and-nethermind-core/18527)



    ![image](https://ethereum-magicians.org/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_500x500.png)



###





          Consensus






(Team’s Twitter handles: @0xjorgeth, @M25Marek, @rmzcrypt, @Smartprogrammer.)  Understanding the distribution of Ethereum’s execution-layer and consensus-layer clients used by validators is vital to ensure a resilient and diverse network. Although...



    Reading time: 10 mins 🕑
      Likes: 18 ❤











---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/skoya/48/11572_2.png) skoya:

> Would that be true of all features?

I assume so.  Especially if you were to attach a penalty, then there would be an incentive to spoof any feature.

Unfortunately this idea is dead in the water.

