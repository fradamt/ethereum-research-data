---
source: magicians
topic_id: 21974
title: All Core Devs - Execution (ACDE) #202, December 19 2024
author: abcoathup
date: "2024-12-05"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-202-december-19-2024/21974
views: 372
likes: 4
posts_count: 2
---

# All Core Devs - Execution (ACDE) #202, December 19 2024

#### Agenda

[Execution Layer Meeting 202 · Issue #1209 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1209) moderated by [@timbeiko](/u/timbeiko)

**
Agenda summary**

by [@nixo](/u/nixo) *(Copied from [Twitter](https://x.com/nixorokish/status/1869110213627818040))*

- Pectra:

Testnet update (who: EL & CL devs)
- New EIP! EIP-7840 introduces a constant blobSchedule in the genesis file, allowing the protocol to define target & max blobs. General support from EL teams. More info in agenda. (who: EL devs)
- Update EIP-7702 to support uint256 chain IDs. Proposed by @Optimism (who: rollups)

**AllCoreDev process improvements**. Change when we move EIPs from “considered for inclusion” to “scheduled for inclusion” *(who: Protocol Support, anyone interested in the process)*
**![:mega:](https://ethereum-magicians.org/images/emoji/twitter/mega.png?v=15) Specific ask**: Should EIP-4444 bump the protocol version or not? Needs input from execution devs. More info in agenda linked above
**General update**: Progress is being made w some contention on when to target for dropping history & should history be dropped in an update or should node operators be given a flag to drop premerge history? & does it require coordination? Most consensus is ‘probably a good idea’ w minority opposition. Suggested target May 1st.
**Oppose removal of NewBlock & NewBlockHashes**. These removals make the protocol incompatible w blockchains that aren’t PoS *(who: [@0xPolygon](https://x.com/0xPolygon), app devs bridging b/t Ethereum & non-merged networks)*
**[EIP-7808](https://eips.ethereum.org/EIPS/eip-7808)**: Meta EIP that reserves a range of tx types for Rollup Improvement Proposals (RIPs) to avoid conflicts w EIPs if using the same identifiers

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #202, December 19 2024](https://ethereum-magicians.org/t/all-core-devs-execution-acde-202-december-19-2024/21974/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> Action Items
> Pectra
>
> EIP-7840 is SFI’d as a replacement to EIP-7742 (PR)
> Pectra system contract audits results to be presented in January
>
> Devnet-5 Changes
>
> Add EIP-7840
> EIP-7702 chain id to u256
> EIP-2537 Gas pricing MAP, MUL and ADD operations
> EIP-2537 Gas pricing pairing operations
> EIP-2537 MSM gas repricing
> EIP-2537 Remove redundant MUL precompiles
> Update EIP-2935 system contract
>
> Other Topics
>
> Discussions about History Expiry rollout to continue in discord, potentially schedule a breakout in…

#### Recording

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/8/89604e441f078f8618e3dfa7d95ad161ff055a76.jpeg)](https://www.youtube.com/watch?v=XtdJ2G8yST4&t=170s)

#### Additional info

- Summary by @nixo
- Crypto & Blockchain Research Reports | Galaxy by @Christine_dkim

## Replies

**timbeiko** (2024-12-19):

# Action Items

## Pectra

- EIP-7840 is SFI’d as a replacement to EIP-7742 (PR)
- Pectra system contract audits results to be presented in January

## Devnet-5 Changes

- Add EIP-7840
- EIP-7702 chain id to u256
- EIP-2537 Gas pricing MAP, MUL and ADD operations
- EIP-2537 Gas pricing pairing operations
- EIP-2537 MSM gas repricing
- EIP-2537 Remove redundant MUL precompiles
- Update EIP-2935 system contract

## Other Topics

- Discussions about History Expiry rollout to continue in discord, potentially schedule a breakout in January
- Re-introduce NewBlock and NewBlockHashes in eth/69 (PR)
- Ensure execution layer specifications support EIP-4803
- PR tying CFI & SFI to denvet inclusion has been merged
- EVM Resource Pricing Working Group
- Two EIPIP call for comments:

Call for Input: Define "Meta" as only relating to processes (effectively excluding hardforks) · Issue #373 · ethcatherders/EIPIP · GitHub
- Call for Input: Forcibly withdraw EIP-7675 · Issue #374 · ethcatherders/EIPIP · GitHub

- Feedback requested on candidate validator nodes requirement definitions

# Call Summary

## Pectra Devnets

- Testing on Mekong still in progress
- Devnet-5 CL specs released
- Initial Kurtosis configs for some clients (Besu, Teku) released

## Pectra Spec

- EIP-7840 is included as a replacement to EIP-7742 (PR)
- Agreed to make EIP-7702 chain_id a u256 value (PR

Agreed to not move forward with this PR: Update EIP-7702: remove chain_id in authorization tuple by fjl · Pull Request #9152 · ethereum/EIPs · GitHub

Agreed to EIP-2537 gas price schedule as well as removing the `MUL` precompiles

- [Gas pricing MAP, MUL and ADD operations](https://github.com/ethereum/EIPs/pull/9097)

- [Gas pricing pairing operations](https://github.com/ethereum/EIPs/pull/9098)

- [MSM gas repricing](https://github.com/ethereum/EIPs/pull/9098)

- [Remove redundant MUL precompiles](https://github.com/ethereum/EIPs/pull/8945/files)
Agreed to [update EIP-2935 system contract](https://github.com/ethereum/EIPs/pull/9144) as per audit recommendations

- Note that the full set of audit results for all Pecrtra systems contract will be presented in early 2025

Progress on [Builder API SSZ support](https://github.com/ethereum/builder-specs/pull/104), still needs to be implemented but can be done in parallel to client development

## History Expiry

- @pipermerriam shared updates on EIP-4444’s rollout plan
- There was general agreement about dropping pre-merge history on May 1st, but a lot of back and forth regarding the implementation and testing details until then. Notably, what eth/  protocols should clients add/change as part of the Pectra hard fork release, if and how to deploy history expiry to testnets prior to mainnet activation, etc.
- Teams agreed to continue the conversation on the R&D discord and potentially have a breakout room in January if things can’t be resolved async

## Decoupling Gas Limit & Payload Size

- @arnetheduck shared a set of proposals to deal with gossip limitations on the consensus layer, a few of which involve adding additional restrictions to the execution layer.
- EL developers were generally against adding size restrictions to blocks in addition to the gas limit, or having a per-transaction gas limit, but further conversation is needed. Teams are encouraged to share their thoughts on the issue directly.

## eth/69

- @yperbasis proposed keeping NewBlock and NewBlockHash as part of the eth/69 networking protocol, as they are useful messages for networks who did not go through The Merge. Ethereum doesn’t broadcast these fields post-merge anyways.
- No objections, OK to merge the PR

## EIP-7503

- Feedback requested on the latest changes to the EIP, no comments on the call.
- @petertdavies highlighted that there are legal considerations people should be mindful of when engaging with these proposals.

## EIP-7508

- This EIP proposes to reserve a transaction range for L2s to adopt different transaction types than L1, similarly to what EIP-7587 did for precompile addresses. No objections to move from Draft to Review.

## EIP-4803

- Confirmed that this EIP has been retroactively applied by client teams, but not in EL specs yet. @petertdavies to open an issue to track this in EELS, but no objections to considering the EIP “applied from genesis”

## Other updates

- PR tying CFI & SFI to denvet inclusion has been merged
- An EVM pricing working group is spinning up in January, more info here

@davidecrapis.eth shared more numbers on the
call

Call for input on two proposed changes to the EIP process

- Call for Input: Define "Meta" as only relating to processes (effectively excluding hardforks) · Issue #373 · ethcatherders/EIPIP · GitHub
- Call for Input: Forcibly withdraw EIP-7675 · Issue #374 · ethcatherders/EIPIP · GitHub

Feedback requested on [candidate validator nodes requirement definitions](https://hackmd.io/@kevaundray/S1hUQuV4Jx)

