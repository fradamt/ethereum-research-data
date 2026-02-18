---
source: magicians
topic_id: 23365
title: "ERC-7930: Interoperable Addresses"
author: teddy
date: "2025-04-03"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7930-interoperable-addresses/23365
views: 1316
likes: 24
posts_count: 19
---

# ERC-7930: Interoperable Addresses

## Abstract

Interoperable Addresses is a binary format to describe an address specific to one chain with an optional human-readable name representation.

It is designed in a manner that allows the community extend it to support naming schemes (or other not-yet-imagined features) in the future, as well as to support arbitrary-length addresses and chainids.

ERC pull request: https://github.com/ethereum/ERCs/pull/1002

## Context

After extensive discussions on the various interop groups and an attempt to push this as a rewrite of ERC-7828, we are pushing a binary-first Interoperable Addresses format, and would like your feedback on the subject.

While we’ve made an effort to list related cross-chain naming & addressing efforts in the ERC itself, I believe some extra content is warranted here:

Initially we tried to push for a single standard to both take care of cross-chain addressing and cross-chain naming, normatively defining both binary and human-readable (in string form) representations for addresses, with varying levels of resolution into more condensed names with the help of ENS and similar resolvers.

We then realized that kind of standard would have two disjoint sets of users:

- Wallet developers, which cared mostly about naming and only tangentially about canonicity or binary encoding.
- On-chain infrastructure (such as cross-chain messaging and liquidity bridging) developers, who have strict requirements on binary payload compactness and canonicity but do not care about naming registries or human-readable representations.

This is a standard aiming to meet the needs of the latter, while hopefully being a building block in achieving the former as well.

## Feedback wanted on:

- How should we coordinate with CASA for it to be the registry where future chain/address types are appended? Ideally I’d like to end up with something resembling BIP-0044/SLIP-0044, where this standard reaches finality with support for a small set of highly-desired chains, and specifications required to support other chains in the future is maintained down the line in the respective chain namespaces
- What should we do about the CAIP-2 limitation on the chain reference’s length? Frangio mentions this standard is actually something different from CAIP-2, as it would be quite hard to convert actual CAIP-2 identifiers to this format, since it’d require extra data not available in the name itself. Also, it would not be possible to define a clear truncation scheme, since CAIP-2 identifiers are text which will have different bounds on what can it store based on the encoding used (eg 16 bytes for base16, or a bit more for base58).
- Should we be more normative with the string representation? less? remove it altogether?

## Replies

**teddy** (2025-04-11):

teddy’s devlog:

- Changed how Solana chain reference serialization works so it’s more easily convertible to CAIP-2. Note that I’m not trying to push for standarization of Solana addresses for any other reason than to provide an example of how the standard is extensible to other domains.
- Defined the case where an address/chain field has a length of zero, which also allows interfaces to consistently use Interoperable Address types when they want to represent (a) a chain, (b) an address, where the chain information is not important or can be assumed, and (c) representing a target address as was the initial scope for the ERC. Had to move the chain reference information outside of the ‘chain’ field, in order for users to know how to interpret the address when the chain reference is not present.
- Will work on (yet another) revamp of 7828 which will leverage the definitions on this document to define better human-readable names by using registries
- I made references to a ‘relevant CASA profile’ which I haven’t defined yet, but I guess it’s not that crucial for the immediate future. Will tackle that next.

---

**undefined** (2025-04-14):

Question: Would this be compatible with UTXO-based chains like Bitcoin or does it assume an Ethereum-style account-based model? IMO an interoperability scheme like this should try to be open in terms of not being locked in to EVM semantics and at least describing how it would work with Bitcoin would be a good signal that this has been properly considered.

---

**teddy** (2025-04-14):

> Would this be compatible with UTXO-based chains like Bitcoin or does it assume an Ethereum-style account-based model?

