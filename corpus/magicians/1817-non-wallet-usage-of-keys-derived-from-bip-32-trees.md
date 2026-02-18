---
source: magicians
topic_id: 1817
title: Non-wallet usage of keys derived from BIP-32 trees
author: bitgamma
date: "2018-11-06"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/non-wallet-usage-of-keys-derived-from-bip-32-trees/1817
views: 5775
likes: 8
posts_count: 7
---

# Non-wallet usage of keys derived from BIP-32 trees

Software interacting with the blockchain, including wallets, do not only revolve around pure asset transfer transactions but might have additional functionalities. In the case of Status that would be chat, but it can be anything like authentication, file encryption, etc. Using keys under the BIP32 tree for these purposes would allow the user to migrate the whole identity from one software to the other using the BIP39 mnemonic alone, since everything else would be derived from there.

We plan to propose a short EIP (ERC maybe?) to formalize a key subtree which would be reserved for this. I have written a draft at https://notes.status.im/UPVhoAKjT0irxIPjs5x8IA and would like to have some feedback on this before submitting it.

A short summary is that we define a separate (from the usual 44’) subtree under master and then have a key type and a key index. The format would thus be m/XXXX’/key_type’/key_index. The XXXX would be the EIP/ERC number.

The list of allocated key type must be maintained in a way similar to the allocated coin types for BIP44.

## Replies

**ligi** (2018-11-10):

Great idea! Just missing in the purpose section of the notes the thing you mention in this post:

> The format would thus be m/XXXX’/key_type’/key_index. The XXXX would be the EIP/ERC number.

---

**bitgamma** (2018-11-13):

Thanks for the feedback! I have added that explaination in the document as well now.

---

**bitgamma** (2019-01-30):

Another update to the draft, regarding the key_index field has been posted https://eips.ethereum.org/EIPS/eip-1581

---

**3esmit** (2019-10-02):

I want to just give a breakdown to clarify things. Seems like some confusion around EIP 1775, and also I suggest that we have a ERC1581+ERC1775 .

[@danfinlay](/u/danfinlay) [@Bunjin](/u/bunjin)

# ERC1581 vs ERC1775

## ERC1581:

Fix the weakness of using the same public key for ethereum address and chat key.

- “non wallet” public key
- path m/43'/60'/1581'/ [key type]' / [key_index]
- dapps can be authorized to view “chat identity” public key
- dapps can be authorized to sign messages at will “chat identity”

## ERC1775:

Fix the privacy weakness of reusing the same ethereum address for several dapps.

- dapp specific ethereum address
- path m/43'/60'/1775'/ [persona path]' / [application uniquely assigned path]' / [app's custom subpath]
- dapps can be authorized to view dapp specific eth address
- authorized dapps can request signatures for each transaction or ERC191 message

## ERC1581+ERC1775:

Fix the privacy weakness of reusing the same public key for several dapps.

- dapp specific “non wallet” public key
- path m/43'/60'/1581'/1775'/ [persona path]' / [application uniquely assigned path]' / [app's custom subpath]
- dapps can be authorized to view “dapp specific chat identity” public key
- dapps can be authorized to sign messages at will

---

**fubuloubu** (2020-05-08):

Similar proposal: [Extensible crypto for wallets](https://ethereum-magicians.org/t/extensible-crypto-for-wallets/2546)

---

**fryorcraken** (2021-09-09):

*Replied mirror in https://github.com/status-im/js-waku/issues/73#issuecomment-915782020 with links because I am not allowed more than 2 links per post as a new user*

The current proposed API in EIP1775:

```auto
const appKey = await provider.send({
  method: 'wallet_getAppKeyForAccount',
  params: [address1]
});
```

Implies that access to a dApp specific **private key** is given to the dApp. I believe this is not ideal as it means the dApp now needs to properly handle the private key.

I agree with you that it’d be ideal if the dApp could instead **request** signing/decrypting messages to the wallet, using the dedicated dApp key. Potentially using a permission based design such as EIP-2255.

However, the challenge is that the decryption/signature method provided by a wallet may not fit the dApp needs.

In regards of the signature scheme, EIP-712 could be a one-fit-all candidate.

However, in terms of decryption, we can see that various schemes are used in the ecosystem and it may be difficult to pick one:

- Metamask uses X25519_XSalsa20_Poly1305.
- Geth uses ECIES
- Waku, originating from Whisper/Geth, also uses ECIES

Another solution would be to provide a generic API that supports several encryption. An idea would be to use CryptoSubtle as the API reference and assume that in the Browser world, some of the encryption supported by Crypto Subtle should be supported by the Wallet API.

