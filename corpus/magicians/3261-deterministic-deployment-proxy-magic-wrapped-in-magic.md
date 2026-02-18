---
source: magicians
topic_id: 3261
title: "Deterministic Deployment Proxy: Magic wrapped in magic"
author: MicahZoltu
date: "2019-05-11"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/deterministic-deployment-proxy-magic-wrapped-in-magic/3261
views: 2284
likes: 12
posts_count: 9
---

# Deterministic Deployment Proxy: Magic wrapped in magic

https://github.com/Zoltu/deterministic-deployment-proxy

TL;DR: Ethereum contract deployed with a one-time-use account (so it has a deterministic address) that can be used to deploy arbitrary contracts via CREATE2 (so they end up with deterministic addresses).

This allows anyone to deploy a contract to any EVM chain and be sure that the contract lives at the same address on every chain.  Similar to how EIP-1820 was deployed, but without the need to hard-code gas-price and gas-limit.

## Replies

**boris** (2019-05-11):

This is definitely magic magic. Thanks for sharing [@MicahZoltu](/u/micahzoltu)!

---

**jpitts** (2019-05-11):

So many potential cross-chain applications, including ERC-725 identity which now uses proxy contracts.

https://erc725alliance.org/

---

**MicahZoltu** (2019-05-12):

I updated the code to use Yul, which brought costs down a bit.

Yul source:

```auto
object "Proxy" {
	// deployment code
	code {
		let size := datasize("runtime")
		datacopy(0, dataoffset("runtime"), size)
		return(0, size)
	}
	object "runtime" {
		// deployed code
		code {
			calldatacopy(0, 0, calldatasize())
			mstore(0, create2(callvalue(), 0, calldatasize(), 0))
			return(12, 20)
		}
	}
}
```

The signed deterministic deployment transaction is now:

```auto
f8748085174876e800830186a08080a3601580600e600039806000f350fe366000600037600036600034f56000526014600cf31ba02222222222222222222222222222222222222222222222222222222222222222a02222222222222222222222222222222222222222222222222222222222222222
```

The init code for the proxy contract is now:

```auto
601580600e600039806000f350fe366000600037600036600034f56000526014600cf3
```

The deployed proxy’s code is now:

```auto
366000600037600036600034f56000526014600cf3
```

---

For fun, I was able to gas golf the deployment code to:

```auto
6f3d36363d3d373d34f53d526014600cf33d5260106010f3
```

and the proxy code to:

```auto
3d36363d3d373d34f53d526014600cf3
```

However, I decided there was value in having Yul source code available for the deployed contract rather than just raw bytecode, so I decided to eat the extra size and costs (they are marginal).

---

**MicahZoltu** (2019-05-12):

Another nice thing about the switch to Yul is that deploying contracts is now done by supplying *only* the deployment bytecode as transaction data and put the proxy as the `to`.  This means you can take a normal deployment transaction and *only* change the `to` field on it from `null` to the proxy address (currently `0xb8744b44784dab81e6ab1e73ea3faa47887157b6`) and it will deploy via the proxy.

---

**PaulRBerg** (2021-08-29):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> This means you can take a normal deployment transaction and only change the to field on it from null to the proxy address (currently 0xb8744b44784dab81e6ab1e73ea3faa47887157b6) and it will deploy via the proxy.

Is this because the “runtime” object from above behaves as a fallback function? Otherwise I don’t see how you could take a deployment tx as it is and not have to compute the function selector.

---

**MicahZoltu** (2021-08-29):

The proxy isn’t written in Solidity, it is written in Yul, so we don’t have to play by the normal rules.  ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=10)

It is Solidity that has the concept of “parameters” and “ABI”.  Yul being just assembly more or less doesn’t have any higher level primitives like that.  Your contract can reference `calldata` via the opcode, but there is no automatic interpretation of it.

---

**Honour-d-dev** (2024-07-06):

Hi, [@MicahZoltu](/u/micahzoltu), what did you mean as a ‘one-time-use account’

---

**MicahZoltu** (2024-07-07):

You create a transaction and then make up a signature (e.g., 0xaaaaaaaa…aaaaa), then “recover” the address from it.  You don’t have the private key, so you can not sign any additional transactions from that address, it can only ever submit that one transaction.