Yes! It would be compatible with UTXO-based chains. The reason I didn’t include Bitcoin into the first draft is that it’s address serialization scheme is not as trivial as Solana’s (or most account-based chains tbh), and wanted to avoid specifying how to reliably serialize all the kinds of Bitcoin addresses and then realizing the community wanted something else entirely.

It’s worth noting that, since the serialization scheme is going to be defined as a CASA profile, it does not need to be hard-coded into this spec, and can be added after this ERC is finalized. It’s not very likely this will be tha case for Bitcoin, but is the expected path for other chains to be part of the standard.

---

**u59149403** (2025-04-29):

I posted my feedback here: [New CAIP profile: interoperable address binary specification by 0xteddybear · Pull Request #350 · ChainAgnostic/CAIPs · GitHub](https://github.com/ChainAgnostic/CAIPs/pull/350)

---

**teddy** (2025-05-01):

Pasting some discussions Lumi started on the PR, regarding checksums:

> could checksums fail or be improperly validated?

I refrained from writing UX guidelines in this document given that it’s mostly concerned with binary addresses, but imagine wallets not giving enough prominence to checksums so they are missed by users could be a possible failure mode.

I didn’t add them on ERC-7828 either, since:

- Wallet’s UX developers will probably be better at choosing how to display information than what I can come up with (@skeletor-spaceman came up with the example of using blockies instead of text checksums, for example)
- There’s not an adversarial relationship between a given wallet’s UX designer and anybody else which could be mitigated by a standard’s normative.

Collisions on 4-byte checksums are feasible to mine, but it’s unlikely the impersonator’s address (or in the case of ERC-7828, name) is also a lookalike of the intended recipient’s

…well, that hinges on the wallet displaying the name also having sane warnings around unicode glyph collisions, in the case if 7828. Will add it as a security consideration of that standard.

I also considered the possibility of hash collisions happening because of there not being a delimiter between address and chainid, but that seems harder to exploit than the fact that checksums are only 4`bytes long

> Could misinterpreted chain identifiers lead to funds loss?

Most definetely, but for non-malicious usecases (such as an attacker mining an address so that `(minedAddres, badChain)` has a 4-byte collision with `(whateverAddress, intendedChain)`) the checksum should be a good mitigation.

> Are there upgrade or compatibility risks introduced by the versioning scheme?

I tried to lay them out in the ‘Restrictions for all Interoperable Address versions’ section, basically we define version bit to mean the Interoperable Address is backwards-compatible with v1, and parseable with the same algorithm.

The main risk would be for a future Interoperable Address to define an associated Interoperable Name which can cause collisions with previous versions, e.g. having a v3 name be equivalent to a v2 name while representing a different (address, chain) pair.

In the past we explored including the address’ version in the Interoperable Name, but that felt like a lazy (albeit robust) solution, which unnecessarily leaked implementation details onto users. The way we actually intend to avoid such a scenario is:

- Review of other ERCs defining further Interoperable Address versions
- Implementing ERC-7828 in a flexible enough way (by coupling the resolution method to a TLD) that lowers the need to define new versions in the near future.

---

**oxlumi** (2025-05-02):

Great! I agree that ux guidance is out of the scope of the ERC itself. Still, it seems important that the security considerations section explicitly acknowledges the following points:

- The 4-byte checksum provides only probabilistic collision resistance and should not be treated as a strong authenticity guarantee.
- Collision risks are accepted within the intended (non-adversarial) use context but could become exploitable if implementers assume stronger guarantees.
- The burden of meaningfully presenting checksums (example: avoiding glyph or display-based confusion) shifts to wallet and dApp implementers.

On the versioning side, the design to keep interoperable names abstracted away from the version bit makes sense, but it would be worth clarifying that cross-version equivalence assumptions should only be made when formally defined. Implementers should not assume, for example, that a v3 name and a v2 name are interchangeable without explicit guarantees

---

**ernestognw** (2025-06-09):

Hi [@Amxx](/u/amxx),

I think there might be a misreading of the specification here. Looking at the current text more carefully:

> AddressLength: 1-byte integer encoding the length of Address in bytes. Note that it MAY be zero, in which the Interoperable Address will not include an address. It MUST NOT be zero if ChainReferenceLength is also zero.

This last sentence actually **does** explicitly forbid both `ChainReference` AND `Address` from being empty at the same time.

The constraint “It MUST NOT be zero if `ChainReferenceLength` is also zero” means:

- If ChainReferenceLength is 0, then AddressLength MUST NOT be 0
- This effectively requires that at least one of the two fields must be non-empty

So the specification already prevents the case you’re concerned about - having an interoperable address that refers only to a “ChainType” with no specific chain or address information.

The current wording already ensures that every valid interoperable address must contain either:

1. A specific chain (with or without an address), or
2. A specific address (with an implied/default chain context)

But never neither. Does this clarify the existing constraint, or am I missing something in your concern?

---

**Amxx** (2025-06-18):

FYI, I created an typescript/javascript library to manipulate (encode/decode) interoperable addresses



      [github.com](https://github.com/Amxx/interoperable-addresses/)




  ![image](https://opengraph.githubassets.com/a138e3981239ebe4c9552520ebfe5b32/Amxx/interoperable-addresses)



###



Contribute to Amxx/interoperable-addresses development by creating an account on GitHub.

---

**skeletor** (2025-10-10):

## Reference Implementation

- Interop-SDK by Wonderland: A TypeScript/JavaScript library for encoding, decoding, and manipulating Interoperable Addresses.
- OpenZeppelin draft implementation Solidity library contract for Interoperable Addresses.

---

**euler0x** (2025-10-14):

ERC-7930, Interoperable Addresses, has reached a stable draft stage, and we’re ready to move it to **Last Call** . This means we’re seeking final feedback and consensus before finalizing the standard.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1240)














####


      `master` ← `defi-wonderland:7930-lastcall`




          opened 06:30PM - 06 Oct 25 UTC



          [![](https://avatars.githubusercontent.com/u/208748321?v=4)
            euler0x](https://github.com/euler0x)



          [+14
            -6](https://github.com/ethereum/ERCs/pull/1240/files)







Move EIP-7930 to Last Call, with deadline 14 days from now: 2025-10-20.

---

**teddy** (2025-12-09):

gm folks, i’ve been affectionately (and informally) referring to this standard  as ‘addy’, and seeing as

- ‘interoperable name’ and ‘interoperable address’ are a bit of a mouthful, and
- nobody has yet claimed the ‘addy’ name in the ecosystem to mean something specific

I propose we make it an official part of the spec. The thing is, should ‘addy’ refer to:

- the interoperable name
- the interoperable address
- both, in contexts where it doesn’t make to tell them apart

0
voters

I personally prefer the latter, as in informal usage it won’t be of huge importance to be clear on to whether we’re talking of a binary or text representation (and might be beneficial to be ambiguous, as software will do the conversions automatically), but *will* be important to express:

- I’m talking about a thing that specifies both an address and chain
- …in ERC-7930’s format, specifically

---

**frangio** (2025-12-16):

I’ve seen “addy” used to refer to addresses in general, I’m not sure we can make it mean interoperable addresses specifically.

But I think “interop address/addy” and “interop name” would be good.

---

**0xrcinus** (2025-12-17):

As mentioned in today’s L2 Interop Working Group, this ERC has recently undergone significant revision for improved clarity, so encouraging folks to review recent changes:



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-7930.md)





####

  [master](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-7930.md)



```md
---
eip: 7930
title: Interoperable Addresses
description: An extensible binary format to refer to an address specific to one chain.
author: Teddy (@0xteddybear), Joxes (@0xJoxess), Nick Johnson (@Arachnid), Francisco Giordano (@frangio), Skeletor Spaceman (@skeletor-spaceman), Racu (@0xRacoon), TiTi (@0xtiti), Gori (@0xGorilla), Ardy (@0xArdy), Onizuka (@onizuka-wl), Sam Kaufman (@SampkaML), Marco Stronati (@paracetamolo), Yuliya Alexiev (@yuliyaalexiev), Jeff Lau (@jefflau), Sam Wilson (@samwilsn), Vitalik Buterin (@vbuterin), Thomas Clowes (@clowestab), Mono (@0xMonoAx)
discussions-to: https://ethereum-magicians.org/t/erc-7930-interoperable-addresses/23365
status: Draft
type: Standards Track
category: ERC
created: 2025-02-02
---

## Abstract
This proposal introduces a **binary format** to describe a chain specific address. Additionally, it defines a human-readable version of that identifier, which improves the user experience in user-facing interactions.

This is achieved through a versioned, length-prefixed binary envelope that supports arbitrary-length data. The interpretation and serialization rules for the data within this envelope are defined by companion standards ([CAIP-350]), which provide profiles for each chain type.

## Motivation
The address format utilized on Ethereum mainnet ([ERC-55]) is shared by a large number of other blockchains. The format does not include details of the chain on which an interaction should occur. This introduces risk if, for example, a transaction is mistakenly executed on a chain where the address is inaccesible. This risk is particularly pronounced for addresses that represent smart contracts or smart accounts.

```

  This file has been truncated. [show original](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-7930.md)










Many thanks to Teddy, [@clowes.eth](/u/clowes.eth) and [@0xMonoAx](/u/0xmonoax) who worked on these improvements

---

**teddy** (2025-12-18):

Regarding the poll above: A good point brought to my attention is that it does not make sense to formally specify how to informally refer to something. If we instead switch from ‘informal name’ to ‘name to use when we do not care if we are referring to the Interoperble Address or Interoperable Name’ does it make more sense then? I’m open to other suggestions for ways to refer to the standard that are easier to type/say, least we end up recurring to the evil acronyms IA /IN.

Another point of discussion, scattered across a few channels, is the subject of separating the Interoperable Names into their own ERC.

It’s important to remember that end users will rarely care about the specific representations, they’ll just want an easy way to refer to something that their wallet will accept as a transaction’s `to:`, and devs who care about the specifics can skip to the standard’s `Terminology` section

First of all, some context on why the 7930(Interoperble Address+Interoperable Name without ENS)/7828(Interoperable Name with ENS) split

Initially I drafted a single standard for both Interoperable Addresses, Interoperable Names, and Interoperable Names with ENS, meant to replace a pre-existing 7828 spec(which wasn’t really normative), but I ended up splitting them because

1. The ENS part (specially around chains) was not really defined and required extensive coordination to define (which is happening now, happily!) (also ERC-7785 was supposed to take care of defining human-readable names for chains)
2. The on-chain usages for this, however, (such as intent definition) could benefit from the binary standard immediately (and were about to use CAIP-10 strings inside smart contracts!)
3. It was good strategy to define the common elements that any human-readable representation of interoperable addresses should have, to achieve the following without without having users really notice a change in format, or being dangerously surprised in any way:
 3.1. Allow for competing or complementing ways to achieve human-readability (e.g. shoehorning openalias into the Interoperable Name format)
3.2. Allow for 7828 to fail and be replaced by another standard
4. 7828 will be a long spec. see how long the ‘reference implementation’ is in the current version, without being really normative or complete. Moving some of the load to 7930 to make 7828 easier to review seemed like a sane tradeoff.

## On The Subject Of Interoperable Names without ENS, And Why They Are Actually Very Important In My Opinion

First of all I’d like to tackle the confusion on there being two human-facing represenations for Interoperable Addresses: the standard does not state that the base16, base58 or other representations of the Interoperable Address should be used for anything. You’re free to represent them however you like in the privacy of your own terminal, but they’re not expected to be used as a mean of communicating Interoperable Addresses. If some part of the standard suggests that to be the case, we should edit it so it’s no longer the case.

### Why are interoperable names without ENS actually necessary?

Barring the obvious case of wanting to refer to something that does not have an ENS name registered to it, there are cases in which being able to display a human-readable string representing an Interoperable Addresses is important.

- MJKqp326RZCHnAAbew9MDdui3iCKWco7fsK9sVuZTX2@solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdpKuc147dw2N9d#88835C11 conveys more to the user than an opaque bytes payload. It shows that it’s a solana address, and the user can also figure out on their own if it matches another solana address, while the alternative is both opaque and unfamiliar. Additionally, end users are empowered to extract information from it (such as the address, or chain/chainid) without the aid of external tools and for example paste the address onto a block explorer that does not yet support ERC-7930.
- There are contexts on which even if an address has an ENS name registered to it, we will not be able to resolve it, the most important one being hardware wallets (I don’t want to be responsible over ‘blind signing’ not just calldata but also the recipient address)

### Why they should be part of 7930

Going over the arguments from the context above:

1. we could finalize 7930 (including names) pretty soon. While we are clos-er to a working chain name resolution for 7828, it still has a way to go.
2. is not relevant, as it’s enough with the interoperable addresses to be part of 7930 to achieve it.
3. is the most important one and still stands. Coupling the checksum definition for all future interoperable names is in particular a very important feature to ensure addresses can be compared, and is coupled to the binary representation.
4. still applies.

An argument for the Interoperable Names being part of 7930, and not their own new standard (let’s call it XYZ), is the following:

Having a spec that forks off 7930 but not XYZ would be more encouraged by that approach, and the loss of compatibility would be detrimental for user experience:

```auto
7930: Interoperable Addresses
    \- XYZ: Interoperable Names
    |   \- 7828: Interoperable Names With ENS
    |   \- shoehorn openalias into interoperable name format
    |   \- 7828 alternative using SNS
    \- (anything here does not guarantee Interoperable Name compatibility and will break stuff)
```

And in my experience having one more ERC will involve a bunch of overhead (get editor attention, an ERC number, etc) that will delay the timelines and mean us spending time dealing with that instead of building cool stuff.

The only argument I can think of *in favor* of separating 7930 and XYZ is for each one to only define *one* concept and have less ambiguity as to whether we’re referring to an Interoperable Name or an Interoperable Address. My take on that is that users will not care about Interoperable Addresses, and ‘7930 thingy’ will mean the `address@chain#checksum` format, and technical users can skim the ERC and get acquainted with both concepts. That (and having a name that’s less of a mouthful) is the point with my poll across.

## Clarifications that we might have to add to the standard

- Human-readable representations of Interoperable Addresses that comply with the versioning requirements outlined by ERC-7930 should also be called Interoperable Names, see my usage of ‘Interoperable Names without ENS’ and ‘Interoperble Names with ENS’ above
- Interoperable Addresses should not be displayed directly to users by converting them to text via base16, base58, etc

---

**katzman** (2025-12-18):

Having integrated ERC-7930 into [ERC-8092](https://ethereum-magicians.org/t/erc-8092-associated-accounts/26858), I’m confused about the motivation for interoperable names.

IMO, the value of ERC-7930 is the binary representation of addresses. Cross-chain/architecture specifications need a standard for encoding these addresses and this specification solves this problem.

In the future I am excited about, humans don’t read addresses. Everything is named/aliased such that addresses are “invisible” substrate like IP addresses are in the modern web. As such, I find it confusing that this specification also specifies a naming standard.

---

**clowes.eth** (2025-12-19):

**TL;DR**

- I am in favour of separation:
– ERC-7930: Interoperable Addresses
– ERC-7828: Interoperable Names using ENS

**More verbose**

ERC-7828 (in its current form) adds two core things:

- An allowance to use an ENS name in the  component
- An allowance to use a chain label in the  component from which chain metadata can be resolved (using ENS and an on-chain registry).

It is imperative that we don’t leave these specs open-ended and confusing. I think they need to be concise, well defined, with a clear separation of concerns.

---

I do not agree that removing the *Interoperable Name* definition from ERC-7930 is complex or will introduce a delay. The change is here: [docs: remove Interoperable Name definition · ethereum/ERCs@5222051 · GitHub](https://github.com/ethereum/ERCs/commit/5222051a380ec78056e29a13438a618f27978a83)

Having spent the past few days working and reflecting on 7828 I think it should be separated and further constrained. I think the `<chain>` component should **only** be allowed to be a chain label - we should go all-in on the on-chain registry.

**Why?** At the moment we are being opinionated on what values from other specifications (CAIP-2, CAIP-350) etc are allowable. We *could* allow a nested *Interoperable Address* in the chain component for example, but thus far have chosen not to.

Additionally the flexibility necessitates additional conditions that have the be defined and explained - they make the spec less accessible. For example, when using an ENS name as the `<address>`  you can no longer use a CASA namespace alone within the `<chain>` component (because ENS names are dynamically resolved for a specific chain).

Only allowing a chain label is clean, consistent, and **all additional chain metadata can be resolved through the on-chain registry**.

Ultimately a spec will get used if it is simple, and adds value. [@katzman](/u/katzman) comment outlines that he wants to use a binary address representation for his use case. Great - ERC-7930, off you go. He can reference it easily as a ‘7930 address’, an ‘Interoperable Address’, an ‘addy’, or something else as he sees fit. He does not care about the human readable representation for his specific use case.

Users (IMO) will be more interested in ERC-7828. `0x123@optimism` or `clowes.eth@arbitrum` make immediate sense to me. When I am on a blockchain explorer e.g. for Optimism, when I click ‘Share’ thats what I want to be copied to my clipboard. Looping back, if we also allow `0x123@eip155:10` **we achieve nothing** but user confusion. dApps whose infra utilizes previous addressing standards can pull that format from the on-chain registry.

**Specific Comments**

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/teddy/48/14524_2.png) teddy:

> If we instead switch from ‘informal name’ to ‘name to use when we do not care if we are referring to the Interoperble Address or Interoperable Name’ does it make more sense then? I’m open to other suggestions for ways to refer to the standard that are easier to type/say, least we end up recurring to the evil acronyms IA /IN.

Is this intention to put this in the spec? My thought is that an informal name is exactly that - one that people choose to use casually. I don’t think we should dictate how people refer to things, but we can certainly choose terms to use ourselves and hope they catch on…

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/teddy/48/14524_2.png) teddy:

> It’s important to remember that end users will rarely care about the specific representations

My understanding was/is that what I defined as an *Interoperable Address* is used in smart contracts, and what I defined as an *Interoperable Name* is used by end users. If I enter an 0x adress into my wallet, select Arbitrum, and then click ‘Copy to Clipboard’ it would give me `0x123@arbitrum#123`. That is immediately clear to me, I’d be comfortable sharing it, and the presence of a checksum provides protections to me.

---

Regarding separation. Initially I was in favour of keeping 7930 as is with a base definition of the *Interoperable Name* which can then be built upon by other specs.  As I’ve begun working on 7828 I find myself regularly referring back to 7930, and having to describe new constraints e.g. When using an ENS name as the `<address>`  you can no longer use a CASA namespace alone within the `<chain>` component. All of a sudden the spec gets overwhelmed with conditions, and becomes less accessible. I think how we separate things is ultimately going to have a huge influence on if these specs succeed or fail.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/teddy/48/14524_2.png) teddy:

