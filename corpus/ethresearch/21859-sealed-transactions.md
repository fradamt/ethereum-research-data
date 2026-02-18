---
source: ethresearch
topic_id: 21859
title: Sealed transactions
author: aelowsson
date: "2025-03-01"
category: Proof-of-Stake
tags: [mev]
url: https://ethresear.ch/t/sealed-transactions/21859
views: 1456
likes: 12
posts_count: 16
---

# Sealed transactions

Thanks to [Julian](https://x.com/_julianma) and [Kev](https://x.com/kevaundray).

## Introduction

Ethereum lacks a trustless mechanism to shield transactions (txs) from MEV extraction. The current recourse—private orderflow—gives trusted actors excessive control over the tx supply network, degrading decentralization and censorship resistance of MEV inducing txs. To alleviate this, the [shutterized beacon chain](https://ethresear.ch/t/shutterized-beacon-chain/12249) proposal uses an encrypted mempool, with encryption keys provided by a set of “[keypers](https://ethresear.ch/t/shutterized-beacon-chain/12249#shutter-6)”. The encrypted txs are included in a block, and the keypers then use threshold cryptography to decrypt the txs in time for their final execution in a subsequent block. A potential concern is the protocol’s reliance on keypers to honestly and consistently perform their duties.

Recent proposals also based on threshold cryptography include a [roadmap for leveraging proposer commitments](https://ethresear.ch/t/the-road-towards-a-distributed-encrypted-mempool-on-ethereum/21717) and an alternative approach using [smart-account encrypted mempools](https://ethresear.ch/t/smart-account-encrypted-mempools/21834). A simple cryptographic strategy, relying on participants themselves for encrypting and decrypting their data, was recently proposed in the form of a [sealed execution auction](https://ethresear.ch/t/sealed-execution-auction/20060). Builders make sealed bids for the right to propose an execution block. The sealed bids are collated and builders then reveal their bids, as observed by attesters. The next proposer collates the revealed bids in the block, and attesters provide attestations contingent on correct collation.

This post explores *sealed transactions*, relying on the primitive developed in the sealed execution auction to achieve an encrypted mempool. It introduces a new tx inclusion path that users can rely on to trustlessly protect their txs against MEV extraction. Users broadcast sealed txs which are commitments consisting of a cryptographic hash computed from the raw tx and a top-of-block fee f_\text{ToB}. These are included in a commitment struct in the first block. Users then unseal their raw txs, as observed by attesters, and the txs are included top-of-block in the next block, ordered by f_\text{ToB}. Attesters attest to the block contingent on correct collation. The mechanism is thus “fork-choice enforced”, a strategy familiar from [FOCIL](https://ethresear.ch/t/fork-choice-enforced-inclusion-lists-focil-a-simple-committee-based-inclusion-list-proposal/19870), [MEV smoothing](https://ethresear.ch/t/committee-driven-mev-smoothing/10408), [MEV burn](https://ethresear.ch/t/mev-burn-a-simple-design/15590), and the [sealed execution auction](https://ethresear.ch/t/sealed-execution-auction/20060).

## Mechanism

Figure 1 outlines the sealed transactions mechanism.

- Before T_1 – Users post sealed txs to the mempool. Sealed txs can be formatted similar to regular txs, but lack to and value fields. They further contain a cryptographic hash. This hash is computed from the raw tx that will eventually be “unsealed” and executed, alongside the f_\text{ToB}. A special form of gasLimit for the tx to be unsealed is also provided, which is charged in full beforehand, directly when the sealed tx is committed. It must cover for the gas consumed by the unsealed tx and will hereinafter be denoted as the gasObligation. The transactor might wish to specify a higher gasObligation than necessary, to further obfuscate the content of the tx.
- T_1 – Sealed txs are included in a specific commitment struct in Block A. Gas for inclusion in the struct (e.g., covering for storing the sealed tx) as well as the gasObligation are charged from the transactor and burned. The priority fee befalls the proposer of Block A. To ensure that the transactor eventually is able to pay the penalty if it fails to unseal its tx, the penalty is reserved by the protocol, for example by charging and burning it, to then be returned upon correct inclusion. The commitment struct has space for txs up to some proportion g_p of the gas limit g_l. Thus, the total gasObligation across all entries in the commitment struct must be below the threshold g_t=g_p \times g_l.
- T_2 – Once a user has observed its sealed tx in a commitment struct and is sure that Block B is the next block to be proposed, it broadcasts its unsealed tx to the mempool, thus also revealing the f_\text{ToB}. Nodes might at this point only propagate unsealed txs if the cryptographic hash contained in the sealed tx matches the hash computed from the unsealed tx, but this depends on compute requirements. Users indicate Block A as the correct anchor for the unsealed tx (for example by block hash) to ensure that the unsealed tx is invalid if Block A is reorged. They can include a priority fee with the unsealed tx.
- T_3 – Attesters observe the timeliness of unsealed txs at T_3, e.g., 3s before the new slot begins. They verify that the cryptographic hash in the sealed commitment matches the hash computed from the unsealed tx and that the raw tx otherwise also fits requirements. If a tx is not properly unsealed at this point, they record that it can be penalized. This will ultimately depend on if the proposer includes the unsealed tx in Block B or not.
- T_4 – The proposer of Block B orders proper unsealed txs top-of-block sorted according to f_\text{ToB} and the f_\text{ToB} is burned. The priority fee(s) can be used as a tiebreaker for ordering, and, in either case, the tx hash can be used as a final tiebreaker. The reserved amount for the penalty is returned for properly unsealed txs. For accounting purposes, the proposer may indicate missing unsealed txs with a reference to the corresponding sealed tx, although this is otherwise implied from Block A. If Block B fails to extend the blockchain, the unsealed txs are instead scheduled for the next block.
- T_5 – Attesters attest contingent on correct collation.

[![Figure 1](https://ethresear.ch/uploads/default/optimized/3X/1/f/1f3f7888ca461dfea7e9015b55423dcb722bf65b_2_690x400.png)Figure 12638×1532 295 KB](https://ethresear.ch/uploads/default/1f3f7888ca461dfea7e9015b55423dcb722bf65b)

**Figure 1.** The sealed transactions mechanism. Sealed txs with associated gas fees are broadcast and collated in `Block A`. They are then unsealed by the transactors themselves, as observed by attesters, and included top-of-block in `Block B`, ordered by f_\text{ToB}. Attesters finally attest contingent on correct collation.

## Discussion

### User sophistication and UX

One concern is the increased sophistication required from transactors that wish to utilize the trustless mechanism. Users who do not run a node must rely on their wallet to fetch data from providers such as Infura or Alchemy. The wallet could for example issue a JSON-RPC API call similar to `eth_getTransactionReceipt` for their sealed txs, in this case instead requesting data from the commitment struct (clients must implement this extension). Upon call receipt and assurance that `Block B` is the next block to be proposed, the wallet will release the unsealed tx. This whole procedure will be automated from the user’s perspective, but increased complexity is still something to keep in mind.

Users also take on the risk of being penalized if their unsealed tx does not reach the attesters on time—*and*—the proposer does not see it, or elects to not include it upon realizing that attesters have not observed it in time. Given that proposers may act as a safety net to include late unsealed txs, a priority fee should presumably also be implemented for unsealed txs (in extension to f_\text{ToB}). There is no other reason for priority fees, given that proposers are forced to include unsealed txs via the fork choice rule. Users must further hold sufficient balance so that the penalty can be reserved.

### Liveness

Constraints to the fork choice must always be scrutinized, to ensure that it does not get overloaded in such a way that liveness is degraded. The rationale for directly relying on fork-choice enforcement in sealed transactions is that all relevant txs are known—if they are scheduled for inclusion they must have been included in a prior block. There is thus a finite number of txs for attesters to observe, and they will have a list of these txs ready beforehand. Yet, this list ought to perhaps not be too extensive, which is ultimately determined by g_t. The potential for liveness degradation, together with degraded UX, are probably the biggest drawbacks of the proposed mechanism and *merit further scrutiny*.

One question is whether [includers](https://ethresear.ch/t/fork-choice-enforced-inclusion-lists-focil-a-simple-committee-based-inclusion-list-proposal/19870) otherwise can be leveraged, as a middle-man between transactors and the proposer. Any unsealed txs included in the \text{IL}_\text{agg} will of course need to be included in the block. However, if the mechanism strictly relies on ILs for enforcement, the transactors must trust includers to properly include their unsealed tx. This would seem like a fairly severe downgrade to what is otherwise a trustless mechanism for preventing MEV extraction. Of course, it would be possible to have includers instead/also list *sealed txs* before T_1, to prevent their censorship. However, txs with unknown content are less likely to be censored in the first place.

### Inclusion delay

Should there be a delay between `Block A` and `Block B`, or should these blocks be consecutive? Furthermore, should transactors independently be able to set such a delay? One reason for a delay is that it gives greater certainty to the transactor that `Block A` will not get reorged. A reorg could occur under the current Gasper consensus mechanism. Under SSF, reducing the delay to 0 seems appropriate. The damage from a block reorg is however moderate. The unsealed tx would still not be executable if `Block A` is reorged, because the tx will specify that `Block A` is the only block to which it anchors. A shorter delay is naturally generally better simply because it enables a tx to be settled faster.

Giving the transactor the ability to independently set the delay could be beneficial. But one cause for concern then is the additional complexity in keeping txs from overflowing some specific future block. The gas threshold g_t must in this case have a forward property and apply to blocks in the future. The proposer would be responsible for tracking txs committed to a future block and ensuring that they do not exceed g_t. There would at the same time still need to be some threshold also for the commitment struct and a limit to how many slots in the future a tx can specify. In some scenarios, users will be eager to have their tx included in a specific slot in the future. Allowing the user to specify a specific future slot for the unsealed tx, as opposed to only a generic delay from getting the sealed tx included, would make this possible. Such an option would prevent a sealed tx from getting included in the “wrong” slot when the user must rely on a delay while trying to target a specific future slot.

### Magnitude of penalty for failure to unseal a tx

What should the penalty be for a failure to unseal a tx? This depends on how much MEV that can be extracted—in expectation—by posting sealed txs with the intent of only unsealing them if it is profitable to do so. It is not a straightforward MEV extraction technique—the extractor must guess the potential tx content and will lack knowledge of f_\text{ToB} and thus the ordering of txs available for extraction. With some appropriate estimate of the expected value of this MEV extraction technique, the penalty can be designed, accounting for the already existing cost of sealed txs (remember, the user must always pay the full gas amount already at `Block A`). The penalty should presumably be fixed, perhaps adding a component that varies with the basefee as well. It is of course possible that a penalty of zero turns out to be appropriate. Finally note that the sealed txs can still be backrun when building the rest of the block, though this is not particularly harmful.

### Mechanics during missed slots

If the slot is missed, the queued txs are instead included in the next block. The unsealed txs will thus never be skipped over just because `Block B` fails to extend the blockchain; they must be included in the correct order in the first successful block. If there is a delay between `Block A` and `Block B`, there might be several queued batches up to g_t of gas of unsealed txs ready for inclusion, once there are missed blocks. For example, if there is a delay of two additional slots between the blocks and a block is missed, then the next block would need to include two batches of unsealed txs. Two solutions are possible:

- If the delay is moderate and g_t also moderate, all txs can be mandated to be included in the first posted block after the missed proposals.
- Another option is to delay by blocks from Block A to Block B, not slots. Thus, if a block is missed, the entire queue is shifted one slot. It should however be noted that this can disrupt the user’s timing for unsealing the tx when a block gets reorged, thus complicating the approach.

Does the sealed transactions mechanism provide an additional reason to pursue missed proposal penalties? Since tx ordering is not disrupted by a failed proposal, it might not be critical but is still one of many reasons to increase incentives for proposers to avoid missed slots.

## Replies

**MCarlomagno** (2025-03-02):

Great stuff ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) just one question

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) Anders Elowsson:

> Magnitude of penalty for failure to unseal a tx

Why to penalize at all? If the sealed tx was fully paid then there is no damage other than a little waste of blockspace

---

**aelowsson** (2025-03-02):

Thanks!

![](https://ethresear.ch/user_avatar/ethresear.ch/mcarlomagno/48/18816_2.png) MCarlomagno:

> Why to penalize at all? If the sealed tx was fully paid then there is no damage other than a little waste of blockspace

The penalty serves to enhance MEV protection in cases where it could otherwise be profitable to post speculative sealed txs with the intent of only unsealing them whenever they are able to extract MEV.

However:

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) Anders Elowsson:

> It is not a straightforward MEV extraction technique—the extractor must guess the potential tx content and will lack knowledge of f_\text{ToB} and thus the ordering of txs available for extraction.

It would thus be interesting to develop estimates of the expected MEV from such techniques. After this:

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) Anders Elowsson:

> With some appropriate estimate of the expected value of this MEV extraction technique, the penalty can be designed, accounting for the already existing cost of sealed txs (remember, the user must always pay the full gas amount already at Block A).

I do believe that a zero (skipped) penalty is one possible outcome of such an analysis.

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) Anders Elowsson:

> It is of course possible that a penalty of zero turns out to be appropriate.

---

**Marchhill** (2025-03-04):

I recently wrote the post you referenced on [smart account encrypted mempools](https://ethresear.ch/t/smart-account-encrypted-mempools/21834) and have some thoughts on how the two approaches compare. Generally I see smart accounts as another way of achieving sealed transactions.

> Recent proposals also based on threshold cryptography include a roadmap for leveraging proposer commitments and an alternative approach using smart-account encrypted mempools

These proposals are not based on threshold cryptography, they address something separate. We need to separate the commit-reveal mechanism (eg. threshold cryptography), from how rules for including unsealed transactions are enforced (eg. smart accounts, proposer commitments). The proposals are concerned with the latter, and are independent of the commit-reveal scheme used.

I would characterise this design for sealed transactions as using an *enshrined fork-choice* approach for enforcing rules, and a *manual commit-reveal* scheme where users have to reveal their unsealed txs at some time.

## Enshrined

- In my post I categorised encrypted mempools by how they their enforce rules. This approach is most similar to a stage 3 enshrined mempool.
- Enshrinement is a good option in the long term, but will require large coordination to pull of complex changes to the protocol such as including new attestation committees for sealed transactions. This would need to be implemented through a hard fork; it could take a long time to reach consensus on a design ready to be included.
- Enshrinement also locks us in to one design, encryption scheme etc. Out-of-protocol solutions can benefit from more experimentation and improvements, such as in cryptography.

## Fork-Choice enforced

- An important difference from how I categorised stage 3 mempools is that instead of enforcing through the block validity conditions, this approach uses fork choice. This means that it does not provide unconditional frontrunning protection, as attesters may fail to reorg a block which frontruns unsealed transactions.
- An interesting approach is to augment smart account enforcement with fork choice. This provides guarantees of unconditional frontrunning protection. It improves the UX of the smart account approach in the case that a proposer does not include unsealed transactions and includes other (potentially frontrunning) transactions. Normally users would have to resubmit their transactions as they would no longer execute, but instead attesters could attempt to reorg the block and the unsealed transactions could be included in the next one.

## Manual commit-reveal

- The design requires users to reveal their unsealed transactions instead of using a threshold encryption approach like Shutter that aims to avoid this by effectively automating the reveal process.
- Having to manually reveal unsealed transactions would add significant added complexity for wallets.
- It allows attacks where the user does not reveal their unsealed transactions, which could be profitable even if they are slashed.
- Requires significant added complexity of new attester committee, and potentially timing difficulties to reveal unsealed transactions in time for the proposer to include them.
- If you want to avoid the honest majority assumption of threshold encryption, using delay encryption seems like a more promising approach to me.

## Misc

> Users indicate Block A as the correct anchor for the unsealed tx (for example by block hash) to ensure that the unsealed tx is invalid if Block A is reorged

It is unclear to me how the unsealed transaction is invalid here, this is where I think smart accounts are useful. Maybe you are suggesting to enshrine this into the validity conditions for all transactions which could add significant overhead. Also when users post their transactions they would not know the hash of block A which has not been proposed yet, so I suggested including the slot number which would achieve the same goal of tying the transaction to block A.

> Once a user has observed its sealed tx in a commitment struct and is sure that Block B is the next block to be proposed

How could a user be sure of the next block?

> Transactors must trust includers to properly include their unsealed tx

With FOCIL, inclusion list builders have no control over where transactions will be included in the final block, this is determined by the builder.

> the gasObligation [is] charged from the transactor and burned

Burning ETH to reserve space is the same approach [currently used by Shutter](https://github.com/gnosischain/specs/blob/8e4376dac4148b152ee7c9a9f1ad6b1c59793abe/shutter/high-level.md#transaction-submission). One disadvantage here is that it imposes significant gas overhead as the user must pay double the gas costs, to first burn, and then execute their unsealed transaction.

A promising approach using smart accounts could be to send ETH to a paymaster to reserve space, and having the paymaster then cover the gas costs of your unsealed UserOp. In this way the user only pays for gas once. You could send extra to the paymaster to cover future transactions and amortise the gas costs of transferring.

> Users broadcast sealed txs which are commitments consisting of a cryptographic hash

Using hashes could leak information, [using another type of commitment](https://ethresear.ch/t/smart-account-encrypted-mempools/21834#p-53079-hashes-or-commitments-17) could be better.

> top-of-block fee

Minor point - is it necessary to introduce a new fee here? Proposers could instead order by priority fee.

---

**aelowsson** (2025-03-04):

Thanks for your feedback!

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> These proposals are not based on threshold cryptography, they address something separate.

Thanks for pointing that out. Agreed that smart accounts for enforcement does not require threshold cryptography. Your post is perhaps better described as “centered around” threshold cryptography as all the examples provided include keypers for releasing the keys. But yes, the idea of smart accounts themselves for enforcement is not based on threshold cryptography, we can agree on that.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> The design requires users to reveal their unsealed transactions instead of using a threshold encryption approach like Shutter that aims to avoid this by effectively automating the reveal process.

..“automating” is doing heavy lifting here. There are benefits and drawbacks with both mechanisms. Just different trade-offs.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> Having to manually reveal unsealed transactions would add significant added complexity for wallets.

I would like to learn more about this. The initial feedback I have received is that this “shouldn’t be a problem”. But that is just one data point, so wallet providers are welcome to chime in.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> It allows attacks where the user does not reveal their unsealed transactions, which could be profitable even if they are slashed.

Which attacks are you thinking about? Could you provide an example? Other than deferred MEV extraction, which is addressed in the post.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> Users indicate Block A as the correct anchor for the unsealed tx (for example by block hash) to ensure that the unsealed tx is invalid if Block A is reorged

It is unclear to me how the unsealed transaction is invalid here, this is where I think smart accounts are useful. Maybe you are suggesting to enshrine this into the validity conditions for all transactions which could add significant overhead.

When attesters review the unsealed tx, they must confirm that the commitment hash of the sealed tx matches the unsealed tx. They would at this time also confirm that the block hash matches. This check could be part of a validity condition or part of the temporal fork-choice enforcement. In either case, it only needs to apply to unsealed txs.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> Also when users post their transactions they would not know the hash of block A which has not been proposed yet, so I suggested including the slot number which would achieve the same goal of tying the transaction to block A.

When users post their unsealed tx, they are aware of Block A, which has already been proposed. The link is not part of the hashed commitment.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> Once a user has observed its sealed tx in a commitment struct and is sure that Block B is the next block to be proposed

How could a user be sure of the next block?

Once a user has observed the block prior to Block B, they will know that Block B is the next block to be proposed which can include txs and become part of the chain. This block may not be Block A if the mechanism uses a delay, hence the formulation.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> Transactors must trust includers to properly include their unsealed tx

With FOCIL, inclusion list builders have no control over where transactions will be included in the final block, this is determined by the builder.

For clarity, I will first include the full quote

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) aelowsson:

> However, if the mechanism strictly relies on ILs for enforcement, the transactors must trust includers to properly include their unsealed tx. This would seem like a fairly severe downgrade to what is otherwise a trustless mechanism for preventing MEV extraction.

To answer your statement, it does not matter if the unsealed tx was listed by an IL or not, it will still need to be ordered according to its ToB fee for the block to be confirmed.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> ..imposes significant gas overhead as the user must pay double the gas costs

The gas cost is only paid once, in Block A.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> Using hashes could leak information, using another type of commitment could be better.

Would be interesting to study further. My initial assumption was that the hashing of a tx containing a signature hash would be sufficient, but I am not a cryptographer.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> top-of-block fee

Minor point - is it necessary to introduce a new fee here? Proposers could instead order by priority fee.

The priority fee needs to still go to the builder and has a different function than the ToB fee.

---

**Marchhill** (2025-03-05):

> all the examples provided include keypers for releasing the keys

I didn’t make it too clear in the post but here I was using the term ‘keyper’ in the way I defined it in the talk I linked in the post. Instead of being specific to threshold cryptography, I use it in a more abstract way to refer to some entity that releases keys, it could be through delay encryption, or the users revealing themselves.

> Which attacks are you thinking about? Could you provide an example? Other than deferred MEV extraction, which is addressed in the post.

I’m referring to deferred MEV extraction; while having a penalty could mitigate the issue it doesn’t exist when the reveal happens ‘automatically’.

> This check could be part of a validity condition or part of the temporal fork-choice enforcement

To make this work in all cases you would need to modify the validity conditions or use smart accounts. As I mentioned fork-choice enforcement will not always work because attesters can fail to reorg a block, so we cannot consider the transactions to be invalid.

> When users post their unsealed tx, they are aware of Block A, which has already been proposed. The link is not part of the hashed commitment.

I don’t see how it could not be part of the hashed commitment? If it is part of the unsealed transaction then we would have needed it to calculate the commitment hash, which is calculated before block A. If it is not part of the unsealed transaction then the unsealed transaction can be copied and used anywhere.

> Once a user has observed the block prior to Block B, they will know that Block B is the next block to be proposed which can include txs and become part of the chain.

How could they know what the block will be because they have seen the previous block? There is a circular dependency here, block B should contain the user’s unsealed transaction but the unsealed transaction will not be revealed until the user knows the contents of block B.

> This block may not be Block A if the mechanism uses a delay, hence the formulation.

How could block A and B be the same block?

> Transactors must trust includers to properly include their unsealed tx

> it does not matter if the unsealed tx was listed by an IL or not, it will still need to be ordered according to its ToB fee for the block to be confirmed.

My point here was that includers don’t have the power to enforce the rules around ordering, this seems to be what is meant by ‘properly includ[ing] their unsealed tx’.

> The gas cost is only paid once, in Block A.

Ok that wasn’t too clear to me, this would require further protocol changes to waive the gas fee for unsealed transactions with a proof of burn then.

> The priority fee needs to still go to the builder and has a different function than the ToB fee.

Ah I see, I missed before that this ToB fee is burned. I suggested that the priority fee could be used for this purpose as this gives an incentive to proposers, but if it is enshrined you don’t necessarily need to as they are forced to include (although this isn’t always the case with fork-choice as I’ve mentioned). As you stated there may still be some priority fee to cover the case that the unsealed tx is late, but the overall reward would likely be minimal or non-existent compared to if the ToB fee went to proposers; users could just make sure to unseal in a timely fashion.

This could be an issue as now proposers have no incentive to include unsealed transactions. Consider a proposer that should build on a block with many sealed transactions that they will be forced to include for no reward. There is an incentive not to build on this block by trying to use proposer boost to reorg it. The proposer would then have no constraints imposed on them so they could fill their whole block with more valuable transactions.

I think this is always a potential problem and not a deal-breaker, but having more incentive to include unsealed transactions could mitigate it.

---

**aelowsson** (2025-03-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> I’m referring to deferred MEV extraction; while having a penalty could mitigate the issue it doesn’t exist when the reveal happens ‘automatically’.

There are no definite guarantees against MEV extraction in either variant; there are just trade-offs. With threshold encryption, the keypers can sneakily help builders extract much more MEV, getting paid for that service. What would be interesting is some analysis of the expected value of probabilistic MEV extraction.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> When users post their unsealed tx, they are aware of Block A, which has already been proposed. The link is not part of the hashed commitment.

I don’t see how it could not be part of the hashed commitment? If it is part of the unsealed transaction then we would have needed it to calculate the commitment hash, which is calculated before block A. If it is not part of the unsealed transaction then the unsealed transaction can be copied and used anywhere.

The requirements are that the hashed commitment relates to specific fields (while not being possible to predict, for example by including a signature hash) and that there is a final signature over the overall unsealed tx containing the link.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> Once a user has observed the block prior to Block B, they will know that Block B is the next block to be proposed which can include txs and become part of the chain.

How could they know what the block will be because they have seen the previous block? There is a circular dependency here, block B should contain the user’s unsealed transaction but the unsealed transaction will not be revealed until the user knows the contents of block B.

They will know that Block B will be next in line because they have observed Block A (and any other block in between Block A and Block B if there is a delay; refer to the [associated section](https://ethresear.ch/t/sealed-transactions/21859) regarding the delay in the original post). There is no circularity in recognizing that once a block has been proposed, the next block must be the one proposed in the subsequent slot.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> This block may not be Block A if the mechanism uses a delay, hence the formulation.

How could block A and B be the same block?

Block A and Block B are never the same block. It is however not always the case that Block B comes directly after Block A. This depends on whether there is a delay in the final implementation.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> My point here was that includers don’t have the power to enforce the rules around ordering, this seems to be what is meant by ‘properly includ[ing] their unsealed tx’.

“transactors must trust includers to properly include their unsealed tx” referred to the scenario where the protocol would rely on the \text{IL}_\text{agg} for enforcing the inclusion rule of unsealed txs (ordering could still be by ToB fee). However, as stipulated in the original post, this was deemed undesirable and discarded as an option.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> The gas cost is only paid once, in Block A.

Ok that wasn’t too clear to me, this would require further protocol changes to waive the gas fee for unsealed transactions with a proof of burn then.

Yes, the unsealed txs are special txs. There will be a check ensuring that the transaction does not consume more gas than the prepaid `gasObligation`.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> There is an incentive not to build on this block by trying to use proposer boost to reorg it.
>
>
> ..I think this is always a potential problem and not a deal-breaker, but having more incentive to include unsealed transactions could mitigate it.

Yes, this is why the post suggests that introducing a delay between Block A and Block B might be reasonable if Sealed transactions were to be implemented before SSF. Otherwise, as you say, some further mandatory incentive could be considered.

---

**Marchhill** (2025-03-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) aelowsson:

> There are no definite guarantees against MEV extraction in either variant

This is why I think delay encryption could be the endgame solution when the cryptography is ready. It has the advantages of threshold crypto without the honest majority assumption.

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) aelowsson:

> The requirements are that the hashed commitment relates to specific fields (while not being possible to predict, for example by including a signature hash) and that there is a final signature over the overall unsealed tx containing the link.

My point here is that you need to include something which ties it to a specific block at the point you create the hashed commitment to prevent it being copied and used elsewhere. Since the block hash is not available when the commitment is created that is why I suggest using the slot number.

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) aelowsson:

> They will know that Block B will be next in line because they have observed Block A (and any other block in between Block A and Block B if there is a delay; refer to the associated section regarding the delay in the original post). There is no circularity in recognizing that once a block has been proposed, the next block must be the one proposed in the subsequent slot.

I’m still confused by this. If we’ve seen Block A and are waiting for the next block, there is no way to know what will be proposed in the next slot unless you are the builder / proposer (even they don’t know until all txs are unsealed) - there may be no block at all. Do you mean that we know that Block B will contain certain unsealed transactions?

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) aelowsson:

> the post suggests that introducing a delay between Block A and Block B

I think this could be unsafe, which I discussed in [an argument for reorg safety](https://ethresear.ch/t/smart-account-encrypted-mempools/21834#p-53079-reorg-safety-15).

Consider we allow a one block delay on inclusion, so the constraint (sealed tx) is posted in block A, then we allow one extra block B, before the unsealed transactions are included in block C. A malicious proposer of block B could potentially frontrun the unsealed transactions by delaying the reveal of their block and attesting to it in private. Now the unsealed transactions will be revealed and block C will be built on block A. Now the malicious proposer reveals block B which contains frontrunning transactions and attempts to reorg out block C. Now the unsealed transactions can be included in a future block C’ built on block B: the unsealed transactions have been frontrun.

I’d be interested to analyse further how viable this attack is, but my current opinion is that the unsealed transactions should only be included in the next block after the constraint is posted with no delay.

---

**sg** (2025-03-06):

I’m concerned about the scenario where Keypers, who are responsible for providing encryption keys, also operate MEV extraction nodes. If they observe a transaction with a potential MEV reward significantly higher than the `fToB` fee, they have a direct incentive to bypass the encryption process and extract that MEV. This could lead to a situation where only low-value MEV transactions are protected, while high-value ones remain vulnerable. Has the potential for this type of exploitation been analyzed?

---

**aelowsson** (2025-03-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/sg/48/14420_2.png) sg:

> I’m concerned about the scenario where Keypers, who are responsible for providing encryption keys, also operate MEV extraction nodes.

There are no keypers; users encrypt and decrypt their txs themselves in a trustless manner.

---

**and882** (2025-03-06):

I think that’s an interesting and necessary debate to have over the assumptions of different encrypted mempool designs. While I see the appeal of having users reveal their own sealed transactions, I think it comes with some limitations:

1. as was mentioned already, letting the wallet reveal the sealed transaction probably adds quite some complexity for wallets.
2. there is the question of how to deal with issues on the user side, e.g., what happens if the user device loses internet connection or crashes?
3. lastly, as already mentioned in the proposal, the user has to constantly monitor the blockchain (through services like Infura etc.).

In general I believe it’s important to keep complexity away from the user side and rather outsource it to the network.

On the other hand, I understand the concern of Keyper collusion in a threshold encrypted mempool. In the Shutter team, we have looked quite a bit into this issue and are currently following several paths to deal with that issue:

1. together with PolyCrypt, we are working on ShutterTEE, where the key share of a Keyper is stored inside a TEE. The TEE allows access to the key share only, when the Keyper can prove that it has a legitimate interest in using the share. This basically allows us to combine the security guarantees of TEEs and threshold encryption.
2. making collusion traceable in threshold schemes is an active area of academic research and we are closely following the progress there (see e.g. here)
3. we are looking into various directions to use slashing to disincentivize collusion.

For delay encryption, I think the main problem is to set the difficulty parameter correctly, so that the transaction gets revealed just in time. There are other issues though that we listed in our [recent blog post](https://docs.shutter.network/docs/shutter/research/the_road_towards_an_encrypted_mempool_on_ethereum).

---

**sg** (2025-03-06):

Understood, thank you.

For elaboration:

1. existing proposal (shuttered beacon chain) - a scheme using Keypers (key holders), where these trusted entities provide the encryption key and decrypt the transaction using a threshold cipher.
2. new proposal (sealed transactions) - a self-sovereign approach that does not require Keypers, where users themselves “seal” transactions (hash-based commitments) and later “open” them (expose the original transaction).

And so my question has been updated:

The main advantage of the new approach is that it provides more trustless MEV protection by allowing users to perform encryption and decryption themselves, without relying on trusted third parties (Keypers). However, there is a restriction that users must pay a sufficiently high top-of-block fee (fToB) for high-value MEV transactions.

I’m curious about your thoughts on this economic balance - do you think this requirement for high fToB fees for valuable transactions creates a practical limitation? Or is this an acceptable trade-off for achieving trustlessness?

---

**aelowsson** (2025-03-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/sg/48/14420_2.png) sg:

> The main advantage of the new approach is that it provides more trustless MEV protection by allowing users to perform encryption and decryption themselves, without relying on trusted third parties (Keypers). However, there is a restriction that users must pay a sufficiently high top-of-block fee (fToB) for high-value MEV transactions.
>
>
> I’m curious about your thoughts on this economic balance - do you think this requirement for high fToB fees for valuable transactions creates a practical limitation? Or is this an acceptable trade-off for achieving trustlessness?

Note that all unsealed transactions end up top-of-block—the ToB fee is only used for ordering between these txs. My expectation is therefore that most transactors will leave the ToB fee at 0 or close to 0.

---

**aelowsson** (2025-03-08):

Thanks for your feedback [@and882](/u/and882) (and once again thanks to [@Marchhill](/u/marchhill)).

#### Generalizing Sealed transactions

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> This is why I think delay encryption could be the endgame solution when the cryptography is ready.

![](https://ethresear.ch/user_avatar/ethresear.ch/and882/48/19073_2.png) and882:

> ..letting the wallet reveal the sealed transaction probably adds quite some complexity for wallets.
> ..what happens if the user device loses internet connection or crashes?
>
>
> For delay encryption, I think the main problem is to set the difficulty parameter correctly, so that the transaction gets revealed just in time.

I do believe there are benefits and drawbacks of all decryption schemes. However, to better understand the contributions of this proposal, it can be interesting to first take a step back and look at the similarities that exist between Sealed transactions and the Shutterized beacon chain:

1. Some form of sealed tx is broadcasted acting as a commitment
2. ..and included in a block.
3. Within a defined time period, an unsealed tx is broadcasted
4. ..and subsequently included top-of-block.

Sealed transactions however differ in that:

- the protocol does not provide the means for decryption,
- the protocol does provide enshrined oversight of the release of the unsealed tx, relieving the proposer of its duties if this tx is not provided. This is ensured by the fork-choice enforcement mechanism.

This distinction is particularly useful in the context of generalizing encrypted mempools. Given some standardized format for the commit–reveal scheme, there would be nothing stopping a transactor from independently using threshold decryption for unsealing the tx in (3). They could for example engage a restaking service such as EigenLayer to this end. Some users may prioritize broad staker coverage for Sybil resistance, others may prefer a diverse set of identifiable parties, and some will ultimately favor a fully trustless solution. Delay encryption could also be leveraged in various setups—it is hard to predict beforehand which among these that will be the most favorable. The consensus layer does not need to have an opinion on this matter and does not need to enshrine one specific decryption scheme. It can merely provide a framework that can be used by any scheme, including the proposed trustless variant.

Re-reading your recent [roadmap post](https://ethresear.ch/t/the-road-towards-a-distributed-encrypted-mempool-on-ethereum/21717), it seems you are indeed looking to a [future](https://ethresear.ch/t/the-road-towards-a-distributed-encrypted-mempool-on-ethereum/21717#p-52835-in-protocol-solution-9) where the encryption mechanism can be generalized.

![](https://ethresear.ch/user_avatar/ethresear.ch/and882/48/19073_2.png)[The Road Towards a Distributed Encrypted Mempool on Ethereum](https://ethresear.ch/t/the-road-towards-a-distributed-encrypted-mempool-on-ethereum/21717/1)

> We also consider a more generalized approach that abstracts away the specific encryption mechanism. That is, the exact technology—whether threshold encryption, delay encryption, TEEs, or any other method—is not the focus as long as the chosen mechanism reliably outputs the decryption key in time to decrypt transactions. Essentially, we treat the encryption mechanism as a black box that accepts an input and produces the necessary decryption keys, allowing flexibility in implementation while maintaining the desired functionality.

Importantly, fork-choice enforcement as in Sealed transaction does away with the requirement:

![](https://ethresear.ch/user_avatar/ethresear.ch/and882/48/19073_2.png)[The Road Towards a Distributed Encrypted Mempool on Ethereum](https://ethresear.ch/t/the-road-towards-a-distributed-encrypted-mempool-on-ethereum/21717/1)

> as long as the chosen mechanism reliably outputs the decryption key in time to decrypt transactions.

With in-protocol oversight of unsealed txs, the protocol can afford to be more permissive, allowing users to manage decryption themselves. My reading of the shutterized beacon chain is that there is no such oversight, but happy to be corrected.

*In conclusion, in-protocol oversight of the decryption step seems like an important component of a fully generalized encrypted mempool, and the Sealed transactions mechanism can be leveraged to this end.*

#### Answers to other questions

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> My point here is that you need to include something which ties it to a specific block at the point you create the hashed commitment to prevent it being copied and used elsewhere. Since the block hash is not available when the commitment is created that is why I suggest using the slot number.

Given that the protocol does not permit a tx to be included several times, the sealed tx cannot be used after having being included. If the user needs to know beforehand in which slot the sealed tx will be included, UX is degraded or protocol complexity increases.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> If we’ve seen Block A and are waiting for the next block, there is no way to know what will be proposed in the next slot unless you are the builder / proposer (even they don’t know until all txs are unsealed) - there may be no block at all. Do you mean that we know that Block B will contain certain unsealed transactions?

Assuming no delay, the protocol will insist that any unsealed txs go into the next block, if the previous block contained the sealed tx. This is the point of the fork-choice enforcement illustrated in Figure 1 in the post, where attesters make observations at T_3 and enforce these observations at T_5.

---

**and882** (2025-03-10):

Thanks for the reply and the clarification, I completely agree with you! We’re indeed thinking in a very similar direction, where the protocol provides a generalized encrypted mempool interface, while the exact implementation remains out-of-protocol so as to leave the choice of the exact encryption/decryption mechanism up to the user.

---

**kladkogex** (2025-04-09):

We have a testnet for BITE protocol  now and it is going into our mainnet soon



      [twitter.com](https://twitter.com/Stan_Kladko/status/1878827892932841611)





####

[@Stan_Kladko](https://twitter.com/Stan_Kladko/status/1878827892932841611)

  My presentation slides from #buidleurope

Announcing SKALE new exciting direction for 2025 - BITE protocol

Hopefully video will follow up soon!

  https://twitter.com/Stan_Kladko/status/1878827892932841611










Our blockchain (as pretty much all modern blockchains) is forkeless, so we do not need the fork rule.

The user encrypts transaction fields CALLDATA and TO using BLS.

They are decrypted by consensus after the block is committed

It is compatible with Eth wallets like Metamask

