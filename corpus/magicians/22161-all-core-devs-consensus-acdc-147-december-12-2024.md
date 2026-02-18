---
source: magicians
topic_id: 22161
title: All Core Devs - Consensus (ACDC) #147, December 12 2024
author: abcoathup
date: "2024-12-11"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-147-december-12-2024/22161
views: 249
likes: 2
posts_count: 2
---

# All Core Devs - Consensus (ACDC) #147, December 12 2024

#### Agenda

[Consensus-layer Call 147 · Issue #1211 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1211) moderated by [@ralexstokes](/u/ralexstokes)

##### Agenda summary by  (Copied from ):

**Relevant teams**: EL, rollups, CL, anyone with a desire for CL-only forks

**Pectra**: the scope is mostly finalized minus a few details.

- Aiming to agree on a BLS precompile final pricing scheme. More info in the “Bls precompile” thread in the Eth R&D #allcoredevs channel (Relevant folks: EL devs)
- Decide on inclusion of EIP-7762: Increasing the min base fee for blobs. More info on the RollCall meeting tomorrow at 2pm UTC - see the Ethereum calendar (Relevant folks: Rollup representatives)
- Minor renaming of a field in CL data structure (Relevant folks: CL devs)
- Implementation detail of maxEB consolidation process. _More info on the Github agenda above (Relevant folks: CL devs)
- Possible removal of EIP-7742 from Pectra. More info in Eth R&D #allcoredevs channel (Relevant folks: CL devs, anyone wanting CL-only hard forks)

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #147, December 12 2024](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-147-december-12-2024/22161/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #147 summary
> Action Items
>
> Be on the lookout for the Pectra devnet-5 CL specs release! We are near the end of the year, but launching pectra-devnet-5 before EOY would set us up to deliver Pectra to mainnet in a timely fashion in early 2025.
> CL teams: ensure your gossip handling follows the 10MB limit in the spec, and keep an eye on gas limit increases over the next few months.
> NOTE: the next ACDC on 26 December is canceled. Happy holidays!
>
> Summary
> We spent most of the call handling some…

#### Recording

  [![image](https://img.youtube.com/vi/VpYzaCzEVe8/maxresdefault.jpg)](https://www.youtube.com/watch?v=VpYzaCzEVe8&t=193s)

#### Additional info

- Summary by @nixo
- Crypto & Blockchain Research Reports | Galaxy by @Christine_dkim
- Highlights of Ethereum's All Core Devs Consensus Meeting #147 by @yashkamalchaturvedi

## Replies

**ralexstokes** (2024-12-12):

**ACDC #147 summary**

**Action Items**

- Be on the lookout for the Pectra devnet-5 CL specs release! We are near the end of the year, but launching pectra-devnet-5 before EOY would set us up to deliver Pectra to mainnet in a timely fashion in early 2025.
- CL teams: ensure your gossip handling follows the 10MB limit in the spec, and keep an eye on gas limit increases over the next few months.
- NOTE: the next ACDC on 26 December is canceled. Happy holidays!

**Summary**

We spent most of the call handling some final open questions for Pectra.

- Started by checking in with ongoing devnet(s)

mekong: stable, at 36M gas limit

Then turned to `pectra-devnet-5` specs and open questions

- Covered a number of recent PRs to last minute Pectra changes

A minor update to clarify the withdrawals type: Rename PartialPendingWithdrawal field `index` to `validator_index` by lucassaldanha · Pull Request #4043 · ethereum/consensus-specs · GitHub
- An update to EIP-7251 specs to use a validator’s effective balance during consolidation: eip7251: Limit consolidating balance by validator.effective_balance by mkalinin · Pull Request #4040 · ethereum/consensus-specs · GitHub
- Another 7251 update to make proposer and sync committee shufflings scale better in light of higher effective balances: Use 16-bit random value in validator filter by jtraglia · Pull Request #4039 · ethereum/consensus-specs · GitHub
- We agreed to merge all of the above for release of devnet-5 specs

Recent discussions around raising the gas limit prompted us to consider the question on the call, and core devs have been busy making sure changes are safely supported by the network. One concrete suggestion that came out of this work was a suggestion to raise the gossip size limits from 10 to 15MB ([Bump GOSSIP_MAX_SIZE from 10MiB to 15MiB by Giulio2002 · Pull Request #4041 · ethereum/consensus-specs · GitHub](https://github.com/ethereum/consensus-specs/pull/4041)).

- This topic is surprisingly intricate, and there was a lot of interesting discussion on the call around the interplay of gas limit, mempool performance, gossip mechanics on the CL, and DoS prevention. Check the call for the full story!

Interested parties can check this post for more of the core dev perspective on raising the gas limit

On Increasing the Block Gas Limit: Technical Considerations & Path Forward - Ethereum Research

After lengthy discussion, we agreed to:

- CL clients ensure they follow the spec today
- Work on a solution for gossip message sizing that scales with the gas limit (so we don’t have to revisit this conversation every N months)
- Not merge #4041, but have it handy in case it is needed pre-Pectra

N.B.: EIP-7623 in Pectra reduces any near-term concern with the 10MB limit, but there is a question of how client teams handle any outsized gas limit increases between now and shipping Pectra on mainnet.

Next, we turned to EIP-7742 which had a blocker arise during implementation

- As written, EIP-7742 passes the target blob count, but not the max, from the CL to the EL node.
- Implementers found a concrete place where the EL still requires the max in an RPC endpoint for blob pricing (eth_feeHistory).
- There are a number of proposals to address the issue, and we explored them on the call. Key properties that EIP-7742 would unlock are (1) easier blob configuration in client software, and (2) the ability for a CL-only fork to raise blob limits, as the CL would serve as the source of truth.
- We had an update from RollCall to speak to the usage of eth_feeHistory by rollups today; Linea was the only heavy user of this endpoint, but they said they could likely find a workaround.
- Taking the above into account, with a strong preference to not delay Pectra, we decided to remove EIP-7742 from Pectra, and instead preserve property (1) above with a different approach. We did lose property (2), but given the importance of these parameters to both the CL and EL many on the call thought a CL-only fork would be tricky to pull off in any case.

And then to round out the RollCall updates, we received word that EIP-7762 that would raise the minimum blob fee is nice to have, but not critical for rollups today. In light of this fact, and the preference to ship Pectra safely (with fewer EIPs) we decided to not pursue EIP-7762 in Pectra any further.
And we concluded the open spec questions with an update to EIP-2537 which still needs agreement on a gas schedule.

- There has been ongoing work amongst client teams to find the right solution, and there will be a suggestion ready for next week’s ACDE to finalize this EIP.

To wrap up this section, we touched on devnet-5 timelines

- Clients agreed to ship the final specs as quickly as they can, and we will aim to launch the devnet around 20 December, while recognizing possible disruptions with the upcoming holidays.

After Pectra, we had a quick update to rebase PeerDAS onto Pectra in the Fulu fork.

- Make initial Fulu spec by jtraglia · Pull Request #3994 · ethereum/consensus-specs · GitHub
- We agreed to move ahead with this, and while client teams are busy with Pectra, PeerDAS is on the horizon as one of the next most important features.

To close out the call, we had an overview of a proposal to more clearly define the use of CFI/SFI in the ACD process and their relation to devnets.

- Update EIP-7723: CFI/SFI & Devnets by timbeiko · Pull Request #9126 · ethereum/EIPs · GitHub
- This proposal aims to add the right sort of structure to the ACD process so we can remain focused and reduce context-switching with the aim to ship faster!

