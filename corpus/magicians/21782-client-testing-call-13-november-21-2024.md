---
source: magicians
topic_id: 21782
title: Client testing call #13, November 21 2024
author: abcoathup
date: "2024-11-22"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/client-testing-call-13-november-21-2024/21782
views: 86
likes: 0
posts_count: 1
---

# Client testing call #13, November 21 2024

## Summary

Update by [@parithosh](/u/parithosh) *(copied from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1309212045140426773))*

### Pectra

#### pectra-devnet-4

- PK is performing deposit tests on the devnet, more information here: #allcoredevs
- Plan to shut down Monday unless there are objections
- Mekong public testnet is live. If there are new client images to be used, please let us know. Mekong will not be updated to devnet-5 specs.
- devnet-5 spec discussion as well as open PRs, we discussed adding a new field for MAX and TARGET blob counts with the _ELECTRA suffix into the spec config.yaml, to indicate the new values to be used at the fork. This would be consumed by the CL along with other EIPs to communicate the blob change to the EL.

### Peerdas and EOF

- Once devnet-5 spec is out, we will pin these releases for EOF/PeerDAS codebases to rebase on top of

### Additional info

- Summary by @Christine_dkim
- https://pectra-devnet-4.ethpandaops.io/
- https://mekong.ethpandaops.io/
