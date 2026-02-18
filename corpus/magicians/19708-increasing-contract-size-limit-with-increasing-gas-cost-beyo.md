---
source: magicians
topic_id: 19708
title: Increasing contract size limit with increasing gas cost beyond 24.5Kb
author: 0xTraub
date: "2024-04-18"
category: EIPs > EIPs core
tags: [evm, opcodes, gas]
url: https://ethereum-magicians.org/t/increasing-contract-size-limit-with-increasing-gas-cost-beyond-24-5kb/19708
views: 1203
likes: 13
posts_count: 31
---

# Increasing contract size limit with increasing gas cost beyond 24.5Kb

Vitalik’s [EIP-170](https://eips.ethereum.org/EIPS/eip-170) which set the current contract size limit at 24.5 Kb was written in 2016, over 8 years ago. Since then a lot has changed about the protocol, including the roadmap decision to include the verge and the purge. I think it is time to reconsider our current contract size limitations. As contracts get bigger and Dapps more complex, this limit becomes a bottleneck for many developers. The restriction has resulted in several design suggestions as well, with the Diamond-Standard being the most popular. However, writing and interacting with Diamond-contracts is a pain point for many developers, and it is not without its own issues. I  want to get started the conversation about how we can increase the contract size-limit without compromising on things like state-growth, decentralization, and security.

My current idea is fairly simple. The current contract size limit should be doubled from ~24.5Kb to ~49Kb. However, 24.5Kb should remain as target, with additional bytes incurring an increasing gas cost per byte, up to the max limit.

Current code cost is defined in the EVM as `code_deposit_cost = 200 * deployed_code_size `

Based on the memory expansion cost, this should put the equation as something like `200 * contract_size + floor(size^2 / 24500)`

I think that this cost should be defined either as a step-function, or more likely as an exponential increase beyond a floor, similar to the memory-expansion cost. A hard-cap should probably be maintained to guard against the DOS-Vector Vitalik lays out in [EIP-170](https://eips.ethereum.org/EIPS/eip-170), but increased nonetheless. However, it could be possible to conceive of a proposal where exponentially increasing cost combined with block-gas-limits prevents against any security issues, and the cap can be removed entirely.

A second potential proposal could be something akin to multi-dimensional EIP-1559, where a target amount of new code is set per-block and the gas cost of deployment dynamic with a target. However, this would be contingent upon other major consensus changes, and is not suggested in the interim.

There’s definitely an appetite in the solidity community for increasing the limit, the question is how to do it with minimal consensus changes. Implementation would be fairly simple as its only a question of what the gas equation ought to be, and can be tweaked in the future as hardware requirements and further state-expiry proposals shift as well.

There must be some reason why nobody has taken this question up? Contract size limitations are a major pain point for solidity developers. The only discussion i’ve seen on this forum is from 2019, pre-merge/1559 and discussion seems to have stalled out.

## Replies

**matt** (2024-04-18):

There have been many discussions about this in different forums. One major issue is code analysis on large contracts. To increase the size, we’d need to see worst case analysis for all the clients vs. current numbers.

---

**0xTraub** (2024-04-18):

I figured that there were but I couldn’t find them. I assumed people much smarter than me had already discussed this since it seemed like an obvious idea. Could you link them please. Also, what’s the impact on verification if its one contract vs several? I.E three contracts at say ~12Kb each deployed in one tx vs a single 36 Kb contract? Similarly how would EOF make this verification easier/more difficult?

---

**matt** (2024-04-18):

I don’t think it is perfectly linear like that. I believe a 36kb contract has higher overhead than 3 12kb contracts. That’s at least the concern which has generally kept the 170 limit in place.

Some discussions:

- Removing or Increasing the Contract Size Limit
- https://x.com/lightclients/status/1737587978032001060

Kinda hard to track them down, would just search eip-170 or code size on twitter.

–

EOF does jump dest analysis one time at deploy and then never again. Non-EOF contracts do jump dest analysis everytime they’re executed.

---

**0xTraub** (2024-04-18):

That makes it sound like once EOF gets put in place then we can revisit the idea of increasing the size. I noticed from the EOF spec doc that they only allocate a uint16 for keeping track of code size so raising the limit to ~65Kb instead of unlimited seems reasonable to me as long as its priced appropriately. Obviously unlimited is better than 65Kb but that should still alleviate some concerns about security from EIP-170 and set an upper limit on which we can benchmark the different implementations.

I think raising the limit but not unlimited is a good stopgag measure we can implement in the interim on the way to fully lifting the cap. I’m sure that people would love to have completely unlimited sized contracts but for now even doubling it will go a long way for a long time, and something like this may be less contentious as it allows the community to tweak the parameters and slowly increase size over time.

Sorry if I’m wasting your time with questions or pointless solutions when I’m missing a lot of established research. Just tryna contribute however I can.

---

**matt** (2024-04-19):

No worries at all. I think one main issue is that no one has taken the time to run the analysis and champion the change. If you’re willing to do that, it would be great. The best way to run all the clients and time them is this: [GitHub - holiman/goevmlab: Evm laboratory](https://github.com/holiman/goevmlab/)

---

**shemnon** (2024-04-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xtraub/48/7553_2.png) 0xTraub:

> EOF spec doc that they only allocate a uint16 for keeping track of code size so raising the limit to ~65Kb instead of unlimited seems reasonable to me as long as its priced appropriately.

(a) That’s 64 Kib per code section, with up to 1024 code sections.  So in theory the current format supports 64Mib contracts.

(b) Once in place the container format can be revised (without breaking changes) to support header elements using variable-width encodings.

---

**0xTraub** (2024-04-19):

Can you provide any insights on what analysis would need to be done first?

---

**hlau** (2024-10-02):

Is there an update on this? ~25 KB is simply not enough. I should also add that this bottleneck usually pops up at the worst time as dev tooling will continue to compile locally. This leads to hellish refactors that stall momentum when one least expects it.

Also agree that the diamond proxy pattern is not an ideal solution.

---

**itsdevbear** (2024-10-03):

24kb is definitely small, but this is a change that as [@matt](/u/matt) said, is something that I can only see being changed if someone has the data, changing it to some arbitrary number based on a feeling is probably more counterproductive

---

**0xTraub** (2024-10-03):

there’s been some discussion in the past about doubling the size. I think the best method is to adopt a 1559-like mechanism whereby the limit is doubled but with an exponentially increasing cost for each byte beyond the 24.5kb target to prevent unnecessary bloat.

What kind of data is necessary. Im willing to kick off the research and work on it but I have no idea what kind of things are necessary to get that accomplished.

---

**shemnon** (2024-10-04):

A floating fee market for contract size beyond 24k seems excessive and unrelated to the reasons for the contract size, which was never bloat. If this was part of a multi-variable fee market the 24k limit would be an undeserved subsidy to small contracts when every byte should be subject to an equal fee.

The reason the contract size limit has survived past the shanghai attacks is that there were some vulnerabilities related to JUMPDEST analysis that kept the size in place until a recent fork where pay-per-initcode-byte fees were put into place.

On the horizon is EOF which eliminates this JUMPDEST analysis and only requires contract validation during a contract creation transaction or when parsing genesis file allocations.

Based on this I’m looking at proposing, for EOF only, an increase in contract size after EOF ships. After that a general uncapping of the limit for EOF can be investigated.

Regardng the notion that the size limit will prevent bloat: it won’t.  Authors will use creative ways to split their contracts, such as the diamond pattern.  Keeping the contract size in place does not reduce the total amount of storage on the chain but marginally increases it because of the overhead imposed by contract splitting techniques like the diamond pattern.

---

**0xTraub** (2024-10-07):

I don’t think it needs to be free-floating. I was picturing more of a memory-expansion cost type fee, where after a floor of 24.5 Kb the cost increases exponentially per Kb, which would still be predictable. While I agree that EOF is a good reason to wait, its unclear when the L2 EVMs will implement that, so this could be an interim fix to support that in the meantime. Perhaps moving this to a RIP would be more suitable.

---

**shemnon** (2024-10-07):

Some L2’s tend to hoover up all L1 changes fairly quickly, since they are a “diff” from geth.

---

**hlau** (2024-10-10):

Is there an established process to port/mirror an EIP to an RIP? And out of curiosity is EOF a lock in the next Pectra upgrade or has that not been finalized yet?

---

**shemnon** (2024-10-10):

(a) I don’t see EIP → RIP as the path, it would be RIP → EIP.  When EOF is a part of released fork most L2s will have it fairly quick.

(a) EOF is “scheduled for inclusion” in the [fork meta for osaka](https://eips.ethereum.org/EIPS/eip-7607). The next highest status is “shipped”

---

**0xTraub** (2024-10-10):

There’s no official EIP right now for what i’m proposing so starting as an RIP would make sense and then allow for porting to an EIP later. I would be concerned about using EOF as the key timeline since who knows how long it will be before a majority of L2s adopt it (ex: tstore/tload) which is why starting as an RIP and interim solution for temporarily alleviating the issue seems reasonable to me.

---

**shemnon** (2024-10-17):

I do not see raising the code limit without EOF as a long term viable path. The size cap is the mitigation to not having code validation.

---

**0xTraub** (2024-10-22):

I’m not suggesting eliminating the cap entirely and not anytime soon but i don’t think its an unreasonable idea that we consider an interim solution while we wait for EOF that makes contract deployments slightly more flexible, as long as we keep a target of 24.5 Kb but allow slightly more up to a point. Clients can handle it.

---

**Jackie** (2024-11-25):

Very much interested in seeing the contract size limit go up. We’re currently extremely constrained by this, as we’ve already tried to minimize our contract footprint (formatted, it’s around 5k SLOC of Yul right now) as much as we can, but still continuously hit the limit–even with optimizer runs set to relatively low values.

Admittedly, I only recently started reading this board more, so am new to EOF. Will explore that too!

---

**axic** (2024-12-02):

We have published an EIP for this: [EIP-7830: Contract size limit increase for EOF](https://ethereum-magicians.org/t/eip-7830-contract-size-limit-increase-for-eof/21927)


*(10 more replies not shown)*
