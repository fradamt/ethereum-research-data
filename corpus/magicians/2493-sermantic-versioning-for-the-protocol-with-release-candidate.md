---
source: magicians
topic_id: 2493
title: Sermantic versioning for the protocol, with release candidates
author: jpitts
date: "2019-01-21"
category: Magicians > Primordial Soup
tags: [core-devs, forks, consensus-protocols]
url: https://ethereum-magicians.org/t/sermantic-versioning-for-the-protocol-with-release-candidates/2493
views: 1788
likes: 4
posts_count: 7
---

# Sermantic versioning for the protocol, with release candidates

From my comment in the  [Jello Paper](https://ethereum-magicians.org/t/jello-paper-as-canonical-evm-spec/2389/23) discussion:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png)[Jello Paper as Canonical EVM Spec](https://ethereum-magicians.org/t/jello-paper-as-canonical-evm-spec/2389/23)

> One notion that I arrived at is that the protocol should itself have semantic version, and that its component parts, i.e. the EVM, consensus, RLP, JSON-RPC, each should have semantic versions. Within their various contexts, the versioning changes would have different meaning.
>
>
> Semantic Versioning 2.0.0
>
>
> Ethereum protocol would increment MAJOR when the update to any of its components leads to a fork.
>
>
> EVM would increment MAJOR only if the update leads to incompatibility or security vulnerability (given contract development norms). MAJOR version increments in EVM is similar to a new series in microprocessors. But MINOR version increments in the EVM would lead to a MAJOR increment at the protocol level.

And regarding “release candidates”, copying my [comments from AllCoreDevs gitter](https://gitter.im/ethereum/AllCoreDevs?at=5c45f1c19bfa375aab38ddc0) here:

> Protocol updates could follow the practice of “release candidate” within the semantic numbering scheme. And these clever release names, this is over-arching for the upgrade initiative and sticks once it stabilizes on mainnet. Constantinople is what you are attempting to get mainnet to.
>
>
> So what you attempted to release was ethereum-8.0.0-rc1, released to the testnets and prepared for mainnet. An issue was found, therefore rc1 was aborted. The main network remains at ethereum-7.x.x. Now you proceed with ethereum-8.0.0-rc2, first on ropsten, etc, and then attempt to release to mainnet.
>
>
> The “release candidate” approach allows you to keep attempting to get from 7.x.x to 8.0.0, by incrementing the x in 8.0.0-rcx. It allows you to not have to worry about the name, which is marketing and communication to the wider community. Once a stable rc-x happens on mainnet, well, IMO that is what becomes “Constantinople”

## Replies

**jpitts** (2019-01-21):

Here’s a [gist](https://gist.github.com/jpitts/4c541a4efa2f8872ce9acf63da5c4921) depicting what the versions of the protocol would look like, only a sketch. The rc1 and rc2 of Constantinople should have notes about which testnets they were released to, accurate representation of EIP changes, etc.

https://gist.github.com/jpitts/4c541a4efa2f8872ce9acf63da5c4921

---

**axic** (2019-01-21):

A similar proposal was made back here: https://github.com/ethereum/EIPs/issues/178

It comes with some differences:

- only considers EVM,
- because of this goes well with https://github.com/ethereum/EIPs/issues/154,
- only uses major/minor in order to save space

---

**axic** (2019-01-21):

Because it only considers the EVM, the versions are a bit different - as an example the “DAO fork” doesn’t have a version.

Another question to consider if it is only for the EVM whether gas changes warrant a major version bump. Before gas changes (Spurious Dragon?) were added, it seemed as if gas cannot be changed. After that point though it felt like gas values cannot be relied on and are not to be considered a constant in contract development.

If gas costs are not considered, the version table looks quite differently.

---

**jpitts** (2019-01-21):

Thanks for the reference! I think that this could be used for advancing the version of the EVM component in a way that dapp developers can understand. Also it can inform how other protocol components might be versioned.

---

**jpitts** (2019-01-23):

It should be noted that in version 0.4.21, Solidity itself began to allow for the targeting of an EVM “version”.

Do developers have a difficult time knowing which EVM-related EIPs are included in these code-named releases?

> you can now specify which EVM version the contract should be compiled for. Valid values are “homestead”, “tangerineWhistle”, “spuriousDragon”, “byzantium” (the default) and “constantinople”. Depending on this setting, different opcodes will be used in some cases. The only place where this is currently used by default is that all gas is forwarded with calls starting from “tangerineWhistle” (in homestead, some gas has to be retained for the  call  opcode itself). Also, the gas estimator reports different costs for the opcodes depending on the version and thus the optimizer might generate different code.


      ![](https://github.githubassets.com/favicons/favicon.svg)

      [GitHub](https://github.com/argotorg/solidity/releases/tag/v0.4.21)



    ![](https://opengraph.githubassets.com/c3f6bdc698c9637dfbf7b35bc1179d44242d779f431254dbc1488e6f6930662f/argotorg/solidity/releases/tag/v0.4.21)

###



We again introduced several changes that are scheduled for version 0.5.0 and can be activated using pragma experimental "v0.5.0";. In this release, this pragma does not generate a warning anymore, ...

---

**jpitts** (2019-01-23):

FYI, I updated the gist of the protocol releases and EIPs in each.

https://gist.github.com/jpitts/4c541a4efa2f8872ce9acf63da5c4921

