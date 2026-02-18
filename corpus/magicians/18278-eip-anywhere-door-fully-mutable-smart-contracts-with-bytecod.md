---
source: magicians
topic_id: 18278
title: "EIP: Anywhere Door - Fully Mutable Smart Contracts with Bytecode Activation"
author: hiddenintheworld
date: "2024-01-23"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-anywhere-door-fully-mutable-smart-contracts-with-bytecode-activation/18278
views: 1129
likes: 0
posts_count: 5
---

# EIP: Anywhere Door - Fully Mutable Smart Contracts with Bytecode Activation

---

## eip: TBC
title: Anywhere Door - Fully Mutable Smart Contracts with Bytecode Activation
author: hiddenintheworld.eth ()
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2024-01-22
requires: None

## Simple Summary

Inspired by “Doraemon’s” magical “Anywhere Door,” this EIP introduces a novel framework for smart contracts, enabling the dynamic addition, removal, or modification of ‘doors’ (functionalities) at any time post-deployment. This concept provides a level of full mutability in smart contracts, complemented by a mechanism for user-submitted door proposals and distinctions between mutable and immutable doors, achieved through “Bytecode Activation.”

## Abstract

The “Anywhere Door” EIP proposes a smart contract architecture that allows for on-the-fly “Bytecode Activation,” enabling dynamic toggling of contract functionalities (referred to as ‘doors’) and state variables. Users can submit new functionalities as door proposals, which authorized parties can activate, deactivate, or mark as immutable. This approach ensures full mutability of the smart contract while preserving the ability to set specific doors as immutable, offering both adaptability and stability within the contract’s ecosystem.

## Motivation

In the rapidly evolving world of decentralized applications, the need for smart contracts that can dynamically adapt to changing requirements and community inputs is paramount. The “Anywhere Door” EIP addresses this need by providing a mutable framework that supports immediate updates and modifications, without the overhead of redeployment. This ability to dynamically add or remove functionalities, as well as to toggle them on and off, fosters innovation and ensures efficiency and adaptability in smart contract development.

## Specification

The following diagram (Figure 1) provides a comprehensive view of the Anywhere Door smart contract ecosystem. This flowchart visually represents the interconnected nature of doors across various smart contracts, demonstrating how they can be linked and interact with each other.

Each door is depicted with indicators (ticks and crosses) to signify their status (active/inactive or open/closed), and arrows or lines show the potential pathways or links between doors across different contracts. This architectural diagram highlights the versatility and complexity of the Anywhere Door system, emphasizing its capability to create a network of dynamic, interlinked functionalities across the blockchain landscape.

