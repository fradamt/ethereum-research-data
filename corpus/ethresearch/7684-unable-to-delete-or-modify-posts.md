---
source: ethresearch
topic_id: 7684
title: Unable to delete or modify posts
author: q
date: "2020-07-14"
category: Administrivia
tags: []
url: https://ethresear.ch/t/unable-to-delete-or-modify-posts/7684
views: 2603
likes: 3
posts_count: 4
---

# Unable to delete or modify posts

The title says it all, I’m unable to delete or modify posts. I’m not sure whether this is intentional but especially for posts that contain information that might need to be appended with new insights, this is kind of annoying and difficult to maintain without losing track of all the changes and updates.

## Replies

**hwwhww** (2020-07-14):

Hey Afri,

We were using  the default setting of:

- post edit time limit (A tl0 or tl1 author can edit their post for (n) minutes after posting): 1440
- tl2 post edit time limit: tl2 post edit time limit: 43200
- editing grace period max diff (Maximum number of character changes allowed in editing grace period, if more changed store another post revision (trust level 0 and 1)): 100
- editing grace period max diff high trust: 300

I just changed them to

- post edit time limit (A tl0 or tl1 author can edit their post for (n) minutes after posting): 4096
- tl2 post edit time limit: tl2 post edit time limit: forever
- editing grace period max diff (Maximum number of character changes allowed in editing grace period, if more changed store another post revision (trust level 0 and 1)): 256
- editing grace period max diff high trust: 1024

I also granted you tl2 member trust level.

Let me know if you are still unable to edit or delete your post.

Thanks.

---

**q** (2020-07-17):

Thanks! 20 Characters!

---

**x** (2021-10-22):

Seems it’s still an issue … I delete my post and it shows `(deleted)` for 300ms and then it goes back to what it was before.

However, the “delete” button is gone and I only see a “restore button”. (Despite the post still being visible to me.)

