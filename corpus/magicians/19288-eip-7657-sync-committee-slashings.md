---
source: magicians
topic_id: 19288
title: "EIP-7657: Sync committee slashings"
author: etan-status
date: "2024-03-21"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7657-sync-committee-slashings/19288
views: 2138
likes: 15
posts_count: 8
---

# EIP-7657: Sync committee slashings

Discussion thread for [EIP-7657: Sync committee slashings](https://eips.ethereum.org/EIPS/eip-7657)

Related notes:

- Sync committee slashing · Issue #3321 · ethereum/consensus-specs · GitHub
- Light client roadmap for Electra - HackMD
- Light Clients Breakout Room - March 6, 2024 - HackMD

Also, could be interesting when combined with Max-Effective-Balance increasing proposals, as that would increase the slashable balance when the sync committee members can have higher balance!

## Replies

**eawosika** (2024-04-20):

Hi [@etan-status](/u/etan-status)! I wrote a [thread](https://twitter.com/eawosikaa/status/1781659545846136876) on Twitter to get more attention to this EIP. I couldn’t find your Twitter account, or I’d have tagged you in the post. Feel free to share with anyone who needs a high-level overview/rationale!

---

**amattm** (2024-04-25):

Thank you [@eawosika](/u/eawosika) for raising the attention here. From a Altair protocol consumer perspective Sygma is super interested in this effort and we will start supporting this more actively. I have reached out to the Lodestar team as well as our respective R&D teams, so we can start contribute here. Expected some more detailed feedback soon.

---

**greg** (2024-04-25):

Very excited for this!!

---

**etan-status** (2024-04-25):

I’m indeed absent from most social media, including Twitter. The day only has so many hours ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

Thanks for the thorough analysis, I think one aspect that’s missing is that the light client may be combined with a trusted multisig. For example, have bridge operators stake additional assets and require them to only submit light client data to the contract which they validated against a full node. It would be great to include that approach in the analysis, so that it becomes easier to see how much value we get with the EIP, and how urgently it is needed to be useful (does it have to be Electra, or can it be bundled with F-fork?)

I’d be interested in advancing the slashing proposal as well, as in, formalizing the specifications and so on, but the other light client related EIPs ([Execution Layer Meeting 186 · Issue #1016 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1016#issuecomment-2077790649)) are farther developed as of now, so prioritization is challenging. I’d also be willing to step in as reviewer/mentor, if someone else wishes to advance the sync committee slashing EIP.

---

**littlehatboy** (2024-05-18):

Given that the likelihood of fraud occurring in the sync-committee is quite low, as stated in Succinct’s article on sync-committee, and considering there are more “profitable” methods, such as finalizing incorrect blocks, what is the motivation or need for implementing this EIP given that it requires changes to the consensus layer?

---

**amattm** (2024-06-13):

[@eawosika](/u/eawosika) We are currently unsure if it’s worth pursuing this effort as:

1. There is reasonable critics as @littlehatboy has mentioned and
2. EIP-7945 - which should make full-consensus verification  feasible - is confirmed for the next hard fork.

We have therefore decided to check feasibility of full-consensus verification first before investing more efforts on advancing Altair-based approaches beyond what we currently have.

---

**eawosika** (2024-06-17):

Cool! I think Succinct’s article makes a great point about probabilities, but it’s still a trust assumption IMHO. Working on full consensus verification would be better than still using Altair (if slashing isn’t implemented). I guess this means you’ll need to build out circuits that verify Casper FFG consensus? I’ve seen some examples [here](https://research.polytope.technology/zkcasper) and [here](https://polyhedra.medium.com/proving-full-node-of-ethereum-in-zk-c7ffaaa688dd).

