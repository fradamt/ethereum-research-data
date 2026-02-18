---
source: magicians
topic_id: 25424
title: All Core Devs - Execution (ACDE) #221, September 25, 2025
author: system
date: "2025-09-12"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-221-september-25-2025/25424
views: 113
likes: 2
posts_count: 5
---

# All Core Devs - Execution (ACDE) #221, September 25, 2025

### Agenda

- Fusaka

Bug bounty
- Testnet releases, schedule in Meta EIP
- 60M mainnet gas limit default
- EIP status updates

Glamsterdam

- EPBS/BALs updates
- PFI deadline
- Update EIP-7723: Include primary point of contact in proposal by wolovim · Pull Request #10391 · ethereum/EIPs · GitHub

Tim OOO from next ACD until EOY, [@adietrichs](/u/adietrichs) filling in!

**Meeting Time:** Thursday, September 25, 2025 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1723)

## Replies

**abcoathup** (2025-09-13):

### Summary

**ACDE TL;DW** by [@timbeiko](/u/timbeiko) [Copied from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1420794699823972495)]

- We’re shipping Fusaka  !

The testnet schedule is now merged into EIP-7607
- Holesky will fork first (Oct 1), with Sepolia and Hoodi following every two weeks, assuming no issues are found.
- Some client already have releases out for testnets, all should be out by Monday and tomorrow the EF blog will announce the upgrade.
- All Fusaka EIPs should be moved to Last Call, PR tracker here: Update EIP-7607: Move to Last Call by timbeiko · Pull Request #10423 · ethereum/EIPs · GitHub

**Mainnet 60M Gas Limit**

- As part of their Fusaka mainnet client releases (once testnets have upgraded), clients will update their default gas limit to 60M.

Glamsterdam

- EPBS and BAL breakouts continuing, BAL devnet-0 expected in October, EPBS breakout tomorrow.
- Deadline for EIP PFI proposals is when Fusaka mainnet releases go live. Proposal to formalize the role of EIP champions: Update EIP-7723: Include primary point of contact in proposal by wolovim · Pull Request #10391 · ethereum/EIPs · GitHub

And, lastly, this was my last ACD before my leave. [@adietrichs](/u/adietrichs) will be taking over ACDE until EOY. See you after Fusaka ![:waving_hand:](https://ethereum-magicians.org/images/emoji/twitter/waving_hand.png?v=15) !

### Recordings/Stream

- https://forkcast.org
- Live stream on X: [x.com/ECHInstitute]

### Writeups

- by @Christine_dkim [christinedkim.substack.com]
- Highlights from the All Core Developers Execution (ACDE) Call #221 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade:

Current devnet: fusaka-devnet-3 [specs]

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam):

- Headliners: consensus layer: EIP7732 ePBS & execution layer: EIP7928 Block-level Access Lists
- Non-headliners are being proposed for inclusion:

---

**poojaranjan** (2025-09-25):

Tweet thread for quick notes - https://x.com/poojaranjan19/status/1971213098733158747

---

**system** (2025-09-25):

### Meeting Summary:

The meeting covered updates on the Fusaka upgrade and associated bug bounty competition, with discussions about testnet schedules and client releases for the Shanghai upgrade. The team reviewed various Ethereum Improvement Proposals (EIPs) and their implementations, including Block Lab Access Lists, Beta Zero for EIP7732, and a new delegate mechanism for smart contract factories. The conversation ended with discussions about formalizing the role of EIP champions and exploring potential new proposals for future Ethereum forks.

**Click to expand detailed summary**

The meeting focused on updates and plans related to the Fusaka upgrade and the associated bug bounty competition. Fredrik reported that the competition is progressing well, with more valid reports as the deadline approaches, and confirmed that no critical issues have emerged that could affect the mainnet upgrade timeline. Tim outlined the testnet schedule, which includes forking Holesky on October 1st, followed by forking Sepolia and Hoodi, with BPOs activated one week after each testnet’s Fusaka activation.

