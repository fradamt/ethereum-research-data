---
source: magicians
topic_id: 22828
title: All Core Devs - Execution (ACDE) #205, February 13, 2025
author: abcoathup
date: "2025-02-11"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-205-february-13-2025/22828
views: 442
likes: 5
posts_count: 3
---

# All Core Devs - Execution (ACDE) #205, February 13, 2025

#### Agenda

https://github.com/ethereum/pm/issues/1271 moderated by [@timbeiko](/u/timbeiko)

[Agenda summary](https://x.com/nixorokish/status/1889415917786067342) by [@nixo](/u/nixo)

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #205, February 13, 2025](https://ethereum-magicians.org/t/all-core-devs-execution-acde-205-february-13-2025/22828/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> Call Summary
> Action Items & Next Steps
> Pectra
>
> Client Teams to make Pectra releases by Feb 14
> Pectra testnet announcement out on Feb 14
> Pectra system contracts should be deployed to testnets + mainnet by Monday’s testing call
> All Pectra EIPs should be moved to Last Call (Tracking PR)
>
> Fusaka Fork scoping timeline:
> * March 13: Fusaka Proposed for Inclusion deadline
> * To do so, open a PR against EIP-7607
> * March 27: Deadline for core devs & researchers to review PFI’d EIPs and share their pref…

#### Recording

  [![image](https://img.youtube.com/vi/N90-qDkUPAo/maxresdefault.jpg)](https://www.youtube.com/watch?v=N90-qDkUPAo&t=232s)

#### Writeups

- Crypto & Blockchain Research Reports | Galaxy by @Christine_dkim
- Highlights of Ethereum's All Core Devs Meeting (ACDE) #205 by @yashkamalchaturvedi

#### Additional info

- Testnets:

Pectra-devnet-6
- Ephemery testnet upgraded to Pectra
- Pectra upgrade client releases for Holešky & Sepolia testnets

Last call for [Pectra Retrospective](https://ethereum-magicians.org/t/pectra-retrospective/22637)

## Replies

**timbeiko** (2025-02-13):

# Call Summary

## Action Items & Next Steps

**Pectra**

- Client Teams to make Pectra releases by Feb 14
- Pectra testnet announcement out on Feb 14
- Pectra system contracts should be deployed to testnets + mainnet by Monday’s testing call
- All Pectra EIPs should be moved to Last Call (Tracking PR)

**Fusaka Fork scoping timeline:**

* **March 13:** Fusaka `Proposed for Inclusion` deadline

* To do so, open a PR against [EIP-7607](https://eips.ethereum.org/EIPS/eip-7607)

* **March 27:** Deadline for core devs & researchers to review PFI’d EIPs and share their preferences async

* Any format is OK, but please link write ups in the [EIP-7607 EthMagicians thread](https://ethereum-magicians.org/t/eip-7607-fusaka-meta-eip/18439)

* **April 10**: Tentative deadline to finalize Fusaka’s scope

**Last Call for Reviews**

- Testing requirements for EIPs
- EOF testnet plans
- Max blobs flag
- Hardware requirement EIP
- Pectra Retrospective Thread

## Call Summary

### Pectra

- Devnet-6 is running smoothly, with the MEV workflow being tested end to end.
- Teams expect to have all releases by tomorrow, after which an EF blog post will announce the testnet forks.
- The system contracts for EIPs 2935, 7002 and 7251 have not been deployed yet. Let’s try and do this by Monday’s testing call.
- Ephemery now supports Pectra!

### Fusaka

#### EIP-7723

- Mario opened a PR for testing requirements at different stages of EIPs
- After some discussion on the call, we agreed to have the following requirements for Pectra:

CFI’d EIPs should have a PR against EELS and EEST test cases
- SFI’d EIPs must have a PR against EELS and EEST test cases

There were concerns about creating a bottleneck on the testing + spec teams, as well as the overhead for client developers to propose changes. Requiring PRs instead of merged changes felt like a sufficient mitigation for the first issue. The value of a shared spec for changes also felt more valuable than trying to maximally reduce friction for client teams who want to propose an EIP.

#### Pectra Retrospective

- Tim reviewed what was shared in the Pectra retrospective and distilled three key desires:

Improving the speed at which we ship network upgrades
- Having clear technical standards for EIPs when including them
- Considering larger process changes to AllCoreDevs

To move things forward, Tim proposed freezing the Fusaka scope now so that we can consider adjusting technical requirements and the overall process without delaying Fusaka.
There was some pushback to this:

- There are other EIPs some client teams would like considered
- There were concerns that the scope for Fusaka, decided a long time ago, was no longer the right one. Several Geth engineers were opposed to including EOF in Fusaka.
- There were other concerns that speeding up the process would not result in us choosing to work on the most impactful features
- And, lastly, there was a shared agreement that we should ship PeerDAS ASAP and not let other EIPs slow it down.

After a lot of back and forth, we agreed to still try and finalize the scope for Fusaka around the time Pectra goes live on mainnet. Specifically:

- EIPs should be Proposed for Inclusion by March 13
- Client teams should share their CFI preferences by March 27

Note: Geth members said they would prefer to share their preferences as individuals rather than a team. This is fine, but the deadline should be the same.

The scope for Fusaka should freeze by April 10

#### EOF

- Danno provided an update on EOF status and plans
- Fusaka-1 devnet deployed yesterday with old EOF Pectra spec
- Fusaka-1 aims to clean up spec changes by April (Pectra mainnet activation)
- Beyond this, there are several optional feature additions that could be considered
- Restore TX create into the spec
- Remove 7698 contract creation transaction
- Add metadata section to EOF container
- Add light-level introspection opcodes

Again, there was some pushback on EOF’s scope and inclusion in Fusaka by some Geth team members

Conversations about the specifics of the `TXCREATE` mechanism ([context](https://github.com/ethereum/pm/issues/1271#issuecomment-2625939241)) will continue async.

### Node Requirements

#### Max Blob Flag

- Feedback from roll-ups: Mildly inconvenient but acceptable if it allows for increased block throughput
- All EL clients except Erigon have agreed to the flag
- There were some concerns about the profitability of the flag. They were addressed by clarifying that this flag only applies to stakers building local blocks, which are less profitable than mev-boost ones by a larger margin than the difference this flag makes.

#### Requirement EIP

- We ran out of time to discuss this, will continue the conversation on ACDC

---

**yashkamalchaturvedi** (2025-02-14):

Call Notes: [Highlights of Ethereum's All Core Devs Meeting (ACDE) #205](https://etherworld.co/2025/02/14/highlights-of-ethereums-all-core-devs-meeting-acde-205/)

