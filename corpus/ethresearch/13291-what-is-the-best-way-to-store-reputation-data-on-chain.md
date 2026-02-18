---
source: ethresearch
topic_id: 13291
title: What is the best way to store reputation data on-chain?
author: mmurthy
date: "2022-08-08"
category: Applications
tags: []
url: https://ethresear.ch/t/what-is-the-best-way-to-store-reputation-data-on-chain/13291
views: 1727
likes: 1
posts_count: 3
---

# What is the best way to store reputation data on-chain?

We are building a [reputation system for DAO contributors](https://www.showkarma.xyz) and the way we do is by aggregating all the contributor activity across on-chain and off-chain systems and then quantify it into a reputation score. We want to put this score along with aggregated data on-chain. What is the best way to put this on-chain?

I was thinking of putting it all on IPFS and then storing a hash on chain but I recently came across Vitalik’s post [Where to use a blockchain in non-financial applications?](https://vitalik.ca/general/2022/06/12/nonfin.html), specifically

```auto
Attestations and access permissions. Especially if the data being stored is less than a few hundred bytes long, it might be more convenient to store the data on-chain than put the hash on-chain and the data off-chain.
```

There are lot of benefits in our case to store this aggregated reputation data on-chain.

My question is, what is the best way to write this data so it’s cheaper to store and update it? Are there best practices, techniques or optimizations I can do to implement this in a contract.

## Replies

**qzhodl** (2022-08-09):

Hi mmurthy, what is benefit of storing this reputation data on-chain instead of a hash of it, it would be nice to share more details of the consideration.

---

**mmurthy** (2022-08-09):

If everything is on-chain, other contracts can read it and leverage this reputation data. Example, you can assign voting power for governance directly based on this data, there are use cases where you can stake your reputation to do X and so on.