[![anywhere_archi](https://ethereum-magicians.org/uploads/default/optimized/2X/3/3307a37175461e48364300b36debd5fbcfd9b34b_2_385x500.png)anywhere_archi2641×3427 331 KB](https://ethereum-magicians.org/uploads/default/3307a37175461e48364300b36debd5fbcfd9b34b)

***Figure 1 : Anywhere Door overall architecture***

The following flowchart (Figure 2) illustrates the workflow for handling door proposals and updating door configurations in the smart contract. The process involves determining if the door is mutable, whether the user is the owner, and then either storing the door proposal or updating the door’s status.

[![anywheredoor_update](https://ethereum-magicians.org/uploads/default/optimized/2X/8/8bc64b5ad09991fe9a651addd146a53b809b016c_2_690x468.png)anywheredoor_update2128×1444 93.5 KB](https://ethereum-magicians.org/uploads/default/8bc64b5ad09991fe9a651addd146a53b809b016c)

***Figure 2: Door Proposal and Update Mechanism***

The following flowchart (Figure 3) demonstrates how the Anywhere Door functions as a proxy, determining the active status of doors and deciding the execution path. It starts with checking if a door is active (open or closed). If closed, it throws an error. If open, it checks for more doors, looping through the process until it reaches a door that is the final execution point.

[![anywheredoor_execution](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c2192cfc5d38981c85f6266312942d0ccae57ec5_2_690x414.png)anywheredoor_execution3244×1948 143 KB](https://ethereum-magicians.org/uploads/default/c2192cfc5d38981c85f6266312942d0ccae57ec5)

***Figure 3: Flowchart of Door Execution and Proxy Routing***

### Contract Storage:

- mapping(bytes4 => address) public doorToImplementation; : Maps door selectors to contract addresses for their implementation.
- mapping(bytes4 => bool) public doorActive; : Indicates whether a door is currently active or inactive.
- mapping(bytes4 => bool) public doorImmutable; : Denotes if a door is immutable.

### Door Submission, Addition, and Update Mechanism:

- Users can propose new doors by submitting their intended door selector and implementation details.
- The contract owner can directly activate, deactivate, or update doors, providing a responsive approach to contract management.
- Essential doors can be marked as immutable upon activation, ensuring their permanence.

### Door Calls:

The “Anywhere Door” contract handles incoming calls by determining the appropriate door to execute based on the call’s signature. It follows a structured process to decide how to handle each call:

1. Identify the Target Door: The contract first identifies which door (functionality) is being called by examining the incoming call’s signature. This is matched against the doorToImplementation mapping to find the corresponding contract address.
2. Check Door Status: Before proceeding with execution, the contract checks the door’s status in doorActive. If the door is inactive, the call is rejected, and an error is thrown. This step ensures that only active doors can process calls.
3. Execution through Delegate Call: For active doors, the contract uses Ethereum’s delegatecall to execute the linked function’s bytecode. This allows the door’s code to execute in the context of the original contract, maintaining the contract’s state and allowing the door to interact seamlessly with other parts of the contract.
4. Handle Immutable Doors: If the door is marked as immutable in doorImmutable, any attempts to modify its implementation or status (apart from activation or deactivation) are rejected. This ensures the integrity and permanence of essential functionalities.

## Rationale

- The “Anywhere Door” concept, combined with “Bytecode Activation,” introduces unprecedented flexibility and efficiency in smart contract management.
- This EIP represents a significant advancement in smart contract technology by enabling full mutability, yet accommodating the option for immutable functionalities.
- The framework suits a broad spectrum of use cases, offering both adaptability for evolving requirements and stability for core operations.

## Security Considerations

- Ensuring the integrity and security of submitted door proposals and bytecode is crucial; robust verification processes are necessary.
- The management of door activation and immutability status must be handled meticulously to prevent any inadvertent alterations.
- Adherence to standard security practices in smart contract development is essential, with an emphasis on the mutable aspects of the contract.

## Backwards Compatibility

- This EIP introduces a novel paradigm in smart contract functionality management, significantly differing from traditional models and existing standards like EIP-2535.

## Implementation

This implementation provides a Solidity example of the Anywhere Door contract. It includes functions for proposing, setting, and toggling door functionalities. The contract owner has the authority to accept proposals, update door functionalities, and toggle their active status.

```auto
pragma solidity ^0.8.0;

contract AnywhereDoor {
    address public owner;
    mapping(bytes4 => address) public doorToImplementation;
    mapping(bytes4 => bool) public doorActive;
    mapping(bytes4 => bool) public doorImmutable;

    struct DoorProposal {
        address implementation;
        bool isActive;
        bool isImmutable;
    }
    mapping(bytes4 => DoorProposal) public proposedDoors;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function.");
        _;
    }

    function proposeOrSetDoorImplementation(bytes4 doorSelector, address implementation, bool isActive, bool isImmutable) external {
        require(!doorImmutable[doorSelector], "Cannot modify immutable door.");

        if (msg.sender == owner) {
            doorToImplementation[doorSelector] = implementation;
            doorActive[doorSelector] = isActive;
            doorImmutable[doorSelector] = isImmutable;
        } else {
            proposedDoors[doorSelector] = DoorProposal(implementation, isActive, isImmutable);
        }
    }

    function acceptDoorProposal(bytes4 doorSelector) external onlyOwner {
        DoorProposal memory proposal = proposedDoors[doorSelector];
        require(proposal.implementation != address(0), "Proposal does not exist.");

        doorToImplementation[doorSelector] = proposal.implementation;
        doorActive[doorSelector] = proposal.isActive;
        doorImmutable[doorSelector] = proposal.isImmutable;
    }

    function toggleDoorActive(bytes4 doorSelector, bool isActive) external onlyOwner {
        require(!doorImmutable[doorSelector], "Cannot modify immutable door.");
        doorActive[doorSelector] = isActive;
    }

    fallback() external {
        address implementation = doorToImplementation[msg.sig];
        bool isActive = doorActive[msg.sig];
        require(implementation != address(0) && isActive, "Door inactive or does not exist.");

        assembly {
            calldatacopy(0, 0, calldatasize())
            let result := delegatecall(gas(), implementation, 0, calldatasize(), 0, 0)
            returndatacopy(0, 0, returndatasize())
            switch result
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }
}
```

## Copyright

Copyright and related rights waived via CC0.

## Replies

**drllau** (2024-01-25):

Interesting … can the “door” concept be used to implement the communicating sequential process ([CSP](https://en.wikipedia.org/wiki/Communicating_sequential_processesa)) model of computation across multiple chains? Imagine each floor to be a distinctive EVM compatible Layer2 chain, each with a subset of implemented functionality (alpha/beta etc). Then so long as there is a consistent layer that operates all floors/chains, then the barrier operation works as a whole. In Hoare’s notation

> PAR (for each chain/floor)
> SEQ (try doors from latest to earlist)
> If !(release / door3)
> if!(beta / door2)
> if!(alpha / door1)
> QES
> RAP

End of barrier … check to see if there is at least one breadth-first search that succeeds). This artifact might be used for progressive updates whereas there’s a reference implementation (your contract1) whilst partial implementations or refinements are at various stages across different chains.

The reason why I picked CSP is that we have decent theories of correctness proofs and the study of dead/live-locks is understood and amenable to static analysis. Proofs can be [provided](https://www.anthonyhall.org/c_by_c_secure_system.pdf).

---

**CedarMist** (2024-01-29):

This is a cool idea, but why does it need to include a one-size-fits-all proposal & update mechanism? Surely that could just be another plugin^H^H^H^Hdoor…

Could you combine this with some kind of access-control?

e.g. ‘function X is access controlled, here is a mapping of functions which are allowed to call it’

Or… to make it more and more general, couldn’t the doors available be dependent on whichever contract or user is calling? The Anywhere Door is mysterious, two people can go through the same door and arrive at different places.

```auto
struct Door {
    address who;
    bytes4[] sigs;
    address target;
}
contract DoorDoor {
    mapping(bytes32 => address) public doors;
    constructor(Door[] calldata in_doors) {
        for( uint i = 0; i < in_doors.length; i++ ) {
            for( uint j = 0; i < in_doors[i].sigs.length; j++ ) {
                doors[keccak(abi.encodePacked(in_doors[i].who, doors[i].sigs[j]))] = in_doors[i].target;
            }
        }
    }
    fallback() external {
        address implementation = doors[keccak(abi.encodePacked(msg.sender, msg.sig))];
        assembly {
            calldatacopy(0, 0, calldatasize())
            let result := delegatecall(gas(), implementation, 0, calldatasize(), 0, 0)
            returndatacopy(0, 0, returndatasize())
            switch result
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }
}
```

An example of the pattern would be an ‘Authenticated Door’ which has access to admin functions, it checks if the user is in the admin list then forwards their request back through the door but with ERC2771 context appended.

Or the DoorDoorDoor, which manages the mappings of which Door the DoorDoor goes through?

---

**hiddenintheworld** (2024-03-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cedarmist/48/11033_2.png) CedarMist:

> Or… to make it more and more general, couldn’t the doors available be dependent on whichever contract or user is calling? The Anywhere Door is mysterious, two people can go through the same door and arrive at different places.

You do have a point, and I did think about this in the initial proposal, but I think the initial proposal has already included a way to archive having like (access control lists, and other logic),by routing calls to different functions or outcomes based on the defined bytecode in each door.

---

**hiddenintheworld** (2024-03-21):

Can you address the implementation for deadlocks and livelocks, and how could we ensure rollback mechanisms function correctly even under different circumstances. I think this could be applied to CSP.

