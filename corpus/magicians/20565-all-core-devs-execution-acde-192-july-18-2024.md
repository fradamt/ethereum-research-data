---
source: magicians
topic_id: 20565
title: All Core Devs - Execution (ACDE) #192, July 18 2024
author: abcoathup
date: "2024-07-16"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-192-july-18-2024/20565
views: 1208
likes: 6
posts_count: 3
---

# All Core Devs - Execution (ACDE) #192, July 18 2024

### Agenda

[Execution Layer Meeting 192 · Issue #1098 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1098)

Moderator: [@timbeiko](/u/timbeiko)

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #192, July 18 2024](https://ethereum-magicians.org/t/all-core-devs-execution-acde-call-192-july-18-2024/20565/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDE 192 Call Summary
> Decisions & Next Steps
>
> devnet-1: expected to launch by next Thursday.
> EOF: remains in Pectra, Geth will not oppose inclusion but does not want to take responsibility for testing, teams will continue working on implementations and testing. Fuzzing should be a priority as soon as we have multiple complete implementations.
> EIP-7702: the spec remains unchanged for now
> logs for system contracts: teams should review prior to next week’s ACDC
> EIP-7742: teams should review prior t…

### Recording

  [![image](https://img.youtube.com/vi/kL58hvM0E68/maxresdefault.jpg)](https://www.youtube.com/watch?v=kL58hvM0E68&t=308s)

### Additional info

- Notes: Crypto & Blockchain Research Reports | Galaxy by @Christine_dkim
- EOF: Why I am against EOF in Pectra – MariusVanDerWijden by @MariusVanDerWijden
- RIP7212: Brief History and Current Situation of RIP-7212 by @ulerdogan

## Replies

**timbeiko** (2024-07-18):

# ACDE 192 Call Summary

## Decisions & Next Steps

- devnet-1: expected to launch by next Thursday.
- EOF: remains in Pectra, Geth will not oppose inclusion but does not want to take responsibility for testing, teams will continue working on implementations and testing. Fuzzing should be a priority as soon as we have multiple complete implementations.
- EIP-7702: the spec remains unchanged for now
- logs for system contracts: teams should review prior to next week’s ACDC
- EIP-7742: teams should review prior to next week’s ACDC
- RIP-7212 on L1: not much discussion, should ideally make a decision about inclusion in next ACDE
- EIP-4444: no updates

## Recap

*Note: this is based on my rough, imperfect notes. For the full context/nuance, please watch the recording. Also, I’ve avoided tagging people because there’s a limit of 10 mentions in a single post.*

### devnet-1

- EF devops team focused on local testing with Kurtosis
- All client sent images for devnet-1, found bugs in Erigon & Prysm, both are being fixed
- Aim to launch devnet-1 next Thursday!

### EOF

- Marius from Geth published a post outlining EOF concerns, a 200+ message discord thread ensued.
- On the call, Marius argued EOF’s benefits are not worth the complexity, especially given we cannot get rid of the legacy EVM
- Daniel from Solidity said they think EOF is superior to all other proposals to bring significant changes to the EVM. Once Solidity supports it, he saw little incentive for developers to keep using legacy contracts. He also didn’t think it would be realistic for L2s to implement EOF today.
- Peter from Geth emphasized that EOF’s benefits are limited if the legacy EVM must be supported and that the proposal increases the risk surface of the EVM. He also highlighted some of EOF’s benefits, such as removing gas introspection, are also minimal when considering the legacy EVM can be called by EOF contracts. If there was a path to remove the legacy EVM, he’d be more suppotive of EOF.
- Ansgar agreed that the L1 cost/benefit may not be as good as it could given the legacy EVM, but argued that we should still do it in order to lead the way for L2s. If L1 does not ship EOF, L2s realistically won’t do so for several years. We should work towards L2 leading the way for EL innovation, but we’re not there yet. This isn’t just an EOF thing: it comes up in the context of account abstraction too.
- Danno from Besu said one way to get rid of the legacy EVM would be to first ban legacy deployments, and then, at some future point, migrate contracts.
- I replied that this would realistically take several years, and may never happen. We shouldn’t make a decision about EOF inclusion based on the assumption that we could perhaps get rid of the legacy EVM. If it happens, we should treat that as a “bonus”, not our base case.
- Andrew from Erigon agreed EOF is complex but thinks we should still do it. Not doing so would freeze progress on EVM development.
- Lukasz from Nethermind agreed with Erigon, and added that EOF is something that they’d prefer to ship as a whole vs. in separate parts. He also stressed that we should test it extensively, including fuzzing client implementations against each other as soon as possible. If testing were to reveal issues that are too hard to overcome, we could still remove it, but it feels premature to do so.
- Dragan from Reth agreed that complexity could be fought with more testing
- Matt from Geth disagreed we should ship EOF, even if it is practical to do so. His argued that EOF isn’t critical for L1’s survival and that we should instead focus on client optimizations, inclusion lists, scaling, etc. He would rather see L2s take this work, and generally the work of improving the EVM, over.
- Danno disagreed with this, arguing that EOF support was existential on a longer time horizon, as other VMs would keep coming along and the EVM may eventually be seen as too inferior.
- Marius ended by saying that Geth would not oppose EOF’s inclusion, but that it would not go above and beyond to test it and ensure there were no outstanding risks. Others would need to step up to champion this work.
- Given this was roughly the state we were in when deciding to include EOF, we kept it in scope for Pectra and agreed to continue testing it extensively.

### EIP-7702

- CODERESET was proposed to allow EOAs to remove external delegation when using 7702.
- Otim labs shared their concerns about the proposal, which were shared by many of the client teams on the call.
- There was a lot of back and forth on these documents, recommend watching the livestream for nuance.
- Ansgar said CODERESET created a “worst-of-both-worlds” scenario, where authorizations are neither guaranteed to be permanent or temporary.
- Matt also argued against the proposal, saying it had many of the same problems as previous EOA migration proposals.
- Yoav Weiss highlighted that even without this proposal, there were still DoS risks to address for 7702.
- Richard Meissner  voiced that constant spec changes make it hard for wallet and tooling teams to actually test 7702 in practice, and that it would be nice to have a stable version to use in devnets.
- I responded that we will have something like that when devnet-1 launches, which uses an old 7702 spec version. When we plan Pectra’s second devnet, we’ll see whether we want to pull in new spec changes from 7702. While this may not be ideal from a 7702 testing perspective, it seems like the best approach to test all of Pectra.

###

- The call had <10 minutes left at this point, so @matt briefly explained the PR and we agreed to discuss this async and take a decision on next week’s ACDC

### EIP-7742

- Similar to the above, client teams will review 7742 before ACDC

### EIP/RIP-7212

- Ulaş Erdoğan shared a document with open questions about bringing EIP-7212 to mainnet.
- I emphasized that we still hadn’t implemented everything we’d committed to for Pectra (and had just spent the rest of the call discussing ongoing spec changes), and that we probably shouldn’t consider extending the scope right now.
- Ansgar shared that we keep pushing back the decision about 7212 and we should aim to make a final one soon, ideally the next ACDE.

### EIP-4444

- No updates shared

