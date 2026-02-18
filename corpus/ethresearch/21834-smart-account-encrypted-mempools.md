---
source: ethresearch
topic_id: 21834
title: Smart Account Encrypted Mempools
author: Marchhill
date: "2025-02-26"
category: Uncategorized
tags: [mev, censorship-resistance]
url: https://ethresear.ch/t/smart-account-encrypted-mempools/21834
views: 2119
likes: 3
posts_count: 10
---

# Smart Account Encrypted Mempools

# Smart Account Encrypted Mempools

*Written by [Marc Harvey-Hill](https://x.com/marchhill1) @ [Nethermind](https://www.nethermind.io/). Special thanks for feedback from [Ahmad Bitar](https://x.com/Smartprogrammer), [Aikaterini-Panagiota Stouka](https://x.com/AikPStouka), [Stefano De Angelis](https://x.com/_deanstef), [Conor McMenamin](https://x.com/ConorMcMenamin9), [Lin Oshitani](https://x.com/linoscope), and [Julie Bettens](https://x.com/0xbbjubjub). Feedback is not necessarily an endorsement.*

This post explores the concept of using smart accounts to validate that encrypted mempool rules are followed. This can strengthen guarantees of frontrunning protection and censorship resistance for cases where block proposers attempt to violate the encrypted mempool rules.

In an encrypted mempool users send encrypted transactions that are posted onchain in a public constraint. This is a constraint on the next proposer to include these transactions in a predefined order (such as ordered by priority fee). Just before the next slot the decryption keys are revealed so that the proposer can decrypt and include the transactions from the public constraint. They *should* include *all* of the valid transactions that were in the constraint at the top of their block in a predetermined order, inserting no transactions beforehand that could frontrun the decrypted transactions. We are concerned with enforcing that proposers follow these rules.

Smart accounts can be used to prevent frontrunning by a malicious proposer. Rather than encrypting normal transactions, users can instead encrypt [ERC-4337](https://eips.ethereum.org/EIPS/eip-4337) smart account transactions (UserOps) that carry out a check that they have been included in the correct order at the correct index within the block (i.e. at the top). If the check fails then the main body of the UserOp (e.g. the swap) will not run, so it is impossible for them to be frontrun.

They can also provide protection if the proposer is not malicious, but goes offline. In these cases the decryption keys will still be revealed, so now everyone can see the decrypted transactions. This means that the next proposer could include these decrypted transactions and insert their own frontrunning transactions beforehand. Again smart accounts can provide protection; as part of the checks performed at the start of the UserOp we can verify that the UserOp is being executed in the slot that it was intended for. If the check fails then the body of the UserOp will not run, so the attack is no longer possible.

In order to have their key properties, frontrunning protection and censorship resistance, encrypted mempools should enforce two rules respectively: ordering and inclusion. As stated smart accounts can be used to enforce ordering, meaning that transactions must be executed in the correct slot, in the correct order, at the correct index within the block (top of block). We will also explore how inclusion can be enforced through a fraud proof game, meaning that if the proposer does not include transactions that were in the public constraint they will lose out on rewards, and potentially be slashed.

Smart account encrypted mempools have several benefits:

- Unconditional frontrunning protection: A proposer cannot frontrun transactions under any circumstance. Even if they are offline and the decrypted transactions are leaked, a future proposer cannot include and frontrun them as the main body of the transaction will not execute in future slots.
- Reorg safety: In the event of a reorg it is still not possible to frontrun.
- Incentive alignment: Proposers miss out on all tips if they censor any encrypted mempool transaction.

## Background

For background I would recommend [this 5 minute talk](https://www.youtube.com/watch?v=mUoWwRoHrvk) I gave outlining the design space of encrypted mempools.

To summarise:

- Users encrypt their transactions.
- The encrypted transactions are posted onchain in a public constraint. The proposer for the next slot should include all of these transactions in a predefined order at the top of their block.
- Just before the start of the next slot, the decryption keys are revealed by ‘keypers’.
- If the proposer is online they build their block. Smart accounts and a fraud proof game can be used to enforce that the proposer follows the rules, respecting the public constraint.

This design focuses on point 4: how to enforce that all transactions from the constraint are included in the correct order. We will explore a smart account approach that mitigates the problem of malicious and offline proposers by enforcing ordering and inclusion rules.

There are other important aspects of the design such as the encryption mechanism, the nature of the keypers, where exactly the public constraint is posted; I will not cover these in this post.

## Encrypted Mempool Taxonomy

We can classify encrypted mempool designs by how strongly they enforce the ordering and inclusion rules on proposers.

### Stage 0 - Trusted

- Fully trusted proposer.
- Ordering and inclusion not enforced, so able to frontrun and censor without consequence.

### Stage 1 - Staking

- Proposer has stake that can be slashed. They could issue proposer commitments.
- If proposer reorders or censors their stake can be slashed. Requires posting proof of proposer breaking rules.
- Ordering only enforced retroactively so still possible to frontrun. Could happen if payoff exceeds stake.
- Instead of slashing, the stake could be used to compensate users.
- Problem: must slash offline proposer who allows decrypted transactions to be leaked, even if they didn’t receive the keys in time.
- Stage 1 mempools are explored in this whitepaper. It uses slashing and proposer commitments.

### Stage 2 - Smart Account

- Ordering enforced by smart account.
- Proposer proves correct ordering onchain before executing.
- Impossible to frontrun, UserOp body will not execute if the ordering is incorrect.
- Proposer loses all encrypted mempool rewards if inclusion is not satisfied. Could also be slashed as in stage 1.

### Stage 3 - Enshrined

- Enforced by block validity conditions.
- Proposer cannot build a valid block if ordering and inclusion are not satisfied; this means they would miss out on block rewards.
- Would have to be enshrined in-protocol through a hard fork.
- Will take longer to coordinate on a design suitable for enshrinement.

Stage 2 has the benefit over stage 1 of unconditional frontrunning protection. With stage 1 frontrunning is still possible as it is only punished after the fact; it could happen if the value gained exceeds the losses from slashing. It could also happen in the case that a proposer simply goes offline and the decrypted transactions from their slot are leaked. With stage 1 the proposer may be slashed for this (which could be unfair if they did not receive the decryption keys in time), whereas with stage 2 this is not a problem as the leaked transactions could not be executed outside of their intended slot.

Ultimately stage 3 will provide the strongest security guarantees in the long term, but realistically it will take a long time to reach consensus on a design suitable to be enshrined in-protocol. For the short to medium term stage 2 should give sufficient protection.

The various enforcement mechanisms of different stages of encrypted mempools are summarised in the following table:

| Stage | Ordering | Inclusion |
| --- | --- | --- |
| 0 | None | None |
| 1 | Slashing | Slashing |
| 2 | Smart account | Slashing |
| 3 | Consensus | Consensus |

Note that the stage of an encrypted mempool is not the only factor in how secure it is, this also depends on other aspects such as the keyper mechanism.

## Design

I will present a design that enforces ordering and inclusion rules on proposers using smart accounts and a fraud proof game. We will start with a high level overview of how this works before exploring the details:

- Users create and encrypt UserOps. These UserOps specify in which slot they should be executed (i.e. the next slot).
- Encrypted UserOps are included onchain in a public constraint.
- At the start of the next slot the decryption keys are broadcasted and the proposer decrypts the UserOps for their slot. They begin building their block (they may use MEV-boost, this is discussed in the PBS section).
- The proposer creates an “ordering declaration”. This declaration is the proposer claiming which transactions were in the public constraint and how they should be ordered according to the rules of the mempool. They can also claim that certain decrypted UserOps were invalid and not include them.
- The proposer bundles together all of the (valid) decrypted UserOps together into a single ERC-4337 transaction. The ordering declaration should be passed into this transaction as calldata.
- The proposer should include this bundled transaction at the top of their block.
- The validation checks are carried out onchain as part of this bundled transaction. The ordering declaration can be verified to satisfy the public constraint, and then each UserOp can then be verified to follow the ordering declaration.
- If the checks pass the UserOp bodies will be executed, otherwise they stop after the check is performed and the main body will not be executed.
- The proposer could have falsely claimed that certain valid transactions were invalid; this is where the fraud proof game is used. The transaction tips are locked up for some challenge period in which anyone can provide proof that the proposer lied about a certain transaction being invalid. The proposer would then be unable to collect their rewards and could be slashed.

The flow is illustrated in this figure:

[![overview](https://ethresear.ch/uploads/default/optimized/3X/7/9/79b061a2ab4c3a102be2ccf2818fdaaa94b1d8fa_2_690x319.png)overview3366×1560 267 KB](https://ethresear.ch/uploads/default/79b061a2ab4c3a102be2ccf2818fdaaa94b1d8fa)

We will now step through an example to see this design working in practice, before exploring the different parts of the process in more detail.

### Example

Three users have UserOps that they want to execute through the encrypted mempool. These UserOps have the hashes 0xa, 0xb, 0xc. The users encrypt their UserOps and send them to the encrypted mempool.

[![Constraint](https://ethresear.ch/uploads/default/optimized/3X/b/8/b8dff00e0ff6d2f1d6c288f5f7c185f7eb14923b_2_179x250.png)Constraint690×960 23.5 KB](https://ethresear.ch/uploads/default/b8dff00e0ff6d2f1d6c288f5f7c185f7eb14923b)

The encrypted UserOps are included in a public constraint posted onchain in blobs or calldata. Alongside the ciphertext the hashes of the underlying UserOps are revealed, as well as a proof that these hashes are of the plaintext UserOps.

Before the start of the next slot the keypers reveal the decryption keys for the UserOps; the proposer must now construct an ordering declaration.

[![Declaration](https://ethresear.ch/uploads/default/optimized/3X/2/8/28285b2df3eb102d5cda368ab6a10dcf1bd96793_2_203x250.png)Declaration780×957 26 KB](https://ethresear.ch/uploads/default/28285b2df3eb102d5cda368ab6a10dcf1bd96793)

In this example the encrypted mempool does ordering by priority fee. The proposer provides a proof of the priority fee for each UserOp and orders them accordingly. The proposer also declares that the UserOp with hash 0xa was invalid against the prestate. The proposer must now construct their block.

[![Block](https://ethresear.ch/uploads/default/optimized/3X/f/b/fba240c508898bc6c9f567730ba0681bf4a41d17_2_257x375.png)Block966×1407 26.1 KB](https://ethresear.ch/uploads/default/fba240c508898bc6c9f567730ba0681bf4a41d17)

The proposer has bundled the valid UserOps into a single transaction which they included at the top of the block. Within this transaction the ordering declaration is first verified. Next the valid UserOps 0xb and 0xc are executed in the correct order. For each of these the validation checks are first carried out before the main body is executed.

Since the proposer declared that UserOp with hash 0xa was invalid they did not include it. However, now anyone can submit a proof that 0xa was actually valid and claim the proposer tips for this slot.

### Ordering Declaration

Once the UserOps are decrypted, the proposer must first post an “ordering declaration” in calldata. This is a list of UserOp hashes that the proposer is declaring to be the correct ordering. Once this list has been proven to be correct against the public constraint, it can then be used by each UserOp to check that it has been included in the correct order.

The ordering declaration should:

(1) Respect the ordering rules of the mempool eg. ordering by priority fee or FCFS.

(2) Not contain any UserOps that were not present in the original constraint.

(3) Declare which UserOps from the constraint were invalid against the prestate.

We can verify (2) immediately by comparing the declaration to the public constraint which was posted in blobs or calldata; the proposer can prove the contents of the constraint against the blob KZG commitment. The public constraint should expose the hashes of the UserOps (users can prove the hash when they submit); these hashes can then be compared to the ordering declaration to ensure there are no hashes present that were not included in the original constraint.

We can also verify (1) immediately by comparing the ordering declaration to the hash list from the public constraint. In the case of FCFS the lists should be identical. With priority fee ordering the proposer must provide an additional proof of the priority fee for each UserOp.

The declaration (3) allows the proposer to claim that some UserOps were not valid so do not need to be included. It would be very expensive to prove this upfront so it can instead be verified afterwards in a fraud proof game. We will expand further on this in the [inclusion section](#inclusion).

Once (1) and (2) have been proven onchain the ordering declaration can now be used in the UserOp ordering checks.

### Ordering

Before the body of a UserOp is executed, checks must be carried out to verify that:

- The UserOp is being executed in the correct place, matching the ordering declaration.
- The current slot matches the one included in the UserOp. This can be checked with the SLOT precompile.
- The bundled transaction is executed at the top of block. This can be checked with the TXINDEX precompile.
- No previous UserOp failed the validation check.

Only once these things have been verified will the main body of the UserOp be executed. If any checks fail then the UserOp body, and those of subsequent UserOps, cannot be executed; the proposer will be unable to claim any rewards and they may be slashed.

### Inclusion

A fraud proof game is used to verify that the proposer did not censor any transactions from the public constraint that were valid. Proposer tips are accumulated in a smart contract and held for some challenge period. During this period anyone can submit a zk proof that a UserOp that the proposer declared to be invalid was indeed valid against the prestate, and there was enough gas left to include it. Anyone who submits this proof can claim the proposer tips from that slot, and the proposer could also be slashed. Some percentage of the rewards could be burned to disincentive the proposer from submitting the fraud proof themselves (if there is no slashing). If no challenge is submitted within the challenge period then the proposer is able to claim all of the tips.

An alternative design could enforce that the proposer provides proof of invalid transactions upfront. Since generating these proofs would be expensive this could lead to griefing attacks against the proposer, so I propose the fraud proof game instead.

## Considerations

### Dependencies

This proposal depends on [EIP-7793](https://github.com/ethereum/EIPs/pull/8981), the TXINDEX precompile; no other consensus level changes are required. It is necessary to have the transaction index in order to check that the bundled transaction is executed at the top of block.

[EIP-7843](https://github.com/ethereum/EIPs/pull/9141), the SLOT precompile, is a soft dependency. With this precompile we can verify that the current slot matches the one specified in the UserOp. It is not a strict dependency as the UserOp could instead contain a timestamp which is checked against the TIMESTAMP opcode. This approach works but is less future-proof as it would need to be updated in the event of a change to the slot length.

[ERC-6900](https://eips.ethereum.org/EIPS/eip-6900) modular smart accounts may be preferable to standard ERC-4337 accounts. These support the implementation of pre-execution hooks that can be used to run the checks before the main UserOp body is executed.

### Reorg Safety

For reorg safety, the decrypted UserOps must be executed in the slot directly after the one in which the public constraint is posted. To understand this, consider what could happen if we post a constraint onchain in slot x, and include the decrypted UserOps in slot x+2. An attacker could wait until the UserOps are decrypted in slot x+2, and then reorg the chain to include a block at slot x+1 containing frontrunning transactions.

This requirement could be removed once single slot finality is implemented.

### Leaking Intentions

Imagine a user is making a large swap from token X to Y through the encrypted mempool. The proposer for the slot is offline so the decrypted UserOp is revealed to everyone. As discussed the swap cannot be included in a future slot where it can be frontrun, as the body of the UserOp will not execute in future slots. However, the users intention to make the swap has been leaked, so someone else could buy up token Y in anticipation of the user resubmitting their swap, effectively frontrunning the user.

It is not clear that this attack could reliably be carried out. It could be the case that the transaction was leaked intentionally in an attempt to manipulate the market and increase the price of token Y, for example.

In some cases this could be a bigger problem, for example if the encrypted mempool was used to submit a transaction to register an ENS name. Although the transaction could not technically be frontrun, leaking the intention to register the name may not be an acceptable risk.

### Hashes or Commitments

For simplicity, I suggested that the public constraint should reveal the hashes of the plaintext UserOps so that they can be compared onchain with the ordering declaration. This approach would undermine the security of the encryption mechanism, since the hash is deterministic this would make the encryption scheme insecure against a chosen plaintext attack.

Instead of a hash, we could use a commitment that will not leak information about the plaintext. It may be possible to use techniques from [Lee et al., 2019](https://eprint.iacr.org/2019/1270) and [Campanelli et al., 2019](https://eprint.iacr.org/2019/142) that combine encryption schemes with commitments.

### EOA Support

With [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702) the same functionality can be brought to EOAs by deploying [ERC-6900](https://eips.ethereum.org/EIPS/eip-6900) code to their address.

### Proposer Builder Separation

So far we have assumed that the proposer will be building the block locally, but the design can still work with [MEV-boost](https://boost.flashbots.net/) or [ePBS](https://eips.ethereum.org/EIPS/eip-7732). The proposer can construct the bundled transaction as usual and request that the builder includes at the top of the block through the [constraints API](https://github.com/eth-fabric/constraints-specs).

## Conclusion

I have outlined a design for a maximally trustless enforcement mechanism for encrypted mempools that requires minimal consensus-level changes. This provides strong guarantees against frontrunning and censorship. Future posts will explore in more detail other parts of the design such as the public constraint.

## Replies

**Marchhill** (2025-03-03):

*Update:* The original design can be improved by not invalidating the UserOp body in future slots when there have only been missed slots with no execution payload. This improves the UX as users would not have to resubmit their transactions if the proposer that should have included their decrypted transactions was offline. They would also avoid leaking their intentions in this case.

Recall that a UserOp includes a slot `s`, and it will carry a check such that the body will only run in slot `s`. We can relax this rule by letting the check pass if there was no execution payload in slot `s`, and any empty slots following it. This is safe to do as if there were no payloads in between then no frontrunning transactions could have executed.

With the change the slot check for a UserOp would happen as follows:

- Check if slot = s. The check passes in this case.
- Otherwise the proposer can prove that the previous execution payload is from slot s-1, so all slots from s up to now have been empty.
- This can be done by proving the header of the previous block against the parent hash (retrieved with BLOCKHASH), which includes the timestamp (or slot with EIP-7843).
- Alternatively a new precompile could be introduced to get the slot number of the parent block to optimise gas usage.

---

**zincoshine** (2025-03-04):

I am a bit confused with this proposal.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> Users create and encrypt UserOps. These UserOps specify in which slot they should be executed (i.e. the next slot).

UserOps are simulated for validity and then “bundled” & relayed on-chain by specialised softwares called “bundlers” and these bundlers do not have any control over slot selection. They usually ought to work with builders to ensure inclusion within the next slot.  Shouldn’t the decryption then happen in the UserOp mempool rather than transaction mempool? Otherwise simulations would fail.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> At the start of the next slot the decryption keys are broadcasted and the proposer decrypts the UserOps for their slot. They begin building their block (they may use MEV-boost, this is discussed in the PBS section).

This presumes decryption keys are broadcast in ONLY in the consensus layer, however these keys are needed for the bundlers to simulate the UserOp before inclusion.

If the proposed design has to be implemented there will be a need to change serveral rules in ERC7562.

I would request [@yoavw](/u/yoavw) and [@drortirosh](/u/drortirosh) to chime in here.

---

**Marchhill** (2025-03-05):

What I am proposing is not that UserOps should go through the normal 4337 inclusion flow, instead the inclusion flow would be:

- Users post encrypted UserOps onchain in a public constraint
- Decryption keys are revealed to everyone. They may be released through threshold crypto or delay encryption, this design is agnostic. They are broadcast over p2p to ELs and the decrypted UserOps can be considered public knowledge at this point.
- The proposer themselves acts as a 4337 bundler for the decrypted UserOps, bundling them all into one transaction. As far as I know there is nothing specialist about this role that means the proposer could not act as a bundler. If there is then perhaps this could still be delegated.
- The proposer includes the bundled transaction at the top of their block. With PBS the constraints API can be used to enforce the builder to include at top of block.

I am not an expert in 4337 so would be great to get feedback from anyone knowledgeable about this EIP.

---

**drortirosh** (2025-03-20):

The TL;DR, is that ERC-4337, as an ERC, can’t support this mechanism of “encrypted mempools”. You *could* use it to encrypt the entire transaction (that is, a complete erc-4337 bundle - which may include one or more UserOps)

In ERC4337, we tried very hard to prevent DoS attacks on the mempool. Thus could happen if someone could inject UserOperations into the mempool which are known to fail validation.

A naive example is a UserOp with validation code `require(block.number & 1 == 0)`. This transaction passes validation on even block, but will certainly fail when included in the next block. So a malicious party could create a lot of these, to spam the mempool.

ERC-7562 validation rules come to prevent such cases, by blocking opcodes (and precompile) that use more than just memory and stack.

Adding a precompile and letting a UserOp to know something on-chain that might differ from its off-chain simulated validation is exactly what can open such attacks on the mempool.

I think that censorship-resistant and MEV-prevention is something that still requires native support, and are hard to add to ERC-based protocols, such as ERC-4337.

---

**Marchhill** (2025-03-21):

Thanks for your feedback.

To be clear, the check (eg. the current slot & TXINDEX) would not be carried out in the `validateUserOp` function but in the account code. So technically the UserOp can still be executed in an incorrect slot, for example. However the *body* of the UserOp cannot execute.

As an example, a user sends an encrypted UserOp carrying out a swap, specifying that it is only valid in slot x. In slot x+k someone attempts to include the UserOp; they are able to do this as it is still a valid fee-paying UserOp that passes the validation phase, but the swap (the ‘body’) will not be carried out as it is wrapped in a check `if (slot == x) then executeSwap()`.

Do you think this makes sense or would this be prevented by the DoS protection mechanisms?

---

**yoavw** (2025-05-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> Do you think this makes sense or would this be prevented by the DoS protection mechanisms?

Yes, if the checks happen in execution rather than validation, then it doesn’t conflict with DoS protection.  The gas is already paid so TXINDEX can be accessed and it can revert execution (on-chain).  The account pays for that revert, but I guess slashing is meant to deter this.

There’s still the issue of preventing mempool spam, regardless of TXINDEX.  If you encrypt the UserOp, how do nodes know that it is valid and not just taking up space?  You could solve this by encrypting only `UserOp.callData` and decrypting it onchain in the account itself.  The mempool would still be able to validate the transaction and determine that it’s not spam and doesn’t break the DoS protection rules, but won’t be able to see what’s going to happen in execution.  During inclusion you reveal the key and the account uses it to decrypt callData and execute it.  If the UserOp gets included without the key, it reverts and you can slash whoever caused this.  There are some issues to consider with this model but maybe they could be solved.

---

**Marchhill** (2025-05-16):

Specifically the timestamp / slot check could happen in a pre-execution hook through a smart account. The ordering and ASSERTTXINDEX checks would happen in a modified ERC-4337 EntryPoint contract.

I don’t actually see mempool spam as a big problem here, the ordering constraint should be onchain so you still have to pay the calldata or blob fee. You could also have a zk-proof that the UserOp is statically valid, but generally it could always be invalidated as it is being executed with one slot of latency - the account could be drained in the previous slot. If you only encrypted the calldata you could leak a lot of information that could be used for frontrunning.

---

**yoavw** (2025-05-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> Specifically the timestamp / slot check could happen in a pre-execution hook through a smart account. The ordering and ASSERTTXINDEX checks would happen in a modified ERC-4337 EntryPoint contract.

I would advise against modifying EntryPoint in any way.  This contract is a singleton for a reason.  It is the protocol, and with EIP-7701 (native AA) it’ll be implemented as part of the protocol. Using a modified EntryPoint will prevent you from getting the benefits of EIP-7701.

The checks should happen inside the account and using an aggregator if needed.  Asserting order can be done by using a 4337 aggregator, since an aggregator contract can see and approve a set of UserOps.  The account would perform its own validation and then instead of returning success it’ll return the address of the aggregator to require its approval as well.  The aggregator gets called exactly once, with all the UserOps it needs to approve in the current bundle.  The account can give it a hint about the order it expects, and it’ll revert the bundle if the requirement is not met.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> I don’t actually see mempool spam as a big problem here, the ordering constraint should be onchain so you still have to pay the calldata or blob fee.

How do you determine that the user should pay this, without validating the UserOp?  If the user hasn’t authorized the UserOp they shouldn’t pay for it.

![](https://ethresear.ch/user_avatar/ethresear.ch/marchhill/48/22206_2.png) Marchhill:

> You could also have a zk-proof that the UserOp is statically

It’s not sufficient that the UserOp is valid.  You need it to prove that it hasn’t violated the ERC-7562 rules during its validation. Otherwise you might face a large number of UserOps with validation that does something like `require(block.timestamp < nextBlockTimestamp)` or any other form of mass invalidation, and you won’t be able to charge the user.

---

**Marchhill** (2025-05-28):

Yes I think these checks can happen in the aggregator contract instead of the EntryPoint. This requires a [change](https://github.com/ethereum/EIPs/pull/9831) to EIP-7793 to make it more flexible, allowing you to check the transaction index anywhere and not just at the start of the contract (i.e. in the EntryPoint).

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> How do you determine that the user should pay this, without validating the UserOp? If the user hasn’t authorized the UserOp they shouldn’t pay for it.

Someone has to pay DA cost to submit the encrypted UserOp onchain, most likely the user themselves. Once it’s decrypted the bundler can validate the UserOps and only include the valid ones. If the bundler omits (censors) a valid UserOp then this can be proved onchain, and they can be slashed out-of-protocol (as described [here](https://ethresear.ch/t/smart-account-encrypted-mempools/21834#p-53079-inclusion-12)).

