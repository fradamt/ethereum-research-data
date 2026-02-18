---
source: ethresearch
topic_id: 426
title: Minimal Viable Plasma
author: vbuterin
date: "2018-01-03"
category: Layer 2 > Plasma
tags: [new-extension]
url: https://ethresear.ch/t/minimal-viable-plasma/426
views: 139151
likes: 288
posts_count: 144
---

# Minimal Viable Plasma

*Special thanks to Joseph Poon and David Knott for discussions that led to this specification.*

The following aims to provide a specification for a “minimal viable plasma implementation”. It aims to provide the basic security properties of Plasma in a very simplified way, though it leans heavily on users being willing to immediately exit as soon as they detect any kind of malfeasance.

#### The Plasma Contract

The Plasma contract maintains the following data structures:

- The owner (set at initialization time)
- A list of Plasma blocks, for each block storing (i) the Merkle root, (ii) the time the Merkle root was submitted.
- A list of submitted exit transactions, storing (i) the submitter address, and (ii) the UTXO position (Plasma block number, txindex, outindex). This must be stored in a data structure that allows transactions to be popped from the set in order of priority.

A Plasma block can be created in one of two ways. First, the operator of the Plasma chain can create blocks. Second, anyone can deposit any quantity of ETH into the chain, and when they do so the contract adds to the chain a block that contains exactly one transaction, creating a new UTXO with denomination equal to the amount that they deposit.

The contract has the following functions:

- submitBlock(bytes32 root): submits a block, which is basically just the Merkle root of the transactions in the block
- deposit(): generates a block that contains only one transaction, generating a new UTXO into existence with denomination equal to the msg.value deposited
- startExit(uint256 plasmaBlockNum, uint256 txindex, uint256 oindex, bytes tx, bytes proof, bytes confirmSig): starts an exit procedure for a given UTXO. Requires as input (i) the Plasma block number and tx index in which the UTXO was created, (ii) the output index, (iii) the transaction containing that UTXO, (iv) a Merkle proof of the transaction, and (v) a confirm signature from each of the previous owners of the now-spent outputs that were used to create the UTXO.
- challengeExit(uint256 exitId, uint256 plasmaBlockNum, uint256 txindex, uint256 oindex, bytes tx, bytes proof, bytes confirmSig): challenges an exit attempt in process, by providing a proof that the TXO was spent, the spend was included in a block, and the owner made a confirm signature.

`startExit` must arrange exits into a priority queue structure, where priority is normally the tuple (blknum, txindex, oindex) (alternatively, blknum * 1000000000 + txindex * 10000 + oindex). However, if when calling exit, the block that the UTXO was created in is more than 7 days old, then the blknum of the oldest Plasma block that is less than 7 days old is used instead. There is a passive loop that finalizes exits that are more than 14 days old, always processing exits in order of priority (earlier to later).

This mechanism ensures that ordinarily, exits from earlier UTXOs are processed before exits from older UTXOs, and particularly, if an attacker makes a invalid block containing bad UTXOs, the holders of all earlier UTXOs will be able to exit before the attacker. The 7 day minimum ensures that even for very old UTXOs, there is ample time to challenge them.

### The Plasma Chain

Each Merkle root should be a root of a tree with depth-16 leaves, where each leaf is a transaction. A transaction is an RLP-encoded object of the form:

```auto
[blknum1, txindex1, oindex1, sig1, # Input 1
 blknum2, txindex2, oindex2, sig2, # Input 2
 newowner1, denom1,                # Output 1
 newowner2, denom2,                # Output 2
 fee]
```

Each transaction has 2 inputs and 2 outputs, and the sum of the denominations of the outputs plus the fee must equal the sum of the denominations of the inputs. The signatures must be signatures of all the other fields in the transaction, with the private key corresponding to the owner of that particular output. A deposit block has all input fields, and the fields for the second output, zeroed out. To make a transaction that spends only one UTXO, a user can zero out all fields for the second input.

### User Behavior

The process for sending a Plasma coin to someone else is as follows:

1. Ask them for their address.
2. Send a transaction that sends some of your UTXOs to their address.
3. Wait for it to get confirmed in a block.
4. Send them a confirm message, signed with the keys that you use for each of your UTXO inputs.

