---
source: magicians
topic_id: 12621
title: "EIP-6357: Single-contract Multi-delegatecall"
author: Pandapip1
date: "2023-01-18"
category: EIPs
tags: [erc, multisend]
url: https://ethereum-magicians.org/t/eip-6357-single-contract-multi-delegatecall/12621
views: 2380
likes: 3
posts_count: 12
---

# EIP-6357: Single-contract Multi-delegatecall

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/6357)














####


      `master` ← `Pandapip1-eip-multicall`




          opened 08:29PM - 18 Jan 23 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/9/9a6e3ca9c5b562ad2b1d66235080626414ed5f18.png)
            Pandapip1](https://github.com/Pandapip1)



          [+79
            -0](https://github.com/ethereum/EIPs/pull/6357/files)







It's remarkable what you can find in OpenZeppelin that should really be standard[…](https://github.com/ethereum/EIPs/pull/6357)ized.

## Replies

**horsefacts** (2023-01-20):

Should this interface also include EIP-165 interface detection?

---

**merkleplant** (2023-01-20):

There are also improved versions of the original `Multicall` contract, most notably the backward-compatible [Multicall3](https://github.com/mds1/multicall#multicall3-contract-addresses) contract from [Matt Solomon](https://github.com/mds1) which was also recently [added](https://github.com/foundry-rs/forge-std/pull/271) to the `forge-std` library.

Is there any reason for not using the optimized `Multicall3` version in the EIP?

---

**horsefacts** (2023-01-20):

`Multicall3` and predecessors batch [external](https://github.com/mds1/multicall/blob/eb34ad2954f9ceb475a24bb0155bff3bef0f5409/src/Multicall3.sol#L67) `call`s to arbitrary addresses (i.e. many calls to many different contracts), while this multicall variant [batches](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.8.1/contracts/utils/Multicall.sol#L20) `delegatecall`s to `address(this)` (i.e. many calls only to one contract).

The OZ contract is called [Multicall](https://docs.openzeppelin.com/contracts/4.x/api/utils#Multicall), but I’ve also seen this version called “Multi delegatecall” [before](https://solidity-by-example.org/app/multi-delegatecall/), which might be a clearer name.

---

**Pandapip1** (2023-01-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/horsefacts/48/8269_2.png) horsefacts:

> The OZ contract is called Multicall, but I’ve also seen this version called “Multi delegatecall” before, which might be a clearer name.

I’ll consider this. It does describe this better.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/merkleplant/48/5188_2.png) merkleplant:

> There are also improved versions of the original Multicall contract, most notably the backward-compatible Multicall3  contract from Matt Solomon which was also recently added to the forge-std library.

These multicalls serve different purposes. See the above comment by @hosefacts (well-explained, thanks!):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/horsefacts/48/8269_2.png) horsefacts:

> Multicall3 and predecessors batch external  calls to arbitrary addresses (i.e. many calls to many different contracts), while this multicall variant batches delegatecalls to address(this) (i.e. many calls only to one contract).

---

**Pandapip1** (2023-01-23):

A question I had: Should the function be payable, and an option be added to allow the splitting of msg.value?

- Non-payable
- Payable
- Both, with the payable one being optional

0
voters

---

**markuswaas** (2023-01-24):

Is there already an EIP for the multicall with `.call` ?

---

**horsefacts** (2023-01-24):

I voted “non-payable.” [delegatecall](https://www.evm.codes/?fork=arrowGlacier) doesn’t accept a `value`, so unfortunately it’s not possible to split up `msg.value` the way I think you’re suggesting. (It would be nice if it were possible, though!) Instead, each `delegatecall` will inherit the same `msg.value` as the top level external call. As smarter people than I have discovered, that’s [seriously](https://github.com/Uniswap/v3-periphery/issues/52) [dangerous](https://www.paradigm.xyz/2021/08/two-rights-might-make-a-wrong#the-discovery).

It might be helpful to seek some feedback from the OZ team—I suspect they’ve thought about this in depth and might have suggestions.

---

**Pandapip1** (2023-01-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/horsefacts/48/8269_2.png) horsefacts:

> unfortunately it’s not possible to split up msg.value the way I think you’re suggesting.

I meant treating it as if msg.value were split up in that way (similar to how EIP-2771 treats msg.sender as not coming from the actual msg.sender)

---

**Pandapip1** (2023-01-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/markuswaas/48/5630_2.png) markuswaas:

> Is there already an EIP for the multicall with .call ?

I don’t think so. Please prove me wrong!

---

**xinbenlv** (2023-02-23):

Cool

Also just FYI this proposal could include multicall, [ERC-5247: Smart Contract Executable Proposal Interface](https://eips.ethereum.org/EIPS/eip-5247)

love to collaborate

---

**Pandapip1** (2023-02-23):

Sure thing! Do you have any suggestions to improve the pre-draft as-is?

