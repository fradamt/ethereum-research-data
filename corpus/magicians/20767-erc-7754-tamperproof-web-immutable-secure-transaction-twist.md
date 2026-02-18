---
source: magicians
topic_id: 20767
title: "ERC-7754: Tamperproof Web Immutable Secure Transaction (TWIST)"
author: uni-guillaume
date: "2024-08-09"
category: ERCs
tags: [erc, wallet]
url: https://ethereum-magicians.org/t/erc-7754-tamperproof-web-immutable-secure-transaction-twist/20767
views: 347
likes: 0
posts_count: 3
---

# ERC-7754: Tamperproof Web Immutable Secure Transaction (TWIST)

Discussion for: https://github.com/ethereum/ERCs/pull/585/files

This EIP written in close collaboration with @remarks propose a new security mechanism to guarantee data integrity between dapps and wallets.

It introduces a new RPC method to be implemented by wallets, `wallet_signedRequest`, that enables dapps to interact with wallets in a tamperproof manner via “signed requests”. The dapp associates a public key with its DNS record and uses the corresponding private key to sign payloads sent to the wallet via `wallet_signedRequest`. Wallets can then use use the public key in the DNS record to validate the integrity of the payload. Wallets can subsequently confirm data integrity to their users

## Replies

**radek** (2024-08-10):

Nice. Addresses one of the attack vectors that lead to blind signing of malicious tx.

We were also considering using DNS record during ETHBrno seucirty, but rather for the browser wallet to check the hashes of the downloaded JS. (As some of the attacks were executed using injected JS to Google Tag Manager).

a) Would you expand this ERC to also consider such injections?

b) Can you elaborate more on PK handling, esp. when no BE is used?

---

**uni-guillaume** (2024-08-12):

a) would definitely be open to it. I’m not familiar with the attack you describe (are you open to DM about it so i can learn more ?) . Wouldn’t the current solution prevent a script injection via google tags ? with the private key on the backend, i don’t see how any injection could tamper with the data, but if there is a way, i am all for modifying this ERC to cover it.

b) PK handling without a backend is not really possible unfortunately, as any code injection would steal the key. We opted to focus on PK + signing on the backend in the first version of this ERC to keep it simple and comprehensive. BE signing is the most flexible and secure way to guarantee data integrity, at the cost of a somewhat expensive setup (backend endpoint to create and sign TX + key management/rotation). We have however discussed possible future improvements that would help pure front end dapps. We could CSP-like entries to the manifest, such as allow/block list of contract address the dapp can interact with, allow/block list of ERC-712 functions that can be used, etc I think your suggestion about code signing would fit very well in that approach. I am unfamiliar with the way an extension can verify the JS payload signature of a web page, but happy to learn about it in DM

