---
source: magicians
topic_id: 6568
title: Add QR code scanning between software wallet & cold signer (hardware wallet)
author: Lixin
date: "2021-06-29"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/add-qr-code-scanning-between-software-wallet-cold-signer-hardware-wallet/6568
views: 4500
likes: 11
posts_count: 9
---

# Add QR code scanning between software wallet & cold signer (hardware wallet)

Hi Magicians.

I am Lixin from Keystone hardware wallet. As a user, we are not satisfied with the current signing solution for DeFi (Ledger + MetaMask). We came up with a new solution for it.

## PoC

We forked MetaMask and created a [PoC for QR code signing](https://twitter.com/KeystoneWallet/status/1409465608643641347) between our hardware wallet Keystone and the browser extension.

## Motivation

- USB connectivity could break from time to time. QR code causes much less compatibility issues. Much better experience not only for users but also for developers.
- With QR code, users can easily turn their old mobile phone into a offline signing device turning on airplane mode with app like Airgap. (Note: another great QR based hww is Ngrave and they share the same opinion with us.)
- With big screen & ABI encoding, complex DeFi transactions can be fully verified on the cold signer (hardware wallet) otherwise the user is blindly trusting the software wallet which can be compromised much more easily compared to the cold signer (hardware wallet). GridPlus is fixing this vulnerability too and they are awesome.

## Importance of Composable Wallets

Personally I really agree with [Andrew Hong’s view about wallets](https://medium.com/coinmonks/1the-importance-of-composable-wallets-for-users-and-developers-accb2aadff49).

- Cold signer (hardware wallet) should be specialized on “Security Layer” in the ecosystem.
- Cold signer (hardware wallet) should be as compatible as possible with other software wallets.
- ABI encoding is an essential part for cold signer (hardware wallet).

## Next Steps

1. We are talking with MetaMask, xDeFi and GasNow for integration.
2. We will raise an EIP for the standard of QR code protocol between cold signer (hardware wallet) and software wallet. More details will be posted within this week or next.
3. Adding more ABIs to our product (firmware update is needed).

Please throw me any questions/concerns you have. All ears here ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

## Replies

**matt** (2021-06-29):

> As a user, we are not satisfied with the current signing solution for DeFi (Ledger + MetaMask). We came up with a new solution for it.

IMO, the QR flow is interesting and maybe easier for some users than connecting over USB, but it doesn’t solve what happened to the Nexus Mutual founder.

What *does* solve that is supporting ABIs in hardware wallets.

I’m curious how you guys go about adding ABIs? Does your team review ABIs for popular applications and then bundle them with your firmware? Do you allow your users to use their own ABIs? Why don’t other hardware wallets have this functionality?

---

**dstreit** (2021-06-29):

+1 For making it easier to sign from an air-gapped wallet, with much better understanding of *what* I’m signing.

Have you checked out [Parity Signer](https://github.com/paritytech/parity-signer)?

---

**Lixin** (2021-06-30):

100% agree.

With QR code, every piece of information getting in&out of the device is auditable/verifiable.



      [twitter.com](https://twitter.com/KeystoneWallet/status/1409938516579164160)





####

[@KeystoneWallet](https://twitter.com/KeystoneWallet/status/1409938516579164160)

  Announcing Keystone QR Verifier! 📢

Verifying QR codes is important, this is why we are releasing the Keystone QR Code Verifier. 🛡️

With this tool you can now brave the big unknown  when scanning QR codes. 🤠

  https://twitter.com/KeystoneWallet/status/1409938516579164160










re Parity Signer -

Yes we know it. It’s a great tool but it seems like it’s not actively maintaining (correct me if I am wrong).

For making a offline mobile phone into a cold signer, [airgap.it](https://airgap.it/) is actively working on that. And they will align their QR protocol with us so we can be compatible with the same software wallets and ETH community will have much more options.

---

**Lixin** (2021-06-30):

Thanks for those questions.

Yes. QR code only solves the problem of USB’s bad connectivity.

To solve the Nexus Mutual founder’s problem, these are needed:

- Big screen for easily verifying complex DeFi transactions.
- Embed ABIs into hardware wallet

And yes we are working on this.

From the video in the tweet you can see we embedded the ABI of Uniswap V2 and shows the details of the unsigned swap transactions. You can also check the screen shot below (we even highlighted the swap destination address if it’s not consistent with your from address).

[![How Keystone sign a Uniswap tx](https://ethereum-magicians.org/uploads/default/optimized/2X/6/64eb02b2b5d00d6e8ecdc20cbe0b5be60ddc005d_2_159x500.jpeg)How Keystone sign a Uniswap tx511×1600 104 KB](https://ethereum-magicians.org/uploads/default/64eb02b2b5d00d6e8ecdc20cbe0b5be60ddc005d)

*Does your team review ABIs for popular applications and then bundle them with your firmware?*


      ![](https://github.githubassets.com/favicons/favicon.svg)

      [github.com](https://github.com/KeystoneHQ/Keystone-cold-app/tree/main/app/src/main/assets/abi)





###



The Keystone hardware wallet application for multi-coin - KeystoneHQ/Keystone-cold-app










These are the ABIs we have added. And we are adding more.

*Do you allow your users to use their own ABIs?*

This is doable and we are researching for a proper solution for it. It needs some time because this may involve some security issues.

*Why don’t other hardware wallets have this functionality?*

Just my 2 gwei -

1. Most hwws are “stateless” design. They minimize what to store on the device. This design is kind of out-dated as blockchain develops really fast. To fully verify more and more complex transactions you have to store something more than just seed or private keys.
2. As I mentioned above, storing ABIs is not enough. UX wise, big screen is a must. It doesn’t make too much sense by just adding ABIs. This might be the reason why they are not doing this.

---

**Aaron** (2021-12-07):

Hi the ethereum magicians,  I am Aaron from Keystone Team.

These days we are working with Metamask for the integration. The integration PR has been merged. ([Introduce QR based signer into MetaMask by aaronisme · Pull Request #12065 · MetaMask/metamask-extension · GitHub](https://github.com/MetaMask/metamask-extension/pull/12065)).

We would like to propose the new ERC idea for the QR code data transmission protocol.

see here: [EIP-Draft: QR Code data transmission protocol for the Ethereum wallets by aaronisme · Pull Request #4527 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/4527)

---

**Lixin** (2021-12-07):

The integration between Keystone hardware wallet with MetaMask will be the first implementation of this drafted EIP.

The integration will be release on Dec 10th, 2021.

Here is a quick demo for the workflow - [Using MeaMask with Keystone Hardware Wallet - 100% Air-gapped Signing with QR Code - YouTube](https://youtu.be/1eM53TYG1YA)

Currently airgap.it and Ngrave are both following this EIP to be compatible with MetaMask.

---

**d10r** (2021-12-12):

Thanks for this EIP! I have a question:

Would this support the use of private keys? I have a bunch of keystore files and private keys which I’d love to airgap, but so far haven’t found a way to do so because afaik no HW wallet supports private key import. The usual recommendation is to move funds over to a new, mnemonic based, account. But for old accounts with a lot of different tokens accumulated, some of which deposited in protocols, that can easily translate to xxxx $ worth of tx fees.

My limited understanding of BIP32 and this EIP suggests it may not work with private keys either.

Is that the case? If so, is there a good reason for not supporting the use of private keys? Could the EIP be changed / extended to have that supported too?

---

**MicahZoltu** (2026-01-01):

I know this EIP is stagnant, but AirGap.it and MetaMask both implement it so understanding it is still relevant.

> If the signer would like to provide multiple public keys instead of the extended public key for any reason, the signer can use crypto-account for that.

`crypto-account` doesn’t appear to be mentioned anywhere in the EIP other than this one line, so it is unclear how a developer would go about using it.

My specific issue is that when an offline tool provides the root view key over the QR code channel, they are doxxing the user by correlating all of the accounts on the offline device together.  Ideally, the wallet will protect the user from this but in an air-gapped scenario one is generally operating under the assumption that the online device may be compromised, so any information given to it should be assumed to be given to an attacker.

If I’m reading the spec right, the way to protect user privacy with this spec is to send individual public keys (likely only one in many scenarios) over the QR code channel, rather than sending the extended public key.

If my understanding is correct, where can I learn more about how to do this?

