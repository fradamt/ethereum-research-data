---
source: ethresearch
topic_id: 8079
title: A balancing attack on Gasper, the current candidate for Eth2's beacon chain
author: jneu
date: "2020-10-06"
category: Proof-of-Stake > Block proposer
tags: []
url: https://ethresear.ch/t/a-balancing-attack-on-gasper-the-current-candidate-for-eth2s-beacon-chain/8079
views: 11376
likes: 7
posts_count: 15
---

# A balancing attack on Gasper, the current candidate for Eth2's beacon chain

*We thank Yan X. Zhang, Danny Ryan and Vitalik Buterin for review and discussions.*

**This attack was subsequently published in: [“Ebb-and-Flow Protocols: A Resolution of the Availability-Finality Dilemma”](https://doi.ieeecomputersociety.org/10.1109/SP40001.2021.00045)**

[Gasper](https://arxiv.org/abs/2003.03052) is the current proposal for Eth2’s beacon chain. In this post, we summarize a liveness attack against Gasper in the synchronous network model. We have recently presented this attack in [this manuscript](https://arxiv.org/abs/2009.04987), and details can be found in Section II and Appendix A of that manuscript. Python code for a high-level simulation of the attack can be found [here](https://github.com/tse-group/gasper-attack). Check out the code for even more details on how exactly adversarial and honest validators behave in each stage of the attack. The goal of this post is to provide an easy-to-understand explanation of the attack with step-by-step illustrations, so that the attack is accessible for a broad audience and the community can be on the watch for similar issues as they may arise in other contexts.

## Severity of the attack

Before we discuss the attack, a few words to put it in context.

To be able to compare the security guarantees provided by different consensus protocols, the consensus literature usually benchmarks protocols under standard network models. Arguably the most basic model is that of a *synchronous network*, where the adversary can decide for each network message how long to delay its delivery, up to a *maximum delay bound* \Delta. Note that the synchronous model does not allow for network partitions or any other *periods of asynchrony* in which the maximum network delay could temporarily exceed \Delta. Another standard model that captures such periods of asynchrony is that of a *partially* (or *eventually*) *synchronous* network, where before an adversarially chosen *global stabilization time* \mathsf{GST} the adversary can delay network messages arbitrarily, while after \mathsf{GST} the adversary can delay messages only up to a maximum delay bound \Delta. Thus, before \mathsf{GST}, the network undergoes a period of asynchrony or network partition, and with \mathsf{GST} the network returns to its normal synchronous operation.

It is perhaps not surprising that consensus is easier in synchronous networks and harder in partially synchronous networks. (Note that synchronous networks are a special case of partially synchronous networks, with \mathsf{GST} = 0.) Indeed, there are provably secure consensus protocols for synchronous networks that tolerate up to 50\% adversarial validators, while provably secure consensus protocols for partially synchronous networks only tolerate up to 33\% adversarial validators. For a pedagogical example, check out [Streamlet](https://eprint.iacr.org/2020/088).

For our attack, we assume that an adversary has the following capabilities:

A) The adversary knows at what points in time honest validators execute the Gasper fork choice rule \mathsf{HLMD}(G) (see Algorithm 4.2 of [Gasper](https://arxiv.org/abs/2003.03052)).

B) The adversary is able to target a message (such as a proposed block or a vote) for delivery to an honest validator just before a certain point in time.

C) Honest validators cannot update each other arbitrarily quickly about messages they have just received.

Note that A) is given by design of Gasper which has predetermined points in time at which honest validators are supposed to cast their votes. Conditions B) and C) are satisfied in the two standard consensus-theoretic models we have discussed before, because the adversary can deliver its own messages without delay (providing B)) and it can delay messages exchanged between honest validators (providing C)). As a result, we can already conclude that Gasper is not secure even in the basic synchronous network model, and thus also not in the partially synchronous model (where the adversary is strictly more powerful).

It is up to everyone to judge for themselves whether they think an adversary might have the above capabilities in a global consensus mechanism such as Ethereum running over the Internet. Some might perhaps argue that it is unrealistic that the adversary has power over network message delays, as is assumed in standard models.

To this we remark threefold:

