---
source: magicians
topic_id: 27375
title: EIP/ERC Website Migration (Jekyll -> Zola)
author: SamWilsn
date: "2026-01-02"
category: Magicians > Process Improvement
tags: [erc, eip, eip-process]
url: https://ethereum-magicians.org/t/eip-erc-website-migration-jekyll-zola/27375
views: 59
likes: 6
posts_count: 5
---

# EIP/ERC Website Migration (Jekyll -> Zola)

A thread for questions/comments/discussion about a possible migration from Jekyll to Zola for rendering the EIPs/ERCs websites. See [preprocessor/MIGRATION.md at master · eips-wg/preprocessor · GitHub](https://github.com/eips-wg/preprocessor/blob/master/MIGRATION.md) for more details.

There’s a preview (that’s occasionally up to date) here: [Ethereum Improvement Proposals](https://eips-wg.github.io/EIPs/)

## Replies

**gballet** (2026-01-03):

Is there any technical advantage to do this? Reading the linked page, nothing is really obvious, save the burden of having to learn another process. It ain’t broken, don’t fix it.

---

**abcoathup** (2026-01-04):

What is the reasoning behind the proposed migration?

Is there a proposed timeline?

---

**SamWilsn** (2026-01-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png) gballet:

> Is there any technical advantage to do this?

The system we have now is fairly brittle, and doesn’t handle cross-repository linting at all. A ton of our automated checks have been turned off since the EIP/ERC split.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png) gballet:

> Reading the linked page, nothing is really obvious

It’s mostly a placeholder for the time being. Nothing has been decided yet.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png) gballet:

> save the burden of having to learn another process

If all goes to plan, unless you’re building locally, the only change you’ll notice is the paths for links.

If you are building locally, I’ll have some better documentation before then.

---

**SamWilsn** (2026-01-04):

No Editor is familiar with Ruby, and there are some serious structural issues with how our build works.

As for a timeline, nothing has been decided. We haven’t even agreed on going through with this.

As the champion of this endeavor, this discussion thread and pull request are mostly to get my ass in gear ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=15)

