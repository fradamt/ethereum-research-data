---
source: magicians
topic_id: 23472
title: Auto Review Bot Failing on PR #930 — "no artifacts found" Error
author: nitin312
date: "2025-04-11"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/auto-review-bot-failing-on-pr-930-no-artifacts-found-error/23472
views: 43
likes: 0
posts_count: 1
---

# Auto Review Bot Failing on PR #930 — "no artifacts found" Error

> Hi maintainers,​
>
>
> I’m working on PR #930 in the ethereum/ERCs repository. After submitting a follow-up comment to request a review, the Auto Review Bot was triggered but failed almost immediately with the following error:​
>
>
>
> Error: no artifacts found​

The GitHub Actions log shows that the `auto-review-bot.yml` ran for just a few seconds before failing. No artifacts were created, and it seems like the job didn’t have the necessary inputs to proceed.​

Has anyone encountered this issue before? Could it be related to a misconfiguration or recent GitHub workflow updates? Any guidance on how to proceed or who to tag would be appreciated!​

Thanks in advance for your time and assistance.​

Best regards,​ Nitin Bhagat ([@nitin312](/u/nitin312))​
