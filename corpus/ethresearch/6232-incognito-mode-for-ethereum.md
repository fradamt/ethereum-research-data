---
source: ethresearch
topic_id: 6232
title: Incognito mode for Ethereum
author: duy
date: "2019-10-02"
category: Privacy
tags: [layer-2]
url: https://ethresear.ch/t/incognito-mode-for-ethereum/6232
views: 10782
likes: 21
posts_count: 17
---

# Incognito mode for Ethereum

[Incognito](https://incognito.org/sidechain) is a privacy blockchain.  This post presents the fully decentralized Incognito-Ethereum bridge that allows anyone to send, receive and store ETH/ERC20 tokens with complete privacy.  Our team would love to get everyone’s feedback on the bridge design and implementation.

[READ THE FULL PAPER HERE](https://medium.com/@incognitochain/incognito-mode-for-ethereum-e0bbae096eaf).

Our team will be at Devcon next week to if you want to connect and chat in person.

Thanks!

![ec4181f%20(1)](https://ethresear.ch/uploads/default/original/2X/1/1f795122d73dd5917891341de27cd909ad0976a1.svg)

## Replies

**vbuterin** (2019-10-03):

Is this just a two-way atomic swap system, with the Incognito blockchain itself supporting ZK transfers internally?

---

**duy** (2019-10-03):

–

re: atomic swap system

it’s actually a two-way relay bridge that lets you transfer assets from ethereum to incognito and vice versa.  when someone converts ETH to pETH (private ETH), they aren’t swapping their asset with someone else’s. instead, ETH is locked in a smart contract and new pETH is minted on incognito. When the pETH are burned (to maintain a 1:1 ratio), the locking contract on ethereum will verify the validity and unlock it upon submission of burn proof.

for example, you can convert 1000 “public” DAI (on ethereum) to 1000 “private DAI” pDAI (on incognito) via ethereum → incognito relay.  once you have 1000 pDAI, on the incognito chain, you can send 500 pDAI to alice privately, send 300 pDAI to bob privately, and then convert the remaining 200 pDAI back to “public” DAI whenever you want via incognito → ethereum relay.

[![qfwuY4jv3_TQWsAPmImJOTEplPKEV6aPuTX4XSfM_3yJieiGpv5XbE7-yvdy7Qz6yvsu03xTi98sIgtDl0Y-rHF2w43Vs62afG1S3eMsGkGe5RuEzMTOnFy1eKiMKwIkYFEs7V7Q](https://ethresear.ch/uploads/default/optimized/2X/8/8b800fb807512dc957c7c4b4d9e30a846fd11ce1_2_690x388.png)qfwuY4jv3_TQWsAPmImJOTEplPKEV6aPuTX4XSfM_3yJieiGpv5XbE7-yvdy7Qz6yvsu03xTi98sIgtDl0Y-rHF2w43Vs62afG1S3eMsGkGe5RuEzMTOnFy1eKiMKwIkYFEs7V7Q1600×901 180 KB](https://ethresear.ch/uploads/default/8b800fb807512dc957c7c4b4d9e30a846fd11ce1)

–

re: support ZK transfers internally

yes, but not just that, incognito makes private transactions run fast too.

on the client side, incognito implements ZK proof generation for android and ios (so users can generate ZK proof under 15s right on their phone).

on the blockchain side, incognito implements a full-sharded architecture (based on to omniledger).  currently on the testnet, incognito is running with 1 beacon chain and 8 shards (32 nodes per shard).  we hope to scale it to 64 shards (with 100 nodes per shard) in november.

[READ THE BRIDGE DESIGN](https://medium.com/@incognitochain/incognito-mode-for-ethereum-e0bbae096eaf)

[READ THE BRIDGE CODE](https://github.com/incognitochain/bridge-eth)

[READ THE ZKP FOR MOBILE CODE](https://github.com/incognitochain/privacy-js-lib)

let us know what you think!

---

**mkoeppelmann** (2019-10-03):

The most interesting/challenging part of sidechains is always the part of brining assets back to Ethereum.

Effectively ETH/tokens here are held in a “m/n” multisig. What is your strategy to find the right validators? Will there be any form of “slashing” of validators for malicious behaviour?

> The proof is only considered valid when more than ⅔ of the current number of validators have signed it. On the Ethereum side, the list of validators is stored and continually updated to mirror Incognito’s.

Have you explored schemes where the correctness of state transitions of the side-chain is validated on Ethereum?

In any case - cool project! Everything that helps to bring privacy to Ethereum is very welcome and much needed!

---

**duy** (2019-10-06):

**What is your strategy to find the right validators?**

On Incognito, validators are chosen using PoS (the stake is in the native coin ‘PRV’). Validators are randomly shuffled every epoch (approx every few hours) to prevent collusion. These validators are authorized to sign a proof to bring the asset back to Ethereum when an equivalent amount has been burned on Incognito.

**Will there be any form of “slashing” of validators for malicious behaviour?**

Once a validator produces a burn proof, that proof will be included in a block and verified by the other validators in a committee. If a burn proof is rejected by the committee and deemed malicious, it will not be included in a finalized block. We’re currently considering a reasonable slashing mechanism in the event of malicious behavior, to be implemented probably in the next milestone.

**Have you explored schemes where the correctness of state transitions of the side-chain is validated on Ethereum?**

This is pretty similar to the “unlocking” scheme mentioned above. Once a new list of validators is proposed, validators in the current committee will sign on a “SwapConfirm” proof (this process happens periodically). The signed proof will be submitted to and verified by the Ethereum smart contract. The contract always holds a list of the last committee’s public keys, so it’s easy to validate the correctness of state transitions and make sure its committee is up to date with Incognito’s.

Our team is at Devcon.  Happy to chat more about the bridge as well as use cases of privacy tokens.

---

**raullenchai** (2019-10-09):

If Ethereum will be supporting “incognito mode” (e.g., aztec, zk rollup), it is less valuable to have a zk-enabled side chain, as it is less secure, carries less assets, and thus offers a lower degree of privacy.

---

**Boogaav** (2019-11-19):

I agree with your comment, but what about the network speed. Will the zkp implementation for ethereum slow down the network?

---

**stvenyin** (2019-11-23):

Martel tree like Bitcoin?

---

**Boogaav** (2019-11-27):

Hi, [@stvenyin](/u/stvenyin) haven’t got to which comment do you argue?)

---

**Boogaav** (2020-01-21):

Hi Everyone!

I would like just highlight that trust-less bridge to Ethereum is live and you send ETH and ERC20 assets privately.

Please try it out and share your feedback!

on [iOS](https://apps.apple.com/us/app/incognito-crypto-wallet/id1475631606?ls=1)

on [Android](https://play.google.com/store/apps/details?id=com.incognito.wallet)

---

**hadv** (2020-02-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/duy/48/4029_2.png) duy:

> The contract always holds a list of the last committee’s public keys

Hi, Can you explain how an Ethereum contract can do this properly?

---

**duy** (2020-02-03):

hi [@hadv](/u/hadv)!  here is the smart contract that handles committee updates.  let me know if you have any questions.  happy to jump on a video call or telegram chat to discuss in depth about the implementation too (not sure if ethresear.ch is the best place to discuss about implementation).  my email is [duy@incognito.org](mailto:duy@incognito.org) and my telegram is [t.me/duy_incognito](http://t.me/duy_incognito)


      [github.com](https://github.com/incognitochain/bridge-eth/blob/c4cbe29927f850f6cfaf478636b5f87300b61a67/bridge/contracts/incognito_proxy.sol)




####

```sol
pragma solidity ^0.5.12;
pragma experimental ABIEncoderV2;

import "./pause.sol";

/**
 * @dev Stores beacon and bridge committee members of Incognito Chain. Other
 * contracts can query this contract to check if an instruction is confimed on
 * Incognito
 */
contract IncognitoProxy is AdminPausable {
    struct Committee {
        address[] pubkeys; // ETH address of all members
        uint startBlock; // The block that the committee starts to work on
    }

    Committee[] public beaconCommittees; // All beacon committees from genesis block
    Committee[] public bridgeCommittees; // All bridge committees from genesis block

    event BeaconCommitteeSwapped(uint id, uint startHeight);
```

  This file has been truncated. [show original](https://github.com/incognitochain/bridge-eth/blob/c4cbe29927f850f6cfaf478636b5f87300b61a67/bridge/contracts/incognito_proxy.sol)

---

**hadv** (2020-03-12):

So we need to call contract frequency to update the latest committees, right?

---

**duy** (2020-05-13):

hey [@hadv](/u/hadv).  yes, the current committees on incognito sign & send the list of new committees to the smart contract every incognito epoch, which is about 400 blocks or ~4.5 hours.

the incognito-ethereum bridge v1 has been live since november 2019.  it has shielded over $2M worth of ETH and ERC20 tokens.  i would say it’s pretty solid and battle-tested at this point.  we’re working on incognito-ethereum bridge v2.


      ![](https://ethresear.ch/uploads/default/original/3X/2/5/253ec4e4ced1d3a5cbd3877b14bcd67a25af1e02.png)

      [Ethereum (ETH) Blockchain Explorer](https://etherscan.io/address/0x0261DB5AfF8E5eC99fBc8FBBA5D4B9f8EcD44ec7#analytics)



    ![](https://ethresear.ch/uploads/default/original/3X/4/1/412acb513cfbcd882b60edb4cbc87bfa6da7f5c7.jpeg)

###



Contract: Unverified | Balance: $0 across 0 Chain | Transactions: 6,435 | As at Dec-29-2025 02:11:35 PM (UTC)










[![image](https://ethresear.ch/uploads/default/optimized/2X/c/c640abf5134ed88f14b857831820bc62b9a02798_2_561x500.png)image2288×2038 369 KB](https://ethresear.ch/uploads/default/c640abf5134ed88f14b857831820bc62b9a02798)

---

**Boogaav** (2020-06-11):

Hey guys !

### FYI: The bridge was upgraded and migrated to a

---

**Boogaav** (2020-07-01):

Hey guys! Happy to share our latest achievements ![:raised_hands:](https://ethresear.ch/images/emoji/facebook_messenger/raised_hands.png?v=14)

Yesterday we released Incognito mode for Kyber Network (on mainnet) Thanks [@duy](/u/duy) & [@loiluu](/u/loiluu) for support ![:pray:](https://ethresear.ch/images/emoji/facebook_messenger/pray.png?v=14)

![kyber](https://ethresear.ch/uploads/default/original/2X/f/f9c84644c295366ee85392c718599d92b24cd59b.gif)

## Privacy for smart-contracts

Earlier this spring we’ve shared research about how [privacy for smart-contracts](https://ethresear.ch/t/pethereum-privacy-mode-for-smart-contracts-integration-with-defi/7336) works.

[Find how to trade anonymously on Kyber →](https://incognito.org/t/how-to-trade-anonymously-on-kyber/3605)

---

---

**Boogaav** (2020-12-12):

Hey guys! Haven’t shared updates for a while, one more Dapp went Incognito. For this integration we also utilized [pEthereum](https://ethresear.ch/t/pethereum-privacy-mode-for-smart-contracts-integration-with-defi/7336) Implementation.

**Announce**


      ![](https://ethresear.ch/uploads/default/original/3X/b/6/b6ba9d8863576a45f3d5bf9632d1d49b46e36986.svg)

      [Uniswap Governance – 10 Dec 20](https://gov.uniswap.org/t/incognito-mode-for-uniswap/9220)



    ![image](https://ethresear.ch/uploads/default/optimized/2X/e/e85c6dbc04fac3ed5e01d100e47eb855e8f9d8c5_2_690x384.png)



###



Hey guys! Andrey is here 👋 👋  This summer we started work on bringing a privacy layer to Uniswap, and I am happy to share that it went live today.     With this implementation, you will be able to trade against any Uniswap pool, remain your...



    Reading time: 2 mins 🕑
      Likes: 21 ❤











**Tutorial**

https://we.incognito.org/t/how-to-trade-anonymously-with-puniswap/8259

Looking forward for your feedback.

