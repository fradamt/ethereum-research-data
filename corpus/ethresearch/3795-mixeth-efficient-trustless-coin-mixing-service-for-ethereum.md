---
source: ethresearch
topic_id: 3795
title: "MixEth: efficient trustless coin mixing service for Ethereum"
author: seresistvan
date: "2018-10-14"
category: Security
tags: []
url: https://ethresear.ch/t/mixeth-efficient-trustless-coin-mixing-service-for-ethereum/3795
views: 4343
likes: 3
posts_count: 17
---

# MixEth: efficient trustless coin mixing service for Ethereum

Hello everyone! Let me present you **MixEth**, which is an efficient trustless coin mixing service for Ethereum. This is a joint work with [@nagydani](/u/nagydani).

***Note:*** this is an early-stage work, hereby we just release the draft paper. Implementation, security proofs and many more are yet to come!

The basic idea is that unlike previous proposals ([Möbius](https://eprint.iacr.org/2017/881.pdf) and [Miximus](https://github.com/barryWhiteHat/miximus) by [@barryWhiteHat](/u/barrywhitehat) ) which used linkable ring signatures and zkSNARKS respectively for coin mixing, we propose using verifiable shuffles for this purpose which is much less computationally heavy. Additionally we retain all the strong notions of anonymity and security achieved by previous proposals consuming way less gas.

The protocol in a nutshell: senders need to deposit certain amount of ether to ECDSA public keys. These public keys can be shuffled by any receiver at most once using a verifiable shuffle protocol. The shuffle is sent to the MixEth contract and anyone can check whether their own public key is shuffled correctly (i.e. it is included in the shuffle). If one creates an incorrect shuffle than it can be challenged and malicious shufflers’ deposits are slashed if challenge is verified. If there are at least 2 honest receivers then we achieve the same nice security properties achieved by Möbius and Miximus. At the end of the protocol receivers can withdraw funds from a shuffled public key which are public keys with respect to a modified version of ECDSA.

For more details, have a look at the [draft version](https://github.com/seresistvanandras/MixEth/blob/master/article/main.pdf) of the MixEth paper.

Any feedback, comment, critique is more than welcome!

## Replies

**Silur** (2018-10-21):

Some observations on the draft:

The original paper generalize the CP proof of logarithm equalty for 2+ elements, for the original construction adresses elgamal pairs (and tweaked for DSA later). This also means that the desired scalability will surely change in the EC generalization and unless the iterated proof is not used, even though the keys are smaller it surely will perform poorly compared to the iterated version.

Also note that the Fiat-Shamir heuristic is not safe in the random-oracle model if it’s (only) binding to the provers state, because the prover has a chance to select the initial blinding exponents to result on a challenge that has low (or even zero, I didn’t benchmark the computational needs) exponent and apply the proof to an indentity-permutation. I’d suggest using a VRF here.

Last, I couldn’t understand your statement on this in the paper, but out of the 2 shuffles presented in Neff’s research you use the version that assumes that the prover knows all the exponents prior the protocol what is not acceptable for eg in multilayer mixing.

---

**noot** (2018-10-21):

a few comments:

to my understanding, someone needs to deploy a MixEth contract each time they wish to mix some transactions, with the constructor including sender addresses, withdraw public keys, and the corresponding shuffles and proofs.

what is the size of all the data needed? what is the gas cost to store it on chain?

the deployer of the contract cannot be hidden; who will be the ones deploying this contract?

as well, regarding the shuffling and challenging rounds: how will the incentivization structure work for this, if there is one?

otherwise, really interesting proposal! I’m also working on a similar project involving creating precompiles for linkable ring signatures + a mixer to go along with it.  I hadn’t considered that a withdrawal from the mixer requires an account that already has ether in it, making it impossible to use a fresh address. not sure if EIP86 fixed this or not, but definitely interesting to look into.

---

**seresistvan** (2018-10-21):

[@Silur](/u/silur)! Actually we do not use Neff’s proof verification for the correctness of the verifiable shuffle. We chose to have a different approach than proving the correctness of a shuffle. We outsource the verification to the participants of the mixer to earn remarkable efficiency gains! They can only prove the incorrectness of the shuffle with 2 Chaum-Pedersen proofs. Neff’s zk-proof has been only put in the article for historical reasons and as inspiration.

I agree that the Fiat-Shamir heuristic for the Chaum-Pedersen proof needs to be done well.

You are right! I probably cited wrong the computational complexity of Neff’s proof! Need to check it, although it does not affect our protocol!

[@noot](/u/noot)!  Well, the constructor does not contain all that data. It is added to the contract in the course of deposit transactions from each sender and potentially shuffling transactions from receivers. I did not make precise calculations yet, I’ve recently started implementing the protocol but I’m quite convinced that this is gonna be lightweight gas-wise. One public key is 64-bytes at worst (you can do actually 32-bytes + the sign of the second coordinate).

Approx sizes of transactions and gas costs:

- Deposit transaction: 1 public key (1point on secp256k1) = 64 bytes. So this requires \approx (2*SSTORE+G_{transaction})=61,000 gas.
- Shuffling transaction: n shuffled public key + shuffling accumulated constant  (n+1 points on the curve): (n+1)*64 bytes. Gas cost for this: 2(n+1)(SSTORE+CALLDATALOAD+CALLDATACOPY)+G_{transaction} \approx 44,000n+21,000
- Challenging a shuffle: transcript of 2 Chaum-Pedersen proofs cca. 400,000 gas
- Withdraw transaction: one single tx signed with the modified ECDSA \approx 21,000 gas

You can look up gas values corresponding to each opcode here. As soon as I have a working proof of concept I will update gas costs here and on github.

Incentivization structure: if you screw up a shuffle your deposit will be slashed, since others can prove to MixEth by 2 Chaum-Pedersen proofs that you misbehaved. Malicious guy’s incorrect shuffle can be reverted and mixing could continue from a previous correct shuffle. MixEth is fine (provides strong notions of anonymity) if there is at least one honest receiver **who shuffles**.

EIP86 or some other form of account abstraction would solve the problem of sending transactions from fresh addresses without ether by allowing recipients to pay for the gas fee.

---

**khovratovich** (2018-10-24):

It seems that the protocol does not work because if a challenger do not know `c` he can not provide a Chaum-Pedersen proof of DDH correctness and thus he can not challenge an incorrect shuffle.

There are other problems:

1. Shuffler’s proof should be verified at the time of shuffle submission
2. A malicious shuffler can steal the money if not everyone verifies the shuffle.

---

**seresistvan** (2018-10-24):

Let’s denote the set of initial public keys as PK=(s_{1}G, \dots s_{n}G), where G is the standard generator element on secp256k1 and s_{i} are the private keys. Then we call C^{*}=cG as the shuffling accumulated constant. Shuffler choses c and a permutation \pi uniformly at random and neither of those should be made public. (Honest shufflers will not reveal them).

This way shuffled public keys can be obtained by the shuffler by:

PK^*=(c(s_{\pi^{-1}(1)}G),c(s_{\pi^{-1}(2)}G),\dots,c({s_{\pi^{-1}(k)}}G)).

Shuffler uploads (PK^{*},C) to the MixEth contract allowing any participants to check whether their own public key was correctly shuffled ie. whether s_{i}C=s_{i}(cG) \in PK^{*}. If not, then challenge, which can be carried out since the shuffling accumulated constant is public and available in the MixEth contract.

![](https://ethresear.ch/user_avatar/ethresear.ch/khovratovich/48/2531_2.png) khovratovich:

> Shuffler’s proof should be verified at the time of shuffle submission

Each participant of the mixer should verify off-chain whether their public key is shuffled correctly. If this is not the case they can challenge the shuffle on-chain by submitting 2 Chaum-Pedersen proofs. Please refer to the paper.

![](https://ethresear.ch/user_avatar/ethresear.ch/khovratovich/48/2531_2.png) khovratovich:

> A malicious shuffler can steal the money if not everyone verifies the shuffle.

That’s right. Well, we assumed that participants are online and watch the MixEth contract to detect any incorrect shuffle. This is basically the same assumption that you have in state-channels if you do not rely on watchtowers or for Plasma exits. I think this is an acceptable assumption.

---

**khovratovich** (2018-10-24):

Oh, I see that the text has changed since a few days ago I looked at it, and now you talk about two proofs that are part of the challenge.

It will work in this setting, however I see another attack vector: the challenger proves that his public key before all shuffles does appear before the last shuffle but does not appear after the last shuffle. This links public keys across shuffles and is actually quite dangerous since a malicious shuffler can submit the shuffle just before the end of the shuffle period, and he will learn at least one position-to-position mapping across all shuffles from the challenge proof. At the cost of the stake, yes.

---

**khovratovich** (2018-10-24):

It would be more correct to submit two pairs (C_i,sC_i),(C_{i+1},sC_{i+1}) and prove the equality of the discrete logarithms in the pairs.

---

**seresistvan** (2018-10-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/khovratovich/48/2531_2.png) khovratovich:

> This links public keys across shuffles and is actually quite dangerous since a malicious shuffler can submit the shuffle just before the end of the shuffle period, and he will learn at least one position-to-position mapping across all shuffles from the challenge proof.

Well, the challenge only links one particular public key in one particular shuffle. Since we assumed that there was one honest shuffler and that Decisional-Diffie-Hellmann holds, we are fine, because there was somewhere a correct and honest shuffle which breaks links between shuffled public keys.

![](https://ethresear.ch/user_avatar/ethresear.ch/khovratovich/48/2531_2.png) khovratovich:

> It would be more correct to submit two pairs (Ci,sCi),(Ci+1,sCi+1)(C_i,sC_i),(C_{i+1},sC_{i+1}) and prove the equality of the discrete logarithms in the pairs.

Actually this is almost identical to what we have right now for challenge verification. Currently MixEth requires 2 Chaum-Pedersen proofs for tuples (G, sG, C_{i}, sC_{i}), (G, sG, C_{i+1}, sC_{i+1}).

I was also thinking about only requiring a single Chaum-Pedersen proof just like you proposed [@khovratovich](/u/khovratovich) for the tuple (C_{i}, sC_{i}, C_{i+1}, sC_{i+1}). I’m just not yet convinced that it is secure. If it is, I will stick to your proposal and will update paper+code accordingly.

---

**khovratovich** (2018-10-24):

> Well, the challenge only links one particular public key in one particular shuffle. Since we assumed that there was one honest shuffler and that Decisional-Diffie-Hellmann holds, we are fine, because there was somewhere a correct and honest shuffle which breaks links between shuffled public keys.

No matter how many honest shuffles were, one incorrect shuffle links one of last keys to one of the first ones, effectively nullifying the mixing property of previous shuffles. By repeating for different keys, an adversary learns the entire first-to-last mapping

---

**seresistvan** (2018-10-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/khovratovich/48/2531_2.png) khovratovich:

> No matter how many honest shuffles were, one incorrect shuffle links one of last keys to one of the first ones, effectively nullifying the mixing property of previous shuffles. By repeating for different keys, an adversary learns the entire first-to-last mapping

I do not see why this would be true. The challenger only reveals in the prove the **last** shuffled public key of hers and the **last but one** shuffled public key of hers. The challenge transaction could be sent from any address and even if one challenge is verified the problematic shuffle is ignored and shuffling might continue from the latest correct shuffle.

[The Decisional-Diffie-Hellman assumption](https://en.wikipedia.org/wiki/Decisional_Diffie%E2%80%93Hellman_assumption) ensures that whenever you try to go back to the very first shuffle you will fail to deanonymize and link public keys if there is at least one honest shuffler who did not disclose the secret multiplier c from C^*.

---

**seresistvan** (2018-10-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/khovratovich/48/2531_2.png) khovratovich:

> It would be more correct to submit two pairs (Ci,sCi),(Ci+1,sCi+1)(C_i,sC_i),(C_{i+1},sC_{i+1}) and prove the equality of the discrete logarithms in the pairs.

Oh, sorry [@khovratovich](/u/khovratovich) ! I’ve just realized that you were absolutely right! We do not have any other choice! We need to apply one Chaum-Pedersen proof in the challenge transaction for the tuple (C_{i},sC{i}, C_{i+1}, sC_{i+1}) otherwise the attack vector (deanonymizating by linking the challenger to the initial receiver public key) you mentioned earlier would work.

---

**kosecki123** (2018-10-28):

> Unfortunately, neither Möbius nor Miximus can be deployed on the present-day Ethereum. When
> users of the coin mixing contract, either Möbius or Miximus would like to withdraw their funds
> they can not do this from a fresh address, since it does not hold any ether. Since as of now only
> the sender of a transaction can pay for the gas fee, users can not withdraw their funds unless they
> ask someone to fund their fresh address.

Can another solution be to pay the 3rd party to withdrawn for you to “fresh address”? Very similar to how Ethereym Alarm Clock provides the execution in the future.

---

**seresistvan** (2018-10-28):

Yes, [@kosecki123](/u/kosecki123)! Similar workarounds are suggested in the [Möbius paper](https://eprint.iacr.org/2017/881.pdf) and on the [Miximus github](https://github.com/barryWhiteHat/miximus), however these workarounds are obviously far from being ideal.

An interesting question is whether we can come up with something which does not rely on such workarounds and is entirely compatible with present-day Ethereum. Personally I would be very interested in such a proposal! ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9)

---

**seresistvan** (2018-10-28):

One of the reasons for existence of MixEth. I expect that cca. 90-105 MixEth txs could fit into a single block.

On of the main bottlenecks of coin mixing protocols is the withdrawal transactions’ gas costs. A Miximus withdrawal transaction burns 1\,903\,305 gas, regardless of the number of participating parties. Since the block gas limit is 8\,000\,266 as of 2018, October 24 only 4 Miximus withdrawal transactions could fit in one Ethereum block. This is even worse for Möbius, since the gas cost for withdrawing coins from a Möbius mixer linearly increases with the numbers of participants.  [![withdrawalComplexity](https://ethresear.ch/uploads/default/original/2X/1/12ce5611d2dd6d19d69c3e1a703bcddef000998d.jpeg)withdrawalComplexity550×390 17.6 KB](https://ethresear.ch/uploads/default/12ce5611d2dd6d19d69c3e1a703bcddef000998d)

---

**kosecki123** (2018-10-29):

Account abstraction?

---

**seresistvan** (2018-10-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/kosecki123/48/2518_2.png) kosecki123:

> Account abstraction?

Yes, account abstraction would solve most of our headaches, although it is still actively discussed. Have a look at the [Account Abstraction Radically Simplified](https://ethresear.ch/t/account-abstraction-radically-simplified/3769) topic here on ethresearch.

