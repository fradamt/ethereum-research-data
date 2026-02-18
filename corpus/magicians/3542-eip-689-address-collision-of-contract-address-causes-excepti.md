---
source: magicians
topic_id: 3542
title: "EIP-689: Address Collision of Contract Address Causes Exceptional Halt"
author: axic
date: "2019-08-11"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-689-address-collision-of-contract-address-causes-exceptional-halt/3542
views: 1055
likes: 0
posts_count: 6
---

# EIP-689: Address Collision of Contract Address Causes Exceptional Halt

Discussion topic for:


      [Ethereum Improvement Proposals](http://eips.ethereum.org/EIPS/eip-689)




###

Ethereum Improvement Proposals (EIPs) describe standards for the Ethereum platform, including core protocol specifications, client APIs, and contract standards.








This was also proposed as [EIP-684](https://github.com/ethereum/EIPs/issues/684) and [EIP-83](https://github.com/ethereum/EIPs/issues/83).

(Some comments were left on the PR: https://github.com/ethereum/EIPs/pull/689)

## Replies

**axic** (2019-08-11):

This has been discussed started ACD#60. On [ACD#61](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2061.md)

> Martin : No. Long time ago we decide on 684 and 689 are roughly the same thing.

On [ACD#62](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2062.md)

> Status : Completed. Exists in Clients and is in tests as it has already been accepted but is not in the yellow paper. No one available to write it into the Yellow Paper.

[@holiman](/u/holiman) I think you also mentioned this was done because of EIP-86, but EIP-86 is not part of any hard fork.

Can you clarify what version of this EIP is implemented and can we mark the EIP final once everything is clarified?

Started to add some clarifications in this PR: [EIP-689: clarifications by axic · Pull Request #2238 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/2238)

---

**holiman** (2019-08-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> Can you clarify what version of this EIP is implemented and can we mark the EIP final once everything is clarified?

See [EIP-1014: Skinny CREATE2](https://eips.ethereum.org/EIPS/eip-1014) , under “Clarifications”:

> The init_code is the code that, when executed, produces the runtime bytecode that will be placed into the state, and which typically is used by high level languages to implement a ‘constructor’.
>
>
> This EIP makes collisions possible. The behaviour at collisions is specified by EIP 684:
>
>
>
> If a contract creation is attempted, due to either a creation transaction or the CREATE (or future CREATE2) opcode, and the destination address already has either nonzero nonce, or nonempty code, then the creation throws immediately, with exactly the same behavior as would arise if the first byte in the init code were an invalid opcode. This applies retroactively starting from genesis.

So, we decided on a call to consider #684 retroactively adopted, and code was added to clients and tests. What prompted this (EIP-684) was that we were contempling EIp-86, and needed to define how to handle collisions.

However, #86 was never actually implemented, for various reasons. So #684 was not really needed (but still accepted), until eventually the next version of EIP-86, the EIP-1014 was implemented.

Therefore, to make things clearer, I made sure to include the “Clarificatios” into 1014, so that the behaviour would be well defined, even if people had forgotten about EIP-684.

I’m not sure where all the confusion comes from, or how we could/should improve it.

---

**axic** (2019-08-12):

This clarifies it a lot. I think where confusion stems from is that a lot of these “EIPs” are not actual EIPs, just issues on the repo.

Seemingly 689 and 684 are identical. I think the best solution going forward would be either:

1. Creating a “real EIP” out of 684 and marking it final and marking 689 as “abandoned”.
2. Updating 689 to match reality completely (e.g. removing references to 86) and marking it final.

---

**holiman** (2019-08-12):

In that case, I’d go with option 1, since that’s the one we did agree on at a call long ago.

Also, back in those times the format of EIPs weren’t well-defined, and a lot of old EIPs are issues rather than md-files. So lifting it into proper form seems the right approach.

---

**axic** (2020-08-28):

I think option 1 sounds good. Someone just needs to do – apparently we haven’t progressed for a year ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

Also two relevant issues/PRs:

- [Missing] EIP-684 · Issue #2220 · ethereum/EIPs · GitHub
- Add EIP-684 to Byzantium Meta by soc1c · Pull Request #2252 · ethereum/EIPs · GitHub