> You’re free to represent them however you like in the privacy of your own terminal, but they’re not expected to be used as a mean of communicating Interoperable Addresses.

Agree

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/teddy/48/14524_2.png) teddy:

> MJKqp326RZCHnAAbew9MDdui3iCKWco7fsK9sVuZTX2@solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdpKuc147dw2N9d#88835C11 conveys more to the user than an opaque bytes payload. It shows that it’s a solana address, and the user can also figure out on their own if it matches another solana address, while the alternative is both opaque and unfamiliar.

Yes. Ultimately an ENS name is dynamically resolved. There is certainly value in the an *Interoperable Name* that doesn’t have an ENS name in the `<address>` component.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/teddy/48/14524_2.png) teddy:

> There are contexts on which even if an address has an ENS name registered to it, we will not be able to resolve it, the most important one being hardware wallets (I don’t want to be responsible over ‘blind signing’ not just calldata but also the recipient address)

I would argue the correct UX flow is that if an *Interoperable Name* with an ENS name in it is pasted into an input field, the client should resolve the components and display them to the user before requesting the signature. The hardware wallet would should the resolved inputs.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/teddy/48/14524_2.png) teddy:

> The only argument I can think of in favor of separating 7930 and XYZ is for each one to only define one concept and have less ambiguity as to whether we’re referring to an Interoperable Name or an Interoperable Address.

