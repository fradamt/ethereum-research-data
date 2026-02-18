---
source: ethresearch
topic_id: 5194
title: "Ideation session: Reasonably fair algorithm to measure current contribution"
author: jpitts
date: "2019-03-21"
category: Economics
tags: []
url: https://ethresear.ch/t/ideation-session-reasonably-fair-algorithm-to-measure-current-contribution/5194
views: 1361
likes: 0
posts_count: 3
---

# Ideation session: Reasonably fair algorithm to measure current contribution

Post ideas about a reasonably fair algorithm to identify contributors and measure current contribution to Ethereum-related work of all kinds.

This algorithm could be run in an oracle and used to allocate community contribution rewards. It would be able to access data from the web or Ethereum mainnet, and track contributors and types of work.

***Please don’t argue about which is good or bad, just reply with ideas.*** I will collect related ideas together for focused evaluation.

## Replies

**jpitts** (2019-03-21):

Inputs, things to measure, things to track over time:

- community priorities, addressed by the work
- the work, quality of the work
- adoption of / use of / dependency on work
- peer review, qualitative and quantitative recognition

Things to counteract:

- distortions caused by social media popularity
- distortions caused by personal choices, e.g. privacy orientation
- stakeholder groups gaming the algo construction process
- gaming of the algo

---

**jpitts** (2019-03-22):

Ok I will take a quick whack at this:

Principles:

- algorithm is oriented toward fulfilling community priorities
- technical and non-technical work is measured
- all current contributors are to be rewarded

Process:

Create a system to form community priorities with output data that can be easily fed into the greater evaluation process. This may need a strong human participation component.

Use a prediction market to identify which clients and projects will have the most impact in 1 year. Then add instrumentation to the active mainnet and testnets, and measure which dapps and clients are impactful now.

From that combined list, create a list of software module dependencies, then create a list of contributors to each, to generate a list of GitHub IDs.

Separately, foster the emergence of TCR lists of events, papers, ideas, and important non-software, non-hosted-on-GitHub work done in the community, then generate a list of contributors from that data.

Once the master list of contributors is established, generate baseline scores of contributions from the the work done. Baseline is weighted according to the established community priorities. Next, create an incentivized subjective evaluation process. From the aggregated baseline and subjective scoring, generate an allocation of ether to each.

Create a reasonable claims process, and affix some kind of reasonable time lock or disbursement schedule.

