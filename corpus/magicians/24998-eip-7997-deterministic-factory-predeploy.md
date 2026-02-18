---
source: magicians
topic_id: 24998
title: "EIP-7997: Deterministic Factory Predeploy"
author: frangio
date: "2025-08-04"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7997-deterministic-factory-predeploy/24998
views: 502
likes: 28
posts_count: 25
---

# EIP-7997: Deterministic Factory Predeploy

Discussion topic for EIP-7997: Deterministic Factory Predeploy



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7997.md)





####

  [master](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7997.md)



```md
---
eip: 7997
title: Deterministic Factory Predeploy
description: A minimal `CREATE2` factory shared by EVM chains.
author: Francisco Giordano (@frangio)
discussions-to: https://ethereum-magicians.org/t/eip-7997-deterministic-factory-predeploy/24998
status: Draft
type: Standards Track
category: Core
created: 2025-08-03
requires: 211, 1014
---

## Abstract

A minimal `CREATE2` factory is inserted as a system contract in the precompile range, to enable deterministic deployments at identical addresses across EVM chains. This benefits developer experience, user experience, and security, in particular for multi-chain and cross-chain applications, including account abstraction.

## Motivation

There are now a large number of EVM chains where users want to transact and developers want to deploy applications, and we can expect this number to continue to grow in line with Ethereum's rollup-centric roadmap and the general adoption of programmable blockchains.
```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7997.md)










#### Update Log

- 2025-08-03: initial draft - ethereum/EIPs#10092
- 2025-08-10: renamed and proposed for inclusion in Glamsterdam
- 2025-08-19: merged

## Replies

**nlordell** (2025-08-04):

This would be, IMO at least, an even more ideal way to have a CREATE2 factory on the same address on every chain and prefer it compared to the proposed [ERC-7955](https://ethereum-magicians.org/t/multi-chain-deployment-process-for-a-permissionless-contract-factory/24318).

I also like your minimal CREATE2 factory bytecode (notably how it explicitly handles cases where `CALLDATASIZE` is smaller than 32, and revert data propagation) and might backport some of it to ERC-7955 ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12).

One question I have is why you opted this to be an EIP instead of pushing RIP-7740 or another equivalent RIP? I feel like the former requires adoption by `Ethereum + Rollups`, while the latter only requires adoption by `Rollups` – so fewer parties.

**Edit**: Also worth pointing out that there was a similar discussion to have a `CREATE2` precompile a few years ago which unfortunately did not lead anywhere: [EIP Proposal: CREATE2 contract factory precompile for deployment at consistent addresses across networks](https://ethereum-magicians.org/t/eip-proposal-create2-contract-factory-precompile-for-deployment-at-consistent-addresses-across-networks/6083)

---

**frangio** (2025-08-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nlordell/48/10721_2.png) nlordell:

> I also like your minimal CREATE2 factory bytecode (notably how it explicitly handles cases where CALLDATASIZE is smaller than 32, and revert data propagation) and might backport some of it to ERC-7955 .

Please do! I hadn’t noticed revert data isn’t propagated in ERC-7955, it definitely should IMO.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nlordell/48/10721_2.png) nlordell:

> One question I have is why you opted this to be an EIP instead of pushing RIP-7740 or another equivalent RIP?

I think if this is standardized in Ethereum L1 and implemented in upstream clients it has the best chance of becoming widely available, even in other L1s.

RIP-7740 is a bit radical in including factories with managed keys. That’s like taking over user accounts in the protocol and I imagine it being unappealing to chain developers. Perhaps if those factories are removed it might be a better proposition. But I don’t know how those conversations have gone so far.

As long as we get a permissionless factory that’s available everywhere I don’t mind if it’s this EIP, ERC-7955, or Deterministic Deployment Proxy via RIP-7740. We might as well try all approaches!

---

