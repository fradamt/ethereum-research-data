---
source: magicians
topic_id: 265
title: "EIP-1053: A proposal to move the content in ethereum/wiki to a Wikipedia-style wiki site"
author: jamesray1
date: "2018-05-03"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-1053-a-proposal-to-move-the-content-in-ethereum-wiki-to-a-wikipedia-style-wiki-site/265
views: 4243
likes: 25
posts_count: 35
---

# EIP-1053: A proposal to move the content in ethereum/wiki to a Wikipedia-style wiki site

> Github wikis have the limitation that anyone can edit them while it is difficult to moderate them (it is not possible to watch a page to get updates for changes), which is a double-edged sword, in that it is great for non-censorship which is in the spirit of the Ethereum philosophy, however it is also prone to graffiti, bias, etc. Because of this limitation of lack of ease for moderation, we should consider moving the content in this wiki to a wiki site, e.g. one that is hosted by Media Wiki, adding a deprecation notice to this wiki and refer to the proposed new Media Wiki hosted site. This would have the benefits of anyone still being able to edit the wiki (they do not even need to create an account, although there are advantages to doing so), as well as being able to more easily moderate content.
> — Home · ethereum/wiki Wiki · GitHub

Also quoted as above in [A proposal to move the content in ethereum/wiki to a Wikipedia-style wiki site · Issue #1053 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/1053).

## Replies

**fubuloubu** (2018-05-03):

I think this content is very expansive, and there may be an opportunity to create sub community wikis run by different interested parties. The section on dapp development specifically could probably be on it’s own away from all the details about the core implementation. Perhaps a main page to link to the different sub-wikis as a focusing point.

A “repository of all shared knowledge” is difficult to maintain across so many different subjects.

---

**jamesray1** (2018-05-03):

Nevertheless, when you look at Wikipedia, the content there is much more expansive.

---

**fubuloubu** (2018-05-03):

Wikipedia also has their own company and legions of editors to manage their wiki haha

---

**mikro2nd** (2018-05-04):

Almost ANY other wiki would be better than MediaWiki for this purpose… the wikisyntax is baroque, overcomplicated and just horrible. It is near impossible for the casual user to edit content without searching through endless (and not very accessible) help pages to get the most basic syntax right.  I feel that it is exclusionary to those who feel a sense of dread and exhaustion at the mere thought of dealing with MediaWiki’s contorted way of doing things.

My own experience with wikis dates all the way back to the very early days of WardsWiki and imho MediaWiki violates pretty-much every goal for WhatWikiIs ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9) If there’s an issue with moderation/spam on the ethereum/wiki (I confess I’ve not been tracking) I’d be willing to jump in to help with that rather than see a switch to MW.

---

**jamesray1** (2018-05-04):

Sure, but I think it is mostly edited by volunteers. And there are Media wiki sites like Bitcoin wiki https://en.bitcoin.it/wiki/Main_Page.

---

**jamesray1** (2018-05-04):