### Emergency exiting

A user should continually validate (or validate at least once per 7 days) that the Plasma chain is fully available and valid; if it is not, they should exit immediately.

### Proof of correctness sketch

Approximate claim: a UTXO with denomination D will entitle its owner to withdraw D coins, and that (i) fraudulent cancellations and (ii) invalid UTXOs successfully withdrawing and draining the contract before the user can fully withdraw will not prevent them from doing so.

Suppose that:

- The first invalid or unavailable transaction is at position (blknum_i, txindex_i).
- There exist TXOs before that point of total denomination M, of which M-N is spent and N is unspent. We call a TXO spent if a transaction spending it has been included in a block, and a commit from the owner of the TXO is in the hands of the owner of at least one of the child TXOs.

Consider any UTXO with denomination D that was confirmed in a position before (blknum_i, txindex_i), call it (blknum_e, txindex_e). We assume that within 1 day of the first invalid or unavailable transaction getting confirmed, the owner of that UTXO publishes an exit. This exit is assigned a priority of (blknum_e, txindex_e), and so it will be processed before (blknum_i, txindex_i). We also assume that if there is a transaction “in flight” spending this UTXO, and this gets included in a future block, then the owner will refuse to sign the commit. We know that:

- By the validity assumption, there are >=N coins deposited in the contract.
- There are no UTXOs with commits spending that UTXO, so a challenge is not possible.
- All TXOs chronologically before (blknum_e, txindex_e) are valid. We ignore TXOs chronologically after (blknum_e, txindex_e) because they have no ability to influence the given UTXO’s ability to exit successfully (TXOs before it can, by draining the balance first)
- TXOs chronologically before (blknum_e, txindex_e) are of two types: (i) unspent, with total denomination N-D, (ii) spent, with total denomination M-N. Exits of the second type can be challenged, and exits of the first type will succeed.

Hence, there will be at least D coins left in the contract’s deposit to pay the owner of the deposit.

The following aims to provide a specification for a “minimal viable plasma implementation”. It aims to provide the basic security properties of Plasma in a very simplified way, though it leans heavily on users being willing to immediately exit as soon as they detect any kind of malfeasance.

## Replies

**jdkanani** (2018-01-09):

Thanks for the post.

Slightly more difficult scenario, how I can enforce correctness in case of state change in account/state based plasma chain?

```
(block 0, state 0, [t1, t2.... ]) -> state 1
(block 1, state 1, [t1, t2.... ]) -> state 2
```

Let’s say if one wants to challenge `block 1`, saying - `t2` in `block 1` in not valid as it should yield `state 2'` instead of `state 2`. How one can generate fraud proof?

---

**kladkogex** (2018-01-09):

I have  read the description several times, I am not sure  though I understand how an exit transaction is verified by the parent blockchain …

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> a confirm signature from each of the previous owners of the now-spent outputs that were used to create the UTXO.

Is this correct to say, that to exit you need to have signatures of all owners of intemediate UTXOs … ? And all of these signatures will be verified during the exit? Correct?))

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> [blknum1, txindex1, oindex1, sig1, # Input 1
> blknum2, txindex2, oindex2, sig2, # Input 2
> newowner1, denom1,                # Output 1
> newowner2, denom2,                # Output 2
> fee]

In this structure if I look at a particular UTXO, it may have two parents, so essentially if I go back N transactions in history for a particular UTXO, I will have 2^N ancestors  … ? correct?) Would it mean that the size of the exit proof would grow exponentially as coins exchange hands?))  Or I am missing something ?))

---

**vbuterin** (2018-01-10):

You do not need to provide a proof of the entire history of a UTXO in order to exit with that UTXO; you just need to prove that the UTXO exists and was included. It seems counterintuitive that you need to prove that little, but it works; it relies heavily on the fact that if any user sees an invalid UTXO get in, they need to exit within some timeframe, and make sure to not finalize transfers that were included after that invalid UTXO.

---

**kladkogex** (2018-01-10):

Vitalik - thank you - this clarifies things for many people!

Let me know if the following example is correct:

