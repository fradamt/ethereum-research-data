---
source: ethresearch
topic_id: 1849
title: General smart contract on plasma chain?
author: ShuangWu
date: "2018-04-27"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/general-smart-contract-on-plasma-chain/1849
views: 3459
likes: 3
posts_count: 9
---

# General smart contract on plasma chain?

Has anyone thought of how to design general smart contracts for plasma?

I have tried for a while and found it really challenging. We have found a way to remove 2-phase confirmation of txs in plasma-mvp, which provides simpler finality of a tx. But we haven’t figured out how to implement secure general smart contracts under block withholding attacks.

I think smart contracts on plasma are important and will be useful for:

1. multi-level plasma chain
2. lightning network / state channel on plasma

If the general smart contract for plasma turns out to be impossible in the end, dedicated smart contract can still support the functionalities above.

I’m wondering if there is any progress in the community.

## Replies

**johba** (2018-04-27):

Hi ShuangWu,

there are very early thoughts about general computation in the plasma classic model written down here: https://parseclabs.org/files/plasma-computation.pdf

It utilizes the truebit verification game to challenge blocks that contain invalid state transitions.

looking forward to your feedback.

---

**ShuangWu** (2018-04-27):

Great! I read about your white paper, which is pretty cool.

I didn’t know that David Knott had found the way to remove 2-phase tx confirmation two months ago. Thanks for the info.

I think we have independently found a very similar way to do that. The core ideas are the same.

BTW, we are working on Fraud Proof without Truebit, which allows parallel TX processing (TXs to the same contract) within one block. There are still some missing pieces of the whole picture. We will share the ideas once it is complete.

---

**johba** (2018-04-30):

sounds great. please keep me updated ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**sg** (2018-05-02):

Do you have any further discussion/code of computation request? I love this.

---

**johba** (2018-05-03):

hey [@sg](/u/sg), we are working on modifying the Truebit VM to take EVM calls, nothing that is presentable until now.

I received an interesting **question** via email recently, and think it is worth sharing and discussing:

> It is not clear how Plasma MVP confirmation or no confirmation schemes for dealing with data availability on UTXO payments child chains extend to to general computation chains.  Would you mind explaining this in more detail?

**The Response:**

Computation in itself does not require any changes to the confirmation model. Yet, there are only very limited use-cases where computation is used in isolation. Often there is a deposit or a reward with the outcome of a computation. For example the computation executed over the course of a poker hand decides the distribution of the funds to players.

The paper proposes 2 types of transactions:

1. transfer-type UTXOs hold funds on the address of a key (as in Bitcoin)
2. computation-request/response UTXOs hold funds than are solely controlled by its code (DAO-like smart contracts)

Type 2. UTXOs are similar to contract accounts in Ethereum, which have no associated private key.

The no-confirmation scheme became interesting when analyzing data withholding during transaction from transfer-type UTXOs to computation UTXOs and vise versa. As there is no private key with computation requests/responses, but only the hash of the contract code, schemes that require signatures by private keys can not be used.

I understand that there are more complexities about securing funds in DAO like constructs on Plasma chains, especially as data withholding is not a discrete event, but a subjective impression. We are currently working on a list of use-cases that we think are applicable for such contracts and try to distinguish them from use cases that can not be used on Plasma chains.

I will follow up with updates in this thread, also keep an eye on [our github](http://github.com/parsec-labs/).

---

**johba** (2018-05-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/shuangwu/48/1259_2.png) ShuangWu:

> BTW, we are working on Fraud Proof without Truebit, which allows parallel TX processing (TXs to the same contract) within one block. There are still some missing pieces of the whole picture. We will share the ideas once it is complete.

[@ShuangWu](/u/shuangwu)  is there any place where I can read about the details?

---

**jdkanani** (2018-05-15):

[@johba](/u/johba) This is cool. We are doing something similar, but using EVM (with the limited state) for now and faster blocks through periodic checkpoints (PoS).

Plus, I see your code uses my commits from plasma MVP ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) Feels good.

---

**johba** (2018-07-13):

There are updates on this. We have an [architecture doc](https://github.com/parsec-labs/solevm-truffle/blob/master/docs/Architecture.md) to use the solEVM to run Truebit-like verification games for off-chain computation.

This is not really in the scope of Plasma, as I’m pretty sure that the subjectivity of data-withholding makes it impossible to construct any effective exit game for smart contracts state.

Yet, computation proofs are useful in a wider scope, and we are funding and driving the development together with [Decentraland](https://decentraland.org/), [Matic Network](https://matic.network/), and [Parsec Labs](https://parseclabs.org/) on Gitcoin:

here is the first task:


      ![](https://ethresear.ch/uploads/default/original/3X/7/2/720b719833927c39bb95f1c2b9ff766b72fffdc7.png)

      [app.buidlbox.io](https://app.buidlbox.io/)





###



HackQuest Acquires BuidlBox to Accelerate Web3 Developer Ecosystem Growth










more issues from this repo are following:


      ![](https://ethresear.ch/uploads/default/original/2X/b/bad3e5f9ad67c1ddf145107ce7032ac1d7b22563.svg)

      [GitHub](https://github.com/leapdao/solEVM-enforcer/issues)



    ![](https://ethresear.ch/uploads/default/optimized/3X/5/9/5905a48cca9ae0fff696089e5b20bcf1887d5e58_2_690x345.png)

###



Partial implementation of the Ethereum runtime in Solidity (PoC) - leapdao/solEVM-enforcer

