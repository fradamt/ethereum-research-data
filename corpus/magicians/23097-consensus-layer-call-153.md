---
source: magicians
topic_id: 23097
title: Consensus-layer Call 153
author: system
date: "2025-03-08"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/consensus-layer-call-153/23097
views: 378
likes: 3
posts_count: 7
---

# Consensus-layer Call 153

# Consensus-layer Call 153

[prev: call 152](https://github.com/ethereum/pm/issues/1323)

Meeting Date/Time: [Thursday 2025/3/20 at 14:00 UTC](https://savvytime.com/converter/utc/mar-20-2025/2pm)

Meeting Duration: 1.5 hours

stream

1. Electra
2. PeerDAS / Blob scaling
3. Research, spec, etc.
4. Open discussion/Closing remarks

[GitHub Issue](https://github.com/ethereum/pm/issues/1356)

## Replies

**abcoathup** (2025-03-20):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [Consensus-layer Call 153](https://ethereum-magicians.org/t/consensus-layer-call-153/23097/3) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #153 summary
> Action Items
>
> If you are a validator of the Hoodi testnet, please get in touch with ethPandaOps for handover if you haven’t already.
> Prepare for the Hoodi Pectra fork next week: Wednesday, March 26, 2025 2:37:12 PM
> Continue implementation work on PeerDAS
>
> Summary
>
> Pectra
>
> The new Hoodi testnet is live!
> Hoodi Pectra fork is: Wednesday, March 26, 2025 2:37:12 PM
> Clients have or are working on releases with Hoodi support
> We touched on post-mortems for the Holesky…

### Recording

  [![image](https://img.youtube.com/vi/PDttc86jEkY/maxresdefault.jpg)](https://www.youtube.com/watch?v=PDttc86jEkY&t=216s)

### Writeups

- Crypto & Blockchain Research Reports | Galaxy by @Christine_dkim
- Highlights of Ethereum's All Core Devs Meeting (ACDC) #153 by @yashkamalchaturvedi

### Additional info

- Holešky testnet Pectra incident post-mortem
- Sepolia testnet Pectra incident post-mortem
- Slot finder upgrade scheduler

---

**ralexstokes** (2025-03-21):

**ACDC #153 summary**

**Action Items**

- If you are a validator of the Hoodi testnet, please get in touch with ethPandaOps for handover if you haven’t already.
- Prepare for the Hoodi Pectra fork next week: Wednesday, March 26, 2025 2:37:12 PM
- Continue implementation work on PeerDAS

**Summary**

- Pectra

The new Hoodi testnet is live!
- Hoodi Pectra fork is: Wednesday, March 26, 2025 2:37:12 PM
- Clients have or are working on releases with Hoodi support
- We touched on post-mortems for the Holesky and Sepolia Pectra upgrades

pm/Pectra/holesky-postmortem.md at master · ethereum/pm · GitHub
- pm/Pectra/sepolia-postmortem.md at master · ethereum/pm · GitHub

Client teams are still in the process of following up on various bugs/issues observed during these testnet upgrades.
Then we touched on milestones we want to see before setting a Pectra mainnet date. Client teams want to see the following before thinking about a mainnet date:

- Hoodi Pectra going smoothly
- Results from the Pectra bug bounty competition assessed
- Time for users/applications to test their Pectra updates sufficiently

Next, we turned to an interaction with history expiry and deposit logs

- Expiring history could complicate how clients get deposit logs from the EL which are required until EIP-6110 in the Pectra upgrade.
- This implies we should see Pectra on mainnet before moving forward with the existing history expiry deployment plan to drop pre-Merge history on May 1 2025.
- Given the current timing with Pectra, the expected history expiry date may need to be moved forward until after Pectra.
- Client teams confirmed this issue, and agreed we should wait for Pectra on mainnet.

And to be precise, there is a transition period that starts at Pectra and finishes when the new 6110 mechanism takes over and the history expiry deadline should be no sooner than the end of this transition period.

We also touched on the rollout of history expiry so that we go through testnet(s) before mainnet deployment.

- The only relevant testnet is Sepolia, and everyone agreed to test on Sepolia.
- Given the caveat above, we agreed to ship history expiry on Sepolia by the May 1st date, and then once that has been verified can plan a mainnet date for the pre-Merge history expiry.

To wrap up Pectra, we had an update around performance testing on `pectra-devnet-6` with 60M gas

- All together, things went well; some minor client interactions were surfaced that caused some issues at that gas limit.

PeerDAS

- Touched on peerdas-devnet-5; some ongoing client work to identify various issues.

Check these notes from the breakouts if you want more detail: PeerDAS Breakout Room notes - Google Docs

On the way to `peerdas-devnet-6`, we turned to the question of validator custody that opened an interesting conversation around some implementation questions.

- The spec currently mandates validator custody, but leaves room for different conforming implementations.
- There are some implementation details around tracking validators by balance, and how frequently the CL updates its operations to custody the correct set of data, and how the user interfaces with their node to customize this behavior.
- We settled on a preference for automatic, periodic checks that piggyback on existing infrastructure in the client (e.g. the validator registrations used for block building). We may want to add implementation notes to the spec, and work here is ongoing.

Relevant links:

make validator custody static for beacon node run session by g11tech · Pull Request #4154 · ethereum/consensus-specs · GitHub
- Clarify validator custody with PeerDAS · Issue #4182 · ethereum/consensus-specs · GitHub

Had an update to wrap up PeerDAS today with ongoing work around the `getBlobs` mechanism. Sunnyside Labs is doing some analysis and is seeking multiple client implementations to help ground data.

Fusaka

- EIP-7688 for SSZ StableContainers was PFI’d for Fusaka. We agreed to focus on stable Fusaka devnets with the current SFI’d EIPs before visiting other features. Dmitry from the Lido team gave an overview of how this EIP would be helpful, and Etan from Nimbus highlighted some other benefits of this EIP for the protocol.

---

**TimDaub** (2025-03-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png) ralexstokes:

> Next, we turned to an interaction with history expiry and deposit logs
>
>
> Expiring history could complicate how clients get deposit logs from the EL which are required until EIP-6110 in the Pectra upgrade.
> This implies we should see Pectra on mainnet before moving forward with the existing history expiry deployment plan to drop pre-Merge history on May 1 2025.

Why are we expiring history? Has anyone of the core devs actually talked to Ethereum application builders? Nobody wants data to be expired. I do not know a single soul that actually wants this. Please read the comments of EIP-4444, everyone is against this. Many app developers will run into the same issues you’re having with the deposit contract logs. It’s sooooooo frustrating. We’ve been saying this for years and no one is listening and everyone is just blinding following this stupid The Purge part of the roadmap. Be that for increasing the cost of calldata or for removing the usefulness of logs. WHYY?

---

**ralexstokes** (2025-03-21):

expiring the history just refers to a “vanilla” full node being able to not store it locally

the history is not being *deleted*, it is just *moving*

there are already multiple alternative ways to access the history in a post-4444 world (e.g. torrents, Portal Network)

i am not sure what clients are planning but you could easily imagine some/all clients retaining a command line flag to configure this behavior so that even after EIP-4444 the full node behavior is the exact same as today

the interaction here w/ the deposit logs is that it is a requirement of the protocol itself so that it would defeat the purpose of EIP-4444. applications/users that consume the history just need to update how they get the history and otherwise are all set

---

**TimDaub** (2025-03-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png)
    [EIP-7623: Increase Calldata Cost](https://ethereum-magicians.org/t/eip-7623-increase-calldata-cost/18647/62) [EIPs core](/c/eips/eips-core/35)



> EIP-4444 was written at a time (2021) when historical block state growth was still an issue. Today, the L1 isn’t even being used anymore! We’re sub 1 gwei gas!! We’re seeing a much slower growth of the total size of the sync because of less activity on L1 and blobs. The motivation for EIP-4444 is outdated! This is what EIP-4444 says in its Motivation
>
> Historical blocks and receipts currently occupy more than 400GB of disk space (and growing!). Therefore, to validate the chain, users must typic…

Read the part on EIP-4444. We do not want to use torrents or IPFS. Please stop suggesting it pleaaaase

don‘t be paternalistic towards devs. Don‘t discuss away problems. Don‘t tell us how to do our job, we don‘t want to use torrents and IPFS

---

**TimDaub** (2025-03-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png) ralexstokes:

> expiring the history just refers to a “vanilla” full node being able to not store it locally

Bad too.

When I build a protocol on top of Ethereum I just wanna build it on vanilla guarantees, not some kind of frankenstein Ethereum configuration

If I cannot, anyday, switch out Alchemy or Infura‘s RPC url then my app is powered by them, not Ethereum

also: It‘s a slippery slope. App devs rely in history. If u remove serving history as an invariant, what else are you going to do in the future. One day I won‘t be able to run my post eip4444 frankenstein config anymore bc u decided to up bandwidth on your vanilla nodes

