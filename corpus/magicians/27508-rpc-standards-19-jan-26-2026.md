---
source: magicians
topic_id: 27508
title: RPC Standards # 19 | Jan 26, 2026
author: system
date: "2026-01-19"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/rpc-standards-19-jan-26-2026/27508
views: 27
likes: 0
posts_count: 3
---

# RPC Standards # 19 | Jan 26, 2026

### Agenda

Open Issues:

- Missing Test Coverage for 11 JSON-RPC Methods · Issue #737 · ethereum/execution-apis · GitHub

Open PR’s:

- fix: playground link in README by zcstarr · Pull Request #738 · ethereum/execution-apis · GitHub
- Fix lint/ci by jshufro · Pull Request #733 · ethereum/execution-apis · GitHub
- Merge rpctestgen in, preserving history and github actions by jshufro · Pull Request #732 · ethereum/execution-apis · GitHub

**Meeting Time:** Monday, January 26, 2026 at 15:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1881)

## Replies

**system** (2026-01-26):

### Meeting Summary:

The team discussed the migration of the RPC test generator to a new repository and addressed various technical issues related to testing and linter problems. They reviewed ongoing PRs and discussed versioning schemes for Execution API and JSON RPC endpoints, with specific attention to backward compatibility concerns. The conversation ended with discussions about improving website content readability and addressing bugs in the spec, including plans to seek input from the Geth team regarding test implementation challenges.

**Click to expand detailed summary**

Mercy led a meeting about RPC Standard Core 19 on January 26, 2026, but Patcha was not present. Chase explained that the RPC test generator, which creates .I/O files for Hive test chain, is being moved from the Lightclients repo to the Ethereum-owned repo. Mercy requested clarification on how to import .I/O files and proceed with future PRs, and Chase clarified that the process would not be significantly different from the current workflow.

Mercy and Chase discussed the process of running commands to clone repositories and generate tests, clarifying that the same command would be executed from within the execution APIs to automatically regenerate tests. Mercy inquired about merging rights for a specific pull request, which Chase confirmed was merged, while another PR (number 733) remained open to address CI and linter issues. The team also discussed website changes, with Chase suggesting that the example generator on the right side of the screen should be made more accessible or hidden to improve content readability, and Zane acknowledged the request, agreeing to investigate further.

Zane identified bugs in the spec, particularly with EFSimulate not following JSON schema, and mentioned that the OpenRPC team is working on a linter to address these issues. Chase discussed formatting confusion in the parameters section, noting that the line breaks and requirements (AND/OR) were unclear. They also talked about the successful merge of the RPC test generator into the Execution APIs repo, which introduced some linter and CI failures, and a PR was created for review and merging.

Mercy raised concerns about missing tests for some methods in the execution-apis repository and created an issue to address this. Chase explained that writing tests for methods with filters would be challenging due to nondeterministic filter IDs returned by clients. They discussed the need to fix a linter issue before proceeding with certain changes, but Chase suggested working on related tasks in parallel. Mercy requested Chase’s help in getting more clients to review and merge a specific PR, and Chase agreed to reach out to relevant team members.

Mercy and Chase discussed the need for stricter field value options in the “Get transaction by hash” feature to simplify testing, with Chase encouraging FLCL to leave a comment on the issue. Simsonraj reported limited progress on error code standardization and the hype test, suggesting merging the original PR since it doesn’t affect validations or generations, pending team agreement.

Mercy and Simsonraj discussed a blocking lint issue in the repository that needs to be fixed before they can manage PRs and continue with core developers. Simsonraj mentioned the need to write tests and get them approved before implementation, but noted challenges with the current test generator due to Geth’s lack of support for certain error codes. They agreed to seek input from the Geth team on whether to write custom tests or wait for Geth’s implementation, with Simsonraj planning to share details in the AllCoreDevs channel and potentially involve Felix from the Geth team in the next meeting.

Mercy and Chase discussed the process of versioning specs and creating a release. They agreed to go through current PRs and issues to determine what features should be included in the first version. Mercy suggested creating a list and posting it in the chat for collective input. Zane mentioned that line breaks would be an easy fix, but the interactive widget might require more thought.

The team discussed versioning schemes for Execution API and JSON RPC endpoints, with Tullio proposing both repository versioning and endpoint versioning. Mercy raised concerns about getting input from application users, suggesting they might reach out to Sam for feedback. Chase noted that adding versioning likely wouldn’t break backward compatibility since everything currently pulls from main. Zane mentioned a PR for restoring built assets in the spec repo, which Mercy agreed to follow up on.

### Next Steps:

- Chase: Talk to Patcha and invite him to future calls to explain how the two repos work
- Chase: Bug people to get merge rights for the repo
- Zane: Look into making the interactive request widget on the website a hidden/pullout column or movable to reduce screen real estate consumption
- Zane: Work on fixing parameter line breaks formatting issue on the website
- FLCL: Leave a comment on issue 729 regarding being stricter about field value options in Get Transaction by Hash
- Simsonraj: Continue working on Hive tests for error code standardization
- Simsonraj: Repost error code standardization PR in AllCoreDevs channel and ask for reviews, explaining the testing issue
- Simsonraj: Reach out to Felix from Geth team to discuss whether to write custom tests in RPC testing before or after Geth implementation
- Mercy: Create a list of current PRs and issues to determine what should be included in the first versioned release and post in Discord
- Mercy: Reach out to Sam and endpoint users to get their input on versioning scheme for API endpoints

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: B%7yzGpY)
- Download Chat (Passcode: B%7yzGpY)
- Download Audio (Passcode: B%7yzGpY)

---

**system** (2026-01-26):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=YKzMqVF-cPI

