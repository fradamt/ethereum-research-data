---
source: ethresearch
topic_id: 1923
title: Casper FFG Contingency Plan
author: fubuloubu
date: "2018-05-06"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/casper-ffg-contingency-plan/1923
views: 2020
likes: 9
posts_count: 7
---

# Casper FFG Contingency Plan

Great presentation about Casper FFG at EdCon. It seems many years of effort are finally paying off as the team prepares for the release of the most anticipated smart contracts ever created.

One interesting thing about CFFG is the phased approach the team is taking. Casper FFG is a finality layer on top of the PoW chain, adding higher security through economic finality to the chain, enough so that there have been discussions on reducing the block reward as the economic security of the network moves slowly from PoW to PoS.

Let’s assume PoS is released to the mainnet. It has been deployed for about a year, and it has worked very well up to this point, accuring 10M ETH in deposits by many 1000s of dedicated validators. Correct me if I’m wrong, but that would make the Casper FFG contract one of the largest honeypots by value ever created as a smart contract, with around 10% of all Ether locked into this account (and at much higher valuations than the DAO).

Now, the team is undergoing multiple verification approaches, which is the right process for building a smart contract which we all know is impossible to change once deployed. This verification will surely weed out easy exploits from the contract, ensuring that any potential exploit would have to be extremely creative. The fact remains, in software, there is ALWAYS something that can be improved, sometimes outright bugs do exist. No amount of verification activity can ever counteract that, only add higher degrees of confidence in the system.

The TL;DR of it all is this:

What process is the Casper FFG team following for monitoring and event response in case an exploit is found, either by a White Hat (who reports the exploit in secret) or a Black Hat (who uses the exploit to drain and/or lock funds in the Casper FFG contract)?

1. Is there a way to lock the operation of the contract (at least the methods that affect fund deposit/recovery) until a proper recovery procedure has been identified?
2. If the exploit traps or withdraws all of the funds in a short time period, how does the PoW reward respond to this event in order to increase the economic security of the network? How does that affect the economics of the network?
3. Is there a way to mitigate this large honeypot through fund storage in a much simpler contract, with defined entry/exit points and the ability to lock access in case of an attack?
4. What is the transition and communication procedure for handling this event, to ensure it occurs as smoothly as possible to those in the community who are rightly concerned?

---

Thank you to an engineer from a company that has undergone a similar exploit event. He reminded me the importance of deployment and response procedures for handling smart contract exploit events, something they have developed as a team in response to their incident and is now integral to their smart contract development process.

## Replies

**ChosunOne** (2018-05-06):

I would imagine in the event of an extreme bug is found, a hard fork is the only appropriate response.  An on-chain mechanism to disrupt normal function will increase the attack surface and perhaps be the primary target for an attacker.  Considering how this is a protocol level change, a hard fork to fix a protocol level bug seems entirely reasonable.

---

**djrtwo** (2018-05-07):

First of all, let’s establish that the FFG contract is part of the core protocol. In the event that we find a protocol level bug of any type (FFG or otherwise), I imagine the community would in general be willing to HF. The FFG contract is interesting in that it is a contract so some might subject it to the arguments of immutability and ‘code is law’, but I ask the community to not be blinded by the choice to put this protocol level code in a contract. Casper FFG could have been entirely implemented at a lower level in the protocol but was chosen to be implemented as a contract in the EVM to reduce the likelihood of consensus errors across clients (we have this virtual machine, the EVM, that all the clients are very good at replicating. Let’s pack as much protocol level stuff into this virtual machine to make client’s jobs easier).

**TLDR**: FFG is part of the core protocol. If the protocol is broken, we should fork to fix it.

To address your specific questions

