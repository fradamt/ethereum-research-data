---
source: magicians
topic_id: 2799
title: "Dapplets: Rethinking Dapp Architecture for better adoption and security"
author: Ethernian
date: "2019-03-02"
category: Web > Wallets
tags: [wallet, ux, dapplets, dapp]
url: https://ethereum-magicians.org/t/dapplets-rethinking-dapp-architecture-for-better-adoption-and-security/2799
views: 9894
likes: 40
posts_count: 44
---

# Dapplets: Rethinking Dapp Architecture for better adoption and security

**Last Update from 25.03.2019:**

full medium article is here:

[Dapplets (part 1): introduce new  Dapp architecture for better UX and security](https://medium.com/@Ethernian/dapplets-part-1-introduce-new-dapp-architecture-for-better-ux-and-security-75a4881b4765)

Any comments and critic are welcome!

TG: [“Dapplets and Secure Signing](https://t.me/joinchat/DvCrSRPUuDP6Y8QvppyXcw)”

============

Hello all!

## 1. Look at current dapp ux critically:

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/d/dfbf815caefb58d3a1888e62f934fa56680d9915_2_565x499.png)image1253×1108 225 KB](https://ethereum-magicians.org/uploads/default/dfbf815caefb58d3a1888e62f934fa56680d9915)

We will see multiple drawbacks:

1. Wallet is unable to present all the information required for signer to make a solid accept/reject decision. The WYSIWYS principle (WhatYouSee-is-WhatYouSign) is broken now.
2. We are unable to reach web2 (legacy) sites because they do not implement any web3 logic. This is one of reasons why we are trying to reinvent wheels like twitter and facebook from scratch.

The root cause is in the Dapp architecture we have adopted from very beginning. We inject `web3` for transaction processing into the website (Dapp) which is inherently unsafe environment with very limited chances for audit. That is why we use now wallets for Tx verification, running in more secure environment than Dapps.

Dapp Architecture based on `web3` injection doesn’t support wallets properly. Lets try re-invent it.

## 2. Let us imagine better UX.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/2/22783370a3a3fc0557292fb0829ba36df2303442_2_573x500.png)image1246×1087 253 KB](https://ethereum-magicians.org/uploads/default/22783370a3a3fc0557292fb0829ba36df2303442)

Our gains:

1. We can let Wallet present exact we would like to sign. Make WYSIWYS great again
2. Because we handle Tx processing in Wallet and not in the Dapp, we can reach legacy sites like twitter now. Not all, but many of them: we need create a control injector for that.
image1370×1015 226 KB

## 3. How it could work?

We need let wallets load and render small Dapps (let us call it **Dapplets**) depending on current context and action. A Dapplet containter will make necessary security checks and audit status. More over it will present more info about Tx and Dapplet in the Header and Footer for better security.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/1/1fed675a4fa03ac679c50ae808cc5298f6b15f8d_2_654x500.png)image1680×1284 422 KB](https://ethereum-magicians.org/uploads/default/1fed675a4fa03ac679c50ae808cc5298f6b15f8d)

We will probably reuse some extended version of WalletConnect

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/8/80c2e0e8663478301d5c0cf0ad20c969c01f8157_2_661x500.png)image2014×1522 510 KB](https://ethereum-magicians.org/uploads/default/80c2e0e8663478301d5c0cf0ad20c969c01f8157)

**Disclaimer:**

There are security challenges here, but I believe they can be solved.

## Current state:

PoC based on Metamask is mostly implemented. Architecture and Security is still a hot topic.

## Summary:

A lot of thanks to [@ligi](/u/ligi) and [@pedrouid](/u/pedrouid) for review and critic.

Special thanks to [@danfinlay](/u/danfinlay) and Metamask Team for great product and their openness.

If you have any critic, please let me know. I love fail-fast.

We will come to Paris for Council, Hackathon and EthCC.

let us talk in details.

## Replies

**hellwolf** (2019-03-03):

The need for auditing makes a new type of hudle of adoption. I am curious what do you think of adding a restricted presentation layer (that it doesn’t allow mangling the original data visually) to https://github.com/ethereum/EIPs/blob/master/EIPS/eip-712.md instead?

---

**weijiekoh** (2019-03-03):

Throwing my hat in the ring here: https://github.com/weijiekoh/eip-typed-data-translation/blob/master/EIPS/eip-typed-data-translation.md

It’s an idea for a standard way to convert EIP712 typed data into natural language.

---

**Spaded** (2019-03-03):

I’m all in favor for this idea.

Just off the top of my head… can we make it as easy as:

1.Dapp sends a call to `Web3.dapplet({myDappletObj})`

```
var myDappletObj = {
    name: "MyDapp", //name of your dapp
    url: "urlOfYourDapp", //url for your domain here for general registery
    category: ERC20, //type of asset for display purposes
    message: { //your dapp object to be displayed
    asset_name: "My CryptoKitty", //optional
    asset_image: "image.com", //optional
    traits: [...]  //optional
    message: "Hello bob"  //optional for any other types
    ...///any other fields for the category types supported
    },
    trasactionObj: {...txData} //pass in normal transaction data
}
```

Where myDappletObj contains information similar to what a transaction contains, except it has **extra** data feeding it the object of the dapplet. Given the use of ERCs, we can accept ERCs transfers, general info such as names, images, ERC-721 assets, or DAO type interactions. Where every interaction is generalized and you are feeding a standard 1 of X number of possible type of widgets into the wallet.

1. Wallet then displays what was given in a limited form, just as it does with a transaction now.
2. User sees the proper info and accepts.

I’d love to see this happen.

---

**Ethernian** (2019-03-03):

Guys,

sorry for delayed response.

I am busy preparing myself for Ethereum Magicians Council tomorrow - will answer in few hours.

---

**danfinlay** (2019-03-03):

I very much like the concept, and am mostly concerned with the security of the implementation, and am interested to see the code.

---

**tbarker** (2019-03-03):

I’d see it as a more visual version of natspec notices [https://github.com/ethereum/wiki/wiki/Ethereum-Natural-Specification-Format].

I think the important thing is that it be determinable what DApplet code was running at any given block. Perhaps the default is that DApplets are immutable and deployed at the same time as the contract itself?

---

**androolloyd** (2019-03-03):

This is great, I have been working on a concept called “Smart Widgets” which sound a lot like dApplets, but they are react-native components.

The concept is similar in that expression actions should be brought to the wallet for rendering and signing and then relayed back to the network.

The end goal of giving developers access to a sandboxed environment where there is an exposed web3 object for them to interact with.

Will be following intently.

---

**Ethernian** (2019-03-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hellwolf/48/9111_2.png) hellwolf:

> The need for auditing makes a new type of hudle of adoption.

I have slightly another angle of view:

While contract audit became usual and desired, the dapp audit is still not in focus. This is because of inherent trade-off between UX and Security. Most projects currently follow User expectations and prefer UX at expenses of Security.

I proposed to extract security sensitive parts of Dapps into Dapplets which are much smaller, utilize simple UI and can be executed in restricted environment. That makes Dapplet audit even possible.

Dapplet audit could become part of contract audit and will not create additional obstacle for adoption.

If some project doesn’t not provide an audit, it could implement all UI as usual in a solid Dapp and without any Dapplets.

---

**Ethernian** (2019-03-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hellwolf/48/9111_2.png) hellwolf:

> I am curious what do you think of adding a restricted presentation layer (that it doesn’t allow mangling the original data visually) to

Yes, it could be thought as presentation layer to [EIP-712](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-712.md) although not instead, but as an additional layer.

I confirm, I need to think deeper about EIP-712, but currently I think, the EIP targets another problem: it creates unambiguously (injective) signatures, which can not be later interpreted as valid in another semantic context.

---

**Ethernian** (2019-03-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/weijiekoh/48/1659_2.png) weijiekoh:

> It’s an idea for a standard way to convert EIP712 typed data into natural language.

Yeah, It is a valuable input, thank you!

I have similar template based way of thinking about visual layer, but I would more strictly separate calculations from data. I would be interested in detailed discussion.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/spaded/48/1660_2.png) Spaded:

> Web3.dapplet({myDappletObj})
> …
> trasactionObj: {…txData} //pass in normal transaction data

I would completely replace the `txData` with json object. It makes no sense to construct `txData` in less trusted environment like Dapp in browser and then try to recover corresponding meta-data from passed `txData` in Wallet. This architecture was introduces years ago because of convenience and simplicity but it doesn’t fit security requirements and should be deprecated, IMHO.

It should be the Wallet, who should be responsible to construct txData based on parameters passed or loaded from other trusted sources.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tbarker/48/1012_2.png) tbarker:

