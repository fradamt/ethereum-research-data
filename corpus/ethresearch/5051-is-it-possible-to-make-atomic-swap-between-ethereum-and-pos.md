---
source: ethresearch
topic_id: 5051
title: Is it possible to make atomic swap between Ethereum and POS chain?
author: lebed2045
date: "2019-02-25"
category: Decentralized exchanges
tags: []
url: https://ethresear.ch/t/is-it-possible-to-make-atomic-swap-between-ethereum-and-pos-chain/5051
views: 2686
likes: 4
posts_count: 4
---

# Is it possible to make atomic swap between Ethereum and POS chain?

There’s a simple way to make an atomic swap between a smart-contact chain and any POW chain.

For example for Ether <-> BTC:

- Alice sends some Ether to the swap smart-contact which locks this money. While doing that she specify her BTC address and Bob’s ethereal address.
- Bob sends BTC to Alice.
- Bob shows the proof of this BTC tx on to the smart-contract and unlocks his Ether.

Bob’s proof is a signed transaction and SPV proof which lead to the valid Merkel root inside the block header. So smart-contact should either believe that proof is legit because it has sufficient level of work (number leading zeros in the hash of the block header, so it’s very costly to fake it) or there are oracles who send time to time these BTC block’s headers to the contact and the smart contact takes the chain with larger PoW as the legit one.

The question: is it possible to design a similar system where the second chain is POS?

The immediate problem with POS is how to verify that the block header is a legit one. Perhaps people who are building POS for Ethereum can give advice? As I understood this is also the problem for the [lite client](https://github.com/ethereum/wiki/wiki/Light-client-protocol)?

thanks.

## Replies

**sina** (2019-02-25):

I wrote a post recently on an idea I dubbed [“layer 2 oracles”](https://ethresear.ch/t/layer-2-oracles-disputable-data-feeds/4935)[0]. The gist of the idea is having a bonded party relay the block headers, where anyone can put up collateral to submit a dispute of a block header, and something like an Augur market is used to settle the dispute. This would work for PoS as well as PoW chains, since the “punishment” for posting a bad block is the relayer losing their bonds, rather than the sunk cost of submitting a valid PoW with the contract verifying it.

More generally you could use this pattern for relaying arbitrary off-chain data feeds; it could definitely work for block headers.

[[0] https://ethresear.ch/t/layer-2-oracles-disputable-data-feeds/4935](https://ethresear.ch/t/layer-2-oracles-disputable-data-feeds/4935)

---

**alexeiZamyatin** (2019-03-05):

What you refer to for tx verification are “chain relays” (name first mentioned in V. Buterin’s report on chain interoperability [1]). The principle is the same as for SPV/light clients. In theory, every chain can implement an SPV client for another chain, independent of the underlying consensus mechanism - in practice this is way more complicated and requires a case-by-case feasibility analysis.

**First, some details on PoW chain relays.**

There exist PoW relay implementations for:

- BTC->ETH: https://github.com/ethereum/btcrelay
- ETCETH: https://github.com/KyberNetwork/peace-relay
and relays are in progress for
- ZEC->ETH: https://github.com/ConsenSys/Project-Alchemy
- DOGE->ETH :  https://github.com/dogethereum/dogethereum-contracts

In our recent paper (XCLAIM)[2] we provide a more detailed discussion of the security, functional requirements and practical challenges of chain relays for PoW blockchains: https://eprint.iacr.org/2018/643.pdf (Sec. V-B, Sec. VII-A,B,D and Appendix D). Another relevant paper is “PoW sidechains”[3]

**PoS Chain Relays**

You implement similar constructions for PoS blockchains. The verification is likely similar to the case of PoW blockchains, however the functional requirements of a such chain relay are slightly different. Specifically, instead of verifying the PoW target against the difficulty (which implies that the relay must implement the difficulty adjustment mechanism), the relay instead must verify the signatures of the PoS committee. From this follows, that the relay must know of the staking mechanism and the distribution at every round/epoch (incl. identities the elected committee).

I have not yet seen an implementation of a such relay, however “PoS Sidechains” by Gazi, Kiayias and Zindros[4] provide some very interesting work.

Hope this helps.

Note: there is a significant difference between “real world” data feeds and cross-chain verification is that we can provide cryptographic proofs for events occurring in blockchains, but (likely) not for events occurring in the “real world” (e.g. a horse race: you *must* trust the provider of the results).

[[1]  Buterin, Vitalik. “Chain interoperability.”  R3 Research Paper (2016).](https://static1.squarespace.com/static/55f73743e4b051cfcc0b02cf/t/5886800ecd0f68de303349b1/1485209617040/Chain+Interoperability.pdf)

[[2] Zamyatin, A., Harz, D., Lind, J., Panayiotou, P., Gervais, A., & Knottenbelt, W. J. “XCLAIM: Trustless, Interoperable Cryptocurrency-Backed Assets”. To appear at IEEE S&P 2019.](https://eprint.iacr.org/2018/643.pdf)

[[3] Kiayias, Aggelos, and Dionysis Zindros. “Proof-of-Work Sidechains”. 3rd Workshop on Trusted Smart Contracts at FC 2019.](https://eprint.iacr.org/2018/1048.pdf)

[[4] Kiayias, Aggelos, and Dionysis Zindros. “Proof-of-Stake Sidechains.” To appear at IEEE S&P 2019.](https://www.computer.org/csdl/csdl/proceedings/sp/2019/6660/00/666000a660.pdf)

---

**sule** (2019-06-14):

This is not how Atomic Swap between BTC <> ETH should work. It can, but there is better, more straight forward way to do it: Ethereum supports RIPEMD160 hashing which is also used in scripts checking the secret in BTC<>LTC atomic swaps for example. Here’s the example of a smart contract for Atomic swap on ethereum side: https://github.com/AltCoinExchange/ethatomicswap

