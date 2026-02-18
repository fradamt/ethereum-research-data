---
source: magicians
topic_id: 20347
title: Template for `discussion-to` threads
author: timbeiko
date: "2024-06-19"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/template-for-discussion-to-threads/20347
views: 807
likes: 7
posts_count: 4
---

# Template for `discussion-to` threads

As announced [here](https://ethereum-magicians.org/t/allcoredevs-network-upgrade-ethmagicians-process-improvements/20157#nup-proposal-2-eip-review-tracker-8), I’d like to propose a default template we could suggest to EIP authors for their `discussion-to` threads on EthMagicians.

The template should be auto-populated when people create a new post in the `EIPs` category. We could potentially store this template in the [ethereum/eips](https://github.com/ethereum/eips/) repo, too.

Here’s a first draft of what it could look like:

---

## discussion-to Template

It is recommended to use the following template when creating a `discussion-to` thread for your EIP on [ethereum-magicians.org](http://ethereum-magicians.org).

## Update Log

> This section should list significant updates to the EIP as the specification evolves. The first entry should be the PR to create the EIP. The recommended format for log entries is:
>
>
> yyyy-mm-dd: Single sentence description, commit link to commit
>
>
> For example, using EIP-1:
>
>
> 2024-06-05: Enable external links to Chain Agnostic Improvement Proposals (CAIPs), commit 32dc740.
> …

## External Reviews

> This section should list notable reviews the EIP has received from the Ethereum community. These can include specific comments on this forum, timestamped audio/video exchanges, formal audits, or other external resources. This section should be the go-to for readers to understand the community’s current assessment of the EIP. Aim for neutrality, quality & thoroughness over “cherry-picking” the most favorable reviews.
>
>
> The recommended format for entries is:
>
>
> yyyy-mm-dd: Single sentence description, link to review
>
>
> For example, using EIP-1559, one entry could be:
>
>
> 2020-12-01: “An Economic Analysis of EIP-1559”, by Tim Roughgarden, full report

## Outstanding Issues

> This section should highlight outstanding issues about the EIP, and, if possible, link to forums where these are being addressed. This section should allow readers to quickly understand what the most important TODOs for the EIP are, and how to best contribute. Once issues are resolved, they should be checked off with a note giving context on the resolution.
>
>
> The recommended format for new entries is:
>
>
>  yyyy-mm-dd: Issue description, link to issue
>
>
> Once issues are addressed, these becomes:
>
>
>  yyyy-mm-dd: Issue description, link to issue
>
> yyyy-mm-dd: Resolution description, link to resolution
>
>
>
>
> For example, using EIP-3675, one entry could be:
>
>
>  2021-07-08: Repurpose the DIFFICULTY opcode, tracking issue
>
> 2021-10-30: Introduce EIP-4399, EIP PR

## Replies

**abcoathup** (2024-06-21):

A [topic template](https://meta.discourse.org/t/topic-templates-for-categories-and-other-alternatives/38295) for the [EIPs](/c/eips/5) category would be great. (also do similar for [ERCs](/c/ercs/57), but want to start somewhere).

We could also [default](https://meta.discourse.org/t/create-a-wiki-post/30802#category-defaults-2) the category to be [wiki posts](https://meta.discourse.org/t/understanding-wiki-posts/30801) so that anyone can edit, removing the burden of maintaining from just the author.

---

**matt** (2024-06-25):

I’ve added this as the template for [EIPs](/c/eips/5) and [Core EIPs](/c/eips/core-eips/35)

