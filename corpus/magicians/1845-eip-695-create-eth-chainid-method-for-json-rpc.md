---
source: magicians
topic_id: 1845
title: "EIP-695: Create `eth_chainId` method for JSON-RPC"
author: sorpaas
date: "2018-11-08"
category: EIPs
tags: [json-rpc, eip-695]
url: https://ethereum-magicians.org/t/eip-695-create-eth-chainid-method-for-json-rpc/1845
views: 6496
likes: 14
posts_count: 26
---

# EIP-695: Create `eth_chainId` method for JSON-RPC

Discussion thread for EIP-695: https://eips.ethereum.org/EIPS/eip-695

## Replies

**ligi** (2018-11-08):

Quantity in this context feels wrong - it’s not really a quantity - it’s an ID:


      [en.wikipedia.org](https://en.wikipedia.org/wiki/Quantity)




###

 Quantity is a property that can exist as a multitude or magnitude. Quantities can be compared in terms of "more", "less", or "equal", or by assigning a numerical value in terms of a unit of measurement. Quantity is among the basic classes of things along with quality, substance, change, and relation. Some quantities are such by their inner nature (as number), while others are functioning as states (properties, dimensions, attributes) of things such as heavy and light, long and short, broad and ...

---

**pedrouid** (2018-12-04):

I think this thread is relevant for the discussion of the EIP-1637



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png)
    [EIP-1637 - Adding chainId parameter to eth_sendTransaction](https://ethereum-magicians.org/t/eip-1637-adding-chainid-parameter-to-eth-sendtransaction/2121) [EIPs](/c/eips/5)



> Following the discussion from the Wallet ring regarding a new scope of JSON-RPC methods prefixed with wallet_ to improve Wallet UX, I propose that existing signing methods such as eth_sendTransaction, eth_sendRawTransaction and eth_signTransaction would benefit a lot from a small change that would be backwards-compatible and easily changed by major JS libraries used as middleware between Dapps and Wallets

---

**pedrouid** (2019-05-21):

Is there any reason this EIP is still `Draft`? cc [@sorpaas](/u/sorpaas)

---

**sorpaas** (2019-06-20):

Just moved EIP-695 to last call status (https://github.com/ethereum/EIPs/pull/2128) with a review period of 4 weeks. Any comments appreciated!

---

**sorpaas** (2019-06-20):

I think it’s just naming convention for Ethereum JSON-RPC. We probably should have named everything as “Hex Numbers”, but for historical reasons they’re all named “QUANTITY” in current JSON-RPC docs.

---

**fulldecent** (2019-06-22):

I have completely reviewed this EIP and fully endorse it to go to FINAL status as is.

One potential improvement is this minor correction https://github.com/ethereum/EIPs/pull/2133

---

**fulldecent** (2019-07-29):

Isaac Ardis, Wei Tang, Fan Torchz, can we please get a PR to move to final here if you will proceed?

---

**fubuloubu** (2019-07-29):

This EIP is more relevant considering EIP-1344’s inclusion into Istanbul, which will define a client-side configuration value that is available internally to the EVM, to which this proposal can make use of.

Discussion here: [EIP-1344: Add chain id opcode](https://ethereum-magicians.org/t/eip-1344-add-chain-id-opcode/1131)

---

**fubuloubu** (2019-08-01):

Just noticed that, like EIP-1344, it should probably be included in the rationale that the client needs to independently provide the value of Chain ID instead of looking it up from the latest signed transaction. Transactions currently have a corner case where both EIP155 compliant and non-EIP155 compliant transactions will validate, so this is not a reliable source of this value, but rather should be checked against the internally-provided configuration of chain ID.

---

**fulldecent** (2019-08-07):

Yo what’s up here…

---

**fubuloubu** (2019-08-07):

I believe both Parity and geth implement this endpoint, so it could probably get finalized on the next ACD call?

Edit: one thing to note is that the quantity should be a uint256 because of the opcode and the future potential scenario where it could be a 32 byte hash.

---

**ajsutton** (2019-08-07):

Pantheon also supports it and I believe MetaMask is already using it. I’m a little surprised this isn’t already final to be honest.

And the spec does explicitly reference the “configured chain ID” although admittedly the meaning of that felt a lot clearer prior to all the discussions around the CHAINID opcode.  Mostly because this JSON-RPC method doesn’t execute in the context of a transaction, it’s a big leap to jump to picking some unspecified transaction from the chain and getting the chain ID from there.

---

**fubuloubu** (2019-08-07):

That discussion largely evolved into *not* having chain ID be set from a transaction, for the specific reason that it’s necessary to validate the EIP-155 `v` value against some configuration anyways. So, this EIP and EIP-1344 should just returned the configured setting from the client, as I believe they already do.

---

**rekmarks** (2020-03-30):

Is anyone trying to bring this over the finish line at the moment? As [@ajsutton](/u/ajsutton) noted back in August, MetaMask is already using this.

An unfortunate development while this EIP has been in last call is that some widely used resources in the community have started to list `chainId`s as decimal numbers, for instance [chainId.network](https://chainid.network/).

At MetaMask, we’re inclined to continue returning a hex string per this EIP. Perhaps [@pedrouid](/u/pedrouid) or [@ligi](/u/ligi) could comment in their capacity as contributors to chainId.network?

---

**ligi** (2020-03-30):

What drawback do you see in chainid.network using decimal? It can be converted easily …

---

**rekmarks** (2020-03-30):

In that case, I take it your intention was not to be prescriptive? I’m fine with that.

Then the remaining question is whether anyone is championing this.

---

**ligi** (2020-03-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rekmarks/48/1626_2.png) rekmarks:

> In that case, I take it your intention was not to be prescriptive?

no - that was not the intention.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rekmarks/48/1626_2.png) rekmarks:

> I’m fine with that.

great!

---

**pedrouid** (2020-03-31):

Basically going to repeat what [@ligi](/u/ligi) said already. The chainId’s on `chainid.network` using decimal is purely informative.

I agree that `eth_chainId` JSON-RPC response should be in hexadecimal format. In fact, that should just be a rule for all values of Ethereum’s JSON-RPC API.

---

**ligi** (2020-04-09):

it could make sense to to specify exactly what “describing the currently configured  `CHAIN_ID`” means. As there are 2 edge cases:

- what is with chains that did not start with EIP-155
- what is with chains that changed the chainID in a fork

this was leading to an issue here:



      [github.com/ethereum/go-ethereum](https://github.com/ethereum/go-ethereum/issues/20894)












####



        opened 06:54AM - 06 Apr 20 UTC



          closed 09:52AM - 12 Jan 21 UTC



        [![](https://avatars.githubusercontent.com/u/3258675?v=4)
          nicinuse](https://github.com/nicinuse)










Hi there,

I am trying to set up a chainlinnk node with latest stable geth cli[…]()ent, but it fails vecause of missing chainId value.

#### System information

Geth version:
```
Geth
Version: 1.9.12-stable
Git Commit: b6f1c8dcc058a936955eb8e5766e2962218924bc
Git Commit Date: 20200316
Architecture: amd64
Protocol Versions: [65 64 63]
Go Version: go1.13.8
Operating System: linux
GOPATH=
GOROOT=/usr/local/go
```
OS & Version:
````
Alpine Linux
```
Commit hash : (if `develop`)

#### Expected behaviour
Return the correct chainId

#### Actual behaviour
ChainId is always "0x0" (not available)

#### Steps to reproduce the behaviour
Run geth with
```
geth --testnet --nousb --rpc --rpcaddr '0.0.0.0' --rpcvhosts '*' --rpccorsdomain '*'
```
Ask for chainId
```
curl -k -X POST -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","method":"eth_chainId","id":1}' http://localhost:8545
```












Also I think we should add eth_chanId to: [JSON RPC · ethereum/wiki Wiki · GitHub](https://github.com/ethereum/wiki/wiki/JSON-RPC)

---

**rekmarks** (2020-04-24):

[@ligi](/u/ligi) do you recommend that 695 should revert to Draft based on those concerns, or are you just noting them for posterity?


*(5 more replies not shown)*
