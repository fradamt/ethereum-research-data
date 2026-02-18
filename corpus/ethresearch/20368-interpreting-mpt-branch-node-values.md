---
source: ethresearch
topic_id: 20368
title: Interpreting MPT branch node values
author: josephjohnston
date: "2024-08-31"
category: Data Structure
tags: []
url: https://ethresear.ch/t/interpreting-mpt-branch-node-values/20368
views: 166
likes: 0
posts_count: 1
---

# Interpreting MPT branch node values

Consider a branch node for an MPT.

Suppose the 17’th item in the branch node list is supposed to be NULL, because the branch node is not a “terminator” node. Ethereum documentation says NULL is encoded as the empty string.

Suppose the 17’th item in the list is supposed to be a value because the branch node is a terminator node. Suppose this value happens to be the empty string.

How to distinguish these two cases?

Note this question should be independent of RLP encoding, which only concerns how we encode the list. I’m asking what’s in the list itself, before considering how the list is subsequently encoded.
