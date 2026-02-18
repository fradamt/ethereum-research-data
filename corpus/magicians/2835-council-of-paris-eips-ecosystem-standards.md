---
source: magicians
topic_id: 2835
title: "[Council of Paris] EIPs & Ecosystem Standards"
author: boris
date: "2019-03-04"
category: Protocol Calls & happenings > Council Sessions
tags: [core-eips, eip, hardfork]
url: https://ethereum-magicians.org/t/council-of-paris-eips-ecosystem-standards/2835
views: 1714
likes: 1
posts_count: 3
---

# [Council of Paris] EIPs & Ecosystem Standards

This is the EIPs & Ecosystem Standards topic thread.

Initial raw import from HackMD. Thanks [@chaals](/u/chaals) for scribing!

## Action Items

*to pull out*

---

Boris: What does it mean to improve standards, create core EIPs, …

There might be improvements to e.g. JSONRPC specs. Chaals works on EEA who would like to just refer to specs for Eth things.

Daniel, colony, want to know about the process because I understand the importance of standards

Paalo, WASM team.

Gabriel

Freferik, Parity

Hadrien, iExec, triyng to understand the ecosystem. Working on TEE interface in EEA

Remco, hoping to get some scaling changes in next hard fork

Cristov, supposed to know blockchain

Fernan

Paolo, want to learn more about core EIP process

Chaals - EEA / PegaSys (long standards history)

Chris, working on ERC-1400 security tokens. Love standards

Boris: Maintaining some content overviews on the Ethereum Wiki -

https://en.ethereum.wiki/roadmap

https://en.ethereum.wiki/roadmap/istanbul

… going over 1.x and some 2.0 and eWASM stuff

… The Core Dev process proposing EIPs for hard forks are as close to in charge as anyone gets…

… Process has a standard - EIP233, there is discussion about improving it. Hope more people will pay attention to this and help improve it. Some CoreDev calls can be not very technical and that sucks time.

… People have accepted a timeline for Istanbul. May 17 deadline for proposals, July 19 implementation, mid-aug testnet, mid-oct for update.

… EIP1679 is the hard fork meta-EIP. I am trying to document what we are planning, where people can include core EIPs. I proposed to add a securirty review period, and maybe have face to face meetings.

… Right now we will propose EIP-615, ProgPoW (change to the mining code to protect against ASICs). Those are the two currently proposed.

??: Will net cost storage 1283 be re-proposed?

Fred: It will come up again, people want it. Don’t know who will push it.

Boris: we might not have answers in this room… [gets pen and paper].

Phil, Parity. Any high-level goals of Istanbul? Will we see stuff on state fees, or other 1.x stuff?

CHaals: I would prefer to see a steady upgrade cycle, without holding stuff up because we might get some favourite thing in.

Fred: This is first time we had a long lead - this helps get stuff in. For state fees we need to have the conversation now just to get a sense of what the community thinks of the political questions.

Boris: In some ways this is “who is the product manager”.

Phil: This is like “so what’s next?”

Fred: It is sort of pushing to improve Ethereum, but there isn’t clear buy-in yet on “the one thing”. WOuld be good to establish the goal for the next hard fork.

Boris: I’m hosting a 1.x roadmap session at EthCC to discuss this. Coming out of Stanford discussions in January, Alexey has been planning out State Fees. (Roughly, instead of storage growing for ever, some old unused stuff can get deleted.) He has a 3-fork (27 month) plan for how this will roll up. This is a new level of planning for the Ethereum ecosystem.

Fred: Also proposing a social contract that stops changes which don’t improve longevity.

Boris: In Eth 2 Zak fielded question of what is EEA’s plan for Eth 2.

Chaals: We need to adopt a particular plan, but roughly we tend to adopt more or less everything that we don’t specifically need to do differently.

Boris: We started discussions in Prague on specification - there are some things where we need to have specs, and it wouold be good if we improved the quality of specifications so buyers know that clients work the same way.

## Remco’s proposals

Remco: Elliptic curve precompile improvements, and fixing the ratio of storage to transaction call data costs. THey make layer 2 inefficient.

Boris: sounds like fixing layer 2 stuff would have a strong chance. What do you know about getting a core EIP accepted?

Remco: crickets.

… I went to the 1.x in Stanford to pitch it, and people didn’t chase me away so that was encouraging. Alexey has been shilling it in his blog.

… There was some traction on the precompile stuff.

… Next step is to get it on the wiki - things that need to be included, then joining the core-dev calls to promote the idea.

Boris: Difference between ERC and EIP - ERC is application layer and doesn’t affect the core clients. You propose one as a Pull Request on the EIPs github repo, referring to EIP 1 for formatting guidance, if you get that your EIP will get merged as a draft and get a number.

[It’s the issue / PR number]

Paolo: EIP 1 said it could be the issue number or something else.

Boris: People were gaming the issue numbers, to get one they liked.

Chris: I can propose an EIP for wallet addressing.

