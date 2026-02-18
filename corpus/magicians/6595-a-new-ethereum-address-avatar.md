---
source: magicians
topic_id: 6595
title: A new Ethereum address Avatar
author: tyevlag
date: "2021-07-04"
category: Magicians > Site Feedback
tags: []
url: https://ethereum-magicians.org/t/a-new-ethereum-address-avatar/6595
views: 827
likes: 2
posts_count: 2
---

# A new Ethereum address Avatar

At present, I know that the existing address avatars are based on certain random rules

For example, two different addresses A and B may have completely different avatars, which are random

When people see a avatar, it’s easy not to know the address of the avatar

Based on this, I think of a more intuitive way to understand the head image information:

[![0xe626E8ca82603e3B44751f8562B5ED126d345140](https://ethereum-magicians.org/uploads/default/original/2X/1/19f257c168e8e9f96ef7fcbf4cef256ac93a257f.png)0xe626E8ca82603e3B44751f8562B5ED126d345140128×128 883 Bytes](https://ethereum-magicians.org/uploads/default/19f257c168e8e9f96ef7fcbf4cef256ac93a257f)

The image is divided into three parts

1. The upper left corner is the text area, showing the first two characters of the address
2. The lower right corner is the text area, showing the end of the address 2 characters
3. The red part is the random area

There are some considerations:

1. The text area may also have random components, but the text content can be clearly seen
2. The random region can be in any way
3. As for ens, there may be more special display methods (for example, the top left corner is the first three characters of the ENS address, and the bottom right corner is a special picture)

Benefits:

Can intuitively know which wallet belongs to from the picture

There may be a ready-made solution, but I don’t know? Please let me know. Thank you

## Replies

**wighawag** (2021-07-10):

I like the idea of adding the first and last 2 characters of an address as part of the address icon.

By the way I built an alternative to the blockie for ethereum address : https://mandalas.eth.link/

Instead of using randomness, it use the address value itself to populate the bitmap, making each mandala completely specified by the address, ensuring no 2 mandalas can be same.

On top of that it repeats the values 8 fold, making easier to visually differentiate 2 mandalas.

The shape of mandalas would accomodate the corner well too.

But blockie while not flawless, are part of ethereum it seems and not sure how to go about using an alternative ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

