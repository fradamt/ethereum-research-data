---
source: magicians
topic_id: 1048
title: "EIP 747: wallet_watchAsset"
author: danfinlay
date: "2018-08-13"
category: EIPs
tags: [token, wallet, eip-747]
url: https://ethereum-magicians.org/t/eip-747-wallet-watchasset/1048
views: 13300
likes: 28
posts_count: 41
---

# EIP 747: wallet_watchAsset

Hi there, I wanted to get a final round of comments on `wallet_watchAsset` before we add it to MetaMask.

We’ve made a properly formatted EIP document here:



      [github.com/estebanmino/EIPs](https://github.com/estebanmino/EIPs/blob/master/EIPS/eip-747.md)





####

  [master](https://github.com/estebanmino/EIPs/blob/master/EIPS/eip-747.md)



```md
---
eip: 747
title: Add wallet_watchAsset to Provider
author: Dan Finlay (@danfinlay), Esteban Mino (@estebanmino)
discussions-to: https://ethereum-magicians.org/t/eip-747-eth-watchtoken/1048
status: Draft
type: Standards Track
category: Interface
created: 2018-08-13
requires: 1474
---

## Simple Summary

A method for allowing users to easily track new assets with a suggestion from sites they are visiting.

## Abstract

```

  This file has been truncated. [show original](https://github.com/estebanmino/EIPs/blob/master/EIPS/eip-747.md)










You can read the original discussion here:

https://github.com/ethereum/EIPs/issues/747

In particular, I’m curious to hear what people think about using a tokenImage URL as an image parameter. Is there a more secure option people can think of?

Thanks! We appreciate it! Co-authored with @estebanmino

Forgive the `fund-recovery` tag, clicking remove on it isn’t working.

## Replies

**danfinlay** (2018-08-14):

One change I might consider:

Changing the `Image` parameter to be an `Object`, with a `type` property, so that it can be forward-compatible with future (non-DNS-based) image hosting solutions.

### Example

```javascript
web3.eth.watchToken(tokenAddress, tokenSymbol, tokenDecimals {
  type: 'url',
  value: imageUrl,
})

// Leaves a path open for new formats, like swarm:
web3.eth.watchToken(otherTokenAddress, otherTokenSymbol, otherTokenDecimals {
  type: 'swarm',
  value: swarmHash,
})
```

---

**danfinlay** (2018-08-14):

Another open question: Would we want the method to declare the format of token being suggested? ERC-20 is old and dated, and we should be looking forward.

What if instead, the method was `eth_watchAsset`, and included a `format` field to describe the asset being added (like `erc-20`, or `erc-721`, even!).

### A bit more on NFTs

I don’t want to go too deep down the 721 rabbit hole, but just thinking ahead a bit:

One thing NFTs require is a special way of looking up their individual images. Adding an NFT might also include a short template string, highly restricted, that instructs the client on how to add the given NFT to the user’s wallet.

That feature might require an additional parameter, or maybe we should just pack more of these into a big, unordered `options` object. Ordered params are annoying anyways.

**Thoughts on using an options object vs a series of parameters?**

---

**jpitts** (2018-08-14):

Removed the fund-recovery tag, kind of unclear how to do that in the UI.

That tag got me to click though!

---

**MicahZoltu** (2018-08-15):

I support making this method support arbitrary asset types.  It would, presumably, include the asset type identifier (e.g., ERC20, ERC777, ERC721, etc.) and an object that includes parameters specific to that asset type.  If the wallet understands the referenced asset type, it will proceed to parse the object for details.

The method would return an error if it doesn’t understand the asset type (error response structure should be well defined so they are easy to switch on in dapps) and if the provided parameters don’t match what is expected for the asset then it would similarly error.

There may be value in creating a workflow (similar to how BIP does SLIPs) for getting new asset types registered (with their associated parameters structure).

---

**tcoulter** (2018-08-20):

This looks like a great addition.

On first glance that feels very Metamask/wallet specific, and not necessarily something a client (like Ganache or geth) should implement. Would it be better to create a new prefix, perhaps something like `metamask_watchToken` or `wallet_watchToken`?

---

**danfinlay** (2018-08-20):

I totally agree, and in fact we’ve already updated the EIP to reflect that change. I’ll now edit the subject post, too. (Was initially eth_watchToken, is now wallet_watchAsset, for those viewing after edits).

---

**boris** (2018-08-30):

I got pointed here after trying to get my BorisCoin added to MetaMask via Github PR, but I don’t have a “reputation” on EtherScan, so watching this with interest ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

Is the flow something like:

1. User visits BorisCoinDotClub with web3 enabled app
2. BorisCoinDotClub prompts web3 provider to “track BorisCoin” or similar
3. User accepts and web3 provider adds to wallet

Another thought is that this might be combined with receiving tokens in some way, but not sure how that would work.

---

**danfinlay** (2018-08-30):

Yes, the flow will be very much like that. I’ve made a simple general purpose token-adding app that people can use for suggesting their tokens (only works with our current develop branch, you can pull a recent build [like this one](https://github.com/MetaMask/metamask-extension/pull/5155#issuecomment-416715395) or take my word for it):

[Add DanCoin on Ropsten](https://metamask.github.io/Add-Token/#add?tokenAddress=0xdc1adf1d0bf59ec597e1b1b8e3dceb31aafd793f&tokenImage=https%3A%2F%2Fpbs.twimg.com%2Fprofile_images%2F723268858644037632%2Fu-kjO4___400x400.jpg&tokenName=Danbucks&tokenNet=3&tokenSymbol=DBX&tokenDecimals=2).

---

**perpetualescap3** (2018-09-04):

I like this idea for a new RPC endpoint / method! Is the proposed name `wallet_watchAsset` / `web3.wallet.watchAsset` or `eth_watchAsset` / `web3.eth.watchAsset`?

[@danfinlay](/u/danfinlay)

---

**danfinlay** (2018-09-26):

The RPC-type method would be `wallet_watchAsset`, MetaMask is initially releasing it namespaced under `metamask_watchAsset`. Generally, the web3.js library exposes underscored namespaces as objects, so that would imply `web3.wallet.watchAsset`, although this EIP reflects no official endorsement from web3.js, nor would any RPC provider be required to implement this method, since it would really only be useful at the signer/wallet layer, hence the `wallet_` namespace.

We’re trying to make `wallet_` happen, because for too long it’s been confusing when things were under eth_ whether they required a signature or not. Like `eth_sendTransaction` versus `eth_sendRawTransaction`. The namespace does not reflect the fact that one requires a signature and the other doesn’t, which is a large fundamental difference.

---

**perpetualescap3** (2018-10-05):

Thanks [@danfinlay](/u/danfinlay), this will be very useful. Great work.

---

**Amxx** (2018-11-05):

Hello,

I first heared about this EIP at Devcon when metamask presented it’s implementation and I was wondering about the hability to expand the watchAsset capability beyound ERC20 and ERC721 tokens.

I am developping smart contracts that contain an (ERC20 based) Escrow. Users can deposit tokens to the escrow using the “allow-deposit” scheme of ERC20. This increases the user balance. This balanced can be withdrawn. In the operation of the Escrow, the balanced can be locked. The locked stake will either be returned of seized depending on the users actions.

My escrow has therefore a viewAccount(address) method that returns 2 uint256 (called “stake” and “locked”). I was wondering if there is any way to have these watched using an extension to EIP747. I’m not aware of any EIP that discusses the API of escrow smart contracts, but that might be a first step.

---

**danfinlay** (2018-11-07):

That’s a very interesting and unique use case, probably meriting a fresh thread.

We are definitely planning to expand this method to include ERC721 tokens, and as you can see, we’ve kept the image rendering logic fairly open ended. Maybe once we have ERC721 support, we devise some image display logic that allowed us to render that given escrow’s contained balance.

If that seems hacky, I’m sure we could also do other things, like making escrow its own type, although I’m certain this will be slower to get all the wallets to implement (we have a long list of “asset types” that we want to integrate, so finding common types is key to getting us to cover bases).

---

**phraktle** (2019-03-13):

[@danfinlay](/u/danfinlay) there’s a UX problem that this spec does not adequately address: when the user has already added the asset (manually or through `wallet_watchAsset`), there should be a way to avoid asking them to add it repeatedly in a dApp.

IMO, this would be best achieved by specifying that a `wallet_watchAsset` should not prompt the user in case the asset is already monitored by the wallet, instead silently reporting success. This way a dApp could detect that the user has some tokens of a specific type and prompt the user to add it, which would just be a no-op in case they have already added these.

---

**danfinlay** (2019-03-14):

I think that’s a very reasonable extension.

I had also thought it might make sense to grant some sites (like etherscan, or whatever registry you prefer) permission to freely update your token list, and maybe even read from it (possibly as a separate permission).

---

**PendicGordan** (2019-05-06):

[@danfinlay](/u/danfinlay) [@phraktle](/u/phraktle) Are there any news about this feature(checking if a token already exists in Metamask)? Now it’s like very tricky for me to know that info, I must store flags in localStorage… But if localStorage is deleted or browser/machine changed, that user must again confirm the token. Or when token is manually deleted in Metamask, localStorage must be deleted. And further “Add Token” popup is not showing explicitly every time, user sometimes must go to the Metamask and only then see the popup. Additionally I must save one flag for each account. So to much complications I think, this can be very useful feature…

---

**danfinlay** (2019-05-13):

Yes, this is in MetaMask now: https://metamask.github.io/metamask-docs/Best_Practices/Registering_Your_Token

---

**3esmit** (2020-10-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> In particular, I’m curious to hear what people think about using a tokenImage URL as an image parameter. Is there a more secure option people can think of?

I think imageURL is bad, because it opens privacy concern of contacting a server everytime you open the wallet.

I would prefer that [EIP-1577 Contenthash](https://eips.ethereum.org/EIPS/eip-1577) is used, so the token image have to be downloaded from a decentralized storage.

---

**3esmit** (2020-10-19):

I think that a page should not automatically request to add token, instead a user action should be needed, so user have to press something to request add token. Otherwise it might become a vector of phishing, e.g. user open a page it starts requesting to add fake tokens. WDYT?

---

**3esmit** (2020-10-19):

Implementation discussion at Status: https://github.com/status-im/status-react/issues/10036


*(20 more replies not shown)*
