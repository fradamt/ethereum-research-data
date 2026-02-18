---
source: ethresearch
topic_id: 18183
title: Trust-minimised DNS oracle based on ZK TLS verification
author: alexhook
date: "2024-01-07"
category: Applications
tags: []
url: https://ethresear.ch/t/trust-minimised-dns-oracle-based-on-zk-tls-verification/18183
views: 1748
likes: 2
posts_count: 2
---

# Trust-minimised DNS oracle based on ZK TLS verification

*This paper contains factual mistakes and will be edited soon*

## Replies

**yush_g** (2024-01-07):

Hey, its great to see more excitement around the best ways to relay DNS on chain! We agree it is a key piece of critical infrastructure for much of the web2 to web3 verification.

However, your proposal seems to rely on this statement: “The party using the certificates (usually just the server, but the client can use them too) also signs its messages with the key whose public key is set in the certificate.”, but i dont see any such signatures mentioned in RFC 7858 ([RFC 7858 - Specification for DNS over Transport Layer Security (TLS)](https://datatracker.ietf.org/doc/html/rfc7858#section-3.3)). Can you provide information on where you found this information? Without this signature, this protocol is no better than [trusting a notary to relay the TLS result, as TLS by default is unsigned](https://blog.aayushg.com/zkemail/#fn:1).

Edit: Unfortunately DNS over TLS is unsigned, as is [DNSCrypt](https://github.com/DNSCrypt/dnscrypt-protocol/blob/afa8157f690bf53bd46da9926a7ef772b81962d1/DNSCRYPT-V2-PROTOCOL.txt).

Most other approaches to DNS verification on chain require either bootstrapping a new network or economic security via global consensus via [staking or other protocols/consensus mechanisms](https://blog.aayushg.com/zkemail/#fn:2).