1. Alice moves 2 ETH into a Plasma chain
2. Alice pays 1 ETH to Bob which leaves an open UTXO for 1 ETH
3. Alice tries to exit the chain with the original 2 ETH UTXO
4. Bob has 7 days to notice the fraud.
5. Bob submits a proof of a later transaction that spent the 2 ETH UTXO.
6. Alice’s transaction is cancelled.

Are steps 1-6 correct? Is Alice penalized in any way, or her transaction is simply cancelled?

The question is what is the incentive for Bob to monitor the chain and submit a fraud proof?  If Alice is successful, why should Bob care ?  He still has his money on the Plasma chain,  why should he care if Alice minted some money on the parent chain ?)  in fact they could agree with Alice to split the profit, could they ?)

Another question is micropayments. If  Alice paid 10 cent to 1000 people, then for each of them submitting a fraud proof to the parent chain may not be economically viable.  If I need to pay $1 to make a fraud proof call,  it may be better for me to forgo 10 cents …?

And yet another question is “cloaking”

If transactions on the Plasma chain are cheap (they presumably will be ), then Alice can create 1000 sybil identities, so and pass the UTXO 1000 times through these identities before it is paid  to Bob. Then, it seems that it will not be clear to Bob what to monitor, he will have dig 1000 transactions back in history and follow every branch of the binary tree to find Alice and monitor her.

---

**ldct** (2018-01-11):

For step 1 do you mean “Alice moves 2 ETH into the plasma chain”?

---

**denett** (2018-01-11):

I think everybody who has coins on the plasma chain should watch the Plasma chain and should check all exits for validity. Eventually these invalid exits could drain the whole plasma contract and you can no longer withdraw your coins. The challengeExit method requires a confirmSig, I assume this signature is broadcast to all plasma watchers, so everybody can challenge all invalid exits.

I think the transaction fee of the challenge is indeed a problem. Why not wait for somebody else to do this challenge and safe on transaction fees (Tragedy of the commons)?

You could probably solve this by requiring a exit deposit in ether (larger than the fraud proof transaction fee). This deposit is returned together with your coins or is given to the person who proofs your exit is invalid.

You should even check all blocks for validity, because otherwise an evil owner could create an invalid block and then withdraw all funds from the plasma contract. In case of an invalid block, you should exits as fast as possible. If you notice the invalid block within 7 days and your funds were already in the blockchain before the invalid block, you will be able the exit before the evil owner.

---

**kladkogex** (2018-01-12):

> For step 1 do you mean “Alice moves 2 ETH into the plasma chain”?

Yep - sorry - I meant the plasma chain )

---

**ldct** (2018-01-12):

> He still has his money on the Plasma chain, why should he care if Alice minted some money on the parent chain

I think a withdrawal doesn’t mint eth on the parent chain, the plasma contract just sends previously-deposited eth to an address. If a spent TXO is fraudulently withdrawn (ie no one challenges the exit) then the plasma contract owns fewer eth than UTXOs and not all UTXOs can be withdrawn.

---

**kladkogex** (2018-01-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> If a spent TXO is fraudulently withdrawn (ie no one challenges the exit) then the plasma contract owns fewer eth than UTXOs and not all UTXOs can be withdrawn.

Correct - there is  a global variable that contains say 1M ETH …  A particular exit will change this global picture  say by 1 ETH - which is a negligible amount …

---

**ldct** (2018-01-12):

It’s not negligible - if there are 1,000,000 UTXOs in the plasma chain but the plasma contract only owns 999,999 ETH, then if everyone tries to withdraw the last person to withdraw must lose 1 ETH

---

**kladkogex** (2018-01-12):

Understood :-)))   IMHO reporting fraudulent withdrawals is doing work for the common good and not specifically an action to avoid personal financial loss …  Since they will have to pay roughly $1 per fraud proof the question is why a particular user need to pay $1 to serve common good …

Another question is how do users of a particular chain mass exit.  If all users try exiting at the same time, it can lead to  a huge spike on the parent chain, and increase gas costs, so they will have to pay $10 to exit instead of regular $1  - it can be something very much similar to a short squeeze on capital markets …

---

**kz** (2018-01-12):

I believe the solution for

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Understood :-)))   IMHO reporting fraudulent withdrawals is doing work for the common good and not specifically an action to avoid personal financial loss …  Since they will have to pay roughly $1 per fraud proof the question is why a particular user need to pay $1 to serve common good …

