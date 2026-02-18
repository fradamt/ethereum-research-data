---
source: magicians
topic_id: 25044
title: Safe and Version-Agnostic Deployment to Consistent Addresses Across EVM Networks
author: Andriian
date: "2025-08-08"
category: Magicians > Primordial Soup
tags: [proxy-contract, create2, contract-deployment]
url: https://ethereum-magicians.org/t/safe-and-version-agnostic-deployment-to-consistent-addresses-across-evm-networks/25044
views: 53
likes: 3
posts_count: 1
---

# Safe and Version-Agnostic Deployment to Consistent Addresses Across EVM Networks

This topic outlines a deployment scheme that enables deploying a set of contracts to consistent (identical) addresses across multiple networks, reducing the complexity of network-specific address configurations in client applications.

Consistent addresses are not tied to a specific contract’s initialization bytecode. A deployer has full control over which contract is deployed to a given address, allowing for consistent or distinct addresses as needed.

The process is robust and minimizes the risk of errors:

- Prevents accidental deployment of incorrect contracts
- Ensures addresses remain stable across versions
- Protects against front‑running
- Allows onboarding new networks at any time later without disrupting the scheme

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/f/f1ccb5b52ae5fc6cdaf2188daf04f3056d5e16eb_2_690x281.png)image738×301 46.7 KB](https://ethereum-magicians.org/uploads/default/f1ccb5b52ae5fc6cdaf2188daf04f3056d5e16eb)

### Deployment Flow (3 Steps)

#### Step 1. Prepare a Proxy Contract

For each target contract intended for consistent addressing, deploy a proxy contract. This ensures that the initialization bytecode has a predictable and deterministic structure.

In this explanation, we use OpenZeppelin’s [TransparentUpgradeableProxy](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/proxy/transparent/TransparentUpgradeableProxy.sol).

You can change the proxy admin owner to zero address if you don’t need it to be upgradeable or use a contract with other delegation logic. While it’s possible to freeze the proxy’s Solidity version and compiler settings to ensure consistent init bytecode, a more robust approach is to hardcode the proxy’s initialization bytecode directly in the configuration.

#### Step 2. Deterministic Management of Constructor Arguments

We need to deterministically manage the smart contract constructor arguments, which are concatenated at the end of the init bytecode. They should be the same for each of the consistent addresses.

The TransparentUpgradeableProxy constructor takes:

```auto
constructor(
    address _logic,
    address initialOwner,
    bytes memory _data
)
```

The `address _logic` parameter refers to the address of the initial implementation contract behind the proxy. However, using the actual implementation here is not ideal. Even if deployed deterministically using CREATE2, there’s no guarantee that the implementation init bytecode won’t change over time, especially across different compiler versions or optimization settings.

There’s a simpler and more robust approach: use a dummy implementation contract. This contract should do nothing and always return successfully, regardless of the calldata it receives (the significance of this behavior will be explained later).

The dummy contract must be deployed to a deterministic address using CREATE2 and should serve as a singleton per network across the entire deployment scheme. It can be extremely minimal, containing just a few opcodes to ensure it’s valid and always succeeds.

For example, consider the following init bytecode: `0x6005600C60003960056000F360006000F3`

This results in deployed runtime bytecode: `0x60006000F3`

which corresponds to:

```auto
    • PUSH1 0x00
    • PUSH1 0x00
    • RETURN
```

This minimal contract always returns an empty byte array and never reverts, regardless of the calldata.

The `address initialOwner` must also be consistent across all deployments in the scheme.

Security note: if this private key is compromised, an attacker could front‑run deployments on new networks.

The `bytes memory _data` argument contains the calldata for the initial call to the implementation contract, executed from the proxy constructor. Since the dummy implementation always succeeds and never reverts, we have flexibility here. This field becomes a tool for differentiating consistent addresses per contract. For instance, to distinguish a `Governance` and a `Vault` contract, you can use calldata corresponding to the UTF-8 hex encodings of strings like “consistent.governance” and “consistent.vault”.

At this point, you have identical proxy init bytecode and constructor arguments for each contract in your deployment scheme, ensuring deterministic and consistent addresses across networks.

#### Step 3. Deploy the Real Implementation

Finally, deploy the actual implementation contract and upgrade the proxy to point to it.

[![image](https://ethereum-magicians.org/uploads/default/original/2X/4/4a4ef2852e679cc33ced0c7dd6037ada301fd27f.png)image454×290 43.5 KB](https://ethereum-magicians.org/uploads/default/4a4ef2852e679cc33ced0c7dd6037ada301fd27f)

### Implementation Example

An implementation example can be found in the [Iden3 protocol contracts](https://github.com/iden3/contracts/tree/master/ignition/modules/deployment), however, it does not yet serve as a universal deployment tool for arbitrary contract systems.

### Enhancement Considerations

- For CREATE2 singleton factories, you can either use CreateX or opt for a permissionless CREATE2 factory, which offers several improvements over the former.
- All deployment transactions, up to and including the proxy deployment, can be executed from any address, without requiring access to the initialOwner’s private key. The only restricted operation is the final upgrade to the real implementation. This separation of responsibilities can simplify deployment system architecture by minimizing reliance on the owner’s private key during the deployment phase. For example, your system can distinguish between deployer roles and a superadmin role.
- Deployment management can be further improved by converting the initialOwner address into a Smart Account that supports delegation via EIP-7702. This allows for more flexible and secure control over upgrade operations, such as delegating upgrade rights to different actors or automating workflows, without exposing the private key of the original owner.
- It’s important to note that some EVM-compatible networks, such as zkSync, may use a different CREATE2 hashing mechanism. As a result, deterministic deployments on these networks yield different proxy addresses, breaking address unification.
- A custom CREATE2 salt can be assigned to each consistent address, enabling the creation of easily recognizable addresses. For example, 0xAAAA… can be an address for a Vault contract and 0xBBBB… for a Governance contract. This can simplify daily development and integration efforts.
