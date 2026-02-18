---
source: magicians
topic_id: 19179
title: Spitballing a JWT-Inspired Access Token System with RBAC
author: luke
date: "2024-03-12"
category: Magicians > Primordial Soup
tags: [security, security-token]
url: https://ethereum-magicians.org/t/spitballing-a-jwt-inspired-access-token-system-with-rbac/19179
views: 927
likes: 4
posts_count: 6
---

# Spitballing a JWT-Inspired Access Token System with RBAC

**TL;DR**

As a newcomer, I’m spitballing a strawman design for a JWT-inspired access token system tailored for smart contracts. It’s not a serious proposal but an attempt to learn from the community’s wisdom by putting forth an idea that might be flawed or overlook key considerations.

I’m learning and was reading the Access Control doc on OpenZeppelin site and I created a system like this described to manage access to a set of microservice HTTP APIs for a client a few years ago. On first blush, it feels like the idea would work with smart contracts, too.

Finally, this idea may already exist or has been shot down.

**Introduction**

In traditional web applications, JSON Web Tokens (JWTs) have become a widely adopted standard for securely transmitting information between parties, including access credentials and permissions. Drawing inspiration from JWTs, I propose a blockchain-based access token system tailored for Ethereum smart contracts. This system aims to streamline the management of access control and permissions within decentralized applications (dApps), while offering enhanced security, efficiency, and developer experience.

The core idea is to introduce a standardized token structure that encapsulates essential information such as the issuer’s contract address, intended contract address, bearer’s address, expiry time, and permissions encoded as bit flags. This structure borrows principles from JWTs but adapts them to the unique requirements and challenges of the Ethereum ecosystem.

By incorporating Role-Based Access Control (RBAC) principles, this system paves the way for a standard auth contract that manages users, group memberships, roles, and permissions (represented as bit offsets). This centralized access control mechanism could greatly simplify the development and management of complex permission models within dApps, fostering a more secure and interoperable ecosystem.

The proposed system addresses key concerns in decentralized environments, such as the risk of token theft and replay attacks, while optimizing for gas efficiency and scalability. By leveraging existing Ethereum standards and minimizing state-changing operations, this approach aims to provide a robust, cost-effective, and future-proof solution for access control in Ethereum smart contracts.

**Proposed Access Token Structure**

At the core of this system is the access token structure, designed to encapsulate all necessary information for secure and efficient permission management within Ethereum dApps. The structure draws inspiration from JWTs but is tailored to the unique requirements of smart contracts and decentralized environments. The proposed token comprises the following components:

1. Version Byte: Indicates the token structure version, allowing for backward-compatible updates and future evolution.
2. Integrity Checksum: A hash of the payload to rapidly reject modified copies.
3. Issuer Contract Address Bytes: The address of the contract issuing the token, establishing its origin and enabling trust verification.
4. Intended Contract Address Bytes: The specific contract address for which the token grants access, preventing misuse across different contracts.
5. Bearer Address Bytes: The address of the entity (user or contract) to whom the token grants permissions, mitigating the risk of token theft.
6. Expiry Time Bytes: Designates the token’s validity period, automating access control management and forcing periodic renewals.
7. Bit Flag Permissions: A compact representation of granted permissions, allowing granular control over the bearer’s authorized actions within the intended contract.

This structure balances gas efficiency considerations with code maintainability, utilizing either byte arrays or Solidity structs based on thorough analysis and community feedback.

**Token Issuance and Validation Process**

The proposed system follows a structured process to ensure secure and efficient token issuance, usage, and validation within the Ethereum ecosystem:

1. Token Request: An entity (user or contract) initiates a request for access by calling a designated function on the issuing contract, providing necessary credentials or identifiers.
2. Request Evaluation: The issuing contract evaluates the request based on predefined criteria, such as the requester’s identity, group memberships, roles, and other relevant factors defined by the access control model.
3. Token Assembly and Issuance: If approved, the issuing contract prepares and dynamically assembles the token data (version, addresses, expiry, permissions) and issues the token to the requester.
4. Token Presentation: To access protected functionalities or resources, the token bearer presents the token to the relying contract (specified by the Intended Contract Address Bytes).
5. Token Validation: The relying contract initiates a comprehensive validation process, including:

