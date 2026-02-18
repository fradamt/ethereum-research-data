---
source: magicians
topic_id: 18381
title: "RollCall Breakout #2: Fee Markets"
author: adietrichs
date: "2024-01-29"
category: Protocol Calls & happenings
tags: [rollcall]
url: https://ethereum-magicians.org/t/rollcall-breakout-2-fee-markets/18381
views: 899
likes: 4
posts_count: 2
---

# RollCall Breakout #2: Fee Markets

As announced on [RollCall #2](https://github.com/ethereum/pm/issues/925), we are organizing a series of breakout calls each Wednesday. The second breakout call will be on L2 fee markets. The intention is for these breakout calls to be optional additions to the monthly RollCalls, and aimed at bringing together the subset of teams interested in each particular topic.

## Meeting Info

- Wed Jan 31, 2024, 14:00-15:30 UTC
- Zoom link shared in the rollcall channel in the EthR&D Discord, which is bridged to the RollCall telegram channel, shortly before the call.

## Agenda

- Introduction (short presentation)
- Rollup teams’ summary of current thinking
- EVM gas cost repricing

use cases (e.g. keccak for zk)
- challenges (backwards compatibility, client & language support)
- removing gas observability via EOF

L1 settlement fees

- fees independent of L2 prices & execution results
- adapting the 4844 tx type
- wallet / tooling support

Congestion pricing

- differences L1 / L2
- potential for unbundling EIP-1559

Open discussion

## Further discussion

Feel free to add comments here with further items of discussion

## Replies

**abcoathup** (2024-02-06):

## RollCall (L2 standards) fee markets breakout call

### Notes by

*(From Eth R&D Discord)*

basically, we talked about 3 main topics:

- repricing EVM operations (say keccak for zk)
- L1 passthrough fees, how to pay for settlement and DA cost
- potential proper multidim pricing (passthrough is basically a simple 2d version of that)

takeaway was that the topic where we might be close to having something to standardize is the L1 settlement cost. we talked a bit about what to standardize there, and the main feedback was that standardizing both a 2d tx type and a fee estimation API would be the best candidates.

So we introduce the concept of “settlement gas” (name tbd), and each L2 can have their own logic for how much settlement gas a tx consumes, and how to set the price for that gas during inclusion, but there would be a standardized way for users to specify limit and max price, and for estimating cost of a tx.

So ideally we can turn this into one or two concrete RIPs and move forward with that.

### Video:

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/3/3a8065ea9ccabc30a2ceeba2ab34d4b9cde0c607.jpeg)](https://www.youtube.com/watch?v=URa8Jn-0aU4&t=2s)

