---
source: ethresearch
topic_id: 1284
title: Research on privacy issues in Ethereum
author: unboxedtype
date: "2018-03-02"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/research-on-privacy-issues-in-ethereum/1284
views: 3604
likes: 3
posts_count: 9
---

# Research on privacy issues in Ethereum

Hello!

Both Bitcoin and Ethereum systems are known to provide pseudo-anonymity for its users:

the real identity can be  revealed only if a user discloses his public key that

hashes to his address.

There were several works showing that at least in Bitcoin world, this kind

of anonymity does not guarantee privacy [1] [2]. Using some

statistical methods, one can trace all the addresses belonging to the same party.

This fact explains new research projects towards privacy-preserving blockchain platforms [3].

But what about Ethereum? From Bitcoin, it differs in a sense that by doing a transaction,

you can transfere value and/or mutate some contract state.

Are there any ongoing research regarding privacy issues that arise in the context of

smart-contracts. By privacy, I do not mean non-disclosure of contract’s state, but rather

concerns of using the same address for each transaction call, for example.

I appreciate any thoughts/pointers regarding this topic.

Thanks.

[1] Ron, Shamir - Quantitative Analysis of the Full Bitcoin Transaction Graph [2012]

[2] Meiklejohn et al - A Fistful of bitcoins [2013]

[3] Kosba et al - Hawk: The BlockChain Model of Cryptography and Privacy-Preserving Smart Contracts (2016)

## Replies

**AntoineRondelet** (2018-03-15):

Hello everyone !

Here is a link to Mobius, a “Trustless Tumbling for Transaction Privacy” on Ethereum, that we have developed as a Proof of Concept here at Clearmatics: https://github.com/clearmatics/mobius

As outlined in the Mobius wiki (see wiki section on github), and in the different issues that have been opened in the past months, Mobius is nothing else than a prototype. Being aware of its current flaws, we are trying to see if such a contract-based solution could be a good way to enhance privacy on Ethereum, without additional pre-compiled contracts or modifications in the EVM, while keeping decent performances and gas cost.

Any feedback is, of course, welcomed,

Cheers,

---

**nootropicat** (2018-03-16):

Utxo model can be emulated by making a second transaction to a new account after every transaction, therefore privacy is theoretically equivalent.

In practical use ethereum provides less plausible deniability because it doesn’t happen, so even if you tried you would stand out.

---

**unboxedtype** (2018-03-16):

Thanks for your replies!

Regarding privacy issues in the context of sending/receiving ether, everything seems quite similar to Bitcoin. However, ether transactions are not the only thing a user may want to hide from public.

Lets say, there is some smart-contract, and the user do not want to disclose the fact of transacting to that contract, but would like to get a service from it.

To overcome this situation, he can generate as many new accounts as he want, the ether should be pumped

into them somehow, however.

Generally, are there any known drawbacks in having multiple accounts in that context? Or it is a silver bullet that

solves all the problems?

---

**Privacy-is-Freedom** (2018-03-30):

The project sounds very interesting!

I’m wondering how much gas used for one transaction. The bn256 computation is very gas consuming.

---

**AntoineRondelet** (2018-04-05):

> To overcome this situation, he can generate as many new accounts as he want, the ether should be pumped into them somehow, however.

Yeah, that could be possible, but as you said, these accounts would need to receive some ethers, and you just end up transposing the problem from “Doing a private transaction (that calls a contract’s function)” to “Doing a private transaction (that funds the new account)”, which is the problem we want to solve…

Another drawback to have a lot of accounts (I’m talking about stealth addresses as a privacy solution here) is that if you receive ethers on these accounts, and you want to spend spend them, this could lead to a leakage of your identity. By spending ethers from these accounts you expose yourself to potential de-anonymization (Eg: you have a network of 3 peers Alice, Bob, Charlie. Alice sends 1Eth to Bob’s stealth address. Now Bob’s identity is obfuscated, but if Bob owes 1Eth to Charlie and uses the account he just received Eth from Alice in, to send Charlie 1Eth, then Bob discloses his “secret” identity to Charlie, and Charlie can now know that Alice did a transfer to Bob).

Morever, since Ethereum doesn’t rely on a UTXO model, if you own 3 accounts with 1ETH on each, and need to buy something for 3ETH, you need to find a way to “gather” your funds into 1 account from which you could do the 3ETH payment. This also leaks ownership of the 3 accounts you had before. Anyone could observe transaction initiated from these addresses converge to a single account…

---

**AntoineRondelet** (2018-04-05):

Some benchmarking as been done over there: https://github.com/clearmatics/mobius/wiki/Performance-Review-V0.1

Withdrawals can become super expensive as the ring signature verification is linearly dependent on the ring size. Looking at the `IsSignatureValid` and `ringLink` functions, we see that we have something like `RING_SIZE * 160 000 + N` gas for a withdrawal (where N is negligible compared to the other terms)

---

**Privacy-is-Freedom** (2018-04-16):

Thanks for your update.

I mentioned the main results are concerning “Ring Signature”.  Is that the way how we hide senders?

On the GitHub issue, I noticed that there is one open issue [range proof](https://github.com/clearmatics/mobius/issues/37)   .   I’m afraid this is of the most expensive part (which may take 70%+ gas consumption of a single transaction).

Have you considered the range proof part?

---

**unboxedtype** (2018-04-24):

Thanks for your insightful comment.

> Yeah, that could be possible, but as you said, these accounts would need to receive some ethers, and you just end up transposing the problem from “Doing a private transaction (that calls a contract’s function)” to “Doing a private transaction (that funds the new account)”, which is the problem we want to solve…

I guess, we could use some escrow service to send Eth into our stealth addresses, but this leads to extra transaction costs.