The team discussed the upcoming formal announcement of client releases for the Shanghai upgrade, with blog posts planned for tomorrow and additional releases expected by Monday. Several clients including Geth, Lighthouse, Nimbus, and Prism are still working on their releases due to various build and process issues, though Nethermind has already released today. The team confirmed that Panel Ops will run a Shadow Fork of Holesky tomorrow with the available releases, and discussed raising the default gas limit on mainnet to 60 million as part of the Shanghai release, which will be implemented once the mainnet releases are completed.

Tim announced that EIP authors should review and approve PRs moving their EIPs to last call for the testnets, as the mainnet launch is imminent. Toni provided an update on Block Lab Access Lists, noting no changes to the EIP and clarifying client handling of self-destructs and precompiles, with a target devnet release by October. Terence mentioned the release of Beta Zero for EIP7732 and progress on container types and stage transition functions, aiming for a devnet release by early November. Several Ethereum clients, including Besu, Geth, and Nethermind, have started working on BAL implementations. Tim suggested using the latest CL spec (Beta 0 from V1.6) as the basis for both BAL and PBS devnets to ensure compatibility with the Fuji testnet. The deadline for new proposals for Glamsterdam was set to coincide with the mainnet release of Fuji in the next month.

Tim invited participants to propose EIPs for Glamsterdam by opening a PR against the Meta EIP. Justin raised a question about managing early EIPs for CFI while juggling smaller PFI issues, to which Tim responded by advocating for limiting new proposals and not moving EIPs from CFI to SFI until late stages of implementation for SFI EIPs like BALs and EPBS. Tim suggested prioritizing EIPs and reviewing them when there is more breathing room in implementation, rather than rushing to promote them from CFI to SFI.

Tim and Wolovim discussed a proposal by Mark to formally define the role of an EIP champion and the associated responsibilities. Wolovim suggested requiring a primary point of contact for each proposed EIP in a given fork to improve communication and reduce friction. Tim agreed with the idea and proposed that the person who opens the PR for an EIP should be considered the champion. Wolovim offered to have the protocol support team identify champions for existing EIPs, and both agreed to review the PR before the next AllCoreDevs meeting.

The team discussed the role and identification of EIP champions, with a focus on whether champions should be explicitly named in Meta EIPs. They agreed to test the concept on ForkCAST for the Glamsterdam fork before potentially formalizing it in either the meta EIPIP or EIP header field. Tim noted that while champions aren’t necessarily authors, there’s value in having an explicit champion for coordination purposes. The group also briefly discussed the possibility of PFI EIP presentations, with Hadrien presenting his Missouri IP proposal for inclusion in Amsterdam.

Hadrien presented EIP-7819, which proposes a new delegate in RLP code to allow smart contract factories to instantiate objects equivalent to current proxies or clones using ERC-1167 or ERC-1967. He explained that this would reduce costs, create smaller objects (23 bytes vs. 70-100+ bytes), and improve upgradability by using existing delegation primitives. The proposal aims to avoid previous bugs and attacks associated with unconventional storage slots in clones and proxies, with the implementation already existing in execution clients.

The meeting focused on a proposal for a CREATE-like mechanism to create and update delegations, with discussions on its potential impact and implementation. Hadrien explained that the mechanism could reduce state growth by approximately 25% of future contract deployments, and the GAST team’s research showed that 89.1% of contracts are deployed from factories. Participants raised concerns about the trade-off of increased interaction costs and discussed the use cases for smart wallets. The group also briefly touched on the possibility of implementing SWAPN and DUPN opcodes without breaking changes to address the “stack too deep” error in Solidity.

### Next Steps:

- Client teams  to release their Fusaka client versions in the next day or so.
- Tim to publish a formal announcement blog post about the Fusaka testnet schedule tomorrow.
- Panel Ops to run a Shadow Fork of Holesky tomorrow with available client releases.
- EIP authors to review and approve PRs to move Fusaka EIPs to last call.
- Protocol Support team  to source champion names for all existing PFI EIPs if the champion proposal is approved.
- Client teams to implement Block Access Lists  for the first devnet by October.
- Client teams to implement ePBS for devnet zero by end of October/early November.
- Developers to submit any EIP proposals for Glamsterdam in the next few weeks before mainnet releases for Fusaka.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: nfCj%?55)
- Download Chat (Passcode: nfCj%?55)

---

**system** (2025-09-25):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=1NIvzSliv44

