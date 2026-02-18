---
source: magicians
topic_id: 5469
title: "EIP-3085: wallet_addEthereumChain"
author: rekmarks
date: "2021-03-04"
category: EIPs > EIPs interfaces
tags: [json-rpc]
url: https://ethereum-magicians.org/t/eip-3085-wallet-addethereumchain/5469
views: 8353
likes: 14
posts_count: 11
---

# EIP-3085: wallet_addEthereumChain

This topic is for discussing EIP-3085. Discussion was originally located at [this GitHub issue](https://github.com/ethereum/EIPs/issues/3086) on the EIPs repository.

Discussion is expected to pick up again as 3085 moves to Review and then Last Call.

## Replies

**rekmarks** (2021-03-04):

A draft PR is up for a related method, `wallet_switchEthereumChain`: https://github.com/ethereum/EIPs/pull/3326

---

**MicahZoltu** (2021-03-05):

Instead of `decimals`, consider requiring a scaling factor instead.  This would allow chains that have scaling factors other than base 10 to be supported.  Ethereum would be `10^18` but other-chain may be `2^32`.

---

**rekmarks** (2021-03-05):

Oh, interesting idea. Something like `scalingFactor: string` matching RegEx `/[1-9]\d*\^[1-9]\d*/`? Or maybe `scalingFactor: [base: number, exponent: number]` where the tuple members are positive integers?

Then we could make `scalingFactor` mutually exclusive with `decimals`.

---

**MicahZoltu** (2021-03-05):

Scaling factor can just be a `QUANTITY` (hex string encoded number).  No need for anything fancy here I think.

---

**rekmarks** (2021-03-05):

Ah, naturally. I’ll PR that in the morning ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=9)

---

**poojaranjan** (2021-03-09):

Watch an overview of the proposal with [@rekmarks](/u/rekmarks)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/5/58722b5bce577b429720b91c8375cf0738a4f9c3.jpeg)](https://www.youtube.com/watch?v=nOIl2w33sGU)

---

**totoptech** (2021-03-29):

Hello,

I am facing an issue while calling wallet_addEthereumChain.

I will appreciate it if you can help me to fix this issue.

ethereum.request({

method: ‘wallet_addEthereumChain’,

params: [{

“chainId”: “0x3”,

“chainName”: “Ropsten Network”,

“rpcUrls”: [

“https://ropsten.infura.io/v3/4ee71c3a70404cf8b1241df95bbc1347”,

],

“iconUrls”: [

“https://raw.githubusercontent.com/trustwallet/assets/master/blockchains/ethereum/assets/0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0/logo.png”

],

“nativeCurrency”: {

“name”: “ETHER Token”,

“symbol”: “ETH”,

“decimals”: 18

}

}]

And this is the issue:

[![image](https://ethereum-magicians.org/uploads/default/original/2X/d/d034d0ccf42b2b3d813f1db4c42784ae6805ee92.png)image480×202 59.1 KB](https://ethereum-magicians.org/uploads/default/d034d0ccf42b2b3d813f1db4c42784ae6805ee92)

Thanks in advance.

---

**totoptech** (2021-03-29):

Actually, I added blockExplorerUrls to the params. Sorry to forgot adding it to the code.

“blockExplorerUrls”: [

“https://ropsten.etherscan.io”

],

FYI, I confirmed that my Infura Project ID is working. This issue is definitely related to the “rpcUrls”.

When I change it to “https://dai.poa.network” with xDAI Chain, it perfectly worked.

---

**samuel-casey** (2021-10-06):

I imagine you figured this out by now, but:

`wallet_addEthereumChain` doesn’t (or at least originally didn’t) support switching to a default network (any Ethereum network like Mainnet, Ropsten, etc.)

Now you can use a combination of `wallet_addEthereumChain` and `wallet_switchEthereumChain` in your dapp to add new networks for users if they do not have it in their MM already, and switch back to default chains like Ropsten afterwards.

You can read more here:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/3326)














####


      `master` ← `rekmarks:3326-create`




          opened 11:32PM - 04 Mar 21 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/5/5d3d47808b8c88c0682f2ef6ff0be22de49565a6.png)
            rekmarks](https://github.com/rekmarks)



          [+130
            -0](https://github.com/ethereum/EIPs/pull/3326/files)







This PR adds EIP-3326, specifying the `wallet_switchEthereumChain` RPC method.
[…](https://github.com/ethereum/EIPs/pull/3326)
Link to rendered file: https://github.com/rekmarks/EIPs/blob/3326-create/EIPS/eip-3326.md

---

**taylorjdawson** (2024-03-19):

I’m finding the wording in this EIP a bit puzzling, particularly around the `rpcUrls` field’s requirements.

Initially, the document states:

```auto
Only the chainId is required per this specification, but a wallet MAY require any other fields listed, impose additional requirements on them, or outright ignore them.
```

However, later on, it asserts:

```auto
The wallet MUST reject the request if the rpcUrls field is not provided, or if the rpcUrls field is an empty array.
```

Moreover, the parameter interface is described as follows:

```auto
interface AddEthereumChainParameter {
  chainId: string;
  blockExplorerUrls?: string[];
  chainName?: string;
  iconUrls?: string[];
  nativeCurrency?: {
    name: string;
    symbol: string;
    decimals: number;
  };
  rpcUrls?: string[];
}
```

From my understanding, this suggests a wallet “MAY” need the `rpcUrls` fields, yet it also states a wallet “MUST” reject requests lacking the `rpcUrls` field. This seems contradictory to me. If this isn’t a contradiction, perhaps the wording needs clarification to explain why this isn’t the case. Could there also be an explanation or scenario where a wallet could function without an `rpcUrl` , if such a situation is feasible?

