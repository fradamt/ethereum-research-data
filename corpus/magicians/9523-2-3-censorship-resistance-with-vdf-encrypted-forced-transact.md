---
source: magicians
topic_id: 9523
title: <2/3 censorship resistance with VDF encrypted forced transactions
author: sadcat
date: "2022-06-07"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/2-3-censorship-resistance-with-vdf-encrypted-forced-transactions/9523
views: 506
likes: 0
posts_count: 1
---

# <2/3 censorship resistance with VDF encrypted forced transactions

**Goal**: sustained censorship is impossible as long as there’s one honest validator, there’s no cartel of >2/3 validators that censors all proposals from validators outside of the cartel, and the chain is finalizing.

**How**: each proposer includes a 1024 byte message encrypted with a VDF secret. VDF parameters are selected to ensure time required for decryption on the fastest hardware is slightly longer than expected time needed to finalize the slot with the message: X slots.

After Y slots (Y > X), with Y calculated to ensure that decryption is possible on a reasonably fast gpu working since the initial block is published, the decrypted message must be posted by the proposer - as part of the consensus.

If there are missing proposals, subsequent blocks must instead include N oldest pending reveals, where N is at least 2.

Each message is interpreted as a transaction. If the transaction is incorrect, whether because of an outright incorrect format (random data), incorrect signature, used nonce etc - it’s ignored and has no effect on the state. If it’s correct, it’s executed first in the block.

By a node default, proposers that don’t have any specific message to post, encrypt zeros - as a way to minimize total load (as a message of zeros can be encoded as a one bit flag when decrypted later).

If otherwise correct, the transaction is executed with the base fee from the block in which the encrypted message was included. Half of priority fee goes to the executor, half to the original proposer of the encrypted transaction.

Fees *must* depend only on the block in which the encrypted transaction was posted - otherwise it would be possible to censor it by manipulating fees.

**Security**: As long as chain is finalizing and >2/3 of validators aren’t actively cooperating to enforce censorship, all it takes is one honest proposer to eventually include censored transactions on-chain.

**Disadvantage**: the disadvantage is that each validator needs to solve Y VDF puzzles in parallel continuously, for which the most practical solution is a GPU capable of Y parallel VDF computations. Y puzzles are necessary due to the requirement to post solutions for missed past blocks. However, at the current eth price that’s only about 0.5% of 32ETH for the gain best attainable censorship resistance. Additionally, the VDF solving service can be subcontracted - and (less economically) could be solved on a multicore server.

**Comparison to reveal schemes** etc: Reveal schemes don’t work, they only move the potential point of censorship. Requiring the reveal of some committed secret to progress the chain creates an obvious denial of service risk (chain stops). Not requiring it (ie. it’s possible to orphan a block, etc) moves the point of censorship to the block with the reveal, which defeats the point, because the commit step achieves nothing. For the same reason oldest missed pending messages have to be posted first - in a VDF scheme there’s no denial of service risk.

---

How to choose censored transactions to include becomes an arbitrary individual decision of each validator and is outside the consensus layer. One very simple algorithm is: a non-validator censored party publishes a transaction with a priority fee >2x higher than the current priority fee. Honest validators observe that over several slots (5?) all blocks with it were orphaned. They decide to include it as an encrypted tx. I’m sure there are better schemes - but it’s outside of the consensus.

Specific implementation should ensure that it’s relatively easy to generate a separate payment to the original validator, for later inclusion (not execution), in case intentional invalidation of encrypted transactions between becomes a problem.

The censored party (from an unrelated account) would lock funds in a non-existing create2 address, then after the transfer is confirmed - publish its salt and full code: if the encrypted message is included, transfer x eth to the original encrypted publisher. Given a sufficiently long timelock, this would guarantee payment for the inclusion no matter what.

---

Are 1024 bytes enough? What about rollups, the most obvious use case? Yes, it should be enough - because censored rollup data can be posted encrypted (xor encrypted with a simple sequential sha3) elsewhere - in a transaction that looks like random data. The forced transaction would only need to decrypt already present data - which can as well be an encrypted contract to be spawned and executed. In fact even 512 bytes may be enough.

In practice, I think the mere existence of a VDF-scheme would prevent any censorship attempts - no point trying if failure is certain.
