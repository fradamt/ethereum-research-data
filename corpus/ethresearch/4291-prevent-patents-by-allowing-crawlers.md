---
source: ethresearch
topic_id: 4291
title: Prevent patents by allowing crawlers
author: DennisPeterson
date: "2018-11-17"
category: Administrivia
tags: []
url: https://ethresear.ch/t/prevent-patents-by-allowing-crawlers/4291
views: 2451
likes: 8
posts_count: 6
---

# Prevent patents by allowing crawlers

One way to help protect against software patents is to make sure posts are stored in Internet Archive, thus giving a reliable publish date. I just attempted to do that with a post, and it didn’t work because they won’t save anything that has a robot.txt prohibiting web crawlers.

Would it be possible to modify robot.txt?

## Replies

**dlubarov** (2018-11-17):

The robots.txt looks fine to me; IA’s crawler should be able to discover and archive any topic pages it likes. It looks like IA’s crawler just hasn’t decided to archive very many topic pages, for whatever reason, but there are some. Here’s an [example](https://web.archive.org/web/20181030070237/https://ethresear.ch/t/explanation-of-daicos/465).

If someone representing the website could email [info@archive.org](mailto:info@archive.org), maybe they could adjust some configuration to make their crawler more likely to archive all the topics here.

Edit: I tried requesting that IA archive a topic page through their web UI, and IA did archive it ([link](https://web.archive.org/web/20181117204721/https://ethresear.ch/t/poc-implementation-of-plasma-evm/3958)), but the server didn’t give it the actual content of the topic; instead it returned “Oops! That page doesn’t exist or is private.” Might be a bug in Discourse? Or it could be some intentional bot blocking code within Discourse, possibly with a rate limit that IA’s crawler sometimes exceeds.

---

**DennisPeterson** (2018-11-17):

Interesting. On one request I got a message about robots.txt but on several other attempts I got the same message you did.

---

**DZack** (2018-12-20):

I can think of another place to store posts for future “proof of publish date”

(or hashes of posts, anyway)

![:blush:](https://ethresear.ch/images/emoji/facebook_messenger/blush.png?v=9)

---

**DZack** (2018-12-21):

…but actually tho, if we can just get posts in a standard/ plaintext format, say once a week, hashing them, storing the hash on Eth, and hosting the content (IPFS, or even just have a few redundant copies hosted somewhere) could be a neat project, and a nice illustration of an easy use-case.

---

**virgil** (2018-12-21):

I will ask my colleagues at [archive.org](http://archive.org) to look at this.

