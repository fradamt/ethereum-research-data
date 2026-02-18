---
source: magicians
topic_id: 24734
title: "ERC-7985: Attributes for Message Control in ERC-7786 gateways"
author: ernestognw
date: "2025-07-04"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7985-attributes-for-message-control-in-erc-7786-gateways/24734
views: 96
likes: 3
posts_count: 3
---

# ERC-7985: Attributes for Message Control in ERC-7786 gateways

**TL;DR:** Standardizing attributes for ERC-7786 cross-chain messaging gateways to enable consistent message lifecycle control, execution timing, and failure handling.

### Background

ERC-7786 introduced an extensible attribute system for cross-chain messaging but left attribute standardization for follow-up specs. Through discussions with Matter Labs’ team and analysis of real-world requirements, clear patterns have emerged for essential message control functionality.

### What We’re Proposing

**7 standard attributes** that address the most common cross-chain messaging needs:

- cancellable(bool) - Enable message cancellation
- timeout(uint256) - Automatic expiration timestamps
- earliestExecTime(uint256) - Delayed execution scheduling
- retryPolicy(bytes) - Standardized retry mechanisms
- revertBehavior(uint8) - Consistent failure handling
- dependsOn(bytes32[]) - Message dependency ordering
- minGasLimit(uint256) - Execution gas requirements

Without standardized attributes, each gateway implements these features differently, creating ecosystem fragmentation. Applications need predictable APIs for message control, especially for complex multi-chain workflows.

**Looking for feedback on:** attribute design, encoding choices, additional use cases we might have missed, and general community input on the approach.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1114)














####


      `master` ← `ernestognw:chore/7786-message-control`




          opened 04:40PM - 04 Jul 25 UTC



          [![](https://avatars.githubusercontent.com/u/33379285?v=4)
            ernestognw](https://github.com/ernestognw)



          [+130
            -0](https://github.com/ethereum/ERCs/pull/1114/files)







Introduces standard attributes for ERC-7786 cross-chain messaging gateways, enab[…](https://github.com/ethereum/ERCs/pull/1114)ling consistent message lifecycle control across implementations.

**Adds 7 standard attributes:**
- `cancellable(bool)` - Message cancellation
- `timeout(uint256)` - Automatic expiration
- `earliestExecTime(uint256)` - Delayed execution
- `retryPolicy(bytes)` - Retry mechanisms
- `revertBehavior(uint8)` - Failure handling
- `dependsOn(bytes32[])` - Message dependencies
- `minGasLimit(uint256)` - Gas requirements

**Benefits:** Ecosystem consistency, predictable APIs, advanced workflows, and reliable error handling. Extends ERC-7786 without breaking changes. Emerged from discussions with Matter Labs' InteropCenter team addressing real-world cross-chain messaging requirements.

## Replies

**sbacha** (2025-08-05):

What constitutes a redelivery of a message exactly or is that beyond the scope for this ERC?

---

**ernestognw** (2025-08-06):

Hey! According to the ERC terminology, redelivery would just mean delivering “twice”, which I think it’s not possible according to 7786.

Would you mind sharing a bit more detalls? Perhaps a use case would help me understand whether it concerns this spec ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

