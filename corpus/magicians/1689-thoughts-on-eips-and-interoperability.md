---
source: magicians
topic_id: 1689
title: Thoughts on EIPs and interoperability
author: Ethernian
date: "2018-10-28"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/thoughts-on-eips-and-interoperability/1689
views: 849
likes: 1
posts_count: 1
---

# Thoughts on EIPs and interoperability

[@boris](/u/boris),

Here is the short collection of my thoughts on EIP process for that sad case if I am not able to take part personally. Would be great if it could be discussed in “EIPs and Interoperability” session.

Thoughts are:

1. Ethereum is not only the Core any more. Now it is the whole ecosystem around it.
Thus, it makes sense to extend the goal of the EIP process from serving the Core Development to serve the whole ecosystem.
2. It is not sufficient to tag all not-Core EIPs as ERC - they are too different in their meaning and their processing.
3. It is not sufficient to include only CoreDevs into the EIP process . Application dev communities should be involved into the EIP workflow too.
4. Call for Action (CfA): It should be possible to call community attention to some global problem without proposing an improvement. CfA will become an EIP if anybody proposes a solution.
5. Editors should classify incoming EIP proposals as one of additional kinds of:

CfA - Call for Action (see above)
6. Design Pattern - nice to have, voluntary to use, mutable in the future, no global consensus needed, no danger of hard fork.
7. Standards (like ERC20): once adopted - then immutable, comprehensive review needed, no global consensus needed, no danger of hard fork, but danger of multiple different standards.
8. other kinds of EIP?

EIPs should be routed (signaled) between different communities in order to collect comprehensive reviews.

There should be simple standardized review states like (OK / INWORK / REJECTED ) to signal the review result between Communities and Editors.

More implementation details you will find in [Decentralizing EIP Workflow Proposal](https://ethereum-magicians.org/t/decentralizing-eip-workflow/1525). I am currently working on software implementation of it, so I am glad to discuss all the details in depth and interested on any specification input.
