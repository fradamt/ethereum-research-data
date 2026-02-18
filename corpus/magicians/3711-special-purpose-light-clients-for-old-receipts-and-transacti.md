---
source: magicians
topic_id: 3711
title: Special-purpose light clients for old receipts and transactions
author: vbuterin
date: "2019-10-19"
category: Working Groups > Ethereum 1.x Ring
tags: []
url: https://ethereum-magicians.org/t/special-purpose-light-clients-for-old-receipts-and-transactions/3711
views: 2572
likes: 9
posts_count: 3
---

# Special-purpose light clients for old receipts and transactions

One of the scalability limitations of ethereum today is the fact that full nodes need to store the entire historical chain, including blocks and receipts. Clients that do not do this (eg. Nethermind) exist, and have <1/4 the storage requirements of clients that do, but major clients are choosing not to implement in part because there are dapps that use very old historical blocks and transactions that we are not willing to break.

I propose that we establish a norm that clients should not store transactions or logs more than 1 million blocks (~4 months) behind the head, and we should work hard to create special-purpose cryptoeconomic light client infrastructure to allow clients to continue to fetch such data. This infrastructure can be included by default into major ethereum clients including full nodes and light nodes.

The setup would work as follows:

1. There would be a registry contract where anyone can register their address as a light client server by providing a deposit (eg. 32 ETH). Deposits can be withdrawn after one day. When depositing, the server must also provide a root HISTORY_ROOT that represents what they think is the Merkle root of all historical blocks.
2. Suppose that a light client wants to learn about the set of all receipts between heights H1 and H2 that contain topic T. The client would send a query (H1, H2, T) to a set of servers S_1 ... S_n that are in the registry and that have submitted R values that the client agrees with.
3. Every S_i would return a signed message (H1, H2, T, R_1, R_2 ... R_m, P_1, P_2 ... P_m, sig) where R_1 ... R_m is a set of all (block, txindex) pairs which issue such a receipt, and P_i is a Merkle proof showing that R_i contains a valid receipt, rooted in the server’s provided HISTORY_ROOT. sig is a signature of (R_1 ... R_m) signed by the registered key.
4. The user would receive the answers, verify each Merkle branch, and see if all answers match among the servers that have responded. If they match, the user would accept. If there is any mismatch, the user would publish a fraud proof into the deposit contract themselves, or rebroadcast the mismatch to a server that would do it for them.
5. The user can optionally pay a fee. Servers can prioritize responding to requests from users that have paid fees to them. This can be done on-chain or through an agreed L2 protocol (eg. optimistic rollup may work well)

A fraud proof consists of (i) a signed message produced in step (3), and (ii) a Merkle proof, rooted in the `HISTORY_ROOT` value submitted by the server at deposit time, of a receipt that is in `(H1, H2)`, has topic `T`, and was not part of the signed message.

**Altogether, this allows clients to fetch the complete set of old receipts with one round of network messaging, completely bypassing the need to scan through bloom filters, greatly increasing the usability of such applications.**

Note that there is one exceptional case, where the receipt is too big to include in a block (this would generally only happen due to malicious DoS attacks, but could also happen if a rollup saves data in receipts). This can be solved by having servers commit to (and send to clients once) a list of all (block, txindex) pairs with oversized logs and adding a separate class of fraud proof for omitting any such transaction.

For historical transactions (“fetch me the transaction with this hash”) the mechanism is similar. If there is a transaction with a given hash, then a simple Merkle branch suffices (we lean on the txhash uniqueness assumption here). If there is no transaction with the desired hash, then the servers can send a signed message, and a fraud proof showing the location of the transaction (which because of how the Patricia tree works would only need to include the transaction hash) suffices to prove that the servers gave an incorrect answer.

### Possible extensions

- If desired, the oversized log problem could be more efficiently solved at protocol level by changing the receipt data structure so that instead of logs it stores logs_root = sha3(logs) and changing the above protocol so that the server must return all transactions whose transaction-level bloom filter matches target even if they do not contain target in their logs; this way the fraud proof would not need to include the body of the list of logs and would always be log-sized.
- The servers could just reply with the list of (block, txindex) pairs, without proofs. This would improve efficiency, but at the cost of weakening the security model (if the cryptoeconomic assumption fails, not only could receipts be omitted, but also the client would see false receipts until a fraud proof comes in).

## Replies

**dominic** (2019-11-01):

+1 on the norm [@vbuterin](/u/vbuterin). Cutting the history is important and will help to reduce the problem of data growth to that of storage growth alone.

Regarding the light client infrastructure for logs and transactions there is a similar concept already deployed from the guys at slock.it. I think the only difference between these concepts is that in your case it is the client who collect multiple answers and checks them for consistency while in the slock.it system the client submits how many validations it wants to have and the replying server is collecting signatures from other light clients server. Fraud proofs are submitted by the other light client servers. This scheme simplifies the client logic and reduces the number of round-trips, but might be easier attackable when the light client server operator has many servers and these collude… but IMHO you always have this problem and the only real lever is to ask for higher deposits / more signatures. [@simon-jentzsch](/u/simon-jentzsch) might have thought about these trade-offs more as this is something we chatted on for a second in Osaka. E.g. should a light client ask for a specific number of validator signatures from the registry or for a total ETH amount deposit strength that is = sum(deposit) of all signing light client servers.

In either case though I’m not aware of a working incentive model yet on either of these.

I’m curious though on your thoughts on this for the base data: storage data and raw transactions (block data). Clearly there is an operational need for nodes to keep the full storage data, but:

1. There is no need to keep any historic storage data (apart from reorgs maybe)
2. There is no need/incentive to help other nodes to sync up. E.g. in a competitive market why should I help my competitors to bootstrap new nodes?

The nature and origin of Ethereum imply to me that there is a certain altruism in the community to at least allow 2. to happen “forever”. But I wanted to know whether this is general consensus.

---

**vbuterin** (2019-11-01):

> There is no need to keep any historic storage data (apart from reorgs maybe)

And even there I think not keeping historical storage older than ~1000 blocks is not needed. If a longer reorg happens it’s IMO better that the chain falls into chaos than a 51% attack cleanly succeeds.

> There is no need/incentive to help other nodes to sync up. E.g. in a competitive market why should I help my competitors to bootstrap new nodes?

This is definitely true, and we do rely on altruism. If we remove the norm that nodes are expected to sync history, then the data per new node that needs to be altruistically uploaded falls from ~200 GB to ~50 GB, which seems like a significant improvement.

