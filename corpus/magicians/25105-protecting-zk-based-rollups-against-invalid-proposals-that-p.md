---
source: magicians
topic_id: 25105
title: Protecting ZK-based Rollups against Invalid Proposals that Pass Verification
author: Samuel.Ranellucci
date: "2025-08-14"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/protecting-zk-based-rollups-against-invalid-proposals-that-pass-verification/25105
views: 109
likes: 1
posts_count: 1
---

# Protecting ZK-based Rollups against Invalid Proposals that Pass Verification

# Protecting ZK-based Rollups against Invalid Proposals that Pass Verification

[Samuel Ranellucci](mailto:samuel.ranellucci@coinbase.com), [Roger Bai](mailto:roger.bai@coinbase.com)

## TLDR

ZK-based rollups are rollups that use zero knowledge proofs to prove state transitions onchain. As these systems are complex, protection against soundness bugs—flaws that allow an adversary to prove an invalid state transition—are crucial. This post proposes a mechanism to help protect the rollup against invalid proposals that pass verification, using concepts introduced in the blog [Soundness alert function for ZK-rollups](https://ethresear.ch/t/a-soundness-alert-function-for-zk-rollups/15377/1) and briefly discussed in Vitalik’s [Multi-Provers for Rollup Security](https://www.youtube.com/watch?v=6hfVzCWT6YI&t=1284s) talk. We leverage the completeness property of a proof system (the guarantee that any true statement can be proven) to create a “soundness alert”. With this solution, if an attacker proposes an invalid proposal that passes verification, an honest party can challenge it by proving the correct proposal for that same block. The existence of two conflicting-but-verified proofs serves as an unambiguous, onchain signal that the proof system has been compromised, allowing the rollup to enter a safe mode to protect itself.

We believe this mechanism is an important layer of security that should be integrated into any rollup using ZK proofs, including multi-prover systems. Below, we detail the mechanism, provide a proof-of-concept, and outline a potential integration path for the OP Stack.

## Related Works

The ideas presented in this document appeared in both the blog [Soundness alert function for ZK-rollups](https://ethresear.ch/t/a-soundness-alert-function-for-zk-rollups/15377/1) and briefly in the talk [Multi-Provers for Rollup Security](https://www.youtube.com/watch?v=6hfVzCWT6YI&t=1284s) from Vitalik. We believe that these ideas are important for protecting rollups and have decided to expand on them, especially since recent disclosures have shown how challenging it is to design a proof system for rollups (see, for e.g., the [security advisory](https://x.com/SuccinctLabs/status/1929773028034204121?t=EtLKfzsi52SRJ4XT2OZ4hA&s=19) from Op-succinct and this [post](https://x.com/risczero/status/1935404812146725042) from Risc Zero).

An alternative to ZK is an approach that we refer to as  “interactive dispute games” that occurs after a party claims that a proposal is invalid. An interactive dispute game is a multi-round protocol that allows honest participants to protect valid proposals and eliminate invalid proposals. There has been significant work towards improving interactive dispute games against attacks such as sybil attacks and resource exhaustion attacks. Unfortunately, in spite of this research, interactive dispute games still have high finality delays.

An approach for securing rollups and reducing finality delays is a multi-proof design using a combination of ZK, [TEE](https://en.wikipedia.org/wiki/Trusted_execution_environment), and fraud proof games. Proposal and talks about this can be found in the following links: [L2 security and finalization roadmap](https://ethereum-magicians.org/t/a-simple-l2-security-and-finalization-roadmap/23309) from Vitalik and [Multi-Prover Implementation](https://scroll.io/blog/scaling-security) from Scroll.

## Soundness and Completeness of ZK-proof Systems

In the context of rollups, a ZK-proof system is a non-interactive proof system that needs to be both complete and sound. Completeness ensures that every true statement can be proven true, while soundness ensures that an adversary cannot prove a false statement.

## The Challenges of Soundness

Securing systems with ZK is challenging due to their complexity. A single flaw, like a missing check, can compromise the soundness of the proof system. If the proof system is not sound, an attacker could provide an invalid proposal with a fake proof, leading to its acceptance. A recent [security advisory](https://x.com/SuccinctLabs/status/1929773028034204121?t=EtLKfzsi52SRJ4XT2OZ4hA&s=19) from SuccinctLabs as well as a recent [disclosure](https://x.com/risczero/status/1935404812146725042) from Risc Zero are just some examples of this issue.

## A Solution: Use Completeness to Protect Against Soundness Error

A potential solution involves building a mechanism within the proof system that allows an honest party to provide a valid proposal to counter an invalid one, even if the invalid proposal passes verification.

The idea is that if the proof system is not sound but is complete, a party can alert the rollup that the system is not sound by providing the correct proposal with a proof of its correctness. The rollup should then discard all non-finalized proposals (including the invalid proposal) and switch to a different method of finalization.

This solution requires minimal overhead in design and implementation. First, this proposal requires that honest parties must have the time to both generate a proof for the correct proposal and have time to submit those to the L1 chain. This can be done by introducing a challenge period for ZK verification (the finality delay required for this challenge will pale in comparison to the delays required for interactive dispute games). Second, this requires that a backup method of finalization be implemented. Third, we need to implement a function for alerting the rollup that the proof system is not sound. In this function, if the rollup accepts that there is a flaw in the proof system, it must discard all non-finalized blocks and switch finalization to the backup method.

The following describes the steps of how a rollup could be alerted to a flaw in the proof system.

- A smart contract receives two distinct proposals for the same block that are each supported by a proof that passes verification.

From a third-party perspective, the submission of two such proposals indicates a soundness error in the proof system. This can occur regardless of the order in which the proofs were submitted, and even if both proposals are invalid.
- Upon detecting this soundness error, the smart contract

Disables the ZK component of the rollup.
- Discards all non-finalized proposals.
- Switches to a backup finalization method.

[![Activity diagram with swimlanes](https://ethereum-magicians.org/uploads/default/optimized/2X/9/93b4feca28f7cbdad69304ba52b5e8a9b56d4554_2_150x375.jpeg)Activity diagram with swimlanes400×1000 29.8 KB](https://ethereum-magicians.org/uploads/default/93b4feca28f7cbdad69304ba52b5e8a9b56d4554)

## Exploiting This Idea in the Context of Threshold Proof Systems

In the context of threshold proof systems, this technique can be used to eliminate faulty components. For example, in a rollup using the 2-out-of-3 [proposal](https://ethereum-magicians.org/t/a-simple-l2-security-and-finalization-roadmap/23309) from Vitalik, where there are three components (TEE, ZK, fault proof game), this idea can be used to remove the ZK-component so that the system essentially becomes a 2-out-of-2 with TEE and a fault proof game. To restore the ZK-component, a security council must proceed to upgrade the ZK component.

# Proof-of-Concept

We demonstrate how this proposal can be applied to a very simple rollup design where the rollup only asks for the hash of the next block of transactions after the current block has been finalized. For this demo, a party will alert the rollup that the proof system is not sound by submitting a proposal that passes verification for the same block as the current proposal.

If the rollup is alerted that the proof system is unsound, the state of the contract is modified so that only the backupProposer can make a proposal. This will hold until the backupProposer calls the function useZKAgain(). In this section, we will only provide the most important component of the POC in this document and will also omit some code to simplify the presentation. The full POC is available [here](https://github.com/roger-bai-coinbase/zk-soundness-prototype).

We decompose the POC into sections.

1. The interface contracts of the POC.

IZKVerifier is an interface for validating proofs.
2. ITransactionsHash is an interface for fetching the next hash of the block.

The code for specifying a proposal and the state.
Code blocks for the `SimpleRollup` contract that relate directly to the proposal including

1. Variables
2. The challengeProof function, where a party challenges the proof for a proposed block
3. The proposal function, where only backupProposer can make a proposal if the proof fails.

Simple test showing that only the backup proposer can prove a proposal after a successful alert.

### Interface

```java
interface IZKVerifier {
    function verifyStateProof(
        uint256 blockNumber,
        bytes32 stateToProve,
        bytes memory proof,
        bytes32 transactionsHash
    ) external view returns (bool);
}

```

```java
interface ITransactionsHash {
    function getTransactionsHash(
        uint256 blockNumber
    ) external view returns (bytes32);
    function startingBlock() external view returns (uint256);
    function updateTransactionsHash(
        uint256 blockNumber,
        bytes32 transactionsHash
    ) external;
}

```

### Proposal and State

```java
struct Proposal {
    // L2 block number
    uint256 blockNumber;
    // L2 state
    bytes32 state;
    // When the proposal was proved
    uint256 timestampProved;
}

```

```java
struct State {
    // L2 block number
    uint256 blockNumber;
    // L2 state
    bytes32 state;
}

```

# Simple rollup Design Integrating Protection

### Variables

```java
contract SimpleRollup {
    // Verifies ZK proofs
    IZKVerifier public zkVerifier;
    // Fetches L2 transaction hashes
    ITransactionHashes public transactionHashes;

    // Time to wait before finalizing a proposal
    uint256 public zkFinalizationDelay;
    // Whether the ZK proof system has failed
    bool public zkFailed;

    address backupProposer;

    // code omitted for clarity
    ..........................
```

### Challenge Invalid Proof

```java
function challengeProof(
        bytes32 alternateState,
        bytes calldata proof
    ) external {
        require(!zkFailed, "ZK has already failed.");
        require(
            alternateState != currentProposal.state,
            "Alternate state is the same as the proposed state."
        );

        require(
            block.timestamp - currentProposal.timestampProved  0,
            "Proposal has not been proved yet."
        );


        Proposal memory proposal = currentProposal;
        require(
            zkVerifier.verifyStateProof(
                proposal.blockNumber,
                alternateState,
                proof,
                transactionHashes.getTransactionsHash(proposal.blockNumber)
            ),
            "Proof is invalid."
        );

        zkFailed = true;
        delete currentProposal;
        emit ZKFailed(proposal.blockNumber, proposal.state, alternateState);
    }

```

### Propose

```java
    function propose(uint256 blockNumber, bytes32 state) public {
        require(
            !zkFailed || msg.sender == backupProposer,
            "ZK down. Only backup proposer can propose."
        );

        //code omitted for clarity
        ..........................
    }

```

### UseZKAgain()

```java
function useZKAgain() external {
        require(zkFailed, "ZK has not failed yet.");
        require(
            msg.sender == backupProposer,
            "Only backup proposer can choose to use ZK again."
        );
        zkFailed = false;
    }

```

### Only Backup Proposer can Submit Proposal After Successful Alert

```java
 function testProveOnlyBackupProposer() public {
        simpleRollup.propose(
            startingL2Block + 1,
            keccak256(abi.encode(startingL2Block + 1))
        );
        simpleRollup.prove(abi.encode(0x1234));

        simpleRollup.challengeProof(
            keccak256(abi.encode(0x1234)),
            abi.encode(0x1234)
        );
        assertEq(simpleRollup.zkFailed(), true);

        vm.prank(backupProposer);
        simpleRollup.propose(
            startingL2Block + 1,
            keccak256(abi.encode(startingL2Block + 1))
        );

        vm.expectRevert("ZK down. Only backup proposer can provide a proof.");
        simpleRollup.prove(abi.encode(0x1234));

        vm.prank(backupProposer);
        simpleRollup.prove(abi.encode(0x1234));

        (
            uint256 blockNumber,
            bytes32 state,
            uint256 timestampProved
        ) = simpleRollup.currentProposal();
        assertEq(blockNumber, startingL2Block + 1);
        assertEq(state, keccak256(abi.encode(startingL2Block + 1)));
        assertEq(timestampProved, block.timestamp);
    }

```

# Suggested Next Steps For the Ecosystem

L2 rollups based on ZKVMs should study this proposal and determine if this proposal could improve the security of their system. If the study concludes that this proposal can improve the security of their system, the next step would be to figure out how to best integrate a soundness alert and determine which fallback methods should be used for finalization (fraud-proof game, permissioned proposer, etc.). Finally, the soundness alert and fallback methods should be integrated and tested on testnet before launching on mainnet.

In the section below, we show how our proposal could be integrated within OP Stack chains.

### Pseudocode for Possible OP Stack Integration

Below is pseudocode for how this system may be implemented for OP Stack chains. The functionality is added to the `AnchorStateRegistry` contract, which will be viewed as the source of truth for the L2 state.

Each proposal contains two pieces of information: the L2 block number and the L2 output root. Hence if two proposals with the same L2 block number but different output roots can be verified with a ZK proof, then there is an error with the proof system.

If the AnchorStateRegistry detects a soundness error, it can switch the game type to a default game type. We believe that this idea could be applied to chains based on Optimism with a reasonable amount of effort.

```java
// SPDX-License-Identifier: MIT
pragma solidity 0.8.15;

import {AnchorStateRegistry} from "...";

contract ZKAnchorStateRegistry is AnchorStateRegistry {
    // The game type for a ZK non-interactive game
    GameType immutable ZK_GAME_TYPE;

    // The amount of time for a resolved ZK game to be considered finalized
    uint256 zkFinalizationDelay;

    event SoundnessError(Proposal proposal, IDisputeGame disputeGame);

    /// @notice Nullify a ZK dispute game
    /// @param proposal The proposal to nullify the game with
    /// @param zkProof The ZK proof to nullify the game with
    /// @param disputeGame The dispute game to nullify
    /// @param publicArgs Additional public arguments for the ZK proof
    function alert(Proposal proposal, Proof zkProof, IDisputeGame disputeGame, bytes calldata publicArgs) public {
        Proposal startingOutputRoot = disputeGame.startingOutputRoot();

        // Check that the proposal can be used to nullify the game
        require(proposal.l2SequenceNumber == startingOutputRoot.l2SequenceNumber, "L2 block number must match");
        require(proposal.root != startingOutputRoot.root, "Cannot contradict with same root");

        // Checks on the public arguments
        require(publicArgs ..., "Public arguments are incorrect");

        // Check that the dispute game can be nullified
        require(isZKGameDisputable(disputeGame), "Game is not disputable");

        // Verify the ZK proof
        require(prover.verify(proposal, zkProof, publicArgs), "ZK proof is invalid");

        // There is a soundness error, so we have to change the game type and retire all current games
        respectedGameType = GameType(1); // permissioned Cannon game type (or whichever game type is chosen to fall back to)
        retirementTimestamp = uint64(block.timestamp); // retire all games

        emit SoundnessError(proposal, disputeGame);
    }

    /// @notice Check if a ZK dispute game can be nullified
    /// @param disputeGame The dispute game to check
    /// @return Whether the game can be nullified
    function isZKGameDisputable(IDisputeGame disputeGame) public view returns (bool) {
        // Game must be a ZK game
        if (disputeGame.gameType() != ZK_GAME_TYPE) return false;

        // Game must be proper i.e. registered, not blacklisted, not retired, not paused
        if (!isGameProper(disputeGame)) return false;

        // Game must be respected i.e. correct game type when created
        if (!isGameRespected(disputeGame)) return false;

        // Game must be resolved
        if (!isGameResolved(disputeGame)) return false;

        // Game must be within the airgap period for a nullification
       if (block.timestamp - disputeGame.resolvedAt().raw() > zkFinalizationDelay) return false;

        // Game must be resolved in favor of the defender.
        if (disputeGame.status() != GameStatus.DefenderWins) return false;

        return true;
    }
```
