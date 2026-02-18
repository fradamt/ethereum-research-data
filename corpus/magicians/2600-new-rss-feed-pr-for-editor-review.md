---
source: magicians
topic_id: 2600
title: New RSS feed [PR for editor review]
author: fulldecent
date: "2019-02-06"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/new-rss-feed-pr-for-editor-review/2600
views: 723
likes: 1
posts_count: 1
---

# New RSS feed [PR for editor review]

Editors, please help to review and approve this update to the RSS feed



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/1693)














####


      `master` ← `spadebuilders:feed-improvements`




          opened 09:04PM - 12 Jan 19 UTC



          [![](https://avatars.githubusercontent.com/u/280420?v=4)
            bmann](https://github.com/bmann)



          [+89
            -27](https://github.com/ethereum/EIPs/pull/1693/files)







Partially addresses #1688

Global ```feed.xml``` that includes all EIPs. You […](https://github.com/ethereum/EIPs/pull/1693)can see a preview here https://5c3a52345d52e7000834b647--ethereum-eips-refactor.netlify.com/ --> and the direct link to feed.xml is here --> https://5c3a52345d52e7000834b647--ethereum-eips-refactor.netlify.com/feed.xml

[W3C Validator passed as valid RSS](https://validator.w3.org/feed/check.cgi?url=https%3A%2F%2F5c3a52345d52e7000834b647--ethereum-eips-refactor.netlify.com%2Ffeed.xml) -- with caveats about wrong link (since link is set to the live EIPS url), including author emails that look like tags, and use of relative URLs (which works in Atom).

Last Call metadata of ```review-end-date```  is done (previously merged in).

A couple of notes:
* refactored eipcontent generation into an include so all feeds can have the same internal content
* created is a manual data by the EIP author -- this is what pubDate is set to
* for the feed lastPubDate I am using the build date -- so every time the site is built, this field will change (since it usually gets built when EIPs are merged, this is OK)
* on Github Pages, you can't easily run a last-modified-date plugin -- we may want to encourage EIP authors to add / edit this manually as they majorly refactor Drafts
* to make more changes to the site -- like adding feeds to All/Core/Networking/etc -- the minima theme that is used needs to have files brought in; I brought in default.html for starters, which has /feed.xml hardcoded in the header by default
