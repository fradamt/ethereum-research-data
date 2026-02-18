---
source: magicians
topic_id: 25434
title: "ERC-8004 Extension: Verifiable AI System Transparency for Trustless Agents"
author: SumeetChougule
date: "2025-09-13"
category: ERCs
tags: [erc-8004]
url: https://ethereum-magicians.org/t/erc-8004-extension-verifiable-ai-system-transparency-for-trustless-agents/25434
views: 178
likes: 1
posts_count: 1
---

# ERC-8004 Extension: Verifiable AI System Transparency for Trustless Agents

## 1. Abstract

This proposal introduces an optional `aiTransparency` object to the ERC-8004 AgentCard standard. It provides a structured framework for agents to make a series of **verifiable claims** about their underlying AI models and infrastructure. By linking these off-chain claims to on-chain proof mechanisms and leveraging the existing `ReputationRegistry` for ongoing audits, this extension enables a truly trust-minimized agent economy where performance, cost, and compliance can be programmatically verified.

## 2. Motivation

The ERC-8004 standard has provided a crucial foundation for on-chain agent identity. As the agent economy matures from simple interactions to high-value commercial services, a new requirement is emerging: the need to trust not just an agent’s identity, but the **underlying AI system it operates.**

An agent’s performance and cost are directly tied to its model (e.g., Llama-3 vs. GPT-4) and infrastructure (e.g., TEE-secured vs. standard cloud). Currently, these details are opaque, self-attested claims, leading to several problems:

1. Unverifiable Claims: An agent can claim to use a powerful model (e.g., GPT-5) while actually using a cheaper, less capable one. There is no way for a user or another agent to verify this.
2. Performance Uncertainty: Users and other agents cannot programmatically select agents based on guaranteed model performance.
3. Regulatory Gaps: Emerging regulations like the EU AI Act will require auditable proof of an AI system’s components, which off-chain claims cannot provide.
4. Lack of Trust in Open Stacks: Open-source models running on decentralized compute need a way to prove their integrity and differentiate themselves from black-box systems.

This proposal solves these issues by creating a standardized, optional, and verifiable framework for AI system transparency.

## 3. Specification

We propose extending the ERC-8004 AgentCard JSON object with a new, optional field: `aiTransparency`.

### 3.1. The aiTransparency Object & VerifiableClaim Structure

The `aiTransparency` object contains a list of **`VerifiableClaim`** objects. This array-based structure allows an agent to make multiple, discrete claims about its complex, multi-part AI system.  Each linking a specific claim to a proof mechanism.

```json
{
  // --- Existing ERC-8004 fields ---
  "registrations": [...],
  "trustModels": [...],

  // --- NEW: Optional Transparency Extension ---
  "aiTransparency": {
    "version": "1.0",
    "claims": [
      {
        "claimType": "model.instance",
        "model": {
          "type": "open-source",
          "identifiers": [
            {
              // Human-readable identifier for context
              "uri": "vmu:registry:huggingface:meta-llama/Llama-3-70B-Instruct",
              "proof": {
                "method": "self-attested",
                "proofURI": null
              }
            },
            {
              // Machine-verifiable identifier for cryptographic proof
              "uri": "vmu:hash:sha256:c3ab8ff13720e8ad...",
              "proof": {
                "method": "onchain-attestation",
                "proofURI": "eip155:1:0xAttestationRegistry/attestation/123"
              }
            }
          ]
        }
      },
      {
        "claimType": "infrastructure.tee",
        "infrastructure": {
          "provider": "abc",
          "teeType": "xyz"
        },
        // A top-level proof is used for non-model claims
        "proof": {
          "method": "provider-attested",
          "proofURI": "ipfs://QmSignedReceipt..."
        }
      },
      {
        "claimType": "model.endpoint",
        "model": {
          "type": "proprietary",
          "identifier": "gpt-5",
          "provider": "openai"
        },
        "proof": {
          "method": "tls-notary-proof",
          "proofURI": "ipfs://Qm..."
        }
      }
    ]
  }
}
```

### VerifiableClaim Fields:

- claimType: (Required) A string defining what is being asserted (e.g., model.instance,  model.endpoint).
- model: (Optional) An object describing the AI model. This field is REQUIRED for claimTypes like model.instance and model.endpoint.

type: A string distinguishing between open-source and proprietary.
- identifiers: (Conditional) For model.instance claims, this object MUST contain an identifiers array.

Each object in the array provides a different way to identify and verify the same model instance and MUST contain:

uri: A string that MUST conform to the Verifiable Model URI (VMU) scheme.
- proof: A Proof Object (see definition below) for that specific uri.

**`infrastructure`:** (Optional) An object describing the computational environment. This field is REQUIRED for `claimType`s like `infrastructure.tee`.
**`proof`:** (Conditional) A top-level `Proof Object`. This field is REQUIRED for claims that do not use the `model.identifiers` structure (e.g., `model.endpoint`, `infrastructure.tee`).

### The Proof Object Structure:

It is a standardized structure used to link a claim to its verification mechanism. It MUST contain the following fields:

- method: (Required) A string specifying the mechanism used (e.g., onchain-attestation, tls-notary-proof, self-attested).
- proofURI: (Optional) A string containing a link to the on-chain or off-chain proof artifact. This field MAY be null for methods like self-attested.

