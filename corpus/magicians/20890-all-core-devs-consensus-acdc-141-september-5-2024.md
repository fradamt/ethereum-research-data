---
source: magicians
topic_id: 20890
title: All Core Devs - Consensus (ACDC) #141, September 5 2024
author: abcoathup
date: "2024-08-25"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-141-september-5-2024/20890
views: 124
likes: 1
posts_count: 1
---

# All Core Devs - Consensus (ACDC) #141, September 5 2024

#### Agenda

[Consensus-layer Call 141 · Issue #1140 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1140) moderated by [@ralexstokes](/u/ralexstokes)

#### Summary

Summary by [@ralexstokes](/u/ralexstokes) *(from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1281347130992365588))*

- Started with Pectra

devnet-2 around for debugging, but deprecated soon

finality bug in Prysm was identified over the weekend and fixed

devnet-3 soon™!

- some clients ready, others ready in next few days
- may start devnet with all prepared clients next week, others can join as soon as they are ready

Next covered some updates to Pectra EIPs

- One for EIP-7251 correlated slashing computation, merged!
- Another for handling execution layer requests in the beacon chain (multiple EIPs)

a small bookkeeping issue but should be merged in next few days

Turned to a discussion around how to best handle the passing of request data from the EL to CL

- covers several EIPs in Pectra
- Felix has this PR to present an option with a minimal number of transformation steps by extracting data from the EL as SSZ and then passing directly to the CL
- good support from CL devs, will decide on next ACDE

Then looked at a PR to update EIP-6110 so that deposit requests from the EL are buffered in a way to prevent CL-layer DoS concerns

- One open question left around interactions with the MaxEB feature; client teams please take a look so we can merge this in ASAP!

Wrapped the Pectra section with a temperature check on two PRs to update EIP-7549

- further refinement of EIP-7549 features to simplify implementation and make it easier to secure both chain data and network traffic
- general support from participants, and need a bit more work before we can merge

And then, PeerDAS

- some early success with a subset of clients on a local devnet on the path to peerdas-devnet-2
- clients generally under way to launch peerdas-devnet-2
- Turned to discuss an issue around timing of PeerDAS proof generation and local block building (where we assume some nodes may have fewer resources available)

Work towards peerdas-devnet-2 identified a hotspot in proof generation performance
- Some proposed solutions from asn here: ⁠data-availability-sampling⁠
- There was a fairly active conversation about all of the considerations here, as we intend to achieve a performant data facility for any node regardless of size/resource supply; so check the call for the full details!
- But ultimately, settled on a near-term and longer-term solution. Exploration of both solutions would be helped by a spec so expect to see something along these lines soon.
- Near-term: go w/ “option 3” linked above, which keeps proof generation on the CL with a richer interface b/t EL and CL during local block building
- Longer-tem: explore more decentralized block + blob building regimes where lower resourced nodes can leverage higher resourced nodes on the network to assist in blob distribution

see ⁠data-availability-sampling if you want to engage with the discussion here!

Wrapped the call with a discussion around the “union” feature in SSZ

- currently part of the specification, but has never been used in a “production” setting and so relatively under-developed and under-tested
- there’s demand to remove or mark them as “experimental” to reduce the design space (in a helpful way!) when discussing various EIPs or client implementations
- will continue the discussion on the PR: Remove SSZ unions by tersec · Pull Request #3906 · ethereum/consensus-specs · GitHub and likely to do something here to make their status clearer in the specs

#### Recording

  [![image](https://img.youtube.com/vi/XMPupRyEBk0/maxresdefault.jpg)](https://www.youtube.com/watch?v=XMPupRyEBk0&t=69s)

#### Additional info

**Notes**: [Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-consensus-call-141/) by [@Christine_dkim](/u/christine_dkim)
