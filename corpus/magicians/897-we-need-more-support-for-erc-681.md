---
source: magicians
topic_id: 897
title: We need more support for ERC-681!
author: ligi
date: "2018-07-30"
category: Web > User Experience
tags: [erc-681]
url: https://ethereum-magicians.org/t/we-need-more-support-for-erc-681/897
views: 3062
likes: 7
posts_count: 7
---

# We need more support for ERC-681!

Alarmed by this tweet: https://twitter.com/Mesqueeb/status/1023714054492147712 I checked some wallets for ERC-681 support. Unfortunately it does not yet look as good as I hoped (https://twitter.com/wallethapp/status/1023856148041134080). Would be great to get more support for it. Also please test with wallets you know - would be great to get more data-points on this.

## Replies

**boris** (2018-07-30):

For reference, ERC 681:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png)[ERC-681: Representing various transactions as URLs](https://ethereum-magicians.org/t/erc-681-representing-various-transactions-as-urls/650/1)

> A standard way of representing various transactions, especially payment requests in Ether and ERC20 tokens as URLs.

Maybe a Wiki Page with wallets that support it?

---

**ligi** (2018-07-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Maybe a Wiki Page with wallets that support it?

Yes - I am working on this. But realized fast that this will be hell to edit in a table of github wiki page. Will make a extra repository that creates this table from json files.

The matrix should not only contain support of ERC-681 - but more ERCs and I also want to split ERC functions (e.g. ERC-681 value payload detection, ERC-681 function detection support, … )

---

**ligi** (2018-08-02):

More reasons why we need more support: https://github.com/walleth/walleth/issues/266

anyone has contacts to developers at BRD wallet or jaxx?

---

**ligi** (2018-08-03):

good news - jaxx answered on twitter that they will care for it. Trust mentioned in a github issue they will care for it. So I think ondly this BRD wallet is missing …

---

**ligi** (2018-08-08):

Just tested with enjin which is also quite large. Unfortunately they are also going off-standard - their ERC-681 looks like this:

`ethereum:0x2E9F06153Ce4bf5cCE30bf18C1BA1899B50A18Ea?token=ETH`

dropped them a mail and invited them to the ring - perhaps it would be good if more people write mails like this. They might ignore a single mail - but they cannot ignore us all ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

[support@enjin.com](mailto:support@enjin.com)

---

**goranjovic** (2018-10-31):

Speaking for Status here. We only have a partial support for eip-681 or in other words, we don’t quite support it at the moment but definitely intend to and have it on our roadmap.

So, to avoid any confusion, we’ll definitely be adding support for this.

