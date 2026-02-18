---
source: magicians
topic_id: 16809
title: Pectra Network Upgrade Meta Thread
author: timbeiko
date: "2023-11-28"
category: Magicians > Process Improvement
tags: [prague-candidate]
url: https://ethereum-magicians.org/t/pectra-network-upgrade-meta-thread/16809
views: 19951
likes: 232
posts_count: 77
---

# Pectra Network Upgrade Meta Thread

## May 22 Update

**From [EIP-7600: Hardfork Meta - Pectra](https://eips.ethereum.org/EIPS/eip-7600):**

> ### EIPs Included
>
>
>
> EIP-2537: Precompile for BLS12-381 curve operations
> EIP-2935: Save historical block hashes in state
> EIP-3074: AUTH and AUTHCALL opcodes
> EIP-6110: Supply validator deposits on chain
> EIP-7002: Execution layer triggerable exits
> EIP-7251: Increase the MAX_EFFECTIVE_BALANCE
> EIP-7549: Move committee index outside Attestation
> EIP-7685: General purpose execution layer requests
>
>
>
> ### EIPs Considered for Inclusion
>
>
>
> EIP-7212: Precompile for secp256r1 Curve Support
> EIP-7547: Inclusion lists
> EIP-7623: Increase calldata cost
> EOF EIPs listed as part of EIP-7692, namely:
>
> EIP-663: SWAPN, DUPN and EXCHANGE instructions
> EIP-3540: EOF - EVM Object Format v1
> EIP-3670: EOF - Code Validation
> EIP-4200: EOF - Static relative jumps
> EIP-4750: EOF - Functions
> EIP-5450: EOF - Stack Validation
> EIP-6206: EOF - JUMPF and non-returning functions
> EIP-7069: Revamped CALL instructions
> EIP-7480: EOF - Data section access instructions
> EIP-7620: EOF Contract Creation
> EIP-7698: EOF - Creation transaction

### Other Pectra Proposals

- EIP-3068: Precompile for BN256 HashToCurve Algorithms
- EIP-5806: Delegate transaction
- EIP-5920: PAY opcode
- EIP-6404: SSZ Transactions Root
- EIP-6465: SSZ Withdrawals Root
- EIP-6466: SSZ Receipts Root
- EIP-6493: SSZ Transaction Signature Scheme
- EIP-6913: SETCODE instruction
- EIP-6914: Reuse validator indices
- EIP-7702: Set EOA account code for one transaction
- EIP-7212: Precompile for secp256r1 Curve Support
- EIP-7377: Migration Transaction
- EIP-7545: Verkle proof verification precompile
- EIP-7553: Separated Payer Transaction
- EIP-7557: Block-level Warming
- EIP-7594: PeerDAS - Peer Data Availability Sampling
- EIP-7609: Decrease TLOAD/TSTORE pricing for common cases
- EIP-7623: Increase calldata cost
- EIP-7664: Access-Key opcode
- EIP-7667: Raise gas costs of hash functions
- NONREENTRANT & REENTRANT opcodes

** April 10 Update **

*Note: I accidentally removed EOF from the proposals list as part of my March 28 update. Fixed on April 5th. Also including EIP-7667 to the list which was [recently proposed](https://github.com/ethereum/pm/issues/997#issuecomment-2028566664)*

**From [EIP-7600: Hardfork Meta - Pectra](https://eips.ethereum.org/EIPS/eip-7600):**

> #### EIPs Included
>
>
>
> EIP-2537: Precompile for BLS12-381 curve operations
> EIP-6110: Supply validator deposits on chain
> EIP-7002: Execution layer triggerable exits
> EIP-7251: Increase the MAX_EFFECTIVE_BALANCE
> EIP-7549: Move committee index outside Attestation
>
>
>
> #### EIPs Considered for Inclusion
>
>
>
> EIP-7547: Inclusion lists

### Other Pectra Proposals

- EOF (megaspec, implementation matrix)
- EIP-2935: Save historical block hashes in state
- EIP-3068: Precompile for BN256 HashToCurve Algorithms
- EIP-3074: AUTH and AUTHCALL opcodes
- EIP-5806: Delegate transaction
- EIP-5920: PAY opcode
- EIP-6404: SSZ Transactions Root
- EIP-6465: SSZ Withdrawals Root
- EIP-6466: SSZ Receipts Root
- EIP-6493: SSZ Transaction Signature Scheme
- EIP-6913: SETCODE instruction
- EIP-6914: Reuse validator indices
- EIP-7212: Precompile for secp256r1 Curve Support
- EIP-7377: Migration Transaction
- EIP-7545: Verkle proof verification precompile
- EIP-7553: Separated Payer Transaction
- EIP-7557: Block-level Warming
- EIP-7594: PeerDAS - Peer Data Availability Sampling
- EIP-7609: Decrease TLOAD/TSTORE pricing for common cases
- EIP-7623: Increase calldata cost
- EIP-7664: Access-Key opcode
- EIP-7667: Raise gas costs of hash functions

### Post-Pectra Proposals

#### Execution Layer: Osaka

From [EIP-7607: Hardfork Meta - Osaka](https://eips.ethereum.org/EIPS/eip-7607):

> #### Considered for Inclusion
>
>
>
> EIP-4762: Statelessness gas cost changes
> EIP-6800: Ethereum state using a unified verkle tree
> EIP-6873: Preimage retention
> EIP-7545: Verkle proof verification precompile

#### Consensus Layer: F-Star

Likely focus on [EIP-7594: PeerDAS - Peer Data Availability Sampling](https://github.com/ethereum/EIPs/pull/8105)

---

** February 5, 2024 Update **

- Prague/Electra Meta EIP PR

EIPs 6110, 7002 and 7549 Included
- EIP-2537 CFI’d

Verkle Tries included in post-Prague EL fork, Osaka
EIP-4444 work to continue in parallel to network upgrades
[CL proposal tracker](https://github.com/ethereum/consensus-specs/issues/3449)
Other EL proposals, in order of appearance here:

- EVM Object Format (EOF)
- EIP-3074: AUTH and AUTHCALL opcodes
- EIP-3068: Precompile for BN256 HashToCurve Algorithms
- EIP-6913: SETCODE instruction
- Increase codesize limit to 2**16
- EIP-7251: Increase the MAX_EFFECTIVE_BALANCE
- EIP-7377: Migration Transaction
- EIP-7547: Inclusion Lists
- EIP-7212: Precompile for secp256r1 Curve Support
- EIP-5920: PAY opcode
- EIP-7553: Separated Payer Transaction
- EIP-5806: Delegate transaction
- EIP-7609: Decrease TLOAD/TSTORE pricing for common cases
- EIP-6404: SSZ Transactions Root
- EIP-6465: SSZ Withdrawals Root
- EIP-6466: SSZ Receipts Root
- EIP-7557: Block-level Warming

---

** January 15, 2024 Update **

## Jan 15, 2024 Update

Proposals so far, in order of appearance, highlighting if they are for the [EL], [CL] or [EL+CL]:

- [EL] EIP-2537: Precompile for BLS12-381 curve operations
- [EL] EVM Object Format (EOF)
- [EL+CL] EIP-7002: Execution layer triggerable exits
- [EL] Verkle Trees
- [CL] EIP-7549: Move committee index outside Attestation
- [EL] EIP-3074: AUTH and AUTHCALL opcodes
- [EL]  EIP-3068: Precompile for BN256 HashToCurve Algorithms
- [EL+CL] EIP-6110: Supply validator deposits on chain
- [EL] EIP-6913: SETCODE instruction
- [EL] Increase codesize limit to 2**16
- [CL]  EIP-7251: Increase the MAX_EFFECTIVE_BALANCE
- [EL] EIP-7377: Migration Transaction
- [EL+CL] EIP-4444: Bound Historical Data in Execution Clients
- [EL+CL] EIP-7547: Inclusion Lists
- [EL] EIP-7212: Precompile for secp256r1 Curve Support
- [EL] EIP-5920: PAY opcode
- [EL] EIP-7553: Separated Payer Transaction
- [CL] EIP-7594: PeerDAS

Additionally, here are extra proposals from the [CL Github issue](https://github.com/ethereum/consensus-specs/issues/3449):

- EIP-6404: SSZ Transactions Root
- EIP-6465: SSZ Withdrawals Root
- EIP-6466: SSZ Receipts Root
- EIP-6914: Reuse validator indices

---

** December 19, 2023 Update **

## Dec 19th Update

Given the activity here, I’ll compile the proposals to date, in order of appearance, highlighting if they are for the [EL], [CL] or [EL+CL]:

- [EL] EIP-2537: Precompile for BLS12-381 curve operations
- [EL] EVM Object Format (EOF)
- [EL+CL] EIP-7002: Execution layer triggerable exits
- [EL] Verkle Trees
- [CL] EIP-7549: Move committee index outside Attestation
- [EL] EIP-3074: AUTH and AUTHCALL opcodes
- [EL]  EIP-3068: Precompile for BN256 HashToCurve Algorithms
- [EL+CL] EIP-6110: Supply validator deposits on chain
- [EL] EIP-6913: SETCODE instruction
- [EL] Increase codesize limit to 2**16
- [CL]  EIP-7251: Increase the MAX_EFFECTIVE_BALANCE
- [EL] EIP-7377: Migration Transaction
- [EL+CL] EIP-4444: Bound Historical Data in Execution Clients

Additionally, here are extra proposals from the [CL Github issue](https://github.com/ethereum/consensus-specs/issues/3449):

- EIP-6404: SSZ Transactions Root
- EIP-6465: SSZ Withdrawals Root
- EIP-6466: SSZ Receipts Root
- EIP-6914: Reuse validator indices

---

** Orignal Post  **

With Dencun wrapping up, the time has come to start thinking about the Prague/Electra upgrade. Similarly to [Cancun](https://ethereum-magicians.org/t/cancun-network-upgrade-meta-thread/12060), I propose using this thread to discuss the overall process and scope of the upgrade.

EIP champions can use the [prague-candidate](https://ethereum-magicians.org/tag/prague-candidate) tag to signal their desire for inclusion in the upgrade. Note that the consensus layer teams already have [a Github issue](https://github.com/ethereum/consensus-specs/issues/3449) to track proposals.

---

As for larger process tweaks, my #1 suggestion is to  **bring back Meta EIPs.**

There currently is no good place to track the full scope of a network upgrade prior to it being deployed and announced in a blog post.

For Dencun, we have EL EIPs in a [hard to find markdown file](https://github.com/ethereum/execution-specs/blob/master/network-upgrades/mainnet-upgrades/cancun.md) and CL EIPs as part of the [Beacon Chain spec](https://github.com/ethereum/consensus-specs/blob/dev/specs/deneb/beacon-chain.md#introduction).

This isn’t great, as both of these are somewhat hard to find, each of them uses a separate “format” and it results in duplication. With ERC and EIPs now separate, I suggest (going back to) using Meta EIPs to track EIPs included in network upgrades.

For coupled upgrades, the EL + CL could share a single Meta EIP, and for de-coupled upgrades, they could each have their own. If an upgrade goes from coupled to de-coupled or vice-versa, we can simply create a new Meta EIP which superceeds the previous one.

---

Lastly, as a “stretch goal”, we should agree on what to do with [“Considered for Inclusion”](https://github.com/ethereum/execution-specs/tree/master/network-upgrades#definitions). This “proto-status” was created to provide more legibility to EIP champions about which EIPs *may* be included in an upgrade. That said, it can be argued the lack of commitment associated with CFI causes more confusion than it removes. Additionally, CFI is only used on the execution layer.

If it isn’t useful, we should consider modifying or removing it, or potentially harmonizing its definition and usage across both the EL & CL processes.

---

## Replies

**ralexstokes** (2023-11-28):

I’ll go ahead and kick things off with [EIP-2537](https://ethereum-magicians.org/t/eip-2537-bls12-precompile-discussion-thread/4187/48)

There may be some minor change to the precompiles and gas schedule but this will all be together in time for serious inclusion discussions for Prague/Electra.

AFAIK previous concerns around this EIP have been resolved (e.g. hardened BLS12-381 implementations in production, esp. given that this code is used in EIP-4844 in Cancun/Deneb) and there is plenty of demand from both rollups and cryptography use cases.

One of my top priorities for this hard fork will be championing for inclusion of BLS12-381 precompiles and it seems like prime time ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**gballet** (2023-11-29):

are we talking about the next major HF or the “small” one between Dencun and the former? Because if it’s the next major HF, the complexity of verkle trees won’t leave much room for anything else.

And if it’s a smaller one, I don’t think we should call it Prague, in the hope that we can pull smaller hardforks faster than we can have devcons. Note that we can no longer add devconnect names, as Instanbul already exists as a fork.

---

**Tudmotu** (2023-11-29):

Not sure if it’s the right place to ask, but is there an update on EOF inclusion? Is it planned for Prague?

---

**shemnon** (2023-11-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png) gballet:

> Note that we can no longer add devconnect names, as Instanbul already exists as a fork.

We’ve already used three names for Istanbul: Byzantium, Constantinople, and Istanbul.  There’s [a list on wikipedia](https://en.wikipedia.org/wiki/Names_of_Istanbul) with more options.

If we run ahead of devcon/devconnect names we could just use more names for istanbul ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

---

**timbeiko** (2023-11-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png) gballet:

> are we talking about the next major HF or the “small” one between Dencun and the former?

I’m personally not really a believer in “small” forks. Historically, the only times we’ve had truly small or quick forks were either emergencies, or simple difficulty bomb pushback. For example, Shanghai was a “small” fork relative to The Merge, and it still shipped 6-7 months after it.

If we are considering any non-trivial EIPs, I’d call this Prague for simplicity. Whether it’s a 6-9 month fork like Shanghai or a 9+ month one like Cancun can only be very roughly predicted based on what EIPs we decide to include.

That said, I agree that we should make a call about whether we include Verkle or not ASAP, as it will dictate how much extra capacity there is for other EIPs.

---

**gballet** (2023-11-29):

also not a believer in “small forks”, but I’ve heard a mention of a fork with only minimal EIPs.

---

**timbeiko** (2023-11-29):

Right, assuming we didn’t do Verkle, we could choose to only do a set of smaller EIPs, but I just want to make sure we don’t do that thinking “it will be done in 3 months” when it’s likely to take 2x+ longer ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

---

**gcolvin** (2023-11-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png) gballet:

> if it’s the next major HF, the complexity of verkle trees won’t leave much room for anything else

At this point the EOF proposals represent some seven years of research and development.  They are solid.  They are needed.  They are really not that difficult to implement.  And the researchers and developers are burning out.  It’s time to get them into an upgrade.

---

**Wander** (2023-11-30):

I think [EIP 7002](https://ethereum-magicians.org/t/eip-7002-execution-layer-triggerable-exits) (EL-induced exits) deserves a mention. The staking community badly needs a way to trigger exits via smart contracts to finally and fully close the loop on trustless staking protocols.

Some interesting ideas for potentially improving it were tossed around at DevConnect this year, but even if it’s included as-is, Ethereum would be significantly safer.

---

**Giulio2002** (2023-12-01):

I think Verkle trees alongside with very few small EIPs (Verkle tree is a big update) such as EIP-2537 is desirable, in alternative we can focus on EOF and many small EIPs

---

**prebuffo** (2023-12-01):

I would divide the discussion into two parts, namely which large EIP (or series of EIPs) to include between Verkle Tree and EOF, and which other ‘small’ EIP to include.

Between Verkle Tree and EOF, a check should be made on the maturity of the project and the opinion of the Core Teams on it.

---

**dgusakov** (2023-12-01):

I believe [EIP-7002](https://ethereum-magicians.org/t/eip-7002-execution-layer-triggerable-exits/14195) is one of the best candidates for inclusion in the next hardfork.

My team and I are working on designing and developing Lido Community Staking Module (CSM). This module is aimed to offer permissionless entry to the Lido on Ethereum validator set. EIP-7002 greatly influences the [risk profile](https://research.lido.fi/t/risk-assessment-for-community-staking/5502) of CSM and any other permissionless staking solution. With EIP-7002 in place, CSM will become more attractive for Lido DAO to increase its staking share. Hence, more independent operators will be able to join Ethereum validation.

---

**TheDZhon** (2023-12-01):

I also feel that including [EIP-7002: Execution Layer Triggerable Exits](https://ethereum-magicians.org/t/eip-7002-execution-layer-triggerable-exits/14195) would be a good choice for the network, being crucial not only for *liquid* staking protocols, and pretty sure not only for Lido.

What I am afraid of is after enabling [EIP-7044: Perpetually valid signed voluntary exits](https://eips.ethereum.org/EIPS/eip-7044) in Dencun, there will be a long-term tail risk of storing and distributing the exit messages in staking protocols involving increased trust assumptions.

If EIP-7002 wasn’t included, it’s predictable that protocols trying to build a permissionless validator set (e.g., requiring bonds) would try to rely on joining the set with a pre-signed exit message intent. The message then should be stored and split in a distributed way. However, as the messages will have an infinite expiration time, it would pose a risk of falsely ‘losing’ the pieces or, in contrast, firing up exits spuriously, potentially leading to turbulence or fund losses.

In contrast, if EIP-7002 is implemented, the trust level built into the staking protocols would be reduced, not expanded.

Finally, EL triggerable exits are akin to Account Abstraction direction: getting rid of UX and trust issues with a smart contract that’s where Ethereum is great.

Thank you for raising this on the topic.

---

**abcoathup** (2023-12-01):

[EDIT]: Not a commentary on the merits of EIP7002.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dgusakov/48/11037_2.png) dgusakov:

> Lido DAO to increase its staking share

Lido is [currently at 32.28%](https://dune.com/hildobby/eth2-staking).

We shouldn’t want any entity to have a share of stake above 33.3% threshold.


      ![](https://ethereum-magicians.org/uploads/default/original/2X/8/8f0a562a90992dd656ced3f9b9b37c942cfbde54.png)

      [HackMD](https://notes.ethereum.org/@djrtwo/risks-of-lsd)



    ![](https://ethereum-magicians.org/uploads/default/original/2X/0/005da072a22360ea3ec05325cd74027d92efbc9c.png)

###



# The Risks of LSD  ### Liquid Staking Derivatives cannot safely exceed consensus thresholds  Liquid

---

**Wander** (2023-12-01):

Strongly agree with this, but I think the adoption of 7002 is independent of this issue and simply provides a safety benefit for all LSTs. If the [recent discussion on adjusting the mechanics pans out](https://ethereum-magicians.org/t/eip-7002-execution-layer-triggerable-exits/14195/4), it could even benefit smaller LSTs more heavily.

---

**dgusakov** (2023-12-02):

I was meaning share of CSM within Lido and overall Lido share.

---

**dapplion** (2023-12-05):

I want to propose [EIP-7549: Move committee index outside Attestation](https://eips.ethereum.org/EIPS/eip-7549)

It’s a very simple consensus-only change that reduces the cost of verifying casper FFG by a factor of 64x. As such, it accelerates the viability of ZK trustless bridges on Ethereum.

---

**smartprogrammer** (2023-12-05):

I would like to re-propose [EIP-3074: AUTH and AUTHCALL opcodes](https://eips.ethereum.org/EIPS/eip-3074)

---

**poojaranjan** (2023-12-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Lastly, as a “stretch goal”, we should agree on what to do with “Considered for Inclusion” . This “proto-status” was created to provide more legibility to EIP champions about which EIPs may be included in an upgrade. That said, it can be argued the lack of commitment associated with CFI causes more confusion than it removes. Additionally, CFI is only used on the execution layer.
>
>
> If it isn’t useful, we should consider modifying or removing it, or potentially harmonizing its definition and usage across both the EL & CL processes.

Earlier, Meta EIP used to list proposals considered for an upgrade. “CFI” was created to fill the gap and provide visibility on the list of proposals under consideration for an upgrade where devs are preparing for multiple upgrades in parallel.

With “Upgrade Meta Thread” and the “Meta EIP” for an upgrade getting back in, I do have places to look for EIPs list rather than depending on “CFIs”.

To keep the EIP status harmonized across layers, type & categories. I’d support removing “CFI”.

For `Core` EIPs we can have standard statuses as explained in [EIP-1](https://eips.ethereum.org/EIPS/eip-1#core-eips) with a high-level understanding of when to change the status as below:

`Draft` = 1st PR

`Review` = Whenever ready for clients’ review/implementation/devnet

`Last Call` = When moved to 1st Public Testnet

`Final` = When deployed on the Mainnet

---

**CluEleSsUK** (2023-12-06):

[EIP-3068: Precompile for BN256 HashToCurve Algorithms](https://eips.ethereum.org/EIPS/eip-3068) would be amazing (and its counterpart for [EIP-2537: Precompile for BLS12-381 curve operations](https://eips.ethereum.org/EIPS/eip-2537), which [@ralexstokes](/u/ralexstokes) already brought up!).

BN254 and a lot of threshold work is really hamstrung without hash_to_curve.


*(56 more replies not shown)*
