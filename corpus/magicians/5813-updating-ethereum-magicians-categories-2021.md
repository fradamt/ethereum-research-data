---
source: magicians
topic_id: 5813
title: Updating Ethereum Magicians Categories - 2021
author: timbeiko
date: "2021-03-26"
category: Magicians > Site Feedback
tags: []
url: https://ethereum-magicians.org/t/updating-ethereum-magicians-categories-2021/5813
views: 1185
likes: 27
posts_count: 14
---

# Updating Ethereum Magicians Categories - 2021

The top-level categories used here seem to be out of date compared to our current areas of work. Here are some suggestions about what we could add/remove at the top level so that posts are categorized more relevantly:

- EIPs

Add an “ERC” sub-category

Primordial Soup

- Consider removing: looking at the posts under this category, it’s hard to find a unifying theme.

Fellowship Gathering

- Perhaps make a sub-category of “Working Groups” ? Or, if we want to use it to advertise certain events/forums, like it has been the case lately, perhaps consider renaming to “Community Calls & Councils”?

Working Groups

- A lot of the actual working groups are outdated. I also think we should perhaps split the core protocol and application-layer working groups. I would suggest adding “Protocol Improvements” as a top-level category with the following subcategories: State Management, Proof of Stake, EVM, Merge, Sharding, Cryptography, Transaction Improvements.

Action Item

- This category seems stale. Perhaps we should archive it?

Curious about others’ thoughts/suggestions!

## Replies

