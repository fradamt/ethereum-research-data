---
source: magicians
topic_id: 8465
title: "EIP-4863: Beacon chain push withdrawals"
author: ralexstokes
date: "2022-03-01"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-4863-beacon-chain-push-withdrawals/8465
views: 2259
likes: 5
posts_count: 3
---

# EIP-4863: Beacon chain push withdrawals

Discussions for EIP-4863.

## Replies

**ralexstokes** (2022-03-03):

A draft PR containing a prototype implementation in Geth can be found here:



      [github.com/ethereum/go-ethereum](https://github.com/ethereum/go-ethereum/pull/24468)














####


      `master` ← `ralexstokes:prototype-withdrawal-txns`




          opened 11:17PM - 24 Feb 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/5/5d705096b99e21043b54ded6bb921211255c36b2.png)
            ralexstokes](https://github.com/ralexstokes)



          [+200
            -5](https://github.com/ethereum/go-ethereum/pull/24468/files)







PR prototyping "push"-style withdrawal transaction processing from the beacon ch[…](https://github.com/ethereum/go-ethereum/pull/24468)ain to the EVM.

## TODO:
- [x] add block validations for tx collation
- [x] to Wei
- [x] clean up tx hash

## Open questions:

- ~Geth uses a transaction's hash to identify it -- in keeping w/ the use of SSZ elsewhere for the serialization of this transaction type, I'd suggest the hash identifier  is the SSZ hash tree root of the withdrawal receipt container. Open to other options though.~
- @fjl had the idea to emit logs for each withdrawal transaction processed. I'm open to the idea and left a note where it would make sense to write them to the state, but I'll leave out the implementation for now.

## Notes:

This PR will accompany a draft EIP that suggests EL upgrades to go into Shanghai to facilitate validator withdrawals. This stye of withdrawal method is accompanied by the CL upgrade in this PR: https://github.com/ethereum/consensus-specs/pull/2836

This PR assumes that this transaction type `0x3` is placed alongside regular user transactions in the `ExecutionPayload` -- the CL PR needs to be updated to reflect this change as noted there.

## Implementation rationale:

This PR changes the "outer" transaction processing logic during the application of state transitions. Another option would be to leverage more of the EVM machinery (detecting the transaction type during EVM execution) but that leads to a number of special cases to support this new transaction type (e.g. `msg.from` could be `nil` but that fails a number of invariants in the EVM that `from` is always some account address). The overall design of the "push"-style transactions also explicitly forgoes EVM processing (to avoid dealing with issues of gas accounting and dealing with failed executions on withdrawal consumption) so the current implementation seems like the best spot to add support for this new transaction type.

---

**mkalinin** (2022-03-17):

I think it worth specifying a network behaviour around withdrawal transactions, i.e. they must not be propagated and advertised, and must never be added to the mempool.

