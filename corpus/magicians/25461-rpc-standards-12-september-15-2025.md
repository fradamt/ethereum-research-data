---
source: magicians
topic_id: 25461
title: RPC Standards #12 | September 15, 2025
author: system
date: "2025-09-15"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/rpc-standards-12-september-15-2025/25461
views: 59
likes: 0
posts_count: 3
---

# RPC Standards #12 | September 15, 2025

### Agenda

- Handling open PRs and issues: Discuss strategies for tackling stale PRs and old issues, agree on a good structure for maintaining the repo, and prioritize merging the open PRs currently in  execution-apis repo

**Meeting Time:** Monday, September 15, 2025 at 15:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1724)

## Replies

**system** (2025-09-15):

### Meeting Summary:

The meeting focused on preparing for an upcoming livestream and discussing the RPC Standard Code 12 event scheduled for September 2025. The team addressed various technical issues including stale PRs, test failures related to Hive RPC compact and execution API, and RPC compatibility across different Ethereum forks. The discussion concluded with updates on standardizing error codes and plans to revamp documentation, with emphasis on creating more comprehensive and accessible resources for implementation teams.

**Click to expand detailed summary**

The meeting began with Akash and Mercy discussing the setup for a livestream on the Ethereum Protocol YouTube channel and ECH Institute X handle. Mercy mentioned that Zane was expected to join shortly. The participants confirmed their well-being, and the meeting transitioned to starting the stream, with Mercy welcoming everyone to the RPC Standard Code 12 event scheduled for September 15th, 2025.

Mercy raised concerns about the large number of stale PRs in the repository and requested discussion on moving forward with them. Kira, who is on the testing team, explained that her focus has been on getting Fusaka ready, but she plans to review the PRs in the coming week, prioritizing the Hive RPC compact test passing. Kira detailed the issues with failing Hive tests, noting that some are due to ordering problems and require changes on both the Execution API side and client sides. Mercy offered to help address the technical aspects of the HiveTest issues and requested more information to assist with moving these items forward.

The team discussed issues with RPC Compact and execution API tests, particularly focusing on problems with ET simulate and schema validation. Zane explained that the execution API spec schema had changed, causing issues with array/object formatting and negative testing. Simsonraj identified that different clients were failing for different reasons, with ET simulate being a common failure point due to method availability. The team agreed that reaching out to implementers for proper feedback would be the best next step to address these ongoing test failures.

The team discussed RPC compatibility issues and potential solutions for handling different Ethereum forks. Keri identified the need to determine which test failures are due to Execution API issues versus client-side problems before contacting client developers. Zane proposed implementing versioning in Execution APIs, suggesting that major versions could represent different forks while minor versions would indicate non-breaking changes. The group agreed that forks could be treated as major versions, though they noted that recent Ethereum changes have been non-breaking in nature.

The team discussed progress on standardizing error codes for Ethereum implementations. Simsonraj reported that he had worked with Zane and Shane to define cohesive error ranges for each category, and plans to create a README file for review before implementing RPC testgen for validation. The solution will initially function as a guidance rather than a strict requirement, starting with warnings before potentially becoming mandatory. Zane explained the importance of formalizing error code ranges to prevent conflicts with existing implementations and to enable better testing of error code returns. The team agreed to create documentation to share with client teams for feedback, with Simsonraj committing to write a spec document now that the technical implementation is complete.

Zane provided an update on documentation rework plans, explaining they are moving towards a more generic approach that would generate markdown directly into the repo and support multiple frameworks like README docs, Pandoc, and PDFs. He also mentioned that the revamp would include individual method pages similar to the previous direction before reverting. Zane invited feedback from users about frustrating aspects of current documentation through Discord messages.

### Next Steps:

- Keri to prioritize fixing the RPC Compat Hive tests before addressing stale PRs
- Keri to analyze which RPC Compat test failures are due to Execution API issues versus client implementation issues
- Mercy to look into the Hive test failures and get back to Keri
- Simsonraj to write a README file for the error codes standardization PR
- Simsonraj to implement RPC testgen for validation and verification of error code ranges
- Simsonraj to create documentation for error code standardization to share with client teams
- Zane to continue work on the documentation revamp with focus on generating markdown for individual methods

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 4aFxX9i#)
- Download Chat (Passcode: 4aFxX9i#)

---

**system** (2025-09-15):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=e2Tu2ffpvoA

