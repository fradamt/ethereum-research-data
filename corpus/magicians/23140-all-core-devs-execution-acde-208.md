---
source: magicians
topic_id: 23140
title: All Core Devs - Execution (ACDE) #208
author: system
date: "2025-03-13"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-208/23140
views: 290
likes: 6
posts_count: 4
---

# All Core Devs - Execution (ACDE) #208

# All Core Devs - Execution (ACDE) #208, March 27, 2025

- March 27, 2025, 14:00-15:30 UTC

 DST warning: double check your local time

90 minutes
Stream: https://www.youtube.com/watch?v=0eVoE_isGBk

# Agenda

- Pectra

Hoodi

Fork activation
- Application/infra testing

[Ethereum Protocol Upgrade Process by fredrik0x · Pull Request #1409 · ethereum/pm · GitHub](https://github.com/ethereum/pm/pull/1409)
[eth_config JSON-RPC Method](https://eips.ethereum.org/EIPS/eip-7910)
[Mainnet timing](https://github.com/ethereum/pm/issues/1374#issuecomment-2741823829)

Fusaka

- PSA: PFI deadline past, client team preferences due by March 31, scope freeze on April 10

PFI PRs:

https://github.com/ethereum/EIPs/pull/9528
- https://github.com/ethereum/EIPs/pull/9451

PeerDAS

- Sunnyside labs update
- EL Cell Proof computation

EOF next steps. **Client teams, please share your thoughts in advance.** Pre-reads:

- EOF Fusaka Options - HackMD
- EOF: When Complexity Outweighs Necessity - HackMD
- All Core Devs - Execution (ACDE) #208 · Issue #1374 · ethereum/pm · GitHub

Portal & History Expiry

- EIP-6110 interactions
- eth/69
- Deployment timelines
- Light client <> Portal issues

[Sepolia replacement name](https://ethereum-magicians.org/t/testnet-name-needed-for-sepolia-replacement/23221)

## Replies

**timbeiko** (2025-03-27):

**ACDE Recap**

1. Pectra:

Mainnet tentatively scheduled for 2025-04-30 14:14:47 (slot 11599872). To be confirmed on ACDC next week. Will also follow up with infra/app teams by then to flag issues.
2. We’ll be using the template in Fredrik’s fork process to coordinate the fork (Ethereum Protocol Upgrade Process by fredriksvantes · Pull Request #1409 · ethereum/pm · GitHub)
3. We’ll wait until Fusaka to try out EIP-7910: eth_config JSON-RPC Method
4. Fusaka:

After a lot of back and forth: EOF remains in Fusaka, with Option A from this doc : EOF Fusaka Options - HackMD. All EIPs from devnet-0 will be SFI’d, and those from devnet-1 and devnet-2 will be CFI’d. PR incoming from Danno.
5. Most EL client teams have already shared their fork scoping preference, with EIP-7883 unanimously favored. Will CFI this too.
6. On next ACDE, we’ll finalize Fusaka scoping. The scope should reflect shipping Fusaka by EOY, and we should not add anything that could delay PeerDAS.
7. We agreed to merge Update EIP-7594: include cell proofs in network wrapper of blob txs by fradamt · Pull Request #9378 · ethereum/EIPs · GitHub (including versioning for the proofs) and Add EIP-7594 (PeerDAS) related changes by 0x00101010 · Pull Request #630 · ethereum/execution-apis · GitHub
8. History Expiry

Due to the EIP-6110 issues, we’ve agreed to delay dropping pre-merge history on mainnet until after Pectra.
9. We agreed to a May 1st deadline to drop pre-merge history on Sepolia. Piper will draft an informational EIP with this info to add it to the Fusaka Meta EIP.
10. We ran out of time to discuss the other topics on the agenda.
11. Barnabé and Ansgar announced the Protocol Reseach Call (first one next Wed 14:00 UTC): Protocol research call
12. If you want to participate in post-Sepolia testnet naming discussions, you can do so here: Testnet name needed for Sepolia replacement

---

**abcoathup** (2025-03-27):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #208](https://ethereum-magicians.org/t/all-core-devs-execution-acde-208/23140/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDE Recap
>
>
> Pectra:
>
> Mainnet tentatively scheduled for 2025-04-30 14:14:47 (slot 11599872). To be confirmed on ACDC next week. Will also follow up with infra/app teams by then to flag issues.
> We’ll be using the template in Fredrik’s fork process to coordinate the fork (Ethereum Protocol Upgrade Process by fredriksvantes · Pull Request #1409 · ethereum/pm · GitHub)
> We’ll wait until Fusaka to try out EIP-7910: eth_config JSON-RPC Method
>
>
>
> Fusaka:
>
> After a lot of back and forth: EOF remains in…

### Recording

  [![image](https://img.youtube.com/vi/0eVoE_isGBk/maxresdefault.jpg)](https://www.youtube.com/watch?v=0eVoE_isGBk&t=172s)

### Writeups

- Crypto & Blockchain Research Reports | Galaxy by @Christine_dkim
- Highlights of Ethereum's All Core Devs Meeting (ACDE) #208 by @yashkamalchaturvedi

### Additional info

- Hoodi testnet
- Ethereum Protocol Upgrade Process
- The Case for EOF | Solidity Programming Language

---

**yashkamalchaturvedi** (2025-03-28):

![image](https://etherworld.co/favicon.png)

      [EtherWorld.co – 27 Mar 25](https://etherworld.co/2025/03/27/highlights-of-ethereums-all-core-devs-meeting-acde-208/)



    ![image](https://etherworld.co/content/images/2025/03/EW-Thumbnails--6-.jpg)

###



Pectra on Hoodi, Ethereum Upgrade Process, Pectra Date, Cell Proofs, EOF Debate, Fusaka Scope, History Expiry, Protocol Research Call & Sepolia Renaming