**jpitts** (2021-03-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> EIPs
>
>
> Add an “ERC” sub-category

Definitely agree!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Primordial Soup
>
>
> Consider removing: looking at the posts under this category, it’s hard to find a unifying theme.

I would argue to keep Primordial Soup, this is useful for when new proposals show up pre-EIP stage. But this could be better positioned i.e. what are general discussions, and what could potentially become an EIP some day.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Fellowship Gathering
>
>
> Perhaps make a sub-category of “Working Groups” ? Or, if we want to use it to advertise certain events/forums, like it has been the case lately, perhaps consider renaming to “Community Calls & Councils”?

Overall this could be broadened to mean “Happenings”, with subcategories “Community Calls”, “In-Person Councils”, “Events”

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Working Groups
>
>
> A lot of the actual working groups are outdated. I also think we should perhaps split the core protocol and application-layer working groups. I would suggest adding “Protocol Improvements” as a top-level category with the following subcategories: State Management, Proof of Stake, EVM, Merge, Sharding, Cryptography, Transaction Improvements.

Agree! [@anett](/u/anett) and I were once discussing that we remove them altogether. We can definitely better organize these, I like the split you propose. One thing too is that a topic discussion usually happens under the context of the “EIPs” category (and there is no way to have more than one category for a topic).

It is actually the EIPs category which is less useful, because w/ the tagging and the title w/ EIP-XYZ anyone can find EIP-related topics. Perhaps we should emphasize the use of general subjects under working groups and remove EIPs.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Action Item
>
>
> This category seems stale. Perhaps we should archive it?

I agree; we should archive this category. We can use tagging and the title for this.

---

**timbeiko** (2021-03-26):

Thanks for the thoughts. Here are a few comments on your comments ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> I would argue to keep Primordial Soup, this is useful for when new proposals show up pre-EIP stage. But this could be better positioned i.e. what are general discussions, and what could potentially become an EIP some day.

My view on this is that the categories themselves are sufficient here. If someone has a rough idea about the merge, they can just make a post in the Merge subcategory directly, for example. EthMagicians already has an aura of “place where you can bring up semi-formalized proposals”, so I’m not sure another “layer” is needed. Weakly held opinion, though!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> Overall this could be broadened to mean “Happenings”, with subcategories “Community Calls”, “In-Person Councils”, “Events”

Yep, I like that!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> One thing too is that a topic discussion usually happens under the context of the “EIPs” category (and there is no way to have more than one category for a topic).

I think that’s fine: when things are EIPs they can move from the Working Groups category to EIPs. This is why I’d remove the “Primordial Soup” category.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> It is actually the EIPs category which is less useful, because w/ the tagging and the title w/ EIP-XYZ anyone can find EIP-related topics. Perhaps we should emphasize the use of general subjects under working groups and remove EIPs.

Hmm interesting! I’d be a bit cautious about removing EIPs because most of the “discussion-to” links from EIPs point here. It’s a nice place to aggregate them. Also, if we remove it, then someone may not know what category to put their `discussion to` link in and it may lead to less stuff being posted here, which is not great.

---

**vbuterin** (2021-03-26):

I would even say that each individual working group should be a top-level category on the same level as Primordial Soup, Fellowship Gathering and the others.

Basically move away from hierarchical categorization entirely; if some topic needs two labels then it can just be put into two categories (eg. “EIPs” and “State Management”)

---

**jpitts** (2021-03-26):

[@vbuterin](/u/vbuterin) the designers of Discourse seem to be very opinionated about only assigning one category per topic. It is “one category, and everything else just use tags”, and I haven’t found a plugin or anything which can change this behavior.

I do like the idea of eliminating some hierarchy, particularly in “working groups”, and also removing the term “rings” from titles and the whole notion that there are “working groups” for simplicity.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/f/fdd0763b73ce972d87ad18a0b66b25d63fdbaed3_2_517x146.png)image1174×332 27.2 KB](https://ethereum-magicians.org/uploads/default/fdd0763b73ce972d87ad18a0b66b25d63fdbaed3)

And this brings me to an idea: how about we move these working groups to be under EIPs instead, ensuring that everything EIP-ish is captured by the links that [@timbeiko](/u/timbeiko) referred to and also that they can all have proper categorization as to subject matter. Core EIPs and last call are relegated to tags.

EIPs basically becomes a catch-all for any proposal work being done here on the forum, implicitly encouraging any discussions under a technical subject leading to the creation of an EIP.

I’ll also check to see if EIPs and other categories can be routed to a tag if we decide to remove categories / flatten it all out as [@vbuterin](/u/vbuterin) has proposed.

---

**timbeiko** (2021-03-29):

Generally agree, [@jpitts](/u/jpitts). One small comment re this:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> how about we move these working groups to be under EIPs instead

I think there are a few efforts which may span >1 EIP that we may want to use a broader category to reference. Specifically, I think these would make sense: State Management, Proof of Stake, Merge, Sharding.

The others I had previously mentioned (Cryptography, EVM, Transaction Improvements) all probably make more sense under specific EIPs.

---

**anett** (2021-03-30):

Thank you Tim for facilitating this discussion.

Regarding Working groups (Rings initially) , we noticed that Working groups are not a thing anymore and the forum has evolved over time significantly as the Ethereum did too. We wanted to announce diminishing Rings (now Working Groups) which they evolved into a real projects (many projects started initially on Ethereum Magicians forum) or those WGs (Rings) dissolved over time.

The forum is now more focused on EIPs and less on Working groups and people working on different topics (like wallets, UX…).

Regarding Categories and keeping up forum up to date:

“Primodial soup” - This is for topics that don’t have it’s own category and authors of the posts are not sure which category it should be under. I would like to keep it

“Fellowship Gathering”- This can be renamed based on [@jpitts](/u/jpitts) mention to “Happenings”. We do plan to host more conversations and organise events when the situation will allow us to do so, hopefully at next Devcon

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> Overall this could be broadened to mean “Happenings”, with subcategories “Community Calls”, “In-Person Councils”, “Events”

I would propose to add Core EIPs, Networking EIPs, Interface EIPs , ERC EIPs , Meta EIPs, Informational EIPs as listed on https://eips.ethereum.org/. We can replace WGs with EIPs which I think is more accurate but we should keep in mind to group EIPs under the same category as on https://eips.ethereum.org/

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Hmm interesting! I’d be a bit cautious about removing EIPs because most of the “discussion-to” links from EIPs point here. It’s a nice place to aggregate them. Also, if we remove it, then someone may not know what category to put their discussion to link in and it may lead to less stuff being posted here, which is not great.

Definitely let’s not delete any of the EIP discussion posts that are already on forum.

---

**jpitts** (2021-03-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> The others I had previously mentioned (Cryptography, EVM, Transaction Improvements) all probably make more sense under specific EIPs.

When you say “under”, do you mean that these are specific EIPs that should be in a subcategory, under the category of EIPs e.g. EIPs/EVM?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> I think there are a few efforts which may span >1 EIP that we may want to use a broader category to reference. Specifically, I think these would make sense: State Management, Proof of Stake, Merge, Sharding.

In my proposal “EIPs” as a category would generally mean that ongoing work is being done rather than a specific EIP number, replacing the notion of “working groups” as the way to organize the main subject areas of technical discussion.

I’ll create a specific proposal below with these suggested top-level non-EIP categories, using EIP subcategories for when the discussions produce formal proposals. “Primordial Soup” is no longer necessary in this scenario, and the categories under “Working Groups” flattened out to the top-level, removing the “Ring” term.

---

**Proposed set of changes to the categories - revision 1:**

X Primordial Soup

**EIPs** - *let’s keep discussing whether to use all of the EIP categories here, or put them all together and use tags*

? Core EIPs

? ERCs

? Interface EIPs

? Meta EIPs

? Networking EIPs

? Informational EIPs

**X Last Call** - this notion is moved to a tag

*Top-level categories of discussions and pre-EIP work:*

**EVM** - *perhaps this is over-specific, we could call this “Execution Environment” and it almost rhymes with EVM* ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

**Cryptography**

**Interfaces**

**Light Clients** - *related topics have been under “constrained resource clients” but this is too long*

**Merge** - *this is a specific initiative, along the lines of Eth1.x, Phase 0, etc. Perhaps a better term is “Integrations” so we can use it for other discussions and initiatives*

**Networking**

**Proof of Stake**

**Proof of Work**

**State Management** - *should we also put Sharding topics under this one? Where would data availability go? There are also discussions under “Data Ring” which can be moved under this broader category*

**Tooling**

**Tokens**

**Transactions** - *removed “Improvement” as all of these categories are about improvement* ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

**Wallets**

**UX**

**Site Feedback**

**Happenings**

**– Community Calls**

**– In-Person Meetings**

**– Events** - *events are basically just a set of in-person meetings so we should keep discussing*

**X Working Groups** - *several these are moved under EIPs, others which are less commonly used are switched to using some tags, others are placed under Archive.*

**X Action Items** - *relegated to a tag*

**Archive** - *this is for initiatives that are no longer active / no longer have a champion*

**– Ethereum 1.x** - *this is the old Eth1.x which came out of Prague, current R&D in this line works happens over at https://ethresear.ch now. The term is increasingly murky IMO*

**– Education**

**– Fund Recovery**

**– Signaling**

---

Whew.

> “There are only two hard things in Computer Science: cache invalidation and naming things.”
>
>
> – Phil Karlton

---

**timbeiko** (2021-03-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> When you say “under”, do you mean that these are specific EIPs that should be in a subcategory, under the category of EIPs e.g. EIPs/EVM?

I meant that these categories are probably not needed, and instead we can create EIP-specific posts (ex: EIP-2315 which is related to the EVM) under the EIPs category, potentially with tags.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> EIPs - let’s keep discussing whether to use all of the EIP categories here, or put them all together and use tags
> ? Core EIPs
> ? ERCs
> ? Interface EIPs
> ? Meta EIPs
> ? Networking EIPs
> ? Informational EIPs
> X Last Call - this notion is moved to a tag

I don’t think we need categories for every type of EIP. For **Last Call**, what do we actually do now? Do we manually move EIP threads to that category when the EIP moves to the Last Call status? If not, then I think we can remove it and use a tag.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> EVM - perhaps this is over-specific, we could call this “Execution Environment” and it almost rhymes with EVM
> Cryptography
> Interfaces
> Light Clients - related topics have been under “constrained resource clients” but this is too long
> Merge - this is a specific initiative, along the lines of Eth1.x, Phase 0, etc. Perhaps a better term is “Integrations” so we can use it for other discussions and initiatives
> Networking
> Proof of Stake
> Proof of Work
> State Management - should we also put Sharding topics under this one? Where would data availability go? There are also discussions under “Data Ring” which can be moved under this broader category
> Tooling
> Tokens
> Transactions - removed “Improvement” as all of these categories are about improvement
> Wallets
> UX

Generally agree with this list, but I would remove **EVM** & **Cryptography**. I think **Merge** and **State Management** are good as is. **Sharding** could also be an extra top-level category.

Everything else LGTM ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

---

**jpitts** (2021-03-30):

Ok, for Merge, how about for clarity call it “Eth1-Eth2 Merger” as proposals have referred to this on EthResearch?

We do need to come up with a better term for this merging of the PoW Ethereum network over to PoS / Beacon Chain, if we are indeed going to try to drop the 1 and 2 distinction.

Or “Mainnet-to-Beacon Chain Merger”?

Some have called it “The Merge” but this is starting to look like marketing to me.

---

**jpitts** (2021-03-30):

**Proposed set of changes to the categories - revision 2**

X Primordial Soup

**EIPs** - *let’s keep discussing whether to use all of the EIP categories here, or put them all together and use tags*

**X Core EIPs" – *this notion is moved to a tag, topic recategorized under EIPs*

**X Last Call** - *this notion is moved to a tag*

*Top-level categories of discussions and pre-EIP work:*

**Cryptography**

**Interfaces**

**Light Clients** - *will move topics under “constrained resource clients” to “Light Clients”*

**Merge** - *what to call this initiative is still being discussed*

**Networking**

**Proof of Stake**

**Proof of Work**

**State Management** - *will move topics categorized under “Data Ring” to "State Management*

**Sharding**

**Tooling**

**Tokens**

**Transactions**

**Wallets**

**UX**

**Site Feedback**

**Happenings**

**– Community Calls**

**– In-Person Meetings**

**– Events** - *events are basically just a set of in-person meetings so we should keep discussing*

**X Working Groups** - *several these are moved under EIPs, others which are less commonly used are switched to using some tags, others are placed under Archive.*

**X Action Items** - *relegated to a tag*

**Archive** - *this is for initiatives that are no longer active / no longer have a champion*

**– Ethereum 1.x**

**– Education**

**– Fund Recovery**

**– Signaling**

---

**timbeiko** (2021-03-30):

List in your last post LGTM. [@vbuterin](/u/vbuterin) any thoughts?  As for the merge category, I think **The Merge** rolls off the tongue better than “Mainnet-to-Beacon Chain Merge”, especially given we are trying to use the terms “eth1” and “eth2” less.

---

**jpitts** (2021-03-30):

Ok, unless there are strong objections: “The Merge” it is ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

“The Merge” is similar to “Eth1.x”: an important initiative involving multiple EIPs and lots of other coordinated work.

---

**jpitts** (2021-04-08):

So the work has begun. The initial work to create the new top-level categories, migrate some Working Groups, and begin to move Core EIPs → EIPs is nearly complete.

I am starting to think that any “initiative” with a deadline, etc. should continue to be under Working Groups. But we should try to keep WGs to a minimum, only groups active in the last 6 months.

One reason for this is Eth1.x, this is still active and there may be links to the “Working Groups / Eth1.x” topic search URL.

Next steps:

- Create the archive for inactive WGs
- Begin to categorize old topics under “primordial soup” and “uncategorized” so they fall under the new “Top-level categories of discussions and pre-EIP work”

