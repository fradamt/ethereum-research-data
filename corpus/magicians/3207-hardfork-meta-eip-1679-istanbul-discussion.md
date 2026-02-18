---
source: magicians
topic_id: 3207
title: "Hardfork Meta EIP-1679: Istanbul discussion"
author: axic
date: "2019-04-26"
category: EIPs > EIPs Meta
tags: [hardfork]
url: https://ethereum-magicians.org/t/hardfork-meta-eip-1679-istanbul-discussion/3207
views: 36137
likes: 30
posts_count: 54
---

# Hardfork Meta EIP-1679: Istanbul discussion

I am adding this as the discussion URL for the Istanbul hardfork meta and propose this thread to be dedicated for discussing proposed EIPs and to judge the sentiment when to move them between the stages.

https://eips.ethereum.org/EIPS/eip-1679

## Replies

**boris** (2019-04-26):

Make PRs against 1679 to propose your EIPs https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1679.md

---

**wighawag** (2019-05-06):

I’d like here to bring my objection to EIP-1344 being included in the Istanbul hard-fork. The concerns behind the objections have already be mentioned on the EIP-1344 discussion thread but since this EIP is being finalized and discussion on each EIP are meant to be about technical soundness, the best place to raise my concerns seemed to be here in this discussion thread.

My concerns are as follow :

1. EIP-1344 opcode can be easily misused as can be shown in the discussion thread and explained partially in the rationale of EIP-1344.
Simply doing an equality check is indeed not enough since after a contentious hard fork (that change the chainID), messages signed before hand (with an older chainID) will fail to be valid, breaking signer’s expectation. EIP-1344 rationale propose thus a contract based caching solution to remedy the problem.
2. EIP-1344 requires thus a contract based solution to be used properly in most use-case. This is due to the design of the solution EIP-1344 proposes (namely only letting access the tip of the chainID history). This increase complexity and gas cost for no benefit.
3. In case of minority-led hardfork as described here in details, the contract based caching is insufficient as there will be a gap where a message signed with a past chainID will not be protected from replay.

Note that while I agree with the importance to have a replay protection mechanism for off-chain messages included in the next hardfork, it should not be EIP-1344.