> … and deployed at the same time as the contract itself?

I don’t think it is necessary, but `same-origin` is a good security note.

---

**tbarker** (2019-03-04):

I was imagining the DApplet being represented as a hash and loaded from IPFS. Wallet is directed to a certain smart contract, queries the contract to find the hash of the canonical DApplet, and then loads it.

---

**Spaded** (2019-03-04):

Yes ofc the data can be pulled wallet side. Was just giving an example that we would include the bare minimum that is included now, plus the extra additional data.

My concern for requiring these dapplets to be hosted or related to the smart contract, is that, once a dapp is deployed, a new dapple may be wanted to be used.

Also dapplets for 721 assets and other non traditional assets most likely need information from off chain to be included within the information passed to the dapplet

---

**Ethernian** (2019-03-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tbarker/48/1012_2.png) tbarker:

> queries the contract to find the hash of the canonical DApplet, and then loads it.

Yes, but quering the smart contract is not the only one way to get a trusted dapplet. The trust for 3rd party dapplet can be established by audit, for example.

I would like to see Dapplet audit as the part of the usual contract audit.

---

**jeluard** (2019-03-06):

Very interesting idea!

Sounds like the gist of the idea is the website logic injection. Having wallet screens sounds orthogonal and might be useful in general, but also kind of complex to spec so that all wallet implementer can agree on.

Maybe worth separating both parts?

---

**jeluard** (2019-03-06):

[@androolloyd](/u/androolloyd) I’d enjoy to know more! Anything you can share?

---

**Ethernian** (2019-03-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jeluard/48/353_2.png) jeluard:

> Maybe worth separating both parts?

Yes, you are completely right. Injection and Dapplets are quite independent parts.

---

**Ethernian** (2019-03-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/androolloyd/48/1082_2.png) androolloyd:

> This is great, I have been working on a concept called “Smart Widgets” which sound a lot like dApplets, but they are react-native components.

Yeah, in PoC implementation we are going the same direction using JSX-like compoments.

Are you in Paris now? Would like to talk about more in details. May be we could join our efforts.

---

**jeluard** (2019-03-06):

I am in Paris. Any availability this afternoon? I am [@jeluard](/u/jeluard) on telegram.

Also this thread sparkled a semi-related idea here: https://discuss.status.im/t/extensions-to-enhance-old-web/1085

---

**androolloyd** (2019-03-06):

Sadly not in Paris. Let’s grab a video call next week.

---

**hellwolf** (2019-03-06):

Going to be in Ethparis, our team is considering different projects and one of the idea is similar to this. I would love to meet you there Ethernian. telegram @miaozc


*(23 more replies not shown)*
