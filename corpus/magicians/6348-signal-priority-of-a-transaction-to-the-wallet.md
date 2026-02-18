---
source: magicians
topic_id: 6348
title: Signal priority of a transaction to the wallet
author: ligi
date: "2021-05-27"
category: Web > Wallets
tags: [wallet, eip-1559]
url: https://ethereum-magicians.org/t/signal-priority-of-a-transaction-to-the-wallet/6348
views: 1443
likes: 10
posts_count: 11
---

# Signal priority of a transaction to the wallet

After post-processing the EIP1559 wallet call and seeing the mock-ups of other wallets I think that we are not yet leveraging EIP1559 to the full extend. The user is still presented with a choice (tx priority/miner tip) in the context of signing a transaction. In a perfect world the wallet would just tell the user what it will cost and be done with it (“Don’t make me think”)

But for this the wallet needs a signal what the priority for this transaction should be. This depends on the type of the transaction e.g. we need a high priority for transactions like a dex token-swap to e.g. not get failed transactions  - and we can live with a low priority when we vote on a DAO proposal where voting closes in a month.

I see 2 ways to signal it to the app:

- NatSpec annotation on the function
- injecting the intent into the RPC

I am leaning to option 2 as it covers more cases (e.g. including plain ETH transfers that are not possible with #1) and also because it can be done with already deployed contracts.

## Replies

**danfinlay** (2021-05-27):

I also prefer option 2 because it allows interfaces to update for contracts that are not upgradable.

Maybe a new parameter for `sendTransaction`, like `urgency`, with a preferred resolution time in `ms`? That way it can be friendly on a variety of evm compatible chains.

---

**danfinlay** (2021-05-27):

Actually that parameter probably isn’t sufficient. You kindof both want a sense of urgency, and also want to know *leniency*. “how long *can* this transaction wait?”. Some transactions legitimately may not be useful after a certain point, and that’s valuable information to convey to the wallet.

---

**ligi** (2021-05-27):

Thanks for chiming in! Yea think we should go the RPC route for sure - but maybe it makes sense to also signal via NatSpec to cover use-cases where no RPC is used (e.g. could imagine a static QR somewhere) - but maybe it’s not worth it for such edge cases. On the other hand “Better to have than to need” and it is not possible-feasible to retro fit it in this case.

And Yea we might need 2 values. Something like a “best before” and an “ideal at”

---

**danfinlay** (2021-05-27):

Doesn’t need to be natspec to be “wallet readable” from the contract. There could be a protocol like optionally implementing a `getTransactionUrgencyLevel(): uint256` method that wallets can ping just in case.

---

**ligi** (2021-05-27):

I would not want to bother nodes with that and also like the prospect it could boost sourcify usage a bit in the process ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9) We need more contracts verified in that manner and that could be a forcing function.

---

**MicahZoltu** (2021-06-01):

I don’t think people should be submitting *any* transaction that won’t be mined within a block or two.  I think it is generally a bad idea to rely on the global pending pool for medium-term storage of transactions and trust that your transaction won’t get dropped.

IMO, wallets should present the user with a cost and the user can take it or leave it.  If they leave it, they may come back and try again at a later time, and maybe some wallets have a “save for later” button to make this easy, but we shouldn’t be encouraging users to submit any transactions that are unlikely to be mined.

On a similar vein, I have advocated in the past and will probably continue to weakly advocate that execution clients should become more aggressive with purging their pending pool of transactions that aren’t likely to be mined anytime soon, even if they have extra space.  These transactions get gossiped around when a new client connects/reconnects and it is not free to keep them around.  If a user truly wants to keep transactions alive indefinitely, they should be using software explicitly designed for that and paying the necessary services for doing so rather than relying on the altruism of network gossip participants to not clear out long lived transactions.

---

**perama-v** (2021-06-02):

I like this idea. If you are going to lowball a transaction for possible inclusion in 1 week, a wallet/client-side system or service can monitor the basefee and resubmit when viable. If after 1 week gas prices are still too high, a user or wallet/client-side system can decide on the new price they will pay.

Regarding the exact size of the mempool (from 2 blocks into the future to an unbounded aggregate), one natural upper bound might be 1 epoch (~6 minutes). Post-merge, a consensus engine with one validator will discover if it will be required to propose a block with a lead time of min(1 epoch, slot_into_epoch), or ~6-12 mins. For the vast majority of its time, it will not otherwise be proposing blocks. The consensus engine can pass a message to the application-layer engine signalling the time until a block is expected to be produced. It can then begin to construct a mempool (either then or 2 blocks / ~30s before) by listening for new transactions being broadcast by the network. If instead, the mempool is being treated as a storage facility for unlikely transactions, the application-layer engine is encouraged to maintain a mempool during the long periods where it has no need to propose a block.

---

**ajsutton** (2021-06-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/perama-v/48/4036_2.png) perama-v:

> Post-merge, a consensus engine with one validator will discover if it will be required to propose a block with a lead time of min(1 epoch, slot_into_epoch), or ~6-12 mins.

Block proposers can only be calculated in the epoch they occur - there is no look ahead period. Nodes maintain a transaction pool to be able to gossip those transactions to other nodes even though they know for sure they will never propose a block (assuming they aren’t running a miner). I don’t think we’d want to lose that property or it would become extremely difficult for transactions to propagate through to block proposers effectively.

---

**quantobria** (2021-06-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> In a perfect world the wallet would just tell the user what it will cost and be done with it (“Don’t make me think”)
> But for this the wallet needs a signal what the priority for this transaction should be.

I like the idea of not making the user think. Especially when the user doesn’t really have the needed information for making the choice (the tradeoff of time).

I think that some good old QoS policies from the traditional networks might be the answer.

---

**perama-v** (2021-07-10):

With the brief of “don’t make me think” and three user groups described the opening post by [@ligi](/u/ligi):

- Generic transaction
- DAO proposal
- Dex token-swap

Here is a three-phase model.

1. Minimal interface yes/no interface (composed of transaction cost derived from Base Fee x 2).

This covers the normal user.
2. Second page for expressing increased desire for ultimate inclusion (derived from a Base Fee multiple, to cover x minutes of unexpected congestion).

This covers the DAO proposal. Any excess fee is refunded if not used.
3. If the user is not happy to pay the current fee, then they do not submit a transaction. If in the future their needs change (the proposal period is ending) and they now accept the current fee, they submit the transaction then.
4. Third page for expressing increased desire for rapid inclusion (derived from an increased Priority Fee, obtained from FeeHistory JSON RPC API).

This covers the dex token-swap. The Priority Fee is not refunded, which is why it is presented third as a specialised choice.

I made some notes and visual representations of that here:



      [Perama’s notes.](https://perama-v.github.io/ethereum/wallet-design)





###



Interesting topics and explorations.

