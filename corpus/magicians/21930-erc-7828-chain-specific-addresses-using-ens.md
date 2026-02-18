---
source: magicians
topic_id: 21930
title: "ERC-7828: Chain-specific addresses using ENS"
author: rudolf
date: "2024-12-02"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7828-chain-specific-addresses-using-ens/21930
views: 1575
likes: 16
posts_count: 17
---

# ERC-7828: Chain-specific addresses using ENS

[github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/735)














####


      `master` ← `jrudolf:master`




          opened 10:44AM - 27 Nov 24 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/2/2efedb0e53c6978d6883047b391e7ca44cbb1c1c.png)
            jrudolf](https://github.com/jrudolf)



          [+241
            -0](https://github.com/ethereum/ERCs/pull/735/files)













Description:

A unified chain-specific address format that allows specifying the account as well as the chain on which that account intends to transact.

## Replies

**kuzdogan** (2024-12-04):

Doesn’t this assume the desired L2 ENS names like `optimism.eth` and `arbitrum.eth` are all owned by the L2s? How does this proposal deal with squatting and other potential issues for future L2s? Or maybe I missed how rollup ENS name resolution is made.

Also this part didn’t seem consistent to me:

The spec:

```auto
chain ::=  |  |  .
user ::=  |
account ::= @
```

the note

> Note the difference between ens-name, which is a full ENS name, and ens-subdomain that is just a segment of a name between dots. E.g. user.app.eth is a name, user and app are subdomains.

and the examples below that:

```auto
Rollup
- 0x12345...6789@chainId
- 0x12345...6789@arbitrum.eth
- alice.eth@arbitrum.eth
```

According to the note `ens-name` is a full ENS name like `arbitrum.eth`. Since `chain` can be an `<ens-name> . <L1-TLD>` I’d have expected the `chain` to be `arbitrum.eth.eth`. Either the example " `user.app.eth` is a name" is wrong (`user.app` is the `ens-name`) or the spec should not have `<L1-TLD>` in `chain ::=`

---

**shemnon** (2024-12-04):

Why not adopt [CAIP-10](https://chainagnostic.org/CAIPs/caip-10)?  It’s a previously existing standard (but not an EIP) that occupies the same space, and either deserves deference or an explanation in the rationale why it was dismissed.

---

**rudolf** (2024-12-09):

thanks for the note, and definitely agree we shouldve made a note in the ERC. The main motivation for this rather than CAIP-10 is to optimize for human-readability. In addition to what Sam [mentioned here](https://ethereum-magicians.org/t/erc-7831-multi-chain-addressing/21942/3)

---

**VGabriel45** (2025-02-04):

Should ERC-7828 explicitly define a rule that only L2 projects themselves should register their own ENS domains?

---

**teddy** (2025-04-15):

Hello all!

I’ve proposed a binary representation for EVM and EVM-adjacent addresses: [ERC 7930: Interoperable Addresses](https://ethereum-magicians.org/t/erc-7930-interoperable-addresses/23365)

And did some work to adapt this ERC to be a potentially-resolved text specification of the above: [7828 name only rewrite by 0xteddybear · Pull Request #2 · jrudolf/ERCs · GitHub](https://github.com/jrudolf/ERCs/pull/2) (PR-to-a-PR, not ideal but the original one isn’t merged yet)

A quick roundup of our edits and the intentions behind them:

- Refer to a strict binary representation for addresses and chain ids (ERC-7930), and how to serialize from/to it, so wallets can reliably know what to convert the names to for uses such as e.g. intent building and cross-chain message passing.
- Defined a way to couple name’s TLDs to name resolvers, so alternatives to ENS can be used.

This allows to e.g. use the centralized chain list for now and seamlessly switch to ERC-7785 in the future.
- Defined how chains and addresses can be resolved via different methods
- Paves the way to stop maintaining the centralized list of chains, and maintain a much smaller list of chain name resolvers.

Defined checksum algorithm.
Defined how to store the naming registry used inside the binary address, so when it is turned back into text the name is always preserved.
Allowed to represent non-EVM addresses & chain ids
Allowed to represent only chain/address within the same standard

We found it also tangentially attacks some of the feedback from the recent review on this standard: [Add ERC: Chain-specific addresses using ENS by jrudolf · Pull Request #735 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/735#pullrequestreview-2769651845)

---

**0xtiti** (2025-04-30):

> If 7828 defines a text representation for cross chain names, where is a text representation for cross chain addresses defined?
> @nicksdjohnson

> in my mind addresses are identifiers meant for machines (including the evm) and names are representations of addresses meant for humans
> from there, 7930 is very strict about defining addresses, and provides a very loose definition of what the names for those should look like
> and 7828 is concerned with a more feature-complete way of naming addresses
> are our taxonomies too dissimilar @nicksdjohnson ? there might be something I’m not seeing
> @teddy_username

> No, but I don’t think you can realistically get away without a canonical text representation of addresses. Even in an ideal world where end users don’t have to deal with addresses, not every address will be named, and developers at least need a way to represent them.
> …in ENS? As I’ve raised before, there’s no way to create a unique and unambiguous mapping of TLDs to naming systems.
> @nicksdjohnson

---

**teddy** (2025-05-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xtiti/48/15124_2.png) 0xtiti:

> No, but I don’t think you can realistically get away without a canonical text representation of addresses

ERC-7930 defines that as an optional representation which looks like this: `0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045@eip155:1#4CA88C9C`

ERC-7828 also allows to refer to addresses without names on any registry, because ERC-7930’s human-readable representations are valid ERC-7828 names

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xtiti/48/15124_2.png) 0xtiti:

> represent them.
> …in ENS? As I’ve raised before, there’s no way to create a unique and unambiguous mapping of TLDs to naming systems.

For context, that was referring to where to store the mapping of TLD → name resolving method. I would 100% agree on storing said info on ENS if there already was both a precedent and tooling for the EF (or similarly neutral body) maintaining & updating something as critical on ENS, but since there isn’t, and we are trying to move the interop roadmap on a timeline not long enough to coordinate it’s development, I opted instead for a list similar to [GitHub - ethereum-lists/chains: provides metadata for chains](https://github.com/ethereum-lists/chains) , since:

- it’s something the community is already familiar with
- it’s an improvement since it’s one indirection level up and will require a way smaller number of entries

Eventually I’d like to deprecate this centralized TLD->name resolver list for a decentralized solution as well, but I believe we are still a few steps away from that, with stuff like e.g. a good execution of ERC-7785 being a pre-requisite.

Again, I don’t have the bandwidth to champion ERC-7785 as well, and would love for somebody else to get involved and push it forward. IIRC [@jaack](/u/jaack) showed some interest? Could alternatively the ENS team take care of it?

---

**nategraf** (2025-05-02):

I like this standard quite a bit. I had a comment about the potential collision with the email namespace. There are two parts to my thoughts here.

### Conflict with TLDs defined by IANA / ICANN

Using the domain name syntax (e.g. `eth.short` or `solana.short`) is very nice, and leans upon existing familiarity and understanding of domains and subdomains. The risks I would like to raise is when this familiarity actually leads to the wrong assumptions.

`.short`, for instance, not a TLD defined by ICANN today [1]. Good chance it will not be one defined by ICANN in the future either, but this represents a risk. If it does become a TLD defined by ICANN in the future, this could be an issue both in that `eth.short` could become owned in the DNS namespace by someone who wants to abuse this. If additional registries are defined, and each assigned a L0-TLD this increases the risk of such a collision occurring.

At this point `.eth` would be unlikely to be allocated by ICANN to be owned by a corporation, since it is big and well-known enough. But ICANN likely is not going to always avoid colliding with less well-established TLDs.

One way to handle this might actually be to lean further in, and use something like `casa.org`, `casa.eth` (or a domain *actually* owned by CASA under DNS or ENS) as your domain, and subdomain as `eth.casa.org`. In this case, you know that a particular organization owns the name number DNS or ENS respectively and can control how resolution is handled in those systems. In these cases, reasoning about ownership of subdomains also follows the intuition established by those systems (`*.casa.org` is a subdomain allocated by `casa.org`).

Individual chains may also find this desirable. For example, Arbitrum could use `arbitrum.io` or another domain it owns as the full chain name. In this case, having it match a DNS name they own and manage integrates with security practices already followed and helps maintain one identity across Web2 and Web3.

There is the question of course about how much of this needs to be specified in the standard. I’m not sure about that. I do think that wherever the ERC-7828 TLDs are defined should take this into consideration.

I also think it would be beneficial to that that when an ERC-7828 TLD does match a TLD defined by ICANN, that the resolution mechanism should not explicitly conflict with the ownership semantics of DNS. One mechanism for this would be to define a DNS-based resolution strategy, likely in a different standard, although I recognize the pitfalls of this in that domain ownership is managed by centralized entities and can be sold and so am not whole-heatedly endorsing this.

### Ambiguity with Email

Some wallets can applications allow you to “send crypto an email”. When this is the case, there could be situations where entering an identifier on the “to” line will be ambiguous as to whether its an email or a ERC-7828 address.

If ICANN TLDs are not valid ERC-7828 TLDs, then there is a deterministic procedure to disambiguating this.

If the TLD is an ICANN TLD, DNS resolution could be used here. E.g. using the rules that if there is not an MX record, then it is not an email address. This means that as long as the owner of the domain associated with a chain *does not* set up MX records on the same domain as they are using for ERC 7828, then there is also a clear procedure to determine the difference. There is also the approach of defining a DNS record to use to indicate affirmatively that a given domain is a chain identifier, although this requires defining that DNS record.

[1] data. iana. org/TLD/tlds-alpha-by-domain.txt

---

One more minor comment. What is the origin of `.short`? Is that official part of the standard. Its quite non-obvious that this is the TLD for defining chain names (versus something like `.chain` or another that would be suitable, and possibly linked to CASA more directly)

---

(note: this is a repost of an earlier comment I made on the wrong thread)

---

**teddy** (2025-05-02):

> What is the origin of .short?

The inspiration for it was [ERC-3770](https://eips.ethereum.org/EIPS/eip-3770), which used the `shortname` field of entries in the [centrlalized chain list](https://github.com/ethereum-lists/chains). But `.shortname` didn’t feel very *short*, so I opted for `.short` instead ![:grin:](https://ethereum-magicians.org/images/emoji/twitter/grin.png?v=12)

> Is that official part of the standard[?]

It’s not part of the ERC-7828 standard itself, but should be one of the entries in the Name Resolver Registry, describing how to use the centralizaed chain list described above.

> Its quite non-obvious that this is the TLD for defining chain names (versus something like .chain or another that would be suitable, and possibly linked to CASA more directly

That is not *the* TLD for defining chain names, it’s one of many possible TLDs, which in the Name Resolver Registry is defined as:

- invalid for addresses (because it’s not explicitly defined)
- referring to the ethereum-lists/chains shortlist when used in chains.

To exemplify the possibility of other TLDs also defining chain names:

One of the goals of this standard is to be a building block on top of which [ERC-7785](https://eips.ethereum.org/EIPS/eip-7785) can be used, and since the former plans to be tightly coupled to ENS, it would be fair for it to be assigned the `.eth` TLD.

Using `.chain` instead of `.short` would make this even less aparent.

I’d like to know if there’s any wording/structure of the document that in your opinion could be changed to make this more evident.

---

**teddy** (2025-05-05):

> (note: this is a repost of an earlier comment I made on the wrong thread)

Thanks for moving this here ![:sparkles:](https://ethereum-magicians.org/images/emoji/twitter/sparkles.png?v=15)

## On the collisions with ICANN/IANA TLDs

I’m apprehensive of leaning *into* DNS and ICANN/IANA TLDs because that’d hugely increase the scope for the proposal [[1]](#footnote-58609-1) and would involve adding multiple off-chain sources of trust, which while making the standard more decentralized in the short term, could paradoxically hinder the ability of moving to a better long-term solution decentralization-wise by e.g. not being able to nuke the on-chain list in favor of a 7785-style registry, needing coordination with multiple parties instead.

Furthermore, integrating with ICANN/IANA would also mean defining what to do when a name’s ownership expires or is otherwise revoked (as happened with `eth.link`), also greatly expanding the probability of that happening.

I propose we instead lean *away* from ICANN/IANA, keeping names hierarchical but being able to easily tell them apart by using a different separator.

## On the collisions with e-mail addresses

Thanks for bringing this up, I saw the initial discussions on the topic and sort of dismissed/forgot about it. I now see there is a significant amount of people concerned with being able to send crypto to e-mail addresses (or at least not being able to do so if that’d mean sending funds to the wrong place). Since that is probably going to stay up for implementation of individual wallets (which would mantain the e-mail address → blockchain account mapping on an ad-hoc basis), as there’s currently no standard defining a more interoperable alternative, I propose we instead use a different separator than email addresses.

## Possible address/chain separators

- : would be somewhat ambiguous when it is also used inside the chain specification, such as eip155:1.short. Not really ambiguous, we can take care of defining the grammar in a way that’s correctly parseable, but something obvious would serve human users better.
- :: better than the above, and is associated to namespacing semantics in other places of cyberspace. But in all honesty that is probably only true for developers, and even in those cases I’m not sure I want to be responsible for causing fellow devs C++ PTSD.
- @: causes the aforementioned collisions with email addresses
- <>: next option that came to mind. The biggest issue I can see with it is that it’s commonly used for symmetrical relationships. E.g. IIRC when Alice creates a google meet with Bob, it will automatically be assigned the name Alice <> Bob.

I’m going to optimistically go for the latter option, since it’s not that hard to change regardless.

1. …and also I’m honestly not qualified to define such a thing, since I’ve only ever made very casual use of DNS at a technical level ↩︎

---

**nategraf** (2025-05-05):

Ah, thank your for linking to the `ethereum-lists/chains` GitHub repo. I was under the impression that `.short` was going to be resolved from a list maintained by CASA, which explains my confusion in not finding it. It is clear enough that each L0-TLD has an associated resolution strategy, and that `.short` is one of many ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12).

Whether or not it is intended to be normative, it does seem likely people will use the name given in ERC-7828 when they want to use this resolution strategy (i.e. pulling from the list), so `.short` will be in use. If feels like one of those things that going to hard to explain in a couple of years, why `.short` is the name for this registry. Maybe `ethlist`, or `.erc7828` if the intention will be to inline the list into this ERC as the `TODO` in the current PR implies (commit 98ecaddea, line 164).

Anyway, this is total bike-shedding territory! Anything works.

> I’m apprehensive of leaning into DNS and ICANN/IANA TLDs because that’d hugely increase the scope for the proposal […] I propose we instead lean away from ICANN/IANA, keeping names hierarchical but being able to easily tell them apart by using a different separator.

I’m actually aligned here. I did sketch out a way to potentially use DNS productively, but probably distracted from my main point. My main point is that there is danger if this system accidentally *conflicts* with ICANN / DNS on the meaning of a given domain, and each system leads to different conclusions.

Using a different separator would cleanly solve this problem.

If the domain structure an `.` separator are kept (e.g. eth.short), my two concrete proposals on this are:

- that it be made explicit that each new L0-TLDs must not be equal to an ICANN TLD.
- that caution is taken towards the risk of an L0-TLD being defined as a ICANN TLD in the future. E.g. .sol is not an ICANN TLD today, but feels more likely to be a TLD in the future than say .erc7828 (its too specific) or .eth (its in wide use by ENS).

> Possible address/chain separators

I will say `<>` is somewhat difficult to type on a phone touchscreen keyboard.

Using `:` or `::` seems somewhat nice to me. Curious what others think.

---

**clowes.eth** (2025-05-07):

> Note: I wrote this at the end of March but was unable to post it due to permissions. Retrying, having caught up.

Some commentary.

My context/background: domain names and [ENS](https://discuss.ens.domains/u/clowes.eth/summary).

# ERC 7785

The current spec as-is seems to lack in clarity what ENS resolution specification this ERC seeks to take advantage of.

ENS have a number of ENSIPs pertaining to address resolution ([ENSIP-1](https://docs.ens.domains/ensip/1), [ENSIP-9](https://docs.ens.domains/ensip/9), and [ENSIP-10](https://docs.ens.domains/ensip/10) for example) as well as the resolution of arbitrary and/or standardised text records (see [ENSIP-5](https://docs.ens.domains/ensip/5)).

Regardless of where it appears, when we see `arbitrum.eth` what exactly are we resolving? Are we resolving an address? I don’t think so - that makes little sense.

[ERC 7885](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-7785.md) states that “*The name should resolve to a record containing not only the chain identifier, but also all the optional information necessary to verify the identifier.*”. The implication here is that we are resolving arbitrary data (in a specific defined format) subject to ENSIP-5. If so, what key are we defining (and standardising) to hold this data?

### Second Level ENS names

A number of people have mentioned that chain operators do not necessarily own their ‘logical’ corresponding second level .eth ENS name.

I **do not** think a specification should define expectations that this is the case - this is an implementation detail. Arbitrum (for example) should be able to choose if they want to use arb.eth, arbitrum.eth, or nitro123.eth.

### 2 Character ENS Names

“*EF populates two subdomains `l2.eth` and `chainid.reverse` using Ethereum lists.*”

The only entity that has the power to assign ownership of the `l2.eth` ENS name is the ENS DAO noting that the minimum length of an ENS name given current rules is 3 characters. This would need careful consideration given the precendent allocating the name would set.

### Subdomains?

I think this using subdomains might be a better approach. An arbitrary ENS name is registered e.g `chaindata.eth` and a custom resolver deployed with revokable admin controls. Subdomains could then be allocated and custom text records set subject to the aforementioned pre-defined key (e.g `chainData`).

The approach can be taken further with versioning within the subname scheme - `v1.arbitrum.chaindata.eth` or `latest.arbitrum.chaindata.eth` (with the canonical latest data resolved from `arbitrum.chaindata.eth`).

My understanding is that chain data is unique and immutable subject to specific rollup configuration - once deployed we can hand off control over subname allocation to the multisigs controlled by the rollup creators.

**For bonus points**: Lobby the ENS DAO for .chain and you unlock the possibility of `v1.optimism.chain`. Note: this will be a big ask giving consideration to the [ENS Constitution](https://docs.ens.domains/dao/constitution) and ICANN’s [new gTLD program](https://newgtldprogram.icann.org/en).

# ERC 7828

In the context of 7828 there is debate about the appropriateness of using `@` and the potential for confusion with email.

Why can we not simply use `user.v1.arbitrum.chaindata.eth`?

- 0x123.v1.arbitrum.chaindata.eth => 0x123 on the chain identified in the chainData text record for  v1.arbitrum.chaindata.eth
- clowes.optimism.chaindata.eth => Resolve the chainData text record on optimism.chaindata.eth and then resolve clowes.eth using ENSIP-9 with the coinType specified in the resolved chainData.

In the latter case we could grandfather in the `coinType` set derived for the current versions of rollups subject to [ENSIP-11](https://docs.ens.domains/ensip/11). `coinType` derivation moving forward could be adapted to consider a version number or they could simply be arbitrarily set with uniqueness checks within the resolver implementation.

## TL;DR

Can this all just be an ENS Resolver contract, an ENSIP-5 text record identifier, and a format for its value?

# More Thoughts (7th May)

## DNS

DNS collision is a non-issue with ENS as .eth is the only **chain only** TLD offered.

.eth is the three letter country code representation of Ethiopia and it [is reserved](https://itp.cdn.icann.org/en/files/generic-names-supporting-organization-council-gnso-council/reserved-blocked-names-topic-21-01-02-2024-en.pdf) but not assigned by ICANN. I believe there have been conversations about the path to potentially getting control of .eth in the zone and utilising it, but don’t quote me on that.

ENS have a [DNS integration](https://docs.ens.domains/learn/dns/). Also see [ENSIP-17](https://docs.ens.domains/ensip/17). The owner of a DNS name can *import* that name and utilise it within the ENS system.

Alternate naming services could cause extension collisions as has been seen historically e.g. [.coin](https://domainnamewire.com/2022/10/18/unstoppable-domains-kills-coin-in-the-name-of-wallet/)

My perception is that the general positioning of ENS DAO participants is one of working collaboratively with ICANN. See for example:



      [x.com](https://x.com/GUA/status/1917988549103882241)





####

[@](https://x.com/GUA/status/1917988549103882241)



  https://x.com/GUA/status/1917988549103882241










![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/teddy/48/14524_2.png) teddy:

> I propose we instead lean away from ICANN/IANA, keeping names hierarchical but being able to easily tell them apart by using a different separator.

If we use ENS this is abstracted away in many respects. This discussion surrounds an **Ethereum** Request for Comment, and I think its a valid call to focus it around ENS - an Ethereum identity primitive.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nategraf/48/15128_2.png) nategraf:

> If the domain structure an . separator are kept (e.g. eth.short), my two concrete proposals on this are:
>
>
> that it be made explicit that each new L0-TLDs must not be equal to an ICANN TLD.
> that caution is taken towards the risk of an L0-TLD being defined as a ICANN TLD in the future. E.g. .sol is not an ICANN TLD today, but feels more likely to be a TLD in the future than say .erc7828 (its too specific) or .eth (its in wide use by ENS).

In my view, any real competitor to ENS would have to have given consideration to ICANN and user experience. Namespace collisions help no-one and as such I think these are fair statements. If someone wanted to create a new naming service using .sol as the extension for example, it would be pragmatic for them to apply for .sol in the root zone as part of the upcoming gTLD process.

Noting this, dot separated subname based chain specific addresses, *I think*, solve this problem in a flexible and extensible manner..

---

**jaack** (2025-05-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/teddy/48/14524_2.png) teddy:

> Again, I don’t have the bandwidth to champion ERC-7785 as well, and would love for somebody else to get involved and push it forward. IIRC @jaack showed some interest? Could alternatively the ENS team take care of it?

I’d love to champion ERC-7785, I’ll brainstorming with some of our engineers at routescan next week to update the draft with some practical instructions.

If this is done with ENS, I suppose they should be involved in some way? Otherwise an agnostic standard needs to be designed.

---

**teddy** (2025-05-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/clowes.eth/48/14634_2.png) clowes.eth:

> ERC 7785

While I appreciate the feedback (and the context on the ways it affects 7828) I’m trying to decouple 7785 from 7828 since the former tries to solve much harder problems (both at the technical and social-consensus layers) and I’m trying to get the latter finalized on a tighter timeline.

I’d like to focus this thread on 7828 (although including the ways in which it can pave the way for a 7785 future is very much in scope) and have any further discussion happen in [its own magicians thread](https://ethereum-magicians.org/t/on-chain-registration-of-chain-identifiers/21299)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/clowes.eth/48/14634_2.png) clowes.eth:

> Why can we not simply use user.v1.arbitrum.chaindata.eth?

Unfortunately there are a few reasons for that:

- It sets a hard blocking between this standard and 7785, meaning 7828 will not be define-able util we have an agreed upon normative spec for 7785, and 7828 Interoperable Names will not be possible to use until 7785 is productive. The currently proposed spec allows to use human-readable names using the best currently available technology, and also upgrade to use 7785 when it’s ready.
- It does not define a way to refer to an address on a chain that is not supported by 7785, meaning users would be exposed to at least two addressing standards. It’s worth noting that given there’s no normative spec of 7785, we can’t really discuss what it’s limitations will be, and therefore it’s an open question which chains would be excluded by this restriction. Some possible options:

 Some kinds of L2s, due to technical limitations on proving stuff on L1 with L2 data.
- Any alt-L1
- In the case where there’s not a permissionless way to register a chain on L2, any chain that has not been given the explicit blessing of whoever owns chaindata.eth.
 While it’s true that an Ethereum standard doesn’t have an obligation to serve the needs of chains outside the ethereum ecosystem (however you define its boundaries), it does have to serve its users by providing a uniform interface for addressing (chain, address) pairs they might encounter in the context of using Ethereum applications, and having a format that’s very different for a chain that works with 7785 than one that doesn’t would be a negative for users.

(potentially solvable) In the case of an L3 chain, e.g. a chain that’s a rollup of a rollup, how would you differentiate between a name for a chain and a name for an address within that chain?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nategraf/48/15128_2.png) nategraf:

> If the domain structure an . separator are kept (e.g. eth.short), my two concrete proposals on this are:

These strike as reasonable demands as well.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/clowes.eth/48/14634_2.png) clowes.eth:

> If we use ENS this is abstracted away in many respects. This discussion surrounds an Ethereum Request for Comment, and I think its a valid call to focus it around ENS - an Ethereum identity primitive.

If we were to do away with the *name resolver registry*, and instead focus on ENS alone, would you stand behind something like the following?

- human-readable names of addresses are entirely delegated to ENS, allowing for use of DNS-in-ENS and doing away with the ICANN collision issue (still would have to dive deep into ENSIP-6)
- chain part is like above, essentially reserved until ERC-7785 ships, but has an exception on the .short TLD to signify usage of the ethereum-lists/chains list of shortnames, so we can have good-enough human-readable chain names in the meantime
- 1-2 ENSIPs are pushed so chainid/cointype used within ENS are both ERC-7785-proofed and consistent with the definitions of ERC-7930, making implementations easier by minimizing the amounts of translations

---

**ndeto** (2025-07-17):

We’ve created a resolver that demos this spec.  It currently uses Chainlist sources to resolve EIP‑7828 names.

The package is here: [ens-7828-resolver](https://github.com/unruggable-labs/ens-7828-resolver)

It focuses on the human‑readable aspects of the spec, prioritizing resolution from ENS names to addresses or CAIP‑2 formats.

We will upgrade it to support ERC‑7785 sources once the ENS registries are deployed.

Feedback is highly appreciated.

---

**0xMonoAx** (2026-02-05):

Hi everyone!

We wanted to share an update on **ERC-7828: Interoperable Names**. After several discussions with Unruggable and other community members, we made some important changes that we believe improve the standard.

### What changed?

#### Restructuring: Interoperable Names now lives in ERC-7828

An important change worth clarifying: [the Interoperable Names definition now lives entirely in ERC-7828](https://ethereum-magicians.org/t/erc-7930-interoperable-addresses/23365/22), rather than inheriting from ERC-7930.

The separation is now:

- ERC-7930: Defines the binary format to reference an address on a specific chain (machine-oriented)
- ERC-7828: Defines human-friendly name resolution to Interoperable Addresses, using ENS

This makes each standard more specific and easier to implement.

#### Optional checksums

One of the longest debates was whether the checksum should be mandatory or not. In the end, we decided to make it optional but recommended for raw addresses, and not necessary for ENS names.

The reason is simple: if you’re using ENS, you’re already trusting its validation mechanisms. Also, ENS names can resolve to different addresses over time (for example, if the owner updates the resolver), which would make an old checksum stop working. Forcing checksums in these cases only adds friction without real benefit.

For raw addresses, the checksum remains useful to avoid typos and spoofing attacks. An important detail: the checksum is calculated on the resolved ERC-7930 address, not on the name or textual representation. This approach guarantees canonicity, but adds complexity for implementers. We’re open to feedback on this design decision.

#### Versioning

We added a versioning section so that Interoperable Names keep working even if ERC-7930 gets updated in the future. The trick is to exclude the Version field from the checksum calculation.

#### Chain registry with on.eth

We updated the spec to align with the latest chain resolver implementation, which will be at `on.eth`. This resolver contract:

- Maps human labels (like optimism) to their canonical ERC-7930 identifiers
- Exposes additional metadata for each chain
- Supports aliases (for example, op.on.eth and optimism.on.eth resolving to the same data)

This way, `optimism.on.eth` would resolve to Optimism’s Interoperable Address.

This proposal is currently [under discussion at ENS DAO](https://discuss.ens.domains/t/ens-dao-newsletter-101-12-2-2025/21685#p-59782-creation-of-oneth-for-cross-chain-registry-13), so it’s not finalized yet.

##### Clearer specification

We restructured the ERC to make it easier to implement. It now has dedicated sections on how to resolve the `<chain>` component and how to resolve the `<address>` component, instead of mixing everything together.

### Why does this matter?

The problem ERC-7828 solves is simple: with hundreds of L2s using the same address format as Ethereum mainnet, an address alone no longer tells you which chain it belongs to. This can result in funds being sent to unreachable addresses on the wrong chain.

With Interoperable Names like `alice.eth@optimism` or `0x123...@base`, both the address and the destination chain are clear.

### Next steps

The ERC is currently in Draft status. Our goal is to move it to Review and eventually to Final. For that, we need community feedback.

We’d love to hear your thoughts on:

- The optional checksum approach, does it balance flexibility and security appropriately?
- Any edge cases or implementation challenges you foresee?

Looking forward to your feedback!

