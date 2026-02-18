---
source: magicians
topic_id: 23749
title: Make Developer Relations in Ethereum Great Again
author: andreolf
date: "2025-04-22"
category: Uncategorized
tags: [devrel, developer-experience]
url: https://ethereum-magicians.org/t/make-developer-relations-in-ethereum-great-again/23749
views: 237
likes: 5
posts_count: 2
---

# Make Developer Relations in Ethereum Great Again

I’d like to express my gratitude to the Ethereum Magicians community members who consistently contribute valuable insights and help improve the ecosystem. Special thanks to [@vbuterin](/u/vbuterin), [@TimDaub](/u/timdaub), [@abcoathup](/u/abcoathup), [@SCBuergel](/u/scbuergel) , [@anett](/u/anett), [@nicocsgy](/u/nicocsgy) and [@beylin](/u/beylin) for their thoughtful discussions and leadership. Your dedication to maintaining high standards while making Ethereum more accessible to developers is what inspired this post. I look forward to your thoughts on how we can collectively improve developer relations in the Ethereum ecosystem.

## Introduction

The Ethereum ecosystem stands at a critical juncture. While the protocol layer continues to evolve with technical innovations like the Dencun upgrade and the ongoing shift to Layer 2 solutions, one aspect demands our urgent attention: developer relations.

Despite Ethereum remaining the favored ecosystem among blockchain developers—with 20.8% of crypto projects built on Ethereum according to a16z Crypto’s statistics—we face significant challenges in developer onboarding, retention, and community support. The health of our developer ecosystem directly impacts Ethereum’s long-term success and ability to fulfill its mission of creating a more open, accessible, and decentralized web.

This post examines the current state of developer relations in Ethereum, identifies key challenges across documentation, tooling, and education, and proposes actionable solutions to strengthen our developer community.

## The Current State of Ethereum’s Developer Ecosystem

### Growth Amid Challenges

The Ethereum developer ecosystem continues to show remarkable resilience and growth. According to Electric Capital’s 2024 Developer Report, the number of established developers in Ethereum grew by 21% in 2024. Ethereum SDK installs increased 31% year over year to 106.4 million downloads in 2023, up from 81.4 million in 2022, according to Alchemy’s Web3 Development Report.

However, these positive metrics mask underlying challenges. As one community member noted in the “Need help drafting an EIP” discussion on Ethereum Magicians: “While we’re passionate about this cause, we recognize we lack the technical expertise and experience of many of you here. We’re reaching out for collaboration, feedback, and advice on shaping this EIP into something that can truly benefit the ecosystem.”

This sentiment echoes across many newcomers to the ecosystem—passion and interest abound, but technical barriers remain high.

### The Shifting Landscape

The Ethereum development landscape is undergoing a significant transformation. In 2022, only 25% of Ethereum ecosystem developers worked on Layer 2 solutions. By 2024, that number had grown to 56%, with Base emerging as the L2 with the most active developers.

This shift creates both opportunities and challenges. While L2s offer improved scalability and reduced transaction costs, they also increase ecosystem complexity and create additional learning curves for new developers.

## Key Challenges in Developer Relations

### Documentation: Fragmentation and Complexity

The Ethereum documentation landscape suffers from fragmentation across multiple sources, projects, and layers. New developers often struggle to find authoritative, up-to-date information tailored to their skill level. Documentation tends to be either too basic or too advanced, with few resources bridging the gap between introductory concepts and production-ready development.

As the ecosystem expands to include multiple L2s, each with its own documentation standards and practices, this fragmentation intensifies. Developers must navigate an increasingly complex web of resources, often with inconsistent terminology and approaches.

### Tooling: Complexity and Rapid Evolution

Ethereum’s development tooling ecosystem is both a strength and a challenge. The diversity of tools provides flexibility but creates confusion for newcomers who struggle to determine which tools to learn and use.

Infrastructure and tooling teams play a critical role in developer access to the core protocol, as noted in discussions on Ethereum Magicians. However, the rapid evolution of these tools means that tutorials and guides quickly become outdated, leaving developers to troubleshoot compatibility issues and navigate breaking changes.

The “ABI Spec is wrong” discussion on Ethereum Magicians highlights how even fundamental specifications can contain inconsistencies that create friction for developers.

### Education: The Onboarding Gap

The journey from blockchain curious to productive Ethereum developer remains unnecessarily difficult. Educational resources often fail to provide clear learning paths that guide developers through the progressive mastery of concepts and tools.

Many developers report feeling overwhelmed by Ethereum’s terminology, concepts, and rapidly evolving standards. The “Need help drafting an EIP” thread on Ethereum Magicians reveals how even motivated community members struggle to navigate governance processes and technical requirements.

## The Developer Journey: Pain Points and Opportunities

The developer journey in Ethereum consists of several key stages, each with its own challenges and opportunities for improvement:

