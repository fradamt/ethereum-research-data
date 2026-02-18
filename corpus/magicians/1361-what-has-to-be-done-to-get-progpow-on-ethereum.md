---
source: magicians
topic_id: 1361
title: What has to be done to get ProgPoW on Ethereum
author: chfast
date: "2018-09-17"
category: EIPs
tags: [progpow, pow]
url: https://ethereum-magicians.org/t/what-has-to-be-done-to-get-progpow-on-ethereum/1361
views: 4324
likes: 4
posts_count: 11
---

# What has to be done to get ProgPoW on Ethereum

1. The ProgPoW OpenCL and CUDA implementations have to be integrated to ethminer as the second PoW algorithm next to Ethash.
2. One of the stratum protocols must be modified to include information about the mining algorithm. I believe that fixing the block number when the switch will happen is too risky, especially when the mining workers do not receive the block number, just the epoch seed hash.
For that I propose  modifying the EthereumStratum by NiceHash. I think the new spec deserves a separate EIP.
3. Also the “getWork” JSON-RPC based protocol should be modified to include the information about algorithm. This is the language (sometimes the only one) many Ethereum clients speak.
4. The ProgPoW verification code must be added to many libraries, including:

GitHub - chfast/ethash: C/C++ implementation of Ethash and ProgPoW – the Ethereum Proof of Work algorithms
5. GitHub - ethereum/ethash
6. go-ethereum/consensus/ethash at master · ethereum/go-ethereum · GitHub.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/eosclassic/48/566_2.png) eosclassic:

> ProgPOW stratum and getWork implementation must be implemented to one of the following open source mining pool implementation
>
>
> GitHub - sammy007/open-ethereum-pool: Open Ethereum Mining Pool
> GitHub - ocminer/ethcore-pool-mpos: ethereum getwork proxy written in go for mpos pools

## Replies

**Anlan** (2018-09-17):

About point 2 the fixing of block number is not only “risky” … it’s impossibile.

ethminer is an ETHASH miner thus allowing mining on any “Ethereum like” chain (ETC, ELLAISM, PIRL etc).

Only options are

- either integrate the work notification payload with the required algo (on the fly switch)
- or provide ethminer with a new cli argument to start mining on specific algo (cold switch)

---

**chfast** (2018-09-17):

Yes, I had some kind of “cold switch” in mind. E.g. `ethminer --progpow-from-block 9000000` or `ethminer --ethereum-mainnet`.

But it still looks much more messy that receiving this information from a pool.

Besides, having a stratum protocol capable of switching algorithms is not bad by itself.

I mostly wander how chains like Monero or Bitcoin Interest did this.

---

**Anlan** (2018-09-17):

If mining NiceHash, unless they provide a specific port for ProgPow, it’s mandatory to have algo signalled in stratum notification.

---

**eosclassic** (2018-09-18):

1. ProgPOW stratum and getWork implementation must be implemented to one of the following open source mining pool implementation

- GitHub - sammy007/open-ethereum-pool: Open Ethereum Mining Pool
- GitHub - ocminer/ethcore-pool-mpos: ethereum getwork proxy written in go for mpos pools

And yes I think merging different stratum specification into 1 will be a good idea ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=9)

---

**atlanticcrypto** (2018-09-21):

Bitcoin Interest brought the entire network down for almost a day.

This sounds like a miserable idea, but would it be possible/how hard would it be to have a window of 5,000 blocks where both algos were in effect - so the network could slowly transition instead of a simple drop dead point for the algo.

Regarding the open source pool code, I have had the OEP software developer do custom builds for us in the past (including the recent Parity rpc convention change). As soon as there is a spec, we can work with him on implementing it.

---

**cosminstefane** (2018-09-30):

If you guys need different hardware to test, let me know and I can provide.

---

**HiddeHoogland** (2018-09-30):

Where can we actively follow the improvements being made? There is a big chunk of the mining community dependent on this progress. Please inform me/us.

---

**MariusVanDerWijden** (2018-11-16):

Hello everyone,

I’ve finished writing the official specification for ProgPoW.

It is still not peer-reviewed, so we need a bit more time until its finished.

The specification can act as a starting point for core developers to implement ProgPoW for their respective client.

Feedback would be appreciated!

greetings, Marius


      [github.com](https://github.com/MariusVanDerWijden/progpowWiki/blob/master/ProgPoW.md)




####

```md

**Contents**

- [Definitions](#definitions)
    - [A note regarding "SHA3" hashes described in this specification](#a-note-regarding-sha3-hashes-described-in-this-specification)
- [Parameters](#parameters)
- [Cache Generation](#cache-generation)
- [Data aggregation function](#data-aggregation-function)
- [Full dataset calculation](#full-dataset-calculation)
- [Main Loop](#main-loop)
- [Mining](#mining)
- [Defining the Seed Hash](#defining-the-seed-hash)
- [Appendix](#appendix)
- [Data Sizes](#data-sizes)

**This spec is REVISION 1. Whenever you substantively (ie. not clarifications) update the algorithm, please update the revision number in this sentence. Also, in all implementations please include a spec revision number**

```

  This file has been truncated. [show original](https://github.com/MariusVanDerWijden/progpowWiki/blob/master/ProgPoW.md)

---

**ajsutton** (2018-11-20):

Hi Marius,

The spec doesn’t clearly state the license it and the code it includes is under.  It would be really useful to explicitly state that and ensure that the license is very permissive - EIPs typically use CC0 which would be ideal.

Thanks,

Adrian.

---

**AltcoinXP-Anthony** (2020-02-24):

What needs to be done as of today? Do all the needed clients have working implementations so that a ProgPoW hard fork can happen today?