is

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> You could probably solve this by requiring a exit deposit in ether (larger than the fraud proof transaction fee). This deposit is returned together with your coins or is given to the person who proofs your exit is invalid.

You can probably design the system in such a way that requiring an exit requires a lot more ether than what is enough to cover fraud proof.

In that way the reporter of fraud proof could actually earn fee for doing work for common good.

That should align the incentives in that regard as far as I can tell.

---

**kz** (2018-01-12):

Could a combination of this

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> deposit(): generates a block that contains only one transaction, generating a new UTXO into existence with denomination equal to the msg.value deposited

and

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> startExit must arrange exits into a priority queue structure, where priority is normally the tuple (blknum, txindex, oindex) (alternatively, blknum * 1000000000 + txindex * 10000 + oindex)

create a potential issue?

There is a potential race condition between:

- Alice, she could be depositing a large sum of ETH into the plasma chain because she has validated the state of plasma chain and she wants to participate
- Bob, (the plasma chain operator) who runs the plasma chain and has decided to generate an invalid plasma block that generates new UTXO out of thin air and wants scam the system because he has registered the huge transaction Alice is making. (he can also use a lot of his ETH to bribe the main chain operators to include his fraudulent transaction that registers the plasma chain merkle root before Alice’s deposit enters the main chain).

**Because of the ordering or exits, the deposit and the resulting exit Alice could be making will be ordered after Bob’s fraudulent exit that references UTXO he created out of thin air, and the amount of ETH on main chain could be depleted before Alice could finish her exit, thus she would be damaged.**

This could be solved in a simple way by treating ETH deposit on main chain with weight of -1.

def ordering(blknum, txindex, oindex):

weight = blknum if not deposit(blknum) else -1

return weight * 1000000000 + txindex * 10000 + oindex

The deposit UTXO could be:

- not spent → then there could be no problems with changing the ordering.
- spent → then one could again submit a fraud proof.

---

**denett** (2018-01-13):

I agree that there could be a potential race condition with deposits, especially a problem when the transaction queue on the parent chain is very long. Alice has not checked (possible invalid) plasma blocks that arrive after she sends her deposit, while these blocks are could be included in the plasma chain before her deposit block.

I don’t know if I understand your use of the -1 as the weight instead of the block number, wouldn’t that allow Alice to withdraw straight without a waiting period? Then she could spend her coins on the plasma chain and withdraw as well before anybody could challenge her. Maybe her waiting period should be a little shorter (a day?) to make sure she will always be able to withdraw safely. So something like: weight = blknum-X where X is the number of blocks in a day.

An other problem could be a double spend on the parent chain. If Alice deposits on the plasma chain and immediately sends the coins to Bob on the Plasma chain, but also double spends her deposit ether on the parent chain by sending it to Carol.

If the parent chain reorganizes, the finalized chain could end up with both the transactions to Bob and Carol, but without the deposit.

So maybe deposited funds should only be spendable on the plasma chain after the deposit block is finalized on the parent chain.

---