![Ethereum Developer Journey Map](https://private-us-east-1.manuscdn.com/sessionFile/ZhznaGsekS3kWgUSst9ghB/sandbox/C5dSG9Z22CqmOcWdv5ixTZ-images_1745312809497_na1fn_L2hvbWUvdWJ1bnR1L2luZm9ncmFwaGljcy9ldGhlcmV1bV9kZXZlbG9wZXJfam91cm5leV9tYXA.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvWmh6bmFHc2VrUzNrV2dVU3N0OWdoQi9zYW5kYm94L0M1ZFNHOVoyMkNxbU9jV2R2NWl4VFotaW1hZ2VzXzE3NDUzMTI4MDk0OTdfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwybHVabTluY21Gd2FHbGpjeTlsZEdobGNtVjFiVjlrWlhabGJHOXdaWEpmYW05MWNtNWxlVjl0WVhBLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc2NzIyNTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=eZEKUR~JZRdgDahSYrvd0xVE0OOwAdVe0uP64LLqAE8l8FVBRNZWKLidDGff8DLntfGzGPilSFEAGfNU4rta35U1FpZTm56Qrz4AzRBTbsWgA9W5J-NmS1rtnWomtd2lPeI4Ag-W4kq-Vc0i1CwHzrZ-s2d28JyE7jcjupShc8uvyqxOF8Qgl-lQrOq3L-G0IZoCplZSYF770cVpqFLEOPXpAA7PJC6PVETQrfWvxNqKLug0DHpZxVVATXQbfz6SgNWh2Dic5KIdzLYC~M9vvH3lHsCi5TT4K2OwPHc--FIZckyak7e444xNNtLBykf4JwGxbASFL2Iz2IpObsArug__)

### Discovery Stage

**Pain Points**: Fragmented resources and overwhelming terminology

**Opportunities**: Centralized resources and beginner-friendly guides

### Learning Stage

**Pain Points**: Steep learning curve and rapidly evolving technology

**Opportunities**: Interactive tutorials and structured learning paths

### First Project Stage

**Pain Points**: Complex setup and debugging challenges

**Opportunities**: Project templates and better error messages

### Tooling Mastery Stage

**Pain Points**: Multiple toolchains and version compatibility issues

**Opportunities**: Unified tooling and better documentation

### Community Engagement Stage

**Pain Points**: Finding mentors and navigating forums

**Opportunities**: Mentorship programs and community onboarding

### Protocol Contribution Stage

**Pain Points**: EIP process complexity and getting community support

**Opportunities**: EIP templates and governance education

## The Ethereum Developer Landscape in Numbers

![Distribution of Crypto Projects by Blockchain](https://private-us-east-1.manuscdn.com/sessionFile/ZhznaGsekS3kWgUSst9ghB/sandbox/C5dSG9Z22CqmOcWdv5ixTZ-images_1745312809498_na1fn_L2hvbWUvdWJ1bnR1L2luZm9ncmFwaGljcy9ldGhlcmV1bV9kZXZlbG9wZXJfc3RhdGlzdGljcw.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvWmh6bmFHc2VrUzNrV2dVU3N0OWdoQi9zYW5kYm94L0M1ZFNHOVoyMkNxbU9jV2R2NWl4VFotaW1hZ2VzXzE3NDUzMTI4MDk0OThfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwybHVabTluY21Gd2FHbGpjeTlsZEdobGNtVjFiVjlrWlhabGJHOXdaWEpmYzNSaGRHbHpkR2xqY3cucG5nIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzY3MjI1NjAwfX19XX0_&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=lxk3j94fQ5hrAQZa91ewJlXb9QFhTMaRFVtXOkH1MLHWDrtxz5n~dT4~iMyo5cpKyID90DpTJoprVbUHPjyYwqN6z4E~YELyV57tOUfB5SlPo3brI~hiAuLQaCcn4rytq90XgxHQ2u2UxDz1jy6GQMPsdrTsA2yQndeCXn6Vo0XabbuDTKZwXx4Yqat7FjsA~OmbbDwv8Xrq1bPf7RY1eVezvhytIq~FC59tjroLiRgur0NYOqeysLcK8SlqxtrojXNHSI9q0smi4Qw21FyNPEzTGnzncFm7xD5LfnUMAEJ2EiSQvtFUN~rbDWKHGk7yyZXeUguhh0bkPGtFEyb-ug__)

Ethereum maintains its leadership position in the developer ecosystem, with 20.8% of crypto projects built on the platform. However, competition is intensifying, with Solana at 11.2% and Base at 10.7%.

![Shift of Ethereum Developers from L1 to L2](https://private-us-east-1.manuscdn.com/sessionFile/ZhznaGsekS3kWgUSst9ghB/sandbox/C5dSG9Z22CqmOcWdv5ixTZ-images_1745312809498_na1fn_L2hvbWUvdWJ1bnR1L2luZm9ncmFwaGljcy9ldGhlcmV1bV9sMV9sMl9kZXZlbG9wZXJfc2hpZnQ.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvWmh6bmFHc2VrUzNrV2dVU3N0OWdoQi9zYW5kYm94L0M1ZFNHOVoyMkNxbU9jV2R2NWl4VFotaW1hZ2VzXzE3NDUzMTI4MDk0OThfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwybHVabTluY21Gd2FHbGpjeTlsZEdobGNtVjFiVjlzTVY5c01sOWtaWFpsYkc5d1pYSmZjMmhwWm5RLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc2NzIyNTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=M4CyZhSqMyIMt1rDj6WRt~Bn7hOd5TA~fftpwCPmwcHSAloKfQ3jL0Wp2DnUpsKmTfIVYbteGldHvO5OBCEs3DSIUZpt63VMraax-4F-4hluQc9QwbyCD9Af2RiN7dExXxhdRhae8fpVFemtIJR4bHtux21xbCsh~ci4xDPTNPEAQacyFgWOMOd9CeiYZWzQ~YjkPvaVkvZpYlJSqoXOU571U8HfEzIb5MUv-oIYDiukugppUKid3mZRLnSd~QXJlvy0cC4KzJH4ovNjCoWSyVeWTCn6Yq1Qc1PV1CBuR6DCFjwuLm4JEtOc3kfbMEQPgrTNOwvStRjUwfu91RuUdg__)

The shift of developer activity from L1 to L2 represents both a challenge and an opportunity. While it demonstrates the ecosystem’s ability to scale and evolve, it also creates additional complexity in the developer experience.

## Solutions: Making Developer Relations Great Again

### 1. Unified Documentation Strategy

**Proposal**: Create a comprehensive, unified documentation portal that serves as a single entry point for all Ethereum developers, regardless of their focus area or skill level.

**Implementation**:

- Establish a cross-ecosystem documentation working group
- Develop consistent terminology and standards across L1 and L2 documentation
- Create clear learning paths from beginner to advanced topics
- Implement a robust system for keeping documentation updated as the ecosystem evolves

### 2. Streamlined Tooling Experience

**Proposal**: Reduce friction in the developer tooling experience through better integration, compatibility, and onboarding.

**Implementation**:

- Develop a unified developer environment that integrates essential tools
- Create better error messages and debugging experiences
- Establish compatibility standards across the tooling ecosystem
- Provide clear migration paths when tools evolve or deprecate features

### 3. Enhanced Education and Mentorship

**Proposal**: Build structured educational pathways and mentorship programs to guide developers from their first steps to mastery.

**Implementation**:

- Develop an official Ethereum Developer Certification program
- Establish a mentorship matching platform connecting newcomers with experienced developers
- Create interactive learning experiences that combine theory with practical application
- Support local meetups and workshops focused on developer education

### 4. Improved Governance Participation

**Proposal**: Lower the barriers to participation in Ethereum’s governance processes.

**Implementation**:

- Create templates and guides for EIP drafting
- Establish a pre-EIP feedback mechanism for early-stage ideas
- Develop educational resources about the governance process
- Implement a mentorship system specifically for first-time EIP authors

### 5. Community Support Structures

**Proposal**: Strengthen community support structures to create a more welcoming environment for developers at all levels.

**Implementation**:

- Establish dedicated support channels for newcomers
- Create recognition programs for community members who support others
- Develop better tools for finding answers to common questions
- Support the creation of specialized interest groups within the broader community

## Conclusion: A Call to Action

The strength of Ethereum has always been its community. To maintain our leadership position and continue growing the ecosystem, we must prioritize developer relations with the same intensity we bring to protocol development.

By addressing the challenges in documentation, tooling, and education, we can create a more accessible, supportive, and productive environment for developers at all levels. This isn’t just about growing numbers—it’s about building a sustainable community that can realize Ethereum’s vision of a more open and decentralized web.

The data shows that interest in Ethereum development remains strong, with significant growth in established developers and SDK installs. Now is the time to capitalize on this interest by removing friction points and creating clear pathways from interest to mastery.

Let’s make developer relations in Ethereum great again—not through empty slogans, but through concrete actions that strengthen our community and welcome the next generation of builders.

## References

1. Ethereum Magicians Forum: “Ethereum’s Social Layer is Broken” - Ethereum’s Social Layer is Broken
2. Ethereum Magicians Forum: “Need help drafting an EIP” - Need help drafting an EIP
3. HashKey Capital: “Is This Time Different for Ethereum?” - https://medium.com/hashkey-capital-insights/is-this-time-different-for-ethereum-a-closer-look-at-its-current-landscape-and-challenges-e464bcd1d020
4. TechCrunch: “Ethereum developer interest hit new all-time highs in 2023” - Ethereum developer interest hit new all-time highs in 2023 despite a bear market | TechCrunch
5. Electric Capital Developer Report 2024
6. Alchemy’s Web3 Development Report 2023
7. a16z Crypto’s Developer Statistics 2025

## Replies

**andreolf** (2025-04-23):

Really appreciate this Vinay, especially coming from you!

Your point about acknowledging non-technical contributors and valuing diverse ways of thinking resonates deeply.

Developer relations isn’t just about docs and code but it’s also about building bridges between different kinds of intelligence, experience, and expression. Thanks for voicing this so clearly. ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

