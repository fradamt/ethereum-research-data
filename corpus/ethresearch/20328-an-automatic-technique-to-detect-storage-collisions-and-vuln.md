---
source: ethresearch
topic_id: 20328
title: An Automatic Technique to Detect Storage Collisions and Vulnerabilities within Solidity Smart Contract
author: WaizKhan7
date: "2024-08-23"
category: Security
tags: [data-structure]
url: https://ethresear.ch/t/an-automatic-technique-to-detect-storage-collisions-and-vulnerabilities-within-solidity-smart-contract/20328
views: 441
likes: 1
posts_count: 1
---

# An Automatic Technique to Detect Storage Collisions and Vulnerabilities within Solidity Smart Contract

Storage collisions and vulnerabilities within Ethereum smart contracts can lead to unexpected issues like freezing funds, escalating privileges, and financial asset theft. A storage collision occurs when two different storage structs unintentionally use same storage slot(s), or the slot layout is changed during the upgrade of implementation contract. These collision vulnerabilities have been detected in large numbers (worth millions of dollars) in a [recent study](https://www.ndss-symposium.org/ndss-paper/not-your-type-detecting-storage-collision-vulnerabilities-in-ethereum-smart-contracts/) within smart contracts deployed on the Ethereum network.

In this topic, we propose a more accurate and complete technique to detect storage vulnerabilities and collisions in Solidity smart contracts. And encourage the Ethereum community to **provide feedback on the proposed technique**.

### Introduction

We are working on a solution based on advanced static analysis techniques that can identify vulnerabilities within the deep storage of Ethereum Solidity smart contracts. We aim to detect storage collisions in proxy contracts deployed on the Ethereum network like ERC-2535 (Diamond/Multi-Facet Proxy), ERC-1822, upgrade proxy pattern, etc., as complex proxy contracts are more likely to experience a storage collision, like during the upgrade of implementation or facet contracts.

[N. Ruaro et al.](https://www.ndss-symposium.org/ndss-paper/not-your-type-detecting-storage-collision-vulnerabilities-in-ethereum-smart-contracts/) analyzed Ethereum contracts using contract bytecode to detect storage collisions and reported 14,891 vulnerable contracts. Their technique was able to identify storage slot types correctly with an accuracy of 87.3%. Whereas, we aim to build a solution that will use source code to accurately analyze the storage layout and slot types of the contract. Furthermore, we will also analyze dynamic arrays, mapping variables, and complex nested structs in our analysis.

Suppose a collision occurs on the state variables’ base slots, our approach will allow us to identify the impact of the collision on dynamic arrays and mapping variables declared consecutively, and arrays data type or mappings key types are same which is a common practice in large contracts like gaming contracts.

As shown in the below example code, the slot layout was changed during the contract upgrade, and since `token_uris` and `token_version` have same key types and data types, both variables will return each other’s data after the upgrade due to collision.

```auto
library ImplementationStorage1 {
    struct AddressSlot {
        address owner; // slot n+0
        mapping(uint256 => string) token_uris; // slot n+1
        mapping(uint256 => string) token_versions; // slot n+2
    }

    function getAddressSlot(bytes32 slot) internal pure returns (AddressSlot storage r) {
        assembly {
            r.slot := slot
        }
    }
}

// updated code
library ImplementationStorage2 {
    struct AddressSlot {
        address owner; //slot n+0
        mapping(uint256 => string) token_versions; // slot n+1 (shld be token_uris)
        mapping(uint256 => string) token_uris; // slot n+2 (shld be token_versions)
    }

    function getAddressSlot(bytes32 slot) internal pure returns (AddressSlot storage r) {
        assembly {
            r.slot := slot
        }
    }
}
```

`token_uris` accessing `token_versions` and vice-versa after the upgrade.

```auto
       (before upgrade)                        (after upgrade)
      _________________                      _________________
     |     Proxy       |                     |     Proxy       |
     |_________________|                     |_________________|
     | * IMPLEMENT_SLOT| --> NFTManager1     | * IMPLEMENT_SLOT| --> NFTManager2
     | * ADMIN_SLOT    |                     | * ADMIN_SLOT    |
     |_________________|                     |_________________|
     | + upgradeTo()   |                     | + upgradeTo()   |
     | + changeAdmin() |                     | + changeAdmin() |
     |_________________|                     |_________________|
              |                                       |
              v                                       v
      _________________                       _________________
     |   NFTManager1   |                     |   NFTManager2   |
     |_________________|                     |_________________|
     | - owner         |                     | - owner         |
     | - token_uris    | **** collision **** | - token_versions|
     | - token_versions| **** collision **** | - token_uris    |
     |_________________|                     |_________________|

```

We plan to build a technology that will automatically detect all storage collisions within a Solidity smart contract.

#### Methodology

We have structured our development plan into three distinct phases, outlined as follows:

- Automatic State Variable Detector and Slot Layout Calculator

In this phase, we focus on developing an automatic state variable detector and slot layout calculator. This component will facilitate the identification of state variables within smart contracts and determine their corresponding slot layout. By automating this process, we aim to streamline the initial analysis procedures.

Sample output of Slot Calculator

```auto
slot 0 - mapping ds.selectorToFacetAndPosition[bytes4] = FacetAddressAndPosition;
slot 1 - mapping ds.facetFunctionSelectors[address] = FacetFunctionSelectors;
slot 2 - address [] ds.facetAddresses;
slot 3 - mapping ds.supportedInterfaces[bytes4] = bool;
slot 4 - address ds.contractOwner;
slot 5 - mapping ds.tempSelectorsNested[uint256] = FacetAddressAndPosition;
slot 6 - FacetAddressAndPosition [] ds.FacetAddressAndPositionArray;
slot 7 - mapping ds.tempMapping[uint256] = uint256;
slot 8 - mapping ds.tempMapping2[address] = uint256;
```

- Mapping Keys Analyzer and Slot Calculator of Complex Variables

Building upon the foundation established in phase 1, in this phase we will first extend the slot calculator capability to calculate the slots of complex variables and their entries (for all data types) i.e. slots of mapping keys, dynamic array, complex struct, mappings with complex struct as value.

This component will also include the approximation of all keys used in mapping variables for saving data using advanced static analysis techniques. By accurately approximating keys and calculating entries, we seek to enhance the precision and breadth of storage slot calculation methodology, which will help detect storage collision within deep storage data of a smart contract.

- Collision Detector for State Variables and Complex Variables All Entries Slots

The final phase of our methodology focuses on implementing a collision detector for both state variables and complex variable slots. This critical component will identify any potential collisions or conflicts within any type of state variables and their associated variable(s)/value(s) slots. By detecting and addressing collisions, we aim to ensure the integrity and reliability of smart contracts.

We aim to develop a robust and comprehensive methodology for smart contract storage collision detectors, by systematically progressing through above discussed three development phases.

#### Conclusion

The development of our solution will allow developers to ensure that their contract has no potential storage collisions before deployment. It will also be able to detect storage collisions within deep storage of deployed smart contracts and can help in securing contracts worth millions of dollars.