- Token Decoding: The token is fully decoded to extract its components.
- Expiry Check: The token’s expiry time is verified to ensure it is still valid.
- Integrity Verification: The token’s digest or checksum is calculated and validated to confirm its integrity.
- Bit Flag Check: Optional: Check the bit is set for the permission needed for the action being taken.
- Whitelist Check: The Issuer Contract Address Bytes are checked against a trusted whitelist of authorized issuers.
- Bearer Verification: The current caller’s address is verified against the Bearer Address Bytes to confirm they are the intended token bearer.
- EIP-1271 Signature Verification: The EIP-1271 isValidSignature function is called, passing the full token data. This step verifies the token’s authenticity with the issuer contract.
- isValidSignature - Permission Validation: The token’s bit flag permissions may be recomputed and compared.
- isValidSignature - Additional Checks: Any other relevant factors, such as the revocation or cessation of the token bearer’s rights or changes in their status since token issuance, are evaluated to ensure the token remains valid for the intended use.

1. Proceed With Rights: If all validation checks pass, the relying contract can proceed using just the permissions bit-flags portion of the token to check further access rights. Note the optional bit-flag check above is a fail-fast optimisation, however lacking a permission may not fail in your use-case but instead directs execution down a different path, e.g. feature flags.

This process leverages existing Ethereum standards, such as ERC-1271 for token validation, and incorporates robust security measures like bearer address verification and replay attack prevention. By relying primarily on read operations, the system is designed for gas efficiency and scalability.

**Standard RBAC Contract**

To streamline the management of permissions and roles, a standard Role-Based Access Control (RBAC) contract can be introduced. This contract would serve as a centralized authority for issuing access tokens based on a well-defined permission model, leveraging mappings to maintain user-group-role-permission relationships.

The RBAC contract would maintain core mappings associating user addresses with group identifiers, linking group identifiers to role identifiers, and mapping role identifiers to their corresponding permission offsets represented as bit flags.

The contract would expose a set of standard functions for managing users (e.g., `addUser`, `removeUserFromGroup`), groups, roles, and permissions, allowing for flexible and granular access control.

By integrating this standard RBAC contract, developers can benefit from a single, independently versioned contract for managing access control. The contract can serve as a trusted issuer of access tokens, ensuring tokens are generated with appropriate permissions based on the user’s group memberships and assigned roles.

This centralized approach simplifies the management of complex permission models and promotes consistency and interoperability across different decentralized applications (dApps) within the Ethereum ecosystem. By adhering to a standardized RBAC contract, developers can leverage a common access control framework, reducing development efforts and fostering a more secure and user-friendly ecosystem.

**Benefits and Advantages**

The proposed access token system for Ethereum smart contracts offers several key benefits and advantages:

1. Enhanced Security:

- Specificity of permissions and intended contract address prevents unauthorized access and replay attacks.
- Bearer’s address inclusion mitigates the risk of token theft and misuse.
- Integrity hash for tamper resistance.
- Potential for a standardised RBAC contract.

1. Gas Efficiency and Cost Optimization:

- Reliance on read operations for token validation minimizes gas costs.
- Compact data structures and efficient validation process optimize gas usage.

1. Improved Developer Experience:

- Intuitive design inspired by familiar concepts lowers the learning curve.
- Granular permission management with bit flag permissions simplifies access control logic.
- Clear documentation and community support to encourage widespread adoption.

1. Upgradability and Future-Proofing:

- Separation of concerns and shorter, focused contracts.
- Versioning system allows for backward-compatible updates and evolution.
- Independent upgradability of components facilitates continuous improvement.

1. Standardization and Interoperability:

- Potential to establish a community-adopted standard for access control.
- Interoperability across contracts and dApps through a standardized token structure.
- Simplifies access management across multiple applications and services.

