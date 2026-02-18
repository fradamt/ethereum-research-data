---
source: magicians
topic_id: 25059
title: "New EIP: A Standard for Composable Token Policies (RWAs, Gaming & More)"
author: SuperDevFavour
date: "2025-08-11"
category: EIPs > EIPs interfaces
tags: [erc, nft, token, erc-721]
url: https://ethereum-magicians.org/t/new-eip-a-standard-for-composable-token-policies-rwas-gaming-more/25059
views: 136
likes: 6
posts_count: 2
---

# New EIP: A Standard for Composable Token Policies (RWAs, Gaming & More)

Hello everyone,

I’ve been wrestling with a problem that I believe will only become more critical as Ethereum continues to absorb real-world use cases, and I wanted to get this community’s feedback on a potential solution.

### Summary / TL;DR

I’m proposing a two-part EIP standard to handle token transfer restrictions in a way that doesn’t break composability.

1. A “Token Layer” EIP that lets a token point to an external “Policy Contract.”
2. A “Policy Layer” EIP that creates a registry for standard policy interfaces (like whitelists, vesting schedules, etc.), so dApps can actually understand the rules.

The goal is to stop the fragmentation we see with RWA and gaming tokens and allow them to play nicely with the existing DeFi ecosystem.

### The Problem: The Coming RWA Composability Crisis

We all know the power of DeFi comes from composability, the “money legos” a la Aave, Uniswap, Maker, etc. This works because ERC-20 is a simple, predictable standard.

But now, consider Real-World Assets (RWAs). A token representing a share of stock *must* have rules. It can’t be transferred to a non-KYC’d address or a wallet in a sanctioned country. Today, projects solve this by hard-coding custom, unique logic into their token contracts.

- TokenA from Company A has a simple isWhitelisted() check.
- TokenB from Company B has a isWhitelisted() check AND a isLockedUp() time check.
- TokenC (a gaming NFT) has a isBoundToPlayer() check.

A DeFi protocol like Aave can’t support any of these without writing expensive, custom, one-off integrations for each. The tokens become isolated islands, unable to participate in the broader DeFi ocean. We’re heading towards a future of massive fragmentation.

### A Proposed Two-Layer Solution

Instead of coding rules *inside* the token, what if the token just delegated the decision?

**EIP-A (The “Port”):** A super simple standard (let’s call it `ITokenPolicyAware`) that adds a single function to a token: `policyContract() returns (address)`. This just points to the contract that holds the rules. The token itself stays simple.

**EIP-B (The “Devices”):** This is the crucial second piece. An on-chain registry where developers can register their policy contracts against standard interfaces (`IWhitelistPolicy`, `IVestingPolicy`, etc.) using the EIP-165 standard.

This means a dApp can not only see *that* a token has rules, but it can query the registry to find out *what kind* of rules it has, and interact with them in a predictable way. It’s like moving from proprietary charging ports to a universal USB-C standard where the system can identify the device you just plugged in.

### A Quick Example: How Aave Wins

1. Alice tries to deposit $FUTR, a tokenized stock, into Aave.
2. Aave sees $FUTR implements EIP-A and calls policyContract() to get the policy address.
3. Aave asks the EIP-B Registry: “What kind of policy is this?”
4. The Registry replies: “It implements the standard IVestingPolicy interface.”
5. Aave now knows it can call standard functions like releasableAmount(alice) on the policy to calculate her actual liquid collateral, ignoring the locked portion.
6. Aave accepts the deposit, fully understanding the token’s properties, all without any custom code.

### Questions for the Community

This is just an idea, and I’m here to have it stress-tested and improved.

1. Is this a problem you’ve encountered or anticipate? Is the fragmentation threat real?
2. Is the two-EIP approach (separating the token layer from the policy registry) the right call? Or would a single, monolithic standard be better?
3. Beyond whitelists and vesting, what other “standard policy interfaces” would be most immediately useful for your projects? (Taxation? Cooldowns? KYC tiers?)
4. What are the biggest security risks or economic exploits this system might introduce?

Looking forward to hearing your thoughts and tearing this idea apart to build it back stronger.

Cheers,

`@SuperDevFavour`

## Replies

**vitali_grabovski** (2025-09-16):

Hello @ [SuperDevFavour](https://ethereum-magicians.org/u/SuperDevFavour). We have been working with compliance and dynamic blockchain policies for a very long time (from the making way to declare dynamic rules on-chain up to drafting an ERC standard on the topic), and I can confirm the arguments, problems, and motivation raised in your message. The ‘isolated islands’ is a good metaphor in this context.

The need for a clear separation between contract logic and policy logic, as well as for composability and flexibility, is crucial – especially for RWAs, gaming, and other regulated use cases, which seem to be increasing in number daily. And I would also pick ‘reusability’ (full or partial) as an important trait for on-chain policy.

I’d encourage you to check this proposal [ERC-8006 (Universal Policy Engine)](https://ethereum-magicians.org/t/erc-8006-universal-policy-engine/25155) which solves mentiond problems and provides required capabilities. This is achieved through DAG/nodes architecture, where each node is a rule of policy

