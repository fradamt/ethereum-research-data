---
source: magicians
topic_id: 21436
title: "ERC-7803: EIP-712 Extensions for Account Abstraction"
author: frangio
date: "2024-10-22"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7803-eip-712-extensions-for-account-abstraction/21436
views: 184
likes: 0
posts_count: 4
---

# ERC-7803: EIP-712 Extensions for Account Abstraction

Discussion topic for EIP-7803:

https://github.com/ethereum/ERCs/pull/693

> This EIP improves on EIP-712 signatures to better support smart contract accounts by 1) introducing signing domains as a way to prevent replay attacks when private keys are shared across accounts, and 2) allowing dapps and wallets to coordinate on the method that will be used to authenticate the signature.

#### Update Log

- 2024-10-21: First draft
- 2024-10-30: Moved from EIPs to ERCs

## Replies

**ernestognw** (2025-06-05):

Hi [@frangio](/u/frangio),

I’ve been working extensively on accounts, and I remain convinced that sophisticated account abstraction use cases will require more robust schemes, such as ERC-7803, rather than ERC-7739

Particularly, cross-chain account interoperability seems more approachable if there are ways to rely on EIP-712 domains to construct cross-chain operations (e.g., intents). One strategy could be using `chainId(0)` to create intentionally replayable signatures across chains. I think these problems are more tractable with ERC-7803’s signing domain approach. See [Universal Cross-Chain Signatures for Account Abstraction](https://ethereum-magicians.org/t/universal-cross-chain-signatures-for-account-abstraction/24452)

On the security considerations side, I haven’t identified any particular concerns with the core mechanism. However, if this standard becomes a foundation for cross-chain setups, there may be some security aspects worth exploring (e.g., is using signing domains with `chainId(0)` the best approach for multi-chain signatures?).

I opened a PR expanding on the rationale and backwards compatibility sections. Would love to hear your thoughts.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1067)














####


      `master` ← `ernestognw:chore/elaborate-7803`




          opened 05:12AM - 05 Jun 25 UTC



          [![](https://avatars.githubusercontent.com/u/33379285?v=4)
            ernestognw](https://github.com/ernestognw)



          [+42
            -10](https://github.com/ethereum/ERCs/pull/1067/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/ERCs/pull/1067)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.












Another question, what do you think of enforcing `ERC-{n}` in the `id` field so that so that `ECDSA` is covered by ERC-7913?

---

**frangio** (2025-06-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ernestognw/48/7916_2.png) ernestognw:

> is using signing domains with chainId(0) the best approach for multi-chain signatures?

For multi chain signatures the chain id should be entirely omitted from the application domain (rather than setting it to zero).

But this does seem to require special support from ERC-7803. I think the wallet has to observe the application domain and make sure that if a multichain signature is requested the signing domains are also multichain. Even in a single chain setting the wallet would need to make sure the signing and application domain chain ids match. Alternatively, the signing domains should always be multi chain, which is easier to implement in the account (if the wallet supports both single and multi chain domains the signatures need a tag that indicates which domain to use, though arguably it’s a good idea to always tag signatures for versioning – note that this is out of scope of ERC-7803).

This requires some special wording in the ERC. Feel free to submit an update.

---

**ernestognw** (2025-06-15):

> signatures need a tag that indicates which domain to use

Yeah I was thinking the `signingDomain` itself includes a `chainId`, so by extending the `chainId=0` (or none), then each `signingDomain` would be tag as chain-specific or multichain too.

> This requires some special wording in the ERC. Feel free to submit an update.

It’s unclear what exactly needs special wording in the ERC. Multi chain signatures considerations are handled by the [cross-chain signatures proposal](https://github.com/ethereum/ERCs/pull/1069). Is the following what you were thinking of?

```auto
## Security Considerations

### Domain Validation Security

Improper domain validation by wallets can lead to signatures being valid in unintended contexts. The wallet validation requirements should ensure that domain mismatches are caught before signature generation.
```

