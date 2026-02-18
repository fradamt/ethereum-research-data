---
source: magicians
topic_id: 1586
title: 3 Proposals For Making Web3 A Better Experience
author: wighawag
date: "2018-10-15"
category: Web > User Experience
tags: []
url: https://ethereum-magicians.org/t/3-proposals-for-making-web3-a-better-experience/1586
views: 1513
likes: 3
posts_count: 1
---

# 3 Proposals For Making Web3 A Better Experience

Hi,

I am still new to the ethereum magicians but I feel this might be the best place to mention 3 proposals for web3 browsers that should improve the general web3 UX by removing unnecessary confirmations

I explained it in details here : https://medium.com/@wighawag/3-proposals-for-making-web3-a-better-experience-974f97765700

It relies on the idea that web3 browsers checks the origin of the current document before signing and derypting data.

Here is a summary of the 3 proposals:

**proposal 1 : automated decryption via checked origin injection :**

Whenever an application want to encrypt some data, it first prepend to the decrypted data, the origin(s) that would be allowed to decrypt. It then encrypt the result.

Then when an application (could be the same) want to decrypt, it request description from the web3 browser.

The web browser will

1. internally decrypt the data,
2. extract the origin
3. check if the origin of the document currently requesting decryption matches the (or one of the) origin prepended to the data.

4 a) if it matches, the data is given to the application decrypted

4 b) if it does not match, decryption is refused and the application get an error

Since,with this scheme it is impossible for an application to decrypt without being part of the allowed origin and that the application having access to the data is the one that set the allowed origin, there is no risk in making such decryption **without user confirmation**, allowing a much nicer experience.

[![automated_decryption](https://ethereum-magicians.org/uploads/default/optimized/2X/f/fa1a9827433027618735688ae4d86b24650049f6_2_556x500.png)automated_decryption935×840 15 KB](https://ethereum-magicians.org/uploads/default/fa1a9827433027618735688ae4d86b24650049f6)

**proposal 2: automated origin check on EIP712 (or other signing method)**

This proposals modifiy EIP712 slightly to (using automated origin checks by the web3 browser) add extra security by ensuring verifiers can know from which origin the user has been requested to sign. This allow the verifier to only allow origin which the user explicitly approved, bringing a new mechanism for per-application approval. This scheme also enable proposal 3.

[![origin_signature](https://ethereum-magicians.org/uploads/default/optimized/2X/a/ad0b4df8554d88671fcc15f57b7858c46f9a3ae5_2_625x500.png)origin_signature1100×880 15.2 KB](https://ethereum-magicians.org/uploads/default/ad0b4df8554d88671fcc15f57b7858c46f9a3ae5)

[![origin_verifier](https://ethereum-magicians.org/uploads/default/optimized/2X/a/ae84a814375f6b747fb4a316a09a3f5d292af2fb_2_590x500.png)origin_verifier1040×880 14.9 KB](https://ethereum-magicians.org/uploads/default/ae84a814375f6b747fb4a316a09a3f5d292af2fb)

**proposal 3: non-interactive signatures**

With this proposal (another addition to EIP712), applications can request so called “non-interactive signature” which are signature signed by the user’s private key without confirmation. These are recognizable by one of their bit/byte set to indicate non-interactivity.

While that sounds scary at first sight, this is only an option and the verifier can choose to accept those or not.

Since with proposal 2, applications cannot sign without prior-approval, applications can now provide a more seamless experience by allowing non-interactive signature for low-risks actions.

Imagine a decentralised social platform where the application’s front-end provides a form with text input and a submit button. It would be for many use cases too much for the users to confirm via an extra scary pop-up after they already pressed the “submit” button. Remember that because the origin is checked, such application’s origin would have to be approved by the users first anyway. And if the content of such origin is verifiable (IPFS, SWARM), the source code could be audited to ensure that no malicious behaviour is even possible.

[![interactive_origin_signature](https://ethereum-magicians.org/uploads/default/optimized/2X/8/83f0e25f13dc9ac8914b1555ae7fdb7a4c4d8909_2_498x500.png)interactive_origin_signature1197×1200 21 KB](https://ethereum-magicians.org/uploads/default/83f0e25f13dc9ac8914b1555ae7fdb7a4c4d8909)

![interactive_origin_verifier](https://ethereum-magicians.org/images/transparent.png)

**conclusion**

I think all of these proposals are actually objectively better that what we currently have and I would like to see them adopted as soon as possible so the general dapp’s UX get improved significantly.
