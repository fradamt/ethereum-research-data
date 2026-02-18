---
source: magicians
topic_id: 3824
title: "EIP-2424: EIP Code of Conduct"
author: jpitts
date: "2019-12-04"
category: Working Groups > Integrity Ring
tags: [eip-process]
url: https://ethereum-magicians.org/t/eip-2424-eip-code-of-conduct/3824
views: 1437
likes: 6
posts_count: 11
---

# EIP-2424: EIP Code of Conduct

Yaz Khoury has created CoC which would cover the EIP process. This is an interesting development as there is no such policy defined for core devs, editors, and other participants.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/2424)














####


      `master` ← `YazzyYaz:patch-1`




          opened 10:23PM - 03 Dec 19 UTC



          [![](https://avatars.githubusercontent.com/u/9094204?v=4)
            YazzyYaz](https://github.com/YazzyYaz)



          [+84
            -0](https://github.com/ethereum/EIPs/pull/2424/files)







Proposing a new EIP for Code of Conduct in the EIP process to its participants.
[…](https://github.com/ethereum/EIPs/pull/2424)

This is due to me noticing actions of some individuals in the larger cryptocurrency ecosystem engaging in behavior that would necessitate the existence of such a document.

The Code of Conduct follows Contributor Covenant: https://www.contributor-covenant.org/

which exists in several open-source communities.

Currently, this Draft EIP will need a new commit to add an appropriate email so victims of harassment within the EIP process have a contact email to send complaints about any fellow member of the EIP process that are violating the Code of Conduct.

Happy to hear any feedback from the EIP community.

It doesn't fully follow the EIP guideline because it is referencing an external document which is licensed under CC-By-4.0 License.












Yaz’s proposed CoC was “taken directly from [Contributor Covenant Open Source Code of Conduct](https://www.contributor-covenant.org/) under the [CC-By-4.0 License](https://github.com/ContributorCovenant/contributor_covenant/blob/release/LICENSE.md)”

Text of the Code of Conduct:

https://github.com/ethereum/EIPs/pull/2424/files

Twitter announcement / discussion:

https://twitter.com/Yazanator/status/1202018509980606464

Reddit discussion:

https://www.reddit.com/r/ethereum/comments/e5wx9t/proposal_for_eip_2424_eip_for_code_of_conduct/

## Replies

**jpitts** (2019-12-04):

To provide some context, earlier in the year there was some work done to create a [policy framework](https://github.com/ethereum-magicians/integrity-ring/issues/11) and a [proposed CoC for community groups to adopt](https://github.com/ethereum-magicians/integrity-ring/blob/master/code-of-conduct/code-of-conduct-0.0.1.md).

This effort stalled, but perhaps EIP-2424 represents a path to move the work forward.

---

**MicahZoltu** (2019-12-04):

I’m not a fan of these sort of things on OSS projects for a variety of reasons but the main one is that it adds what I believe is a bureaucratic process to “don’t be a dick”.  I haven’t seen any serious conduct violations, even in the face of significant disagreement (e.g., Proof of Work Algorithm, Licensing, Miner Fee Rate, etc.) so I don’t think we need to introduce, debate, and codify “don’t be a dick”.

If people would like, I can go into my other reasons for disliking this sort of thing, but it is mostly political and I suspect it is the same arguments that have been made a million times across the internet as these sort of things have gained popularity.  I would *prefer* to avoid digging into the political side of the discussion if possible since I suspect it won’t go anywhere useful.

---

**Yazanator** (2019-12-04):

I removed the Github discussions-to link and pointed discussions to this url.

---

**Yazanator** (2019-12-04):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I’m not a fan of these sort of things on OSS projects for a variety of reasons but the main one is that it adds what I believe is a bureaucratic process to “don’t be a dick”. I haven’t seen any serious conduct violations, even in the face of significant disagreement (e.g., Proof of Work Algorithm, Licensing, Miner Fee Rate, etc.) so I don’t think we need to introduce, debate, and codify “don’t be a dick”.
>
>
> If people would like, I can go into my other reasons for disliking this sort of thing, but it is mostly political and I suspect it is the same arguments that have been made a million times across the internet as these sort of things have gained popularity. I would prefer to avoid digging into the political side of the discussion if possible since I suspect it won’t go anywhere useful.

I do want to clarify that I would like to allow for dissent as its important in a decentralized community. What I instead hope to achieve with this EIP-2424 is to minimize doxing and harassment of fellow EIP editors within the EIP repository itself.

If someone says something vulgar when submitting an EIP document, as long as its not targeting another individual, it seems fine to me. This EIP is still in draft stage and can be subject to change based on feedback and recommendations of those who wish to participate in helping draft one that better targets Ethereum.

In general, the document it references is the Contributor Covenant which has been adopted by multiple open source projects on a repository level.

As an example, if this EIP is say in Active mode, it doesn’t mean it applies to another repository like say Trinity or Vyper whose CoC, if applicable, is local to those repositories. EIP 2424 is local to the EIP repository only.

---

**localethereumMichael** (2019-12-04):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/y/ea5d25/48.png) Yazanator:

> What I instead hope to achieve with this EIP-2424 is to minimize doxing and harassment of fellow EIP editors within the EIP repository itself.

Is this an actual problem? Please point to some examples of doxing and harassment in the EIP repository.

---

**3esmit** (2019-12-05):

I think plagiarism should be mentioned in the list of harmful behavior. Just like all the others, it’s obvious, but this one is common in open source communities, even causing open source developers to only reveal source codes at launch.

---

**Yazanator** (2019-12-05):

I’ve seen it happen twice in other crypto communities, but I don’t want to bring back attention to it as it’s just needlessly re-instigating previous issues.

---

**Ashaman** (2019-12-09):

I agree with the posts here saying the purpose of this draft CoC is unclear, since there don’t seem to be many examples of the problem it is trying to solve (in the fora where EIPs are seriously discussed - crypto Twitter and Reddit are a different world but the CoC wouldn’t apply there anyway).

I’ve been engaging in online discussions since the BBS days of the early 90s and all the healthy communities that I’ve been part of stayed that way due to efficient moderation based on shared community values (not formal policies which - in larger organizations - tend to exist because of legal requirements and protect management from risk). The “we need a policy because we need a policy to point to if there is trouble” kind of thing is much less important in a decentralized community. I can see why it is useful for companies and people like conference and event organizers, but less so for a decentralized online community.

Of course you could say that a CoC is a reflection of community values that everyone can refer to etc, but from what I can see there isn’t enough of a problem to make it worth addressing (I am open to being corrected - if there’s a list of incidents which breach community values, then it may well be worth it to have a policy which would address future incidents and provide a mechanism to deal with it).

In the absence of that, IMHO, the tradeoff isn’t worth it. Community sanction for breach of community values is pretty good, and the Ethereum development community (by which I mean the group of people who actually discuss and contribute to EIPs, which is much smaller than the group of people who have invested in or use ETH) is still relatively small and community sanction relatively effective.

Plus drafting a CoC is a difficult job, even more so when it moves from merely stating principles to enforcement mechanisms and creates a whole new layer of risk and potential liability once you start having contact e-mail addresses and people who need to start deciding about excluding other people and so on. And even if a CoC is needed in principle, actually creating one is fraught with difficulty…

EDIT: Just wanted to add. I’m not against a CoC in all circumstances. I think for larger organizations and events like conferences, they serve a purpose. For a decentralized online community - particularly a smallish one which does not appear to have significant ongoing problems with harassment etc - I don’t think the tradeoff is worth it. That’s Stage 1 - do we need a CoC? Stage 2 is actually creating one and what it should include and what the enforcement mechanisms (if any) should be and that is difficult too. But if we don’t clear Stage 1, then there is no point in going to Stage 2.

---

**jpitts** (2019-12-09):

To add some context which may be obvious: this scene is global with lots of events and travel. We see each other all of the time, and there is a lot of workplace and personal interaction blending. What starts in online forums or in person at a party ends up affecting our job, etc.

So, basically, with a CoC adopted by the core devs, **the problems addressed are those that traditional legal systems cannot address** for people involved in the coordination of the protocol and those in the wider community that they interact with.

I think that one problem addressed by a CoC (and some kind of adjudication process) is that of **misrepresentation**. Often there is a situation in which someone accuses someone else (or their organization), of some kind of misdeed. It would be helpful to have a procedure in which one could say: you have violated this clause of this policy. Then evidence comes out, and it is settled.

Another recurring problem is **intimidation**, as in the case of Afri (no longer participating in the Ethereum community). Due to some actions he took, community members began ganging up on him in reddit and Twitter, spreading conspiracy theories, and worse. He experienced a great deal of personal stress and ended up leaving the Ethereum core devs, which was a very significant loss to the community.

This kind of situation is probably most clearly addressed in the [proposed CoC](https://github.com/ethereum/EIPs/pull/2424/files).

> Trolling, insulting or derogatory comments, and personal or political attacks

Perhaps a few people could have had a formal reprimand or certain privileges curtailed due to CoC violations, creating the impression that there are consequences for violations, reducing the tendency to attack.

Perhaps the online attacks against Afri could have been prevented had there been a CoC in place and an avenue to point out his own violations (not that there were any). Those attacking him may have felt that he was harming the community. The presence of a CoC and process alleviates some of the need to attack, because we have agreed that this is the process for finding justice.

Another situation is that of **sexual harassment**. There are some cases of this in the community. This is covered to an extent by CoCs used at events, but what about outside the context of our gatherings. We are an international scene and sexual harassment and other harms can occur which would basically be impossible to raise objections to, find justice for, except by public accusation. This has its own problems as it can devolve into injustices such as exile without due process.

In the proposed CoC, sexual harassment is partly covered by the following clause:

> The use of sexualized language or imagery, and sexual attention or advances of any kind

---

**Ashaman** (2019-12-16):

Thank you for the detailed response, it’s very useful to get some more details on what uses the CoC could be put to and why it may be useful.

I don’t think what happened to Afri was right, and the harassment he suffered should be condemned (ditto any kind of sexual harassment). I fully support the values set out in the CoC.

My concern is that this proposed CoC appears to be a solution looking for a problem. I don’t understand what problem it is meant to solve, why it is needed, or what specific difference it will make. I appreciate you’ve given some situations where it could be applied, but I don’t understand specifically how it would be applied and used.

Taking the Afri fiasco as an example - I don’t understand what exactly this CoC could have been used for (if it had been around then). Could it have been used to reprimand some of the people behind the Twitter and Reddit accounts that harassed him? How?

IMHO, harassment should be dealt with in the online forum or IRL event at which it happens (meaning the admins in charge of the online forum, the event organizers for events etc, along with the relevant local law, both civil and criminal). Those are the people best placed to a) investigate; and b) enforce any punishment that may be applied.

I’m skeptical about the value of this kind of overarching governance for a decentralized community, especially in circumstances where the CoC language is vague, decisions on “guilt” are certain to be controversial, and enforcement of sanctions is likely to be difficult.

Is this really the job of the core devs (or whoever agrees to be the contact person for complaints)? Adjudicating harassment complaints?

I think a CoC setting out values and principles that this community believes in is a great idea. When we start including sanctions, punishment and formal excommunication in the CoC, we’re opening a real can of worms, practically, procedurally and legally.

These are my concerns about having a CoC (with a quasi-judicial punishment process) at all. But if we do go ahead with one, I also have a number of detailed suggestions to address some of the practical issues with the CoC that I’m not getting into now.

