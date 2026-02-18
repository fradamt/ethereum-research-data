---
source: magicians
topic_id: 20648
title: All Core Devs - Execution (ACDE) #193, August 1 2024
author: abcoathup
date: "2024-07-27"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-193-august-1-2024/20648
views: 919
likes: 10
posts_count: 4
---

# All Core Devs - Execution (ACDE) #193, August 1 2024

#### Agenda

[Execution Layer Meeting 193 · Issue #1104 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1104) moderated by [@timbeiko](/u/timbeiko)

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #193, August 1 2024](https://ethereum-magicians.org/t/all-core-devs-execution-acde-193-august-1-2024/20648/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDE Call Summary
> Highlights & Action Items
>
> devnet-2 spec stays as-s
> devnet-3 will contain the latest EIP-7702 changes, and possibly other minor tweaks, but no other major feature addition such as EOF
>
> EOF devnet readiness to be discussed on ACDE#194
>
>
> General support for engine_getBlobsV1, with the caveat that the honest validator spec should be updated to define the recommended usage. @tbenr / Teku will open a PR about this in the next few days and a final decision is expected on next week’s …

#### Recording

  [![image](https://img.youtube.com/vi/vbh9C2_-TIc/maxresdefault.jpg)](https://www.youtube.com/watch?v=vbh9C2_-TIc&t=140s)

### Additional info

- Slides EIP-7736 (Leaf-level State Expiry) - Google Präsentationen
- Notes: Crypto & Blockchain Research Reports | Galaxy by @Christine_dkim

## Replies

**timbeiko** (2024-08-01):

# ACDE Call Summary

## Highlights & Action Items

- devnet-2 spec stays as-s
- devnet-3 will contain the latest EIP-7702 changes, and possibly other minor tweaks, but no other major feature addition such as EOF

EOF devnet readiness to be discussed on ACDE#194

General support for [engine_getBlobsV1](https://github.com/ethereum/execution-apis/pull/559), with the caveat that the honest validator spec should be updated to define the recommended usage. [@tbenr](/u/tbenr) / Teku will open a PR about this in the next few days and a final decision is expected on next week’s ACDC.
No decision on including EIP/RIP-7212. To improve the likelihood of the EIP’s inclusion, its champions should extend testing coverage to match other currently included Pectra EIPs.
Discussions of Ethereum’s overall quantum resistance readiness should continue in the [#cryptography channel of the R&D discord](https://discord.gg/BsPm3Ncc).
Discussions of possible alternatives to Verkle Trie are welcome in the [Verkle Implementers calls](https://github.com/ethereum/pm/issues/1121). If other alternatives are to be seriously explored, we should start looking into them now.
[New state expiry proposal](https://notes.ethereum.org/@gballet/leaf-level-state-expiry) → discussion to continue on [EthMagicians](https://ethereum-magicians.org/t/eip-7736-leaf-level-state-expiry-in-verkle-trees/20474)
[@parithosh](/u/parithosh) has added EIP-7463 proofs to his [4444 torrent prototype](https://ethresear.ch/t/torrents-and-eip-4444/19788/17)

## Recap

*Note: this is based on my rough, imperfect notes. For the full context/nuance, please watch the recording.*

### Pectra

#### devnets

- devnet-1 launched last week, but issues with 7702 led to several forks, making it hard to diagnose bugs
- devnet-2 was launched this week to sidestep these issues and focus on other EIPs given the pending spec changes for 7702. It has the same spec as devnet-1, but testing explicitly omits interacting with 7702.
- Several bugs have been found on devnet-2, with some fixed (e.g. an Erigon block production issue) and more in-progress.
- devnet-2 is currently in a healthy state

#### EOF

- EOF implementations are currently being fuzzed against each other and more tests are still being written. Not ready to include in devnets yet, but worth discussing again in two weeks.

#### EIP-7702

- There was another 7702 breakout this week. Biggest decision made is to restrict 7702 to temporarily extending EOA’s functionality, and not use the EIP to also introduce permanent EOA → Smart Contract Account migration.
- With the latest merged PR, the spec is roughly stable. This should be the target for future devnets.
- Open question: should 7702 allow introspection into the delegated contract? Should it restrict delegation to EOF addresses?

No firm answer, but @shemnon’s instinct is that the behaviour should match the type of contract the account delegates to. If it’s an EOF contract, then no introspection. If not, then OK to allow it.
- Best way to determine this is to see them both on a devnet and think more deeply about the interactions.

The latest 7702 spec will be the main change for devnet-3. Other small things may also be added, but no additional large EIPs.

#### EIP-6110 requests objects encoding

- @fjl pointed out that EIP-6110 request objects are currently JSON encoded, which means the object needs to be read to determine the proper encoding scheme. He proposed to instead have EL clients SSZ encode the objects before sending them over the Engine API.
- While this would require EL clients to add SSZ support, the change is simple enough that implementing it from scratch isn’t too different from the work required for the current JSON encoding. Teams could possibly support this even if there are no good libraries in their language.
- @mkalinin pointed out that several SSZ libraries still lack support for union types, which would be required.
- Other teams were generally supportive, but hadn’t reviewed the change extensively.
- I highlighted that given the amount of things we have to do for Pectra, it’s probably best to wait until we are farther along in the process to decide if we’d like to do this. Teams already have JSON implementations complete. We won’t be moving forward with this change for now.

#### engine_getBlobsV1

- @michaelsproul proposed a new Engine API method for CL clients to obtain blobs directly from their EL rather than the p2p network: https://github.com/ethereum/execution-apis/pull/559
- Teams were generally supported, but @tbenr flagged that this could potentially be abused. Validators could be bad peers by refusing to broadcasts any blobs they can get directly from their EL. Assuming the feature doesn’t get used this way, there were no objections. @tbenr volunteered to extend the honest validator specs to specify the recommended usage of the method in the next few days. Teams can review both changes and make a final decision on next week’s ACDC.

### EIP/RIP-7212

- On ACDE#192, we hoped to make a decision about 7212’s inclusion on this ACDE.
- Besu, Erigon, and Nethermind were in favour of including it, but @matt questioned the urgency of making a decision about it now vs. when Pectra implementations are farther along.
- I agreed with Matt’s skepticism on the urgency. I highlighted that Pectra is already the largest fork we’ve ever taken on and that the testing team is still working on adding coverage for included EIPs.
- @ulerdogan shared the current tests for the EIP, which are far less comprehensive than what Pectra EIPs require. @marioevz said that reviewing/importing these tests into the cross-client suites would require a non-trivial amount of work.
- Given this, we agreed to not include the EIP in Pectra for now and make a decision at a later date, when we have a better sense of other EIP’s readiness. The 7212 champions are encouraged to extend the testing coverage of the EIP to increase the likelihood we can include it in the fork.
- In addition to the testing concerns, @Nerolation shared his discomfort with enshrining a curve which is rumoured to possibly be backdoorded by the US government.

## Quantum & Verkle

Following an [EthCC talk](https://ethcc.io/archive/a-keynote-with-Vitalik-Buterin) by [@vbuterin](/u/vbuterin), [@yperbasis](/u/yperbasis) raised two quantum computing questions on the call agenda:

> How feasible/practical is this theoretical vulnerability and what would be concrete consequences of a successful attack?
> Is it possible to have something similar to Vekle, but quantum-resistant? Shouldn’t we upgrade to that directly, given that the danger might become imminent only in a few years?

- @gballet confirmed that Verkle was quantum-insecure, and that the cryptographic properties that provide quantum resistance are partially at odds with many of the desirable properties of Verkle (e.g. small proofs, homomorphic encryption, etc.)
- @fjl pointed out that Ethereum in general, beyond Verkle, was vulnerable to quantum computing breaking elliptic curve cryptography, as it is used in many parts of the protocol
- @ihagopian highlighted this was already a concern for blobs, which rely in quantum-insecure cryptography for KZG commitments.
- We agreed that we would not solve Ethereum’s quantum resistance problems on the call. The conversation will continue in the #cryptography channel of the R&D discord.

#### Verkle Alternatives

- Following up on credible alternatives for Verkle, @gballet said he was aware of a few possible ideas, but that nothing had been specified or developed to the level of providing a credible alternative to Verkle. He invited people to discuss this further in the Verkle Implementers calls.
- @potuz asked whether we could commit to changing Ethereum’s state trie in Osaka, but not on the specific format? @adietrichs objected that many alternatives may take a few more years to develop and we may want to simply wait for them to be ready instead of doing a trie migration now.
- Following this, there was some back and forth about the relative importance of state vs. history growth.

### EIP-7736

- @weiihann presented a new scheme for state expiry: EIP-7736

note: presentation link missing

The EIP uses a novel approach, where it only expires leaf nodes in the state trie, rather than full sets of branches. This reduces the complexity of implementing the change, including removing the need for address space extension (!!), and is fully backwards-compatible with Verkle. The EIP works best with “flat tries” such as Verkle Tries, given they have a higher ratio of leaf to branch nodes.  The EIP does not strictly bound state growth, but slows it significantly, which may be a reasonable compromise. How clients handle the expired trie leafs is left up to them.
The Besu team raised concerns about state expiry in general, arguing that it can complicate UX for users who want to independently maintain their state proofs. I conceded this point and emphasized that all state expiry proposals assumed that users would either store their own state or fetch it from a third party. The only alternative is something like state rent, where an address could opt-in to pay the network to not have its state pruned. Work on Portal Network was also mentioned as a potential out of protocol solution to distribute state.
[@weiihann](/u/weiihann) encouraged people to continue the discussion on the [EthMagicians thread](https://ethereum-magicians.org/t/eip-7736-leaf-level-state-expiry-in-verkle-trees/20474).

### EIP-4444

- @parithosh has been working on a 4444 torrent prototype and recently added EIP-7463 proofs to it. Follow the discussion here.

---

**abcoathup** (2024-08-02):

### EIP-7736 presentation



      [docs.google.com](https://docs.google.com/presentation/d/1zCTf54E7OaMrppUeA_T2S4YWvvgGixvlGt4j0E0s1zg/edit)



    https://docs.google.com/presentation/d/1zCTf54E7OaMrppUeA_T2S4YWvvgGixvlGt4j0E0s1zg/edit

###

EIP-7736 Leaf-Level State Expiry Guillaume Ballet (@gballet), Wei Han Ng (weiihann)

