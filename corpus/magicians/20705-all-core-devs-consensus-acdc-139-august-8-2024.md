---
source: magicians
topic_id: 20705
title: All Core Devs - Consensus (ACDC) #139, August 8 2024
author: abcoathup
date: "2024-08-03"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-139-august-8-2024/20705
views: 216
likes: 0
posts_count: 3
---

# All Core Devs - Consensus (ACDC) #139, August 8 2024

#### Agenda

[Consensus-layer Call 139 · Issue #1116 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1116) moderated by [@ralexstokes](/u/ralexstokes)

#### Summary

Summary by [@ralexstokes](/u/ralexstokes) *(from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1271599772905766932))*

- Specs release v1.5.0-alpha.4 is out!

Release Tynamo · ethereum/consensus-specs · GitHub
- Various fixes including an Electra bug fix for MaxEB consolidation processing

Pectra devnet-2 update

- Minor known issues in clients but network is generally stable and going well
- EF Devops ran a non-finality test that nodes were able to recover from
- Discussed next steps to devnet-3

a few spec issues to resolve (i.e. EIP-7702), but devnet-3 should be ready soon
- agreed on a testing breakout to streamline devnet coordination as we get closer to mainnet Pectra

see info/poll on R&D discord for timing, but be on the lookout for a testing call that ideally has representation from each client team every call!

Next, some open questions relating to Pectra

- First, a set of changes around reducing the demand for blob propagation leveraging the work of the mempool

https://github.com/ethereum/execution-apis/pull/559
- https://github.com/ethereum/consensus-specs/pull/3864
- Client teams please take a look; these two items are still open but consensus is to merge in the coming weeks

Then, revisited the topic of deprecating `mplex` , a multiplexing protocol used in the libp2p stack of the CL networking software

- mplex has generally been deprecated in favor of other solutions like yamux
- Need some coordination amongst clients to ensure nodes remain interoperable during bootstrapping on the network
- At least one implementation (for the Teku client) is still not quite production-ready, and there were some performance concerns around the JS implementation in Lodestar
- And so we decided to defer deprecation of mplex in Ethereum to a later point in time once all clients feel it is time

And last we discussed the work to include EIP-7688 for SSZ stable containers in Pectra

- Progress has generally been good for the EIP in isolation
- There’s some demand for this feature in Pectra from applications, although it is not clear the demand is urgent
- Given this, and the fact that we prefer to iterate a few more devnets for the current Pectra feature set to get to a place of greater stability, we decided to defer the inclusion discussion until a later time in the hard fork delivery timeline

Then, we turned to PeerDAS

- We started by checking in with the PeerDAS implementers on development progress
- Landed on getting an explicit spec release to target for an upcoming PeerDAS devnet
- Also touched on the blob Beacon APIs and how they should be updated to respect PeerDAS
- Discussed this PR to drop peer sampling from PeerDAS: Spec without peer sampling by fradamt · Pull Request #3870 · ethereum/consensus-specs · GitHub and decided it is a worthy step on the data scaling roadmap; so expect to see it in future PeerDAS devnets

Remainder of the call covered a variety of topics

- A question around the interaction of sync committees and consolidations under Max EB, as you can still have a validator assigned to a sync committee, even if their balance is in the process of consolidating to another validator

Agreed to leave as-is with an explicit call out around this behavior for implementers
- Will also analyze further interactions in Pectra to ensure there are no security implications for this edge-case behavior

Touched on standardizing the `quic` entry to a node’s ENR

- general agreement on this, follow-up here for more info: https://github.com/ethereum/consensus-specs/pull/3644

Closed the call with a presentation by ProbeLab to share their work on networking/discovery protocol analysis; check their website here: [Week 2024-29 | ProbeLab Analytics](https://probelab.io/ethereum/discv5/2024-29/)

#### Recording

  [![image](https://img.youtube.com/vi/o8p47gIt7Bs/maxresdefault.jpg)](https://www.youtube.com/watch?v=o8p47gIt7Bs&t=187s)

#### Additional info

**Notes**: [Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-consensus-call-139/) by [@Christine_dkim](/u/christine_dkim)

## Replies
