---
source: ethresearch
topic_id: 7114
title: Atomic Cross Shard Function Calls using System Events, Live Parameter Checking, & Contract Locking
author: drinkcoffee
date: "2020-03-14"
category: Sharded Execution
tags: [cross-shard]
url: https://ethresear.ch/t/atomic-cross-shard-function-calls-using-system-events-live-parameter-checking-contract-locking/7114
views: 5534
likes: 17
posts_count: 14
---

# Atomic Cross Shard Function Calls using System Events, Live Parameter Checking, & Contract Locking

The following has been released early to allow for open and collaborative research. Please tell me if you find issues with this or if you have ideas on how to improve the proposal.

# 1. Introduction

Application developers need to be able to create programs on the Ethereum 2 platform that have contracts on different shards in different execution environments. The application developers need to be able to use the synchronous atomic composable programming techniques that they are accustomed to using with the Ethereum 1 platform. This post proposes a technique that could allow for this.

In the diagram below, for example, a Cross Shard call is used to get the value of an oracle. If the value returned is below a certain amount, then a Cross Shard call is used to buy a commodity.

[![Example Cross Shard Function Call](https://ethresear.ch/uploads/default/optimized/2X/d/d9c62395c2ad2a714a3d491da52565232f1aeacd_2_690x318.png)Example Cross Shard Function Call2654×1224 319 KB](https://ethresear.ch/uploads/default/d9c62395c2ad2a714a3d491da52565232f1aeacd)

The technology described herein leverages many of the ideas from Atomic Crosschain Transactions (see [Atomic Crosschain Transactions White Paper](https://github.com/PegaSysEng/sidechains-samples/blob/a4d73c17cb672649ec8cc3c69d53be69cc8f9dcf/AtomicCrosschainTransactions-WhitePaper.pdf) ).

This Cross Shard Transaction technology relies on the following functionality being added to Execution Environments (EE):

- System Event messages that are added to transaction receipts, that can be referenced from other EEs on other shards via Beacon Chain Crosslinks. In an EE, when the function call that is the target of a transaction ends, the EE produces a System Event message. System Event messages are different from application event messages that could be produced by contract code. Contract code can not produce events that forge System Event messages.
- Live parameter checking: when contract code calls makes a cross shard function call, check that the actual shard, EE, contract, function and parameters match those that are expected to be called.
- Contract lockability: When contracts are deployed they need to be specified as able to be locked (lockable) or not able to be locked (nonlockable). When a Transaction Segment executes, any contract that has a state update needs to be locked. If a contract was deployed as nonlockable, then it can not be locked and the transaction fails.
- Provisional state storage and contract locking: when a contract is updated as part of a Cross Shard transaction, its updated state is stored in provisional storage and the contract is locked. If the Cross Shard transaction is committed, the provisional state replaces the contract state and the contract is unlocked. If the Cross Shard transaction is ignored, the provisional state is discarded and the contract is unlocked.
- New Transaction Types: The EE needs to support the transaction types described later in this proposal.

# 2. Example

The best way of understanding this technology is to work through an example. Imagine the call graph shown below. The Segment Transactions with (no updates) written below them are function calls that read state and return a value. The Segment Transactions with (updates) written below them are function calls that write state and return a value.

[![Example Call Graph](https://ethresear.ch/uploads/default/optimized/2X/2/28052026320a82b07f3d080d92e50f6b6a09f04f_2_690x338.png)Example Call Graph2236×1098 241 KB](https://ethresear.ch/uploads/default/28052026320a82b07f3d080d92e50f6b6a09f04f)

The transactions to execute this complex Cross Shard Transaction are shown in the diagram below. In the diagram, blocks are represented by square boxes and transactions by rounded cornered boxes. The signed state root for Shard blocks for block number N-1 feed into Beacon Chain blocks for block number N and are known as Cross Links. The Cross Links for all Shard blocks in a Beacon Chain block for block number N are available for use by Shard blocks for block number N. The dashed lines indicate the submission of Cross Links into Beach Chain blocks from Shard blocks and their availability for use in Shard blocks from Beacon Chain blocks. The solid lines indicate transactions submitted by the application into transaction pools and then included into Shard blocks.

[![Example Transactions and Blocks](https://ethresear.ch/uploads/default/optimized/2X/4/419657f530ff60b7451983c1b27b7a24d6e55f71_2_690x370.jpeg)Example Transations and Blocks2690×1446 539 KB](https://ethresear.ch/uploads/default/419657f530ff60b7451983c1b27b7a24d6e55f71)

Walking through the processing:

- The application submits the Start transaction to Shard 1. This reserves the Cross Shard Transaction Id for the Cross Shard Transaction and specifies the call graph of the Root Transaction and Transaction Segments that will make up the Cross Shard Transaction.
- The application submits leaf Transaction Segments to Shard 3, 5, 6, and 7. The transactions execute function calls that could update state and could return a value. The EEs that execute the transactions emit System Events that include information about the transaction call and function call, including the error status and return result. For the purposes of the example, assume that only Shard 7 has any state updates.
- The application waits for a Beacon Chain block to be produced that includes a Cross Link for the Shard block that includes the submitted transactions.
- The application submits a Transaction Segment to Shard 2 to execute a function call. The transaction includes the System Event information from the transactions that executed on Shard 3 and 5 and Merkle Proofs showing that information relates to transactions that are parts of blocks that executed on the shards. The Merkle Root can be compared with the Cross Link in the Beacon Block for the shard. For the purposes of this example, assume that the transaction on Shard 2 causes no state updates.
- In parallel with submitting the Transaction Segment to Shard 2, the application submits a Transaction Segment to Shard 4 to execute a function call. The transaction includes the System Event information and Merkle Proofs for the transactions that executed on shard 6 and shard 7. For the purposes of this example, assume that this transaction causes state updates on Shard 4.
- The application waits for a Beacon Chain block to be produced that includes a Cross Link for the Shard block that includes the submitted transactions.
- The application submits the Root Transaction, along with System Event information and Merkle Proofs for the Transaction Segments on Shard 2 and 4. System Event information is emitted that indicates the entire Cross Shard Transaction should be committed.
- The application waits for a Beacon Chain block to be produced that includes a Cross Link for the Shard block that includes the submitted transactions.
- The application submits Signalling transactions on Shard 4 and 7 to unlock the contracts on Shard 4 and 7.
- The application submits a Clean transaction on Shard 1 to remove the Cross Shard Transaction Id from the list of outstanding unique ids.

# 3. Transaction Types

Cross Shard Transactions consist of multiple transaction types.

## 3.1 Start Transaction

Start transactions indicate the start of a Cross Shard Transaction. This transaction is used to reserve a per-shard and per-EE “unique” Cross Shard Transaction Id, and to register the overall call graph of Root Transaction and Transaction Segments.

Transaction fields include:

- Cross Shard Transaction Id
- Time-out block number.
- Root Transaction information (shard, EE, function call & parameters).
- For each Transaction Segment called from the code executed as a result of this transaction:

Log message with Shard, EE, Contract Address, Function Name, Parameter Values of function called
- Return result
- Whether there was a state update and the transaction has resulted in a locked contract.
- Merkle Proof to a specified block to a crosslink.
- Note that the list of transactions must be in the order that the functions are expected to be called.

Transaction processing:

1. Fail if the Cross Shard Transaction Id is in use.
2. Check that the time-out block number is a suitable value.
3. Register the Cross Shard Transaction Id
4. Emit a Start System Event containing:

Tx Origin / Msg Sender: The account that signed the transaction.
5. Cross Shard Transaction Id
6. Hierarchical call graph of cross shard function calls / Transaction Segments starting at the Root Transaction. For each call include:

Shard
7. EE
8. Contract address
9. Data: Function name and Parameters

## 3.2 Root Transaction

The Root Transaction contains the function call that is the entry point for the overall call graph of the Cross Shard transaction. This transaction type indicates that the code should execute as per a normal Transaction Segment (see below), and all locked contracts on all shards should be committed or ignored. If the transaction completes successfully prior to the time-out block, all state updates as a result of all Transaction Segments that are part of the Cross Shard Transaction should be committed. If any of the Transaction Segments have failed, or if the transaction is submitted after the time-out, then all Transaction Segment updates should be discarded.

Transaction fields include:

- Cross Shard Transaction Id
- Shard, EE, Contract, Function and Parameters to be called.
- Start Transaction Log message & Merkle Proof (note: includes time-out block number)
- For each Transaction Segment called from the code executed as a result of this transaction:

Log message with Shard, EE, Contract Address, Function Name, Parameter Values of function called
- Return result
- Whether there was a state update and the transaction has resulted in a locked contract.
- Merkle Proof to a specified block to a crosslink.
- Note that the list of transactions must be in the order that the functions are expected to be called.

Transaction processing:

1. Verify the log information for the Start Transaction and each Transaction Segment, checking the Merkle proof up to the Shard Crosslink.
2. If the block number is after the timeout, or if any of the Transaction Segment logs indicate an error, emit a System Event indicating the entire Cross Shard Transaction should be aborted.
3. Check that the transaction has been submitted by the same entity as is indicated by the Start Transaction Log.
4. Execute the code, using cached return values for the Transaction Segments.

Note: only lockable contracts can have state changes.
5. Check that the Transaction Segments called by the code matches what was expected to be called in the Start Transaction Log.
6. The state updates are committed.
7. When the entry point function call for this shard completes, emit a System Event Message. This includes:

Tx Origin / Msg Sender: The account that signed the transaction.
8. Cross Shard Transaction Id.
9. Contract address.
10. Data: Function name and parameter values specified in the transaction.
11. Indication if the transaction was successful or if an error was thrown.
12. If an error is indicated: Some error code.
13. If success:

List of addresses of locked contracts.
14. The return value of the function call.
15. Note: the shard id and EE id do not need to be included as they will be implied by the Merkle Tree required to prove the log message is valid.

## 3.3 Transaction Segments

These transactions execute on shards to run function calls. They may update state and / or return function values. The code may call one or more functions that may return values from a different shard and may update state on a different shard. These are nested Transaction Segments.

Transaction fields include:

- Cross Shard Transaction Id
- Shard, EE, Contract, Function and Parameters to be called.
- Start Transaction Log message & Merkle Proof connecting the log message to the cross link (note: includes time-out block number).
- Depth and offset within the call graph specified in the Start Transaction Event message.
- For each Transaction Segment called from the code executed as a result of this transaction:

Log message with Shard, EE, Contract Address, Function Name, Parameter Values of function called
- Return result
- Whether there was a state update and the transaction has resulted in a locked contract.
- Merkle Proof to a specified block to a crosslink.
- Note that the list of transactions must be in the order that the functions are expected to be called.

Transaction processing:

1. Verify the log information for the Start Transaction and each Transaction Segment, checking the Merkle proof up to the Shard Crosslink.
2. If the block number is after the timeout, or if any of the Transaction Segment logs indicate an error, emit a System Event indicating an error.
3. Check that the transaction has been submitted by the same entity as is indicated by the Start Transaction Log.
4. Verify that the call graph from the Start Transaction Event matches the Transaction Segment calls that were passed in.
5. Execute the code, using cached return values for the Transaction Segments.

Note: only lockable contracts can have state changes.
6. Check that the Transaction Segments called by the code matches what was expected to be called in the Start Transaction Log.
7. The state updates are put into provisional storage and the contracts are locked.
8. When the entry point function call for this shard completes, emit a System Event Message that is the same as the one described for the Root Transaction.

## 3.4 Signalling Transactions

These transactions are used to unlock a contract locked by a Transaction Segments.

This transaction includes:

- Root transaction log information and Merkle Proofs showing the Root Transaction has completed successfully or has failed / timed-out.
- Transaction Segment for this shard log and Merkle Proof, showing which contracts were locked.

Transaction processing:

1. If the Root transaction log indicates “Commit”, apply the provisional updates and unlock the contracts
2. If the Root transaction log indicates “Ignore”, discard provisional updates and unlock the contracts.

These transactions should be either free, or perhaps even an incentive should be paid to ensure participants submit this transaction when there was a failure / if the entity that locked the contract stops participating. Invalid Signalling transactions should penalise users. The penalty should not be onerous, as invalid Signalling transactions may occur as a result of Beacon Chain reorganisations.

## 3.5 Clean Transaction

Removes the unique id from the list of outstanding unique ids.

The transaction fields include:

- Start transaction log and proof (indicating the call graph of Cross Shard Transactions),
- Root Transaction log and proof
- Transaction Segments logs and Merkle Proofs (indicating which if any contracts were locked),
- Signalling Transactions logs and Merkle Proofs (indicating that the appropriate Signalling Transactions were called).

Valid Clean transactions should be incentivized to ensure participants submitted this transaction. However, invalid Clean transactions should penalise users. The penalty should not be onerous, as invalid Clean transactions may occur as a result of Beacon Chain reorganisations.

## 3.6 Other Transactions

In addition to the transaction types described above, other transactions that the EE needs to support are:

- Deploy a lockable contract.
- Deploy a nonlockable contract.
- For certain scenarios it might be possible to create specialised transaction types that remove the need for the Start and Clean transactions. For instance, if there is a Root Transaction and a single Transaction Segment that executes a cross shard read and does not update state, it might be possible to create a specialised Root Transaction that does not require the Start and Clean transactions. This is currently being considered further.

# 4. Cross Shard Processing

To do a Cross Shard Transaction, the application would do the following. Note that, the user’s application does not do much, and most of the complexity would be handled by a library wrapper, like Web3J.

1. Determine call graph and parameter values for transactions using dynamic program analysis (code simulation).
2. Submit the Start Transaction. This could be done in parallel with the next step, or this could be done in one slot prior to the next step.
3. Submit leaf Transaction Segments. A “leaf” transaction is a transaction who’s function calls do not call other cross-shard functions.
4. Wait a block for cross links to be published.
5. Submit Transaction Segments that contain functions that call other Transaction Segments. Repeat for each “layer” of nested transactions.
6. Wait a block for cross links to be published.
7. Submit the Root Transaction
8. Wait a block for cross links to be published.
9. Submit all Signalling transactions on all Shards on which Transaction Segments were executed that updated state.

# 5. Live Parameter Checking

Live parameter checking is used to ensure that as contract code executes, the actual value of parameters passed into cross shard function calls matches the parameter values that are in the signed Transaction Segments. Recall that the parameter values for Transaction Segments are published in System Events when the transactions execute, and that the application feeds this information into the Transaction Segments or Root Transactions that call the functions that they represent. This means that the EE has access to the expected parameter values for cross shard function calls from Transaction Segments as the code executes.

The diagram below shows example contract code that calls a function on another shard that returns a value (sh2.ee2.conC.funcC()), and then, depending on the value of state1, might call a function on another shard that does not return a value (sh1.ee4.conD.funcD() ).

[![Live Parameter Checking](https://ethresear.ch/uploads/default/optimized/2X/b/bc464b19898cdce5ea2c9e0e438ea25620c54b6a_2_689x276.png)Live Parameter Checking2688×1078 186 KB](https://ethresear.ch/uploads/default/bc464b19898cdce5ea2c9e0e438ea25620c54b6a)

When an application is creating the Transaction Segments for the calls to funcC and funcD, it needs to simulate the code execution. For example, if _param1 is going to be 5, and state1 is 2 and state2 is 3, and funcC will return 10 given the parameter is 5, then Transaction Segments need to be created with parameter values 5 passed into funcB, 5 passed into funcC, and 13 passed into funcD. Note that if state1 was 1, then Transaction Segments would only be constructed for the call to funcB and funcC, as funcD would never be called.

## 6. Safety & Liveness

The following walks through a set of possible failure scenarios and describes how the scenario is handled.

## 6.1 Root Transaction Fails

If the Root Transaction fails for any reason, a System Event is created that indicates that all updates for all Transaction Segments should be discarded. Based on this System Event, Signalling Transactions can be used to unlock all contracts on all Shards in all EEs. The Root Transaction could fail because:

- The code in the Root Transaction could throw an error.
- The System Event messages passed into the Root Transaction may indicate that an error occurred with one of the Transaction Segments.
- The parameters that a cross shard function is called with do not match the parameter values in the System Event message for the Transaction Segment for the function call.
- The Root Transaction is submitted after the Cross Shard Transaction block time-out.

## 6.2 Transaction Segment Fails

If a Transaction Segment fails for any reason, a System Event is created that indicates that it failed. This System Event can be passed up to the Root Transaction to cause the entire Cross Shard Transaction to fail. A Transaction Segment could fail because:

- The code in the Transaction Segment could throw an error.
- The System Event messages passed into the Transaction Segment may indicate that an error occurred with one of the subordinate Transaction Segments.
- The parameters that a cross shard function is called with do not match the parameter values in the System Event message for the Transaction Segment for the function call.
- The Transaction Segment is submitted after the Cross Shard Transaction block time-out.

## 6.3 Invalid Merkle Proof or Invalid System Event

The application could submit an invalid Merkle Proof or an invalid System Event message such that the hashing of the System Event message combined with the Merkle Proof does not yield a Merkle Root that matches the Cross Link’s state root. In this case, the transaction in question would fail.

## 6.4 Application does not submit a Transaction Segment

The application could see that a subordinate Transaction Segment has failed, and decide to not submit any further Transaction Segments, the Root Transaction, or Signalling Transactions. To address this, another user could wait for the Cross Shard Transaction to time-out, and submit a Root Transaction to fail the overall Cross Shard Transaction (this would be free), and submit Signalling Transactions (would reward the caller) and the Clean Transaction (would reward the caller) to unlock all locked contracts and remove the Cross Shard Transaction Id.

## 6.5 Application does not submit a Root Transaction

The application could see that a subordinate Transaction Segment has failed, and decide to not submit the Root Transaction, or Signalling Transactions. To address this, another user could wait for the Cross Shard Transaction to time-out, and submit a Root Transaction to fail the overall Cross Shard Transaction (this would be free), and submit Signalling Transactions (would reward the caller) and the Clean Transaction (would reward the caller) to unlock all locked contracts and remove the Cross Shard Transaction Id.

## 6.6 Replay Attacks

The Root Transaction and Transaction Segments are tied to the account used to sign the Start Transaction, except in failure cases when the Cross Shard time-out has expired. The transactions for the account will have an account nonce, that will prevent replay. Other users that try to replay Root Transaction and Transaction Segments will fail as they will not be able to sign the transactions with the private key that signed the Start Transaction.

## 6.7 Denial of Service (DOS) Attacks

An attacker could submit Clean transactions that include correct data, with a single incorrect Merkle Proofs. The attacker could submit the transaction repeatedly in an attempt to cause lots of processing to occur on the Ethereum Clients. A large call graph would result in the Ethereum Clients needing to process many Merkle Proofs. This behaviour is discouraged by penalising invalid Clean transactions. Additionally, any user could receive a small reward for submitting a valid Clean transaction.

## 6.8 Beacon Chain Forks

If the Beacon Chain forks, transactions for shard blocks on all shards will need to be replayed, based on the revised Cross Links. Some of the replayed transactions might expect Cross Links that no longer exist, and hence rather than passing, these transactions will fail. In this scenario, the Cross Shard Transaction would fail and the provisional state for any state updates would be discarded.

## 6.9 Finality

The Cross Shard Transaction would be final once the Checkpoint after the last Signalling Transaction has been finalised. This is usually the first beacon block in an epoch. Once a Checkpoint is final, all prior blocks are final, and implicitly all prior Cross Links will be final, and hence all Shard blocks will be final.

# 7. Hotel Train Example (including ERC20)

The Hotel and Train problem is an example of a scenario involving a travel agent that needs to ensure the atomicity of a complex multi-contract transaction that crosses three shards. The travel agent needs to ensure that they either book both the hotel room and the train seat, or neither, so that they avoid the situation where a hotel room is successfully booked but the train reservation fails, or vice versa. Additionally, payment via ERC 20 tokens needs to only occur if the reservations are made. A final requirement is that the transactions need to occur in such a way that other users can book hotel rooms and train seats, and pay for them, simultaneously.

Imagine there are three shards involved: the travel agency operates on Shard 1, the hotel on Shard 3 and the train on Shard 4. Also have a second travel agency that operates on Shard 2. This is shown diagrammatically below.

[![Hotel Train Example](https://ethresear.ch/uploads/default/optimized/2X/a/ac48e5515da9ef235b21f6338fb51a5a5318be85_2_690x380.png)Hotel Train Example2648×1462 455 KB](https://ethresear.ch/uploads/default/ac48e5515da9ef235b21f6338fb51a5a5318be85)

The hotel is represented as a nonlockable router contract and multiple lockable hotel room contracts. The hotel issues ERC 20 tokens for travel agencies to pay for hotel rooms. The ERC 20 contract consists of a router contract and one or more payment slot contracts for each account.  Similarly, the train is represented by a nonlockable router contract and mutiple lockable train seat contracts.

To book a room, the travel agency creates cross shard function calls (Transaction Segments) that book a hotel room and a train seat and pay for them. The Hotel Router contract works by finding an appropriate room that is available on the requested day that is not currently booked, and then booking the room. When searching for a room, the code skips room contracts that are currently locked. Similarly, when paying for a room, the ERC router contract needs to transfer money from the travel agency’s account to the hotel’s account. It does this by finding a payment slot contract for the hotel that is not locked and paying into that.

Given the ability to determine programmatically which contracts are locked, and thus avoid them, the hotel, train, and ERC 20 contracts can be written such that both travel agencies can simultaneously execute bookings without encountering a locked contract.

# 8. Other Considerations

Account Nonces: Account nonces are deemed to be outside lockable state. As such, when an account submits a transaction, and the transaction nonce value increases, the account does not get locked.

Ether Transfer: Currently, this scheme is just focused on function calls. Ether transfer between shards may be possible with this technique. It just has not been considered yet.

Pay for Gas on All Shards: It would be great if a user could have Ether on one shard, and use it to pay for gas on all of the shards that the Cross Shard Transaction executes on. This technique ca not do that at present. Perhaps when Ether Transfer is resolved, this will be possible.

Transaction size: Transactions in this proposal often include multiple Merkle Proofs and other data. The probable effects on transaction size need to be analysed.

Ethereum 1.x: Assuming Ethereum 1.x is in an EE on a shard, all existing contracts could be marked as nonlockable. The EE could support the features described in this post. Additional EVM opcodes could be added to allow cross shard function calls.

Application code: I hear you say, “There sounds like a lot of complexity in the application. Wasn’t this technique supposed to make application development simpler?” The answer to this is that the vast majority of the complexity will be absorbed into libraries such as Web3J. Contract code and other application code should be straight forward.

# 9. Acknowledgements

This research has been undertaken whilst I have been employed full-time at ConsenSys. I acknowledge the support of University of Queensland where I am completing my PhD, and in particular the support of my PhD supervisor Dr Marius Portmann.

I acknowledge the co-authors of the [original Atomic Crosschain Transaction paper](https://arxiv.org/abs/1904.12079) and the co-authors of the [Atomic Crosschain Transaction white paper](https://github.com/PegaSysEng/sidechains-samples/blob/a4d73c17cb672649ec8cc3c69d53be69cc8f9dcf/AtomicCrosschainTransactions-WhitePaper.pdf) [@Raghavendra-PegaSys](/u/raghavendra-pegasys) (Dr Raghavendra Ramesh), Dr Sandra Johnson, John Brainard, Dr David Hyland-Wood and Roberto Saltini for their help creating the technology upon which this post is based. I thank @cat (Dr Catherine Jones) for reviewing this paper and providing astute feedback. I thank [@benjaminion](/u/benjaminion) (Ben Edgington) for answering lots of questions about Eth2.

## Replies

**poemm** (2020-03-16):

Thank you for this! Very useful to see the diagrams!

The events/locks may need a way to deal with race conditions between shards.

At tx signing-time, the signer must know the call graph – what is called, the order in which things are called, arguments, and the outcome of each call. In Eth1, these may be undecidable at tx signing-time, so this design is less expressive than Eth1, but it is expressive enough for many use cases!

Runtime requirements may not be met. For example, a lock can be quickly obtained by an attacker before another tx gets it. A commit may not happen before the time-out because the shard is overwhelmed by an ICO or a DoS attack.

Lots of transactions are needed, including extra transactions to coordinate locks and commits. These transactions add many merkle proofs to each stateless block, adding to the block size bottleneck. Moreover, each validator must monitor system events. So this may have similar throughput to Eth1, which is OK.

In 6.5 and 6.7, perhaps people could just wait for the time-out to unlock everything. Economics (free transaction, reward the caller) enable subtle attacks. Penalties may require a whole system of deposits, which may introduce new complexity and attacks. It may be wise to avoid economic mechanisms unless there is no other option.

What is the minimal protocol needed to do something like this? Can events/locks be done at the contract-level instead of the protocol-level, at the cost of extra txs to lock things? Please note that there is a push to have a minimal protocol, so proposals like this need compelling evidence that it is a good option at the protocol-level.

Does anyone plan to prototype this?

Again, thank you for this major effort!

---

**drinkcoffee** (2020-03-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/poemm/48/2402_2.png) poemm:

> The events/locks may need a way to deal with race conditions between shards.

The locking model at moment is for a simple “fail if already locked”. As such, no dead locks are possible, but live lock is possible.

Live lock would be where you have four contracts, A, B, C, and D, each on different shards. Transaction 1 needs to lock A, B, and C. Transaction 2 needs to lock B, C, and D. The Transaction 1 starts and gains locks on A and B; in parallel Transaction 2 starts and gains locks on D and C. When Transaction 1 tries to get a lock on C it fails. When Transaction 2 tries to get a lock on B it fails. The applications behind Transaction 1 and Transaction 2 retry, fail, and retry and fail repeatedly.

Is this what you mean by “race conditions between shards”?

---

**drinkcoffee** (2020-03-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/poemm/48/2402_2.png) poemm:

> Runtime requirements may not be met. For example, a lock can be quickly obtained by an attacker before another tx gets it. A commit may not happen before the time-out because the shard is overwhelmed by an ICO or a DoS attack.

Good points.

Contracts can have permissioning, in a similar way to how things work with Eth 1 (require(msg.sender == approvedAddress). I wrote a paper which discussed application authentication for cross-blockchain calls. This is for the Atomic Crosschain Transaction technology. I expect a lot of the ideas to feed through into this technology. The paper is here: [[1911.08083] Application Level Authentication for Ethereum Private Blockchain Atomic Crosschain Transactions](https://arxiv.org/abs/1911.08083)

In addition to the application authentication, contracts such as the hotel or train contract can be designed so that an attacker would need to have ERC 20 tokens to book an item, and hence cause a state update and cause a contract to be locked.

What you say about DOS attacks or just very high transaction volume is true. If you were trying to do a cross shard call during a time of high transaction volume, increasing the time-out would be good. However, the longer the time-out, the longer contracts might be locked, with the updates later discarded. I think we will need to do some modelling on this.

---

**drinkcoffee** (2020-03-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/poemm/48/2402_2.png) poemm:

> Lots of transactions are needed, including extra transactions to coordinate locks and commits. These transactions add many merkle proofs to each stateless block, adding to the block size bottleneck. Moreover, each validator must monitor system events. So this may have similar throughput to Eth1, which is OK.

I think we will need to do some modelling to work out how much the technique affects transaction size, and in turn block size.

For a common use-case: State Update on a Shard with a Read from another Shard. I think this can be done using just two transactions, one Transaction Segment for the Read and one specialised Root Transaction.

The validators do not need to monitor system events. The application gathers the system events and submits them, along with Merkle Proofs, in the transaction. The validators will need to verify the Merkle Proofs against the Cross Link.

---

**drinkcoffee** (2020-03-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/poemm/48/2402_2.png) poemm:

> What is the minimal protocol needed to do something like this? Can events/locks be done at the contract-level instead of the protocol-level, at the cost of extra txs to lock things? Please note that there is a push to have a minimal protocol, so proposals like this need compelling evidence that it is a good option at the protocol-level.
>
>
> Does anyone plan to prototype this?

The current design needs no changes at the Beacon chain level. It needs the things described at the top of the post to any EE that wanted to support the technology. Most of the complexity is moved to the library that the application uses to communicate with Ethereum nodes.

It might be possible to do this at the contract layer. I think having an atomic cross shard function call mechanism as part of the EE is important.

We are in discussions within PegaSys about whether we should prototype this. We have an existing PoC of the Atomic Crosschain Transaction technology.

Sample code and scripts: [GitHub - Consensys/sidechains-samples: Sample code for Atomic Crosschain Transactions](https://github.com/PegaSysEng/sidechains-samples)

Modified Hyperledger Besu: [GitHub - Consensys/sidechains-besu: An enterprise-grade Java-based, Apache 2.0 licensed Ethereum client](https://github.com/PegaSysEng/sidechains-besu)

Modified Web3J for generating code wrappers: [GitHub - Consensys/sidechains-web3j: Lightweight Java and Android library for integration with Ethereum clients](https://github.com/PegaSysEng/sidechains-web3j)

The sample code repo includes our PoC version of the Hotel Train problem using Atomic Crosschain Transactions. A video of me running through the demo is here:

  [![image](https://ethresear.ch/uploads/default/original/3X/3/4/34a7204e0028e975ceb9a63a8e1ddfbbfc65c3c2.jpeg)](https://www.youtube.com/watch?v=5ASxwvTdKDM&t=4s)

This talk describes the Atomic Crosschain Transactions and the application level authentication: https://www.youtube.com/watch?v=MrrUHC-d6lc

---

**drinkcoffee** (2020-03-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/drinkcoffee/48/2326_2.png) drinkcoffee:

> Log message with Shard, EE, Contract Address, Function Name, Parameter Values of function called
> Return result
> Whether there was a state update and the transaction has resulted in a locked contract.
> Merkle Proof to a specified block to a crosslink.

[@Raghavendra-PegaSys](/u/raghavendra-pegasys) pointed out that this is wrong. Sorry.

Rather than log messages, it should be information about what is expected to be called, the call graph: Shard, EE, Contract Address, Function Name, Parameter Values of function called

There is no Merkle Proof.

There is no “state update” or information about locking.

The purpose of the start message is to register intent.

---

**Raghavendra-PegaSys** (2020-03-17):

As with Atomic Crosschain Technology, we do have the limitation of contract-scale recursion. Meaning a contract cannot appear more than once in the cross-shard call-chain.

Suppose there are contracts A on shard 1, and B on shard 2. Then a call chain of the form: A.f( ) -> B.g( ) -> A.h( ) is not valid. Because by the time A.f( ) is called the contract A is already locked. This is true when A.h( ) is updating the state. However, if A.h( ) does not update state, the contract A is not locked, and A.f can be processed.

So, it may be fair to say that as long as the reads are done before the writes on the same contract, the call chain is valid.

It is valid to have a contract appearing more than once in an intra-shard call chain. Meaning recursions are allowed if contracts happen to be on the same shard. A call chain of the form A.f( ) —> C.k( ) —> A.h( ) —> B.g( ) is allowed, where A and C are deployed on the same shard, and B on a different shard. This is because the inter contract calls on a single shard is structured as a single transaction.

---

**hmijail** (2020-03-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/poemm/48/2402_2.png) poemm:

> At tx signing-time, the signer must know the call graph – what is called, the order in which things are called, arguments, and the outcome of each call. In Eth1, these may be undecidable at tx signing-time, so this design is less expressive than Eth1, but it is expressive enough for many use cases!

In our Eth1 PoC we do implement a code simulation step, as mentioned in 4.1. This allows the app to prepare and sign all the required Transaction Segments. It’s worth noting that even in Eth1 one should know the contracts one is calling, so the natural extension to a cross-shard transaction is knowing the call graph between contracts.

Having said that, we envision that the simulation step can be automated: for example with dynamic analysis of the contracts and their current state, or maybe with a “trial run” and a posterior commit step: the app sends the *proposed* function calls to the shards, who provisionally lock-in the resulting state, and respond to the app with the values that need to be signed in the final function calls to commit the state.

![](https://ethresear.ch/user_avatar/ethresear.ch/poemm/48/2402_2.png) poemm:

> Runtime requirements may not be met. For example, a lock can be quickly obtained by an attacker before another tx gets it. A commit may not happen before the time-out because the shard is overwhelmed by an ICO or a DoS attack.

I’d argue that that’s actually the expected behavior of locks. However, to disincentivize an attacker from securing locks arbitrarily, a cost can be added.

A better option might be to slightly evolve the locking mechanism to allow multiple transactions to happen at the same time, each with its own separate provisional state, and only commit the first one that completes (maybe including a gas bias). This gives semantics closer to current Eth1 and to [atomic instructions in “traditional” CPUs](https://en.wikipedia.org/wiki/Load-link/store-conditional).

These options were about implicit locking (again, not unlike Eth1). But yet another option would be to implement an explicit locking instruction, with an explicit cost. Probably too messy though…

---

**hmijail** (2020-03-20):

Summarizing what [@Raghavendra-PegaSys](/u/raghavendra-pegasys)  explained, our current model is (for the sake of PoC simplicity) akin to a traditional vanilla mutex: the owner of the mutex is blocked from acquiring the mutex again.

But we expect it would be easy to generalize to the case of recursive mutexes, which would allow any order of transactions, since any transaction would be able to reacquire locks transparently. This removes yet another burden from the application design.

---

**drinkcoffee** (2020-04-03):

In discussion with [@Raghavendra-PegaSys](/u/raghavendra-pegasys) we realised that there was an issue. In the scheme as described above, there is no way to determine if the Root transaction has already been processed. As such, the sender could submit a Root transaction prior to the time-out, and an attacker could submit a second Root transaction after the time-out. The attacker could then attempt to send Signalling transactions indicating the overall cross chain transaction had failed prior to the sender of the Root transaction, thus causing some shards to ignore and others to commit.

The solution is for the Root transaction to update some state related to the Cross Shard Transaction Id to indicate that the Root transaction has been processed. Doing this ensures that only one Root transaction is submitted, ensuring that the state for all shards will be consistent.

---

**drinkcoffee** (2020-06-07):

I have come up with a blockchain layer 2 approach for cross-shard that builds on the technique described in this post. A description of the technique, assuming it is for generic cross-blockchain is here: https://arxiv.org/abs/2005.09790 The simplification for cross-shard will be that the block header transfer is not needed as crosslinks can be used.

---

**Lunaticf** (2020-06-27):

I was wondering that if a contract deployed on a local blockchain, the contract will be locked so that only the cross-chain transaction can modify the state of the contract，all local blockchain transaction that update this contract can not be processed? which is a huge lock cost if the cross-chain transcation consume too much time to finish or fail，and all the local transaction will be discarded in this time gap.

I am thinking a optimistic lock-free concurrency control method to optimize this…

---

**drinkcoffee** (2020-06-27):

A cross-blockchain system which derives from the protocol described in this post is here: https://arxiv.org/abs/2005.09790

You are correct: when a contract is locked it can’t be used until it is unlocked due to commit/ignore/ignore due to time-out. Careful design segregating contract information will allow this locking to not have too big an impact. Have a look at the use-case section of the paper I have linked to above.

As you say, more complex locking could be used.

