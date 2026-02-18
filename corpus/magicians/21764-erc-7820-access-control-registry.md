---
source: magicians
topic_id: 21764
title: "ERC-7820: Access Control Registry"
author: shubh-ta
date: "2024-11-19"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7820-access-control-registry/21764
views: 254
likes: 2
posts_count: 10
---

# ERC-7820: Access Control Registry

This is the PR link: [Add ERC: Access Control Registry by shubh-ta · Pull Request #723 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/723)

**Motivation**: The need for a standardized access control mechanism across ethereum smart contracts is paramount. Current practices involve bespoke implementations, leading to redundancy and potential security flaws. By providing a unified interface for registering contracts and managing roles, this standard simplifies development, ensures consistency, and enhances security. It facilitates easier integration and auditing, fostering a more robust and interoperable ecosystem.

**Abstract**: The Access Control Registry (ACR) standard defines a universal interface for managing role-based access control across multiple smart contracts. This standard introduces a centralized registry where contracts can register themselves and designate an administrator responsible for managing roles within their contract. The ACR provides functionality to grant and revoke roles for specific accounts, either individually or in bulk, ensuring that only authorized users can perform specific actions within a contract.This EIP introduces an on-chain registry system that a decentralized protocol may use to manage access controls for their smart contracts.

The core of the standard includes:

- Registration and Unregistration: Contracts can register with the ACR, specifying an admin who can manage roles within the contract. Contracts can also be unregistered when they are no longer active.
- Role Management: Admins can grant or revoke roles for accounts, either individually or in batches, ensuring fine-grained control over who can perform what actions within a contract.
- Role Verification: Any account can verify if another account has a specific role in a registered contract, providing transparency and facilitating easier integration with other systems.

By centralizing access control management, the ACR standard aims to reduce redundancy, minimize errors in access control logic, and provide a clear and standardized approach to role management across smart contracts. This improves security and maintainability, making it easier for developers to implement robust access control mechanisms in their applications.

Specification:

```auto
pragma solidity 0.8.23;

interface IAccessControlRegistry {

    struct ContractInfo {
        bool isActive;
        address admin;
    }

    event ContractRegistered(address indexed _contract, address indexed _admin);
    event ContractUnregistered(address indexed _contract);
    event RoleGranted(address indexed targetContract, bytes32 indexed role, address indexed account);
    event RoleRevoked(address indexed targetContract, bytes32 indexed role, address indexed account);

    function registerContract(address _contract, address _admin) external;
    function unRegisterContract(address _contract) external;
    function grantRole(
        address[] memory targetContracts,
        bytes32[] memory roles,
        address[] memory accounts
    ) external;
    function revokeRole(
        address[] memory targetContracts,
        bytes32[] memory roles,
        address[] memory accounts
    ) external;
    function getRoleInfo(
        address targetContract,
        address account,
        bytes32 role
    ) external view returns (bool);
    function getContractInfo(
        address _contract
    ) external view returns (bool isActive, address admin);
}
```

**Rationale**: The IAccessControlRegistry interface aims to provide a standardized way to manage access control across multiple contracts within the ecosystem. By defining a clear structure and set of events, this interface helps streamline the process of registering, unregistering, and managing roles for contracts.

**Design Decisions**

- Decentralized Contract Registration
- No Central Owner: There is no central owner who can register contracts. This design choice promotes decentralization and ensures that individual contracts are responsible for their own registration and management.
- Bulk Role Assignment: Functions like grantRole and revokeRole allow for the assignment and revocation of roles to multiple accounts for multiple contracts in a single transaction. This bulk operation reduces gas costs and simplifies the process of role management in large systems.
- Event Logging: Emitting events for each significant action (registration, unregistration, role granting, and revocation) provides a transparent log that can be monitored and audited. This helps detect and respond to unauthorized or suspicious activities promptly.

## Replies

**radek** (2024-11-23):

Nice. Is this supposed to be a singleton on the particular chain, or do you envision that as a standard to be used within a set of contracts?

---

**MASDXI** (2024-11-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shubh-ta/48/13746_2.png) shubh-ta:

> event ContractUnregistered(address indexed _contract);

not sure about the event `ContractUnregistered` it does not include an admin address like `ContractRegistered`, I think it’s should be the same as `ContractRegistered` to increase visibility and transparency if the implementation contract has multiple admin.

---

**shubh-ta** (2024-11-24):

This standard is to used within a set of contracts for access control management.

[@radek](/u/radek) Also, if we set-up this singleton on the particular chain, it may create a single point of failure. Probably, we need to come-up with some core EIPs for such changes.

---

**shubh-ta** (2024-11-24):

[@MASDXI](/u/masdxi) Thanks for your feedback. I’ll make this change.

---

**shubh-ta** (2024-11-26):

[@MASDXI](/u/masdxi) I have made the changes as suggested. Let us know if you have any other feedback or questions.

---

**shubh-ta** (2024-12-11):

[@Arvolear](/u/arvolear)  [@xinbenlv](/u/xinbenlv) [@frangio](/u/frangio) Please provide your feedback on this ERC.

---

**Arvolear** (2024-12-11):

IDK, this sounds a bit too simple for a full-fledged ERC. If we are talking about real “Role Based Access Control (RBAC)”, something like [this](https://github.com/dl-solarity/solidity-lib/blob/master/contracts/access/RBAC.sol) with [that](https://github.com/dl-solarity/solidity-lib/blob/master/contracts/access/extensions/RBACGroupable.sol) groups extension is more like it.

With the current specification, I see no particular reason to stick to the ERC when the `AccessControl` contract is available by OpenZeppelin.

Can the global access control registry bring any public good?

---

**shubh-ta** (2024-12-12):

The ERC’s primary goal isn’t to replace OpenZeppelin’s AccessControl but rather to introduce a standardized interface that can work as a single point for handling access controls for multiple smart contracts. The global access control registry enables access control management for any protocol contracts.

---

**radek** (2025-03-05):

If such registry shall be deployed to any evm chain, this proposal might be relevant - [EIP potential proposal - Deterministic pure runtime bytecode deployment](https://ethereum-magicians.org/t/eip-potential-proposal-deterministic-pure-runtime-bytecode-deployment/23070)

