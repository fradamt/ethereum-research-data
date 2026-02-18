---
source: ethresearch
topic_id: 13572
title: Permissioned Privacy Pools
author: ameensol
date: "2022-09-04"
category: Applications
tags: []
url: https://ethresear.ch/t/permissioned-privacy-pools/13572
views: 4428
likes: 11
posts_count: 6
---

# Permissioned Privacy Pools

# Permissioned Privacy Pools

Ethereum users wish to protect their privacy while interacting with the blockchain. The only practical way for users to fund a *fresh* Ethereum address is through the use of a privacy pool. In this post we start a discussion on various designs for a *permissioned privacy pool* which allows users to protect their privacy, but can also allow operators to keep unwanted participants out of the pool.

There are two basic approaches to permissioned privacy pools, which can be combined. The first is to curate an “allowlist” of addresses that are allowed to deposit. The second is to curate a “blocklist” of unwanted addresses, and require a ZKP from users upon withdrawal that their deposit address is *not* part the blocklisted addresses.

### Allowlist

The purpose of an allowlist is to *proactively* limit privacy pool participation to approved entities only. This could be token holders, NFT holders, all unique humans according to [Proof-of-Humanity](https://www.proofofhumanity.id/), or be based some other scheme.

By itself, an allowlist only provides surface level protection against unwanted deposits. If an unwanted address is mistakenly added to the allowlist, then the address will be able to deposit into a privacy pool until its access is revoked. To mitigate the potential damage from a single mistake, rate-limits can be imposed on each deposit address. More trustworthy deposit addresses can have higher rate limits. This would also help mitigate the risk of approved entities going rogue and abusing their access to a privacy pool.

### Blocklist

Vitalik explains the basic outline of a blocklist-enabled privacy pool in this [clip](https://www.youtube.com/clip/Ugkx7LeQPvONM0OFOfAUazyjf0JSj_9y7Tqw).

The purpose of a blocklist is to *reactively* restrict privacy pool withdrawals from unwanted depositors. The fundamental challenge is identifying which deposit addresses to restrict, which requires imposing a time delay (e.g. 1 week) between deposits and withdrawals. To be effective, a blocklist would need to be seeded with known unwanted addresses (e.g. addresses responsible for hacks), but also expanded to trace all addresses downstream from the initial set, including tracking cross-chain activity. Due to the computational complexity of tracking unwanted addresses, effective blocklists will likely be only queryable offchain. For onchain authentication, blocklists can publish merkle roots directly onchain periodically, or sign an offchain merkle root that can be passed along with a user’s withdrawal payload.

When attempting to withdraw from a privacy pool with a blocklist, the user would have to provide proof that:

- their deposit is valid and unspent (as usual)
- the time delay has passed (e.g. 1 week)
- their deposit is not a member of the blocklist

If a deposit *is* a member of a blocklist, the withdrawal can be prevented outright, but there are other options as well:

- allow the user to withdraw, but force a withdrawal to the original deposit address
- same as above, but also charge a “blocklist exit tax”

Blocklists could also be combined with allowlists to also prevent approved depositors who go rogue from abusing the privacy pool.

To pay for the cost of managing the blocklist and querying depositor addresses, a small fee on all deposits/withdrawals would likely be necessary.

In theory, a sufficient powerful blocklist makes an allowlist unnecessary. In practice, using an allowlist to gate deposit access would mean far fewer blocklist queries—it would only be necessary to monitor for allowlist addresses being added to the blocklist.

### MVP Implementation Considerations

A privacy pool using only an allowlist is relatively easy to implement. The operator could be a multisig or a DAO, depositors rate limited to 1 ETH per day. If a DAO is managing approvals, revocations could still be delegated to multisigs for expediency. With the goal of trying to keep unwanted addresses out, it may make more sense to have many smaller permissioned privacy pools instead of one really big one, with each pool better able to manage its allowlist.

Implementing a blocklist has additional challenges. Currently the only offchain lists of unwanted addresses are published by Chainalysis and TRM Labs. The lists would need to be aggregated and published in a format friendly for authentication as well as generating the ZKP for both proof-of-exclusion.

Ideally the blocklist publisher would be a separate entity than the privacy pool operator, so there may be a role for an independent community operated blocklist publisher in the future as well. Multiple privacy pools could benefit from pointing to the same blocklist.

### Next Steps

This was a quick intro post to frame the problem and the solutions at a high level, but more work is needed to propose and evaluate implementation details.

We have assembled a small Privacy 2.0 R&D working group to discuss implementation - please DM me on twitter to join the discussion.

## Replies

**MicahZoltu** (2022-09-04):

Once created, the power to censor individuals will eventually be captured.  By creating a whitelist/blacklist, you are creating the power to censor and even though you plan to only use that power for good, eventually bad people will gain control of that power and use it for evil.

Separately, what exactly are you trying to achieve with this strategy?  The US government has shown a complete unwillingness to care about any internal attempts at complainer, as shown by the fact that Tornado has a compliance tool which the US completely ignored when they sanctioned Tornado.  I suspect that creating censorable privacy tools won’t cause the USG to suddenly behave rationally/reasonably, so all you would be accomplishing is creating tools that will eventually be used by bad people to do bad things.

If there was some way to prevent censorship from being used by bad people to censor good people then I think it may be worthwhile to investigate, but history has shown us that censorship begets censorship and this is a slippery slope that human governance institutions have repeatedly slid down.

---

**Kames** (2022-09-05):

Thanks for kicking off these conversations [@ameensol](/u/ameensol) ![:handshake:](https://ethresear.ch/images/emoji/facebook_messenger/handshake.png?v=12) super important!

I’ll share some of the ideas/thoughts expressed in the Telegram channel earlier.

## General Allowlist/Deposit Strategy

Organizations and Institutions are bad arbiters of truth by themselves.

W3C specifications like Decentralized Identifiers and [Verifiable Credentials](https://www.w3.org/TR/vc-data-model/) offer a neutral infrastructure for distributed AccessControl networks using Public Key Infrastructures (PKIs) and/or Web of Trust systems. Issuers (centralized or decentralized) can issue Verifiable Credentials containing attestations required for entering network/zone specific PrivacyPools.

One setup I’ve been thinking about recently is a “Double Gated Entry” protocol that would utilize the current zero-knowledge stack, EVM Object Capabilities and a JIT AccessControl System that consumes trusted Verifiable Credentials.

The idea relies heavily on [Delegatable](https://github.com/delegatable/delegatable-sol) - an EVM Object Capabilities framework architected by Dan Finlay and Rick Dudley.

## Double Gated Entry (Privacy Pools w/ JIT AccessControls)

The Double Gated Entry MVP would use **Verifiable Credentials** in combination with Delegatable to issue time/block constrained **AccessControls** for public **PrivacyPools**.

The premise of the Delegatable smart contract framework is to scale on-chain AccessControl using off-chain Delegations/Invocations; enabling chainable multi-party signatures.

What’s interesting about the framework is fine-grained AccessControl enforcement not available in native EVM transactions. For example timestamp and/or blockNumber constraints can easily be added to a multi-party-signing setup i.e a User can be authorized to execute a transaction in 2-3 hour window, and afterwards the signature will be invalid -  the complete opposite of today’s unbounded permissions.

**Example:**

- TrustAnchor issues Credential to Alice
- Alice shares Credential with AccessControlGateway
- AccessControlGateway validates Credential and issues JITAccessControl to Alice
- Alice invokes JITAccessControl on PrivacyPool consuming AccessControlGateway packets

**TrustAnchors** in this example would issue KYC compliant Verifiable Credentials.

**AccessControlGateways**, using a public key infrastructure, could easily lookup what TrustAnchor(s) are following open standards for KYC compliant Verifiable Credentials.

**PrivacyPools** using on-chain governance, can be configured to accept JITAccessControl packets from trusted AccessControlGateways.

For example Coinbase, ConsenSys and Kraken could create a Verifiable Credential consortium known to prove *non-baddy* status. Anyone can run AccessControlGateways consuming the Credentials issued by the this Open Web3 Consortium. And PrivacyPools can partner with AccessControlGateways, depending on their unique jurisdictional requirements.

The splitting of responsibilities (issuing/consuming of Verifiable Credentials) is both convenient technologically and culturally (governance) because it can be implemented to respect neutrality, while limiting liability for Corporations providing essential AccessControl infrastructure.

Additionally, a peer-to-peer verifiable credential issuance network could also established; eliminating reliance on only centralized authorities being arbiters of truth for access to PrivacyPools.

---

**k1rill-fedoseev** (2022-09-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/ameensol/48/1455_2.png) ameensol:

> If a deposit is a member of a blocklist, the withdrawal can be prevented outright, but there are other options as well:
>
>
> allow the user to withdraw, but force a withdrawal to the original deposit address
> same as above, but also charge a “blocklist exit tax”

The third option here is to make blocklist in a non-restrictive, permissionless and censorship-resistant way. System can allow its users to selectively choose subset of all “unwanted” deposits they don’t want be associated or mixed with. Default frontend could simply use Chainalysis / TRM Labs endpoints for determine such subsets, but anyone is free spin up their own frontend with any other provider or even without such provider at all.

This way the system does not introduce any vendor lock or censorship risks, as each user is free to selectively choose their anonymity subset by themselves.

As long as the majority of system users would continuously mark the same set of “unwanted” deposits and prove their withdrawal is not associated with any of them, the system would eventually split into 2 anonymity subsets of “good-only” and “bad-only” deposits.

If the “bad” funds can only be mixed within the “bad-only” subset among other “bad” funds, then there is no real purpose in using such system for “bad” actors in the first place, eventually reducing the total number of “bad” actors in the system as a whole.

---

**branigan.eth** (2022-09-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/ameensol/48/1455_2.png) ameensol:

> Ideally the blocklist publisher would be a separate entity than the privacy pool operator, so there may be a role for an independent community operated blocklist publisher in the future as well. Multiple privacy pools could benefit from pointing to the same blocklist.

+1

IMO endgame for privacy needs modular layers throughout the tech stack.

- A modular layer that just publishes and labels addresses is necessary for legal decentralization because publishing a list of addresses is pure speech and will be censorship-proof per the First Amendment.
- Right now this role is filled by TRM and other private companies that do not “show their work.” The decentralized solution should make its process and product open source.

---

**0x132fabb5bc2fb61fc6** (2024-03-06):

I realize this is an older thread, but I came across the implementation on GitHub and am curious if there have been any attempts to audit the codebase. I’m particularly interested in the security aspects and implementation details. There’s a fork that has introduced some additional features and is currently seeking support for a security audit. I unfortunately cannot include a link, but the user on GitHub is 0x132fabb5bc2fb61fc68bcfb5508841ddb11e9.

