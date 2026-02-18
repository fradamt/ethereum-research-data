---
source: magicians
topic_id: 20810
title: Annotated EIPs - Concept Feedback
author: samuelemarro
date: "2024-08-15"
category: Magicians > Process Improvement
tags: [education]
url: https://ethereum-magicians.org/t/annotated-eips-concept-feedback/20810
views: 103
likes: 7
posts_count: 7
---

# Annotated EIPs - Concept Feedback

TL;DR: A website where endorsed users can annotate EIPs can fill the knowledge gap between the standard and the actual “know-how”

Hello Magicians,

I’ve been thinking recently about the gap between the content of EIPs and the actual knowledge required to fully understand and implement them.

Related EIPs, gold-standard implementations, existing projects, common implementation pitfalls: all of this information, while beyond the scope of EIPs, is still extremely important for understanding them. Think reading EIP-1559 without knowing Roughgarden’s paper, EIP-1155 without OpenZeppelin’s reference implementations, or EIP-721 without its various extension EIPs.

Sure, we have threads on this forum, discussions on PRs and lots of blogs/Twitter threads, but none of this information is structured and/or specific, i.e. a comment on a specific line of an EIP might be buried among other discussions and be generally hard to find. Adding this information to the EIP itself is not feasible either, since a) the line between opinions and factual information can be fuzzy, and EIPs tend to err on the side of caution b) the process to update an EIP requires several checks and discussions, which is way too much effort for a single comment or off-hand reference.

For this reason, I was brainstorming about a website where endorsed users (see below) can add annotations to EIPs in the form of comments, while everyone else can upvote/downvote them. These can be either structured (e.g. standard templates for “Compare with EIP X”, “Platform X uses this EIP”, “See X for an in-depth analysis”, “Be careful of X while implementing this EIP”, which can be machine-readable) or free-form. The annotations can refer to the EIP as a whole or to specific parts of it.

To avoid spam/malicious annotations, I’m taking inspiration from arXiv’s endorsement system. In particular:

- All EIP authors and core contributors are automatically endorsed
- Endorsed users can endorse n other users
- Non-endorsers users can petition to be manually endorsed

What do you think? Would you find this useful for the ecosystem? Any problems/pitfalls you might foresee? Any useful applications?

## Replies

**matt** (2024-08-15):

It’s an interesting idea. The challenging part is getting the endorsements right and then surfacing the useful discussions. I’m not sure how to best do this or what the end value will be in such a platform, but it would be interesting to see.

I’m afraid there isn’t quite enough demand for such a solution.

---

**samuelemarro** (2024-08-15):

Thanks for the feedback! One thing I’ve been thinking about, especially in terms of demand vs supply, is that the people quite comfortable with EIPs are also the people who don’t really need annotated EIPs, since they already need to be familiar with the literature in order to author a standard. The two most likely cases would be in my opinion:

- Out-of-domain expertise, e.g. you’re very familiar with NFT EIPs but not consensus-level EIPs, which means you can contribute to the former and learn new things about the latter
- Unknown unknowns: if some EIPs rely on a lot of “folk knowledge”, it can be easy to work in an area without stumbling upon certain facts or connections. Having all common knowledge in a single place helps with that

Plus, of course, the benefits for new devs starting out, for whom a lot of information is inaccessible.

In any case, thanks for your feedback! I’ll look into how some of these issues might be addressed.

---

**abcoathup** (2024-08-16):

Eth Magicians [wiki posts](https://meta.discourse.org/t/editing-and-creating-wiki-posts/30801) may be one way to solve this, with some restriction on what user [trust level](https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/) can edit.

There still may be contention which may require moderation and any wiki has potential for vandalism.

Alternatively an append only topic may be better.

Ideally using something off the shelf (especially using the existing Discourse forum) would be fastest.

---

[EIP.tools](https://eip.tools) has been experimenting quickly, adding a GPT summary of an EIP/RIP/ERC for increasing quick understanding.

---

**eawosika** (2024-08-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samuelemarro/48/6309_2.png) samuelemarro:

> I’ve been thinking recently about the gap between the content of EIPs and the actual knowledge required to fully understand and implement them.

This is precisely why I started [eips.wiki](https://eips.wiki/). This [brain dump](https://eipswiki.notion.site/Meta-Creating-a-Wiki-pedia-for-EIPs-1a0a438c1dda496e895e8d938c78bbd5?pvs=4) goes into more details, but the reasoning is familiar. I was going to write up a post after we created a website but never got around to doing it.

EIP Wiki articles (at least the better ones) provide an explanation of the EIP specification and are meant to complement the EIPs For Nerds series. Here’s an example of an EIP Wiki article on EIP-3675: [EIP-3675 | 2077's EIP Wiki](https://eips.wiki/eips/protocol/consensus/eip-3675/). Here’s an example of an EIPs For Nerds article (see [here](https://hackmd.io/@emmanuel-awosika/Introducing-EIPs-For-Nerds) for a discussion of the rationale): [EIPs for Nerds #8: EIP-7685 (General Purpose Execution Requests)](https://research.2077.xyz/eips-for-nerds-8-eip-7685)

Can you look through and let me know what you think? We recently had an internal conversation and a few team members questioned if people actually wanted this. Glad I stumbled on this post and I can ask for feedback. Cc: @lightclient [@matt](/u/matt) [@abcoathup](/u/abcoathup)

---

**eawosika** (2024-08-28):

EIP Tools is great, and I’ve considered deprecating [eips.wiki](https://eips.wiki/) since that exists. But one of the original reasons for starting the project (see some musings [here](https://eipswiki.notion.site/Meta-Creating-a-Wiki-pedia-for-EIPs-1a0a438c1dda496e895e8d938c78bbd5?pvs=4)) was to provide the same level of structure as you’ll find on [eips.ethereum.org](http://eips.ethereum.org).

So EIP Tools requires knowing which EIP you’re looking for. But I think there’s also the case of people looking for different things (e.g., “all token standards”) and want some information organization. That’s where EIP Wiki is useful: I did a lot to make the categorization meaningful and helpful.

One possible model is to use AI generated summaries + human editors to populate EIP Wiki. People can still use EIP Tools if they want, especially since the information can change faster as the LLM is trained on new information (EIP Wiki would require human editors).

---

**samuelemarro** (2024-08-28):

eips.wiki looks good! The wiki format definitely makes sense for this type of thing. First impressions/feedback:

- Good design, and having a categorized list of EIPs is very nice on its own
- You should consider adding a visual way to distinguish between EIPs that have a wiki page and those that don’t. I’d also recommend adding some sort of meta-page with the list of current pages on the wiki
- The link “Contribute to the EIPwiki” actually links to the Rollup Improvements Proposal page

I’d also recommend avoiding LLM-written content. The point of a wiki is to provide very accurate information; since LLMs tend to make a lot of mistakes (especially on high-level, non-trivial stuff), there’s a risk that very few people would trust the content of the wiki. Sure, humans can make mistakes as well, but there’s usually a correlation between the tone/quality of writing and the correctness of content; LLMs tend to make egregious mistakes while using a very formal and academic style.