**nlordell** (2025-08-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> RIP-7740 is a bit radical in including factories with managed keys. That’s like taking over user accounts in the protocol and I imagine it being unappealing to chain developers. Perhaps if those factories are removed it might be a better proposition.

That is a good point. You could argue to restrict RIP-7740 to just Nick’s deployment (cc [@rmeissner](/u/rmeissner)). That being said - we’ve seen some success at Safe with just convincing chains that they should include Safe’s CREATE2 factory deployment as a “preinstall”, just standardization efforts have not been that successful AFAIK ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> don’t mind if it’s this EIP, ERC-7955, or Deterministic Deployment Proxy via RIP-7740.

I personally prefer this or RIP-7740, ERC-7955 is nice because it works without network changes, but has some weaknesses IMO:

1. It relies on EIP-7702 which not all networks implement AFAIK
2. It will pontentially break in the future if permanent account upgrades becomes a thing.

---

**norswap** (2025-08-08):

Sorry if I missed the relevant explanation, but what is this intended to solve compared to the status quo?

The status quo being that most chain deploy this deterministic deployment factory ([GitHub - Arachnid/deterministic-deployment-proxy: An Ethereum proxy contract that can be used for deploying contracts to a deterministic address on any chain.](https://github.com/Arachnid/deterministic-deployment-proxy/)) at address 0x4e59b44847b379578588920ca78fbf26c0b4956c (this is deployed using Nick’s method).

This is widely integrated:

- Foundry uses it by default when you deploy contracts from a deploy script.
- All OP stack chain come with the factory pre-deployed.

Weaknesses of this method are:

- gas limit is hardcoded, so changes to the gas schedule could break it
- chains need to support legacy transactions

Here’s a writeup I have that explains this in more detail: [Notion](https://happychain.notion.site/xchain-deterministic-deploy)

---

**frangio** (2025-08-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/norswap/48/4243_2.png) norswap:

> what is this intended to solve compared to the status quo?

To provide a native solution to this problem that doesn’t rely on shaky assumptions.

The weaknesses are the ones you listed. For reference, this is mentioned in the Motivation section of this EIP:

> For this to work, the chain must support legacy transactions without EIP-155 replay protection, and the fixed gas price and gas limit must be sufficiently high, but not so high as to exceed the limits of the chain.

Additionally, here’s the relevant section from [ERC-7955](https://github.com/ethereum/ERCs/pull/1052/files#diff-7982f33c6a3421dc20ea9a40957801b01b45c0f80ca27766d71346e025470fa4):

> It does not work on chains that only accept EIP-155 replay-protected transactions.
> It is sensitive to changes in gas parameters on the target chain since the gas price and limit in the deployment transaction is sealed, and a new one cannot be signed without a private key.
> Reverts, such as those caused by alternative gas schedules, make the CREATE2 factory no longer deployable.

And here are [notes](https://github.com/ipsilon/eof/issues/162#issuecomment-2538446370) from [@pcaversaccio](/u/pcaversaccio) based on his experience developing the CreateX factory:

> Also, there are many RPCs that don’t support per-EIP-155 transactions even though at the network level it would be supported (reason being that Geth defaults to non-support of pre-EIP-155 transactions since Berlin; see ethereum/go-ethereum#22339) as well as networks that simply don’t support pre-EIP-155 transactions. Furthermore, some note on why Nick’s method doesn’t scale: I have 3 presigned transactions for CreateX creation available (see here), with one having 45m gasLimit. The last one couldn’t be broadcasted on Ethereum due to today’s block gasLimit. But even that one wouldn’t be enough to e.g. deploy on Filecoin, which requires more than 100m gasLimit.

I think Nick’s Method as well as ERC-7955 are beautiful workarounds, but they’re not reliable solutions and this seems to be widely understood, so the status quo in my opinion is that this problem is not solved. [@norswap](/u/norswap) Let me know if you disagree with this!

---

**norswap** (2025-08-08):

Thanks for clarifying, and sorry, I read the bulleted list in the EIP as being what you were proposing, not what the previous method was.

So I suppose the succinct version of your proposal is “create a new precompile (actually a pre-deploy) for the deterministic deployment factory”.

That makes a lot of sense, I think it’s great ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

---

**frangio** (2025-08-08):

Got it, will try to clarify in the EIP.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/norswap/48/4243_2.png) norswap:

> create a new precompile (actually a pre-deploy) for the deterministic deployment factory

Yeah, I’m avoiding the term precompile because it’s quite different, and predeploys in Ethereum so far have been done using Nick’s method, so this is a new category of thing.

---

**ernestognw** (2025-08-26):

Hi [@frangio](/u/frangio), I have a question about the approach taken in this EIP.

Could EIP-7702 + Nick’s method solve the same problem?

Essentially, Nick’s method can’t be replicated in every chain given EIP-155 and the `chainId`. However, this is not an issue for EIP-7702 delegations since they allow the `chainId` to be 0. In this way, one could:

1. Use Nick’s method to create a “keyless” address with a random signature
2. Use EIP-7702 to delegate that address to the factory code on every chain
3. Result: The same factory exists at the same address everywhere, deterministically and trustlessly (nobody has the private key)

If this is correct, then the deterministic factory could be achieved without requiring protocol changes. Thanks for your thoughts!

---

**frangio** (2025-08-26):

Yes, EIP-7702 can help. The exact scheme you described doesn’t work because the random signature can only be generated for a specific delegation, so it’s tied to the address of the delegation target, and you’d need the delegation target to be a multi-chain factory which is exactly what you don’t have and are trying to obtain, so it’s back to step 0. But EIP-7702 can be used in the way that [ERC-7955](https://eips.ethereum.org/EIPS/eip-7955) has proposed. This is mentioned in one of the alternatives in the Motivation section, along with why I don’t think it’s a complete solution.

---

**ernestognw** (2025-08-26):

> it’s tied to the address of the delegation target

Yes, I missed that.

In any case, deploying the delegation target on every EVM chain is already possible with the same mechanism as pcversaccio’s [CreateX](https://github.com/pcaversaccio/createx). I would’ve thought the delegation target doesn’t really matter if it’s the bytecode described in EIP-7997

Thanks for clarifying!

---

**nlordell** (2025-09-04):

Random shower thought: since the contract is being deployed to the precompile range - why isn’t it just specified as a precompile instead of being implemented as EVM code? Just felt odd that this would be the only precompile with non-zero `extcodesize`.

---

**frangio** (2025-09-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nlordell/48/10721_2.png) nlordell:

> why isn’t it just specified as a precompile instead of being implemented as EVM code?

As far as I know core devs are generally wary of precompiles. They’ve caused consensus bugs in the past, which is why there’s discussion (though no plans yet) to replace precompiles with EVM (or RISC-V) contracts. In this case, since the contract isn’t meant to offer optimized gas costs (like say `modexp`) and there’s a very clear EVM implementation, I thought that was the easiest way to specify the feature. However, I’m open to it being done as a precompile if that’s core devs’ preference, I’ll be asking for feedback soon.

---

**zergity** (2025-09-08):

How about a new `CREATE3` opcode that ignore the sender address?

---

**frangio** (2025-09-13):

I’m considering withdrawing this EIP based on [data collected by @nlordell](https://gist.github.com/nlordell/79208037f013a91f2965d74e221bc402) and [further data collected by me](https://gist.github.com/frangio/795b121e384f7bdb9ab1793a5c66c934#file-results-txt) which shows that, in practice, Nick’s Deterministic Deployment Proxy is very widely available. Out of ~2350 chains in [chainlist.org](http://chainlist.org) (including testnets) about 550 have the factory available.

So I’m now thinking that a more productive approach is to “enshrine” it as a preinstall in new chains like proposed by [RIP-7740](https://github.com/ethereum/RIPs/blob/master/RIPS/rip-7740.md).

I’d personally modify RIP-7740 to remove all other factories, and encourage people to use this one, so that it gains the momentum necessary to make it obvious to chains that they must have it available. That said, it clearly already has momentum and we should keep adding to it.

I do want to point out that the technical issues with this factory remain. First that the one-time transaction may not work on some chains, and second that it isn’t post-quantum resistant, although as far as I can tell the only thing a quantum adversary could do is introduce censorship into the factory. In either case, the solution is to make it a preinstall. I’m looking for ways in which we could make this somehow a default or as easy as possible. Ideally this would come out of the box in Ethereum execution clients (my motivation for making this EIP) but this seems quite unorthodox.

---

**rmeissner** (2025-10-20):

[@frangio](/u/frangio) Would be happy if you propose the changes to the RIP and add yourself as an author.

do you think it would be ok that we have the other factories as “recommendations”. I think in RFC words Nick’s factory would be a MUST, while the others would be a SHOULD.

I am currently only loosely following the RollCall schedule, but happy to coordinate that we join there to make a case (again) for this RIP.

---

**ADMlN** (2026-01-07):

On monday, [@fjl](/u/fjl) argumented in favor of this EIP and most ACD participants agreed to CFI it AFAIK. [@frangio](/u/frangio) Can you provide an update whether you are still considering withdrawal of this EIP or whether there is any kind of adjustment to be made to it?

---

**frangio** (2026-01-13):

As far as I know there are no technical issues with this EIP that merit withdrawal. One thing to review is the address where the factory code is deposited. I chose a precompile-like low address but I think it’s easy to argue that choosing a random address will better ensure it’s not used anywhere.

The reasons I considered withdrawing were “social”. The value of this factory depends on it being available everywhere, we don’t know how long it’s going to take to diffuse, it depends on chains upgrading, and there will be a period during which existing factories have wider availability. I do think these things need to be weighed, but based on ACD discussion this appears to be a very low effort upgrade with asymmetric potential upside.

The potential negative effect of shipping this upgrade is eating into the network effects of those existing factories, but I’m not convinced that this is a strong argument.

---

**shemnon** (2026-01-20):

Adding a contract like this requires new functionality for all the clients: inserting a contract at a fork. Which is a non-trivial task.

Combine this with a question as to why this is better than the [arachnid CREATE2 contract](https://github.com/Arachnid/deterministic-deployment-proxy) and the [RIP-7740 “Preinstall deterministic deployment factories”](https://github.com/ethereum/RIPs/blob/master/RIPS/rip-7740.md) list that has the arachnid CREATE2 deployer on the list for recommended pre-deployed utility contracts, addressing the diffusion aspect.

So between the effort of new work vs. the availability of a reasonable alternative, it’s not a social problem as much as a project management issue: the expected value of success is lower than the effort needed to achieve it.

---

**fvictorio** (2026-01-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> although as far as I can tell the only thing a quantum adversary could do is introduce censorship into the factory

For the record, we talked about this with frangio and realized that a quantum adversary could do something worse than censoring.

Deterministic factories normally return the address of the deployed contract. If you are using a factory without verifying that the returned address matches the expected CREATE2 address, then the compromised factory could deploy something completely different and return that address instead.

To be more specific, the scenario is:

1. There is a new chain in town.
2. The private key of a factory deployed using Nick’s method is obtained.
3. An attacker deploys a compromised factory, which will have the same address if this is the first transaction sent with that account.
4. Someone uses the factory as usual and relies on the returned address without double-checking that it’s the one that they expect.

---

**fjl** (2026-01-29):

We have since discovered new use cases for this in EIP-8141. In particular, it would be very good to have EIP-7997 available as a canonical deployment mechanism for smart accounts.

Pointing to a precompile as the deployer is very nice because it is an obvious choice for allow-listing in mempool.


*(4 more replies not shown)*
