---
source: ethresearch
topic_id: 16514
title: "PEPC-DVT: PEPC with no changes to the consensus protocol"
author: diego
date: "2023-08-31"
category: Economics
tags: []
url: https://ethresear.ch/t/pepc-dvt-pepc-with-no-changes-to-the-consensus-protocol/16514
views: 4315
likes: 19
posts_count: 10
---

# PEPC-DVT: PEPC with no changes to the consensus protocol

*Thanks to [Barnabé Monnot](https://twitter.com/barnabemonnot), [Xyn Sun](https://twitter.com/sxysun1), [Cairo](https://twitter.com/cairoeth), [Mike Neuder](https://twitter.com/mikeneuder), [William X](https://twitter.com/W_Y_X), [Pranav Garimidi](https://twitter.com/PGarimidi), and many others for insightful discussions throughout the development of this idea.*

**tl;dr**: I introduce a novel mechanism for enforcing proposer commitments in Ethereum without altering the existing consensus protocol.

##  Glossary

- PEPC-DVT: Stands for “Protocol-Enforced Proposer Commitments - Distributed Validator Technology.” This is a framework designed to ensure that block proposers in Ethereum fulfill specific commitments without requiring changes to the existing consensus algorithm.
- Validator: Refers to an entity, identified by a public key, that participates in Ethereum’s proof-of-stake consensus mechanism to validate transactions and create new blocks.
- Proposer: A specialized role within the set of Validators. A Proposer is a Validator chosen to create a new block for a specific time slot in the blockchain.
- Distributed Validator (DV): This is a collective of individuals or nodes that share the responsibilities of a single Validator. The Validator’s private key is divided among these participants using secret-sharing techniques, ensuring that no complete signature can be generated without approval from a majority of the group. The distributed validator client is the software that enables participation in a Distributed Validator setup.
- In-Protocol Commitments: These are a specific type of commitment that are directly related to the roles and responsibilities within the Ethereum protocol. An example is a commitment to propose a block with a certain attribute.

##  What problem does PEPC-DVT address?

### The Problem Scenario

Consider two parties, Alice and Bob, who wish to engage in a contractual agreement. Alice promises to include Bob’s transaction in the next block she proposes on Ethereum mainnet. Furthermore, she commits to placing it as the first transaction in that block. In return, Bob agrees to pay Alice, but only if she fulfills both conditions.

### The Shortcoming of Current Systems

When Alice’s turn comes to propose a block, she includes Bob’s transaction but fails to place it as the first transaction in the block. As a result, she violates her commitment and does not receive the payment from Bob. However, the Ethereum consensus protocol still validates and adds this block to the blockchain, despite the broken commitment.

### The Core Issue

The existing system neither enforces nor acknowledges Alice’s commitment to Bob. Alice must be “trusted” to fulfill her end of the bargain. If she calculates that the benefits of not adhering to the commitment outweigh Bob’s payment, she has a rational incentive to cheat.

### Economic Consequences

This lack of effective enforcement leads to high contracting costs and creates an environment with strategic uncertainty. Additionally, Alice has access to information that Bob doesn’t about what’s going to happen, possibly allowing her to exploit this asymmetry for her benefit.

##  What does PEPC-DVT do?

PEPC-DVT is designed to enforce the commitments made by block proposers in the Ethereum network. It does so by making the validity of a block dependent on whether the proposer’s commitments are met. The system utilizes Distributed Validator Technology to achieve this without altering the existing Ethereum consensus protocol.

### Key Components

- Validator Key Shares: The validator’s private key is divided into parts, known as “shares” using an algorithm like Shamir’s Secret Sharing. The validator retains 50% of these shares, while the remaining 50% are distributed among a network of specialized nodes called Distributed Validator Nodes.
- Commitment Specifications: These nodes run a specialized client that on requests for their signature it checks that the data being signed satisfies the validator’s commitments.
- Smart Contract in EVM: The client interacts with a smart contract in the Ethereum Virtual Machine (EVM) to verify if the commitments are satisfied.
- Gas Limit: To prevent abuse, a gas limit is set for the computational resources used to check commitments.

### Detailed Workflow

1. Commitment Setup: Alice and Bob agree on their respective commitments and record them in a smart contract within the EVM. Bob also escrows the payment in a contract.
2. Validator Key Distribution: Alice divides her validator key into shares. She keeps half and distributes the other half to the Distributed Validator Nodes.
3. Block Proposal: When it’s Alice’s turn to propose a block, she creates a SignedBeaconBlock and broadcasts it to the network.
4. Commitment Verification: The Distributed Validator Nodes receive this block and initiate a verification process. Each node’s client software communicates with the EVM to check if the block satisfies Alice’s commitments.
5. Signature Provision: Based on the verification result, two scenarios can occur:

- Case 1: If the block satisfies Alice’s commitments, the nodes contribute their share of the signature, enabling Alice to obtain sufficient signature shares to get the validator’s signature. This allows her to achieve her goal of having the block be recognized by the protocol.
- Case 2: If the block doesn’t satisfy Alice’s commitments, the nodes withhold their signature. Consequently, the validator’s signature is not achieved and Ethereum consensus doesn’t recognize the block.

### Reliability and Risks

The system’s reliability hinges on the integrity of the Distributed Validator Nodes. If a majority of these nodes are compromised, they could falsely validate a block that doesn’t meet the commitments. However, this risk is mitigated by distributing the validator key shares over a decentralized network of nodes. It’s also important to note that this risk doesn’t find its way inside the protocol (i.e., PEPC-DVT belongs to the Diet PEPC family of solutions, which are out-of-protocol), so I don’t see how a new type of risk would be introduced for the protocol.

##  Why PEPC-DVT?

### Unique Advantages

- Seamless Integration: No changes to Ethereum’s consensus layer.
- Commitment Versatility: Supports diverse commitment use-cases.
- Robust Security: Uses distributed validator technology for secure commitment enforcement.
- Bounded Resource Usage: Bounds social cost associated with evaluating some user’s commitments.
- Transparency: On-chain verification enhances accountability and facilitates credible contracting between agents.

### Broader Implications

- Agent-Based Programmability at Consensus: Facilitates programmability for in-protocol behavior, allowing for a more dynamic and responsive consensus layer.
- Economic Incentives: Could introduce new revenue models for validators.
- Interoperability: Potential for cross-chain transactions with other blockchain platforms.

##  Emily: A Protocol for Credible Commitments

Emily offers a robust and efficient way to manage commitments within the EVM. It not only simplifies the process for distributed validators but also ensures that computational resources are effectively managed. It handles the logic for determining whether some user’s commitments are satisfied on behalf of the distributed validator clients, allowing them to find this out by just simulating a call to the smart contract.

### Core Components

- Commitment Manager: Central smart contract that orchestrates the commitment process.
- Commitment Structure: Defines the properties of a commitment.
- Commitment Library: Contains methods for evaluating and finalizing commitments.

### Commitment Manager

The Commitment Manager is a smart contract that serves as the backbone of Emily. It performs two key functions:

1. Creating Commitments: Allows any EVM address to make new commitments.
2. Evaluating Commitments: Checks if a given value satisfies the conditions of a user’s commitments.

Users can create commitments without incurring gas costs by utilizing EIP712 signatures. Multiple commitments can also be bundled and submitted simultaneously.

### Commitment Structure

A commitment is characterized by two main elements:

1. Target: Specifies the subject matter of the commitment, similar to the concept of ‘scope’ in constraint satisfaction problems.
2. Indicator Function: A function that returns ‘1’ if the commitment is satisfied by a given value, and ‘0’ otherwise.

```auto
struct Commitment {
    uint256 timestamp;
    function (bytes memory) external view returns (uint256) indicatorFunction;
}
```

It is with the indicator function that the commitment extensionally defines the subset of values that satisfies it.

### Commitment Library: CommitmentsLib

This library contains methods for:

1. Evaluating Commitments: Checks if a given value satisfies an array of commitments.
2. Finalizing Commitments: Determines if a commitment is finalized.

```auto
library CommitmentsLib {
    function areCommitmentsSatisfiedByValue(Commitment[] memory commitments, bytes calldata value) public view returns (bool);
    function isFinalized(Commitment memory commitments) public view returns (bool finalized);
}
```

Currently, commitments are only considered probably finalized by checking if some amount of time has passed since the commitment was included. This, however, is not ideal. In practice, a better option may be for the protocol to verify a proof for the commitment’s finalization.

### Resource Management

Managing computational resources is a challenge due to the EVM’s gas-based operation. To prevent abuse, Emily allocates a fixed amount of gas for evaluating any user’s array of commitments. This ensures that computational resources are capped, bounding the worst-case scenario for distributed validators.

##  Integrating Emily into Smart Contracts

Smart contracts that wish to enforce commitments can utilize a special modifier called `Screen` after inheriting from `Screener.sol`. This modifier enables functions to validate whether user actions meet the commitments of their originator.

For a practical example of how this works, refer to the sample implementation for PBS in the repository under `samples/PEPC.sol`, which implements PBS in terms of commitments.

### Account Abstraction (ERC4337)

The repository also includes an example that integrates commitments into ERC4337 accounts. Specifically, it screens user operations to ensure they satisfy the sender’s commitments.

As part of account abstraction, ERC4337 accounts can self-declare the contract responsible for their signature aggregator. The signature aggregator, not the account, is the one that implements the logic for verifying signatures, which can be arbitrary.

In the implementation below, the sample BLS signature aggregator has been extended to enforce commitments on user operations. In practice, a screening function is used to enforce commitments.

Here’s what integrating commitments into a SignatureAggregator looks like. Notice the that the only change is the addition of the modifier `Screen`.

```auto
/**
* validate signature of a single userOp
* This method is called after EntryPoint.simulateValidation() returns an aggregator.
* First it validates the signature over the userOp. then it return data to be used when creating the handleOps:
* @param userOp the userOperation received from the user.
* @return sigForUserOp the value to put into the signature field of the userOp when calling handleOps.
*    (usually empty, unless account and aggregator support some kind of "multisig"
*/

function validateUserOpSignature(UserOperation calldata userOp)
    external
    view
    Screen(userOp.sender, this.validateUserOpSignature.selector, abi.encode(userOp))
    returns (bytes memory sigForUserOp)
{
    uint256[2] memory signature = abi.decode(userOp.signature, (uint256[2]));
    uint256[4] memory pubkey = getUserOpPublicKey(userOp);
    uint256[2] memory message = _userOpToMessage(userOp, _getPublicKeyHash(pubkey));

    require(BLSOpen.verifySingle(signature, pubkey, message), "BLS: wrong sig");
    return "";
}
```

### Token Bound Accounts (ERC6551)

The same commitment-enforcing logic has been applied to token-bound accounts, which is carried out by a slight modification in the `executeCall` function. Notice the modifier.

```auto
/// @dev executes a low-level call against an account if the caller is authorized to make calls
function executeCall(address to, uint256 value, bytes calldata data)
    external
    payable
    onlyAuthorized
    onlyUnlocked
    Screen(address(this), this.executeCall.selector, abi.encode(to, value, data))
    returns (bytes memory)
{
    emit TransactionExecuted(to, value, data);

    _incrementNonce();

    return _call(to, value, data);
}
```

This change ensures that whenever a call is executed by the account, it satisfies the account’s commitments.

##  Challenges and Security

### Challenges

1. Dependency on Distributed Validators: The system’s effectiveness is contingent on the reliability and honesty of distributed validator nodes.
2. Gas Griefing Risks: There’s a potential for malicious actors to exploit the system by consuming excessive gas, thereby affecting its performance.
3. Network Latency Concerns: The time delay in transmitting data across the network could impact the system’s efficiency and responsiveness.

### Security Measures

1. Node Decentralization: To mitigate the risk of collusion or a single point of failure, validator nodes would need to be credibly decentralized.
2. Gas Limit for Commitment Verification: A predefined maximum amount of gas is allocated for checking commitments, preventing gas griefing attacks.
3. Local Commitment Validation: Commitment checks are performed locally by the execution client, enhancing security and reducing latency.

#  Resources

- Work-in-progress specs for a PEPC distributed validator: PEPC-DVT Specs
- Protocol for credible commitments: Emily

Your feedback is highly appreciated! Feel free to reach out via [twitter](https://twitter.com/0xfuturistic).

## Replies

**maniou-T** (2023-08-31):

I love your idea, it enforces commitments without requiring modifications to Ethereum’s consensus algorithm. This maintains the integrity of the protocol while introducing a new layer of commitment enforcement.

---

**nikete** (2023-09-02):

This seems like a really neat proposal, looking forward to see it deployed. Having said that, I will now nitpick some details:

![](https://ethresear.ch/user_avatar/ethresear.ch/diego/48/13248_2.png) diego:

> Gas Limit for Commitment Verification: A predefined maximum amount of gas is allocated for checking commitments, preventing gas griefing attacks.

**preventing** seems a bit too strong a term. In particular if there is support gasless onboarding the limit on the gas for checking commitments, an attacker can still arbitrarily degrade service for others at minimal cost, via sybils. Or am I missing something?

**Distributed Validators** / **Node Decentralization** :  this is the load bearing part that seems under-specified and where this may be begging the question. Is it possible to provide economic incentives for this kind of distributed validators? is there any way to check or verify this?

---

**nick-fc** (2023-09-04):

Great post! I have a few questions:

1. Who do you imagine will serve as the supervising DVT nodes?

If you use large, reputable validators to supervise, they’ll be able to easily collude. If you use anonymous / decentralized validators, it’s easier for them to act maliciously since they have no reputation at stake. Would these operators need to be whitelisted? What’s the selection process?

1. Could PEPC-DVT use a rotation mechanism where the DVT validators change every epoch? It’d be easy to do OOP collusion with the supervising DVT nodes if they remain the same for a long period of time.
2. A big challenge with PEPC-DVT is the small DVT set. Eigenlayer provides a solution to easily scale the supervising set. What is the advantage of PEPC-DVT over just using Eigenlayer? I thought the value of normal PEPC over Eigenlayer was largely around the commitment logic being enshrined, but PEPC-DVT isn’t.
3. Just curious — do these commits open up the protocol to potential economic attacks? I’m thinking of something similar to a time bandit attack, where a proposer proposes a block that satisfies their commitments, and then the next block proposer tries to propose a block that skips the previous block.

---

**mikeneuder** (2023-09-11):

great post Diego! love how you took it past ideation and started writing some code.

some similar comments to [@nick-fc](/u/nick-fc)!

- It is a very cool use of DVT, but is there anything particular about DVT that this design hinges on? Would a simple multisig solve the same problem but without the need for DVT?
- As Nick mentioned, it seems like the selection of the “enforcement committee” is the most important feature here. If the proposer has 50% of the key, then they only need to bribe a single committee member to produce a valid signature, so the committee would have an N out of N honesty assumption right? I guess that parameter can be tuned, but its still for sure worth considering, especially if breaking the commitment could lead to outsized rewards, e.g., large MEV opportunities.
- I am curious about the timing of commitments especially in the presence of reorgs. Like could a proposer make a commitment to a builder, but then reorg the chain so that it looks like they didn’t make that commitment to trick the enforcement committee into signing their block? I guess in general these commitment schemes seem super latency sensitive, so I am curious about the games proposers could play with them.

---

**OisinKyne** (2023-09-22):

Firstly, great work [@diego](/u/diego)!

I wanted to weigh in here, to answer some people’s questions, and slightly refine one piece the proposal.

The one issue here is with the idea that the proposer has 50% of the validator private key and other DV nodes have the other 50%. Within a DV cluster, each node has an equal amount of the private key (more specifically they each have a coefficient of a polynomial that represents the private key rather than pieces of the key itself), and the node that has the right to propose is rotated deterministically per the rules of the consensus algorithm the cluster is running. (Usually QBFT at the moment). The operator that happens to be the proposer uses its mev-boost or CL to craft a block, and proposes to the rest of the cluster that they approve it for signing. The rest of the nodes check it conforms to the agreed upon rules (for now, that the fee recipient is as expected), and if so, they play their part in the consensus game to approve it. Once consensus (within the cluster) is achieved on the block, the validator clients are given it to sign.

In a PEPC-DVT world, these DV clients would use their EL RPC APIs to run the block through Emily, and only agree to it if the commitment checks pass.

Now to answer some of the rest of the comments:

![](https://ethresear.ch/user_avatar/ethresear.ch/nick-fc/48/12463_2.png) nick-fc:

> Who do you imagine will serve as the supervising DVT nodes?

This depends on which operators make up a given distributed validator. If a builder wanted to only use a subset of doxxed validators, they would not bid for upcoming proposals by validator indices they don’t know. (e.g. validators that aren’t bound to honesty with eigenlayer, or validators that don’t belong to lido)

![](https://ethresear.ch/user_avatar/ethresear.ch/nick-fc/48/12463_2.png) nick-fc:

> Could PEPC-DVT use a rotation mechanism where the DVT validators change every epoch? It’d be easy to do OOP collusion with the supervising DVT nodes if they remain the same for a long period of time.

Every slot is proposed by a new validator, run by different (but static) operators. There is up to 32 slots of lookahead. Operators within a given DV can plan to collude with one another for the next time they get a proposal, so at its most basic, a PEPC-DVT proposal for a single slot could be compromised by 3 colluding operators. The risk of this could be reduced by introducing a PEPC-DVT++ type of setup, where the operators agree to be bound by restaking slashing rules if they propose something that doesn’t conform to their commitments.

![](https://ethresear.ch/user_avatar/ethresear.ch/nick-fc/48/12463_2.png) nick-fc:

> A big challenge with PEPC-DVT is the small DVT set. Eigenlayer provides a solution to easily scale the supervising set. What is the advantage of PEPC-DVT over just using Eigenlayer? I thought the value of normal PEPC over Eigenlayer was largely around the commitment logic being enshrined, but PEPC-DVT isn’t.

You can use eigenlayer with DVT as they are complementary ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) Eigenlayer alone can only punish a validator up to all of its stake. With eigenlayer + DVT, you make it more difficult to ‘defect’ and break the commitments, as you need most of the operators in the cluster to agree to do so.

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> is there anything particular about DVT that this design hinges on? Would a simple multisig solve the same problem but without the need for DVT?

DVT basically is a consensus mechanism + multisig for validating ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> it seems like the selection of the “enforcement committee” is the most important feature here. If the proposer has 50% of the key, then they only need to bribe a single committee member to produce a valid signature, so the committee would have an N out of N honesty assumption right? I guess that parameter can be tuned, but its still for sure worth considering, especially if breaking the commitment could lead to outsized rewards, e.g., large MEV opportunities.

Check my nuance at the top of this post, but more or less yes. With this proposal you have M out of N honesty assumptions (where M must be > 2/3rds of N for consensus safety reasons). You can combine this with up the 32 ether of economic incentive via eigenlayer, but even together they still may not be enough for large defection opportunities to happen. I’m not sure there is an out of protocol mechanism that can do better than that.

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> could a proposer make a commitment to a builder, but then reorg the chain so that it looks like they didn’t make that commitment to trick the enforcement committee into signing their block? I guess in general these commitment schemes seem super latency sensitive, so I am curious about the games proposers could play with them.

I think at the very least a commitment scheme shouldn’t be allowed to be changed and used in the same block. A builder should probably wait until a commitment is finalized to be extremely safe. This design will definitely be latency sensitive, but more towards brittleness than vulnerability imo. Blinded beacon block headers are small (KBs), full blocks are large (MBs). Currently coming to consensus on a proposal takes little verification time, with PEPC DVT you now have to run the large block through an EL RPC api to simulate a solidity function call that involves signature verification (and can have lots of gas cost). All of this runs the risk of taking too long for a proposal to happen and the slot getting missed. However Diego is already [exploring](https://ethresear.ch/t/making-pepc-dvt-private-with-bls-blinded-multi-signatures/16692) designs that might reduce this back down to light in size and verification time, either with ZK or MEVboost type approaches.

![](https://ethresear.ch/user_avatar/ethresear.ch/nikete/48/10338_2.png) nikete:

> Is it possible to provide economic incentives for this kind of distributed validators? is there any way to check or verify this?

The short answer here is yes they can be *provided* [@nikete](/u/nikete), but verifying these economic incentives are *objective* is pretty hard. We’ll be putting out some research by the [Nethermind team](https://blog.obol.tech/looking-forward-obol-v2/) over the coming weeks on the challenges relating to this topic.  ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**diego** (2023-09-23):

Thanks for your reply [@nikete](/u/nikete) and sorry for not getting back to you here earlier.

![](https://ethresear.ch/user_avatar/ethresear.ch/nikete/48/10338_2.png) nikete:

> preventing seems a bit too strong a term. In particular if there is support gasless onboarding the limit on the gas for checking commitments, an attacker can still arbitrarily degrade service for others at minimal cost, via sybils. Or am I missing something?

I think you’re right about this. It would be worthwhile to consider anti-sybil mechanisms that could be used in this context. In any case, it might be useful to explore how these issues have been addressed by ERC4337 with respect to signature aggregators that could consume arbitrary gas.

![](https://ethresear.ch/user_avatar/ethresear.ch/nikete/48/10338_2.png) nikete:

> Distributed Validators / Node Decentralization : this is the load bearing part that seems under-specified and where this may be begging the question. Is it possible to provide economic incentives for this kind of distributed validators? is there any way to check or verify this?

With respect to this second point, I agree that this is a tricky part. One approach could be to rely on the user setting up some reward in a smart contract that gets unlocked by a DVT node by posting a proof. This proof would correspond to an inclusion check of the DVT node’s share of the signature in a successful aggregate signature used by the distributed validator. Note that in this example the DVT node would claim a share of the reward proportional to their share of the signature. I’d be curious to see if these inclusion checks are possible (or, alternatively, if some other Oracle-based approach could make sense).

---

**diego** (2023-09-23):

Thanks for all the great questions [@nick-fc](/u/nick-fc) ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

[@OisinKyne](/u/oisinkyne) already gave a pretty detailed response to many of the points, so I will only elaborate on the ones I can expand.

![](https://ethresear.ch/user_avatar/ethresear.ch/nick-fc/48/12463_2.png) nick-fc:

> Who do you imagine will serve as the supervising DVT nodes?

This question targets directly the possible principal-agent problem that could emerge from DVT nodes. I’d need to think about it more, but one approach could be having these nodes put up a stake in some smart contract that gets slashed if a proof of misbehavior is posted. Part of the stake could go to the address that posted the proof. In essence, this idea is to rely on some kind of optimistic system that increases the costs of undesirable behavior. The next question would be – in what ways could misbehavior materialize and can we successfully prove that misbehavior on-chain? If not all behavior can successfully be proven on-chain, an escalation game akin to UMA’s could be carried out, for example.

![](https://ethresear.ch/user_avatar/ethresear.ch/nick-fc/48/12463_2.png) nick-fc:

> A big challenge with PEPC-DVT is the small DVT set. Eigenlayer provides a solution to easily scale the supervising set. What is the advantage of PEPC-DVT over just using Eigenlayer? I thought the value of normal PEPC over Eigenlayer was largely around the commitment logic being enshrined, but PEPC-DVT isn’t.

With respect to this question, the key insight here is that Eigenlayer does not make the validator’s signature conditional on any behavior. It’s fundamentally an optimistic system that increases the costs associated with certain behaviors for the validator by introducing the risk of getting slashed. PEPC-DVT seeks to address the fact that sometimes we want to make some actions actually prohibited and not just economically expensive. This is the case for making the validator’s signature conditional on commitment validity. Now, the intersection of the two approaches could be interesting though. As [@OisinKyne](/u/oisinkyne) pointed out, one interesting idea is for the distributed validator to additionally get slashed for posting a commitment-invalid block. That is, if the DVT nodes fail and the validator effectively posts a commitment-invalid block, they could get slashed after the fact by Eigenlayer on-chain.

![](https://ethresear.ch/user_avatar/ethresear.ch/nick-fc/48/12463_2.png) nick-fc:

> Just curious — do these commits open up the protocol to potential economic attacks? I’m thinking of something similar to a time bandit attack, where a proposer proposes a block that satisfies their commitments, and then the next block proposer tries to propose a block that skips the previous block.

Concerning this last question, PEPC-DVT doesn’t introduce a risk that the protocol doesn’t already experience. This is because from the perspective of the protocol, a commitment-valid block is indistinguishable from any other block proposed, so the risks of the next block proposer trying to propose a block that skips the previous ones should be no different.

---

**diego** (2023-09-23):

Thanks [@mikeneuder](/u/mikeneuder) for all the questions! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> It is a very cool use of DVT, but is there anything particular about DVT that this design hinges on? Would a simple multisig solve the same problem but without the need for DVT?

I agree with this point. In fact, PEPC-DVT could be framed in terms of BLS Multi-Signatures, as [this new article](https://ethresear.ch/t/making-pepc-dvt-private-with-bls-blinded-multi-signatures/16692) explores in the context of blinded signatures that would make PEPC-DVT private.

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> I am curious about the timing of commitments especially in the presence of reorgs. Like could a proposer make a commitment to a builder, but then reorg the chain so that it looks like they didn’t make that commitment to trick the enforcement committee into signing their block? I guess in general these commitment schemes seem super latency sensitive, so I am curious about the games proposers could play with them.

With respect to this question, my solution was that the commitments enforced (deemed “active”) were only the ones introduced by transactions already finalized. The tricky part here is how to find this out on-chain if we want to delegate all the logic of checking commitments to a smart contract (such that the DVT client only has to make a call to this contract passing the block). In the worst case, the DVT client could be the one that makes sure to only consider commitments finalized. By only considering finalized ones, we prevent the protocol from considering a commitment that may later be excluded.

---

**mikeneuder** (2023-09-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/diego/48/13248_2.png) diego:

> With respect to this question, my solution was that the commitments enforced (deemed “active”) were only the ones introduced by transactions already finalized. The tricky part here is how to find this out on-chain if we want to delegate all the logic of checking commitments to a smart contract (such that the DVT client only has to make a call to this contract passing the block). In the worst case, the DVT client could be the one that makes sure to only consider commitments finalized. By only considering finalized ones, we prevent the protocol from considering a commitment that may later be excluded.

Are the commitments something we expect proposers to make just before their slot though? Like if I want to commit to selling my block to a specific builder, then I only want to do that if I know they are giving me the best price, which will depend highly on the binance spot price at the beginning of my slot.

The attack I am worried about is a pretty straightforward reorg.

- i commit to a builder at the beginning of my slot
- the payload gets revealed b/c the commitment is signed off by my committee
- i unbundle the payload to steal all the MEV
- i publish my new block and broadcast it faster to win the attesting committee race

(i think in general commitment devices seem vulnerable to this! i don’t think its a feature of only PEPC-DVT) just curious your thoughts!

