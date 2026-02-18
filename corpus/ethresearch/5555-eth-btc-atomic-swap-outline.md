---
source: ethresearch
topic_id: 5555
title: ETH-BTC Atomic Swap Outline
author: efalken
date: "2019-06-04"
category: Decentralized exchanges
tags: []
url: https://ethresear.ch/t/eth-btc-atomic-swap-outline/5555
views: 3127
likes: 1
posts_count: 6
---

# ETH-BTC Atomic Swap Outline

I think atomic swaps between eth and bitcoin should be straightforward given Ethereum’s contracting capabilities. I am curious why this has not been done. For example:

Bob and Alice agree to trade 32 eth for 1 btc. Alice gives Bob her BTC address, and tells Bob where their Ethereum Atomic Swap Contract is. Bob tells Alice his Ethereum address.

1. Alice posts 32 ETH into EthereumAtomic Swap Contract, and a hash of her private message m, h. It will pay out to Bob if Bob can supply the private message m so that sha256(m)=h. After 24 hours, Alice can withdraw the ETH back to her account.
2. Bob gets onto the bitcoin blockchain and sends 1 BTC in a Hash Time Locked Bitcoin Contract to Alice’s bitcoin address. Alice can receive the 1 BTC if she provides m such that sha256(m)=h. If Alice does not retrieve the BTC within 6 hours, Bob can claim it.
3. Alice withdraws the 1 BTC in time, revealing m.
4. Bob uses m to withdraw 32 ETH from the Ethereum Atomic Swap Contract.

This seems completely secure. If Bob does not show up, Alice cannot show her private message to Bob, and she can get her ETH back. If Alice does not show up to retrieve Bob’s BTC and reveal her private message, Bob can get his BTC back.

Has anyone created something like that? It would seem useful.

## Replies

**Ping** (2019-06-04):

Yes, it is totally possible, and surely sure someone has built it before.

But here’s some problems:

1. How can individuals find counterparty to trade with?
2. Since the ‘swap’ process is interactive, an order maker has to stay online to response taker. That’s terrible.

---

**efalken** (2019-06-04):

With maker-taker it would need a low latency solution to instantiate the contract, so that would require trust, and couldn’t happen  in the US. Nonetheless, there are lots of such solutions in utero that have the same problem: bisq, forkdelta. I think the problem might be that this is only useful for transactions of sufficient size, and so take 10x the trust, which is hard.

If you know of something like this I’d appreciate the link.

---

**sule** (2019-06-14):

[GitHub - AltCoinExchange/ethatomicswap: Ethereum atomic swap](https://github.com/AltCoinExchange/ethatomicswap) The code is old and not updated for a while but you should get the idea. This is for Ethereum side ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

---

**raullenchai** (2019-06-17):

1. can be addressed by services like localbitcoin.com. 2) is terrible if Alice claimed but Bob failed to withdraw 32 ETH – perhaps that’s why atomic swap is not that popular.

---

**elliotolds** (2019-07-11):

It looks like [liquality.io](http://liquality.io) is what you’re looking for. I’ve never tried it though.

