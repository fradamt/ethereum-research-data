---
source: ethresearch
topic_id: 2344
title: "Plasmabits: Viable Stateful Sidechain"
author: esteban
date: "2018-06-25"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasmabits-viable-stateful-sidechain/2344
views: 5395
likes: 4
posts_count: 10
---

# Plasmabits: Viable Stateful Sidechain

## Plasmabits

This is a proposal for a Plasma sidechain implementation that can run EVM-based smart contracts. In Plasmabits, the operator (a centralized block issuer) must do its best to keep the liveness, availability and correctness of the sidechain, or lose a security deposit on the root chain. This is similar to a proof of authority sidechain, as it can achieve sub-second times between blocks, but it’s completely validated on the root chain. We deal with the risk of block withholding using preimage challenges, and validation of consensus rules is enforced using a system of challenges, and a TrueBit-like verification for the EVM execution. All these challenges are incentivized with a bounty, coming from a security deposit.

The main motivator for this is to run software as similar as what we currently have, without needing special plasma light clients or nodes. The security deposit makes it easier to estimate the security of the sidechain in monetary terms. I wasn’t sure about calling this plasma, as most designs out there are UTXO-based and this is state-based, but it keeps (at least I think so) the assurance that it’s safe under block withholding.

It’s my first post here, so please let me know of any etiquette mistakes ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

### Challenges

When working correctly, the operator frequently commits to the sidechain blocks in the root chain. A set of validations keep the operator honest. There are a number of insurance contracts incentivizing the verification of the chain. These contracts combined would make for a complete set of consensus validation rules (an actual virtual client) on the root blockchain. Such rules include:

- Withholding challenges: The operator might have submitted blocks to the blockchain, but it withheld the contents. The operator must present a preimage or get slashed
- Parsing challenges: The operator submitted an invalid block structure.
- Transaction censorship: Submit a transaction on the root chain, requesting for it to be included in the sidechain within a certain timeframe
- Invalid block signature: The operator provided an invalid signature of the block.
- Invalid previous block hash, height, or previous state, among other block verifications.
- Any other consensus failure checks, like transaction receipts posting an invalid after state.
- Invalid transaction execution: Need an on-chain way to verify a transaction.

The last step is the most complex technically, but using a Truebit-like binary search, we would only need to verify one EVM state transition. A PASITO contract (Plasma Arbitration Stepping Instruction Test Operator) computes such transition.

### Block commitments to the root chain & Withholding

With a certain frequency (to be parametrized), the operator submits to the blockchain the root hash of a Merkle tree with all the block headers since the last checkpoint, plus what range of block heights it is committing to. The validators can construct such tree and verify that they are following the same chain.

In case the validator created a fork, this commitment serves as a proof to show the existence of two blocks with the same height (because the twin block would be signed with the operator’s private key). There are some data structures that could save some storage space on the long run, like a Merkle Mountain Range. This commitment can also be used to challenge downtime of the operator (at least one submission every X time). In case the operator submitted a Merkle tree that validators can’t create, a challenge can be created to query for a particular leaf value and its path. Weaknesses with this are network congestion of the root chain.

In order to validate that the operator is not withholding blocks, any validator might request the operator to submit a preimage of the hash of the block. Blocks on the sidechain would be limited in terms of size to whatever can be sent as data of a transaction in the root chain, accounting for the cost of hashing and verifying the hash. This is not so much a scalability problem, as blocks in the sidechain could have 1 tx per block.

### Sidechain Halting

For any successful challenge, the contract tracking the status of the sidechain would stop accepting any further updates. This starts a challenge period where there needs to be certainty on which is the first block that broke consensus (the first invalid/withheld block, or the previous block from a fork) through a series of new challenges. But even in the case that an on-chain challenge is happening, other users and validators could decide to carry on if they don’t agree with the challenge. Validating nodes could continue operating, if they trust that the challenge will eventually be resolved. Some challenges could even be solved by the validators themselves, as that they might want to mitigate the risk of a spam attack or miner censorship attack (or even the operator attacking itself).

### Entering and Exiting

