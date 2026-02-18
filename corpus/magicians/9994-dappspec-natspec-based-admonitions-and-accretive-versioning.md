---
source: magicians
topic_id: 9994
title: "Dappspec: Natspec-based Admonitions and Accretive Versioning"
author: sbacha
date: "2022-07-19"
category: Magicians > Process Improvement
tags: [evm, solidity, versioning, natspec]
url: https://ethereum-magicians.org/t/dappspec-natspec-based-admonitions-and-accretive-versioning/9994
views: 719
likes: 0
posts_count: 1
---

# Dappspec: Natspec-based Admonitions and Accretive Versioning

# Dappspec

[Dappspec](https://sambacha.github.io/dappspec/)

Well-Auditable code is easier to enforce and produce when there are formats and processes that are generally accepted and well thought out. This is an initial attempt at making Solidity’s Natspec more useful than it currently is today with respect to documenting code bases.

[TLDR: here is a first draft of the generated docs](https://sambacha.github.io/dappspec/)

Dappspec

> does AUTOGENERATE docs
> does VERSIONING codebases
> does NOT deal with packaging
> does NOT deal with distribution

## Versioning

Why keep versioning separate from package managers? Developers can then pick how they want to ingest the artifact without reliance on using one service/distribution mechanism. Also, versioning for package managers is closely related to proprietary semi-deterministic processes to generate ‘lockfiles’ that are used in the versioning of the artifact distributable. By using the concept of accretive versioning (as discussed below), we can make contract versioning much easier and more importantly much more relevant and informative to the developer than current regimes of semantic or calver usage currently.

> Much of this builds on Rich Hickey’s talk, ‘Spec-Ulation’ + Haskell’s Package Manager

There are two orthogonal problems when importing an external dependency (generally):

**Availability**: Will A be available at the host site?

**Compatibility**: Will the version of A available at the host is compatible with P?

Versioning in this regard is referred to as **Accretive Versioning**[[1]](#footnote-26918-1)

**Accretive versioning is based on matching type signatures against a generated ABI V2.**

Imagine a package manager that ran the test suite of the version you’re currently using against the code of the version you’d like to upgrade to, and told you exactly what wasn’t going to work. This is a lofty goal, and for the purposes of this discussion worthwhile to mention but beyond the scope of this spec (and intro).

Basically, take the compiler’s ABI-generated artifact, and generate a solidity interface from that ABI, that is your ‘version’.  Mark functions depreciated minor increments or patch. Those specifics I have not narrowed down yet, but I think the idea of automated versioning via diffing generated interfaces warrants further investigation as it’s simple, robust (at least for our purposes, YMMV when traveling into other ecosystems), and best of all, automated. The issues with Semver et al are all due to the human inference into the process of creating a versioned release, which is why you see such applications such as changesets / semantic versioning CI pipelines that try to automate this away from developers’ interjections.

[Additionally, with well-versioned artifacts, things like scoping become easier to do](https://github.com/sambacha/forge-scope). Note that I mention this here only to provide additional context as to how an implementation may look like for persisting that sort of versioning information (hint: it is not going to be in your TOML file).

### Forge Tags

Originally the issue I was wanting to resolve was not using git submodules. There is a GitHub action at the repo that handles git tagging with these semantics (not this is not per see Accretive Versioning!)

#### Forge Tagging Releases GitHub Action

By default, if you do not pass a `tags` input this action will use an algorithm based on the state of your git repo to determine the Foundry/DPack tag(s).

Below is a table detailing how the GitHub trigger (branch or tag) determines the Foundry tag(s).

| Trigger | Commit SHA | addLatest | addTimestamp | Foundry Tag(s) |
| --- | --- | --- | --- | --- |
| /refs/tags/v1.0 | N/A | false | N/A | v1.0 |
| /refs/tags/v1.0 | N/A | true | N/A | v1.0,latest |
| /refs/heads/dev | 1234567 | false | true | dev-1234567-2021-09-01.195027 |
| /refs/heads/dev | 1234567 | true | false | dev-1234567,latest |
| /refs/heads/master | 1234567 | false | true | master-1234567-2021-09-01.195027 |
| /refs/heads/master | 1234567 | true | false | master-1234567,latest |
| /refs/heads/SOME-feature | 1234567 | false | true | some-feature-1234567-2021-09-01.195027 |
| /refs/heads/SOME-feature | 1234567 | true | false | some-feature-1234567,latest |

The Accretive versioning spec is not formalized yet, so would like to hear any feedback at all.

## Dappspec: @custom/natspec:

Dappspec takes the` @custom:... natspec`  tag and provides a list of admonitions for generating documentation for Solidity contracts.

The Specifics Admonitions include identifiers for code blocks that reference gas optimizations, assembly blocks and emit events.

The @custom: security tag is used by OpenZeppelin for identifying the point of contact. Similar to security.txt, [see an example here](https://www.manifoldfinance.com/.well-known/security.txt)

The General Admonitions are meant to render the docstring content as a code block that you would find in generators like mkdocs. [see squidfunk.github.io/mkdocs-material/reference/admonitions/#supported-types](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#supported-types)

The style of how to do `@custom` tags is  not decided yet, in fact I just yesterday added the container OCI schema as a potential way of doing it

```auto
/**
 * @custom:org.label-schema.security='ops@manifoldfinance.com'
 * @custom:org.label-schema.support='github.com/manifoldfinance/support'
 * @custom:org.label-schema.vcs-url='github.com/manifoldfinance'
 * @custom:org.label-schema.vendor='CommodityStream, Inc'
 * @custom:org.label-schema.schema-version="1.0"
 */
```

## Documentation:

Autogenerated and opinionated: this is from the ‘literate programming’ movement, originally sourced from ‘groc’, [see more here https://github.com/nevir/groc/blob/master/README.md](https://github.com/nevir/groc/blob/master/README.md)

Basically, This all builds on each other: Versioned well documented, and oriented towards lowering friction both on the developer side and consumer side.

If any of these ideas / etc are of interest do not hesitate to reach out!  Your feedback is most welcomed, If I am missing something obvious pray please tell me.

Thank you,

Sam

1. The Monad.Reader/Issue2/EternalCompatibilityInTheory - HaskellWiki ↩︎
