---
source: magicians
topic_id: 3748
title: Core Paper Project of EVM
author: sorpaas
date: "2019-11-02"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/core-paper-project-of-evm/3748
views: 940
likes: 2
posts_count: 4
---

# Core Paper Project of EVM

[github.com](https://github.com/corepaper/evm)




  ![image](https://opengraph.githubassets.com/4d22c2c97fbcf15bdf5300aa0475354e/corepaper/evm)



###



The Core Paper Project of EVM










Quote from the README:

> The current EIP and ECIP process basically composes of
> “changelogs”. We define, as informal specifications, about what is
> changed when the EIP is applied. This works well for simple changes
> such as gas cost modification and opcode addition, because the change
> is only at a single point and assumed not to affect the rest of the
> system.
>
>
> However, totally relying on changelog format has its expressiveness
> limit. For pressing issues on Ethereum we’re facing nowadays, many
> structual and potentially complex changes of the EVM are required. When
> writing them under EIP “changelog” format, it’s both hard for authors
> to express themselves, and for readers to understand the
> specification. This has led to confusions and implementation consensus
> issues in the past. What’s more, some of the previously-thought single
> point changes turned out to affect a larger part of the EVM, such as
> EIP-1283 and EIP-1884, relying on changelog format solely made it
> harder for readers to review those effects.
>
>
> The Core Paper Project of EVM is an attempt to address those
> issues. Instead of one-step “changelog” process as in EIP and ECIP,
> here feature upgrades are defined under a two-step process:
>
>
> Refactoring: Any new feature upgrades is identified as a “module
> change”. We first refactor the whole EVM specification to get a
> functionally equivalent specification.
> Module change: We then add the module change, and write the
> “changelog” simply as the actual module change.
>
>
> As an example, to add new EVM features that require additional
> validation step in the beginning, we first refactor the whole EVM
> specification to have a no-op validation step, which is functionallly
> equivalent to what we have now. After that, the new feature can simply
> be added as an additional module. This process is much more clear
> compared with the changelog process.
>
>
> At the same time, we hope the modular design and specification allow
> reusibility outside of the context of Ethereum and Ethereum Classic,
> and can encourage better standardization, for EVM features that are
> not designed for Ethereum or Ethereum Classic mainnet.

The current goal is to define account versioning using the *core paper format*, and see how it goes.

## Replies

**boris** (2019-11-02):

Hey [@sorpaas](/u/sorpaas) – any reason to not contribute to the Jello Paper? https://jellopaper.org/

I don’t think you’re going to see lots of adoption of this, and adding to the quality of the Jello Paper is likely a better path. At our RUNEVM, we had already talked to eg. Monax (Hyperledger Burrow) and other non-core-ETH teams about this. I can point some of them at this, but I still think the formal verification path of Jello Paper is a better direction.

---

**sorpaas** (2019-11-02):

Jello paper looks like exact replication of yellow paper with formal verification. I don’t think that suits the need for what Core Paper of EVM tries to accomplish, which is about a specification that is modular, and suitable for upgrade process.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> I don’t think you’re going to see lots of adoption of this

That’s rude. Core Paper of EVM is planned to be a modular specification for [Substrate EVM](https://github.com/paritytech/substrate/pull/3927). No disrespect, but that is, in my opinion, better adoptions than just “talking with teams”.

---

**boris** (2019-11-02):

No rudeness intended.

I think of formal verification like CI/CD being built into the spec — knowing that it’s always correct. For key things like the EVM — I think it’s very important.

If you intend to include formal verification into Core Paper — great. See what you can learn from the Jello Paper.

