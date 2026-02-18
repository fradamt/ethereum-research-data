---
source: magicians
topic_id: 18946
title: "EIP-7637: EXTCODEHASH optimize"
author: ZWJKFLC
date: "2024-02-26"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7637-extcodehash-optimize/18946
views: 653
likes: 0
posts_count: 2
---

# EIP-7637: EXTCODEHASH optimize

Discussion for [Add EIP: EXTCODEHASH optimize by ZWJKFLC · Pull Request #8261 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8261/files)

`EIP-1052` was proposed to save gas fees.

In order to include the role of `BALANCE`, let the codehash of the address without balance be 0x, and the codehash of the address with balance be hash(0x).

The contract address can be calculated in advance. Whether it is create or create2, it is possible that the contract is not created but has a balance. For security, you can actually only use keccak256(add.code) == keccak256(bytes(" ")) instead of add.codehash == 0, which makes the original intention of EIP-1052 meaningless.

For example, uniswap V2 uses stored addresses to determine whether a contract exists. If this `EXTCODEHASH` is optimized, can save a huge amount of gas.

If someone uses a codehash of 0x to determine whether a contract has been created, due to intuition and the lack of details in many documents, they will not think that the codehash of an address with a balance will change from 0x to hash (0x). If someone maliciously attacks at this time, it will cause some bad effects.

## Replies

**ZWJKFLC** (2024-02-27):

I have re edited the questions, simplified and organized the main ones.

Just to determine whether an address is a contract, whether it has eth or not, the general method is

```auto
keccak256(add.code) == keccak256(bytes(" "));
add.code.length ==0;
```

When the code is very long, the gas will be very high. To save gas, codehash should be used

```auto
add.codehash == 0;
```

But when I specifically use and understand codehash, An address is not a contract. When there is no eth, the codehash is 0x. An address is not a contract. When there is eth, the codehash is keccak256(bytes(" ")).

```auto
add.code=0;
add.codehash =！ 0;
add.codehash ==keccak256(bytes(" "));
```

In actual applications, the contract has not been created yet, but it is normal to have eth. Therefore, for the sake of security, codehash is not used in the end, but other methods are used. It completely deviates from the original intention of [eip-1052](https://eips.ethereum.org/EIPS/eip-1052) to save gas, making EXTCODEHASH a bit meaningless.

