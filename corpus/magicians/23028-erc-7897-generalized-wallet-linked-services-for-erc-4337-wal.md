---
source: magicians
topic_id: 23028
title: "ERC-7897: Generalized Wallet-Linked Services for ERC-4337 Wallets"
author: sullof
date: "2025-03-01"
category: ERCs
tags: [wallet, eip-4337]
url: https://ethereum-magicians.org/t/erc-7897-generalized-wallet-linked-services-for-erc-4337-wallets/23028
views: 172
likes: 1
posts_count: 5
---

# ERC-7897: Generalized Wallet-Linked Services for ERC-4337 Wallets

While developing **Sentinelle**, a service enabling NFT owners to designate beneficiaries for inheritance based on Proof of Life (PoL) using [ERC-7656](https://eips.ethereum.org/EIPS/eip-7656), we recognized a broader application: **recovering ERC-4337 wallets**. The key advantage of ERC-6551 and ERC-7656 is their ability to extend functionality for existing NFTs without requiring changes to the NFT itself. Inspired by this, we propose a new standard to deploy **wallet-linked services** for ERC-4337 wallets, inspired by ERC6551/7656 to enable modular extensibility for recovery mechanisms and other services.

We propose the introduction of a registry for **wallet-linked services**, allowing ERC-4337 wallets to attach external services (e.g., recovery, automation, compliance) in a permissionless and non-invasive manner. By leveraging **ERC-1167 minimal proxies** and **CREATE2**, it ensures deterministic deployments and backward compatibility with existing ERC-4337 wallets.

---

### Motivation

ERC-4337 (Account Abstraction) revolutionized smart accounts, but existing proposals like [ERC-6900](https://eips.ethereum.org/EIPS/eip-6900) focus on internal modules. This proposal generalizes service binding, enabling wallets to attach **external services** dynamically. Key benefits include:

- Modular Extensibility: Wallets can attach services without upgrades.
- Permissionless Innovation: Developers can create services for any ERC-4337 wallet.
- Backward Compatibility: Works with existing wallets like Safe, Argent, and Biconomy.

---

### Specification Overview

The proposal introduces a Registry interface for deploying and managing wallet-linked services. Key features include:

1. Deterministic Deployment: Services are deployed using CREATE2, ensuring predictable addresses.
2. Minimal Proxies: ERC-1167 proxies minimize deployment costs.
3. Immutable Wallet Linkage: Each service is permanently tied to a specific wallet.

#### Registry Interface

```solidity
interface IERC7897Registry {
    event ServiceDeployed(
        address deployedService,
        address indexed serviceImplementation,
        bytes32 salt,
        uint256 chainId,
        address indexed wallet
    );

    error DeployFailed();

    function deployService(
        address serviceImplementation,
        bytes32 salt,
        address wallet
    ) external returns (address service);

    function serviceAddress(
        address serviceImplementation,
        bytes32 salt,
        uint256 chainId,
        address wallet
    ) external view returns (address service);
}
```

#### Bytecode Structure

Each wallet-linked service is deployed as an ERC-1167 minimal proxy with the following bytecode structure:

```auto
ERC-1167 Header                      (10 bytes)
    (20 bytes)
ERC-1167 Footer                      (15 bytes)
                     (32 bytes)
                  (32 bytes)
                   (20 bytes)
```

#### Service Interface

Services SHOULD implement the `IERC7897Service` interface to expose the linked wallet’s details:

```solidity
interface IERC7897Service {
    function wallet() external view returns (uint256 chainId, address wallet);
}
```

#### Access Control

Services MAY implement access control to restrict critical operations to the wallet owner. For example:

```solidity
function owner() public view returns (address) {
    (, address wallet) = IERC7897Service(address(this)).wallet();
    return wallet;
}

modifier onlyOwner() {
    require(msg.sender == owner(), "Unauthorized");
    _;
}
```

---

### Use Cases

1. Account Recovery: Attach recovery mechanisms to wallets, enabling beneficiary nomination or multi-sig fallbacks.
2. Transaction Automation: Enable recurring payments, automated approvals, or scheduled transactions.
3. Regulatory Compliance: Integrate KYT (Know Your Transaction) or compliance monitoring services.

---

### Security Considerations

- Access Control: Services MUST implement robust access control to prevent unauthorized interactions.
- Upgradeability Risks: Use secure upgrade mechanisms (e.g., timelocks) to mitigate risks.
- Reentrancy: Follow best practices to prevent reentrancy attacks.

---

### Conclusion

This proposal extends the modularity of ERC-4337 wallets, enabling permissionless innovation and robust recovery mechanisms. By leveraging ERC-1167 and CREATE2, it ensures gas efficiency, backward compatibility, and deterministic deployments.

---

### References

- ERC-4337: Account Abstraction
- ERC-1167: Minimal Proxy Standard
- ERC-6900: Modular Smart Contract Accounts
- ERC-7656: Generalized Token-Linked Services

---

I am working on an official ERC proposal, while testing a reference implementation. Both will come soon.

Any suggestion, critic, opinion is very welcomed.

What do you think?

## Replies

**sullof** (2025-03-13):

I wonder if there is any advantage in giving to the address 32 bytes. On Solana and other non-EVM chains the address is often a bytes32 but this registry is supposed to work only on EVM-compatible chains and so I am quite confident that 20 bytes are enough, reducing the size of the deployed proxy of 12 bytes — that in some case may have an impact. Opinions?

---

**sullof** (2025-03-13):

I don’t have a use case right now but I was thinking that the `IERC7897Service` interface may use a different name for the function. The proposal has been set for 4337 accounts but the way it works, this can be used to associate a service to any deployed contract, so maybe there may be a more general name for the function. Instead of `wallet` which is very specific, it may be, for example, `account`, which works similarly, or `owningContract`, which is less elegant but very general.

---

**sullof** (2025-03-13):

I’m considering canceling this new proposal and instead modifying ERC7656 to be more general. Currently, ERC7656 is designed specifically for NFTs, but with a small adjustment, it could also support ERC4337 accounts.

Instead of:

```auto
ERC-1167 Header               (10 bytes)
    (20 bytes)
ERC-1167 Footer               (15 bytes)
              (32 bytes)
           (32 bytes)
     (32 bytes)
           (32 bytes)
```

The modified structure would be:

```auto
ERC-1167 Header               (10 bytes)
    (20 bytes)
ERC-1167 Footer               (15 bytes)
              (32 bytes)
           (32 bytes)
     (20 bytes)
             (1 byte)
           (32 bytes)
```

Where `hasId` is `true` for NFTs.

This allows the registry to deploy a proxy with the full dataset for NFTs, while for ERC4337 accounts, it can deploy using:

```auto
ERC-1167 Header               (10 bytes)
    (20 bytes)
ERC-1167 Footer               (15 bytes)
              (32 bytes)
           (32 bytes)
     (20 bytes)
             (1 byte)
```

where `hasId` is `false`.

This approach reduces the added overhead in ERC7897 to just 1 byte while keeping the logic unified under ERC7656. While it would increase the complexity of the registry code, it avoids maintaining two separate ERCs that function in essentially the same way.

---

**sullof** (2025-03-22):

I am withdrawing this ERC, because I am incorporating the concept behind ERC7897 in ERC7656. Follow the conversation at



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sullof/48/3709_2.png)
    [ERC-7656: Variation to ERC6551 to deploy any kind of contract linked to an NFT](https://ethereum-magicians.org/t/erc-7656-variation-to-erc6551-to-deploy-any-kind-of-contract-linked-to-an-nft/19223/17) [ERCs](/c/ercs/57)



> I set up a new repo for the reference implementation of ERC-7656 at
>
> It has been taken from the Cruna Protocol implementation, which also has full coverage of the smart contracts.
> A canonical version has been deployed at the address
> 0x7656f0fB4Ca6973cf99D910B36705a2dEDA97eA1
> using Nick’s Factory with the following salt:
> 0x765600000000000000000000000000000000000000000000000000000000cf7e
> on mainnets (Etherum, Polygon, BNB Chain) and on testnets (Avalanche Fuji and Celo Alfajores).
> The code …

for more details about it.

