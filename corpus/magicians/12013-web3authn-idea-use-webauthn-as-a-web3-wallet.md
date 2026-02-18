---
source: magicians
topic_id: 12013
title: Web3Authn idea - use webauthn as a web3 wallet
author: vorcigernix
date: "2022-12-04"
category: Magicians > Primordial Soup
tags: [authentication]
url: https://ethereum-magicians.org/t/web3authn-idea-use-webauthn-as-a-web3-wallet/12013
views: 1241
likes: 1
posts_count: 3
---

# Web3Authn idea - use webauthn as a web3 wallet

I accidentally discovered the [WebAuthn](https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API) protocol and I can’t stop wondering why we don’t use the standard, browser supported solution instead of wallets. There is an [alternative description](https://webauthn.guide/) of how webauthn works. There are two things that need to be solved on top of an existing protocol to serve the web3 use case. First is accepting a transaction, my idea in a picture attached is that every transaction would cause re-authentication and as an app developer you will be responsible to explain what the user is signing. I understand that this could be problematic from the security perspective, but I’d argue that most people sign the gibberish anyway and the current solution is wrong anyway.

Second problem to solve is that the registration is scoped. I propose to have a simple federation server (could be ENS) that will serve as a registry, redirecting the authentication to the server where the user is registered. This is an MVP version, later we can figure out some sync mechanism - after all the private key stays on the client device, so the registration is not really security sensitive (IMO).

Please see the (super simplified) illustration that can make my idea more clear.

[![web3authn](https://ethereum-magicians.org/uploads/default/optimized/2X/9/9fa4f9852178027a5894bf9679a9d8c19d129085_2_642x500.png)web3authn4690×3652 231 KB](https://ethereum-magicians.org/uploads/default/9fa4f9852178027a5894bf9679a9d8c19d129085)

## Replies

**vorcigernix** (2022-12-04):

One thing to add, problem #3: There is no recovery key or anything like that. I have no idea how to solve it, webauthn is designed in a way that kind of removes our ability to reverse create a recovery from the private key or something like that. Maybe something like a weak multisig like smart contract can help, but my level of expertise is limiting my thoughts in the area. Will dig deeper though.

---

**vaumoney** (2022-12-05):

isn’t `--nat=extip` critically-necessary for a proper [content-security allow-list](https://github.com/ethereum/go-ethereum/issues/2765#issuecomment-1337699235) (i.e. to allow `_mint` by [RLP](https://github.com/NickCarducci/Nonce-Minter-Bot))? I think Authority by consensus can be useful for a [forgot pass minter](https://ethereum-magicians.org/t/nonce-minter-bot-for-erc20mintable-open-source-wallet-supply-recovery), *but I don’t think much else tbf*.

