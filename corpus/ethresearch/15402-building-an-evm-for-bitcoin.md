---
source: ethresearch
topic_id: 15402
title: Building an EVM for Bitcoin
author: punk3700
date: "2023-04-24"
category: EVM
tags: []
url: https://ethresear.ch/t/building-an-evm-for-bitcoin/15402
views: 4463
likes: 20
posts_count: 24
---

# Building an EVM for Bitcoin

Our team has been working on a fun experiment of combining an EVM with Bitcoin in the last couple of months.  Since the Taproot Upgrade, we can write more data onto Bitcoin.  Ordinals was the first one that let people write files onto Bitcoin.  We took a different approach.  Instead of jpegs and text files, we let developers deploy smart contracts and dapps onto Bitcoin.

So now we can write “bigger” smart contracts thanks to the large on-chain storage on Bitcoin.  Did anyone explore this direction?  Would love to exchange notes.

[![pasted image 0](https://ethresear.ch/uploads/default/optimized/2X/a/a46b48b7832a532f5230b7ff69eb6dd367ff3ce9_2_355x500.png)pasted image 01138×1600 81.3 KB](https://ethresear.ch/uploads/default/a46b48b7832a532f5230b7ff69eb6dd367ff3ce9)


      ![](https://ethresear.ch/uploads/default/original/3X/8/1/81dbf3be3e95f0ec338a3f1ceb06efb13c042723.jpeg)

      [docs.bvm.network](https://docs.bvm.network/bvm/)



    ![](https://ethresear.ch/uploads/default/optimized/3X/0/e/0e3af80fb698b645e3eb7bd14e051e2f1c978c1d_2_690x362.png)

###

## Replies

**bsanchez1998** (2023-04-24):

This is really interesting. What stage are you in? I think building the UI will be a challenge for sure. When I tried to invest in Ordinals, setting up sparrow and having to read the docs to do it and the risks just made it seem like a nightmare if it were to be introduced to the masses, it just would not take as is. I am curious about your take on how you’re approaching this issue.

---

**punk3700** (2023-04-24):

The protocol is live.  There are already some sample dapps on Bitcoin (written in Solidity).  These dapps are super easy to use.  You can even use MetaMask to interact with these dapps.


      ![](https://ethresear.ch/uploads/default/original/3X/e/1/e1e9692d758a9c3b43c06b2726657952be80d57c.svg)

      [newbitcoincity.com](https://newbitcoincity.com/tc)



    ![](https://ethresear.ch/uploads/default/optimized/3X/8/c/8ce7f390cd193989290913cf890387d66f710425_2_690x437.png)

###



Launch your own Bitcoin L2 blockchain in one click.

---

**BitcoinEvm** (2023-04-27):

This has already been accomplished over a year ago & been stress tested.

https://bitcoinevm.com

Enjoy!

---

**BitcoinEvm** (2023-04-27):

Bitcoin nft marketplace https://crosschainasset.com

---

**BitcoinEvm** (2023-04-27):

Bitcoin decentralized swap https://BTCswap.org you can swap using Bitcoin with extremely low fees.

---

**bsanchez1998** (2023-04-27):

Oh okay awesome. Super interesting, I am excited to see where it goes!

---

**LuozhuZhang** (2023-04-28):

Can I understand that you run an “off-chain” EVM and write the states of the transaction results to the Bitcoin blockchain ledger?

---

**punk3700** (2023-04-28):

Hello.  Each Trustless Computer node batches & writes EVM transactions to Bitcoin.  The other Trustless Computer nodes read the EVM transactions from Bitcoin and update the “state” locally.  So it inherits Bitcoin consensus & security.

---

**punk3700** (2023-04-28):

Hello.  Will study it more.  Looks interesting.  Thank you for sharing!

---

**MicahZoltu** (2023-04-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/punk3700/48/11900_2.png) punk3700:

> Each Trustless Computer node batches & writes EVM transactions to Bitcoin. The other Trustless Computer nodes read the EVM transactions from Bitcoin and update the “state” locally. So it inherits Bitcoin consensus & security.

How do you deal with clients diverging if there aren’t regular state updates that are agreed to via some consensus mechanism that the network can synchcronize on?

---

**punk3700** (2023-04-28):

The consensus mechanism is actually the Bitcoin consensus mechanism.  Trustless Computer inherits Bitcoin security.  Trustless Computer nodes agree on the ordering of the EVM transactions written to each Bitcoin block.

---

**MicahZoltu** (2023-04-28):

Agreeing on transaction order alone is great in a hypothetical world where all software does exactly what it was supposed to do rather than what it was programmed to do.  The reason Ethereum includes the latest state root in the block header is to allow clients to synchronize on what the current state is so if any individual client has a bug or corrupted data it can immediately notice that it disagrees with the network and people can troubleshoot the problem.

Today I learned that Bitcoin doesn’t do this!  This feels crazy to me, but perhaps it is acceptable in the Bitcoin world because there is functionally only one client so the chance of desync is low (but not zero!).

---

**kladkogex** (2023-05-01):

So its basically merged mining. The blocks of the other chain are posted on Bitcoin and Bitcoin serves as a ledger that orders transactions.

Which mechanism do you use to transfer actual bitcoins into this chain ?) Also, how do you incentivize mining - do you have a separate token ?))

---

**tycho1212** (2023-05-01):

I’m very interested in the response to this question ![:pray:](https://ethresear.ch/images/emoji/facebook_messenger/pray.png?v=12)

---

**Zergity** (2023-05-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> The reason Ethereum includes the latest state root in the block header is to allow clients to synchronize on what the current state is so if any individual client has a bug or corrupted data it can immediately notice that it disagrees with the network and people can troubleshoot the problem.

I think the latest state root in the block header is mainly for state proofs, as client synchronization can easily be done via P2P messages between clients.

---

**zilayo** (2023-12-07):

has there been any further progress on this?

it seems like taproot related stuff has became really popular this year (ordinals in particular)

---

**SilkE** (2023-12-08):

What is the tps potential here? Anything that promotes more activity on Bitcoin is always worth exploring. Only concern is scalability compared to the likes of Solana and even Monad coming to ETH

---

**punk3700** (2024-11-13):

hey there!  sorry completely missed this.  yes, it’s live.  after we deployed the EVM for Bitcoin, we have made a lot of progress, bringing uniswap, op stack, and zk stack over to Bitcoin too.  more info on our site and our docs

bvm.network

docs.bvm.network

---

**bajpai244** (2024-11-13):

Interesting!

I guess Citrea is also doing something very cool! Rather than first writing a single txn to Bitcoin and then executing it, it runs an EVM network and then inscribes zk-proofs to Bitcoin!

This, combined with bit-VM being practical, could be a very great architecture, where u can optimistically verify zk-proofs on Bitcoin!

---

**Ashy5000** (2024-11-13):

Is the current EVM state stored onchain, or is it recalculated/hydrated from all the TXs that have been published to the Bitcoin network?


*(3 more replies not shown)*
