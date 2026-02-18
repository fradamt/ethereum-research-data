---
source: ethresearch
topic_id: 4929
title: Historical Chart for the Minting of any ERC20 token
author: adrien-be
date: "2019-02-02"
category: Data Science
tags: []
url: https://ethresear.ch/t/historical-chart-for-the-minting-of-any-erc20-token/4929
views: 2654
likes: 1
posts_count: 4
---

# Historical Chart for the Minting of any ERC20 token

I’m trying to find out if there is any tool out there that can provide me a chart where I can see the minting of any ERC20 token over time.

Thanks!

## Replies

**d-ontmindme** (2019-04-09):

This could be created using BigQuery by checking for contract creations of contracts with the ERC20 Function Signatures.


      ![](https://ethresear.ch/uploads/default/original/3X/0/4/04470a180329d5f8c5853638d1c9c7acc01fa381.png)

      [Google Cloud Blog](https://cloud.google.com/blog/products/data-analytics/ethereum-bigquery-public-dataset-smart-contract-analytics)



    ![](https://ethresear.ch/uploads/default/optimized/2X/1/10068072379455c7f46c42accf5af10ec16a8ebe_2_690x382.png)

###










Alternatively on eth.events: [https://eth.events](https://eth.events/)

---

**admazzola** (2019-04-10):

This is an open source token minting tracker you can rip code from, just inspect source and steal the JS or go to the github page via the github icon link ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

[0xBitcoin Statistics](https://0x1d00ffff.github.io/0xBTC-Stats/?page=stats&amp);

Its made for a token that is literally MINED but could work for any events that are logged such as those for normal MINTING by a centralized token monarch of course.  Usually ppl don’t build tools for that though because there is no reason to, for those projects.

---

**lane** (2019-04-28):

This is something that I’m pretty sure could be accomplished using The Graph, cf. https://github.com/graphprotocol/graph-node/blob/876ecab190ca54c8b3ec8552334c2d358344caad/docs/getting-started.md. Probably better for ongoing, production-style uses cases than for a one-off query.

