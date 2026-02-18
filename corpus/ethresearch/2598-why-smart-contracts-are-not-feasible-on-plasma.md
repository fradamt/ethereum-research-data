---
source: ethresearch
topic_id: 2598
title: Why Smart Contracts are NOT feasible on Plasma
author: johba
date: "2018-07-18"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/why-smart-contracts-are-not-feasible-on-plasma/2598
views: 15404
likes: 41
posts_count: 18
---

# Why Smart Contracts are NOT feasible on Plasma

While some MVP implementations are approaching production, more teams are exploring the realm of general computation on Plasma chains.

Here are some assumptions/expectations about smart contract running on Plasma that I have been hearing:

- Account-like structure with code and persistent state.
- Ability to have custody of funds.
- Exit games under subjective data-availability assumptions.

In this post I want to describe my thoughts on why smart contracts are infeasible on Plasma under those assumptions and give an example.

## TL;DR

**Once data-withholding starts, all contract states and  balances have to be considered corrupted, as state transitions during data withholding can not be verified. Subjective data-availability prevents the construction of an efficient exit game.**

## Example

We assume a very basic multi-signature wallet contract on the Plasma chain. Alice and Eve have a key in the wallet, the wallet balance is 1 PETH (Plasma ETH), and the contract has only 2 bits of state, `signed-by-alice` and `signed-by-eve`. To flip one of the bits a transaction needs to be send to the wallet with a valid signature by Alice or Eve. Once both bits are set to `true`, 1 PETH is transferred to Eve.

In the scenario of the operator becoming byzantine, we want to be able to construct an exit game for the given contract that allows to exit the state (2 bits) and contract funds (1 PETH) into an identical contract on the main network. Alice and Eve should be able to continue using the multi-sig wallet on Ethereum.

### Youngest State Exits

A naive exit game with the following rules is constructed:

- Period 1 - Find the youngest included contract transaction and concluding state. Allow to append further non-included transactions that spend directly from that state, but require a bond for each.
- Period 2 - Allow to challenge any appended transactions using a Truebit-like computation verification game. Successful challenger receives bonds of all following invalidated transactions.

After the second period the latest unchallenged state of the contract is exited.

The table below shows the state of the Plasma chain at different times (**t**):

`t - 1` - 1 PETH in contract, no signatures to spend from contract.

`t + 0` - This block is withheld from Alice by operator.

`t + 1` - The new contract state is Alice having approved the withdrawal already. (Yet, she never sent her signature, the operator simply flipped the bit in the unavailable block.)

`t + 2` - Eve signs with her key and receives 1 PETH.

|  | t - 1 | t + 0 | t + 1 | t + 2 |
| --- | --- | --- | --- | --- |
| Alice | b: 0 | ~ | b: 0 | b: 0 |
| Eve | b: 0 | ~ | b: 0 | b: 1 |
| Contract | b: 1, s: [0, 0] | ~ | b: 1, s: [1, 0] | b: 0, s: [1, 1] |

