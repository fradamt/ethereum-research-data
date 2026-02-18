---
source: magicians
topic_id: 20922
title: All Core Devs - Execution (ACDE) #196, September 12 2024
author: abcoathup
date: "2024-08-31"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-196-september-12-2024/20922
views: 438
likes: 4
posts_count: 2
---

# All Core Devs - Execution (ACDE) #196, September 12 2024

#### Agenda

[Execution Layer Meeting 196 · Issue #1143 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1143) moderated by [@timbeiko](/u/timbeiko)

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #196, September 12 2024](https://ethereum-magicians.org/t/all-core-devs-execution-acde-196-september-12-2024/20922/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> Call Summary & Action Items
> Action Items
>
>  Client teams should listen to the call recording concerning a potential Pectra split and come to next ACDC with a view on (1) whether to split or not and (2) if splitting, are there more things beyond the current devnet-3 spec we should urgently include in “Pectra1”?
>  Wallet and tooling developers can use devnet-3 to test EIP-7702
>  @fjl to update the Request Encoding PRs to explicitly specify ordering constraints and the handling of invalid requests, ai…

#### Recording

  [![image](https://img.youtube.com/vi/A_DuQRICW70/maxresdefault.jpg)](https://www.youtube.com/watch?v=A_DuQRICW70&t=248s)

#### Additional info

- pectra scheduling into two forks - HackMD by @ralexstokes
- Crypto & Blockchain Research Reports | Galaxy by @Christine_dkim

## Replies

**timbeiko** (2024-09-12):

# Call Summary & Action Items

## Action Items

- Client teams should listen to the call recording concerning a potential Pectra split and come to next ACDC with a view on (1) whether to split or not and (2) if splitting, are there more things beyond the current devnet-3 spec we should urgently include in “Pectra1”?
- Wallet and tooling developers can use devnet-3 to test EIP-7702
- @fjl to update the Request Encoding PRs to explicitly specify ordering constraints and the handling of invalid requests, aim to get all PRs merged before next week’s ACDC
- Merge Update EIP-7702: 7702 validity by lightclient · Pull Request #8845 · ethereum/EIPs · GitHub and investigate potentially constraining values for v further.
- EL teams should benchmark the EIP-2537 MSM precompiles with concurrency disabled to determine whether the gas cost should be updated.
- Teams should review their bootnodes in mainnet, sepolia and holesky configs, in the respective eth-clients repositories’ PRs.

## Call Summary

### Pectra Scope Changes

*Note: this discussion happened at the end of the call but was the most consequential, so I’ve moved its summary to the top.*

On the last ACDE, we discussed multiple potential additions to Pectra. On today’s call, we planned to determine which EIPs among these should be included: [Update EIP-7600: Update eip-7600.md by timbeiko · Pull Request #8846 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8846)

As we began discussing the potential inclusion of EIP-7742 and 7623, which had been supported ahead of time by some client teams, concerns about the overall scope of Pectra were raised.

**[@ralexstokes](/u/ralexstokes) and [@parithosh](/u/parithosh) proposed that we consider splitting Pectra in two forks, as it would simplify spec and testing work.**  There was a lot of back and forth about what this could look like (strongly recommend watching the recording for the nuance!). A few noteworthy comments:

- @adietrichs emphasized that if we split Pectra, then we should ship “Pectra 1” ASAP, ideally in early 2025
- I supported the change, arguing that shipping Pectra in two parts would likely result in an overall shorter delivery time, as testing complexities grows super-linearly as more EIPs are added.
- There were concerns raised that if we split Pectra in two forks, we’d open the door to several new EIPs being included in the second fork, slowing things down again in a few months. There seemed to be rough agreement that we should limit the scope of “both” Pectra forks to what is already being considered for Pectra, and no more.
- @shemnon suggested that we could use the current devnet-3 spec as the basis for Pectra 1, and then devnet-4 onwards could be rebased on Pectra 1 and be the basis for Pectra 2.

devnet-3 currently has all Included Pectra EIPs (EIP-7600: Hardfork Meta - Pectra) except EOF and PeerDAS, which would be scheduled for Pectra 2.

[@gballet](/u/gballet) raised concerns that this would delay Verkle, as teams would not start spending significant effort on it if another fork was scheduled prior to it. He also felt that Verkle was being held to a higher standard than other EIPs, notably EOF, when debating its inclusion.

There seemed to be broad consensus that splitting Pectra was the best path forward, but due to the significance of the decision and many details to think through, we agreed to give teams the week to think through the options. We hope to make a decision about the this on next week’s ACDC.

Aside from whether Pectra should be split or not, teams should consider which Proposed EIPs should potentially be included in the first vs. second fork.

---

*post-call note: [@ralexstokes](/u/ralexstokes) shared his thoughts [here](https://hackmd.io/@ralexstokes/rJVuKtlpR).*

### Pectra devnet-3

- devnet-3 is live! Wallet & tooling developers can use it to test EIP-7702!
- The main spec changes are updates to EIP-7702 and validator consolidations. Both have been tested on the devnet.
- Some issues were found in EthereumJS and Nethermind. Nethermind issues are fixed, and EthJS is being worked on.
- We confirmed the EL spec test version to use for the devnet is v1.5.0

### Pectra Request Encoding Changes

On the last ACDC, [@fjl](/u/fjl) proposed changing the way requests are encoded by system contracts to be flat rather than RLP-encoded. This would simplify the EL implementations, as they would not need an extra layer of encoding and could continue passing the EL payload in client internals without context about the current fork.

Prior to ACDE, he made PRs to the relevant EIPs to propose the changes:

- Update EIP-7685: change requests hash to flat hash EIPs#8854
- Update EIP-7002: change request to flat encoding EIPs#8855
- Update EIP-6110: change request to flat encoding EIPs#8856
- Update EIP-7251: change request to flat encoding EIPs#8857

[@potuz](/u/potuz) commented that if the EL passes the data as a single list for all requests in a block, CL clients will then need to parse it to determine which requests map to which feature. @tersec raised similar concerns [on the Engine API PR](https://github.com/ethereum/execution-apis/pull/577#issuecomment-2342387462) earlier this week. Felix emphasized that removing this responsibility from the EL would lead to significant simplifications, which Reth agreed with.

In addition to this, @tersec had concerns that the EIPs as currently specified did not enforce a strict ordering of the requests in a block, or deal with the cases of invalid requests. A few EL devs confirmed that the implementation of the EIP does produce a deterministic ordering, but [@fjl](/u/fjl) agreed to make this more explicit in the EIP and Engine API. We also agreed that if a request is deemed invalid by the CL, it should invalidate the entire block, similarly to other cases where the EL returns an `INVALID` response through the Engine API.

There were also some concerns that this approach is not future-proof w.r.t SSZ, but we agreed these were not blocking.

### EIP-7702 Validity Checks

[@yperbasis](/u/yperbasis) raised concerns that the current validity checks in EIP-7702 were inconsistent with those in EIP-2, and [a PR to address this](https://github.com/ethereum/EIPs/pull/8865).

[@matt](/u/matt) already had a PR updating the validity checks for the EIP: [Update EIP-7702: 7702 validity by lightclient · Pull Request #8845 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8845)

Olivier from Reth noted that the bound on `v` in Matt’s PR could likely be made smaller than 2^256, and that the value being too big had minor performance implications. The constraint was chosen because it mirrors the constraint for all other transaction types.

We agreed to move forward with Matt’s PR and investigate whether we should restrict the `v` validity check further separately.

### BLS MSM Precompile Pricing

[@jwasinger](/u/jwasinger) ran benchmarks on the BLS-12381 precompiles and found that “MSM precompiles are underpriced compared to the other EIP-2537 precompiles when concurrency is disabled.” See the full benchmarks here: [GitHub - jwasinger/eip2537-evm-benchmarks: Cross-client EVM Benchmarks for EIP-2537](https://github.com/jwasinger/eip2537-evm-benchmarks?tab=readme-ov-file#geth-benchmark-results)

He argued we should not create a precedent of setting gas prices based on parallel execution, and suggested doubling the entires in the [discount table](https://eips.ethereum.org/EIPS/eip-2537#g1g2-msm).

We agreed to benchmark this on all EL clients and, if the performance is similar across them, raise the gas prices as suggested by Jared. Jared has already converted his benchmarks to static tests for other teams to use. Additionally, Nethermind shared their own benchmarking tool: https://github.com/NethermindEth/gas-benchmarks

### Network Config Updates

[@pk910](/u/pk910) has been aligning the configuration structure across mainnet, Holesky and Sepolia and invites teams to review the bootnodes that are currently listed:

- Align config structure with other public testnet repositories by pk910 · Pull Request #1 · eth-clients/mainnet · GitHub
- Align config structure with other public testnet repositories by pk910 · Pull Request #111 · eth-clients/holesky · GitHub
- Align config structure with other public testnet repositories by pk910 · Pull Request #89 · eth-clients/sepolia · GitHub