All the concerns mentioned above are non-existent with [EIP-1965](https://github.com/ethereum/EIPs/pull/1965) which achieve full replay protection without requiring added complexity from the users.

EIP-1965 should be thus chosen for off-chain message replay-protection instead of EIP-1344 in the next hardfork.

Why not have both ? Because EIP-1344 has no useful purpose of its own if EIP-1965 was included.

As PR 1965 is not merged in yet though, I can’t add it to proposed list yet. If anyone reading here could help on that, that would be great. Thanks

---

**fubuloubu** (2019-05-10):

I proposed EIP-1344 for Istanbul because I think it’s the most straightforward and flexible proposal for managing chain ID-based domain separation in the application layer. I don’t believe EIP-1965 has to be Accepted to be proposed for Istanbul, so that should not be an issue in proposing it. It does however have several unresolved technical issues concerning how it might be implemented which are being worked through as we speak.

There are many potential use cases for chain ID in the application layer, many of which may yet to be discovered. Some of them require consideration of a change to the value of chain ID in a contentious fork scenario, which is easily implemented in application code per the requirements the developer has for those scenarios (if such a feature is required). EIP-1344 does not wish to be prescriptive of how these scenarios are resolved, instead providing the rationale that developers should consider this scenario when implementing it in their application. Being too prescriptive could potentially be burdensome to the application developer in some circumstances.

That being said, there *are* scenarios where having access to a list of prior chain IDs would be helpful, namely the use of “counterfactual” settlement contracts where transaction history needs to be processed (in scenarios where the results are not simply aggregated in a final message).

I will also state for the record that EIP-1959 was proposed alongside EIP-1344, and may be complementary to it. An oracle contract could be developed to satisfy the intention of EIP-1959 or EIP-1965 if EIP-1344 were made available, with only a marginal increase in complexity of the mechanism required for it to work correctly (the block heights might end up a few off of the true height where the contentious split happened).

There are many options here, and I believe EIP-1344 to be the simplest and most straightforward since the information is already accessible in the VM execution context due to EIP-155, as well as the fact that we haven’t seen a contentious split with EIP-155 implemented at the present time (and that we have no actual process in place for changing it in light of a contentious fork).

---

Edit: I added a link to an example implementation of such a trustless chain ID oracle contract leveraging EIP-1344 to the forum for that proposal here:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png)
    [EIP-1344: Add chain id opcode](https://ethereum-magicians.org/t/eip-1344-add-chain-id-opcode/1131/96) [EIPs](/c/eips/5)



> I decided to draft an example of a “Trustless Oracle Contract” for historical chain IDs, which is something that could very easily be implemented, audited, and leveraged as a standard for any potential use case requiring access to historical chain IDs, without the complexity of alternative proposals.
> Check it out here:
>
>
>
> Again would like to note that assuming what the end user might want to use current chain ID for may not be known in advance, and adding a more complicated API may otherwise…

---

**fubuloubu** (2019-05-10):

One on-topic discussion point. As an example, both EIP-1344 and EIP-1959 (as well as EIP-1965) all use the same opcode number, which seems like putting the cart before the horse. Should EIPs specify opcode numbers?

If instead of the EIPs specifying the opcode number, the Meta Hardfork EIP where the given proposal becomes “merged” into the network where “in charge” of specifying these numbers (as it is arguably a very important implementation detail), then we could avoid this scenario of colliding opcode numbers.

After the Hardfork Meta is merged, we can go back and update the individual proposals for the finalized opcode number at the point the hardfork is completed.

---

**axic** (2019-05-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> If instead of the EIPs specifying the opcode number, the Meta Hardfork EIP where the given proposal becomes “merged” into the network where “in charge” of specifying these numbers (as it is arguably a very important implementation detail), then we could avoid this scenario of colliding opcode numbers.
>
>
> After the Hardfork Meta is merged, we can go back and update the individual proposals for the finalized opcode number at the point the hardfork is completed.

I think this is a reasonable proposal, albeit there must be some placeholders in the EIPs for clients to be able to implement it and create tests. The testing implication is the problem, because a lot coordination is required to assign and sync these opcodes during the implementation and testing phase.

---

**jochem-brouwer** (2019-05-14):

In Constantinople we initially had that [EIP 210](http://eips.ethereum.org/EIPS/eip-210) was going to be a feature of this fork - but it was removed later. Is there any reason why it is not considered to be added to Istanbul?

---

**boris** (2019-05-14):

Because no one has proposed it.

---

**AlexeyAkhunov** (2019-05-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> The testing implication is the problem, because a lot coordination is required to assign and sync these opcodes during the implementation and testing phase

One way to solve it is to parameterise opcode numbers in the tests, we will take it into account

---

**axic** (2019-05-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> One way to solve it is to parameterise opcode numbers in the tests, we will take it into account

The point is that you do need to agree on an opcode in order to genereate tests **and** run those tests on multiple clients. Otherwise one would need to require that:

1. the “test generation team” generates multiple sets for different clients using different opcodes
2. the client teams need to generate tests themselves (which might lead to inconsistencies in tests, defying the purpose of tests)

---

**jochem-brouwer** (2019-05-15):

Sorry for my ignorance, but what is the protocol in place to propose an EIP for Istanbul?

---

**boris** (2019-05-15):

Make an EIP that is at least draft status (is merged in, formatting correct) and then file a PR to add a link to the EIP in proposed section for 1679 which is the meta-EIP for Istanbul.

No sorry required! This is an updated process just starting with Istanbul.

---

**fubuloubu** (2019-05-15):

Yeah, I definitely agree with Alex here that for testing and implementation we’d need to choose *some* opcode number, or else it won’t work (it wouldn’t even make sense). But I think the hardfork EIP should have final say on what the numbers should be since that coordinates what goes into production. It’s fairly easy to change that number if required, I just would like to see this decision purposely documented and enforced by the hardfork meta EIP as a point of process to ensure it goes smoothest.

---

**AlexeyAkhunov** (2019-05-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> Sorry for my ignorance, but what is the protocol in place to propose an EIP for Istanbul?

Do you know who is going to be working on that change? If there is no one who wants to do that, the change will definitely not happen, and in that case there is no point of putting the EIP in.

---

**jochem-brouwer** (2019-05-18):

There is no one. A bit stupid of me to assume I could just propose an EIP when no one is available to work on it.

As a sidenote - the EIP states that “today” (Friday 17 May) is the “hard deadline” to propose EIPs for Istanbul. A timezone is not mentioned, so it is not clear when this hard deadline actually is. I think it should be more clear what the actual time is regarding timezones?

---

**boris** (2019-05-18):

We don’t need to be that strict about it to specify time zones.

---

**AlexeyAkhunov** (2019-05-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> A bit stupid of me to assume I could just propose an EIP when no one is available to work on it.

No, it is not stupid at all. It has been the modus operandi before, but now I am trying to get the process participants accept the obvious (that if noone wants to do an EIP, it won’t be done), and also to remove the bottleneck of relying on go-ethereum or parity or Aleth developers to implement EIPs, as described [here](https://medium.com/@akhounov/ethereum-1x-as-an-attempt-to-change-the-process-783efa23cf60).

---

**MadeofTin** (2019-05-19):

I am in the processing of being hired for testing coordination and helping dimitry. Would be great to sync up on good ways to approach this so I can start opening lines of communitcations with everyone needed. At least we will have one person able to focus on this as 25 EIPs is a lot to sift through. Also, I imagine testing requirements will be a good sifting point.

---

**boris** (2019-05-19):

You should connect with the testing working group



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/eric/48/1236_2.png)
    [Ethereum 1.x Testing Working Group](https://ethereum-magicians.org/t/ethereum-1-x-testing-working-group/3268) [Ethereum 1.x Ring](/c/working-groups/ethereum-1-x-ring/33)



> The Ethereum 1.x Testing Working Group is dedicated to setting the standards for testing Ethereum 1.x.
> This working group is not unlike the testing working group in existence within the Enterprise Ethereum Alliance, where members are attempting to define standards and tests for various enterprise client implementations on the Ethereum network. Simiarly, discussions here will include but are not limited to pre/post fork testing, testnets, identifying key metrics within Ethereum 1.x, conformance …

---

**MadeofTin** (2019-05-19):

Yeah I am talking with them.

---

**fubuloubu** (2019-05-20):

EIP-1702 and EIP-1803 has no `discussions-to`


*(33 more replies not shown)*
