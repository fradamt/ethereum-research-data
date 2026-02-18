---
source: magicians
topic_id: 2905
title: "\"BlockCypher’s Ethereum API was knocked out after the St. Petersberg HF\""
author: jpitts
date: "2019-03-12"
category: Working Groups > Data Ring
tags: [education, node-operators]
url: https://ethereum-magicians.org/t/blockcypher-s-ethereum-api-was-knocked-out-after-the-st-petersberg-hf/2905
views: 936
likes: 4
posts_count: 3
---

# "BlockCypher’s Ethereum API was knocked out after the St. Petersberg HF"

cc “Education Ring” ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

Ok, so we have this Twitter discussion and some misconceptions:

https://twitter.com/Catheryne_N/status/1105218247736012800

She experienced sync problems after the HF, and seems to have avoided normal channels for support, and reached out directly to [@vbuterin](/u/vbuterin).

https://blog.blockcypher.com/ethereum-woes-d9b2af62da67

> After examining every which way we could think of to add the Trie state to our Ethereum state, we asked Vitalik for assistance. His first comment to us was “oh you’re one of the few running one of those big, scary nodes.” We asked him if he knew of anyone else running a “big, scary node” to see if we could possibly sync with them. He knew of no one, not even the Ethereum Foundation keeps a full archival copy of the Ethereum chain.

It highlights an education-related issue that I see. We need entry points for users of various kinds so that they know where to start, where to bring problems up. This person does not even seem to be aware of the Data Ring.

## Replies

**tjayrush** (2019-03-13):

There’s a fair amount of misinformation as well. Running an archive node is not that hard. I run two of them IN MY HOUSE (plus two Parity tracing nodes – one on a laptop). It’s not that hard or that scary.

---

**boris** (2019-03-14):

There were sync problems before the HF. Various Twitter responses from knowledgeable devops folks points out they don’t seem to know what they are doing. And, of course, the interaction with VB sounds like a fabrication.

But back to your point – this is a commercial company. I think messaging / education / entry points for commercial companies could be VERY interesting. We want to welcome them and onboard them as open source contributors – or make it clear who they can pay for help.

For example, I wonder if they are running Geth or Parity.

For the Geth team, might they list trusted consultants who do paid work? Who would pay an affiliate fee?

For Parity, they should add a paid support option right in their repo.

