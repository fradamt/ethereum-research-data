---
source: magicians
topic_id: 2687
title: Let's say we patched together THE community web site
author: jpitts
date: "2019-02-20"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/lets-say-we-patched-together-the-community-web-site/2687
views: 988
likes: 8
posts_count: 4
---

# Let's say we patched together THE community web site

**What would you like it to be?**

The EF could release a new website soon, and many cool projects like [ethhub.io](http://ethhub.io) are gaining traction. This is a way for the community to contribute.

Before we dump our deepest rage or beautiful wishes about a website, let’s decide on how to approach this. Here’s a proposal about how to structure our individual thoughts about THE website:

First, **Strategy**:

- objectives of the website
- weighted target users
- entry points (domain name, SEO, sec), exit points

And then **Structure**:

- main blocks / sections of the home page
- main navigation links on the website
- which people / organizations should run which sections
- how to balance options (e.g. is it opinionated about how to run a node)

And then **Sustainability**:

- how to govern sections, how to manage the updates
- how to pay everyone, how to credit our work

## Replies

**boris** (2019-02-20):

Hey Jamie thanks for taking this long form. I’m not going to follow your structure ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

I think the first question is whether it is a shared community resource or not. If it’s not – then any opinions we have are just that, and people may be better off banding together and creating something like EthHub. Which is pretty darn good and uses common open source norms for managing a repo, pull requests, and markdown editing. You get stuff like contributors and diffs and discussions on changes as part of being based on git. So I would be disappointed if `ethereum.org` is just a different version of EthHub.

Then there’s the [Ethereum Wiki](https://en.ethereum.wiki), which Virgil ported from what was a stale Github Wiki. This has a web front end which anyone can edit (currently – the WikiJS system it runs is backed by Git and can have page / path level permissions set, as well as user logins). I have added several pages there, but the wiki is “lightly maintained” – that is, as far as I know, there isn’t anyone regularly monitoring and updating it.

[Drupal.com](http://www.drupal.com/) is an example of a highly informative “landing page” style site for a community.

So, let’s assume it’s an EF run landing page, since EthHub and the Ethereum Wiki already exist.

Here are my thoughts on objectives for an EF run landing / home page for Ethereum:

- What is Ethereum? What is Ether?
- Major news (newsletter sign up?)
- Major events
- Direct people to where they need to go based on what kind of target user they are – end user, developer, miner, exchange
- Case studies (like DrupalDotCom) – there was a call for impact so maybe those are a start; this could be contentious to curate; different types of case studies for open source projects? research? etc.?
- Foundation-specific objectives

It’s the foundation’s site. I think they should commit to transparency and open-ness, so I would suggest the source of the site on Git and clear ways of filing issues, contributing, and so on – if they want help maintaining it. But it should be relatively static other than major events a couple of times per year. So – perhaps not necessary.

I think what was sad was having the source code open and issue queue open, but then basically ignoring community input, especially as we spent years begging them to help update it.

Having an actual site for the foundation would be awesome, too – like at `foundation.ethereum.org` or `/foundation`.

The Drupal site has a link to the trademark policy – which seems like it would be useful.

How to pay everyone: I mean, hire people? If it’s an EF owned property, it’s going to need at least one full time person doing content and answering questions around it, plus web dev as needed for maintenance.

Credit work: github commits. But not necessary at all if it is a landing-page style site, that’s just distracting.

I loved Aya’s talk at DevCon4, with the concept of the constellation or galaxy – this is probably a good start for target users (HOWEVER – nothing here about core governance or implementation, just researchers).

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/1/1e918500a5ab0282b24ac3fe646435aa96d8923c_2_690x386.jpeg)1756×984 327 KB](https://ethereum-magicians.org/uploads/default/1e918500a5ab0282b24ac3fe646435aa96d8923c)

---

In looking at other subdomains of EthereumDotOrg, I found a bunch of other stuff. Like, the footer of the [blog](https://blog.ethereum.org/) links to the [LinkedIn profile of some dude in Calgary](https://linkedin.com/in/ethereum) – it’s a Jekyll blog, but I have no idea who to contact about that other than to tweet at maybe Hudson and/or Virgil.

---

**fubuloubu** (2019-02-20):

I do think since it is the EF’s site, then it’s theirs to do with what they want in terms of content. In my mind however, the EF is (or should be) an open community resource, and help point to awesome community projects for different focus groups to get the information they require in it’s own self-sufficient format (i.e. the information gets updated and corrected because someone is incentivized to do so).

EF has power here to legitimize some projects and delegitimize others, I don’t think there’s any getting away from that, so the idea is just embrace it in light terms: where do I go to download clients (geth and parity pages, others), where do I go to learn about research (ethresearch) and engineering proposals (FEM?), where do I go to learn more about Ethereum (wiki and ethhub?), Where do I go to learn more about how to develop on Ethereum (I can’t think of a good central resource for this yet, but several have been proposed).

---

**lrettig** (2019-03-27):

I just posted a Twitter thread with my thoughts:

https://twitter.com/lrettig/status/1110515675678867456?s=20

Some people have begun to contribute to a new initiative here: https://github.com/ethereum-dot-org

