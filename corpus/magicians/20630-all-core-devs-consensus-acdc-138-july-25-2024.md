---
source: magicians
topic_id: 20630
title: All Core Devs - Consensus (ACDC) #138, July 25 2024
author: abcoathup
date: "2024-07-24"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-138-july-25-2024/20630
views: 517
likes: 2
posts_count: 2
---

# All Core Devs - Consensus (ACDC) #138, July 25 2024

### Agenda

[Consensus-layer Call 138 · Issue #1100 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1100)

Moderator: [@ralexstokes](/u/ralexstokes)

### Summary

Recap by [@ralexstokes](/u/ralexstokes) (*from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1266221913836097648)*)

- Started the call with an update on pectra-devnet-1 , which launched this week

The network is live but participation is low and the chain has forked into 3-4 pieces
- The initial chain split appears to have been caused by an EIP-7702 transaction, and there’s ongoing work to debug

Next, we turned to a proposal to restructure the requests types added in Pectra

- These requests types are data coming from the EL which are required for the CL to process with each block
- Until now, CL clients prune EL data as otherwise the data would be duplicated within one Ethereum node given the dual CL-EL architecture
- The proposal here suggests moving the requests data outside the block structure CL clients already prune so we can easily have the requests data handy with minimal code change
- We discussed the design space addressing this problem on the call as there are a few different ways to satisfy the problem, but there was broad support for @potuz’s solution linked above.

Then we had a proposal from [@matt](/u/matt) to change how these requests types are arranged in the Engine API to facilitate ease of implementation of the EL interfacing with the CL

- There was some back and forth on the details, as a large part of answering this question comes down to finding the best way to share the technical complexity of this feature set between EL and CL implementations.
- This proposal appears to mirror the implementation of these features on the EL which can simply forward them into the Engine API; in turn, the CL then has some additional work to do to map the unified data into the requisite parts.
- Given the fact that CL implementations generally have stronger typing of per-fork types, we landed on this PR making sense and intend to move forward with it.
- CL teams please take a look here to chime in further.

After discussing these request types, we turned to an update on the SSZ stable container EIPs.

- @etan-status gave a great summary of the progress here and proposed we include EIP-7688 and EIP-7495 into Pectra devnet-2.
- I clarified that the purpose of the pectra devnets is to reflect the formally included set of EIPs in Pectra, and so rather than simply including these EIPs in devnet-2, we must first agree to inclusion in Pectra.
- We discussed formal inclusion on the call with a variety of viewpoints: while the benefits of these changes are sound in isolation, there was strong pushback that Pectra is already quite large and the testing and security processes around the hard fork development are already quite strained given the size of the fork.
- There was no strong push for inclusion of these SSZ EIPs on the call and especially in light of the instability of the existing Pectra devnet agreed to focus on hardening the existing fork as specified before moving to consider additional features.

PeerDAS was up after the core Pectra discussions

- There hasn’t been much movement on the peerdas-devnet front, as the last network was not stable and clients have been in the process of hardening implementations before attempting another devnet.
- Acknowledging this, I gave an overview of the option to simplify PeerDAS further by dropping the “sampling” phase of the data availability mechanism of PeerDAS so that we can still have something shipped in Pectra without significantly delaying timelines.

This solution would still have nodes down segments of the blob data and for a small change in some of the PeerDAS parameters still maintains the same security profile as PeerDAS with sampling.

There was interest on further exploring the idea and I’ll write something soon to share more widely beyond the call. Attendees are open to the idea, especially given the broad support for data scaling in Pectra.

This discussion segued into a general discussion of how to arrange PeerDAS alongside the rest of the Pectra features

- The current approach has PeerDAS activated at a separate epoch than the Pectra fork epoch; these two parameters could ultimately be the same but allows for a relatively easy way to “disable” PeerDAS from Pectra in the event development timelines didn’t align with the rest of the Pectra EIP set.
- There were a variety of opinions on the best way to do this so I recommend checking the call for the full color.
- Ultimately, we decided to focus on getting a more stable network around the other Pectra EIPs (cf. devnet-1 stability) and revisit the best way to merge in the PeerDAS work once that is done.

We concluded the call with [a proposal](https://github.com/ethereum/consensus-specs/pull/3845) from [@dapplion](/u/dapplion) to enhance the expressivity of the `BeaconBlocksByRange` networking method — take a look at that PR and please provide any feedback.

### Recording

  [![image](https://img.youtube.com/vi/lmzAUqsIbIE/maxresdefault.jpg)](https://www.youtube.com/watch?v=lmzAUqsIbIE&t=148s)

### Additional info

Notes by [@Christine_dkim](/u/christine_dkim): [Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-consensus-call-138)

## Replies