1. No, there is not a way to lock the operation of the contract. This would introduce serious centralization concerns. That said, clients will ship with a --casper-fork-choice flag that will allow them to disable the casper fork choice and revert to pure PoW. This does not deal with the deposits/recovery but gives the rest of the protocol some peace of mind. All valid routes out of the contract involve a 4 month withdrawal period which implies that at least many of the potential bugs would give us this withdrawal a period to make and execute a plan.
2. Even with the reduction of PoW reward to 0.6 ETH/block, the ethereum network on PoW alone still has a substantial security especially in comparison to other top PoW blockchains. See here for analysis of current and future PoW security. If it were assessed during an attack that PoW was not substantial enough, an increase in block reward during a recovery HF could be considered.
3. I’m not sure if a separate contract would significantly reduce the complexity of the in/out procedures of the FFG contract. That said, if someone proposes a model that does demonstrate increased simplicity to model correctness, we’d be open ears. As for locking this contract, I disagree with that being a reasonable solution. What sort of conditions do you think can/should lock the contract? Central actor? Validator vote? N of M stewards of the contract? I’d be concerned with any of those.
4. We should definitely think about this more. Consider the different attack scenarios and range of needed response. We are working on spec’ing out what migrating the contract would look like in a future non-attack HF, and this might illuminate some of the procedures that could be taken in the event of an attack/hack. I’ll post here when we have something more concrete.

100% agree it’s time to discuss and think through this some more. Thank you for bringing it up. It’s been something that has been simmering on low in the back of my mind, but now is a good time to dig in.

---

**liangcc** (2018-05-07):

Come up with this plan with Danny. We have some scenarios of successful attacks and the respective hard fork strategies. Feedbacks are welcomed ![:grinning:](https://ethresear.ch/images/emoji/facebook_messenger/grinning.png?v=9) .


      [gist.github.com](https://gist.github.com/ChihChengLiang/3f138c896721a519b9d438e9d75e77d4)




####

##### Casper_Contingency_plan.md

```
# Casper Contingency Plan

[toc]

## Scenarios that trigger the plan

- Contract bug that can increase arbitrary deposit to a validator.
    - Fix:
        - [R] Need to adding an assert line in a function.
        - [W] Need to add a new varible in validator struct to track new info.
```

This file has been truncated. [show original](https://gist.github.com/ChihChengLiang/3f138c896721a519b9d438e9d75e77d4)

---

**fubuloubu** (2018-05-07):

Awesome! This is exactly what I like to hear as a response, that we have plans and procedures in place for failures and how the clients and validators can mitigate certain classes of events.

It’s really the right time to be thinking about contingencies, as rollout occurs and issues arise we have an analysis to point to as a guideline for what we should do in moments of crisis. If only more smart contract systems developed such documents, we could respond to scenarios in a much faster and more formal way, and build scripts and tools for helping us to mitigate any scenarios that are uncovered.

I will have to take a look at that document and comment when I get a chance. I’m really very excited for Casper FFG’s release on the main net following Vitalik’s presentation at EdCon, as well as Karl and Vlad’s presentations.

---

**fubuloubu** (2018-05-07):

Also, in a similar vein, do you guys have an “envelope expansion plan”? (Excuse the aerospace-y terms)

Such a plan would include an analysis of how the system should grow as it becomes adopted, and what would happen in case there’s too much or not enough interest, both initially and over time. I know the system is incentivized towards 10M ether (IIRC), is that the only metric for success? What should the growth and adoption curves look like for a successful release? (+/- some error bounds) What would lead to calling the trial a failure in terms of hard numbers? (Which would trigger a re-parameterization effort and/or a mechanism redesign)

---

**data** (2018-06-08):

I assume that the verification of the contract will include  [@djrtwo](/u/djrtwo)’s condition that all valid routes out of the contract involve a 4-month delay.

If however the quick withdraw from the above document becomes true, the proposed solution in the document above is to revert to a previously finalized block. There might also be scenarios not described yet that require such a reversion(?).

By reverting, we will necessarily revert some operations on the blockchain. At least for value transfers, would a recovery fund as proposed before be an option? The intention here is to not have users bear the cost of core protocol breakage. However, a pure recovery fund will probably not cover a substantial subset of smart contracts, such as ERC721 tokens etc., so it is probably too specialized a solution?

PS: Good initiative. I think both update & recovery options need to be clear before deployments to the mainnet, no matter how well verified and proofread the contract is. This goes doubly so for the economic incentivization.

