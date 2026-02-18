---
source: magicians
topic_id: 27336
title: Aetrna - on-chain cloud / eSign
author: 0x000hx
date: "2025-12-28"
category: Web
tags: [on-chain-documents, post-quantum, on-chain-storage, argon2, mlkem]
url: https://ethereum-magicians.org/t/aetrna-on-chain-cloud-esign/27336
views: 38
likes: 0
posts_count: 1
---

# Aetrna - on-chain cloud / eSign

Hey guys, after a year of development we have finally released a preview version and now are looking for feedback and feature requests!

**What is Aetrna?**

It is the e2e tool to securely encrypt and permanently store any media or jointly sign docs directly on EVM without IPFS. Aetrna does not store the user data and can not see whats inside your files (its encrypted in your browser). The only identifier used is web3 wallet.

Screenshot of eSign feature:

[![image](https://ethereum-magicians.org/uploads/default/optimized/3X/d/e/de8f0d19890a63ac66a44834fbf3be5528add6b4_2_517x350.png)image1221×827 114 KB](https://ethereum-magicians.org/uploads/default/de8f0d19890a63ac66a44834fbf3be5528add6b4)

**Why care?**

Centralized apps store your data as intermediary, they can delete or censor, modify or read it, they are prone to outages and leaks.

Aetrna does not see what docs you are signing nor does it store the user data. It is built in a way to serve the user even if the app is offline decades later (you can restore the files by hand). In case of the hack, the adversary will only see the uploader wallets and metadata that is already visible on-chain. The app has no databases on backend.

**Where the files are stored?**

The data is stored in either

- calldata - split across transactions
- blobs - temporarily
- Arweave layer - for big files, no new wallets needed, subsidized by Relayer

Mental model for uploads:

[![image](https://ethereum-magicians.org/uploads/default/optimized/3X/8/1/81f2e566db263427a63bd0ba88064043ff0e020c_2_517x331.png)image776×498 106 KB](https://ethereum-magicians.org/uploads/default/81f2e566db263427a63bd0ba88064043ff0e020c)

**How does the e-sign work?**

The e-sign feature is done via delta encoding. The initiating party uploads the document, the co-signer then only uploads the delta with his signature and additional data like arbitrary text. Then on download both parts are getting concatenated to form a final document with initiator and co-signer signatures.

Mental model for e-sign:

[![image](https://ethereum-magicians.org/uploads/default/optimized/3X/6/1/61570598eaecc7d596b3f6c604e3f449e1ca7bb2_2_510x375.png)image895×657 100 KB](https://ethereum-magicians.org/uploads/default/61570598eaecc7d596b3f6c604e3f449e1ca7bb2)

**What encryption is used?**

1. ECIES (ECDH, HKDF, AES-GCM) - encrypt with just public key, decrypt with private key. Offline decryption tool is open source now. ECDH here is done with ephemeral keys, no private keys are needed from the user.
2. MLKEM (Kyber1024) - encrypt for the public key of receiver, post-quantum option. The app allows to generate a separate keypair in browser and publish the public key.
3. Argon2id - encrypt with a password, this KDF is also considered strong against quantum computers.

**What networks are supported?**

Sepolia and Base testnet.

**Whats the state of the project?**

The project started in January 2025, currently in alpha test. The next update is going to include the EIP-7212 to enable the passkeys.

**Links**

The app is – app.aetrna.cloud

Read more about how it works – docs.aetrna.cloud

Get in touch on TG and X – @aetrna_cloud

Would love to hear some feedback! Also we can spare some testnet tokens.
