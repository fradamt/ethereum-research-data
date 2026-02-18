---
source: magicians
topic_id: 7674
title: Ephemeral networks and chain ids
author: fvictorio
date: "2021-12-03"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/ephemeral-networks-and-chain-ids/7674
views: 2506
likes: 10
posts_count: 8
---

# Ephemeral networks and chain ids

Ephemeral networks ([Hardhat Network](https://hardhat.org/hardhat-network/), [Ganache](https://www.trufflesuite.com/ganache), [geth --dev](https://geth.ethereum.org/docs/getting-started/dev-mode)`) are used as temporary networks during development. This makes them different from the mainnet and testnets, since you can’t assume that they will continue to exist indefinitely. Because of this, some common problems arise:

- MetaMask caches some data for each connected network, like the latest block number or the nonce of each account. When a network is ephemeral and a new, empty instance is started, the information that MetaMask uses becomes invalid. This causes some very annoying issues (see invalid block tag, invalid nonce 1, invalid nonce 2, invalid nonce 3).
- Deployment systems might use the chain id to know which previous deployments were done in each chain. Again, if you are using an ephemeral one, this is problematic. For example, if you deploy something, reset the network, and deploy it again, the second time it won’t be deployed because the system thinks it already did.

### Possible solution 1: random/incremental chain id

One approach to solving this problem is to use a random or incremental chain id, which would guarantee (or at least increase the chances) that two instances of the same ephemeral network have a different identifier.

A downside of this approach is that there’s a small but annoying possibility of using an id that corresponds to an existing chain. The probability of this happening could be reduced if we’d agree on a “reserved range” of chain ids for ephemeral networks (say, from 10.000 to 99.999).

Another problem is that this is somewhat backward-incompatible. For example, Hardhat Network’s default chain id is 31337 and Ganache’s is 1337. Changing those to a random/increasing one could break something. This doesn’t seem like an insurmountable problem though.

Another example of this approach being problematic is that, when you add a new network to MetaMask, you need to specify a (fixed) chain id. So this is not compatible with the idea of a variable chain id but, again, it’s not something that couldn’t be fixed.

### Possible solution 2: a new identifier

A second possible approach is to add a new RPC method, for example `eth_chainInstanceId` (the name is debatable) which returns a value corresponding to the network’s *instance*. If you then kill your node and start a new one, you’ll get the same id but a different chain instance id.

Non-ephemeral networks could implement this by simply returning the same value returned by `eth_chainId`.

This solution has some advantages compared to the previous one:

- It’s more backward compatible, for the reasons mentioned before.
- It doesn’t rely on an unenforceable reserved range.
- Even if not all nodes implement it, tools can use it and, if the RPC method doesn’t exist, they can just assume that the chain is not ephemeral.

---

I personally think that the second solution is better. The first one feels hackish and it’s the kind of backward-incompatibility that is very subtle (instead of things just crashing, which at least is obvious).

## Replies

**wighawag** (2021-12-03):

I agree with the sentiment as a developer and wallet like metamask could easily improve.

I created an issue for metamask here : [Whenever I restart a local network like hardhat-network metamask do not detect changes and keep caching old nonces · Issue #12211 · MetaMask/metamask-extension · GitHub](https://github.com/MetaMask/metamask-extension/issues/12211)

And in it I actually mention a solution that is similar to 2) but do not require any new rpc method:

**the genesis hash can act as network identifier already**

---

**fvictorio** (2021-12-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> the genesis hash can act as network identifier already

The hash of the genesis block? That’s a really interesting idea. Right now Hardhat has the same hash for different instances of the network, but I think we could randomize some field (like the nonce) so that the hash is different each time.

EDIT: I was getting the same hash because I was using a project that has a fixed initial date. With the default config, the hash will be different indeed.

---

**martriay** (2021-12-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fvictorio/48/3828_2.png) fvictorio:

> EDIT: I was getting the same hash because I was using a project that has a fixed initial date. With the default config, the hash will be different indeed.

I think the random nonce should go, you’ve just found a scenario where the genesis hash by itself doesn’t work.

---

**fvictorio** (2021-12-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/martriay/48/5015_2.png) martriay:

> I think the random nonce should go, you’ve just found a scenario where the genesis hash by itself doesn’t work.

Yes, but I think using the hash of the genesis block won’t be enough: if you run two different instances of a Hardhat network with mainnet forking, the hash will be the same.

---

**martriay** (2021-12-06):

right, hence adding the random nonce into the mix should work, no?

---

**fvictorio** (2021-12-08):

No, because that would mean modifying the genesis block of the forked network, and we don’t want to do that (it would be weird to modify data of the forked chain).

---

**sbacha** (2022-02-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fvictorio/48/3828_2.png) fvictorio:

> A second possible approach is to add a new RPC method, for example eth_chainInstanceId (the name is debatable) which returns a value corresponding to the network’s instance. If you then kill your node and start a new one, you’ll get the same id but a different chain instance id.
>
>
> Non-ephemeral networks could implement this by simply returning the same value returned by eth_chainId.

I really like this eth_chainInstanceId - we made custom ethers provider specific for metamask that changes its behavior (different approach and use case, but similar annoyance with metamask) [GitHub - manifoldfinance/ablative-provider: Web3 Provider for Intercepting Metamask](https://github.com/manifoldfinance/ablative-provider)