### 3.2. The Verifiable Model URI (VMU) Scheme

To provide a robust and extensible standard for identifying open-source AI models, this specification introduces the Verifiable Model URI (VMU) scheme. The **`uri` field** within an `identifier` object SHOULD conform to this structure.

The canonical format is `vmu:<method>:<value>`.

This standard defines three initial methods:

**1. `hash` (Content-Address):**

- Purpose: To provide a cryptographically unique identifier for a specific, bit-for-bit replica of a model file.
- Format: vmu:hash::
- Example: vmu:hash:sha256:c3ab8ff13720e8ad9047dd39466b3c8974e592c2fa383d4a3960714caef0c4f2

**2. `registry` (Human-Readable Identifier):**

- Purpose: To link a model to its canonical entry in a well-known public registry, providing discoverability and human-readable context.
- Format: vmu:registry::/[@]
- Example: vmu:registry:huggingface:meta-llama/Llama-3-70B-Instruct@main

**3. `fingerprint` (Behavioral-Address):**

- Purpose: To prove that a model behaves identically to a reference implementation, regardless of its file format or quantization. This is achieved by hashing the model’s outputs against a standardized benchmark suite of prompts.
- Format: vmu:fingerprint::
- Example: vmu:fingerprint:chaos-bench-v1:b1a2c3d4e5f6...

**Rationale for the Structure:** An AI model has multiple facets: a human-readable name, a cryptographic hash, and a behavioral profile. A robust transparency standard must be able to represent all of these without redundancy.

This specification achieves this through a single `VerifiableClaim` of type `model.instance`. This avoids the inefficiency of repeating claims and makes it semantically clear that all identifiers refer to the same conceptual model. The `model.identifiers` array provides a clean, efficient structure where each distinct identifier (`registry`, `hash`, `fingerprint`) is directly linked to its own specific `Proof Object`. This provides maximum clarity and verifiability while minimizing the size of the AgentCard.

### 3.3. Tiered Proof Mechanisms

The `proof.method` field allows the market to value stronger proofs more highly. This specification defines three initial tiers:

1. onchain-attestation (Highest Trust): For verifiable statements about an open stack. An on-chain contract (e.g., a generic AttestationRegistry) holds signed attestations from infrastructure providers who can use TEEs or ZKPs to prove statements like, “I am verifiably running the model identified by the VMU vmu:hash:sha256:c3ab8....”
2. tls-notary-proof (High Trust for Closed Models): For proprietary models. An agent uses a TLS notary service to generate a cryptographic proof that it received a specific response from an official API endpoint (e.g., api.openai.com).
3. self-attested/  provider-attested (Lowest Trust): The agent provides no cryptographic proof. This maintains backward compatibility and provides a baseline level of transparency, relying on the reputation system for trust.

### 3.4. Integration with ReputationRegistry for Ongoing Accountability

This system is made robust through the existing `ReputationRegistry`. We propose a standardized feedback context, **`aiSystem.audit.v1`**, which allows any agent to programmatically submit a “System Audit” on another agent’s transparency claims.

**The “System Audit” Feedback Loop:**

1. Authorization: A server agent calls the standard ReputationRegistry.acceptFeedback() to authorize a client agent, as per the ERC-8004 specification.
2. Feedback Submission: The client agent constructs a structured feedback object, linked via the FeedbackAuthID, and hosts it at its public FeedbackDataURI.

**Standardized “System Audit” Feedback Schema:**

```json
{
  "FeedbackAuthID": "eip155:1:{FeedbackAuthID}",
  "contextId": "aiSystem.audit.v1",
  "claimsVerified": [
    {
      "claimType": "model.instance",
      "verifiedStatus": "success",
      // The URI of the model the auditor *actually* observed.
      "observedModelURI": "vmu:hash:sha256:c3ab8ff13720e8ad...",
      "notes": "Observed model hash matches the agent's claim."
    },
    {
      "claimType": "infrastructure.tee",
      "verifiedStatus": "failure",
      "notes": "TEE attestation check failed during programmatic audit."
    }
  ],
  "overallResult": "partial_success", // Can be 'success', 'failure', or 'partial_success'
  "auditTimestamp": "2025-09-11T10:00:00Z"
}

```

This feedback loop creates a rich, on-chain history of an agent’s honesty regarding its infrastructure, enabling the creation of a “System Honesty Score” and ensuring the entire ecosystem is self-policing and economically secure.

---

### 4. Rationale

- Modular & Granular: The VerifiableClaim structure allows agents to transparently represent complex, multi-component AI systems.
- Optimized for Adoption: The standard is optional and backward-compatible. The tiered proof system and flexible VMU scheme allow all agents (open and closed) to participate at a level of transparency they are comfortable with.
- Composable with ERC-8004: It leverages the existing ReputationRegistry for accountability, making it a natural and seamless extension of the core standard without requiring new on-chain infrastructure.

---

### 5. Questions for the Community

1. Is the VerifiableClaim structure sufficient for initial use cases?
2. Are the proposed proof.method tiers clear and comprehensive?
3. What other claimTypes (e.g., dataset.instance, training.process) should be considered for future standardization?
4. For the vmu:registry scheme, which public registries (e.g., huggingface, replicate) should be formally included in the standard to ensure consistent identifiers?
