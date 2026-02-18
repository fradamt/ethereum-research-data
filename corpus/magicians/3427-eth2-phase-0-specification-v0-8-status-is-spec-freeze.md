---
source: magicians
topic_id: 3427
title: Eth2 Phase 0 Specification v0.8 - status is "spec freeze"
author: jpitts
date: "2019-07-01"
category: Magicians > Primordial Soup
tags: [consensus-layer, standards-writing]
url: https://ethereum-magicians.org/t/eth2-phase-0-specification-v0-8-status-is-spec-freeze/3427
views: 1828
likes: 10
posts_count: 8
---

# Eth2 Phase 0 Specification v0.8 - status is "spec freeze"

So Eth2 Phase 0 is apparently a frozen spec. ![:tada:](https://ethereum-magicians.org/images/emoji/twitter/tada.png?v=12)



      [twitter.com](https://twitter.com/dannyryan/status/1145554469884555264)



    ![image](https://pbs.twimg.com/profile_images/869016575839539200/Eh7zVsBa_200x200.jpg)

####

[@dannyryan](https://twitter.com/dannyryan/status/1145554469884555264)

  Eth2 spec release v0.8 -- SubZero

The phase 0 spec freeze is here! Thank you to everyone for all of the incredible work that has gone into this
https://t.co/XuSHr4NCnP

  https://twitter.com/dannyryan/status/1145554469884555264










The Phase 0 document appears to be a code-only or code-mostly “specification”, and elsewhere in the repo are tests. This approach to creating specifications poses challenges to implementers and security researchers, but is probably something which the Ethereum protocol researchers will not or cannot change.

https://github.com/ethereum/eth2.0-specs/blob/v0.8.0/specs/core/0_beacon-chain.md

Update: there is to be a wiki which will contain key parts of the spec.



      [twitter.com](https://twitter.com/dannyryan/status/1145741707528376320)



    ![image](https://pbs.twimg.com/profile_images/869016575839539200/Eh7zVsBa_200x200.jpg)

####

[@dannyryan](https://twitter.com/dannyryan/status/1145741707528376320)

  @DeanEigenmann @protolambda @badcryptobitch updating to v0.8 today and will put in the spec repo wiki

  https://twitter.com/dannyryan/status/1145741707528376320










Is there anything Magicians can do to help create a better specification for the next-generation protocol?

## Replies

**vbuterin** (2019-07-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> This approach to creating specifications poses challenges to implementers and security researchers, but is probably something which the Ethereum protocol researchers will not or cannot change.

Can you elaborate? If you want more English-language descriptions of what’s going on, I definitely know that we’re open to it and some of us have written such things to a partial extent already.

---

**jpitts** (2019-07-04):

A lot of work has been done to elaborate on the different aspects of Phase 0, in documents, in real-time chat, ethresear.ch, and in the implementers’ calls. And this has been done iteratively, evolving to what was released as the frozen Eth2 Phase 0 spec.

Having said that, I think that to call this a specification, all of the relevant descriptions, data structures, and codifications need to be brought together coherently into one document. And written in a way so that the intended behavior of the system and how the components interact are unambiguous.

The goal is that it would be possible for a qualified person who did not follow the evolution of Phase 0 or participate in the chats and implementers’ calls to comprehend and implement Phase 0.

It is true however that a technology cannot be developed in a vacuum, that any implementer would need to be inculcated with Eth2 culture and practices. Still, it would be helpful for Eth2 to have a solid specification in order to encourage further implementations and attracter wider security and economic review.

---

**jpitts** (2019-07-04):

Also, I found this helpful resource from the IETF: [Guide for Internet Standards Writers](https://tools.ietf.org/html/rfc2360). I think that it can be repurposed for the Ethereum community, not only adapted for protocol specifications but also for ERCs and dapp infrastructure.

https://tools.ietf.org/html/rfc2360

---

**greg** (2019-08-01):

The ETH2.0 specs looks a lot different than ETH1.x yellow paper, and imo thats totally fine. The ETH2.0 [spec](https://github.com/ethereum/eth2.0-specs/) is essentially a mono-repo of items that are “must haves” towards building out a full blown client. Is it organized in a meaningful way? No and yes, let me explain. You have probably over 20-30 people actively contributing to it in a month, across three different “phases” & a bunch of other docs. I wouldn’t say its a straight forward task, if you made everything into a single document, then no one would be able to keep up with the upstream changes because that one MD file would change 10 times a day (ill get back to this).

Let’s discuss the content. A specification should provide an implementer with what is absolutely necessary to maintain consensus, and as Danny famously says *[…] the rest is an implementation detail*. A blockchain consists of a dozen or so core modules; sync, databases, caching, ops, tooling (wallet gen, etc…), networking (peer discovery, peer sync, etc…), the node itself, an api server, and then debugging tools (grafana, geth attach) the list goes on. This stuff is not described by the spec, and if it was ETH2.0 would never ship.

What does the current spec offer us? It describes all necessary data structures, constants & state transition functions. This information is expressed through pseudocode examples and light descriptions, the yellow paper looks similar (ish) but with more mathematical formulas and proofs, which thankfully was not included in this.

What does the current spec miss? It doesn’t give us a good rational for ***WHY*** things are done, and it has a [supplementary doc](https://notes.ethereum.org/jDcuUp3-T8CeFTv0YpAsHw?view) but /shrug its not great. Using only the spec, you can in-fact implement an eth2.0 node, you just probably won’t understand what you’re writing. Also, the pseudocode is almost overly specific (in some cases) to python, or it’s overly optimized code, and requires three passes to make sure you read it correctly.

What I would like to see? A spec that walks us through a story of wtf is going on, sort of a user story. Writing it out more thoroughly would mean that instead of inline code snippets we could have an appendix to reference. Explanations of why Justification and finalization looks so bloody scary, whats going on here `justification_bits[1] = 0b1`? The best definition is from the supplementary doc, and says:

> "justification_bits  – 4 bits used to track justification during the last 4 epochs to aid in finality calculations

Still don’t get it? Most don’t at first, this is where we need better definitions.

Having a story (rather just plain english i guess?), walk through the spec might make more sense, such that researchers don’t need to spend as much time explaining things it for the 10th time. This would eliminate the need for a wiki, save time for researchers, and allow for anyone to drop in and understand whats happening. Now I think we’re in a unique time where non-implementers actually care a lot to read these specs. So the traditional, slap it on a MD and ask questions later approach is blowing up a bit.

Maybe it’s time to spend a month or so, agree on a new format, freeze all specs for a week and revamp. IMO it will be useless for “someone to create a better spec” without the researchers agreeing to it, now you’re maintaining two versions.

Wrap up - The [supplementary doc](https://notes.ethereum.org/jDcuUp3-T8CeFTv0YpAsHw?view) is a good first start, if this was in much more detail, placed at the top of the [phase 0 spec](https://github.com/ethereum/eth2.0-specs/blob/dev/specs/core/0_beacon-chain.md) I think we would be on to something.

With all that said and done, this is a research project and the implementers jumped the gun (a year ago, not so much now), and forced them (researchers) to expedite their efforts. Here we are, and we still have lots of time to fix it and perhaps set some standards moving forward.

*Shoutout to all the lads who complained and nagged but never wrote anything formally. This one’s for you Dean and Jonny.*

---

**dryajov** (2019-08-01):

Thanks for the link [@greg](/u/greg), I’m catching up on Eth2.0 and had never come across this supplementary doc. Makes a huge difference when coming up to speed. It should definitely be linked in the spec repo readme.

On the spec itself, I agree with the general sentiment, though it outlines all algorithms and data structures, it gives little context as to why they’re needed. I’m unsure of why this format was chosen, it’s close to what you’d expect from a formal language spec, but even those have a prose version that digest the formalisms. For example the webassembly spec uses this conventions - https://webassembly.github.io/multi-value/core/valid/conventions.html, it uses a formal notation and a prose notation that unwinds the formalisms.

IMO, an implementers manual that outlines the goals, gives context and expands on the formalisms is not out of place. I’m unsure who should produce those - the researchers or the implementers, but it’s clear that unless you’ve paid close attention to the various posts, threads and discussions scattered across many resources, implementing based solely on the spec would make what is already a complex piece of software that much harder to produce (if at all possible). We wouldn’t need this if there was already a reference implementation, but there isn’t one AFAIK?

---

**dryajov** (2019-08-01):

BTW, not suggesting that we should follow the format of the webassembly spec, just using it as an example. The supplementary doc seems just fine, it has sufficient detail to be able to understand why something needs to happen, maybe cross referencing to the python/pseudocode examples in the specs to give more context, etc…

---

**gcolvin** (2019-08-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dryajov/48/788_2.png) dryajov:

> On the spec itself, I agree with the general sentiment, though it outlines all algorithms and data structures, it gives little context as to why they’re needed. I’m unsure of why this format was chosen, it’s close to what you’d expect from a formal language spec, but even those have a prose version that digest the formalisms. For example the webassembly spec uses this conventions - https://webassembly.github.io/multi-value/core/valid/conventions.html , it uses a formal notation and a prose notation that unwinds the formalisms.

Anotther approach is [@ehildenb](/u/ehildenb)’s  KEVM paper and the corresponding  active [repo](https://github.com/kframework/evm-semantics) for an executable K specification of the current EVM.  Like the Wasm spec they use a careful mix of prose and formal notation.

