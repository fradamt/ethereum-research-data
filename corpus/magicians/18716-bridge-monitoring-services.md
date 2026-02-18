---
source: magicians
topic_id: 18716
title: Bridge monitoring services
author: KyrylR
date: "2024-02-16"
category: Uncategorized
tags: [bridge]
url: https://ethereum-magicians.org/t/bridge-monitoring-services/18716
views: 416
likes: 1
posts_count: 1
---

# Bridge monitoring services

I am interested in exploring existing open-source solutions or concepts that can aid in bridge monitoring.

Are there any open-source solutions capable of pausing the bridge in an emergency? Are there any concepts, whitepapers, or protocols that could facilitate this?

Is this a feasible task, or are the benefits too minor to justify addressing the issue?

From my perspective, I have not found alternatives beyond the current solutions:

1. Monitoring transactions on both chains; if the deposit transaction on the source chain cannot be located, the service will attempt to pause the bridge to minimize the impact of any exploit.
2. Setting up transaction limits.
3. Utilizing services to detect unusual behaviour and pause the bridge.
4. Having an Admin (a trusted party) who can pause the bridge upon discovering a bug or a similar issue.

Thanks in advance!
