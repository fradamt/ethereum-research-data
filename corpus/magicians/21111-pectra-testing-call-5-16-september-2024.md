---
source: magicians
topic_id: 21111
title: Pectra testing call #5, 16 September 2024
author: abcoathup
date: "2024-09-17"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/pectra-testing-call-5-16-september-2024/21111
views: 88
likes: 1
posts_count: 1
---

# Pectra testing call #5, 16 September 2024

#### Summary

Update by [@parithosh](/u/parithosh) *(from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1285250566657675336))*

##### pectra:

- pectra-devnet-3 is live! Find details here: https://pectra-devnet-3.ethpandaops.io/
- Nethermind, lodestar, erigon bugs have been patched, network is at ~92% participation
- EthereumJS is having issues, Are clients providing requestBytes as an array as per EIP-7685? info here: ⁠devnet-3 issues (EthereumJS)⁠
- We need someone to update the builder-specs such that we can have client teams start/work on implementations: GitHub - ethereum/builder-specs: Specification for the external block builders.
- Remote signer API needs updating for pectra as well, is someone working on this: GitHub - ethereum/remote-signing-api: This repository outlines standard remote signing application programming interface (APIs) for communication between remote signers and Ethereum validator clients. Remote signing service allows validator clients to offload signing of validation duties (e.g Attestations, BeaconBlocks) by managing security, slashing protection, and key management., info here: ⁠apis⁠

##### eof :

- Testing is going well and more clients are achieving readiness for a devnet
- Devnet would depend on fork split decision, likely at ACD this week
- We’d do interleaved devnets, so eof-devnet-0… and a decision needs to be made if its done as prague or as osaka
- We’d need to be careful not to trigger the same bugs as pectra devnets to reduce debugging overhead. One approach would be to remove the faucet (we plan this for peerDAS), but the downside is that EOF would benefit a lot from public testing

##### peerDAS :

- Update on local devnet and its issues
- Lodestar endianness bug
- Public devnets once local issues are triaged
- Devnet cycle would depend on fork split decision made likely during ACD this week

##### fuzzing :

- Marius would focus on pectra fuzzing and bad block generators (also open call for other clients to implement this and take some load off of him/speed up the fork)

##### general :

- We had a brief temp check on fork splitting and what open tasks that would make shipping quickly a blocker