**vbuterin** (2018-01-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> The challengeExit method requires a confirmSig, I assume this signature is broadcast to all plasma watchers, so everybody can challenge all invalid exits.

The signature is not broadcast to all plasma watchers, because that would allow any sender to hold up the system by not broadcasting their signature. Rather, if you receive a UTXO, then you need to show the confirm sig for the UTXO *at the time that you spend* the UTXO. Slightly different mechanism, but same effect.

> Why not wait for somebody else to do this challenge and safe on transaction fees (Tragedy of the commons)?

If we want to, we can require participants to submit an additional deposit upon joining the system, and give this deposit as a reward to those who challenge.

> You should even check all blocks for validity

Exactly correct. And if you notice even one invalid block get accepted, you exit immediately (or at least within 7 days).

> If all users try exiting at the same time, it can lead to a huge spike on the parent chain, and increase gas costs, so they will have to pay $10 to exit instead of regular $1 - it can be something very much similar to a short squeeze on capital markets …

This is indeed the fundamental flaw in *all* channel systems, raiden and lightning included, and is the reason why the scalability of this system can’t go *too* far above the scalability of the main chain. 2-3 orders of magnitude probably but not that much more.

> There is a potential race condition between:

You’re right. One simple way of fixing this is to require a minimum waiting period between consecutive submitted blocks, so if you want your deposit would be safe you would submit yours right after the plasma chain submitted a new block, so that it would with quite high probability get included on time.

---

**denett** (2018-01-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Rather, if you receive a UTXO, then you need to show the confirm sig for the UTXO at the time that you spend the UTXO. Slightly different mechanism, but same effect

So if Alice sends plasma coins to Bob, at first only Bob is able to challenge her exit. Only after Bob spends his coins the confirmSig is publicly known and everybody can do the challenge. If Bob keeps the plasma coins, but fails to challenge Alice’s exit, I assume he is punished and cannot spend the plasma coins anymore.

---

**kz** (2018-01-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> So something like: weight = blknum-X where X is the number of blocks in a day.

I’ve had the same idea, but it would be great to have a solution that doesn’t have additional assumptions (that there is a plasma block speed limit) and works.

The speed by which plasma chain operator produces blocks can be manipulated, so that creates another potential attack vector.

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> wouldn’t that allow Alice to withdraw straight without a waiting period?

Ah yes, sorry. That could be solved by adding additional priority queue (ordered by ETH block number) that delays exits of just deposited UTXOs for specific safety time delay approximated in main block count. That would require propagating main block number through plasma UTXO. After enough time has elapsed (e.g. 3.5 days), they are added to normal exit queue with weight -1. That gives enough time to report double spend fraud.

I think that ETH main block number or time stamp will need to be stored in priority queue anyway:

`(Plasma block number, txindex, outindex, **mainBlockNumber**)`

… since otherwise one is trusting plasma chain operator block time stamps to make sure e.g. 7 days have passed.

I’m not sure does the proposed solution have some additional flaws ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> You’re right. One simple way of fixing this is to require a minimum waiting period between consecutive submitted blocks, so if you want your deposit would be safe you would submit yours right after the plasma chain submitted a new block, so that it would with quite high probability get included on time.

[@vbuterin](/u/vbuterin) Thnx for your time ![:bowing_man:](https://ethresear.ch/images/emoji/facebook_messenger/bowing_man.png?v=12)

I wonder could this be also gamed. Let’s assume that there is a minimal waiting period, but if that minimal period elapses, one is again open to that race condition since one can’t guarantee when will next plasma block be produced ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) That could create problems in scenarios where plasma block production isn’t predictable.

---

**kz** (2018-01-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> If the parent chain reorganizes, the finalized chain could end up with both the transactions to Bob and Carol, but without the deposit.

Oooooh, nice catch. I’ve just realized that the plasma chain would probably also need to be nondeterministic until blocks can be finalized.

How would one determine the correct winning plasma chain tip since there could be multiple plasma chains depending on multiple ETH chain branches?

---

**kz** (2018-01-14):

I’m just trying to wrap my head around this.

Does entering plasma chain requires validating entire plasma chain history?

It seems to me that otherwise one risks entering insolvent plasma chain.

If so, how could some system with huge state (e.g. omise go) be built on top of a plasma chain?

---

**denett** (2018-01-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/kz/48/685_2.png) kz:

> I’ve had the same idea, but it would be great to have a solution that doesn’t have additional assumptions (that there is a plasma block speed limit) and works.

At the time of the startExit call the contract can calculate how many blocks have passed in the 24 hours before the deposit and use that as X for this exit.

I assume the timing of the 7 and 14 days is based on the block times on the parent chain and not on the block time of the plasma chain (if there is any).

Drawback of this extra 24 hours is that everybody has to watch the plasma chain at least every 6 days instead of 7.

Therefore I like [@vbuterin](/u/vbuterin) solution better to have a minimal spacing between blocks that is enforced in the contract, although this does not work if the transaction queue on the parent chain is long and unpredictable. In that case you should not deposit all your ether at once but do it in batches, to minimize the risk.

Another solution is to have the operator deposit a certain amount of ether that has a longer waiting period. That would also incentivize the operator to challenge all invalid exits, because the operators funds are the first on the line.


*(123 more replies not shown)*