- Since we do not know what exact capabilities an adversary might have, why not err on the side of caution and design protocols for pessimistic worst-case scenarios?
- In particular since we have protocols that are secure even under these pessimistic scenarios, why settle for anything short of that?
- Finally, any real system will have plenty of ‘imperfections’ which bring even more uncertainty about the adversary’s capabilities. For instance, network communication is neither point-to-point nor broadcast but a peer-to-peer gossip network – what additional influence over the message delay might this provide for the adversary? Some of such imperfections can be lumped into a pessimistic worst-case model.

Personally, we think that protocols should be evaluated in standard consensus-theoretic models (such as under synchrony or partial synchrony) to avoid making overly specific assumptions about the adversary’s capabilities and running the risk of underestimating the adversary, and to enable a fair evaluation of different protocols.

## Overview of the attack

Now to the attack. Gasper is a vote-based proof-of-stake protocol which combines [Casper FFG](https://arxiv.org/abs/1710.09437) with a committee-based blockchain block proposal mechanism where the fork

is chosen using the ‘greedy heaviest observed sub-tree’ (GHOST) rule under the ‘latest message driven’ (LMD) paradigm, i.e., taking into consideration only the most recent vote per validator. A Gasper vote consists of two parts, a GHOST vote and a Casper FFG vote. While details of Gasper preclude the vanilla bouncing attack (cf. [here](https://ethresear.ch/t/beacon-chain-casper-mini-spec/2760/17), [here](https://ethresear.ch/t/analysis-of-bouncing-attack-on-ffg/6113), and [here](https://ethresear.ch/t/prevention-of-bouncing-attack-on-ffg/6114)) on the Casper FFG layer, Gasper is vulnerable to a similar balancing attack on the GHOST layer.

Recall that Gasper is run with C slots per epoch. For simplicity, let C divide n so that every slot has a *committee* of size n/C. For each epoch, a random permutation of all n validators assigns validators to slots’ committees and designates a *proposer* per slot. Per slot, the proposer produces a new block extending the tip determined by the fork choice rule \mathsf{HLMD}(G) executed in local view G (see Algorithm 4.2 of [Gasper](https://arxiv.org/abs/2003.03052)). Then, each validator of the slot’s committee decides what block to vote for using \mathsf{HLMD}(G) in local view G.

For the Casper FFG layer, a block can only become finalized if two-thirds of validators vote for it. The adversary in our attack aims to keep honest validators split between two options (‘left’ and ‘right’ chain, see Figure 1 for an overview of the attack) indefinitely, so that neither option ever gets two-thirds votes and thus no block ever gets finalized.

[![Fig1](https://ethresear.ch/uploads/default/optimized/2X/2/231ccc2c3873c70420cd1787067c45a139e3aff7_2_422x500.png)Fig11073×1271 189 KB](https://ethresear.ch/uploads/default/231ccc2c3873c70420cd1787067c45a139e3aff7)

The basic idea of the attack is as follows (for a detailed description, see Appendix A of [our manuscript](https://arxiv.org/abs/2009.04987)). The adversary waits for an opportune epoch to kick-start the attack. An epoch is opportune if the proposer in the first slot is adversarial and there are ‘enough’ (six suffice; explained in detail in Appendix A of [our manuscript](https://arxiv.org/abs/2009.04987)) adversarial validators in every slot of the epoch. In particular in the regime of many validators (n \to \infty), the probability that a particular epoch is opportune is roughly f/n, where f is the number of adversarial validators. For ease of exposition, let epoch 0 be opportune.

The adversarial proposer of slot 0 equivocates and produces two conflicting blocks (‘left’ and ‘right’, see Figure 2) which it reveals to two suitably chosen equal-sized subsets of the committee. One subset votes ‘left’, the other subset votes ‘right’ – a tie.

[![Fig2](https://ethresear.ch/uploads/default/optimized/2X/7/71c6140041e4014ab6de5de66ded8e82e9b4e585_2_690x255.png)Fig21073×398 71.7 KB](https://ethresear.ch/uploads/default/71c6140041e4014ab6de5de66ded8e82e9b4e585)

The adversary then selectively releases withheld votes from slot 0 (see Figure 3) to split validators of slot 1 into two equal-sized groups, one which sees ‘left’ as leading and votes for it, and one which sees ‘right’ as leading and votes for it – still a tie.

[![Fig3](https://ethresear.ch/uploads/default/optimized/2X/7/7735b4df368c3ea9443e5c0a66b7d39b9c9e9a81_2_690x236.png)Fig31073×367 59.5 KB](https://ethresear.ch/uploads/default/7735b4df368c3ea9443e5c0a66b7d39b9c9e9a81)

The adversary continues this strategy to maintain the tie throughout epoch 0 (see Figure 4).

[![Fig4](https://ethresear.ch/uploads/default/optimized/2X/c/ca6b283f6f363f5bfd9f3dc58e2573169025e498_2_690x290.png)Fig41073×451 60.3 KB](https://ethresear.ch/uploads/default/ca6b283f6f363f5bfd9f3dc58e2573169025e498)

During epoch 1, the adversary selectively releases additional withheld votes from epoch 0 (see Figure 5) to keep splitting validators into two groups, one of which sees ‘left’ as leading and votes ‘left’, the other sees ‘right’ as leading and votes ‘right’.

[![Fig5](https://ethresear.ch/uploads/default/optimized/2X/1/14415dc3012d0c4125b8799c776721012be827d7_2_690x456.png)Fig51073×710 91.5 KB](https://ethresear.ch/uploads/default/14415dc3012d0c4125b8799c776721012be827d7)

Note that these groups now do not have to be equal in size. It suffices for the adversary to release withheld votes selectively so as to reaffirm honest validators in their illusion that whatever chain they previously voted for happens to still be leading, so that they renew their vote. Due to the LMD paradigm of Gasper’s fork choice rule, only the most recent vote per validator counts. At the end of epoch 1 there are still two chains with equally many votes and thus neither gets finalized.

Finally, for epoch 2 and beyond the adversary repeats its actions of epoch 1 (see Figure 1). Note that the validators whose withheld epoch 0 votes the adversary used to sway honest validators in epoch 1 have themselves not voted in epoch 1 yet. Thus, during epoch 2 the adversary selectively releases votes from epoch 1 to maintain the tie between the two chains. This continues indefinitely.

## Conclusion

Thus, Gasper is not live in the synchronous network model. In fact, all we need for this attack to succeed are the three adversary capabilities presented initially, which are used to sway honest validators via selectively releasing withheld votes. What is more, the block proposal mechanism is rendered unsafe by the attack as the chosen fork flip-flops between ‘left’ and ‘right’. Note that the probability that an epoch is opportune for the adversary to start the attack is \approx f/n (for large n), so that even an adversary controlling only 1\% of validators would have to wait on average only 100 epochs to be able to launch the attack.

## Replies

**alonmuroch** (2020-10-08):

How would the attacker split the network with such isolation?

Also, wouldn’t validators from slot 1 forward will know that 2 blocks for the same height were proposed and will slash one?

---

**jneu** (2020-10-09):

Regarding slashing: Yes, equivocating proposals are slashable, so that first adversarial proposer in slot 0 will get slashed and will lose its stake. But the equivocating blocks themselves are not slashed, but remain part of the consensus process, and the attack continues unimpaired as described above. (How would one “slash a block”?)

Regarding network model: Note that we are not requiring some permanent isolation/separation/partition of validators. At the end of each slot, all validators can see all messages – that’s OK, they will see a tie. All that’s necessary are these capabilities A)-C), in particular B) delivering messages to subsets of validators at a specific time such that C) validators outside the subset can’t hear about these new messages immediately. Standard models (such as synchrony and partial synchrony) allow the adversary to control the network delay (up to \Delta) and thus provide B)+C). The Gasper paper says on p. 8/sec. 2.6: “When studying probabilistic liveness […], we will use the notion (ii) of partial synchrony above.” The attack shows that there is no liveness under that model. (And neither under synchrony.)

---

**nrryuya** (2020-11-08):

Great work!

I also encountered this issue when I was working on the liveness of Casper. (There was a [discussion](https://t.me/c/1223138737/790) in [the Eth2 Telegram channel](https://t.me/c/1223138737/805). Also, the “last-minute delivery” attack appears in another context: see the section [splitting attack](https://ethresear.ch/t/prevention-of-bouncing-attack-on-ffg/6114) in the post of the bouncing attack.)

At that time, I conceived one possible solution. Basically, we modify which attestations (votes) are counted in the fork-choice rule (e.g., GHOST, LMD GHOST, [FMD GHOST](https://ethresear.ch/t/saving-strategy-and-fmd-ghost/6226)). Specifically, to calculate the score of block *B*,

- For attestors (validators who make attestations), only the attestations that are included in a descendant block of B are counted.
- For block proposers, all the attestations observed are counted (the same as before).

In the figures below, we assume a vanilla GHOST, but we can apply the same technique for LMD/FMD GHOST.

[![image](https://ethresear.ch/uploads/default/optimized/2X/e/e203aaf8916302bc8944dca0af63bc1c19c9efa2_2_285x500.png)image393×688 11.1 KB](https://ethresear.ch/uploads/default/e203aaf8916302bc8944dca0af63bc1c19c9efa2)

With this modification, the attacker cannot “sway” honest attestors by releasing attestations. Let us assume that the block proposer of the current slot is honest, and the attacker does not publish any saved block. The honest attestors in this slot receive the newly proposed block before they make an attestation (by the synchrony assumption). They calculate the score of blocks based on the same set of attestations, i.e., the attestations included in the proposed block or the blocks they received by the previous slot. Therefore, they vote for the same block.

Ties of blocks are broken in favor of the number of attestations that vote for them but are not included in any block yet.  Let us assume a case where there is an honest slot, and the next slot is adversarial (i.e., the attacker is selected as the block proposer). Here, the attacker can ignore the honest block and attestations from the previous slot and make a fork. The score of the newly proposed attacker’s block and the honest block from the previous slot is zero, making a tie. However, the honest block voted by the honest attestations from the previous slot wins by the tie-breaking rule and gains the current slot’s honest attestations. If the block proposer of the next slot is honest, these attestations are included in a block.

[![image](https://ethresear.ch/uploads/default/optimized/2X/d/d3e03b5f3ea507ef3f56c527708d7896aae085a8_2_554x499.png)image740×667 33.1 KB](https://ethresear.ch/uploads/default/d3e03b5f3ea507ef3f56c527708d7896aae085a8)

This also shows that honest attestations in an adversarial slot can increase the main chain’s score later unless an attacker’s chain takes over the main chain.

---

**kladkogex** (2020-11-10):

Great, timely and important work!!! Congratulations guys!

Several comments:

1. The attack can be made even simpler by the attacker (proposer) releasing/not releasing a single unique block to a subset of nodes.

The two-block attack could be addressed by adding a uniqueness proof requirement for every proposal, requiring every proposal to be signed by a  supermajority 2 t + 1 signature of the committee (we do it at SKALE btw).

But if fact you do not need to have two blocks! You can have a single block and still keep Gasper from finalizing forever by the attacker carefully distributing/non-distributing the block to a subset for participants, and then keeping the system in the unstable equilibrium forever.

The proportion of the bad guys can be epsilon, where epsilon can be artbitrary small.

1. Second, it seems that algorithms like Gasper are  UNFIXABLE per se, simply because a liveliness proof of Gasper would imply a binary consensus algorithm with a constant complexity per participant, which is as far as we know is too good to be true.

All practical binary consensus algorithms that we know have complexity N  per participant. This means, that an algorithm that finalizes a system with large N in constant  time as Casper claims to do probably **does not exist.**

What authors suggest instead is using a probable consensus protocol like PBFT to infrequently finalize shapshots, which makes total sense to me.

---

**vbuterin** (2020-11-12):

> For attestors (validators who make attestations), only the attestations that are included in a descendant block of B are counted.

The problem with this approach is that it removes a lot of the important benefits that we gain from counting attestations outside of blocks. Particularly, it hands local-consensus-making power back into the hands of proposers, and so gives short-range attackers power to do nasty things. One example is that if you control two slots in a row, and the head before you is B, then you can make a sister of B (call it B’), attest to it, make a child B’’ including the attestations, and then from the point of view of the attesters in the slot after B’‘, B’’ is the winner, and after *their* attestations supporting B’’ it wins the fork choice counting all attestations too.

The fact that the current LMD design allows for hundreds of independent “confirmations” to happen in parallel is a key part of its power to avoid such situations.

---

**vbuterin** (2020-11-12):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Second, it seems that algorithms like Gasper are UNFIXABLE per se, simply because a liveliness proof of Gasper would imply a binary consensus algorithm with a constant complexity per participant, which is as far as we know is too good to be true.

I don’t think this is true, at least in the appropriate model for this circumstance. Particularly, chain-based PoS protocols have come up with liveness proofs, and those do have constant complexity per participant. So this suggests that we can solve the problem by importing the key characteristic of chain-based protocols (namely, the proposer bottlenecking) in a safe way, which is what I have proposed here:


      ![](https://ethresear.ch/uploads/default/original/2X/5/50c8596d557541aeba2b4e2c4be22d9542e8c360.png)

      [HackMD](https://notes.ethereum.org/@vbuterin/lmd_ghost_mitigation)



    ![](https://ethresear.ch/uploads/default/original/2X/8/882285f3628ea3784835c306639dd8f62179a6d9.png)

###



# Proposal for mitigation against balancing attacks to LMD GHOST  One key way in which eth2's fork c

---

**nrryuya** (2020-11-12):

Thanks for replying! I agree that in my proposal block proposers have much more power on the fork-choice. However, we still preserve some benefits of the “many parallel voting” paradigm.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> One example is that if you control two slots in a row, and the head before you is B, then you can make a sister of B (call it B’), attest to it, make a child B’’ including the attestations, and then from the point of view of the attesters in the slot after B’’, B’’ is the winner, and after their attestations supporting B’’ it wins the fork choice counting all attestations too.

Let *n* be the number of validators, *h(x)* (resp. *a(x)*) be the number of honest (resp. attackers’) attestors allocated to slot *x*, and *i* be the slot when block *B* is proposed. The small attack to fork *B* off fails if the next honest proposer favors *B*, i.e., *h(i)+ h(i + 1) > a(i + 1) + a(i + 2) + h(i + 2) = n - h(i + 1) + n = 2n - h(i + 1) <=> h(i)/2+ h(i + 1) > n*.

We are already assuming that most slots have a supermajority of honest attestors to make a successful crosslink. If it is true for slot *i* and slot *i + 1*, *h(i) > 2n/3 and h(i + 1) > 2n/3*, and then the attack fails.

[![image](https://ethresear.ch/uploads/default/optimized/2X/c/c53cd26c5e3ad8539e05458099df63bf51fd66ff_2_238x500.png)image326×684 17.7 KB](https://ethresear.ch/uploads/default/c53cd26c5e3ad8539e05458099df63bf51fd66ff)

The attack is possible in more unlikely cases, e.g., the attacker has three slots in a row, but all the attacker can do is just to fork one block off.

---

**vbuterin** (2020-11-13):

Hmm, ok you’re right that it’s three and not two. Though even still, an attacker with portion p of the stake being able to revert blocks \frac{1}{p^3} of the time is not ideal, especially given that the attacker knows ahead of time when they’ll be able to do this! Hence the interest in still taking into account attestations that are not part of any block.

One way to think about this is: why not make a linear hybrid between the two techniques: from an attester’s PoV, attestations that are not in a block only have weight 1/2, or even 3/4? This would reduce the vulnerability to proposer manipulation even further, but still leave proposers with enough decision-swaying power to force everyone to agree on one block or the other. And I think this actually starts to come pretty close to what I proposed above, so maybe it’s a different way of thinking about the same type of solution…

---

**kladkogex** (2020-11-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I don’t think this is true, at least in the appropriate model for this circumstance. Particularly, chain-based PoS protocols have come up with liveness proofs, and those do have constant complexity per participant. So this suggests that we can solve the problem by importing the key characteristic of chain-based protocols (namely, the proposer bottlenecking) in a safe way, which is what I have proposed here:

My gut feeling about this you can probably prove liveliness of non-finalizing PoS algorithms. BTC and ETH1 never finalize. ETH2 without Casper never finalizes.

If a blockchain finalizes (using say Casper), this pretty much make it a solution of a binary consensus problem.

Indeed, you can simply deploy a smartcontract that collect votes of byzantine generals, and once the SC collect 2 t + 1 votes , it will solve the binary consensus problem by simply choosing the the majority vote (1 or 0).

So **any finalizing blockchain leads to a practical solution of binary consensus**, which is, as we suspect **O(N^2) at best**.  No one ever proved that one cant do binary consensus better than O(N^2) but many people tried and did not invent anything better.

Based on the hand waving argument above,  ETH2 **may be made provably live without finalization**,  but if one wants to finalize, the attacks as described in the paper may be **unaddressable.**

It is my subjective feeling based on the argument above.

It may be that one needs to act out of the box, in particular involve PoW or VDF to help resolve the deadlock, as I suggest here



    ![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png)

      [Fixing balancing attacks on Gasper using VDF](https://ethresear.ch/t/fixing-balancing-attacks-on-gasper-using-vdf/8224) [Proof-of-Stake](/c/proof-of-stake/5)




> Here a balancing attack on gasper is described.
> https://ethresear.ch/t/a-balancing-attack-on-gasper-the-current-candidate-for-eth2s-beacon-chain/
> The essence of the attack IMO is to bring the complex network into an undecided equilibrium of a split vote and then use a small number of malicious nodes to keep the system in the undecided equilibrium forever.
> I think it may be impossible to solve problems like this while staying purely PoS  in large systems, since essentially resolving an undecid…

Essentially I am suggesting to use a VDF to introduce a new proposer if finalization gets stuck. The proposer can affect things if things are not stuck, since VDF time can be made larger than a typical finalization time.

As far a the block proposal uniqueness is concerned, it can be easily addressed by having a proposal signed by a 2 t + 1 signature of a committee.  It is an easy fix which would make ETH2 work much better.

To summarize, I do not have exact proof for what I am stating,  but the argument seems pretty strong to me.

Another direction for thinking is how realistic the attacks are.  It may be that some of them become impractical when the system grows because computational requirements on the attacker grow fast. Essentially keeping a system in unstable equlibrium requires lots of effort.

It may be that one can do faster binary consensus under the assumption that computational resources of the attacker are finite. It is a really interesting direction of research IMO.

---

**hest** (2020-11-18):

[@jneu](/u/jneu) This is very interesting work, and agreed with [@kladkogex](/u/kladkogex) that these type of timing attacks apply beyond Eth2 to most PoS I’ve seen.

Beyond halting the protocol, or preventing any finalization, wouldn’t there be the added issue of growing adversarial power.

Namely, this attack could be run recursively, splitting the “left” and “right” votes into “left-left”, “left-right”, “right-left” and “right-right” in a later epoch, and so on. In each of these sub-forks, the power needed to reliably “sway” the vote decreases given honest power is split across each of these forks. Accordingly, this could allow a relatively small adversary not just to delay finality, but to control vote outcomes in the chain when they choose to end the recursion.

---

**jneu** (2020-11-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/hest/48/5316_2.png) hest:

> Beyond halting the protocol, or preventing any finalization, wouldn’t there be the added issue of growing adversarial power.

Could you elaborate on this “amplification via recursion” idea? Our attack succeeds for any adversarial fraction \beta>0, as long as n and C are such that the adversarial \beta-fraction of each committee (committees are of size n/C) in an epoch amounts to \geq 6 adversarial validators. So six adversarial validators per slot are enough to sway (any number of) honest validators between two options in perpetuity.

---

**vbuterin** (2020-11-19):

I don’t see how finalization makes proving liveness harder. It’s fairly easy to prove that a finalizing consensus algo is live if most participants are building on top of the same blocks, and “most participants are building on top of the same blocks” is exactly the property you get if the chain is live. So proving liveness of the non-finalizing component is sufficient to prove liveness of the finalizing component.

---

**hest** (2021-01-06):

Hi [@jneu](/u/jneu). Sorry for the lag.

I guess my question, is could you do it with fewer than 6 adversarial validators: in the case where a tie can be maintained by the adversary for a bit. Could you run the attack within each of your “left” and “right” validator constituencies again by waiting for an “opportune” epoch there and once more splitting the validators. Each time this is done, the likelihood that a given epoch will be opportune increases given the fact that the honest fraction of each constituency decreases.

Did that make sense?

---

**kladkogex** (2021-01-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> So proving liveness of the non-finalizing component is sufficient to prove liveness of the finalizing component.

It depends on how you define liveliness.  Is something live if it does not finalize?

Having said this,  it it seems like getting bad actors in PoS networks seems to be realistic (I mean that the worst thing people do is inactivity).

