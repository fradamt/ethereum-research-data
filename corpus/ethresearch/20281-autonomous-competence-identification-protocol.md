---
source: ethresearch
topic_id: 20281
title: Autonomous Competence Identification Protocol
author: peersky
date: "2024-08-15"
category: Meta-innovation
tags: [dao]
url: https://ethresear.ch/t/autonomous-competence-identification-protocol/20281
views: 155
likes: 0
posts_count: 1
---

# Autonomous Competence Identification Protocol

I’m excited to share my ongoing research on a protocol designed to streamline communication and decision-making around subjective matters, particularly within DAOs and R&D processes. This protocol establishes a ranking system that counters common governance issues, fostering a more collaborative and effective environment.

I’m posting this in the meta-innovation category because it has implications both for DAO/Consensus research and for potential collaboration tools within the Ethereum community.

*Link to paper in progress: https://github.com/peersky/papers/blob/main/acid/whitepaper.pdf*

## TL’DR

The protocol enables subjective decision-making and quantifies proposer ratings. Participants define a context and engage in rounds of discussion, providing and receiving feedback without revealing identities until the round concludes. This mitigates biases like the [Halo effect](https://en.wikipedia.org/wiki/Halo_effect), and collusion (sybil attack) risks.

Protocol streamlines discussions and enables autonomously assign competent decision makers as well as create pre-arranged agenda for any follow up voting systems (hence addresses [Agenda Manipulation](https://www.sciencedirect.com/science/article/abs/pii/0022053176900405),  ( casually explained in [this youtube video](https://www.youtube.com/watch?v=goQ4ii-zBMw) ) problem

## Motivation

### Communication Complexities Hinder Decision-Making

Effective decision-making is hindered by communication complexities.

- Traditional methods (meetings, chats): don’t scale, leading to information overload and delays.
- More stakeholders exponentially increase communication complexity, leaving less time for effective decisions.
- Individual contributions can get lost, leading to under-appreciation and high turnover.

### Traditional Organizations are Sub-optimally Managed

Despite modern networking and project management technologies, the primary, basis of hierarchical communication hasn’t changed much over centuries. Decisions still require large centralization force, which will step in and cut opinions to shape performance capable decision.

- Centralized decision-making prioritizes efficiency over diverse input, fostering internal politics and biased decisions.
- This breeds internal politics, leading to biased decisions that may harm the organization.
- Current methods lack objective ways to measure and reward valuable contributions, limiting organizational potential.
- Does not let organizations reach their full potential

This touches every organization, including Ethereum R&D.

### ICOs do not work well for DAOs

Research shows that many DAOs are highly centralized, with low participation rates and vulnerability to governance attacks. The incentive structures in Proof of Stake (PoS) and Proof of Work (PoW) systems can lead to centralization.

[![img](https://ethresear.ch/uploads/default/optimized/3X/1/e/1edd6c487afe9524d47e660bb04cf7872abb6008_2_690x274.jpeg)img2280×906 301 KB](https://ethresear.ch/uploads/default/1edd6c487afe9524d47e660bb04cf7872abb6008)

[![img2](https://ethresear.ch/uploads/default/optimized/3X/4/e/4e7ea5b4ee785ee33c7f3664e698a915d71867f8_2_690x374.jpeg)img21862×1010 162 KB](https://ethresear.ch/uploads/default/4e7ea5b4ee785ee33c7f3664e698a915d71867f8)

### Cyber-Physical-Social-Systems

There’s a growing need for DAOs to bridge traditional management with AI agents and automated infrastructure, as highlighted by research in Cyber-Physical-Social Systems (CPSS).

## Approach

The protocol aims to incentivize participation without enabling influence compounding. It builds on a real-world game where participants propose and vote on ideas (like music tracks) without revealing identities until the round ends.

### Key requirements for the protocol:

- Mission aligned: Participant activity directly impacts organizational goals.
- Highly performant: Organizations using the protocol should outperform traditional structures.
- Centralization resilient: Financial contributions shouldn’t lead to disproportionate influence.
- Multidimensional: Support diverse participant interests.
- Rational: Function even when agents act in their self-interest.

### Key features:

- Competence-based participation: Participants earn governance rights through demonstrated competence, not just financial contributions.
- Sybil attack resistance: A tournament ladder structure imposes costs and time requirements, making manipulation difficult.
- Progressive decentralization: Organizations can evolve by adding governance layers, increasing overall governance surface area.

## Current State

- Research paper in progress: Seeking feedback and potential co-authors.
- Basic prototype and testing: Exploring use cases beyond music, such as manage-less code writing.
- Website with Telegram group: https://rankify.it
