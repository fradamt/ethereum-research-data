---
source: ethresearch
topic_id: 23409
title: "A trivial form of PBS: MEV Lock"
author: potuz
date: "2025-11-07"
category: Consensus
tags: [mev]
url: https://ethresear.ch/t/a-trivial-form-of-pbs-mev-lock/23409
views: 469
likes: 9
posts_count: 11
---

# A trivial form of PBS: MEV Lock

I learned this idea (if not exactly the same something very similar) from [@JustinDrake](/u/justindrake).

## Summary

With EIP-7732 coming in the Gloas fork, we have new on-chain validators with a specific withdrawal prefix `0x03` that are allowed to produce payloads and bid for their inclusion. In this proposal, I describe a very simple to implement way of separating completely the builder role from the proposer role of validators. This mechanism has several advantages:

- It solves completely the [free option]( [2509.24849] The Free Option Problem of ePBS ) problem.
- It removes any comunication proposer  builder affecting  latency of block building and slot pipelining.
- It removes some of the complexity of the consensus specification around builder payments to proposers.
- It has a positive effect in the economics of ETH the asset.

## The mechanism

The mechanism is very simple, it consist of

1. Remove any validating duties and rewards/penalties from 0x03 validators. Their stake is only locked up in the beacon chain without getting rewards nor being penalized.
2. Remove any cap on the stake of 0x03 validators, they are allowed to stake as much as they want.
3. The protocol chooses builders at random, in a similar way as we do now with proposers, only from 0x03 validators. This choice is sampled randomly but weighted by stake.
4. Add an automatic failsafe mechanism to temporarily blacklist some 0x03 builders if they fail to deliver some payloads and ultimately fall back to self building if no more 0x03 builders are available.

## Pros

- The free option problem dissapears as there is no commitment to a particular payload from the builder. There is only the deadline at the time of revealing, blocks and blobs.
- There is no need for the proposer to commit at all to any bid from the builder, the proposer only commits to the parent block hash in the execution layer, the builder needs to build on top of that execution head. This way, the decentralized set of proposers keep decisions on forkchoice. Builders only sequence the chain.
- There is no need for any communication between consensus proposers and execution builders.
- There is no need for any payment mechanism to pay a bid from the builder to the proposer. The builder no longer pays anyone, their cost is the capital cost of being staked.
- MEV revenue shifts from proposers to being shared by builders (as they no longer need to pay bids) and ETH holders (as the cost of the missed interest rate on the locked ETH which is paid by builders, is ultimately shared by all ETH holders).
- If the protocol so desires, we can even do a form of MEV burn by actually charging the 0x03 stake a constant rate according to market conditions.

## Cons

- This is a centralizing force on block building. FOCIL or any forced inclusion list mechanism is necessary for this system to be implemented.
- Staking pools would be affected. However, staking pools by definition have control over large amounts of ETH. If the MEV revenue lost from fees becomes more than the capital cost of staking that ETH as a 0x03 validator, staking pools can themselves be builders and potentially auction out off protocol their slots.
- Collusion between a centralized set of builders is possible. In many respects, on the one hand multiple slot MEV becomes more predominant when there is a reduced set of builders. On the other hand a small set of builders may collude to minimize their locked capital cost. However, since the system is permissionless, it is rational for ETH holders to stake in this situation, mitigating both aspects.

## Replies

**Julian** (2025-11-10):