Sounds alarming, but as I mentioned, there is no way to get email notifications for changes to wiki pages, unlike Media Wiki sites. I agree that the syntax isn’t as good as GitHub Flavoured Markdown. You would either have to happen to notice a change while browsing or trawl through the edit history of each page and compare the history of revisions. If you know of a Wiki host that has a notification functionality with a UI that is more preferable to you then I’m all ears. I’ve asked a [question on WebMasters Stack Exchange about this](https://webmasters.stackexchange.com/questions/114899/host-for-a-wiki-site-that-has-watch-ability-for-pages-with-email-notifications), and previously I passed on feedback to GitHub Support to request for watchability. To watch a page on a Media WIki site, you tick the “Watch this page” check button while making an edit, or add the title of the page in a new line at https://en.wikipedia.org/wiki/Special:EditWatchlist/raw.

Note that there have not been too many graffiti edits so it doesn’t seem to be too much of an issue now, but as Ethereum grows that may change. At one point a user (probably unintentionally) edited the title of the home page while translating it, which actually broke the link to the home page. I have added a warning to the home page to help avoid this from happening. Other people have added spam, or self-promotional content in areas that are not really suitable for it to be added.

Another example: someone [edited this list of dapps](https://github.com/ethereum/wiki/wiki/Decentralized-apps-(dapps)/_compare/bb8350ae0e7f6c96a5703bbfd8f2eee90288f5f2...5c0375adcdea9a31bb0361a63dd855d336477344) with a statement that is not true, claiming that the list of dapps on the page was sourced from DappInsight, which they added a link to in the list. I happened to check the change when I saw the latest edit was from someone else when I went back to add something to the list. They also added more references to DappInsight in the sidebar and another reference on that page, which were unnecessary.

---

**jamesray1** (2018-05-05):

Another example that occurred today of changing the title, which breaks links to the old page: https://github.com/ethereum/wiki/wiki/Ethereum-Contract-ABI/_compare/62dee53b9b19ef22893edad778319980788ccbfc. I created an issue: https://github.com/ethereum/wiki/issues/591.

---

**boris** (2018-05-07):

I agree that GitHub Wikis don’t really work that well.

The question becomes what to move to, and the bike shedding around what system to use, who will maintain it, etc.

The wiki functionality here in Discourse, for instance, works and has great discussion forums, but doesn’t do cross page linking syntax very easily.

Do you have some thoughts on the goals & scope of the Ethereum wiki? Who is the audience? What content belongs, vs which doesn’t?

---

**jpitts** (2018-05-07):

Right now those working on documentation aggregate in the ethereum/documentation Gitter channel: https://gitter.im/ethereum/documentation

I’ll post a link to EIP-1053 there…

---

**jamesray1** (2018-05-08):

Hi Boris, like Wikipedia, the audience and content of the wiki could be very broad, covering the whole Ethereum ecosystem, but there is content that is more relevant to different groups, e.g. users, researchers, dapp developers, core developers, sharding researchers and developers, Casper researchers and developers, enterprises, etc. Lots of content could potentially be in one wiki site, provided that it is well organized and searchable.

I think the wiki is useful for people who are interesting in contributing in getting up to speed.

---

**boris** (2018-05-08):

Everyone you’ve listed is mainly involved in technical efforts. BUT – even there, user researchers and designers need to optimize for different things than slightly-better-than-Github-wikis that might be a fit for documentation writers and devs. Internationalization and versioning might be most important for doc writing, for example.

We have to understand who the audience is and who is taking responsibility. Which “entity” will run a single Ethereum wiki? How do we both collaborate and intensify efforts around one repository, while leaving room for other groups to run parallel efforts (forking documentation?).

I am even sensitive to colonizing this site. Have had great discussions with [@jpitts](/u/jpitts) on Twitter, but am essentially “assuming” that I can move in and use the Working Groups space as an area to document best practices for having technical / design / etc. meetups.

Anyone: question 1 is – which entity (including no entity, just a group of people who do it) will take responsibility for hosting, running, and maintaining the wiki at a technical level, as well as at a moderation level.

Essentially, who gets to say “no”?

I’d love to see efforts like this go into a grant system as well. Let’s gather some funds so N people can work on it for three months. This is what I am exploring – the collaborative funding and support model, so it doesn’t all have to get done by one Foundation or a small group of privately held companies.

---

**jpitts** (2018-05-08):

We do need a working group for operating “Online Presence”, one of the practices described in https://goo.gl/DrJRJV. This would include https://ethereum-magicians.org and any future web site.

Currently, I am looking after this Discourse website, but over time we will add moderators and it will become more formalized.

As for the Wiki itself, this is an entirely different beast. It needs more champions (there are some very good ones, but perhaps not enough). It needs governance.

---

**boris** (2018-05-08):

Here’s an example of an Ethereum focused wiki that is very specialized http://tokenengineering.net/

That’s Trent McConaghy of BigChainDB / OceanProtocol who kicked it off.

Bottom line: great idea, pick a topic / area of interest / type of audience and gather a group to host it and maintain it and go from there.

---

**jamesray1** (2018-05-09):

Personally I’ve already spent a lot of time editing docs pro-bono, so I’m not keen to create a new wiki site and copy and paste the contents of the Github wiki to the new site. Additionally if the syntax of the wiki doesn’t support Markdown then it would have to converted (manually or automatically if there’s a tool for that). I had a look at http://doc.wikidot.com, but it doesn’t support `[link](URL)` style links.

---

**geleeroyale** (2018-05-09):

If you just want people to have a nicer experience reading the wiki, you could easily port it over to mkdocs. I made the Giveth wiki, using mkdocs with material theme - it takes markdown files and renders them out nicely. Have a look at https://wiki.giveth.io

It is mainly a task of setting up mkdocs, write a mkdocs.yml file for site structure, choose a theme and host the thing (we use netlify). If you don’t want to do it, or don’t want to do it pro-bono, we can put it up as a task for Giveth social coding with a bounty attached.

---

**boris** (2018-05-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jamesray1/48/1548_2.png) jamesray1:

> Personally I’ve already spent a lot of time editing docs pro-bono, so I’m not keen to create a new wiki site and copy and paste the contents of the Github wiki to the new site.

Yes, this is exactly my point! You’re already at the point where you feel that your contribution isn’t being valued.

Someone has to choose to host and maintain such a thing. You don’t need permission if you want to do it. If you need resources, you’ll need to gather supporters and help.

I don’t know who runs these other wikis:

- Welcome to The Ethereum Wiki - The Ethereum Wiki
- Home | ethereum.org

It might be interesting to start by curating a list of all the wikis, who runs them, what is their intended audience, and then go from there.

Let me know what you need help with.

---

**jamesray1** (2018-05-09):

Hmm, it’d be interesting to see if you can use the wiki in a repo, rather than the code, to generate the site.

---

**jamesray1** (2018-05-09):

I’m working on sharding development, there is a lot to do there (and Drops of Diamond has not received a grant for that yet either). So I need to limit my time that I spend on other things as much as possible. I’m happy to spend a bit of time updating the wiki, mainly on sharding, with new research as it comes out, but I don’t have time to set up a new site.

Interesting, I haven’t seen https://theethereum.wiki/w/index.php/Main_Page before! Still, this is a MediaWiki site, so it won’t be easy to move all the Github wiki content to this site, and the syntax isn’t as nice. The site [isn’t active](https://theethereum.wiki/w/index.php/Special:Statistics). there are [junk pages](https://theethereum.wiki/w/index.php/Special:AllPages) and you can’t create an account and edit pages. But due to the syntax I don’t think we should revive it or use a MediaWiki site.

Ethdocs is a historical reference for Homestead, I submitted a [pull request on the source code](https://github.com/ethereum/homestead-guide/commit/1c1c597d9bd229055cd957e2b16e37933a9759) to that effect last week which has been merged. I submitted [another PR](https://github.com/ethereum/homestead-guide/pull/447) just now to update the site, not just the repo.

I’ve started a list [here](https://github.com/ethereum/wiki/wiki/List-of-other-Ethereum-wikis-and-documentation).

More sites were suggested [here](https://www.quora.com/Whats-a-good-host-for-a-wiki-site-that-has-watch-ability-for-pages-with-email-notifications-for-changes-and-compatibility-with-GitHub-Flavoured-Markdown/answer/Jeremy-Lee-Jenkins-1?__filter__&__nsrc__=2&__snid3__=2451575456).

---

**fubuloubu** (2018-05-10):

In response to “working group” style wikis, I am a member of the [SecurEth.org](http://SecurEth.org) team who has a foundation grant to create Smart Contract Development Software Engineering guidelines. Part of that is coming up with a governance structure for how that effort accepts proposals and makes edits, in order to ensure the proposals capture the spirit of what guidelines are (“why” do something and multiple suggestions for how) and actually stay relevant to the reality of the ecosystem.

I think if we’re discussing multiple working groups (UX/Wallet, smart contracts, front end UI, token engineering, etc.) there should be a meta conversation here, and some sort of organization of those efforts so we don’t end up with multiple different sources of “truth”.

This is a growing pain I think. The realization that there are multiple “jobs” that need to get done, and ad-hoc wikis are not the best way to organize these efforts.

---

**fubuloubu** (2018-05-10):

We have a guidelines repo I was intending on using in this way.


*(14 more replies not shown)*
