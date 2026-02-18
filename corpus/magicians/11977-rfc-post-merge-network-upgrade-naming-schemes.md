---
source: magicians
topic_id: 11977
title: "RFC: Post-Merge Network Upgrade Naming Schemes"
author: timbeiko
date: "2022-12-01"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/rfc-post-merge-network-upgrade-naming-schemes/11977
views: 5659
likes: 50
posts_count: 33
---

# RFC: Post-Merge Network Upgrade Naming Schemes

Happy birthday, beacon chain ![:birthday:](https://ethereum-magicians.org/images/emoji/twitter/birthday.png?v=12) : ! Two years after your launch, you’re now successfully serving as the consensus layer for the entire Ethereum network ![:tada:](https://ethereum-magicians.org/images/emoji/twitter/tada.png?v=12) !

---

The Merge moved us from “eth1” & “eth2” to a single, unified Ethereum network, but there are still process bits outside the network that need to be harmonized. One of these is naming!

On the execution layer, we’ve been using [devcon cities](https://ethereum-magicians.org/t/more-frequent-smaller-hardforks-vs-less-frequent-larger-ones/2929/33) to name upgrades (with a shoutout to EthCC for [paris](https://github.com/ethereum/execution-specs/blob/master/network-upgrades/mainnet-upgrades/paris.md)). On the consensus layer, [star names are used](https://github.com/ethereum/eth2.0-pm/issues/215).

There is value in keeping separate names to identify the specific EL & CL specs corresponding to a specific upgrade, but for end users having a single upgrade with two names is confusing. Luckily, the first time this happened we had “The Merge” we could use in announcements rather than “The Paris/Bellatrix Fork”. But now, we’re looking at “Shanghai/Capella” and “Cancun/???” coming, which are both terrible monikers for upgrades.

**I would therefore like to propose moving to a new naming scheme which uses a single term to describe the high-level upgrade (like “The Merge” did) and has related terms to describe the individual EL & CL specs (like Shanghai/Capella). I think a good theme for this is “structures with sub-components”**.

For example, you can imagine a naming scheme being “Planets and their stars”, where the planets refer to the high level upgrade (like “The Merge”) and EL and CL releases are each identified with a star name corresponding to this planet. Another theme could be “genus & species” (e.g. the [Cavia](https://dept.dokkyomed.ac.jp/dep-m/macro/mammal/en/genus/cavia.html) upgrade with the [Aperea](https://dept.dokkyomed.ac.jp/dep-m/macro/mammal/en/species/cavia_aperea.html) EL & [Porcellus](https://dept.dokkyomed.ac.jp/dep-m/macro/mammal/en/species/cavia_porcellus.html) CL releases)… there are many possibilities here!

Feedback welcome on both the high-level idea and specific suggestions of themes ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

## Replies

**ajsutton** (2022-12-01):

Adding another layer of name seems like it will just add confusion. I’d suggest we just have a single naming scheme for all upgrades. When both execution and consensus layers upgrade at the same time we just use the same name for both (so the next hard fork would just be Shanghai which is what most people outside of consensus core devs are calling it anyway) - when they’re separate they just take the next name in line.

---

**timbeiko** (2022-12-01):

I’m happy with that if it works for client & testing teams! The one risk I could see is that *something*, *somewhere* expects the EL & CL names for an upgrade to be distinct and breaks ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)  if that’s not a concern, then single names work for me just as well ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

Also agreed switching after Shanghai would be ideal given the community is already aware of this name.

---

**axic** (2022-12-01):

Out of curiosity, what is the reason the current scheme is not sufficient (for the short/medium term)? We still have Shanghai, Cancun, Prague, Osaka, Bogota to go on the EL side, and unlimited options on the CL side.

---

**timbeiko** (2022-12-01):

The dual names are confusing. We could alternate between cities and stars though! Or even move to one or the other.

---

**ethjoe** (2022-12-01):

By moving on from the current system, we can pay homage to Ethereum’s history, while working toward something unique that can be long-standing, and that meets the goal of representing both layers as “parts of a whole”.

On the first note, the *original* Ethereum roadmap included the four stages: Frontier, Homestead, Metropolis and Serenity.

Frontier and Homestead were delivered, as was Metropolis, albeit in three stages (Byzantium, Constantinople, Istanbul). The final stages of that original vision included a complete proof-of-stake and sharding. Relatedly, EIP-4844 marks the start of sharding, after Shanghai closes out the PoS upgrade and withdrawals. This makes for a great opportunity to finally close that original chapter.

**I’d first propose that the name of Serenity be applied to the EIP-4844 upgrade**, marking an end to the celestial naming scheme that’s touched both the original roadmap and the current CL forks, before moving forward to a greener future.

For the future naming scheme proposal, an initial idea was to choose something that reflected the CL/EL, while having a parent-name that solidifies the relationship between two parts of one whole. For example, if one upgrade package was dubbed “Purple”, upgrades within it would consist of two sides, with one layer designated as “Blue” and the other “Red”.

There were a number of potential ideas discussed here (stars, sister cities, rivers), some of which I’ll include below. But these days, one of Ethereum’s unique powers is its ability to continue to develop independently of any original plans and roadmaps, founders, or a few OGs. This natural growth (combined with “garden” mantras that have taken *root* and the PoS narrative meshing well with a greener/cleaner system) led to exploration of botanical or ecological schemes.

**Specifically, I’d propose to make use of `families of trees` and species within those families to accomplish many of the goals set out above (reflecting on life, ecology, evolution, strength…)**. There are [enough unique families and varieties to apply to upgrades for years or decades to come](https://en.wikipedia.org/wiki/List_of_tree_genera). Examples, like Fir and Cedar as two sides of a package dubbed “Pinaceae” would do well to convey this natural relationship in a unique way. There’s enough diversity to (a) move in alphabetical order and/or to (b) skip specific species if/when there’s something too odd to include a name, or to (c) include more than two names for upgrades that require multiple steps. Some even come with their own (controversy-free) emojis ![:evergreen_tree:](https://ethereum-magicians.org/images/emoji/twitter/evergreen_tree.png?v=12) ![:palm_tree:](https://ethereum-magicians.org/images/emoji/twitter/palm_tree.png?v=12) ![:deciduous_tree:](https://ethereum-magicians.org/images/emoji/twitter/deciduous_tree.png?v=12)!  And on ordering, Latin names can be used as something more neutral if/when English names are less of a fit.

*Tl;dr suggestion: After Shanghai, sharding begins with the Serenity upgrade, which pays homage to Ethereum’s history (past and present) and closes an important chapter before moving forward. Going into the future thereafter with something that reflects biodiversity, evolution and connectedness, like tree-species and families, encompasses Ethereum’s natural growth (merkle trees anyone?), uniqueness, diversity, and the green future created by the work put into bringing the Beacon Chain and Merge to life.*

–

JS

Initial ideations:

A. Binary Star systems.

- Package: System
- EL: Star A
- CL: Star B

Reasoning against: Celestial names have been used for the CL and by many Cosmos and other chains. We can do more to be original and aligned here.

B. Major Rivers/Cities

- Package: Major River (e.g. Nile, Rhine, or Tigris)
- EL: City A (e.g. Cairo, Bonn, Baghdad)
- CL: City B (e.g. Giza, Cologne, Mosul)

Reasoning against: While this version (suggested by Peri) is my favorite alternative to the above, this suggestion also gets caught in our current city-scheme that’s been used for the better part of a decade. There’s been pushback against flags and nationalism related to upgrades as well.

C. Planets & Largest Moons

- Package: Planet (e.g. Mars)
- EL: Moon A (e.g. Phobos)
- CL: Moon B (e.g. Deimos)

Discussed and suggested by Tim above, this is solid and unique with many options, but continues the celestial track.

Thanks to Tim, Pari, Peter and others for their input!!

---

**axic** (2022-12-01):

Right. I assume it may only confusing when they are rolled out together? Independent updates would not be confusing, but will we get independent updates?

---

**timbeiko** (2022-12-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> Independent updates would not be confusing, but will we get independent updates?

Yeah my assumption is coupled will likely be the default, but perhaps that’s wrong. For non emergency updates it seems simpler to bundle testing, releases, etc.

---

**protolambda** (2022-12-01):

We can keep eth conference cities for EL and stars for CL, but just combine them for the short upgrade names where necessary.

Suggestions:

Lontair (Londen + Altair)

Paritrix (Paris + Bellatrix)

Shapella (Shanghai + Capella)

Canubhe (Cancun + Dubhe)

Practra (Prague + Electra)

**Dubhe** would be my strong preference for star name after Capella: it’s the traditional/formal name for Alpha Ursae Majoris, also known as the “Big Dipper” and “**Great Bear**”: the ideal name to close a bear market with.

Electra would then be a great follow-up star name: Electra is a star in the Taurus constellation (bull after bear ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12) ).

---

**vgururao** (2022-12-02):

Since consensus layer is the common ground, and execution is like built environment on top of it, perhaps a natural feature of the city…so Shanghai might go with river Huangpu.

Or if the star is common ground natural object, the constellation becomes like the city. So Capella would go with Auriga.

Another option would be to link cities to stars using astrology somehow.

---

**abcoathup** (2022-12-02):

I wanted [emojis](https://emojipedia.org/) as a short reference to the name for the memeability, on that basis I thought about animals or the [zodiac](https://en.wikipedia.org/wiki/Chinese_zodiac).

[@protolambda](/u/protolambda)’s [name blending](https://en.wikipedia.org/wiki/Name_blending#Names_used_to_refer_to_celebrity_couples) feels like a **winning** concept.

It allows the continued Devcon city names (or notable Ethereum cities) for EL upgrades and alphabetical star names for CL upgrades, and nicely links them.

We also can use it now and don’t have to wait for the upgrade after Shapella.

We can use an emoji which fits either the name or the main feature(s) of the upgrade.

![:red_gift_envelope:](https://ethereum-magicians.org/images/emoji/twitter/red_gift_envelope.png?v=12) Shapella (Shanghai + Capella)

![:bear:](https://ethereum-magicians.org/images/emoji/twitter/bear.png?v=12) Canubhe (Cancun + Duhbe)

![:european_castle:](https://ethereum-magicians.org/images/emoji/twitter/european_castle.png?v=12) Practra (Prague + Electra)

---

**spalladino** (2022-12-04):

How about gods names from the Greco-Roman pantheon, using the Greek and Roman name for EL and CL? The god’s attribute can be the high-level friendly name. So the Dyonisius/Bacchus update would be affectionately called the Wine one, the Jupiter/Zeus Thunder, and so forth.

---

**abcoathup** (2022-12-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/spalladino/48/36_2.png) spalladino:

> Greco-Roman pantheon

I like the idea of tying the EL and CL upgrade names together, but I think we should leave the gods to the gods.  My concern is offending believers and the strong European cultural focus.

EL upgrades continuing to use Devcon (and other prominent Ethereum cities) city names would be representative of Ethereum culture & history, though we need to avoid flags/nationalism.

---

**mkalinin** (2022-12-09):

I like this proposal the most. We should decide a name of which layer to use as the name for the whole thing in the case of two-layer HF. And then keep the same notation as we use to day for spec docs, e.g. Capella for CL, Shanghai for Engine API specs.

Using a mixed name is a good one but I don’t like it because everyone will have to keep three names in mind when talking about two-layer HF.

Note that we will run out of Devcon city names in case of >1 HF per year. Devcons to be happening in locations defined by EL’s HF names is one of potential solutions to this problem.

---

**LukaszRozmej** (2022-12-15):

For D I like Deneb more: [Deneb - Wikipedia](https://en.wikipedia.org/wiki/Deneb)

---

**mcdee** (2022-12-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> I would therefore like to propose moving to a new naming scheme which uses a single term to describe the high-level upgrade (like “The Merge” did) and has related terms to describe the individual EL & CL specs (like Shanghai/Capella). I think a good theme for this is “structures with sub-components”.

Please can we just stick with what we have for the execution and consensus layers?  We already have a history of past names and a plan for future names, so any change will cause disruption and add to the technical debt of the ecosystem.

Naming things is hard, because we don’t know what the future brings so cannot pick something that will work well with future changes (Ethereum is a good example of this).  But consistency brings its own benefits, and reduces the mental load when coming in to the Ethereum space.  Taking the consensus layer as an example, we are now on a path “A,B,C,…” for each hard fork, which makes it very easy for someone coming in to the space to know the ordering of the hard forks.  Execution layer requires a bit of tribal knowledge, but that is now a given and not going to change so the best we can do is not to increase their burden but having multiple systems that happen at different points in time.

As for having a user-facing name for the upgrades, I maintain that the best solution here is to talk about the execution layer name and not the consensus layer.  Anything that is consensus layer-specific is likely to only matter to validators, and they are generally speaking more aware of the difference between the layers and understanding of what is activated when (the BLS to execution change operations are a good example of this).  If we consider users to be those that may generate execution layer transactions, or benefit from execution layer transactions, then the thing they care about is upgrades in the execution layer so that it is what we should be talking about.

---

**merikarhu** (2022-12-16):

Kindly birthday note beacon chain, and the community!

conversations? of a posthumous naming scheme layer. Examples; Hawking,

Name is identity, whether we imagine a planet, city or else. In my mind, I compare updates/upgrades to historical artworks. “Pink. Election” draws pictures of our Consciousness. However; the term and the story behind delegate curiosity via different tenses.

Happy Holidays!

Enzo

---

**abcoathup** (2022-12-18):

A vote for Deneb

https://twitter.com/sproulm_/status/1604430081325436930

Caneb (Cancun + Deneb)

---

**sbacha** (2022-12-22):

Please do not do this this is barely decipherable and will make it difficult for non english speakers.

---

**abcoathup** (2022-12-26):

Associating an emoji per release would hopefully make it easier to identify upgrades, regardless of language.

The Merge (Paris + Bellatrix) ![:panda_face:](https://ethereum-magicians.org/images/emoji/twitter/panda_face.png?v=12)

Shapella (Shanghai + Capella) ![:owl:](https://ethereum-magicians.org/images/emoji/twitter/owl.png?v=12) ( for [withdrOWLs](https://twitter.com/Renethftw/status/1595451793349255170))

---

**Pandapip1** (2022-12-27):

How about instead we create an inline-able image, to differentiate between actual use of an emoji and using it to reference Ethereum upgrades?


*(12 more replies not shown)*
