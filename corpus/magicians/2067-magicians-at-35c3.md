---
source: magicians
topic_id: 2067
title: Magicians at 35c3
author: ligi
date: "2018-11-29"
category: Protocol Calls & happenings > Regional Sessions
tags: []
url: https://ethereum-magicians.org/t/magicians-at-35c3/2067
views: 2619
likes: 33
posts_count: 16
---

# Magicians at 35c3

will other magicians attending 35c3? Perhaps we can have some spontaneous sessions there. We might perhaps be able to do this in the[Critical Decentralisation Cluster](https://signup.c3assemblies.de/assembly/54102b7b-aeff-427c-9da3-f39c4863ee1a) or allocate some workshop room for some sessions. I will also bring some magician stickers to 35c3 - I can also bring some more so they can be relayed to local groups.

## Replies

**5chdn** (2018-11-30):

I’m down, Ligi ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

#35c3

---

**veox** (2018-11-30):

Should nothing go horribly wrong, I’ll be at the congress.

---

**JosefJ** (2018-12-06):

Great idea! We can either submit that as part of the CDC program or we can do it ad hoc in the chill-out setup.

---

**ligi** (2018-12-06):

I think we should do one session as part of the CDC program - ad-hoc sessions will happen anyway ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=15)

Really want to make some people at #35c3 aware that they are Magicians as I think people from there could contribute and fit nicely in our ecosystem. Will also put a lot of these stickers on the sticker-tables - in the hope people check out what the Magicians are.

