---
source: magicians
topic_id: 24560
title: Eth_simulate Implementers' | Meeting # 53 | June 16, 2025
author: system
date: "2025-06-16"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eth-simulate-implementers-meeting-53-june-16-2025/24560
views: 76
likes: 0
posts_count: 3
---

# Eth_simulate Implementers' | Meeting # 53 | June 16, 2025

# eth_simulate Implementers’ Meeting # 53, June 16, 2025

- Date and time in UTC in format June 16, 2025, 12:00 UTC

# Agenda

- Notes from Meeting 52
- Client Implementation update
- Test
- Discuss spec for eth_simulateV2

Other comments and resources

The zoom link will be sent to the facilitator via email

Facilitator emails: [Killari@gmail.com](mailto:Killari@gmail.com), [pooja@ethcatherders.com](mailto:pooja@ethcatherders.com)

 **🤖 config**

- Duration in minutes : 60 mins
- Recurring meeting : true
- Call series : eth simulate
- Occurrence rate : weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : false
- display zoom link in invite : true

[GitHub Issue](https://github.com/ethereum/pm/issues/1574)

## Replies

**system** (2025-06-16):

### Meeting Summary:

The team addressed concerns about low meeting attendance and discussed potential solutions, including the possibility of cancellation. Development topics were covered, including a gas estimate feature and standardization of error codes, with the team favoring a client-generated approach. The group also reviewed the Hivetests website and discussed potential improvements to error case information display.

**Click to expand detailed summary**

The team discussed the low attendance at their meetings and considered canceling them if participation doesn’t improve. Sina mentioned forgetting to share some box-related reports with the representative, attributing it to a chaotic week. The group also touched on some net issues, though the specifics weren’t clear.

The team discussed the need for a gas estimate feature and acknowledged slow development momentum, with Sina emphasizing its importance for future adoption. Mercy presented two options for standardizing error codes: a repository with a generator for client use or allowing clients to generate types themselves, with the team favoring the latter due to maintenance concerns. The group also reviewed the Hivetests website, which displays client performance across different test suits, and discussed the possibility of adding more detailed error case information, though Sina noted this would require custom pages for each test suite.

### Next Steps:

- Sina to report the bugs found in the previous meeting.
- Mercy to continue working on standardizing error codes, focusing on the option of allowing clients to generate types themselves using provided tools.
- Sina to investigate the possibility of adding method-specific test results to the Hive testing website.
- Killari to reach out to the maintainers of the Hive testing website about adding filters for viewing results by method.
- Team to discuss and decide on the future of these meetings due to low attendance.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 46#f.wwK)
- Download Chat (Passcode: 46#f.wwK)

---

**system** (2025-06-23):

### Meeting Summary:

The team discussed issues with the Execution API spec check, focusing on schema mismatches between expected object types and actual array outputs in test cases and specifications. They explored potential solutions, including modifying schemas to accommodate both object and array cases, and identified the need to update the YAML schema for Ethereum simulate results. Additionally, the team addressed CI configuration problems causing pull requests to fail checks after merging to master, and agreed to continue discussions on Discord regarding specification updates for the EthSimulateBlockResultSuccess schema.

**Click to expand detailed summary**

Mercy reported an issue with the Execution API spec check, where an array is causing CI failures. The team discussed whether modifying the schema to include both an object and an array would be acceptable, though Micah and Killari expressed uncertainty about making such changes. Mercy shared a PR and screen to demonstrate the problem, which Micah confirmed could be investigated further.

The team discussed an issue with test cases and specifications where the test was failing due to an expected output type mismatch in the schema. Mercy explained that the problem arises from multiple block state calls being bound into a response as an array, which conflicts with the spec that requires a single object type. Micah and Killari clarified that while some test cases might not have valid outputs, error responses should always be valid according to the specification.

Mercy and Micah discussed a schema issue where the result was expected to be an object but was outputting as an array. They examined the execution-apis repo to understand the correct schema specification, with killari providing guidance on where to find the relevant components under the schemas section. The discussion focused on aligning the schema to properly handle both object and array cases.

The team discussed an issue with the YAML schema for Ethereum simulate results, where the schema incorrectly specified that results should be an object when they should be an array. Micah explained that the correct schema should define two cases: one for successful results (containing a result array) and another for errors (containing an error object). Kalari agreed to update the YAML schema to reflect this, using references to the existing successful and error cases.

Micah and the team discussed an issue where pull requests (PRs) were failing to pass CI checks only after being merged to master, not during the initial submission. Micah hypothesized that the CI configuration was incorrectly set up to run against the master branch instead of the PR branch, which could happen if the CI process accidentally clones the head instead of the PR. Micah suggested this was likely a configuration issue with the CI setup, and he was investigating the problem further.

The team discussed a specification issue in the EthSimulateBlockResultSuccess schema, where Micah clarified that the result property should be an array while the error property should be an object, and objects can only have one of these properties. Micah agreed to mention this to Laurie and Jason in the JSON RPC API Discord channel, and suggested that Mercy could test the fix after it’s implemented. The team decided to continue the discussion on Discord and planned to follow up next week.

### Next Steps:

- Killari to submit a pull request with the corrected YAML schema for eth_simulate results in the execution API spec.
- Micah to review Killari’s pull request for the YAML schema correction.
- Micah to follow up with Light Client on Discord regarding the CI configuration issue.
- Mercy to monitor the progress of the schema correction and CI issue resolution.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: P&?5KTiY)
- Download Chat (Passcode: P&?5KTiY)

