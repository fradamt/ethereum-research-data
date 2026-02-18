---
source: magicians
topic_id: 22511
title: Client testing call #20, January 13, 2025
author: parithosh
date: "2025-01-13"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/client-testing-call-20-january-13-2025/22511
views: 105
likes: 1
posts_count: 1
---

# Client testing call #20, January 13, 2025

#### Pectra

- Spec releases were done last week, v1.5.0-beta.0 and pectra-devnet-5@v1.2.0
- Pari will trigger the Hive update after Mario’s/Dan’s fix.
- New tests have been added for EIP-7623 into the EEST release
- No more major test releases for devnets are expected
- EEST tests are being consumed in Assertor, and initial results look promising
- No other open PRs; the testing is moving closer to the final release and testnet phase.
- Depending on the hive bugfix, Nethermind should pass all Hive tests.
- Erigon: close to passing all Spec tests; Hive test results are pending. Code review is in progress and looks positive.
- Besu: In a similar position to Erigon with Hive tests needed fixes. But they are also doing code review and progress looks positive.
- Open Topics:

Tbenr raised the topic of SSZ support for builder flow on CL.
- Pari clarified that SSZ support is optional and not the main focus but will be tested in collaboration with the Flashbots team at a later point.
- Lighthouse is still missing from Kurtosis tests, which impacts Pectra testing as Lighthouse is essential for the mock workflow. Updates are expected this week.

> Note: Pectra Devnet 5 will launch without MEV support by default but will add it later.

#### PeerDAS

- Highlights from the last meeting:

Most clients are working on rebasing and local testing.
- Standardizing metrics may temporarily break some clients.

#### EOF

- Danno will merge the branch for testing.
- Some issues with block tests were noted but are expected.
- Building for the Osaka 0 devnet will start once there are three merged clients.
