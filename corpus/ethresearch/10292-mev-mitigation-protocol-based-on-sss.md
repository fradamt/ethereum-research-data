---
source: ethresearch
topic_id: 10292
title: MEV mitigation protocol based on SSS
author: marcellobardus
date: "2021-08-09"
category: Miscellaneous
tags: [mev]
url: https://ethresear.ch/t/mev-mitigation-protocol-based-on-sss/10292
views: 2443
likes: 4
posts_count: 6
---

# MEV mitigation protocol based on SSS

# MEV mitigation protocol based on SSS

Nowadays searchers do not have any guarantee that whenever they find MEV opportunities those won’t be simulated and front-ran by the block producer.

Let’s assume that the chain on which the MEV opportunity was found consists of a protcol built on top of it, which is able to operate on a shared ECDSA key using techniques (e.g. [SSS](https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing)).

The participants of such a protocol would be:

- Block producers
- Block producers verifiers
- Users/Searchers

Such a key could be generated and split accross the protocol where the number of it’s block producers and cerifiers is known.

Whenever a searcher or a user wants to submit a transaction, it will have the ability to encrypt its content with the shared and known public key.

For the sake of simplification let’s introduce something I call `Banana Transaction` or `BTx`.

The `BTx` could have the structure below:

```auto
{
    encryptedContent: {
        recipient,
        data,
        gasLimit,
        value,
    },
    gasPrice,
    encryptedContentHash,
    signature
}
```

`BTxns` might exist only in the mempool, those are not part of the chain.

The lifecycle of a block including `BTxns` can be the following:

1. EOA submits a BTx to a dedicated mempool.
2. The BTx spreads accross the protocol through the p2p layer.
3. Block producer will pick up a BTx from the mempool and form a block or append to an existing one.
NOTE: The transactions will be ordered by its gasPrice
4. Once the block is formed it will be proposed to the protocol participants.
5. The protocol network in response will agree on the block and decryptBTxns.
6. The original block producer will include the block into the chain preserving the proposed order (sorted by gasPrice, if there are 2 or more BTxns with equal gasPrice the BTx with the bigger hash will be included on the top) and exclude invalid BTxns (if any).
7. Whenever the protocol participants will observe that the included block did not preserve the proposed order the block producer will be punished (e.g. slashing).

This design could be widely applied to most of the chains because it does not require any hard fork.

The `network/MEV mitigation protocol` can be setup by picking up the actors below:

- Block producer which will stake some tokens in order to participate in the protocol.
- Verifiers who ensure that the proposed order was preserved.
- Searchers/Users willing to submit BTxns.

The value of posted stake by the block producer should be high enough in a way, that the loss because of slahing is bigger than the potential outcome from including another block than the proposed one.

Also the proposal assumes that `Searchers/Users` are willing to pay higher `gasPrice` than usual, in order to incentivise block producers to participate in the network.

Such a solution prevents:

1. Block producers from frontrunning MEV searchers.
2. Sandwiching bots from sandwiching users transactions.
3. Any sort of MEV done on top of the mempool(BTxns mempool) content.

Weak points and solutions:

- DDOS - Sending BTxns with invalid content within the encrypted section

Requires the BTx origin to submit a valid hash cash solution on time of submission.

How can a distributed protocol detect that the block producer changed the order?

- The participants can vote that the block producer cheated by reaching a majority ← This is weak cause the majority can be unfair and steal the stake deposited by the producer by enforcincg slashing?
- Include fraud proofs where the rlp encoded decrypted txns are sent to a smart contract, the contract will order them and recompute the block hash, check if the recomputed blockhash matches the hash of block producer by the block producer. If not the fraud is proven.

## Replies

**norswap** (2021-08-09):

I’ve been thinking exactly along the same lines! I have a big writeup on MEV incoming where I do touch on this idea.

In my scheme I was envisioning that the block proposer would commit to a full block instead of tx-by-tx. There is the obvious issue that we do not know the gas cost of an encrypted tx. One way around this issue is to:

1. Include a “gas estimate” along the transaction, and to change the protocol so that gasEstimate * gasPrice (but the London version of course) may be extracted from the user if the transaction’s content is invalid. Alternatively, we could simply have a bondAmount field working on the same principle, and simply include a lot of transactions in the block (see point (2) on how to deal with excess transactions). We need to look out for spamming of transactions with invalid signatures, high gas price but low gas estimate / bond.
2. When the block (with encrypted tx) is being proposed, include the target block size. This enables dropping any transaction that would exceed the target size, and not reduce the base fee if we end up using less gas than the target. If the target is not included, this lets the miner drop transactions from the end of the block at his discretion (since he could choose to make the block bigger under EIP-1559), which is undesirable.

Note that point (1) solves the DDOS issue.

Under this scheme, the other validators would first sign the proposed block, then, once it has reached enough signatures, work together to decrypt the transactions. The “enough-signed” block can be used to slash the proposer in a fraud proof.

> This is weak cause the majority can be unfair and steal the stake deposited by the producer by enforcincg slashing?

Isn’t it already game over if the majority of validators are corrupt in PoS?

---

**marcellobardus** (2021-08-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/norswap/48/6891_2.png) norswap:

> This is weak cause the majority can be unfair and steal the stake deposited by the producer by enforcincg slashing?

I agree that the voting approach is really weak, however fraud proofs could solve the problem.

---

**kladkogex** (2021-08-11):

Preventing front running using threshold encryption is already part of SKALE



    ![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png)

      [Input causality option in ETH 2.0?](https://ethresear.ch/t/input-causality-option-in-eth-2-0/4741) [Cryptography](/c/cryptography/28)




> Since in ETH 2.0 validators are going to have BLS key, there is an interesting proposal to include input causality into ETH 2.0.
> For input causality, you do not know what transaction is included in the blockchain, until the moment it is included.  The transaction is threshold-encrypted by the user, and only once it is included in the block and finalized,  validators collectively exchange messages, decrypt it and run EVM on it.
> A system like this would automatically prevent front running.

---

**norswap** (2021-08-13):

My point was the opposite: I don’t think it’s that weak. If the majority is unfair/colluding, the network is probably fubar anyway.

---

**norswap** (2021-08-13):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Preventing front running using threshold encryption is already part of SKALE

Nice, I’ll try reading the whitepaper. Any other resource that would be better to learn about that?

Are any insight to be gleaned of how using theshold encryption for this purpose has worked out on Skale chains? In particular, I’d be curious if you have any kind of MEV potential like liquidations? And if so, how did that work out? Do you shuffle in addition to using encryption?

If you check [my writeup on MEV](https://hackmd.io/@norswap/mev) you’ll see one thing people are (rightfully) worried about is the potential for spamming when such a MEV opportunity arise. So say you have an oracle update that could lead to a liquidation. Nobody knows before the block is released. Afterwards, if there is shuffling, you’re incentivized to spam transactions so that one of your transaction ends up before all other liquidation attempts in the next block. If there is no shuffling you have very classical MEV where the block proposer can put its own encrypted liquidation first in the block.

