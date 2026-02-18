---
source: ethresearch
topic_id: 2066
title: Better history access by contracts
author: fahree
date: "2018-05-25"
category: EVM
tags: []
url: https://ethresear.ch/t/better-history-access-by-contracts/2066
views: 3759
likes: 4
posts_count: 17
---

# Better history access by contracts

Currently, the Ethereum API only gives access to the last 256 blocks. This makes it hard and expensive for contracts to verify that something did indeed happen a long time in the past, though it isn’t impossible, as demonstrated by Andrew Miller’s and Kobi Gurkan’s https://github.com/amiller/ethereum-blockhashes

My proposal for a future hard fork: add a function that provides logarithmic access to the entire blockchain history, whereby each block of number N offers direct access to the hash of the \lceil log_2 N\rceil blocks of number (N-1) \& ~(-1 << k) for k from 0 to \lceil log_2 N\rceil-1.

Then contracts can cheaply verify the presence of a transaction or log event in logarithmic time and space for both clients and servers. Validators don’t need to maintain more than a logarithmic extra state, though full history servers may have to maintain O(N log N) extra bits (or only O(N) using some compression at the cost of recomputing O(log N) hashes on demand).

PS: Shouldn’t there be a topic for discussion of the contract API? Or is the API considered fixed in stone forever, even for backward-compatible extensions?

## Replies

**lithp** (2018-05-25):

