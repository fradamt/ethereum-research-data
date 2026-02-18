---
source: magicians
topic_id: 11183
title: Proposal for adding blockTimestamp to logs object returned by eth_getLogs and related requests
author: wighawag
date: "2022-10-04"
category: Working Groups > Provider Ring
tags: []
url: https://ethereum-magicians.org/t/proposal-for-adding-blocktimestamp-to-logs-object-returned-by-eth-getlogs-and-related-requests/11183
views: 4166
likes: 39
posts_count: 19
---

# Proposal for adding blockTimestamp to logs object returned by eth_getLogs and related requests

# Motivation

Currently, most contract events that act on the notion of time do not add timestamp information as it is already available on the block where the event occurs. This saves them the extra gas cost of adding timestamps to the events.

Unfortunately `eth_getLogs` do not provide the timestamp as part of the log objects returned. And so indexers that fetches these events using `eth_getLogs`, need to make one extra request for each different block to get the timestamps at which these events happen.

This significantly reduces the speed at which such an indexer can compute the state from the events. With an `eth_getLogs` you can get thousands of events and process them but for events that require timestamp information, you indeed currently need to perform thousands of requests more for it.

This is especially difficult for indexers that run in-browsers where each user would have to perform all the extra requests. Also in such an environment, [EIP-1193](https://eips.ethereum.org/EIPS/eip-1193) prevents them from using batch requests, which could have alleviated the issue.

Ideally, the log object returned by `eth_getLogs` would include the block’s timestamp along the block’s hash and number.

# Spec

Here is the spec for `eth_getLogs` with the added `blockTimestamp` field

### eth_getLogs {}

Returns an array of all logs matching a given filter object.

**Parameters**

1. Object - The filter options:

- fromBlock: QUANTITY|TAG - (optional, default: "latest") Integer block number, or "latest" for the last mined block or "pending", "earliest" for not yet mined transactions.
- toBlock: QUANTITY|TAG - (optional, default: "latest") Integer block number, or "latest" for the last mined block or "pending", "earliest" for not yet mined transactions.
- address: DATA|Array, 20 Bytes - (optional) Contract address or a list of addresses from which logs should originate.
- topics: Array of DATA, - (optional) Array of 32 Bytes DATA topics. Topics are order-dependent. Each topic can also be an array of DATA with “or” options.
- blockhash: DATA, 32 Bytes - (optional, future) With the addition of EIP-234, blockHash will be a new filter option which restricts the logs returned to the single block with the 32-byte hash blockHash. Using blockHash is equivalent to fromBlock = toBlock = the block number with hash blockHash. If blockHash is present in in the filter criteria, then neither fromBlock nor toBlock are allowed.

params: [ { topics: [ “0x000000000000000000000000a94f5374fce5edbc8e2a8697c15331677e6ebf0b”, ], }, ]

**Returns**

`Array` - Array of log objects, with following params:

- removed: TAG - true when the log was removed, due to a chain reorganization. false if its a valid log.
- logIndex: QUANTITY - integer of the log index position in the block. null when its pending log.
- transactionIndex: QUANTITY - integer of the transactions index position log was created from. null when its pending log.
- transactionHash: DATA, 32 Bytes - hash of the transactions this log was created from. null when its pending log.
- blockHash: DATA, 32 Bytes - hash of the block where this log was in. null when its pending. null when its pending log.
- blockNumber: QUANTITY - the block number where this log was in. null when its pending. null when its pending log.
- blockTimestamp: QUANTITY - the unix timestamp for when the block where this log was in, was collated. null when its pending. null when its pending log.
- address: DATA, 20 Bytes - address from which this log originated.
- data: DATA - contains one or more 32 Bytes non-indexed arguments of the log.
- topics: Array of DATA - Array of 0 to 4 32 Bytes DATA of indexed log arguments. (In solidity: The first topic is the hash of the signature of the event (e.g. Deposit(address,bytes32,uint256)), except you declared the event with the anonymous specifier.)

Was originally posted  on the [ethereum/execution-apis repo](https://github.com/ethereum/execution-apis/issues/295)

## Replies

**tjayrush** (2022-10-05):

I absolutely, 100% support this issue.

It would speed up our processing when building our index by nearly double.

The shortcoming of `eth_getLogs` came up recently in the Erigon issues ([feature request: add field`timestamp` to `eth_getLogs` response · Issue #4951 · ledgerwatch/erigon · GitHub](https://github.com/ledgerwatch/erigon/issues/4951)). For a short time, it was in `eth_getLogs`, but it was moved to `erigon_getLogs` because they reserve the `eth_` namespace for “standards.” (In other words, there’s already an existing implementation.)

This is a simple win for every RPC user who uses logs and needs timestamps on those logs, as it immediately lessens the number of RPC queries by nearly half.

Such a change is also backwards compatible, since the `timestamp` field didn’t exist in the past, adding it shouldn’t break anything (except possibly some test cases, but those can be easily updated).

---

**aaaaa** (2022-10-05):

adding timestamp to eth_getLogs is a hill i will die on every day of the week

not only does it greatly reduce the speed of client building indices, but also reduces server load since you already have the ts in the block header for your getlogs query.

beyond indices, it would also allow web3 frontends to much easier display historical events with real timestamp instead of just block, which I think would be super benificial for non native user accessibility

---

**dcposch** (2023-08-08):

I was about to make this issue, but it’s already here.

Fundamentally, most eth UIs have to show two things, current state and history (actions taken, transfers sent and received, etc).

For the first, we have `eth_call`. For the second, we have `eth_get[Filter]Logs`. Nearly 100% of the time you are querying logs, you need timestamps to go with them.

(This is also true if it’s an intermediate indexer, rather than a UI directly, that’s doing the querying.) In fact I’m curious to see a real-world use of `eth_getLogs` are that *doesn’t* also up querying block timestamps.

This seems like a nice win:

- Backward compatible (no existing fields removed or modified)
- Self-contained
- Likely a small diff in all node implementations
- Easy to roll out gradually (if some RPC providers/nodes/etc have it and others don’t, no existing code breaks)

---

**bear2525** (2023-09-17):

Is there any workaround for this in order to avoid making hundreds of thousands of RPC calls that can take an infeasibly long amount of time? I’m not looking to get the block timestamp specifically, but other consensus-level data that can be obtained with `getBlockByNumber`.

---

**tjayrush** (2023-09-29):

What ever happened to this obviously useful idea?

---

**iFrostizz** (2024-03-05):

This add would be extremely useful indeed, and this might be a great add as well so that we won’t be bothered by having to make an additional call to get the timestamp but also any information in the block.

For this, we could include an optional bool for the “full block” information that would as well return the information of the block that the event was emitted from.

---

**auryn** (2024-04-17):

+1 for this idea. Super useful.

---

**mattstam** (2024-04-20):

Reth already has this implemented: [feat(rpc): add block timestamp to logs by cairoeth · Pull Request #7606 · paradigmxyz/reth · GitHub](https://github.com/paradigmxyz/reth/pull/7606)

It would be great if the other EL teams could try to do so as well, as this only really works when all RPCs have it.

---

**zergity** (2024-04-22):

+1 support this, some clients and apis already implement it

---

**timolegros.eth** (2024-05-21):

+1 this would be amazing.

---

**Mutinda-Kioko** (2024-08-16):

I agree, currently we have to make 2 rpc calls just to get the timestamp. This would be an amazing addition .

---

**okwme** (2025-02-05):

hey [@wighawag](/u/wighawag) have you found any alternative solutions? I’ve been using https://indexsupply.net which I love as a fast and flexible events API but I still need a solution to convert block numbers to timestamps. Have you come across any service that does this fast / efficiently? Even if it had to happen as a second call, if it could be done in batches it could work ok…

---

**wighawag** (2025-02-05):

My alternative solution is to add timestamp to my events.

If you cannot do this and you have access to batching, then you can use my [indexer](https://github.com/jolly-roger-eth/ethereum-indexer) and configure it to fetch timestamp. Not sure how it compares to other solution in term of speed though,

otherwise as [this comment](https://ethereum-magicians.org/t/proposal-for-adding-blocktimestamp-to-logs-object-returned-by-eth-getlogs-and-related-requests/11183/9) indicate Reth seems to support the timestamp in their log

---

**okwme** (2025-02-05):

ah nice!

your indexer looks like a nice solution if i run something myself, but i’m also interested in hosted solutions as well as solutions that work for many alt evm networks.

thanks for the info : )

---

**TimDaub** (2025-03-19):

You sadly cannot assume a block every 12 seconds post merge because this isn’t 100% accurate:

- https://etherscan.io/block/15537446
- https://etherscan.io/block/15537445

the timestamps are more than 12s apart. Besides, that’s an unrealistic assumption towards builders. We cannot expect every builder to have a maximally nuanced understanding of the timestamp guarantees of the Ethereum consensus. That’s not socially scalable. Also there are no future guarantees in that approach. Besides, that approximation would anyways only work for Mainnet, and not e.g. rollups.

```auto
import fetch from "node-fetch"; // npm install node-fetch

// Configuration
const ALCHEMY_API_KEY = "";
const ALCHEMY_URL = `https://eth-mainnet.g.alchemy.com/v2/${ALCHEMY_API_KEY}`;
const MERGE_BLOCK = 15537394;

async function getBlock(blockNumber) {
  const blockHex = "0x" + blockNumber.toString(16);
  const response = await fetch(ALCHEMY_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "eth_getBlockByNumber",
      params: [blockHex, false],
    }),
  });

  const data = await response.json();
  if (data.error) throw new Error(data.error.message);
  return {
    number: blockNumber,
    timestamp: parseInt(data.result.timestamp, 16),
  };
}

async function main() {
  // Get the merge block as a reference point
  const mergeBlock = await getBlock(MERGE_BLOCK);
  let currentBlock = MERGE_BLOCK + 1;

  try {
    while (true) {
      const block = await getBlock(currentBlock);
      // Calculate expected timestamp based on seconds since merge block
      const blocksSinceMerge = currentBlock - MERGE_BLOCK;
      const calculated = mergeBlock.timestamp + blocksSinceMerge * 12;
      const diff = Math.abs(block.timestamp - calculated);

      console.log(
        `Block ${currentBlock}: timestamp=${block.timestamp}, calculated=${calculated}, diff=${diff}`
      );

      if (diff > 0) {
        console.log(
          `❌ Mismatch found at block ${currentBlock} (diff=${diff} seconds)`
        );
        break;
      }

      currentBlock++;
      await new Promise((r) => setTimeout(r, 200)); // Respect rate limits
    }
  } catch (error) {
    console.error(`Error at block ${currentBlock}:`, error.message);
  }
}

main();
```

```auto
Block 15537395: timestamp=1663224191, calculated=1663224191, diff=0
Block 15537396: timestamp=1663224203, calculated=1663224203, diff=0
Block 15537397: timestamp=1663224215, calculated=1663224215, diff=0
Block 15537398: timestamp=1663224227, calculated=1663224227, diff=0
Block 15537399: timestamp=1663224239, calculated=1663224239, diff=0
Block 15537400: timestamp=1663224251, calculated=1663224251, diff=0
Block 15537401: timestamp=1663224263, calculated=1663224263, diff=0
Block 15537402: timestamp=1663224275, calculated=1663224275, diff=0
Block 15537403: timestamp=1663224287, calculated=1663224287, diff=0
Block 15537404: timestamp=1663224299, calculated=1663224299, diff=0
Block 15537405: timestamp=1663224311, calculated=1663224311, diff=0
Block 15537406: timestamp=1663224323, calculated=1663224323, diff=0
Block 15537407: timestamp=1663224335, calculated=1663224335, diff=0
Block 15537408: timestamp=1663224347, calculated=1663224347, diff=0
Block 15537409: timestamp=1663224359, calculated=1663224359, diff=0
Block 15537410: timestamp=1663224371, calculated=1663224371, diff=0
Block 15537411: timestamp=1663224383, calculated=1663224383, diff=0
Block 15537412: timestamp=1663224395, calculated=1663224395, diff=0
Block 15537413: timestamp=1663224407, calculated=1663224407, diff=0
Block 15537414: timestamp=1663224419, calculated=1663224419, diff=0
Block 15537415: timestamp=1663224431, calculated=1663224431, diff=0
Block 15537416: timestamp=1663224443, calculated=1663224443, diff=0
Block 15537417: timestamp=1663224455, calculated=1663224455, diff=0
Block 15537418: timestamp=1663224467, calculated=1663224467, diff=0
Block 15537419: timestamp=1663224479, calculated=1663224479, diff=0
Block 15537420: timestamp=1663224491, calculated=1663224491, diff=0
Block 15537421: timestamp=1663224503, calculated=1663224503, diff=0
Block 15537422: timestamp=1663224515, calculated=1663224515, diff=0
Block 15537423: timestamp=1663224527, calculated=1663224527, diff=0
Block 15537424: timestamp=1663224539, calculated=1663224539, diff=0
Block 15537425: timestamp=1663224551, calculated=1663224551, diff=0
Block 15537426: timestamp=1663224563, calculated=1663224563, diff=0
Block 15537427: timestamp=1663224575, calculated=1663224575, diff=0
Block 15537428: timestamp=1663224587, calculated=1663224587, diff=0
Block 15537429: timestamp=1663224599, calculated=1663224599, diff=0
Block 15537430: timestamp=1663224611, calculated=1663224611, diff=0
Block 15537431: timestamp=1663224623, calculated=1663224623, diff=0
Block 15537432: timestamp=1663224635, calculated=1663224635, diff=0
Block 15537433: timestamp=1663224647, calculated=1663224647, diff=0
Block 15537434: timestamp=1663224659, calculated=1663224659, diff=0
Block 15537435: timestamp=1663224671, calculated=1663224671, diff=0
Block 15537436: timestamp=1663224683, calculated=1663224683, diff=0
Block 15537437: timestamp=1663224695, calculated=1663224695, diff=0
Block 15537438: timestamp=1663224707, calculated=1663224707, diff=0
Block 15537439: timestamp=1663224719, calculated=1663224719, diff=0
Block 15537440: timestamp=1663224731, calculated=1663224731, diff=0
Block 15537441: timestamp=1663224743, calculated=1663224743, diff=0
Block 15537442: timestamp=1663224755, calculated=1663224755, diff=0
Block 15537443: timestamp=1663224767, calculated=1663224767, diff=0
Block 15537444: timestamp=1663224779, calculated=1663224779, diff=0
Block 15537445: timestamp=1663224791, calculated=1663224791, diff=0
Block 15537446: timestamp=1663224815, calculated=1663224803, diff=12
❌ Mismatch found at block 15537446 (diff=12 seconds)```
```

---

**wighawag** (2025-03-19):

I created a PR in the execution-apis repo that adds the blockTimestamp to the log schema

This seems to be now the process to get rpc methods included or modified (and not EIPS anymore): [add blockTimestamp to Logs by wighawag · Pull Request #639 · ethereum/execution-apis · GitHub](https://github.com/ethereum/execution-apis/pull/639)

---

**sinamahmoodi** (2025-05-23):

I was surprised to read this thread and see the sheer amount of support for this idea. I never knew it was such a pain point for users. IMO it’s a nobrainer fix and it’s a process failure that we don’t have it yet.

Opened a PR to implement this in geth: [core/types: add timestamp to derived logs by s1na · Pull Request #31887 · ethereum/go-ethereum · GitHub](https://github.com/ethereum/go-ethereum/pull/31887).

---

**bastien** (2025-07-06):

Closing the loop - `blockTimestamp` was added to logs in Geth v1.16.0 (Terran Rivets).

`blockTimestamp` is now hex encoded as of v1.16.1.