This is a very compelling argument IMO.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/katzman/48/15394_2.png) katzman:

> IMO, the value of ERC-7930 is the binary representation of addresses.

Whilst a singular data point, Steve’s position demonstrates the value of this defined separation of concerns - he wants a binary representation of addresses for his use case, whereas for my use case I wan’t a easily shareable human-readable representation of an address on a specific chain. No-one is right or wrong, we just have different use cases.

---

**ndeto** (2025-12-19):

I generally agree with the idea to split IA and IN. Keep 7930 as the canonical IA representation for machines, and constrain 7828 to ENS-based chain registry labels.

This is a much simpler mental model with a precise separation of concepts: a single canonical representation for machines and an ENS-backed human-readable representation for users.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/clowes.eth/48/14634_2.png) clowes.eth:

> Why? At the moment we are being opinionated on what values from other specifications (CAIP-2, CAIP-350) etc are allowable. We could allow a nested Interoperable Address in the chain component for example, but thus far have chosen not to.
>
>
> Additionally the flexibility necessitates additional conditions that have the be defined and explained - they make the spec less accessible. For example, when using an ENS name as the  you can no longer use a CASA namespace alone within the  component (because ENS names are dynamically resolved for a specific chain).

Agreed. A related concern is that accommodating potentially ambiguous meanings in the specification introduces additional downstream complexity in human-readable formats.

