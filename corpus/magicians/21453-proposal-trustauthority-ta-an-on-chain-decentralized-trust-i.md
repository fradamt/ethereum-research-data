---
source: magicians
topic_id: 21453
title: "Proposal: TrustAuthority (TA) - An On-Chain Decentralized Trust Infrastructure similar to Certificate Authority"
author: darwintree
date: "2024-10-24"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/proposal-trustauthority-ta-an-on-chain-decentralized-trust-infrastructure-similar-to-certificate-authority/21453
views: 79
likes: 6
posts_count: 1
---

# Proposal: TrustAuthority (TA) - An On-Chain Decentralized Trust Infrastructure similar to Certificate Authority

I’d like to propose a new ERC standard called TrustAuthority (TA). This standard aims to establish a decentralized trust infrastructure for Ethereum, similar to a Certificate Authority.

Here’s my concept:

Interface Definition (Draft):

```solidity
interface ITrustAuthority {
  function canTrust(address target) external view returns (bool);
  function canTrust(address target, address[] calldata trustChain) external view returns (bool);
  function canTrust(address target, uint maxChainLen) external view returns (bool);
  function isSubTrustAuthority(address target) external view returns (bool);
}
```

A TA can authorize addresses and sub-TAs. This standard allows wallets or on-chain smart contracts to **choose their own** trusted root TAs, thereby limiting their interaction scope with contracts and users, enhancing the overall ecosystem security.

**Relationship with ENS:**

While ENS primarily provides name resolution services, mapping human-readable names to Ethereum addresses, the TA system aims to build a multi-tiered trust network. Although both involve address identification, TA focuses more on providing a verifiable trust mechanism rather than just name resolution.

A key feature of the TA system is its **accountability**. If an address authorized by a TA engages in malicious behavior, the TA’s reputation would be affected, potentially leading users to revoke trust in that TA. This mechanism ensures TAs are motivated to maintain the integrity of their authorization lists and swiftly address any potential threats.

**Significance and Use Cases:**

1. Reducing phishing and fraud risks: The TA system allows users and smart contracts to interact only with verified addresses, significantly lowering the risk of being deceived by phishing sites or malicious contracts.
2. Additional security layer for DeFi projects: In the DeFi realm, TAs can be used to verify the authenticity of protocols, liquidity pools, and other critical components, reducing the risk of interacting with fake tokens or malicious contracts.
3. Facilitating enterprise-level adoption on Ethereum: The TA system provides enterprises with a trust model similar to traditional PKI systems, helping businesses migrate existing trust mechanisms to the blockchain.
4. Standardized trust mechanism for smart contract audits: Audit firms can act as TAs, issuing certifications for audited contracts, improving the accessibility and automation of audit results.

I kindly request feedback from community members, particularly regarding:

- Whether similar ERC proposals already exist
- Potential improvements to this proposal
- Possible implementation challenges

I look forward to hearing your thoughts and suggestions to collectively advance the Ethereum ecosystem.

Thank you for your time and consideration.
