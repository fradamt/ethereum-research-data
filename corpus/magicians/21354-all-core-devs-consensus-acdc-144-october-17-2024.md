---
source: magicians
topic_id: 21354
title: All Core Devs - Consensus (ACDC) #144, October 17 2024
author: abcoathup
date: "2024-10-11"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-144-october-17-2024/21354
views: 166
likes: 4
posts_count: 2
---

# All Core Devs - Consensus (ACDC) #144, October 17 2024

#### Agenda

[Consensus-layer Call 144 · Issue #1178 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1178) moderated by [@ralexstokes](/u/ralexstokes)

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #144, October 17 2024](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-144-october-17-2024/21354/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #144 summary
> Action Items
>
> Debugging and monitoring of devnet-4 should be a top priority for client teams to solidify the core Pectra features.
> Consider EIP-7742 implementation to parallelize work towards a blob count increase in Pectra.
> ACDC on 14 November 2024 will be canceled. Plenty of substitute gatherings will occur that week at Devcon.
>
> Summary
>
> Started with Pectra devnets
>
> There is an open block proposal issue with Grandine, but otherwise devnet-3 is looking good. Agreed to spin …

#### Recording

  [![image](https://img.youtube.com/vi/p3FRr5umt4U/maxresdefault.jpg)](https://www.youtube.com/watch?v=p3FRr5umt4U&t=72s)

#### Additional Info

[Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-consensus-call-144/) by [@Christine_dkim](/u/christine_dkim)

## Replies

**ralexstokes** (2024-10-18):

**ACDC #144 summary**

**Action Items**

- Debugging and monitoring of devnet-4 should be a top priority for client teams to solidify the core Pectra features.
- Consider EIP-7742 implementation to parallelize work towards a blob count increase in Pectra.
- ACDC on 14 November 2024 will be canceled. Plenty of substitute gatherings will occur that week at Devcon.

**Summary**

- Started with Pectra devnets

There is an open block proposal issue with Grandine, but otherwise devnet-3 is looking good. Agreed to spin down the devnet on 17 October.
- Reviewed readiness for devnet-4; clients are generally ready and plan launch of devnet-4 with a majority of CL and EL clients on 18 October.

Next, turned to a basket of items to finalize the Pectra scope

- Raised the SingleAttestation PR for consideration again; there wasn’t strong support for it on the call and an issue was raised around the exact security implications this PR aims to address. Lean towards passing on this change given implementation complexity unless a stronger security argument can be made.
- Considered this PR to change networking rate limiting to coincide with Pectra client releases; no opposition and clients leaned towards moving ahead
- Call to review a bug fix in withdrawals handling and the interaction with EIP-7251. Intent is to have ready for devnet-5 specs.
- Addressed the proposal to support SSZ encoding in the builder APIs; no opposition
- A note that Pectra will change the generalized indices of elements in the BeaconState; if you are a consumer of this feature, please be aware as it is a breaking change for your application.
- And a quick shout out around the EIP-2537 breakout call which had the action item to seek more feedback from users of that EIP’s precompiles.

Then turned to PeerDAS and the question of scaling blobs in Pectra and beyond

- Started with a call for final comments on some P2P clarifications around how clients will leverage the engine_getBlobsV1 endpoint

no opposition, should merge shortly

Then asked for implementation updates as clients expect to leverage this feature to provide bandwidth savings for nodes

- Early investigation from Terence found an improvement in download bandwidth, but also a complication around the interplay of external block builders and this feature. Analysis is ongoing to further isolate the benefits expected for local block builders.

And then revisited a PR to rebase the PeerDAS consensus-specs feature onto Electra which reflects the current deployment schedule agreed to on ACD.

- Strong support from client teams, but do want to check directly with PeerDAS implementers who couldn’t provide a strong signal on the call

And then Francis presented [further analysis and a proposal](https://docs.google.com/document/d/19jZcm5CgWM12Eqg1HRwG_ppd1EL9tduheckBmoFBCNM/edit?tab=t.0#heading=h.hs20rimb4nkm) to raise the blob counts in Pectra

- Key point is that there is likely headroom for some improvement, especially in light of several implementation updates in progress including the engine_getBlobV1 method above, improvements to usage of gossip on the network, and further extensions like IDONTWANT messages on the network
- Argued that a conservative approach would be setting target to 4 blobs per blocks and leaving max at 6 blob per block, with a recommendation to target 5 with a max of 8 blobs per block.
- Attendees agreed to track these implementation updates along with continued analysis of the mainnet to gain confidence in one of these two options.

This presentation segued into the question of moving ahead with some blob adjustment in Pectra (vs. none) and attendees agreed the minimum requirement would be the EIP to make the blob parameter adjustments along with EIP-7742.

- We agreed to move ahead with EIP-7742 to set us up for some blob adjustment. Expect final migration from CFI to SFI on next ACDE.

Closed the call with an overview of EIP-7783 and EIP-7782 which propose to increase base layer throughput with reduced slot times and suggest a mechanism to reduce volatility in the block gas limit downstream to these potential changes

- Consensus was that the slot reduction proposal needs more analysis, with an even more attractive option being shorter slot times (2-4s vs 8s) as 8s felt like a change with the same UX as today’s timings while incurring the cost that changing slot times would have for the network, implementations, tooling and ecosystem. There was a strong signal that any such changes like this should be considered against other potential protocol upgrades which may interact in conflicting ways.

To close out the call, we touched on the idea to cancel the ACDC session on 14 November as it will be during the Devcon conference where many ACDC participants will already be. There was no opposition on the call to canceling the call on the 14th.