Obviously Alice will initiate a Plasma exit, as she can not see the data in **t + 0**, and try exit state **t - 1**. Eve will be able to use *youngest transaction* rule from period 1 of the exit game and replace **t-1** with **t+1**. Eve will then append **t+2** during the exit game. Alice will not be able to challenge, as the transition is valid, and the wallet will be exited without funds, even though Alice never signed a withdrawal to Eve. ![:cry:](https://ethresear.ch/images/emoji/facebook_messenger/cry.png?v=9)

### Oldest State Exits

We construct another naive exit game with rules to catch the previous case:

- Period 1 - Find the oldest included contract transaction. Allow to append further included or non-included transactions that spend directly from that state, but require a bond for each.
- Period 2 - Same as before, filter out invalid state transitions through crypto-economic computation verification.

The table below shows the state of the Plasma chain at different times (**t**):

`t - 99` - Contract balance is 1 PETH, signature by Alice present.

`t - x` - A lot of interactions with contract that don’t change state.

`t - 2` - Contract balance is 1 PETH, signature by Alice present.

`t - 1` - Eve signs and receives 1 PETH.

`t + 0` - Data withholding starts.

|  | t - 99 | t - x | t - 2 | t - 1 | t + 0 |
| --- | --- | --- | --- | --- | --- |
| Alice | b: 0 | … | b: 0 | b: 0 | ~ |
| Eve | b: 0 | … | b: 0 | b: 1 | ~ |
| Contract | b: 1, s: [1, 0] | … | b: 1, s: [1, 0] | b: 0, s: [1, 1] | ~ |

Eve has received 1 PETH on the Plasma chain already, and exits the funds through the priority queue. In addition, Eve decides to propose an old state of the contract at **t - 99** according to the exit rules for contracts defined above. Due to a bunch of spam interactions with the contract, other participants are not able to “catch up” the state, as it is too expensive to submit 90+ transactions to the main net.

=> The contract is exited with a balance of 1 ETH and a ready approval by Alice in its state. Eve claims the 1 ETH with an on-chain transaction to the multi-sig and now has 2 ETH total. ![:cry:](https://ethresear.ch/images/emoji/facebook_messenger/cry.png?v=9) It is assumed that the extra ETH comes from an honest participant of the Plasma chain that had a UTXO younger than Eve’s. This participant will not be able to exit.

## General Computation with Tradeoffs

The previous example has shown that subjective data availability paired with persistent state prevents the construction of any efficient exit game for smart contracts. How does this change if some of the assumptions made about contracts on Plasma are relaxed?

- Drop State: Verification of computation can be done during the exit game independent of previous state. While loosing the convenience of stateful programming, Bitcoin script-like applications would still be possible.
- Drop Custody: Contracts can be executed on Plasma, but can never hold funds or exit their state. This enables routing of funds on Plasma and chains for DEX-like applications. Interesting use-cases that require custody need to stay on main net.
- Notarize youngest available block: Knowing the youngest available block would make the first exit game in the example feasible. This could be done with a bonded set of notaries that vote on the availability of blocks using crypto-economic aggregate signatures. (Note: This is out of scope of Plasma, more similar in design to sharding.) The security assumptions of funds held in smart contracts would not be the same as for other UTXO’s on the Plasma chain. While funds held directly would be as secure as on the main network, contract funds would only be secured up to the deposit size of the notaries.
- Write all contract as zkSNARK/STARK circuits: This is an interesting approach that would allow to construct Plasma chains that are correct by construction. It is currently limited by circuit size, developer convenience, and the ability to nest proofs.

## Questions

- Do you agree or disagree with the statement that smart contracts are infeasible on Plasma?
- Which one is you favorite tradeoff?

## Replies

**kfichter** (2018-07-18):

I’ve been asked about “EVM Plasma” a few times over the last week so I figured I’d share my opinions here (seems relevant).

The Plasma framework effectively relies on something I call “state objects.” Each of these objects are pieces of state that can only be modified under certain conditions. For example, a UTXO can only be converted from “unspent” to “spent” if a valid spending signature is present. Additionally, each state object can only be exited under certain conditions. Note that the conditions under which a state object can be exited may differ from the conditions under which it can be modified. For example, it might make sense that a tic tac toe game can only be modified by one player on their respective turn but can be exited at any time by either player. Plasma app designers also need to specify a state transition validation function. The logic here is application specific.

A key consideration is that we must always exit the last valid state to the root chain. Any valid state update from state A to state B will invalidate any exit on state A. Therefore, if someone can cause a valid state update, they can block an exit.

The problem with thinking about smart contracts on Plasma in the same way we think about smart contracts on Ethereum is that Ethereum contracts make bad state objects.

Ethereum contracts typically have no clear overall owner, even though individual components of the contract might. This means it’s not easy to assign the user(s) responsible to exit the object. Contracts can also often be modified by many, if not all, network participants. Remember that exits on these objects would be blocked by any valid state transition.

This mental framework allows us to see another path to plasma smart contracts: going back to “nested Plasma.” Instead of thinking of smart contracts as the smallest atomic state objects, we can instead think of smart contracts as mini plasma chains that contain their own state objects.

We basically want to break these contracts down into explicit pieces of state with a reasonable ownership model. For example, we can think of an ERC20 as a version of Plasma MVP with more interesting state transitions. It might not be possible to reconcile contracts where state cannot be reduced to clear ownership (“satoshi’s place” style stuff).

---

**ldct** (2018-07-20):

I’ve run into similar problems thinking about how to run payment channel smart contracts on top of plasma. That said, while designing an efficient exit game that works for all smart contracts seems tricky (and I have nothing to offer in that regard), maybe we should try to do it for specific contracts / classes of contracts, and then try to generalize.

1. We know plasma cash / MVP work, hence we know “plasmafied payments” work. Similarly any other stateless smart contract should be pretty straightforwardly portable, eg fully collateralized swap options and stateless multisig wallets.
2. If you can split the dapp into a small stateful part and a large stateless-UTXO part, you could run the stateful part on ethereum. An example: if there were a trusted on-chain oracle that gives you the result of some real-world event (implemented for e.g. by SGX, and under the security assumption that you trust Intel), you could modify plasma cash to have the ownership changes of UTXOs dependent on the on-chain oracle, which plasmafies the trading functionality of aprediction market. Another example would be a bounty contract where the bounty can be claimed by producing a pair of sha3 collisions; bounty can be funded on the plasma chain but the resolution (i.e. the verification of the collision) done on ethereum.
3. For smart contracts with defined participant sets, the construction in State Channels and Plasma Cash can be used, and you do end up getting most of the benefits of plasma out of this, so I do consider this to be a way to “run the dapp on plasma” in some sense. The big reason why you might not consider it to be so is that the bound on how much someone can grief doesn’t change compared to just running your dapp in a state channel.

But it is still an open question to me how far this can be carried, e.g., if an Augur-like resolution mechanism can also be carried out on the plasma chain, since that resolution mechanism does depend on data availability and censorship resistance (e.g. if I see an incorrect resolution I’m supposed to contest it).

Another mechanism the analysis doesn’t rule out is some way to rely on the nonzero consensus strength of the plasma chain, e.g. if it is run by proof-of-stake, presumably the value of the staking coin represents the expected future revenue of transaction fees, and block producers need to have a collective incentive of that amount (e.g. someone bribes them, or they have a position in the prediction market) to censor or to withhold blocks. I think this is something the original plasma paper discusses in the context of nested plasma chains.

---

**Equilibrium94** (2018-08-16):

Can you expand more on the zkSNARK/STARK circuits solution? Maybe with an example?

Thanks!

---

**fubuloubu** (2018-08-16):

I wonder if a modification of the subchain which looks more like Bitcoin might work. It might use a subset of EVM (that might be called EVMscript) which might be implementable as a smaller interpreter with limited functionality on the main chain.

Each UTXO can then be locked with a small EVM program that evals to True/False and can only read environment state variables like msg.sender and blk.number. The smallest valid program might look like `msg.sender == 0x...` (msg.sender gets interpretted as the signer of the transaction)

Someone has probably thought of this before and knows why it’s stupid, but a reduction of scope on what a transaction can do that’s UTXO-compatible and works with the EVM would be a cool way to scale up Plasma computation a bit.

Ha, maybe if you had library code in the main chain your plasma contract points to, you can have short “macros” it can point to in the transaction data.

---

**solidblu1992** (2018-08-17):

Another thing to explore would be scriptless scripts using Schnorr adaptor signatures.  That’s something that’s very compatible with the UTXO model from MVP.  However, I’m not sure how close that gets you to general computation.  I’m still learning about them and their limitations.

---

**nginnever** (2018-08-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> We basically want to break these contracts down into explicit pieces of state with a reasonable ownership model. For example, we can think of an ERC20 as a version of Plasma MVP with more interesting state transitions.

I think this is right. It would seem that ERC20 is achievable in plasma in theory since all of the stored state has some clear owner and you see that expressed in a UTXO way in MVP.

The hard part is dealing with state that matters to multiple people, though this may actually be rare state so to speak, I can think of a few simple examples of it (i.e. a score count that marks a global record like total sales in a token sale or number of wins in a game for a group). Consider the case of a contract that takes one state transition to increment an integer counter, if there was no account ownership of this integer, then we have no clear owner of the integer. If it is found that the operator decided to say decrement the integer in a state transition present in a block, we would want to revive our communal progress on incrementing this integer back to a safe validator set. In order to handle what I am now calling “commons” type state, we have to think of more clever mechanisms perhaps.

If we want to extend this simple contract to nested chains, i believe we still have to be sure these nested chains respect that ownership is clearly defined in the application. I am currently speculating on what can be done about this commons state…

*EDIT: First thoughts*

**Forking plasma exits: A democratic approach to state exits**

Maybe we can construct the exit rules of the plasma parent contract to handle communal state exits by allowing the exit to fork. To do this we will require that an exit from a plasma chain comes with a snapshot of the state. This snapshot will come in the form of the block height of the plasma chain at which it is no longer valid to process transactions. I.e. if we have a plasma chain contract with the following state updates.

T-1: correct state

T-0: state withheld by operator, suspect invalid transition

T+1-n: Suspected invalid plasma chain continues

Here, the honest party will want to exit on state T-1 and not allow the exit to process any transactions beyond that block height. This first request to limit the height to T-1 will flag to the community of some alarm and allow others to exit under this height. Each height chosen to exit will create a separate on-chain state storage object to house the exit and essentially fork the plasma chain into multiple chains on the parent. If the operator is byzantine or colluding with a small set of accounts on the child chain then they will want to exit on a fork that the rest of the community does not want to exit on so they will only be able to exit with incorrect transitions to their block height fork. This fork could later be determined invalid by the community.

Considerations:

This requires the majority of honest participants to know when an operator is byzantine.

Forks are generally not nice to deal with though I am not sure if we have any examples to draw on of a fork like this (the dApp space wasn’t mature enough to be really affected by the ETC fork?).

Maybe voting on a canonical chain with a CAS exit could be done.

---

**sg** (2018-08-27):

As per this PlasmaMVP exit discussion, out-of-thin-air-exit causes mass exit.



    ![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png)
    [Exiting invalid tx in omg mvp?](https://ethresear.ch/t/exiting-invalid-tx-in-omg-mvp/3016/2) [Plasma](/c/layer-2/plasma/7)



> The contract doesn’t prevent validators from including this type of transaction. However, once a transaction like that is included, everyone on the Plasma MVP chain needs to exit within a specified period of time (~1 week).
> Basically it doesn’t matter if we do the check or not. The contract can check that the transaction is valid (inputs >= outputs), but the validators can just spend the invalid UTXO and create a transaction that appears to be valid.

Let’s say in the EVM Plasma context, contract-deposited-or-locked UTXO might be vulnerable to this attack coz the withdrawal Tx would update the timestamp of this UTXO.

Now the options are only two

1. Contract exits the locked UTXO (only if the contract has that spec)
2. Withdraw deposit and exit (This UTXO’s exit will be inferior priority than out-of-thin-air-exit Tx so that Rootchain deposited fund would be damaged)

This is also one of another difficulty of EVM Plasma.

“UTXO history’s full scanning before exit” could be mitigation though, this construction must answer some questions which are “Who will do that?”, “Is it fairly decentralized?”, and “Is the gaming probability enough mitigated?”

---

**nadahalli** (2018-08-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/johba/48/20905_2.png) johba:

> Once data-withholding starts, all contract states and  balances have to be considered corrupted, as state transitions during data withholding can not be verified. Subjective data-availability prevents the construction of an efficient exit game.

When you say data-availability and unavailable blocks, you mean that the Plasma operator and Eve are together making the underlying root chain’s (Ethereum, in this case) blocks not visible to Alice (by doing some sort of block withholding attack). And that’s why Alice is unable to exit Plasma at t+0, when Alice should have seen a block, but did not.

Or is data-unavailability in this case referring to the Plasma blocks? I didn’t quite follow this.

---

**johba** (2018-10-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/nadahalli/48/2063_2.png) nadahalli:

> Or is data-unavailability in this case referring to the Plasma blocks?

Yes, all thoughts about data-unavailability and unavailable blocks concern the Plasma chain only. As you correctly said, Eve and the Plasma operator may collude. But they can only affect the visibility and content of the Plasma chain.

![](https://ethresear.ch/user_avatar/ethresear.ch/nadahalli/48/2063_2.png) nadahalli:

> the Plasma operator and Eve are together making the underlying root chain’s (Ethereum, in this case) blocks not visible to Alice (by doing some sort of block withholding attack)

An eclipse attack on Alice is also a possible scenario (not limited to Plasma, it could affect main-net transactions and state channels), but the cost of doing so is probably a manyfold of the value locked in the Plasma chain. Hence I have not considered such attacks here.

The [Plasma Leap](https://ethresear.ch/t/plasma-leap-a-state-enabled-computing-model-for-plasma/3539) write-up has some ideas how to deal with state under subjective data-availability assumptions.

---

**johba** (2018-10-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> I wonder if a modification of the subchain which looks more like Bitcoin might work. It might use a subset of EVM (that might be called EVMscript) which might be implementable as a smaller interpreter with limited functionality on the main chain.

[@fubuloubu](/u/fubuloubu) Would you be interested to co-author or review this [paper draft](https://docs.google.com/document/d/1vStTjqvqZGyiI5AVtpwCIMlHFnzC_4bbixsCfs27-M8). It is full of your ideas like EVMscript and bitcoin-like spending-conditions. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**fubuloubu** (2018-10-08):

Lol, we chatted in Berlin about it.

I reviewed the draft. It’s looking good so far!

---

**syuhei176** (2018-10-15):

We are considering about similar things.

When we treat UTXO(include coin), it ofeten has unlock script. it is not complex one, just locking value. We can verify all state transition on RootChain(in exit and challenge process) and Plasma. And every state is exitable and withdrawable.(users can continue state transition on RootChain)

And I have problem, that we can’t lock value on Plasma. This problem may from that users can’t trust anyone in Plasma. User have to verify history on coin before recieveing. So every transactions need confirmation signatures by receiver(They are also exitable user of this UTXO). So user who locked value always can prevent “unlock”. And who should verify unlock action for the value is not clearly in any time. This is the reason why users can’t lock value on Plasma.

If you have any suggestions or ideas about it, I wanna discuss.

zkSNARK/STARK may solve this, but may also have circuits size problem.

---

**technocrypto** (2018-10-28):

As [ldct](https://ethresear.ch/u/ldct) mentions I think it is useful to start with less-than-ideal solutions here and see how they can be made more ideal.  To that end:

1. Assume that all state transitions within Plasma blocks are proven correct by [some method].  Personally I think aggregated zero knowledge is very likely to get used for this if the engineering work gets put in, but feel free to substitute your preferred method.  (This is different from most current Plasma designs).
2. Assume that when state is claimed unavailable by a Plasma user we have some mechanism to either submit the state to the main chain, or invoke a mass exit (so we’re not going to try for the additional efficiencies yet of identifying subsets of the overall state that were unaffected by a specific availability issue, we’re just treating the whole state as a blob that’s either totally available or totally unavailable for a given block).
3. Assume that we have some method of forcing valid Plasma state transitions from the main chain side if they are being censored Plasma side (like anyone can submit a Plasma block if they prove the state transition is correct, even if they have to reserve a slot or something).

Okay, that is a pile of assumptions.  But under these assumptions, it seems like we can just do the “yanking” thing from sharding and say:  each contract on Plasma sets its rules for when it can be yanked, and that yank is initiated by a Plasma tx which satisfies those rules.  If the Plasma operator interferes with valid yanking you just submit the Plasma tx from the main chain side to complete the yank.  And if data availability issues happen while a contract is unyanked you have to finish the mass exit in some way that either moves the contract to a new Plasma operator unyanked and available or yanks it in a fashion acceptable to its own rules.  Now contracts have to figure out their own tradeoff between the “griefing” issue of letting anyone just yank the contract at any time, and the coordination of cost of requiring ever higher criteria be met before yanking can happen (same as on sharding anyways, so there will be plenty of best practices around).  Users who own state on contracts they can’t yank can just build other yankable contracts, assign the state to them, and then yank them, and all the other things one will have to do for sharding anyways.  Thoughts?  I realise there is a lot of hand-waving here but I am not at all convinced yet that Plasma can’t do general smart contracts, and this seems like at least one way to start figuring out how they might be possible.

---

**qbig** (2018-12-10):

This looks promising as people are trying similar things:

https://blog.chain.com/introducing-txvm-the-transaction-virtual-machine-5e4c9ef1478f https://parseclabs.org/files/plasma-computation.pdf

---

**qbig** (2018-12-10):

I have read your blogs and replies many times and finally being able to understand the nuances, that we could only exit/challenge a “state” with clear ownership: eg. UTXO or non-fungible token or even ERC20 token. In other words, if I own a coin, I should be able to exit it from the plasma chain, to my account on the root chain. In other words, we are focusing on the “valuable assets” aspect of state, rather than generic data. Eg. Deposits, withdrawal, exit, challenge etc, all these terminologies are revolving around coins/tokens/assets.

But in general, ownership of state in a contract is not always clearly assigned. So could we instead focus on the general validity of a transaction? Or rethink what we means by “exit” for a smart contract with no coins?

In this case, we could totally see why modeling EVM computation as UTXO might work:

- TxVM Slides
- Plasma - MVP to General Computation
as UTXO clearly owned by particular users.

---

**qbig** (2018-12-10):

Could you explain why user needs to  “lock” value on plasma chain ?

---

**syuhei176** (2018-12-10):

I’m sorry I didn’t make it clear enough.

We are working on simple multi-sig in Plasma. (Also aiming to more complex smart contract)

So we wanted to lock value(like UTXO programming)

The above question was solved ourselves.

https://github.com/cryptoeconomicslab/plasma-chamber

