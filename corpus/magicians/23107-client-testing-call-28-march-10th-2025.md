---
source: magicians
topic_id: 23107
title: Client Testing Call #28, March 10th 2025
author: danceratopz
date: "2025-03-10"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/client-testing-call-28-march-10th-2025/23107
views: 133
likes: 3
posts_count: 1
---

# Client Testing Call #28, March 10th 2025

## Sepolia Pectra Fork

[@MariusVanDerWijden](/u/mariusvanderwijden) wrote-up a concise [full incident report](https://mariusvanderwijden.github.io/blog/2025/03/08/Sepolia/), otherwise here’s an overview:

- An issue encountered shortly after the hardfork caused empty blocks on the network.
- Blocks containing deposit transactions triggered an issue in clients which caused blocks to be invalided. The root cause was unexpected log emissions from the Sepolia deposit contract (which are not present in mainnet’s deposit contract). This difference is due to deposits being token-gated on Sepolia; depositors must additionally send an ERC20 in order to successfully deposit. This triggered an additional log emission, which was not accounted for by clients, resulting in the block containing deposit txs being invalidated.
- The patch was relatively simple. Clients agreed to filter out irrelevant logs emitted by the deposit contract.
- Coordinated rollout from client teams and ethpandaops at 14 UTC → network finalized, blocks correctly produced, no other issues observed.

See the Pectra discussion below for a suggestion how to formalize deposit behavior in the EIP-6110.

Ethpandaops:

- The assertoor tests haven’t been executed on Sepolia yet.
- The deposit tests are made from a fresh wallet which doesn’t work due to the token gated deposit contract.
- This needs a small fix, but should be done this week.

Nethermind:

- As of today: Some users reporting client crashes related to a BLST library.
- Probably due to some hardware acceleration not implemented across all CPUs in this library.
- Issue only discovered today, will provide more details in #allcoredevs soon in case other clients depend on the same library.

## Sepolia Network Pectra Fork Update

Ethpandaops Summary:

- Almost reached finality early on March 10th: 64% finality reached:

https://light-holesky.beaconcha.in/epoch/118937 (thanks for the link, Roman!)

We will try to achieve finality over the next few days.

- Plan A: Is still to get Holesky to finalize.
- Plan B: Holesky shadow fork (but only if finality not achieved within next few days).

Bottleneck seems to be attestation propagation, if resolved, we should have enough validators online to finalize.
All 7702 testing can continue continue on Sepolia

Lodestar:

- Found bug in attesting processing leading to bad aggregates and missing attestations.
- Node is otherwise stable and following head.

Relevant Eth R&D discussion in the [Holesky attestations thread](https://discord.com/channels/595666850260713488/1347536232695205898), Ethereum R&D [interop](/tag/interop) channel.

## Pectra

### BLS Precompile Issues

Bugs found in Nethermind and evmone as part of the ongoing bug bounty (Clarification: evmone is not running in Erigon3 with a Pectra config).

Summary available here: [BLS12-381 Pairing Consensus Issue](https://ethereum-magicians.org/t/bls12-381-pairing-consensus-issue/23019)

EEST:

- The missing test vectors have been added to the EIP and now have been included in EEST. Other related PRS can be found here, if interested: chore(tests): update bls12 test vectors by spencer-tb · Pull Request #1289 · ethereum/execution-spec-tests · GitHub
- New EEST release is planned today/tomorrow.

### Deposit Event Update for EIP-6110

EthereumJS, [@jochem-brouwer](/u/jochem-brouwer):

- Added a suggestion to update EIP-6110 with deposit data parsing spec
- Discussion in this thread in #allcoredevs.

## PeerDAS

Ethpandaops:

- Devnet-5 is up and running. we’re doing some potion of the network as full sync and we tested genesis sync (and its working).
- More stress tests coming for PeerDAS

## EOF

Ipsilon:

- Working on the EOF devnet plan.
- Working on eof-devnet-1 this week (still at least 2 weeks out).
- All essential EOF features will be included in eof-devnet-1.
- Will add 3 more EIPs to be potentially included for eof-devnet-2, but these are optional, based on ACD decisions and timeline.