Boris: If it doesn’t require a core protocol hange, it can be an ERC and get taken up when it gets adoption. Now there are about 5 people making proposals, because you can make them. [[xkcd.com/927](http://xkcd.com/927)].

… Question is how much work editors should do on ERCs, or should they focus on core EIPs.

[Core == protocol changes.]

Boris: If it requires a hard fork, it is a core EIP.

Paolo: sometimes a proposal could be done at app layer, but would be better as a core EIP.

Boris: More and more app-layer EIPs are coming out. That motivated rings, to colelct expertise.

Fred: There is a grey zone - stuff like RPC that require client changes but not to protocol also get onto Core EIP list.

Boris: So, things that change the protocol or require client changes to make stuff work.

Fred: Yes - requires clients to change.

??: There is the idea that looking at the repo is hard because 300+ open issues. Brian proposed adding audiences as a category, so we know who should be looking at stuff, and help streamline the work because people find the stuff they should be doing more effectively.

… having a stage in the process that makes that group of people major stakeholders to move a proposal forward.

… kind of like petitions that have to get a response if it has a given number of signatures.

… should also help reduce load on EIP editors.

Boris: I know Bryant did a related EIP. Right now, the repo uses almost no features of github. 6 EIP editors are there to mostly help move stuff through. Nick Johnson has an automerger, so when the format is correct and you get merged, you can update the proposal in draft mode.

…Draft is indefinite, looking for support, review, quality, etc.

… Last Call hasn’t been very widely used yet. Idea is you got consensus, it’s all good, here is the last call for review. That should be at least 2 weeks long, and you hope people look at it then.

Chaals: EEA reads the RSS feed, and notes when EIPs go into Last Call on their weekly agenda.

… Last Call is good, but you want to get audience labeled right because you don’t want people saying at the end of Last Call “waaaait, we need to start again”

Boris: There are not enough eyes on review. That’s a hugely valuable thing to do for the community, and we need more of it.

… EIP editors make a decision after Last Call what to do with it based on comments, and then an ERC is final.

… for core EIPs, now (they didn’t go through last call until a few months ago) after Last Call it goes to a core-dev call. But core-devs should have been looking at it already. It gets scheduled on core-devs, and any core EIP can get onto that agenda. Sometimes EIPs get discussed pretty early then. Then there is an accepted state, which requires at least 2 major implementations.

??: Core-devs was used in the past to see if an EIP makes sense at all, in the early stage. It maybe got 5 minutes of time then, to help guide whether to pursue the idea. Now you need to convince core-devs to do a last call review at all - why does it go there again? You don’t need discussion there…

Boris: Yes, you need implementation. Which is not the same as specification. E.g. the Yeloow/Jello paper don’t include specs for the latest round of EIPs.

…: nor for Byzantium, for months.

Boris: Right. There is a discussion on improving the core EIP process.

[how does this work?]

Boris: EIP 1 doesn’t mention core devs. You have a spec, then it needs to get implemented, then it comes up on core-devs. As I read it.

Paolo: yes, that is what happens.

Boris: WOuld like to add a change, that whatever spec is being changed has to be updated before it can be accepted.

Chaals: Big fat plus one for that proposal.

Paolo: hard fork meta EIP 233 was merged. One version said before hard fork goes to final, spec must be upated. This was proposed 2 years ago, and people were really opposed. Part of the question was who would do the work. Consensus was not to require the work. But that was a time in the past…

Fred: Came up again, a few months ago. Felt like general consensus is that should be a requirement, on the EIP creator.

Boris: Figuring out decisions in the past and whether we can revisit them is hard - this is helpful to know.

Boris: You have your implementations, scheduled core-dev, generally that goes “yeah, sure”, and you do a PR on the hard-fork meta to include it on the roadmap. There is some confusion - people would like signaling earlier, which is one reason for the wiki noting what people are hoping to do. Would like more attention on that. So Remco you can start by linking your proposal from the wiki.

Paolo: Thinking maybe on the hard fork meta there should be proposed changes up to a certain stage. There was no distinction between proposed things that look likely and accepted things. That is a good visibility point.

Boris: Yep, has some formality of the github stuff around it. We can check and see if stuff will actually get worked on. Maybe we have “scheduled”, and “proposed” (for stuff people are **aiming** to get accepted).

Paolo: it comes down to the decision process.

Boris: Seems better in the repo than in the wiki, if possible. Using Github itself would help too in tagging stuff like this.

??: We went the other direction before. But with auto-merging it makes it harder to use all the github features. because things are not in the PR, they are merged as a file. There was discussion proposing to do this, and saying you can’t just merge drafts.

Boris: Specifically talking about doing this in meta-EIPs. They are not exposed in the repo.

Paolo: We started with labels, and then we narrowed the role of editors, to stop having opinion on the issue, and just checking the quality of the documentation. If you use the labels, you mix the roles of release manager.

## Replies

**chaals** (2019-03-04):

[HackMD notes](https://hackmd.io/lSbvnPNFRPukJQDuBwZX9A)

---

**boris** (2019-03-19):

Follow up from this session – as per [@axic](/u/axic) suggestion, changes to the Hardfork Meta. See:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png)
    [EIP-233: Formal process of hard forks](https://ethereum-magicians.org/t/eip-233-formal-process-of-hard-forks/1387) [EIPs](/c/eips/5)



> This topic is intended be the discussion for EIP-233. Any comment or feedback is very much appreciated!

