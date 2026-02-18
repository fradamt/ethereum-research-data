---
source: magicians
topic_id: 6994
title: Improve syncing RPC call
author: ligi
date: "2021-09-02"
category: Uncategorized
tags: [json-rpc]
url: https://ethereum-magicians.org/t/improve-syncing-rpc-call/6994
views: 872
likes: 2
posts_count: 1
---

# Improve syncing RPC call

Inspired by this geth issue: [Expose State Sync ETA in eth.syncing · Issue #23448 · ethereum/go-ethereum · GitHub](https://github.com/ethereum/go-ethereum/issues/23448) we where thinking about improving the output of eth_syncing.

currently this is the reply as defined in the [execution-apis spec](https://github.com/ethereum/execution-apis/blob/37d67680e6d2171e2b1ceb738b324d1386d9b5bc/src/schemas/client.json):

```json
"oneOf": [
			{
				"title": "Syncing progress",
				"type": "object",
				"properties": {
					"startingBlock": {
						"title": "Starting block",
						"$ref": "#/components/schemas/uint"
					},
					"currentBlock": {
						"title": "Current block",
						"$ref": "#/components/schemas/uint"
					},
					"highestBlock": {
						"title": "Highest block",
						"$ref": "#/components/schemas/uint"
					}
				}
			},
			{
				"title": "Not syncing",
				"description": "Should always return false if not syncing.",
				"type": "boolean"
			}
		]
```

I think the case of “Not syncing” is good but in the case of syncing we should expose some more information.

Geth already adds knownStates and pulledStates - unfortunately this is not standardized yet.

In this process we should also add the sync method as e.g. with snap-sync you can give a better estimate of the progress than with full-sync.