Thanks for taking the time to read this through. As someone new to the Ethereum space, I want to emphasize that this is not a serious proposal but rather an attempt to spitball ideas and learn from the community’s feedback.

I recognize that this initial design may have flaws or overlook important considerations, which is why I’m presenting it as a strawman proposal. The purpose is to gather insights, critiques, and suggestions from more experienced people.

I appreciate your time and look forward to any feedback, whether it’s identifying weaknesses in the proposal, or why it may be *totally unworkable* or simply not idiomatic for Ethereum, or suggesting improvements or entirely different approaches.

Thanks

Luke

## Replies

**bumblefudge** (2024-03-12):

not to be the “prior art” queen of this fellowship of witches, but:

1.) how does this differ in goals and methods from [dan finlay’s delegatable](https://mirror.xyz/0x55e2780588aa5000F464f700D2676fD0a22Ee160/pTIrlopsSUvWAbnq1qJDNKU1pGNLP8VEn1H8DSVcvXM) framework for EVM?

2.) or, regardless of whether scope is EVM or all VMs, could this be a [UCAN](https://github.com/ucan-wg) adapter/toolchain rather than a net-new authZ DSL?

I think having an RBAC singleton makes a lot of sense, my question is whether it might get more adoption if it spoke Delegatable and/or UCAN and could thus pull in SDKs and libraries from those ecosystems to encode and decode its tokens ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

---

**luke** (2024-03-13):

Hello - thanks for reading. Prior art is mostly what I was looking for, and expecting to unearth. Sadly the use of the word “token” clouds my searches and the LLMs don’t seem to know!

I’ll need to look into the other stuff you wrote to try and understand it.

**Note** - The hash is pointless. It jolted me awake last night that there’s no private salt material to hash with, so anyone can just modify and rehash the contents.

---

**luke** (2024-04-12):

Posting a tweet to Dan Finlay today. I read some of the ideas he has but I don’t really understand, it lacks the necessary preamble I need to lead into it, and it’s too deep, touching on things that are within nodes. I’m not sure these two ideas are related or operate at different layers.

> Dan, I’m just a beginner with Ethereum. I posted this on Eth Magicians about permissions/JWT-like tokens, below.
>
>
> Your work seems similar but perhaps completely different, since you talk about UserOps and other deeper execution concepts like the Bundler that I only have a vague understanding of.
>
>
> My idea is perhaps way higher in the stack. Essentially it’s for obtaining a JWT-like structure from an issuer contract and then presenting it when calling methods on a contract.
>
>
> Both contracts would be written by the same team, but the issuer contract could be library code.
>
>
> The issuer could have roles > capabilities > permission flag offsets and user > roles, with functions to manage adding/removing.
>
>
> The token would, among other things, contain bit flags representing permissions to gain access to functionality in the called contract.
>
>
> Sorry to distract you. I recognised your name from a reply on the thread.

---

**mratsim** (2024-04-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/luke/48/11841_2.png) luke:

> As a newcomer, I’m spitballing a strawman design for a JWT-inspired access token system tailored for smart contracts. It’s not a serious proposal but an attempt to learn from the community’s wisdom by putting forth an idea that might be flawed or overlook key considerations.

Any JWT-inspired design need to overcome the serious concerns from cryptographers and cybersec folks and the implementation pitfalls they have:

- Cryptographer hate for JWT (This includes cryptographers writing RustCrypto, or maintaining go/crypto.
- Cryptographic Agility and Superior Alternatives - Dhole Moments
- JSON Web Tokens (JWT) are Dangerous for User Sessions—Here’s a Solution - Redis
- Why JWTs Suck as Session Tokens | Okta Developer
- Stop using JWT for sessions - joepie91's Ramblings
- 7 Ways to Avoid API Security Pitfalls when using JWT or JSON
- JWT: A Cryptographic Love Story with Security, Vulnerabilities, and a State of Confusion

---

**luke** (2025-11-18):

Hello - I’ve not had a look but I love this kind of revelation/challenge. I had no idea of any of this. Thanks.