This is externalized to the contracts that want to do operations crossing the boundaries of both chains. The root chain hash needs to be included on the side chain, in order to facilitate atomic swaps between the sidechain and the root chain. In this case, the ETH that enters the plasma chain could behave like an ERC20. Exiting a halted sidechain would also be left to the cross-chain contracts, as users can provide proof of the world state of the sidechain before it came to a halt.

#### Entering

1. Alice deposits ETH in contract A. Contract A provides an uuid for this deposit and maps it to the amount.
2. Upon enough confirmations of the root chain, a block in the sidechain will include the root state of the main chain block where the deposit happened.
3. Alice can create a proof of state of the mainchain’s contract A, for her deposit’s UUID.
4. The contract B, in the side chain, issues an equivalent amount of tokens to Alice upon her submission of the proof. Marks the uuid as claimed.

#### Exiting (not halted):

1. Alice sends her sidechain-ETH to the contract B. The deposit gets burned.
2. Once the challenge period for withholding and other checks has elapsed, Alice can show proof of the burn in the sidechain to the contract in the mainchain and retrieve her ETH.

#### Exiting while Block withholding:

Assuming Alice is running a fully validating sidechain node, she should have all the blocks up to the moment when she did the burn, so she can submit the blocks herself (they are signed by the operator). If the block with the burn is withheld, and the operator fails to show proof of it in the mainchain, then the sidechain will halt, and Alice can follow the steps described in the next subsection. Otherwise, if the block next to her burn is withheld, the mainchain contract would handle this as in the previous subsection, and Alice won’t be able to double-spend because her balance at the moment of the halt will be zero. In any case, Alice should not consider transactions finalized until receiving the block with the transaction, and making sure that all blocks before are valid and available (she can respond to challenges herself).

#### Exiting (halted):

1. Alice shows proof of the world state in the sidechain at the block when the sidechain halted.
2. Contract A returns the equivalent amount of ETH, and marks that the address can no longer withdraw (which is fine since the sidechain is halted).

Also, there could be a “Never exiting” policy, where a new sidechain can pick up from where the previous operator left, as specified in the root chain contract (perhaps some oracle, or an auction for who creates the biggest security deposit).

It could have some constraints to accommodate for security margins and challenge periods.

### PASITO: EVM²

