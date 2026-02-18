---
source: magicians
topic_id: 2392
title: Standardizing output from RPC's across nodes
author: ankitchiplunkar
date: "2019-01-11"
category: Working Groups > Data Ring
tags: [json-rpc]
url: https://ethereum-magicians.org/t/standardizing-output-from-rpcs-across-nodes/2392
views: 1110
likes: 1
posts_count: 4
---

# Standardizing output from RPC's across nodes

Hi all,

I am Ankit Chiplunkar I currently work at https://www.tokenanalyst.io/ and earlier developed [GitHub - analyseether/ether_sql: A python library to push ethereum blockchain data into an sql database.](https://github.com/analyseether/ether_sql). Posting here on the suggestion of [@tjayrush](/u/tjayrush) .

We collect, clean and format all types of data gathered from Ethereum clients, and regularly fall into problems where different nodes return different types. We have written a few blogs and opened several PR’s on the issue, but I think this ring can be a good place to standardize the data returned from Ethereum clients.

What do you guys think?

References:

**Blogs:**

https://medium.com/tokenanalyst/weird-quirks-we-found-in-ethereum-nodes-d5dcbad0c86

https://medium.com/tokenanalyst/towards-production-grade-open-source-ethereum-nodes-6ef2e9458fb4

**PR’s**

1. GitHub · Where software is built
2. GitHub · Where software is built

## Replies

**tjayrush** (2019-01-13):

Hey Ankit. Thanks for posting this.

Summary of findings from the above article **[with my comments]**:

- Use an SSD. [Confirmed]
- Parity RPC responds even while syncing, Geth does not. [Not confirmed]
- There is no standard error reporting from the nodes. Different nodes report errors in different ways. [Confirmed]
- ‘r’, ‘s’, and ‘v’ fields differ between clients. [Not confirmed]
- Parity syncs faster than Geth. [Believed to be true]
- JSON-RPC interface is not type-safe. [Is any JSON type safe?]
- Tracing and state diff appear only in Parity (not Geth) and then with some inconsistancies. [Not confirmed]
- RPC and Web socket interfaces handle block re-orgs. There’s a question if they are correctly handled. [Not confirmed]
- Small differences between Geth and Parity: [Not confirmed]

Uncle size is null in Parity, but does exist in Geth.
- Filter IDs on Geth and Parity are different.
- Geth assigns random IDs, and Parity uses an incremental counter.

The consensus rules among clients have to match in order to make Ethereum work, but everything else, e.g. the exposed API, or RPC interface can be totally different. **[Should be the same but are possibly different]**

Take each client with a grain of salt. **[Confirmed]**

---

**jpzk** (2019-01-14):

Hey tjayrush,

Thanks for checking on the findings, when you write “Not confirmed” do you mean a) you are going to evaluate it or b) you evaluated it and you did confirm that this issue exists.

Best,

Jendrik

---

**tjayrush** (2019-02-08):

[@jpzk](/u/jpzk) When I say ‘not confirmed’ above I meant that I did not independently test the claim made by Ankit. In other words, I don’t know if it right or wrong.

