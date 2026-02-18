---
source: magicians
topic_id: 9920
title: Whats going to happen to Rinkeby?
author: kladkogex
date: "2022-07-12"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/whats-going-to-happen-to-rinkeby/9920
views: 1271
likes: 9
posts_count: 11
---

# Whats going to happen to Rinkeby?

We at skale run lots of tests on Rinkeby, and  going to be a pain to move to another test network.

I think an option for us is to fork a Rinkeby node and keep using it internally.

I wonder, if there are other people negatively affected by the future death of Rinkeby

## Replies

**abcoathup** (2022-07-13):

Sepolia and Goerli are the public testnets to use moving forward.

### EF testnet deprecation blog post:


      ![](https://blog.ethereum.org/images/favicon.png)

      [Ethereum Foundation Blog](https://blog.ethereum.org/2022/06/21/testnet-deprecation)



    ![](https://blog.ethereum.org/images/posts/upload_8d7ea1c612b90c3235dd54044d541b6a.jpg)

###










### Peter on Rinkeby:

https://twitter.com/peter_szilagyi/status/1526065746165567488

---

**kladkogex** (2022-07-14):

Well the problem is that we have historic smart contract infrastructure that was deployed to Rinkeby by our QA team over several years.

Moving Sepolia and Goerli is not an option to us.

What we will probably need to do is keep Rinkeby running at least for us internally. If someone else is interesting in continuing Rinkeby to run please let me know.

---

**timbeiko** (2022-07-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> Well the problem is that we have historic smart contract infrastructure that was deployed to Rinkeby by our QA team over several years.

What are the blockers to redeploying this on another testnet? Would be curious to better understand and see if other projects are in the same situation.

One note re: Rinkeby is that it won’t be run through The Merge (or future forks), so as of The Merge, it won’t be a good staging environment for mainnet.

---

**kladkogex** (2022-12-09):

Hey [@timbeiko](/u/timbeiko)

Our QA team is having lots of problems getting testeth for Goerlie.  May be ETH foundation starts charging a little for it ? At the moment there seems to be hardly any way to get a significant amount of it.

---

**abcoathup** (2022-12-09):

App devs should use Sepolia (due to Goerli supply issues)

There is a one time 10 Sepolia & Goerli testnet ETH claim: https://collect-test-eth.org/

For larger amounts you would need a Goerli whale.

---

**timbeiko** (2022-12-09):

Sepolia should not have the same long-term supply issues as Goerli because it uses an ERC20 token for the beacon chain, and therefore can mint more testnet ETH. [@kladkogex](/u/kladkogex) if you need a short term “transition” amount of GoETH, let me know your address and roughly how much. Thanks!

---

**kladkogex** (2022-12-16):

Thank you Tim!!!

Here is the address of our QA team

0xE74ad5437C6CFB0cCD6bADda1F6b57b6E542E75e

1000 would be enough for our QA team short term so we can test the next release

We will move to Sepolia then as you suggest.

Appreciate your help!

---

**timbeiko** (2023-01-02):

[@kladkogex](/u/kladkogex) done! apologies for the delay

---

**kladkogex** (2023-01-16):

Thank you Tim !!!

---

**JoGetBlock** (2023-04-20):

Hi Tim, I am from GetBlock, a top blockchain RPC node provider that supports 50+ blockchains, we work with multiple big projects such as Binance, Polygon and Chainlink. I’m reaching out to discuss an opportunity to support the web3 community of developers. We would like to create an Ethereum testnet faucet powered by GetBlock.

To make this possible, we would like to kindly ask for your support. We believe that Testnet Whale’s contribution (by providing L2 Goerly ETH) would be invaluable in helping to make this project a success.

Your support would help us to facilitate the development of new and innovative decentralized applications and drive the growth of the Ethereum community.

Please, let me know if you could help us with this.

