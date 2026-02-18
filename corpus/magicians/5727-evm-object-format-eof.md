---
source: magicians
topic_id: 5727
title: EVM Object Format (EOF)
author: axic
date: "2021-03-16"
category: EIPs
tags: [evm, core-eips, shanghai-candidate, evm-object-format, cancun-candidate]
url: https://ethereum-magicians.org/t/evm-object-format-eof/5727
views: 73883
likes: 76
posts_count: 136
---

# EVM Object Format (EOF)

Last week I have shared a document on the Eth R&D discord explaining some background on why some EVM changes are hard and motivation for improving the situation:


      ![](https://ethereum-magicians.org/uploads/default/original/2X/5/50c8596d557541aeba2b4e2c4be22d9542e8c360.png)

      [HackMD](https://notes.ethereum.org/@axic/evm-object-format)



    ![](https://ethereum-magicians.org/uploads/default/original/1X/fbd15b64d2d2a97a7802df3537bf0c034cd319fa.png)

###



# EVM encapsulation format  > Name suggestion: *EOF – EVM Object Format* > Or could go the GNU way:










It also suggests a container format for EVM, which would enable further improvements, such as removing jumpdests, moving to static jumps, etc. While the document does not aim to provide a final, implementable solution, it is a good one for discussions.

## Replies

**axic** (2021-03-16):

[@chriseth](/u/chriseth) published his initial opinion here:


      ![](https://ethereum-magicians.org/uploads/default/original/2X/5/50c8596d557541aeba2b4e2c4be22d9542e8c360.png)

      [notes.ethereum.org](https://notes.ethereum.org/BgA648JCQ6uVHPUVFrLzkQ)



    ![](https://notes.ethereum.org/images/media/HackMD-og.jpg)

###

---

**axic** (2021-03-16):

And with [@chfast](/u/chfast) and [@gumb0](/u/gumb0) we have looked into some other potential changes this could bring in the long term:


      ![](https://ethereum-magicians.org/uploads/default/original/2X/5/50c8596d557541aeba2b4e2c4be22d9542e8c360.png)

      [notes.ethereum.org](https://notes.ethereum.org/t-1tLFnLSKCtLZpb-Rw0IA?view)



    ![](https://notes.ethereum.org/images/media/HackMD-og.jpg)

###

---

**MicahZoltu** (2021-04-30):

Can we change this EIP to just say any contract deployment that has an unused opcode as the first byte is invalid and should revert?  Rather than just have a single opcode that is considered invalid?  There is no good reason to start a contract with an unused opcode, and maybe we’ll want the others later.

---

**chfast** (2021-04-30):

This is technically possible, but this would block much bigger set of “data contracts” from being deployed, therefore there would be bigger chance to break some existing factory contracts.

Data contracts are deployed bytecodes with no intention for execution from which you can read data with `EXTCODECOPY`.

On the other hand, this increases our chance to have shorter EOF prefix.

Some middle ground would be to reject some fixed range based on the analysis of currently deployed contracts. E.g. `D0-EF`.

---

**MicahZoltu** (2021-05-01):

I wonder if we should enshrine data contracts somehow?  Maybe have a contract prefix specifically for them?

---

**jochem-brouwer** (2021-05-02):

If we disallow contracts starting with 0xEF then I’d say we should also explicitly mark 0xEF as an INVALID opcode (or alternatively if we want to use 0xEF at some point it should use  >=1 stack items), otherwise we get these weird situations that contracts want to start using this opcode but have to push a dummy item to stack first.

I am assuming that this only disallows the code deposit starting with 0xEF, we could technically still try to CREATE a contract where the deploycode starts with 0xEF? (Just for clarification here)

---

**axic** (2021-05-03):

I see a much bigger risk of this change not making into London if the range is extended. I think it has merits to reject any contract with invalid starting byte, but perhaps that can be done separately and even after London.

---

**axic** (2021-05-13):

The first step towards this is defined under EIP-3541:


      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-3541)




###

Details on Ethereum Improvement Proposal 3541 (EIP-3541): Reject new contracts starting with the 0xEF byte








It is also considered for the upcoming London fork.

---

**Vie** (2021-05-21):

So, when we try to add TokenA and TokenB to uniswap v2, we maybe got error as `create2` create a pair start with `0xEF`?

---

**axic** (2021-05-21):

No working contract starts with `0xEF`.

---

**Vie** (2021-05-27):

Ok, I’ll try to fix out that.

---

**axic** (2021-06-09):

This first step has been accepted for London.

The next step was proposed for Shanghai:


      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-3540)




###

Details on Ethereum Improvement Proposal 3540 (EIP-3540): EVM Object Format (EOF) v1








This introduces code - data separation as the main tangible benefit to users.

---

**poojaranjan** (2021-06-15):

Watch an overview of EIP-3540 & EIP-3541 by [@axic](/u/axic) [@chfast](/u/chfast) [@gumb0](/u/gumb0).

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/b/b649855f9ffb85743ae025f127d357ecdd2993dc.jpeg)](https://www.youtube.com/watch?v=E02THhW-yTE)

---

**axic** (2021-06-16):

There is also a new overview document here:


      ![](https://ethereum-magicians.org/uploads/default/original/2X/5/50c8596d557541aeba2b4e2c4be22d9542e8c360.png)

      [HackMD](https://notes.ethereum.org/@ipsilon/evm-object-format-overview)



    ![](https://storage.googleapis.com/ethereum-hackmd/upload_8ad7ca0c0d66a0b3b53f0a45f1b9d2a0.jpg)

###



# Everything about the EVM Object Format (EOF)  The aim of this document is to serve as an explainer










This gives an explanation of why two hard forks, gives a roadmap of different features we investigate (Shanghai, Cancun, and beyond), and links to all relevant resources.

(We plan to drop the two-hard fork explainer from EIP-3540 to simplify it.)

---

**axic** (2021-07-20):

As a further step, we suggest to introduce code validation with EOF: [EIP-3670: EOF - Code Validation](https://ethereum-magicians.org/t/eip-3670-eof-code-validation/6693)

It is proposed as a separate EIP to keep concerns separated and the EIPs shorter.

---

**axic** (2021-08-07):

A potential way to remove the need for jumpdest analysis at execution time was published here: [EIP-3690: EOF - JUMPDEST Table](https://ethereum-magicians.org/t/eip-3690-eof-jumpdest-table/6806)

---

**axic** (2021-09-23):

A proposal made possible by EOF is to have static jumps:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png)
    [EIP-4200: Static relative jumps](https://ethereum-magicians.org/t/eip-4200-static-relative-jumps/7108) [Core EIPs](/c/eips/core-eips/35)



> This is the discussion topic for
>
> This proposal started as a comment back in February and was one of the reasons which kicked off our journey with EVM Object Format (EOF). In the past few months @gumb0 has been working on experimenting and validating this in evmone (PR here), but now is the time to release an actual EIP.

---

**chfast** (2021-10-23):

After the London upgrade which included EIP-3541 we were able to collect all previously deployed bytecodes starting with the `0xEF` byte. The following document has information about collected data and 2 possible EOF prefix values. We recommend the use `0xEF00` 2-byte prefix.

[EOF Prefix Selection](https://notes.ethereum.org/@ipsilon/eof-prefix-selection)

---

**MicahZoltu** (2021-10-24):

Has anyone looked into figuring out what https://etherscan.io/address/0xca7bf67ab492b49806e24b6e2e4ec105183caa01 does?

Given that there are only 3 contracts that start with `0xEF` and two of them have (in theory) reachable owners/authors and the third doesn’t actually *do* anything, I think we should explore the option of an irregular state change to get rid of them so we have a completely clear 0xEF space.

This is especially true since all 3 of them were created after EIP-3541 was proposed, and I suspect at least two of them (the contracts that merely deployed 0xEF) were created explicitly to cause problems for us (the third possibly as well, but that one is slightly less clear).

---

**axic** (2021-10-24):

I asked about the long contract here: https://twitter.com/alexberegszaszi/status/1452210984987369474

Writing an EIP for the irregular state change is easy enough, ACD may or may accept it, but it definitely is yet another hurdle to overcome.

I’d be happy if we could get rid of those three contracts, if someone champions that change.


*(115 more replies not shown)*