Hey [@potuz](/u/potuz) ! Thanks for writing this up. I think the mechanism you describe here is almost the same as [Execution Tickets](https://ethresear.ch/t/execution-tickets/17944). The difference is that potential builders buy tickets by staking instead of by paying money directly for the tickets. The “buying part” of the two mechanisms is different but the way in which building rights would be allocated is similar, e.g. use RANDAO to allocate building rights randomly with some lookahead.

Execution Tickets has known drawbacks, which you also point out.

- Multi-slot MEV becomes possible because it is known beforehand which builder builds the next block. If builder A knows it builds two slots in a row it could adjust the contents of the first block to extract more MEV in the second one. Multi-slot MEV has negative externalities on users and makes it harder to design applications.
- Block building becomes more centralized since builders need to predict block value.

The fundamental problem with multi-slot MEV in this design is that it is known beforehand who builds the next X blocks. In MEV-Boost builders need to compete again every slot so it is only known who builds the next block just before it needs to be propagated.

The probability of being allocated two consecutive slots in this design depends on the fraction of 0x03 stake any builder controls. I think we cannot rely on that probability simply being very low. The builder market is very concentrated today because the difference in profitability between the top builders and the rest is large. If builders do not collude, they could still find multi-slot MEV opportunities, however, it may then not be rational for ETH holders to stake so multi-slot MEV is not mitigated.

---

**potuz** (2025-11-12):

Hey yeah it is exactly like ET just that the stake is already in the CL and is already locked. I think the multislot MEV thing is not that much of a problem with the CL doing the auction because we can potentially apply WHISK-like techniques and only reveal the builder for the current slot at the current slot. Or it can be as simple as having  the Randao reveal take into account sub-epoch blocks/payloads.

---

**Julian** (2025-11-13):

To prevent multi-slot MEV the builder of block N should not know whether it will also be the builder of block N+1.

A potential way to do so is to do a MEV-Burn and appoint the execution proposer of slot N in the beacon block of slot N (assuming beacon block and execution payload are separated). That looks a bit like the following.

[![APS_Beam_Call_#5 (1)](https://ethresear.ch/uploads/default/optimized/3X/e/3/e3e4ae8562d4d7b3c81e23064ae1587ef0c777df_2_690x388.png)APS_Beam_Call_#5 (1)960×540 25 KB](https://ethresear.ch/uploads/default/e3e4ae8562d4d7b3c81e23064ae1587ef0c777df)

The problem is that no one knows who will be the block N execution proposer in the time interval after the execution payload of slot N-1 is released and before the beacon block of slot N is released. That removes the possibility of providing preconfs during that time interval.

If we do want to have preconfs and prevent multi-slot MEV, we would need to generate randomness just after the last execution payload. It may look something like this

[![APS_Beam_Call_#5](https://ethresear.ch/uploads/default/optimized/3X/5/4/542ca4ac227d7d5a159c371871736d300a2589f6_2_690x388.png)APS_Beam_Call_#5960×540 33.5 KB](https://ethresear.ch/uploads/default/542ca4ac227d7d5a159c371871736d300a2589f6)

I wouldn’t know how to get this to work in the context of Ethereum though. At first I thought that it would be possible to use an encrypted mempool and then generate randomness based on e.g. the hash of the post-state root given that transactions are encrypted after block 99 in the image. Together with [@b-wagn](/u/b-wagn) I explored [encrypted mempools](https://ethresear.ch/t/hybrid-encrypted-mempools/23360) but they do not have a clear solution either.

If you could explain a bit more what you mean with the WHISK-like techniques or RANDAO that would be very nice!

---

**potuz** (2025-11-14):

What I’m pointing out is that when the builders are registered at the CL, we can just reveal the builder whenever we want. It doesn’t need to be an epoch before. It can be right before the slot. And the randomness can use information from the CL proposer right up to the involved slot ( or one before  ). So it’s simple to enable preconfs by just revealing the next builder after the last payload (or CL block) is revealed . All of this is already implemented and existing code in the CL. As a form of optimization we just fix the proposers a couple of epochs in advance. But there used to be some efforts to hide this right until the time of proposal. This is what WHISK does and it was merged into the CL spec repo until not long ago [Whisk: A practical shuffle-based SSLE protocol for Ethereum](https://ethresear.ch/t/whisk-a-practical-shuffle-based-ssle-protocol-for-ethereum/11763) . Those efforts were a little hindered by the proposer lookahead in Fulu in EIP-7919 but we can keep the CL proposer lookahead and still use those techniques to hide the builder until the last moment. All of these are already available in the CL. I’m not pointing to anything new, I’m just pointing that we have most of this available and implemented and it enables MEV burn as soon as Glamsterdam is we wanted to.

---

**jcschlegel** (2025-11-19):

Two additional points besides what Julian wrote:

- I have made the point in the past that PoS can have slightly better market structure than some versions of execution tickets. So that is in favor of your proposal.
- On separating the roles of proposing and validating and having two pools of stake for the two roles. People have argued in favor of similar un-bundling of roles, e.g. rainbow staking. What I find potentially problematic is that it is more wasteful: In the status-quo, staked ETH is used to provide economic security, for consensus duties and for proposer selection. With your proposal, the 0x03 stake just does the last thing. So un-bundling and using the stake separately uses capital less efficiently, it’s in some sense the opposite of re-staking.

---

**potuz** (2025-11-20):

I wouldn’t say the stake is useless, but yes, the 0x03 stake would not be useful for economic finality, but it’s useful for other purposes. As long as the market equilibrium keeps a decent economic security I don’t think this is much of the problem, as this stake also won’t affect the base reward, in principle could consist in large part from stake that wouldn’t go as 0x01/2 otherwise

---

**aelowsson** (2025-11-21):

It seems to me that with this mechanism, the supply of `0x03` validators will expand and contract with the value of the MEV. If MEV increases tenfold, the supply of `0x03` validators will expand rather close to tenfold, etc. It seems more intuitive to avoid capital inefficiencies by also letting `0x03` validators participate in consensus, and to keep the supply/proportion of `0x03` validators fixed, varying the fee for being eligible for builder selection. The simplest changes are thus to keep `0x03` validators staked, and to keep a fixed proportion of `0x03` validators by running a 1559-style auction to set the fee taken out each epoch for being a `0x03` validator. The fee is burned. It’s like [ABPS](https://ethresear.ch/t/rainbow-roles-incentives-abps-focilr-as/21826#p-53062-h-2-abps-4), but adapted to concern only `0x03` validators, targeting a lower proportion.

Note that `0x03` validators will still need to sell the right to build the blocks rather often, because the builder able to extract the most MEV from the block won’t always be selected (albeit this will then be done out-of-protocol).

In any case, the concerns both you and Julian raise seem rather important. In my view, slot-auctions could be great for tackling the free option problem. Although there are then other issues to go through, they could potentially be resolved.

---

**potuz** (2025-11-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) aelowsson:

> Note that 0x03 validators will still need to sell the right to build the blocks rather often, because the builder able to extract the most MEV from the block won’t always be selected (albeit this will then be done out-of-protocol).

I do not see this as a problem, or rather it is secondary to the design. If `0x03` validators want to resell their rights off protocol that may even make for a healthier market. The point is that the protocol will have already had collected MEV rewards that today are impossible to collect (and the proposers are getting them). So since I am being asked this elsewhere I want to spell this out:

- CL proposers will not get anything anymore from MEV.
- Builders will not need to bid at all, no need to pay nor divert any priority fees to any proposer.
- The protocol will regularly charge a rent to 0x03 validators. So not only these validators will not accrue staking rewards, but rather they will be burning their principal.

This way the protocol gets to collect part of the MEV that is today collected by proposers. Reselling JIT will need to at least offset this rent.

---

**aelowsson** (2025-11-27):

The quotes from the post and the last comment are difficult to reconcile for me:

![](https://ethresear.ch/user_avatar/ethresear.ch/potuz/48/11413_2.png) potuz:

> There is no need for any payment mechanism to pay a bid from the builder to the proposer. The builder no longer pays anyone, their cost is the capital cost of being staked.

![](https://ethresear.ch/user_avatar/ethresear.ch/potuz/48/11413_2.png) potuz:

> The protocol will regularly charge a rent to 0x03 validators. So not only these validators will not accrue staking rewards, but rather they will be burning their principal.

If we are in agreement on charging `0x03` validators for the opportunity to be selected to build the block, then it looks more viable. This is also where the [pricing mechanism](https://ethresear.ch/t/rainbow-roles-incentives-abps-focilr-as/21826#p-53062-h-5-dynamic-pricing-auction-dpa-32) in attester–beacon proposer separation comes in. There is a fixed proportion of stake in the pool eligible for proposal rights, and the price adjusts dynamically to maintain this proportion.

If we believe that block-building rights will be resold anyway, it seems we can allow for a bigger pool of validators to participate, while they at the same time perform their consensus duties. And the cost of opting-in to the opportunity of being selected is priced according to the dynamic mechanism. However, since we may not feel the need to sell both proposal rights, it can indeed be only the execution proposal rights that are allocated in this manner, as this post suggests.

Let me know if I misunderstood something.

---

**potuz** (2025-11-28):

Yeah it seems that I agree with your way of trivializing the proposal: if we do think these will be resold, then it just boils down the the current status quo, except with the nuance that we may actually have negative issuance on some validators that are allowed to build from time to time.

