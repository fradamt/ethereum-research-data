---
source: magicians
topic_id: 23279
title: "EIP-7921: Skip `JUMPDEST` immediate argument check"
author: wjmelements
date: "2025-03-27"
category: EIPs > EIPs core
tags: [evm]
url: https://ethereum-magicians.org/t/eip-7921-skip-jumpdest-immediate-argument-check/23279
views: 122
likes: 8
posts_count: 7
---

# EIP-7921: Skip `JUMPDEST` immediate argument check

–

Discussion topic for [EIP-7921](https://ethereum.org/en/eips/eip-7921/)

#### Update Log

- initial draft PR

## Replies

**wjmelements** (2025-03-27):

Copied [discussion](https://github.com/ethereum/EIPs/pull/9548#discussion_r2015130733) by [@jochem-brouwer](/u/jochem-brouwer) from Github:

> Current contracts performing dynamic jumps may gain new unintended functionality if it is possible to jump to an immediate argument containing JUMPDEST.
> It is expected that very few contracts will become vulnerable in this way.

Right, in fact I think we can be confident to say one has to explicitly craft a malicious contract which will behave this way.

Because if a non-malicious contract would use this now, it would mean this non-malicious contract JUMPs inside an immediate PUSHx which has 0x5B as immediate value, which does not make much sense (one would choose INVALID for that immediate value if one wanted to explicitly jump there)

```auto

```

---

**wjmelements** (2025-03-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png)
    [EIP-7830: Contract size limit increase for EOF](https://ethereum-magicians.org/t/eip-7830-contract-size-limit-increase-for-eof/21927/20) [EIPs core](/c/eips/eips-core/35)



> Where’s the discussion top in “remove jumpdest analysis?” Several of my Ipsilon teammates think it would be dangerous and reckless, but I don’t want to derail this EIP’s discussion.

The necessary conditions for it being dangerous are:

1. Uses dynamic jumps
2. Dynamic jump can arrive at an immediate arg containing JUMPDEST
3. The code beginning at the newly valid JUMPDEST does not execute an invalid opcode (or REVERT) before JUMP, JUMPI, RETURN, or STOP.

Because solidity and vyper don’t make use of unbounded dynamic jumps, I predict very few (possibly zero) contracts will become vulnerable.

Nevertheless I also propose developing a static analysis tool to identify possibly vulnerable contracts:

> A static analysis tool should be developed and made publicly available to test if a contract might become vulnerable, and the program should be run for all current contracts in order to notify projects about potential security issues.
> Affected programs will have ample time to migrate.

---

**jochem-brouwer** (2025-03-27):

This comment needs analysis on code though, because this can significantly break stuff. Have been a bit too fast saying “we can be confident”, this is a bit shortsighted of me because there could be compiler actually using this as a trick, and this could therefore break contracts or open vulnerabilities which were not there.

---

**wjmelements** (2025-03-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> there could be compiler actually using this as a trick

I don’t think there is, but static analysis will be important for determining the impact to existing code.

---

**chfast** (2025-03-27):

The argument why JUMPDEST analysis is needed: [Why EVM has JUMPDEST](https://ethereum-magicians.org/t/why-evm-has-jumpdest/23288).

---

**wjmelements** (2025-03-27):

I don’t think that is especially specific to the immediate argument analysis that must be performed to determine which `0x5b` are valid `JUMPDEST`. This proposal expands the set of valid JUMPDEST to include all `0x5b`, which can result in overlapping blocks, but these blocks are still finite and can be analyzed and JIT’d in the same way.

Although the stack-returns used for internal functions are considered dynamic jumps, these are not the kind of dynamic jumps that would become vulnerable, because the stack return is a constant and not computed or provided by calldata.

> JUMPDESTs prevent data execution in EVM

EIP-7921 would trade that safety in order to remove the DoS vector and allow for additional immediate-argument opcodes such as DUPN otherwise only possible in EOF.

