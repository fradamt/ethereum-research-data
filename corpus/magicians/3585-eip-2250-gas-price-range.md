---
source: magicians
topic_id: 3585
title: "EIP-2250: Gas Price Range"
author: tomhschmidt
date: "2019-08-26"
category: EIPs
tags: [wallet]
url: https://ethereum-magicians.org/t/eip-2250-gas-price-range/3585
views: 2601
likes: 9
posts_count: 11
---

# EIP-2250: Gas Price Range

Link to PR: [EIP-2250 : Gas Price Range by tomhschmidt · Pull Request #2250 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/2250)

Hi all! This EIP came from many discussions with wallet and dApp teams, and a lot of in-depth data analysis to understand user behavior at scale.

## Replies

**tomhschmidt** (2019-08-26):

Thanks to [@danfinlay](/u/danfinlay) for the inspiration and [@Recmo](/u/recmo) for early feedback

---

**danfinlay** (2019-08-27):

Really my only issue with this is that it adds a whole new method for what seems like should amount to some extra specificity/parameters on the existing `eth_sendTransaction` method.

Maybe a second options object after the main tx params could specify required traits of that parameter? Something like this?:

```javascript
const txHash = await provider.send({
  method: 'eth_sendTransaction',
  params: [ normalTxParams,
    {
      gasPrice: {
        max: '10',
        min: '200',
      }
    }
  }]
})
```

That params-settings object could also exist on another key in the current `txParams`.

```javascript
const txHash = await provider.send({
  method: 'eth_sendTransaction',
  params: [{
    ...normalTxParams,
    paramRequirements: {
      gasPrice: {
        max: '10',
        min: '200',
      }
    }
  }]
})
```

---

**tomhschmidt** (2019-08-27):

Hah [great minds something something](https://github.com/ethereum/EIPs/pull/2250#issuecomment-525145345) ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

I originally spec’d it as an extension to `eth_sendTransaction`, but worry that it breaks the current paradigm of all params being sent into `eth_sendTransaction` being encoded, hashed, and signed as the range params would be stripped out beforehand.

I like the optional params concept, but again, worry that this introduces a totally new paradigm. Is there any precedent for something like this?

I do like the “cleanliness” of `eth_proposeTransaction` – just a supplementary function that providers need to implement and care about, but is ultimately just an abstraction on top of `eth_sendTransaction`, but also worry that it might open the floodgate for everyone wanting their own JSON RPC fn.

---

**danfinlay** (2019-08-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tomhschmidt/48/2196_2.png) tomhschmidt:

> I originally spec’d it as an extension to eth_sendTransaction , but worry that it breaks the current paradigm of all params being sent into eth_sendTransaction being encoded, hashed, and signed as the range params would be stripped out beforehand.
>
>
> I like the optional params concept, but again, worry that this introduces a totally new paradigm. Is there any precedent for something like this?

Today, wallets like MetaMask generally will set the `nonce` for the user, as well as letting the user customize the `gasPrice` before signing it, so there is indeed precedent for signing something slightly different than what the application initially suggests.

Adding a `paramRequirements` parameter could allow applications to be much more specific about which parameters are safe to modify, and which must be constrained to certain values to deliver their intended functionality.

---

**mcdee** (2019-08-28):

Wouldn’t it make sense to decouple this entirely from a given transaction?  If you want to include a transaction in a given number of blocks, and assume that the next *n* blocks will look roughly the same as the last *n* blocks, then you should be able to provide `(gas, n)` to an RPC method and receive `gas price` in return.  It would then be up to the wallet to provide this to the user, worry about if it fell within the acceptable bounds the user has specified, *etc*.

---

**shemnon** (2019-08-29):

How does this interact with [EIP-1559](https://eips.ethereum.org/EIPS/eip-1559), the proposed fee market change? It seems like there is a lot of overlap even though mechanisms and layers are different.

---

**tomhschmidt** (2019-08-29):

Yeah, I like this a lot. Gas price estimation (how we actually get to these params) is a whole can of worms. Most people use ethgasstation today, but naturally, their estimations are just a best guess and are a bit raw – to your point, most people think “This txn needs to get mined in the next minute” and it would be nice to build an interface that lets them put something like that in and spit out something that can be used to generate a transaction (gas price).

Ultimately, I think something like this would be *extremely* welcome as a utility / helper function to generate the value for these parameters, but for sake of determinism, I think still allowing dApps to pass in raw gas price bounds is a level of abstraction we need to expose.

---

**tomhschmidt** (2019-08-29):

Good callout! Definitely similar, to your point. My understanding of EIP-1559 is that it’s more designed to cap the sometimes out-of-control gas price auction and dampen gas price fluctuations across blocks. There’s some partial overlap in that this EIP could be used to allow dApps to put a gas price ceiling into their application, but it’s much more limited in scope in that it exists at the wallet level (before the txn is signed) and is only relevant for users of that app that are using a wallet which respects the EIP. Purely anecdotal, but most of the transactions that I’ve seen driving up gas prices on Ethereum are coming from trading bots trying to frontrun each other to snag some juicy opportunities. See: http://frontrun.me/

This EIP also includes gas price flooring, which is more important for the problem that we’re trying to solve for of users setting far too low of a gas price to get mined in a reasonable amount of time.

---

**mcdee** (2019-08-31):

[Ethereal](https://github.com/wealdtech/ethereal) works along the idea outlined above, where gas price can be determined based on these criteria, for example:

```auto
$ ethereal gas price --blocks=5 --gas=4000000
3.4 GWei
$ ethereal gas price --blocks=10 --gas=200000
1.1 GWei
```

Shouldn’t be hard to take the code and turn it in to some sort of web page / API.

---

**tomhschmidt** (2019-09-04):

Yeah, this is really nice. I do think gas price estimation is a related, but separate issue. We’re trying to make sure that when a dApp sets an appropriate suggested gas price (however that is obtained, such as through the Ethereal method that you mentioned) that users do not then go and mess with it, unintentionally ruining the UX.

