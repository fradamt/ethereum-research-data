---
source: magicians
topic_id: 21314
title: All Core Devs - Execution (ACDE) #198, October 10 2024
author: abcoathup
date: "2024-10-09"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-198-october-10-2024/21314
views: 321
likes: 5
posts_count: 5
---

# All Core Devs - Execution (ACDE) #198, October 10 2024

#### Agenda

[Execution Layer Meeting 198 · Issue #1163 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1163) moderated by [@timbeiko](/u/timbeiko)

#### Action Items & summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #198, October 10 2024](https://ethereum-magicians.org/t/all-core-devs-execution-acde-198-october-10-2024/21314/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> Action Items
>
>  pectra-devnet-4 to tentatively launch by Oct 17
>
>  EL test release expected by Oct 11
>  Teams should review 7702 RPC changes
>
>
>  BLS Breakout to finalize specs & gas pricing on Oct 14
>  Pectra Public Testnet expected to go live before Devcon
>
> Call Summary
> Pectra
> devnet-4 specs
>
> CL spec release is out (1.5.0-alpha.8)
> All devnet-4 blocking PRs have been merged  !
>
> Late addition: Update EIP-7702: add s value check by lightclient · Pull Request #8950 · ethereum/EIPs · GitHub
> Not blo…

#### Recording

  [![image](https://img.youtube.com/vi/YQwdKE0d8LI/maxresdefault.jpg)](https://www.youtube.com/watch?v=YQwdKE0d8LI&t=61s)

#### Additional Info

[Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-execution-call-198/) by [@Christine_dkim](/u/christine_dkim)

## Replies

**timbeiko** (2024-10-10):

# Action Items

- pectra-devnet-4 to tentatively launch by Oct 17

 EL test release expected by Oct 11
- Teams should review 7702 RPC changes

 [BLS Breakout](https://github.com/ethereum/pm/issues/1176) to finalize specs & gas pricing on Oct 14
 Pectra Public Testnet expected to go live before Devcon

# Call Summary

## Pectra

###

- CL spec release is out (1.5.0-alpha.8)
- All devnet-4 blocking PRs have been merged  !

Late addition: Update EIP-7702: add s value check by lightclient · Pull Request #8950 · ethereum/EIPs · GitHub
- Not blocking, but teams should review 7702 RPC changes

EL tests expected by this Friday
No EIP-2537 changes in scope for devnet-4 (see below)
**Devnet launch expected before next week’s ACDC**

### BLS Precompile Gas Pricing

We had an extensive discussion about repricing the MSM precompiles with different teams reporting benchmarks, and [@chfast](/u/chfast) sharing his [analysis](https://ethereum-magicians.org/t/eip-2537-bls12-precompile-discussion-thread/4187/81), but no clear consensus reached on the right amounts.

Additionally, there was a proposal by [@chfast](/u/chfast) to [remove the MUL precompiles](https://github.com/ethereum/EIPs/pull/8945). We also discussed potentially removing subgroup checks, making them optional with input flags, or moving them to separate precompiles to provide a wider range of options to applications.

A [breakout room](https://github.com/ethereum/pm/issues/1176) was scheduled for next Monday to better consider these options. **We agreed to not include EIP-2537 changes to devnet-4, in order to finalize specs.**

### implementation updates

- devnet-3 had finality issues caused by Geth forking off the of the network. The issue was found, fixed, and deployed during the call, with the network finalizing before we wrapped up  !
- EthereumJS also had issues, and their validators were exited to help stabilize the network.
- Lighthouse had issues with Geth that seemed to be fixed with a restart of the nodes. Still investigating the root cause.

### Pectra Public Testnet

To allow the community to test Pectra in a relatively stable environment, we plan to launch a testnet by Devcon! [The name is still TBD, with Moodeng being the leading contender](https://ethereum-magicians.org/t/naming-the-public-pectra-testnet/21263). Depending on the complexity of further EIP-2537 changes, they may be excluded from this testnet.

Given many client developers will be attending devcon and we’re unlikely to launch new devnets during that time, **we’ll aim to have the testnet live before the conference!**

## Other EIPs

### EIP-7623

[@Nerolation](/u/nerolation) made changes to EIP-7623 which should simplify client implementations. The intrinsic gas cost is no longer deducted before execution. Instead, the EIP now validates that the transaction sender’s balance can cover the floor cost of the transaction. Nethermind has already implemented the changes.

###

***Note: the discussion of EIPs 7782 & 7783 was quite fluid and went back and forth between similar concerns around the EIPs. I recommend watching the livestream for the full nuance here.***

This EIP, which came in response to EIP-7782 (see below) proposes a mechanism for clients to dynamically set their gas limit when proposing a block, while still maintaining a cap. The EIP would not require a hard fork, given the gas limit is controlled by block proposers. It would simply change the default behaviour from using a fixed value until changed to a gradually growing value over time, allowing for a smoother raising of the gas limit.

Some concerns were raised around increasing the rate of history/state growth, with pushback about history growth rates being lower post-4844 and state growth not being a pressing issue. There were also concerns about distracting attention/engineering time away from Pectra. Even though this is not a core EIP, and a relatively simple change clients can implement independently, in practice similar individuals are involved across the efforts.

###

This EIP proposes to reduce the slot time from 12 to 8 seconds. On the call, [@benaadams](/u/benaadams) explained his motivation was for this to be an alternative to raising the blob count. By reducing the slot time, we effectively increase the number of blobs/second.

Here, concerns were raised about the impact on bandwidth usage. [@Giulio2002](/u/giulio2002) additionally highlighted that even if we could lower the slot time to 8 seconds today, it may impact future efforts such as DVT or SSF, and that impact should be considered as part of the discussion.

There were also concerns raised about this potentially breaking contracts. While this seems very unlikely to be a large issue, it should at least be verified.

## Pectra Builder Spec changes

[@ralexstokes](/u/ralexstokes) asked for feedback on Pectra changes to the [Builder Spec](https://github.com/ethereum/builder-specs/pull/101). No major concerns, so leaving the PR as is.

## Staking Bandwidth Considerations

[@ryanberckmans](/u/ryanberckmans) had [raised concerns](https://ethresear.ch/t/wheres-the-home-staking-bandwidth-research/20507) about the lack of research on home-staker bandwidth consideration.

While there were no comments about this directly on the call, two bandwidth improvements were highlighted: [IDONTWANT](https://github.com/libp2p/specs/pull/548) and [engine_getBlobsV1](https://github.com/ethereum/execution-apis/pull/559), with other efforts [listed](https://ethresear.ch/t/wheres-the-home-staking-bandwidth-research/20507/4) on the original post.

## EIP-4444 updates

- Nethermind is continuing their work on integrating with the Portal Network to both seed and fetch history from it.
- Two EPF fellows are working on Portal improvements

---

**siladu** (2024-10-10):

Thanks for these posts [@abcoathup](/u/abcoathup) ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

Is it possible to upload the zoom chat along with the recording in future posts please?

---

**abcoathup** (2024-10-11):

[@siladu](/u/siladu) I would love the chat logs & transcripts to be shared straight after the call.

Formatting chat logs is apparently a manual task, and Eth o’clock (timing for many protocol calls) is when I am asleep in Australia so I haven’t had a chance to try.

For more background see:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)
    [AllCoreDevs, Network Upgrade & EthMagicians Process Improvements](https://ethereum-magicians.org/t/allcoredevs-network-upgrade-ethmagicians-process-improvements/20157/36) [Process Improvement](/c/magicians/process-improvement/6)



> @abcoathup I agree with a lot of your suggestions in the last post! In short:
>
> Big +1 on summaries being valuable but not visible enough. I’m going to focus on shifting that, and make EthMag summaries my #1 artifacts, which gets crossposted to Twitter/Discord/Farcaster/etc.
> The /pm repo is due for a refresh, and I’d rather wait a bit longer until more stuff around EthMag is figured out. It still feels like the right medium-term place for agendas and transcripts to live.
> I think it’s fine to not…

Transcripts are eventually shared in [GitHub - ethereum/pm: Project Management: Meeting notes and agenda items](https://github.com/ethereum/pm) but these don’t tend to appear quickly…

---

**siladu** (2024-10-11):

Thanks for the extra context, I’ve replied on that thread too.

Fellow Australian here, so in the same boat with Eth o’clock ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

I would rather have badly formatted chat logs than none at all

