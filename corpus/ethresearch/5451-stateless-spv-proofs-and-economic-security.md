---
source: ethresearch
topic_id: 5451
title: Stateless SPV Proofs and economic security
author: liamzebedee
date: "2019-05-14"
category: Security
tags: []
url: https://ethresear.ch/t/stateless-spv-proofs-and-economic-security/5451
views: 2491
likes: 0
posts_count: 1
---

# Stateless SPV Proofs and economic security

Stateless SPV proofs ([original talk](https://youtu.be/njGSFAOz7F8?t=555) and [slides](https://docs.google.com/presentation/d/1HZ9TSaVjqkf9QAkdBA3hXNNl1ai0gz4OvigWycVk3ak/edit#slide=id.g525e62c02c_0_2)) are an interesting solution from James Prestwich of Summa, to the problem of btcrelay’s incentive incompatibility .

To quote from the btcrelay repo:

> “the hurdle is when BTC Relay is generating “revenue”, then relayers will want a piece for it and will continue relaying, but to get “revenue” BTC Relay needs to be current with the Bitcoin blockchain and needs the relayers first”

### How it works

(taken from [ZBTC](https://docs.google.com/document/d/1sjdZB78hy5NgFdzsbjzwwX9RKKbh3rvRcyjKfqavDoM/edit#))

Stateless SPV approximates the finality of a transaction based on its accumulated difficulty. Instead of verifying and storing all block headers to date, we compute the cumulative difficulty of a set of headers. As long as the oldest header includes the transaction, and each following header builds upon the last, we can approximate the economic cost to making a fraudulent transaction. The current Bitcoin difficulty, multiplied out by six blocks, can be an approximate cost of Bitcoin’s transaction finality. As there is not much material out yet (it was introduced in March 2019), pseudocode below is included to explain better:

```python
def work(header):
	"""Returns CPU work expended in a block header"""
	assert hash(header) >= header.difficulty
	return header.difficulty

def cumulative_work(header):
	if header.prev_block:
		return work(header) + work(header.prev_block)

	return work(header)

def longest_chain(head1, head2):
	"""Determines which head refers to the longest chain of CPU work"""
	if cumulative_work(head1) > cumulative_work(head2):
		return head1
	else:
		return head2
```

This approach is rather bespoke - due to the simplicity of Bitcoin’s consensus algorithm, and the network effect of its hashpower, stateless SPV is seemingly secure. If the hashpower were lower, it would be vastly more vulnerable to attacks.

### Application to cross-chain proofs

Stateless SPV is a nice approximation on the economic finality of a transaction. It’s only useful for simple Nakamoto consensus for now, but if we can produce a succinct ZK proof of Ethash, it could be an interesting approach to proving state on other chains (Cosmos for example) **without trusted relayers**.
