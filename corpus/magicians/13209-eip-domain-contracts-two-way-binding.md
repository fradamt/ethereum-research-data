---
source: magicians
topic_id: 13209
title: "EIP: Domain-contracts two-way binding"
author: web3panther
date: "2023-03-07"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-domain-contracts-two-way-binding/13209
views: 740
likes: 0
posts_count: 3
---

# EIP: Domain-contracts two-way binding

This EIP proposes a standard way for dapps to maintain their official domains and contracts that are linked through an on-chain and off-chain two-way binding mechanism.

**Motivation**

Web3 users sometimes get attacked due to vulnerebilities in web2 systems. For example, in Nov 2022, [Curve.fi](http://Curve.fi) suffered a DNS attack. This attack would have been prevented if there was a standard way to allow dapp developers to disclose their official contracts. If this was possible, wallets could have easily detected un-official contracts and warned users.

An added advantage to this approach is to predictably find the the official contract addresses of a dapp. Most dapp’s docs are non-standard and it is difficult to find the official contract addresses.

More details: [eip draft](https://github.com/VenkatTeja/EIPs/blob/master/eip-domain-contracts-binding.md)

This is work in progress. Sharing to get community opinion.

## Replies

**SamWilsn** (2023-09-13):

I might suggest using the [/.well-known/](https://en.wikipedia.org/wiki/Well-known_URI) prefix for the path on the domain. Several other services already use that directory for fixed-location information files and it might make sense here too.

---

**SamWilsn** (2023-10-30):

> Is there a call I can present this? Like a community call?

We have biweekly EIP Editing Office Hours. The next one is tomorrow, October 31st at 11am ET (3pm UTC.)

> I have written decent amount of explanations in comments here but I don’t understand how its still unclear.

Is there only ever one `DomainContractRegistry` deployed? Like there’s one canonical `DomainContractRegistry` that holds the mapping for all dapps? If so, you should mention that explicitly in the proposal.

Further, how do you prevent sniping? If I were an attacker, couldn’t I register a DRC for `app.uniswap.org` immediately and block the actual uniswap developers? A comment that says “use chainlink” is somewhat inappropriate for an EIP.

That’s why I mentioned DNSSEC. With that, you can prove ownership of the domain, and the validity of TXT records on it, using the same chain of trust that browsers use to resolve the domain in the first place. You don’t need a third party to accomplish it.

