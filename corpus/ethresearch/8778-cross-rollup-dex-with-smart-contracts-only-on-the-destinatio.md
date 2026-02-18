---
source: ethresearch
topic_id: 8778
title: Cross-rollup DEX with smart contracts only on the destination side
author: vbuterin
date: "2021-02-28"
category: Layer 2
tags: []
url: https://ethresear.ch/t/cross-rollup-dex-with-smart-contracts-only-on-the-destination-side/8778
views: 34137
likes: 37
posts_count: 31
---

# Cross-rollup DEX with smart contracts only on the destination side

Suppose that we have two rollups, A and B, and Alice wishes to exchange some quantity of coins on rollup A for the same coins on rollup B. There are already [proposals](https://ethresear.ch/t/hop-send-tokens-across-rollups/8581) for how to do this in a decentralized way if A and B both have full smart contract support. This document proposes how to do it in the case where only rollup B has full smart contract support (and rollup A can only process simple transactions).

We assume that transactions on rollup A have some kind of “memo field”; if they do not, we can use lower-order digits of the value sent as a memo.

### Proposal

Suppose there is an exchange intermediary, Ivan (in a real implementation there would be many intermediaries to choose from). Ivan has an account `IVAN_A` on rollup A (that he fully controls). Ivan also has some funds deposited in a smart contract `IVAN_B` on rollup B.

The smart contract `IVAN_B` has the following rules:

- If anyone sends a transaction sending TRADE_VALUE coins to IVAN_A, containing an address DESTINATION as a memo, then after MIN_REDEMPTION_DELAY blocks they can send a transaction to IVAN_B containing a proof of the transfer, which queues a withdrawal of TRADE_VALUE coins to address DESTINATION.
- Withdrawals are processed after some delay (eg. 1 day) in order of the batch and index the transfers were included in on rollup A.
- When Ivan sees that he received funds at IVAN_A, he has the ability to personally send TRADE_VALUE * (1 - fee) coins to DESTINATION. He can do this by sending the transaction through a method in IVAN_B, which saves a record that prevents the automated-send clause in the contract from triggering for that trade.

The expected behavior is simple:

1. Alice sends a transaction to IVAN_A with N coins and a memo ALICE_B
2. Ivan sends a transaction sending TRADE_VALUE * (1 - fee) coins through IVAN_B to ALICE_B

The second step can happen immediately after the first step. The contract can even have rules that allow the `fee` to be greater if Ivan shows proof that the timestamp difference between the second transaction and the first is very low.

The “worst-case” behavior is if Ivan does *not* send coins to `ALICE_B` as he is expected to. In this case, Alice can wait until the transaction on rollup A confirms, find some alternate route to getting coins on rollup B to pay fees, and then simply claim the funds herself.

### Capital costs

The main limitation of the scheme is that `IVAN_B` needs to hold a large amount of capital to ensure that all senders will be paid. Particularly, suppose that:

- We place a trade size limit of TRADE_LIMIT coins (so transactions going to IVAN_A with value > TRADE_LIMIT are not valid trades)
- Each rollup batch can contain a maximum of TXS_PER_BATCH transactions

Alice can check herself how many unprocessed trades there are before the upcoming batch on rollup A, subtract this value from the capital she sees in the `IVAN_B` contract, and check if the remaining amount is enough. Because withdrawals are processed sequentially (this is the goal of the queue mechanism above), Alice need not concern herself with the possibility of future withdrawals being processed before her own.

The maximum amount that could be traded in one batch is `TRADE_LIMIT * TXS_PER_BATCH`, and so the `IVAN_B` contract needs to hold at least this amount of ETH, plus enough to cover unprocessed trades. As an example, suppose `TRADE_LIMIT = 0.1 ETH` (low limits are okay because a larger trade can be done with multiple transactions) and `TXS_PER_BATCH = 1000`. Then, `IVAN_B` would need to hold 100 ETH.

Note that there is an extra implicit fee in this design, because anyone trading more than 0.1 ETH would need to waste block space. This is traded off against capital requirements: if you halve the block waste, you double the capital requirements, and vice versa. It seems likely that the correct balance would be the point where the implicit fee is a few times smaller than the explicit fee that emerges in the market.

If we want to reduce or remove this waste, rollup A could be designed to do so, for example by having the sequencer send a signed message attesting to Alice all messages approved in the batch so far. Alice would then know that there are no trades before hers (though a malicious sequencer could, at high cost to themselves, trick Alice).

### Memos

The design above assumes that transactions on rollup A have a memo field that Alice can use to specify `ALICE_B` as her destination. If rollups do *not* have this feature, then we can use the following workaround. Alice can register `ALICE_B` on rollup B in a sequential registry contract, and get a sequentially assigned ID (so Alice’s ID equals the number of users who registered before her). Let `MAX_USER_COUNT` be a maximum on the user count; if necessary, this value could adjust upwards over time. Alice can simply ensure that `TRADE_VALUE % MAX_USER_COUNT` equals (Alice’s ID), using the low-order digits of `TRADE_VALUE`, which represent an inconsequential amount of value, to represent the amount she wants to trade.

### B to A trades

If Alice starts with coins on rollup B and moves them to rollup A, a similar mechanism can be used, except with reversed roles:

- Alice sends coins to IVAN_B
- After some delay, she gets the right to take the coins back
- She loses that right if Ivan can prove to IVAN_B that he sent Alice coins on rollup A

## Replies

**chris.whinfrey** (2021-03-01):

This is really cool!

> The “worst-case” behavior is if Ivan does  not  send coins to  ALICE_B  as he is expected to. In this case, Alice can wait until the transaction on rollup A confirms, find some alternate route to getting coins on rollup B to pay fees, and then simply claim the funds herself.

In this case, would Alice be required to make a layer-1 transaction to provide proof of the transfer and claim the funds on rollup B? Or is it possible to prove this on rollup B directly?

---

**vbuterin** (2021-03-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/chris.whinfrey/48/10236_2.png) chris.whinfrey:

> In this case, would Alice be required to make a layer-1 transaction to provide proof of the transfer and claim the funds on rollup B? Or is it possible to prove this on rollup B directly?

You could do it on rollup B directly. All you need is for rollup B to have access to block hashes of the L1 chain before the previous batch (this can be done safely). Then the transaction in rollup B can contain a Merkle branch (or a SNARK of a Merkle branch) going [L1 block hash → root of rollup A batch → transaction record in rollup A], and that branch can be verified inside the rollup.

---

**leohio** (2021-03-01):

Elegant specification, I think.

I have some questions.

1. How can Ivan withdraw his fund from the contract IVAN_B?
If he must do it by depositing to IVAN_A with the memo “IVAN_B2_ADDRESS”, the double amount of this coin is needed to exit. (And, while this is not so important, the last fee is always left in this account). We can’t do this easily because IVAN_B is overcollateralized basically and we need to add the same amount of fund of that collateral to withdraw it. Then I think Ivan needs to withdraw money from IVAN_B directly with a method of this smart contract.
2. When IVAN_A sends coins to IVAN_A with memo “IVAN_B2_ADDRESS”, he can claim all the funds in IVAN_B which ruins the over collateral security. Does IVAN_A need some restrictions other than TRADE_LIMIT? It seems that it’ll be more dangerous when Ivan is the  aggregator since he can insert his deposit transactions just before Alice. Is not DEPOSIT_LIMIT to IVAN_A needed?

By the way, I think this can be used for the exchange between different types of coins as well.

The IVAN_B contract address is used as an orderbook with a limited price which allows partial filling of exchanges. At the same time, the partial orderbook cancel action can be done with the withdrawal action in IVAN_B if implemented. Maybe IVAN_B can be implemented as an address which is a smart contract code applied, then not so much storage and memory will be used.

---

**chris.whinfrey** (2021-03-01):

> Then the transaction in rollup B can contain a Merkle branch (or a SNARK of a Merkle branch) going [L1 block hash → root of rollup A batch → transaction record in rollup A], and that branch can be verified inside the rollup.

This is fantastic! I didn’t realize this was possible.

I think it would make sense for us to integrate a concept like this or have it live in parallel to our current setup in order to support non-smart-contract layer-2s.

I believe it’s possible to use your concept to swap directly across two non-smart-contract rollups as long as the exchange intermediary has funds deposited in a third smart-contract-enabled rollup.

For example, rollup A and rollup B are not smart contract enabled and rollup C is smart contract enabled. Ivan has EOA accounts `IVAN_A` and `IVAN_B` and a smart contract with funds deposited, `IVAN_C`.

The expected behavior is similar to above:

1. Alice sends a transaction to  IVAN_A  with N coins and a memo  ALICE_B
2. Ivan sends TRADE_VALUE * (1 - fee)  coins from  IVAN_B  to  ALICE_B

In the case where Alice sends a transaction to Ivan on Rollup A and Ivan does nothing, Alice can prove she made the transaction in step 1 and start a withdrawal process for her funds from `IVAN_C` exactly like she does in the original example. *But* Ivan also has a chance to prove the swap was fulfilled on rollup B which would invalidate Alice’s withdraw from `IVAN_C`.

---

**vbuterin** (2021-03-01):

> When IVAN_A sends coins to IVAN_A with memo “IVAN_B2_ADDRESS”, he can claim all the funds in IVAN_B

Yes, he can, and I guess this could just *be* the withdrawal mechanism.

> which ruins the over collateral security.

How so? It can only lead to a valid withdrawal on the B side if it has `<= TRADE_LIMIT` coins per transaction, and so Ivan can only withdraw `TRADE_LIMIT * TXS_PER_BATCH` coins per block. Any transaction on the B side sending more than `TRADE_LIMIT` is, from the system’s point of view, just a donation to Ivan, and so not a security risk.

---

**leohio** (2021-03-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> When IVAN_A sends coins to IVAN_A with memo “IVAN_B2_ADDRESS”, he can claim all the funds in IVAN_B

Yes, he can, and I guess this could just *be* the withdrawal mechanism.

I see this is the withdraw mechanism. If so, there are no need to have the double fund, then it seems that there’s no problem.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> How so?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Any transaction on the B side sending more than TRADE_LIMIT is, from the system’s point of view, just a donation to Ivan, and so not a security risk.

TL;DR: If the withdraw mechanism above, Alice’s security is not automatically guaranteed, she should claim in rollupB in the period.

Only the case **the blocks of rollupA is filled with Ivan’s transaction from IVAN_A to IVAN_A and the blocks of rollupB is filled with Ivan’s exit transaction and Alice does not claim with IVAN_B** will be problem as far as I understand, because effective TRADE_LIMIT security will be zero where all funds can be withdrawed by Ivan before Alice withdraws.

If the relationships of  transactions or memo are strictly indexed and indexes are used for the TRADE_LIMIT, it can’t be security problem with the condition below, but Alice can deposit to IVAN_A just with memo and this will not be always queued since rollupB and rollupA are different system.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Ivan can only withdraw TRADE_LIMIT * TXS_PER_BATCH coins per block

---

**vbuterin** (2021-03-01):

> the blocks of rollupA is filled with Ivan’s transaction from IVAN_A to IVAN_A and the blocks of rollupB is filled with Ivan’s exit transaction and Alice does not claim with IVAN_B

Are you taking into account the fact that withdrawals are put into a queue and delayed for 1 day so that they can be processed in order of the transaction on rollup A that authorized them? This ensures that even if Ivan quickly makes many send-to-self transactions completely filling many batches on rollup A, if Alice makes a trade that comes before them she would be able to withdraw before Ivan can.

Oh also, if we want an easier withdrawal mechanism that doesn’t require spamming rollup A, we could also let Ivan initiate a withdrawal on rollup B, with a delay significantly longer than `MIN_REDEMPTION_DELAY` plus the withdrawal period.

---

**alonmuroch** (2021-03-01):

That’s very interesting, similar to how banks clear transactions between themselves.

Batching assets into separate “accounts” could have limitations, a solution could be just big pools on either ends and fees split pro rata.

---

**leohio** (2021-03-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Are you taking into account the fact that withdrawals are put into a queue and delayed for 1 day so that they can be processed in order of the transaction on rollup A that authorized them?

Yes. And, “withdrawals are put into a queue” is difficult in a strictly speaking because of the case that the withdrawal tx can not be rolluped and queued by the rollupB aggregator in one day. The spamming is only an example condition that this tx can not be rolluped and queued, and the most direct case is that the aggregator keeps ignoring tx for a day.

This is easily solved by banning tx from IVAN_A to IVAN_A and keeping the balance of IVAN_B higher than that of IVAN_A like you said here.

> Alice can check herself how many unprocessed trades there are before the upcoming batch on rollup A, subtract this value from the capital she sees in the  IVAN_B  contract, and check if the remaining amount is enough.

But the tx from IVAN_A to IVAN_A can ruin this condition IVAN_A < IVAN_B, then the censorship (or spamming) in rollupB can be an attack vector.

Or, we add a function on L1 to force the aggregator to include a withdrawal tx to the block, this also will be fine. But in this emergency security, Alice’s security is not guaranteed automatically, and do this action in the period. I think the tx from IVAN_A to IVAN_A should be banned.

---

**vbuterin** (2021-03-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png) leohio:

> And, “withdrawals are put into a queue” is difficult in a strictly speaking because of the case that the withdrawal tx can not be rolluped and queued by the rollupB aggregator in one day.

Right, so the withdrawal period would need to be extended to be long enough that it exceeds the maximum length of any possible failiures.

> The spamming is only an example condition that this tx can not be rolluped and queued

Meaning, if there are so many trades that because of the asymmetry where a Merkle branch is more expensive than a trade, `IVAN_B`’s queue starts getting longer and longer? I grant that such an attack could happen, but surely that would just lead to longer withdrawal delays, and not anyone’s safety guarantee being violated?

> the most direct case is that the aggregator keeps ignoring tx for a day.

The Optimism rollup has a scheme by which parties other than the sequencer can submit batches to chain and the sequencer is forced to include them, and my understanding of Arbitrum is less but I believe that they have also some “anyone can push transactions” mechanic.

> Or, we add a function on L1 to force the aggregator to include a withdrawal tx to the block, this also will be fine

Right, this is what Optimism already has, and my impression is Arbitrum already has as well.

> I think the tx from IVAN_A to IVAN_A should be banned.

I don’t think this would help anything, because `IVAN_A` is already assumed to be an EOA that Ivan can withdraw from at will, so Ivan could just do `IVAN_A` → `IVAN_A_2` → `IVAN_A` or any more complicated scheme. Only the coins held in `IVAN_B` are part of the security model.

Another thing is that if we want to improve user experience in the “unhappy case” further (not require Alice to wait a week if Ivan misbehaves), then we could, entirely on the `IVAN_B` side, add a mechanic by which Alice can sell her withdrawal slot to someone else. This could even be integrated with the “Ivan fast path” mechanic: after some delay (eg. this could even be 1 batch) not just Ivan but *anyone* could route a transaction through `IVAN_B` to pay Alice and take over ownership of the withdrawal slot.

---

**vbuterin** (2021-03-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/alonmuroch/48/4817_2.png) alonmuroch:

> a solution could be just big pools on either ends and fees split pro rata.

The challenge with pooling is that the pool would have to somehow own the funds on the rollup A side, and I’m avoiding the assumption that any ability to do anything other than direct single-key ownership on the rollup A side exists.

---

**leohio** (2021-03-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I don’t think this would help anything […] so Ivan could just do IVAN_A → IVAN_A_2 → IVAN_A or any more complicated scheme.

This is totally right. We cannot ban its equivalents.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Right, so the withdrawal period would need to be extended to be long enough that it exceeds the maximum length of any possible failiures.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I believe that they have also some “anyone can push transactions” mechanic.

Finally, I understood the meaning of your specification.

---

**jliphard** (2021-03-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Suppose that we have two rollups, A and B, and Alice wishes to exchange some quantity of coins on rollup A for the same coins on rollup B

Your proposal is much more general, right, in the sense that it not only addresses the difficulties that rollups A and B might have, but *any* L2 (with metadata support or steganography in the low order value bits) with *any* other L2 (with smart contract support), and *any* L2 with mainchain? Basically, it’s a general purpose high speed off ramp from ‘basic’ L2’s to anything with smart contract support. Nice!

---

**vbuterin** (2021-03-04):

Right, I guess that’s true! The only requirements are that (i) it must eventually be possible to create a proof of payment from the source L2 to the destination L2, and (ii) there must be a bound on how many transactions can take place in the source L2 within a particular span of time.

---

**shenyangaoti** (2021-03-05):

Write very good, very good

---

**Norfolks** (2021-03-05):

Right, it could be a protection from Atomic swap fee&lock attack.

Alice and Ivan could make an agreement of an Atomic swap exchange on some `chainC` with available smart-contracts.

Then Alice starts a swap with `coinA`, and if Ivan does not send an appropriative transaction with `coinB`, Alice can make the punishment on `chainC`.

---

**Norfolks** (2021-03-05):

There shouldn’t be even a transaction on `chainC`.

Alice and Ivan can just store signed agreement, and only if one of them cheats, another party can reveal an agreement to smart-contract on `chainC`.

---

**breeze0502** (2021-03-06):

yes，but will the payment proof be difficult，since it‘s depended on merkle or SNARK.just like we know that zk rollup solution is possible, but it’s not easy. I doubt if we can have a general solution for the payment proof either.

And btw, if the payment proof can be solved, can the Ivan B account be set to transfer the fund to Alice B automatically after Ivan is proved to have do evil.

> then we could, entirely on the  IVAN_B  side, add a mechanic by which Alice can sell her withdrawal slot to someone else. This could even be integrated with the “Ivan fast path” mechanic: after some delay (eg. this could even be 1batch) not just Ivan but  anyone could route a transaction through  IVAN_B  to pay Alice and take over ownership of the withdrawal slot.

For this part, related scenarios can involve incentive mechanisms, like the yield farming thing.

---

**praneethmendu** (2021-03-25):

Hey guys, I want to work on this, but proving transactions that happened on one chain on another does not seem obvious to me, maybe you can point me to some resources to help me out ?

---

**TimDaub** (2021-07-08):

Yoda:

> I know that we are talking about layer 2, but we have solved a similar issue for a new cross-chain swap between BTC<>ETH. that solution will be open soon for free on our https://smartswap.exchange/ .

Hey I’ve tried checking out your GitHub in search for a technical document but your page has

[![Screen Shot 2021-07-08 at 21.26.28](https://ethresear.ch/uploads/default/optimized/2X/e/e02b4b51932bf42aac89286e54644086ab9810a2_2_690x184.png)Screen Shot 2021-07-08 at 21.26.28914×244 52.6 KB](https://ethresear.ch/uploads/default/e02b4b51932bf42aac89286e54644086ab9810a2)

for most links. I couldn’t find anything useful on Google either. Your GH profile doesn’t point to an org: https://github.com/Juderegev

I’m not into making baseless claims but maybe a mod should look into that comment?


*(10 more replies not shown)*
