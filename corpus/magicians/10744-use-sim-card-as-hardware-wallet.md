---
source: magicians
topic_id: 10744
title: Use SIM card as hardware wallet
author: Evonne
date: "2022-09-08"
category: EIPs
tags: [hardware-wallet]
url: https://ethereum-magicians.org/t/use-sim-card-as-hardware-wallet/10744
views: 2170
likes: 13
posts_count: 8
---

# Use SIM card as hardware wallet

Hi Magicians,

The SIM card can be used to store wallet keys; it would be like metamask through the SIM card, a SIMgap solution to utilize SIM hardware chip to secure the private keys.

**PoC**

A SIM card with a custom Java SIMgap applet that uses the STK (SIM Tool Kit) menu to ask for user PIN to confirm signature requests

Android APP using Android built-in APIs to construct requests to the SIMgap applet

iOS APP using BIP (Bearer Independent Protocal) to request the SIMgap applet for performing transactions.

**Motivation**

On mobile phones, software wallets are convenient to use but potentially insecure and cumbersome to move to a new device; hardware wallets, while secure, are expensive or requires additional cables or hardware if not unsupported at all.

The SIM card seems like a perfect solution: a piece of secure hardware controlled by the user that is always in the phone and can be moved between devices.

**Next Steps**

Try for an EIP to define the standard between the SIM and APP.

## Replies

**denglinlu** (2022-09-15):

Hey, it’s great, I like to hear you would implement secure hardware wallet solution and you have done PoC. Including you will try to propose EIP to define the standard between the SIM and APP and I would like to hope coming soon.

---

**cjpais** (2022-10-03):

Have you considered using something like a TPM or Secure Enclave as well? This is something that a considerable amount of modern devices have built into the hardware and extend outside of the phone compute environment.

---

**lanlan3322** (2022-10-04):

Great idea. Just wondering why there is no giant like Apple, or Samsung doing this. it should be super easy for them to integrate this.

---

**high_byte** (2022-10-04):

funny, some months ago I thought about this exact thing.

I wouldn’t go as far as saying it’s perfect, but it is a nice to have option.

it was a bit difficult researching the subject, it also seems that information like IMSI is encoded by the manufacturer and is kept in a database. other information like contacts is readable from the mobile device, so that’s no good. I’m not sure if there’s a trivial way to encode a key securely on a SIM.

the other option mentioned here is secure enclaves, Trusted Execution Environment (TEE), etc.

I wonder if existing wallets already implement this?

---

**Evonne** (2022-10-06):

The key advantage of using SIM as hardware wallet is the removable feature from the mobile devices. Dependencies on the phone manufacturers would involve complications about compatibility, portability and universal certification for security. SIM wallet can be open souce with its applet design, which shares different security domain with other SIM functions by firewalls implemented by javacard framework.

SIM can be an “open device wallet” which is compatible with mobile phones, as well as cold wallet and airgap devices which can provide a standard SIM slot. When SIM were introduced in the mobile network while motorola was still dominating the mobile phone supply, the phone devices started to diversify with so many popolar branded manufacturers. We are looking forward to seeing the same advancements in web3 with more hardware wallet suppliers other than Ledger and Trezor for more advances use cases.

---

**lanlan3322** (2022-10-26):

SIMs are also controlled by telecom giants and providers which vary from country to country. We need open-source SIM standards adopted by telecom providers. They are able to block SIMs to enter the network that is not authorized by them.

---

**high_byte** (2024-01-18):

yes but the sim also has storage and processing.

just like IMSI or contacts that can be stored on a SIM, encode a private key.

except the key shouldn’t be readable from the OS, it should behave like a hardware signing wallet.

