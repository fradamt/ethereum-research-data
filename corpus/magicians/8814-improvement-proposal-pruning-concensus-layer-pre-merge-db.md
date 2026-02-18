---
source: magicians
topic_id: 8814
title: "Improvement Proposal: Pruning Concensus Layer Pre Merge DB"
author: CryptoBlockchainTech
date: "2022-04-03"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/improvement-proposal-pruning-concensus-layer-pre-merge-db/8814
views: 496
likes: 0
posts_count: 1
---

# Improvement Proposal: Pruning Concensus Layer Pre Merge DB

I recently spun up a new Concensus beacon node and the sync took 4 days versus < a day for Geth. My limited understanding of the current CL chain is that there have been very little to no transactions since Genesis. If possible my proposal is to prune the last 1.5 years from the beacon chain to reduce the size of the db. Not sure if this is even possible or if this is something that the CL clients can do later post merge.
