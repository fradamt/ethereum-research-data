---
source: magicians
topic_id: 8713
title: "EIP-4760: Selfdestruct bomb"
author: dankrad
date: "2022-03-25"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-4760-selfdestruct-bomb/8713
views: 2323
likes: 2
posts_count: 4
---

# EIP-4760: Selfdestruct bomb

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/4760)














####


      `master` ← `dankrad:selfdestruct-bomb`




          opened 08:47PM - 03 Feb 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/c/cc63c5d10a473c2079ea4ee24ce896c0942d6825.jpeg)
            dankrad](https://github.com/dankrad)



          [+63
            -0](https://github.com/ethereum/EIPs/pull/4760/files)







Deactivate SELFDESTRUCT by changing it to SENDALL, which does recover all funds […](https://github.com/ethereum/EIPs/pull/4760)to the caller but does not delete any contract code or storage. In order to give applications good time to switch to new constructions, do this via a stage of exponential gas cost increases.












For discussing the merits of deactivating `SELFDESTRUCT` in general, I suggest using the thread for [EIP-4758: Deactivate selfdestruct](https://ethereum-magicians.org/t/eip-4758-deactivate-selfdestruct/8710/2). This thread should be used only for discussing the advantages/disadvantages of preceding this with an exponential gas schedule as a warning to Dapps.

## Replies

**xinbenlv** (2022-11-30):

Hi [@dankrad](/u/dankrad) , great EIP. I support your idea for increasing the gas cost as a way to warn developer until finally change the functionality from SELFDESTRUCT to SENDALL.

I have a design question: do you have any preference *if* these smart contract holds ERC20s, ERC721 or other type of contract-based tokens other than just `ethers`?

Context: the only relevant text about this question lies in :

> Security section: 1. Any use where SELFDESTRUCT is used to burn non-ETH token balances, such as ERC20, inside a contract. We do not know of any such use (since it can easily be done by sending to a burn address this seems an unlikely way to use SELFDESTRUCT)

---

**Joe** (2022-11-30):

Just wonder if it’s deactivated for now? Coz I found out it’s currently programmed in draft status ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12)



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-4760)





###



Deactivate SELFDESTRUCT by changing it to SENDALL and stage this via a stage of exponential gas cost increases.

---

**fulldecent** (2022-12-20):

Spells are one use case of a smart contract design pattern that could be affected by this EIP.

Documenting here so that anybody looking to study on-chain usage of `SELFDESTRUCT` and the like can know about it.

Spells are where you deploy a zero-code ephemeral smart contract, possibly ending with a `SELFDESTRUCT` at the end. All the effect of the spell is in the “constructor” if you’re using a higher level language. Spells can be useful for all types of hacks, such as running a +EV sandwich, minting 100 NFTs in a for-loop against a contract that is expecting one-per-person, stuff with Aave, working with dangerous contracts like potential honeypots. Maybe others know of more mainstream applications and this approach is well documented in Solidity tutorials.

