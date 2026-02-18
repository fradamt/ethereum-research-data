---
source: magicians
topic_id: 20642
title: "New EIP: Auditable JSON-RPC Specification"
author: blockjoe
date: "2024-07-25"
category: EIPs
tags: [json-rpc, interfaces]
url: https://ethereum-magicians.org/t/new-eip-auditable-json-rpc-specification/20642
views: 282
likes: 3
posts_count: 1
---

# New EIP: Auditable JSON-RPC Specification

Discussion topic for [EIP-XXXX: Auditable JSON-RPC](https://github.com/ethereum/EIPs/pull/8760)

#### Update Log

- 2024-07-25: initial draft with supporting resources Add EIP: Auditable JSON-RPC API Specification by blockjoe · Pull Request #8760 · ethereum/EIPs · GitHub

#### External Reviews

I will note the bias that anything before 2024-07-25 is seeded from resources from the Author(s). While these should not be taken explicitly as reviews for the proposed specification, they are here to highlight the importance of keeping these API standards changes visible in the EIP process.

> This section should list notable reviews the EIP has received from the Ethereum community. These can include specific comments on this forum, timestamped audio/video exchanges, formal audits, or other external resources. This section should be the go-to for readers to understand the community’s current assessment of the EIP. Aim for neutrality, quality & thoroughness over “cherry-picking” the most favorable reviews.

- 2022-12-05: “Unmitigatable exposure to theft of funds, XSS injection, and malware distribution due to the lack of idempotency in core Ethereum Execution JSON-RPC API logic in a compromised provider scenario.”, by Joseph Habel Original Disclosure
- 2024-07-08: “Accelerating the Distribution of a Verifiable Web”, by Jessica Daugherty (Presented by Joseph Habel) EthCC[7] Presentation

#### Outstanding Issues

- 2024-07-24: These changes belong in the Execution APIs Context

#### Discussing the Broader Communications Impact

While I understand for the sake of the Ethereum process that the adoption of these changes happen via the Execution APIs repository, and am happy to submit the test cases and updated OpenRPC specification there, I would like to open a broader discussion of what the process need be for signaling the need for these changes not just to the Execution Client developers, but rather all projects claiming to “Support Ethereum Compatibility”.

This specification, while I realize on a technical basis is irrelevant to the work of the core dev team, has engrained a set of developer anti-patterns that need to be addressed at a “cultural level” core to the experience of ecosystem and application developers.

I’m happy to shepard the technical changes through the proper process, but would like to discuss what the avenue here would be for signaling to projects that have inherited these anti-patterns in the goal of “Ethereum Support”. The EIP nomenclature acts as a very effective communication tool when discussing the importance of changes to other development teams outside of the EL client developers, in a way that an unnamable PR to a supporting repository cannot.

When seeking feedback about these changes in private conversations, the means of effectively communicating the importance comes from demonstrating proof of concept injection attacks. I have chosen not to publicly broadcast these to this point, but I would love feedback about if there’s a stronger middle ground here for herding the branching downstream changes that would need to happen in response.
