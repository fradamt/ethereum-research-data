---
source: magicians
topic_id: 9667
title: Low-level transaction URLs, like EIP-681 but with binary data
author: php4fan
date: "2022-06-18"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/low-level-transaction-urls-like-eip-681-but-with-binary-data/9667
views: 580
likes: 0
posts_count: 1
---

# Low-level transaction URLs, like EIP-681 but with binary data

If I want to request a transaction to a given contract address, on a given network, with a given value (i.e. amount of currency), calling a given function with a given set of parameters, EIP-681 defines how to build a URL for that transaction.

But say I have the encoded binary data. That is, I want to make do a transaction to a given contract address, with a given value, and given hex data.

That doesn’t seem to be possible with EIP-681. That seems to me a huge design flaw in the EIP itself, or is there a different EIP with a different url schema for that?