[![ethmagicians](https://ethereum-magicians.org/uploads/default/optimized/2X/e/e1f93bb782aebced15e44ac8493f2a84b7fd3b9e_2_690x388.jpeg)ethmagicians4000×2250 3.14 MB](https://ethereum-magicians.org/uploads/default/e1f93bb782aebced15e44ac8493f2a84b7fd3b9e)

---

**cleanunicorn** (2018-12-13):

I’ll be there too and could help spread the stickers.

---

**ligi** (2018-12-16):

[@cleanunicorn](/u/cleanunicorn) great!

and a small teaser: https://peepeth.com/ligi/peeps/QmfKRF1PTK6RaFhJmsG6VJg9BGdPmTHeiZfMzpikrsdR1a

---

**ligi** (2018-12-18):

the wiki for self organized sessions is now open:

https://events.ccc.de/congress/2018/wiki/index.php/Static:Self-organized_Sessions

Thinking about adding a session there - just not yet sure which room - I am undecided between these 2 options:

- Seminar room 14-15,  FCFS  – with 66 square meters and 20 seats (banquette seating) - projector, tables
- Lecture room M1,  FCFS  – with 118 square meters and 48 seats (classroom seating) – projector, tables

would prefer banquette seating - but this is for a max of 20 humans. Would keep the topic quite open like “Ethereum Magicians gathering at 35c3”

Also what length should we allocate? I would tend to 60min.

Also thinking about a session on the topic of ethereum key management (talking about hardware wallets, java-cards, …)

Other ideas or suggestions?

---

**mariapaulafn** (2018-12-18):

I’ll be there! and ready to help.

60 minutes is good. Key management as well. I think that some general education would  be ace too, and what we have been doing at magi about it.

The 48 people room sounds good. I think if we talk key management we will have enough interested people.

I’d like us to cover burner wallets as well, this is an interesting topic for CCC, happy to present it.

---

**mariapaulafn** (2018-12-25):

Hey [@ligi](/u/ligi) any updates on this? I have to opt-out Friday due to work, so im trying to work my fahrplan ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**ligi** (2018-12-25):

dam - I already registered for Friday a while ago - but just realized that I just posed it there:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png)
    [Wallet relevant sessions at 35c3](https://ethereum-magicians.org/t/wallet-relevant-sessions-at-35c3/2245/2) [Wallets](/c/wallets/17)



> One more interesting session (yes keys on smart-cards will be a thing in 2019 - https://github.com/status-im/status-keycard):
> https://fahrplan.events.ccc.de/congress/2018/Fahrplan/events/9346.html
> cc @bitgamma

---

**mariapaulafn** (2018-12-26):

Cool, ill be there! anything I can do to help?

---

**ligi** (2018-12-26):

great! Not that I am aware of - just wanted to have a loose gathering of magicians - don’t think there is a need for much preparation - but if you have ideas please shoot! Are you at location already.

---

**mariapaulafn** (2018-12-27):

Ah crap I just realized friday is 28th. Shit, I’ll try to come!

---

**veox** (2019-01-03):

### Recap

*(This is just a personal recollection, for the sake of posterity; you’ll see shortly that it’s of parts where I participated myself (what a surprise!..). Phrases in quotes are not actual quotes, but me paraphrasing.)*

The meeting lasted ~1 hour. There were ~30 (~50?..) people in the room, of various backgrounds - researchers, protocol developers, [d]application developers, auditors (security specialists?..), “generally interested”.

Of those present, ~10 (15?..) voiced one opinion or the other, or asked questions. Others participated in the “introduce yourself” part only.

The room was “almost big enough”, but there were not chairs for everybody. So, during several show-of-hands, we could’ve missed someone in the corner.

One person had a laptop open, but I’m not sure if they were taking notes, or just keeping an eye on the clock.

Two topics were discussed broadly: “state storage rent” and “governance”.

#### State storage rent

- A mention of why state bloat is increasingly an issue was made.
- A general description of “rent” was given.
- Of everyone present, no one was against the idea “over my dead body” (via show-of-hands).

One person was willing to argue against rent if need be, for the sake of those not present. This was not explored.

“Stateless” contracts (of the “merkle proof” variety) were discussed, but not delved deep into (as they do not provide a mechanism to remove state entries “no longer wanted by anybody”?..).
It was noted that, indeed, all contracts would have to be rewritten under the new “rent paradigm”, as they’ve so far been written without the consideration.
Recent proposals by [@AlexeyAkhunov](/u/alexeyakhunov) were mentioned.

- Of those present, only one person seemed to have at least some familiarity with those (via show-of-hands) - me, with the first one.
- I tried to describe a non-essential facet of the proposal, as it related to the discussion at hand: namely, that a “rent balance” is introduced, how it is drawn from, and by whom. Think I butchered it.
- The core of the proposal - namely, modification of the “storage layout” to allow for direct attribution of “who wrote what to the state”, using new opcodes, - was not discussed.
- Alexey’s second proposal, revolving around CREATE2, was not discussed.

The issue with rent remaining for infrastructure/“commons” on-chain contracts, such as the ENS Registry (hash map) was mentioned.

#### Governance

- Of those present, at least two were “satisfied with current governance in general” (via show-of-hands).
- The need for a systemic/actionable approach to this broad topic was raised - namely, either:

identify undesirable aspects of the current system/process, and describe approaches to get rid of them; or
- describe a desirable system/process, and then approaches to transition from one to the other.

*(I was one of the two “already satisfied” people, so zoned out during most of the discussion. Someone else could provide a summary…)*

### Post-meeting

There was a brief shuffle on the balcony, after which the participants dispersed throughout the congress. Assume undocumented “work in workgroups”.

[A session](https://events.ccc.de/congress/2018/wiki/index.php/Session:JuliaLang_--_A_first_introduction_and_why_*I*_am_excited_about_(let%27s_talk_compiler%27s_and_GPUs)) (unrelated to the above) was organised by @chriseth, to present JuliaLang; was not there, can’t describe.

I’m aware of no other Ethereum-related sessions. Ping if you do.

---

**AlexeyAkhunov** (2019-01-03):

Thank you so much for this write-up!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/veox/48/10_2.png) veox:

> Alexey’s second proposal, revolving around CREATE2 , was not discussed.

I have not got myself together to write the second version (needed to make some time for other things), but it will be done very soon.

