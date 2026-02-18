---
source: magicians
topic_id: 3053
title: Ethereum Core Devs Meeting 58 - Summary
author: mariapaulafn
date: "2019-03-31"
category: Protocol Calls & happenings > Announcements
tags: [core-devs]
url: https://ethereum-magicians.org/t/ethereum-core-devs-meeting-58-summary/3053
views: 1739
likes: 7
posts_count: 11
---

# Ethereum Core Devs Meeting 58 - Summary

After the last ECH (Cat Herders Call) - some of us agreed on summarizing the core dev meetings and post here and on Reddit for better accessibility and to expand the audience following core dev meetings by creating easy to read summaries.

Brett summarized this time. Thank you! (I would appreciate [@jpitts](/u/jpitts) if we could create a category for these summaries for people to find them easily)

### DECISIONS MADE

**DECISION 58.1**  The [ProgPoW Carbon Vote](http://www.progpowcarbonvote.com/) signal will be shutting down in 13 days from today. Everyone that wishes to vote will need to do so before this date and ensure they leave their ETH in the address they voted from until after block number 7504000, as per [Lane’s tweet](https://twitter.com/lrettig/status/1111652965331415040).

**DECISION 58.2**  Going forward Clients will not provide generic verbal updates in the meeting but should provide an update in the comments in the agenda. If there are any questions or anything specific to discuss a space will be left to do so.

**DECISION 58.3**  Going forward Reseach will not provide generic verbal updates but should provide an update in the comments in the agenda. If there are any questions or anything specific to discuss a space will be left to do so.

### ACTIONS REQUIRED

**ACTION 58.1**  Cat Herders to look at updating EIP1, see [here](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/ethereum-cat-herders/PM#19).

**ACTION 58.2**  Review the proposed solutions for Roadmaps in the [Ethereum Magicians](https://ethereum-magicians.org/t/more-frequent-smaller-hardforks-vs-less-frequent-larger-ones/2929) forum to decide if going forward the Core Devs adopts smaller hardforks rather than larger hardforks.

**ACTION 58.3**  Vitalik to format the currently proposed [EIP-1559](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/ethereum/EIPs#1559) so that it is correctly presented.

**ACTION 58.4**  Lane to provide a block number for when the [ProgPoW Carbon Vote](http://www.progpowcarbonvote.com/) will be shutdown.

**ACTION 58.5**  Discuss if ProgPoW should continue to be implemented if the Technical Audit is not funded in [Ethereum Magicians](https://ethereum-magicians.org/tags/progpow) or [here](https://ethereum-magicians.org/t/what-has-to-be-done-to-get-progpow-on-ethereum/1361) or [here](https://ethereum-magicians.org/t/motion-to-not-include-progpow-without-audit/3027).

**ACTION 58.6**  Clients should provide updates for future Core Dev Calls in the comments of the agenda and request an update to the agenda if they wish to discuss anything specific.

**ACTION 58.7**  Research should provide updates for future Core Dev Calls in the comments of the agenda and request an update to the agenda if they wish to discuss anything specific.

**ACTION 58.8**  Alexey to create a Beacon Chain Finality Gadget initiative working group and find someone to lead it, for context please see discussion in [Ethereum Magicians](https://ethereum-magicians.org/t/eth2-in-eth1-light-clients/2880).

## Replies

**jpitts** (2019-04-01):

This is a really good format, really needed!

Wondering what is appropriate (generally, finished content would go elsewhere e.g. EIPs, [EthHub](https://docs.ethhub.io), and Magicians’ scrolls).

Would we eventually be summarizing other meetings in the community, not just the core devs?

---

**mariapaulafn** (2019-04-01):

Hi! if we have sufficient volunteers…

We chose Magicians for the summaries and Github for the full call summary - let me know if you have better ideas

---

**jpitts** (2019-04-01):

Ok should this be a new Ring, or under the Education Ring? It may be MP’s Summary Ring ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9), but you’ll want to have this so others can easily help out. A community TLDR for core devs decisions!

I found myself doing the same thing with a list of Protocol releases, there was no definitive document. These things needs to be summarized and not primarily in 15 experts’ heads.

---

**boris** (2019-04-01):

It could go in [#eips:core-eips](/c/eips/core-eips/35) but really it should be called what it is – “Core Dev Calls”, and have a category called that. Just like EthMagicians hosts long form discussion for EIPs, no reason the same can’t happen for other content.

Edit: under the EIPs top level category might still make sense? Not sure if we need another top level.

---

**gcolvin** (2019-04-02):

Seems summaries (or at least copies of them) should be kept in the https://github.com/ethereum/pm repo along with the agenda and notes.

---

**boris** (2019-04-02):

yes, agreed that committing them as markdown files in the repo would be good, too.

The point of posting them here is that discussion and interaction and communication / broadcast goes beyond the bowels of Github.

---

**gcolvin** (2019-04-02):

Exactly.

01234567890

---

**jpitts** (2019-04-03):

So this brings me back to a Ring formation.

This work could happen in a Ring here in the Forum, perhaps this is associated with the Education Ring. The output could be delivered to the EthCatHerders, or simply posted directly to the comments of the core devs meeting agenda (this is always an issue e.g. https://github.com/ethereum/pm/issues/89).

---

**boris** (2019-04-03):

I’ll make a GitHub issue to finalize. But it’s not an Education ring. It’s a Core Dev notes category. We don’t have to have everything be a ring.

[@mariapaulafn](/u/mariapaulafn) what do you think — details in the issue:

https://github.com/ethereum-magicians/scrolls/issues/66

The issues get closed, where they are hidden by default.

---

**jpitts** (2019-04-03):

I do love the " Fellowship Gatherings > Core Dev Meeting Notes" suggestion LOL ![:smiling_imp:](https://ethereum-magicians.org/images/emoji/twitter/smiling_imp.png?v=9)… who is to say that the core devs conference call is not also a gathering of Magicians? Each Ring is free to call themselves whatever they wish.

I will go with this one initially.

