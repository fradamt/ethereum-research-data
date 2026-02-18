---
source: ethresearch
topic_id: 7448
title: "Comparing discovery advertisement features by efficiency: ENR attributes and topic advertisement"
author: zilm
date: "2020-05-20"
category: Networking
tags: []
url: https://ethresear.ch/t/comparing-discovery-advertisement-features-by-efficiency-enr-attributes-and-topic-advertisement/7448
views: 2567
likes: 2
posts_count: 1
---

# Comparing discovery advertisement features by efficiency: ENR attributes and topic advertisement

Ongoing development of the Ethereum network, both 1.x and 2.0 requires specialization of peers and introducing a set of different peer roles and responsibilities. In order to make appropriate peers easily discoverable, several techniques were suggested, but most promising are topic advertisements in Discovery V5 and ENR attributes. By choosing several metrics to draw up a complete picture of advertisement efficiency and testing selected advertisement solutions in the simulator we were able to compare it.

Our analysis shows that in most cases ENR serves better than topic advertisement, especially when the advertiser wants to support an advertisement in the long run. Measurement of time and traffic spent by an advertiser shows that topic advertisement consumes 150 times more traffic during 24 hours. Moreover, measurement of time and traffic spent by the media stacked with advertiser metrics shows that overall network efforts spent on advertisement measured in steps of peer action is almost 25 times higher in case of using topic advertisement.

In order to improve search time and reduce traffic for ENR attribute, make possible to find even smaller attributed fractions in network in small time and decrease traffic in all ENR search cases, following Discovery V5 API is proposed:

---

### FINDNODEATT Request (0x09)

```
message-data = [request-id, attribute-key, (attribute-value)]
message-type = 0x09
attribute-key = searched ENR attribute key
attribute-value = (optional) searched ENR attribute value for provided key
```

FINDNODEATT queries for nodes with non-null ENR attribute identified by `attribute-key`.

If optional parameter `attribute-value` is provided, only ENRs with `attribute-key == attribute-value` should be returned. Maximum number of returned records is `K-BUCKET`. If more than `K-BUCKET` records are found by search, it is recommended to return a random subset of `K-BUCKET` size from it.

---

Let’s see how it will work 64 nodes advertised in 10,000 peers network: we got 1.4 seconds on average search and just 3.3 Kb of traffic per searcher!

[![](https://ethresear.ch/uploads/default/optimized/2X/a/a3f96130b84d68655d9f3aad832858eda95738c7_2_690x424.png)1131×696 35.5 KB](https://ethresear.ch/uploads/default/a3f96130b84d68655d9f3aad832858eda95738c7)

The only disadvantage of ENR is distribution speed:

In metric where we measure how fast network gets knowledge about an ad we got following number:

- 50% of network peers knew about ENR change in 2 minutes, under 25% churn rate in 3 minutes
- 80% of network peers got this info in 3.5 minutes, under the same churn - in 11 minutes

It’s not an issue when you serve your role for more than hour and want to be easy discoverable, but you will need time in the beginning for ENR to be distributed.

Above is just a short version of conclusion, [full write-up is here](https://hackmd.io/@zilm/BJGorvHzL)

Thank you
