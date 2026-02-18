---
source: ethresearch
topic_id: 10035
title: Improving security for users of DeFi services/DEXs through MPC/threshold signatures
author: ra
date: "2021-07-08"
category: Security
tags: []
url: https://ethresear.ch/t/improving-security-for-users-of-defi-services-dexs-through-mpc-threshold-signatures/10035
views: 2112
likes: 3
posts_count: 8
---

# Improving security for users of DeFi services/DEXs through MPC/threshold signatures

Excited to finally have our paper out that describes a protocol for improving security for users of DeFi services/DEXs through MPC/threshold signatures. Currently, using DeFi services/DEXs users have to trust people and devices to hold and secure secret keys that fully control their funds. Requiring such level of trust for day-to-day operations poses social and technical security risk, which is a significant limitation for professional users such as market makers, who often host their trading algorithms on cloud infrastructure and operate on shared accounts within trading firms. The protocol presented in our paper replaces the signing algorithm, operating on a single device with a secret key, with a client/server protocol that protects from the client holding the secret key as a single-point-of-failure. With the client/server protocol, the client has an API key and can generate pre-signatures that are then sent to the server, and the server will only finalize the signatures based on a security policy (and cannot generate signatures unilaterally either). A security policy can describe any computable property. For example, a policy can restrict an API key to trade on certain markets only and to withdraw funds only to a specific address, restrict access from a specific geolocation only, or require biometric information. In this way, users can provide restricted access to their funds, significantly limiting downside risk in the event their software or systems are compromised. The protocol can be applied to any existing DeFi service/DEX. We have deployed the protocol on Nash exchange as well as on Uniswap and 1inch.

We are looking forward to hearing your feedback, further use cases that come into your mind, and any questions you may have!

The full paper is published on arXiv: [[2106.10972] Improving security for users of decentralized exchanges through multiparty computation](https://arxiv.org/abs/2106.10972).

The code is available on GitHub: [nash-rust/mpc-wallet/nash-mpc at master · nash-io/nash-rust · GitHub](https://github.com/nash-io/nash-rust/tree/master/mpc-wallet/nash-mpc).

## Replies

**kelvin** (2021-07-08):

Sounds very interesting! Tried to access the paper but the link appears broken, though.

---

**ra** (2021-07-08):

Strange, it works for me. Does that one work for you? https://arxiv.org/pdf/2106.10972.pdf

---

**kelvin** (2021-07-08):

I think it may be a local DNS error here for me. I managed to access it now by going though google cache.

---

**crazybae** (2021-07-23):

Interesting and practical idea.

In fact, there are a few secure MPC-based wallets in the Ethereum eco system.

For example,

- Dekey (chrome extension, webassembly) https://www.dekey.app/   (our team ^^)
- Zengo (mobile)  https://www.zengo.com/

The most challenging points are performance in user’s platforms (Paillier enc) and usabilities (backup, …).  But there are a lot of benefits including real 2 factor authentication and no single point of failure.

---

**srw** (2023-08-06):

We implemented the Zengo MPC ECDSA TSS for WebAssembly. In this way you can run it in a browser or any platform not supporting Rust [directly]. Hope it helps to have more alternatives: [GitHub - CoinFabrik/wasm-multi-party-ecdsa: Full WASM Secure Threshold Signature ECDSA Library](https://github.com/CoinFabrik/wasm-multi-party-ecdsa/tree/main)

---

**MaxC** (2023-08-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/ra/48/6670_2.png) ra:

> Excited to finally have our paper out that describes a protocol for improving security for users of DeFi services/DEXs through MPC/threshold signatures. Currently, using DeFi services/DEXs users have to trust people and devices to hold and secure secret keys that fully control their funds. Requiring such level of trust for day-to-day operations poses social and technical security risk, which is a significant limitation for professional users such as market makers, who often host their trading algorithms on cloud infrastructure and operate on shared accounts within trading firms. The protocol presented in our paper replaces the signing algorithm, operating on a single device with a secret key, with a client/server protocol that protects from the client holding the secret key as a single-point-of-failure. With the client/server protocol, the client has an API key and can generate pre-signatures that are then sent to the server, and the server will only finalize the signatures based on a security policy (and cannot generate signatures unilaterally either). A security policy can describe any computable property. For example, a policy can restrict an API key to trade on certain markets only and to withdraw funds only to a specific address, restrict access from a specific geolocation only, or require biometric information. In this way, users can provide restricted access to their funds, significantly limiting downside risk in the event their software or systems are compromised. The protocol can be applied to any existing DeFi service/DEX. We have deployed the protocol on Nash exchange as well as on Uniswap and 1inch.

Use the internet computer for threshold signing… rather than a server.

---

**ra** (2023-08-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> Use the internet computer for threshold signing… rather than a server.

Can the internet computer sign hundreds of messages per second per CPU?