This past October, a precompile was suggested to run the [EVM inside an EVM](https://github.com/ethereum/EIPs/issues/726). We intend to do the same, by having a stepper contract that can compute a EVM state transition.

Some work on this already started (see [solevm](https://github.com/Ohalo-Ltd/solevm/blob/master/src/EthereumRuntime.sol)), but we want to focus on correctly encoding the whole EVM state in such a way that it can fit inside a transaction in the root chain, for the purposes of verifying it with an interactive Truebit game. We believe that a large security deposit, plus other economic interests that participants might have in the correct operation of the sidechain, would lead to less risks than general purpose Truebit (sorry about the hand-waviness here – this needs more careful analysis).

Some elements of the EVM state could be submitted under a hash tree structure to save transaction bytes, like unaccessed parts of the code, memory, and the stack if it grows too much. The final truebit transaction would have to provide witnesses for storage as needed.

Potentially, all the *COPY operations would be the most problematic opcodes – because creating a succinct proof for highly partitioned memory can be very challenging (would need to have a nice data structure to produce offset-friendly-merkle-trees to calculate quickly the overlay of one array on top of another). Overlaying multiple merkle proofs can do the trick, but this is still early work in progress (it could be a list where its elements have a range and the merkle root for each range; so retrieving a value from here is achieved by cycling through this list until the range matches, and finding the value in the merkle tree).

Something that is pretty interesting is that running only one step makes things like snapshots or rollbacks an easier problem than with a normal interpreter, so actually the CALL ops are not very difficult.

### Economic incentives for validation

To prevent front-running, all challenges should follow a commit-reveal schema. But validators that are not miners could be still be exposed to front-running, thus reducing the incentive to validate the chain if one doesn’t have a root chain mining operation (a miner could not validate the sidechain until it sees a challenge, and censor the transaction until it can see the mistake in the execution of the EVM or a similar error). This is one of the biggest blockers and where we would really appreciate feedback.

On the subject of allowing several challenges at the same time, the first committed-to challenge would win, but further research on what kinds of situations this can bring is required.

Withholding challenges would have to have a cost, but the dynamic of this is a little weak - either the users could grief the operator, or the operator grief the users by always withholding until challenged.

### Ideas / Difficulties

- Economic incentives for the slashing/rewarding of the validators: would like to provide the security deposit in full to the successful challenger, but to prevent the operator from challenging itself, burning a percentage (say, half of the deposit) looks like a better idea.
- The EVM stepper has to be completely compatible with geth/parity execution
- Build a validating client that can generate proofs
- Complexity of the evm state transition contract
- Network attacks (spam, miners, high transaction fees, high cost of answering challenges)
- Considering ewasm instead of evm
- Complexity of the transaction cleanup (correct receipts included in the block and state updates)

I’ve been trying to get as much feedback as I could, and I feel this is a fairly viable solution in the short term. Would love to hear feedback on potential blockers. Our next steps involve focusing on clarifying some parameters, like time between commitments, complexity in the operation of validator code, complexity of proofing the current instruction to run, instantiating the EVM state, and more.

Thanks [@jdkanani](/u/jdkanani), [@johba](/u/johba), [@federicobond](/u/federicobond) and others for reading earlier versions of this and gifting me your valuable input.

Some related posts: [SMART Plasma proposal](https://ethresear.ch/t/smart-plasma-proposal/2122), [Plasma checkpoint cost and block time](https://ethresear.ch/t/plasma-checkpoint-cost-and-block-time/2016), [A cryptoeconomic accumulator for state-minimised contracts](https://ethresear.ch/t/a-cryptoeconomic-accumulator-for-state-minimised-contracts/385)

## Replies

**josojo** (2018-06-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/esteban/48/1386_2.png) esteban:

> With a certain frequency (to be parametrized), the operator submits to the blockchain the root hash of a Merkle tree with all the block headers since the last checkpoint,

![](https://ethresear.ch/user_avatar/ethresear.ch/esteban/48/1386_2.png) esteban:

> This is not so much a scalability problem, as blocks in the sidechain could have 1 tx per block.

What happens when the complete preimage of all blocks and block headers are not available? Then all blocks would be needed to put on the main chain, right?

I feel like you are running here exactly in the problem of the data-unavailability. The validators claiming data unavailability, are causing a huge cost and require the operator to dump a lot of data in the blockchain. If then the data turns out to be valid, one can not slash the validator, who claimed data unavailability, since the data might have been unavailable before. This is basically the dilemma. See also [here](https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding)

---

**esteban** (2018-06-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> Then all blocks would be needed to put on the main chain, right?

Yes, but only using up gas for transaction bytes, no need to store them completely (you can retrieve the transaction and extract the data from there). There’s a mempool limit of 32kb for transactions, so the limit for block sizes would be around there

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> I feel like you are running here exactly in the problem of the data-unavailability. […] This is basically the dilemma. See also here

Thanks for the link! I’m currently inclined towards adding a cost to challenge withholding, protecting the operator (hence, edging towards “surviving altruistic fishers”) because the alternative (allowing the operator to grief the users) in the long term would go side-by-side with users detecting this behavior and abandoning the chain.

---

**kfichter** (2018-06-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/esteban/48/1386_2.png) esteban:

> Blocks on the sidechain would be limited in terms of size to whatever can be sent as data of a transaction in the root chain, accounting for the cost of hashing and verifying the hash. This is not so much a scalability problem, as blocks in the sidechain could have 1 tx per block.

This is problematic if I withhold very many blocks at the same time. Plus, the challenger necessarily has to pay for the operator’s gas. The operator can grief validators by occasionally withholding blocks and forcing validators to request block pre-images.

![](https://ethresear.ch/user_avatar/ethresear.ch/esteban/48/1386_2.png) esteban:

> Alice sends her sidechain-ETH to the contract B. The deposit gets burned.
> Once the challenge period for withholding and other checks has elapsed, Alice can show proof of the burn in the sidechain to the contract in the mainchain and retrieve her ETH.

The “burn-withdrawal” mechanism is unsafe if there’s no challenge period. The operator can simply (in a single transaction) (1) submit an invalid block that includes an “out of nowhere transaction” (2) submit a proof of burn and (3) submit a withdrawal that instantly steals money from the contract.

![](https://ethresear.ch/user_avatar/ethresear.ch/esteban/48/1386_2.png) esteban:

> I’ve been trying to get as much feedback as I could, and I feel this is a fairly viable solution in the short term. Would love to hear feedback on potential blockers.

Things to think about:

- EVM Plasma means that we need to assign each object some “owner” - who gets the money if a contract on the EVM chain holds funds and the chain stops?
- Users can grief if they’re expecting to lose money. If we’re playing Tic Tac Toe and your next move will cause me to lose money, then I can just refuse to go to the next state and claim that I never got the state update (exit).

---

**esteban** (2018-06-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> The “burn-withdrawal” mechanism is unsafe if there’s no challenge period.

That’s why I stated “Once the challenge period for withholding and other checks has elapsed” – “other checks” means no invalid blocks (which I think might be in the order of a few days since truebit verification requires patience). So between point (1) and (2) that you stated, there’s a significant amount of time that needs to elapse

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> EVM Plasma means that we need to assign each object some “owner”

Object as in plasma’s utxos? Say I have any token, I send it to a plasmabits-aware contract, that will hold it for me. If the chain halts, given that the contract is plasmabits-aware, I can tell the contract to give it back, providing a patricia tree proof of storage state from the last valid block of the plasmabit chain.

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> Users can grief if they’re expecting to lose money. If we’re playing Tic Tac Toe and your next move will cause me to lose money, then I can just refuse to go to the next state and claim that I never got the state update (exit).

After the problems with grieving and withholding (which is the weakest part – I’m working on it), any exit from the sidechain would be considered safe, because effectively we’re checkpointing the sidechain after the challenge periods. Given that there’s a commitment on the main chain to the state hash of the sidechain, the main chain to do any arbitrary state lookup on the last valid sidechain block, halted or not. Perhaps I shouldn’t call this  plasma, just a regular sidechain?

---

**kfichter** (2018-06-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/esteban/48/1386_2.png) esteban:

> If the chain halts, given that the contract is plasmabits-aware, I can tell the contract to give it back, providing a patricia tree proof of storage state from the last valid block of the plasmabit chain.

I think the problems are more when it’s not easy for funds to be retrieved. For a simple example, imagine that you have a Plasma contract that locks funds for 1 year. If we allow the operator to exit invalid funds after 2 weeks, then the lock is problematic. The best solution I’ve seen so far is to exit a state root and funds to a contract, and then allow users to piece together the entire state over time.

I’m still generally unsure about chain halting mechanisms. There’s a large cost to challenge each withheld block. I just did the math, for 10k txs/block @ 500 bytes/tx and 2 gwei gas price it’s about 32m gas = 300 USD to publish the entire block to calldata. So it’ll require multiple Ethereum blocks to publish. Given that the operator can withhold a valid block, validators will have to cover this cost. We could add a rule that the operator can’t publish any blocks while there’s a challenge, but then I could continuously grief and block the chain at a cost of $300/block.

---

**esteban** (2018-06-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> The best solution I’ve seen so far is to exit a state root and funds to a contract, and then allow users to piece together the entire state over time.

Not sure how this is different from what I’m suggesting, am I missing something? If I have a contract in the sidechain that is holding funds, and the chain halts, I won’t be able to retrieve those funds through a simple exit (because the exit needs a log of the burn from the sidechain). Unless they entered the chain through some “funds-freezing-aware” contract. In pseudo code, it’d look somewhat like this:

```auto
recover(frozenLogProof, amount, time):
  require(sidechain.state == HALT);
  require(validFrozenBalanceProof(frozenLogProof, amount, time, msg.sender));
  require(now > time);
  msg.sender.transfer(amount);

exit(burnLogProof, amount, height):
  require(validBurn(height, burnLogProof, amount, msg.sender);
  require(sidechain.height > height + CHALLENGE_PERIOD || sidechain.state == HALT);
  msg.sender.transfer(amount);
```

Note that `recover` can be called at any time after the sidechain halted. But indeed it’s not easy to retrieve any kind of state and every case must be well coordinated – every sidechain contract must have its logic to handle these cases themselves.

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> I just did the math, for 10k txs/block @ 500 bytes/tx and 2 gwei gas price it’s about 32m gas = 300 USD to publish the entire block to calldata.

I’d reach a blocker before, as there’s a soft limit of 32kb per tx (not a consensus rule – but mempools won’t accept more) so that’s a hard cap for each block of the sidechain. Multiple blocks can be merkelized (yet that adds another withholding dimention).

I’m inclined towards adding a large bond to withholding challenges. That can be used to incentivize other participants to respond to the challenges (which could have some eclipse attack problems) and in case the operator is really not broadcasting any more blocks but submitting them, the sum of all bonds it took to halt the chain could be recovered by the challenger(s) (eventually the operator will run out of money or fail to answer a challenge).

If the operator is not withholding, the bond needs to be large enough so the grieving is enough to cover cost + risk, and other validators might answer invalid challenges to earn a portion of its bond. A time extension after an unsuccessful withhold challenge might make sense but adds some unconfortable complexity. I feel I need to think more about this part, thanks a lot for the feedback!

---

**Dapploper** (2018-07-30):

Do you have any code to implement this idea proposal?

---

**esteban** (2018-08-20):

Hey [@Dapploper](/u/dapploper), not at the moment. We’ll probably add some kind of proof of stake to try and solve the withholding, but first we want to reduce uncertainty on EVM running on the EVM. We’re working with Parsec labs to build it:


      [github.com](https://github.com/leapdao/solEVM-enforcer/blob/master/docs/Architecture.md)




####

```md
# EVM Fraud Proof Architecture

The work builds on [solEVM](https://github.com/Ohalo-Ltd/solevm), an EVM runtime written in Solidity. This document will describe how the Solidy EVM Runtime can be extended to provide the 3 function that are necessary to do on-chain computation verification:

1. Run a program and export state at specific step (number of instructions executed).
2. Initiate the VM at any specific step with state exported in 1.
3. Once initiated as in 2., run the next OP-code and export state again as in 1.

These 3 functions together will allow to run any EVM code step by step, while producing the same results as a continuous run of an EVM. We will compress the exported state of the EVM through a deterministic hashing function. This hash will give us the follow two abilities:

- Ability to compare state of EVM at different states of the binary search (Truebit protocol)
- Ability to verify that EVM has been set up with correct parameters in state 2

## Execution Modes

We distinguish two modes of operation for the implementation we create:

**Off-chain Mode** - This mode is used to initiate the VM with a computation task and instruct it to run until a specific instruction count. The VM should then stop and export the state (function 1. above). For this mode the VM can be invoked with a static call.

```

  This file has been truncated. [show original](https://github.com/leapdao/solEVM-enforcer/blob/master/docs/Architecture.md)









      ![image](https://github.githubassets.com/favicon.ico)
      [GitHub](https://github.com/leapdao/solEVM-enforcer/issues)


    ![image](https://repository-images.githubusercontent.com/137391346/f6fb6500-6c1e-11e9-9334-2e3426ae00a1)

###

Partial implementation of the Ethereum runtime in Solidity (PoC) - leapdao/solEVM-enforcer

---

**u2** (2019-02-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/esteban/48/1386_2.png) esteban:

> If the block with the burn is withheld, and the operator fails to show proof of it in the mainchain, then the sidechain will halt,

How does the mainchain distinguish whether the sidechain is withheld? It’s a dilemma.

![](https://ethresear.ch/user_avatar/ethresear.ch/esteban/48/1386_2.png) esteban:

> Alice shows proof of the world state in the sidechain at the block when the sidechain halted.

If Alice shows the history world state, not the latest state, she can steal the assert.

