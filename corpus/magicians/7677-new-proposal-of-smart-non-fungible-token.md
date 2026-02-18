---
source: magicians
topic_id: 7677
title: New proposal of Smart Non Fungible Token
author: Arcenegui
date: "2021-12-03"
category: Magicians > Primordial Soup
tags: [nft, token]
url: https://ethereum-magicians.org/t/new-proposal-of-smart-non-fungible-token/7677
views: 3671
likes: 4
posts_count: 9
---

# New proposal of Smart Non Fungible Token

The novelty introduced in this EIP is the proposal of smart Non-Fungible Tokens (NFTs), named as SmartNFTs, to represent smart assets such as IoT devices, which are physical smart assets. Smart assets can have a blockchain account (BCA) address to participate actively in the blockchain transactions, they are also identified as the utility of a user, they can establish secure communication channels with owners and users, and they operate dynamically with several operating modes associated with their token states. A SmartNFT is physically bound to a smart asset, for example an IoT device, because the device is the only one able to generate its BCA address from its private key. The physical asset is the only one in possesion of its private key. This can be ensured, for example, if the IoT device does not store the private key but uses a Physical Unclonable Function (PUF) that allows recovering its private key. SmartNFTs extend ERC-721 non-fungible tokens (which only allow representing assets by a unique identifier, as a possession of an owner).

A first version was presented in a paper of the Special Issue **Security, Trust and Privacy in New Computing Environments)** of **Sensors** journal of **mdpi** editorial. The paper, entitled **Secure Combination of IoT and Blockchain by Physically Binding IoT Devices to Smart Non-Fungible Tokens Using PUFs**. This paper is available: **[Sensors | Free Full-Text | Secure Combination of IoT and Blockchain by Physically Binding IoT Devices to Smart Non-Fungible Tokens Using PUFs](https://doi.org/10.3390/s21093119)**

## Replies

**mryalamanchi** (2022-02-14):

The EIP seems to require an ESP32 device running a firmware, but the source code for the same isn’t provided.

It will be required for anyone to test out the PoC and reproduce the results.

---

**SamWilsn** (2022-04-05):

Gotta say, this is really cool stuff!

One non-formatting related question: is it possible to drop the private key entirely and use a challenge-response protocol instead? Even though the minute manufacturing differences in the device aren’t cloneable, it might be possible to extract the private key (either through software hacks, side-channel attacks, etc.) Since smart contracts are programmable, you don’t necessarily need to use an ECDSA signature to authorize an action.

---

**lumi2018** (2022-05-26):

If the objective is to authenticate the device, a challenge-response protocol can be used. Another protocol that can be used is a zero-knowledge protocol based on the LPN problem, which is very simple for a low-cost device. See, for example:

https://www.sciencedirect.com/science/article/abs/pii/S2542660518301124

In case the device needs signing messages, then a private key and a digital signature algorithm is required.

---

**j540** (2022-07-26):

Is the POC source code for the ESP32 available? I am interested in reproducing the results of the demonstrated POC.

---

**Arcenegui** (2022-07-27):

It is available [here](https://github.com/ethereum/EIPs/tree/master/assets/eip-4519/ESP32_Firmware)

---

**asac** (2022-11-28):

Thanks for your effort on this. Could you elaborate the “timeout” element of your spec a bit? From the reference implementation it is not clear to me what happens after the timeout and how the lifecycle of the token continues…

---

**Arcenegui** (2022-12-09):

The timeout element is just to notify that something is wrong with the asset. When an asset updates the timestamp, it depends on the specifications of each project that happens with the token, if it works again as before or the token is considered extinct, among other options.

---

**j540** (2023-09-27):

Where can I follow the adoption status of this standard? Sorry if that’s a very simple question, I am primarily a hardware engineer, not a blockchain contributor, so please excuse me.

