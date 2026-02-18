---
source: magicians
topic_id: 22959
title: Consensus-layer Call 152
author: system
date: "2025-02-22"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/consensus-layer-call-152/22959
views: 225
likes: 2
posts_count: 4
---

# Consensus-layer Call 152

# Consensus-layer Call 152

[prev: call 151](https://github.com/ethereum/pm/issues/1280)

Meeting Date/Time: [Thursday 2025/3/6 at 14:00 UTC](https://savvytime.com/converter/utc/mar-6-2025/2pm)

Meeting Duration: 1.5 hours

stream

1. Electra
2. PeerDAS / Blob scaling
3. Research, spec, etc.
4. Open discussion/Closing remarks

[GitHub Issue](https://github.com/ethereum/pm/issues/1323)

## Replies

**yashkamalchaturvedi** (2025-03-07):

![image](https://etherworld.co/favicon.png)

      [EtherWorld.co – 7 Mar 25](https://etherworld.co/2025/03/07/highlights-of-ethereums-all-core-devs-meeting-acdc-152/)



    ![image](https://etherworld.co/content/images/2025/03/EW-Thumbnails-6.jpg)

###



Holesky Testnet Updates, Pectra Shadow Fork, Pectra Sepolia Fork Updates, Pectra Mainnet Readiness & Fee Mechanism Analysis

---

**ralexstokes** (2025-03-08):

**ACDC #152 summary**

**Action Items**

- Run any available validators on the Holesky network. Check this doc for further details around the Holesky recovery: Holesky rescue efforts v2 - HackMD

**Summary**

- Pectra

The Holesky testnet succesfully upgraded to Pectra, but a series of bugs impacted network health and we have not been finalizing since 24th February.
- Client teams are currently working to restore finality, and we began the call with discussions around the best way to achieve that.
- Lighthouse started by highlighting some updates to their client to handle growing state size during times of non-finality.
- Manu from Prysm built a model to estimate when we would expect finality given the current state of the network: Holesky wen finality - Google Sheets. This model estimates the restoration of finality on 28th March.
- Next, we turned to a doc from Pari to explore some options on a path forward.

Path forward for Holesky - HackMD

Everyone agreed we should restore Holesky, and given the potential for this process to take weeks, Pari raised the question of a temporary second network to allow stakers to test in parallel. A straightforward option would be a shadow-fork of Holesky that would replicate a similar setting to Holesky today, with the caveat that network topology would likely not match Holesky (which is more similar to mainnet than a shadow-fork would be). The biggest blocker to a shadow-fork useful for testing would be the tooling and infrastructure layer as we would need duplicates to run along with the current Holesky setup.
We had a Lido representative on the call who could chime in as one of the stakers who would like to test. In short, they could work with a second network, although they would still want to do some testing on Holesky once it finalizes.
Some client teams chimed in with some downsides to a second network:

- Some bugs on Holesky need to be resolved, and we would not see them on a second healthy network.
- Having a second network would dilute attention of client teams from recovering Holesky as their primary focus.

We briefly touched on `pectra-devnet-7` and decided to spin the network down as we have verified everything on this network worth testing.
Another point was raised that even if we do finalize Holesky, many validators will be exited from slashing and so restoring Holesky to a high validator count (~1.8M) would take a long time due to the activation queue.
The PandaOps team highlighted the importance of non-finality testnets, and attendees agreed the best way to handle this is in parallel to other R&D efforts. This suggests we try to move ahead with finalizing Holesky as soon as possible.
Taken together, we ultimately agreed that a second network is worthwhile, and while we will evaluate the situation after Holesky finalizes again we expect to terminate the second network upon regaining finality.
Next, we turned to Sepolia which upgraded to Pectra this week and also had some small turbulence following the triggering of a bug after the upgrade. Sepolia has returned to normal operation.
One issue that came up from the Sepolia bug was the consideration of specifying how clients parse deposit logs and usage of the deposit contract’s ABI encoding.

- There was quite a bit of back and forth between EL client teams around how to handle this as some clients do not want to enshrine the encoding in the spec.
- Check the call for the full discussion, and expect more conversation on next week’s ACDE.

We rounded out the Pectra discussion with a number of bugs recently found:

- 2 BLS issues that have been resolved, with enhanced test coverage.
- A griefing vector in EIP-7002 (and to a lesser extent EIP-7251); we agreed no change is necessary at the moment as the extent of the griefing vector does not appear that severe.

PeerDAS / blob scaling

- peerdas-devnet-5 is going well, and the point was raised that this is in part due to broad usage of “supernodes” that add a stable backbone providing data availability.

N.B.: The high usage of supernodes is a stepping stone along the development process and future devnets will focus on different node and validator topologies to exercise different sampling regimes in the PeerDAS design.

Sean from Sigma Prime raised two PeerDAS PRs that need input from EL devs:

- Update EIP-7594: include cell proofs in network wrapper of blob txs by fradamt · Pull Request #9378 · ethereum/EIPs · GitHub
- Define EIP-7594 related changes by 0x00101010 · Pull Request #630 · ethereum/execution-apis · GitHub

---

**abcoathup** (2025-03-08):

### Audio

### Writeup



      [Galaxy](https://www.galaxy.com/insights/research)



    ![](https://images.ctfassets.net/f2k4wquz44by/463x5RWiljKDUDreKR2jBr/b63f3a1e75664639bb120e02663c68fc/galaxy.com.png?w=1200&h=675&fit=fill&q=60&fm=jpg&fl=progressive)

###



Explore Galaxy’s Insights for in-depth crypto and blockchain research, including crypto mining, hedge fund, and venture reports. Learn more with Galaxy today!

