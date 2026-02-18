---
source: ethresearch
topic_id: 18663
title: Simple decentralized names with proof-of elapsed time?
author: Uptrenda
date: "2024-02-13"
category: Applications
tags: []
url: https://ethresear.ch/t/simple-decentralized-names-with-proof-of-elapsed-time/18663
views: 1129
likes: 0
posts_count: 4
---

# Simple decentralized names with proof-of elapsed time?

I remember a while back reading a paper I think about Hyperledger and ‘proof-of-elapsed’ time. The idea was something like using trusted processor features to create the holy grail of verifiable delay functions: creating a function that verifiably runs for exactly the amount of time it says it has. Independent of any advances to hardware speeds. It obviously relies on the security of the trusted hardware features – be it enclaves or the AMD equivalent. But its an interesting concept… which got me thinking:

Registering a ‘name’ is basically just the earliest possible point in time that a name existed. If you want to prove who really ‘owns’ a name, then you just need to prove how long a person has ran a VDF on that name for. The longest run-time is accepted as the owner. The downside to this is that you can’t transfer names. But not every use-case needs transferable property records. On the other hand: if you adopt this scheme there’s some pretty massive benefits to it.

You actually don’t need any kind of ledger, database, or key-value system for this to function. Records can be completely distributed among peers since their validity is inherently verifiable (subject to an optional refutation protocol.) So that makes the name system highly scalable over a blockchain-based consensus system like ENS that needs history chains to function. All such existing name systems either rely on a centralized server (which costs money) or need coins to use them. This idea could be adopted p2p without the need for dedicated servers to maintain the naming system. Although the peers would need to keep their ‘clocks’ running inside the enclave – potentially something that can be outsourced if longer-term names are required.

I see this being a good use-case for quick named addresses in peer-to-peer applications. Where you want to use addresses in applications with friends instead of dealing with large scale IPs and meta-data.

## Replies

**MicahZoltu** (2024-02-14):

While a well designed VDF runs in the same order of magnitude across multiple machines, it isn’t precise.  This means that someone running a VDF on their laptop will be “passed up” eventually by someone running a VDF on an overclocked ASIC.

---

**Uptrenda** (2024-02-14):

Yes, I don’t mean to imply using a real VDF for this. The idea of ‘proof-of-elapsed time’ is its a proof from a specific program that vouches for run time using trusted computing. This relies on the security of hardware features. So it could be defeated if someone is able to infiltrate the measures within that hardware protection. I suppose you could always combine trusted computing bases across AMD, Amazon Nitro, Intel SGX, even phone, and smart cards – it would be very hard to bypass all of them.

---

**MicahZoltu** (2024-02-14):

Blockchains are already decentralized timestamping services that are much more robust against attack than things like trusted computing.  Seems like the best solution is to just use one of those, but at that point you basically have ENS.

