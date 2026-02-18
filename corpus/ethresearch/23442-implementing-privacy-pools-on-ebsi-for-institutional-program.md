---
source: ethresearch
topic_id: 23442
title: Implementing Privacy Pools on EBSI for Institutional Programmable Privacy & Compliance
author: EugeRe
date: "2025-11-13"
category: Applications
tags: [transaction-privacy, identity, zero-knowledge]
url: https://ethresear.ch/t/implementing-privacy-pools-on-ebsi-for-institutional-programmable-privacy-compliance/23442
views: 521
likes: 4
posts_count: 3
---

# Implementing Privacy Pools on EBSI for Institutional Programmable Privacy & Compliance

## Abstract

Privacy Pools may enable users to withdraw assets only if their deposit belongs to an approved association set (a Merkle tree of deposits maintained by an Association Set Provider). This work investigates whether this tool could operate in tandem with an Institutional Identity Framework supported by the European Blockchain Services Infrastructure project ([EBSI](https://ec.europa.eu/digital-building-blocks/sites/spaces/EBSI/pages/590447955/What+is+EBSI)) running on Besu. This setup requires a significant compromise between Ethereum’s permissionless environment and EBSI’s permissioned design but still is a significant application framework for institutional clients.

EBSI nodes are hosted and operated by participants approved by the EUROPEUM‑EDIC and must follow some off-chain governance rules. The system consists of trust registers (e.g., DID Registry, Trusted Issuers), while credential exchanges happen off-chain. We therefore propose adapting Privacy Pools to fit EBSI’s constraints by treating the association set and verifier contract as a public good service managed by a list of institutional stakeholders through the EDIC, using Verifiable Credentials and off-chain proof generation. This research outlines how the Ethereum protocol and its community can serve as a “public good” to institutional environments, specifically in the EU context.

Outside of the EU context, there are other institutional identity networks around the globe, such as [Lacchain](https://lnet.global/en/) in Latam and Caribbean zones, so defining a standardized way for interacting with such institutional projects may be beneficial for Ethereum institutional adoption globally!

The work also aligns quite well with [Project Kohaku](https://ethereum.github.io/kohaku) and we could envision some sort of institution/enterprise-based services framed in the project scope. From a business-wise perspective, we could see enterprises and institutions accessing privacy pools for compliant on/off ramping as a sort of “virtual ATMs” for accessing digital asset services.

Here is the [link](https://www.notion.so/Implementing-Privacy-Pools-on-EBSI-2a08eee793d08095a44be2f05806d76f?source=copy_link) to a Notion page for full reading in case you want to go deeper. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

## Why It Matters for Ethereum?

- Institutional adoption through compliance. Ethereum’s privacy tools often clash with regulatory requirements. Adapting privacy pools to EBSI illustrates how zero‑knowledge proofs can coexist with regulated infrastructure. EBSI’s framework uses W3C Verifiable Credentials and wallet endpoints to let users prove attributes without exposing personal data. Integrating Privacy Pools in this environment demonstrates a path for compliant privacy tooling that could encourage institutions to build on Ethereum.
- Public‑good infrastructure bridging institutions. EBSI is not a commercial blockchain; it is the first EU‑wide infrastructure driven by the public sector where a network of stakeholders (administrations, financial institutions, and universities maintain trust in off-chain environments), and it is designed to deliver cross‑border services for public administrations, businesses, and citizens. Its architecture, built on a network of distributed nodes across Europe and governed by EUROPEUM‑EDIC, shows how blockchain could function as a public good. By exploring Privacy Pools within EBSI, we show how Ethereum’s technology and tooling can support financial institutions and government agencies in a regulated setting. This, sends a signal that Ethereum is not just a platform for speculative activity but a foundation on which financial institutions (FIs) and governments can build trusted, interoperable services.
- Synergies with identity standards. EBSI uses Decentralized Identifiers (DIDs) and Trusted Issuers for credential management. A privacy‑preserving compliance tool that can query credential status lists and authorize users through short‑lived tokens bridges Ethereum’s anonymity techniques with modern identity standards. This synergy could enrich the Ethereum ecosystem with selective disclosure mechanisms and strengthen the case for embedding identity-aware privacy.
- Pathway for compliant anonymity. Regulators increasingly demand that crypto‑asset service providers accompany transfers with information about originators and beneficiaries. EU Regulation 2023/1113 requires CASPs to transmit such data. By designing Privacy Pools that check association‑set membership off‑chain and issue proofs through trusted ASPs, Ethereum developers can help meet these obligations without storing personal data on-chain.

## Why It Matters for Institutions and the EU?

- Balancing privacy with oversight. EBSI’s ledger is designed to avoid storing personal data, yet institutions still need assurance that funds come from lawful sources. The Privacy Pools design allows users to prove that a deposit is part of an approved association set maintained by an authorized provider, without revealing their entire transaction history. Regulators could receive aggregated metrics rather than direct transaction details, aligning with the EU’s data minimization principles.
- Leveraging existing trust infrastructure. EBSI’s Trusted Issuer and DID registries already support cross‑border credential verification. A privacy‑preserving mixer built as an EDIC‑approved service would build on these registers: participants would receive Verifiable Credentials from trusted issuers, generate zero‑knowledge proofs off‑chain, and present them to the network via the Authorisation API. This harnesses existing EU infrastructure rather than duplicating it.
- Demonstrating regulatory leadership. The EU has been a pioneer in digital identity and data protection. Adapting Privacy Pools to EBSI shows that Europe’s frameworks can support advanced crypto privacy tools without undermining AML/KYC requirements and may influence other jurisdictions to adopt similar architectures.
- Encouraging safe innovation. By working within the EDIC’s governance (where new contracts must be approved and deployed by the EBSI core team) and adhering to GDPR and Transfer of Funds Regulation obligations, institutions can experiment with privacy‑enhancing technologies without risking non‑compliance. This creates a sandbox for innovation in DeFi and payments that respects European rules.

## Call to Action!

The research highlights both promise and complexity, its a work in progress and I think it could be an interesting topic for:

1. Ethereum researchers to continue exploring privacy‑preserving compliance. How can association sets be maintained off‑chain without centralising trust ? What cryptographic primitives (e.g., Halo2, STARKs) best suit regulated environments? Your feedback on our model and its assumptions is welcome.
2. European institutions and regulators to engage with the open‑source community. Approving a Privacy Pools‑like service on EBSI would require EDIC endorsement and integration into the Authorisation API. We encourage stakeholders to participate in design discussions and consider pilot programmes.
3. Developers & Community Members to prototype tools. Build off‑chain proof services compliant with EBSI’s APIs and experiment with verifiable presentations. Evaluate how association‑set updates and credential revocations could be governed transparently.

## Further Areas For Research

A further research direction could assess how [Private Proofs of Innocence](https://docs.railgun.org/wiki/assurance/private-proofs-of-innocence) (POI), such as those developed by the Railgun community, might complement the operation of authorized Association Service Providers (ASPs). These zero-knowledge commitments could provide cryptographic assurance about asset provenance, verifying that deposits and withdrawals do not originate from tainted sources, while ASPs would remain responsible for coordinating institutional identity checks and enforcing compliance logic on-chain. Investigating how POI frameworks and institutional identity layers (e.g., EBSI) can interoperate offers a pathway to richer, modular compliance architectures that combine verifiable identity and verifiable asset integrity.

Also, another area of interest for further research would be investigating how, in the context of institutional-based systems identity frameworks such as EBSI combined with privacy-preserving transaction tools like Association Service Providers (ASPs) and Private Proofs of Innocence (POI) could represent a compliance-oriented feature acting in the execution layer. This can harmonize inclusive future proposal implementations (e.g., [FOCIL](https://ethereum-magicians.org/t/eip-7805-committee-based-fork-choice-enforced-inclusion-lists-focil/21578)), which aims to guarantee fair and censorship-resistant transaction inclusions at the consensus layer. In short, a sort of compliance-verified transaction flow for institutional setup that could benefit from wider inclusion guarantees.

By bringing together privacy experts, Ethereum developers, and European policymakers, we can create infrastructure that preserves both anonymity and accountability while ensuring institutional compliance and wide outreach.

I would also like to thank the EF [0xbow](https://0xbow.io/), [Iden3](https://iden3.io/), teams for their support and technical guidance during this research, especially [@Julian](/u/julian) [@OBrezhniev](/u/obrezhniev) [Mike](https://www.linkedin.com/in/mike-mccabe-6a78a2146/?lipi=urn%253Ali%253Apage%253Ad_flagship3_profile_view_base%253BsnHTLRJxQaWzKp0TzEg6vA%253D%253D) and [Jose](https://www.linkedin.com/in/josempanizo/) for supporting the review.

Let’s make privacy‑preserving compliance not just an ideological dream but a possible reality in worldwide institutional environments!

## Replies

**andreolf** (2025-11-13):

This is a thoughtful exploration of how institutional verification layers (EBSI identity proofs, ASP logic and POI-style checks) could interface with Ethereum’s evolving block production pipeline. One point worth highlighting is the relevance of upcoming protocol changes like **PeerDAS** and **enshrined PBS (ePBS)** both of which will seem to arrive long before any fork-choice–level mechanisms like FOCIL. Institutional verification systems and Ethereum protocol upgrades are converging around modular, proof-oriented transaction flows. This kind of applied research helps ensure that compliance-driven architectures can integrate smoothly into Ethereum’s permissionless block production model without compromising decentralization or privacy.

---

**EugeRe** (2025-11-13):

[@andreolf](/u/andreolf) thanks for this! I think we are fully aligned with a sense of utility vision that developing a standardized interaction between privacy preserving features and institutional networks in the execution layer can help to syncronize or streamline blocks pipeline.

