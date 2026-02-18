---
source: magicians
topic_id: 24632
title: "ERC-XXXX: ZK Privacy-Preserving Account Recovery - Withdrawn"
author: aryaethn
date: "2025-06-22"
category: ERCs
tags: [erc, wallet, zkp, recovery]
url: https://ethereum-magicians.org/t/erc-xxxx-zk-privacy-preserving-account-recovery-withdrawn/24632
views: 266
likes: 14
posts_count: 13
---

# ERC-XXXX: ZK Privacy-Preserving Account Recovery - Withdrawn

# [Discussion] ERC: ZK Privacy-Preserving Account Recovery

## Note

This ERC has been withdrawn. The reasons are clearly mentioned in the README.md of the [GitHub - aryaethn/Privacy-Preserving-Account-Recovery](https://github.com/aryaethn/Privacy-Preserving-Account-Recovery) repository. We sincerely thank you for your interest in this concept.

## Discussion

Hello everyone,

We are proposing a new ERC for a standardized, privacy-preserving account recovery mechanism using zero-knowledge proofs. We believe this addresses a critical gap in wallet security and user experience, and we are seeking community feedback on the initial draft.

---

## Abstract

Zero-knowledge Privacy-Preserving Account Recovery (zkPPAR) standardises an interface that enables Ethereum accounts to rotate their signing key by presenting a zero-knowledge proof (ZKP) of knowledge of one or more private recovery factors (password, e-mail account, or both) while leaking **no** guardian identities or social-graph metadata on-chain. The specification defines a lightweight *Guardian* registry for factor hashes and a *Verifier* contract that authorises key rotation for EOAs (EIP-7702) and ERC-4337 smart accounts.

We are also working on a minimal implementation of on-chain contracts and off-chain circuits for 2FA mode on Gmail DKIM signature for EOAs.

## Motivation

Key loss is a massive, unsolved problem, resulting in billions of dollars in permanently inaccessible assets. While solutions exist, they present significant trade-offs:

- Off-chain backups (seed phrases) are vulnerable to physical loss, theft, and phishing.
- On-chain social recovery (e.g., via ERC-4337) exposes the user’s social graph (their guardians) publicly on the blockchain, creating a significant privacy leak.
- Custodial solutions re-introduce trusted third parties, undermining the core principle of self-custody.

This proposal aims to create a new standard for on-chain, self-custodial recovery that preserves user privacy by leveraging ZKPs. A user can prove they know a password or have access to an email account without revealing the secret or the identity of any “guardian” service on-chain.

## Specification Overview

The proposed standard consists of two main on-chain components and one off-chain component.

1. Guardian Contract: A minimal, non-custodial registry where an account can store hashes of its chosen recovery factors (e.g., H(password), H(emailAddress)). This is done by the user before they lose their key.
2. Verifier Contract: A contract responsible for authorising key rotation. It works as follows:

It receives a ZKP from the user attempting recovery.
3. It verifies this proof against the public inputs, which include the hash of the recovery factor retrieved from the Guardian contract.
4. If the proof is valid, it executes the rotateKey function.
5. Off-Chain Circuits: ZK circuits where the user generates the proof. The circuit proves statements like H(myPassword) == onChainPasswordHash without revealing myPassword.

The `rotateKey` function is designed to be compatible with both standard EOAs (based on EIP-7702) and Smart Accounts (via their existing ownership update mechanisms, based on EIP-4337).

## Rationale & Design Choices

- Minimalism: The standard only defines the necessary interfaces for interoperability (Guardian storage layout, function signatures, events). It leaves the choice of ZK proving system (e.g., Groth16, PLONK), hash function, and circuit implementation to the developer.
- Privacy: By design, no private information or social graph data ever touches the chain. Only a proof and the new signer’s address are submitted.
- Flexibility: Supports single-factor (password or email) and two-factor (password and email) recovery modes. The recover function can accept proof data via calldata or, for larger proofs, via an EIP-4844 blob commitment.

## Discussion

We are particularly interested in any improvements, points, and questions on this ERC design.

Also, our minimal implementation will be available as soon as it is ready.

## Replies

**CypherVae** (2025-06-25):

Hmm for a privacy preserving mechanism, I’m not sure if the Guardian contract hinders this impact, especially if it is reliant on what I assume to be centralised operators like email providers (i.e. Gmail) for recovery methods…

---

**aryaethn** (2025-06-26):

Thank you for raising this important point, [@CypherVae](/u/cyphervae).

We appreciate your concern regarding the potential centralization risks introduced by relying on email providers (e.g., Gmail) as part of the recovery process. Let me clarify the design rationale and trade-offs we considered when incorporating this mechanism:

### 1. On-Chain Privacy via Hash Commitment

The Guardian contract **does not store any plaintext personal identifiers** such as passwords or email addresses. Instead, it stores **cryptographic hashes** of user-selected recovery factors. These hashes act as **commitments**, ensuring that no identifiable information or metadata is publicly visible or linkable on-chain.

### 2. Centralization vs. Usability Trade-Off

Your concern about relying on centralized services like Gmail is entirely valid. However, this decision was made after evaluating several design alternatives, each with its own trade-offs between **security, usability, and decentralization**:

#### 2.1 ZKP-Only Recovery (Pre-generated Proofs)

Our initial idea involved users pre-generating zero-knowledge proofs and storing them in a guardian contract. However, this created a significant **usability burden**, as users would need to safeguard both their private key and the precomputed proof. If either was lost, recovery would become impossible—defeating the purpose of the mechanism.

#### 2.2 Password-Only Recovery

Next, we explored a design using a single-factor password hash as the recovery anchor. However, this approach is **highly vulnerable to offline dictionary attacks**, particularly if users choose weak or short passwords. We concluded that requiring long, complex passwords would impair user experience and adoption.

#### 2.3 Email-Based Recovery (via DKIM Signatures or JWT tokens)

We ultimately opted for an email-based factor, leveraging **Gmail’s DKIM-signed emails or JWT token** to construct a **verifiable proof of email account access**. This method aligns with users’ existing mental models—many are already accustomed to using their email accounts for authentication flows across web applications, including web3 wallets via OAuth or AA sessions.

While this method does introduce a degree of reliance on centralized infrastructure, it offers a **pragmatic and user-friendly** recovery path. The recovery mechanism remains **non-custodial**, as the mail provider does not interact with the blockchain directly, nor does it hold or rotate keys—users prove access to their own accounts via off-chain ZKPs.

---

In summary, our design prioritizes **privacy on-chain**, while balancing **user experience and implementation feasibility**. We are also exploring pluggable factor types to reduce reliance on centralized services in future iterations.

We welcome further feedback and **alternative** ideas that may preserve both privacy and decentralization without sacrificing UX.

---

**ivanmmurcia** (2025-06-26):

Hey [@aryaethn](/u/aryaethn) thanks for this proposal. You’re in the way to create something great together with [@Arvolear](/u/arvolear)’s [EIP-7947: Account Abstraction Recovery Interface (AARI) - #11 by Arvolear](https://ethereum-magicians.org/t/eip-7947-account-abstraction-recovery-interface-aari/24080/11)

---

**aryaethn** (2025-06-26):

Hi [@ivanmmurcia](/u/ivanmmurcia),

Yeah. Great proposal by [@Arvolear](/u/arvolear). We wanted to make sure that our proposal is feasible, so at first we started implementing the circuits. After a week or two I saw EIP-7947 (AARI) submitted by him.

I hope both of these EIP/ERCs help the whole community in Private Key Recovery.

---

**CypherVae** (2025-10-27):

Have you got an ERC proposal number assigned? Where are you stuck?

---

**0xkoiner** (2025-10-27):

Nice, idea.

What the diff between your propose and ZKEmail impl. ?

Its very similar to what ZKEmail team run in prod.

---

**aryaethn** (2025-10-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xkoiner/48/15407_2.png) 0xkoiner:

> Its very similar to what ZKEmail team run in prod.

Hi [@0xkoiner](/u/0xkoiner) ,

Great mentioning. We’ll have to update our README.md and mention this project as a working product of our idea.

Thanks.

---

**aryaethn** (2025-10-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cyphervae/48/15406_2.png) CypherVae:

> Where are you stuck?

Hi [@CypherVae](/u/cyphervae),

Thank you for showing interest in our idea.

As discussed in this commit:



      [github.com/aryaethn/Privacy-Preserving-Account-Recovery](https://github.com/aryaethn/Privacy-Preserving-Account-Recovery/commit/7f8af5f5967827a619e0ba4853fb713633e1c621)












####



        committed 01:58PM - 31 Aug 25 UTC



        [![](https://avatars.githubusercontent.com/u/47050616?v=4)
          aryaethn](https://github.com/aryaethn)



        [+1
          -1](https://github.com/aryaethn/Privacy-Preserving-Account-Recovery/commit/7f8af5f5967827a619e0ba4853fb713633e1c621)













We were outrun by two other great proposals by [@Arvolear](/u/arvolear) (ERC-7947) and [@fumeng00mike](/u/fumeng00mike) (ERC-7969). Although our idea was a bit different to these ERCs, we decided to respect their great work, and withdraw our proposal, since it could be seen as a product of a combination of the two.

However, you can see our non-audited version of the working product in the [GitHub - aryaethn/Privacy-Preserving-Account-Recovery](https://github.com/aryaethn/Privacy-Preserving-Account-Recovery) repository.

Thanks again.

---

**Ankita.eth** (2025-11-05):

This is an impressive effort, and the vision behind zkPPAR resonates strongly with the direction self-custodial wallets need to evolve. Key loss remains one of the most critical unsolved problems in Ethereum, and approaching it with zero-knowledge proofs rather than custodial intermediaries or exposing social graphs is the right balance between usability and privacy.

The modular design—separating Guardian storage, Verifier contracts, and off-chain ZK circuits—shows foresight. It allows developers to adopt minimal standards while choosing their preferred proving systems and hash functions, which is crucial for ecosystem-wide interoperability. I particularly appreciate the dual support for EOAs (EIP-7702) and smart accounts (EIP-4337), signaling readiness for both current and future account abstractions.

Even though this ERC has been withdrawn, the approach is highly aligned with the future of privacy-preserving self-custody. Solutions like ZKEmail validate the feasibility of this approach, but formalizing a standard remains essential for widespread adoption. I’d be keen to see this extended to support additional recovery factors, multi-party proofs, and broader smart account compatibility—it could redefine how Ethereum handles account security and user privacy.

---

**aryaethn** (2025-11-05):

Thanks for your kind words, [@Ankita.eth](/u/ankita.eth).

We do believe that zkPPAR (actually its applications like the ZKEmail fantastic project) can be the future of self-custody without worrying about key loss.

However, as mentioned before, we were late, and proposing this as a separate ERC is of no benefit for the whole ecosystem.

---

**Ankita.eth** (2025-11-11):

Totally understand, and I appreciate the transparency. Even if the ERC itself is withdrawn, the concepts and modular design you’ve demonstrated are valuable reference points for future privacy-preserving recovery solutions. Excited to see how projects like ZKEmail continue to push this space forward!

---

**aryaethn** (2025-11-19):

Yes. I hope we are of help for the privacy preserving recovery community. Our codebase is fully open-source on my GitHub and everyone can utilize it. It is notable that our codes are not audited.