I’m not someone deeply involved in the Ethereum community so I could be leading you wrong here but I think the reason there’s no topic is because this isn’t the right forum to ask for this kind of consensus-breaking improvement. You might have better luck by [opening an EIP](https://eips.ethereum.org/)?

---

**fahree** (2018-05-25):

I believe it is a bit too early to open an EIP; I’d like to test the waters of the community first — I’m just starting to get involved, and I am not sure what the best forum is. The [EIP repository’s template](https://github.com/ethereum/EIPs/blob/master/ISSUE_TEMPLATE.md) suggests posting to the the [Protocol Discussion forum](https://forum.ethereum.org/categories/protocol-and-client-discussion). I will do just that.

Thanks!

---

**lithp** (2018-05-25):

Good luck! I hope you get some useful feedback. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**MicahZoltu** (2018-05-25):

Changing the number of blocks available to smart contracts would change client’s ability to prune old blocks, or start processing from a snapshot near head.  With the 256 block limit, clients can choose to start processing at some snapshot block > 256 blocks behind head and have a fully functioning validating client.  If we make it *possible* to lookup blocks from an arbitrary time in the past, then it means a validating client *must* retain all blocks in history and cannot start from a snapshot nor prune history.

---

**fahree** (2018-05-25):

Why couldn’t you prune old blocks? You only need to remember ~23 extra blocks at any given time.

---

**MicahZoltu** (2018-05-25):

Perhaps I am vastly misunderstanding your proposal.  In the original message you said:

![](https://ethresear.ch/user_avatar/ethresear.ch/fahree/48/1380_2.png) fahree:

> access to the entire blockchain history

This tells me that the entire blockchain history is *available*, meaning retained somewhere that is accessible.  Right now this is not a requirement, only the most recent 256 blocks actually need to be retained.

When you say:

![](https://ethresear.ch/user_avatar/ethresear.ch/fahree/48/1380_2.png) fahree:

> You only need to remember ~23 extra blocks

I’m confused because that seems to conflict with the first quote.

At the moment, *all* nodes could delete all but the most recent 256 blocks and the system *will* continue to function.  New nodes wouldn’t be able to sync from genesis block, but the chain could continue to mine new blocks and state would continue to update properly.  Any system that requires access to blocks older than 256 ago in smart contracts will make this scenario no longer possible.

---

**fahree** (2018-05-25):

That’s a total non-sequitur. Ethereum blocks already contain indirect links to the entire chain, and yet you already don’t need to maintain the entire history to validate the next block.

Instead of remembering just “the (hash of the) previous” block, you remember “the (hash of the) previous” block modulo 2^k for all k. That’s a tiny amount of information. You never need to go back in history to consult new values when you only go forward. Going from block N to N+1, each of the K “previous” blocks either is unchanged or becomes block N. No need to preserve much state if at all.

(Also, 23 is less than one tenth of 256, in case you didn’t notice, though for backward compatibility reasons you can’t just drop those 256 backlinks.)

Those who do keep parts of the history that matter to them (or all of it) can then trivially prove to a verifying contract that they did the right thing at some point in the past, at cost O(ln N) instead of O(N), without using clever, somewhat expensive, and possibly less stable, indirect, means such as amiller’s contract.

---

**fahree** (2018-12-19):

I realize I was reinventing my own variant of a patricia merkle tree. It would be simpler to just reuse the usual ethereum patricia merkle tree, and include a trie of all the past blocks. The essential property still holds: a non-archival client only needs keep O(log N) block hashes in memory, it doesn’t need to remember the details of the blocks.

---

**kaibakker** (2018-12-27):

I don’t see which applications would profit from it? You still have a hard time proofing a random blockhash was indeed included in the chain if the number is not in your defined set. These blockhashes could also be verified through a seperate smart contract a.k.a. http://btcrelay.org/ , but that has proven to be too expensive for proof of work check.

---

**kladkogex** (2018-12-28):

It is probably not such a good idea.  if one wants to remember history of transactions, one can save it in the smart contract.  Nodes should be able to prune old blocks.

---

**fahree** (2018-12-28):

[@kaibakker](/u/kaibakker)

- Users would be any contract that wants to verify transaction log entries left by the same or by some other contract, which would be much cheaper and safer than storing state in a contract then having an API for other contracts to check it.
- Yes, some relays like Efficiently Bridging EVM Blockchains Relay Networks V2 could be used, but they are much more complex and expensive.

[@kladkogex](/u/kladkogex)

- Once again, you don’t need to remember a history of transactions. To build and verify the historical merkle trees, only the spine of the previous historical merkle tree needs be kept in active memory. Using the existing Ethereum patricia merkle trees, this spine contains about 4 \log_2 N hashes where N is the height of the current block, so about 96 at current height. This is actually fewer hashes than the 256 most recent currently kept (that we still need, if only for backward compatibility).
- The details beyond the hashes in this spine can be safely dropped down the nearest memory hole by the regular ethereum nodes. Those users who care about some of the historical activity can save merkle proofs then use the historical tree to verify that activity cheaply.

---

**kaibakker** (2019-01-01):

I don’t understand how I can verify a random log with this functionality… Without sending all the blocks in between the block you want to proof something about and one of the stored blocks.

---

**fahree** (2019-01-02):

You send a Merkle proof for the block, which is contains about 4 \log_2 N hashes (about 96 at current height). Once the block is identified, you need to show the block headers, then another Merkle proof from the header to the specific transaction of log entry you want to prove was in the block which is about another hundred hashes.

All in all, you need to show a few hundred hashes, which is not nothing, but is still affordable, especially if you only have to show them when challenged, at which point  the bad guy pays.

---

**tim-becker** (2022-09-22):

We are using a similar approach for accessing historical block hashes on-chain in Relic Protocol. We store Merkle roots of chunks of historical block hashes in storage, and use zk-SNARKs to prove their validity.

For reference, see [relic-contracts/BlockHistory.sol at 2ecb2ffdd3a450a8eb7c352628c2ef51ed038c42 · Relic-Protocol/relic-contracts · GitHub](https://github.com/Relic-Protocol/relic-contracts/blob/2ecb2ffdd3a450a8eb7c352628c2ef51ed038c42/contracts/BlockHistory.sol)

This is already deployed on mainnet, and we’ll be releasing a developer SDK for integration shortly.

---

**aliatiia** (2023-08-22):

dApp-layer solutions for this are coming out, whereby Ethereum history (think: any query an archive node returns) is proven in zero-knowledge and provided onchain for consumption by L1 contracts, see for example:




      [docs.axiom.xyz](https://docs.axiom.xyz/developers/reading-historic-block-data)



    ![image](https://www.gitbook.com/cdn-cgi/image/width=1280,dpr=2,height=640,fit=contain,format=auto/https%3A%2F%2F2360979947-files.gitbook.io%2F~%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F0zt5FAwt1SbP42MMEkAR%252Fsocialpreview%252FjhkMBWbHdpdeRdg1CGLV%252Fhorizontal_black.png%3Falt%3Dmedia%26token%3D85745c5c-6c24-4d09-b296-4e8f9668e842)

###



Access historic block hashes from Axiom.

---

**MorseOlive** (2023-08-24):

Retrieving historical data can be expensive in terms of gas fees (transaction costs) and processing time. Balancing the cost-effectiveness of historical data access is crucial.