This approach instead provides a clear binary format and a specification that becomes more concise by relying on ENS to make both addresses and chain registry information fully human-readable.

---

**0xMonoAx** (2026-01-20):

## Update ERC-7930 and ERC-7828: Restructuring and Separation of Concerns

Hey everyone, we want to share an important update on the restructuring of these standards. We’re updating the forum discussions for both ERC-7930 and ERC-7828 to keep the community informed on our progress.

### New Structure

We reorganized the responsibilities between the two ERCs:

| Standard | Purpose |
| --- | --- |
| ERC-7930 | Binary machine-friendly format to reference an address on a specific chain |
| ERC-7828 | Human-friendly name resolution to Interoperable Addresses, using ENS |

### Summary of Changes

**ERC-7930:**

- Removed the Interoperable Name definition (now lives in ERC-7828)
- Added a section on text representation in user-facing contexts
- Simplified the ERC making it more specific and straightforward for developers

**ERC-7828:**

- Incorporated the Interoperable Name definition
- Discussing specifications to achieve a coherent ERC

**CAIP-350** (awaiting CASA review):

- Removed “Interoperable Name” references, replaced with “text representation”
- Added a “Chain Identifier Text Representation” section with the standard format : and update templeta and profiles

### Current Status

- ERC-7930 is in draft and will soon move to review
- ERC-7828 is entering a new phase of discussion and iteration. We’re working to make the ERC complete, coherent, and easy to understand

### Topics Under Discussion

- Checksums: Whether they should be part of the ERC, how to compute them, and when to display them to users
- Versioning: Defining compatibility constraints between ERC-7828 and ERC-7930
- General specifications: Reviewing clarity and consistency across different sections

We’d love to hear more perspectives from the community!

### Next Steps

- Move forward quickly with ERC-7828 while ERC-7930 heads to review
- Continue iterating with community feedback

